'use client';

import { useState, useEffect } from 'react';
import LeadRow from '@/components/dashboard/LeadRow';
import EmptyState from '@/components/dashboard/EmptyState';
import type { Lead } from '@/types/provider';
import { getProviderLeads, updateLeadStatus } from '@/lib/provider-api';

export default function LeadsPage() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getProviderLeads()
      .then(setLeads)
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

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
        <h1 className="text-xl font-bold text-gray-900">Leads</h1>
        <p className="text-sm text-gray-500 mt-0.5">{leads.length} total</p>
      </div>

      {leads.length === 0 ? (
        <EmptyState
          title="No leads yet"
          description="Leads from clients will appear here once you start receiving inquiries."
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
