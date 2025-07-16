from googlesearch import search

def find_analyst_reports(ticker: str, num_results: int = 10):
    """
    Finds analyst reports or articles related to a stock ticker.
    Returns a list of dictionaries with title and URL.
    """
    query = f"{ticker} analyst report site:icicidirect.com OR site:hdfcsec.com OR site:moneycontrol.com filetype:pdf"
    results = []

    try:
        for url in search(query, num_results=num_results):
            results.append({"title": url.split("/")[-1], "url": url})
    except Exception as e:
        return [{"title": "Error fetching reports", "url": str(e)}]

    return results
