export default function AlzheimerLoading() {
  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="mx-auto max-w-7xl">
        {/* Header Skeleton */}
        <div className="mb-8 animate-pulse">
          <div className="mb-2 h-8 w-64 rounded-lg bg-gray-200"></div>
          <div className="h-4 w-96 rounded bg-gray-200"></div>
        </div>

        {/* Module Cards Grid Skeleton */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {[...Array(6)].map((_, i) => (
            <div
              key={i}
              className="animate-pulse rounded-lg border border-gray-200 bg-white p-6 shadow-sm"
            >
              {/* Icon */}
              <div className="mb-4 h-12 w-12 rounded-lg bg-purple-100"></div>
              
              {/* Title */}
              <div className="mb-2 h-6 w-3/4 rounded bg-gray-200"></div>
              
              {/* Description */}
              <div className="space-y-2">
                <div className="h-4 w-full rounded bg-gray-200"></div>
                <div className="h-4 w-5/6 rounded bg-gray-200"></div>
              </div>
              
              {/* Button */}
              <div className="mt-4 h-10 w-full rounded-md bg-gray-200"></div>
            </div>
          ))}
        </div>

        {/* Info Section Skeleton */}
        <div className="mt-8 animate-pulse rounded-lg border border-gray-200 bg-white p-6">
          <div className="mb-4 h-6 w-48 rounded bg-gray-200"></div>
          <div className="space-y-2">
            <div className="h-4 w-full rounded bg-gray-200"></div>
            <div className="h-4 w-full rounded bg-gray-200"></div>
            <div className="h-4 w-3/4 rounded bg-gray-200"></div>
          </div>
        </div>
      </div>
    </div>
  );
}