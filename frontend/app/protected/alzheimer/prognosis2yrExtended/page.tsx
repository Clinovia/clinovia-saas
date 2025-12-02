"use client";

import { useState } from "react";
import Prog2yrExtendedForm from "@/features/alzheimer/components/Prog2yrExtendedForm";
import Prog2yrExtendedResult from "@/features/alzheimer/components/Prog2yrExtendedResult";
import { AlzheimerPrognosis2yrExtendedInput, AlzheimerPrognosis2yrExtendedOutput } from "@/features/alzheimer/types";

export default function Prog2yrExtendedPage() {
  const [input, setInput] = useState<AlzheimerPrognosis2yrExtendedInput | null>(null);
  const [prognosis, setPrognosis] = useState<AlzheimerPrognosis2yrExtendedOutput | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (data: AlzheimerPrognosis2yrExtendedInput) => {
    setLoading(true);
    setError(null); // clear previous errors
    // Keep existing `input` if you want to preserve it on reset—optional
    setInput(data);

    try {
      const token = localStorage.getItem("accessToken");
      if (!token) {
        setError("You must be logged in to use this module.");
        setLoading(false);
        return;
      }

      const response = await fetch("/api/v1/alzheimer/prognosis2yrExtended", {
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

      const result: AlzheimerPrognosis2yrExtendedOutput = await response.json();
      console.log("API Response:", result);
      setPrognosis(result);
    } catch (error: any) {
      console.error("Error predicting 2-year progression (extended):", error);
      setError(error.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    // Optional: keep form filled by not resetting `input`
    setPrognosis(null);
    setError(null);
    // If you want to clear the form too, uncomment:
    // setInput(null);
  };

  return (
    <div className="max-w-6xl mx-auto p-4 space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-50 to-indigo-50 border border-purple-200 rounded-lg p-6 shadow-sm">
        <h1 className="text-3xl font-bold text-gray-800">🧠 Alzheimer's 2-Year Prognosis (Extended)</h1>
        <p className="text-gray-600 mt-2">
          Advanced model with biomarker analysis and SHAP-based explainability for predicting progression to Alzheimer's dementia within 2 years.
        </p>
      </div>

      {/* Form: always visible */}
      <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
        <Prog2yrExtendedForm onSubmit={handleSubmit} loading={loading} />
      </div>

      {/* Loading State */}
      {loading && (
        <div className="flex flex-col items-center justify-center py-12 space-y-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
          <p className="text-gray-600 font-medium">Analyzing patient data with biomarkers...</p>
          <p className="text-gray-500 text-sm">Computing SHAP values and feature importance</p>
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

      {/* Result: appended below form when ready */}
      {prognosis && input && !loading && (
        <Prog2yrExtendedResult 
          input={input}
          prognosis={prognosis}
          onReset={handleReset} 
        />
      )}

      {/* Info Box */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="text-sm font-semibold text-blue-900 mb-2">ℹ️ About This Tool</h3>
        <div className="text-sm text-blue-800 space-y-2">
          <p>
            This extended prognostic model incorporates advanced biomarker data including CSF markers 
            (Aβ42, tau, p-tau), neuroimaging (hippocampal volume, FDG-PET, amyloid PET), alongside 
            demographic and cognitive measures.
          </p>
          <p className="font-medium">
            <strong>Key Features:</strong>
          </p>
          <ul className="list-disc list-inside ml-2 space-y-1">
            <li>SHAP (SHapley Additive exPlanations) values for interpretable AI</li>
            <li>Confidence intervals for probability estimates</li>
            <li>Feature importance ranking</li>
            <li>Biomarker-enhanced predictions</li>
          </ul>
        </div>
      </div>
    </div>
  );
}