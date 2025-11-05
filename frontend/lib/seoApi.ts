// SEO API data layer for fetching SEO page data
export interface Country {
  id: number;
  code: string;
  name: string;
  default_locale: string;
}

export interface Language {
  id: number;
  code: string;
  name: string;
}

export interface SeoPlan {
  id: number;
  name: string;
  slug: string;
  features: Record<string, any>;
  order: number;
}

export interface SeoContentBlock {
  id: number;
  key: string;
  content: string;
  order: number;
}

export interface SeoPage {
  id: number;
  country?: Country;
  language: Language;
  slug: string;
  page_type: 'home' | 'service' | 'city' | 'country' | 'blog' | 'custom';
  plan: SeoPlan;
  
  // Basic SEO fields
  meta_title: string;
  meta_description: string;
  h1: string;
  h2?: string;
  canonical_url: string;
  robots: string;
  image_alt_fallback?: string;
  
  // Growth fields (conditional)
  keywords_hint?: string;
  internal_links?: Array<{ title: string; href: string }>;
  sitemap_include?: boolean;
  og_title?: string;
  og_description?: string;
  og_image_url?: string;
  twitter_card?: string;
  twitter_image_url?: string;
  
  // Premium fields (conditional)
  json_ld?: string;
  breadcrumbs?: Array<{ name: string; url: string }>;
  local_business_schema?: Record<string, any>;
  service_schema?: Record<string, any>;
  
  // Meta
  is_published: boolean;
  publish_at?: string;
  created_at: string;
  updated_at: string;
  content_blocks: SeoContentBlock[];
  absolute_url: string;
  can_use_growth_features: boolean;
  can_use_premium_features: boolean;
}

export interface SitemapEntry {
  url: string;
  country_code?: string;
  language_code: string;
  page_type: string;
  updated_at: string;
  publish_at?: string;
}

export interface FetchSeoPageParams {
  lang: string;
  country?: string;
  slug?: string;
  type?: string;
}

const API_BASE = '/api/seo';

export class SeoApiError extends Error {
  constructor(message: string, public status?: number) {
    super(message);
    this.name = 'SeoApiError';
  }
}

async function apiRequest<T>(url: string): Promise<T> {
  try {
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new SeoApiError(
        `API request failed: ${response.status} ${response.statusText}`,
        response.status
      );
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    if (error instanceof SeoApiError) {
      throw error;
    }
    throw new SeoApiError(`Network error: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

/**
 * Fetch a specific SEO page by parameters
 */
export async function fetchSeoPage(params: FetchSeoPageParams): Promise<SeoPage | null> {
  const searchParams = new URLSearchParams();
  
  if (params.lang) {
    searchParams.set('language__code', params.lang);
  }
  if (params.country) {
    searchParams.set('country__code', params.country.toUpperCase());
  }
  if (params.slug) {
    searchParams.set('slug', params.slug);
  }
  if (params.type) {
    searchParams.set('page_type', params.type);
  }
  
  // Only return published pages
  searchParams.set('is_published', 'true');
  
  const url = `${API_BASE}/api/pages/?${searchParams.toString()}`;
  
  try {
    const response = await apiRequest<{ results: SeoPage[] }>(url);
    return response.results.length > 0 ? response.results[0] : null;
  } catch (error) {
    console.error('Failed to fetch SEO page:', error);
    return null;
  }
}

/**
 * Fetch sitemap data for all published pages
 */
export async function fetchSitemap(): Promise<SitemapEntry[]> {
  try {
    const response = await apiRequest<SitemapEntry[]>(`${API_BASE}/api/pages/sitemap/`);
    return response;
  } catch (error) {
    console.error('Failed to fetch sitemap:', error);
    return [];
  }
}

/**
 * Fetch all countries
 */
export async function fetchCountries(): Promise<Country[]> {
  try {
    const response = await apiRequest<{ results: Country[] }>(`${API_BASE}/api/countries/`);
    return response.results || [];
  } catch (error) {
    console.error('Failed to fetch countries:', error);
    return [];
  }
}

/**
 * Fetch all languages
 */
export async function fetchLanguages(): Promise<Language[]> {
  try {
    const response = await apiRequest<{ results: Language[] }>(`${API_BASE}/api/languages/`);
    return response.results || [];
  } catch (error) {
    console.error('Failed to fetch languages:', error);
    return [];
  }
}

/**
 * Fetch all SEO plans
 */
export async function fetchSeoPlans(): Promise<SeoPlan[]> {
  try {
    const response = await apiRequest<{ results: SeoPlan[] }>(`${API_BASE}/api/plans/`);
    return response.results || [];
  } catch (error) {
    console.error('Failed to fetch SEO plans:', error);
    return [];
  }
}

/**
 * Helper function to build meta tags for Next.js Head component
 */
export function buildMetaTags(seoPage: SeoPage) {
  const metaTags: Record<string, string> = {
    title: seoPage.meta_title,
    description: seoPage.meta_description,
    robots: seoPage.robots,
  };
  
  if (seoPage.canonical_url) {
    metaTags.canonical = seoPage.canonical_url;
  }
  
  // Growth features
  if (seoPage.can_use_growth_features) {
    if (seoPage.og_title) {
      metaTags['og:title'] = seoPage.og_title;
    }
    if (seoPage.og_description) {
      metaTags['og:description'] = seoPage.og_description;
    }
    if (seoPage.og_image_url) {
      metaTags['og:image'] = seoPage.og_image_url;
    }
    if (seoPage.twitter_card) {
      metaTags['twitter:card'] = seoPage.twitter_card;
    }
    if (seoPage.twitter_image_url) {
      metaTags['twitter:image'] = seoPage.twitter_image_url;
    }
  }
  
  return metaTags;
}

/**
 * Helper function to get JSON-LD structured data
 */
export function getStructuredData(seoPage: SeoPage): Record<string, any> | null {
  if (!seoPage.can_use_premium_features || !seoPage.json_ld) {
    return null;
  }
  
  try {
    return JSON.parse(seoPage.json_ld);
  } catch (error) {
    console.error('Invalid JSON-LD data:', error);
    return null;
  }
}