"""Fertilizer recommendations based on soil type and crop nutrient needs."""

SOIL_AMENDMENTS = {
    "clay": ["Add organic compost to improve drainage", "Gypsum application if waterlogged"],
    "sandy": ["Frequent organic matter additions", "Mulching to retain moisture"],
    "loam": ["Maintain organic matter with green manure"],
    "silt": ["Avoid over-tilling; use cover crops"],
    "black": ["Monitor for zinc deficiency in high pH patches"],
    "red": ["Lime or dolomite if pH below 5.5; phosphorus often limiting"],
    "alluvial": ["Balanced NPK based on soil test"],
}

CROP_FERTILIZER = {
    "Rice": {"npk": "120:60:40", "stages": ["Basal NPK at transplant", "Urea top-dress at tillering", "Potash before panicle"]},
    "Wheat": {"npk": "120:60:40", "stages": ["Full basal at sowing", "Nitrogen split at crown root and flowering"]},
    "Maize": {"npk": "150:75:60", "stages": ["Basal at sowing", "Side-dress N at knee-high stage"]},
    "Cotton": {"npk": "100:50:50", "stages": ["Basal P&K", "N in splits through square formation"]},
    "Soybean": {"npk": "20:60:40", "stages": ["Low N; focus P&K at sowing", "Rhizobium inoculation"]},
    "Groundnut": {"npk": "25:50:50", "stages": ["Gypsum at pegging", "Avoid excess nitrogen"]},
    "Millet (Bajra)": {"npk": "60:30:30", "stages": ["Basal at sowing", "Light N if rainfed"]},
    "Sorghum": {"npk": "80:40:40", "stages": ["Basal", "Top-dress N before boot stage"]},
    "Sugarcane": {"npk": "250:80:120", "stages": ["Basal", "Top-dress every 60–90 days"]},
    "Potato": {"npk": "150:100:120", "stages": ["Full basal before planting", "Foliar micronutrients if needed"]},
    "Tomato": {"npk": "100:80:100", "stages": ["Basal", "Calcium nitrate during fruiting"]},
    "Onion": {"npk": "100:50:75", "stages": ["Basal", "N splits during bulb development"]},
    "Pulses (Moong)": {"npk": "20:40:20", "stages": ["Minimal N; P&K at sowing"]},
    "Mustard": {"npk": "80:40:40", "stages": ["Basal at sowing", "Sulfur if deficient"]},
    "Banana": {"npk": "200:60:300", "stages": ["Monthly splits", "Heavy K for fruit quality"]},
}

ORGANIC_BY_SOIL = {
    "clay": ["Farmyard manure 10 t/acre", "Vermicompost 2 t/acre"],
    "sandy": ["Green manure (dhaincha)", "Coconut coir pith compost"],
    "loam": ["Compost 5–8 t/acre", "Neem cake 200 kg/acre"],
    "red": ["Bone meal for P", "Wood ash for K in small doses"],
    "black": ["Compost 6 t/acre", "Biofertilizers (Azotobacter)"],
}


def recommend_fertilizers(soil_type: str, crops: list[str]) -> list[dict]:
    soil_n = soil_type.strip().lower()
    amendments = SOIL_AMENDMENTS.get(soil_n, ["Conduct soil test for precise dosing"])
    organic = ORGANIC_BY_SOIL.get(soil_n, ["Compost 5 t/acre", "Vermicompost 1 t/acre"])

    plans = []
    for crop in crops[:3]:
        profile = CROP_FERTILIZER.get(crop, {"npk": "80:40:40", "stages": ["Basal NPK at sowing", "Top-dress as per growth"]})
        chemical = [
            {"stage": stage, "application": f"Apply per {profile['npk']} kg/ha equivalent"}
            for stage in profile["stages"]
        ]
        plans.append(
            {
                "crop": crop,
                "npk_ratio": profile["npk"],
                "organic_options": organic,
                "chemical_schedule": chemical,
                "soil_amendments": amendments,
                "notes": [
                    "Split nitrogen to reduce leaching and improve uptake",
                    "Apply micronutrients only after soil test",
                    "Integrate organic + chemical for sustainable productivity",
                ],
            }
        )
    return plans
