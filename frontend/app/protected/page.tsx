"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";

export default function ProtectedDashboard() {
  const router = useRouter();

  // Authentication check
  useEffect(() => {
    const token = localStorage.getItem("accessToken"); // use consistent token name
    if (!token) {
      router.push("/login"); // redirect to login page
    }
  }, [router]);

  return (
    <div className="container mx-auto py-16 px-4">
      <h1 className="text-3xl font-bold mb-8">Welcome to the Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        {/* Cardiology */}
        <Link href="/protected/cardiology" className="no-underline">
          <Card className="hover:shadow-xl transition-shadow cursor-pointer">
            <CardHeader>
              <CardTitle>Cardiology</CardTitle>
              <CardDescription>
                Access cardiology modules and resources.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p>Explore ASCVD, EF prediction, BP categories, and more.</p>
            </CardContent>
          </Card>
        </Link>

        {/* Neurology */}
        <Link href="/protected/alzheimer" className="no-underline">
          <Card className="hover:shadow-xl transition-shadow cursor-pointer">
            <CardHeader>
              <CardTitle>Neurology</CardTitle>
              <CardDescription>
                Access neurology modules and resources.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p>Explore stroke, epilepsy, and other neurology topics.</p>
            </CardContent>
          </Card>
        </Link>

      </div>
    </div>
  );
}
