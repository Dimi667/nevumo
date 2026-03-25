export type LeadStatus = 'created' | 'contacted' | 'done' | 'rejected';
export type AvailabilityStatus = 'active' | 'busy' | 'offline';
export type PriceType = 'fixed' | 'hourly' | 'request' | 'per_sqm';

export interface Lead {
  id: string;
  phone: string;
  description: string | null;
  status: LeadStatus;
  source: string | null;
  created_at: string;
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
  accepted_matches: number;
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
  availability_status?: AvailabilityStatus;
  category_slug?: string;
  city_slug?: string;
}
