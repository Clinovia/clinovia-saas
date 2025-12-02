"use client";

import { ReactNode, useEffect } from "react";
import { useRouter } from "next/navigation";

interface ProtectedLayoutProps {
  children: ReactNode;
}

export default function ProtectedLayout({ children }: ProtectedLayoutProps) {
  const router = useRouter();

  // Check authentication
  useEffect(() => {
    const token = localStorage.getItem("accessToken"); // consistent key
    if (!token) {
      router.push("/auth/login");
    }
  }, [router]);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Do NOT include <Navbar /> here */}
      {children}
    </div>
  );
}
