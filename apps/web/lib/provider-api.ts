import { getAuthToken } from '@/lib/auth-store';
import type { UserInfo } from '@/lib/auth-types';
import type {
  AnalyticsData,
  CreateServiceInput,
  DashboardResponse,
  Lead,
  LeadStatus,
  LeadsFilters,
  LeadsResponse,
  ProviderProfile,
  ProviderSlugHistoryItem,
  Service,
  UpdateProfileInput,
} from '@/types/provider';

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

export class ProviderApiError extends Error {
  code: string;
  status: number;
  data?: unknown;
  constructor(code: string, message: string, status: number, data?: unknown) {
    super(message);
    this.code = code;
    this.status = status;
    this.data = data;
    this.name = 'ProviderApiError';
  }
}

async function authFetch<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getAuthToken();
  const fullUrl = `${API_BASE}${path}`;
  
  console.log(`NETWORK: Request to ${fullUrl}`);
  console.log(`NETWORK: Method: ${options.method || 'GET'}`);
  console.log(`NETWORK: Headers:`, {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(options.headers ?? {}),
  });
  if (options.body) {
    console.log(`NETWORK: Body:`, options.body);
  }
  
  const res = await fetch(fullUrl, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers ?? {}),
    },
  });

  console.log(`NETWORK: Response status: ${res.status}`);
  console.log(`NETWORK: Response headers:`, Object.fromEntries(res.headers.entries()));

  const json = await res.json() as {
    success: boolean;
    data?: T;
    error?: { code: string; message: string };
  };
  
  console.log(`NETWORK: Response body:`, json);

  if (!json.success) {
    const err = json.error;
    console.error(`NETWORK: API Error:`, err);
    throw new ProviderApiError(
      err?.code ?? 'UNKNOWN_ERROR',
      err?.message ?? 'An unexpected error occurred',
      res.status,
      json.data
    );
  }

  console.log(`NETWORK: Success, returning data:`, json.data);
  return json.data as T;
}

// ---------------------------------------------------------------------------
// Dashboard
// ---------------------------------------------------------------------------

export async function getProviderDashboard(): Promise<DashboardResponse> {
  return authFetch<DashboardResponse>('/api/v1/provider/dashboard');
}

// ---------------------------------------------------------------------------
// Leads
// ---------------------------------------------------------------------------

export async function getProviderLeads(filters?: LeadsFilters): Promise<LeadsResponse> {
  const params = new URLSearchParams();
  if (filters?.status) params.set('status', filters.status);
  if (filters?.period) params.set('period', filters.period);
  if (filters?.date_from) params.set('date_from', filters.date_from);
  if (filters?.date_to) params.set('date_to', filters.date_to);

  const queryString = params.toString();
  const url = `/api/v1/provider/leads${queryString ? `?${queryString}` : ''}`;

  return authFetch<LeadsResponse>(url);
}

export async function updateLeadStatus(
  leadId: string,
  status: Exclude<LeadStatus, 'created'>
): Promise<{ lead_id: string; status: string }> {
  return authFetch(`/api/v1/provider/leads/${leadId}`, {
    method: 'PATCH',
    body: JSON.stringify({ status }),
  });
}

// ---------------------------------------------------------------------------
// Profile
// ---------------------------------------------------------------------------

export async function getProviderProfile(): Promise<ProviderProfile> {
  return authFetch<ProviderProfile>('/api/v1/provider/profile');
}

export async function updateProviderProfile(
  data: UpdateProfileInput
): Promise<ProviderProfile> {
  return authFetch<ProviderProfile>('/api/v1/provider/profile', {
    method: 'PATCH',
    body: JSON.stringify(data),
  });
}

