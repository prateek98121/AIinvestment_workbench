"""Decision-oriented company research workspace for the Streamlit app."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from typing import Any

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


DISCLAIMER = (
    "Educational research tool only. It does not provide investment, tax, or "
    "legal advice. Verify company facts, market data, and filings independently."
)

DIMENSIONS = {
    "Business quality": 0.20,
    "Durable advantage": 0.20,
    "Financial resilience": 0.15,
    "Management & allocation": 0.10,
    "Valuation & return": 0.20,
    "Risk & uncertainty": 0.15,
}


@dataclass(frozen=True)
class CompanyTemplate:
    ticker: str
    company: str
    role: str
    thesis: str
    why_now: str
    variant_view: str
    moat: str
    risks: str
    disconfirming: str
    watch: str
    scores: dict[str, int]


TEMPLATES = {
    "Blank company": CompanyTemplate(
        ticker="",
        company="",
        role="Define where this company sits in the value chain.",
        thesis="State the investment thesis in one falsifiable sentence.",
        why_now="What has changed, and why does the opportunity exist now?",
        variant_view="What does the market misunderstand or underweight?",
        moat="What protects returns on capital from competition?",
        risks="List the two or three ways permanent capital loss could occur.",
        disconfirming="What evidence would prove the thesis wrong?",
        watch="Name leading indicators, filing metrics, and decision dates.",
        scores={dimension: 5 for dimension in DIMENSIONS},
    ),
    "Lam Research (LRCX)": CompanyTemplate(
        ticker="LRCX",
        company="Lam Research",
        role="Semiconductor wafer-fabrication equipment; an enabling layer of AI compute capacity.",
        thesis=(
            "AI infrastructure growth can increase demand for advanced memory and logic "
            "manufacturing intensity, while process complexity supports the value of "
            "specialised deposition and etch tools."
        ),
        why_now=(
            "Use this as a research hypothesis: test whether current expectations already "
            "price in the memory recovery and sustained AI-related capital spending."
        ),
        variant_view=(
            "The debate is not simply whether AI grows; it is whether wafer-fab equipment "
            "intensity and Lam's share of process steps grow faster than expectations."
        ),
        moat=(
            "Installed base, process expertise, customer qualification, service relationships, "
            "and the cost of failure in advanced manufacturing may create switching friction."
        ),
        risks=(
            "Semiconductor capital-spending cycles; customer concentration; export controls; "
            "technology or share loss; paying a peak multiple on peak earnings."
        ),
        disconfirming=(
            "Sustained share loss in critical process steps, weaker service economics, or "
            "equipment spending that rises without corresponding revenue and margin capture."
        ),
        watch=(
            "Memory and foundry capex, advanced-node mix, installed-base/service growth, gross "
            "margin, China exposure, customer concentration, and valuation versus mid-cycle earnings."
        ),
        scores={
            "Business quality": 8,
            "Durable advantage": 8,
            "Financial resilience": 7,
            "Management & allocation": 7,
            "Valuation & return": 5,
            "Risk & uncertainty": 5,
        },
    ),
    "Equinix (EQIX)": CompanyTemplate(
        ticker="EQIX",
        company="Equinix",
        role="Global data-centre and interconnection platform; digital infrastructure for distributed workloads.",
        thesis=(
            "Dense ecosystems of networks, clouds, and enterprises can reinforce interconnection "
            "advantages, while AI and hybrid-cloud workloads may support long-duration demand."
        ),
        why_now=(
            "Test whether power constraints, financing costs, and required development capital "
            "create a temporary valuation gap or a structurally lower-return regime."
        ),
        variant_view=(
            "The key question is whether ecosystem density and interconnection economics matter "
            "more than raw data-centre capacity as AI workloads scale."
        ),
        moat=(
            "Network density, customer ecosystems, switching costs, scarce locations and power, "
            "global reach, and operational reliability may reinforce one another."
        ),
        risks=(
            "Leverage and refinancing; high capital intensity; power availability; competition; "
            "customer optimisation; development returns below the cost of capital."
        ),
        disconfirming=(
            "Weakening interconnection growth, falling returns on new capacity, leverage rising "
            "without per-share cash-flow growth, or customers treating capacity as commoditised."
        ),
        watch=(
            "Recurring revenue, interconnection growth, churn, utilisation, development yield, "
            "AFFO per share, leverage, financing cost, power pipeline, and valuation."
        ),
        scores={
            "Business quality": 8,
            "Durable advantage": 8,
            "Financial resilience": 6,
            "Management & allocation": 7,
            "Valuation & return": 5,
            "Risk & uncertainty": 5,
        },
    ),
}


def _state_key(field: str) -> str:
    return f"workbench_{field}"


def _load_template(name: str) -> None:
    template = TEMPLATES[name]
    for field in (
        "ticker", "company", "role", "thesis", "why_now", "variant_view",
        "moat", "risks", "disconfirming", "watch",
    ):
        st.session_state[_state_key(field)] = getattr(template, field)
    for dimension, score in template.scores.items():
        st.session_state[_state_key(f"score_{dimension}")] = score
    st.session_state[_state_key("loaded_template")] = name


def _ensure_template(name: str) -> None:
    if st.session_state.get(_state_key("loaded_template")) != name:
        _load_template(name)


def _scorecard() -> tuple[pd.DataFrame, float]:
    rows = []
    total = 0.0
    for dimension, weight in DIMENSIONS.items():
        score = st.slider(
            dimension,
            min_value=1,
            max_value=10,
            value=TEMPLATES["Blank company"].scores[dimension],
            key=_state_key(f"score_{dimension}"),
            help="1 is weak/unattractive; 10 is exceptional/attractive.",
        )
        contribution = score * weight
        total += contribution
        rows.append(
            {
                "Dimension": dimension,
                "Score": score,
                "Weight": weight,
                "Weighted score": contribution,
            }
        )
    return pd.DataFrame(rows), total


def _radar_chart(scorecard: pd.DataFrame) -> go.Figure:
    categories = scorecard["Dimension"].tolist()
    values = scorecard["Score"].tolist()
    figure = go.Figure(
        go.Scatterpolar(
            r=values + values[:1],
            theta=categories + categories[:1],
            fill="toself",
            line={"color": "#2563EB", "width": 3},
            fillcolor="rgba(37, 99, 235, 0.18)",
            hovertemplate="%{theta}: %{r}/10<extra></extra>",
        )
    )
    figure.update_layout(
        height=430,
        margin={"l": 45, "r": 45, "t": 30, "b": 30},
        polar={
            "radialaxis": {"visible": True, "range": [0, 10], "dtick": 2},
            "angularaxis": {"direction": "clockwise"},
        },
        showlegend=False,
    )
    return figure


def _scenario_inputs() -> list[dict[str, Any]]:
    st.markdown("#### Scenario discipline")
    st.caption(
        "Use your own verified price and per-share value estimates. Probabilities must sum to 100%."
    )
    current_price = st.number_input(
        "Current share price",
        min_value=0.0,
        value=100.0,
        step=1.0,
        key=_state_key("current_price"),
    )
    scenarios = []
    defaults = [("Bear", 25, 70.0), ("Base", 50, 120.0), ("Bull", 25, 170.0)]
    columns = st.columns(3)
    for column, (label, probability, value) in zip(columns, defaults):
        with column:
            st.markdown(f"**{label} case**")
            probability_value = st.number_input(
                "Probability (%)",
                min_value=0,
                max_value=100,
                value=probability,
                step=5,
                key=_state_key(f"{label}_probability"),
            )
            estimated_value = st.number_input(
                "Estimated value/share",
                min_value=0.0,
                value=value,
                step=1.0,
                key=_state_key(f"{label}_value"),
            )
            assumption = st.text_area(
                "Critical assumptions",
                placeholder="Growth, margins, multiple, balance sheet...",
                key=_state_key(f"{label}_assumption"),
                height=110,
            )
            scenarios.append(
                {
                    "Scenario": label,
                    "Probability": probability_value,
                    "Value/share": estimated_value,
                    "Return": ((estimated_value / current_price) - 1) if current_price else 0,
                    "Critical assumptions": assumption,
                }
            )
    return scenarios


def _build_memo(
    scorecard: pd.DataFrame,
    total_score: float,
    scenarios: list[dict[str, Any]],
) -> str:
    get = lambda field: st.session_state.get(_state_key(field), "")
    probability_total = sum(item["Probability"] for item in scenarios)
    expected_value = sum(
        item["Value/share"] * item["Probability"] / 100 for item in scenarios
    )
    lines = [
        f"# Investment decision memo — {get('company') or 'Untitled company'} ({get('ticker') or 'N/A'})",
        "",
        f"_Prepared {date.today().isoformat()}_",
        "",
        "## Decision snapshot",
        "",
        f"- Weighted mental-model score: **{total_score:.1f}/10**",
        f"- Probability-weighted value/share: **{expected_value:,.2f}**",
        f"- Scenario probability check: **{probability_total}%**",
        "",
        "## Role in the AI value chain",
        "",
        get("role"),
        "",
        "## Core thesis",
        "",
        get("thesis"),
        "",
        "## Why now",
        "",
        get("why_now"),
        "",
        "## Variant perception",
        "",
        get("variant_view"),
        "",
        "## Durable advantage",
        "",
        get("moat"),
        "",
        "## Principal risks",
        "",
        get("risks"),
        "",
        "## What would change my mind",
        "",
        get("disconfirming"),
        "",
        "## Monitoring and exit triggers",
        "",
        get("watch"),
        "",
        "## Mental-model scorecard",
        "",
        scorecard.to_markdown(index=False, floatfmt=".2f"),
        "",
        "## Scenarios",
        "",
        pd.DataFrame(scenarios).to_markdown(index=False, floatfmt=".2f"),
        "",
        "## Evidence log",
        "",
        get("evidence_log") or "Add dated primary-source evidence here.",
        "",
        f"> {DISCLAIMER}",
    ]
    return "\n".join(lines)


def render_investment_workbench() -> None:
    """Render a repeatable, falsifiable company-research workflow."""

    st.subheader("Investment Workbench")
    st.caption(
        "Turn mental models into a decision: frame the thesis, score the business, "
        "quantify scenarios, record evidence, and define what would change your mind."
    )

    template_name = st.selectbox(
        "Start with a research template",
        options=list(TEMPLATES),
        key=_state_key("template_selector"),
    )
    _ensure_template(template_name)

    identity_one, identity_two = st.columns([1, 2])
    identity_one.text_input("Ticker", key=_state_key("ticker"))
    identity_two.text_input("Company", key=_state_key("company"))

    thesis_tab, score_tab, scenario_tab, evidence_tab, memo_tab = st.tabs(
        ["Thesis", "Scorecard", "Scenarios", "Evidence & triggers", "Decision memo"]
    )

    with thesis_tab:
        st.text_area("Role in the AI value chain", key=_state_key("role"), height=100)
        st.text_area("Core thesis", key=_state_key("thesis"), height=130)
        first, second = st.columns(2)
        first.text_area("Why now?", key=_state_key("why_now"), height=150)
        second.text_area("Variant perception", key=_state_key("variant_view"), height=150)
        st.text_area("Durable advantage / moat", key=_state_key("moat"), height=130)

    with score_tab:
        left, right = st.columns([1, 1])
        with left:
            scorecard, total_score = _scorecard()
            st.metric("Weighted score", f"{total_score:.1f} / 10")
            st.caption(
                "A score is a forcing function, not a recommendation. Record the evidence behind each number."
            )
        with right:
            st.plotly_chart(_radar_chart(scorecard), width="stretch")

    with scenario_tab:
        scenarios = _scenario_inputs()
        probability_total = sum(item["Probability"] for item in scenarios)
        expected_value = sum(
            item["Value/share"] * item["Probability"] / 100 for item in scenarios
        )
        first, second = st.columns(2)
        first.metric("Probability total", f"{probability_total}%")
        second.metric("Probability-weighted value/share", f"{expected_value:,.2f}")
        if probability_total != 100:
            st.warning("Scenario probabilities must sum to 100%.")

    with evidence_tab:
        st.text_area("Principal risks", key=_state_key("risks"), height=130)
        st.text_area(
            "What would change my mind?",
            key=_state_key("disconfirming"),
            height=130,
        )
        st.text_area(
            "Monitoring and exit triggers",
            key=_state_key("watch"),
            height=130,
        )
        st.text_area(
            "Dated evidence log",
            key=_state_key("evidence_log"),
            placeholder=(
                "2026-08-24 — 10-Q — Claim supported or contradicted — link\n"
                "2026-08-24 — Earnings call — Metric or management statement — link"
            ),
            height=180,
        )
        st.info(
            "Prefer primary sources: SEC filings, investor-relations materials, "
            "earnings transcripts, and official regulatory disclosures."
        )

    with memo_tab:
        memo = _build_memo(scorecard, total_score, scenarios)
        st.markdown(memo)
        filename_ticker = st.session_state.get(_state_key("ticker"), "company") or "company"
        st.download_button(
            "Download decision memo",
            data=memo,
            file_name=f"{filename_ticker.lower()}_decision_memo.md",
            mime="text/markdown",
            width="stretch",
        )
        state_payload = {
            key.removeprefix("workbench_"): value
            for key, value in st.session_state.items()
            if key.startswith("workbench_")
        }
        st.download_button(
            "Download editable research data",
            data=json.dumps(state_payload, indent=2, default=str),
            file_name=f"{filename_ticker.lower()}_research.json",
            mime="application/json",
            width="stretch",
        )

    st.divider()
    st.caption(DISCLAIMER)
