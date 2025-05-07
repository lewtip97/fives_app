# player_stats_display.py

import streamlit as st
import os
import json
from PIL import Image
from utils import DataLoader

class PlayerStatsDisplayApp:
    def __init__(self):
        self.player_stats = {}
        self.results_df = None

    def load_data(self):
        with open("data/player_stats/player_stats.json", "r") as f:
            self.player_stats = json.load(f)
        loader = DataLoader()
        self.results_df = loader.results_data()

    def load_player_image(self, player_name):
        image_path = f'player_images/{player_name}.png'
        return Image.open(image_path) if os.path.exists(image_path) else None

    def display_player_stats(self, player, season):
        stats = self.player_stats.get(player, {}).get(season, None)
        if not stats:
            st.write("No data available.")
            return

        player_image = self.load_player_image(player)
        col1, col2 = st.columns([1, 2])
        with col1:
            if player_image:
                st.image(player_image, caption=player, width=200)
            else:
                st.write("Image not available")
        with col2:
            st.write(f"**Goals Scored:** {stats['goals_scored']}")
            st.write(f"**Appearances:** {stats['appearances']}")
            st.write(f"**Average Team Goals Scored (when playing):** {stats['avg_team_goals_scored']:.2f}")
            st.write(f"**Average Team Goals Conceded (when playing):** {stats['avg_team_goals_conceded']:.2f}")
            st.write(f"**Win Rate:** {stats['win_rate']:.2f}%")
            st.write(f"**Goals Per Game:** {stats['goals_per_game']:.2f}")

    def run(self):
        self.load_data()
        st.title("Player Statistics")
        st.write("Detailed statistics for each player. Select a player to view their stats.")
        players = sorted(self.player_stats.keys())
        player = st.selectbox("Select a player", players)

        seasons = sorted(self.results_df['Season'].unique())
        tab_labels = ['All Seasons'] + seasons
        tabs = st.tabs(tab_labels)

        with tabs[0]:
            st.subheader("All Seasons")
            self.display_player_stats(player, season='All Seasons')

        for i, season in enumerate(seasons):
            with tabs[i + 1]:
                st.subheader(f"Season: {season}")
                self.display_player_stats(player, season=season)

# Run app
if __name__ == "__main__":
    app = PlayerStatsDisplayApp()
    app.run()
