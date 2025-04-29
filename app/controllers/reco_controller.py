from fastapi import APIRouter, Query, HTTPException
from typing import List
from pydantic import BaseModel
from typing import Optional
from app.services.reco_service import get_recommendations_service

router = APIRouter()

class Recommendation(BaseModel):
    city: str
    score: Optional[float]

@router.get("/reco", response_model=List[Recommendation])
async def get_recommendations(city: str = Query(..., min_length=3), k: int = Query(..., ge=1)):
    try:
        recommendations = await get_recommendations_service(city, k)
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))