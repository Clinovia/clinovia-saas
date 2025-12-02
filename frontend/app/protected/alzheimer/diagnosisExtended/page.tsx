"use client";

import { useState } from "react";
import DiagExtendedForm from "@/features/alzheimer/components/DiagExtendedForm";
import DiagExtendedResult from "@/features/alzheimer/components/DiagExtendedResult";
import { AlzheimerDiagnosisExtendedInput, AlzheimerDiagnosisExtendedOutput } from "@/features/alzheimer/types";

export default function ExtendedDiagnosisPage() {
  const [output, setOutput] = useState<AlzheimerDiagnosisExtendedOutput | undefined>();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (data: AlzheimerDiagnosisExtendedInput) => {
    setLoading(true);
    setOutput(undefined);
    setError(null);

    try {
      // 🔥 Get JWT token from localStorage
      const token = localStorage.getItem("accessToken");

      if (!token) {
        setError("You must be logged in to use this module.");
        setLoading(false);
        return;
      }

      const response = await fetch("/api/v1/alzheimer/diagnosisExtended", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`, // 🔥 send token
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.error || `API Error: ${response.statusText}`);
      }

      const result: AlzheimerDiagnosisExtendedOutput = await response.json();
      setOutput(result);
    } catch (err: any) {
      console.error("Error submitting extended diagnosis:", err);
      setError(err.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-4 space-y-6">
      <h1 className="text-2xl font-bold">🧠 Alzheimer's Extended Diagnosis</h1>
      <DiagExtendedForm onSubmit={handleSubmit} loading={loading} />
      {error && <p className="text-red-600">{error}</p>}
      <DiagExtendedResult output={output} />
    </div>
  );
}
