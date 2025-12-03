// frontend/app/protected/alzheimer/diagnosisScreening/page.tsx

"use client";

import { useState } from "react";
import DiagnosisScreeningForm from "@/features/alzheimer/components/DiagScreeningForm";
import DiagnosisScreeningResult from "@/features/alzheimer/components/DiagScreeningResult";
import { AlzheimerDiagnosisScreeningInput, AlzheimerDiagnosisScreeningOutput } from "@/features/alzheimer/types";

export default function AlzheimerPage() {
  const [result, setResult] = useState<AlzheimerDiagnosisScreeningOutput | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (data: AlzheimerDiagnosisScreeningInput) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Get auth token from localStorage (optional — API may allow unauthenticated screening)
      const token = localStorage.getItem("accessToken");

      const response = await fetch("/api/v1/alzheimer/diagnosisScreening", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token && { Authorization: `Bearer ${token}` }),
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.error ||
            errorData.detail ||
            errorData.message ||
            `API Error: ${response.status} ${response.statusText}`
        );
      }

      const resultData: AlzheimerDiagnosisScreeningOutput = await response.json();
      setResult(resultData);
    } catch (err: any) {
      console.error("Alzheimer screening error:", err);
      setError(err.message || "Failed to process your request. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <header>
        <h1 className="text-3xl font-bold mb-4">Cognitive Status Classification</h1>
        <p className="text-gray-700 mb-6">
          Predict cognitive status (Cognitively Normal, Mild Cognitive Impairment, Alzheimer's Disease)
          using clinical and cognitive assessment data.
        </p>
      </header>

      <section>
        <DiagnosisScreeningForm onSubmit={handleSubmit} loading={loading} />
      </section>

      {loading && (
        <p className="text-blue-600 mt-4" data-testid="alzheimer-loading">
          Calculating prediction...
        </p>
      )}

      {error && (
        <p className="text-red-600 mt-4" data-testid="alzheimer-error">
          {error}
        </p>
      )}

      {result && (
        <section data-testid="alzheimer-result">
          <DiagnosisScreeningResult result={result} />
        </section>
      )}

      <footer className="pt-4 border-t border-gray-200">
        <p className="text-sm text-gray-500">
          ⚠️ For research and planning use only. Not a medical device. Consult a clinician for diagnosis.
        </p>
      </footer>
    </div>
  );
}