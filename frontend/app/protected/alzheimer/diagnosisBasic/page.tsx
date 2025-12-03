"use client";

import { useState } from "react";
import DiagBasicForm from "@/features/alzheimer/components/DiagBasicForm";
import DiagBasicResult from "@/features/alzheimer/components/DiagBasicResult";
import {
  AlzheimerDiagnosisBasicInput,
  AlzheimerDiagnosisBasicOutput,
} from "@/features/alzheimer/types";

import {
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";

export default function BasicDiagnosisPage() {
  const [output, setOutput] = useState<AlzheimerDiagnosisBasicOutput | undefined>();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (data: AlzheimerDiagnosisBasicInput) => {
    setLoading(true);
    setOutput(undefined);
    setError(null);

    try {
      const token = localStorage.getItem("accessToken");

      if (!token) {
        setError("You must be logged in to use this module.");
        setLoading(false);
        return;
      }

      const response = await fetch("/api/v1/alzheimer/diagnosisBasic", {
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

      const result: AlzheimerDiagnosisBasicOutput = await response.json();
      setOutput(result);
    } catch (err: any) {
      console.error("Error submitting basic diagnosis:", err);
      setError(err.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-4 space-y-6">
      
      <header>
        <h1 className="text-3xl font-bold mb-4">Alzheimer Diagnosis with Basic Features</h1>
        <p className="text-gray-700 mb-6">
          Trained on ADNI data. Research use only.
        </p>
      </header>

      <DiagBasicForm onSubmit={handleSubmit} loading={loading} />

      {error && <p className="text-red-600">{error}</p>}

      <DiagBasicResult output={output} />
      <p className="text-sm text-gray-500 mt-6">
        ⚠️ For research and planning use only. Not a medical device.
      </p>
    </div>
  );
}
