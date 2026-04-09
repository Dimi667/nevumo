'use client';

import { useState, useEffect, useCallback } from 'react';
import { useDashboardI18n } from '@/lib/provider-dashboard-i18n';
import type { AnalyticsData } from '@/types/provider';
import { getProviderAnalytics } from '@/lib/provider-api';
import { t, type TranslationDict } from '@/lib/ui-translations';

function getSourceLabels(dict: TranslationDict): Record<string, string> {
  return {
    seo: t(dict, 'label_source_seo', 'SEO'),
    widget: t(dict, 'label_source_widget', 'Widget'),
    qr: t(dict, 'label_source_qr', 'QR Code'),
    direct: t(dict, 'label_source_direct', 'Direct'),
    other: t(dict, 'label_source_other', 'Other'),
  };
}

const SOURCE_COLORS: Record<string, string> = {
  seo: 'bg-orange-500',
  widget: 'bg-blue-500',
  qr: 'bg-purple-500',
  direct: 'bg-green-500',
  other: 'bg-gray-400',
};

type Period = 7 | 30;

export default function AnalyticsPage() {
   const { dict } = useDashboardI18n();

  const [period, setPeriod] = useState<Period>(30);
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback((p: Period) => {
    setLoading(true);
    setError(null);
    getProviderAnalytics(p)
      .then(setData)
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    fetchData(period);
  }, [fetchData, period]);

  const sourceLabels = getSourceLabels(dict);
  const maxSourceCount = data
    ? Math.max(...Object.values(data.sources), 1)
    : 1;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div>
          <h1 className="text-xl font-bold text-gray-900">{t(dict, 'nav_analytics', 'Analytics')}</h1>
          <p className="text-sm text-gray-500 mt-0.5">{t(dict, 'analytics_subtitle', 'Lead performance overview')}</p>
        </div>

        {/* Period toggle */}
        <div className="flex items-center gap-1 bg-gray-100 rounded-lg p-1 self-start sm:self-auto">
          {([7, 30] as Period[]).map(p => (
            <button
              key={p}
              onClick={() => setPeriod(p)}
              className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${
                period === p
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              {t(dict, 'label_last_x_days', 'Last {p} days').replace('{p}', String(p))}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-20">
          <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : error ? (
        <div className="bg-red-50 text-red-700 rounded-xl p-4 text-sm">
          {t(dict, 'msg_failed_load_analytics', 'Failed to load analytics')}: {error}
        </div>
      ) : data?.total_leads === 0 ? (
        <div className="bg-white rounded-xl border border-gray-200 p-10 text-center">
          <div className="w-14 h-14 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-4">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="text-gray-400">
              <line x1="18" y1="20" x2="18" y2="10" /><line x1="12" y1="20" x2="12" y2="4" />
              <line x1="6" y1="20" x2="6" y2="14" />
            </svg>
          </div>
          <h3 className="text-base font-semibold text-gray-800 mb-1">{t(dict, 'msg_no_leads_yet', 'No leads yet')}</h3>
          <p className="text-sm text-gray-500 max-w-xs mx-auto">
            {t(dict, 'msg_analytics_appear_when_leads', 'Analytics will appear once you start receiving leads.')}
          </p>
        </div>
      ) : (
        <>
          {/* KPI cards */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="bg-white rounded-xl border border-gray-200 p-5">
              <p className="text-xs text-gray-500 uppercase tracking-wide font-medium">{t(dict, 'stat_leads_received', 'Leads Received')}</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{data?.total_leads ?? 0}</p>
            </div>
            <div className="bg-white rounded-xl border border-gray-200 p-5">
              <p className="text-xs text-gray-500 uppercase tracking-wide font-medium">{t(dict, 'stat_leads_contacted', 'Leads Contacted')}</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{data?.contacted_leads ?? 0}</p>
            </div>
            <div className="bg-white rounded-xl border border-orange-100 bg-orange-50 p-5">
              <p className="text-xs text-orange-600 uppercase tracking-wide font-medium">{t(dict, 'stat_conversion_rate', 'Conversion Rate')}</p>
              <p className="text-3xl font-bold text-orange-600 mt-2">{data?.conversion_rate ?? 0}%</p>
            </div>
          </div>

          {/* Lead sources breakdown */}
          <div className="bg-white rounded-xl border border-gray-200 p-5">
            <h2 className="text-sm font-semibold text-gray-800 mb-5">{t(dict, 'label_lead_sources', 'Lead Sources')}</h2>
            <div className="space-y-4">
              {(['seo', 'widget', 'qr', 'direct', 'other'] as const).map(src => {
                const count = data?.sources[src] ?? 0;
                const pct = maxSourceCount > 0 ? Math.round(count / maxSourceCount * 100) : 0;
                return (
                  <div key={src}>
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="text-sm text-gray-700 font-medium">{sourceLabels[src]}</span>
                      <span className="text-sm font-semibold text-gray-900">{count}</span>
                    </div>
                    <div className="w-full bg-gray-100 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full transition-all duration-500 ${SOURCE_COLORS[src]}`}
                        style={{ width: `${pct}%` }}
                      ></div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
