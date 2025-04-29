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

async def create_offer(offer: dict):
    try:
        # Validate required fields
        required_fields = ["from", "to", "departDate", "returnDate", "provider", "price", "currency", "legs"]
        for field in required_fields:
            if field not in offer:
                raise ValueError(f"Missing required field: {field}")

        # Validate optional fields
        optional_fields = ["hotel", "activity"]
        for field in optional_fields:
            if field not in offer:
                offer[field] = None

        # Generate a unique offerId
        offer["offerId"] = str(ObjectId())

        # Insert the offer into the MongoDB database
        print("Inserting offer into MongoDB")
        try:
            result = await mongodb.offers.insert_one(offer)
        except Exception as e:
            print(f"Erreur lors de l'insertion dans MongoDB : {e}")
            raise

        offer["_id"] = str(result.inserted_id)
        # Store the offer in Redis cache
        key = build_cache_key(offer["from"], offer["to"])
        store_offers_in_cache(key, [offer], ttl=60)

        return {"success": True, "offerId": offer["offerId"]}
    except Exception as e:
        print(f"Erreur lors de la création de l'offre : {e}")
        print(f"Offre : {offer}")
        raise


async def broadcasted_offer(offer: dict):
    try:
        # Assuming the offer has a field 'offerId' to broadcast
        offer_id = offer.get("offerId")
        if not offer_id:
            raise ValueError("Offer ID is required for broadcasting.")

        # Broadcast the offer to Redis
        redis.publish("offers:new", json.dumps(offer))
        return True
    except Exception as e:
        print(f"Erreur lors de la diffusion de l'offre : {e}")
        raise