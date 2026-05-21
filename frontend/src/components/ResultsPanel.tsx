"use client";

import type { RecommendationResult } from "@/lib/api";

const severityColor: Record<string, string> = {
  critical: "bg-red-100 text-red-800 border-red-200",
  high: "bg-orange-100 text-orange-800 border-orange-200",
  medium: "bg-amber-100 text-amber-800 border-amber-200",
  low: "bg-blue-100 text-blue-800 border-blue-200",
};

type Props = {
  result: RecommendationResult | null;
};

export default function ResultsPanel({ result }: Props) {
  if (!result) return null;

  return (
    <div className="space-y-6">
      <div className="card bg-field-600 text-white">
        <h2 className="text-xl font-semibold mb-2">Summary</h2>
        <p className="text-field-50 leading-relaxed">{result.summary}</p>
      </div>

      <section className="card">
        <h3 className="text-xl font-display text-field-800 mb-4">Recommended crops</h3>
        <div className="space-y-3">
          {result.crops.map((c, i) => (
            <div
              key={c.crop}
              className={`rounded-xl p-4 border ${
                i === 0 ? "border-harvest-500 bg-harvest-400/10" : "border-field-100 bg-field-50/50"
              }`}
            >
              <div className="flex justify-between items-start gap-2">
                <span className="font-bold text-lg text-field-900">
                  {i === 0 && "★ "}
                  {c.crop}
                </span>
                <span className="text-field-700 font-semibold">{c.suitability_score}% match</span>
              </div>
              <p className="text-sm text-field-600 mt-1">
                Confidence: {c.confidence}
                {c.expected_yield_t_per_acre != null &&
                  ` · Est. yield ~${c.expected_yield_t_per_acre} t/acre`}
              </p>
              <ul className="mt-2 text-sm text-field-700 list-disc list-inside">
                {c.reasons.map((r) => (
                  <li key={r}>{r}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>

      <section className="card">
        <h3 className="text-xl font-display text-field-800 mb-4">Fertilizer plan</h3>
        {result.fertilizers.map((f) => (
          <div key={f.crop} className="mb-4 pb-4 border-b border-field-100 last:border-0">
            <h4 className="font-semibold text-field-800">{f.crop} — NPK {f.npk_ratio}</h4>
            <p className="text-sm text-field-600 mt-1">
              Organic: {f.organic_options.join(", ")}
            </p>
            <p className="text-sm text-field-600">Soil: {f.soil_amendments.join("; ")}</p>
          </div>
        ))}
      </section>

      <section className="card">
        <h3 className="text-xl font-display text-field-800 mb-2">Irrigation schedule</h3>
        <p className="text-sm text-field-600 mb-3">
          Method: <strong>{result.irrigation.method_recommended}</strong> · Daily water:{" "}
          <strong>{result.irrigation.daily_water_liters.toLocaleString()} L</strong>
        </p>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-field-700 border-b">
                <th className="py-2">Day</th>
                <th>Time</th>
                <th>Duration</th>
                <th>Water/acre</th>
              </tr>
            </thead>
            <tbody>
              {result.irrigation.weekly_schedule.map((s) => (
                <tr key={`${s.day}-${s.time}`} className="border-b border-field-50">
                  <td className="py-2 font-medium">{s.day}</td>
                  <td>{s.time}</td>
                  <td>{s.duration_minutes} min</td>
                  <td>{Math.round(s.water_liters_per_acre).toLocaleString()} L</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <ul className="mt-3 text-sm text-field-700 list-disc list-inside">
          {result.irrigation.conservation_tips.map((t) => (
            <li key={t}>{t}</li>
          ))}
        </ul>
      </section>

      <section className="card">
        <h3 className="text-xl font-display text-field-800 mb-4">Weather alerts</h3>
        <p className="text-sm text-field-600 mb-3">{result.weather.forecast_summary}</p>
        {result.weather.alerts.map((a) => (
          <div
            key={a.type}
            className={`rounded-lg border p-3 mb-2 ${severityColor[a.severity] || severityColor.low}`}
          >
            <p className="font-semibold">{a.message}</p>
            <p className="text-sm mt-1">{a.precaution}</p>
          </div>
        ))}
        <ul className="mt-3 text-sm list-disc list-inside text-field-700">
          {result.weather.farming_precautions.map((p) => (
            <li key={p}>{p}</li>
          ))}
        </ul>
      </section>

      <section className="card bg-field-50">
        <h3 className="text-lg font-semibold text-field-800 mb-2">Coming soon</h3>
        <ul className="text-sm text-field-700 space-y-1">
          {Object.entries(result.future_features).map(([k, v]) => (
            <li key={k}>
              <span className="font-medium capitalize">{k.replace(/_/g, " ")}</span>: {v}
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
