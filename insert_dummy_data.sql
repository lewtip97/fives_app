-- Use this UUID for all created_by fields (replace with your own if needed)
-- '00000000-0000-0000-0000-000000000000'

-- TEAMS
INSERT INTO teams (id, name, created_by)
VALUES
  ('11111111-1111-1111-1111-111111111111', 'Red Rockets', '00000000-0000-0000-0000-000000000000'),
  ('22222222-2222-2222-2222-222222222222', 'Blue Blizzards', '00000000-0000-0000-0000-000000000000');

-- PLAYERS
INSERT INTO players (id, name, position, created_by)
VALUES
  ('a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1', 'Alice', 'Forward', '00000000-0000-0000-0000-000000000000'),
  ('a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2', 'Bob', 'Midfielder', '00000000-0000-0000-0000-000000000000'),
  ('a3a3a3a3-a3a3-a3a3-a3a3-a3a3a3a3a3a3', 'Charlie', 'Defender', '00000000-0000-0000-0000-000000000000'),
  ('a4a4a4a4-a4a4-a4a4-a4a4-a4a4a4a4a4a4', 'Diana', 'Goalkeeper', '00000000-0000-0000-0000-000000000000'),
  ('b1b1b1b1-b1b1-b1b1-b1b1-b1b1b1b1b1b1', 'Eve', 'Forward', '00000000-0000-0000-0000-000000000000'),
  ('b2b2b2b2-b2b2-b2b2-b2b2-b2b2b2b2b2b2', 'Frank', 'Midfielder', '00000000-0000-0000-0000-000000000000'),
  ('b3b3b3b3-b3b3-b3b3-b3b3-b3b3b3b3b3b3', 'Grace', 'Defender', '00000000-0000-0000-0000-000000000000'),
  ('b4b4b4b4-b4b4-b4b4-b4b4-b4b4b4b4b4b4', 'Heidi', 'Goalkeeper', '00000000-0000-0000-0000-000000000000');

-- OPPONENTS
INSERT INTO opponents (id, name, created_by)
VALUES
  ('33333333-3333-3333-3333-333333333333', 'Green Giants', '00000000-0000-0000-0000-000000000000'),
  ('44444444-4444-4444-4444-444444444444', 'Yellow Yetis', '00000000-0000-0000-0000-000000000000');

-- MATCHES
INSERT INTO matches (id, team_id, opponent_id, score1, score2, gameweek, season, played_at, created_by)
VALUES
  -- Red Rockets vs Green Giants, Gameweek 1
  ('aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaa1', '11111111-1111-1111-1111-111111111111', '33333333-3333-3333-3333-333333333333', 3, 2, 1, '2024', '2024-01-10T19:00:00Z', '00000000-0000-0000-0000-000000000000'),
  -- Red Rockets vs Yellow Yetis, Gameweek 2
  ('aaaaaaa2-aaaa-aaaa-aaaa-aaaaaaaaaaa2', '11111111-1111-1111-1111-111111111111', '44444444-4444-4444-4444-444444444444', 1, 1, 2, '2024', '2024-01-17T19:00:00Z', '00000000-0000-0000-0000-000000000000'),
  -- Blue Blizzards vs Green Giants, Gameweek 1
  ('bbbbbbb1-bbbb-bbbb-bbbb-bbbbbbbbbbb1', '22222222-2222-2222-2222-222222222222', '33333333-3333-3333-3333-333333333333', 2, 2, 1, '2024', '2024-01-10T20:00:00Z', '00000000-0000-0000-0000-000000000000'),
  -- Blue Blizzards vs Yellow Yetis, Gameweek 2
  ('bbbbbbb2-bbbb-bbbb-bbbb-bbbbbbbbbbb2', '22222222-2222-2222-2222-222222222222', '44444444-4444-4444-4444-444444444444', 0, 1, 2, '2024', '2024-01-17T20:00:00Z', '00000000-0000-0000-0000-000000000000');

-- APPEARANCES (each player plays both matches for their team, random goals)
-- Red Rockets, Gameweek 1
INSERT INTO appearances (match_id, player_id, goals)
VALUES
  ('aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaa1', 'a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1', 1),
  ('aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaa1', 'a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2', 1),
  ('aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaa1', 'a3a3a3a3-a3a3-a3a3-a3a3-a3a3a3a3a3a3', 1),
  ('aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaa1', 'a4a4a4a4-a4a4-a4a4-a4a4-a4a4a4a4a4a4', 0);

-- Red Rockets, Gameweek 2
INSERT INTO appearances (match_id, player_id, goals)
VALUES
  ('aaaaaaa2-aaaa-aaaa-aaaa-aaaaaaaaaaa2', 'a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1', 0),
  ('aaaaaaa2-aaaa-aaaa-aaaa-aaaaaaaaaaa2', 'a2a2a2a2-a2a2-a2a2-a2a2-a2a2a2a2a2a2', 1),
  ('aaaaaaa2-aaaa-aaaa-aaaa-aaaaaaaaaaa2', 'a3a3a3a3-a3a3-a3a3-a3a3-a3a3a3a3a3a3', 0),
  ('aaaaaaa2-aaaa-aaaa-aaaa-aaaaaaaaaaa2', 'a4a4a4a4-a4a4-a4a4-a4a4-a4a4a4a4a4a4', 0);

-- Blue Blizzards, Gameweek 1
INSERT INTO appearances (match_id, player_id, goals)
VALUES
  ('bbbbbbb1-bbbb-bbbb-bbbb-bbbbbbbbbbb1', 'b1b1b1b1-b1b1-b1b1-b1b1-b1b1b1b1b1b1', 1),
  ('bbbbbbb1-bbbb-bbbb-bbbb-bbbbbbbbbbb1', 'b2b2b2b2-b2b2-b2b2-b2b2-b2b2b2b2b2b2', 1),
  ('bbbbbbb1-bbbb-bbbb-bbbb-bbbbbbbbbbb1', 'b3b3b3b3-b3b3-b3b3-b3b3-b3b3b3b3b3b3', 0),
  ('bbbbbbb1-bbbb-bbbb-bbbb-bbbbbbbbbbb1', 'b4b4b4b4-b4b4-b4b4-b4b4-b4b4b4b4b4b4', 0);

-- Blue Blizzards, Gameweek 2
INSERT INTO appearances (match_id, player_id, goals)
VALUES
  ('bbbbbbb2-bbbb-bbbb-bbbb-bbbbbbbbbbb2', 'b1b1b1b1-b1b1-b1b1-b1b1-b1b1b1b1b1b1', 0),
  ('bbbbbbb2-bbbb-bbbb-bbbb-bbbbbbbbbbb2', 'b2b2b2b2-b2b2-b2b2-b2b2-b2b2b2b2b2b2', 0),
  ('bbbbbbb2-bbbb-bbbb-bbbb-bbbbbbbbbbb2', 'b3b3b3b3-b3b3-b3b3-b3b3-b3b3b3b3b3b3', 0),
  ('bbbbbbb2-bbbb-bbbb-bbbb-bbbbbbbbbbb2', 'b4b4b4b4-b4b4-b4b4-b4b4-b4b4b4b4b4b4', 0); 