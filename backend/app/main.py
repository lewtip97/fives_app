from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from app.routers import teams, players

app = FastAPI()

app.include_router(teams.router, prefix="/teams", tags=["Teams"])
app.include_router(players.router, prefix="/players", tags=["Players"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Biesla's Rejects API"}
