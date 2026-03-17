from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import pandas as pd
import streamlit as st

from src.config import APP_MANAGED_DATASET, DATASET_CANDIDATES


@dataclass
class DatasetBundle:
    df: pd.DataFrame
    source_path: str | None
    is_mock: bool
    message: str
    is_managed_copy: bool = False


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned.columns = [str(column).strip() for column in cleaned.columns]
    object_columns = cleaned.select_dtypes(include="object").columns
    for column in object_columns:
        cleaned[column] = cleaned[column].astype(str).str.strip()
        cleaned.loc[cleaned[column].isin(["", "nan", "None", "NaT"]), column] = pd.NA
    return cleaned


def _build_mock_dataset() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Employee_Name": "Jordan Miles",
                "EmpID": 9001,
                "Department": "Operations",
                "Position": "HR Coordinator",
                "Salary": 52000,
                "Termd": 0,
                "EmploymentStatus": "Active",
                "PerformanceScore": "Fully Meets",
                "EngagementSurvey": 3.1,
                "EmpSatisfaction": 2,
                "SpecialProjectsCount": 0,
                "DaysLateLast30": 3,
                "Absences": 8,
                "DateofHire": "2024-05-10",
                "DOB": "1992-03-15",
                "ManagerName": "Patricia Wong",
                "Sex": "F",
                "RaceDesc": "Undisclosed",
            },
            {
                "Employee_Name": "Alex Carter",
                "EmpID": 9002,
                "Department": "IT/IS",
                "Position": "Systems Analyst",
                "Salary": 76000,
                "Termd": 0,
                "EmploymentStatus": "Active",
                "PerformanceScore": "Exceeds",
                "EngagementSurvey": 4.7,
                "EmpSatisfaction": 4,
                "SpecialProjectsCount": 3,
                "DaysLateLast30": 0,
                "Absences": 1,
                "DateofHire": "2020-09-01",
                "DOB": "1988-11-23",
                "ManagerName": "Lucas Brown",
                "Sex": "M",
                "RaceDesc": "Undisclosed",
            },
        ]
    )


def _load_csv(path) -> pd.DataFrame:
    return _clean_dataframe(pd.read_csv(path))


@st.cache_data(show_spinner=False)
def load_hr_dataset() -> DatasetBundle:
    if APP_MANAGED_DATASET.exists():
        return DatasetBundle(
            df=_load_csv(APP_MANAGED_DATASET),
            source_path=str(APP_MANAGED_DATASET),
            is_mock=False,
            message="Managed HR dataset loaded successfully.",
            is_managed_copy=True,
        )

    for candidate in DATASET_CANDIDATES:
        if candidate.exists():
            return DatasetBundle(
                df=_load_csv(candidate),
                source_path=str(candidate),
                is_mock=False,
                message="Real HR dataset loaded successfully.",
                is_managed_copy=False,
            )

    return DatasetBundle(
        df=_clean_dataframe(_build_mock_dataset()),
        source_path=None,
        is_mock=True,
        message=(
            "No HR dataset was found. The app is running with a small internal mock dataset. "
            "Add a real file or create a managed copy from the Add Employee page."
        ),
        is_managed_copy=False,
    )


def _safe_unique_emp_id(df: pd.DataFrame) -> int:
    if "EmpID" not in df.columns:
        return 100001
    numeric_ids = pd.to_numeric(df["EmpID"], errors="coerce").dropna()
    if numeric_ids.empty:
        return 100001
    return int(numeric_ids.max()) + 1


def _default_for_column(df: pd.DataFrame, column: str):
    defaults = {
        "Termd": 0,
        "EmploymentStatus": "Active",
        "DateofTermination": pd.NA,
        "TermReason": pd.NA,
        "Absences": 0,
        "DaysLateLast30": 0,
        "SpecialProjectsCount": 0,
        "FromDiversityJobFairID": 0,
        "EngagementSurvey": 3.0,
        "EmpSatisfaction": 3,
        "PerformanceScore": "Fully Meets",
        "PerfScoreID": 3,
        "Internal_Transfer_Request": "No request made",
        "Avg_Overtime_Hours": 0.0,
        "Distance_From_Home_Km": 0.0,
        "Remote_Work_Frequency": 0,
        "Exit_Interview_Feedback": pd.NA,
    }
    if column in defaults:
        return defaults[column]

    if column in df.columns:
        series = df[column].dropna()
        if not series.empty:
            return series.mode().iloc[0] if not series.mode().empty else series.iloc[0]
    return pd.NA


def _normalize_value_for_storage(column: str, value):
    if isinstance(value, date):
        return value.isoformat()
    return value


def append_employee_record(employee_data: dict) -> tuple[bool, str, dict | None]:
    try:
        dataset = load_hr_dataset()
        base_df = dataset.df.copy()
        if base_df.empty:
            base_df = _build_mock_dataset()

        new_row = {column: _default_for_column(base_df, column) for column in base_df.columns}
        for column, value in employee_data.items():
            if column in new_row:
                new_row[column] = _normalize_value_for_storage(column, value)

        if "EmpID" in new_row:
            proposed_id = pd.to_numeric(pd.Series([new_row["EmpID"]]), errors="coerce").iloc[0]
            if pd.isna(proposed_id) or int(proposed_id) <= 0:
                new_row["EmpID"] = _safe_unique_emp_id(base_df)
            else:
                existing_ids = set(pd.to_numeric(base_df["EmpID"], errors="coerce").dropna().astype(int).tolist()) if "EmpID" in base_df.columns else set()
                if int(proposed_id) in existing_ids:
                    return False, "Employee ID already exists.", None
                new_row["EmpID"] = int(proposed_id)

        if not str(new_row.get("Employee_Name", "")).strip():
            return False, "Employee name is required.", None

        for column in base_df.columns:
            if column not in new_row:
                new_row[column] = _default_for_column(base_df, column)

        updated_df = pd.concat([base_df, pd.DataFrame([new_row], columns=base_df.columns)], ignore_index=True)
        updated_df = _clean_dataframe(updated_df)
        APP_MANAGED_DATASET.parent.mkdir(parents=True, exist_ok=True)
        updated_df.to_csv(APP_MANAGED_DATASET, index=False)
        load_hr_dataset.clear()
        return True, "Employee added successfully.", new_row
    except Exception as exc:  # pragma: no cover
        return False, f"Failed to persist the employee record: {exc}", None
