'use client';

import { useState, useCallback, useEffect } from 'react';
import { formatDashboardDate, useDashboardI18n } from '@/lib/provider-dashboard-i18n';
import { t, type TranslationDict } from '@/lib/ui-translations';
import StatusBadge from './StatusBadge';
import { updateLeadNotes } from '@/lib/provider-api';
import type { Lead } from '@/types/provider';

interface LeadDetailModalProps {
  lead: Lead | null;
  isOpen: boolean;
  onClose: () => void;
  onNotesSaved?: (leadId: string, notes: string | null) => void;
}

// Toast component for success notification
function Toast({ message, onDone }: { message: string; onDone: () => void }) {
  // Auto-dismiss after 3 seconds
  setTimeout(onDone, 3000);

  return (
    <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-[60] bg-gray-900 text-white text-sm px-4 py-2.5 rounded-xl shadow-lg animate-in fade-in slide-in-from-bottom-2">
      {message}
    </div>
  );
}

function getSourceLabel(source: string | null, dict: TranslationDict): string {
  if (!source) return '—';
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

export default function LeadDetailModal({ lead, isOpen, onClose, onNotesSaved }: LeadDetailModalProps) {
  const { dict, lang } = useDashboardI18n();
  const [notes, setNotes] = useState(lead?.provider_notes ?? '');
  const [saving, setSaving] = useState(false);
  const [toast, setToast] = useState<string | null>(null);

  // Reset notes when lead changes
  useEffect(() => {
    setNotes(lead?.provider_notes ?? '');
  }, [lead]);

  const handleNotesChange = (value: string) => {
    setNotes(value);
  };

  const clearToast = useCallback(() => setToast(null), []);

  const handleSaveNotes = async () => {
    if (!lead) return;
    setSaving(true);
    try {
      const result = await updateLeadNotes(lead.id, notes);
      setToast(t(dict, 'msg_notes_saved', 'Notes saved successfully'));
      onNotesSaved?.(lead.id, result.provider_notes);
    } catch {
      setToast(t(dict, 'msg_notes_save_failed', 'Failed to save notes'));
    } finally {
      setSaving(false);
    }
  };

  if (!isOpen || !lead) return null;

  return (
    <>
      {toast && <Toast message={toast} onDone={clearToast} />}

      {/* Modal Overlay */}
      <div
        className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm transition-opacity"
        onClick={onClose}
      />

      {/* Modal Content */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none">
        <div className="bg-white rounded-2xl shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto pointer-events-auto">
          {/* Header */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100">
            <h2 className="text-lg font-semibold text-gray-900">
              {t(dict, 'lead_detail_title', 'Lead Details')}
            </h2>
            <button
              onClick={onClose}
              className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
              aria-label={t(dict, 'aria_close', 'Close')}
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </div>

          {/* Body */}
          <div className="px-6 py-4 space-y-6">
            {/* Lead Info Grid */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                  {t(dict, 'label_date', 'Date')}
                </label>
                <p className="text-sm text-gray-900 mt-1">
                  {formatDashboardDate(lead.created_at, lang)}
                </p>
              </div>
              <div>
                <label className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                  {t(dict, 'label_phone', 'Phone')}
                </label>
                <p className="text-sm font-medium text-gray-900 mt-1">
                  {lead.phone}
                </p>
              </div>
              <div>
                <label className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                  {t(dict, 'label_status', 'Status')}
                </label>
                <div className="mt-1">
                  <StatusBadge status={lead.status} />
                </div>
              </div>
              <div>
                <label className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                  {t(dict, 'label_source', 'Source')}
                </label>
                <p className="text-sm text-gray-900 mt-1">
                  {getSourceLabel(lead.source, dict)}
                </p>
              </div>
            </div>

            {/* Client Description Section */}
            <div className="bg-gray-50 rounded-xl p-4">
              <label className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                {t(dict, 'label_client_message', 'CLIENT MESSAGE')}
              </label>
              <p className="text-sm text-gray-800 mt-2 whitespace-pre-wrap">
                {lead.description ?? t(dict, 'msg_no_description', 'No description provided')}
              </p>
            </div>

            {/* Private Notes Section - Sticky Note Style */}
            <div className="bg-amber-50 border border-amber-200 rounded-xl p-4">
              <div className="flex items-center gap-2 mb-3">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-amber-600">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <polyline points="14 2 14 8 20 8" />
                  <line x1="16" y1="13" x2="8" y2="13" />
                  <line x1="16" y1="17" x2="8" y2="17" />
                  <polyline points="10 9 9 9 8 9" />
                </svg>
                <label className="text-sm font-semibold text-amber-800">
                  {t(dict, 'label_private_notes', 'Private Notes')}
                </label>
              </div>

              <p className="text-xs text-amber-700 mb-3">
                {t(dict, 'label_notes_privacy_disclaimer', 'These notes are only visible to you and will not be shared with the client.')}
              </p>

              <textarea
                value={notes}
                onChange={(e) => handleNotesChange(e.target.value)}
                placeholder={t(dict, 'placeholder_private_notes', 'Write your private notes here...')}
                rows={4}
                className="w-full px-3 py-2.5 text-sm bg-white/80 border border-amber-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-400 focus:border-amber-400 resize-none placeholder:text-amber-400/70 text-gray-800"
              />

              <div className="flex justify-end mt-3">
                <button
                  onClick={handleSaveNotes}
                  disabled={saving}
                  className="px-4 py-2 bg-amber-600 hover:bg-amber-700 disabled:opacity-50 disabled:cursor-not-allowed text-white text-sm font-medium rounded-lg transition-colors flex items-center gap-2"
                >
                  {saving ? (
                    <>
                      <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                      {t(dict, 'msg_saving', 'Saving...')}
                    </>
                  ) : (
                    <>
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z" />
                        <polyline points="17 21 17 13 7 13 7 21" />
                        <polyline points="7 3 7 8 15 8" />
                      </svg>
                      {t(dict, 'btn_save_notes', 'Save Notes')}
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="px-6 py-4 border-t border-gray-100 bg-gray-50 rounded-b-2xl">
            <button
              onClick={onClose}
              className="w-full px-4 py-2 bg-white border border-gray-300 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50 transition-colors"
            >
              {t(dict, 'btn_close', 'Close')}
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
