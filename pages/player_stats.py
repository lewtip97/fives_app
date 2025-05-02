import streamlit as st
import pandas as pd
import os
from PIL import Image
from utils import SelectSeason, DataLoader, FilterGameweeks, CollectGameweeks

class PlayerStatsApp:
    def __init__(self):
        self.goals_df = None
        self.appearances_df = None
        self.results_df = None
        self.season_by_gameweek = None

    def load_data(self):
        loader = DataLoader()
        self.goals_df = loader.goals_data()
        self.appearances_df = loader.appearances_data()
        self.results_df = loader.results_data()
        # Create gameweek → season mapping
        self.season_by_gameweek = self.results_df.set_index('Game week')['Season'].to_dict()

    def load_player_image(self, player_name):
        image_path = f'player_images/{player_name}.png'
        if os.path.exists(image_path):
            return Image.open(image_path)
        return None

    def calculate_player_stats(self, player, season=None):
        goals_df = self.goals_df
        appearances_df = self.appearances_df
        results_df = self.results_df

        player_goals = goals_df[goals_df['Player'] == player]
        player_appearances = appearances_df[appearances_df['Player'] == player]

        if player_appearances.empty or player_goals.empty:
            return {
                'goals_scored': 0,
                'appearances': 0,
                'avg_team_goals_scored': 0,
                'avg_team_goals_conceded': 0,
                'win_rate': 0,
                'goals_per_game': 0
            }

        gameweek_cols = [col for col in goals_df.columns if col.startswith('Gameweek')]

        total_goals = 0
        total_appearances = 0
        played_gameweeks = []

        for col in gameweek_cols:
            gw_num = int(col.split()[-1])
            if season and self.season_by_gameweek.get(gw_num) != season:
                continue

            appearance = player_appearances[col].values[0]
            goals = player_goals[col].values[0]

            if appearance == 1:
                played_gameweeks.append(gw_num)
                total_appearances += 1
                total_goals += goals
            elif appearance == 0:
                total_goals += goals  # include goals even if no appearance? optional

        relevant_results = results_df[results_df['Game week'].isin(played_gameweeks)]

        avg_goals_for = relevant_results['Score home'].mean() if not relevant_results.empty else 0
        avg_goals_against = relevant_results['Score away'].mean() if not relevant_results.empty else 0

        wins = relevant_results[relevant_results['Result'] == 'Win'].shape[0]
        total_games_played = relevant_results.shape[0]
        win_rate = (wins / total_games_played) * 100 if total_games_played > 0 else 0
        goals_per_game = total_goals / total_appearances if total_appearances > 0 else 0

        return {
            'goals_scored': total_goals,
            'appearances': total_appearances,
            'avg_team_goals_scored': avg_goals_for,
            'avg_team_goals_conceded': avg_goals_against,
            'win_rate': win_rate,
            'goals_per_game': goals_per_game
        }


    def display_player_stats(self, player, season=None):
        player_image = self.load_player_image(player)
        col1, col2 = st.columns([1, 2])
        with col1:
            if player_image:
                st.image(player_image, caption=player, width=200)
            else:
                st.write("Image not available")
        with col2:
            stats = self.calculate_player_stats(player, season=season)
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
        player = st.selectbox('Select a player', self.goals_df['Player'].unique())

        seasons = sorted(self.results_df['Season'].unique())
        tab_labels = ['All Seasons'] + seasons
        tabs = st.tabs(tab_labels)

        with tabs[0]:
            st.subheader("All Seasons")
            self.display_player_stats(player, season=None)

        for i, season in enumerate(seasons):
            with tabs[i + 1]:
                st.subheader(f"Season: {season}")
                self.display_player_stats(player, season=season)


# Instantiate and run
if __name__ == "__main__":
    app = PlayerStatsApp()
    app.run()