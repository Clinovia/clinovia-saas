// frontend/features/cardiology/ECGInterpreterResult.tsx
import React from "react";
import { ECGInterpreterInput, ECGInterpreterOutput } from "@/features/cardiology/types";

interface Props {
  input: ECGInterpreterInput;
  interpretation: ECGInterpreterOutput;
  onReset: () => void;
}

export default function ECGInterpreterResult({ input, interpretation, onReset }: Props) {
  // Helper to format field names nicely
  const formatFieldName = (key: string): string => {
    return key
      .replace(/_/g, " ")
      .replace(/\b\w/g, (char) => char.toUpperCase());
  };

  // Helper to format values
  const formatValue = (value: any): string => {
    if (value === null || value === undefined) return "N/A";
    if (typeof value === "boolean") return value ? "Yes" : "No";
    if (Array.isArray(value)) return value.length > 0 ? value.join(", ") : "None";
    return String(value);
  };

  // Get risk badge color
  const getRiskColor = (risk: string): string => {
    const riskLower = risk.toLowerCase();
    if (riskLower === "routine" || riskLower === "low") return "bg-green-100 text-green-800";
    if (riskLower === "moderate" || riskLower === "medium") return "bg-yellow-100 text-yellow-800";
    if (riskLower === "high" || riskLower === "urgent") return "bg-red-100 text-red-800";
    return "bg-gray-100 text-gray-800";
  };

  return (
    <div className="mt-6 border border-gray-200 rounded-lg bg-white shadow-sm">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 px-6 py-4 border-b border-gray-200 rounded-t-lg">
        <h2 className="text-2xl font-bold text-gray-800">📊 ECG Interpretation Result</h2>
        <p className="text-sm text-gray-600 mt-1">
          Model: {interpretation.model_name || "N/A"} (v{interpretation.model_version || "1.0.0"})
        </p>
      </div>

      <div className="p-6 space-y-6">
        {/* Key Findings Section */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h3 className="text-lg font-semibold text-blue-900 mb-3">🔍 Key Findings</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Rhythm */}
            <div>
              <p className="text-sm font-medium text-gray-600">Rhythm</p>
              <p className="text-lg font-semibold text-gray-900 capitalize">
                {interpretation.rhythm || "N/A"}
              </p>
            </div>

            {/* Overall Risk */}
            <div>
              <p className="text-sm font-medium text-gray-600">Overall Risk</p>
              <span className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${getRiskColor(interpretation.overall_risk || "routine")}`}>
                {formatFieldName(interpretation.overall_risk || "routine")}
              </span>
            </div>
          </div>

          {/* Findings List */}
          <div className="mt-4">
            <p className="text-sm font-medium text-gray-600 mb-2">Clinical Findings</p>
            {interpretation.findings && interpretation.findings.length > 0 ? (
              <ul className="list-disc list-inside space-y-1">
                {interpretation.findings.map((finding, idx) => (
                  <li key={idx} className="text-gray-800 capitalize">
                    {finding}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500 italic">No specific findings</p>
            )}
          </div>
        </div>

        {/* Input Parameters Section */}
        <div>
          <h3 className="text-lg font-semibold text-gray-800 mb-3">📋 Input Parameters</h3>
          <div className="bg-gray-50 rounded-lg p-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            <div className="bg-white p-3 rounded border border-gray-200">
              <p className="text-xs text-gray-500">Heart Rate</p>
              <p className="text-lg font-semibold text-gray-900">{input.heart_rate} bpm</p>
            </div>
            
            <div className="bg-white p-3 rounded border border-gray-200">
              <p className="text-xs text-gray-500">QRS Duration</p>
              <p className="text-lg font-semibold text-gray-900">{input.qrs_duration} ms</p>
            </div>
            
            <div className="bg-white p-3 rounded border border-gray-200">
              <p className="text-xs text-gray-500">QT Interval</p>
              <p className="text-lg font-semibold text-gray-900">{input.qt_interval} ms</p>
            </div>
            
            <div className="bg-white p-3 rounded border border-gray-200">
              <p className="text-xs text-gray-500">PR Interval</p>
              <p className="text-lg font-semibold text-gray-900">{input.pr_interval} ms</p>
            </div>
            
            <div className="bg-white p-3 rounded border border-gray-200">
              <p className="text-xs text-gray-500">Rhythm</p>
              <p className="text-lg font-semibold text-gray-900 capitalize">{input.rhythm}</p>
            </div>
            
            <div className="bg-white p-3 rounded border border-gray-200">
              <p className="text-xs text-gray-500">ST Elevation</p>
              <p className="text-lg font-semibold text-gray-900">
                {input.st_elevation ? "✓ Yes" : "✗ No"}
              </p>
            </div>
            
            <div className="bg-white p-3 rounded border border-gray-200">
              <p className="text-xs text-gray-500">T-Wave Inversion</p>
              <p className="text-lg font-semibold text-gray-900">
                {input.t_wave_inversion ? "✓ Yes" : "✗ No"}
              </p>
            </div>
          </div>
        </div>

        {/* Warnings Section (if any) */}
        {interpretation.warnings && interpretation.warnings.length > 0 && (
          <div className="bg-yellow-50 border border-yellow-300 rounded-lg p-4">
            <h3 className="text-lg font-semibold text-yellow-900 mb-2">⚠️ Warnings</h3>
            <ul className="list-disc list-inside space-y-1">
              {interpretation.warnings.map((warning, idx) => (
                <li key={idx} className="text-yellow-800">{warning}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Error Section (if any) */}
        {interpretation.error && (
          <div className="bg-red-50 border border-red-300 rounded-lg p-4">
            <h3 className="text-lg font-semibold text-red-900 mb-2">❌ Error</h3>
            <p className="text-red-800">{interpretation.error}</p>
          </div>
        )}

        {/* Metadata Section */}
        <div className="text-xs text-gray-500 space-y-1 pt-4 border-t border-gray-200">
          <p><strong>Prediction ID:</strong> {interpretation.prediction_id || "N/A"}</p>
          <p><strong>Status:</strong> {interpretation.status || "N/A"}</p>
          {interpretation.timestamp && (
            <p><strong>Timestamp:</strong> {new Date(interpretation.timestamp).toLocaleString()}</p>
          )}
          {interpretation.confidence_interval && (
            <p><strong>Confidence Interval:</strong> {JSON.stringify(interpretation.confidence_interval)}</p>
          )}
        </div>

        {/* Reset Button */}
        <div className="pt-4 border-t border-gray-200">
          <button
            className="w-full sm:w-auto px-6 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors shadow-sm"
            onClick={onReset}
          >
            🔄 New Interpretation
          </button>
        </div>
      </div>
    </div>
  );
}