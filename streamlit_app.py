"""Standalone Streamlit entry point for the AI Investment Workbench."""

import streamlit as st

from investment_workbench import render_investment_workbench


st.set_page_config(
    page_title="AI Investment Workbench",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("AI Investment Workbench")
st.caption(
    "A disciplined research system for turning an AI investment narrative "
    "into a falsifiable, monitored decision."
)
render_investment_workbench()
