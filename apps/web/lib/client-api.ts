import { ApiError, type ApiResponse, API_BASE } from '@/lib/api';

export type ClientLeadFilterStatus = 'all' | 'active' | 'done' | 'rejected';
export type ClientLeadStatus = 'created' | 'pending_match' | 'matched' | 'contacted' | 'done' | 'rejected' | 'expired' | 'cancelled';

export interface ClientDashboardStats {
  active_leads: number;
  completed_leads: number;
  reviews_written: number;
}

export interface ClientDashboardRecentLead {
  id: string;
  category_slug: string;
  category_name: string;
  city: string;
  provider_business_name: string | null;
  status: ClientLeadStatus;
  created_at: string;
}

export interface ClientDashboardData {
  stats: ClientDashboardStats;
  recent_leads: ClientDashboardRecentLead[];
}

export interface ClientLead {
  id: string;
  category_slug: string;
  category_name: string;
  city: string;
  city_slug: string;
  provider_id: string | null;
  provider_business_name: string | null;
  provider_slug: string | null;
  status: ClientLeadStatus;
  description: string | null;
  source: string | null;
  created_at: string;
  has_review: boolean;
}

export interface ClientLeadsData {
  items: ClientLead[];
  total: number;
}

export interface ClientReview {
  id: string;
  provider_id: string;
  provider_business_name: string | null;
  lead_id: string | null;
  lead_description: string | null;
  rating: number;
  comment: string | null;
  created_at: string;
  provider_reply: string | null;
  provider_reply_at: string | null;
  provider_reply_edited_at: string | null;
  provider_reply_edit_count: number;
  is_reply_edited: boolean;
}

export interface ClientReviewsData {
  items: ClientReview[];
  total: number;
  limit: number;
  offset: number;
}

export interface EligibleLead {
  id: string;
  description: string | null;
  created_at: string;
  provider_id: string;
  provider_business_name: string | null;
  has_review: boolean;
}

export interface EligibleLeadsData {
  leads: EligibleLead[];
  count: number;
}

export interface SubmitReviewResult {
  id: string;
  provider_id: string;
  lead_id: string;
  rating: number;
  comment: string | null;
  created_at: string;
}

export interface ReviewPreferences {
  review_reply_email_enabled: boolean;
  description: string;
}

async function clientFetch<T>(token: string, path: string, options: RequestInit = {}): Promise<T> {
  if (!token) {
    throw new ApiError('UNAUTHORIZED', 'Missing auth token');
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    cache: 'no-store',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
      ...(options.headers ?? {}),
    },
  });

  const json = (await response.json().catch(() => null)) as ApiResponse<T> | null;

  if (!json) {
    throw new ApiError('INVALID_RESPONSE', 'Invalid server response');
  }

  if (!json.success) {
    throw new ApiError(json.error.code, json.error.message);
  }

  return json.data;
}

export async function getClientDashboard(token: string): Promise<ClientDashboardData> {
  return clientFetch<ClientDashboardData>(token, '/api/v1/client/dashboard', { method: 'GET' });
}

export async function getClientLeads(
  token: string,
  status?: ClientLeadFilterStatus,
  limit?: number,
  offset?: number,
): Promise<ClientLeadsData> {
  const params = new URLSearchParams();

  if (status) {
    params.set('status', status);
  }

  if (typeof limit === 'number') {
    params.set('limit', String(limit));
  }

  if (typeof offset === 'number') {
    params.set('offset', String(offset));
  }

  const query = params.toString();
  return clientFetch<ClientLeadsData>(
    token,
    `/api/v1/client/leads${query ? `?${query}` : ''}`,
    { method: 'GET' },
  );
}

export async function getClientReviews(token: string): Promise<ClientReviewsData> {
  return clientFetch<ClientReviewsData>(token, '/api/v1/client/reviews', { method: 'GET' });
}

export async function getEligibleLeads(token: string): Promise<EligibleLeadsData> {
  return clientFetch<EligibleLeadsData>(token, '/api/v1/client/reviews/eligible-leads', { method: 'GET' });
}

export async function submitReview(
  token: string,
  lead_id: string,
  rating: number,
  comment?: string,
): Promise<SubmitReviewResult> {
  return clientFetch<SubmitReviewResult>(token, '/api/v1/client/reviews', {
    method: 'POST',
    body: JSON.stringify({
      lead_id,
      rating,
      comment: comment?.trim() || undefined,
    }),
  });
}

export async function getReviewPreferences(token: string): Promise<ReviewPreferences> {
  return clientFetch<ReviewPreferences>(token, '/api/v1/client/reviews/preferences', { method: 'GET' });
}

export async function updateReviewPreferences(token: string, enabled: boolean): Promise<ReviewPreferences> {
  return clientFetch<ReviewPreferences>(
    token,
    `/api/v1/client/reviews/preferences?review_reply_email_enabled=${String(enabled)}`,
    { method: 'PATCH' },
  );
}
