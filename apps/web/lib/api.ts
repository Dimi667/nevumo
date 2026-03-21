const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// ─── Response envelope ───────────────────────────────────────────────────────

export interface ApiSuccess<T> {
  success: true;
  data: T;
}

export interface ApiError {
  success: false;
  error: { code: string; message: string };
}

export type ApiResponse<T> = ApiSuccess<T> | ApiError;

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
  price_type: string;
  base_price: number | null;
}

export interface ProviderDetail {
  id: string;
  business_name: string;
  description: string | null;
  rating: number;
  verified: boolean;
  slug: string;
  services: ServiceOut[];
}

export interface CategoryOut {
  slug: string;
  name: string;
}

export interface CityOut {
  slug: string;
  name: string;
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

export async function getProviderBySlug(providerSlug: string): Promise<ProviderDetail | null> {
  try {
    const res = await fetch(
      `${API_BASE}/api/v1/providers/${encodeURIComponent(providerSlug)}`,
      { cache: 'no-store' },
    );
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
