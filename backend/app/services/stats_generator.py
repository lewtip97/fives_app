from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def generate_player_gameweek_stats(team_id=None):
    """
    Generate player gameweek stats for all players or a specific team.
    """
    try:
        # Get all matches
        matches_query = supabase.table("matches").select("*")
        if team_id:
            matches_query = matches_query.eq("team_id", team_id)
        matches_response = matches_query.execute()
        matches = matches_response.data

        # Get all appearances
        appearances_response = supabase.table("appearances").select("*").execute()
        appearances = appearances_response.data

        # Get all players
        players_query = supabase.table("players").select("*")
        if team_id:
            players_query = players_query.eq("team_id", team_id)
        players_response = players_query.execute()
        players = players_response.data

        # Get all teams
        teams_query = supabase.table("teams").select("*")
        if team_id:
            teams_query = teams_query.eq("id", team_id)
        teams_response = teams_query.execute()
        teams = teams_response.data

        # Calculate stats
        stats = {}
        for appearance in appearances:
            # Find the match for this appearance
            match = next((m for m in matches if m["id"] == appearance["match_id"]), None)
            if not match:
                continue

            player_id = appearance["player_id"]
            team_id = match["team_id"]
            season = match["season"]
            gameweek = match["gameweek"]
            goals = appearance["goals"]

            key = (player_id, team_id, season)
            if key not in stats:
                stats[key] = {}
            if gameweek not in stats[key]:
                stats[key][gameweek] = 0
            stats[key][gameweek] += goals

        # Create records for database
        records = []
        for (player_id, team_id, season), gameweek_goals in stats.items():
            team = next((t for t in teams if t["id"] == team_id), None)
            team_name = team["name"] if team else "Unknown"
            
            cumulative = 0
            for gameweek in sorted(gameweek_goals.keys()):
                goals = gameweek_goals[gameweek]
                cumulative += goals
                
                # Try to insert, if conflict then update
                try:
                    supabase.table("player_gameweek_stats").insert({
                        "player_id": player_id,
                        "team_id": team_id,
                        "team_name": team_name,
                        "gameweek": gameweek,
                        "season": season,
                        "goals": goals,
                        "cumulative_goals": cumulative,
                    }).execute()
                except Exception:
                    # Update existing record
                    supabase.table("player_gameweek_stats").update({
                        "goals": goals,
                        "cumulative_goals": cumulative,
                    }).eq("player_id", player_id).eq("season", season).eq("gameweek", gameweek).execute()

        return {"status": "success", "message": f"Generated stats for {len(stats)} player-season combinations"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def generate_team_stats(team_id=None):
    """
    Generate team stats for all teams or a specific team.
    """
    try:
        # Get all matches
        matches_query = supabase.table("matches").select("*")
        if team_id:
            matches_query = matches_query.eq("team_id", team_id)
        matches_response = matches_query.execute()
        matches = matches_response.data

        # Calculate team stats
        team_stats = {}
        for match in matches:
            team_id = match["team_id"]
            season = match["season"]
            gameweek = match["gameweek"]
            score1 = match["score1"]
            score2 = match["score2"]

            key = (team_id, season)
            if key not in team_stats:
                team_stats[key] = {}

            if gameweek not in team_stats[key]:
                team_stats[key][gameweek] = {
                    "games_played": 0,
                    "goals_scored": 0,
                    "goals_conceded": 0,
                    "wins": 0,
                    "losses": 0,
                    "draws": 0,
                }

            # Update stats for this gameweek
            team_stats[key][gameweek]["games_played"] += 1
            team_stats[key][gameweek]["goals_scored"] += score1
            team_stats[key][gameweek]["goals_conceded"] += score2

            if score1 > score2:
                team_stats[key][gameweek]["wins"] += 1
            elif score1 < score2:
                team_stats[key][gameweek]["losses"] += 1
            else:
                team_stats[key][gameweek]["draws"] += 1

        # Calculate cumulative stats and create records
        records = []
        for (team_id, season), gameweek_stats in team_stats.items():
            cumulative = {
                "games_played": 0,
                "goals_scored": 0,
                "goals_conceded": 0,
                "wins": 0,
                "losses": 0,
                "draws": 0,
            }

            for gameweek in sorted(gameweek_stats.keys()):
                stats = gameweek_stats[gameweek]
                
                # Add to cumulative
                cumulative["games_played"] += stats["games_played"]
                cumulative["goals_scored"] += stats["goals_scored"]
                cumulative["goals_conceded"] += stats["goals_conceded"]
                cumulative["wins"] += stats["wins"]
                cumulative["losses"] += stats["losses"]
                cumulative["draws"] += stats["draws"]

                # Calculate win rate
                total_games = cumulative["wins"] + cumulative["losses"] + cumulative["draws"]
                win_rate = cumulative["wins"] / total_games if total_games > 0 else 0

                # Try to insert, if conflict then update
                try:
                    supabase.table("team_stats").insert({
                        "team_id": team_id,
                        "season": season,
                        "gameweek": gameweek,
                        "games_played": cumulative["games_played"],
                        "goals_scored": cumulative["goals_scored"],
                        "goals_conceded": cumulative["goals_conceded"],
                        "wins": cumulative["wins"],
                        "losses": cumulative["losses"],
                        "draws": cumulative["draws"],
                        "win_rate": win_rate,
                    }).execute()
                except Exception:
                    # Update existing record
                    supabase.table("team_stats").update({
                        "games_played": cumulative["games_played"],
                        "goals_scored": cumulative["goals_scored"],
                        "goals_conceded": cumulative["goals_conceded"],
                        "wins": cumulative["wins"],
                        "losses": cumulative["losses"],
                        "draws": cumulative["draws"],
                        "win_rate": win_rate,
                    }).eq("team_id", team_id).eq("season", season).eq("gameweek", gameweek).execute()

        return {"status": "success", "message": f"Generated stats for {len(team_stats)} team-season combinations"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def generate_all_stats(team_id=None):
    """
    Generate both player and team stats.
    """
    player_result = generate_player_gameweek_stats(team_id)
    team_result = generate_team_stats(team_id)
    
    return {
        "player_stats": player_result,
        "team_stats": team_result
    } 