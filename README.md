# AI Equity Research MVP

This app mimics equity research analysts by ingesting analyst reports, earnings call transcripts, and stock data to generate AI-based buy/sell recommendations.

## Features
- Upload analyst reports (PDFs)
- Analyze earnings call YouTube links
- Fetch stock metrics
- Run LLM + FinBERT logic for sentiment + recommendation

## Setup
```bash
pip install -r requirements.txt
streamlit run app.py
```