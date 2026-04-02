'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { getClientReviews, getClientEmailPreferences, updateClientEmailPreferences } from '@/lib/review-api';
import type { ClientReviewItem, EmailPreferences } from '@/types/review';

export default function ClientReviewsPage() {
  const params = useParams();
  const lang = typeof params.lang === 'string' ? params.lang : 'en';

  const [reviews, setReviews] = useState<ClientReviewItem[]>([]);
  const [preferences, setPreferences] = useState<EmailPreferences | null>(null);
  const [loading, setLoading] = useState(true);
  const [savingPreference, setSavingPreference] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    try {
      setLoading(true);
      const [reviewsData, prefsData] = await Promise.all([
        getClientReviews(),
        getClientEmailPreferences(),
      ]);
      setReviews(reviewsData.items);
      setPreferences(prefsData);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to load reviews');
    } finally {
      setLoading(false);
    }
  }

  async function handleToggleEmailPreference() {
    if (!preferences) return;

    try {
      setSavingPreference(true);
      const newValue = !preferences.review_reply_email_enabled;
      await updateClientEmailPreferences(newValue);
      setPreferences({ ...preferences, review_reply_email_enabled: newValue });
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to update preference');
    } finally {
      setSavingPreference(false);
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-gray-900">My Reviews</h1>
        <p className="text-sm text-gray-500 mt-0.5">
          Reviews you have submitted and provider replies
        </p>
      </div>

      {error && (
        <div className="bg-red-50 text-red-700 rounded-lg p-4 text-sm">
          {error}
        </div>
      )}

      {/* Email preferences */}
      {preferences && (
        <div className="bg-white rounded-xl border border-gray-200 p-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-medium text-gray-900">Email Notifications</h3>
              <p className="text-sm text-gray-500">
                {preferences.description || 'Receive emails when providers reply to your reviews'}
              </p>
            </div>
            <button
              onClick={handleToggleEmailPreference}
              disabled={savingPreference}
              aria-label={preferences.review_reply_email_enabled ? 'Disable email notifications' : 'Enable email notifications'}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                preferences.review_reply_email_enabled
                  ? 'bg-orange-500'
                  : 'bg-gray-200'
              } disabled:opacity-50`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  preferences.review_reply_email_enabled
                    ? 'translate-x-6'
                    : 'translate-x-1'
                }`}
              />
            </button>
          </div>
          <p className="text-xs text-gray-400 mt-2">
            Currently {preferences.review_reply_email_enabled ? 'enabled' : 'disabled'}
          </p>
        </div>
      )}

      {/* Reviews list */}
      <div className="space-y-4">
        {reviews.length === 0 ? (
          <div className="bg-gray-50 rounded-xl p-8 text-center">
            <div className="text-4xl mb-3">⭐</div>
            <h3 className="text-lg font-medium text-gray-900 mb-1">No reviews yet</h3>
            <p className="text-sm text-gray-500">
              Complete a job and submit a review to see it here.
            </p>
          </div>
        ) : (
          reviews.map((review) => (
            <div
              key={review.id}
              className="bg-white rounded-xl border border-gray-200 p-5"
            >
              {/* Review header */}
              <div className="flex items-start justify-between mb-3">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-gray-900">
                      {review.provider_business_name || 'Provider'}
                    </span>
                    <span className="text-xs text-gray-400">
                      {new Date(review.created_at).toLocaleDateString()}
                    </span>
                  </div>
                  <div className="flex items-center gap-1 mt-1">
                    {[...Array(5)].map((_, i) => (
                      <svg
                        key={i}
                        width="14"
                        height="14"
                        viewBox="0 0 24 24"
                        fill={i < review.rating ? '#fbbf24' : 'none'}
                        stroke={i < review.rating ? 'none' : '#d1d5db'}
                        strokeWidth="2"
                      >
                        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
                      </svg>
                    ))}
                  </div>
                </div>
                {review.provider_reply && (
                  <span className="px-2 py-1 bg-green-100 text-green-600 text-xs font-medium rounded-full">
                    Provider Replied
                  </span>
                )}
              </div>

              {/* Lead info */}
              {review.lead_description && (
                <div className="text-xs text-gray-500 mb-3">
                  Job: {review.lead_description}
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
                <div className="bg-green-50 rounded-lg p-3 border-l-4 border-green-400">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-medium text-green-600">
                      Provider&apos;s Reply
                    </span>
                    {review.is_reply_edited && (
                      <span className="text-xs text-gray-500">Edited</span>
                    )}
                  </div>
                  <p className="text-sm text-gray-700">{review.provider_reply}</p>
                  {review.provider_reply_at && (
                    <p className="text-xs text-gray-500 mt-2">
                      Replied on {new Date(review.provider_reply_at).toLocaleDateString()}
                    </p>
                  )}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
