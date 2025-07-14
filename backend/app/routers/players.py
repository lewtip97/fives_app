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

router = APIRouter(prefix="/players", tags=["players"])

# Pydantic models
class PlayerCreate(BaseModel):
    name: str
    team_id: str

class PlayerResponse(BaseModel):
    id: str
    name: str
    team_id: str
    created_by: str
    created_at: str

USER_ID = "00000000-0000-0000-0000-000000000000"

@router.post("/", response_model=PlayerResponse)
def create_player(player: PlayerCreate):
    try:
        response = supabase.table("players").insert({
            "name": player.name,
            "team_id": player.team_id,
            "created_by": USER_ID,
            "created_at": "now()"
        }).execute()
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to create player")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[PlayerResponse])
def get_players():
    try:
        response = supabase.table("players").select("*").eq("created_by", USER_ID).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{player_id}", response_model=PlayerResponse)
def get_player(player_id: str):
    try:
        response = supabase.table("players").select("*").eq("id", player_id).eq("created_by", USER_ID).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Player not found")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{player_id}", response_model=PlayerResponse)
def update_player(player_id: str, player: PlayerCreate):
    try:
        response = supabase.table("players").update({
            "name": player.name,
            "team_id": player.team_id
        }).eq("id", player_id).eq("created_by", USER_ID).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Player not found")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{player_id}")
def delete_player(player_id: str):
    try:
        response = supabase.table("players").delete().eq("id", player_id).eq("created_by", USER_ID).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Player not found")
        return {"message": "Player deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
