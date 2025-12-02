"use client";
import { AlzheimerRiskScreenerOutput } from "@/features/alzheimer/types";

type Props = {
  output: AlzheimerRiskScreenerOutput;
};

export default function AlzheimerRiskResult({ output }: Props) {
  // Capitalize first letter for display
  const displayRiskLevel =
    output.risk_category.charAt(0).toUpperCase() + output.risk_category.slice(1);

  // Helper function to get risk color
  const getRiskColor = (category: string) => {
    switch (category.toLowerCase()) {
      case "high":
        return "text-red-600";
      case "moderate":
        return "text-yellow-600";
      case "low":
        return "text-green-600";
      default:
        return "text-gray-600";
    }
  };

  return (
    <div className="space-y-4 mt-4">
      <div className="p-4 border rounded bg-gray-50">
        <h3 className="font-semibold text-lg mb-2">Risk Assessment Result</h3>

        <div className="mb-2">
          <strong>Risk Level:</strong>{" "}
          <span className={`font-bold ${getRiskColor(output.risk_category)}`}>
            {displayRiskLevel}
          </span>
        </div>

        <div>
          <strong>Recommendation:</strong>{" "}
          {output.recommendation ? output.recommendation : ""}
        </div>
      </div>

            {/* Model Info */}
      <p className="text-sm text-gray-500">
        Model: {output.model_name} (v{output.model_version})
      </p>
    </div>
  );
}
