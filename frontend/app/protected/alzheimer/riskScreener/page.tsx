"use client";

import { useState } from "react";
import AlzheimerRiskForm from "@/features/alzheimer/components/RiskScreenerForm";
import AlzheimerRiskResult from "@/features/alzheimer/components/RiskScreenerResult";
import { AlzheimerRiskScreenerInput, AlzheimerRiskScreenerOutput } from "@/features/alzheimer/types";

export default function RiskScreenerPage() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AlzheimerRiskScreenerOutput | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (data: AlzheimerRiskScreenerInput) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // 🔥 Get JWT token from localStorage
      const token = localStorage.getItem("accessToken");
      if (!token) {
        setError("You must be logged in to use this module.");
        setLoading(false);
        return;
      }

      const response = await fetch("/api/v1/alzheimer/riskScreener", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`, // 🔥 include token
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.error || `API Error: ${response.statusText}`);
      }

      const resultData: AlzheimerRiskScreenerOutput = await response.json();
      setResult(resultData);
    } catch (err: any) {
      console.error("Error submitting risk screener:", err);
      setError(err.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-4">Alzheimer Risk Screener</h1>
      <p className="mb-6">
        Assess the risk of Alzheimer's based on clinical, cognitive, and genetic factors.
      </p>

      <AlzheimerRiskForm onSubmit={handleSubmit} loading={loading} />

      {error && <p className="text-red-600 mt-4">{error}</p>}

      {result && <AlzheimerRiskResult output={result} />}

      <p className="text-sm text-gray-500 mt-6">
        ⚠️ For research and planning use only. Not a medical device.
      </p>
    </div>
  );
}
