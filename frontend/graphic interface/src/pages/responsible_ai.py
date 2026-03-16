from __future__ import annotations

import streamlit as st

from src.config import SENSITIVE_COLUMNS
from src.ui_components import bullet_card, info_card, notice, page_header, section_header


def render_responsible_ai_page(df, schema: dict[str, str | None], dataset, ai_context: dict) -> None:
    page_header(
        "Responsible AI and Transparency",
        "A readable view of the product boundaries, demo limitations, explainability approach, and safeguards expected around sensitive HR data.",
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
            "Demo version limitations",
            "Some AI components are simulated in this demo version. Final production outputs may differ once the ML and NLP pipelines are connected.",
        )
    with overview_right:
        info_card(
            "Explainability",
            "The current experience favors interpretable rules and contribution-style factors so HR users can understand what is being shown.",
        )
        info_card(
            "Frugality",
            "The product prioritizes lightweight processing and modular integration rather than opaque or computationally heavy workflows.",
        )
        info_card(
            "Decision-support only",
            "No HR decision should be made automatically based only on this tool. Human review remains mandatory.",
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
                "Some AI components are simulated in this demo version.",
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
                "No external AI output files were detected. Risk, explanations, and recommendations currently rely on transparent fallback logic.",
                tone="warning",
            )
        info_card(
            "Data protection reminder",
            "Only the minimum necessary data should be exposed in business workflows, and access should stay aligned with HR governance rules.",
        )
