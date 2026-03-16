from __future__ import annotations

from typing import Any

import pandas as pd


FIELD_CANDIDATES = {
    "employee_id": ["EmpID", "EmployeeID", "employee_id", "id"],
    "employee_name": ["Employee_Name", "EmployeeName", "FullName", "Name", "employee_name"],
    "department": ["Department", "Dept", "DeptName", "department"],
    "position": ["Position", "JobTitle", "Role", "position"],
    "salary": ["Salary", "AnnualSalary", "salary"],
    "term_flag": ["Termd", "IsTerminated", "Terminated", "term_flag"],
    "term_reason": ["TermReason", "TerminationReason", "ExitReason", "term_reason"],
    "employment_status": ["EmploymentStatus", "Status", "employment_status"],
    "performance_score": ["PerformanceScore", "PerfScoreID", "performance_score"],
    "engagement": ["EngagementSurvey", "EngagementScore", "engagement"],
    "satisfaction": ["EmpSatisfaction", "Satisfaction", "satisfaction"],
    "projects": ["SpecialProjectsCount", "ProjectsCount", "projects"],
    "absences": ["Absences", "AbsenceCount", "absences"],
    "lateness": ["DaysLateLast30", "LateDaysLast30", "lateness"],
    "hire_date": ["DateofHire", "HireDate", "hire_date"],
    "termination_date": ["DateofTermination", "TerminationDate", "termination_date"],
    "birth_date": ["DOB", "BirthDate", "birth_date"],
    "manager": ["ManagerName", "Manager", "manager"],
    "sex": ["Sex", "Gender", "sex"],
    "race": ["RaceDesc", "Race", "race"],
}


def _find_column(columns: list[str], candidates: list[str]) -> str | None:
    lower_map = {column.lower().strip(): column for column in columns}
    for candidate in candidates:
        match = lower_map.get(candidate.lower().strip())
        if match:
            return match
    return None


def detect_schema(df: pd.DataFrame) -> dict[str, str | None]:
    columns = list(df.columns)
    return {field: _find_column(columns, candidates) for field, candidates in FIELD_CANDIDATES.items()}


def get_column(df: pd.DataFrame, schema: dict[str, str | None], field: str) -> pd.Series:
    column = schema.get(field)
    if column and column in df.columns:
        return df[column]
    return pd.Series([pd.NA] * len(df), index=df.index)


def has_field(schema: dict[str, str | None], field: str) -> bool:
    return bool(schema.get(field))


def coerce_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def coerce_datetime(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, errors="coerce")


def derive_tenure_years(df: pd.DataFrame, schema: dict[str, str | None]) -> pd.Series:
    hire_dates = coerce_datetime(get_column(df, schema, "hire_date"))
    termination_dates = coerce_datetime(get_column(df, schema, "termination_date"))
    effective_end = termination_dates.fillna(pd.Timestamp.today().normalize())
    tenure_days = (effective_end - hire_dates).dt.days
    return tenure_days.div(365.25)


def derive_age_years(df: pd.DataFrame, schema: dict[str, str | None]) -> pd.Series:
    birth_dates = coerce_datetime(get_column(df, schema, "birth_date"))
    age_days = (pd.Timestamp.today().normalize() - birth_dates).dt.days
    return age_days.div(365.25)


def normalize_text_value(value: Any) -> str:
    if pd.isna(value):
        return "Not available"
    text = str(value).strip()
    return text if text else "Not available"
