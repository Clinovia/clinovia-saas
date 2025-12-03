"use client";

import { EchonetEFOutput } from "@/features/cardiology/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type Props = {
  output?: EchonetEFOutput;
  onReset?: () => void; 
};

export default function EFResult({ output }: Props) {
  if (!output) {
    return (
      <div className="p-4 border rounded bg-gray-50 mt-4 animate-pulse">
        <div className="h-4 bg-gray-300 rounded w-1/3 mb-3"></div>
        <div className="space-y-2">
          <div className="h-3 bg-gray-200 rounded"></div>
          <div className="h-3 bg-gray-200 rounded w-2/3"></div>
          <div className="h-3 bg-gray-200 rounded w-1/2"></div>
        </div>
      </div>
    );
  }

  return (
    <Card className="mt-4">
      <CardHeader>
        <CardTitle>EF Prediction Result</CardTitle>
      </CardHeader>
      <CardContent>
        <p>
          <strong>Ejection Fraction:</strong> {output.ef_percent?.toFixed(1)}%
        </p>
        <p>
          <strong>Category:</strong> {output.category}
        </p>
        <p>
          <strong>Model:</strong> {output.model_name} v{output.model_version}
        </p>
      </CardContent>
    </Card>
  );
}
