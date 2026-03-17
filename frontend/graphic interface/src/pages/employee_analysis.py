from __future__ import annotations

import json

import pandas as pd
import streamlit as st

from src.config import OLLAMA_MODEL
from src.llm_service import generate_employee_brief_with_cache
from src.model_artifacts import build_model_metadata
from src.schema_utils import derive_tenure_years, normalize_text_value
from src.ui_components import (
    bullet_card,
    contribution_chart,
    empty_state,
    info_card,
    page_header,
    render_risk_badge,
    section_header,
)


def _employee_label(row: pd.Series, schema: dict[str, str | None]) -> str:
    name_col = schema.get("employee_name")
    id_col = schema.get("employee_id")
    name = normalize_text_value(row.get(name_col)) if name_col else "Employee"
    if id_col and pd.notna(row.get(id_col)):
        return f"{name} | {row[id_col]}"
    return name


def _summary_fields(row: pd.Series, schema: dict[str, str | None], tenure_years: pd.Series) -> list[tuple[str, str]]:
    salary_value = row.get(schema.get("salary")) if schema.get("salary") else pd.NA
    if pd.notna(salary_value):
        salary_text = f"${float(salary_value):,.0f}"
    else:
        salary_text = "Not available"

    tenure_value = tenure_years.loc[row.name]
    tenure_text = f"{tenure_value:.1f} years" if pd.notna(tenure_value) else "Not available"

    return [
        ("Identifier", normalize_text_value(row.get(schema.get("employee_id"))) if schema.get("employee_id") else "Not available"),
        ("Department", normalize_text_value(row.get(schema.get("department"))) if schema.get("department") else "Not available"),
        ("Position", normalize_text_value(row.get(schema.get("position"))) if schema.get("position") else "Not available"),
        ("Performance", normalize_text_value(row.get(schema.get("performance_score"))) if schema.get("performance_score") else "Not available"),
        ("Salary", salary_text),
        ("Manager", normalize_text_value(row.get(schema.get("manager"))) if schema.get("manager") else "Not available"),
        ("Employment status", normalize_text_value(row.get(schema.get("employment_status"))) if schema.get("employment_status") else "Not available"),
        ("Tenure", tenure_text),
    ]


def _employee_payload(row: pd.Series, schema: dict[str, str | None], explanations: list[dict], actions: list[str]) -> dict:
    def _value(field: str) -> str:
        column = schema.get(field)
        return normalize_text_value(row.get(column)) if column else "Not available"

    payload = {
        "employee": _value("employee_name"),
        "employee_id": _value("employee_id"),
        "department": _value("department"),
        "position": _value("position"),
        "risk_score": row.get("risk_score"),
        "risk_level": row.get("risk_level"),
        "top_factors": explanations[:5],
        "deterministic_actions": actions[:4],
        "manager": _value("manager"),
        "employment_status": _value("employment_status"),
    }
    for optional_column in ["Exit_Interview_Feedback", "Internal_Transfer_Request"]:
        if optional_column in row.index and pd.notna(row.get(optional_column)):
            payload["text_insight"] = str(row.get(optional_column))
    payload["allowed_actions"] = actions[:4]
    return payload


