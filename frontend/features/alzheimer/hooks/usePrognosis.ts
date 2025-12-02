import { useState, useCallback } from "react";

interface PrognosisPayload {
  age: number;
  mmse?: number;
  baselineSymptoms?: string[];
  geneticFactors?: string[];
  imagingScore?: number;
  [key: string]: any;
}

interface PrognosisResult {
  progressionRisk: number; // example: % chance of decline in 2 yrs
  category: "low" | "medium" | "high";
  expectedTrajectory?: string;
}

export function usePrognosis() {
  const [result, setResult] = useState<PrognosisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const runPrognosis = useCallback(async (data: PrognosisPayload) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await fetch("/api/alzheimer/prognosis", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!res.ok) {
        throw new Error("Failed to compute prognosis.");
      }

      const json = await res.json();
      setResult(json);
    } catch (err: any) {
      setError(err.message || "Unexpected error during prognosis.");
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    runPrognosis,
    loading,
    error,
    result,
  };
}
