import { useState, useEffect, useCallback } from 'react';

interface UseAsyncState<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
}

interface UseAsyncReturn<T> extends UseAsyncState<T> {
  execute: () => Promise<void>;
  reset: () => void;
}

/**
 * Custom hook for handling async operations
 * Manages loading, error, and data states
 * 
 * @param asyncFunction - Async function to execute
 * @param immediate - Execute immediately on mount (default: true)
 * @returns Object with data, loading, error states and control functions
 * 
 * @example
 * const { data, loading, error, execute } = useAsync(
 *   async () => {
 *     const response = await fetch('/api/data');
 *     return response.json();
 *   },
 *   true // Execute on mount
 * );
 */
export function useAsync<T>(
  asyncFunction: () => Promise<T>,
  immediate: boolean = true
): UseAsyncReturn<T> {
  const [state, setState] = useState<UseAsyncState<T>>({
    data: null,
    loading: immediate,
    error: null,
  });

  /**
   * Execute the async function
   */
  const execute = useCallback(async () => {
    setState({ data: null, loading: true, error: null });

    try {
      const response = await asyncFunction();
      setState({ data: response, loading: false, error: null });
    } catch (error) {
      setState({ 
        data: null, 
        loading: false, 
        error: error instanceof Error ? error : new Error(String(error))
      });
    }
  }, [asyncFunction]);

  /**
   * Reset state to initial values
   */
  const reset = useCallback(() => {
    setState({ data: null, loading: false, error: null });
  }, []);

  // Execute on mount if immediate is true
  useEffect(() => {
    if (immediate) {
      execute();
    }
  }, [execute, immediate]);

  return {
    ...state,
    execute,
    reset,
  };
}

/**
 * Hook for handling async operations with manual trigger
 * Similar to useAsync but doesn't execute immediately
 * 
 * @example
 * const [execute, { data, loading, error }] = useAsyncCallback(
 *   async (id: string) => {
 *     const response = await fetch(`/api/data/${id}`);
 *     return response.json();
 *   }
 * );
 * 
 * // Call with parameters
 * <button onClick={() => execute('123')}>Load Data</button>
 */
export function useAsyncCallback<T, Args extends any[]>(
  asyncFunction: (...args: Args) => Promise<T>
): [(...args: Args) => Promise<void>, UseAsyncState<T>] {
  const [state, setState] = useState<UseAsyncState<T>>({
    data: null,
    loading: false,
    error: null,
  });

  const execute = useCallback(
    async (...args: Args) => {
      setState((prev) => ({ ...prev, loading: true, error: null }));

      try {
        const response = await asyncFunction(...args);
        setState({ data: response, loading: false, error: null });
      } catch (error) {
        setState({ 
          data: null, 
          loading: false, 
          error: error instanceof Error ? error : new Error(String(error))
        });
      }
    },
    [asyncFunction]
  );

  return [execute, state];
}