-- Enable UUID generation extension (if not already enabled)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- TEAMS
DROP TABLE IF EXISTS teams CASCADE;
CREATE TABLE teams (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    team_size INTEGER DEFAULT 5,
    created_by UUID NOT NULL, -- Supabase Auth UID
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- PLAYERS
DROP TABLE IF EXISTS players CASCADE;
CREATE TABLE players (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    team_id UUID REFERENCES teams(id) ON DELETE CASCADE,
    profile_picture TEXT, -- URL to player's profile picture
    created_by UUID NOT NULL, -- Supabase Auth UID
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- OPPONENTS
DROP TABLE IF EXISTS opponents CASCADE;
CREATE TABLE opponents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    team_id UUID REFERENCES teams(id) ON DELETE CASCADE,
    created_by UUID NOT NULL, -- Supabase Auth UID
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- MATCHES
DROP TABLE IF EXISTS matches CASCADE;
CREATE TABLE matches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    team_id UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    opponent_id UUID NOT NULL REFERENCES opponents(id) ON DELETE CASCADE,
    score1 INTEGER NOT NULL,
    score2 INTEGER NOT NULL,
    gameweek INTEGER NOT NULL,
    season TEXT NOT NULL,
    played_at TIMESTAMPTZ NOT NULL,
    created_by UUID NOT NULL, -- Supabase Auth UID
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- APPEARANCES
DROP TABLE IF EXISTS appearances CASCADE;
CREATE TABLE appearances (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    match_id UUID NOT NULL REFERENCES matches(id) ON DELETE CASCADE,
    player_id UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    goals INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- PLAYER STATS
DROP TABLE IF EXISTS player_stats CASCADE;
CREATE TABLE player_stats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    season TEXT NOT NULL,
    gameweek INTEGER NOT NULL,
    goals INTEGER NOT NULL DEFAULT 0,
    cumulative_goals INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(player_id, season, gameweek)
);

-- PLAYER GAMEWEEK STATS
DROP TABLE IF EXISTS player_gameweek_stats CASCADE;
CREATE TABLE player_gameweek_stats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    team_id UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    team_name TEXT NOT NULL,
    gameweek INTEGER NOT NULL,
    season TEXT NOT NULL,
    goals INTEGER NOT NULL DEFAULT 0,
    cumulative_goals INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(player_id, season, gameweek)
);
CREATE INDEX IF NOT EXISTS idx_player_gameweek_stats_player_id ON player_gameweek_stats(player_id);
CREATE INDEX IF NOT EXISTS idx_player_gameweek_stats_team_id ON player_gameweek_stats(team_id);

-- TEAM STATS (cumulative per gameweek)
DROP TABLE IF EXISTS team_stats CASCADE;
CREATE TABLE team_stats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    team_id UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    season TEXT NOT NULL,
    gameweek INTEGER NOT NULL,
    games_played INTEGER NOT NULL DEFAULT 0,
    goals_scored INTEGER NOT NULL DEFAULT 0,
    goals_conceded INTEGER NOT NULL DEFAULT 0,
    wins INTEGER NOT NULL DEFAULT 0,
    losses INTEGER NOT NULL DEFAULT 0,
    draws INTEGER NOT NULL DEFAULT 0,
    win_rate FLOAT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(team_id, season, gameweek)
);
CREATE INDEX IF NOT EXISTS idx_team_stats_team_id ON team_stats(team_id);

-- Indexes for performance (optional but recommended)
CREATE INDEX IF NOT EXISTS idx_teams_created_by ON teams(created_by);
CREATE INDEX IF NOT EXISTS idx_players_created_by ON players(created_by);
CREATE INDEX IF NOT EXISTS idx_players_team_id ON players(team_id);
CREATE INDEX IF NOT EXISTS idx_opponents_created_by ON opponents(created_by);
CREATE INDEX IF NOT EXISTS idx_opponents_team_id ON opponents(team_id);
CREATE INDEX IF NOT EXISTS idx_matches_team_id ON matches(team_id);
CREATE INDEX IF NOT EXISTS idx_matches_opponent_id ON matches(opponent_id);
CREATE INDEX IF NOT EXISTS idx_appearances_match_id ON appearances(match_id);
CREATE INDEX IF NOT EXISTS idx_appearances_player_id ON appearances(player_id);
CREATE INDEX IF NOT EXISTS idx_player_stats_player_id ON player_stats(player_id);
CREATE INDEX IF NOT EXISTS idx_team_stats_team_id ON team_stats(team_id); 