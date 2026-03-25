import StatusBadge from './StatusBadge';
import type { Lead } from '@/types/provider';

interface LeadRowProps {
  lead: Lead;
  onContact: (id: string) => void;
  onReject: (id: string) => void;
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  });
}

export default function LeadRow({ lead, onContact, onReject }: LeadRowProps) {
  const isTerminal = lead.status === 'done' || lead.status === 'rejected';
  const isContacted = lead.status === 'contacted';

  return (
    <tr className="border-b border-gray-100 hover:bg-gray-50 transition-colors">
      <td className="px-4 py-3 text-sm text-gray-500 whitespace-nowrap">
        {formatDate(lead.created_at)}
      </td>
      <td className="px-4 py-3 text-sm font-medium text-gray-900 whitespace-nowrap">
        {lead.phone}
      </td>
      <td className="px-4 py-3 text-sm text-gray-600 max-w-xs">
        <p className="truncate">{lead.description ?? '—'}</p>
      </td>
      <td className="px-4 py-3 text-sm text-gray-500 whitespace-nowrap">
        {lead.source ?? '—'}
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
                Contact
              </button>
            )}
            {isContacted && (
              <button
                onClick={() => onContact(lead.id)}
                className="px-3 py-1 text-xs font-medium bg-green-500 hover:bg-green-600 text-white rounded-lg transition-colors"
              >
                Done
              </button>
            )}
            <button
              onClick={() => onReject(lead.id)}
              className="px-3 py-1 text-xs font-medium border border-gray-300 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
            >
              Reject
            </button>
          </div>
        )}
      </td>
    </tr>
  );
}
