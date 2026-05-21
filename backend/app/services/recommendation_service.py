from app.schemas import FarmConditionsInput
from app.services.crop_engine import recommend_crops
from app.services.fertilizer_engine import recommend_fertilizers
from app.services.irrigation_engine import recommend_irrigation
from app.services.weather_service import get_weather_for_farm

FUTURE_FEATURES = {
    "crop_disease_detection": "Planned: upload leaf images for ML disease classification",
    "market_price_prediction": "Planned: regional mandi price forecasts",
    "multilingual_support": "Planned: Hindi, Tamil, Telugu, Marathi UI",
    "iot_sensor_integration": "Planned: soil moisture and weather station MQTT feeds",
}


async def generate_full_recommendation(payload: FarmConditionsInput) -> dict:
    crops = recommend_crops(
        soil_type=payload.soil_type,
        season=payload.season,
        temperature_c=payload.temperature_c,
        water_availability=payload.water_availability,
        land_size_acres=payload.land_size_acres,
    )
    top_crops = [c["crop"] for c in crops]
    primary = top_crops[0] if top_crops else "Wheat"

    fertilizers = recommend_fertilizers(payload.soil_type, top_crops)
    irrigation = recommend_irrigation(
        payload.water_availability,
        payload.land_size_acres,
        primary,
        payload.temperature_c,
    )
    weather = await get_weather_for_farm(
        payload.latitude,
        payload.longitude,
        payload.temperature_c,
    )

    summary = (
        f"Top recommendation: {primary} ({crops[0]['suitability_score']}% match) "
        f"for {payload.land_size_acres} acres in {payload.season} season. "
        f"Use {irrigation['method_recommended']} to optimize water use."
    )

    return {
        "crops": crops,
        "fertilizers": fertilizers,
        "irrigation": irrigation,
        "weather": weather,
        "summary": summary,
        "future_features": FUTURE_FEATURES,
    }
