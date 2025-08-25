import os
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

class ActivityTracker:
    def __init__(self):
        self.supabase = supabase
    
    def get_recent_activities(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent activities for a user, including:
        - Recent matches played
        - Player milestones (goals, appearances)
        - Team changes (players added/removed)
        """
        print(f"🔍 ActivityTracker: Getting recent activities for user {user_id}")
        activities = []
        
        try:
            # Get user's teams
            print(f"🔍 ActivityTracker: Querying teams for user {user_id}")
            teams_response = self.supabase.table("teams").select("id, name").eq("created_by", user_id).execute()
            user_teams = teams_response.data
            print(f"🔍 ActivityTracker: Found {len(user_teams)} teams: {user_teams}")
            
            if not user_teams:
                print("🔍 ActivityTracker: No teams found, returning empty activities")
                return activities
            
            team_ids = [team["id"] for team in user_teams]
            print(f"🔍 ActivityTracker: Team IDs: {team_ids}")
            
            # 1. Recent matches (last 7 days)
            print("🔍 ActivityTracker: Getting recent matches...")
            recent_matches = self._get_recent_matches(team_ids, limit=5)
            print(f"🔍 ActivityTracker: Found {len(recent_matches)} recent matches")
            activities.extend(recent_matches)
            
            # 2. Player milestones (goals, appearances)
            print("🔍 ActivityTracker: Getting player milestones...")
            milestones = self._get_player_milestones(team_ids, limit=3)
            print(f"🔍 ActivityTracker: Found {len(milestones)} milestones")
            activities.extend(milestones)
            
            # 3. Team changes (players added/removed)
            print("🔍 ActivityTracker: Getting team changes...")
            team_changes = self._get_team_changes(team_ids, limit=2)
            print(f"🔍 ActivityTracker: Found {len(team_changes)} team changes")
            activities.extend(team_changes)
            
            # Sort all activities by timestamp and take the most recent
            activities.sort(key=lambda x: x.get('timestamp', datetime.min), reverse=True)
            print(f"🔍 ActivityTracker: Total activities found: {len(activities)}")
            
            return activities[:limit]
            
        except Exception as e:
            print(f"❌ ActivityTracker: Error getting recent activities: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _get_recent_matches(self, team_ids: List[str], limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent matches with basic stats"""
        try:
            print(f"🔍 ActivityTracker: Getting recent matches for teams: {team_ids}")
            # Get matches from last 7 days
            week_ago = (datetime.now() - timedelta(days=7)).isoformat()
            print(f"🔍 ActivityTracker: Looking for matches since: {week_ago}")
            
            matches_response = self.supabase.table("matches").select(
                "*, opponents(name), teams(name)"
            ).in_("team_id", team_ids).gte("played_at", week_ago).order("played_at", desc=True).limit(limit).execute()
            
            matches = matches_response.data
            print(f"🔍 ActivityTracker: Raw matches response: {matches}")
            activities = []
            
            for match in matches:
                print(f"🔍 ActivityTracker: Processing match: {match}")
                # Get top scorers for this match
                appearances_response = self.supabase.table("appearances").select(
                    "*, players(name)"
                ).eq("match_id", match["id"]).gt("goals", 0).order("goals", desc=True).limit(3).execute()
                
                top_scorers = []
                for appearance in appearances_response.data:
                    if appearance.get("goals", 0) > 0:
                        top_scorers.append(f"{appearance['players']['name']} ({appearance['goals']} goals)")
                
                # Create activity entry
                activity = {
                    'type': 'match',
                    'id': match['id'],
                    'title': f"{match['teams']['name']} vs {match['opponents']['name']}",
                    'description': f"Final Score: {match['score1']}-{match['score2']}",
                    'details': f"{', '.join(top_scorers)}" if top_scorers else "No goals scored",
                    'timestamp': match['played_at'],
                    'icon': '⚽',
                    'color': 'primary',
                    'team_id': match['team_id'],
                    'opponent_id': match['opponent_id']
                }
                
                activities.append(activity)
            
            print(f"🔍 ActivityTracker: Created {len(activities)} match activities")
            return activities
            
        except Exception as e:
            print(f"❌ ActivityTracker: Error getting recent matches: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _get_player_milestones(self, team_ids: List[str], limit: int = 3) -> List[Dict[str, Any]]:
        """Get player milestones (goals, appearances)"""
        try:
            milestones = []
            
            # Get all players for user's teams
            players_response = self.supabase.table("players").select("id, name, team_id").in_("team_id", team_ids).execute()
            players = players_response.data
            
            for player in players:
                # Get player's total goals and appearances
                appearances_response = self.supabase.table("appearances").select(
                    "*, matches(team_id)"
                ).eq("player_id", player["id"]).execute()
                
                appearances = appearances_response.data
                total_goals = sum(app.get("goals", 0) for app in appearances)
                total_appearances = len(appearances)
                
                # Check for goal milestones (10, 25, 50, 100)
                goal_milestones = [10, 25, 50, 100]
                for milestone in goal_milestones:
                    if total_goals >= milestone and total_goals < milestone + 10:  # Within 10 goals of milestone
                        # Check if this milestone was reached recently
                        recent_goals = [app for app in appearances if app.get("goals", 0) > 0]
                        if recent_goals:
                            latest_goal = max(recent_goals, key=lambda x: x.get("created_at", ""))
                            if latest_goal:
                                milestone_activity = {
                                    'type': 'milestone',
                                    'id': f"milestone_{player['id']}_{milestone}",
                                    'title': f"{player['name']} Reached {milestone} Goals!",
                                    'description': f"Milestone achieved in recent match",
                                    'details': f"Total goals: {total_goals}",
                                    'timestamp': latest_goal.get("created_at", datetime.now().isoformat()),
                                    'icon': '🏆',
                                    'color': 'success',
                                    'player_id': player['id'],
                                    'milestone_type': 'goals',
                                    'milestone_value': milestone
                                }
                                milestones.append(milestone_activity)
                                break
                
                # Check for appearance milestones (10, 25, 50, 100)
                appearance_milestones = [10, 25, 50, 100]
                for milestone in appearance_milestones:
                    if total_appearances >= milestone and total_appearances < milestone + 5:  # Within 5 appearances of milestone
                        if appearances:
                            latest_appearance = max(appearances, key=lambda x: x.get("created_at", ""))
                            if latest_appearance:
                                milestone_activity = {
                                    'type': 'milestone',
                                    'id': f"milestone_{player['id']}_{milestone}_apps",
                                    'title': f"{player['name']} Reached {milestone} Appearances!",
                                    'description': f"Milestone achieved in recent match",
                                    'details': f"Total appearances: {total_appearances}",
                                    'timestamp': latest_appearance.get("created_at", datetime.now().isoformat()),
                                    'icon': '👟',
                                    'color': 'warning',
                                    'player_id': player['id'],
                                    'milestone_type': 'appearances',
                                    'milestone_value': milestone
                                }
                                milestones.append(milestone_activity)
                                break
            
            # Sort by timestamp and take most recent
            milestones.sort(key=lambda x: x.get('timestamp', datetime.min), reverse=True)
            return milestones[:limit]
            
        except Exception as e:
            print(f"Error getting player milestones: {e}")
            return []
    
    def _get_team_changes(self, team_ids: List[str], limit: int = 2) -> List[Dict[str, Any]]:
        """Get recent team changes (players added/removed)"""
        try:
            changes = []
            
            # Get recent player additions (last 30 days)
            month_ago = (datetime.now() - timedelta(days=30)).isoformat()
            
            # Note: We can't directly track player deletions, but we can track recent additions
            # In a real system, you might want to add audit logs for deletions
            recent_players_response = self.supabase.table("players").select(
                "*, teams(name)"
            ).in_("team_id", team_ids).gte("created_at", month_ago).order("created_at", desc=True).limit(limit).execute()
            
            recent_players = recent_players_response.data
            
            for player in recent_players:
                change_activity = {
                    'type': 'team_change',
                    'id': f"player_added_{player['id']}",
                    'title': f"New Player Added",
                    'description': f"{player['name']} joined {player['teams']['name']}",
                    'details': f"Player added to team",
                    'timestamp': player['created_at'],
                    'icon': '👤',
                    'color': 'info',
                    'player_id': player['id'],
                    'team_id': player['team_id'],
                    'change_type': 'player_added'
                }
                
                changes.append(change_activity)
            
            return changes
            
        except Exception as e:
            print(f"Error getting team changes: {e}")
            return []
    
    def format_timestamp(self, timestamp: str) -> str:
        """Format timestamp to relative time (e.g., '2 hours ago')"""
        try:
            if isinstance(timestamp, str):
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            else:
                dt = timestamp
            
            now = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.now()
            diff = now - dt
            
            if diff.days > 0:
                return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
            elif diff.seconds >= 3600:
                hours = diff.seconds // 3600
                return f"{hours} hour{'s' if hours != 1 else ''} ago"
            elif diff.seconds >= 60:
                minutes = diff.seconds // 60
                return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
            else:
                return "Just now"
                
        except Exception as e:
            print(f"Error formatting timestamp: {e}")
            return "Unknown time"

# Create a global instance
activity_tracker = ActivityTracker()
