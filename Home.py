import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("Bieslas Rejects")
st.write("Up the rejects!")

# Load precomputed data
result_counts = pd.read_csv("data/homepage/result_counts.csv")
goals_summary = pd.read_csv("data/homepage/goals_summary.csv")
recent_results = pd.read_csv("data/homepage/recent_results.csv")['Recent Results'].tolist()
latest_match_df = pd.read_csv("data/homepage/latest_match.csv").iloc[0]

# Extract values
win_count = result_counts.loc[result_counts['Result'] == 'Win', 'Count'].values[0]
draw_count = result_counts.loc[result_counts['Result'] == 'Draw', 'Count'].values[0]
loss_count = result_counts.loc[result_counts['Result'] == 'Loss', 'Count'].values[0]

goals_scored = goals_summary.loc[goals_summary['Metric'] == 'Scored', 'Goals'].values[0]
goals_against = goals_summary.loc[goals_summary['Metric'] == 'Conceded', 'Goals'].values[0]

opponent = latest_match_df['Opponent']
home_score = latest_match_df['Score Home']
away_score = latest_match_df['Score Away']
scorers_text = latest_match_df['Scorers Text']

form_colors = {'Win': '#4CAF50', 'Draw': '#BDBDBD', 'Loss': '#F44336'}

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
