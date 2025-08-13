-- Add profile_picture column to players table
-- Run this in your Supabase SQL editor

ALTER TABLE players 
ADD COLUMN IF NOT EXISTS profile_picture TEXT;

-- Add comment for documentation
COMMENT ON COLUMN players.profile_picture IS 'URL to player profile picture stored in Supabase Storage'; 