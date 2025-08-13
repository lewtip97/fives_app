from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PlayerBase(BaseModel):
    name: str
    team_id: str

class PlayerCreate(PlayerBase):
    profile_picture: Optional[str] = None

class PlayerUpdate(BaseModel):
    name: Optional[str] = None
    team_id: Optional[str] = None
    profile_picture: Optional[str] = None

class PlayerResponse(PlayerBase):
    id: str
    profile_picture: Optional[str] = None
    created_at: datetime
    created_by: str

    class Config:
        orm_mode = True

class TeamBase(BaseModel):
    name: str
    team_size: int

class TeamCreate(TeamBase):
    pass

class TeamUpdate(BaseModel):
    name: Optional[str] = None
    team_size: Optional[int] = None

class TeamResponse(TeamBase):
    id: str
    created_at: datetime
    created_by: str

    class Config:
        orm_mode = True

class MatchBase(BaseModel):
    team_id: str
    opponent_id: str
    score1: int
    score2: int
    gameweek: int
    season: str
    played_at: datetime

class MatchCreate(MatchBase):
    pass

class MatchResponse(MatchBase):
    id: str
    created_at: datetime
    created_by: str

    class Config:
        orm_mode = True

class AppearanceBase(BaseModel):
    match_id: str
    player_id: str
    goals: int

class AppearanceCreate(AppearanceBase):
    pass

class AppearanceResponse(AppearanceBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True

class OpponentBase(BaseModel):
    name: str
    team_id: str

class OpponentCreate(OpponentBase):
    pass

class OpponentUpdate(BaseModel):
    name: Optional[str] = None

class OpponentResponse(OpponentBase):
    id: str
    created_at: datetime
    created_by: str

    class Config:
        orm_mode = True
