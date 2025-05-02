import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import DataLoader

st.set_page_config(layout="wide")

st.title("Bieslas Rejects")
st.write("Up the rejects!")

# Load data
loader = DataLoader()
results_df = loader.results_data()
goals_df = loader.goals_data()

results_df = results_df.sort_values(by='Game week', ascending=True)

# Compute basic stats
win_count = results_df[results_df['Result'] == 'Win'].shape[0]
draw_count = results_df[results_df['Result'] == 'Draw'].shape[0]
loss_count = results_df[results_df['Result'] == 'Loss'].shape[0]
total_matches = win_count + draw_count + loss_count

goals_scored = results_df['Score home'].sum()
goals_against = results_df['Score away'].sum()

recent_results = results_df.tail(5)['Result'].tolist()
form_colors = {'Win': '#4CAF50', 'Draw': '#BDBDBD', 'Loss': '#F44336'}

# Latest match info
latest_match = results_df.iloc[-1]
opponent = latest_match['opponents']
home_score = latest_match['Score home']
away_score = latest_match['Score away']
latest_gameweek = int(latest_match['Game week'])
gw_col = f'Gameweek {latest_gameweek}'

scorers = []
if gw_col in goals_df.columns:
    for _, row in goals_df.iterrows():
        goals = row[gw_col]
        if goals > 0:
            player = row['Player']
            scorers.append(f"{player} ({int(goals)})" if goals > 1 else player)
scorers_text = ', '.join(scorers) if scorers else 'No goalscorers recorded.'

# Layout with 2 rows
top_col1, top_col2 = st.columns(2)

with top_col1:
    st.subheader("All-Time Win %")
    fig_pie = px.pie(
        names=["Win", "Draw", "Loss"],
        values=[win_count, draw_count, loss_count],
        color_discrete_sequence=["#F44336", "#4CAF50", "#9E9E9E"]
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with top_col2:
    st.subheader("All time goals")
    fig_bar = go.Figure(data=[
        go.Bar(x=["Scored", "Conceded"], y=[goals_scored, goals_against],
               marker=dict(color=["green", "red"]))
    ])
    fig_bar.update_layout(
        xaxis_title="",
        yaxis_title="Goals",
        showlegend=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Second row for Form and Latest Match tiles
bottom_col1, bottom_col2 = st.columns(2)

with bottom_col1:
    st.subheader("Recent Form (Last 5)")

    # Use Streamlit columns to show results as colored boxes
    cols = st.columns(len(recent_results))

    for col, result in zip(cols, recent_results):
        letter = result[0]
        color = form_colors.get(result, "#CCCCCC")
        col.markdown(
            f"""
            <div style='
                background-color: {color};
                color: white;
                padding: 8px;
                border-radius: 4px;
                text-align: center;
                font-weight: bold;
                font-size: 16px;
            '>{letter}</div>
            """,
            unsafe_allow_html=True
        )



with bottom_col2:
    st.subheader("Latest Match")
    match_html = f"""
    <div style="border: 1px solid #DDD; padding: 16px; border-radius: 10px; background-color: #f9f9f9;">
        <div style="font-size: 24px; font-weight: bold; margin-bottom: 10px;">
            Bieslas Rejects {home_score}–{away_score} {opponent}
        </div>
        <div style="font-size: 16px; color: #444;">
            <strong>Scorers:</strong> {scorers_text}
        </div>
    </div>
    """
    st.markdown(match_html, unsafe_allow_html=True)
