"use client";

import { Button } from "@/components/ui/button";
import { AlertCircle } from "lucide-react";

interface ErrorMessageProps {
  message?: string;
  details?: string;
  onRetry?: () => void;
}

export default function ErrorMessage({
  message = "Something went wrong.",
  details,
  onRetry,
}: ErrorMessageProps) {
  return (
    <div className="w-full flex flex-col items-center text-center p-6 border border-red-300 bg-red-50 rounded-xl">
      <AlertCircle className="h-8 w-8 text-red-500 mb-3" />

      <p className="text-red-700 font-semibold">{message}</p>

      {details && (
        <p className="text-sm text-red-600 mt-1 whitespace-pre-line">{details}</p>
      )}

      {onRetry && (
        <Button onClick={onRetry} variant="outline" className="mt-4">
          Try Again
        </Button>
      )}
    </div>
  );
}
