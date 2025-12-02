import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

/**
 * Token refresh API route
 * POST /api/auth/refresh
 */
export async function POST(request: NextRequest) {
  try {
    // Get refresh token from cookies
    const refreshToken = cookies().get('refresh_token')?.value;

    if (!refreshToken) {
      return NextResponse.json(
        { error: 'No refresh token found' },
        { status: 401 }
      );
    }

    // Call your backend API to refresh token
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const response = await fetch(`${backendUrl}/api/v1/auth/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });

    const data = await response.json();

    // Handle refresh failure
    if (!response.ok) {
      // Clear cookies on refresh failure
      cookies().delete('auth_token');
      cookies().delete('refresh_token');

      return NextResponse.json(
        { 
          error: data.message || 'Token refresh failed',
          details: data.details 
        },
        { status: response.status }
      );
    }

    // Update access token cookie
    cookies().set('auth_token', data.access_token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: 60 * 60 * 24 * 7, // 7 days
      path: '/',
    });

    // Update refresh token if backend provides a new one
    if (data.refresh_token) {
      cookies().set('refresh_token', data.refresh_token, {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'lax',
        maxAge: 60 * 60 * 24 * 30, // 30 days
        path: '/',
      });
    }

    return NextResponse.json({
      success: true,
      message: 'Token refreshed successfully',
    }, { status: 200 });

  } catch (error) {
    console.error('Token refresh error:', error);
    
    // Clear cookies on error
    cookies().delete('auth_token');
    cookies().delete('refresh_token');
    
    return NextResponse.json(
      { 
        error: 'An error occurred during token refresh',
        details: process.env.NODE_ENV === 'development' ? String(error) : undefined
      },
      { status: 500 }
    );
  }
}

/**
 * GET handler to check if refresh token is valid
 * GET /api/auth/refresh
 */
export async function GET() {
  try {
    const refreshToken = cookies().get('refresh_token')?.value;
    const authToken = cookies().get('auth_token')?.value;

    return NextResponse.json({
      hasRefreshToken: !!refreshToken,
      hasAuthToken: !!authToken,
    }, { status: 200 });

  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to check token status' },
      { status: 500 }
    );
  }
}

/**
 * OPTIONS handler for CORS
 */
export async function OPTIONS() {
  return NextResponse.json({}, { status: 200 });
}