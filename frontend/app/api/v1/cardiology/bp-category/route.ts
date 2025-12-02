// frontend/app/api/v1/cardiology/bp-category/route.ts

import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function POST(request: NextRequest) {
  try {
    // ---- Parse JSON body safely ----
    const body = await request.json().catch(() => null);
    if (!body) {
      return NextResponse.json(
        { error: "Invalid JSON body" },
        { status: 400 }
      );
    }

    // ---- Extract JWT token (from client -> API route) ----
    const authHeader = request.headers.get("authorization");
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
    };

    if (authHeader) {
      headers["Authorization"] = authHeader;
    }

    // ---- Forward request to FastAPI ----
    const backendResponse = await fetch(
      `${BACKEND_URL}/api/v1/cardiology/bp-category`,
      {
        method: "POST",
        headers,
        body: JSON.stringify(body),
      }
    );

    // ---- Handle backend errors ----
    const responseData = await backendResponse
      .json()
      .catch(() => ({ detail: "Unknown error" }));

    if (!backendResponse.ok) {
      return NextResponse.json(
        { error: responseData.detail || "Failed to categorize blood pressure" },
        { status: backendResponse.status }
      );
    }

    // ---- Success ----
    return NextResponse.json(responseData, { status: 200 });
  } catch (err: any) {
    console.error("BP Category API Error:", err);

    return NextResponse.json(
      { error: err?.message || "Internal server error" },
      { status: 500 }
    );
  }
}
