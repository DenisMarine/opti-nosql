
import zlib
import json
from app.databases.mongodb import db as mongodb
from app.databases.redis import redis
from app.databases.neo4j import neo4j_driver as driver
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException
import logging

logger = logging.getLogger("uvicorn")

def build_cache_key(from_code: str, to_code: str) -> str:
    return f"offers:{from_code}:{to_code}"

def decompress_offer(data: bytes) -> dict:
    return json.loads(zlib.decompress(data).decode())

def decompress_offers(data: bytes) -> list:
    return json.loads(zlib.decompress(data).decode())

def compress_offer(data: bytes) -> dict:
    return zlib.compress(json.dumps(data).encode())

def compress_offers(offers: list) -> bytes:
    return zlib.compress(json.dumps(offers).encode())

async def get_offers_from_cache(key: str, limit: int):
    cached = redis.get(key)
    if cached:
        return decompress_offers(cached)[:limit]
    return None

def get_offer_from_cache(key: str):
    cached = redis.get(key)
    if cached:
        try:
            return decompress_offer(cached)
        except Exception as e:
            logger.error(f"Error while decompressing cached offer: {e}")
            return None
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
        "from": 1,
        "provider": 1,
        "price": 1,
        "currency": 1,
        "legs": 1
    }
    cursor = mongodb.offers.find({"from": from_code, "to": to_code}, projection).sort("price", 1).limit(limit)
    offers = await cursor.to_list(length=limit)
    return serialize(offers)

async def get_offer_from_db(offer_id: str):
    projection = {
        "_id": 1,
        "from": 1,
        "departDate": 1,
        "provider": 1,
        "price": 1,
        "currency": 1,
        "legs": 1
    }
    try:
        offer = await mongodb.offers.find_one({"_id": ObjectId(offer_id)}, projection)
        if offer:
            offer["_id"] = str(offer["_id"])
        return offer
    except Exception as e:
        return None

def store_offers_in_cache(key: str, offers: list, ttl: int = 60):
    try:
        compressed = compress_offers(offers)
        redis.setex(key, ttl, compressed)
    except Exception as e:
        logger.error(f"Error while storing in Redis : {e}")
        raise

def store_offer_in_cache(key: str, offer: dict, ttl: int = 300):
    try:
        compressed = compress_offer(offer)
        redis.setex(key, ttl, compressed)
    except Exception as e:
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

async def get_offer_for_id(offer_id: str):
    key = f"offer:{offer_id}"
    offer = get_offer_from_cache(key)
    if not offer:
        offer = await get_offer_from_db(offer_id)
        offer = serialize(offer)
        if offer:
            store_offer_in_cache(key, offer)
    
    offer = serialize(offer)
    return offer

async def get_related_offers(city_code, date):
    nearby_cities = await get_nearby_cities(city_code)    
    best_offers = await get_best_offers_for_nearby_cities(nearby_cities, date)
    return {
        "relatedOffers": best_offers
    }
    
async def get_nearby_cities(city_code):
    query = """
    MATCH (city:City {code: $city_code})
    MATCH (city)-[r:NEAR]->(relatedCity:City)
    RETURN DISTINCT relatedCity.code AS relatedCityCode, r.weight AS weight
    ORDER BY r.weight DESC
    """
    async with driver.session() as session:
        result = await session.run(query, city_code=city_code)
        nearby_cities = []
        async for record in result:
            nearby_cities.append({
                "city_code": record["relatedCityCode"],
                "weight": record["weight"]
            })
        return nearby_cities
    
async def get_best_offers_for_nearby_cities(nearby_cities, date):
    offers = []
    seen_ids = set()
    top_cities = nearby_cities[:3]
    for city in top_cities:
        city_code = city["city_code"]
        offer_cursor = mongodb.offers.find({"from": city_code, "departDate": date})
        async for offer in offer_cursor:
            offer = serialize(offer)
            if offer["_id"] not in seen_ids:
                seen_ids.add(offer["_id"])
                offer["relatedCity"] = city_code
                offer["weight"] = city["weight"] 
                offers.append(offer)
    sorted_offers = sorted(offers, key=lambda x: x["weight"], reverse=True)[:3]
    return sorted_offers
    
async def create_offer(offer: dict):
    try:
        required_fields = ["from", "to", "departDate", "returnDate", "provider", "price", "currency", "legs"]
        for field in required_fields:
            if field not in offer:
                raise ValueError(f"Missing required field: {field}")

        optional_fields = ["hotel", "activity"]
        for field in optional_fields:
            if field not in offer:
                offer[field] = None

        offer["_id"] = str(ObjectId())

        try:
            result = await mongodb.offers.insert_one(offer)
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error while inserting into MongoDB : {e}")

        return {"success": True, "offerId": offer["_id"]}
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Error while offer creation : {e}")

async def broadcasted_offer(offer: dict):
    try:
        offer_id = offer.get("offerId")
        if not offer_id:
            raise ValueError("Offer ID is required for broadcasting.")

        redis.publish("offers:new", json.dumps(offer))
        return True
    except Exception as e:
        logger.error(f"Error while broadcasting the offer : {e}")
        raise