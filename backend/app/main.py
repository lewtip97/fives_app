from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware
from .routers import teams, players, matches, opponents, stats
from supabase import create_client, Client
import os


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
app = FastAPI()

# Allowed origins for CORS
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
]

# Custom CORS middleware to handle preflight requests
class CustomCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("origin")
        
        # Handle preflight OPTIONS requests
        if request.method == "OPTIONS":
            if origin in ALLOWED_ORIGINS:
                return Response(
                    status_code=200,
                    headers={
                        "Access-Control-Allow-Origin": origin,
                        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, HEAD, PATCH",
                        "Access-Control-Allow-Headers": "*",
                        "Access-Control-Allow-Credentials": "true",
                        "Access-Control-Max-Age": "600",
                    }
                )
        
        # Process the request
        response = await call_next(request)
        
        # Add CORS headers to the response
        if origin in ALLOWED_ORIGINS:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, HEAD, PATCH"
            response.headers["Access-Control-Allow-Headers"] = "*"
        
        return response

# Add custom CORS middleware
app.add_middleware(CustomCORSMiddleware)

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

@app.get("/health")
def health_check():
    """Health check endpoint for Docker and load balancers"""
    try:
        # Simple check that Supabase connection is working
        supabase.table("teams").select("id").limit(1).execute()
        return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e), "timestamp": "2024-01-01T00:00:00Z"}

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