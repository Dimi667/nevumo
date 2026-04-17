export const API_BASE = typeof window === 'undefined'
  ? (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000')
  : '';

// ─── Auth token helper ─────────────────────────────────────────────────────

function getAuthToken(): string | null {
  if (typeof window === 'undefined') return null;
  try {
    return localStorage.getItem('nevumo_auth_token');
  } catch {
    return null;
  }
}

// ─── Authenticated API client ───────────────────────────────────────────────

async function authFetch<T>(path: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
  const token = getAuthToken();
  const fullUrl = `${API_BASE}${path}`;

  const res = await fetch(fullUrl, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });

  const json = await res.json();
  return json as ApiResponse<T>;
}

export const api = {
  async get<T>(path: string): Promise<ApiSuccess<T>> {
    const response = await authFetch<T>(path, { method: 'GET' });
    if (!response.success) {
      throw new ApiError(response.error.code, response.error.message);
    }
    return response;
  },

  async post<T>(path: string, body: Record<string, unknown>): Promise<ApiSuccess<T>> {
    const response = await authFetch<T>(path, {
      method: 'POST',
      body: JSON.stringify(body),
    });
    if (!response.success) {
      throw new ApiError(response.error.code, response.error.message);
    }
    return response;
  },

  async patch<T>(path: string, body?: Record<string, unknown>): Promise<ApiSuccess<T>> {
    const response = await authFetch<T>(path, {
      method: 'PATCH',
      body: body ? JSON.stringify(body) : undefined,
    });
    if (!response.success) {
      throw new ApiError(response.error.code, response.error.message);
    }
    return response;
  },
};

// ─── Response envelope ───────────────────────────────────────────────────────

export interface ApiSuccess<T> {
  success: true;
  data: T;
}

interface ApiErrorEnvelope {
  success: false;
  error: { code: string; message: string };
}

export type ApiResponse<T> = ApiSuccess<T> | ApiErrorEnvelope;

// ─── Auth API error class ─────────────────────────────────────────────────────

export class ApiError extends Error {
  code: string;
  constructor(code: string, message: string) {
    super(message);
    this.code = code;
    this.name = "ApiError";
  }
}

export async function apiPost<T>(path: string, body: Record<string, unknown>): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const json = await res.json();
  if (!json.success) {
    throw new ApiError(
      json.error?.code || "UNKNOWN_ERROR",
      json.error?.message || "An unexpected error occurred"
    );
  }
  return json.data as T;
}

// ─── Domain types ─────────────────────────────────────────────────────────────

export interface ProviderListItem {
  id: string;
  business_name: string;
  rating: number;
  verified: boolean;
  slug: string;
}

export interface ServiceOut {
  id: string;
  title: string;
  description: string | null;
  price_type: string;
  base_price: number | null;
  category_slug: string | null;
  currency: string;
}

export interface LatestReviewPreview {
  client_name: string;
  rating: number;
  comment_preview: string | null;
  created_at: string;
}

export interface LatestLeadPreview {
  client_name: string;
  city_name: string;
  created_at: string;
  client_image_url: string | null;
}

export interface ProviderDetail {
  id: string;
  business_name: string;
  description: string | null;
  slug: string;
  profile_image_url: string | null;
  rating: number;
  verified: boolean;
  services: ServiceOut[];
  jobs_completed: number;
  review_count: number;
  leads_received: number;
  city_leads: number;
  translations: Record<string, string>;
  canonical_path?: string | null;
  latest_lead_preview?: LatestLeadPreview | null;
  latest_review?: LatestReviewPreview | null;
  is_claimed: boolean;
}

export interface CategoryOut {
  id: number;
  slug: string;
  name: string;
}

export interface CityOut {
  id: number;
  slug: string;
  city: string;
  city_en: string;
  country_code: string;
  currency: string;
}

export interface LeadCreateInput {
  category_slug: string;
  city_slug: string;
  provider_slug?: string;
  phone: string;
  description?: string;
  utm_source?: string;
  utm_campaign?: string;
  source?: string;
}

export interface LeadCreateResult {
  lead_id: string;
}

// ─── Price Range Types ─────────────────────────────────────────────────────

export interface PriceRangeData {
  min: number;
  max: number;
  currency: string;
  provider_count: number;
}

// ─── API functions ────────────────────────────────────────────────────────────

export async function getProviders(
  categorySlug: string,
  citySlug: string,
  lang: string,
): Promise<ProviderListItem[]> {
  try {
    const params = new URLSearchParams({ category_slug: categorySlug, city_slug: citySlug, lang });
    const res = await fetch(`${API_BASE}/api/v1/providers?${params}`, { cache: 'no-store' });
    if (!res.ok) return [];
    const json: ApiResponse<ProviderListItem[]> = await res.json();
    return json.success ? json.data : [];
  } catch {
    return [];
  }
}

