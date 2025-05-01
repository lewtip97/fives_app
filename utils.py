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
    results_df = pd.read_csv("data/results.csv")
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
        self.results_df = pd.read_csv("data/results.csv")['Season'].unique().tolist()
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
