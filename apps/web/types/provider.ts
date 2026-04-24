export type LeadStatusQuery = 'all' | 'new' | 'contacted' | 'done' | 'rejected';
export type LeadStatus = 'new' | 'created' | 'pending_match' | 'matched' | 'contacted' | 'done' | 'rejected' | 'cancelled' | 'expired';
export type AvailabilityStatus = 'active' | 'busy' | 'offline';
export type PriceType = 'fixed' | 'hourly' | 'request' | 'per_sqm';

export interface Lead {
  id: string;
  phone: string;
  description: string | null;
  status: LeadStatus;
  source: string | null;
  created_at: string;
  provider_notes: string | null;
}

export interface ServiceCity {
  id: number;
  slug: string;
  city: string;
}

export interface Service {
  id: string;
  title: string;
  description: string | null;
  category_id: number;
  category_slug: string;
  cities: ServiceCity[];
  price_type: PriceType;
  base_price: number | null;
  currency: string;
}

export interface ProviderProfile {
  id: string;
  business_name: string;
  description: string | null;
  slug: string;
  slug_change_count: number;
  profile_image_url: string | null;
  rating: number;
  verified: boolean;
  availability_status: AvailabilityStatus;
  created_at: string;
  is_complete: boolean;
  missing_fields: string[];
  current_category?: { slug: string; name: string } | null;
  current_city?: { slug: string; name: string } | null;
}

export interface DashboardStats {
  total_leads: number;
  new_leads: number;
  contacted_leads: number;
  rating: number;
  verified: boolean;
  availability_status: AvailabilityStatus;
}

export interface AnalyticsSources {
  seo: number;
  widget: number;
  qr: number;
  direct: number;
  other: number;
}

export interface AnalyticsData {
  period_days: number;
  total_leads: number;
  contacted_leads: number;
  conversion_rate: number;
  sources: AnalyticsSources;
}

export interface AnalyticsSummary {
  period_days: number;
  total_leads: number;
  contacted_leads: number;
  sources: Omit<AnalyticsSources, 'other'>;
}

export interface DashboardResponse {
  stats: DashboardStats;
  profile: ProviderProfile;
  analytics_summary?: AnalyticsSummary;
}

export interface CreateServiceInput {
  title: string;
  category_id: number;
  city_ids: number[];
  description?: string;
  price_type: PriceType;
  base_price?: number;
  currency?: string;
}

export interface UpdateProfileInput {
  business_name?: string;
  description?: string;
  slug?: string;
  is_onboarding_setup?: boolean;
  availability_status?: AvailabilityStatus;
  category_slug?: string;
  city_slug?: string;
}

export interface LeadsFilters {
  status?: LeadStatusQuery;
  period?: 'all' | '7' | '30' | '90';
  date_from?: string;
  date_to?: string;
  search?: string;
}

export interface LeadsResponse {
  leads: Lead[];
  total: number;
}

export interface ProviderSlugHistoryItem {
  id: string;
  old_slug: string;
  new_slug: string;
  changed_at: string;
  ip_address: string | null;
  user_agent: string | null;
}
