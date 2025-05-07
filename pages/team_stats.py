import streamlit as st
import pandas as pd
import altair as alt
import os
import plotly.graph_objects as go
from PIL import Image
from utils import SelectSeason, DataLoader



class TeamStatsApp:
    def __init__(self):
        self.goals_df = None
        self.results_df = None

    def load_goals_data(self):
        loader = DataLoader()
        return loader.goals_data()

    def load_results_data(self):
        loader = DataLoader()
        return loader.results_data()

    def load_player_image(self, player_name):
        image_path = f'player_images/{player_name}.png'
        return image_path if os.path.exists(image_path) else None

    def prepare_goals_long(self, df):
        goals_long = pd.melt(df, id_vars=['Player'], var_name='Gameweek', value_name='Goals')
        goals_long['Gameweek'] = goals_long['Gameweek'].str.extract(r'(\d+)').astype(int)
        goals_long = goals_long.sort_values(by=['Player', 'Gameweek'])
        goals_long['Cumulative Goals'] = goals_long.groupby('Player')['Goals'].cumsum()
        return goals_long

    def get_gameweeks_for_season(self, season):
        season_weeks = self.results_df[self.results_df['Season'] == season]['Gameweek']
        return season_weeks.tolist()

    def display_plot(self, goals_long, title):
        fig = go.Figure()

        for player in goals_long['Player'].unique():
            player_data = goals_long[goals_long['Player'] == player]
            fig.add_trace(go.Scatter(
                x=player_data['Gameweek'],
                y=player_data['Cumulative Goals'],
                mode='lines+markers',
                name=player
            ))

        occupied_positions = {}
        x_offset = 0.4
        y_offset = 0

        final_scores = goals_long.groupby('Player').tail(1)
        for _, row in final_scores.iterrows():
            player = row['Player']
            final_goals = row['Cumulative Goals']
            final_gameweek = row['Gameweek']
            player_image = self.load_player_image(player)

            if player_image:
                key = (final_gameweek, final_goals)
                occurrences = occupied_positions.get(key, 0)
                new_x = final_gameweek + (occurrences * x_offset)
                new_y = final_goals + (occurrences * y_offset)
                occupied_positions[key] = occurrences + 1

                fig.add_layout_image(dict(
                    source=Image.open(player_image),
                    x=new_x,
                    y=new_y,
                    xref="x",
                    yref="y",
                    sizex=1,
                    sizey=1,
                    xanchor="center",
                    yanchor="middle",
                    layer="above"
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
        self.goals_df = self.load_goals_data()
        self.results_df = self.load_results_data()

        st.title("Team Stats - Goals Over Time")

        all_seasons = self.results_df['Season'].unique().tolist()
        all_seasons.sort()
        tabs = st.tabs(['All Seasons'] + all_seasons)

        for i, season in enumerate(['All'] + all_seasons):
            with tabs[i]:
                if season == 'All':
                    goals_long = self.prepare_goals_long(self.goals_df)
                else:
                    season_gameweeks = self.get_gameweeks_for_season(season)
                    gameweek_cols = [f'Gameweek {int(gw)}' for gw in season_gameweeks if f'Gameweek {int(gw)}' in self.goals_df.columns]
                    filtered_df = self.goals_df[['Player'] + gameweek_cols]
                    goals_long = self.prepare_goals_long(filtered_df)

                    # Remap Gameweek to start from 1 for plotting
                    mapping = {gw: i+1 for i, gw in enumerate(sorted(goals_long['Gameweek'].unique()))}
                    goals_long['Gameweek'] = goals_long['Gameweek'].map(mapping)

                title = f"Cumulative Goals - {season}" if season != 'All' else "Cumulative Goals - All Seasons"
                self.display_plot(goals_long, title)


# To run the app
if __name__ == "__main__":
    app = TeamStatsApp()
    app.run()