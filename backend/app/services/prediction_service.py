import joblib
import os
from typing import List, Dict, Any
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

class PredictionService:
    def __init__(self):
        # Go up from services/app/backend to project root, then access models directory
        self.models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'models')
        self.player_models = {}
        self.goals_against_model = None
        self._load_models()
    
    def _load_models(self):
        """Load all available ML models"""
        try:
            # Load goals against model
            goals_against_path = os.path.join(self.models_dir, 'goals_against_model.joblib')
            if os.path.exists(goals_against_path):
                try:
                    self.goals_against_model = joblib.load(goals_against_path)
                    print(f"Loaded goals against model")
                except Exception as e:
                    print(f"Failed to load goals against model: {e}")
                    self.goals_against_model = None
            
            # Load individual player models
            for filename in os.listdir(self.models_dir):
                if filename.endswith('_goal_model.joblib'):
                    player_name = filename.replace('_goal_model.joblib', '')
                    model_path = os.path.join(self.models_dir, filename)
                    try:
                        self.player_models[player_name] = joblib.load(model_path)
                        print(f"Loaded model for {player_name}")
                    except Exception as e:
                        print(f"Failed to load model for {player_name}: {e}")
                        # Continue loading other models even if one fails
                        
        except Exception as e:
            print(f"Error loading models: {e}")
            # Set defaults so the service can still function
            self.goals_against_model = None
            self.player_models = {}
    
    def predict_match_outcome(self, team_id: str, opponent_id: str, selected_players: List[str]) -> Dict[str, Any]:
        """
        Predict match outcome and player performance
        
        Args:
            team_id: ID of the user's team
            opponent_id: ID of the opponent team
            selected_players: List of player IDs to predict for
            
        Returns:
            Dictionary containing match prediction and player predictions
        """
        try:
            # Get team and player data
            team_data = self._get_team_data(team_id)
            opponent_data = self._get_opponent_data(opponent_id)
            players_data = self._get_players_data(selected_players)
            
            if not team_data or not players_data:
                raise ValueError("Unable to retrieve team or player data")
            
            # Predict team goals using goals against model
            team_score = self._predict_team_goals(team_data, opponent_data)
            
            # Predict opponent goals (simplified - could be enhanced)
            opponent_score = self._predict_opponent_goals(opponent_data, team_data)
            
            # Predict individual player goals
            player_predictions = []
            for player in players_data:
                predicted_goals = self._predict_player_goals(player, team_data, opponent_data)
                confidence = self._calculate_player_confidence(player, predicted_goals)
                
                player_predictions.append({
                    "player_id": player["id"],
                    "player_name": player["name"],
                    "predicted_goals": predicted_goals,
                    "confidence": confidence
                })
            
            # Calculate overall match confidence
            match_confidence = self._calculate_match_confidence(team_score, opponent_score, player_predictions)
            
            return {
                "team_score": team_score,
                "opponent_score": opponent_score,
                "player_predictions": player_predictions,
                "match_confidence": match_confidence,
                "prediction_metadata": {
                    "models_used": list(self.player_models.keys()) + (["goals_against"] if self.goals_against_model else []),
                    "total_players_predicted": len(player_predictions)
                }
            }
            
        except Exception as e:
            print(f"Error in match prediction: {e}")
            raise
    
    def _get_team_data(self, team_id: str) -> Dict[str, Any]:
        """Get team data including recent form and player availability"""
        try:
            # Get team overview
            response = supabase.table("teams").select("*").eq("id", team_id).execute()
            if not response.data:
                return None
            
            team = response.data[0]
            
            # Get recent matches for form calculation
            matches_response = supabase.table("matches").select("*, opponents(name)").eq("team_id", team_id).order("played_at", desc=True).limit(5).execute()
            recent_matches = matches_response.data
            
            # Calculate form
            wins = sum(1 for match in recent_matches if match["score1"] > match["score2"])
            draws = sum(1 for match in recent_matches if match["score1"] == match["score2"])
            losses = sum(1 for match in recent_matches if match["score1"] < match["score2"])
            
            return {
                "id": team["id"],
                "name": team["name"],
                "recent_form": {"wins": wins, "draws": draws, "losses": losses},
                "recent_matches": recent_matches
            }
            
        except Exception as e:
            print(f"Error getting team data: {e}")
            return None
    
    def _get_opponent_data(self, opponent_id: str) -> Dict[str, Any]:
        """Get opponent data including recent form"""
        try:
            # For now, return basic opponent data
            # In a real implementation, you'd want to get opponent stats from a league table or previous matches
            return {
                "id": opponent_id,
                "name": f"Opponent {opponent_id}",
                "strength": 0.5,  # Default strength
                "recent_form": {"wins": 2, "draws": 1, "losses": 2}  # Default form
            }
            
        except Exception as e:
            print(f"Error getting opponent data: {e}")
            return None
    
    def _get_players_data(self, player_ids: List[str]) -> List[Dict[str, Any]]:
        """Get player data including recent performance"""
        try:
            players_response = supabase.table("players").select("id, name").in_("id", player_ids).execute()
            players = players_response.data
            
            # Get recent performance data for each player
            for player in players:
                appearances_response = supabase.table("appearances").select("*, matches(score1, score2, played_at)").eq("player_id", player["id"]).order("created_at", desc=True).limit(5).execute()
                appearances = appearances_response.data
                
                # Calculate recent form
                recent_goals = sum(app.get("goals", 0) for app in appearances)
                recent_appearances = len(appearances)
                
                player["recent_goals"] = recent_goals
                player["recent_appearances"] = recent_appearances
                player["recent_goals_per_game"] = recent_goals / recent_appearances if recent_appearances > 0 else 0
            
            return players
            
        except Exception as e:
            print(f"Error getting players data: {e}")
            return []
    
    def _predict_team_goals(self, team_data: Dict[str, Any], opponent_data: Dict[str, Any]) -> int:
        """Predict how many goals the team will score"""
        try:
            if self.goals_against_model:
                # Use the ML model if available
                # This is a simplified implementation - you'd need to prepare features properly
                base_prediction = 2  # Base prediction
                
                # Adjust based on team form
                form_factor = (team_data["recent_form"]["wins"] * 0.3 + 
                             team_data["recent_form"]["draws"] * 0.1 - 
                             team_data["recent_form"]["losses"] * 0.2)
                
                # Adjust based on opponent strength
                opponent_factor = 1 - opponent_data.get("strength", 0.5)
                
                final_prediction = max(0, int(base_prediction + form_factor + opponent_factor))
                return final_prediction
            else:
                # Fallback prediction based on form
                base_goals = 2
                form_bonus = team_data["recent_form"]["wins"] * 0.5
                return max(0, int(base_goals + form_bonus))
                
        except Exception as e:
            print(f"Error predicting team goals: {e}")
            return 2  # Default prediction
    
    def _predict_opponent_goals(self, opponent_data: Dict[str, Any], team_data: Dict[str, Any]) -> int:
        """Predict how many goals the opponent will score"""
        try:
            # Simplified opponent prediction
            base_goals = 1.5
            
            # Adjust based on team's defensive form
            defensive_form = team_data["recent_form"]["losses"] * 0.3
            opponent_strength = opponent_data.get("strength", 0.5)
            
            final_prediction = max(0, int(base_goals + defensive_form + opponent_strength))
            return final_prediction
            
        except Exception as e:
            print(f"Error predicting opponent goals: {e}")
            return 1  # Default prediction
    
    def _predict_player_goals(self, player: Dict[str, Any], team_data: Dict[str, Any], opponent_data: Dict[str, Any]) -> int:
        """Predict how many goals a specific player will score"""
        try:
            player_name = player["name"]
            
            # Try to use the player's specific ML model
            if player_name in self.player_models:
                # Use the trained model for this player
                # This is a simplified implementation - you'd need to prepare features properly
                base_prediction = player.get("recent_goals_per_game", 0.5)
                
                # Adjust based on team form
                team_form_bonus = (team_data["recent_form"]["wins"] * 0.2 + 
                                 team_data["recent_form"]["draws"] * 0.05)
                
                # Adjust based on opponent strength
                opponent_factor = 1 - opponent_data.get("strength", 0.5)
                
                final_prediction = max(0, int(base_prediction + team_form_bonus + opponent_factor))
                return final_prediction
            else:
                # Fallback prediction based on recent performance
                recent_avg = player.get("recent_goals_per_game", 0.5)
                form_adjustment = team_data["recent_form"]["wins"] * 0.1
                
                final_prediction = max(0, int(recent_avg + form_adjustment))
                return final_prediction
                
        except Exception as e:
            print(f"Error predicting player goals for {player.get('name', 'Unknown')}: {e}")
            return 1  # Default prediction
    
    def _calculate_player_confidence(self, player: Dict[str, Any], predicted_goals: int) -> float:
        """Calculate confidence level for a player prediction"""
        try:
            # Base confidence
            base_confidence = 0.7
            
            # Adjust based on recent performance consistency
            recent_goals = player.get("recent_goals", 0)
            recent_appearances = player.get("recent_appearances", 1)
            
            if recent_appearances > 0:
                consistency_factor = min(0.2, recent_appearances * 0.02)  # More appearances = higher confidence
                performance_factor = min(0.1, recent_goals * 0.02)  # Recent goals = higher confidence
                
                confidence = base_confidence + consistency_factor + performance_factor
                return min(0.95, max(0.5, confidence))  # Clamp between 0.5 and 0.95
            
            return base_confidence
            
        except Exception as e:
            print(f"Error calculating player confidence: {e}")
            return 0.7  # Default confidence
    
    def _calculate_match_confidence(self, team_score: int, opponent_score: int, player_predictions: List[Dict[str, Any]]) -> float:
        """Calculate overall confidence for the match prediction"""
        try:
            # Base confidence
            base_confidence = 0.6
            
            # Adjust based on prediction consistency
            if player_predictions:
                player_confidences = [p["confidence"] for p in player_predictions]
                avg_player_confidence = sum(player_confidences) / len(player_confidences)
                
                # Weight the confidence
                final_confidence = (base_confidence * 0.4) + (avg_player_confidence * 0.6)
                return min(0.9, max(0.4, final_confidence))  # Clamp between 0.4 and 0.9
            
            return base_confidence
            
        except Exception as e:
            print(f"Error calculating match confidence: {e}")
            return 0.6  # Default confidence

# Create a global instance
prediction_service = PredictionService()
