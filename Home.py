import streamlit as st
import pandas as pd
#from FootballVisualisation import FootballVisualisation
import os
import tempfile
import pages.team_stats as team_stats

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
    st.header("Player Statistics")
    st.write("This is the player stats page. (More content will come here)")
    # You can include content from other pages/files if needed.
    
elif selection == "Team Stats":
    team_stats.run()

elif selection == "Match forecaster":
    st.header("Team Visualisation")
    st.write("This is where the Football Visualisation will appear.")



