-- Clear Match Data Script
-- This script will clear all match-related data so you can test if the system correctly registers new data

-- Clear appearances (player goals in matches)
DELETE FROM appearances;

-- Clear matches
DELETE FROM matches;

-- Clear player stats
DELETE FROM player_stats;

-- Clear player gameweek stats
DELETE FROM player_gameweek_stats;

-- Clear team stats
DELETE FROM team_stats;

-- Reset sequences if any (PostgreSQL will handle this automatically with UUIDs)

-- Optional: Clear opponents if you want to start completely fresh
-- DELETE FROM opponents;

-- Optional: Clear players if you want to start completely fresh
-- DELETE FROM players;

-- Optional: Clear teams if you want to start completely fresh
-- DELETE FROM teams;

-- Verify tables are empty
SELECT 'appearances' as table_name, COUNT(*) as record_count FROM appearances
UNION ALL
SELECT 'matches', COUNT(*) FROM matches
UNION ALL
SELECT 'player_stats', COUNT(*) FROM player_stats
UNION ALL
SELECT 'player_gameweek_stats', COUNT(*) FROM player_gameweek_stats
UNION ALL
SELECT 'team_stats', COUNT(*) FROM team_stats
ORDER BY table_name;
