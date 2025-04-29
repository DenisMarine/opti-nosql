from fastapi import APIRouter, Query, HTTPException
from app.services.offer_service import get_offers
from app.services.offer_service import create_offer
from app.services.offer_service import broadcasted_offer
from pydantic import BaseModel
from typing import List, Optional, Dict

router = APIRouter()

@router.get("/offers")
async def offers_endpoint(from_: str = Query(..., alias="from"),
                          to: str = Query(...),
                          limit: int = 10):
    try:
        return await get_offers(from_, to, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/offers")
async def create_offer_endpoint(offer_data: dict):
    try:
        # Validate required fields
        required_fields = ["from", "to", "departDate", "returnDate", "provider", "price", "currency", "legs"]
        for field in required_fields:
            if field not in offer_data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")

        # Validate optional fields
        optional_fields = ["hotel", "activity"]
        for field in optional_fields:
            if field not in offer_data:
                offer_data[field] = None

        # Create the offer
        print("Creating offer with create_offer function")
        created_offer = await create_offer(offer_data)
        if not created_offer.get("success"):
            raise HTTPException(status_code=400, detail="Failed to create offer.")

        # Broadcast a JSON message on redis offers:new with the data structure { "offerId": "abc123", "from": "PAR", "to": "TYO" }
        broadcast_message = {
            "offerId": created_offer["offerId"],
            "from": offer_data["from"],
            "to": offer_data["to"]
        }
        print("Broadcasting offer with broadcasted_offer function")
        broadcasted = await broadcasted_offer(broadcast_message)
        if not broadcasted:
            raise HTTPException(status_code=500, detail="Failed to broadcast offer.")

        # Return the created offer
        return created_offer
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    