from fastapi import APIRouter
from typing import List
from app.schemas import Player
from app.crud import get_all_players

router = APIRouter()

@router.get("/", response_model=List[Player])
async def read_players():
    return await get_all_players()
