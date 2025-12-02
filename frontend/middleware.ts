import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// Define route types
const publicRoutes = ['/', '/explore'];
const authRoutes = ['/login', '/signup', '/forgot-password'];
const protectedRoutes = ['/alzheimer', '/cardiology', '/protected'];

/**
 * Middleware to handle authentication and route protection
 */
export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  
  // Get auth token from cookies
  const token = request.cookies.get('auth_token')?.value;
  const isAuthenticated = !!token;

  // Check if current path is public
  const isPublicRoute = publicRoutes.some(route => 
    pathname === route || pathname.startsWith(`${route}/`)
  );

  // Check if current path is an auth route
  const isAuthRoute = authRoutes.some(route => 
    pathname === route || pathname.startsWith(`${route}/`)
  );

  // Check if current path is protected
  const isProtectedRoute = protectedRoutes.some(route => 
    pathname.startsWith(route)
  );

  // Allow API routes and static files
  if (
    pathname.startsWith('/api') ||
    pathname.startsWith('/_next') ||
    pathname.startsWith('/static') ||
    pathname.includes('.')
  ) {
    return NextResponse.next();
  }

  // Redirect authenticated users away from auth pages
  if (isAuthRoute && isAuthenticated) {
    return NextResponse.redirect(new URL('/protected', request.url));
  }

  // Redirect unauthenticated users to login
  if (isProtectedRoute && !isAuthenticated) {
    const loginUrl = new URL('/login', request.url);
    // Store the intended destination for post-login redirect
    loginUrl.searchParams.set('redirect', pathname);
    return NextResponse.redirect(loginUrl);
  }

  // Allow public routes
  if (isPublicRoute) {
    return NextResponse.next();
  }

  // For authenticated users accessing protected routes, add user info header
  if (isAuthenticated && isProtectedRoute) {
    const response = NextResponse.next();
    
    // Optional: Add custom headers for debugging/logging
    response.headers.set('x-authenticated', 'true');
    
    return response;
  }

  return NextResponse.next();
}

/**
 * Matcher configuration - defines which routes this middleware runs on
 */
export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public files (images, etc.)
     */
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
};