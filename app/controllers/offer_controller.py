from fastapi import APIRouter, Query, HTTPException
from app.services.offer_service import broadcasted_offer, create_offer, get_offers
from app.services.offer_service import get_offer_for_id, get_offers, get_related_offers
from starlette.responses import JSONResponse

router = APIRouter()

@router.get("/offers")
async def offers_endpoint(from_: str = Query(..., alias="from"),
                          to: str = Query(...)):
    try:
        offers = await get_offers(from_, to, 10)
        return JSONResponse(content = {"offers" : offers}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/offers")
async def create_offer_endpoint(offer_data: dict):
    try:
        required_fields = ["from", "to", "departDate", "returnDate", "provider", "price", "currency", "legs"]
        for field in required_fields:
            if field not in offer_data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        optional_fields = ["hotel", "activity"]
        for field in optional_fields:
            if field not in offer_data:
                offer_data[field] = None
        created_offer = await create_offer(offer_data)
        if not created_offer.get("success"):
            raise HTTPException(status_code=400, detail="Failed to create offer.")
        broadcast_message = {
            "offerId": created_offer["offerId"],
            "from": offer_data["from"],
            "to": offer_data["to"]
        }
        broadcasted = await broadcasted_offer(broadcast_message)
        if not broadcasted:
            raise HTTPException(status_code=500, detail="Failed to broadcast offer.")
        return JSONResponse(content=created_offer, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/offers/{id}")
async def offer_by_id_endpoint(id: str):
    try:
        offer = await get_offer_for_id(id)
        if not offer:
            raise HTTPException(status_code=404, detail="Offer not found")
        city = offer["from"]
        date = offer["departDate"]
        related = await get_related_offers(city, date)
        if not related:
            related = []
        return JSONResponse(content={"offer": offer, "relatedOffers": related}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
