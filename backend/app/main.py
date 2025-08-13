from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import teams, players, matches, opponents, stats
from supabase import create_client, Client
import os


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Supabase client first
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Then include routers
app.include_router(teams.router)
app.include_router(players.router)
app.include_router(matches.router)
app.include_router(opponents.router)
app.include_router(stats.router)


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