'use client';

import StatusBadge from './StatusBadge';
import { formatDashboardDate, useDashboardI18n } from '@/lib/provider-dashboard-i18n';
import type { Lead } from '@/types/provider';

interface LeadRowProps {
  lead: Lead;
  onContact: (id: string) => void;
  onReject: (id: string) => void;
  onView?: (lead: Lead) => void;
  updatingIds: Set<string>;
}

function getSourceLabel(source: string, t: (key: string, fallback?: string) => string): string {
  switch (source) {
    case 'seo':
      return t('label_source_seo', 'SEO');
    case 'widget':
      return t('label_source_widget', 'Widget');
    case 'qr':
      return t('label_source_qr', 'QR Code');
    case 'direct':
      return t('label_source_direct', 'Direct');
    case 'other':
      return t('label_source_other', 'Other');
    default:
      return source;
  }
}

export default function LeadRow({ lead, onContact, onReject, onView, updatingIds }: LeadRowProps) {
  const { t, lang } = useDashboardI18n();
  const isTerminal = lead.status === 'done' || lead.status === 'rejected' || (lead.status as string) === 'cancelled';
  const isContacted = lead.status === 'contacted';
  const isUpdating = updatingIds.has(lead.id);

  const getStatusMeta = (status: string, cancelledBy?: string | null) => {
    if (status === 'cancelled') {
      return {
        label: cancelledBy === 'client'
          ? t('status_label_cancelled_by_client', 'Client cancelled')
          : t('status_label_cancelled_by_provider', 'Cancelled'),
        className: 'bg-red-50 text-red-600'
      };
    }
    return null;
  };

  const statusMeta = getStatusMeta(lead.status, (lead as any).cancelled_by);

  const handleRowClick = () => {
    onView?.(lead);
  };

  return (
    <tr
      className="border-b border-gray-100 hover:bg-gray-50 transition-colors cursor-pointer"
      onClick={handleRowClick}
    >
      <td className="px-4 py-3 text-sm text-gray-500 whitespace-nowrap">
        {formatDashboardDate(lead.created_at, lang)}
      </td>
      <td className="px-4 py-3 text-sm font-medium text-gray-900 whitespace-nowrap">
        {lead.phone}
      </td>
      <td className="px-4 py-3 text-sm text-gray-600 max-w-xs">
        <p className="truncate">{lead.description ?? '—'}</p>
      </td>
      <td className="px-4 py-3 text-sm text-gray-500 whitespace-nowrap">
        {lead.source ? getSourceLabel(lead.source, t) : '—'}
      </td>
      <td className="px-4 py-3 text-sm text-gray-600 max-w-xs">
        {lead.provider_notes ? (
          <div className="flex items-center gap-1.5">
            <span>📝</span>
            <span className="truncate">{lead.provider_notes.slice(0, 40)}</span>
          </div>
        ) : (
          <span className="text-gray-300">—</span>
        )}
      </td>
      <td className="px-4 py-3">
        {statusMeta ? (
          <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${statusMeta.className}`}>
            {statusMeta.label}
          </span>
        ) : (
          <StatusBadge status={lead.status} />
        )}
      </td>
      <td className="px-4 py-3">
        <div className="flex items-center gap-2">
          {/* View button */}
          <button
            onClick={(e) => {
              e.stopPropagation();
              onView?.(lead);
            }}
            className="px-3 py-1 text-xs font-medium bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors"
            title={t('btn_view', 'View')}
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
              <circle cx="12" cy="12" r="3" />
            </svg>
          </button>

          {!isTerminal && (
            <>
              {!isContacted && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onContact(lead.id);
                  }}
                  disabled={isUpdating}
                  className="px-3 py-1 text-xs font-medium bg-orange-500 hover:bg-orange-600 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {t('btn_contact', 'Contact')}
                </button>
              )}
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onReject(lead.id);
                }}
                disabled={isUpdating}
                className="px-3 py-1 text-xs font-medium border border-gray-300 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {t('btn_reject', 'Reject')}
              </button>
            </>
          )}
        </div>
      </td>
    </tr>
  );
}
