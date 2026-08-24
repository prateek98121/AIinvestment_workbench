# AI Investment Workbench

A standalone Streamlit app for turning an investment narrative into a repeatable, falsifiable decision process.

## What it does

- starts with editable Lam Research (LRCX) and Equinix (EQIX) research templates;
- frames the company's role in the AI value chain, thesis, timing, and variant view;
- scores business quality, durable advantage, financial resilience, management, valuation, and risk;
- calculates bull, base, and bear probability-weighted scenarios;
- captures disconfirming evidence, monitoring metrics, and exit triggers;
- maintains a dated evidence log;
- exports a Markdown decision memo and editable JSON research file.

The example templates are hypotheses to investigate, not current recommendations. The app contains no personal portfolio values.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

## Deploy on Streamlit Community Cloud

Create a new Streamlit app with:

- repository: `pkot98121/AIinvestment_workbench`
- branch: `main` after this change is merged
- entry point: `streamlit_app.py`

No API keys or secrets are required.

## Research discipline

Scores are forcing functions, not recommendations. Verify company facts, prices, financial metrics, and management statements with primary sources such as SEC filings, investor-relations releases, earnings materials, and official regulatory disclosures.

This project is an educational research tool. It does not provide investment, tax, or legal advice.
