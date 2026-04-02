'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useParams, useRouter } from 'next/navigation';
import StatsCard from '@/components/dashboard/StatsCard';
import type { DashboardResponse } from '@/types/provider';
import { getProviderDashboard } from '@/lib/provider-api';
import { getLatestReviewPreview } from '@/lib/review-api';
import type { LatestReviewPreview } from '@/types/review';
import { deriveOnboardingState, getHeroContent, CompactStepIndicator } from '@/lib/onboarding-utils';

function LeadsIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
      <circle cx="9" cy="7" r="4" />
      <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
      <path d="M16 3.13a4 4 0 0 1 0 7.75" />
    </svg>
  );
}

function NewLeadsIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12 19.79 19.79 0 0 1 1.65 3.33 2 2 0 0 1 3.62 1h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.6a16 16 0 0 0 5.35 5.35l.96-.96a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z" />
    </svg>
  );
}

function StarIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
    </svg>
  );
}

function CheckIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="20 6 9 17 4 12" />
    </svg>
  );
}

const SOURCE_LABELS: Record<string, string> = {
  seo: 'SEO',
  widget: 'Widget',
  qr: 'QR Code',
  direct: 'Direct',
};

// Motivational KPI values for incomplete onboarding
const MOTIVATIONAL_RATING = '5.0';
const MOTIVATIONAL_CONTACTED = 137;

