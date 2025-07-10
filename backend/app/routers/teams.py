from fastapi import APIRouter

router = APIRouter()

@router.get("/teams")
def get_teams():
    return {"message": "List of teams"}
