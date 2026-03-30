from supabase import create_client, Client
from datetime import datetime
import os
from dotenv import load_dotenv
from database_service import create_user_profile, get_user_profile

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def sign_up(email: str, password: str, username: str):
    """Sign up a new user and create their profile"""
    try:
        # Create auth user
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {"data": {"username": username}}
        })
        
        if response.user:
            # Create user profile in database
            profile = create_user_profile(response.user.id, username, email)
            return {
                "user_id": response.user.id,
                "email": response.user.email,
                "username": username,
                "message": "Sign up successful"
            }
        return {"error": "Sign up failed"}
    except Exception as e:
        print(f"Sign up error: {e}")
        return {"error": str(e)}

def login(email: str, password: str):
    """Login user"""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if response.user:
            # Get user profile
            profile = get_user_profile(response.user.id)
            return {
                "user_id": response.user.id,
                "email": response.user.email,
                "username": profile.get("username") if profile else "User",
                "cash_balance": profile.get("cash_balance") if profile else 0,
                "message": "Login successful"
            }
        return {"error": "Login failed"}
    except Exception as e:
        print(f"Login error: {e}")
        return {"error": str(e)}

def get_session():
    """ Check if user is logged in """
    response = supabase.auth.get_user()
    return response.user if response else None

def sign_out():
    """ Sign out of current session """
    supabase.auth.sign_out()

def get_profile(user_id: str):
    """ Get users profile """
    profile = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
    return profile.data