export default function DashboardOverviewPage() {
  const params = useParams();
  const router = useRouter();
  const lang = typeof params.lang === 'string' ? params.lang : 'en';
  const base = `/${lang}/provider/dashboard`;

  const [data, setData] = useState<DashboardResponse | null>(null);
  const [reviewPreview, setReviewPreview] = useState<LatestReviewPreview | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      getProviderDashboard(),
      getLatestReviewPreview().catch(() => null), // Non-critical, don't fail if this errors
    ])
      .then(([dashboardData, reviewData]) => {
        setData(dashboardData);
        setReviewPreview(reviewData);
      })
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, [lang, router]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 text-red-700 rounded-xl p-4 text-sm">
        Failed to load dashboard: {error}
      </div>
    );
  }

  const stats = data?.stats;
  const profile = data?.profile;
  const analytics = data?.analytics_summary;

  // Derive onboarding state from missing_fields
  const onboardingState = deriveOnboardingState(profile?.missing_fields);
  const isOnboardingComplete = profile?.is_complete ?? true;
  const heroContent = !isOnboardingComplete ? getHeroContent(onboardingState) : null;

  // Top sources for the preview (sorted desc, top 3)
  const topSources = analytics
    ? Object.entries(analytics.sources)
        .sort(([, a], [, b]) => b - a)
        .slice(0, 3)
        .filter(([, count]) => count > 0)
    : [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-gray-900">
          {profile?.business_name ?? 'Dashboard'}
        </h1>
        <p className="text-sm text-gray-500 mt-0.5">Overview of your business</p>
      </div>

      {/* Incomplete onboarding hero banner */}
      {!isOnboardingComplete && heroContent && (
        <div className="bg-gradient-to-r from-orange-50 to-orange-100 border border-orange-200 rounded-xl p-6 space-y-4 max-w-2xl mx-auto">
          <div className="text-center">
            <div className="text-2xl mb-2">🚀</div>
            <h2 className="text-lg font-bold text-gray-900 mb-1">
              {heroContent.headline}
            </h2>
            <p className="text-sm text-gray-600 mb-4">
              {heroContent.description}
            </p>
            <Link
              href={`${base}/profile`}
              className="inline-flex items-center gap-2 px-6 py-3 bg-orange-500 hover:bg-orange-600 text-white text-sm font-medium rounded-lg transition-colors"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="12" y1="5" x2="12" y2="19" /><line x1="5" y1="12" x2="19" y2="12" />
              </svg>
              {heroContent.ctaLabel}
            </Link>
          </div>
          {/* Compact step indicator */}
          <CompactStepIndicator 
            isProfileComplete={onboardingState.isProfileComplete}
            isServiceComplete={onboardingState.isServiceComplete}
          />
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Leads - clickable link, locked during onboarding */}
        <Link href={`${base}/leads`} className={`relative block ${!isOnboardingComplete ? 'pointer-events-none' : ''}`}>
          <div className={`relative ${!isOnboardingComplete ? 'opacity-50' : ''}`}>
            {!isOnboardingComplete && (
              <div className="absolute inset-0 bg-white/80 rounded-lg flex items-center justify-center z-10 cursor-pointer"
                   onClick={() => router.push(`${base}/profile`)}>
                <div className="text-center">
                  <div className="text-2xl mb-1">🔒</div>
                  <p className="text-xs text-gray-600 font-medium">Add a service to unlock</p>
                </div>
              </div>
            )}
            <StatsCard
              title="Total Leads"
              value={stats?.total_leads ?? 0}
              icon={<LeadsIcon />}
            />
          </div>
        </Link>

        {/* New Leads - clickable link, locked during onboarding */}
        <Link href={`${base}/leads?status=new`} className={`relative block ${!isOnboardingComplete ? 'pointer-events-none' : ''}`}>
          <div className={`relative ${!isOnboardingComplete ? 'opacity-50' : ''}`}>
            {!isOnboardingComplete && (
              <div className="absolute inset-0 bg-white/80 rounded-lg flex items-center justify-center z-10 cursor-pointer"
                   onClick={() => router.push(`${base}/profile`)}>
                <div className="text-center">
                  <div className="text-2xl mb-1">🔒</div>
                  <p className="text-xs text-gray-600 font-medium">Add a service to unlock</p>
                </div>
              </div>
            )}
            <StatsCard
              title="New Leads"
              value={stats?.new_leads ?? 0}
              description="Awaiting action"
              icon={<NewLeadsIcon />}
              accent
            />
          </div>
        </Link>

        {/* Contacted - clickable link, locked during onboarding */}
        <Link href={`${base}/leads?status=contacted`} className={`relative block ${!isOnboardingComplete ? 'pointer-events-none' : ''}`}>
          <div className={`relative ${!isOnboardingComplete ? 'opacity-50' : ''}`}>
            {!isOnboardingComplete && (
              <div className="absolute inset-0 bg-white/80 rounded-lg flex items-center justify-center z-10 cursor-pointer"
                   onClick={() => router.push(`${base}/profile`)}>
                <div className="text-center">
                  <div className="text-2xl mb-1">🔒</div>
                  <p className="text-xs text-gray-600 font-medium">Add a service to unlock</p>
                </div>
              </div>
            )}
            <StatsCard
              title="Contacted"
              value={isOnboardingComplete ? (stats?.contacted_leads ?? 0) : MOTIVATIONAL_CONTACTED}
              description="Leads contacted"
              icon={<CheckIcon />}
            />
          </div>
        </Link>

        {/* Rating - non-clickable, shows motivational value during onboarding */}
        <div className={`relative ${!isOnboardingComplete ? 'opacity-50' : ''}`}>
          {!isOnboardingComplete && (
            <div className="absolute inset-0 bg-white/80 rounded-lg flex items-center justify-center z-10 cursor-pointer"
                 onClick={() => router.push(`${base}/profile`)}>
              <div className="text-center">
                <div className="text-2xl mb-1">🔒</div>
                <p className="text-xs text-gray-600 font-medium">Add a service to unlock</p>
              </div>
            </div>
          )}
          <StatsCard
            title="Rating"
            value={isOnboardingComplete 
              ? (stats?.rating !== undefined && stats.rating !== null ? stats.rating.toFixed(1) : '—')
              : MOTIVATIONAL_RATING
            }
            icon={<StarIcon />}
          />
        </div>
      </div>

      {/* Analytics preview */}
      <div className={`bg-white rounded-xl border border-gray-200 p-5 relative ${
        !isOnboardingComplete ? 'opacity-50' : ''
      }`}>
        {!isOnboardingComplete && (
          <div className="absolute inset-0 bg-white/80 rounded-xl flex items-center justify-center z-10 cursor-pointer"
               onClick={() => router.push(`${base}/profile`)}>
            <div className="text-center">
              <div className="text-3xl mb-2">🔒</div>
              <p className="text-sm text-gray-600 font-medium">Add a service to unlock analytics</p>
            </div>
          </div>
        )}
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-sm font-semibold text-gray-800">Last 30 days</h2>
          {isOnboardingComplete && (
            <Link
              href={`${base}/analytics`}
              className="text-xs text-orange-500 hover:text-orange-600 font-medium transition-colors"
            >
              View Analytics →
            </Link>
          )}
        </div>

        {analytics && analytics.total_leads === 0 ? (
          <p className="text-sm text-gray-400">No leads yet in the last 30 days.</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <p className="text-xs text-gray-500">Leads received</p>
              <p className="text-2xl font-bold text-gray-900 mt-0.5">
                {analytics?.total_leads ?? 0}
              </p>
            </div>
            <div>
              <p className="text-xs text-gray-500">Leads contacted</p>
              <p className="text-2xl font-bold text-gray-900 mt-0.5">
                {analytics?.contacted_leads ?? 0}
              </p>
            </div>
            <div>
              <p className="text-xs text-gray-500 mb-1.5">Top sources</p>
              {topSources.length > 0 ? (
                <div className="space-y-1">
                  {topSources.map(([src, count]) => (
                    <div key={src} className="flex items-center justify-between text-xs">
                      <span className="text-gray-600">{SOURCE_LABELS[src] ?? src}</span>
                      <span className="font-medium text-gray-800">{count}</span>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-gray-400">No data</p>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Reviews Preview - only show when onboarding is complete */}
      {isOnboardingComplete && reviewPreview && reviewPreview.has_reviews && (
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold text-gray-800">Latest Review</h2>
            <Link
              href={`${base}/reviews`}
              className="text-xs text-orange-500 hover:text-orange-600 font-medium transition-colors"
            >
              View All →
            </Link>
          </div>

          <div className="bg-gray-50 rounded-lg p-4">
            <div className="flex items-start justify-between mb-2">
              <div>
                <span className="font-medium text-gray-900">
                  {reviewPreview.latest_review?.client_name}
                </span>
                <div className="flex items-center gap-1 mt-1">
                  {[...Array(5)].map((_, i) => (
                    <svg
                      key={i}
                      width="12"
                      height="12"
                      viewBox="0 0 24 24"
                      fill={i < (reviewPreview.latest_review?.rating || 0) ? '#fbbf24' : 'none'}
                      stroke={i < (reviewPreview.latest_review?.rating || 0) ? 'none' : '#d1d5db'}
                      strokeWidth="2"
                    >
                      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
                    </svg>
                  ))}
                </div>
              </div>
              {!reviewPreview.latest_review?.has_reply && (
                <span className="px-2 py-1 bg-orange-100 text-orange-600 text-xs font-medium rounded-full">
                  Needs Reply
                </span>
              )}
            </div>

            {reviewPreview.latest_review?.comment_preview && (
              <p className="text-sm text-gray-600 italic mb-3">
                &ldquo;{reviewPreview.latest_review.comment_preview}&rdquo;
              </p>
            )}

            <p className="text-xs text-gray-400">
              {new Date(reviewPreview.latest_review?.created_at || '').toLocaleDateString()}
            </p>
          </div>

          {reviewPreview.unreplied_count > 0 && (
            <div className="mt-4 flex items-center justify-between bg-orange-50 rounded-lg p-3">
              <span className="text-sm text-orange-700">
                {reviewPreview.unreplied_count} review{reviewPreview.unreplied_count > 1 ? 's' : ''} waiting for your reply
              </span>
              <Link
                href={`${base}/reviews`}
                className="text-xs text-orange-600 hover:text-orange-700 font-medium"
              >
                Reply now →
              </Link>
            </div>
          )}
        </div>
      )}

      {/* Empty state for reviews */}
      {isOnboardingComplete && reviewPreview && !reviewPreview.has_reviews && (
        <div className="bg-gray-50 rounded-xl border border-gray-200 p-5 text-center">
          <div className="text-3xl mb-2">⭐</div>
          <h3 className="text-sm font-medium text-gray-900">No reviews yet</h3>
          <p className="text-xs text-gray-500 mt-1">
            When clients review your services, they will appear here
          </p>
        </div>
      )}
    </div>
  );
}
