import { api } from './api';
import type {
  ClientReviewListResponse,
  EmailPreferences,
  EligibleLead,
  LatestReviewPreview,
  ProviderReviewItem,
  ReviewEligibilityResponse,
  ReviewListResponse,
} from '@/types/review';

interface CreatedReview {
  id: string;
  provider_id: string;
  lead_id: string;
  rating: number;
  comment?: string;
  created_at: string;
}

interface EligibleLeadsResponse {
  leads: EligibleLead[];
  count: number;
}

interface GetReviewsOptions {
  limit?: number;
  offset?: number;
  unrepliedOnly?: boolean;
}

export async function getProviderReviews(
  options: GetReviewsOptions = {}
): Promise<ReviewListResponse> {
  const params = new URLSearchParams();
  if (options.limit) params.set('limit', options.limit.toString());
  if (options.offset) params.set('offset', options.offset.toString());
  if (options.unrepliedOnly) params.set('unreplied_only', 'true');

  const response = await api.get<ReviewListResponse>(`/api/v1/provider/reviews?${params.toString()}`);
  return response.data;
}

export async function getLatestReviewPreview(): Promise<LatestReviewPreview> {
  const response = await api.get<LatestReviewPreview>('/api/v1/provider/reviews/latest-preview');
  return response.data;
}

export async function addReviewReply(
  reviewId: string,
  reply: string
): Promise<ProviderReviewItem> {
  const response = await api.post<ProviderReviewItem>(`/api/v1/provider/reviews/${reviewId}/reply`, {
    reply,
  });
  return response.data;
}

export async function updateReviewReply(
  reviewId: string,
  reply: string
): Promise<ProviderReviewItem> {
  const response = await api.patch<ProviderReviewItem>(`/api/v1/provider/reviews/${reviewId}/reply`, {
    reply,
  });
  return response.data;
}

// Client API functions
export async function getEligibleLeadsForReview(): Promise<EligibleLeadsResponse> {
  const response = await api.get<EligibleLeadsResponse>('/api/v1/client/reviews/eligible-leads');
  return response.data;
}

export async function createReview(
  leadId: string,
  rating: number,
  comment?: string
): Promise<CreatedReview> {
  const response = await api.post<CreatedReview>('/api/v1/client/reviews', {
    lead_id: leadId,
    rating,
    comment,
  });
  return response.data;
}

export async function getClientReviews(): Promise<ClientReviewListResponse> {
  const response = await api.get<ClientReviewListResponse>('/api/v1/client/reviews');
  return response.data;
}

export async function getClientEmailPreferences(): Promise<EmailPreferences> {
  const response = await api.get<EmailPreferences>('/api/v1/client/reviews/preferences');
  return response.data;
}

export async function updateClientEmailPreferences(
  reviewReplyEmailEnabled: boolean
): Promise<EmailPreferences> {
  const response = await api.patch<EmailPreferences>(
    `/api/v1/client/reviews/preferences?review_reply_email_enabled=${reviewReplyEmailEnabled}`
  );
  return response.data;
}

export async function canReviewProvider(providerId: string): Promise<ReviewEligibilityResponse> {
  const response = await api.get<ReviewEligibilityResponse>(
    `/api/v1/client/reviews/can-review-provider/${providerId}`
  );
  return response.data;
}
