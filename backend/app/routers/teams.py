from fastapi import APIRouter, HTTPException, Request, Query, Depends
from pydantic import BaseModel
from typing import List, Optional
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from generate_player_gameweek_stats import recalculate_player_gameweek_stats
from generate_team_stats import main as recalculate_team_stats
from backend.app.auth import get_current_user_id

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

@router.post("/", response_model=TeamResponse)
def create_team(team: TeamCreate, user_id: str = Depends(get_current_user_id)):
    """
    Create a new team for the current user.
    """
    try:
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
def get_teams(user_id: str = Depends(get_current_user_id)):
    """
    Get all teams for the current user.
    """
    try:
        response = supabase.table("teams").select("*").eq("created_by", user_id).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{team_id}", response_model=TeamResponse)
def get_team(team_id: str, user_id: str = Depends(get_current_user_id)):
    """
    Get a specific team by ID.
    """
    try:
        response = supabase.table("teams").select("*").eq("id", team_id).eq("created_by", user_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Team not found")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{team_id}", response_model=TeamResponse)
def update_team(team_id: str, team: TeamCreate, user_id: str = Depends(get_current_user_id)):
    """
    Update a team's name.
    """
    try:
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
def delete_team(team_id: str, user_id: str = Depends(get_current_user_id)):
    """
    Delete a team.
    """
    try:
        response = supabase.table("teams").delete().eq("id", team_id).eq("created_by", user_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Team not found")
        return {"message": "Team deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{team_id}/stats", response_model=List[TeamStatsResponse])
def get_team_stats(team_id: str, season: Optional[str] = None, user_id: str = Depends(get_current_user_id)):
    """
    Get team statistics for a specific team, optionally filtered by season.
    """
    try:
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
def get_all_team_stats(season: Optional[str] = None, user_id: str = Depends(get_current_user_id)):
    """
    Get team statistics for all teams of the current user, optionally filtered by season.
    """
    try:
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
async def trigger_player_gameweek_stats(team_id: str = Query(..., description="Team ID to recalculate stats for"), user_id: str = Depends(get_current_user_id)):
    """
    Trigger recalculation of player gameweek stats for a specific team and write to the database.
    """
    try:
        recalculate_player_gameweek_stats(team_id=team_id)
        return {"status": "success", "message": f"Player gameweek stats recalculated for team {team_id}."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/stats/recalculate/team")
async def trigger_team_stats(team_id: str = Query(..., description="Team ID to recalculate stats for"), user_id: str = Depends(get_current_user_id)):
    """
    Trigger recalculation of team stats for a specific team and write to the database.
    """
    try:
        recalculate_team_stats(team_id=team_id)
        return {"status": "success", "message": f"Team stats recalculated for team {team_id}."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
