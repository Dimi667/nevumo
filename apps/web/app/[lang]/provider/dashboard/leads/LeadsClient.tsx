'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { useSearchParams, useRouter, usePathname } from 'next/navigation';
import LeadRow from '@/components/dashboard/LeadRow';
import LeadDetailModal from '@/components/dashboard/LeadDetailModal';
import EmptyState from '@/components/dashboard/EmptyState';
import { useDashboardI18n } from '@/lib/provider-dashboard-i18n';
import type { Lead, LeadStatusQuery, LeadsResponse } from '@/types/provider';
import { getProviderLeads, updateLeadStatus } from '@/lib/provider-api';

type PeriodOption = 'all' | '7' | '30' | '90';

function getStatusOptions(t: (key: string, fallback?: string) => string): { value: LeadStatusQuery; label: string }[] {
  return [
    { value: 'all', label: t('status_all', 'All') },
    { value: 'new', label: t('status_new', 'New') },
    { value: 'contacted', label: t('status_contacted', 'Contacted') },
    { value: 'done', label: t('status_done', 'Done') },
    { value: 'rejected', label: t('status_rejected', 'Rejected') },
  ];
}

function getPeriodOptions(t: (key: string, fallback?: string) => string): { value: PeriodOption; label: string }[] {
  return [
    { value: 'all', label: t('period_all_time', 'All time') },
    { value: '7', label: t('period_last_7_days', 'Last 7 days') },
    { value: '30', label: t('period_last_30_days', 'Last 30 days') },
    { value: '90', label: t('period_last_90_days', 'Last 90 days') },
  ];
}

function getTitleAndSubtitle(status: LeadStatusQuery | null, total: number, t: (key: string, fallback?: string) => string): { title: string; subtitle: string } {
  switch (status) {
    case 'new':
      return { title: t('label_new_leads', 'New leads'), subtitle: `${total} ${t('label_total', 'total')}` };
    case 'contacted':
      return { title: t('label_contacted_leads', 'Contacted leads'), subtitle: `${total} ${t('label_total', 'total')}` };
    case 'done':
      return { title: t('label_done_leads', 'Done leads'), subtitle: `${total} ${t('label_total', 'total')}` };
    case 'rejected':
      return { title: t('label_rejected_leads', 'Rejected leads'), subtitle: `${total} ${t('label_total', 'total')}` };
    default:
      return { title: t('nav_leads', 'Leads'), subtitle: `${total} ${t('label_total', 'total')}` };
  }
}

