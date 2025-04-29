from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_DB, MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]