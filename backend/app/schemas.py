from pydantic import BaseModel

class Player(BaseModel):
    id: int
    name: str
    position: str

    class Config:
        orm_mode = True
