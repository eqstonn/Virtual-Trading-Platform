import yfinance as yf
import os
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("FINNHUB_KEY")

def get_current_price(ticker: str):
    """Fetches the current price from Finnhub."""
    url = f"https://finnhub.io/api/v1/quote?symbol={ticker.upper()}&token={key}"
    try:
        response = requests.get(url)
        data = response.json()
        
        # c is letter for current price
        current_price = data.get('c')
        
        if current_price and current_price != 0:
            return float(current_price)
        return None
    except Exception as e:
        print(f"Finnhub Error for {ticker}: {e}")
        return None

def get_history(ticker: str, period = "1m", interval = "1d"):
    """
    Fetches historical data from yfinance.
    Period options: 1d, 5d, 1mo, 3mo, 6mo, 1y, 5y, max
    Interval options: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
    """

    try:
        stock = yf.Ticker(ticker.upper())
        data = stock.history(period = period, interval = interval)
        if data.empty:
            return None
        return data
    except Exception as e:
        print(f"Yfinance Error in fetching {ticker.upper()} history: {e}")
        return None

if __name__ == "__main__":
    # This only runs if you do: python market_data.py
    print("Testing get_current_price...")
    p = get_current_price("AAPL")
    print(f"Price: {p}")