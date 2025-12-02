"use client";

import React from "react";
import { AlzheimerPrognosis2yrExtendedInput, AlzheimerPrognosis2yrExtendedOutput } from "@/features/alzheimer/types";

interface Props {
  input: AlzheimerPrognosis2yrExtendedInput; // kept for future use or debugging
  prognosis: AlzheimerPrognosis2yrExtendedOutput; // required — only rendered when valid
  onReset: () => void;
}

export default function Prog2yrExtendedResult({ input, prognosis, onReset }: Props) {
  // Since this component is only rendered when prognosis exists (from parent),
  // we assume `prognosis` is valid. But still guard critical fields defensively.

  const safePercent = (value: number | null | undefined): string => {
    if (value == null || isNaN(value)) return "N/A";
    return `${(value * 100).toFixed(1)}%`;
  };

  const safeWidth = (value: number | null | undefined): string => {
    if (value == null || isNaN(value)) return "0%";
    return `${Math.min(value * 100, 100).toFixed(1)}%`;
  };

  const getRiskColor = (risk: string | null | undefined): string => {
    const riskLower = (risk || "unknown").toLowerCase();
    if (riskLower === "low") return "bg-green-100 text-green-800";
    if (riskLower === "moderate") return "bg-yellow-100 text-yellow-800";
    if (riskLower === "high") return "bg-red-100 text-red-800";
    return "bg-gray-100 text-gray-800";
  };

  const formatFieldName = (key: string | null | undefined): string => {
    if (!key) return "Unknown";
    return key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
  };

  return (
    <div className="mt-6 border border-gray-200 rounded-lg bg-white shadow-sm">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-50 to-indigo-50 px-6 py-4 border-b border-gray-200 rounded-t-lg">
        <h2 className="text-2xl font-bold text-gray-800">🧠 Alzheimer’s 2-Year Advanced Prognosis</h2>
        <p className="text-sm text-gray-600 mt-1">
          Model: {prognosis.model_name || "N/A"} (v{prognosis.model_version || "1.0.0"})
        </p>
      </div>

      <div className="p-6 space-y-6">
        {/* Summary */}
        <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
          <h3 className="text-lg font-semibold text-purple-900 mb-3">🔍 Prognosis Summary</h3>
          <div className="mb-4 p-3 bg-white rounded-lg border border-purple-100">
            <p className="text-gray-800 leading-relaxed">
              {prognosis.summary_text || "No summary available."}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Progression Probability */}
            <div className="bg-white p-4 rounded-lg border border-purple-200">
              <p className="text-sm font-medium text-gray-600 mb-2">
                Probability of Progression to AD (2 years)
              </p>
              <p className="text-3xl font-bold text-purple-700">
                {safePercent(prognosis.probability_progression_to_AD_within_2yrs)}
              </p>
              <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-purple-600 h-2 rounded-full transition-all duration-500"
                  style={{ width: safeWidth(prognosis.probability_progression_to_AD_within_2yrs) }}
                />
              </div>
            </div>

            {/* Stable Probability */}
            <div className="bg-white p-4 rounded-lg border border-purple-200">
              <p className="text-sm font-medium text-gray-600 mb-2">
                Probability of Remaining Stable (2 years)
              </p>
              <p className="text-3xl font-bold text-green-700">
                {safePercent(prognosis.probability_stable_within_2yrs)}
              </p>
              <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-green-600 h-2 rounded-full transition-all duration-500"
                  style={{ width: safeWidth(prognosis.probability_stable_within_2yrs) }}
                />
              </div>
            </div>

            {/* Risk Level */}
            <div className="md:col-span-2">
              <p className="text-sm font-medium text-gray-600 mb-2">Risk Level</p>
              <span
                className={`inline-block px-4 py-2 rounded-full text-base font-semibold ${getRiskColor(
                  prognosis.risk_level
                )}`}
              >
                {formatFieldName(prognosis.risk_level)} Risk
              </span>
            </div>
          </div>
        </div>

        {/* Top Features */}
        {Array.isArray(prognosis.top_features) && prognosis.top_features.length > 0 && (
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-3">📊 Key Influential Factors</h3>
            <div className="bg-gray-50 rounded-lg p-4">
              <ul className="space-y-2">
                {prognosis.top_features.map((feature, idx) => (
                  <li key={idx} className="flex items-start">
                    <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-purple-100 text-purple-700 text-sm font-semibold mr-3 flex-shrink-0">
                      {idx + 1}
                    </span>
                    <span className="text-gray-800">{formatFieldName(feature)}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {/* Error (should rarely appear since parent handles API errors, but safe to keep) */}
        {prognosis.error && (
          <div className="bg-red-50 border border-red-300 rounded-lg p-4">
            <h3 className="text-lg font-semibold text-red-900 mb-2">❌ Error</h3>
            <p className="text-red-800">{prognosis.error}</p>
          </div>
        )}

        {/* Disclaimer */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-sm text-blue-900">
            <strong>⚕️ Clinical Note:</strong> This prediction is a statistical estimate and should be used as one component of broader clinical assessment.
          </p>
        </div>

        {/* Reset Button */}
        <div className="pt-4 border-t border-gray-200">
          <button
            className="w-full sm:w-auto px-6 py-2 bg-purple-600 text-white rounded-lg font-medium hover:bg-purple-700 transition-colors shadow-sm"
            onClick={onReset}
          >
            🔄 New Prognosis
          </button>
        </div>
      </div>
    </div>
  );
}