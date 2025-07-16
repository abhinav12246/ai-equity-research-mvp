import streamlit as st
from chains.stock_summary_chain import run_summary_chain
from chains.sentiment_chain import analyze_sentiment
from utils.advanced_pdf_parser import parse_pdf_report_advanced as parse_pdf_report
from utils.get_stock_data import fetch_key_ratios
from utils.find_analyst_reports import find_analyst_reports

import requests
from io import BytesIO

st.set_page_config(page_title="AI Equity Research Assistant", layout="wide")
st.title("🧠 AI Equity Research Assistant")

ticker = st.text_input("Enter Stock Ticker (e.g., TCS)")
uploaded_file = st.file_uploader("Upload Analyst Report (PDF)", type=["pdf"])
yt_link = st.text_input("Optional: Paste YouTube Earnings Call Link")

if st.button("🔍 Analyze") and ticker:

    sentiment = "Neutral"
    report_text = ""

    # -----------------------------
    # 🧾 1. Use uploaded report if provided
    # -----------------------------
    if uploaded_file:
        report_text = parse_pdf_report(uploaded_file)
        insights = extract_insights_from_report(report_text)
        
        st.subheader("🧠 Analyst Insights")
        if "error" in insights:
            st.error(insights["error"])
        else:
            st.markdown(f"**🏦 Brokerage:** {insights['brokerage']}")
            st.markdown(f"**📌 Rating:** {insights['rating']}")
            st.markdown(f"**🎯 Target Price:** ₹{insights['target_price']}")
        
            st.markdown("**💡 Thesis**")
            for point in insights["thesis"]:
                st.markdown(f"- {point}")
        
            st.markdown("**⚠️ Risks**")
            for point in insights["risks"]:
                st.markdown(f"- {point}")

    # -----------------------------
    # 🌐 2. If no upload, fetch from internet
    # -----------------------------
    elif not uploaded_file:
        st.info("No PDF uploaded. Searching for analyst reports online...")
        reports = find_analyst_reports(ticker)
        if reports:
            first_report_url = reports[0]['url']
            st.markdown(f"Using online report: [{reports[0]['title']}]({first_report_url})")

            try:
                response = requests.get(first_report_url)
                if response.status_code == 200:
                    pdf_bytes = BytesIO(response.content)
                    from utils.storage import load_from_cache, save_to_cache, append_to_db
                    from utils.llm_report_extractor import extract_insights_from_report
                    
                    report_text = parse_pdf_report(pdf_bytes)
                    
                    # Check cache
                    cached = load_from_cache(ticker, report_text)
                    if cached:
                        insights = cached
                        st.info("✅ Loaded from cache")
                    else:
                        insights = extract_insights_from_report(report_text)
                        save_to_cache(ticker, report_text, insights)
                        append_to_db({
                            "ticker": ticker,
                            "brokerage": insights.get("brokerage"),
                            "rating": insights.get("rating"),
                            "target_price": insights.get("target_price"),
                            "thesis": insights.get("thesis"),
                            "risks": insights.get("risks"),
                        })

                    st.subheader("🧠 Analyst Insights")
                    if "error" in insights:
                        st.error(insights["error"])
                    else:
                        st.markdown(f"**🏦 Brokerage:** {insights['brokerage']}")
                        st.markdown(f"**📌 Rating:** {insights['rating']}")
                        st.markdown(f"**🎯 Target Price:** ₹{insights['target_price']}")
                    
                        st.markdown("**💡 Thesis**")
                        for point in insights["thesis"]:
                            st.markdown(f"- {point}")
                    
                        st.markdown("**⚠️ Risks**")
                        for point in insights["risks"]:
                            st.markdown(f"- {point}")
                else:
                    st.error("Failed to fetch the analyst report from the web.")
            except Exception as e:
                st.error(f"Error downloading PDF: {str(e)}")
        else:
            st.error("No analyst reports found online for this stock.")
            st.stop()

    # -----------------------------
    # 🧠 3. Use YouTube sentiment if provided
    # -----------------------------
    if yt_link:
        from utils.youtube_transcriber import get_transcript_from_youtube
        transcript = get_transcript_from_youtube(yt_link)
        sentiment = analyze_sentiment(transcript)
    else:
        sentiment = analyze_sentiment(report_text)

    ratios = fetch_key_ratios(ticker)
    ai_output = run_summary_chain(ticker=ticker, sentiment=sentiment, metrics=ratios)

    st.subheader("📌 Recommendation")
    st.markdown(ai_output["recommendation"])

    st.subheader("📈 Target Price")
    st.markdown(ai_output["target_price"])

    st.subheader("🧾 Investment Rationale")
    st.markdown(ai_output["thesis"])
