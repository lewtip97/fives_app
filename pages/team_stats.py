import streamlit as st
import pandas as pd
import altair as alt
import os
import plotly.graph_objects as go
from PIL import Image
from utils import SelectSeason, DataLoader



def run():
    # season select
    SelectSeason()
    # Set up the title for the Player Stats page
    st.title("Team Stats - Goals Over Time")

    # Load the data
    @st.cache_data
    def load_data():
        # Loading goals.csv from the 'data' directory
        loader = DataLoader()
        data = loader.goals_data()
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

    # Dictionary to track occupied positions (keys are tuples of (gameweek, cumulative_goals))
    occupied_positions = {}

    # Define the offset for stacking images
    x_offset = 0.4  # Offset value to place images side by side
    y_offset = 0  # Vertical offset (optional, adjust if needed)

    # Overlay images at the final gameweek
    final_scores = goals_long.groupby('Player').tail(1)
    for idx, row in final_scores.iterrows():
        player = row['Player']
        final_goals = row['Cumulative Goals']
        final_gameweek = row['Gameweek']

        # Load the player's image
        player_image = load_player_image(player)

        if player_image:
            # Check if the coordinates are already occupied
            if (final_gameweek, final_goals) in occupied_positions:
                # Get the number of times the position is already occupied
                occurrences = occupied_positions[(final_gameweek, final_goals)]
                # Update the position with an offset
                new_x = final_gameweek + (occurrences * x_offset)
                new_y = final_goals + (occurrences * y_offset)  # Optional, adjust vertical stacking if needed
                # Increment the count of occurrences
                occupied_positions[(final_gameweek, final_goals)] += 1
            else:
                # If position is not occupied, place the image at the original position
                new_x = final_gameweek
                new_y = final_goals
                # Mark the position as occupied with the first occurrence
                occupied_positions[(final_gameweek, final_goals)] = 1

            # Add the player's image to the plot at the updated position
            fig.add_layout_image(
                dict(
                    source=Image.open(player_image),
                    x=new_x,  # Use the adjusted x coordinate
                    y=new_y,  # Use the adjusted y coordinate
                    xref="x",  # Reference x-axis
                    yref="y",  # Reference y-axis
                    sizex=1,   # Adjust the size of the image as per your needs
                    sizey=1,
                    xanchor="center",  # Center the image at the data point
                    yanchor="middle",
                    layer="above"
                )
            )


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



run()