'use client';

import StatusBadge from './StatusBadge';
import { formatDashboardDate, useDashboardI18n } from '@/lib/provider-dashboard-i18n';
import { t } from '@/lib/ui-translations';
import type { Lead } from '@/types/provider';

interface LeadRowProps {
  lead: Lead;
  onContact: (id: string) => void;
  onReject: (id: string) => void;
}

function getSourceLabel(source: string, dict: Record<string, string>): string {
  switch (source) {
    case 'seo':
      return t(dict, 'label_source_seo', 'SEO');
    case 'widget':
      return t(dict, 'label_source_widget', 'Widget');
    case 'qr':
      return t(dict, 'label_source_qr', 'QR Code');
    case 'direct':
      return t(dict, 'label_source_direct', 'Direct');
    case 'other':
      return t(dict, 'label_source_other', 'Other');
    default:
      return source;
  }
}

export default function LeadRow({ lead, onContact, onReject }: LeadRowProps) {
  const { dict, lang } = useDashboardI18n();
  const isTerminal = lead.status === 'done' || lead.status === 'rejected';
  const isContacted = lead.status === 'contacted';

  return (
    <tr className="border-b border-gray-100 hover:bg-gray-50 transition-colors">
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
        {lead.source ? getSourceLabel(lead.source, dict) : '—'}
      </td>
      <td className="px-4 py-3">
        <StatusBadge status={lead.status} />
      </td>
      <td className="px-4 py-3">
        {!isTerminal && (
          <div className="flex items-center gap-2">
            {!isContacted && (
              <button
                onClick={() => onContact(lead.id)}
                className="px-3 py-1 text-xs font-medium bg-orange-500 hover:bg-orange-600 text-white rounded-lg transition-colors"
              >
                {t(dict, 'btn_contact', 'Contact')}
              </button>
            )}
            {isContacted && (
              <button
                onClick={() => onContact(lead.id)}
                className="px-3 py-1 text-xs font-medium bg-green-500 hover:bg-green-600 text-white rounded-lg transition-colors"
              >
                {t(dict, 'status_done', 'Done')}
              </button>
            )}
            <button
              onClick={() => onReject(lead.id)}
              className="px-3 py-1 text-xs font-medium border border-gray-300 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
            >
              {t(dict, 'btn_reject', 'Reject')}
            </button>
          </div>
        )}
      </td>
    </tr>
  );
}
