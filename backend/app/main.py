from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from app.routers import teams
from supabase import create_client, Client
import os


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
app = FastAPI()

app.include_router(teams.router)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


@app.get("/")
def read_root():
    return {"message": "Fives App API"}

@app.get("/appearances")
def get_appearances():
    try:
        response = supabase.table("appearances_all").select("*").execute()
        return {
            "data": response.data,
            "count": len(response.data) if response.data else 0,
            "status": "success"
        }
    except Exception as e:
        return {"error": str(e), "status": "error"}

@app.get("/goals")
def get_goals():
    try:
        response = supabase.table("goals_all").select("*").execute()
        return {
            "data": response.data,
            "count": len(response.data) if response.data else 0,
            "status": "success"
        }
    except Exception as e:
        return {"error": str(e), "status": "error"}

@app.get("/results")
def get_results():
    try:
        response = supabase.table("results_all").select("*").execute()
        return {
            "data": response.data,
            "count": len(response.data) if response.data else 0,
            "status": "success"
        }
    except Exception as e:
        return {"error": str(e), "status": "error"}