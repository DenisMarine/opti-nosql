import zlib
import json
from app.databases.mongodb import db as mongodb
from app.databases.redis import redis
from bson import ObjectId
from datetime import datetime

def build_cache_key(from_code: str, to_code: str) -> str:
    return f"offers:{from_code}:{to_code}"

def decompress_offers(data: bytes) -> list:
    return json.loads(zlib.decompress(data).decode())

def compress_offers(offers: list) -> bytes:
    return zlib.compress(json.dumps(offers).encode())

async def get_offers_from_cache(key: str, limit: int):
    cached = redis.get(key)
    if cached:
        return decompress_offers(cached)[:limit]
    return None

def serialize(doc):
    if isinstance(doc, dict):
        return {key: serialize(value) for key, value in doc.items()}
    elif isinstance(doc, list):
        return [serialize(item) for item in doc]
    elif isinstance(doc, ObjectId):
        return str(doc)
    elif isinstance(doc, datetime):
        return doc.isoformat()
    else:
        return doc

async def get_offers_from_db(from_code: str, to_code: str, limit: int):
    projection = {
        "_id": 1,
        "provider": 1,
        "price": 1,
        "currency": 1,
        "legs": 1
    }
    cursor = mongodb.offers.find({"from": from_code, "to": to_code}, projection).sort("price", 1).limit(limit)
    offers = await cursor.to_list(length=limit)
    return serialize(offers)

def store_offers_in_cache(key: str, offers: list, ttl: int = 60):
    try:
        compressed = compress_offers(offers)
        redis.setex(key, ttl, compressed)
    except Exception as e:
        print(f"Erreur lors du stockage dans Redis : {e}")
        raise

async def get_offers(from_code: str, to_code: str, limit: int = 10):
    key = build_cache_key(from_code, to_code)

    offers = await get_offers_from_cache(key, limit)
    if offers:
        return offers

    offers = await get_offers_from_db(from_code, to_code, limit)
    if offers:
        store_offers_in_cache(key, offers)
    return offers