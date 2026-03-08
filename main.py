from supabase import create_client, Client
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

try:
    data = {
        "title": "First proj",
        "content": "First post using supabase and python",
        "created_at": datetime.now().isoformat()
        }    
    
    test = supabase.table("posts").select("id").limit(1).execute()
    print("Connection successful! Sample data: ", test.data)

    response = supabase.table("posts").insert(data).execute()
    print("reponse succesfully added", response.data)

except Exception as e:
    print("Connetion failed:", e)