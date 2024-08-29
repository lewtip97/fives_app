import random
import datetime
import pandas as pd

class FootballTeamDataGenerator:
    def __init__(self, games_played, players):
        self.games_played = games_played
        self.players = players
        self.results_table = self.generate_results_table()
        self.players_list = [f"Player {i+1}" for i in range(players)]

    def generate_results_table(self):
        results = []
        for week in range(1, self.games_played + 1):
            date = self.generate_random_date(week)
            opponent = self.generate_random_opponent()
            result, score_home, score_away = self.generate_random_result()
            opponent_wins = random.randint(0, week)  # Random wins for the opponent
            opponent_losses = random.randint(0, week)  # Random losses for the opponent
            opponent_form = self.generate_opponent_form(opponent_wins, opponent_losses)
            
            result_row = {
                "Game week": week,
                "Date": date,
                "Opponents": opponent,
                "Result": result,
                "Opponent_wins": opponent_wins,
                "Opponent_losses": opponent_losses,
                "Opponent_form (%)": opponent_form,
                "Score home": score_home,
                "Score away": score_away
            }
            results.append(result_row)
        
        return pd.DataFrame(results)

    def generate_random_date(self, week):
        start_date = datetime.date(2023, 8, 1)
        return start_date + datetime.timedelta(weeks=week)

    def generate_random_opponent(self):
        opponents = ["Team A", "Team B", "Team C", "Team D", "Team E"]
        return random.choice(opponents)

    def generate_random_result(self):
        possible_results = ["Win", "Lose", "Draw"]
        result = random.choice(possible_results)
        score_home, score_away = self.generate_random_scores(result)
        return result, score_home, score_away

    def generate_random_scores(self, result):
        if result == "Win":
            score_home = random.randint(1, 5)
            score_away = random.randint(0, score_home - 1)
        elif result == "Lose":
            score_away = random.randint(1, 5)
            score_home = random.randint(0, score_away - 1)
        else:  # Draw
            score_home = score_away = random.randint(0, 3)
        return score_home, score_away

    def generate_opponent_form(self, wins, losses):
        last_3_matches = random.choices(['W', 'L'], k=3)
        wins_in_last_3 = last_3_matches.count('W')
        win_percentage = (wins_in_last_3 / 3) * 100
        return int(win_percentage)

    def get_results_dataframe(self):
        return self.results_table

    def generate_appearances_and_goals_dataframes(self):
        appearances_data = {f"Gameweek {week+1}": [] for week in range(self.games_played)}
        goals_data = {f"Gameweek {week+1}": [] for week in range(self.games_played)}
        appearances_data['Player'] = self.players_list
        goals_data['Player'] = self.players_list
        
        for week in range(self.games_played):
            # Get the score_home for the current gameweek
            score_home = self.results_table.loc[week, "Score home"]
            
            # Ensure that only up to 7 players appear in each gameweek
            appearances = [0] * self.players
            selected_players = random.sample(range(self.players), 7)
            for idx in selected_players:
                appearances[idx] = 1
            
            # Distribute the score_home among the selected players
            goals = [0] * self.players
            if score_home > 0:
                for _ in range(score_home):
                    selected_scorer = random.choice(selected_players)
                    goals[selected_scorer] += 1

            # Append the generated data to the respective lists
            for player in range(self.players):
                appearances_data[f"Gameweek {week+1}"].append(appearances[player])
                goals_data[f"Gameweek {week+1}"].append(goals[player])
        
        # Convert the dictionaries to DataFrames
        appearances_df = pd.DataFrame(appearances_data)
        goals_df = pd.DataFrame(goals_data)
        
        # Ensure "Player" column is the first column in both DataFrames
        cols = ['Player'] + [col for col in appearances_df if col != 'Player']
        appearances_df = appearances_df[cols]
        goals_df = goals_df[cols]
        
        return appearances_df, goals_df
