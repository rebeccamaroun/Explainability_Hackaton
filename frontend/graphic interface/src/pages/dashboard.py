from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.schema_utils import coerce_numeric, derive_age_years, derive_tenure_years, get_column, has_field
from src.ui_components import bullet_card, empty_state, footer_note, info_card, metric_card, page_header, section_header, style_plotly_figure


def _risk_counts(df: pd.DataFrame) -> dict[str, int]:
    counts = df["risk_level"].value_counts().to_dict() if "risk_level" in df.columns else {}
    return {level: int(counts.get(level, 0)) for level in ["Low", "Medium", "High"]}


def _column_is_numeric_code(series: pd.Series) -> bool:
    numeric = pd.to_numeric(series, errors="coerce")
    non_null_ratio = numeric.notna().mean()
    return bool(non_null_ratio > 0.9)


def _resolved_age_series(df: pd.DataFrame, schema: dict[str, str | None]) -> pd.Series:
    if "Age" in df.columns:
        age = coerce_numeric(df["Age"])
        age = age.where((age >= 14) & (age <= 90))
        if age.notna().any():
            return age
    derived_age = derive_age_years(df, schema)
    return derived_age.where((derived_age >= 14) & (derived_age <= 90))


def render_dashboard_page(df: pd.DataFrame, schema: dict[str, str | None], dataset, ai_context: dict) -> None:
    page_header(
        "HR Dashboard",
        "A concise view of workforce risk, structure, and immediate HR priorities.",
    )

    risk_counts = _risk_counts(df)
    total_employees = len(df)
    term_share = None
    if has_field(schema, "term_flag"):
        term_numeric = coerce_numeric(get_column(df, schema, "term_flag")).fillna(0)
        term_share = f"{(term_numeric.mean() * 100):.1f}%"

    global_risk = f"{df['risk_score'].mean():.0f}%" if "risk_score" in df.columns else "Not available"

    kpi_top = st.columns(4)
    with kpi_top[0]:
        metric_card("Total employees", f"{total_employees}", "People currently included in the review scope")
    with kpi_top[1]:
        metric_card("Observed turnover", term_share or "Not available", "Based on termination fields detected in the dataset")
    with kpi_top[2]:
        metric_card("Estimated risk exposure", global_risk, "Average score across current employee profiles")
    with kpi_top[3]:
        metric_card("High-priority cases", f"{risk_counts['High']}", "Profiles currently requiring immediate HR review")

    kpi_bottom = st.columns(3)
    with kpi_bottom[0]:
        metric_card("Low risk", str(risk_counts["Low"]), "Profiles with stable signals")
    with kpi_bottom[1]:
        metric_card("Medium risk", str(risk_counts["Medium"]), "Profiles to monitor and discuss")
    with kpi_bottom[2]:
        metric_card("High risk", str(risk_counts["High"]), "Profiles needing preventive intervention")

    st.markdown("<div class='tg-hr'></div>", unsafe_allow_html=True)
    section_header("Workforce composition", "Use these visuals to understand how the population and turnover signals are distributed.")

    chart_left, chart_right = st.columns(2)
    department_column = schema.get("department")
    position_column = schema.get("position")

    if department_column:
        department_series = df[department_column]
        department_label = "Department code" if _column_is_numeric_code(department_series) else "Department"
        dept_counts = department_series.fillna("Not available").value_counts().head(10).reset_index()
        dept_counts.columns = [department_label, "Employees"]
        fig = px.bar(
            dept_counts,
            x=department_label,
            y="Employees",
            title="Employees by department" if department_label == "Department" else "Employees by department code",
            color="Employees",
            color_continuous_scale="Blues",
        )
        fig.update_layout(coloraxis_showscale=False)
        chart_left.plotly_chart(style_plotly_figure(fig), use_container_width=True)
    else:
        with chart_left:
            empty_state("Department data unavailable", "No department column was detected in the current dataset.")

    if position_column:
        position_series = df[position_column]
        position_label = "Position code" if _column_is_numeric_code(position_series) else "Position"
        pos_counts = position_series.fillna("Not available").value_counts().head(10).reset_index()
        pos_counts.columns = [position_label, "Employees"]
        fig = px.bar(
            pos_counts,
            x="Employees",
            y=position_label,
            orientation="h",
            title="Employees by position" if position_label == "Position" else "Employees by position code",
            color="Employees",
            color_continuous_scale="Tealgrn",
        )
        fig.update_layout(coloraxis_showscale=False)
        chart_right.plotly_chart(style_plotly_figure(fig), use_container_width=True)
    else:
        with chart_right:
            empty_state("Position data unavailable", "No position column was detected in the current dataset.")

    dist_cols = st.columns(3)
    tenure_years = derive_tenure_years(df, schema)
    age_years = _resolved_age_series(df, schema)
    salary = coerce_numeric(get_column(df, schema, "salary"))

    if tenure_years.notna().any():
        fig = px.histogram(
            tenure_years.dropna(),
            nbins=15,
            title="Tenure distribution (years)",
            color_discrete_sequence=["#0f4c81"],
        )
        dist_cols[0].plotly_chart(style_plotly_figure(fig), use_container_width=True)
    else:
        with dist_cols[0]:
            empty_state("Tenure unavailable", "Hire dates are missing or could not be interpreted.")

    if age_years.notna().any():
        fig = px.histogram(
            age_years.dropna(),
            nbins=15,
            title="Employees by age",
            color_discrete_sequence=["#4a8f72"],
        )
        fig.update_layout(xaxis_title="Age", yaxis_title="Employees")
        dist_cols[1].plotly_chart(style_plotly_figure(fig), use_container_width=True)
    else:
        with dist_cols[1]:
            empty_state("Age unavailable", "Birth dates are missing or could not be interpreted.")

    if salary.notna().any():
        fig = px.box(salary.dropna(), title="Salary overview")
        fig.update_traces(marker_color="#c7a14a")
        dist_cols[2].plotly_chart(style_plotly_figure(fig), use_container_width=True)
    else:
        with dist_cols[2]:
            empty_state("Salary unavailable", "No salary field was detected for the current dataset.")

    if has_field(schema, "term_flag") and department_column:
        st.markdown("<div class='tg-hr'></div>", unsafe_allow_html=True)
        section_header("Observed turnover", "This view highlights where historical departures appear more concentrated.")
        term_numeric = coerce_numeric(get_column(df, schema, "term_flag")).fillna(0)
        turnover_df = pd.DataFrame(
            {
                "Department": df[department_column].fillna("Not available"),
                "Terminated": term_numeric,
            }
        )
        turnover_summary = (
            turnover_df.groupby("Department", as_index=False)["Terminated"].mean().sort_values("Terminated", ascending=False)
        )
        turnover_summary["Terminated"] = turnover_summary["Terminated"] * 100
        fig = px.bar(
            turnover_summary.head(10),
            x="Department",
            y="Terminated",
            title="Observed turnover rate by department",
            color="Terminated",
            color_continuous_scale="OrRd",
        )
        fig.update_layout(yaxis_title="Turnover rate (%)")
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(style_plotly_figure(fig), use_container_width=True)

    st.markdown("<div class='tg-hr'></div>", unsafe_allow_html=True)
    insight_cols = st.columns([1.05, 0.95])

    with insight_cols[0]:
        section_header("Main observed factors", "The most frequent signals currently driving estimated risk in the dataset.")
        top_factors = (
            df["key_factors"].str.split(", ").explode().value_counts().head(5)
            if "key_factors" in df.columns
            else pd.Series(dtype="int64")
        )
        if len(top_factors):
            bullet_card(
                "Most recurring signals",
                [f"{factor.capitalize()} appears in {count} employee profiles." for factor, count in top_factors.items()],
            )
        else:
            empty_state("No factor summary yet", "The application could not generate a factor summary for the current data.")

    with insight_cols[1]:
        section_header("Priority HR actions", "A concise view of the preventive actions most often recommended first.")
        actions = (
            df["priority_action"].fillna("Review with HR").value_counts().head(4)
            if "priority_action" in df.columns
            else pd.Series(dtype="int64")
        )
        if len(actions):
            for action, count in actions.items():
                info_card(action, f"Currently suggested as the leading action for {count} employee cases.")
        else:
            empty_state("No action summary yet", "Action recommendations are not available for the current data.")

    st.markdown("<div class='tg-hr'></div>", unsafe_allow_html=True)
    footer_note("Decision-support only. This interface supports HR review and should not be used as an automated decision-maker.")
