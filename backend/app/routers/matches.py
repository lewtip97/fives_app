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

router = APIRouter(prefix="/matches", tags=["matches"])

class AppearanceIn(BaseModel):
    player_id: str
    goals: int

class MatchFullIn(BaseModel):
    team_id: str
    opponent_name: str
    season: str
    played_at: str  # ISO date string
    gameweek: int
    score1: int
    score2: int
    appearances: List[AppearanceIn]

@router.post("/full")
def create_full_match(match: MatchFullIn, user_id: str = Depends(get_current_user_id)):
    try:
        # 1. Find or create opponent for this user
        opponent_resp = supabase.table("opponents").select("id").eq("name", match.opponent_name).eq("created_by", user_id).execute()
        if opponent_resp.data:
            opponent_id = opponent_resp.data[0]["id"]
        else:
            new_opp_resp = supabase.table("opponents").insert({
                "name": match.opponent_name,
                "created_by": user_id,
                "created_at": "now()"
            }).execute()
            if not new_opp_resp.data:
                raise HTTPException(status_code=400, detail="Failed to create opponent")
            opponent_id = new_opp_resp.data[0]["id"]

        # 2. Create the match
        match_resp = supabase.table("matches").insert({
            "team_id": match.team_id,
            "opponent_id": opponent_id,
            "score1": match.score1,
            "score2": match.score2,
            "gameweek": match.gameweek,
            "season": match.season,
            "played_at": match.played_at,
            "created_by": user_id,
            "created_at": "now()"
        }).execute()
        if not match_resp.data:
            raise HTTPException(status_code=400, detail="Failed to create match")
        match_id = match_resp.data[0]["id"]

        # 3. Create appearances
        for app in match.appearances:
            app_resp = supabase.table("appearances").insert({
                "match_id": match_id,
                "player_id": app.player_id,
                "goals": app.goals,
                "created_at": "now()"
            }).execute()
            if not app_resp.data:
                raise HTTPException(status_code=400, detail=f"Failed to create appearance for player {app.player_id}")

        return {"message": "Match, opponent, and appearances created successfully", "match_id": match_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/full/{match_id}")
def update_full_match(match_id: str, match: MatchFullIn, user_id: str = Depends(get_current_user_id)):
    try:
        # 1. Verify the match belongs to this user
        match_check = supabase.table("matches").select("id").eq("id", match_id).eq("created_by", user_id).execute()
        if not match_check.data:
            raise HTTPException(status_code=404, detail="Match not found or access denied")

        # 2. Find or create opponent for this user
        opponent_resp = supabase.table("opponents").select("id").eq("name", match.opponent_name).eq("created_by", user_id).execute()
        if opponent_resp.data:
            opponent_id = opponent_resp.data[0]["id"]
        else:
            new_opp_resp = supabase.table("opponents").insert({
                "name": match.opponent_name,
                "created_by": user_id,
                "created_at": "now()"
            }).execute()
            if not new_opp_resp.data:
                raise HTTPException(status_code=400, detail="Failed to create opponent")
            opponent_id = new_opp_resp.data[0]["id"]

        # 3. Update the match
        match_resp = supabase.table("matches").update({
            "team_id": match.team_id,
            "opponent_id": opponent_id,
            "score1": match.score1,
            "score2": match.score2,
            "gameweek": match.gameweek,
            "season": match.season,
            "played_at": match.played_at
        }).eq("id", match_id).eq("created_by", user_id).execute()
        if not match_resp.data:
            raise HTTPException(status_code=404, detail="Failed to update match")

        # 4. Delete existing appearances for this match
        supabase.table("appearances").delete().eq("match_id", match_id).execute()

        # 5. Create new appearances
        for app in match.appearances:
            app_resp = supabase.table("appearances").insert({
                "match_id": match_id,
                "player_id": app.player_id,
                "goals": app.goals,
                "created_at": "now()"
            }).execute()
            if not app_resp.data:
                raise HTTPException(status_code=400, detail=f"Failed to create appearance for player {app.player_id}")

        return {"message": "Match, opponent, and appearances updated successfully", "match_id": match_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Response models for GET endpoints
class MatchResponse(BaseModel):
    id: str
    team_id: str
    opponent_id: str
    score1: int
    score2: int
    gameweek: int
    season: str
    played_at: str
    created_by: str
    created_at: str

class MatchWithDetailsResponse(BaseModel):
    id: str
    team_id: str
    opponent_id: str
    opponent_name: str
    score1: int
    score2: int
    gameweek: int
    season: str
    played_at: str
    created_by: str
    created_at: str
    appearances: List[dict]  # Will contain player_id, goals, player_name

@router.get("/", response_model=List[MatchWithDetailsResponse])
def get_matches(season: str = None, team_id: str = None, user_id: str = Depends(get_current_user_id)):
    """
    Get all matches for the current user, optionally filtered by season or team.
    """
    try:
        # user_id = USER_ID # This line is removed as per the edit hint
        
        # Build the query
        query = supabase.table("matches").select("*").eq("created_by", user_id)
        
        # Add filters if provided
        if season:
            query = query.eq("season", season)
        if team_id:
            query = query.eq("team_id", team_id)
            
        # Execute and get matches
        response = query.execute()
        
        # For each match, get the opponent name and appearances
        matches_with_appearances = []
        for match in response.data:
            # Get opponent name
            opponent_response = supabase.table("opponents").select("name").eq("id", match["opponent_id"]).execute()
            opponent_name = opponent_response.data[0]["name"] if opponent_response.data else "Unknown"
            
            # Get appearances for this match
            appearances_response = supabase.table("appearances").select("*, players(name)").eq("match_id", match["id"]).execute()
            
            # Format the match data
            match_data = {
                "id": match["id"],
                "team_id": match["team_id"],
                "opponent_id": match["opponent_id"],
                "opponent_name": opponent_name,
                "score1": match["score1"],
                "score2": match["score2"],
                "gameweek": match["gameweek"],
                "season": match["season"],
                "played_at": match["played_at"],
                "created_by": match["created_by"],
                "created_at": match["created_at"],
                "appearances": appearances_response.data
            }
            matches_with_appearances.append(match_data)
        
        return matches_with_appearances
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{match_id}", response_model=MatchWithDetailsResponse)
def get_match(match_id: str, user_id: str = Depends(get_current_user_id)):
    """
    Get a specific match with all details including appearances.
    """
    try:
        # user_id = USER_ID # This line is removed as per the edit hint
        
        # Get the match
        response = supabase.table("matches").select("*").eq("id", match_id).eq("created_by", user_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Match not found")
        
        match = response.data[0]
        
        # Get opponent name
        opponent_response = supabase.table("opponents").select("name").eq("id", match["opponent_id"]).execute()
        opponent_name = opponent_response.data[0]["name"] if opponent_response.data else "Unknown"
        
        # Get appearances for this match
        appearances_response = supabase.table("appearances").select("*, players(name)").eq("match_id", match_id).execute()
        
        # Format the response
        match_data = {
            "id": match["id"],
            "team_id": match["team_id"],
            "opponent_id": match["opponent_id"],
            "opponent_name": opponent_name,
            "score1": match["score1"],
            "score2": match["score2"],
            "gameweek": match["gameweek"],
            "season": match["season"],
            "played_at": match["played_at"],
            "created_by": match["created_by"],
            "created_at": match["created_at"],
            "appearances": appearances_response.data
        }
        
        return match_data
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 