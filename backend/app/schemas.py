from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field


class FarmerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    email: EmailStr | None = None
    phone: str | None = None
    region: str | None = None


class FarmerResponse(FarmerCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class FarmConditionsInput(BaseModel):
    farmer_id: int | None = None
    farmer_name: str | None = Field(None, description="Used when creating a new farmer inline")
    soil_type: str = Field(..., examples=["clay", "loam", "sandy", "silt", "black", "red"])
    season: str = Field(..., examples=["kharif", "rabi", "zaid", "summer", "winter", "monsoon"])
    temperature_c: float = Field(..., ge=-10, le=55)
    water_availability: str = Field(
        ..., examples=["low", "medium", "high", "rainfed", "irrigated"]
    )
    land_size_acres: float = Field(..., gt=0, le=10000)
    latitude: float | None = None
    longitude: float | None = None


class CropRecommendation(BaseModel):
    crop: str
    suitability_score: float
    confidence: str
    reasons: list[str]
    expected_yield_t_per_acre: float | None = None


class FertilizerRecommendation(BaseModel):
    crop: str
    npk_ratio: str
    organic_options: list[str]
    chemical_schedule: list[dict[str, Any]]
    soil_amendments: list[str]
    notes: list[str]


class IrrigationSlot(BaseModel):
    day: str
    time: str
    duration_minutes: int
    water_liters_per_acre: float
    method: str


class IrrigationPlan(BaseModel):
    weekly_schedule: list[IrrigationSlot]
    daily_water_liters: float
    conservation_tips: list[str]
    method_recommended: str


class WeatherAlert(BaseModel):
    type: str
    severity: str
    message: str
    precaution: str


class WeatherInsights(BaseModel):
    current_temp_c: float | None
    forecast_summary: str
    rainfall_mm_next_7d: float | None
    alerts: list[WeatherAlert]
    farming_precautions: list[str]


class FullRecommendationResponse(BaseModel):
    id: int | None = None
    farmer_id: int | None
    crops: list[CropRecommendation]
    fertilizers: list[FertilizerRecommendation]
    irrigation: IrrigationPlan
    weather: WeatherInsights
    summary: str
    future_features: dict[str, str]


class RecommendationHistoryItem(BaseModel):
    id: int
    farmer_id: int
    summary: str | None
    created_at: datetime
    top_crop: str | None = None

    model_config = {"from_attributes": True}
