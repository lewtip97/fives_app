-- Clear Data Options Script
-- Choose which level of data clearing you want to perform

-- OPTION 1: Clear only match data (recommended for testing)
-- This keeps your teams, players, and opponents but removes all match history
BEGIN;

-- Clear match-related data
DELETE FROM appearances;
DELETE FROM matches;
DELETE FROM player_stats;
DELETE FROM player_gameweek_stats;
DELETE FROM team_stats;

-- Verify match data is cleared
SELECT 'Match data cleared successfully' as status;

COMMIT;

-- OPTION 2: Clear everything except teams (if you want to keep team structure)
-- Uncomment the lines below if you want this option instead
/*
BEGIN;

DELETE FROM appearances;
DELETE FROM matches;
DELETE FROM player_stats;
DELETE FROM player_gameweek_stats;
DELETE FROM team_stats;
DELETE FROM players;
DELETE FROM opponents;

-- Verify data is cleared
SELECT 'All data cleared except teams' as status;

COMMIT;
*/

-- OPTION 3: Complete reset (nuclear option - clears everything)
-- Uncomment the lines below if you want to start completely fresh
/*
BEGIN;

DELETE FROM appearances;
DELETE FROM matches;
DELETE FROM player_stats;
DELETE FROM player_gameweek_stats;
DELETE FROM team_stats;
DELETE FROM players;
DELETE FROM opponents;
DELETE FROM teams;

-- Verify everything is cleared
SELECT 'Complete reset - all data cleared' as status;

COMMIT;
*/

-- Check current state of all tables
SELECT 
    'appearances' as table_name, 
    COUNT(*) as record_count 
FROM appearances
UNION ALL
SELECT 'matches', COUNT(*) FROM matches
UNION ALL
SELECT 'player_stats', COUNT(*) FROM player_stats
UNION ALL
SELECT 'player_gameweek_stats', COUNT(*) FROM player_gameweek_stats
UNION ALL
SELECT 'team_stats', COUNT(*) FROM team_stats
UNION ALL
SELECT 'players', COUNT(*) FROM players
UNION ALL
SELECT 'opponents', COUNT(*) FROM opponents
UNION ALL
SELECT 'teams', COUNT(*) FROM teams
ORDER BY table_name;
