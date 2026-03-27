const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

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
  translations: Record<string, string>;
}

export interface CategoryOut {
  id: number;
  slug: string;
  name: string;
}

export interface CityOut {
  id: number;
  slug: string;
  name: string;
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

export async function getProviderBySlug(providerSlug: string, lang: string): Promise<ProviderDetail | null> {
  try {
    const url = new URL(`${API_BASE}/api/v1/providers/${encodeURIComponent(providerSlug)}`);
    url.searchParams.set('lang', lang);
    const res = await fetch(url.toString(), { cache: 'no-store' });
    if (!res.ok) return null;
    const json: ApiResponse<ProviderDetail> = await res.json();
    return json.success ? json.data : null;
  } catch {
    return null;
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

export async function getCities(country: string): Promise<CityOut[]> {
  try {
    const res = await fetch(
      `${API_BASE}/api/v1/cities?country=${encodeURIComponent(country)}`,
      { next: { revalidate: 3600 } },
    );
    if (!res.ok) return [];
    const json: ApiResponse<CityOut[]> = await res.json();
    return json.success ? json.data : [];
  } catch {
    return [];
  }
}

export async function createLead(input: LeadCreateInput): Promise<LeadCreateResult | null> {
  try {
    const res = await fetch(`${API_BASE}/api/v1/leads`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(input),
    });
    if (!res.ok) return null;
    const json: ApiResponse<LeadCreateResult> = await res.json();
    return json.success ? json.data : null;
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
