"use client";
import { useState } from "react";
import ASCVDForm from "@/features/cardiology/components/ASCVDForm";
import ASCVDResult from "@/features/cardiology/components/ASCVDResult";
import { ASCVDInput, ASCVDOutput } from "@/features/cardiology/types";

export default function ASCVDPage() {
  const [result, setResult] = useState<ASCVDOutput | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (data: ASCVDInput) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Get auth token from localStorage (adjust if you store it differently)
      const token = localStorage.getItem("accessToken");
      
      const response = await fetch("/api/v1/cardiology/ascvd", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token && { "Authorization": `Bearer ${token}` }),
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || errorData.detail || `API Error: ${response.statusText}`);
      }

      const resultData: ASCVDOutput = await response.json();
      setResult(resultData);
    } catch (err: any) {
      console.error(err);
      setError(err.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <h1 className="text-3xl font-bold mb-4">🫀 ASCVD Risk Calculator</h1>
      <p className="text-gray-700 mb-6">
        Enter patient data below to calculate the 10-year ASCVD risk percentage and category.
      </p>

      <ASCVDForm onSubmit={handleSubmit} loading={loading} />

      {loading && <p className="text-blue-600 mt-4">Calculating risk...</p>}
      {error && <p className="text-red-600 mt-4">{error}</p>}
      {result && <ASCVDResult output={result} />}
      <p className="text-sm text-gray-500 mt-6">
        ⚠️ For research and planning use only. Not a medical device.
      </p>
    </div>
  );

}