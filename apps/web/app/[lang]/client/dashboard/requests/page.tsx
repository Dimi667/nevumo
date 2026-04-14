'use client';

import Link from 'next/link';
import { useCallback, useEffect, useState } from 'react';
import { useParams, useSearchParams, useRouter } from 'next/navigation';
import { getAuthToken } from '@/lib/auth-store';
import {
  getClientLeads,
  submitReview,
  type ClientLead,
  type ClientLeadFilterStatus,
  type ClientLeadStatus,
} from '@/lib/client-api';
import { useTranslation } from '@/lib/use-translation';

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

function getStatusMeta(status: ClientLeadStatus, t: (key: string, fallback?: string) => string): { label: string; className: string } {
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

export default function ClientRequestsPage() {
  const params = useParams();
  const searchParams = useSearchParams();
  const router = useRouter();
  const lang = typeof params.lang === 'string' ? params.lang : 'en';

  const getInitialTab = useCallback((): ClientLeadFilterStatus => {
    const statusFromUrl = searchParams.get('status');
    const validStatuses: ClientLeadFilterStatus[] = ['all', 'active', 'done', 'rejected'];
    if (statusFromUrl && validStatuses.includes(statusFromUrl as ClientLeadFilterStatus)) {
      return statusFromUrl as ClientLeadFilterStatus;
    }
    return 'all';
  }, [searchParams]);

  const [activeTab, setActiveTab] = useState<ClientLeadFilterStatus>(getInitialTab);
  const [leads, setLeads] = useState<ClientLead[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [toast, setToast] = useState<string | null>(null);
  const [reviewingLeadId, setReviewingLeadId] = useState<string | null>(null);
  const [reviewForm, setReviewForm] = useState<ReviewFormState>({ rating: 5, comment: '' });
  const [submitting, setSubmitting] = useState(false);
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
      const response = await getClientLeads(token, status);
      setLeads(response.items);
      setTotal(response.total);
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
            const statusMeta = getStatusMeta(lead.status, t);

            return (
              <div key={lead.id} className="bg-white rounded-xl border border-gray-200 p-5 space-y-4">
                <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                  <div className="space-y-1.5">
                    <h2 className="text-base font-semibold text-gray-900">
                      {lead.category_name}
                    </h2>
                    <p className="text-sm text-gray-500">{lead.city}</p>
                    <p className="text-sm text-gray-700">
                      {lead.provider_business_name || 'Marketplace'}
                    </p>
                  </div>
                  <div className="flex flex-col items-start gap-2 lg:items-end">
                    <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${statusMeta.className}`}>
                      {statusMeta.label}
                    </span>
                    <span className="text-sm text-gray-500">{formatDate(lead.created_at, lang)}</span>
                  </div>
                </div>

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
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
