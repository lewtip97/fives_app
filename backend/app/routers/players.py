from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from typing import List
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from ..auth import get_current_user_id
from ..schemas import PlayerCreate, PlayerUpdate, PlayerResponse
import uuid
import time

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

@router.post("/{player_id}/picture")
async def upload_player_picture(
    player_id: str,
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id)
):
    """Upload a profile picture for a player"""
    try:
        # Verify the player exists and belongs to the user
        player_check = supabase.table('players').select('id, team_id').eq('id', player_id).execute()
        
        if not player_check.data:
            raise HTTPException(status_code=404, detail="Player not found")
        
        # Verify user owns the team that contains this player
        team_id = player_check.data[0]['team_id']
        team_check = supabase.table('teams').select('id').eq('id', team_id).eq('created_by', user_id).execute()
        
        if not team_check.data:
            raise HTTPException(status_code=403, detail="Not authorized to modify this player")
        
        # Validate file type
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Generate unique filename
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
        filename = f"player_{player_id}_{int(time.time())}.{file_extension}"
        
        # Read file content
        file_content = await file.read()
        
        # Upload to Supabase Storage
        storage_response = supabase.storage.from_('player-pictures').upload(
            filename,
            file_content,
            {"content-type": file.content_type}
        )
        
        if not storage_response.data:
            raise HTTPException(status_code=500, detail="Failed to upload file to storage")
        
        # Get public URL
        public_url = supabase.storage.from_('player-pictures').get_public_url(filename)
        
        # Update player record with new picture URL
        update_response = supabase.table('players').update({
            'profile_picture': public_url
        }).eq('id', player_id).execute()
        
        if not update_response.data:
            raise HTTPException(status_code=500, detail="Failed to update player record")
        
        return {"message": "Picture uploaded successfully", "url": public_url}
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
