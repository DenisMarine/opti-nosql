from fastapi import APIRouter, Query, HTTPException
from app.services.login_service import login

router = APIRouter()

@router.post("/login")
async def login_user(
  user_id: str = Query(..., alias="userId")
):
  # Login a user and return a token with expiry time
  try:
    return await login(user_id)
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
