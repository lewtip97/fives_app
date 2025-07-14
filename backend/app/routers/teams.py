from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from generate_player_gameweek_stats import recalculate_player_gameweek_stats

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

class TeamStatsResponse(BaseModel):
    id: str
    team_id: str
    team_name: str
    gameweek: int
    season: str
    goals: int
    cumulative_goals: int
    created_at: str

# Replace all instances of user_id = "test-user-id" with the valid UUID
USER_ID = "00000000-0000-0000-0000-000000000000"

@router.post("/", response_model=TeamResponse)
def create_team(team: TeamCreate):
    """
    Create a new team for the current user.
    """
    try:
        user_id = USER_ID
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
        user_id = USER_ID
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
        user_id = USER_ID
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
        user_id = USER_ID
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
        user_id = USER_ID
        response = supabase.table("teams").delete().eq("id", team_id).eq("created_by", user_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Team not found")
        return {"message": "Team deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{team_id}/stats", response_model=List[TeamStatsResponse])
def get_team_stats(team_id: str, season: Optional[str] = None):
    """
    Get team statistics for a specific team, optionally filtered by season.
    """
    try:
        user_id = USER_ID
        team_check = supabase.table("teams").select("id").eq("id", team_id).eq("created_by", user_id).execute()
        if not team_check.data:
            raise HTTPException(status_code=404, detail="Team not found or access denied")
        query = supabase.table("team_stats").select("*").eq("team_id", team_id)
        if season:
            query = query.eq("season", season)
        response = query.order("gameweek").execute()
        return response.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/all", response_model=List[TeamStatsResponse])
def get_all_team_stats(season: Optional[str] = None):
    """
    Get team statistics for all teams of the current user, optionally filtered by season.
    """
    try:
        user_id = USER_ID
        teams_response = supabase.table("teams").select("id").eq("created_by", user_id).execute()
        team_ids = [team["id"] for team in teams_response.data]
        if not team_ids:
            return []
        query = supabase.table("team_stats").select("*").in_("team_id", team_ids)
        if season:
            query = query.eq("season", season)
        response = query.order("team_id, season, gameweek").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stats/recalculate/player-gameweek")
def trigger_player_gameweek_stats():
    """
    Trigger recalculation of player gameweek stats and write to the database.
    """
    try:
        recalculate_player_gameweek_stats()
        return {"status": "success", "message": "Player gameweek stats recalculated."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
