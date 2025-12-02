"use client";
import { useState, useRef } from "react";
import EFResult from "@/features/cardiology/components/EFResult";
import { EchonetEFOutput } from "@/features/cardiology/types";

export default function EFPage() {
  const [result, setResult] = useState<EchonetEFOutput | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [patientId, setPatientId] = useState<string>("");
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const handleSubmit = async (file: File) => {
    setLoading(true);
    setError(null);
    setResult(null);
    setUploadedFile(file);

    try {
      const token = localStorage.getItem("accessToken");
      if (!token) throw new Error("You must be logged in to use this module.");

      const formData = new FormData();
      formData.append("video", file);

      const response = await fetch("/api/v1/cardiology/ejection-fraction", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (!response.ok) {
        const errText = await response.text();
        console.error("Error response:", errText);
        try {
          const errData = JSON.parse(errText);
          throw new Error(errData.error || errData.detail || `API Error: ${response.statusText}`);
        } catch {
          throw new Error(`API Error: ${response.statusText} - ${errText}`);
        }
      }

      const text = await response.text();
      console.log("RAW RESPONSE:", text);
      console.log("Response length:", text.length);
      console.log("First 100 chars:", text.substring(0, 100));

      // Check if response is empty
      if (!text || text.trim().length === 0) {
        throw new Error("Backend returned empty response");
      }

      try {
        const resultData: EchonetEFOutput = JSON.parse(text);
        setResult(resultData);
      } catch (e: any) {
        console.error("JSON parse error:", e);
        console.error("Failed to parse:", text);
        throw new Error(`Invalid JSON response: ${e.message}. Response: ${text.substring(0, 200)}`);
      }
    } catch (err: any) {
      console.error(err);
      setError(err.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    
    const files = e.dataTransfer.files;
    if (files && files[0]) {
      handleSubmit(files[0]);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDragEnter = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files[0]) {
      handleSubmit(files[0]);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
    setPatientId("");
    setUploadedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className="max-w-5xl mx-auto p-4 space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-red-50 to-pink-50 border border-red-200 rounded-lg p-6 shadow-sm">
        <h1 className="text-3xl font-bold text-gray-800">🫀 Ejection Fraction Prediction</h1>
        <p className="text-gray-600 mt-2">
          Upload an echocardiogram video to predict the ejection fraction (EF) and its category using deep learning
        </p>
      </div>

      {/* Form - only show if no result */}
      {!result && (
        <div className="bg-white border border-gray-200 rounded-lg shadow-sm p-6 space-y-4">          
          {/* Drag-and-Drop Zone */}
          <div
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragEnter={handleDragEnter}
            onDragLeave={handleDragLeave}
            onClick={() => !loading && fileInputRef.current?.click()}
            className={`
              border-2 border-dashed rounded-lg p-12 text-center transition-all
              ${loading 
                ? 'border-gray-300 bg-gray-50 cursor-not-allowed' 
                : 'border-red-300 bg-red-50 cursor-pointer hover:border-red-500 hover:bg-red-100'
              }
            `}
          >
            <div className="flex flex-col items-center space-y-3">
              <svg
                className="w-16 h-16 text-red-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                />
              </svg>
              <div>
                <p className="text-lg font-medium text-gray-700">
                  Drop video here or click to upload
                </p>
                <p className="text-sm text-gray-500 mt-1">
                  Supported formats: MP4, AVI, MOV
                </p>
              </div>
            </div>
          </div>

          {/* Hidden File Input */}
          <input
            type="file"
            accept="video/*"
            ref={fileInputRef}
            className="hidden"
            onChange={handleFileSelect}
            disabled={loading}
          />
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="flex flex-col items-center justify-center py-12 space-y-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600"></div>
          <p className="text-gray-600 font-medium">Analyzing echocardiogram video...</p>
          <p className="text-gray-500 text-sm">This may take a moment</p>
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
      {result && !loading && uploadedFile && (
        <EFResult 
          output={result} 
          videoFile={uploadedFile}
          onReset={handleReset}
        />
      )}

      {/* Info Box */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="text-sm font-semibold text-blue-900 mb-2">ℹ️ About This Tool</h3>
        <div className="text-sm text-blue-800 space-y-2">
          <p>
            This tool uses EchoNet-Dynamic deep learning model to automatically measure left ventricular 
            ejection fraction (LVEF) from echocardiogram videos.
          </p>
          <p className="font-medium">
            <strong>Clinical Categories:</strong>
          </p>
          <ul className="list-disc list-inside ml-2 space-y-1">
            <li><strong>Normal:</strong> EF ≥ 50% - Normal left ventricular function</li>
            <li><strong>Mild:</strong> 40-49% - Mildly reduced function</li>
            <li><strong>Moderate:</strong> 30-39% - Moderately reduced function</li>
            <li><strong>Severe:</strong> &lt; 30% - Severely reduced function</li>
          </ul>
        </div>
      </div>
    </div>
  );
}