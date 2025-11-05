from sqlalchemy import Table, Column, Integer, String, MetaData
from app.database import metadata

players = Table(
    "players",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("position", String),
)