def render_employee_analysis_page(df: pd.DataFrame, schema: dict[str, str | None], dataset, ai_context: dict) -> None:
    model_metadata = build_model_metadata()
    page_header(
        "Employee Analysis",
        "Employee profile, risk evidence, and follow-up options.",
    )

    labels = [_employee_label(row, schema) for _, row in df.iterrows()]
    selected_label = st.selectbox("Select an employee", labels)
    selected_index = labels.index(selected_label)
    row = df.iloc[selected_index]
    tenure_years = derive_tenure_years(df, schema)
    initial_actions = row.get("recommended_actions", [])
    if isinstance(initial_actions, str):
        initial_actions = [initial_actions]
    elif not isinstance(initial_actions, list):
        initial_actions = []
    initial_factors = row.get("explanation_details", [])
    if not isinstance(initial_factors, list):
        initial_factors = []
    llm_payload = _employee_payload(row, schema, initial_factors, initial_actions)
    employee_identifier = str(llm_payload.get("employee_id") or llm_payload.get("employee") or row.name)
    llm_state_key = f"employee_llm_result::{employee_identifier}"
    llm_button_key = f"employee_llm_generate::{employee_identifier}"

    summary_tab, drivers_tab, actions_tab = st.tabs(["Profile", "Drivers", "Actions"])

    with summary_tab:
        section_header("Employee summary")
        summary_fields = _summary_fields(row, schema, tenure_years)
        summary_cols = st.columns(4)
        for index, (label, value) in enumerate(summary_fields):
            summary_cols[index % 4].metric(label, value)

        lead_col, summary_col = st.columns([0.88, 1.12])
        with lead_col:
            section_header("Risk posture")
            render_risk_badge(row.get("risk_level", "Unknown"), row.get("risk_score"))
            with st.expander("View status details", expanded=False):
                components = ai_context.get("components", {})
                st.caption(f"Risk scores: {components.get('risk_scores', 'unknown')}")
                st.caption(f"Explanations: {components.get('explanations', 'unknown')}")
                st.caption(f"Recommendations: {components.get('recommendations', 'unknown')}")
                if bool(row.get("summary_is_simulated", ai_context["mode"] == "demo")):
                    st.caption("Narrative summary and some HR guidance may still rely on heuristic logic.")
            st.caption("Use this output to support review, not to automate a decision.")

        with summary_col:
            section_header("HR summary")
            st.write(row.get("hr_summary", "No HR summary is available for this employee."))
            st.caption("Optional local AI wording is available on request.")
            summary_placeholder = st.empty()
            if st.button("Generate AI HR Summary", key=llm_button_key, use_container_width=False):
                with summary_placeholder.container():
                    notice("Generating AI summary...", "Please wait while the local model prepares the summary.", tone="info")
                    with st.spinner("Generating AI summary..."):
                        llm_result = generate_employee_brief_with_cache(
                            employee_identifier,
                            model_metadata.get("model_version", "unknown"),
                            model_metadata.get("explanation_version", "unknown"),
                            OLLAMA_MODEL,
                            json.dumps(llm_payload, sort_keys=True, default=str),
                            timeout_seconds=45,
                        )
                        st.session_state[llm_state_key] = llm_result
                summary_placeholder.empty()

            llm_result = st.session_state.get(llm_state_key)
            if llm_result and llm_result.get("available"):
                st.caption(f"AI-assisted wording generated locally via {llm_result.get('source')}.")
                info_card("AI-assisted HR summary", llm_result.get("summary") or "No LLM summary returned.")
                diagnostics = llm_result.get("diagnostics", {})
                if diagnostics:
                    with st.expander("View AI generation diagnostics", expanded=False):
                        st.caption(
                            f"LLM latency: {diagnostics.get('latency_seconds', 'n/a')}s | "
                            f"load: {diagnostics.get('load_duration_ms', 'n/a')} ms | "
                            f"eval: {diagnostics.get('eval_duration_ms', 'n/a')} ms | "
                            f"cache hit: {diagnostics.get('cache_hit', False)}"
                        )
            elif llm_result and not llm_result.get("available"):
                info_card("AI summary unavailable right now", llm_result.get("error", "Local Ollama service not reachable."))

    with drivers_tab:
        driver_col, factor_col = st.columns([1.2, 0.9])
        explanations = row.get("explanation_details", [])
        if not isinstance(explanations, list):
            explanations = []

        with driver_col:
            section_header("Why this risk level?")
            if explanations:
                st.plotly_chart(contribution_chart(explanations), use_container_width=True)
            else:
                empty_state("No explanation details available", "No structured explanation was found for this employee.")

        with factor_col:
            section_header("Main risk factors")
            if explanations:
                bullet_card(
                    "Detected signals",
                    [f"{item['factor'].capitalize()} ({item['contribution']:+.0f})" for item in explanations[:5]],
                )
            else:
                empty_state("No factors available", "The current profile does not include factor-level explanation details.")

    with actions_tab:
        actions = initial_actions
        factors = initial_factors

        left, right = st.columns([1.05, 0.95])
        with left:
            section_header("Recommended preventive actions")
            if actions:
                for index, action in enumerate(actions[:4]):
                    linked_factor = factors[index]["factor"] if index < len(factors) else "general review"
                    info_card(action, f"Linked factor: {linked_factor}.")
            else:
                empty_state("No actions available", "No preventive action suggestion is available for this employee.")
            llm_result = st.session_state.get(llm_state_key)
            if llm_result and llm_result.get("available") and llm_result.get("actions"):
                st.caption("AI-assisted recommendations are phrased from model evidence and local context only.")
                for action in llm_result.get("actions", [])[:3]:
                    info_card(action, "Generated locally by Ollama from deterministic model evidence.")

        with right:
            section_header("How to use this output")
            bullet_card(
                "Good practice reminders",
                [
                    "Validate the signal with recent manager and HR context.",
                    "Use the output to prioritize outreach, not to automate a decision.",
                    "Check whether sensitive or incomplete data could distort the picture.",
                    "Document follow-up actions and review outcomes over time.",
                ],
            )
            llm_result = st.session_state.get(llm_state_key)
            if llm_result and llm_result.get("available") and llm_result.get("manager_talking_points"):
                bullet_card("AI-assisted talking points", llm_result["manager_talking_points"][:3])
