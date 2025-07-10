from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

router = APIRouter(prefix="/teams", tags=["teams"])

# Pydantic models for request/response
class TeamCreate(BaseModel):
    name: str

class TeamResponse(BaseModel):
    id: str
    name: str
    created_by: str
    created_at: str

@router.post("/", response_model=TeamResponse)
def create_team(team: TeamCreate):
    """
    Create a new team for the current user.
    For now, we'll use a hardcoded user ID for testing.
    """
    try:
        # TODO: Replace with actual user ID from authentication
        user_id = "test-user-id"
        
        response = supabase.table("teams").insert({
            "name": team.name,
            "created_by": user_id,
            "created_at": "now()"
        }).execute()
        
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to create team")
        
        return response.data[0]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[TeamResponse])
def get_teams():
    """
    Get all teams for the current user.
    """
    try:
        # TODO: Replace with actual user ID from authentication
        user_id = "test-user-id"
        
        response = supabase.table("teams").select("*").eq("created_by", user_id).execute()
        
        return response.data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{team_id}", response_model=TeamResponse)
def get_team(team_id: str):
    """
    Get a specific team by ID.
    """
    try:
        # TODO: Replace with actual user ID from authentication
        user_id = "test-user-id"
        
        response = supabase.table("teams").select("*").eq("id", team_id).eq("created_by", user_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Team not found")
        
        return response.data[0]
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{team_id}", response_model=TeamResponse)
def update_team(team_id: str, team: TeamCreate):
    """
    Update a team's name.
    """
    try:
        # TODO: Replace with actual user ID from authentication
        user_id = "test-user-id"
        
        response = supabase.table("teams").update({
            "name": team.name
        }).eq("id", team_id).eq("created_by", user_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Team not found")
        
        return response.data[0]
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{team_id}")
def delete_team(team_id: str):
    """
    Delete a team.
    """
    try:
        # TODO: Replace with actual user ID from authentication
        user_id = "test-user-id"
        
        response = supabase.table("teams").delete().eq("id", team_id).eq("created_by", user_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Team not found")
        
        return {"message": "Team deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
