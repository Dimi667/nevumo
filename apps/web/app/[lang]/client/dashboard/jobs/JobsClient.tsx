'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { getEligibleLeadsForReview, createReview } from '@/lib/review-api';
import type { EligibleLead } from '@/types/review';

export default function JobsClient({ lang }: { lang: string }) {
  const [leads, setLeads] = useState<EligibleLead[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [reviewingLead, setReviewingLead] = useState<string | null>(null);
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  useEffect(() => {
    loadLeads();
  }, []);

  async function loadLeads() {
    try {
      setLoading(true);
      const data = await getEligibleLeadsForReview();
      setLeads(data.leads);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to load jobs');
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmitReview(leadId: string) {
    try {
      setSubmitting(true);
      setError(null);
      await createReview(leadId, rating, comment.trim() || undefined);

      // Refresh leads
      await loadLeads();

      // Reset form
      setReviewingLead(null);
      setRating(5);
      setComment('');
      setSuccessMessage('Review submitted successfully!');

      // Clear success message after 3 seconds
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to submit review');
    } finally {
      setSubmitting(false);
    }
  }

  function startReview(leadId: string) {
    setReviewingLead(leadId);
    setRating(5);
    setComment('');
  }

  function cancelReview() {
    setReviewingLead(null);
    setRating(5);
    setComment('');
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
        <h1 className="text-xl font-bold text-gray-900">Completed Jobs</h1>
        <p className="text-sm text-gray-500 mt-0.5">
          Review your completed jobs and submit ratings
        </p>
      </div>

      {successMessage && (
        <div className="bg-green-50 text-green-700 rounded-lg p-4 text-sm">
          {successMessage}
        </div>
      )}

      {error && (
        <div className="bg-red-50 text-red-700 rounded-lg p-4 text-sm">
          {error}
        </div>
      )}

      {/* Jobs list */}
      <div className="space-y-4">
        {leads.length === 0 ? (
          <div className="bg-gray-50 rounded-xl p-8 text-center">
            <div className="text-4xl mb-3">📋</div>
            <h3 className="text-lg font-medium text-gray-900 mb-1">No completed jobs</h3>
            <p className="text-sm text-gray-500">
              When you complete a job with a provider, it will appear here for review.
            </p>
            <Link
              href={`/${lang}`}
              className="inline-block mt-4 px-4 py-2 bg-orange-500 text-white text-sm font-medium rounded-lg hover:bg-orange-600 transition-colors"
            >
              Browse Services
            </Link>
          </div>
        ) : (
          leads.map((lead) => (
            <div
              key={lead.id}
              className="bg-white rounded-xl border border-gray-200 p-5"
            >
              <div className="flex items-start justify-between mb-3">
                <div>
                  <h3 className="font-medium text-gray-900">
                    {lead.provider_business_name || 'Service Provider'}
                  </h3>
                  <p className="text-xs text-gray-400">
                    Completed on {new Date(lead.created_at).toLocaleDateString()}
                  </p>
                </div>
                {lead.has_review ? (
                  <span className="px-2 py-1 bg-green-100 text-green-600 text-xs font-medium rounded-full">
                    Reviewed
                  </span>
                ) : (
                  <span className="px-2 py-1 bg-orange-100 text-orange-600 text-xs font-medium rounded-full">
                    Needs Review
                  </span>
                )}
              </div>

              {lead.description && (
                <p className="text-sm text-gray-600 mb-4">
                  {lead.description}
                </p>
              )}

              {reviewingLead === lead.id ? (
                <div className="bg-gray-50 rounded-lg p-4 space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Your Rating
                    </label>
                    <div className="flex items-center gap-2">
                      {[1, 2, 3, 4, 5].map((star) => (
                        <button
                          key={star}
                          onClick={() => setRating(star)}
                          className="p-1 transition-colors"
                          aria-label={`Rate ${star} stars`}
                        >
                          <svg
                            width="28"
                            height="28"
                            viewBox="0 0 24 24"
                            fill={star <= rating ? '#fbbf24' : 'none'}
                            stroke={star <= rating ? '#f59e0b' : '#d1d5db'}
                            strokeWidth="2"
                          >
                            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
                          </svg>
                        </button>
                      ))}
                      <span className="ml-2 text-sm text-gray-600">
                        {rating}/5
                      </span>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Your Review (optional)
                    </label>
                    <textarea
                      value={comment}
                      onChange={(e) => setComment(e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-orange-500"
                      rows={3}
                      maxLength={1000}
                      placeholder="Share your experience with this provider..."
                    />
                    <p className="text-xs text-gray-400 mt-1">
                      {comment.length}/1000 characters
                    </p>
                  </div>

                  <div className="flex justify-end gap-2">
                    <button
                      onClick={cancelReview}
                      className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800"
                    >
                      Cancel
                    </button>
                    <button
                      onClick={() => handleSubmitReview(lead.id)}
                      disabled={submitting}
                      className="px-4 py-2 bg-orange-500 text-white text-sm font-medium rounded-lg hover:bg-orange-600 disabled:opacity-50"
                    >
                      {submitting ? 'Submitting...' : 'Submit Review'}
                    </button>
                  </div>
                </div>
              ) : lead.has_review ? (
                <Link
                  href={`/${lang}/client/dashboard/reviews`}
                  className="text-sm text-green-600 hover:text-green-700 font-medium"
                >
                  View your review →
                </Link>
              ) : (
                <button
                  onClick={() => startReview(lead.id)}
                  className="text-sm text-orange-500 hover:text-orange-600 font-medium"
                >
                  Write a review
                </button>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
