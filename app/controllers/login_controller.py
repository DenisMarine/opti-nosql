from fastapi import APIRouter, Query, HTTPException
from app.services.login_service import login
from starlette.responses import JSONResponse

router = APIRouter()

@router.post("/login")
async def login_user(
  user_id: str = Query(..., alias="userId")
):
  try:
    result = await login(user_id)
    return JSONResponse(content=result, status_code=200)
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
