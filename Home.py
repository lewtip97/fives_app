import streamlit as st
import pandas as pd
#from FootballVisualisation import FootballVisualisation
import os
import tempfile
import pages.team_stats as team_stats
import pages.player_stats as player_stats
import pages.match_forecaster as match_forecaster

# Set the theme of the Streamlit app
st.set_page_config(
    page_title="Football Visualisation",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="auto"
)

# Custom theme with white, yellow, and black colors
st.markdown(
    """
    <style>
    body {
        background-color: white;
        color: black;
    }
    .stTextInput, .stFileUploader, .stSelectbox {
        background-color: white;
        color: black;
    }
    h1, h2, h3, h4 {
        color: black;
    }
    div[data-baseweb="radio"] > div {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main header
st.title("⚽ Bielsas Rejects Season review")

# Instructions
st.markdown(
    """
    Up the rejects!
    """
)
# Sidebar for navigation between pages
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Home", "Player Stats", "Team Stats", "Match forecaster"])

# Home page content
if selection == "Home":
    st.header("Welcome to the Home Page")
    st.write("Up the Rejects!")
    
elif selection == "Player Stats":
    player_stats.run()
    
elif selection == "Team Stats":
    team_stats.run()

elif selection == "Match forecaster":
    match_forecaster.run()



