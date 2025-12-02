"use client";
import { useState } from "react";
import Prog2yrBasicForm from "@/features/alzheimer/components/Prog2yrBasicForm";
import Prog2yrBasicResult from "@/features/alzheimer/components/Prog2yrBasicResult";
import { AlzheimerPrognosis2yrBasicInput, AlzheimerPrognosis2yrBasicOutput } from "@/features/alzheimer/types";

export default function Prog2yrBasicPage() {
  const [input, setInput] = useState<AlzheimerPrognosis2yrBasicInput | null>(null);
  const [output, setOutput] = useState<AlzheimerPrognosis2yrBasicOutput | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (data: AlzheimerPrognosis2yrBasicInput) => {
    setLoading(true);
    setInput(data);
    setOutput(null);
    setError(null);

    try {
      // 🔥 Get JWT token from localStorage
      const token = localStorage.getItem("accessToken");
      if (!token) {
        setError("You must be logged in to use this module.");
        setLoading(false);
        return;
      }

      const response = await fetch("/api/v1/alzheimer/prognosis2yrBasic", {
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

      const result: AlzheimerPrognosis2yrBasicOutput = await response.json();
      setOutput(result);
    } catch (error: any) {
      console.error("Error predicting 2-year progression:", error);
      setError(error.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setInput(null);
    setOutput(null);
    setError(null);
  };

  return (
    <div className="max-w-5xl mx-auto p-4 space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-50 to-indigo-50 border border-purple-200 rounded-lg p-6 shadow-sm">
        <h1 className="text-3xl font-bold text-gray-800">🧠 Alzheimer's 2-Year Prognosis</h1>
        <p className="text-gray-600 mt-2">
          Basic model for predicting progression to Alzheimer's dementia within 2 years
        </p>
      </div>

      {/* Form - only show if no result */}
      {!output && (
        <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
          <Prog2yrBasicForm onSubmit={handleSubmit} loading={loading} />
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="flex flex-col items-center justify-center py-12 space-y-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
          <p className="text-gray-600">Analyzing patient data and computing prognosis...</p>
        </div>
      )}

      {/* Error Message */}
      {error && !loading && (
        <div className="bg-red-50 border border-red-300 rounded-lg p-4">
          <h3 className="text-lg font-semibold text-red-900 mb-2">❌ Error</h3>
          <p className="text-red-800">{error}</p>
          <button
            onClick={handleReset}
            className="mt-3 px-4 py-2 bg-red-600 text-white rounded-lg font-medium hover:bg-red-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      )}

      {/* Result */}
      {output && input && !loading && (
        <Prog2yrBasicResult 
          input={input} 
          prognosis={output} 
          onReset={handleReset} 
        />
      )}

      {/* Info Box */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="text-sm font-semibold text-blue-900 mb-2">ℹ️ About This Tool</h3>
        <p className="text-sm text-blue-800">
          This basic prognostic model uses demographic data, cognitive scores, and genetic markers 
          to estimate the probability of progression to Alzheimer's dementia within 2 years. 
          For enhanced predictions with biomarker analysis and SHAP explanations, use the Extended model.
        </p>
      </div>
    </div>
  );
}