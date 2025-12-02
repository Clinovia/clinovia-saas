// app/api/v1/cardiology/ejection-fraction/route.ts
import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function POST(request: NextRequest) {
  try {
    // ✅ Get FormData (not JSON) because we're uploading a video file
    const formData = await request.formData();
    
    // Get the JWT token from the Authorization header
    const authHeader = request.headers.get("authorization");
    if (!authHeader) {
      return NextResponse.json(
        { error: "Missing Authorization header" },
        { status: 401 }
      );
    }

    // Forward the request to the FastAPI backend
    const backendUrl = `${BACKEND_URL}/api/v1/cardiology/ejection-fraction`;
    console.log("Forwarding EF request to:", backendUrl);

    // ✅ Fixed: Use parenthesis, not backtick
    const response = await fetch(backendUrl, {
      method: "POST",
      headers: {
        "Authorization": authHeader,
        // ✅ Don't set Content-Type - fetch automatically sets it with boundary for FormData
      },
      body: formData, // ✅ Send FormData directly, not JSON
    });

    console.log("Backend response status:", response.status);
    
    // Get the response as text first for debugging
    const responseText = await response.text();
    console.log("Backend response (first 500 chars):", responseText.substring(0, 500));

    if (!response.ok) {
      console.error("Backend error response:", responseText);
      
      // Try to parse error as JSON
      try {
        const errorData = JSON.parse(responseText);
        return NextResponse.json(
          { error: errorData.detail || errorData.error || "Failed to predict ejection fraction" },
          { status: response.status }
        );
      } catch {
        return NextResponse.json(
          { error: `Backend error: ${responseText}` },
          { status: response.status }
        );
      }
    }

    // Check if response is empty
    if (!responseText || responseText.trim().length === 0) {
      console.error("Backend returned empty response");
      return NextResponse.json(
        { error: "Backend returned empty response" },
        { status: 500 }
      );
    }

    // Parse successful response
    try {
      const data = JSON.parse(responseText);
      return NextResponse.json(data, { status: 200 });
    } catch (parseError: any) {
      console.error("Failed to parse backend response:", parseError.message);
      console.error("Response text:", responseText);
      return NextResponse.json(
        { 
          error: "Invalid JSON from backend", 
          details: parseError.message,
          response: responseText.substring(0, 200)
        },
        { status: 500 }
      );
    }

  } catch (error: any) {
    console.error("EF Prediction API Error:", error);
    return NextResponse.json(
      { 
        error: error.message || "Internal server error",
        stack: process.env.NODE_ENV === "development" ? error.stack : undefined
      },
      { status: 500 }
    );
  }
}