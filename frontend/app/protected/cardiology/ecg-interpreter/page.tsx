"use client";

import { useState } from "react";
import ECGInterpreterForm from "@/features/cardiology/components/ECGInterpreterForm";
import ECGInterpreterResult from "@/features/cardiology/components/ECGInterpreterResult";
import { ECGInterpreterInput, ECGInterpreterOutput } from "@/features/cardiology/types";

export default function ECGInterpreterPage() {
  const [input, setInput] = useState<ECGInterpreterInput | null>(null);  // ✅ Track input
  const [result, setResult] = useState<ECGInterpreterOutput | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (data: ECGInterpreterInput) => {
    setLoading(true);
    setError(null);
    setResult(null);
    setInput(data);  // ✅ Store the input data

    try {
      // Get JWT token
      const token = localStorage.getItem("accessToken");
      if (!token) {
        setError("You must be logged in to use this module.");
        setLoading(false);
        return;
      }

      const response = await fetch("/api/v1/cardiology/ecg-interpreter", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.error || `API Error: ${response.statusText}`);
      }

      const resultData: ECGInterpreterOutput = await response.json();
      setResult(resultData);
    } catch (err: any) {
      console.error("ECG Interpreter error:", err);
      setError(err.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setInput(null);
    setResult(null);
    setError(null);
  };

  return (
    <main className="max-w-3xl mx-auto p-6 space-y-6">
      <header>
        <h1 className="text-3xl font-bold mb-4">⚡ ECG Interpreter</h1>
        <p className="text-gray-700 mb-6">
          Analyze ECG parameters for AI-assisted rhythm and abnormality detection.
        </p>
      </header>

      <section>
        <ECGInterpreterForm onSubmit={handleSubmit} loading={loading} />
      </section>

      {loading && (
        <p className="text-blue-600 mt-4" data-testid="loading-message">
          Analyzing ECG...
        </p>
      )}

      {error && (
        <p className="text-red-600 mt-4" data-testid="error-message">
          {error}
        </p>
      )}

      {result && input && (
        <section>
          <ECGInterpreterResult 
            input={input}              // ✅ Pass the stored input
            interpretation={result}
            onReset={handleReset}      // ✅ Pass the reset handler
          />
        </section>
      )}
      <p className="text-sm text-gray-500 mt-6">
        ⚠️ For research and planning use only. Not a medical device.
      </p>
    </main>
  );
}