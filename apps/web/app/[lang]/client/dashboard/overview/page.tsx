'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import StatsCard from '@/components/dashboard/StatsCard';
import { getAuthToken } from '@/lib/auth-store';
import {
  getClientDashboard,
  type ClientDashboardData,
  type ClientLeadStatus,
} from '@/lib/client-api';
import { fetchTranslations, t, type TranslationDict } from '@/lib/ui-translations';

function ActiveRequestsIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
      <circle cx="9" cy="7" r="4" />
      <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
      <path d="M16 3.13a4 4 0 0 1 0 7.75" />
    </svg>
  );
}

function CompletedServicesIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9 12l2 2 4-4" />
      <path d="M21 12c0 4.97-4.03 9-9 9s-9-4.03-9-9 4.03-9 9-9 9 4.03 9 9Z" />
    </svg>
  );
}

function ReviewsIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
    </svg>
  );
}

function formatDate(value: string, locale: string): string {
  const date = new Date(value);

  try {
    return new Intl.DateTimeFormat(locale, {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
    }).format(date);
  } catch {
    return date.toLocaleDateString();
  }
}

function getStatusMeta(status: ClientLeadStatus, dict: TranslationDict): { label: string; className: string } {
  if (status === 'done') {
    return {
      label: t(dict, 'status_completed', 'Completed'),
      className: 'bg-green-100 text-green-700',
    };
  }

  if (status === 'rejected' || status === 'expired' || status === 'cancelled') {
    return {
      label: t(dict, 'status_rejected', 'Rejected'),
      className: 'bg-gray-100 text-gray-600',
    };
  }

  return {
    label: t(dict, 'status_active', 'Active'),
    className: 'bg-orange-100 text-orange-700',
  };
}

export default function ClientOverviewPage() {
  const params = useParams();
  const lang = typeof params.lang === 'string' ? params.lang : 'en';

  const [data, setData] = useState<ClientDashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [dict, setDict] = useState<TranslationDict>({});

  useEffect(() => {
    async function loadDashboard() {
      const token = getAuthToken();

      if (!token) {
        setError('Липсва активна сесия.');
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError(null);
        const dashboard = await getClientDashboard(token);
        setData(dashboard);
      } catch (e: unknown) {
        setError(e instanceof Error ? e.message : 'Неуспешно зареждане на dashboard.');
      } finally {
        setLoading(false);
      }
    }

    void loadDashboard();
  }, []);

  useEffect(() => {
    async function loadTranslations() {
      const translations = await fetchTranslations(lang, 'client_dashboard');
      setDict(translations);
    }

    void loadTranslations();
  }, [lang]);

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
        {error}
      </div>
    );
  }

  const stats = data?.stats;
  const recentLeads = data?.recent_leads ?? [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-gray-900">{t(dict, 'overview_title', 'Overview')}</h1>
        <p className="text-sm text-gray-500 mt-0.5">{t(dict, 'overview_subtitle', 'Overview of your requests and reviews')}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        <Link
          href={`/${lang}/client/dashboard/requests?status=active`}
          className="cursor-pointer hover:ring-2 hover:ring-orange-400 transition rounded-xl block"
        >
          <StatsCard
            title={t(dict, 'stat_active_requests', 'Active Requests')}
            value={stats?.active_leads ?? 0}
            icon={<ActiveRequestsIcon />}
            accent
          />
        </Link>
        <Link
          href={`/${lang}/client/dashboard/requests?status=done`}
          className="cursor-pointer hover:ring-2 hover:ring-orange-400 transition rounded-xl block"
        >
          <StatsCard
            title={t(dict, 'stat_completed_services', 'Completed Services')}
            value={stats?.completed_leads ?? 0}
            icon={<CompletedServicesIcon />}
            accent
          />
        </Link>
        <Link
          href={`/${lang}/client/dashboard/reviews`}
          className="cursor-pointer hover:ring-2 hover:ring-orange-400 transition rounded-xl block"
        >
          <StatsCard
            title={t(dict, 'stat_reviews', 'Reviews')}
            value={stats?.reviews_written ?? 0}
            icon={<ReviewsIcon />}
            accent
          />
        </Link>
      </div>

      {recentLeads.length === 0 ? (
        <div className="bg-gradient-to-r from-orange-50 to-orange-100 border border-orange-200 rounded-xl p-6 md:p-8 text-center space-y-4">
          <div className="space-y-1.5">
            <h2 className="text-xl font-bold text-gray-900">{t(dict, 'empty_requests_title', 'No requests yet')}</h2>
            <p className="text-sm text-gray-600 max-w-xl mx-auto">
              {t(dict, 'empty_requests_desc', 'Browse available services...')}
            </p>
          </div>
          <Link
            href={`/${lang}`}
            className="inline-flex items-center gap-2 px-4 py-2.5 bg-orange-500 hover:bg-orange-600 text-white text-sm font-medium rounded-lg transition-colors"
          >
            {t(dict, 'cta_find_service', 'Find Service')}
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          <div>
            <h2 className="text-lg font-semibold text-gray-900">{t(dict, 'recent_title', 'Recent Requests')}</h2>
            <p className="text-sm text-gray-500 mt-0.5">{t(dict, 'recent_subtitle', 'Your latest activity in Nevumo')}</p>
          </div>
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
            {recentLeads.map((lead) => {
              const statusMeta = getStatusMeta(lead.status, dict);

              return (
                <div key={lead.id} className="bg-white rounded-xl border border-gray-200 p-5 space-y-4">
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <h3 className="text-base font-semibold text-gray-900">{lead.category_name}</h3>
                      <p className="text-sm text-gray-500 mt-0.5">{lead.city}</p>
                    </div>
                    <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${statusMeta.className}`}>
                      {statusMeta.label}
                    </span>
                  </div>
                  <div className="space-y-1">
                    <p className="text-xs uppercase tracking-wide text-gray-400 font-medium">{t(dict, 'label_provider', 'Provider')}</p>
                    <p className="text-sm text-gray-700">
                      {lead.provider_business_name || t(dict, 'label_marketplace', 'Marketplace Request')}
                    </p>
                  </div>
                  <div className="space-y-1">
                    <p className="text-xs uppercase tracking-wide text-gray-400 font-medium">{t(dict, 'label_date', 'Date')}</p>
                    <p className="text-sm text-gray-700">{formatDate(lead.created_at, lang)}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
