import pandas as pd
from sklearn import linear_model
import pickle
from joblib import dump, load



# Load data
goals_df = pd.read_csv('data/goals.csv')
appearances_df = pd.read_csv('data/appearances.csv')
results_df = pd.read_csv('data/results.csv')



def create_master_dataframe_per_player(player_name, goals_df, appearances_df, results_df):
    # Filter data for the selected player
    player_goals = goals_df[goals_df['Player'] == player_name]
    player_appearances = appearances_df[appearances_df['Player'] == player_name]

    # Reset indices for proper alignment
    player_goals = player_goals.set_index(goals_df.columns[0])
    player_appearances = player_appearances.set_index(appearances_df.columns[0])

    # Get the list of all players
    all_players = goals_df['Player'].unique()

    # Create an empty master dataframe
    master_df = pd.DataFrame()

    # Iterate through each gameweek where the player has appeared
    for gameweek in player_appearances.columns[1:]:
        # Check if the player played in the gameweek
        if player_appearances[gameweek].values[0] == 1:
            # Filter results for the current gameweek
            results_gameweek = results_df[results_df['Gameweek'] == int(gameweek.split(' ')[-1])]
            
            if results_gameweek.empty:
                continue  # Skip if no results for the current gameweek
            
            # Get opponent details
            opponent_info = results_gameweek[['Date', 'Opponents','Opponent_form (%)', 'Score home', 'Score away']].iloc[0]
            
            # Create a dictionary for the current row
            row_data = {
                'Gameweek': gameweek,
                'Date': opponent_info['Date'],
                'Opponent': opponent_info['Opponents'],
                'Opponent_form': opponent_info['Opponent_form (%)'],
                'Score_home': opponent_info['Score home'],
                'Score_away': opponent_info['Score away'],
                'Player': player_name,
                'Player_Goals': player_goals[gameweek].values[0]
            }
            
            # Add columns for each player with binary values indicating appearance
            for other_player in all_players:
                if other_player == player_name:
                    continue
                
                # Get appearance data for the other player
                other_player_appearances = appearances_df[appearances_df['Player'] == other_player]
                
                # If the other player played in this gameweek, mark as 1, else 0
                appearance_value = 1 if other_player_appearances[gameweek].values[0] == 1 else 0
                row_data[f'{other_player}_appearance'] = appearance_value
            
            # Append the row to the master dataframe
            master_df = master_df.append(row_data, ignore_index=True)

    return master_df

for player in all_players:
    player_master_df = create_master_dataframe_per_player(player,goals_df, appearances_df, results_df)
    
    columns_to_drop = ['Gameweek', 'Date', 'Opponent','Player', 'Score_away', 'Score_home', 'Player_Goals']
    X = player_master_df.drop(columns = columns_to_drop, inplace=False)
    y = player_master_df.pop('Player_Goals')

    clf = linear_model.PoissonRegressor()
    clf.fit(X, y)
    player_model = f'models/{player}_goal_model.joblib'
    dump(clf, player_model)
    print(f'{player} model saved to {player_model}')