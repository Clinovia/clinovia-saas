"use client";

import { BPCategoryOutput } from "@/features/cardiology/types";

type Props = {
  output?: BPCategoryOutput;
};

export default function BPCategoryResult({ output }: Props) {
  if (!output) {
    return (
      <div className="p-4 border rounded bg-gray-50 mt-4 animate-pulse">
        <div className="h-4 bg-gray-300 rounded w-1/3 mb-3"></div>
        <div className="space-y-2">
          <div className="h-3 bg-gray-200 rounded"></div>
          <div className="h-3 bg-gray-200 rounded w-1/2"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-4 border rounded bg-gray-50 mt-4">
      <h3 className="font-semibold text-lg mb-2">Blood Pressure Category</h3>
      <p>
        <strong>Category:</strong>{" "}
        <span
          data-testid="bp-category"
          className="font-bold text-blue-600"
        >
          {output.category.replace(/_/g, " ").toUpperCase()}
        </span>
      </p>
      <p>
        <strong>Model:</strong> {output.model_name}
      </p>
    </div>
  );
}
