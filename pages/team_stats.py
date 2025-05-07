import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import DataLoader

class TeamStatsApp:
    def __init__(self):
        self.results_df = None

    def load_results_data(self):
        loader = DataLoader()
        return loader.results_data()

    def load_goals_long(self, season=None):
        path = "data/team_stats"
        if season is None or season == "All":
            return pd.read_csv(f"{path}/all_seasons.csv")
        else:
            return pd.read_csv(f"{path}/{season}.csv")

    def display_plot(self, goals_long, title):
        fig = go.Figure()

        # Extended color palette (20+ distinct colors)
        extended_colors = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
            '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
            '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5',
            '#393b79', '#637939', '#8c6d31', '#843c39', '#7b4173'
        ]

        players = goals_long['Player'].unique()
        for i, player in enumerate(players):
            player_data = goals_long[goals_long['Player'] == player]
            fig.add_trace(go.Scatter(
                x=player_data['Gameweek'],
                y=player_data['Cumulative Goals'],
                mode='lines+markers',
                name=player,
                line=dict(color=extended_colors[i % len(extended_colors)])
            ))

        fig.update_layout(
            title=title,
            xaxis_title='Gameweek',
            yaxis_title='Cumulative Goals',
            showlegend=True,
            width=800,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)


    def run(self):
        self.results_df = self.load_results_data()

        st.title("Team Stats - Goals Over Time")
        all_seasons = sorted(self.results_df['Season'].unique().tolist())
        tabs = st.tabs(['All Seasons'] + all_seasons)

        for i, season in enumerate(['All'] + all_seasons):
            with tabs[i]:
                goals_long = self.load_goals_long(season if season != "All" else None)
                title = f"Cumulative Goals - {season}" if season != 'All' else "Cumulative Goals - All Seasons"
                self.display_plot(goals_long, title)

if __name__ == "__main__":
    app = TeamStatsApp()
    app.run()
