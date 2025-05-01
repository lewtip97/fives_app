import streamlit as st
import pandas as pd
import os
from PIL import Image
from utils import SelectSeason, DataLoader

# Function to load data
@st.cache_data
def load_data():
    # Load goals and appearances data
    loader = DataLoader()
    #goals_df = pd.read_csv('data/goals_all.csv')
    goals_df = loader.goals_data()
    appearances_df = loader.appearances_data()
    #appearances_df = pd.read_csv('data/appearances_all.csv')
    results_df = loader.results_data()
    #results_df = pd.read_csv('data/results_all.csv')  
    return goals_df, appearances_df, results_df

# Function to load player image
def load_player_image(player_name):
    image_path = f'player_images/{player_name}.png'
    if os.path.exists(image_path):
        return Image.open(image_path)
    else:
        return None  # Return None if image doesn't exist

# Function to calculate player stats
def calculate_player_stats(player, goals_df, appearances_df, results_df):
    # Filter data for the selected player
    player_goals = goals_df[goals_df['Player'] == player]
    player_appearances = appearances_df[appearances_df['Player'] == player]

    # Reset indices for proper alignment with results
    player_goals = player_goals.set_index(goals_df.columns[0])

    # Calculate total goals and appearances
    total_goals = player_goals.iloc[:, 1:].sum().sum()  # Summing all gameweek columns
    total_appearances = player_appearances.iloc[:, 1:].sum().sum()  # Sum of binary appearances

    relevant_gameweeks_array = player_appearances.to_numpy()[0][1:]

    # Convert the array to a boolean mask (True for 1, False for 0)
    row_mask = pd.Series(relevant_gameweeks_array, dtype=bool)

    # Filter the DataFrame to include only the rows where binary_array is 1
    relevant_results = results_df[row_mask]

    # Calculate average team goals scored and conceded when the player was playing
    team_goals_when_playing = relevant_results['Score home'].mean()
    team_goals_conceded_when_playing = relevant_results['Score away'].mean()

    # Calculate win rate (%)
    wins = relevant_results[relevant_results['Result'] == 'Win'].shape[0]
    total_games_played = relevant_results.shape[0]
    win_rate = (wins / total_games_played) * 100 if total_games_played > 0 else 0

    # Calculate goals per game
    goals_per_game = total_goals / total_appearances if total_appearances > 0 else 0

    return {
        'goals_scored': total_goals,
        'appearances': total_appearances,
        'avg_team_goals_scored': team_goals_when_playing,
        'avg_team_goals_conceded': team_goals_conceded_when_playing,
        'win_rate': win_rate,
        'goals_per_game': goals_per_game
    }

# Function to run the Player Stats page
def run():
    SelectSeason()  # Call the function to get the season
    # Load the data
    goals_df, appearances_df, results_df = load_data()

    # Create a dropdown for player selection
    player = st.selectbox('Select a player', goals_df['Player'].unique())

    # Load and display the player's image
    player_image = load_player_image(player)

    # Create columns for image and stats
    col1, col2 = st.columns([1, 2])  # Adjust column ratios as needed

    with col1:
        if player_image:
            st.image(player_image, caption=player, width=200)
        else:
            st.write("Image not available")

    with col2:
        # Calculate and display player statistics
        stats = calculate_player_stats(player, goals_df, appearances_df, results_df)
        
        # Display player statistics
        st.write(f"**Goals Scored:** {stats['goals_scored']}")
        st.write(f"**Appearances:** {stats['appearances']}")
        st.write(f"**Average Team Goals Scored (when playing):** {stats['avg_team_goals_scored']:.2f}")
        st.write(f"**Average Team Goals Conceded (when playing):** {stats['avg_team_goals_conceded']:.2f}")
        st.write(f"**Win Rate:** {stats['win_rate']:.2f}%")
        st.write(f"**Goals Per Game:** {stats['goals_per_game']:.2f}")

def main():
    # Set the title for the Player Stats page
    st.title("Player Statistics")
    st.write("Detailed statistics for each player, select a player to view their stats.")

    # Run the player stats function
    run()

main()
