import pandas as pd
from sklearn.linear_model import PoissonRegressor
from joblib import dump
from utils import DataLoader


# Load data
loader = DataLoader()
goals_df = loader.goals_data()
appearances_df = loader.appearances_data()
results_df = loader.results_data()


def create_master_dataframe_per_player(player_name, goals_df, appearances_df, results_df):
    # Filter data for the selected player
    player_goals = goals_df[goals_df['Player'] == player_name]
    player_appearances = appearances_df[appearances_df['Player'] == player_name]

    # Reset indices for proper alignment
    player_goals = player_goals.set_index(goals_df.columns[0])
    player_appearances = player_appearances.set_index(appearances_df.columns[0])

    # Get the list of all players
    all_players = goals_df['Player'].unique()

    # List to collect rows (faster than appending to DataFrame)
    master_data = []

    # Iterate through each gameweek where the player has appeared
    for gameweek in player_appearances.columns[1:]:
        # Check if the player played in the gameweek
        if player_appearances.loc[:, gameweek].values[0] == 1:
            # Filter results for the current gameweek
            gw_number = int(gameweek.split(' ')[-1])
            results_gameweek = results_df[results_df['Gameweek'] == gw_number]
            
            if results_gameweek.empty:
                continue  # Skip if no results for the current gameweek
            
            # Get opponent details
            opponent_info = results_gameweek[['Date', 'opponents', 'opponent_form', 'Score home', 'Score away']].iloc[0]
            
            # Create a dictionary for the current row
            row_data = {
                'Gameweek': gameweek,
                'Date': opponent_info['Date'],
                'Opponent': opponent_info['opponents'],
                'Opponent_form': opponent_info['opponent_form'],
                'Score_home': opponent_info['Score home'],
                'Score_away': opponent_info['Score away'],
                'Player': player_name,
                'Player_Goals': player_goals.loc[:, gameweek].values[0]
            }
            
            # Add columns for each player with binary values indicating appearance
            for other_player in all_players:
                if other_player == player_name:
                    continue

                other_appearance = appearances_df[appearances_df['Player'] == other_player]
                row_data[f'{other_player}_appearance'] = int(
                    not other_appearance.empty and other_appearance.loc[:, gameweek].values[0] == 1
                )

            master_data.append(row_data)

    return pd.DataFrame(master_data)


# Train a Poisson regression model for each player
all_players = goals_df['Player'].unique()

for player in all_players:
    player_master_df = create_master_dataframe_per_player(player, goals_df, appearances_df, results_df)

    if player_master_df.empty:
        print(f"Skipping {player}: no data")
        continue

    columns_to_drop = ['Gameweek', 'Date', 'Opponent', 'Player', 'Score_away', 'Score_home', 'Player_Goals']
    X = player_master_df.drop(columns=columns_to_drop)
    y = player_master_df['Player_Goals']

    clf = PoissonRegressor()
    clf.fit(X, y)

    player_model_path = f'models/{player}_goal_model.joblib'
    dump(clf, player_model_path)
    print(f'{player} model saved to {player_model_path}')
