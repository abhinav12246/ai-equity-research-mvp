import os
from openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

LLM_PROMPT_TEMPLATE = """You are a financial analyst. Given the following text from an analyst report, extract the following fields:
- Rating (Buy/Sell/Hold)
- Target Price (in INR, if available)
- Investment Thesis (3 bullet points)
- Risks Mentioned (if any)
- Brokerage Firm Name (if available)

Please respond in this JSON format:
{{
  "rating": "...",
  "target_price": "...",
  "thesis": ["...", "...", "..."],
  "risks": ["..."],
  "brokerage": "..."
}}

Report text:
\"\"\"
{report_text}
\"\"\"
"""

llm = ChatOpenAI(temperature=0.3)

def extract_insights_from_report(report_text: str):
    prompt = LLM_PROMPT_TEMPLATE.format(report_text=report_text[:7000])  # truncate for token limits
    try:
        response = llm([HumanMessage(content=prompt)])
        return eval(response.content)  # response is JSON string
    except Exception as e:
        return {"error": str(e)}
