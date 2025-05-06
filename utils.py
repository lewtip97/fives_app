import pandas as pd
import streamlit as st
import os
import json
import const as c

def update_session_state(key, value):
    # Load existing session state from the JSON file
    try:
        with open(c.SESSION_STATE_FILE_PATH, 'r') as f:
            session_state = json.load(f)
    except FileNotFoundError:
        session_state = {}  # Initialize if the file doesn't exist

    # Update the session state
    session_state[key] = value

    # Write the updated session state back to the JSON file
    with open(c.SESSION_STATE_FILE_PATH, 'w') as f:
        json.dump(session_state, f, indent=4)



def get_session_state(key):
    try:
        # Load session state from the JSON file
        with open(c.SESSION_STATE_FILE_PATH, 'r') as f:
            session_state = json.load(f)
            return session_state.get(key, None)  # Return the value or None if the key doesn't exist
    except FileNotFoundError:
        return None  # Return None if the file doesn't exist


def get_season(current_season=None):
    # Load season options from CSV
    results_df = pd.read_csv("data/results_all.csv")
    season_options = sorted(results_df['Season'].dropna().unique(), reverse=True)
    season_options.insert(0, "All seasons")  # Add "All seasons" option at the top

    # Sidebar: Season selector
    st.sidebar.markdown("### Select Season")
    selected_season = st.sidebar.selectbox("Season", season_options)

    # Store selection in session_state
    st.session_state["selected_season"] = selected_season
    current_season = selected_season

class SelectSeason:
    def __init__(self):
        # Load the pipeline families from the CSV
        self.results_df = pd.read_csv("data/results_all.csv")['Season'].unique().tolist()
        self.results_df.append("All seasons")

        # Ensure 'selected_pipeline_family' is in the session state
        if 'selected_season' not in st.session_state:
            st.session_state['selected_season'] = get_session_state('selected_season')

        # Get the currently selected family from the session state
        selected_season = get_session_state('selected_season')
        
        # Determine the default index to use for the selectbox
        default_index = self.results_df.index(selected_season) if selected_season in self.results_df else 0

        st.session_state['selected_season'] = st.sidebar.selectbox(
            'Select season',
            options=self.results_df,
            index=default_index,
            key='season',
            help='Select the season you want to work with.'
        )
        
        # Update the session state with the selected option
        update_session_state('selected_season', st.session_state['selected_season'])


class DataLoader:
    def __init__(self):
        self.data_folder = c.DATA_PATH

    def results_data(self):
        df = pd.read_csv(self.data_folder / 'results_all.csv')
        return df
    
    def goals_data(self):
        df = pd.read_csv(self.data_folder / 'goals_all.csv')
        # Remove row where the first column has value 'TOTAL'
        first_col = df.columns[0]
        df = df[df[first_col] != 'TOTAL']

        # Drop the column named 'TOTAL' if it exists
        if 'TOTAL' in df.columns:
            df = df.drop(columns=['TOTAL'])

        return df

    def appearances_data(self):
        df = pd.read_csv(self.data_folder / 'appearances_all.csv')

        # Remove row where the first column has value 'TOTAL'
        first_col = df.columns[0]
        df = df[df[first_col] != 'TOTAL']

        # Drop the column named 'TOTAL' if it exists
        if 'TOTAL' in df.columns:
            df = df.drop(columns=['TOTAL'])

        return df
    
class CollectGameweeks:
    def __init__(self, season):
        self.season = season
        loader = DataLoader()
        self.results = loader.results_data()  # Store results for reuse
    def collect(self):
        df = self.results

        if self.season != "All seasons":
            df = df[df["Season"] == self.season]

        # Drop NA, get unique values, sort
        gameweeks = sorted(df["Game week"].dropna().unique().tolist())
        return gameweeks
    
class FilterGameweeks:
    def __init__(self, gameweeks):
        self.gameweeks = gameweeks  # e.g., [1, 2, 3]

    def results_filter(self, results_df):
        return results_df[results_df["Game week"].isin(self.gameweeks)]

    def appearances_filter(self, appearances_df):
        cols_to_keep = ["Player"] + [f"Gameweek {gw}" for gw in self.gameweeks]
        return appearances_df[cols_to_keep]

    def goals_filter(self, goals_df):
        cols_to_keep = ["Player"] + [f"Gameweek {gw}" for gw in self.gameweeks]
        return goals_df[cols_to_keep]




        
