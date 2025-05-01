import streamlit as st
import pages.team_stats as team_stats
import pages.player_stats as player_stats
import pages.match_forecaster as match_forecaster

# Set the theme and config
st.set_page_config(
    page_title="Football Visualisation",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("Bieslas Rejects")
st.write("Up the rejects!")
