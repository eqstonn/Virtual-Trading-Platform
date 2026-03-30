from supabase import create_client, Client
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def create_user_profile(user_id: str, username: str, email: str):
    """Create a new user profile in the database with initial balance"""
    try:
        profile = supabase.table("profiles").insert({
            "id": user_id,
            "username": username,
            "email": email,
            "cash_balance": 100000.00,  # Initial trading balance
            "created_at": datetime.utcnow().isoformat(),
        }).execute()
        return profile.data[0] if profile.data else None
    except Exception as e:
        print(f"Error creating user profile: {e}")
        return None

def get_user_profile(user_id: str):
    """Get user profile from database"""
    try:
        profile = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
        return profile.data
    except Exception as e:
        print(f"Error fetching profile: {e}")
        return None

def update_user_balance(user_id: str, new_balance: float):
    """Update user's cash balance"""
    try:
        result = supabase.table("profiles").update({"cash_balance": new_balance}).eq("id", user_id).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Error updating balance: {e}")
        return None

def get_all_trades(user_id: str):
    """Get all trades for a user"""
    try:
        trades = supabase.table("trades").select("*").eq("user_id", user_id).execute()
        return trades.data
    except Exception as e:
        print(f"Error fetching trades: {e}")
        return None

def create_trade(user_id: str, symbol: str, quantity: float, price: float, trade_type: str):
    """Record a new trade in the database"""
    try:
        trade = supabase.table("trades").insert({
            "user_id": user_id,
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
            "trade_type": trade_type,  # 'buy' or 'sell'
            "created_at": datetime.utcnow().isoformat(),
        }).execute()
        return trade.data[0] if trade.data else None
    except Exception as e:
        print(f"Error creating trade: {e}")
        return None
