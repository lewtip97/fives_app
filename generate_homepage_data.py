# generate_homepage_data.py

import pandas as pd
from utils import DataLoader
import os

def generate_homepage_data():
    loader = DataLoader()
    results_df = loader.results_data()
    goals_df = loader.goals_data()

    results_df = results_df.sort_values(by='Gameweek', ascending=True)

    # Compute summary stats
    win_count = results_df[results_df['Result'] == 'Win'].shape[0]
    draw_count = results_df[results_df['Result'] == 'Draw'].shape[0]
    loss_count = results_df[results_df['Result'] == 'Loss'].shape[0]

    goals_scored = results_df['Score home'].sum()
    goals_against = results_df['Score away'].sum()

    recent_results = results_df.tail(5)['Result'].tolist()

    latest_match = results_df.iloc[-1]
    opponent = latest_match['opponents']
    home_score = latest_match['Score home']
    away_score = latest_match['Score away']
    latest_gameweek = int(latest_match['Gameweek'])
    gw_col = f'Gameweek {latest_gameweek}'

    scorers = []
    if gw_col in goals_df.columns:
        for _, row in goals_df.iterrows():
            goals = row[gw_col]
            if goals > 0:
                player = row['Player']
                scorers.append(f"{player} ({int(goals)})" if goals > 1 else player)

    scorers_text = ', '.join(scorers) if scorers else 'No goalscorers recorded.'

    # Save to disk
    os.makedirs("data/homepage", exist_ok=True)
    pd.DataFrame({
        'Result': ['Win', 'Draw', 'Loss'],
        'Count': [win_count, draw_count, loss_count]
    }).to_csv("data/homepage/result_counts.csv", index=False)

    pd.DataFrame({'Metric': ['Scored', 'Conceded'], 'Goals': [goals_scored, goals_against]}) \
      .to_csv("data/homepage/goals_summary.csv", index=False)

    pd.DataFrame({'Recent Results': recent_results}).to_csv("data/homepage/recent_results.csv", index=False)

    pd.DataFrame([{
        'Opponent': opponent,
        'Score Home': home_score,
        'Score Away': away_score,
        'Scorers Text': scorers_text
    }]).to_csv("data/homepage/latest_match.csv", index=False)

if __name__ == "__main__":
    generate_homepage_data()
