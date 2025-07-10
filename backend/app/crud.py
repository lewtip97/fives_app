from app.models import players
from app.database import database

async def get_all_players():
    query = players.select()
    return await database.fetch_all(query)
