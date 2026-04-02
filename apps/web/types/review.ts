export interface ProviderReviewItem {
  id: string;
  provider_id: string;
  client_id: string;
  client_name: string;
  lead_id?: string;
  rating: number;
  comment?: string;
  created_at: string;
  provider_reply?: string;
  provider_reply_at?: string;
  provider_reply_edited_at?: string;
  provider_reply_edit_count: number;
  is_reply_edited: boolean;
}

export interface ClientReviewItem {
  id: string;
  provider_id: string;
  provider_business_name?: string;
  lead_id?: string;
  lead_description?: string;
  rating: number;
  comment?: string;
  created_at: string;
  provider_reply?: string;
  provider_reply_at?: string;
  provider_reply_edited_at?: string;
  provider_reply_edit_count: number;
  is_reply_edited: boolean;
}

export interface ReviewListResponse {
  items: ProviderReviewItem[];
  total: number;
  limit: number;
  offset: number;
}

export interface ClientReviewListResponse {
  items: ClientReviewItem[];
  total: number;
  limit: number;
  offset: number;
}

export interface LatestReviewPreview {
  has_reviews: boolean;
  latest_review?: {
    id: string;
    client_name: string;
    rating: number;
    comment_preview?: string;
    has_reply: boolean;
    created_at: string;
    unreplied_count: number;
  };
  unreplied_count: number;
}

export interface EligibleLead {
  id: string;
  description?: string;
  created_at: string;
  provider_id: string;
  provider_business_name?: string;
  has_review: boolean;
}

export interface ReviewEligibilityResponse {
  can_review: boolean;
  reason?: string;
  message?: string;
  eligible_leads?: Array<{
    id: string;
    description?: string;
    created_at: string;
  }>;
}

export interface EmailPreferences {
  review_reply_email_enabled: boolean;
  description?: string;
}
