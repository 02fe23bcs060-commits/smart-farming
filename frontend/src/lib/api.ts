// Browser uses same origin (Next.js proxies /api → backend). Avoids localhost/EC2 URL issues.
function getApiBase(): string {
  if (typeof window !== "undefined") {
    return "";
  }
  return process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
}

const API_URL = getApiBase();

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

async function parseError(res: Response): Promise<string> {
  try {
    const err = await res.json();
    if (typeof err.detail === "string") return err.detail;
    if (Array.isArray(err.detail)) return err.detail.map((d: { msg?: string }) => d.msg).join(", ");
  } catch {
    /* ignore */
  }
  return `Request failed (${res.status})`;
}

export async function analyzeFarm(data: FarmFormData): Promise<RecommendationResult> {
  let res: Response;
  try {
    res = await fetch(`${API_URL}/api/recommendations/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
  } catch {
    throw new Error(
      "Failed to fetch — API not reachable. On EC2: rebuild frontend (git pull && docker compose build --no-cache frontend && docker compose up -d)."
    );
  }
  if (!res.ok) {
    throw new Error(await parseError(res));
  }
  return res.json();
}

export async function fetchHistory(farmerId: number) {
  try {
    const res = await fetch(`${API_URL}/api/recommendations/history/${farmerId}`);
    if (!res.ok) return [];
    return res.json();
  } catch {
    return [];
  }
}
