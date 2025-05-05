import streamlit as st
import pandas as pd
import os
from PIL import Image
from joblib import load
from utils import DataLoader


class ScorePredictorApp:
    def __init__(self):
        self.loader = DataLoader()
        self.players_df = self.loader.goals_data()
        self.players = self.players_df['Player'].unique()

        # Define the goalkeepers and outfield players
        self.goalkeepers = ['Jack J', 'Keenan']
        self.outfield_players = [player for player in self.players if player not in self.goalkeepers]

        # Retrieve selected goalkeeper and players from session state
        self.selected_goalkeeper = st.session_state.get('selected_goalkeeper', None)
        self.selected_players = st.session_state.get('selected_players', [])

        # Ensure that the selected players are valid outfield players
        self.selected_players = [player for player in self.selected_players if player in self.outfield_players]

        self.form_mapping = {"bad": 0, "average": 33, "good": 66, "great": 100}

    def load_player_image(self, player_name):
        image_path = f'player_images/{player_name}.png'
        return Image.open(image_path) if os.path.exists(image_path) else None

    def display_player_selection(self):
        st.title("Select 6 Players for Score Prediction")

        # Create two columns: one for selection and one for displaying selected players
        left_col, right_col = st.columns([1, 2])  # Left column size 1, Right column size 2

        with left_col:
            # Goalkeeper selection (user can only select one)
            selected_goalkeeper = st.selectbox(
                "Select Goalkeeper", options=self.goalkeepers, index=self.goalkeepers.index(self.selected_goalkeeper) if self.selected_goalkeeper else 0
            )

            # Outfield player selection (user selects 5)
            selected_players = st.multiselect(
                "Select Outfield Players (5 players)", options=self.outfield_players, default=self.selected_players, max_selections=5
            )

            # Opponent form selection
            opponent_form_str = st.selectbox("Select Opponent Form", options=list(self.form_mapping.keys()))
            opponent_form_value = self.form_mapping[opponent_form_str]
            st.session_state.opponent_form_str = opponent_form_str

            # Save session state
            st.session_state.selected_goalkeeper = selected_goalkeeper
            st.session_state.selected_players = selected_players

            if len(selected_players) != 5:
                st.warning("Please select exactly 5 outfield players.")

            if not selected_goalkeeper:
                st.warning("Please select one goalkeeper.")

        with right_col:
            # Display the selected players with images in a 1-3-2 formation
            st.subheader("Selected Players")
            
            # First row: Goalkeeper in the center
            cols = st.columns([1, 2, 1])  # Three columns, with middle column wider
            if selected_goalkeeper:
                with cols[1]:  # Center column
                    player_image = self.load_player_image(selected_goalkeeper)
                    if player_image:
                        st.image(player_image, caption=selected_goalkeeper, width=50)  # Smaller size for clarity

            # Second row: 3 Outfield players (center-aligned in the 3 columns)
            cols = st.columns([1, 1, 1])  # Three columns equally spaced
            for idx, player in enumerate(selected_players[:3]):
                with cols[idx]:
                    player_image = self.load_player_image(player)
                    if player_image:
                        st.image(player_image, caption=player, width=50)  # Smaller size for clarity

            # Third row: 2 Outfield players (center-aligned in the 2 columns)
            cols = st.columns([1, 1])  # Two columns equally spaced
            for idx, player in enumerate(selected_players[3:]):
                with cols[idx]:
                    player_image = self.load_player_image(player)
                    if player_image:
                        st.image(player_image, caption=player, width=50)  # Smaller size for clarity

    def predict_goals(self):
        predictions = {}

        for player in self.selected_players + [self.selected_goalkeeper]:
            model_path = f"models/{player}_goal_model.joblib"
            if not os.path.exists(model_path):
                st.error(f"Model not found for {player}")
                continue

            model = load(model_path)
            all_features = model.feature_names_in_

            # Default feature vector
            features = {feat: 0 for feat in all_features}

            # Mark teammate appearances
            for teammate in self.selected_players:
                if teammate != player:
                    col_name = f"{teammate}_appearance"
                    if col_name in features:
                        features[col_name] = 1

            # Add opponent form
            if 'Opponent_form' in features:
                features['Opponent_form'] = self.form_mapping[st.session_state.opponent_form_str]

            # Create DataFrame and predict
            X = pd.DataFrame([features])
            X = X.reindex(columns=model.feature_names_in_, fill_value=0)
            predicted_goals = model.predict(X)[0]
            predictions[player] = round(predicted_goals, 2)

        return predictions

    def run(self):
        self.display_player_selection()

        if len(self.selected_players) == 5 and self.selected_goalkeeper:
            # Generate score button
            if st.button("Generate Score"):
                predictions = self.predict_goals()
                st.subheader("Predicted Goals per Player")
                for player, goals in predictions.items():
                    st.write(f"**{player}**: {goals} goals")


def run():
    app = ScorePredictorApp()
    app.run()


run()
