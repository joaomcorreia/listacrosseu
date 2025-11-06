// Use direct Django API for server-side rendering, proxy for client-side
const getApiBase = () => {
  const isDev = process.env.NODE_ENV === 'development';
  if (typeof window === 'undefined') {
    // Server-side rendering - use direct Django API
    return isDev ? 'http://127.0.0.1:8000/api/v1' : 'https://your-domain.com/api/v1';
  } else {
    // Client-side - use Next.js proxy
    return '/api/v1';
  }
};

/**
 * Simple fetch wrapper for API calls
 * @param path API endpoint path (e.g., '/blog/posts/')
 * @param init Optional fetch init object
 * @returns JSON response or null on error
 */
export async function apiCall(path: string, init?: RequestInit) {
  try {
    const apiBase = getApiBase();
    const response = await fetch(`${apiBase}${path}`, { 
      cache: "no-store", 
      ...init 
    });
    
    if (!response.ok) {
      console.error(`API call failed: ${response.status} ${response.statusText}`);
      return null;
    }
    
    return await response.json();
  } catch (error) {
    console.error('API call error:', error);
    return null;
  }
}

// Shorter alias for convenience
export const j = apiCall;