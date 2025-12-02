// app/cardiology/layout.tsx
// NOTE: 🚫 Do NOT use "use client" here — layouts should be server components.

import Sidebar from "@/components/layout/Sidebar";

export default function CardiologyLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 p-6">{children}</main>
    </div>
  );
}
