"""Irrigation scheduling and water conservation recommendations."""

WATER_LITERS_PER_ACRE = {
    "low": 8000,
    "medium": 15000,
    "high": 25000,
    "rainfed": 5000,
    "irrigated": 20000,
}

CROP_WATER_FACTOR = {
    "Rice": 1.4,
    "Wheat": 1.0,
    "Maize": 1.1,
    "Cotton": 1.2,
    "Sugarcane": 1.8,
    "Tomato": 1.15,
    "Banana": 1.5,
    "Groundnut": 0.85,
    "Millet (Bajra)": 0.7,
    "Sorghum": 0.75,
}


def recommend_irrigation(
    water_availability: str,
    land_size_acres: float,
    primary_crop: str,
    temperature_c: float,
) -> dict:
    water_n = water_availability.strip().lower()
    base = WATER_LITERS_PER_ACRE.get(water_n, 12000)
    factor = CROP_WATER_FACTOR.get(primary_crop, 1.0)
    temp_factor = 1.15 if temperature_c > 32 else 1.0 if temperature_c > 25 else 0.9

    daily_per_acre = base * factor * temp_factor / 7
    total_daily = round(daily_per_acre * land_size_acres, 0)

    if water_n in {"low", "rainfed"}:
        method = "Drip irrigation with mulching"
        slots = [
            {"day": "Mon", "time": "06:00", "duration_minutes": 45, "water_liters_per_acre": daily_per_acre * 0.4, "method": "drip"},
            {"day": "Thu", "time": "06:00", "duration_minutes": 45, "water_liters_per_acre": daily_per_acre * 0.35, "method": "drip"},
        ]
        tips = [
            "Use drip lines to cut water use by 30–50%",
            "Apply straw mulch to reduce evaporation",
            "Harvest rainwater in farm ponds",
        ]
    elif water_n == "medium":
        method = "Sprinkler or furrow (alternate rows)"
        slots = [
            {"day": "Mon", "time": "06:00", "duration_minutes": 60, "water_liters_per_acre": daily_per_acre * 0.35, "method": "sprinkler"},
            {"day": "Wed", "time": "06:00", "duration_minutes": 50, "water_liters_per_acre": daily_per_acre * 0.3, "method": "sprinkler"},
            {"day": "Sat", "time": "06:00", "duration_minutes": 50, "water_liters_per_acre": daily_per_acre * 0.3, "method": "sprinkler"},
        ]
        tips = [
            "Irrigate early morning to limit evaporation",
            "Check soil moisture at 15 cm depth before watering",
            "Group crops by water need in the same block",
        ]
    else:
        method = "Furrow or basin with scheduling"
        slots = [
            {"day": "Mon", "time": "05:30", "duration_minutes": 90, "water_liters_per_acre": daily_per_acre * 0.3, "method": "furrow"},
            {"day": "Tue", "time": "05:30", "duration_minutes": 70, "water_liters_per_acre": daily_per_acre * 0.25, "method": "furrow"},
            {"day": "Thu", "time": "05:30", "duration_minutes": 90, "water_liters_per_acre": daily_per_acre * 0.3, "method": "furrow"},
            {"day": "Sat", "time": "06:00", "duration_minutes": 60, "water_liters_per_acre": daily_per_acre * 0.2, "method": "furrow"},
        ]
        tips = [
            "Avoid over-irrigation to prevent nutrient leaching",
            "Install flow meters on main channels",
            "Consider alternate wetting and drying for paddy where feasible",
        ]

    return {
        "weekly_schedule": slots,
        "daily_water_liters": total_daily,
        "conservation_tips": tips,
        "method_recommended": method,
    }
