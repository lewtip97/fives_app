#!/usr/bin/env python3
"""
Clear Database Data Script
This script clears match-related data from your database so you can test if the system correctly registers new data.
"""

import os
import sys
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from supabase import create_client, Client
    
    # Load environment variables
    load_dotenv()
    
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
    
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        print("❌ Error: SUPABASE_URL and SUPABASE_ANON_KEY must be set in your .env file")
        sys.exit(1)
    
    # Create Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    
    def clear_match_data():
        """Clear all match-related data"""
        print("🧹 Clearing match data...")
        
        try:
            # Clear appearances (player goals in matches)
            result = supabase.table("appearances").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
            print(f"✅ Cleared {len(result.data) if result.data else 0} appearances")
            
            # Clear matches
            result = supabase.table("matches").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
            print(f"✅ Cleared {len(result.data) if result.data else 0} matches")
            
            # Clear player stats
            result = supabase.table("player_stats").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
            print(f"✅ Cleared {len(result.data) if result.data else 0} player stats")
            
            # Clear player gameweek stats
            result = supabase.table("player_gameweek_stats").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
            print(f"✅ Cleared {len(result.data) if result.data else 0} player gameweek stats")
            
            # Clear team stats
            result = supabase.table("team_stats").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
            print(f"✅ Cleared {len(result.data) if result.data else 0} team stats")
            
            print("\n🎉 Match data cleared successfully!")
            
        except Exception as e:
            print(f"❌ Error clearing data: {e}")
            return False
        
        return True
    
    def clear_all_data():
        """Clear all data including teams and players"""
        print("🧹 Clearing ALL data...")
        
        try:
            # Clear everything in the correct order (respecting foreign keys)
            result = supabase.table("appearances").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
            print(f"✅ Cleared {len(result.data) if result.data else 0} appearances")
            
            result = supabase.table("matches").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
            print(f"✅ Cleared {len(result.data) if result.data else 0} matches")
            
            result = supabase.table("player_stats").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
            print(f"✅ Cleared {len(result.data) if result.data else 0} player stats")
            
            result = supabase.table("player_gameweek_stats").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
            print(f"✅ Cleared {len(result.data) if result.data else 0} player gameweek stats")
            
            result = supabase.table("team_stats").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
            print(f"✅ Cleared {len(result.data) if result.data else 0} team stats")
            
            result = supabase.table("players").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
            print(f"✅ Cleared {len(result.data) if result.data else 0} players")
            
            result = supabase.table("opponents").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
            print(f"✅ Cleared {len(result.data) if result.data else 0} opponents")
            
            result = supabase.table("teams").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
            print(f"✅ Cleared {len(result.data) if result.data else 0} teams")
            
            print("\n🎉 ALL data cleared successfully!")
            
        except Exception as e:
            print(f"❌ Error clearing data: {e}")
            return False
        
        return True
    
    def check_data_status():
        """Check the current status of all tables"""
        print("\n📊 Current Data Status:")
        print("-" * 40)
        
        tables = [
            "appearances", "matches", "player_stats", 
            "player_gameweek_stats", "team_stats", 
            "players", "opponents", "teams"
        ]
        
        for table in tables:
            try:
                result = supabase.table(table).select("id", count="exact").execute()
                count = result.count if hasattr(result, 'count') else len(result.data) if result.data else 0
                print(f"{table:25}: {count:3} records")
            except Exception as e:
                print(f"{table:25}: ERROR - {e}")
    
    def main():
        print("🗑️  Database Data Clearer")
        print("=" * 40)
        print("Choose an option:")
        print("1. Clear match data only (keep teams/players)")
        print("2. Clear all data (complete reset)")
        print("3. Check current data status")
        print("4. Exit")
        
        while True:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                if clear_match_data():
                    check_data_status()
                break
            elif choice == "2":
                confirm = input("⚠️  This will delete ALL data including teams and players. Are you sure? (yes/no): ").strip().lower()
                if confirm == "yes":
                    if clear_all_data():
                        check_data_status()
                else:
                    print("Operation cancelled.")
                break
            elif choice == "3":
                check_data_status()
                break
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you have the required dependencies installed:")
    print("pip install python-dotenv supabase")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
