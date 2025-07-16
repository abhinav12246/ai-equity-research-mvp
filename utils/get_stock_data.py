import yfinance as yf

def fetch_key_ratios(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    ratios = {
        "P/E": info.get("trailingPE"),
        "ROE": info.get("returnOnEquity"),
        "Debt/Equity": info.get("debtToEquity"),
        "Market Cap": info.get("marketCap"),
    }
    return ratios
