import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// Supported languages
const locales = ['eu', 'en', 'fr', 'nl', 'pt', 'de', 'es'];
const defaultLocale = 'eu';

function getLocale(request: NextRequest) {
  // Check if there is any supported locale in the pathname
  const pathname = request.nextUrl.pathname;
  const pathnameIsMissingLocale = locales.every(
    (locale) => !pathname.startsWith(`/${locale}/`) && pathname !== `/${locale}`
  );

  return pathnameIsMissingLocale ? defaultLocale : null;
}

async function checkMaintenanceMode(request: NextRequest) {
  try {
    // Always check the Django backend for maintenance status
    const backendUrl = 'http://127.0.0.1:8000';
    const response = await fetch(`${backendUrl}/api/v1/core/maintenance-status/`);
    if (response.ok) {
      const data = await response.json();
      return data.maintenance_mode === true;
    }
  } catch (error) {
    // If we can't check maintenance status, assume operational
    console.error('Error checking maintenance mode:', error);
    return false;
  }
  return false;
}

export async function middleware(request: NextRequest) {
  // Check if there is any supported locale in the pathname
  const pathname = request.nextUrl.pathname;
  
  // Skip middleware for static files and API routes
  if (
    pathname.startsWith('/_next/') ||
    pathname.includes('/api/') ||
    pathname.includes('.') ||
    pathname === '/favicon.ico'
  ) {
    return NextResponse.next();
  }

  // Skip maintenance check for admin routes and maintenance page itself
  if (pathname.startsWith('/admin') || pathname === '/maintenance') {
    // Continue with locale handling for admin routes
  } else {
    // Check maintenance mode for public routes
    const isMaintenanceMode = await checkMaintenanceMode(request);
    if (isMaintenanceMode) {
      return NextResponse.redirect(new URL('/maintenance', request.url));
    }
  }

  // Check if the pathname is missing a locale
  const pathnameIsMissingLocale = locales.every(
    (locale) => !pathname.startsWith(`/${locale}/`) && pathname !== `/${locale}`
  );

  // Redirect if there is no locale
  if (pathnameIsMissingLocale) {
    const locale = getLocale(request) || defaultLocale;
    
    // Special case for root path
    if (pathname === '/') {
      return NextResponse.redirect(new URL(`/${locale}`, request.url));
    }
    
    // Add locale to other paths
    return NextResponse.redirect(new URL(`/${locale}${pathname}`, request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    // Skip all internal paths (_next)
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
};