"use client";

export default function LoadingSpinner({ size = 32 }: { size?: number }) {
  return (
    <div className="flex justify-center items-center py-8">
      <div
        className="animate-spin rounded-full border-4 border-gray-300 border-t-black"
        style={{ width: size, height: size }}
      />
    </div>
  );
}
