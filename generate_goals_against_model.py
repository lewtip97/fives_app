import pandas as pd
from sklearn import linear_model
import pickle
from joblib import dump, load



# Load data
goals_df = pd.read_csv('data/goals_all.csv')
appearances_df = pd.read_csv('data/appearances_all.csv')
results_df = pd.read_csv('data/results_all.csv')



def create_master_dataframe(goals_df, appearances_df, results_df):
    # Check if 'Player' is in columns
    if 'Player' not in goals_df.columns or 'Player' not in appearances_df.columns:
        raise KeyError("'Player' column not found in one of the dataframes")

    # Reset indices for proper alignment
    appearances_df = appearances_df.set_index(appearances_df.columns[0])

    # Get the list of all players
    all_players = goals_df['Player'].unique()

    # Create an empty master dataframe
    master_df = pd.DataFrame()

    # Iterate through each gameweek in the results dataframe
    for _, result_row in results_df.iterrows():
        gameweek = result_row['Gameweek']
        
        # Filter results for the current gameweek
        opponent_info = result_row[['Date', 'Opponents', 'Opponent_wins', 'Opponent_form (%)', 'Score home', 'Score away']]
        
        # Create a dictionary for the current row
        row_data = {
            'Gameweek': gameweek,
            'Date': opponent_info['Date'],
            'Opponent': opponent_info['Opponents'],
            'Opponents Form': opponent_info['Opponent_form (%)'],
            'Opponents Wins': opponent_info['Opponent_wins'],
            'Score_home': opponent_info['Score home'],
            'Score_away': opponent_info['Score away']
        }

        # Add columns for each player with binary values indicating appearance
        for player in all_players:
            # Check if the player has appearance data for this gameweek
            if player in appearances_df.index:
                player_appearances = appearances_df.loc[player]
                appearance_value = 1 if 'Gameweek ' + str(gameweek) in player_appearances.index and player_appearances['Gameweek ' + str(gameweek)] ==1 else 0
            else:
                appearance_value = 0

            row_data[f'{player}_appearance'] = appearance_value

        # Append the row to the master dataframe
        master_df = master_df.append(row_data, ignore_index=True)

    return master_df

# Create the master dataframe
master_df = create_master_dataframe(goals_df, appearances_df, results_df)



columns_to_drop = ['Gameweek', 'Date', 'Opponent','Opponents Wins', 'Score_home', 'Score_away']

X = master_df.drop(columns = columns_to_drop)
y = master_df.pop('Score_away')


clf = linear_model.PoissonRegressor()
clf.fit(X, y)

# save the model to disk
filename = 'models/goals_against_model.joblib'
dump(clf, filename)