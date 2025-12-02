import { useState, useCallback } from "react";

interface DiagnosisPayload {
  age: number;
  mmse?: number;
  moca?: number;
  biomarkerA?: number;
  biomarkerB?: number;
  [key: string]: any;
}

interface DiagnosisResult {
  diagnosis: string;
  probability: number;
  recommendations?: string[];
}

export function useDiagnosis() {
  const [result, setResult] = useState<DiagnosisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const runDiagnosis = useCallback(async (data: DiagnosisPayload) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await fetch("/api/alzheimer/diagnosis", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!res.ok) {
        throw new Error("Failed to compute diagnosis.");
      }

      const json = await res.json();
      setResult(json);
    } catch (err: any) {
      setError(err.message || "Unexpected error.");
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    runDiagnosis,
    loading,
    error,
    result,
  };
}
