import streamlit as st
import pandas as pd
import altair as alt
import os
import plotly.graph_objects as go


def run():
    # Set up the title for the Player Stats page
    st.title("Player Stats - Goals Over Time")

    # Load the data
    @st.cache_data
    def load_data():
        # Loading goals.csv from the 'data' directory
        data = pd.read_csv('data/goals.csv')
        return data

    # Load the player images from the 'player_images' folder
    def load_player_image(player_name):
        image_path = f'player_images/{player_name}.png'
        if os.path.exists(image_path):
            return image_path
        else:
            return None  # Return None if image doesn't exist

    # Call the load_data function to read in the CSV
    goals_df = load_data()

    # Convert the dataframe from wide to long format for easier plotting
    goals_long = pd.melt(goals_df, id_vars=['Player'], var_name='Gameweek', value_name='Goals')

    # Clean the 'Gameweek' column to extract only the numeric part
    goals_long['Gameweek'] = goals_long['Gameweek'].str.extract('(\d+)').astype(int)

    # Sort the data by player and gameweek
    goals_long = goals_long.sort_values(by=['Player', 'Gameweek'])

    # Calculate the cumulative goals for each player
    goals_long['Cumulative Goals'] = goals_long.groupby('Player')['Goals'].cumsum()

    # Create an interactive Altair chart (without legend)
    chart = alt.Chart(goals_long).mark_line(point=True).encode(
        x=alt.X('Gameweek:O', title='Gameweek'),
        y=alt.Y('Cumulative Goals:Q', title='Cumulative Goals'),
        color='Player:N',  # This assigns a unique color per player
        tooltip=['Player', 'Gameweek', 'Cumulative Goals']
    ).properties(
        title='Cumulative Goals Scored Over Time',
        width=1200,
        height=600
    ).interactive()  # This makes the chart interactive (zoom/pan)

    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)

    # For each player, display their image at the bottom of the chart
    # Get the last gameweek and their final cumulative score
    final_scores = goals_long.groupby('Player').tail(1)


    # Create Plotly figure
    fig = go.Figure()

    # Add a line for each player
    for player in goals_long['Player'].unique():
        player_data = goals_long[goals_long['Player'] == player]
        fig.add_trace(go.Scatter(
            x=player_data['Gameweek'],
            y=player_data['Cumulative Goals'],
            mode='lines+markers',
            name=player
        ))

    # Overlay images at the final gameweek
    final_scores = goals_long.groupby('Player').tail(1)
    for idx, row in final_scores.iterrows():
        player = row['Player']
        final_goals = row['Cumulative Goals']
        final_gameweek = row['Gameweek']

        # Load the player's image
        player_image = load_player_image(player)

        if player_image:
            fig.add_layout_image(
            dict(
                source="player_images/Player 1.png",
                x=[final_gameweek],
                y=[final_goals],
                sizex = 0.8,
                sizey = 0.8
            ))

    # Update layout to remove legend (if desired)
    fig.update_layout(
        title='Cumulative Goals Scored Over Time',
        xaxis_title='Gameweek',
        yaxis_title='Cumulative Goals',
        showlegend=True,
        width=800,
        height=400
    )
    # Display the Plotly figure in Streamlit
    st.plotly_chart(fig, use_container_width=True)


    # Create a placeholder for images to align them based on final scores
    st.markdown("### Final Scores (Players with Images)")

    for idx, row in final_scores.iterrows():
        player = row['Player']
        final_goals = row['Cumulative Goals']
        final_gameweek = row['Gameweek']

        # Load the player's image
        player_image = load_player_image(player)

        if player_image:
            # Display player image with their final gameweek score
            st.image(player_image, caption=f"{player}: {final_goals} goals (Gameweek {final_gameweek})", width=100)
