import os
from supabase import create_client, Client
from dotenv import load_dotenv
import logging
from collections import defaultdict
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise ValueError("Missing Supabase environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def fetch_matches(team_id: Optional[str] = None):
    matches = supabase.table("matches").select("*", "team_id, score1, score2, season, gameweek").execute().data
    if team_id:
        matches = [m for m in matches if m["team_id"] == team_id]
    logger.info(f"Fetched {len(matches)} matches")
    return matches

def calculate_team_stats(matches):
    # Group matches by (team_id, season)
    matches_by_team_season = defaultdict(list)
    for match in matches:
        key = (match["team_id"], match["season"])
        matches_by_team_season[key].append(match)
    records = []
    for (team_id, season), team_matches in matches_by_team_season.items():
        # Sort by gameweek
        team_matches.sort(key=lambda m: m["gameweek"])
        games_played = 0
        goals_scored = 0
        goals_conceded = 0
        wins = 0
        losses = 0
        draws = 0
        for match in team_matches:
            games_played += 1
            score1 = match["score1"]
            score2 = match["score2"]
            goals_scored += score1
            goals_conceded += score2
            if score1 > score2:
                wins += 1
            elif score1 < score2:
                losses += 1
            else:
                draws += 1
            win_rate = wins / games_played if games_played > 0 else 0
            records.append({
                "team_id": team_id,
                "season": season,
                "gameweek": match["gameweek"],
                "games_played": games_played,
                "goals_scored": goals_scored,
                "goals_conceded": goals_conceded,
                "wins": wins,
                "losses": losses,
                "draws": draws,
                "win_rate": win_rate,
                "created_at": "now()"
            })
    logger.info(f"Prepared {len(records)} team stats records")
    return records

def upsert_team_stats(records):
    team_season_keys = set((r["team_id"], r["season"]) for r in records)
    for team_id, season in team_season_keys:
        logger.info(f"Deleting existing stats for team {team_id}, season {season}")
        supabase.table("team_stats").delete().eq("team_id", team_id).eq("season", season).execute()
    if records:
        logger.info(f"Inserting {len(records)} team stats records")
        response = supabase.table("team_stats").insert(records).execute()
        if not response.data:
            raise Exception("Failed to insert team stats")
        logger.info(f"Successfully inserted {len(response.data)} team stats records")
    else:
        logger.warning("No team stats to insert")

def main(team_id: Optional[str] = None):
    try:
        logger.info("Starting team stats calculation...")
        matches = fetch_matches(team_id=team_id)
        if not matches:
            logger.warning("No matches found")
            return
        records = calculate_team_stats(matches)
        if not records:
            logger.warning("No team stats calculated")
            return
        upsert_team_stats(records)
        logger.info("Team stats calculation completed successfully!")
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise

if __name__ == "__main__":
    main() 