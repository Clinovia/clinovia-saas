import { useState, useCallback, useRef } from "react";

export function useEF() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const abortRef = useRef<AbortController | null>(null);

  const runEF = useCallback(async (file: File) => {
    setLoading(true);
    setError(null);
    setProgress(0);
    setResult(null);

    const controller = new AbortController();
    abortRef.current = controller;

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch("/api/cardiology/ef-prediction", {
        method: "POST",
        body: formData,
        signal: controller.signal,
      });

      if (!res.ok) {
        throw new Error("EF prediction failed.");
      }

      const json = await res.json();
      setResult(json);
    } catch (err: any) {
      if (err.name === "AbortError") {
        setError("Upload canceled.");
      } else {
        setError(err.message || "Unexpected error.");
      }
    } finally {
      setLoading(false);
      setProgress(null);
    }
  }, []);

  const cancel = useCallback(() => {
    if (abortRef.current) {
      abortRef.current.abort();
    }
  }, []);

  return {
    runEF,
    cancel,
    loading,
    progress,
    error,
    result,
  };
}
