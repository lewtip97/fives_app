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

        self.selected_goalkeeper = st.session_state.get('selected_goalkeeper', None)
        self.selected_players = [p for p in st.session_state.get('selected_players', []) if p in self.outfield_players]

        self.form_mapping = {"bad": 0, "average": 33, "good": 66, "great": 100}

    def load_player_image(self, player_name):
        image_path = f'player_images/{player_name}.png'
        return Image.open(image_path) if os.path.exists(image_path) else None

    def display_player_selection(self):
        st.title("Select 6 Players for Score Prediction")

        left_col, right_col = st.columns([1, 2])

        with left_col:
            selected_goalkeeper = st.selectbox(
                "Select Goalkeeper", options=self.goalkeepers,
                index=self.goalkeepers.index(self.selected_goalkeeper) if self.selected_goalkeeper else 0
            )

            selected_players = st.multiselect(
                "Select Outfield Players (5 players)",
                options=self.outfield_players,
                default=self.selected_players,
                max_selections=5
            )

            opponent_form_str = st.selectbox("Select Opponent Form", options=list(self.form_mapping.keys()))
            opponent_form_value = self.form_mapping[opponent_form_str]

            # Save to session state
            st.session_state.selected_goalkeeper = selected_goalkeeper
            st.session_state.selected_players = selected_players
            st.session_state.opponent_form_str = opponent_form_str
            st.session_state.opponent_form_value = opponent_form_value

            if len(selected_players) != 5:
                st.warning("Please select exactly 5 outfield players.")
            if not selected_goalkeeper:
                st.warning("Please select one goalkeeper.")

        with right_col:
            st.subheader("Selected Players")

            # 1-3-2 Formation display
            cols = st.columns([1, 2, 1])
            if selected_goalkeeper:
                with cols[1]:
                    img = self.load_player_image(selected_goalkeeper)
                    if img:
                        st.image(img, caption=selected_goalkeeper, width=50)

            cols = st.columns([1, 1, 1])
            for idx, player in enumerate(selected_players[:3]):
                with cols[idx]:
                    img = self.load_player_image(player)
                    if img:
                        st.image(img, caption=player, width=50)

            cols = st.columns([1, 1])
            for idx, player in enumerate(selected_players[3:]):
                with cols[idx]:
                    img = self.load_player_image(player)
                    if img:
                        st.image(img, caption=player, width=50)

    def predict_goals(self):
        predictions = {}

        all_players = self.selected_players + [self.selected_goalkeeper]

        for player in all_players:
            model_path = f"models/{player}_goal_model.joblib"
            if not os.path.exists(model_path):
                st.error(f"Model not found for {player}")
                continue

            model = load(model_path)
            all_features = model.feature_names_in_
            features = {feat: 0 for feat in all_features}

            for teammate in self.selected_players:
                if teammate != player:
                    col = f"{teammate}_appearance"
                    if col in features:
                        features[col] = 1

            if 'Opponent_form' in features:
                features['Opponent_form'] = st.session_state.opponent_form_value

            X = pd.DataFrame([features])
            X = X.reindex(columns=model.feature_names_in_, fill_value=0)
            predicted_goals = model.predict(X)[0]
            predictions[player] = round(predicted_goals, 2)

        return predictions

    def predict_goals_against(self):
        model_path = "models/goals_against_model.joblib"
        if not os.path.exists(model_path):
            st.error("Goals against model not found.")
            return None

        model = load(model_path)
        all_features = model.feature_names_in_
        features = {feat: 0 for feat in all_features}

        for player in self.selected_players + [self.selected_goalkeeper]:
            col = f"{player}_appearance"
            if col in features:
                features[col] = 1

        if 'Opponent_form' in features:
            features['Opponent_form'] = st.session_state.opponent_form_value

        X = pd.DataFrame([features])
        X = X.reindex(columns=model.feature_names_in_, fill_value=0)
        predicted_goals_against = model.predict(X)[0]
        return round(predicted_goals_against, 2)

    def display_scoreboard(self, total_goals_for, goals_against):
        """Displays the score in a football scoreboard style."""
        st.markdown("""
        <style>
            .scoreboard {
                font-size: 48px;
                font-weight: bold;
                text-align: center;
                background-color: #333;
                color: white;
                padding: 10px;
                border-radius: 10px;
            }
            .scoreboard .home, .scoreboard .away {
                font-size: 72px;
                color: white;
            }
            .scoreboard.win {
                background-color: #28a745;
            }
            .scoreboard.draw {
                background-color: #6c757d;
            }
            .scoreboard.loss {
                background-color: #dc3545;
            }
        </style>
        """, unsafe_allow_html=True)

        # Round to whole numbers (no decimal places)
        total_goals_for = int(round(total_goals_for))  # Convert to integer
        goals_against = int(round(goals_against))  # Convert to integer

        # Determine the scoreboard color
        if total_goals_for > goals_against:
            result_class = 'win'
        elif total_goals_for == goals_against:
            result_class = 'draw'
        else:
            result_class = 'loss'

        st.markdown(f"""
        <div class="scoreboard {result_class}">
            <span class="home">{total_goals_for}</span> - <span class="away">{goals_against}</span>
        </div>
        """, unsafe_allow_html=True)

    def run(self):
        self.display_player_selection()

        if len(self.selected_players) == 5 and self.selected_goalkeeper:
            if st.button("Predict Score"):
                predictions = self.predict_goals()
                goals_against = self.predict_goals_against()

                # Sum up goals first, then round the total
                total_goals_for = sum(predictions.values())
                total_goals_for = round(total_goals_for)  # Round the total after summing

                # Display score in football scoreboard format
                if goals_against is not None:
                    self.display_scoreboard(total_goals_for, goals_against)


def run():
    app = ScorePredictorApp()
    app.run()


run()