export async function getProviderBySlug(
  slug: string,
  lang: string = 'en',
  citySlug?: string,
): Promise<ProviderDetail | null> {
  try {
    const params = new URLSearchParams({ lang });
    if (citySlug) params.set('city_slug', citySlug);
    const response = await fetch(`${API_BASE}/api/v1/providers/${slug}?${params.toString()}`, { cache: 'no-store' });
    if (!response.ok) {
      if (response.status === 404) return null;
      throw new Error(`HTTP ${response.status}`);
    }
    const json = await response.json();
    return json.success ? json.data : null;
  } catch (error: any) {
    if (error.response?.status === 404) return null;
    throw error;
  }
}

export async function resolveSlug(slug: string): Promise<{found: boolean, slug: string | null, redirected: boolean}> {
  try {
    const response = await fetch(`${API_BASE}/api/v1/providers/resolve/${slug}`);
    if (!response.ok) {
      if (response.status === 404) return {found: false, slug: null, redirected: false};
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error: any) {
    return {found: false, slug: null, redirected: false};
  }
}

export async function getCategories(lang: string): Promise<CategoryOut[]> {
  try {
    const res = await fetch(
      `${API_BASE}/api/v1/categories?lang=${encodeURIComponent(lang)}`,
      { next: { revalidate: 3600 } },
    );
    if (!res.ok) return [];
    const json: ApiResponse<CategoryOut[]> = await res.json();
    return json.success ? json.data : [];
  } catch {
    return [];
  }
}

export async function getCities(country: string, lang?: string): Promise<CityOut[]> {
  try {
    const params = new URLSearchParams({ country });
    if (lang) params.set('lang', lang);
    const res = await fetch(
      `${API_BASE}/api/v1/cities?${params.toString()}`,
      { next: { revalidate: 3600 } },
    );
    if (!res.ok) return [];
    const json: ApiResponse<CityOut[]> = await res.json();
    return json.success ? json.data : [];
  } catch {
    return [];
  }
}

export async function getCityBySlug(slug: string, lang?: string): Promise<CityOut | null> {
  try {
    const params = new URLSearchParams();
    if (lang) params.set('lang', lang);
    const url = `${API_BASE}/api/v1/cities/${encodeURIComponent(slug)}${params.toString() ? `?${params.toString()}` : ''}`;
    const res = await fetch(url, { next: { revalidate: 3600 } });
    if (!res.ok) return null;
    const json: ApiResponse<CityOut> = await res.json();
    return json.success ? json.data : null;
  } catch {
    return null;
  }
}

export async function createLead(input: LeadCreateInput): Promise<LeadCreateResult | { success: false; error: { code: string; message: string } } | null> {
  try {
    const token = getAuthToken();
    const res = await fetch(`${API_BASE}/api/v1/leads`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify(input),
    });
    const json: ApiResponse<LeadCreateResult> = await res.json();
    if (!json.success) {
      return { success: false, error: json.error };
    }
    return json.data;
  } catch {
    return null;
  }
}

export async function trackEvent(
  leadId: string,
  eventType: string,
  metadata?: Record<string, unknown>,
): Promise<void> {
  try {
    await fetch(`${API_BASE}/api/v1/events`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ lead_id: leadId, event_type: eventType, metadata }),
    });
  } catch {
    // silently fail
  }
}

export async function getProviderById(providerId: string): Promise<ProviderDetail | null> {
  try {
    const url = new URL(`${API_BASE}/api/v1/providers/id/${encodeURIComponent(providerId)}`);
    const res = await fetch(url.toString(), { cache: 'no-store' });
    if (!res.ok) return null;
    const json: ApiResponse<ProviderDetail> = await res.json();
    return json.success ? json.data : null;
  } catch {
    return null;
  }
}

export async function getPriceRange(
  categorySlug: string,
  citySlug: string,
): Promise<PriceRangeData | null> {
  try {
    const isDev = process.env.NODE_ENV === 'development';
    const fetchOptions: RequestInit = isDev
      ? { cache: 'no-store' }
      : { next: { revalidate: 3600 } };

    const params = new URLSearchParams({ category_slug: categorySlug, city_slug: citySlug });
    const res = await fetch(`${API_BASE}/api/v1/price-range?${params}`, fetchOptions);
    if (!res.ok) return null;
    const json: ApiResponse<PriceRangeData | null> = await res.json();
    return json.success ? json.data : null;
  } catch {
    return null;
  }
}
