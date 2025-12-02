import { useState, useCallback } from "react";

interface RiskScreenerPayload {
  age: number;
  familyHistory?: boolean;
  geneticFactors?: string[];
  lifestyleFactors?: string[];
  cognitiveComplaints?: boolean;
  [key: string]: any;
}

interface RiskScreenerResult {
  riskScore: number; // 0–1 or 0–100 depending on model
  category: "low" | "moderate" | "high";
  recommendations?: string[];
}

export function useRiskScreener() {
  const [result, setResult] = useState<RiskScreenerResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const runRiskScreener = useCallback(async (data: RiskScreenerPayload) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await fetch("/api/alzheimer/risk-screener", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!res.ok) {
        throw new Error("Risk screening failed.");
      }

      const json = await res.json();
      setResult(json);
    } catch (err: any) {
      setError(err.message || "Unexpected error during risk screening.");
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    runRiskScreener,
    loading,
    error,
    result,
  };
}
