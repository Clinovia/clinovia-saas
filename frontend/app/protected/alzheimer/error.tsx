'use client';

import { useEffect } from 'react';
import { AlertTriangle, RefreshCcw, Home, Brain } from 'lucide-react';
import Link from 'next/link';
import { ROUTES } from '@/config';

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function AlzheimerError({ error, reset }: ErrorProps) {
  useEffect(() => {
    // Log error to error reporting service
    console.error('Alzheimer module error:', error);
  }, [error]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 p-6">
      <div className="w-full max-w-2xl">
        <div className="rounded-lg bg-white p-8 shadow-xl">
          {/* Error Icon with Module Color */}
          <div className="mb-6 flex justify-center">
            <div className="relative">
              <div className="rounded-full bg-purple-100 p-4">
                <Brain className="h-16 w-16 text-purple-600" />
              </div>
              <div className="absolute -bottom-2 -right-2 rounded-full bg-red-100 p-2">
                <AlertTriangle className="h-6 w-6 text-red-600" />
              </div>
            </div>
          </div>

          {/* Error Title */}
          <h1 className="mb-2 text-center text-2xl font-bold text-gray-900">
            Alzheimer's Module Error
          </h1>

          {/* Error Description */}
          <p className="mb-6 text-center text-gray-600">
            We encountered an issue loading the Alzheimer's assessment tools. Please try again or
            return to the dashboard.
          </p>

          {/* Error Details (development only) */}
          {process.env.NODE_ENV === 'development' && (
            <div className="mb-6 rounded-lg bg-gray-50 p-4">
              <p className="mb-2 text-sm font-semibold text-gray-700">Error details:</p>
              <pre className="overflow-x-auto whitespace-pre-wrap break-words text-xs text-gray-600">
                {error.message}
              </pre>
              {error.digest && (
                <p className="mt-2 text-xs text-gray-500">Error ID: {error.digest}</p>
              )}
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex flex-col gap-3 sm:flex-row">
            <button
              onClick={reset}
              className="flex flex-1 items-center justify-center gap-2 rounded-md bg-purple-600 px-4 py-3 text-sm font-semibold text-white transition-colors hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2"
            >
              <RefreshCcw className="h-4 w-4" />
              Try Again
            </button>

            <Link
              href={ROUTES.DASHBOARD.DASHBOARD}
              className="flex flex-1 items-center justify-center gap-2 rounded-md border border-gray-300 bg-white px-4 py-3 text-sm font-semibold text-gray-700 transition-colors hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
            >
              <Home className="h-4 w-4" />
              Go to Dashboard
            </Link>
          </div>

          {/* Alternative Actions */}
          <div className="mt-6 border-t pt-6">
            <p className="mb-3 text-center text-sm font-medium text-gray-700">
              Or try another module:
            </p>
            <div className="flex flex-col gap-2 sm:flex-row sm:justify-center">
              <Link
                href={ROUTES.CARDIOLOGY.BASE}
                className="inline-flex items-center justify-center gap-2 rounded-md bg-red-50 px-4 py-2 text-sm font-medium text-red-700 transition-colors hover:bg-red-100"
              >
                Cardiology Module
              </Link>
              <Link
                href={ROUTES.DASHBOARD.REPORTS}
                className="inline-flex items-center justify-center gap-2 rounded-md bg-blue-50 px-4 py-2 text-sm font-medium text-blue-700 transition-colors hover:bg-blue-100"
              >
                View Reports
              </Link>
            </div>
          </div>

          {/* Support Link */}
          <p className="mt-6 text-center text-sm text-gray-500">
            Need help?{' '}
            <a href="/support" className="font-medium text-purple-600 hover:text-purple-700">
              Contact Support
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}