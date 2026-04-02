import { api } from './api';
import type { ProviderReviewItem, ReviewListResponse, LatestReviewPreview } from '@/types/review';

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

  const response = await api.get(`/api/v1/provider/reviews?${params.toString()}`);
  return response.data;
}

export async function getLatestReviewPreview(): Promise<LatestReviewPreview> {
  const response = await api.get('/api/v1/provider/reviews/latest-preview');
  return response.data;
}

export async function addReviewReply(
  reviewId: string,
  reply: string
): Promise<ProviderReviewItem> {
  const response = await api.post(`/api/v1/provider/reviews/${reviewId}/reply`, {
    reply,
  });
  return response.data;
}

export async function updateReviewReply(
  reviewId: string,
  reply: string
): Promise<ProviderReviewItem> {
  const response = await api.patch(`/api/v1/provider/reviews/${reviewId}/reply`, {
    reply,
  });
  return response.data;
}

// Client API functions
export async function getEligibleLeadsForReview() {
  const response = await api.get('/api/v1/client/reviews/eligible-leads');
  return response.data;
}

export async function createReview(
  leadId: string,
  rating: number,
  comment?: string
) {
  const response = await api.post('/api/v1/client/reviews', {
    lead_id: leadId,
    rating,
    comment,
  });
  return response.data;
}

export async function getClientReviews() {
  const response = await api.get('/api/v1/client/reviews');
  return response.data;
}

export async function getClientEmailPreferences() {
  const response = await api.get('/api/v1/client/reviews/preferences');
  return response.data;
}

export async function updateClientEmailPreferences(
  reviewReplyEmailEnabled: boolean
) {
  const response = await api.patch(
    `/api/v1/client/reviews/preferences?review_reply_email_enabled=${reviewReplyEmailEnabled}`
  );
  return response.data;
}

export async function canReviewProvider(providerId: string) {
  const response = await api.get(
    `/api/v1/client/reviews/can-review-provider/${providerId}`
  );
  return response.data;
}
