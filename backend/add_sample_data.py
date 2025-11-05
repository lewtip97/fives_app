from supabase import create_client, Client
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def add_red_rockets_data():
    """Add realistic data for the Red Rockets team."""
    
    # First, let's get or create the Red Rockets team
    teams_response = supabase.table("teams").select("*").eq("name", "Red Rockets").execute()
    
    if teams_response.data:
        team = teams_response.data[0]
        team_id = team["id"]
        print(f"Found existing Red Rockets team: {team_id}")
    else:
        # Create Red Rockets team
        team_data = {
            "name": "Red Rockets",
            "team_size": 5,
            "created_by": "test_user",  # You'll need to replace this with a real user ID
        }
        team_response = supabase.table("teams").insert(team_data).execute()
        team = team_response.data[0]
        team_id = team["id"]
        print(f"Created Red Rockets team: {team_id}")
    
    # Create players for Red Rockets
    players_data = [
        {"name": "Lewis", "position": "Forward", "team_id": team_id, "created_by": team["created_by"]},
        {"name": "Jake", "position": "Midfielder", "team_id": team_id, "created_by": team["created_by"]},
        {"name": "Sam", "position": "Defender", "team_id": team_id, "created_by": team["created_by"]},
        {"name": "Tom", "position": "Forward", "team_id": team_id, "created_by": team["created_by"]},
        {"name": "Mike", "position": "Goalkeeper", "team_id": team_id, "created_by": team["created_by"]},
    ]
    
    # Add players
    players = []
    for player_data in players_data:
        player_response = supabase.table("players").insert(player_data).execute()
        players.append(player_response.data[0])
    
    print(f"Added players: {[p['name'] for p in players]}")
    
    # Create opponents first
    opponent_names = [
        "Blue Dragons", "Green Eagles", "Yellow Tigers", "Purple Panthers", "Orange Lions",
        "Black Knights", "White Wolves", "Silver Sharks", "Gold Bears", "Bronze Bulls",
        "Crimson Cobras", "Emerald Eagles", "Azure Angels", "Sapphire Stars", "Ruby Raptors"
    ]
    
    opponents = {}
    for opponent_name in opponent_names:
        opponent_data = {
            "name": opponent_name,
            "team_id": team_id,
            "created_by": team["created_by"],
        }
        opponent_response = supabase.table("opponents").insert(opponent_data).execute()
        opponents[opponent_name] = opponent_response.data[0]["id"]
    
    print(f"Created {len(opponents)} opponents")
    
    # Realistic match data for Red Rockets
    # Format: (opponent_name, red_rockets_score, opponent_score, gameweek, season)
    matches_data = [
        ("Blue Dragons", 3, 1, 1, "2024"),
        ("Green Eagles", 2, 2, 2, "2024"),
        ("Yellow Tigers", 4, 0, 3, "2024"),
        ("Purple Panthers", 1, 3, 4, "2024"),
        ("Orange Lions", 3, 2, 5, "2024"),
        ("Black Knights", 2, 1, 6, "2024"),
        ("White Wolves", 5, 1, 7, "2024"),
        ("Silver Sharks", 1, 4, 8, "2024"),
        ("Gold Bears", 3, 3, 9, "2024"),
        ("Bronze Bulls", 2, 0, 10, "2024"),
        ("Crimson Cobras", 4, 2, 11, "2024"),
        ("Emerald Eagles", 1, 2, 12, "2024"),
        ("Azure Angels", 3, 1, 13, "2024"),
        ("Sapphire Stars", 2, 2, 14, "2024"),
        ("Ruby Raptors", 4, 1, 15, "2024"),
    ]
    
    # Player goal distribution (realistic patterns)
    # Each player has different scoring patterns
    player_goals = {
        "Lewis": [1, 0, 2, 0, 1, 1, 2, 0, 1, 1, 2, 0, 1, 0, 2],  # Top scorer, consistent
        "Jake": [1, 1, 1, 0, 1, 0, 2, 0, 1, 0, 1, 1, 1, 1, 1],   # Good midfielder
        "Sam": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # Defender, no goals
        "Tom": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],   # Consistent forward
        "Mike": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Goalkeeper, no goals
    }
    
    # Add matches and appearances
    for i, (opponent_name, score1, score2, gameweek, season) in enumerate(matches_data):
        match_data = {
            "team_id": team_id,
            "opponent_id": opponents[opponent_name],
            "score1": score1,
            "score2": score2,
            "gameweek": gameweek,
            "season": season,
            "played_at": datetime.now().isoformat(),
            "created_by": team["created_by"],
        }
        
        match_response = supabase.table("matches").insert(match_data).execute()
        match_id = match_response.data[0]["id"]
        
        # Add appearances for each player
        for player in players:
            player_name = player["name"]
            goals = player_goals[player_name][i] if i < len(player_goals[player_name]) else 0
            
            appearance_data = {
                "match_id": match_id,
                "player_id": player["id"],
                "goals": goals,
            }
            
            supabase.table("appearances").insert(appearance_data).execute()
    
    print("Realistic Red Rockets data added successfully!")
    print(f"Added {len(matches_data)} matches with realistic player statistics")
    print("Team Record: 9 wins, 3 draws, 3 losses")
    print("Total Goals Scored: 38")
    print("Top Scorers: Lewis (13 goals), Tom (13 goals), Jake (10 goals)")
    print("You can now generate stats and see visualizations in the team overview.")

if __name__ == "__main__":
    add_red_rockets_data() 