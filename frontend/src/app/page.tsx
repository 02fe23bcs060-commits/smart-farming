"use client";

import { useState } from "react";
import FarmForm from "@/components/FarmForm";
import ResultsPanel from "@/components/ResultsPanel";
import { analyzeFarm, type FarmFormData, type RecommendationResult } from "@/lib/api";

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<RecommendationResult | null>(null);

  const handleSubmit = async (data: FarmFormData) => {
    setLoading(true);
    setError(null);
    try {
      const res = await analyzeFarm(data);
      setResult(res);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen">
      <header className="bg-field-800 text-white py-8 px-4 shadow-lg">
        <div className="max-w-6xl mx-auto">
          <p className="text-field-200 text-sm uppercase tracking-wider">Next-gen agriculture</p>
          <h1 className="text-3xl md:text-4xl font-display mt-1">AgriSmart Farming Advisor</h1>
          <p className="text-field-100 mt-2 max-w-2xl text-lg">
            Data-driven crop, fertilizer, and water recommendations — reduce guesswork and farm
            smarter....
          </p>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-4 py-8 grid lg:grid-cols-2 gap-8">
        <div>
          <FarmForm onSubmit={handleSubmit} loading={loading} />
          {error && (
            <p className="mt-4 text-red-700 bg-red-50 border border-red-200 rounded-xl p-4">
              {error}
            </p>
          )}
        </div>
        <div>
          {!result && !loading && (
            <div className="card text-center text-field-600 py-16">
              <p className="text-5xl mb-4">🌾</p>
              <p>Fill in your farm details and tap Get AI recommendations to see results here.</p>
            </div>
          )}
          {loading && (
            <div className="card text-center text-field-600 py-16 animate-pulse">
              Analyzing soil, season, weather, and water…
            </div>
          )}
          <ResultsPanel result={result} />
        </div>
      </div>

      <footer className="text-center text-field-600 text-sm py-8 border-t border-field-100">
        Smart Farming · Docker · Jenkins · AWS · Ansible · Built for sustainable agriculture
      </footer>
    </main>
  );
}
