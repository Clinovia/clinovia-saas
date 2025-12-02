'use client';

import { useEffect } from 'react';
import { AlertCircle, RefreshCcw, Home } from 'lucide-react';

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function Error({ error, reset }: ErrorProps) {
  useEffect(() => {
    // Log error to error reporting service
    console.error('Application error:', error);
  }, [error]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-red-50 to-orange-50 p-4">
      <div className="w-full max-w-md">
        <div className="rounded-lg bg-white p-8 shadow-xl">
          {/* Error icon */}
          <div className="mb-6 flex justify-center">
            <div className="rounded-full bg-red-100 p-3">
              <AlertCircle className="h-12 w-12 text-red-600" />
            </div>
          </div>

          {/* Error title */}
          <h1 className="mb-2 text-center text-2xl font-bold text-gray-900">
            Something went wrong
          </h1>

          {/* Error description */}
          <p className="mb-6 text-center text-gray-600">
            We encountered an unexpected error. Please try again or contact support if the problem persists.
          </p>

          {/* Error details (development only) */}
          {process.env.NODE_ENV === 'development' && (
            <div className="mb-6 rounded-md bg-gray-50 p-4">
              <p className="mb-2 text-sm font-semibold text-gray-700">Error details:</p>
              <pre className="overflow-x-auto text-xs text-gray-600">
                {error.message}
              </pre>
              {error.digest && (
                <p className="mt-2 text-xs text-gray-500">
                  Error ID: {error.digest}
                </p>
              )}
            </div>
          )}

          {/* Action buttons */}
          <div className="flex flex-col gap-3 sm:flex-row">
            <button
              onClick={reset}
              className="flex flex-1 items-center justify-center gap-2 rounded-md bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              <RefreshCcw className="h-4 w-4" />
              Try again
            </button>
            
            <a
              href="/"
              className="flex flex-1 items-center justify-center gap-2 rounded-md border border-gray-300 bg-white px-4 py-2.5 text-sm font-semibold text-gray-700 transition-colors hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
            >
              <Home className="h-4 w-4" />
              Go home
            </a>
          </div>

          {/* Support link */}
          <p className="mt-6 text-center text-sm text-gray-500">
            Need help?{' '}
            <a
              href="/support"
              className="font-medium text-blue-600 hover:text-blue-700"
            >
              Contact support
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}