from __future__ import annotations

import streamlit as st

from src.llm_service import OllamaService
from src.model_artifacts import build_model_metadata
from src.config import SENSITIVE_COLUMNS
from src.ui_components import bullet_card, info_card, notice, page_header, section_header


def render_responsible_ai_page(df, schema: dict[str, str | None], dataset, ai_context: dict) -> None:
    model_metadata = build_model_metadata()
    llm_ok, llm_message = OllamaService().health_check()
    page_header(
        "Responsible AI and Transparency",
        "A readable view of the real predictive model integration, explainability source, local LLM role, and safeguards expected around sensitive HR data.",
        eyebrow="Trust and governance",
        badges=[("Responsible use", "demo"), ("Human review required", "warn")],
        aside_title="What this page answers",
        aside_body="What the tool does, what it does not do, and why the output should remain auditable and review-based.",
    )

    overview_left, overview_right = st.columns(2)
    with overview_left:
        info_card(
            "What the tool does",
            "It helps HR teams review retention patterns, detect plausible warning signals, and organize preventive follow-up.",
        )
        info_card(
            "What the tool does not do",
            "It does not automate promotions, compensation changes, sanctions, or termination decisions.",
        )
        info_card(
            "Model integration",
            "The app uses exported outputs from the frugal Random Forest model and its SHAP explanations when those artifacts are available.",
        )
    with overview_right:
        info_card(
            "Explainability",
            "Employee-level factor views are grounded in exported SHAP impacts from the trained frugal model.",
        )
        info_card(
            "Frugality",
            f"The predictive core is a 10-feature frugal model ({model_metadata['model_name']}) documented in the project notebook.",
        )
        info_card(
            "Local LLM role",
            "Ollama is used only for wording, summaries, talking points, and recommendation phrasing. It does not generate the risk score.",
        )

    st.markdown("<div class='tg-hr'></div>", unsafe_allow_html=True)
    section_header(
        "Sensitive data and audit perspective",
        "Sensitive fields may exist in the dataset, but they should be treated as governance signals, not direct decision levers.",
    )
    sensitive_present = [column for column in SENSITIVE_COLUMNS if column in df.columns]

    if sensitive_present:
        notice(
            "Sensitive variables detected",
            "Sensitive variables should be reviewed for fairness, audit, and governance purposes. They should not be used directly to recommend individual actions without proper assessment.",
            tone="warning",
        )
        bullet_card("Detected sensitive columns", sensitive_present)
    else:
        notice(
            "No predefined sensitive columns detected",
            "The current dataset does not expose the predefined sensitive fields tracked by the transparency page.",
            tone="info",
        )

    principles_col, status_col = st.columns(2)
    with principles_col:
        section_header(
            "Responsible use statements",
            "These principles should remain visible in any demo, review meeting, or future production rollout.",
        )
        bullet_card(
            "Core statements",
            [
                "The results displayed are intended as decision-support only.",
                "Predictive scores come from the real frugal model when exported artifacts are available.",
                "Local LLM assistance is limited to narrative transformation and wording.",
                "Sensitive variables should not be used directly to recommend individual actions without audit.",
                "No HR decision should be made automatically based only on this tool.",
                "The system prioritizes lightweight and interpretable approaches.",
            ],
        )

    with status_col:
        section_header("Integration status", "Current pipeline state and what it means for trust in the displayed outputs.")
        if ai_context["mode"] in {"real", "hybrid"}:
            component_lines = ai_context.get("components", {})
            notice(
                "External AI outputs detected",
                (
                    f"The application detected the following external files: {', '.join(ai_context['available_files']) or 'metadata only'}. "
                    f"Current component status - risk scores: {component_lines.get('risk_scores', 'unknown')}, "
                    f"explanations: {component_lines.get('explanations', 'unknown')}, "
                    f"recommendations: {component_lines.get('recommendations', 'unknown')}."
                ),
                tone="info",
            )
        else:
            notice(
                "Fallback demo logic active",
                "No exported model artifacts were detected. Risk, explanations, and recommendations currently rely on transparent fallback logic.",
                tone="warning",
            )
        info_card(
            "Data protection reminder",
            "Only the minimum necessary data should be exposed in business workflows, and access should stay aligned with HR governance rules.",
        )
        notice(
            "Local Ollama status",
            llm_message if llm_ok else f"LLM-assisted sections will stay disabled. {llm_message}",
            tone="info" if llm_ok else "warning",
        )
