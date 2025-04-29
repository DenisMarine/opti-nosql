from fastapi import APIRouter, Query, HTTPException
from app.services.offer_service import get_offers
import asyncio
import logging
from starlette.responses import JSONResponse

router = APIRouter()
logger = logging.getLogger("uvicorn")

TIMEOUT = 0.7

@router.get("/offers")
async def offers_endpoint(from_: str = Query(..., alias="from"),
                          to: str = Query(...)):
    try:
        offers = await asyncio.wait_for(get_offers(from_, to, 10), timeout=TIMEOUT)
        return JSONResponse(content = {"offers" : offers}, status_code=200)
    except asyncio.TimeoutError:
        logger.warning(f"/offers request took too long (exceeded {TIMEOUT} seconds).")
        raise HTTPException(status_code=504, detail="Request took too long to process")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))