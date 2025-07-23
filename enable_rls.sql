-- Enable RLS on all user tables
ALTER TABLE teams ENABLE ROW LEVEL SECURITY;
ALTER TABLE players ENABLE ROW LEVEL SECURITY;
ALTER TABLE opponents ENABLE ROW LEVEL SECURITY;
ALTER TABLE matches ENABLE ROW LEVEL SECURITY;
ALTER TABLE appearances ENABLE ROW LEVEL SECURITY;
ALTER TABLE player_stats ENABLE ROW LEVEL SECURITY;
ALTER TABLE player_gameweek_stats ENABLE ROW LEVEL SECURITY;
ALTER TABLE team_stats ENABLE ROW LEVEL SECURITY;

-- Teams: Only allow access to own teams
CREATE POLICY "Users can access their own teams" ON teams
  FOR ALL
  USING (created_by = auth.uid());

-- Players: Only allow access to own players
CREATE POLICY "Users can access their own players" ON players
  FOR ALL
  USING (created_by = auth.uid());

-- Opponents: Only allow access to own opponents
CREATE POLICY "Users can access their own opponents" ON opponents
  FOR ALL
  USING (created_by = auth.uid());

-- Matches: Only allow access to own matches
CREATE POLICY "Users can access their own matches" ON matches
  FOR ALL
  USING (created_by = auth.uid());

-- Appearances: Only allow access to matches owned by user
CREATE POLICY "Users can access appearances for their own matches" ON appearances
  FOR ALL
  USING (
    match_id IN (
      SELECT id FROM matches WHERE created_by = auth.uid()
    )
  );

-- player_stats: Only allow access to player_stats for players owned by the user
CREATE POLICY "Users can access their own player_stats" ON player_stats
  FOR ALL
  USING (
    player_id IN (
      SELECT id FROM players WHERE created_by = auth.uid()
    )
  );

-- player_gameweek_stats: Only allow access to stats for own players
CREATE POLICY "Users can access their own player_gameweek_stats" ON player_gameweek_stats
  FOR ALL
  USING (
    player_id IN (
      SELECT id FROM players WHERE created_by = auth.uid()
    )
  );

-- team_stats: Only allow access to stats for own teams
CREATE POLICY "Users can access their own team_stats" ON team_stats
  FOR ALL
  USING (
    team_id IN (
      SELECT id FROM teams WHERE created_by = auth.uid()
    )
  ); 