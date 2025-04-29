from fastapi import APIRouter, Query, HTTPException
from app.services.offer_service import get_offers

router = APIRouter()

@router.get("/offers")
async def offers_endpoint(from_: str = Query(..., alias="from"),
                          to: str = Query(...)):
    try:
        return await get_offers(from_, to, 10)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))