export async function checkSlugAvailability(
  slug: string,
  citySlug?: string,
  categorySlug?: string
): Promise<{ available: boolean; suggestions?: string[]; error?: string }> {
  const params = new URLSearchParams({ slug });
  if (citySlug) params.set('city_slug', citySlug);
  if (categorySlug) params.set('category_slug', categorySlug);

  const res = await fetch(
    `${API_BASE}/api/v1/provider/slug/check?${params}`,
    { cache: 'no-store' }
  );
  const json = await res.json() as { 
    success: boolean; 
    data?: { available: boolean; suggestions?: string[] };
    error?: { code: string; message: string } 
  };
  
  if (!json.success) {
    return {
      available: false,
      suggestions: [],
      error: json.error?.message ?? 'Failed to check availability',
    };
  }
  
  return json.data as { available: boolean; suggestions?: string[]; error?: string };
}

export async function uploadProviderImage(file: File): Promise<{ image_url: string }> {
  const token = getAuthToken();
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${API_BASE}/api/v1/provider/profile/image`, {
    method: 'POST',
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    body: formData,
  });

  const json = await res.json() as { success: boolean; data?: { image_url: string }; error?: { code: string; message: string } };
  if (!json.success) {
    const err = json.error;
    throw new ProviderApiError(
      err?.code ?? 'UNKNOWN_ERROR',
      err?.message ?? 'Upload failed',
      res.status
    );
  }
  return json.data as { image_url: string };
}

// ---------------------------------------------------------------------------
// Services
// ---------------------------------------------------------------------------

export async function getProviderServices(): Promise<Service[]> {
  const data = await authFetch<{ services: Service[] }>('/api/v1/provider/services');
  return data.services;
}

export async function createService(data: CreateServiceInput): Promise<Service> {
  return authFetch<Service>('/api/v1/provider/services', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function updateService(
  id: string,
  data: Partial<CreateServiceInput>
): Promise<Service> {
  return authFetch<Service>(`/api/v1/provider/services/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

export async function deleteService(id: string): Promise<void> {
  await authFetch<{ message: string }>(`/api/v1/provider/services/${id}`, {
    method: 'DELETE',
  });
}

// ---------------------------------------------------------------------------
// Cities
// ---------------------------------------------------------------------------

export async function addProviderCity(cityId: number): Promise<{ message: string }> {
  return authFetch('/api/v1/provider/cities', {
    method: 'POST',
    body: JSON.stringify({ city_id: cityId }),
  });
}

// ---------------------------------------------------------------------------
// QR Code
// ---------------------------------------------------------------------------

export async function getProviderSlugHistory(): Promise<ProviderSlugHistoryItem[]> {
  const data = await authFetch<{ items: ProviderSlugHistoryItem[] }>('/api/v1/provider/slug-history');
  return data.items;
}

export async function getQRCode(): Promise<{ public_url: string; canonical_url: string; qr_code: string }> {
  return authFetch('/api/v1/provider/qr-code');
}

export async function getEnhancedQRCode(language: string = 'en'): Promise<{ 
  public_url: string; 
  canonical_url: string; 
  qr_code: string; 
  language: string;
  business_name: string;
  service_name: string;
}> {
  return authFetch('/api/v1/provider/enhanced-qr-code', {
    method: 'POST',
    body: JSON.stringify({ language }),
  });
}

export async function downloadEnhancedQRSVG(language: string = 'en', filename: string = 'nevumo-qr.svg'): Promise<void> {
  const token = getAuthToken();
  const res = await fetch(`${API_BASE}/api/v1/provider/enhanced-qr-code-svg`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify({ language }),
  });
  
  if (!res.ok) {
    throw new Error('Failed to download SVG');
  }
  
  const blob = await res.blob();
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
}

// ---------------------------------------------------------------------------
// Analytics
// ---------------------------------------------------------------------------

export async function getProviderAnalytics(period: 7 | 30): Promise<AnalyticsData> {
  return authFetch<AnalyticsData>(`/api/v1/provider/analytics?period=${period}`);
}

// ---------------------------------------------------------------------------
// Role Switch
// ---------------------------------------------------------------------------

export async function switchRole(
  role: 'provider' | 'client'
): Promise<{ token: string; user: UserInfo }> {
  return authFetch<{ token: string; user: UserInfo }>('/api/v1/auth/switch-role', {
    method: 'POST',
    body: JSON.stringify({ role }),
  });
}
