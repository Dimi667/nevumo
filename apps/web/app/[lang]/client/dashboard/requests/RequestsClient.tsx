'use client';

import Link from 'next/link';
import { useCallback, useEffect, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { getAuthToken } from '@/lib/auth-store';
import {
  getClientLeads,
  submitReview,
  type ClientLead,
  type ClientLeadFilterStatus,
  type ClientLeadStatus,
} from '@/lib/client-api';
import { useTranslation } from '@/lib/use-translation';
import ClientLeadDetailModal from '@/components/client/ClientLeadDetailModal';

interface ExtendedClientLead extends ClientLead {
  cancelled_by?: 'client' | 'provider' | 'system' | null;
  status_changed_by?: string | null;
}

type ReviewFormState = {
  rating: number;
  comment: string;
};

const TAB_OPTIONS: Array<{ value: ClientLeadFilterStatus; label: string }> = [
  { value: 'all', label: 'status_all' },
  { value: 'active', label: 'status_active' },
  { value: 'done', label: 'status_completed' },
  { value: 'rejected', label: 'status_rejected' },
];

function Toast({ message, onDone }: { message: string; onDone: () => void }) {
  useEffect(() => {
    const timeoutId = window.setTimeout(onDone, 3000);
    return () => window.clearTimeout(timeoutId);
  }, [message, onDone]);

  return (
    <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50 bg-gray-900 text-white text-sm px-4 py-2.5 rounded-xl shadow-lg">
      {message}
    </div>
  );
}

function StarRatingInput({
  value,
  onChange,
}: {
  value: number;
  onChange: (value: number) => void;
}) {
  return (
    <div className="flex items-center gap-2">
      {Array.from({ length: 5 }, (_, index) => {
        const star = index + 1;

        return (
          <button
            key={star}
            type="button"
            onClick={() => onChange(star)}
            className="p-1 transition-transform hover:scale-105"
            aria-label={`Rate ${star} stars`}
          >
            <svg
              width="26"
              height="26"
              viewBox="0 0 24 24"
              fill={star <= value ? '#fbbf24' : 'none'}
              stroke={star <= value ? '#f59e0b' : '#d1d5db'}
              strokeWidth="2"
            >
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
            </svg>
          </button>
        );
      })}
      <span className="text-sm text-gray-500">{value}/5</span>
    </div>
  );
}

function formatDate(value: string, locale: string): string {
  const date = new Date(value);

  try {
    return new Intl.DateTimeFormat(locale, {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
    }).format(date);
  } catch {
    return date.toLocaleDateString();
  }
}

function getStatusMeta(lead: ExtendedClientLead, t: (key: string, fallback?: string) => string): { label: string | null; className: string } {
  const { status, cancelled_by } = lead;

  if (status === 'done') {
    return {
      label: t('status_label_done', 'Completed'),
      className: 'bg-green-100 text-green-700',
    };
  }

  if (status === 'cancelled') {
    if (cancelled_by === 'provider') {
      return {
        label: t('status_label_cancelled_by_provider', 'Cancelled by specialist'),
        className: 'bg-gray-100 text-gray-600',
      };
    }
    return {
      label: t('status_label_cancelled_by_client', 'Cancelled'),
      className: 'bg-gray-100 text-gray-600',
    };
  }

  if (status === 'rejected') {
    return {
      label: t('status_label_cancelled_by_provider', 'Cancelled by specialist'),
      className: 'bg-gray-100 text-gray-600',
    };
  }

  if (status === 'expired') {
    return {
      label: null,
      className: '',
    };
  }

  if (status === 'contacted') {
    return {
      label: t('status_label_contacted', 'Contact made'),
      className: 'bg-blue-100 text-blue-700',
    };
  }

  if (['created', 'pending_match', 'matched'].includes(status)) {
    return {
      label: t('status_label_created', 'Submitted'),
      className: 'bg-orange-100 text-orange-700',
    };
  }

  return {
    label: t('status_active', 'Active'),
    className: 'bg-orange-100 text-orange-700',
  };
}

export default function RequestsClient({ lang }: { lang: string }) {
  const searchParams = useSearchParams();
  const router = useRouter();

  const getInitialTab = useCallback((): ClientLeadFilterStatus => {
    const statusFromUrl = searchParams.get('status');
    const validStatuses: ClientLeadFilterStatus[] = ['all', 'active', 'done', 'rejected'];
    if (statusFromUrl && validStatuses.includes(statusFromUrl as ClientLeadFilterStatus)) {
      return statusFromUrl as ClientLeadFilterStatus;
    }
    return 'all';
  }, [searchParams]);

  const [activeTab, setActiveTab] = useState<ClientLeadFilterStatus>(getInitialTab);
  const [leads, setLeads] = useState<ExtendedClientLead[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [toast, setToast] = useState<string | null>(null);
  const [reviewingLeadId, setReviewingLeadId] = useState<string | null>(null);
  const [reviewForm, setReviewForm] = useState<ReviewFormState>({ rating: 5, comment: '' });
  const [submitting, setSubmitting] = useState(false);
  const [selectedLead, setSelectedLead] = useState<ExtendedClientLead | null>(null);
  const [statusUpdating, setStatusUpdating] = useState<string | null>(null);
  const [confirmingStatus, setConfirmingStatus] = useState<{ leadId: string; status: 'done' | 'cancelled' } | null>(null);
  const [actionError, setActionError] = useState<Record<string, string>>({});
  const { t } = useTranslation('client_dashboard', lang);

  const clearToast = useCallback(() => setToast(null), []);

  const loadLeads = useCallback(async (status: ClientLeadFilterStatus) => {
    const token = getAuthToken();

    if (!token) {
      setError('Липсва активна сесия.');
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const response = await getClientLeads(token, status, undefined, undefined, lang);
      setLeads(response.items as ExtendedClientLead[]);
      setTotal(response.total);

      // Auto-open modal from URL param
      const openId = searchParams.get('open');
      if (openId) {
        const targetLead = response.items.find((l: ClientLead) => l.id === openId);
        if (targetLead) {
          setSelectedLead(targetLead);
          // Clean up URL without reload
          const url = new URL(window.location.href);
          url.searchParams.delete('open');
          router.replace(url.pathname + (url.search || ''), { scroll: false });
        }
      }
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Неуспешно зареждане на заявките.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadLeads(activeTab);
  }, [activeTab, loadLeads]);


  function openReviewForm(leadId: string) {
    setReviewingLeadId(leadId);
    setReviewForm({ rating: 5, comment: '' });
    setError(null);
  }

  function closeReviewForm() {
    setReviewingLeadId(null);
    setReviewForm({ rating: 5, comment: '' });
  }

  async function handleSubmitReview(leadId: string) {
    const token = getAuthToken();

    if (!token) {
      setError('Липсва активна сесия.');
      return;
    }

    try {
      setSubmitting(true);
      setError(null);
      await submitReview(token, leadId, reviewForm.rating, reviewForm.comment);
      closeReviewForm();
      setToast(t('review_submitted', 'Review submitted successfully'));
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Неуспешно изпращане на отзив.');
    } finally {
      setSubmitting(false);
    }
  }

  async function handleStatusUpdate(leadId: string, newStatus: 'contacted' | 'done' | 'cancelled') {
    const token = getAuthToken();
    if (!token) {
      setActionError(prev => ({ ...prev, [leadId]: 'Session expired.' }));
      return;
    }

    try {
      setStatusUpdating(leadId);
      setActionError(prev => {
        const next = { ...prev };
        delete next[leadId];
        return next;
      });

      const res = await fetch(`/api/v1/client/leads/${leadId}/status`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus }),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData?.error?.message || 'Failed to update status');
      }

      setConfirmingStatus(null);
      setLeads(prev => prev.map(l =>
        l.id === leadId
          ? { ...l, status: newStatus, cancelled_by: newStatus === 'cancelled' ? 'client' : null }
          : l
      ));
      await loadLeads(activeTab);
    } catch (err) {
      setActionError(prev => ({ ...prev, [leadId]: err instanceof Error ? err.message : 'Error updating status' }));
    } finally {
      setStatusUpdating(null);
    }
  }

  return (
    <div className="space-y-6">
      {toast && <Toast message={toast} onDone={clearToast} />}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-lg font-semibold text-gray-900">{t('requests_title', 'My Requests')}</h1>
          <p className="text-sm text-gray-500 mt-0.5">{total} резултата</p>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-4">
        <div className="flex flex-wrap gap-2">
          {TAB_OPTIONS.map((tab) => (
            <button
              key={tab.value}
              type="button"
              onClick={() => {
                setActiveTab(tab.value);
                const newParams = new URLSearchParams(searchParams.toString());
                if (tab.value === 'all') {
                  newParams.delete('status');
                } else {
                  newParams.set('status', tab.value);
                }
                router.replace(`/${lang}/client/dashboard/requests?${newParams.toString()}`, { scroll: false });
              }}
              className={`px-3 py-1.5 text-sm rounded-lg transition-colors ${
                activeTab === tab.value
                  ? 'bg-orange-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {t(tab.label, tab.label)}
            </button>
          ))}
        </div>
      </div>

      {error && (
        <div className="bg-red-50 text-red-700 rounded-xl p-4 text-sm">
          {error}
        </div>
      )}

      {leads.length === 0 ? (
        <div className="bg-gray-50 rounded-xl border border-gray-200 p-8 text-center space-y-3">
          <h2 className="text-lg font-medium text-gray-900">{t('requests_empty_title', 'No requests found')}</h2>
          <p className="text-sm text-gray-500">
            {t('requests_empty_desc', 'Send a new request and it will appear here.')}
          </p>
          <Link
            href={`/${lang}`}
            className="inline-flex items-center gap-2 px-4 py-2 bg-orange-500 hover:bg-orange-600 text-white text-sm font-medium rounded-lg transition-colors"
          >
            {t('cta_find_service', 'Find Service')}
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {leads.map((lead) => {
            const statusMeta = getStatusMeta(lead, t);

            return (
              <div
                key={lead.id}
                onClick={() => setSelectedLead(lead)}
                className="bg-white rounded-xl border border-gray-200 p-5 space-y-4 cursor-pointer"
              >
                <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                  <div className="space-y-1.5">
                    <h2 className="text-base font-semibold text-gray-900">
                      {lead.category_name}
                    </h2>
                    <p className="text-sm text-gray-500">{lead.city}</p>
                    <p className="text-sm text-gray-700">
                      {lead.provider_business_name ?? (
                        <span className="text-gray-400 italic text-sm truncate">
                          {t('msg_broadcast_lead', 'Sent to many specialists')}
                        </span>
                      )}
                    </p>
                  </div>
                    <div className="flex flex-col items-start gap-2 lg:items-end">
                      <div className="flex items-center gap-2">
                        {statusMeta.label && (
                          <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${statusMeta.className}`}>
                            {statusMeta.label}
                          </span>
                        )}
                      </div>
                      <span className="text-sm text-gray-500">{formatDate(lead.created_at, lang)}</span>
                    </div>
                </div>

                {/* Status Action Buttons */}
                {['created', 'pending_match', 'matched', 'contacted'].includes(lead.status) && (
                  <div className="pt-2" onClick={(e) => e.stopPropagation()}>
                    {confirmingStatus?.leadId === lead.id ? (
                      <div className="flex flex-wrap items-center gap-3 bg-orange-50 p-3 rounded-lg border border-orange-100">
                        <p className="text-sm font-medium text-orange-800">
                          {confirmingStatus.status === 'done'
                            ? t('status_confirm_done', 'Are you sure the service is completed?')
                            : t('status_confirm_cancel', 'Are you sure you want to cancel this request?')}
                        </p>
                        <div className="flex items-center gap-2">
                          <button
                            type="button"
                            disabled={statusUpdating === lead.id}
                            onClick={() => handleStatusUpdate(lead.id, confirmingStatus.status)}
                            className="px-3 py-1.5 bg-orange-500 hover:bg-orange-600 text-white text-xs font-semibold rounded-md transition-colors disabled:opacity-50"
                          >
                            {t('status_confirm_yes', 'Yes')}
                          </button>
                          <button
                            type="button"
                            disabled={statusUpdating === lead.id}
                            onClick={() => setConfirmingStatus(null)}
                            className="px-3 py-1.5 bg-white border border-gray-300 text-gray-700 hover:bg-gray-50 text-xs font-semibold rounded-md transition-colors disabled:opacity-50"
                          >
                            {t('status_confirm_no', 'No')}
                          </button>
                        </div>
                      </div>
                    ) : (
                      <div className="flex flex-wrap gap-2">
                        {['created', 'pending_match', 'matched'].includes(lead.status) && (
                          <>
                            <button
                              type="button"
                              disabled={statusUpdating === lead.id}
                              onClick={() => handleStatusUpdate(lead.id, 'contacted')}
                              className="px-4 py-2 bg-orange-500 hover:bg-orange-600 text-white text-sm font-medium rounded-lg transition-colors disabled:opacity-50"
                            >
                              {t('status_btn_contacted', 'The specialist contacted me')}
                            </button>
                            <button
                              type="button"
                              disabled={statusUpdating === lead.id}
                              onClick={() => setConfirmingStatus({ leadId: lead.id, status: 'cancelled' })}
                              className="px-4 py-2 border border-gray-300 text-gray-700 hover:bg-gray-50 text-sm font-medium rounded-lg transition-colors disabled:opacity-50"
                            >
                              {t('status_btn_cancel', 'Cancel request')}
                            </button>
                          </>
                        )}
                        {lead.status === 'contacted' && (
                          <>
                            <button
                              type="button"
                              disabled={statusUpdating === lead.id}
                              onClick={() => setConfirmingStatus({ leadId: lead.id, status: 'done' })}
                              className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white text-sm font-medium rounded-lg transition-colors disabled:opacity-50"
                            >
                              {t('status_btn_done', 'Mark as completed')}
                            </button>
                            <button
                              type="button"
                              disabled={statusUpdating === lead.id}
                              onClick={() => setConfirmingStatus({ leadId: lead.id, status: 'cancelled' })}
                              className="px-4 py-2 border border-gray-300 text-gray-700 hover:bg-gray-50 text-sm font-medium rounded-lg transition-colors disabled:opacity-50"
                            >
                              {t('status_btn_cancel', 'Cancel request')}
                            </button>
                          </>
                        )}
                      </div>
                    )}
                    {actionError[lead.id] && (
                      <p className="mt-2 text-xs text-red-600 font-medium">{actionError[lead.id]}</p>
                    )}
                  </div>
                )}

                {(lead.status === 'done' && !lead.has_review && lead.provider_id !== null) && (
                  <div className="space-y-3">
                    {reviewingLeadId === lead.id ? (
                      <div className="bg-gray-50 rounded-xl border border-gray-200 p-4 space-y-4">
                        <div className="space-y-2">
                          <p className="text-sm font-medium text-gray-700">{t('btn_rate_service', 'Rate Service')}</p>
                          <StarRatingInput
                            value={reviewForm.rating}
                            onChange={(rating) => setReviewForm((current) => ({ ...current, rating }))}
                          />
                        </div>
                        <div className="space-y-2">
                          <label className="block text-sm font-medium text-gray-700" htmlFor={`review-comment-${lead.id}`}>
                            {t('label_comment', 'Comment')}
                          </label>
                          <textarea
                            id={`review-comment-${lead.id}`}
                            value={reviewForm.comment}
                            onChange={(event) => setReviewForm((current) => ({
                              ...current,
                              comment: event.target.value,
                            }))}
                            rows={4}
                            maxLength={1000}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400"
                            placeholder={t('review_placeholder', 'Share your impressions...')}
                          />
                          <p className="text-xs text-gray-400">{reviewForm.comment.length}/1000</p>
                        </div>
                        <div className="flex justify-end gap-2">
                          <button
                            type="button"
                            onClick={closeReviewForm}
                            className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900"
                          >
                            {t('btn_cancel', 'Cancel')}
                          </button>
                          <button
                            type="button"
                            onClick={() => handleSubmitReview(lead.id)}
                            disabled={submitting}
                            className="px-4 py-2 bg-orange-500 hover:bg-orange-600 disabled:opacity-50 text-white text-sm font-medium rounded-lg transition-colors"
                          >
                            {submitting ? t('btn_submitting', 'Submitting…') : t('btn_submit', 'Submit')} Review
                          </button>
                        </div>
                      </div>
                    ) : (
                      <button
                        type="button"
                        onClick={() => openReviewForm(lead.id)}
                        className="inline-flex items-center gap-2 px-4 py-2 bg-orange-500 hover:bg-orange-600 text-white text-sm font-medium rounded-lg transition-colors"
                      >
                        {t('btn_write_review', 'Write a Review')}
                      </button>
                    )}
                  </div>
                )}

                {lead.description && (
                  <p className="text-sm text-gray-600 mt-1 truncate">
                    {lead.description}
                  </p>
                )}

                {/* Note hint / preview */}
                <div className="mt-2 pt-2 border-t border-gray-100 flex items-center gap-1.5">
                  {/* Pencil-note SVG icon — modern, no emoji */}
                  <svg
                    className="w-3.5 h-3.5 shrink-0 text-orange-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={1.75}
                      d="M16.862 4.487a2.25 2.25 0 013.182 3.182L7.5 20.213l-4.5 1.5 1.5-4.5L16.862 4.487z"
                    />
                  </svg>
                  {lead.client_notes ? (
                    <span className="text-xs text-gray-500 truncate">
                      {lead.client_notes.length > 45
                        ? lead.client_notes.slice(0, 45) + '…'
                        : lead.client_notes}
                    </span>
                  ) : (
                    <span className="text-xs text-orange-400">
                      {t('btn_add_note', 'Add note')}
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {selectedLead && (
        <ClientLeadDetailModal
          lead={selectedLead}
          lang={lang}
          onClose={() => setSelectedLead(null)}
          onNotesChange={(leadId, newNotes) => {
            setLeads(prev =>
              prev.map(l => l.id === leadId ? { ...l, client_notes: newNotes } : l)
            );
            setSelectedLead(prev =>
              prev?.id === leadId ? { ...prev, client_notes: newNotes } : prev
            );
          }}
        />
      )}
    </div>
  );
}
