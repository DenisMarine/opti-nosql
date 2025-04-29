from fastapi import APIRouter, Query, HTTPException
from app.services.offer_service import get_offers
import asyncio
import logging
from starlette.responses import JSONResponse
from app.services.offer_service import create_offer
from app.services.offer_service import broadcasted_offer
from pydantic import BaseModel
from typing import List, Optional, Dict
from app.services.offer_service import get_offer_for_id, get_offers, get_related_offers

TIMEOUT = 0.7

# Configure logger
logger = logging.getLogger("uvicorn")

router = APIRouter()

@router.get("/offers")
async def offers_endpoint(from_: str = Query(..., alias="from"),
                          to: str = Query(...)):
    try:
        return await get_offers(from_, to, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/offers/{id}")
async def offer_by_id_endpoint(id: str):
    try:
        print(f"Fetching offer for id: {id}")
        offer = await get_offer_for_id(id)

        if offer is None:
            print(f"Offer with id {id} not found")
            raise HTTPException(status_code=404, detail="Offer not found")

        print(f"Offer fetched successfully: {offer}")

        print(f"Fetching related offers for id: {id}")
        related = await get_related_offers(id)

        if not related:
            print(f"No related offers found for id: {id}")
            related = []

        print(f"Related offers: {related}")

        offer["relatedOffers"] = related
        return offer

    except Exception as e:
        print(f"Error in offer_by_id_endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
