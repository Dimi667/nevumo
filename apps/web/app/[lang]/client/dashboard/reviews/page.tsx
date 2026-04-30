'use client';

import Link from 'next/link';
import { useCallback, useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { getAuthToken } from '@/lib/auth-store';
import {
  getClientDashboard,
  getClientReviews,
  getEligibleLeads,
  getReviewPreferences,
  submitReview,
  updateReviewPreferences,
  type ClientReview,
  type EligibleLead,
  type ReviewPreferences,
} from '@/lib/client-api';
import { fetchTranslations, t, type TranslationDict } from '@/lib/ui-translations';

type ReviewsTab = 'written' | 'pending';

type ReviewFormState = {
  leadId: string | null;
  providerId: string | null;
  rating: number;
  comment: string;
};

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

function StarDisplay({ rating }: { rating: number }) {
  return (
    <div className="flex items-center gap-1 mt-1">
      {Array.from({ length: 5 }, (_, index) => {
        const star = index + 1;

        return (
          <svg
            key={star}
            width="14"
            height="14"
            viewBox="0 0 24 24"
            fill={star <= rating ? '#fbbf24' : 'none'}
            stroke={star <= rating ? '#f59e0b' : '#d1d5db'}
            strokeWidth="2"
          >
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
          </svg>
        );
      })}
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

export default function ClientReviewsPage() {
  const params = useParams();
  const lang = typeof params.lang === 'string' ? params.lang : 'en';

  const [activeTab, setActiveTab] = useState<ReviewsTab>('written');
  const [writtenReviews, setWrittenReviews] = useState<ClientReview[]>([]);
  const [pendingLeads, setPendingLeads] = useState<EligibleLead[]>([]);
  const [lastCitySlug, setLastCitySlug] = useState<string | null>(null);
  const [preferences, setPreferences] = useState<ReviewPreferences | null>(null);
  const [loadingTab, setLoadingTab] = useState(true);
  const [loadingPreferences, setLoadingPreferences] = useState(true);
  const [savingPreference, setSavingPreference] = useState(false);
  const [reviewForm, setReviewForm] = useState<ReviewFormState>({ leadId: null, providerId: null, rating: 5, comment: '' });
  const [submittingId, setSubmittingId] = useState<string | null>(null); // leadId:providerId
  const [expandedReplies, setExpandedReplies] = useState<Record<string, boolean>>({});
  const [toast, setToast] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [dict, setDict] = useState<TranslationDict>({});

  const clearToast = useCallback(() => setToast(null), []);

  const loadPreferences = useCallback(async () => {
    const token = getAuthToken();

    if (!token) {
      setError('Липсва активна сесия.');
      setLoadingPreferences(false);
      return;
    }

    try {
      setLoadingPreferences(true);
      const prefsData = await getReviewPreferences(token);
      setPreferences(prefsData);

      // Also fetch dashboard to get last_city_slug for the "Find Service" button
      try {
        const dashboard = await getClientDashboard(token, lang);
        setLastCitySlug(dashboard.last_city_slug ?? null);
      } catch (e) {
        console.error('Error fetching dashboard for last_city_slug:', e);
      }
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Неуспешно зареждане на настройките.');
    } finally {
      setLoadingPreferences(false);
    }
  }, []);

  const loadWrittenReviews = useCallback(async (showLoading: boolean = true) => {
    const token = getAuthToken();

    if (!token) {
      setError('Липсва активна сесия.');
      setLoadingTab(false);
      return;
    }

    try {
      if (showLoading) {
        setLoadingTab(true);
      }

      setError(null);
      const reviewsData = await getClientReviews(token);
      setWrittenReviews(reviewsData.items);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Неуспешно зареждане на ревютата.');
    } finally {
      if (showLoading) {
        setLoadingTab(false);
      }
    }
  }, []);

  const loadPendingLeads = useCallback(async (showLoading: boolean = true) => {
    const token = getAuthToken();

    if (!token) {
      setError('Липсва активна сесия.');
      setLoadingTab(false);
      return;
    }

    try {
      if (showLoading) {
        setLoadingTab(true);
      }

      setError(null);
      const eligibleData = await getEligibleLeads(token);
      setPendingLeads(eligibleData.leads.filter((lead) => !lead.has_review));
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Неуспешно зареждане на чакащите ревюта.');
    } finally {
      if (showLoading) {
        setLoadingTab(false);
      }
    }
  }, []);

  useEffect(() => {
    void loadPreferences();
  }, [loadPreferences]);

  useEffect(() => {
    if (activeTab === 'written') {
      void loadWrittenReviews();
      return;
    }

    void loadPendingLeads();
  }, [activeTab, loadPendingLeads, loadWrittenReviews]);

  useEffect(() => {
    async function loadTranslations() {
      const translations = await fetchTranslations(lang, 'client_dashboard');
      setDict(translations);
    }

    void loadTranslations();
  }, [lang]);

  async function handleToggleEmailPreference() {
    const token = getAuthToken();

    if (!token || !preferences) {
      setError('Липсва активна сесия.');
      return;
    }

    try {
      setSavingPreference(true);
      setError(null);
      const updated = await updateReviewPreferences(token, !preferences.review_reply_email_enabled);
      setPreferences(updated);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Неуспешно обновяване на настройката.');
    } finally {
      setSavingPreference(false);
    }
  }

  function openReviewForm(leadId: string, providerId: string) {
    setReviewForm({ leadId, providerId, rating: 5, comment: '' });
  }

  function closeReviewForm() {
    setReviewForm({ leadId: null, providerId: null, rating: 5, comment: '' });
  }

  function toggleReply(reviewId: string) {
    setExpandedReplies((current) => ({
      ...current,
      [reviewId]: !current[reviewId],
    }));
  }

  async function handleSubmitReview(leadId: string, providerId: string) {
    const token = getAuthToken();

    if (!token) {
      setError('Липсва активна сесия.');
      return;
    }

    try {
      const subId = `${leadId}:${providerId}`;
      setSubmittingId(subId);
      setError(null);
      await submitReview(token, leadId, providerId, reviewForm.rating, reviewForm.comment);
      closeReviewForm();
      setToast('Ревюто беше изпратено успешно.');
      await Promise.all([
        loadPendingLeads(false),
        loadWrittenReviews(false),
      ]);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Неуспешно изпращане на ревю.');
    } finally {
      setSubmittingId(null);
    }
  }

  if (loadingTab && ((activeTab === 'written' && writtenReviews.length === 0) || (activeTab === 'pending' && pendingLeads.length === 0))) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <>
      {toast && <Toast message={toast} onDone={clearToast} />}
      <div className="space-y-6">
        <div>
          <h1 className="text-xl font-bold text-gray-900">{t(dict, 'reviews_title', 'Reviews')}</h1>
          <p className="text-sm text-gray-500 mt-0.5">
            {t(dict, 'reviews_subtitle', 'Your written reviews and pending ratings')}
          </p>
        </div>

        <div className="flex gap-2 border-b border-gray-200">
          <button
            type="button"
            onClick={() => setActiveTab('written')}
            className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
              activeTab === 'written'
                ? 'border-orange-500 text-orange-600'
                : 'border-transparent text-gray-600 hover:text-gray-900'
            }`}
          >
            {t(dict, 'tab_written', 'Written')}
            <span className="ml-2 px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded-full">
              {writtenReviews.length}
            </span>
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('pending')}
            className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
              activeTab === 'pending'
                ? 'border-orange-500 text-orange-600'
                : 'border-transparent text-gray-600 hover:text-gray-900'
            }`}
          >
            {t(dict, 'tab_pending', 'Pending Review')}
            <span className="ml-2 px-2 py-0.5 bg-orange-100 text-orange-600 text-xs rounded-full">
              {pendingLeads.length}
            </span>
          </button>
        </div>

        {error && (
          <div className="bg-red-50 text-red-700 rounded-lg p-4 text-sm">
            {error}
          </div>
        )}

        {/* Reviews list */}
        <div className="space-y-4">
          {activeTab === 'written' ? (
            writtenReviews.length === 0 ? (
              <div className="bg-gray-50 rounded-xl p-8 text-center">
                <div className="text-4xl mb-3">⭐</div>
                <h3 className="text-lg font-medium text-gray-900 mb-1">{t(dict, 'empty_reviews_title', 'No reviews written yet')}</h3>
                <p className="text-sm text-gray-500">
                  {t(dict, 'empty_reviews_desc', 'When you rate a completed service...')}
                </p>
              </div>
            ) : (
              writtenReviews.map((review) => {
                const isReplyExpanded = !!expandedReplies[review.id];

                return (
                  <div
                    key={review.id}
                    className="bg-white rounded-xl border border-gray-200 p-5"
                  >
                    {/* Review header */}
                    <div className="flex items-start justify-between mb-3 gap-4">
                      <div>
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="font-medium text-gray-900">
                            {review.provider_business_name || t(dict, 'label_provider', 'Provider')}
                          </span>
                          <span className="text-xs text-gray-400">
                            {formatDate(review.created_at, lang)}
                          </span>
                        </div>
                        <StarDisplay rating={review.rating} />
                      </div>
                      {review.provider_reply && (
                        <span className="px-2 py-1 bg-green-100 text-green-600 text-xs font-medium rounded-full">
                          {t(dict, 'label_has_reply', 'Has Reply')}
                        </span>
                      )}
                    </div>

                    {/* Lead info */}
                    {review.lead_description && (
                      <div className="text-xs text-gray-500 mb-3">
                        {t(dict, 'label_service', 'Service: ')}{review.lead_description}
                      </div>
                    )}

                    {/* Client comment */}
                    {review.comment && (
                      <div className="bg-gray-50 rounded-lg p-3 mb-3">
                        <p className="text-sm text-gray-700">{review.comment}</p>
                      </div>
                    )}

                    {/* Provider reply */}
                    {review.provider_reply && (
                      <div className="space-y-2">
                        <button
                          type="button"
                          onClick={() => toggleReply(review.id)}
                          className="text-sm text-orange-500 hover:text-orange-600 font-medium"
                        >
                          {isReplyExpanded ? t(dict, 'label_hide_reply', 'Hide Provider Reply') : t(dict, 'label_provider_reply', 'Provider Reply')}
                        </button>
                        {isReplyExpanded && (
                          <div className="bg-orange-50 rounded-lg p-3 border-l-4 border-orange-300">
                            <div className="flex items-center gap-2 mb-2">
                              <span className="text-xs font-medium text-orange-700">
                                {t(dict, 'label_provider_reply', 'Provider Reply')}
                              </span>
                              {review.is_reply_edited && (
                                <span className="text-xs text-gray-500">(редактиран)</span>
                              )}
                            </div>
                            <p className="text-sm text-gray-700">{review.provider_reply}</p>
                            {review.provider_reply_at && (
                              <p className="text-xs text-gray-500 mt-2">
                                {t(dict, 'label_replied_on', 'Replied on ')}{formatDate(review.provider_reply_at, lang)}
                              </p>
                            )}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })
            )
          ) : pendingLeads.length === 0 ? (
            <div className="bg-gray-50 rounded-xl p-8 text-center space-y-3">
              <div className="text-4xl mb-1">📝</div>
              <h3 className="text-lg font-medium text-gray-900">{t(dict, 'empty_pending_title', 'No pending reviews')}</h3>
              <p className="text-sm text-gray-500">
                {t(dict, 'empty_pending_desc', 'Completed services you have not rated...')}
              </p>
              <Link
                href={lastCitySlug ? `/${lang}/${lastCitySlug}` : `/${lang}/izberi-grad`}
                className="inline-flex items-center gap-2 px-4 py-2 bg-orange-500 hover:bg-orange-600 text-white text-sm font-medium rounded-lg transition-colors"
              >
                {t(dict, 'cta_find_service', 'Find Service')}
              </Link>
            </div>
          ) : (
            pendingLeads.flatMap((lead) => 
              (lead.reviewable_providers || []).map((provider) => ({
                ...lead,
                current_provider: provider
              }))
            ).map((item) => {
              const lead = item;
              const provider = item.current_provider;
              const isFormOpen = reviewForm.leadId === lead.id && reviewForm.providerId === provider.provider_id;
              const subId = `${lead.id}:${provider.provider_id}`;

              return (
                <div key={subId} className="bg-white rounded-xl border border-gray-200 p-5 space-y-4">
                  <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                    <div>
                      <h3 className="font-medium text-gray-900">
                        {provider.provider_name}
                      </h3>
                      <div className="flex items-center gap-2 mt-1">
                        <span className="text-xs font-medium px-2 py-0.5 bg-gray-100 text-gray-600 rounded-md">
                          {lead.category_name}
                        </span>
                        <span className="text-xs text-gray-400">
                          {lead.city}
                        </span>
                        <span className="text-xs text-gray-400">•</span>
                        <span className="text-xs text-gray-400">{formatDate(lead.created_at, lang)}</span>
                      </div>
                    </div>
                    {!isFormOpen && (
                      <button
                        type="button"
                        onClick={() => openReviewForm(lead.id, provider.provider_id)}
                        className="inline-flex items-center gap-2 px-4 py-2 bg-orange-500 hover:bg-orange-600 text-white text-sm font-medium rounded-lg transition-colors"
                      >
                        {t(dict, 'btn_rate_service', 'Rate')}
                      </button>
                    )}
                  </div>

                  {lead.description && (
                    <p className="text-sm text-gray-600">{lead.description}</p>
                  )}

                  {isFormOpen && (
                    <div className="bg-gray-50 rounded-xl border border-gray-200 p-4 space-y-4">
                      <div className="space-y-2">
                        <p className="text-sm font-medium text-gray-700">{t(dict, 'label_rating', 'Rating')}</p>
                        <StarRatingInput
                          value={reviewForm.rating}
                          onChange={(rating) => setReviewForm((current) => ({ ...current, rating }))}
                        />
                      </div>
                      <div className="space-y-2">
                        <label className="block text-sm font-medium text-gray-700" htmlFor={`pending-review-comment-${subId}`}>
                          {t(dict, 'label_comment', 'Comment')}
                        </label>
                        <textarea
                          id={`pending-review-comment-${subId}`}
                          value={reviewForm.comment}
                          onChange={(event) => setReviewForm((current) => ({
                            ...current,
                            comment: event.target.value,
                          }))}
                          rows={4}
                          maxLength={1000}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-orange-400"
                          placeholder={t(dict, 'review_placeholder', 'Share your impressions...')}
                        />
                        <p className="text-xs text-gray-400">{reviewForm.comment.length}/1000</p>
                      </div>
                      <div className="flex justify-end gap-2">
                        <button
                          type="button"
                          onClick={closeReviewForm}
                          className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900"
                        >
                          {t(dict, 'btn_cancel', 'Cancel')}
                        </button>
                        <button
                          type="button"
                          onClick={() => handleSubmitReview(lead.id, provider.provider_id)}
                          disabled={submittingId === subId}
                          className="px-4 py-2 bg-orange-500 hover:bg-orange-600 disabled:opacity-50 text-white text-sm font-medium rounded-lg transition-colors"
                        >
                          {submittingId === subId ? t(dict, 'btn_submitting', 'Submitting...') : t(dict, 'btn_submit_review', 'Submit Review')}
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              );
            })
          )}
        </div>

        {/* Email preferences */}
        <div className="bg-white rounded-xl border border-gray-200 p-4">
          <div className="flex items-center justify-between gap-4">
            <div>
              <h3 className="font-medium text-gray-900">{t(dict, 'settings_email_notif', 'Receive email on review reply')}</h3>
              <p className="text-sm text-gray-500">
                {preferences?.description ?? 'Ще получаваш известие, когато доставчик отговори на ревюто ти.'}
              </p>
            </div>
            {loadingPreferences ? (
              <div className="w-11 h-6 rounded-full bg-gray-200 animate-pulse" />
            ) : (
              <button
                onClick={handleToggleEmailPreference}
                disabled={savingPreference || !preferences}
                aria-label={preferences?.review_reply_email_enabled ? 'Disable email notifications' : 'Enable email notifications'}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  preferences?.review_reply_email_enabled
                    ? 'bg-orange-500'
                    : 'bg-gray-200'
                } disabled:opacity-50`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    preferences?.review_reply_email_enabled
                      ? 'translate-x-6'
                      : 'translate-x-1'
                  }`}
                />
              </button>
            )}
          </div>
        </div>
      </div>
    </>
  );
}
