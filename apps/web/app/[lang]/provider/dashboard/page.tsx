'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useParams, useRouter } from 'next/navigation';
import StatsCard from '@/components/dashboard/StatsCard';
import type { DashboardResponse } from '@/types/provider';
import { getProviderDashboard } from '@/lib/provider-api';

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

export default function DashboardOverviewPage() {
  const params = useParams();
  const router = useRouter();
  const lang = typeof params.lang === 'string' ? params.lang : 'en';
  const base = `/${lang}/provider/dashboard`;

  const [data, setData] = useState<DashboardResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getProviderDashboard()
      .then(d => {
        if (!d.profile.is_complete) {
          router.push(`/${lang}/provider/dashboard/profile`);
          return;
        }
        setData(d);
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

      {profile && !profile.is_complete && profile.missing_fields && profile.missing_fields.length > 0 && (
        <div className="bg-orange-50 border border-orange-200 rounded-xl p-4">
          <p className="text-sm font-medium text-orange-700">Complete your profile</p>
          <p className="text-xs text-orange-600 mt-1">
            Missing: {profile.missing_fields.join(', ')}
          </p>
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard
          title="Total Leads"
          value={stats?.total_leads ?? 0}
          icon={<LeadsIcon />}
        />
        <StatsCard
          title="New Leads"
          value={stats?.new_leads ?? 0}
          description="Awaiting action"
          icon={<NewLeadsIcon />}
          accent
        />
        <StatsCard
          title="Rating"
          value={stats?.rating !== undefined && stats.rating !== null ? stats.rating.toFixed(1) : '—'}
          icon={<StarIcon />}
        />
        <StatsCard
          title="Accepted"
          value={stats?.accepted_matches ?? 0}
          description="Completed matches"
          icon={<CheckIcon />}
        />
      </div>

      {/* Analytics preview */}
      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-sm font-semibold text-gray-800">Last 30 days</h2>
          <Link
            href={`${base}/analytics`}
            className="text-xs text-orange-500 hover:text-orange-600 font-medium transition-colors"
          >
            View Analytics →
          </Link>
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
    </div>
  );
}
