"use client";
import { useState } from "react";
import EFForm from "@/features/cardiology/components/EFForm";
import EFResult from "@/features/cardiology/components/EFResult";
import { EchonetEFInput, EchonetEFOutput } from "@/features/cardiology/types";
import { Info } from "lucide-react";

export default function EFPage() {
  const [result, setResult] = useState<EchonetEFOutput | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);

  const handleSubmit = async (data: EchonetEFInput) => {
    setLoading(true);
    setError(null);
    setResult(null);
    setUploadedFile(data.video_file);

    try {
      const token = localStorage.getItem("accessToken");
      if (!token) throw new Error("You must be logged in to use this module.");

      const formData = new FormData();
      formData.append("video", data.video_file);

      const response = await fetch("/api/v1/cardiology/ejection-fraction", {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
        body: formData,
      });

      if (!response.ok) {
        const errText = await response.text();
        let message = `API Error: ${response.statusText}`;
        try {
          const parsed = JSON.parse(errText);
          message = parsed.error || parsed.detail || message;
        } catch {
          message = `${message} - ${errText}`;
        }
        throw new Error(message);
      }

      const json: EchonetEFOutput = await response.json();
      setResult(json);
    } catch (err: any) {
      console.error("EF Prediction Error:", err);
      setError(err.message || "Unknown error occurred.");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setError(null);
    setResult(null);
    setUploadedFile(null);
  };

  return (
    <div className="max-w-5xl mx-auto p-4 space-y-6">
      {/* Header */}
      <h1 className="text-3xl font-bold mb-4">🫀 Ejection Fraction Prediction</h1>
      <p className="text-gray-700 mb-6">
        Upload an echocardiogram video to predict ejection fraction (EF) and clinical severity.
      </p>

      {/* Model Training Notice */}
      <div className="flex gap-3 items-start bg-amber-50 border border-amber-300 rounded-lg p-4">
        <Info className="h-5 w-5 text-amber-700 flex-shrink-0 mt-0.5" />
        <p className="text-sm text-amber-900">
          This model was trained on EchoNet-Dynamic with cleanly curated video files. 
          Unprocessed video files may result in inaccurate results.{" "}
          <strong>Preprocessing workflow is being added.</strong>
        </p>
      </div>

      {/* Form - shows video preview */}
      <EFForm 
        onSubmit={handleSubmit} 
        loading={loading}
        videoFile={uploadedFile}
      />

      {/* Loading */}
      {loading && (
        <div className="flex flex-col items-center justify-center py-10 space-y-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600"></div>
          <p className="text-gray-600 font-medium">Analyzing echocardiogram...</p>
        </div>
      )}

      {/* Error */}
      {error && !loading && (
        <div className="bg-red-50 border border-red-300 rounded-lg p-4">
          <h3 className="text-lg font-semibold text-red-900 mb-2">❌ Error</h3>
          <p className="text-red-800">{error}</p>
          <button
            onClick={handleReset}
            className="mt-3 px-4 py-2 bg-red-600 text-white rounded-lg font-medium hover:bg-red-700 transition"
          >
            Try Again
          </button>
        </div>
      )}

      {/* Result - stacked below the video */}
      {result && !loading && uploadedFile && (
        <EFResult 
          output={result} 
          onReset={handleReset}
        />
      )}

      {/* Info Box */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="text-sm font-semibold text-blue-900 mb-2">ℹ️ About This Tool</h3>
        <div className="text-sm text-blue-800 space-y-2">
          <p>
            This tool uses the EchoNet-Dynamic model to automatically measure left ventricular 
            ejection fraction (LVEF) from echocardiogram videos.
          </p>
          <ul className="list-disc list-inside ml-2 space-y-1">
            <li><strong>Normal:</strong> EF ≥ 50%</li>
            <li><strong>Mildly Reduced:</strong> 40–49%</li>
            <li><strong>Moderately Reduced:</strong> 30–39%</li>
            <li><strong>Severely Reduced:</strong> &lt; 30%</li>
          </ul>
        </div>
      </div>
      <p className="text-sm text-gray-500 mt-6">
        ⚠️ For research and planning use only. Not a medical device.
      </p>
    </div>
  );
}