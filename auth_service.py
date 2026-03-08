from supabase import create_client, Client
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def sign_up(email: str, password: str, username: str):
    response = supabase.auth.sign_up({
        "email": email,
        "password": password,
        "options": {"data": {"username": username}}
    })
    return response

def login(email: str, password: str):
    response = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })
    return response

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