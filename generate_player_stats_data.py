# generate_player_stats_data.py

import os
import json
from utils import DataLoader
import pandas as pd

def calculate_all_player_stats():
    loader = DataLoader()
    goals_df = loader.goals_data()
    appearances_df = loader.appearances_data()
    results_df = loader.results_data()

    season_by_Gameweek = results_df.set_index('Gameweek')['Season'].to_dict()
    all_stats = {}

    for player in goals_df['Player'].unique():
        player_goals = goals_df[goals_df['Player'] == player]
        player_appearances = appearances_df[appearances_df['Player'] == player]

        if player_appearances.empty or player_goals.empty:
            continue

        Gameweek_cols = [col for col in goals_df.columns if col.startswith('Gameweek')]
        player_stats_by_season = {}

        for season in [None] + sorted(results_df['Season'].unique()):
            total_goals = 0
            total_appearances = 0
            played_Gameweeks = []

            for col in Gameweek_cols:
                gw_num = int(col.split()[-1])
                if season and season_by_Gameweek.get(gw_num) != season:
                    continue

                appearance = player_appearances[col].values[0]
                goals = player_goals[col].values[0]

                if appearance == 1:
                    played_Gameweeks.append(gw_num)
                    total_appearances += 1
                    total_goals += goals
                elif appearance == 0:
                    total_goals += goals

            relevant_results = results_df[results_df['Gameweek'].isin(played_Gameweeks)]

            avg_goals_for = relevant_results['Score home'].mean() if not relevant_results.empty else 0
            avg_goals_against = relevant_results['Score away'].mean() if not relevant_results.empty else 0
            wins = relevant_results[relevant_results['Result'] == 'Win'].shape[0]
            total_games_played = relevant_results.shape[0]
            win_rate = (wins / total_games_played) * 100 if total_games_played > 0 else 0
            goals_per_game = total_goals / total_appearances if total_appearances > 0 else 0

            key = 'All Seasons' if season is None else season
            player_stats_by_season[key] = {
            'goals_scored': int(total_goals),
            'appearances': int(total_appearances),
            'avg_team_goals_scored': float(avg_goals_for),
            'avg_team_goals_conceded': float(avg_goals_against),
            'win_rate': float(win_rate),
            'goals_per_game': float(goals_per_game)
            }


        all_stats[player] = player_stats_by_season

    os.makedirs("data/player_stats", exist_ok=True)
    with open("data/player_stats/player_stats.json", "w") as f:
        json.dump(all_stats, f, indent=2)

    print("✅ Player stats data generated and saved to data/player_stats/player_stats.json")

if __name__ == "__main__":
    calculate_all_player_stats()
