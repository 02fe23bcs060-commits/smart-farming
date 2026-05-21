"use client";

import { useState } from "react";
import type { FarmFormData } from "@/lib/api";

const SOIL_OPTIONS = ["loam", "clay", "sandy", "silt", "black", "red", "alluvial"];
const SEASON_OPTIONS = ["kharif", "rabi", "zaid", "summer", "winter", "monsoon"];
const WATER_OPTIONS = ["low", "medium", "high", "rainfed", "irrigated"];

type Props = {
  onSubmit: (data: FarmFormData) => void;
  loading: boolean;
};

export default function FarmForm({ onSubmit, loading }: Props) {
  const [form, setForm] = useState<FarmFormData>({
    farmer_name: "",
    soil_type: "loam",
    season: "kharif",
    temperature_c: 28,
    water_availability: "medium",
    land_size_acres: 2,
  });

  const update = (key: keyof FarmFormData, value: string | number) => {
    setForm((f) => ({ ...f, [key]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const payload: FarmFormData = { ...form };
    if (!payload.farmer_name?.trim()) delete payload.farmer_name;
    onSubmit(payload);
  };

  return (
    <form onSubmit={handleSubmit} className="card space-y-5">
      <h2 className="text-2xl font-display text-field-800">Your farm details</h2>
      <p className="text-field-600 text-sm">
        Enter your field conditions. Our AI engine will suggest crops, fertilizer, and irrigation plans.
      </p>

      <div>
        <label className="label" htmlFor="farmer_name">
          Your name (optional — saves history)
        </label>
        <input
          id="farmer_name"
          className="input-field"
          placeholder="e.g. Ramesh Kumar"
          value={form.farmer_name || ""}
          onChange={(e) => update("farmer_name", e.target.value)}
        />
      </div>

      <div className="grid sm:grid-cols-2 gap-4">
        <div>
          <label className="label" htmlFor="soil_type">Soil type</label>
          <select
            id="soil_type"
            className="input-field"
            value={form.soil_type}
            onChange={(e) => update("soil_type", e.target.value)}
          >
            {SOIL_OPTIONS.map((s) => (
              <option key={s} value={s}>
                {s.charAt(0).toUpperCase() + s.slice(1)}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="label" htmlFor="season">Season</label>
          <select
            id="season"
            className="input-field"
            value={form.season}
            onChange={(e) => update("season", e.target.value)}
          >
            {SEASON_OPTIONS.map((s) => (
              <option key={s} value={s}>
                {s.charAt(0).toUpperCase() + s.slice(1)}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="grid sm:grid-cols-2 gap-4">
        <div>
          <label className="label" htmlFor="temperature">
            Temperature (°C): {form.temperature_c}
          </label>
          <input
            id="temperature"
            type="range"
            min={5}
            max={48}
            step={1}
            className="w-full accent-field-600"
            value={form.temperature_c}
            onChange={(e) => update("temperature_c", Number(e.target.value))}
          />
        </div>
        <div>
          <label className="label" htmlFor="water">Water availability</label>
          <select
            id="water"
            className="input-field"
            value={form.water_availability}
            onChange={(e) => update("water_availability", e.target.value)}
          >
            {WATER_OPTIONS.map((w) => (
              <option key={w} value={w}>
                {w.charAt(0).toUpperCase() + w.slice(1)}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div>
        <label className="label" htmlFor="land">
          Land size (acres): {form.land_size_acres}
        </label>
        <input
          id="land"
          type="range"
          min={0.1}
          max={100}
          step={0.1}
          className="w-full accent-field-600"
          value={form.land_size_acres}
          onChange={(e) => update("land_size_acres", Number(e.target.value))}
        />
      </div>

      <button type="submit" className="btn-primary w-full text-lg" disabled={loading}>
        {loading ? "Analyzing your farm…" : "Get AI recommendations"}
      </button>
    </form>
  );
}
