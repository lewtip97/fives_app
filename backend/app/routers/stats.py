from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List, Optional
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from ..auth import get_current_user_id
from ..services.stats_generator import generate_all_stats, generate_player_gameweek_stats, generate_team_stats
from ..services.prediction_service import prediction_service
from ..services.activity_tracker import activity_tracker

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
        
        # Get player stats from appearances table (correct source for appearances and goals)
        # First get all matches for this team, then get appearances for those matches
        match_ids = [match["id"] for match in matches]
        
        if not match_ids:
            return {"team_id": team_id, "player_stats": []}
        
        # Get all appearances for these matches
        appearances = supabase.table('appearances').select('*').in_('match_id', match_ids).execute()
        
        if not appearances.data:
            return {"team_id": team_id, "player_stats": []}
        
        # Process appearances to get player totals
        player_totals = {}
        
        for appearance in appearances.data:
            player_id = appearance['player_id']
            
            if player_id not in player_totals:
                player_totals[player_id] = {
                    'player_id': player_id,
                    'total_appearances': 0,
                    'total_goals': 0,
                    'total_assists': 0,
                    'total_clean_sheets': 0,
                    'total_yellow_cards': 0,
                    'total_red_cards': 0
                }
            
            # Count this appearance
            player_totals[player_id]['total_appearances'] += 1
            
            # Add stats
            player_totals[player_id]['total_goals'] += appearance.get('goals', 0)
            player_totals[player_id]['total_assists'] += appearance.get('assists', 0)
            player_totals[player_id]['total_clean_sheets'] += appearance.get('clean_sheets', 0)
            player_totals[player_id]['total_yellow_cards'] += appearance.get('yellow_cards', 0)
            player_totals[player_id]['total_red_cards'] += appearance.get('red_cards', 0)
        
        # Convert to list and add player names
        player_stats = []
        for player_id, totals in player_totals.items():
            # Get player name
            player = supabase.table('players').select('name').eq('id', player_id).execute()
            if player.data:
                totals['player_name'] = player.data[0]['name']
                player_stats.append(totals)
        
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
            "player_stats": player_stats
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/player/{player_id}")
def get_individual_player_stats(player_id: str, user_id: str = Depends(get_current_user_id)):
    """
    Get comprehensive stats for an individual player.
    """
    try:
        # Verify player belongs to user
        player_check = supabase.table("players").select("id, name, team_id, profile_picture").eq("id", player_id).eq("created_by", user_id).execute()
        if not player_check.data:
            raise HTTPException(status_code=404, detail="Player not found or access denied")
        
        player = player_check.data[0]
        team_id = player["team_id"]
        
        # Get all appearances for this player
        appearances_response = supabase.table("appearances").select("*, matches(score1, score2, played_at, opponents(name))").eq("player_id", player_id).execute()
        appearances = appearances_response.data
        
        # Get all matches where this player appeared
        matches = []
        for appearance in appearances:
            if appearance.get("matches"):
                match = appearance["matches"]
                match["goals"] = appearance.get("goals", 0)
                matches.append(match)
        
        # Calculate basic stats
        total_appearances = len(appearances)
        total_goals = sum(appearance.get("goals", 0) for appearance in appearances)
        goals_per_game = total_goals / total_appearances if total_appearances > 0 else 0
        
        # Calculate team performance when player plays
        team_wins = 0
        team_draws = 0
        team_losses = 0
        team_goals_scored = 0
        team_goals_conceded = 0
        
        for match in matches:
            score1 = match.get("score1", 0)
            score2 = match.get("score2", 0)
            team_goals_scored += score1
            team_goals_conceded += score2
            
            if score1 > score2:
                team_wins += 1
            elif score1 == score2:
                team_draws += 1
            else:
                team_losses += 1
        
        total_team_matches = len(matches)
        win_rate = team_wins / total_team_matches if total_team_matches > 0 else 0
        avg_goals_scored = team_goals_scored / total_team_matches if total_team_matches > 0 else 0
        avg_goals_conceded = team_goals_conceded / total_team_matches if total_team_matches > 0 else 0
        
        # Get goals over time for charting
        goals_over_time = []
        for match in sorted(matches, key=lambda x: x.get("played_at", "")):
            goals_over_time.append({
                "date": match.get("played_at"),
                "goals": match.get("goals", 0),
                "opponent": match.get("opponents", {}).get("name", "Unknown") if match.get("opponents") else "Unknown"
            })
        
        # Calculate form (last 5 games)
        recent_matches = sorted(matches, key=lambda x: x.get("played_at", ""), reverse=True)[:5]
        form = []
        for match in recent_matches:
            score1 = match.get("score1", 0)
            score2 = match.get("score2", 0)
            if score1 > score2:
                form.append("W")
            elif score1 == score2:
                form.append("D")
            else:
                form.append("L")
        
        return {
            "player": player,
            "total_appearances": total_appearances,
            "total_goals": total_goals,
            "goals_per_game": goals_per_game,
            "win_rate": win_rate,
            "avg_goals_scored_when_playing": avg_goals_scored,
            "avg_goals_conceded_when_playing": avg_goals_conceded,
            "goals_over_time": goals_over_time,
            "form": form,
            "recent_matches": recent_matches
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict")
def predict_match_outcome(
    team_id: str,
    opponent_id: str,
    selected_players: List[str],
    user_id: str = Depends(get_current_user_id)
):
    """
    Predict match outcome and player performance for a specific match.
    """
    try:
        # Verify team belongs to user
        team_check = supabase.table("teams").select("id, name").eq("id", team_id).eq("created_by", user_id).execute()
        if not team_check.data:
            raise HTTPException(status_code=404, detail="Team not found or access denied")
        
        # Generate prediction using the ML models
        prediction = prediction_service.predict_match_outcome(team_id, opponent_id, selected_players)
        
        return prediction
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recent-activities")
def get_recent_activities(user_id: str = Depends(get_current_user_id)):
    """
    Get recent activities for the home page including matches, milestones, and team changes.
    """
    try:
        activities = activity_tracker.get_recent_activities(user_id, limit=10)
        return activities
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test-activities")
def test_activities():
    """
    Test endpoint to verify the activity tracker is working.
    """
    try:
        # Test with a dummy user ID
        test_user_id = "00000000-0000-0000-0000-000000000000"
        activities = activity_tracker.get_recent_activities(test_user_id, limit=5)
        return {
            "status": "success",
            "message": "Activity tracker is working",
            "activities_count": len(activities),
            "activities": activities
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "message": str(e),
            "activities_count": 0,
            "activities": []
        }
