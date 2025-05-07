import pandas as pd
import os
import json
from utils import DataLoader

def prepare_goals_long(df):
    goals_long = pd.melt(df, id_vars=['Player'], var_name='Gameweek', value_name='Goals')
    goals_long['Gameweek'] = goals_long['Gameweek'].str.extract(r'(\d+)').astype(int)
    goals_long = goals_long.sort_values(by=['Player', 'Gameweek'])
    goals_long['Cumulative Goals'] = goals_long.groupby('Player')['Goals'].cumsum()
    return goals_long

def generate_all_goals_data():
    loader = DataLoader()
    goals_df = loader.goals_data()
    results_df = loader.results_data()

    all_seasons = results_df['Season'].unique().tolist()
    all_seasons.sort()

    output_dir = "data/team_stats"
    os.makedirs(output_dir, exist_ok=True)

    # Save all seasons
    all_data = prepare_goals_long(goals_df)
    all_data.to_csv(f"{output_dir}/all_seasons.csv", index=False)

    for season in all_seasons:
        season_gameweeks = results_df[results_df['Season'] == season]['Gameweek']
        gameweek_cols = [f'Gameweek {int(gw)}' for gw in season_gameweeks if f'Gameweek {int(gw)}' in goals_df.columns]
        filtered_df = goals_df[['Player'] + gameweek_cols]

        season_data = prepare_goals_long(filtered_df)

        # Remap gameweeks to start from 1
        mapping = {gw: i+1 for i, gw in enumerate(sorted(season_data['Gameweek'].unique()))}
        season_data['Gameweek'] = season_data['Gameweek'].map(mapping)

        season_data.to_csv(f"{output_dir}/{season}.csv", index=False)

    print(f"✅ Team stats data saved to {output_dir}/team_stats/")

if __name__ == "__main__":
    generate_all_goals_data()
