from app.databases.redis import redis
from fastapi import HTTPException
import uuid

async def login(user_id: str):
  session_id = str(uuid.uuid4())
  key = f"session:{session_id}"
  try:
    redis.set(key, user_id, ex=900)
    return {"token": session_id, "expires_in": 900}
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error while storing in Redis : {e}")