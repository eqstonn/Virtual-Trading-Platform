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