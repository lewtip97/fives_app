import pandas as pd
from sklearn import linear_model
from joblib import dump
from utils import DataLoader

# Load data
loader = DataLoader()
goals_df = loader.goals_data()
appearances_df = loader.appearances_data()
results_df = loader.results_data()

def create_master_dataframe(goals_df, appearances_df, results_df):
    if 'Player' not in goals_df.columns or 'Player' not in appearances_df.columns:
        raise KeyError("'Player' column not found in one of the dataframes")

    appearances_df = appearances_df.set_index(appearances_df.columns[0])
    all_players = goals_df['Player'].unique()
    master_df = pd.DataFrame()

    for _, result_row in results_df.iterrows():
        gameweek = result_row['Gameweek']
        row_data = {
            'Gameweek': gameweek,
            'Date': result_row.get('Date'),
            'Opponent': result_row.get('opponents'),
            'Opponent_form': result_row.get('opponent_form'),
            'Opponents Wins': result_row.get('opponent_wins'),
            'Score_home': result_row.get('Score home'),
            'Score_away': result_row.get('Score away')
        }

        for player in all_players:
            col_name = f'Gameweek {gameweek}'
            if player in appearances_df.index:
                player_appearances = appearances_df.loc[player]
                appearance_value = 1 if col_name in player_appearances and player_appearances[col_name] == 1 else 0
            else:
                appearance_value = 0

            row_data[f'{player}_appearance'] = appearance_value

        master_df = pd.concat([master_df, pd.DataFrame([row_data])], ignore_index=True)

    return master_df

# Create master dataframe
master_df = create_master_dataframe(goals_df, appearances_df, results_df)

# Drop unused columns
columns_to_drop = ['Gameweek', 'Date', 'Opponent', 'Opponents Wins', 'Score_home', 'Score_away']
X = master_df.drop(columns=columns_to_drop)
y = master_df['Score_away']

# Check for NaNs
if X.isnull().values.any() or y.isnull().values.any():
    print("❌ NaN values detected!")
    print("NaNs in X:")
    print(X[X.isnull().any(axis=1)])
    print("\nNaNs in y:")
    print(y[y.isnull()])
    raise ValueError("NaN values detected in input data. Please clean the dataset before training.")

# Fit the model
clf = linear_model.PoissonRegressor()
clf.fit(X, y)

# Save the model
filename = 'models/goals_against_model.joblib'
dump(clf, filename)
print(X)
print(f"✅ Model saved to {filename}")
