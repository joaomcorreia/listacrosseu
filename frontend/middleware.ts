import { NextRequest, NextResponse } from 'next/server';

// All supported locales (27 EU languages)
const locales = [
  'en', 'es', 'fr', 'de', 'nl', 'pt', 'it', 'pl', 'cs', 'sk', 
  'hu', 'ro', 'bg', 'hr', 'sl', 'et', 'lv', 'lt', 'mt', 'cy',
  'fi', 'se', 'da', 'no', 'is', 'ie', 'lu'
];

const defaultLocale = 'en';

// Get locale from pathname
function getLocaleFromPathname(pathname: string): string | null {
  const segments = pathname.split('/').filter(Boolean);
  const firstSegment = segments[0];
  return locales.includes(firstSegment) ? firstSegment : null;
}

// Detect browser language
function detectBrowserLanguage(request: NextRequest): string {
  const acceptLanguage = request.headers.get('accept-language');
  if (!acceptLanguage) return defaultLocale;

  // Parse Accept-Language header
  const languages = acceptLanguage
    .split(',')
    .map(lang => {
      const [code, quality = '1'] = lang.trim().split(';q=');
      return { code: code.split('-')[0], quality: parseFloat(quality) };
    })
    .sort((a, b) => b.quality - a.quality);

  // Find first supported language
  for (const { code } of languages) {
    if (locales.includes(code)) {
      return code;
    }
  }

  return defaultLocale;
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  
  // Skip middleware for API routes, static files, and admin
  if (
    pathname.startsWith('/api/') ||
    pathname.startsWith('/_next/') ||
    pathname.startsWith('/admin/') ||
    pathname.includes('.') ||
    pathname === '/favicon.ico'
  ) {
    return NextResponse.next();
  }

  const currentLocale = getLocaleFromPathname(pathname);
  
  // If no locale in URL, redirect to localized version
  if (!currentLocale) {
    // Check for saved language preference
    const savedLocale = request.cookies.get('preferred-locale')?.value;
    
    let targetLocale = defaultLocale;
    
    if (savedLocale && locales.includes(savedLocale)) {
      // Use saved preference
      targetLocale = savedLocale;
    } else if (!request.cookies.has('locale-detected')) {
      // First visit - detect browser language
      targetLocale = detectBrowserLanguage(request);
    }
    
    const url = request.nextUrl.clone();
    url.pathname = `/${targetLocale}${pathname}`;
    
    const response = NextResponse.redirect(url);
    
    // Set cookies to remember preferences
    response.cookies.set('preferred-locale', targetLocale, {
      maxAge: 60 * 60 * 24 * 365, // 1 year
      path: '/',
    });
    
    response.cookies.set('locale-detected', 'true', {
      maxAge: 60 * 60 * 24 * 365, // 1 year
      path: '/',
    });
    
    return response;
  }
  
  // Update preferred locale cookie if user changed language manually
  const savedLocale = request.cookies.get('preferred-locale')?.value;
  if (currentLocale !== savedLocale) {
    const response = NextResponse.next();
    response.cookies.set('preferred-locale', currentLocale, {
      maxAge: 60 * 60 * 24 * 365, // 1 year
      path: '/',
    });
    return response;
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - admin (admin routes)
     */
    '/((?!api|_next/static|_next/image|favicon.ico|admin).*)',
  ],
};