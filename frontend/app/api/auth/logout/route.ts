import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

/**
 * Logout API route
 * POST /api/auth/logout
 */
export async function POST(request: NextRequest) {
  try {
    const authToken = cookies().get('auth_token')?.value;

    // Optional: Call backend to invalidate token server-side
    if (authToken) {
      const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      
      try {
        await fetch(`${backendUrl}/api/v1/auth/logout`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`,
          },
        });
      } catch (error) {
        // Continue with logout even if backend call fails
        console.error('Backend logout failed:', error);
      }
    }

    // Clear authentication cookies
    cookies().delete('auth_token');
    cookies().delete('refresh_token');

    return NextResponse.json({
      success: true,
      message: 'Logged out successfully',
    }, { status: 200 });

  } catch (error) {
    console.error('Logout error:', error);
    
    // Still clear cookies even on error
    cookies().delete('auth_token');
    cookies().delete('refresh_token');
    
    return NextResponse.json(
      { 
        success: true,
        message: 'Logged out with errors',
        details: process.env.NODE_ENV === 'development' ? String(error) : undefined
      },
      { status: 200 }
    );
  }
}

/**
 * OPTIONS handler for CORS
 */
export async function OPTIONS() {
  return NextResponse.json({}, { status: 200 });
}