from __future__ import annotations

import json
import logging
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from functools import lru_cache


logger = logging.getLogger(__name__)


def _env_flag(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class OllamaConfig:
    enabled: bool = _env_flag("OLLAMA_ENABLED", True)
    base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model: str = os.getenv("OLLAMA_MODEL", "qwen3:8b")
    timeout_seconds: int = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "25"))
    keep_alive: str = os.getenv("OLLAMA_KEEP_ALIVE", "10m")
    num_predict: int = int(os.getenv("OLLAMA_NUM_PREDICT", "120"))
    temperature: float = float(os.getenv("OLLAMA_TEMPERATURE", "0.2"))


def _truncate_text(value: str, limit: int = 180) -> str:
    text = str(value or "").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


class OllamaService:
    def __init__(self, config: OllamaConfig | None = None) -> None:
        self.config = config or OllamaConfig()

    def health_check(self) -> tuple[bool, str]:
        if not self.config.enabled:
            return False, "LLM assistance disabled by configuration."

        request = urllib.request.Request(f"{self.config.base_url}/api/tags", method="GET")
        try:
            with urllib.request.urlopen(request, timeout=min(self.config.timeout_seconds, 4)) as response:
                if 200 <= response.status < 300:
                    return True, f"Ollama reachable with model target {self.config.model}."
        except urllib.error.URLError as exc:
            return False, f"Local Ollama service not reachable: {exc.reason}."
        except Exception as exc:  # pragma: no cover
            return False, f"Local Ollama health check failed: {exc}."
        return False, "Unexpected Ollama response."

    def _build_prompt(self, payload: dict) -> str:
        compact_payload = {
            "employee_id": payload.get("employee_id"),
            "employee": payload.get("employee"),
            "department": payload.get("department"),
            "position": payload.get("position"),
            "risk_score": payload.get("risk_score"),
            "risk_level": payload.get("risk_level"),
            "top_factors": payload.get("top_factors", [])[:3],
            "text_insight": _truncate_text(payload.get("text_insight", "")),
            "allowed_actions": payload.get("allowed_actions", [])[:4],
        }
        return (
            "Rewrite the supplied HR evidence into concise professional English.\n"
            "Use only the evidence provided.\n"
            "Do not invent causes, scores, personal context, or actions beyond the evidence.\n"
            "Return strict JSON with keys: summary, actions, manager_talking_points.\n"
            "Each array must contain at most 3 short strings.\n"
            f"Evidence: {json.dumps(compact_payload, ensure_ascii=True)}"
        )

    def generate_employee_brief(self, payload: dict, timeout_seconds: int | None = None) -> dict:
        ok, message = self.health_check()
        if not ok:
            return {"available": False, "error": message, "diagnostics": {"health_check": message}}

        prompt = self._build_prompt(payload)
        body = json.dumps(
            {
                "model": self.config.model,
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "keep_alive": self.config.keep_alive,
                "think": False,
                "options": {
                    "temperature": self.config.temperature,
                    "num_predict": self.config.num_predict,
                },
            }
        ).encode("utf-8")

        request = urllib.request.Request(
            f"{self.config.base_url}/api/generate",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        started_at = time.perf_counter()
        try:
            with urllib.request.urlopen(request, timeout=timeout_seconds or self.config.timeout_seconds) as response:
                raw_response = json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            return {"available": False, "error": f"Local LLM service timeout or network error: {exc.reason}", "diagnostics": {"latency_seconds": round(time.perf_counter() - started_at, 3)}}
        except Exception as exc:  # pragma: no cover
            return {"available": False, "error": f"LLM generation failed: {exc}", "diagnostics": {"latency_seconds": round(time.perf_counter() - started_at, 3)}}

        latency_seconds = round(time.perf_counter() - started_at, 3)
        diagnostics = {
            "latency_seconds": latency_seconds,
            "total_duration_ms": round(raw_response.get("total_duration", 0) / 1_000_000, 2),
            "load_duration_ms": round(raw_response.get("load_duration", 0) / 1_000_000, 2),
            "prompt_eval_duration_ms": round(raw_response.get("prompt_eval_duration", 0) / 1_000_000, 2),
            "eval_duration_ms": round(raw_response.get("eval_duration", 0) / 1_000_000, 2),
            "model": self.config.model,
            "cache_hit": False,
        }

        try:
            model_output = json.loads(raw_response.get("response", "{}"))
        except json.JSONDecodeError:
            return {"available": False, "error": "LLM returned invalid JSON.", "diagnostics": diagnostics}

        result = {
            "available": True,
            "summary": str(model_output.get("summary", "")).strip(),
            "actions": [str(item).strip() for item in model_output.get("actions", []) if str(item).strip()][:3],
            "manager_talking_points": [str(item).strip() for item in model_output.get("manager_talking_points", []) if str(item).strip()][:3],
            "source": f"Local Ollama model: {self.config.model}",
            "diagnostics": diagnostics,
        }
        logger.info("Ollama generation completed in %.3fs for model %s", latency_seconds, self.config.model)
        return result


@lru_cache(maxsize=256)
def cached_generate_employee_brief(
    employee_id: str,
    model_version: str,
    explanation_version: str,
    llm_model_name: str,
    payload_json: str,
    timeout_seconds: int | None = None,
) -> dict:
    service = OllamaService(OllamaConfig(model=llm_model_name))
    result = service.generate_employee_brief(json.loads(payload_json), timeout_seconds=timeout_seconds)
    if result.get("diagnostics"):
        result["diagnostics"]["cache_hit"] = False
    return result


def generate_employee_brief_with_cache(
    employee_id: str,
    model_version: str,
    explanation_version: str,
    llm_model_name: str,
    payload_json: str,
    timeout_seconds: int | None = None,
) -> dict:
    before = cached_generate_employee_brief.cache_info()
    result = cached_generate_employee_brief(
        employee_id,
        model_version,
        explanation_version,
        llm_model_name,
        payload_json,
        timeout_seconds,
    )
    after = cached_generate_employee_brief.cache_info()
    response = dict(result)
    if response.get("diagnostics"):
        response["diagnostics"] = dict(response["diagnostics"])
        response["diagnostics"]["cache_hit"] = after.hits > before.hits
    return response
