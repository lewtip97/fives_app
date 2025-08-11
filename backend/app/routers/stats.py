from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List, Optional
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from ..auth import get_current_user_id
from ..services.stats_generator import generate_all_stats, generate_player_gameweek_stats, generate_team_stats

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

router = APIRouter(prefix="/stats", tags=["stats"])

@router.post("/generate")
def generate_stats(team_id: Optional[str] = Query(None, description="Optional team ID to generate stats for specific team"), user_id: str = Depends(get_current_user_id)):
    """
    Generate player and team stats for all teams or a specific team.
    """
    try:
        result = generate_all_stats(team_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate/players")
def generate_player_stats(team_id: Optional[str] = Query(None, description="Optional team ID to generate stats for specific team"), user_id: str = Depends(get_current_user_id)):
    """
    Generate player gameweek stats.
    """
    try:
        result = generate_player_gameweek_stats(team_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate/teams")
def generate_team_stats_endpoint(team_id: Optional[str] = Query(None, description="Optional team ID to generate stats for specific team"), user_id: str = Depends(get_current_user_id)):
    """
    Generate team stats.
    """
    try:
        result = generate_team_stats(team_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/players/{team_id}")
def get_player_stats(team_id: str, user_id: str = Depends(get_current_user_id)):
    """
    Get player stats for a specific team.
    """
    try:
        response = supabase.table("player_gameweek_stats").select("*").eq("team_id", team_id).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/teams/{team_id}")
def get_team_stats(team_id: str, user_id: str = Depends(get_current_user_id)):
    """
    Get team stats for a specific team.
    """
    try:
        response = supabase.table("team_stats").select("*").eq("team_id", team_id).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/overview/{team_id}")
def get_team_overview(team_id: str, user_id: str = Depends(get_current_user_id)):
    """
    Get comprehensive team overview including matches, stats, and player data.
    """
    try:
        # Verify team belongs to user
        team_check = supabase.table("teams").select("id, name").eq("id", team_id).eq("created_by", user_id).execute()
        if not team_check.data:
            raise HTTPException(status_code=404, detail="Team not found or access denied")
        
        team = team_check.data[0]
        
        # Get all matches for this team with opponent names
        matches_response = supabase.table("matches").select("*, opponents(name)").eq("team_id", team_id).order("played_at", desc=True).execute()
        matches = matches_response.data
        
        # Calculate team statistics
        total_matches = len(matches)
        wins = sum(1 for match in matches if match["score1"] > match["score2"])
        draws = sum(1 for match in matches if match["score1"] == match["score2"])
        losses = sum(1 for match in matches if match["score1"] < match["score2"])
        win_percentage = wins / total_matches if total_matches > 0 else 0
        
        total_goals_scored = sum(match["score1"] for match in matches)
        total_goals_conceded = sum(match["score2"] for match in matches)
        
        # Get player stats
        player_stats_response = supabase.table("player_gameweek_stats").select("*").eq("team_id", team_id).execute()
        player_stats = player_stats_response.data
        
        # Get player names separately
        if player_stats:
            player_ids = list(set([stat["player_id"] for stat in player_stats]))
            players_response = supabase.table("players").select("id, name").in_("id", player_ids).execute()
            players = {p["id"]: p["name"] for p in players_response.data}
        else:
            players = {}
        
        # Calculate player totals
        player_totals = {}
        for stat in player_stats:
            player_id = stat["player_id"]
            if player_id not in player_totals:
                player_totals[player_id] = {
                    "player_id": player_id,
                    "player_name": players.get(player_id, "Unknown"),
                    "total_appearances": 0,
                    "total_goals": 0
                }
            player_totals[player_id]["total_appearances"] += 1
            player_totals[player_id]["total_goals"] += stat.get("goals", 0)
        
        return {
            "team": team,
            "total_matches": total_matches,
            "wins": wins,
            "draws": draws,
            "losses": losses,
            "win_percentage": win_percentage,
            "total_goals_scored": total_goals_scored,
            "total_goals_conceded": total_goals_conceded,
            "matches": matches,
            "player_stats": list(player_totals.values())
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 