import yfinance as yf
import os
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("FINNHUB_KEY")

def get_current_price(ticker: str):
    """Fetches the current price from Finnhub, with yfinance fallback."""
    ticker = ticker.upper().strip()
    
    # Try Finnhub first
    if key:
        url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={key}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                
                # Check for API errors in response
                if 'error' in data:
                    print(f"Finnhub API error for {ticker}: {data['error']}")
                else:
                    # c is the key for current price
                    current_price = data.get('c')
                    
                    if current_price and current_price > 0:
                        return float(current_price)
        except requests.exceptions.RequestException as e:
            print(f"Finnhub connection error for {ticker}: {e}")
        except Exception as e:
            print(f"Finnhub error for {ticker}: {e}")
    else:
        print("Warning: FINNHUB_KEY not set in environment")
    
    # Fallback to yfinance
    try:
        print(f"Falling back to yfinance for {ticker}")
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        
        if not data.empty:
            current_price = data['Close'].iloc[-1]
            if current_price > 0:
                return float(current_price)
    except Exception as e:
        print(f"Yfinance error for {ticker}: {e}")
    
    print(f"Could not fetch price for {ticker} from any source")
    return None

def get_history(ticker: str, period = "1mo", interval = "1d"):
    """
    Fetches historical data from yfinance.
    Period options: 1d, 5d, 1mo, 3mo, 6mo, 1y, 5y, max
    Interval options: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
    """
    ticker = ticker.upper().strip()
    
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period = period, interval = interval)
        if data.empty:
            print(f"No historical data found for {ticker}")
            return None
        return data
    except Exception as e:
        print(f"Yfinance Error in fetching {ticker} history: {e}")
        return None

if __name__ == "__main__":
    # This only runs if you do: python market_data.py
    print("Testing get_current_price...")
    p = get_current_price("AAPL")
    print(f"AAPL Price: {p}")
    p = get_current_price("NVDA")
    print(f"NVDA Price: {p}")