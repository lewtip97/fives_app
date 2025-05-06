import streamlit as st
import pandas as pd
import hmac
import io
from datetime import datetime

def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False
    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True
    # Show input for password.
    st.text_input(
        "Enter the password to visit the manager's office:", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Blimey, that was further off than the average Jake shot!")
    return False

# Function to load the CSV files
def load_data():
    results_df = pd.read_csv('data/results_all.csv')
    goals_df = pd.read_csv('data/goals_all.csv')
    appearances_df = pd.read_csv('data/appearances_all.csv')
    return results_df, goals_df, appearances_df

# Function to save data back to CSV
def save_data(results_df, goals_df, appearances_df):
    results_df.to_csv('data/results_all.csv', index=False)
    goals_df.to_csv('data/goals_all.csv', index=False)
    appearances_df.to_csv('data/appearances_all.csv', index=False)

# Admin page
def admin_page():
    st.title('Manager\'s Office - Add New Result')

    results_df, goals_df, appearances_df = load_data()

    # Add new result section
    st.header('Add New Result')

    # Input fields for the new result
    gameweek = st.number_input('Gameweek', min_value=1, max_value=38, key='gameweek')
    season = st.text_input('Season', 'Prem S1', key='season')
    date = st.date_input('Date', datetime.today(), key='date')
    opponent = st.text_input('Opponent', key='opponent')
    friendly = st.selectbox('Friendly', options=[0, 1], index=0, key='friendly')
    result = st.selectbox('Result', options=['Win', 'Loss', 'Draw'], key='result')
    opponent_win_rate = st.number_input('Opponent Win Rate (%)', min_value=0, max_value=100, key='opponent_win_rate')
    opponent_losses = st.number_input('Opponent Losses', min_value=0, key='opponent_losses')
    opponent_form = st.number_input('Opponent Form (%)', min_value=0, max_value=100, key='opponent_form')
    score_home = st.number_input('Home Team Score', min_value=0, key='score_home')
    score_away = st.number_input('Away Team Score', min_value=0, key='score_away')

    # Input for players who played and goals scored
    players = list(appearances_df['Player'])
    players_played = st.multiselect('Select Players Who Played', options=players, key='players_played')
    goals_scored = {}
    for player in players_played:
        goals_scored[player] = st.number_input(f'Goals Scored by {player}', min_value=0, key=f'goals_scored_{player}')

    # Button to add new result
    if st.button('Add New Result'):
        # Add result to the results dataframe
        new_result = {
            'Gameweek': gameweek,
            'Season': season,
            'Date': date.strftime('%d/%m/%y'),
            'opponents': opponent,
            'Friendly': friendly,
            'Result': result,
            'opponent_win_rate': opponent_win_rate,
            'opponent_losses': opponent_losses,
            'opponent_form': opponent_form,
            'Score home': score_home,
            'Score away': score_away
        }
        results_df = results_df.append(new_result, ignore_index=True)

        # Add player appearances and goals to the respective dataframes
        for player in players_played:
            gameweek_column = f'Gameweek {gameweek}'
            appearances_df.loc[appearances_df['Player'] == player, gameweek_column] = 1
            if player in goals_scored:
                goals_df.loc[goals_df['Player'] == player, gameweek_column] = goals_scored[player]

        # Save updated data
        save_data(results_df, goals_df, appearances_df)

        st.success('New result added successfully!')

    # Remove gameweek section
    st.header('Remove Gameweek')

    # Select a gameweek to remove
    gameweeks = results_df['Gameweek'].unique()
    selected_gameweek = st.selectbox('Select Gameweek to Remove', index=None, placeholder = 'Select a gamweek...', options=gameweeks, key='remove_gameweek')

    if selected_gameweek:
        st.warning('Warning: This action cannot be undone!')
        if st.button('Remove Selected Gameweek'):
            st.write(f'remove gameweek {selected_gameweek}')
            st.write('here')
            # Remove the selected gameweek's data from the results dataframe
            results_df = results_df[results_df['Gameweek'] != selected_gameweek]
            st.write('here')
            # Remove the selected gameweek's column from the goals dataframe
            goals_df = goals_df.drop(columns=[f'Gameweek {selected_gameweek}'])
            st.write('here')
            # Remove the selected gameweek's column from the appearances dataframe
            appearances_df = appearances_df.drop(columns=[f'Gameweek {selected_gameweek}'])
            st.write('here')
            # Save updated data
            save_data(results_df, goals_df, appearances_df)

            st.success(f'Gameweek {selected_gameweek} removed successfully!')

                

# Display admin page only if the user enters the correct password
admin_rights = check_password()
if admin_rights:
    admin_page()
