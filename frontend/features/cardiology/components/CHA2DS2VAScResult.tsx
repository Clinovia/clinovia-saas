"use client";

import { CHA2DS2VAScOutput } from "@/features/cardiology/types";

type Props = {
  output?: CHA2DS2VAScOutput;
};

export default function CHA2DS2VAScResult({ output }: Props) {
    if (!output) {
    return (
      <div className="p-4 border rounded bg-gray-50 mt-4 animate-pulse">
        <div className="h-4 bg-gray-300 rounded w-1/2 mb-3"></div>
        <div className="space-y-2">
          <div className="h-3 bg-gray-200 rounded"></div>
          <div className="h-3 bg-gray-200 rounded w-2/3"></div>
          <div className="h-3 bg-gray-200 rounded w-1/2"></div>
        </div>
      </div>
    );
  }
  return (
    <div className="p-4 border rounded bg-gray-50 mt-4">
      <h3 className="font-semibold text-lg mb-2">CHA₂DS₂-VASc Score</h3>

      <p>
        <strong>Score:</strong> {output.score}
      </p>

      <p>
        <strong>Risk Category:</strong>{" "}
        <span
          className={`font-bold ${
            output.risk_category === "high"
              ? "text-red-600"
              : output.risk_category === "moderate"
              ? "text-yellow-600"
              : "text-green-600"
          }`}
        >
          {output.risk_category.toUpperCase()}
        </span>
      </p>

      <p>
        <strong>Model:</strong> {output.model_name}
      </p>
    </div>
  );
}
