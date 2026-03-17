from __future__ import annotations

import json

import pandas as pd
import streamlit as st

from src.config import OLLAMA_MODEL, RISK_LEVEL_ORDER
from src.llm_service import generate_employee_brief_with_cache
from src.model_artifacts import build_model_metadata
from src.schema_utils import normalize_text_value
from src.ui_components import empty_state, notice, page_header, safe_download_dataframe, section_header


def render_action_plan_page(df: pd.DataFrame, schema: dict[str, str | None], dataset, ai_context: dict) -> None:
    model_metadata = build_model_metadata()
    page_header(
        "Action Plan",
        "Prioritize HR follow-up by filtering the highest-risk cases, reviewing key factors, and exporting a practical action list for next steps.",
        eyebrow="Prioritization",
        badges=[
            (
                "Heuristic priorities"
                if ai_context["mode"] == "demo"
                else "Hybrid priorities"
                if ai_context["mode"] == "hybrid"
                else "AI-enriched priorities",
                "demo" if ai_context["mode"] == "demo" else "warn",
            )
        ],
        aside_title="What this page answers",
        aside_body="Which employees should be reviewed first, what is driving urgency, and which action should start the follow-up.",
    )

    work_df = df.copy()
    employee_col = schema.get("employee_name")
    dept_col = schema.get("department")

    filter_cols = st.columns([1.1, 0.9, 0.9, 0.9])
    departments = ["All"] + sorted(work_df[dept_col].dropna().unique().tolist()) if dept_col else ["All"]
    selected_department = filter_cols[0].selectbox("Department", departments)
    selected_risk = filter_cols[1].selectbox("Risk level", ["All"] + RISK_LEVEL_ORDER)
    sort_by = filter_cols[2].selectbox("Sort by", ["Risk score", "Employee", "Department"])
    max_rows = filter_cols[3].selectbox("Rows", [10, 25, 50, 100], index=1)

    if selected_department != "All" and dept_col:
        work_df = work_df[work_df[dept_col] == selected_department]
    if selected_risk != "All" and "risk_level" in work_df.columns:
        work_df = work_df[work_df["risk_level"] == selected_risk]

    if sort_by == "Risk score" and "risk_score" in work_df.columns:
        work_df = work_df.sort_values("risk_score", ascending=False)
    elif sort_by == "Employee" and employee_col:
        work_df = work_df.sort_values(employee_col)
    elif sort_by == "Department" and dept_col:
        work_df = work_df.sort_values(dept_col)

    if "priority_status" not in work_df.columns:
        work_df["priority_status"] = "To launch"

    section_header("Priority queue", "A review table focused on actionability rather than technical detail.")

    display = pd.DataFrame(
        {
            "Employee": work_df[employee_col].apply(normalize_text_value) if employee_col else ["Not available"] * len(work_df),
            "Department": work_df[dept_col].apply(normalize_text_value) if dept_col else ["Not available"] * len(work_df),
            "Risk level": work_df["risk_level"] if "risk_level" in work_df.columns else ["Not available"] * len(work_df),
            "Risk score": work_df.get("risk_score", pd.Series([pd.NA] * len(work_df))),
            "Key factors": work_df["key_factors"] if "key_factors" in work_df.columns else ["Not available"] * len(work_df),
            "Priority action": work_df["priority_action"] if "priority_action" in work_df.columns else ["Review with HR"] * len(work_df),
            "Status": work_df["priority_status"] if "priority_status" in work_df.columns else ["To launch"] * len(work_df),
        }
    )

    if display.empty:
        empty_state("No matching employee profiles", "Adjust the filters to recover employees in scope for the action plan.")
    else:
        preview_cols = st.columns([0.85, 0.85, 0.85, 1.2])
        preview_cols[0].metric("Profiles in scope", f"{len(display)}")
        preview_cols[1].metric("High risk", f"{(display['Risk level'] == 'High').sum()}")
        preview_cols[2].metric("Medium risk", f"{(display['Risk level'] == 'Medium').sum()}")
        preview_cols[3].metric("Top action", display["Priority action"].mode().iloc[0] if not display["Priority action"].mode().empty else "Review with HR")

        styled = display.head(max_rows).style.map(
            lambda value: "background-color: #f7e7e5; color: #8a3f38; font-weight: 700;" if value == "High"
            else "background-color: #f5eddf; color: #8a6331; font-weight: 700;" if value == "Medium"
            else "background-color: #e7f2ec; color: #2f6b52; font-weight: 700;" if value == "Low"
            else "",
            subset=["Risk level"],
        )
        st.dataframe(
            styled,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Risk score": st.column_config.NumberColumn("Risk score", format="%.0f"),
                "Priority action": st.column_config.TextColumn("Priority action", width="large"),
                "Key factors": st.column_config.TextColumn("Key factors", width="large"),
            },
        )

    lower = st.columns([1.15, 0.85])
    with lower[0]:
        notice(
            "Operational guidance",
            "Start with high-risk cases, validate the signal with context, and document the first preventive action in a structured follow-up process.",
            tone="info",
        )
    with lower[1]:
        safe_download_dataframe(display, "Export current action plan", "talentguard_action_plan.csv")
        st.caption("The export follows the active filters and sorting choices.")

    if not display.empty:
        st.markdown("<div class='tg-hr'></div>", unsafe_allow_html=True)
        section_header("AI-assisted action rationale", "Generate an optional short rationale for one selected employee only.")
        candidate_rows = display.head(max_rows).copy()
        labels = [f"{row.Employee} | {row.Department} | {row['Risk level']}" for _, row in candidate_rows.iterrows()]
        selected_label = st.selectbox("Select an employee for AI details", labels, key="action_plan_llm_employee")
        selected_index = labels.index(selected_label)
        selected_row = candidate_rows.iloc[selected_index]
        llm_state_key = f"action_plan_llm::{selected_row['Employee']}"
        payload = {
            "employee_id": selected_row["Employee"],
            "employee": selected_row["Employee"],
            "department": selected_row["Department"],
            "position": "Not available",
            "risk_score": selected_row["Risk score"],
            "risk_level": selected_row["Risk level"],
            "top_factors": [{"factor": item.strip(), "contribution": 0} for item in str(selected_row["Key factors"]).split(",")[:3] if item.strip()],
            "allowed_actions": [selected_row["Priority action"]],
            "text_insight": "",
        }
        st.caption("This optional step does not affect the table load. It uses the local LLM only after user request.")
        if st.button("Generate AI Action Rationale", key="action_plan_llm_generate"):
            with st.spinner("Generating local AI rationale..."):
                llm_result = generate_employee_brief_with_cache(
                    str(selected_row["Employee"]),
                    model_metadata.get("model_version", "unknown"),
                    model_metadata.get("explanation_version", "unknown"),
                    OLLAMA_MODEL,
                    json.dumps(payload, sort_keys=True, default=str),
                )
                st.session_state[llm_state_key] = llm_result

        llm_result = st.session_state.get(llm_state_key)
        if llm_result and llm_result.get("available"):
            notice(
                "AI-assisted rationale",
                llm_result.get("summary") or "No rationale returned.",
                tone="info",
            )
            if llm_result.get("actions"):
                for action in llm_result["actions"][:3]:
                    notice("AI-assisted action phrasing", action, tone="info")
            diagnostics = llm_result.get("diagnostics", {})
            if diagnostics:
                st.caption(
                    f"LLM latency: {diagnostics.get('latency_seconds', 'n/a')}s | "
                    f"load: {diagnostics.get('load_duration_ms', 'n/a')} ms | "
                    f"eval: {diagnostics.get('eval_duration_ms', 'n/a')} ms | "
                    f"cache hit: {diagnostics.get('cache_hit', False)}"
                )
        elif llm_result and not llm_result.get("available"):
            notice("AI rationale unavailable right now", llm_result.get("error", "Local LLM service timeout."), tone="warning")
