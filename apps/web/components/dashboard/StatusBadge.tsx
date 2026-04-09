'use client';

import { useDashboardI18n } from '@/lib/provider-dashboard-i18n';
import { t } from '@/lib/ui-translations';
import type { AvailabilityStatus, LeadStatus } from '@/types/provider';

type BadgeStatus = LeadStatus | AvailabilityStatus | 'invited';

interface StatusBadgeProps {
  status: BadgeStatus;
}

export default function StatusBadge({ status }: StatusBadgeProps) {
  const { dict } = useDashboardI18n();

  const config: Record<BadgeStatus, { label: string; className: string }> = {
    created: { label: t(dict, 'status_new', 'New'), className: 'bg-blue-50 text-blue-700' },
    contacted: { label: t(dict, 'status_contacted', 'Contacted'), className: 'bg-orange-50 text-orange-700' },
    done: { label: t(dict, 'status_done', 'Done'), className: 'bg-green-50 text-green-700' },
    rejected: { label: t(dict, 'status_rejected', 'Rejected'), className: 'bg-red-50 text-red-600' },
    invited: { label: t(dict, 'status_new', 'New'), className: 'bg-blue-50 text-blue-700' },
    active: { label: t(dict, 'availability_active', 'Active'), className: 'bg-green-50 text-green-700' },
    busy: { label: t(dict, 'availability_busy', 'Busy'), className: 'bg-yellow-50 text-yellow-700' },
    offline: { label: t(dict, 'availability_offline', 'Offline'), className: 'bg-gray-100 text-gray-500' },
  };

  const cfg = config[status] ?? { label: status, className: 'bg-gray-100 text-gray-500' };
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${cfg.className}`}>
      {cfg.label}
    </span>
  );
}
