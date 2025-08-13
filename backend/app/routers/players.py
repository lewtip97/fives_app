from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from typing import List
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from ..auth import get_current_user_id
from ..schemas import PlayerCreate, PlayerUpdate, PlayerResponse
import uuid

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

router = APIRouter(prefix="/players", tags=["players"])

@router.post("/", response_model=PlayerResponse)
def create_player(player: PlayerCreate, user_id: str = Depends(get_current_user_id)):
    try:
        # Verify team belongs to user
        team_check = supabase.table("teams").select("id").eq("id", player.team_id).eq("created_by", user_id).execute()
        if not team_check.data:
            raise HTTPException(status_code=404, detail="Team not found or access denied")
        
        response = supabase.table("players").insert({
            "name": player.name,
            "team_id": player.team_id,
            "profile_picture": player.profile_picture,
            "created_by": user_id,
            "created_at": "now()"
        }).execute()
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to create player")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[PlayerResponse])
def get_players(user_id: str = Depends(get_current_user_id)):
    try:
        response = supabase.table("players").select("*").eq("created_by", user_id).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{player_id}", response_model=PlayerResponse)
def get_player(player_id: str, user_id: str = Depends(get_current_user_id)):
    try:
        response = supabase.table("players").select("*").eq("id", player_id).eq("created_by", user_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Player not found")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{player_id}", response_model=PlayerResponse)
def update_player(player_id: str, player: PlayerUpdate, user_id: str = Depends(get_current_user_id)):
    try:
        # Build update data (only include fields that are provided)
        update_data = {}
        if player.name is not None:
            update_data["name"] = player.name
        if player.team_id is not None:
            # Verify new team belongs to user
            team_check = supabase.table("teams").select("id").eq("id", player.team_id).eq("created_by", user_id).execute()
            if not team_check.data:
                raise HTTPException(status_code=404, detail="Team not found or access denied")
            update_data["team_id"] = player.team_id
        if player.profile_picture is not None:
            update_data["profile_picture"] = player.profile_picture
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        response = supabase.table("players").update(update_data).eq("id", player_id).eq("created_by", user_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Player not found")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{player_id}")
def delete_player(player_id: str, user_id: str = Depends(get_current_user_id)):
    try:
        response = supabase.table("players").delete().eq("id", player_id).eq("created_by", user_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Player not found")
        return {"message": "Player deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{player_id}/upload-picture")
async def upload_player_picture(
    player_id: str, 
    file: UploadFile = File(...), 
    user_id: str = Depends(get_current_user_id)
):
    """Upload a profile picture for a player"""
    try:
        print(f"DEBUG: Starting upload for player {player_id}, user {user_id}")
        print(f"DEBUG: File info - name: {file.filename}, content_type: {file.content_type}, size: {file.size}")
        
        # Verify player belongs to user
        print(f"DEBUG: Verifying player ownership...")
        player_check = supabase.table("players").select("id, name").eq("id", player_id).eq("created_by", user_id).execute()
        print(f"DEBUG: Player check result: {player_check.data}")
        
        if not player_check.data:
            raise HTTPException(status_code=404, detail="Player not found or access denied")
        
        # Validate file type
        print(f"DEBUG: Validating file type: {file.content_type}")
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Generate unique filename
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
        filename = f"player_{player_id}_{uuid.uuid4().hex[:8]}.{file_extension}"
        print(f"DEBUG: Generated filename: {filename}")
        
        # Read file content
        print(f"DEBUG: Reading file content...")
        file_content = await file.read()
        print(f"DEBUG: File content size: {len(file_content)} bytes")
        
        # Upload to Supabase Storage
        print(f"DEBUG: Uploading to Supabase Storage...")
        storage_response = supabase.storage.from_('player-pictures').upload(
            path=filename,
            file=file_content,
            file_options={"content-type": file.content_type}
        )
        print(f"DEBUG: Storage response: {storage_response}")
        
        if not storage_response:
            raise HTTPException(status_code=500, detail="Failed to upload image")
        
        # Get public URL
        print(f"DEBUG: Getting public URL...")
        public_url = supabase.storage.from_('player-pictures').get_public_url(filename)
        print(f"DEBUG: Public URL: {public_url}")
        
        # Update player record with new picture URL
        print(f"DEBUG: Updating player record...")
        update_response = supabase.table("players").update({
            "profile_picture": public_url
        }).eq("id", player_id).eq("created_by", user_id).execute()
        print(f"DEBUG: Update response: {update_response.data}")
        
        if not update_response.data:
            raise HTTPException(status_code=500, detail="Failed to update player")
        
        print(f"DEBUG: Upload completed successfully")
        return {
            "message": "Profile picture uploaded successfully",
            "profile_picture": public_url,
            "player": update_response.data[0]
        }
        
    except HTTPException:
        print(f"DEBUG: HTTPException raised")
        raise
    except Exception as e:
        print(f"DEBUG: Unexpected error: {str(e)}")
        print(f"DEBUG: Error type: {type(e)}")
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
