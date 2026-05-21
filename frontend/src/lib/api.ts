const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export type FarmFormData = {
  farmer_name?: string;
  farmer_id?: number;
  soil_type: string;
  season: string;
  temperature_c: number;
  water_availability: string;
  land_size_acres: number;
  latitude?: number;
  longitude?: number;
};

export type RecommendationResult = {
  id?: number;
  farmer_id?: number;
  crops: Array<{
    crop: string;
    suitability_score: number;
    confidence: string;
    reasons: string[];
    expected_yield_t_per_acre?: number;
  }>;
  fertilizers: Array<{
    crop: string;
    npk_ratio: string;
    organic_options: string[];
    chemical_schedule: Array<{ stage: string; application: string }>;
    soil_amendments: string[];
    notes: string[];
  }>;
  irrigation: {
    weekly_schedule: Array<{
      day: string;
      time: string;
      duration_minutes: number;
      water_liters_per_acre: number;
      method: string;
    }>;
    daily_water_liters: number;
    conservation_tips: string[];
    method_recommended: string;
  };
  weather: {
    current_temp_c?: number;
    forecast_summary: string;
    rainfall_mm_next_7d?: number;
    alerts: Array<{
      type: string;
      severity: string;
      message: string;
      precaution: string;
    }>;
    farming_precautions: string[];
  };
  summary: string;
  future_features: Record<string, string>;
};

export async function analyzeFarm(data: FarmFormData): Promise<RecommendationResult> {
  const res = await fetch(`${API_URL}/api/recommendations/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to get recommendations");
  }
  return res.json();
}

export async function fetchHistory(farmerId: number) {
  const res = await fetch(`${API_URL}/api/recommendations/history/${farmerId}`);
  if (!res.ok) return [];
  return res.json();
}
