import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import HTTPException
import asyncio

logger = logging.getLogger("uvicorn")

TIMEOUT = 0.7

class OffersRouteTimeOut(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/offers"):
            try :
                response = await asyncio.wait_for(call_next(request), timeout=TIMEOUT)
            except asyncio.TimeoutError:
                logger.warning(f"/offers request took too long (exceeded {TIMEOUT} seconds).")
                raise HTTPException(status_code=408, detail="Request took too long to process")
        else :
            response = await call_next(request)
        return response