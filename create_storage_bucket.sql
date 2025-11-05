-- Create storage bucket for player profile pictures
-- Run this in your Supabase SQL editor

-- Create the storage bucket
INSERT INTO storage.buckets (id, name, public)
VALUES ('player-pictures', 'player-pictures', true)
ON CONFLICT (id) DO NOTHING;

-- Set up storage policies for the bucket
-- Allow authenticated users to upload files
CREATE POLICY "Allow authenticated users to upload player pictures" ON storage.objects
FOR INSERT WITH CHECK (
  bucket_id = 'player-pictures' 
  AND auth.role() = 'authenticated'
);

-- Allow authenticated users to view their own player pictures
CREATE POLICY "Allow users to view player pictures" ON storage.objects
FOR SELECT USING (
  bucket_id = 'player-pictures' 
  AND auth.role() = 'authenticated'
);

-- Allow users to update their own player pictures
CREATE POLICY "Allow users to update their own player pictures" ON storage.objects
FOR UPDATE USING (
  bucket_id = 'player-pictures' 
  AND auth.role() = 'authenticated'
);

-- Allow users to delete their own player pictures
CREATE POLICY "Allow users to delete their own player pictures" ON storage.objects
FOR DELETE USING (
  bucket_id = 'player-pictures' 
  AND auth.role() = 'authenticated'
); 