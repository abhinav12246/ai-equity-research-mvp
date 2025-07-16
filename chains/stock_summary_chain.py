from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from openai import RateLimitError  # Add this at the top if not already imported

llm = ChatOpenAI(temperature=0.3)

template = PromptTemplate.from_template("""
You are a financial analyst. Given the metrics: {metrics} and sentiment: {sentiment}, write:
1. Buy/Sell/Hold Recommendation for {ticker}
2. Target Price
3. 3-bullet Investment Thesis
""")

def extract_section(text, keyword):
    lines = text.split("\n")
    for line in lines:
        if keyword.lower() in line.lower():
            return line
    return "Not found"

def run_summary_chain(ticker, sentiment, metrics):
    prompt = template.format(ticker=ticker, sentiment=sentiment, metrics=metrics)
    
    try:
        response = llm.predict(prompt)
        return {
            "recommendation": extract_section(response, "Recommendation"),
            "target_price": extract_section(response, "Target Price"),
            "thesis": extract_section(response, "Investment Thesis")
        }
    
    except RateLimitError:
        return {
            "recommendation": "⚠️ OpenAI API rate limit hit. Please wait and try again.",
            "target_price": "-",
            "thesis": "-"
        }

    except Exception as e:
        return {
            "recommendation": f"❌ Unexpected error: {str(e)}",
            "target_price": "-",
            "thesis": "-"
        }

