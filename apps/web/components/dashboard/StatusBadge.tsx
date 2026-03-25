import type { AvailabilityStatus, LeadStatus } from '@/types/provider';

type BadgeStatus = LeadStatus | AvailabilityStatus | 'invited';

const CONFIG: Record<BadgeStatus, { label: string; className: string }> = {
  created:   { label: 'New',       className: 'bg-blue-50 text-blue-700' },
  contacted: { label: 'Contacted', className: 'bg-orange-50 text-orange-700' },
  done:      { label: 'Done',      className: 'bg-green-50 text-green-700' },
  rejected:  { label: 'Rejected',  className: 'bg-red-50 text-red-600' },
  invited:   { label: 'New',       className: 'bg-blue-50 text-blue-700' },
  active:    { label: 'Active',    className: 'bg-green-50 text-green-700' },
  busy:      { label: 'Busy',      className: 'bg-yellow-50 text-yellow-700' },
  offline:   { label: 'Offline',   className: 'bg-gray-100 text-gray-500' },
};

interface StatusBadgeProps {
  status: BadgeStatus;
}

export default function StatusBadge({ status }: StatusBadgeProps) {
  const cfg = CONFIG[status] ?? { label: status, className: 'bg-gray-100 text-gray-500' };
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${cfg.className}`}>
      {cfg.label}
    </span>
  );
}
