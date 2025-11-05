// API integration helpers for Django admin data

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

export interface DjangoUser {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_staff: boolean;
  is_active: boolean;
  date_joined: string;
}

export interface Business {
  id: number;
  name: string;
  description: string;
  category: string;
  city: string;
  country: string;
  is_active: boolean;
  is_featured: boolean;
  created_at: string;
}

export interface BlogPost {
  id: number;
  title: string;
  content: string;
  slug: string;
  published_at: string;
  is_published: boolean;
  author: string;
}

export interface SEOSettings {
  id: number;
  site_name: string;
  site_description: string;
  default_meta_title: string;
  default_meta_description: string;
}

// API Functions
export async function fetchDashboardStats() {
  try {
    const response = await fetch(`${API_BASE_URL}/dashboard/stats/`);
    if (!response.ok) throw new Error('Failed to fetch dashboard stats');
    return await response.json();
  } catch (error) {
    console.error('Error fetching dashboard stats:', error);
    return null;
  }
}

export async function fetchUsers(): Promise<DjangoUser[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/users/`);
    if (!response.ok) throw new Error('Failed to fetch users');
    return await response.json();
  } catch (error) {
    console.error('Error fetching users:', error);
    return [];
  }
}

export async function fetchBusinesses(): Promise<Business[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/businesses/`);
    if (!response.ok) throw new Error('Failed to fetch businesses');
    return await response.json();
  } catch (error) {
    console.error('Error fetching businesses:', error);
    return [];
  }
}

export async function fetchBlogPosts(): Promise<BlogPost[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/blog/posts/`);
    if (!response.ok) throw new Error('Failed to fetch blog posts');
    return await response.json();
  } catch (error) {
    console.error('Error fetching blog posts:', error);
    return [];
  }
}

export async function fetchSEOSettings(): Promise<SEOSettings | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/seo/settings/`);
    if (!response.ok) throw new Error('Failed to fetch SEO settings');
    return await response.json();
  } catch (error) {
    console.error('Error fetching SEO settings:', error);
    return null;
  }
}

// CSRF Token helper for Django
export async function getCSRFToken(): Promise<string | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/csrf-token/`);
    if (!response.ok) throw new Error('Failed to fetch CSRF token');
    const data = await response.json();
    return data.csrf_token;
  } catch (error) {
    console.error('Error fetching CSRF token:', error);
    return null;
  }
}

// Helper function for authenticated requests
export async function authenticatedRequest(
  url: string, 
  options: RequestInit = {}
): Promise<Response> {
  const csrfToken = await getCSRFToken();
  
  const headers = {
    'Content-Type': 'application/json',
    ...(csrfToken && { 'X-CSRFToken': csrfToken }),
    ...options.headers,
  };

  return fetch(url, {
    ...options,
    headers,
    credentials: 'include', // Include cookies for Django session auth
  });
}