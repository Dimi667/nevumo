'use client';

import { useState, useCallback, useEffect, useRef } from 'react';
import Link from 'next/link';
import { formatDashboardDate } from '@/lib/provider-dashboard-i18n';
import { updateClientLeadNotes, type ClientLead } from '@/lib/client-api';
import { useTranslation } from '@/lib/use-translation';

interface ClientLeadDetailModalProps {
  lead: ClientLead;
  lang: string;
  onClose: () => void;
  onNotesChange: (leadId: string, newNotes: string | null) => void;
}

function getStatusMeta(status: string, t: (key: string, fallback?: string) => string): { label: string; className: string } {
  if (status === 'done') {
    return {
      label: t('status_completed', 'Completed'),
      className: 'bg-green-100 text-green-700',
    };
  }

  if (status === 'rejected' || status === 'expired' || status === 'cancelled') {
    return {
      label: t('status_rejected', 'Rejected'),
      className: 'bg-gray-100 text-gray-600',
    };
  }

  return {
    label: t('status_active', 'Active'),
    className: 'bg-orange-100 text-orange-700',
  };
}

export default function ClientLeadDetailModal({
  lead,
  lang,
  onClose,
  onNotesChange,
}: ClientLeadDetailModalProps) {
  const { t } = useTranslation('client_dashboard', lang);
  const [notes, setNotes] = useState(lead.client_notes ?? '');
  const [isSaving, setIsSaving] = useState(false);
  const debounceTimerRef = useRef<NodeJS.Timeout | null>(null);

  const saveNotes = useCallback(async (value: string) => {
    setIsSaving(true);
    try {
      const notesToSave = value.trim() || null;
      await updateClientLeadNotes(lead.id, notesToSave);
      onNotesChange(lead.id, notesToSave);
    } catch (err) {
      // Silently ignore as per requirements
    } finally {
      setIsSaving(false);
    }
  }, [lead.id, onNotesChange]);

  const handleNotesChange = (value: string) => {
    setNotes(value);
    
    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
    }

    debounceTimerRef.current = setTimeout(() => {
      saveNotes(value);
    }, 500);
  };

  const handleBlur = () => {
    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
      debounceTimerRef.current = null;
    }
    // Only save if different from the initial lead notes
    if (notes !== (lead.client_notes ?? '')) {
      saveNotes(notes);
    }
  };

  useEffect(() => {
    return () => {
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }
    };
  }, []);

  const statusMeta = getStatusMeta(lead.status, t);

  return (
    <>
      {/* Overlay */}
      <div
        className="fixed inset-0 bg-black/50 z-50 backdrop-blur-sm transition-opacity"
        onClick={onClose}
      />

      {/* Modal Container */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none">
        <div className="bg-white rounded-lg max-w-lg w-full mx-auto shadow-xl relative pointer-events-auto max-h-[90vh] overflow-y-auto">
          {/* Header */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100">
            <h2 className="text-lg font-semibold text-gray-900">
              {t('modal_title_request', 'Your request')}
            </h2>
            <button
              onClick={onClose}
              className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </div>

          {/* Info Grid */}
          <div className="px-6 py-4 space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                  {t('label_date', 'Date')}
                </label>
                <p className="text-sm text-gray-900 mt-1">
                  {formatDashboardDate(lead.created_at, lang)}
                </p>
              </div>
              <div>
                <label className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                  {t('label_specialist', 'Specialist')}
                </label>
                <div className="mt-1">
                  {lead.provider_id ? (
                    <Link
                      href={`/${lang}/${lead.city_slug}/${lead.category_slug}/${lead.provider_slug}`}
                      className="text-sm text-orange-500 hover:underline"
                    >
                      {lead.provider_business_name}
                    </Link>
                  ) : (
                    <p className="text-sm text-gray-500 italic">
                      {t('msg_broadcast_lead', 'Your request was sent to many specialists who will send you offers')}
                    </p>
                  )}
                </div>
              </div>
              <div>
                <label className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                  {t('label_status', 'Status')}
                </label>
                <div className="mt-1">
                  <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium ${statusMeta.className}`}>
                    {statusMeta.label}
                  </span>
                </div>
              </div>
            </div>

            {/* Message Section */}
            <div className="bg-gray-50 rounded-lg p-4">
              <label className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                {t('label_your_message', 'Your message to the specialist')}
              </label>
              <p className="text-sm text-gray-800 mt-2 whitespace-pre-wrap">
                {lead.description || '—'}
              </p>
            </div>

            {/* Notes Section */}
            <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <span className="text-orange-600">📝</span>
                  <label className="text-sm font-semibold text-orange-800">
                    {t('label_client_notes', 'Your notes (visible only to you)')}
                  </label>
                </div>
                {isSaving && (
                  <svg className="animate-spin h-4 w-4 text-orange-600" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                )}
              </div>

              <textarea
                value={notes}
                onChange={(e) => handleNotesChange(e.target.value)}
                onBlur={handleBlur}
                placeholder={t('placeholder_client_notes', 'Add a note about this request...')}
                rows={4}
                className="w-full px-3 py-2 text-sm bg-white border border-orange-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500 resize-none placeholder:text-orange-300 text-gray-800"
              />
            </div>
          </div>

          {/* Footer */}
          <div className="px-6 py-4 border-t border-gray-100 flex justify-center">
            <button
              onClick={onClose}
              className="px-6 py-2 bg-white border border-gray-300 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50 transition-colors"
            >
              {t('btn_save_and_close', 'Save and close')}
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
