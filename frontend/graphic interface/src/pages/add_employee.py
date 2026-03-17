from __future__ import annotations

import json
from datetime import date

import pandas as pd
import streamlit as st

from src.config import EXPLAINABILITY_ROOTS
from src.data_loader import append_employee_record
from src.ui_components import info_card, page_header, section_header


FORM_FIELD_ORDER = [
    "EmpID",
    "Employee_Name",
    "Department",
    "Position",
    "ManagerName",
    "EmploymentStatus",
    "Salary",
    "DateofHire",
    "DOB",
    "PerformanceScore",
    "PerfScoreID",
    "EngagementSurvey",
    "EmpSatisfaction",
    "SpecialProjectsCount",
    "Absences",
    "DaysLateLast30",
    "FromDiversityJobFairID",
    "Sex",
    "RaceDesc",
    "MaritalDesc",
    "CitizenDesc",
]


DISPLAY_LABEL_OVERRIDES = {
    "Sex": {
        "F": "Female",
        "M": "Male",
        "M ": "Male",
    }
}


@st.cache_data(show_spinner=False)
def _load_encoding_mappings() -> dict:
    for root in EXPLAINABILITY_ROOTS:
        mapping_path = root / "data" / "cleaned" / "encoding_mappings.json"
        if mapping_path.exists():
            return json.loads(mapping_path.read_text(encoding="utf-8"))
    return {}


def _mapping_label(column: str, raw_label: str) -> str:
    normalized = str(raw_label).strip()
    return DISPLAY_LABEL_OVERRIDES.get(column, {}).get(raw_label, DISPLAY_LABEL_OVERRIDES.get(column, {}).get(normalized, normalized))


def _mapping_options(column: str) -> list[str]:
    mappings = _load_encoding_mappings()
    if column not in mappings:
        return []
    labels = [_mapping_label(column, label) for label in mappings[column].keys()]
    return sorted(labels, key=lambda value: value.lower())


def _encode_form_value(column: str, value):
    mappings = _load_encoding_mappings()
    if column not in mappings:
        return value

    reverse_lookup = {}
    for raw_label, encoded in mappings[column].items():
        reverse_lookup[_mapping_label(column, raw_label)] = encoded
    return reverse_lookup.get(value, value)


def _field_options(df: pd.DataFrame, column: str) -> list:
    mapped_options = _mapping_options(column)
    if mapped_options:
        return mapped_options

    if column not in df.columns:
        return []
    values = df[column].dropna().astype(str).str.strip()
    cleaned = [v for v in values.unique().tolist() if v]
    unique = sorted(
        cleaned,
        key=lambda value: (pd.to_numeric(pd.Series([value]), errors="coerce").isna().iloc[0], str(value).lower())
    )
    return unique[:200]


def _default_date_from_series(df: pd.DataFrame, column: str) -> date:
    if column not in df.columns:
        return date.today()
    dates = pd.to_datetime(df[column], errors="coerce").dropna()
    if dates.empty:
        return date.today()
    return dates.max().date()


def _render_field(df: pd.DataFrame, column: str):
    label = column.replace("_", " ")
    numeric_columns = {
        "EmpID",
        "Salary",
        "PerfScoreID",
        "EngagementSurvey",
        "EmpSatisfaction",
        "SpecialProjectsCount",
        "Absences",
        "DaysLateLast30",
        "FromDiversityJobFairID",
    }
    date_columns = {"DateofHire", "DOB"}
    select_columns = {
        "Department",
        "Position",
        "Sex",
        "RaceDesc",
        "MaritalDesc",
        "CitizenDesc",
        "EmploymentStatus",
        "ManagerName",
        "PerformanceScore",
    }

    if column in date_columns:
        return st.date_input(label, value=_default_date_from_series(df, column), key=f"add_employee_{column}")

    if column in numeric_columns:
        if column == "Salary":
            return st.number_input(label, min_value=0.0, step=1000.0, format="%.0f", key=f"add_employee_{column}")
        if column == "EngagementSurvey":
            return st.number_input(label, min_value=0.0, max_value=5.0, step=0.1, key=f"add_employee_{column}")
        return st.number_input(label, step=1, key=f"add_employee_{column}")

    if column in select_columns:
        options = _field_options(df, column)
        if options:
            return st.selectbox(label, options, index=0, key=f"add_employee_{column}")

    return st.text_input(label, key=f"add_employee_{column}")


def render_add_employee_page(df: pd.DataFrame, schema: dict[str, str | None], dataset, ai_context: dict) -> None:
    page_header("Add Employee")
    with st.form("add_employee_form", clear_on_submit=False):
        section_header("Core employee details")
        available_fields = [field for field in FORM_FIELD_ORDER if field in df.columns]
        top_fields = [field for field in available_fields if field in {"EmpID", "Employee_Name", "Department", "Position", "ManagerName", "EmploymentStatus"}]
        work_fields = [field for field in available_fields if field in {"Salary", "DateofHire", "DOB", "PerformanceScore", "PerfScoreID", "EngagementSurvey", "EmpSatisfaction"}]
        people_fields = [field for field in available_fields if field in {"SpecialProjectsCount", "Absences", "DaysLateLast30", "FromDiversityJobFairID", "Sex", "RaceDesc", "MaritalDesc", "CitizenDesc"}]

        for field_group in [top_fields, work_fields, people_fields]:
            if not field_group:
                continue
            cols = st.columns(2)
            for index, column in enumerate(field_group):
                with cols[index % 2]:
                    _render_field(df, column)

        submit_col, cancel_col = st.columns([0.5, 0.5])
        submitted = submit_col.form_submit_button("Add Employee", type="primary", use_container_width=True)
        cancelled = cancel_col.form_submit_button("Cancel", use_container_width=True)

    if cancelled:
        st.session_state["talentguard_next_page"] = "Employee Analysis"
        st.rerun()

    if submitted:
        employee_name = st.session_state.get("add_employee_Employee_Name", "").strip()
        if not employee_name:
            st.error("Employee name is required.")
            return

        payload = {}
        for column in available_fields:
            value = st.session_state.get(f"add_employee_{column}")
            if value in ("", None):
                continue
            payload[column] = _encode_form_value(column, value)

        success, message, created_row = append_employee_record(payload)
        if not success:
            st.error(message)
            return

        st.session_state["talentguard_post_submit_message"] = message
        st.session_state["talentguard_next_page"] = "Employee Analysis"
        st.session_state["talentguard_new_employee_id"] = created_row.get("EmpID")
        st.session_state["talentguard_new_employee_name"] = created_row.get("Employee_Name")
        st.rerun()

    info_card(
        "Persistence behavior",
        "New records are saved into the app-managed dataset copy so the original source file remains unchanged.",
    )
