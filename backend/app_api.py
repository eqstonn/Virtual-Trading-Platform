from auth_service import sign_up, login, get_session, sign_out, get_profile, supabase
from trading_service import buy_stock, sell_stock
from market_data import get_current_price, get_history
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models for JSON body validation
class SignUpRequest(BaseModel):
    email: str
    password: str
    username: str

class LoginRequest(BaseModel):
    email: str
    password: str

class TradeRequest(BaseModel):
    user_id: str
    ticker: str
    shares: int
    price: float

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/sign_up")
def api_sign_up(request: SignUpRequest):
    result = sign_up(request.email, request.password, request.username)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/login")
def api_login(request: LoginRequest):
    result = login(request.email, request.password)
    if "error" in result:
        raise HTTPException(status_code=401, detail=result["error"])
    return result

@app.post("/signout")
def api_sign_out():
    sign_out()
    return {"status": "sucess", "detail": "logged out"}

@app.get("/session")
def api_get_session():
    user = get_session()
    if not user:
        raise HTTPException(status_code = 401, detail = "No active session found")
    return {"user_id": user.id, "email": user.email}

@app.get("/profile/{user_id}")
def api_get_profile(user_id: str):
    profile = get_profile(user_id)
    if not profile:
        raise HTTPException(status_code = 404, detail = "No profile exist")
    return profile

@app.get("/holdings/{user_id}")
def api_get_holdings(user_id: str):
    try:
        holdings = supabase.table("holdings").select("*").eq("user_id", user_id).execute()
        if holdings.data:
            return holdings.data
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching holdings: {str(e)}")

@app.get("/stock-price/{ticker}")
def api_get_stock_price(ticker: str):
    try:
        price = get_current_price(ticker)
        if price is None:
            raise HTTPException(status_code=404, detail=f"Could not fetch price for {ticker}. Please check the ticker symbol.")
        return {"ticker": ticker, "price": price}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Exception in stock-price endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching price for {ticker}: {str(e)}")

@app.get("/stock-history/{ticker}")
def api_get_stock_history(ticker: str, period: str = "1mo", interval: str = "1d"):
    try:
        history = get_history(ticker, period, interval)
        if history is None:
            raise HTTPException(status_code=404, detail=f"Could not fetch history for {ticker}. Please check the ticker symbol.")
        
        # Convert to list format for JSON serialization
        data = []
        for date, row in history.iterrows():
            data.append({
                "date": str(date.date()),
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": int(row["Volume"]),
            })
        return {"ticker": ticker, "data": data}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Exception in stock-history endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching history for {ticker}: {str(e)}")

@app.post("/trade/buy")
def api_buy_stock(request: TradeRequest):
    try:
        result = buy_stock(request.user_id, request.ticker, request.shares, request.price)
        if not result.get("Success", False):
            raise HTTPException(status_code=400, detail=result.get("Detail", "Trade failed"))
        return result
    except HTTPException:
        raise
    except Exception as e:
        print(f"Exception in buy trade endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error executing buy trade: {str(e)}")

@app.post("/trade/sell")
def api_sell_stock(request: TradeRequest):
    try:
        result = sell_stock(request.user_id, request.ticker, request.shares, request.price)
        if not result.get("Success", False):
            raise HTTPException(status_code=400, detail=result.get("Detail", "Trade failed"))
        return result
    except HTTPException:
        raise
    except Exception as e:
        print(f"Exception in sell trade endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error executing sell trade: {str(e)}")