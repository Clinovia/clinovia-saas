"use client";

import { ASCVDOutput } from "@/features/cardiology/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type Props = {
  output?: ASCVDOutput;
};

export default function ASCVDResult({ output }: Props) {
  if (!output) {
    return (
      <Card className="mt-4 animate-pulse">
        <CardContent className="space-y-2">
          <div className="h-4 bg-gray-300 rounded w-1/3 mb-3"></div>
          <div className="space-y-2">
            <div className="h-3 bg-gray-200 rounded"></div>
            <div className="h-3 bg-gray-200 rounded w-2/3"></div>
            <div className="h-3 bg-gray-200 rounded w-1/2"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  const categoryColor = {
    high: "text-red-600",
    intermediate: "text-yellow-600",
    borderline: "text-orange-600",
    low: "text-green-600",
  }[output.risk_category] || "text-gray-600";

  return (
    <Card className="mt-4">
      <CardHeader>
        <CardTitle>ASCVD Risk Result</CardTitle>
      </CardHeader>
      <CardContent className="space-y-2">
        <p>
          <strong>Risk Percentage:</strong> {output.risk_percentage.toFixed(1)}%
        </p>
        <p>
          <strong>Risk Category:</strong>{" "}
          <span className={`font-bold ${categoryColor}`}>
            {output.risk_category.toUpperCase()}
          </span>
        </p>
        <p>
          <strong>Model:</strong> {output.model_name}
        </p>
      </CardContent>
    </Card>
  );
}
