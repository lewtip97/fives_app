from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

router = APIRouter(prefix="/opponents", tags=["opponents"])

USER_ID = "00000000-0000-0000-0000-000000000000"

class OpponentCreate(BaseModel):
    name: str
    team_id: str  # UUID

class OpponentResponse(BaseModel):
    id: str
    name: str
    team_id: str
    created_by: str
    created_at: str

@router.get("/", response_model=List[OpponentResponse])
def get_opponents(team_id: str):
    """
    List all opponents for a given team (and user).
    """
    try:
        response = supabase.table("opponents").select("*").eq("created_by", USER_ID).eq("team_id", team_id).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=OpponentResponse)
def create_opponent(opponent: OpponentCreate):
    try:
        response = supabase.table("opponents").insert({
            "name": opponent.name,
            "team_id": opponent.team_id,
            "created_by": USER_ID
        }).execute()
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to create opponent")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{opponent_id}", response_model=OpponentResponse)
def get_opponent(opponent_id: str):
    try:
        response = supabase.table("opponents").select("*").eq("id", opponent_id).eq("created_by", USER_ID).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Opponent not found")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{opponent_id}")
def delete_opponent(opponent_id: str):
    try:
        response = supabase.table("opponents").delete().eq("id", opponent_id).eq("created_by", USER_ID).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Opponent not found")
        return {"message": "Opponent deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 