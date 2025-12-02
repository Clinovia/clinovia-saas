"use client";

import React from "react";

export type AlzheimerDiagnosisOutput = {
  patient_id?: number | null;
  model_name?: string;
  model_version?: string;
  predicted_class: "CN" | "MCI" | "AD";
  confidence: number;
  probabilities: Record<string, number>;
  top_features?: string[] | null;
};

type Props = {
  result: AlzheimerDiagnosisOutput;
};

export const AlzheimerClassificationResult: React.FC<Props> = ({ result }) => {
  const { patient_id, model_name, model_version, predicted_class, confidence, probabilities, top_features } = result;

  const formatPercentage = (value: number) => (value * 100).toFixed(2) + "%";

  return (
    <div className="bg-white shadow rounded-lg p-6 space-y-4">
      <h2 className="text-xl font-semibold">Alzheimer Classification Result</h2>

      {patient_id && <p><strong>Patient ID:</strong> {patient_id}</p>}
      <p><strong>Model:</strong> {model_name} (v{model_version})</p>

      <div className="mt-2">
        <p>
          <strong>Predicted Class:</strong>{" "}
          <span className={
            predicted_class === "AD" ? "text-red-600" :
            predicted_class === "MCI" ? "text-yellow-600" : "text-green-600"
          }>
            {predicted_class}
          </span>
        </p>
        <p><strong>Confidence:</strong> {formatPercentage(confidence)}</p>
      </div>

      <div className="mt-2">
        <h3 className="font-medium">Class Probabilities:</h3>
        <ul className="list-disc list-inside">
          {Object.entries(probabilities).map(([cls, prob]) => (
            <li key={cls}>
              {cls}: {formatPercentage(prob)}
            </li>
          ))}
        </ul>
      </div>

      {top_features && top_features.length > 0 && (
        <div className="mt-2">
          <h3 className="font-medium">Top Features:</h3>
          <ul className="list-disc list-inside">
            {top_features.map((feature, idx) => (
              <li key={idx}>{feature}</li>
            ))}
          </ul>
        </div>
      )}

      <p className="text-sm text-gray-500">
        Model: {model_name} (v{model_version})
      </p>
    </div>
  );
};

export default AlzheimerClassificationResult;
