"""Weather insights via Open-Meteo (no API key required)."""

import httpx

from app.config import settings


async def fetch_weather(lat: float, lon: float) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,precipitation,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "forecast_days": 7,
        "timezone": "auto",
    }
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()


def build_weather_insights(data: dict, farm_temp: float) -> dict:
    current = data.get("current", {})
    daily = data.get("daily", {})
    cur_temp = current.get("temperature_2m")
    precip_sum = sum(daily.get("precipitation_sum", []) or [0])
    max_temps = daily.get("temperature_2m_max", []) or []
    min_temps = daily.get("temperature_2m_min", []) or []

    alerts = []
    precautions = []

    if precip_sum > 50:
        alerts.append(
            {
                "type": "heavy_rainfall",
                "severity": "high",
                "message": f"Expected ~{precip_sum:.0f} mm rain in next 7 days",
                "precaution": "Delay fertilizer top-dress; ensure field drainage",
            }
        )
        precautions.append("Prepare drainage channels before heavy rain")
    elif precip_sum < 5 and farm_temp > 30:
        alerts.append(
            {
                "type": "drought_risk",
                "severity": "medium",
                "message": "Low rainfall forecast with warm conditions",
                "precaution": "Increase irrigation frequency; mulch soil surface",
            }
        )

    if max_temps and max(max_temps) > 38:
        alerts.append(
            {
                "type": "heat_stress",
                "severity": "high",
                "message": f"Peak temperature may reach {max(max_temps):.0f}°C",
                "precaution": "Irrigate during early morning; avoid midday field work",
            }
        )
        precautions.append("Provide shade nets for sensitive vegetables if possible")

    if min_temps and min(min_temps) < 5:
        alerts.append(
            {
                "type": "frost_risk",
                "severity": "medium",
                "message": f"Minimum temperature may drop to {min(min_temps):.0f}°C",
                "precaution": "Protect seedlings; delay transplanting",
            }
        )

    if farm_temp > 40:
        alerts.append(
            {
                "type": "extreme_heat",
                "severity": "critical",
                "message": f"Reported farm temperature {farm_temp}°C is extreme",
                "precaution": "Prioritize irrigation and avoid chemical sprays in peak heat",
            }
        )

    if not precautions:
        precautions.append("Weather conditions appear favorable; monitor 3-day forecast daily")

    summary_parts = []
    if cur_temp is not None:
        summary_parts.append(f"Current {cur_temp:.0f}°C")
    if precip_sum:
        summary_parts.append(f"7-day rain ~{precip_sum:.0f} mm")
    forecast_summary = "; ".join(summary_parts) if summary_parts else "Forecast data available"

    return {
        "current_temp_c": cur_temp,
        "forecast_summary": forecast_summary,
        "rainfall_mm_next_7d": precip_sum,
        "alerts": alerts,
        "farming_precautions": precautions,
    }


async def get_weather_for_farm(
    latitude: float | None,
    longitude: float | None,
    farm_temp: float,
) -> dict:
    lat = latitude if latitude is not None else settings.default_latitude
    lon = longitude if longitude is not None else settings.default_longitude
    try:
        data = await fetch_weather(lat, lon)
        return build_weather_insights(data, farm_temp)
    except Exception:
        return {
            "current_temp_c": farm_temp,
            "forecast_summary": "Live weather unavailable; using farm-reported temperature",
            "rainfall_mm_next_7d": None,
            "alerts": [
                {
                    "type": "service_notice",
                    "severity": "low",
                    "message": "Connect internet for live rainfall and temperature alerts",
                    "precaution": "Use local IMD/weather apps as backup",
                }
            ],
            "farming_precautions": [
                "Monitor local rainfall manually",
                "Adjust irrigation when heat exceeds 35°C",
            ],
        }
