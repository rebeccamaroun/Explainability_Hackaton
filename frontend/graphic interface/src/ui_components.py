from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.config import APP_NAME, APP_TAGLINE


def use_app_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --tg-bg: #f3f5f8;
            --tg-surface: rgba(255, 255, 255, 0.82);
            --tg-surface-strong: #ffffff;
            --tg-border: #dde4ec;
            --tg-border-strong: #cfd8e3;
            --tg-text: #10233a;
            --tg-muted: #61758a;
            --tg-navy: #143a5c;
            --tg-blue: #2f5d86;
            --tg-blue-soft: #eaf1f8;
            --tg-gold-soft: #f5eddf;
            --tg-green-soft: #e7f2ec;
            --tg-red-soft: #f7e7e5;
            --tg-shadow: 0 18px 40px rgba(16, 35, 58, 0.06);
            --tg-radius-xl: 24px;
            --tg-radius-lg: 18px;
            --tg-radius-md: 14px;
        }

        html, body, [class*="css"]  {
            font-family: Aptos, "Segoe UI", "Helvetica Neue", sans-serif;
            color: var(--tg-text);
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(47, 93, 134, 0.08), transparent 32%),
                linear-gradient(180deg, #f7f8fa 0%, #eef2f7 100%);
        }

        .block-container {
            max-width: 1280px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #112c44 0%, #173853 100%);
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        [data-testid="stSidebar"] * {
            color: #f4f7fb;
        }

        [data-testid="stSidebar"] .stRadio > label,
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] .stCaption {
            color: rgba(244, 247, 251, 0.82);
        }

        [data-testid="stSidebar"] [role="radiogroup"] {
            gap: 0.45rem;
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
            color: #ffffff;
            letter-spacing: 0.01em;
        }

        .tg-shell-title {
            font-size: 1.08rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 0.2rem;
        }

        .tg-shell-copy {
            color: rgba(244, 247, 251, 0.78);
            font-size: 0.92rem;
            line-height: 1.45;
            margin-bottom: 1.2rem;
        }

        .tg-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.32rem 0.75rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.01em;
            margin-right: 0.4rem;
            margin-bottom: 0.5rem;
            border: 1px solid transparent;
        }

        .tg-badge.demo {
            background: rgba(20, 58, 92, 0.08);
            color: var(--tg-navy);
            border-color: rgba(20, 58, 92, 0.12);
        }

        .tg-badge.warn {
            background: rgba(183, 131, 47, 0.12);
            color: #7d5920;
            border-color: rgba(183, 131, 47, 0.16);
        }

        .tg-badge.low {
            background: var(--tg-green-soft);
            color: #2f6b52;
            border-color: rgba(47, 107, 82, 0.12);
        }

        .tg-badge.medium {
            background: var(--tg-gold-soft);
            color: #8a6331;
            border-color: rgba(138, 99, 49, 0.12);
        }

        .tg-badge.high {
            background: var(--tg-red-soft);
            color: #a15349;
            border-color: rgba(161, 83, 73, 0.12);
        }

        .tg-hero {
            background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.88) 100%);
            border: 1px solid rgba(221, 228, 236, 0.95);
            border-radius: var(--tg-radius-xl);
            padding: 1.45rem 1.5rem;
            box-shadow: var(--tg-shadow);
            margin-bottom: 1.25rem;
        }

        .tg-hero-grid {
            display: grid;
            grid-template-columns: 1.8fr 1fr;
            gap: 1rem;
            align-items: start;
        }

        .tg-overline {
            font-size: 0.78rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--tg-muted);
            margin-bottom: 0.55rem;
            font-weight: 700;
        }

        .tg-hero h1, .tg-page-header h2 {
            margin: 0;
            color: var(--tg-text);
            letter-spacing: -0.025em;
        }

        .tg-hero-copy, .tg-page-copy {
            color: var(--tg-muted);
            font-size: 0.98rem;
            line-height: 1.55;
            margin: 0.55rem 0 0 0;
            max-width: 56rem;
        }

        .tg-mini-panel {
            background: rgba(243, 246, 250, 0.9);
            border: 1px solid rgba(221, 228, 236, 1);
            border-radius: 18px;
            padding: 1rem 1.05rem;
        }

        .tg-mini-label {
            font-size: 0.76rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--tg-muted);
            font-weight: 700;
            margin-bottom: 0.35rem;
        }

        .tg-mini-value {
            color: var(--tg-text);
            font-size: 1rem;
            font-weight: 700;
            line-height: 1.4;
        }

        .tg-page-header {
            margin: 0.25rem 0 1rem 0;
        }

        .tg-section-title {
            font-size: 1.02rem;
            font-weight: 700;
            color: var(--tg-text);
            margin-bottom: 0.15rem;
        }

        .tg-section-copy {
            color: var(--tg-muted);
            font-size: 0.92rem;
            margin-bottom: 0.8rem;
        }

        .tg-kpi {
            background: linear-gradient(180deg, rgba(255,255,255,0.96) 0%, rgba(249,251,253,0.96) 100%);
            border: 1px solid rgba(221, 228, 236, 0.95);
            border-radius: var(--tg-radius-lg);
            padding: 1.15rem 1.15rem 1rem 1.15rem;
            min-height: 132px;
            box-shadow: 0 10px 22px rgba(16, 35, 58, 0.05);
        }

        .tg-kpi-label {
            color: var(--tg-muted);
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.55rem;
            font-weight: 700;
        }

        .tg-kpi-value {
            font-size: 2rem;
            line-height: 1.05;
            font-weight: 700;
            color: var(--tg-text);
            margin-bottom: 0.5rem;
        }

        .tg-card {
            background: var(--tg-surface-strong);
            border: 1px solid rgba(221, 228, 236, 0.96);
            border-radius: var(--tg-radius-lg);
            padding: 1rem 1.1rem;
            box-shadow: 0 8px 18px rgba(16, 35, 58, 0.04);
        }

        .tg-card-title {
            color: var(--tg-text);
            font-size: 1rem;
            font-weight: 700;
            margin: 0 0 0.35rem 0;
        }

        .tg-card-body {
            margin: 0;
            color: #485c70;
            line-height: 1.55;
            font-size: 0.94rem;
        }

        .tg-notice {
            border-radius: var(--tg-radius-lg);
            border: 1px solid rgba(221, 228, 236, 0.95);
            padding: 1rem 1.05rem;
            background: rgba(255,255,255,0.94);
            margin-bottom: 0.8rem;
        }

        .tg-notice.info { background: rgba(234, 241, 248, 0.9); }
        .tg-notice.warning { background: rgba(245, 237, 223, 0.9); }
        .tg-notice.alert { background: rgba(247, 231, 229, 0.92); }

        .tg-notice-title {
            font-size: 0.92rem;
            font-weight: 700;
            color: var(--tg-text);
            margin-bottom: 0.2rem;
        }

        .tg-notice-body {
            color: #4c6177;
            font-size: 0.92rem;
            line-height: 1.5;
            margin: 0;
        }

        .tg-list {
            margin: 0.25rem 0 0 0;
            padding-left: 1rem;
            color: #42586f;
        }

        .tg-list li {
            margin-bottom: 0.4rem;
            line-height: 1.5;
        }

        .tg-hr {
            border-top: 1px solid rgba(221, 228, 236, 0.95);
            margin: 1rem 0;
        }

        [data-testid="stMetric"] {
            background: rgba(255,255,255,0.95);
            border: 1px solid rgba(221, 228, 236, 0.92);
            border-radius: 16px;
            padding: 0.9rem 1rem;
            box-shadow: 0 8px 18px rgba(16, 35, 58, 0.04);
        }

        [data-testid="stDataFrame"] {
            border: 1px solid rgba(221, 228, 236, 0.95);
            border-radius: 18px;
            overflow: hidden;
            background: rgba(255,255,255,0.96);
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.35rem;
        }

        .stTabs [data-baseweb="tab"] {
            background: rgba(255,255,255,0.85);
            border: 1px solid rgba(221, 228, 236, 0.9);
            border-radius: 999px;
            padding: 0.4rem 0.9rem;
            color: var(--tg-muted);
        }

        .stTabs [aria-selected="true"] {
            background: rgba(20, 58, 92, 0.08) !important;
            color: var(--tg-navy) !important;
            border-color: rgba(20, 58, 92, 0.12) !important;
        }

        .stSelectbox label, .stMultiSelect label {
            font-weight: 600;
            color: var(--tg-text);
        }

        .stDownloadButton button {
            border-radius: 999px;
            border: 1px solid rgba(20, 58, 92, 0.16);
            background: white;
            color: var(--tg-navy);
            font-weight: 700;
            padding: 0.45rem 1rem;
        }

        .stButton button {
            border-radius: 999px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(
    title: str,
    description: str | None = None,
    eyebrow: str | None = None,
    badges: list[tuple[str, str]] | None = None,
    aside_title: str | None = None,
    aside_body: str | None = None,
) -> None:
    with st.container():
        if eyebrow:
            st.markdown(f'<div class="tg-overline">{eyebrow}</div>', unsafe_allow_html=True)

        main_col, aside_col = st.columns([1.8, 1])
        with main_col:
            if badges:
                badge_html = "".join(f'<span class="tg-badge {tone}">{label}</span>' for label, tone in badges)
                st.markdown(badge_html, unsafe_allow_html=True)
            st.subheader(title)
            if description:
                st.caption(description)

        with aside_col:
            if aside_title and aside_body:
                st.markdown(
                    f"""
                    <div class="tg-mini-panel">
                        <div class="tg-mini-label">{aside_title}</div>
                        <div class="tg-mini-value">{aside_body}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def render_app_header(ai_context: dict, dataset) -> None:
    st.markdown(
        f"""
        <div class="tg-hero">
            <h1>{APP_NAME}</h1>
            <p class="tg-hero-copy">{APP_TAGLINE}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_global_messages(dataset, ai_context: dict) -> None:
    components = ai_context.get("components", {})
    if components:
        status_parts = [
            f"risk scores: {components.get('risk_scores', 'unknown')}",
            f"explanations: {components.get('explanations', 'unknown')}",
            f"recommendations: {components.get('recommendations', 'unknown')}",
        ]
        status_text = "Current AI layer status - " + ", ".join(status_parts) + "."
    else:
        status_text = (
            "The HR dataset is loaded when available. Explanations and recommendations stay clearly labeled "
            "when they rely on demo logic."
        )

    with st.expander("View system status", expanded=False):
        st.caption(status_text)
        if dataset.is_mock:
            st.caption(dataset.message)
        elif ai_context["mode"] == "demo":
            st.caption("Fallback heuristic logic is currently active for missing model layers.")
        elif ai_context["mode"] == "hybrid":
            st.caption("Real model outputs are active with limited fallbacks on remaining layers.")


def section_header(title: str, description: str | None = None) -> None:
    st.markdown(
        f"""
        <div class="tg-section-title">{title}</div>
        {f'<div class="tg-section-copy">{description}</div>' if description else ''}
        """,
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, help_text: str | None = None) -> None:
    st.markdown(
        f"""
        <div class="tg-kpi">
            <div class="tg-kpi-label">{label}</div>
            <div class="tg-kpi-value">{value}</div>
            <div class="tg-card-body">{help_text or ''}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="tg-card">
            <div class="tg-card-title">{title}</div>
            <p class="tg-card-body">{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def notice(title: str, body: str, tone: str = "info") -> None:
    st.markdown(
        f"""
        <div class="tg-notice {tone}">
            <div class="tg-notice-title">{title}</div>
            <p class="tg-notice-body">{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def bullet_card(title: str, items: list[str]) -> None:
    items_html = "".join(f"<li>{item}</li>" for item in items)
    st.markdown(
        f"""
        <div class="tg-card">
            <div class="tg-card-title">{title}</div>
            <ul class="tg-list">{items_html}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def risk_color(level: str) -> str:
    return {"High": "#a15349", "Medium": "#8a6331", "Low": "#2f6b52"}.get(level, "#5d7189")


def render_risk_badge(level: str, score: float | None = None) -> None:
    numeric_score = pd.to_numeric(pd.Series([score]), errors="coerce").iloc[0]
    tone = level.lower() if isinstance(level, str) else "demo"
    text = f"{level} risk" if pd.isna(numeric_score) else f"{level} risk | {numeric_score:.0f}/100"
    st.markdown(f'<span class="tg-badge {tone}">{text}</span>', unsafe_allow_html=True)


def contribution_chart(explanations: list[dict]) -> go.Figure:
    factors = [item.get("factor", "Unknown").capitalize() for item in explanations] or ["No significant factor"]
    values = [item.get("contribution", 0) for item in explanations] or [0]
    colors = ["#bf6b60" if value > 0 else "#5e8f78" for value in values]
    fig = go.Figure(
        go.Bar(
            x=values,
            y=factors,
            orientation="h",
            marker_color=colors,
            text=[f"{value:+.0f}" for value in values],
            textposition="outside",
            hovertemplate="%{y}: %{x:+.0f}<extra></extra>",
        )
    )
    fig.update_layout(
        margin=dict(l=8, r=8, t=8, b=8),
        height=290,
        xaxis_title="Effect on demo risk score",
        yaxis_title="",
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
        font=dict(color="#10233a"),
    )
    fig.update_xaxes(gridcolor="rgba(207, 216, 227, 0.6)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0)")
    return fig


def style_plotly_figure(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(color="#10233a"),
        margin=dict(l=10, r=10, t=42, b=10),
        title_font=dict(size=16, color="#10233a"),
    )
    fig.update_xaxes(gridcolor="rgba(207, 216, 227, 0.6)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(207, 216, 227, 0.25)", zeroline=False)
    return fig


def empty_state(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="tg-card">
            <div class="tg-card-title">{title}</div>
            <p class="tg-card-body">{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def safe_download_dataframe(df: pd.DataFrame, label: str, filename: str) -> None:
    st.download_button(
        label=label,
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=filename,
        mime="text/csv",
        use_container_width=False,
    )


def footer_note(text: str) -> None:
    st.caption(text)
