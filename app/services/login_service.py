from app.databases.redis import redis
import uuid

async def login(user_id: str):
  session_id = str(uuid.uuid4())
  key = f"session:{session_id}"
  try:
    redis.set(key, user_id, ex=900)
    return {"token": session_id, "expires_in": 900}
  except Exception as e:
    print(f"Erreur lors du stockage dans Redis : {e}")
    raise