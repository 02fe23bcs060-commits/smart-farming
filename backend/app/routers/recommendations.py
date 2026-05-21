from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import FarmInput, Farmer, RecommendationHistory
from app.schemas import (
    FarmConditionsInput,
    FullRecommendationResponse,
    RecommendationHistoryItem,
)
from app.services.recommendation_service import generate_full_recommendation

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])


@router.post("/analyze", response_model=FullRecommendationResponse)
async def analyze_farm(payload: FarmConditionsInput, db: Session = Depends(get_db)):
    farmer_id = payload.farmer_id

    if farmer_id is None and payload.farmer_name:
        farmer = Farmer(name=payload.farmer_name)
        db.add(farmer)
        db.commit()
        db.refresh(farmer)
        farmer_id = farmer.id
    elif farmer_id is not None:
        if not db.query(Farmer).filter(Farmer.id == farmer_id).first():
            raise HTTPException(status_code=404, detail="Farmer not found")

    result = await generate_full_recommendation(payload)

    history_id = None
    farm_input_id = None
    if farmer_id:
        farm_input = FarmInput(
            farmer_id=farmer_id,
            soil_type=payload.soil_type,
            season=payload.season,
            temperature_c=payload.temperature_c,
            water_availability=payload.water_availability,
            land_size_acres=payload.land_size_acres,
            latitude=payload.latitude,
            longitude=payload.longitude,
        )
        db.add(farm_input)
        db.flush()
        farm_input_id = farm_input.id

        history = RecommendationHistory(
            farmer_id=farmer_id,
            farm_input_id=farm_input_id,
            crop_recommendations={"crops": result["crops"]},
            fertilizer_plan={"fertilizers": result["fertilizers"]},
            irrigation_schedule=result["irrigation"],
            weather_alerts=result["weather"],
            summary=result["summary"],
        )
        db.add(history)
        db.commit()
        db.refresh(history)
        history_id = history.id

    return FullRecommendationResponse(
        id=history_id,
        farmer_id=farmer_id,
        crops=result["crops"],
        fertilizers=result["fertilizers"],
        irrigation=result["irrigation"],
        weather=result["weather"],
        summary=result["summary"],
        future_features=result["future_features"],
    )


@router.get("/history/{farmer_id}", response_model=list[RecommendationHistoryItem])
def get_history(farmer_id: int, db: Session = Depends(get_db)):
    rows = (
        db.query(RecommendationHistory)
        .filter(RecommendationHistory.farmer_id == farmer_id)
        .order_by(RecommendationHistory.created_at.desc())
        .limit(20)
        .all()
    )
    items = []
    for row in rows:
        top_crop = None
        crops = (row.crop_recommendations or {}).get("crops", [])
        if crops:
            top_crop = crops[0].get("crop")
        items.append(
            RecommendationHistoryItem(
                id=row.id,
                farmer_id=row.farmer_id,
                summary=row.summary,
                created_at=row.created_at,
                top_crop=top_crop,
            )
        )
    return items
