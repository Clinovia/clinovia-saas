"use client";

import { useState } from "react";
import CHA2DS2VAScForm from "@/features/cardiology/components/CHA2DS2VAScForm";
import CHA2DS2VAScResult from "@/features/cardiology/components/CHA2DS2VAScResult";
import { CHA2DS2VAScInput, CHA2DS2VAScOutput } from "@/features/cardiology/types";

export default function CHA2DS2VAScPage() {
  const [result, setResult] = useState<CHA2DS2VAScOutput | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (data: CHA2DS2VAScInput) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // 🔥 Get JWT token
      const token = localStorage.getItem("accessToken");

      if (!token) {
        setError("You must be logged in to use this module.");
        setLoading(false);
        return;
      }

      const response = await fetch("/api/v1/cardiology/cha2ds2vasc", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`, // 🔥 IMPORTANT
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.error || `API Error: ${response.statusText}`);
      }

      const resultData: CHA2DS2VAScOutput = await response.json();
      setResult(resultData);

    } catch (err: any) {
      console.error(err);
      setError(err.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="max-w-3xl mx-auto p-6 space-y-6">
      <header>
        <h1 className="text-3xl font-bold mb-4">💓 CHA₂DS₂-VASc Score</h1>
        <p className="text-gray-700 mb-6">
          Assess stroke risk for atrial fibrillation using the CHA₂DS₂-VASc scoring system.
        </p>
      </header>

      <section>
        <CHA2DS2VAScForm onSubmit={handleSubmit} loading={loading} />
      </section>

      {loading && (
        <p className="text-blue-600 mt-4" data-testid="loading-message">
          Calculating...
        </p>
      )}

      {error && (
        <p className="text-red-600 mt-4" data-testid="error-message">
          {error}
        </p>
      )}

      {result && (
        <section>
          <CHA2DS2VAScResult output={result} />
        </section>
      )}
    </main>
  );
}
