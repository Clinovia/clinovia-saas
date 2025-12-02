"use client";

import { AlzheimerDiagnosisBasicOutput } from "@/features/alzheimer/types";

type Props = {
  output?: AlzheimerDiagnosisBasicOutput;
};

export default function DiagBasicResult({ output }: Props) {
  if (!output) {
    return (
      <div className="p-4 border rounded bg-gray-50 mt-4 animate-pulse space-y-2">
        <div className="h-4 bg-gray-300 rounded w-1/3"></div>
        <div className="h-3 bg-gray-200 rounded"></div>
        <div className="h-3 bg-gray-200 rounded w-2/3"></div>
        <div className="h-3 bg-gray-200 rounded w-1/2"></div>
      </div>
    );
  }

  return (
    <div className="p-4 border rounded bg-gray-50 mt-4 space-y-4">
      <h3 className="font-semibold text-lg">🧠 Alzheimer Diagnosis Result</h3>

      {/* Predicted Class */}
      <p>
        <strong>Predicted Class:</strong>{" "}
        <span
          className={`font-bold ${
            output.predicted_class === "AD"
              ? "text-red-600"
              : output.predicted_class === "MCI"
              ? "text-yellow-600"
              : "text-green-600"
          }`}
        >
          {output.predicted_class}
        </span>
      </p>

      {/* Confidence */}
      <p>
        <strong>Confidence:</strong> {(output.confidence * 100).toFixed(1)}%
      </p>

      {/* Probabilities */}
      <div>
        <strong>Probabilities:</strong>
        <ul className="ml-4 list-disc">
          {Object.entries(output.probabilities).map(([cls, prob]) => (
            <li key={cls}>
              {cls}: {(prob * 100).toFixed(1)}%
            </li>
          ))}
        </ul>
      </div>

      {/* Top Features */}
      {output.top_features && output.top_features.length > 0 && (
        <div>
          <strong>Top Features:</strong>
          <ul className="ml-4 list-disc">
            {output.top_features.map((feat) => (
              <li key={feat}>{feat.replace("_bl", "")}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Model Info */}
      <p className="text-sm text-gray-500">
        Model: {output.model_name} (v{output.model_version})
      </p>
    </div>
  );
}
