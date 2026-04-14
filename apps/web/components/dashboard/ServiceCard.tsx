'use client';

import { useDashboardI18n } from '@/lib/provider-dashboard-i18n';
import type { Service } from '@/types/provider';

interface ServiceCardProps {
  service: Service;
  onEdit: (service: Service) => void;
  onDelete: (service: Service) => void;
}

export default function ServiceCard({ service, onEdit, onDelete }: ServiceCardProps) {
  const { t } = useDashboardI18n();

  const priceTypeLabels: Record<string, string> = {
    fixed: t('price_type_fixed', 'Fixed price'),
    hourly: t('price_type_hourly', 'Per hour'),
    request: t('price_type_request', 'Per request (quote)'),
    per_sqm: t('price_type_per_sqm', 'Per sq.m.'),
  };

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 flex flex-col gap-3">
      {/* Header */}
      <div className="min-w-0">
        <h3 className="text-sm font-semibold text-gray-900 truncate">{service.title}</h3>
        {service.category_slug && (
          <p className="text-xs text-gray-400 mt-0.5 capitalize">{service.category_slug.replace(/-/g, ' ')}</p>
        )}
      </div>

      {/* Cities */}
      {service.cities.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {service.cities.map(c => (
            <span key={c.id} className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">
              {c.city}
            </span>
          ))}
        </div>
      )}

      {/* Price row */}
      <div className="flex items-center gap-2">
        <span className="text-xs text-gray-500 bg-gray-100 px-2 py-0.5 rounded-full">
          {priceTypeLabels[service.price_type] ?? service.price_type}
        </span>
        {service.base_price !== null && (
          <span className="text-sm font-semibold text-orange-500">
            {service.base_price} {service.currency}
          </span>
        )}
      </div>

      {/* Actions */}
      <div className="flex items-center gap-2 pt-1 border-t border-gray-100">
        <button
          onClick={() => onEdit(service)}
          className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-gray-600 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
        >
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
          </svg>
          {t('btn_edit', 'Edit')}
        </button>
        <button
          onClick={() => onDelete(service)}
          className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-red-500 border border-red-200 rounded-lg hover:bg-red-50 transition-colors"
        >
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <polyline points="3 6 5 6 21 6" />
            <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6" />
            <path d="M10 11v6M14 11v6" />
            <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2" />
          </svg>
          {t('btn_delete', 'Delete')}
        </button>
      </div>
    </div>
  );
}
