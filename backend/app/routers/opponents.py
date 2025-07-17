from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from backend.app.auth import get_current_user_id

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

router = APIRouter(prefix="/opponents", tags=["opponents"])

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
def get_opponents(user_id: str = Depends(get_current_user_id)):
    """
    List all opponents for a given team (and user).
    """
    try:
        response = supabase.table("opponents").select("*").eq("created_by", user_id).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=OpponentResponse)
def create_opponent(opponent: OpponentCreate, user_id: str = Depends(get_current_user_id)):
    try:
        response = supabase.table("opponents").insert({
            "name": opponent.name,
            "created_by": user_id,
            "created_at": "now()"
        }).execute()
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to create opponent")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{opponent_id}", response_model=OpponentResponse)
def get_opponent(opponent_id: str, user_id: str = Depends(get_current_user_id)):
    try:
        response = supabase.table("opponents").select("*").eq("id", opponent_id).eq("created_by", user_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Opponent not found")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{opponent_id}", response_model=OpponentResponse)
def update_opponent(opponent_id: str, opponent: OpponentCreate, user_id: str = Depends(get_current_user_id)):
    try:
        response = supabase.table("opponents").update({
            "name": opponent.name
        }).eq("id", opponent_id).eq("created_by", user_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Opponent not found")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{opponent_id}")
def delete_opponent(opponent_id: str, user_id: str = Depends(get_current_user_id)):
    try:
        response = supabase.table("opponents").delete().eq("id", opponent_id).eq("created_by", user_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Opponent not found")
        return {"message": "Opponent deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 