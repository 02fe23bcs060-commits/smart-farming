from app.services.crop_engine import recommend_crops


def test_recommend_crops_returns_ranked_list():
    results = recommend_crops(
        soil_type="loam",
        season="kharif",
        temperature_c=28,
        water_availability="medium",
        land_size_acres=2.0,
    )
    assert len(results) == 5
    assert results[0]["suitability_score"] >= results[-1]["suitability_score"]
    assert "crop" in results[0]
    assert results[0]["confidence"] in ("high", "medium", "low")


def test_low_water_favors_drought_tolerant():
    results = recommend_crops(
        soil_type="sandy",
        season="summer",
        temperature_c=35,
        water_availability="low",
        land_size_acres=1.0,
    )
    crop_names = [r["crop"] for r in results]
    assert any("Millet" in c or "Groundnut" in c or "Sorghum" in c for c in crop_names)
