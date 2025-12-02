"use client";

import { useState } from "react";
import BPCategoryForm from "@/features/cardiology/components/BPCategoryForm";
import BPCategoryResult from "@/features/cardiology/components/BPCategoryResult";
import { BPCategoryInput, BPCategoryOutput } from "@/features/cardiology/types";

export default function BPCategoryPage() {
  const [result, setResult] = useState<BPCategoryOutput | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (data: BPCategoryInput) => {
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

      const response = await fetch("/api/v1/cardiology/bp-category", {
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

      const resultData: BPCategoryOutput = await response.json();
      setResult(resultData);

    } catch (err: any) {
      console.error("BP Category Error:", err);
      setError(err.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <h1 className="text-3xl font-bold mb-4">🩺 Blood Pressure Category</h1>
      <p className="text-gray-700 mb-6">
        Enter blood pressure readings to classify the patient’s BP category.
      </p>

      <BPCategoryForm onSubmit={handleSubmit} loading={loading} />

      {loading && <p className="text-blue-600 mt-4">Classifying...</p>}
      {error && <p className="text-red-600 mt-4">{error}</p>}
      {result && <BPCategoryResult output={result} />}
    </div>
  );
}
