'use client';

import { useState, useEffect, useCallback } from 'react';
import { useSearchParams, useRouter, usePathname } from 'next/navigation';
import LeadRow from '@/components/dashboard/LeadRow';
import EmptyState from '@/components/dashboard/EmptyState';
import type { Lead, LeadStatusQuery, LeadsResponse } from '@/types/provider';
import { getProviderLeads, updateLeadStatus } from '@/lib/provider-api';

type PeriodOption = 'all' | '7' | '30' | '90';

const STATUS_OPTIONS: { value: LeadStatusQuery; label: string }[] = [
  { value: 'all', label: 'All' },
  { value: 'new', label: 'New' },
  { value: 'contacted', label: 'Contacted' },
  { value: 'done', label: 'Done' },
  { value: 'rejected', label: 'Rejected' },
];

const PERIOD_OPTIONS: { value: PeriodOption; label: string }[] = [
  { value: 'all', label: 'All time' },
  { value: '7', label: 'Last 7 days' },
  { value: '30', label: 'Last 30 days' },
  { value: '90', label: 'Last 90 days' },
];

function getTitleAndSubtitle(status: LeadStatusQuery | null, total: number): { title: string; subtitle: string } {
  switch (status) {
    case 'new':
      return { title: 'New leads', subtitle: `${total} total` };
    case 'contacted':
      return { title: 'Contacted leads', subtitle: `${total} total` };
    case 'done':
      return { title: 'Done leads', subtitle: `${total} total` };
    case 'rejected':
      return { title: 'Rejected leads', subtitle: `${total} total` };
    default:
      return { title: 'Leads', subtitle: `${total} total` };
  }
}

export default function LeadsPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();

  // Read filters from URL
  const urlStatus = (searchParams.get('status') as LeadStatusQuery) || 'all';
  const urlPeriod = (searchParams.get('period') as PeriodOption) || 'all';
  const urlDateFrom = searchParams.get('date_from') || '';
  const urlDateTo = searchParams.get('date_to') || '';

  const [leads, setLeads] = useState<Lead[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Local filter state (synced with URL)
  const [status, setStatus] = useState<LeadStatusQuery>(urlStatus);
  const [period, setPeriod] = useState<PeriodOption>(urlPeriod);
  const [dateFrom, setDateFrom] = useState(urlDateFrom);
  const [dateTo, setDateTo] = useState(urlDateTo);

  // Sync local state with URL changes
  useEffect(() => {
    setStatus(urlStatus);
    setPeriod(urlPeriod);
    setDateFrom(urlDateFrom);
    setDateTo(urlDateTo);
  }, [urlStatus, urlPeriod, urlDateFrom, urlDateTo]);

  // Fetch leads when filters change
  useEffect(() => {
    setLoading(true);
    getProviderLeads({
      status: status === 'all' ? undefined : status,
      period: period === 'all' ? undefined : period,
      date_from: dateFrom || undefined,
      date_to: dateTo || undefined,
    })
      .then((data: LeadsResponse) => {
        setLeads(data.leads);
        setTotal(data.total);
      })
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, [status, period, dateFrom, dateTo]);

  // Update URL when filters change (without triggering reload)
  const updateUrlParams = useCallback(
    (updates: Partial<{ status: LeadStatusQuery; period: PeriodOption; date_from: string; date_to: string }>) => {
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

  const { title, subtitle } = getTitleAndSubtitle(status, total);

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
        Failed to load leads: {error}
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
        <div className="flex flex-wrap gap-4">
          {/* Status filter */}
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-medium text-gray-500">Status</label>
            <div className="flex flex-wrap gap-2">
              {STATUS_OPTIONS.map((opt) => (
                <button
                  key={opt.value}
                  onClick={() => handleStatusChange(opt.value)}
                  className={`px-3 py-1.5 text-sm rounded-lg transition-colors ${
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
            <label className="text-xs font-medium text-gray-500">Period</label>
            <select
              value={period}
              onChange={(e) => handlePeriodChange(e.target.value as PeriodOption)}
              aria-label="Select period filter"
              className="px-3 py-1.5 text-sm border border-gray-200 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-orange-500"
            >
              {PERIOD_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>

          {/* Date range */}
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-medium text-gray-500">Date range</label>
            <div className="flex items-center gap-2">
              <input
                type="date"
                value={dateFrom}
                onChange={(e) => handleDateFromChange(e.target.value)}
                className="px-3 py-1.5 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                placeholder="From"
              />
              <span className="text-gray-400">-</span>
              <input
                type="date"
                value={dateTo}
                onChange={(e) => handleDateToChange(e.target.value)}
                className="px-3 py-1.5 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                placeholder="To"
              />
            </div>
          </div>
        </div>
      </div>

      {leads.length === 0 ? (
        <EmptyState
          title="No leads found"
          description="Try adjusting your filters or check back later."
        />
      ) : (
        <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-gray-100 bg-gray-50">
                  <th className="px-4 py-3 text-xs font-medium text-gray-500 uppercase tracking-wide whitespace-nowrap">Date</th>
                  <th className="px-4 py-3 text-xs font-medium text-gray-500 uppercase tracking-wide whitespace-nowrap">Phone</th>
                  <th className="px-4 py-3 text-xs font-medium text-gray-500 uppercase tracking-wide">Description</th>
                  <th className="px-4 py-3 text-xs font-medium text-gray-500 uppercase tracking-wide whitespace-nowrap">Source</th>
                  <th className="px-4 py-3 text-xs font-medium text-gray-500 uppercase tracking-wide whitespace-nowrap">Status</th>
                  <th className="px-4 py-3 text-xs font-medium text-gray-500 uppercase tracking-wide whitespace-nowrap">Actions</th>
                </tr>
              </thead>
              <tbody>
                {leads.map(lead => (
                  <LeadRow
                    key={lead.id}
                    lead={lead}
                    onContact={handleContact}
                    onReject={handleReject}
                  />
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
