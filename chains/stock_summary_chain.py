from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

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
    response = llm.predict(prompt)
    return {
        "recommendation": extract_section(response, "Recommendation"),
        "target_price": extract_section(response, "Target Price"),
        "thesis": extract_section(response, "Investment Thesis")
    }
