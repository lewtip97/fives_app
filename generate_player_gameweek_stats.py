import os
from supabase import create_client, Client
from dotenv import load_dotenv
import logging
from typing import Dict, List, Optional

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

def fetch_data(team_id: Optional[str] = None):
    match_query = supabase.table("matches").select("*", "team_id").execute()
    matches = match_query.data
    if team_id:
        matches = [m for m in matches if m["team_id"] == team_id]
    match_ids = [m["id"] for m in matches]
    appearances = supabase.table("appearances").select("*", "player_id, match_id, goals").execute().data
    if team_id:
        appearances = [a for a in appearances if a["match_id"] in match_ids]
    players = supabase.table("players").select("*").execute().data
    teams = supabase.table("teams").select("*").execute().data
    logger.info(f"Fetched {len(matches)} matches, {len(appearances)} appearances, {len(players)} players, {len(teams)} teams")
    return matches, appearances, players, teams

def build_lookup_tables(matches, players, teams):
    match_lookup = {m["id"]: m for m in matches}
    player_lookup = {p["id"]: p for p in players}
    team_lookup = {t["id"]: t for t in teams}
    return match_lookup, player_lookup, team_lookup

def calculate_player_gameweek_stats(matches, appearances, players, teams):
    match_lookup, player_lookup, team_lookup = build_lookup_tables(matches, players, teams)
    stats = {}
    for app in appearances:
        match = match_lookup.get(app["match_id"])
        if not match:
            continue
        player_id = app["player_id"]
        team_id = match["team_id"]
        team_name = team_lookup[team_id]["name"] if team_id in team_lookup else "Unknown"
        season = match["season"]
        gameweek = match["gameweek"]
        goals = app["goals"]
        key = (player_id, team_id, team_name, season)
        if key not in stats:
            stats[key] = {}
        if gameweek not in stats[key]:
            stats[key][gameweek] = 0
        stats[key][gameweek] += goals
    records = []
    for (player_id, team_id, team_name, season), gw_goals in stats.items():
        cumulative = 0
        for gameweek in sorted(gw_goals.keys()):
            goals = gw_goals[gameweek]
            cumulative += goals
            records.append({
                "player_id": player_id,
                "team_id": team_id,
                "team_name": team_name,
                "gameweek": gameweek,
                "season": season,
                "goals": goals,
                "cumulative_goals": cumulative,
                "created_at": "now()"
            })
    logger.info(f"Prepared {len(records)} player gameweek stats records")
    return records

def upsert_player_gameweek_stats(records):
    player_season_keys = set((r["player_id"], r["season"]) for r in records)
    for player_id, season in player_season_keys:
        logger.info(f"Deleting existing stats for player {player_id}, season {season}")
        supabase.table("player_gameweek_stats").delete().eq("player_id", player_id).eq("season", season).execute()
    if records:
        logger.info(f"Inserting {len(records)} player gameweek stats records")
        response = supabase.table("player_gameweek_stats").insert(records).execute()
        if not response.data:
            raise Exception("Failed to insert player gameweek stats")
        logger.info(f"Successfully inserted {len(response.data)} player gameweek stats records")
    else:
        logger.warning("No player gameweek stats to insert")

def recalculate_player_gameweek_stats(team_id: Optional[str] = None):
    logger.info("Starting player gameweek stats calculation...")
    matches, appearances, players, teams = fetch_data(team_id=team_id)
    if not matches or not appearances:
        logger.warning("No matches or appearances found")
        return
    records = calculate_player_gameweek_stats(matches, appearances, players, teams)
    if not records:
        logger.warning("No player gameweek stats calculated")
        return
    upsert_player_gameweek_stats(records)
    logger.info("Player gameweek stats calculation completed successfully!")

def main():
    try:
        recalculate_player_gameweek_stats()
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise

if __name__ == "__main__":
    main() 