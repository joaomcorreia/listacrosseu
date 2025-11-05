export const API_BASE = process.env.NODE_ENV === 'production' 
  ? 'https://your-domain.com/api/v1'
  : 'http://127.0.0.1:8000/api/v1';

/**
 * Simple fetch wrapper for API calls
 * @param path API endpoint path (e.g., '/blog/posts/')
 * @param init Optional fetch init object
 * @returns JSON response or null on error
 */
export async function apiCall(path: string, init?: RequestInit) {
  try {
    const response = await fetch(`${API_BASE}${path}`, { 
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