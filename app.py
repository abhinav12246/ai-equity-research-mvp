import streamlit as st
from chains.stock_summary_chain import run_summary_chain
from chains.sentiment_chain import analyze_sentiment
from utils.extract_financials import parse_pdf_report
from utils.get_stock_data import fetch_key_ratios

st.set_page_config(page_title="AI Equity Research Assistant", layout="wide")
st.title("🧠 AI Equity Research Assistant")

ticker = st.text_input("Enter Stock Ticker (e.g., TCS)")
uploaded_file = st.file_uploader("Upload Analyst Report (PDF)", type=["pdf"])
yt_link = st.text_input("Optional: Paste YouTube Earnings Call Link")

if st.button("🔍 Analyze"):
    sentiment = "Neutral"
    if uploaded_file:
        report_text = parse_pdf_report(uploaded_file)
        sentiment = analyze_sentiment(report_text)
    elif yt_link:
        from utils.youtube_transcriber import get_transcript_from_youtube
        transcript = get_transcript_from_youtube(yt_link)
        sentiment = analyze_sentiment(transcript)

    ratios = fetch_key_ratios(ticker)
    ai_output = run_summary_chain(ticker=ticker, sentiment=sentiment, metrics=ratios)

    st.subheader("📌 Recommendation")
    st.markdown(ai_output["recommendation"])

    st.subheader("📈 Target Price")
    st.markdown(ai_output["target_price"])

    st.subheader("🧾 Investment Rationale")
    st.markdown(ai_output["thesis"])
