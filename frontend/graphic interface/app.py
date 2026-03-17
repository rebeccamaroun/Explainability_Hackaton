from pathlib import Path

import streamlit as st

from src.config import APP_NAME
from src.data_loader import load_hr_dataset
from src.demo_ai import build_demo_ai_outputs
from src.real_ai_adapter import enrich_with_ai_outputs
from src.schema_utils import detect_schema
from src.ui_components import render_app_header, render_global_messages, use_app_styles
from src.pages.add_employee import render_add_employee_page
from src.pages.action_plan import render_action_plan_page
from src.pages.dashboard import render_dashboard_page
from src.pages.employee_analysis import render_employee_analysis_page
from src.pages.responsible_ai import render_responsible_ai_page


def main() -> None:
    st.set_page_config(
        page_title=f"{APP_NAME} | HR Retention Intelligence",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    use_app_styles()

    dataset = load_hr_dataset()
    schema = detect_schema(dataset.df)
    demo_baseline = build_demo_ai_outputs(dataset.df, schema)
    enriched_df, ai_context = enrich_with_ai_outputs(demo_baseline, schema)

    st.session_state["talentguard_dataset"] = dataset
    st.session_state["talentguard_schema"] = schema
    st.session_state["talentguard_ai_context"] = ai_context
    st.session_state["talentguard_enriched_df"] = enriched_df

    render_app_header(ai_context, dataset)
    render_global_messages(dataset, ai_context)

    pages = {
        "HR Dashboard": render_dashboard_page,
        "Employee Analysis": render_employee_analysis_page,
        "Add Employee": render_add_employee_page,
        "Action Plan": render_action_plan_page,
        "Responsible AI": render_responsible_ai_page,
    }

    if "talentguard_next_page" in st.session_state:
        st.session_state["talentguard_selected_page"] = st.session_state.pop("talentguard_next_page")

    st.sidebar.markdown(f'<div class="tg-shell-title">{APP_NAME}</div>', unsafe_allow_html=True)
    st.sidebar.markdown(
        '<div class="tg-shell-copy">A calm workspace for HR teams to review retention signals, explanations, and action priorities.</div>',
        unsafe_allow_html=True,
    )
    if st.sidebar.button("Add Employee", use_container_width=True):
        st.session_state["talentguard_next_page"] = "Add Employee"
        st.rerun()
    st.sidebar.markdown("### Navigation")
    if "talentguard_selected_page" not in st.session_state:
        st.session_state["talentguard_selected_page"] = "HR Dashboard"
    selected_page = st.sidebar.radio(
        "Go to",
        list(pages.keys()),
        key="talentguard_selected_page",
        label_visibility="collapsed",
    )

    with st.sidebar:
        st.markdown("### Data status")
        st.caption(f"Source file: `{Path(dataset.source_path).name if dataset.source_path else 'Mock dataset'}`")
        st.caption(f"Rows loaded: `{len(enriched_df)}`")
        st.caption(f"AI mode: `{ai_context['label']}`")
        st.caption("Decision-support only. HR judgment remains required.")

    if message := st.session_state.pop("talentguard_post_submit_message", None):
        st.success(message)

    pages[selected_page](enriched_df, schema, dataset, ai_context)


if __name__ == "__main__":
    main()
