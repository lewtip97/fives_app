import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import Dict, List
from datetime import datetime

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def get_all_matches_for_user(user_id: str = "test-user-id") -> List[Dict]:
    """Get all matches for a user with opponent and appearance details."""
    try:
        # Get matches with opponent names
        matches_response = supabase.table("matches").select("*").eq("created_by", user_id).execute()
        
        matches_with_details = []
        for match in matches_response.data:
            # Get opponent name
            opponent_response = supabase.table("opponents").select("name").eq("id", match["opponent_id"]).execute()
            opponent_name = opponent_response.data[0]["name"] if opponent_response.data else "Unknown"
            
            # Get appearances for this match
            appearances_response = supabase.table("appearances").select("*, players(name)").eq("match_id", match["id"]).execute()
            
            match_data = {
                **match,
                "opponent_name": opponent_name,
                "appearances": appearances_response.data
            }
            matches_with_details.append(match_data)
        
        return matches_with_details
    except Exception as e:
        print(f"Error getting matches: {e}")
        return []

def calculate_player_stats_for_season(matches: List[Dict], season: str, user_id: str = "test-user-id") -> Dict:
    """Calculate stats for all players for a specific season."""
    player_stats = {}
    
    # Filter matches for this season
    season_matches = [m for m in matches if m["season"] == season]
    
    for match in season_matches:
        team_id = match["team_id"]
        score1 = match["score1"]  # Your team's score
        score2 = match["score2"]  # Opponent's score
        is_win = score1 > score2
        is_draw = score1 == score2
        
        # Process each appearance in this match
        for appearance in match["appearances"]:
            player_id = appearance["player_id"]
            player_name = appearance.get("players", {}).get("name", "Unknown")
            goals = appearance.get("goals", 0)
            
            if player_id not in player_stats:
                player_stats[player_id] = {
                    "player_id": player_id,
                    "player_name": player_name,
                    "team_id": team_id,
                    "season": season,
                    "goals_scored": 0,
                    "appearances": 0,
                    "wins": 0,
                    "draws": 0,
                    "losses": 0,
                    "team_goals_scored": 0,
                    "team_goals_conceded": 0
                }
            
            # Update stats
            player_stats[player_id]["goals_scored"] += goals
            player_stats[player_id]["appearances"] += 1
            player_stats[player_id]["team_goals_scored"] += score1
            player_stats[player_id]["team_goals_conceded"] += score2
            
            if is_win:
                player_stats[player_id]["wins"] += 1
            elif is_draw:
                player_stats[player_id]["draws"] += 1
            else:
                player_stats[player_id]["losses"] += 1
    
    # Calculate averages and percentages
    for player_id, stats in player_stats.items():
        appearances = stats["appearances"]
        if appearances > 0:
            stats["avg_team_goals_scored"] = round(stats["team_goals_scored"] / appearances, 2)
            stats["avg_team_goals_conceded"] = round(stats["team_goals_conceded"] / appearances, 2)
            stats["goals_per_game"] = round(stats["goals_scored"] / appearances, 2)
            
            total_games = stats["wins"] + stats["draws"] + stats["losses"]
            if total_games > 0:
                stats["win_rate"] = round((stats["wins"] / total_games) * 100, 2)
            else:
                stats["win_rate"] = 0.0
        else:
            stats["avg_team_goals_scored"] = 0.0
            stats["avg_team_goals_conceded"] = 0.0
            stats["goals_per_game"] = 0.0
            stats["win_rate"] = 0.0
    
    return player_stats

def calculate_all_seasons_stats(matches: List[Dict], user_id: str = "test-user-id") -> Dict:
    """Calculate stats for all players across all seasons combined."""
    return calculate_player_stats_for_season(matches, "All Seasons", user_id)

def upsert_player_stats(player_stats: Dict, user_id: str = "test-user-id"):
    """Insert or update player stats in the database."""
    try:
        for player_id, stats in player_stats.items():
            # Prepare data for upsert
            stats_data = {
                "player_id": stats["player_id"],
                "team_id": stats["team_id"],
                "season": stats["season"],
                "goals_scored": stats["goals_scored"],
                "appearances": stats["appearances"],
                "avg_team_goals_scored": stats["avg_team_goals_scored"],
                "avg_team_goals_conceded": stats["avg_team_goals_conceded"],
                "win_rate": stats["win_rate"],
                "goals_per_game": stats["goals_per_game"],
                "created_by": user_id,
                "updated_at": datetime.now().isoformat()
            }
            
            # Try to insert first, if it fails due to unique constraint, update instead
            try:
                response = supabase.table("player_stats").insert(stats_data).execute()
                print(f"Inserted stats for {stats['player_name']} - {stats['season']}")
            except Exception as insert_error:
                # If insert fails, try to update
                response = supabase.table("player_stats").update(stats_data).eq("player_id", stats["player_id"]).eq("season", stats["season"]).execute()
                if response.data:
                    print(f"Updated stats for {stats['player_name']} - {stats['season']}")
                else:
                    print(f"Failed to update stats for {stats['player_name']} - {stats['season']}")
                
    except Exception as e:
        print(f"Error upserting player stats: {e}")

def calculate_and_store_all_player_stats(user_id: str = "test-user-id"):
    """Main function to calculate and store all player stats."""
    print("Starting player stats calculation...")
    
    # Get all matches
    matches = get_all_matches_for_user(user_id)
    if not matches:
        print("No matches found for user")
        return
    
    print(f"Found {len(matches)} matches")
    
    # Get unique seasons
    seasons = list(set(match["season"] for match in matches))
    print(f"Seasons found: {seasons}")
    
    # Calculate stats for each season
    for season in seasons:
        print(f"Calculating stats for season: {season}")
        season_stats = calculate_player_stats_for_season(matches, season, user_id)
        upsert_player_stats(season_stats, user_id)
    
    # Calculate "All Seasons" stats
    print("Calculating stats for All Seasons")
    all_seasons_stats = calculate_all_seasons_stats(matches, user_id)
    upsert_player_stats(all_seasons_stats, user_id)
    
    print("Player stats calculation completed!")

def get_player_stats_summary(user_id: str = "test-user-id") -> Dict:
    """Get a summary of all player stats for the user."""
    try:
        response = supabase.table("player_stats").select("*").eq("created_by", user_id).execute()
        return response.data
    except Exception as e:
        print(f"Error getting player stats: {e}")
        return []

if __name__ == "__main__":
    # Run the calculation
    calculate_and_store_all_player_stats()
    
    # Print summary
    print("\n" + "="*50)
    print("PLAYER STATS SUMMARY")
    print("="*50)
    
    stats = get_player_stats_summary()
    for stat in stats:
        print(f"{stat['player_id']} - {stat['season']}: {stat['goals_scored']} goals in {stat['appearances']} appearances") 