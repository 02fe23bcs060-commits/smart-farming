"""AI-style crop recommendation engine using weighted multi-factor scoring."""

from dataclasses import dataclass

SOIL_TYPES = {"clay", "loam", "sandy", "silt", "black", "red", "alluvial"}
SEASONS = {"kharif", "rabi", "zaid", "summer", "winter", "monsoon", "spring", "autumn"}
WATER_LEVELS = {"low", "medium", "high", "rainfed", "irrigated"}


@dataclass
class CropProfile:
    name: str
    ideal_soils: set[str]
    seasons: set[str]
    temp_min: float
    temp_max: float
    water_need: str
    min_acres: float
    yield_t_per_acre: float
    notes: str


CROP_DATABASE: list[CropProfile] = [
    CropProfile("Rice", {"clay", "loam", "alluvial", "silt"}, {"kharif", "monsoon"}, 20, 35, "high", 0.5, 2.8, "Staple for wet seasons"),
    CropProfile("Wheat", {"loam", "alluvial", "clay"}, {"rabi", "winter"}, 10, 25, "medium", 0.25, 3.2, "Cool season cereal"),
    CropProfile("Maize", {"loam", "silt", "alluvial"}, {"kharif", "summer", "rabi"}, 18, 32, "medium", 0.25, 3.5, "Versatile feed and food crop"),
    CropProfile("Cotton", {"black", "loam", "alluvial"}, {"kharif", "summer"}, 21, 35, "medium", 1.0, 1.2, "Cash crop, needs warmth"),
    CropProfile("Soybean", {"black", "loam", "clay"}, {"kharif", "monsoon"}, 20, 30, "medium", 0.5, 1.8, "Legume improves soil nitrogen"),
    CropProfile("Groundnut", {"sandy", "loam", "red"}, {"kharif", "summer", "zaid"}, 25, 35, "low", 0.25, 1.5, "Drought-tolerant oilseed"),
    CropProfile("Millet (Bajra)", {"sandy", "red", "loam"}, {"kharif", "summer"}, 25, 42, "low", 0.25, 1.2, "Excellent for arid zones"),
    CropProfile("Sorghum", {"loam", "clay", "red"}, {"kharif", "rabi"}, 22, 38, "low", 0.5, 1.6, "Resilient coarse grain"),
    CropProfile("Sugarcane", {"loam", "alluvial", "black"}, {"kharif", "rabi", "zaid"}, 20, 38, "high", 1.0, 70.0, "Long duration, high water"),
    CropProfile("Potato", {"loam", "silt", "alluvial"}, {"rabi", "winter", "zaid"}, 15, 25, "medium", 0.25, 12.0, "Cool season tuber"),
    CropProfile("Tomato", {"loam", "silt", "alluvial"}, {"rabi", "zaid", "winter"}, 18, 30, "medium", 0.1, 18.0, "High-value vegetable"),
    CropProfile("Onion", {"loam", "silt", "alluvial"}, {"rabi", "zaid"}, 13, 28, "medium", 0.1, 10.0, "Needs good drainage"),
    CropProfile("Pulses (Moong)", {"loam", "sandy", "alluvial"}, {"zaid", "kharif"}, 25, 35, "low", 0.1, 0.6, "Short duration legume"),
    CropProfile("Mustard", {"loam", "alluvial", "clay"}, {"rabi", "winter"}, 10, 25, "low", 0.25, 1.0, "Oilseed for cool dry season"),
    CropProfile("Banana", {"loam", "alluvial", "clay"}, {"kharif", "zaid", "summer"}, 22, 35, "high", 0.25, 15.0, "Perennial fruit, humid climate"),
]


def _normalize(value: str) -> str:
    return value.strip().lower().replace(" ", "_")


def _score_soil(crop: CropProfile, soil: str) -> tuple[float, list[str]]:
    soil_n = _normalize(soil)
    if soil_n in crop.ideal_soils:
        return 1.0, [f"Soil type '{soil}' is ideal for {crop.name}"]
    if soil_n in {"clay", "loam"} and "loam" in crop.ideal_soils:
        return 0.7, [f"Soil '{soil}' is acceptable for {crop.name}"]
    return 0.35, [f"Soil '{soil}' is suboptimal; consider soil amendments for {crop.name}"]


def _score_season(crop: CropProfile, season: str) -> tuple[float, list[str]]:
    season_n = _normalize(season)
    if season_n in crop.seasons:
        return 1.0, [f"Season '{season}' matches growing window for {crop.name}"]
    overlap = {"summer", "monsoon", "kharif"} & crop.seasons
    if season_n in {"summer", "monsoon"} and overlap:
        return 0.75, [f"Season '{season}' partially overlaps with {crop.name} cycle"]
    return 0.4, [f"Season '{season}' is outside primary window for {crop.name}"]


def _score_temperature(crop: CropProfile, temp: float) -> tuple[float, list[str]]:
    if crop.temp_min <= temp <= crop.temp_max:
        return 1.0, [f"Temperature {temp}°C is within optimal range ({crop.temp_min}–{crop.temp_max}°C)"]
    margin = 3
    if crop.temp_min - margin <= temp <= crop.temp_max + margin:
        return 0.65, [f"Temperature {temp}°C is near acceptable limits for {crop.name}"]
    return 0.25, [f"Temperature {temp}°C may stress {crop.name}; monitor closely"]


def _score_water(crop: CropProfile, water: str) -> tuple[float, list[str]]:
    water_n = _normalize(water)
    need = crop.water_need
    order = {"low": 1, "medium": 2, "high": 3, "rainfed": 1, "irrigated": 3}
    avail = order.get(water_n, 2)
    required = order.get(need, 2)
    if avail >= required:
        return 1.0, [f"Water availability '{water}' meets {crop.name} requirements"]
    if avail == required - 1:
        return 0.55, [f"Water '{water}' is marginal for {crop.name}; plan supplemental irrigation"]
    return 0.2, [f"Insufficient water for {crop.name}; not recommended without irrigation upgrade"]


def _score_land(crop: CropProfile, acres: float) -> tuple[float, list[str]]:
    if acres >= crop.min_acres:
        return 1.0, [f"Land size {acres} acres is sufficient for {crop.name}"]
    return 0.5, [f"Minimum recommended area for {crop.name} is {crop.min_acres} acres"]


def recommend_crops(
    soil_type: str,
    season: str,
    temperature_c: float,
    water_availability: str,
    land_size_acres: float,
    top_n: int = 5,
) -> list[dict]:
    results = []
    for crop in CROP_DATABASE:
        scores, reasons = [], []
        for fn, weight in [
            (_score_soil, 0.25),
            (_score_season, 0.25),
            (_score_temperature, 0.2),
            (_score_water, 0.2),
            (_score_land, 0.1),
        ]:
            if fn == _score_soil:
                s, r = fn(crop, soil_type)
            elif fn == _score_season:
                s, r = fn(crop, season)
            elif fn == _score_temperature:
                s, r = fn(crop, temperature_c)
            elif fn == _score_water:
                s, r = fn(crop, water_availability)
            else:
                s, r = fn(crop, land_size_acres)
            scores.append(s * weight)
            reasons.extend(r)

        total = sum(scores) * 100
        confidence = "high" if total >= 75 else "medium" if total >= 55 else "low"
        results.append(
            {
                "crop": crop.name,
                "suitability_score": round(total, 1),
                "confidence": confidence,
                "reasons": reasons[:4],
                "expected_yield_t_per_acre": crop.yield_t_per_acre,
                "notes": crop.notes,
            }
        )

    results.sort(key=lambda x: x["suitability_score"], reverse=True)
    return results[:top_n]