export default function LeadsClient() {
  const { t, lang } = useDashboardI18n();
  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();

  // Read filters from URL
  const urlStatus = (searchParams.get('status') as LeadStatusQuery) || 'all';
  const urlPeriod = (searchParams.get('period') as PeriodOption) || 'all';
  const urlDateFrom = searchParams.get('date_from') || '';
  const urlDateTo = searchParams.get('date_to') || '';
  const urlSearch = searchParams.get('search') || '';

  const [leads, setLeads] = useState<Lead[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Local filter state (synced with URL)
  const [status, setStatus] = useState<LeadStatusQuery>(urlStatus);
  const [period, setPeriod] = useState<PeriodOption>(urlPeriod);
  const [dateFrom, setDateFrom] = useState(urlDateFrom);
  const [dateTo, setDateTo] = useState(urlDateTo);
  const [search, setSearch] = useState(urlSearch);

  // Local input state for search (not synced with URL, debounced)
  const [searchInput, setSearchInput] = useState(urlSearch);
  const [isSearching, setIsSearching] = useState(false);

  // Update document title when translations are loaded
  useEffect(() => {
    const title = t('nav_leads', 'Leads');
    document.title = `${title} - Nevumo`;
  }, [t]);

  // Modal state
  const [selectedLead, setSelectedLead] = useState<Lead | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Debounce ref for search
  const searchDebounceRef = useRef<NodeJS.Timeout | null>(null);

  // Sync local state with URL changes
  useEffect(() => {
    setStatus(urlStatus);
    setPeriod(urlPeriod);
    setDateFrom(urlDateFrom);
    setDateTo(urlDateTo);
    setSearch(urlSearch);
  }, [urlStatus, urlPeriod, urlDateFrom, urlDateTo, urlSearch]);

  // Fetch leads when filters change
  useEffect(() => {
    setLoading(true);
    setIsSearching(true);
    getProviderLeads({
      status: status === 'all' ? undefined : status,
      period: period === 'all' ? undefined : period,
      date_from: dateFrom || undefined,
      date_to: dateTo || undefined,
      search: search || undefined,
    })
      .then((data: LeadsResponse) => {
        setLeads(data.leads);
        setTotal(data.total);
      })
      .catch((e: Error) => setError(e.message))
      .finally(() => {
        setLoading(false);
        setIsSearching(false);
      });
  }, [status, period, dateFrom, dateTo, search]);

  // Update URL when filters change (without triggering reload)
  const updateUrlParams = useCallback(
    (updates: Partial<{ status: LeadStatusQuery; period: PeriodOption; date_from: string; date_to: string; search: string }>) => {
      const params = new URLSearchParams(searchParams.toString());

      if (updates.status !== undefined) {
        if (updates.status === 'all') {
          params.delete('status');
        } else {
          params.set('status', updates.status);
        }
      }

      if (updates.period !== undefined) {
        if (updates.period === 'all') {
          params.delete('period');
        } else {
          params.set('period', updates.period);
        }
      }

      if (updates.date_from !== undefined) {
        if (updates.date_from) {
          params.set('date_from', updates.date_from);
        } else {
          params.delete('date_from');
        }
      }

      if (updates.date_to !== undefined) {
        if (updates.date_to) {
          params.set('date_to', updates.date_to);
        } else {
          params.delete('date_to');
        }
      }

      if (updates.search !== undefined) {
        if (updates.search) {
          params.set('search', updates.search);
        } else {
          params.delete('search');
        }
      }

      router.replace(`${pathname}?${params.toString()}`, { scroll: false });
    },
    [searchParams, router, pathname]
  );

  const handleStatusChange = (newStatus: LeadStatusQuery) => {
    setStatus(newStatus);
    updateUrlParams({ status: newStatus });
  };

  const handlePeriodChange = (newPeriod: PeriodOption) => {
    setPeriod(newPeriod);
    // Clear date range when selecting a preset period
    if (newPeriod !== 'all') {
      setDateFrom('');
      setDateTo('');
      updateUrlParams({ period: newPeriod, date_from: '', date_to: '' });
    } else {
      updateUrlParams({ period: newPeriod });
    }
  };

  const handleDateFromChange = (value: string) => {
    setDateFrom(value);
    // Clear period preset when setting custom date
    if (value) {
      setPeriod('all');
      updateUrlParams({ date_from: value, period: 'all' });
    } else {
      updateUrlParams({ date_from: value });
    }
  };

  const handleDateToChange = (value: string) => {
    setDateTo(value);
    // Clear period preset when setting custom date
    if (value) {
      setPeriod('all');
      updateUrlParams({ date_to: value, period: 'all' });
    } else {
      updateUrlParams({ date_to: value });
    }
  };

  // Handle search input with debounce
  const handleSearchChange = (value: string) => {
    setSearchInput(value);

    // Clear previous debounce timer
    if (searchDebounceRef.current) {
      clearTimeout(searchDebounceRef.current);
    }

    // Set new debounce timer (500ms)
    searchDebounceRef.current = setTimeout(() => {
      setSearch(value);
      updateUrlParams({ search: value });
    }, 500);
  };

  // Sync searchInput when URL changes (e.g., back button, initial load)
  useEffect(() => {
    setSearchInput(urlSearch);
  }, [urlSearch]);

  // Cleanup debounce on unmount
  useEffect(() => {
    return () => {
      if (searchDebounceRef.current) {
        clearTimeout(searchDebounceRef.current);
      }
    };
  }, []);

  // Modal handlers
  const handleViewLead = (lead: Lead) => {
    setSelectedLead(lead);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedLead(null);
  };

  const handleNotesSaved = (leadId: string, notes: string | null) => {
    setLeads(prev => prev.map(l => l.id === leadId ? { ...l, provider_notes: notes } : l));
  };

  async function handleContact(id: string) {
    const lead = leads.find(l => l.id === id);
    if (!lead) return;
    const nextStatus = lead.status === 'contacted' ? 'done' : 'contacted';
    try {
      await updateLeadStatus(id, nextStatus);
      setLeads(prev => prev.map(l => l.id === id ? { ...l, status: nextStatus } : l));
    } catch {
      // silently ignore — row stays unchanged
    }
  }

  async function handleReject(id: string) {
    try {
      await updateLeadStatus(id, 'rejected');
      setLeads(prev => prev.map(l => l.id === id ? { ...l, status: 'rejected' } : l));
    } catch {
      // silently ignore
    }
  }

  const { title, subtitle } = getTitleAndSubtitle(status, total, t);

  // Handle initial loading state (first load only)
  if (loading && leads.length === 0) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 text-red-700 rounded-xl p-4 text-sm">
        {t('msg_failed_load_leads', 'Failed to load leads')}: {error}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-xl font-bold text-gray-900">{title}</h1>
        <p className="text-sm text-gray-500 mt-0.5">{subtitle}</p>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-xl border border-gray-200 p-4 space-y-4">
        {/* Search bar */}
        <div className="w-full">
          <label className="text-xs font-medium text-gray-500 mb-1.5 block">{t('label_search', 'Search')}</label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg className="h-4 w-4 text-gray-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="11" cy="11" r="8" />
                <line x1="21" y1="21" x2="16.65" y2="16.65" />
              </svg>
            </div>
            <input
              type="text"
              value={searchInput}
              onChange={(e) => handleSearchChange(e.target.value)}
              placeholder={t('placeholder_search_leads', 'Search name, email, phone, description or notes...')}
              className="w-full pl-10 pr-10 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
            />
            {isSearching ? (
              <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                <div className="w-4 h-4 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
              </div>
            ) : searchInput && (
              <button
                onClick={() => handleSearchChange('')}
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
                aria-label={t('clear_search', 'Clear search')}
              >
                <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <line x1="18" y1="6" x2="6" y2="18" />
                  <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
              </button>
            )}
          </div>
        </div>

        <div className="flex flex-wrap items-start gap-6">
          {/* Status filter */}
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-medium text-gray-500">{t('label_status', 'Status')}</label>
            <div className="flex flex-wrap gap-2">
              {getStatusOptions(t).map((opt) => (
                <button
                  key={opt.value}
                  onClick={() => handleStatusChange(opt.value)}
                  className={`px-3 py-1.5 text-sm rounded-lg transition-colors h-[34px] ${
                    status === opt.value
                      ? 'bg-orange-500 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {opt.label}
                </button>
              ))}
            </div>
          </div>

          {/* Period filter */}
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-medium text-gray-500">{t('label_period', 'Period')}</label>
            <select
              value={period}
              onChange={(e) => handlePeriodChange(e.target.value as PeriodOption)}
              aria-label={t('aria_select_period_filter', 'Select period filter')}
              className="px-3 py-1.5 text-sm border border-gray-200 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-orange-500 h-[34px]"
            >
              {getPeriodOptions(t).map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>

          {/* Date range */}
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-medium text-gray-500">{t('label_date_range', 'Date range')}</label>
            <div className="flex items-center gap-2">
              <input
                type="date"
                value={dateFrom}
                onChange={(e) => handleDateFromChange(e.target.value)}
                className="px-3 py-1.5 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 h-[34px]"
                placeholder={t('placeholder_from', 'From')}
              />
              <span className="text-gray-400">-</span>
              <input
                type="date"
                value={dateTo}
                onChange={(e) => handleDateToChange(e.target.value)}
                className="px-3 py-1.5 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 h-[34px]"
                placeholder={t('placeholder_to', 'To')}
              />
            </div>
          </div>
        </div>
      </div>

      {leads.length === 0 ? (
        <EmptyState
          title={t('msg_no_leads_found', 'No leads found')}
          description={t('msg_adjust_filters', 'Try adjusting your filters or check back later.')}
        />
      ) : (
        <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-gray-100 bg-gray-50">
                  <th className="px-4 py-3 text-xs font-medium text-gray-500 uppercase tracking-wide whitespace-nowrap">{t('label_date', 'Date')}</th>
                  <th className="px-4 py-3 text-xs font-medium text-gray-500 uppercase tracking-wide whitespace-nowrap">{t('label_phone', 'Phone')}</th>
                  <th className="px-4 py-3 text-xs font-medium text-gray-500 uppercase tracking-wide">{t('label_description', 'Description')}</th>
                  <th className="px-4 py-3 text-xs font-medium text-gray-500 uppercase tracking-wide whitespace-nowrap">{t('label_source', 'Source')}</th>
                  <th className="px-4 py-3 text-xs font-medium text-gray-500 uppercase tracking-wide whitespace-nowrap">{t('label_notes', 'Notes')}</th>
                  <th className="px-4 py-3 text-xs font-medium text-gray-500 uppercase tracking-wide whitespace-nowrap">{t('label_status', 'Status')}</th>
                  <th className="px-4 py-3 text-xs font-medium text-gray-500 uppercase tracking-wide whitespace-nowrap">{t('label_actions', 'Actions')}</th>
                </tr>
              </thead>
              <tbody>
                {leads.map(lead => (
                  <LeadRow
                    key={lead.id}
                    lead={lead}
                    onContact={handleContact}
                    onReject={handleReject}
                    onView={handleViewLead}
                  />
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Lead Detail Modal */}
      <LeadDetailModal
        lead={selectedLead}
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        onNotesSaved={handleNotesSaved}
      />
    </div>
  );
}
