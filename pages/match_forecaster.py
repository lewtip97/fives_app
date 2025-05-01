import streamlit as st
import pandas as pd
import os
from PIL import Image
from utils import SelectSeason, DataLoader


# Load the list of players
def load_players():
    loader = DataLoader()
    players_df = loader.goals_data()
    return players_df['Player'].unique()

# Load player image
def load_player_image(player_name):
    image_path = f'player_images/{player_name}.png'
    if os.path.exists(image_path):
        return Image.open(image_path)
    else:
        return None  # Return None if the image doesn't exist

# Main function to run the player selection page
def run():
    SelectSeason()
    st.title("Select 6 Players for Score Prediction")

    # Load the players
    players = load_players()

    # Store selected players in session state
    if 'selected_players' not in st.session_state:
        st.session_state.selected_players = []

    # Reset button at the top to clear the selection
    if st.button("Reset Selection"):
        st.session_state.selected_players = []

    # Function to handle player selection
    def select_player(player):
        if player in st.session_state.selected_players:
            st.session_state.selected_players.remove(player)
        else:
            if len(st.session_state.selected_players) < 6:
                st.session_state.selected_players.append(player)

    # Display all players with their images and a select button
    cols = st.columns(4)  # Show 4 players per row

    for idx, player in enumerate(players):
        with cols[idx % 4]:
            player_image = load_player_image(player)
            if player_image:
                st.image(player_image, caption=player, width=100)

            # Select button for each player
            if player in st.session_state.selected_players:
                st.button(f"Deselect {player}", key=f'deselect_{player}', on_click=select_player, args=(player,))
            else:
                st.button(f"Select {player}", key=f'select_{player}', on_click=select_player, args=(player,))

    # Display selected players
    st.write("Selected Players:", st.session_state.selected_players)

    # Show a message if less than 6 players are selected
    if len(st.session_state.selected_players) != 6:
        st.warning("Please select exactly 6 players to enable the 'Generate Score' button.")

    # Generate Score button, enabled only when exactly 6 players are selected
    if len(st.session_state.selected_players) == 6:
        if st.button("Generate Score"):
            # Handle the score generation logic here
            st.success("Generating score...")


run()