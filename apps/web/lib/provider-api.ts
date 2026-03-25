import { getAuthToken } from '@/lib/auth-store';
import type { UserInfo } from '@/lib/auth-types';
import type {
  AnalyticsData,
  CreateServiceInput,
  DashboardResponse,
  Lead,
  LeadStatus,
  ProviderProfile,
  Service,
  UpdateProfileInput,
} from '@/types/provider';

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

class ProviderApiError extends Error {
  code: string;
  status: number;
  constructor(code: string, message: string, status: number) {
    super(message);
    this.code = code;
    this.status = status;
    this.name = 'ProviderApiError';
  }
}

async function authFetch<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getAuthToken();
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers ?? {}),
    },
  });

  const json = await res.json() as { success: boolean; data?: T; error?: { code: string; message: string } };

  if (!json.success) {
    const err = json.error;
    throw new ProviderApiError(
      err?.code ?? 'UNKNOWN_ERROR',
      err?.message ?? 'An unexpected error occurred',
      res.status
    );
  }

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

export async function getProviderLeads(): Promise<Lead[]> {
  const data = await authFetch<{ leads: Lead[]; total: number }>('/api/v1/provider/leads');
  return data.leads;
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

export async function getQRCode(): Promise<{ public_url: string; qr_code: string }> {
  return authFetch('/api/v1/provider/qr-code');
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
