"use client";
import Link from 'next/link';
import { FileQuestion, ArrowLeft, Home, Search } from 'lucide-react';

export default function NotFound() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-gray-50 to-blue-50 p-4">
      <div className="w-full max-w-2xl">
        <div className="text-center">
          {/* 404 illustration */}
          <div className="mb-8 flex justify-center">
            <div className="relative">
              <div className="text-9xl font-bold text-gray-200">404</div>
              <div className="absolute inset-0 flex items-center justify-center">
                <FileQuestion className="h-24 w-24 text-blue-600" />
              </div>
            </div>
          </div>

          {/* Title */}
          <h1 className="mb-4 text-4xl font-bold text-gray-900">
            Page not found
          </h1>

          {/* Description */}
          <p className="mb-8 text-lg text-gray-600">
            Sorry, we couldn't find the page you're looking for. It might have been moved or doesn't exist.
          </p>

          {/* Action buttons */}
          <div className="flex flex-col gap-4 sm:flex-row sm:justify-center">
            <Link
              href="/"
              className="inline-flex items-center justify-center gap-2 rounded-md bg-blue-600 px-6 py-3 text-sm font-semibold text-white transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              <Home className="h-4 w-4" />
              Back to home
            </Link>

            <button
              onClick={() => window.history.back()}
              className="inline-flex items-center justify-center gap-2 rounded-md border border-gray-300 bg-white px-6 py-3 text-sm font-semibold text-gray-700 transition-colors hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
            >
              <ArrowLeft className="h-4 w-4" />
              Go back
            </button>
          </div>

          {/* Quick links */}
          <div className="mt-12 rounded-lg bg-white p-6 shadow-sm">
            <h2 className="mb-4 flex items-center justify-center gap-2 text-sm font-semibold text-gray-900">
              <Search className="h-4 w-4" />
              Quick links
            </h2>
            <div className="grid gap-3 sm:grid-cols-2">
              <Link
                href="/modules"
                className="rounded-md border border-gray-200 p-3 text-sm text-gray-700 transition-colors hover:border-blue-300 hover:bg-blue-50"
              >
                <span className="font-medium">Modules</span>
                <p className="text-xs text-gray-500">Browse all available modules</p>
              </Link>
              
              <Link
                href="/alzheimer"
                className="rounded-md border border-gray-200 p-3 text-sm text-gray-700 transition-colors hover:border-blue-300 hover:bg-blue-50"
              >
                <span className="font-medium">Alzheimer's</span>
                <p className="text-xs text-gray-500">Diagnosis & prognosis tools</p>
              </Link>
              
              <Link
                href="/cardiology"
                className="rounded-md border border-gray-200 p-3 text-sm text-gray-700 transition-colors hover:border-blue-300 hover:bg-blue-50"
              >
                <span className="font-medium">Cardiology</span>
                <p className="text-xs text-gray-500">Cardiac risk assessment</p>
              </Link>
              
              <Link
                href="/login"
                className="rounded-md border border-gray-200 p-3 text-sm text-gray-700 transition-colors hover:border-blue-300 hover:bg-blue-50"
              >
                <span className="font-medium">Sign in</span>
                <p className="text-xs text-gray-500">Access your account</p>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}