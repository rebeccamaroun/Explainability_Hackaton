from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import streamlit as st

from src.config import DATASET_CANDIDATES


@dataclass
class DatasetBundle:
    df: pd.DataFrame
    source_path: str | None
    is_mock: bool
    message: str


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned.columns = [str(column).strip() for column in cleaned.columns]
    object_columns = cleaned.select_dtypes(include="object").columns
    for column in object_columns:
        cleaned[column] = cleaned[column].astype(str).str.strip()
        cleaned.loc[cleaned[column].isin(["", "nan", "None"]), column] = pd.NA
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
            {
                "Employee_Name": "Samira Patel",
                "EmpID": 9003,
                "Department": "Sales",
                "Position": "Account Executive",
                "Salary": 69000,
                "Termd": 1,
                "EmploymentStatus": "Voluntarily Terminated",
                "PerformanceScore": "Needs Improvement",
                "EngagementSurvey": 2.8,
                "EmpSatisfaction": 2,
                "SpecialProjectsCount": 0,
                "DaysLateLast30": 4,
                "Absences": 11,
                "DateofHire": "2023-01-12",
                "DateofTermination": "2025-12-08",
                "TermReason": "career change",
                "DOB": "1995-07-04",
                "ManagerName": "Maria Keller",
                "Sex": "F",
                "RaceDesc": "Undisclosed",
            },
        ]
    )


@st.cache_data(show_spinner=False)
def load_hr_dataset() -> DatasetBundle:
    for candidate in DATASET_CANDIDATES:
        if candidate.exists():
            df = pd.read_csv(candidate)
            return DatasetBundle(
                df=_clean_dataframe(df),
                source_path=str(candidate),
                is_mock=False,
                message="Real HR dataset loaded successfully.",
            )

    return DatasetBundle(
        df=_clean_dataframe(_build_mock_dataset()),
        source_path=None,
        is_mock=True,
        message=(
            "HRDataset_v14.csv was not found. The app is running with a small internal mock dataset. "
            "Place the CSV in graphic interface/data/ or next to the project to use the real dataset."
        ),
    )
