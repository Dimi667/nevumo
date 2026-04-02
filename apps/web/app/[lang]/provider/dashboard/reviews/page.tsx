'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { getProviderReviews, addReviewReply, updateReviewReply } from '@/lib/review-api';
import type { ProviderReviewItem } from '@/types/review';

export default function ProviderReviewsPage() {
  const params = useParams();
  const lang = typeof params.lang === 'string' ? params.lang : 'en';

  const [reviews, setReviews] = useState<ProviderReviewItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeFilter, setActiveFilter] = useState<'all' | 'unreplied'>('all');
  const [replyingTo, setReplyingTo] = useState<string | null>(null);
  const [editReplyId, setEditReplyId] = useState<string | null>(null);
  const [replyText, setReplyText] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    loadReviews();
  }, [activeFilter]);

  async function loadReviews() {
    try {
      setLoading(true);
      const data = await getProviderReviews({
        unrepliedOnly: activeFilter === 'unreplied',
      });
      setReviews(data.items);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to load reviews');
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmitReply(reviewId: string, isEdit: boolean) {
    if (!replyText.trim()) return;

    try {
      setSubmitting(true);
      if (isEdit) {
        await updateReviewReply(reviewId, replyText.trim());
      } else {
        await addReviewReply(reviewId, replyText.trim());
      }

      // Refresh reviews
      await loadReviews();

      // Reset form
      setReplyingTo(null);
      setEditReplyId(null);
      setReplyText('');
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to submit reply');
    } finally {
      setSubmitting(false);
    }
  }

  function startEdit(review: ProviderReviewItem) {
    setEditReplyId(review.id);
    setReplyingTo(null);
    setReplyText(review.provider_reply || '');
  }

  function startReply(reviewId: string) {
    setReplyingTo(reviewId);
    setEditReplyId(null);
    setReplyText('');
  }

  function cancelReply() {
    setReplyingTo(null);
    setEditReplyId(null);
    setReplyText('');
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const unrepliedCount = reviews.filter(r => !r.provider_reply).length;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-gray-900">Reviews</h1>
        <p className="text-sm text-gray-500 mt-0.5">
          Manage your client reviews and replies
        </p>
      </div>

      {/* Filter tabs */}
      <div className="flex gap-2 border-b border-gray-200">
        <button
          onClick={() => setActiveFilter('all')}
          className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
            activeFilter === 'all'
              ? 'border-orange-500 text-orange-600'
              : 'border-transparent text-gray-600 hover:text-gray-900'
          }`}
        >
          All Reviews
          <span className="ml-2 px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded-full">
            {reviews.length}
          </span>
        </button>
        <button
          onClick={() => setActiveFilter('unreplied')}
          className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
            activeFilter === 'unreplied'
              ? 'border-orange-500 text-orange-600'
              : 'border-transparent text-gray-600 hover:text-gray-900'
          }`}
        >
          Unreplied
          {unrepliedCount > 0 && (
            <span className="ml-2 px-2 py-0.5 bg-orange-100 text-orange-600 text-xs rounded-full">
              {unrepliedCount}
            </span>
          )}
        </button>
      </div>

      {error && (
        <div className="bg-red-50 text-red-700 rounded-lg p-4 text-sm">
          {error}
        </div>
      )}

      {/* Reviews list */}
      <div className="space-y-4">
        {reviews.length === 0 ? (
          <div className="bg-gray-50 rounded-xl p-8 text-center">
            <div className="text-4xl mb-3">⭐</div>
            <h3 className="text-lg font-medium text-gray-900 mb-1">No reviews yet</h3>
            <p className="text-sm text-gray-500">
              When clients review your services, they will appear here.
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
                      {review.client_name}
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
                {!review.provider_reply && (
                  <span className="px-2 py-1 bg-orange-100 text-orange-600 text-xs font-medium rounded-full">
                    Needs Reply
                  </span>
                )}
              </div>

              {/* Client comment */}
              {review.comment && (
                <div className="bg-gray-50 rounded-lg p-3 mb-4">
                  <p className="text-sm text-gray-700">{review.comment}</p>
                </div>
              )}

              {/* Provider reply section */}
              {review.provider_reply ? (
                <div className="bg-blue-50 rounded-lg p-3 border-l-4 border-blue-400">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-medium text-blue-600">Your Reply</span>
                    <div className="flex items-center gap-2">
                      {review.is_reply_edited && (
                        <span className="text-xs text-gray-500">
                          Edited {review.provider_reply_edited_at
                            ? new Date(review.provider_reply_edited_at).toLocaleDateString()
                            : ''}
                        </span>
                      )}
                      <button
                        onClick={() => startEdit(review)}
                        className="text-xs text-blue-600 hover:text-blue-700 font-medium"
                      >
                        Edit
                      </button>
                    </div>
                  </div>
                  {editReplyId === review.id ? (
                    <div className="space-y-2">
                      <textarea
                        value={replyText}
                        onChange={(e) => setReplyText(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                        rows={3}
                        maxLength={2000}
                        placeholder="Write your reply..."
                      />
                      <div className="flex justify-end gap-2">
                        <button
                          onClick={cancelReply}
                          className="px-3 py-1.5 text-xs text-gray-600 hover:text-gray-800"
                        >
                          Cancel
                        </button>
                        <button
                          onClick={() => handleSubmitReply(review.id, true)}
                          disabled={submitting || !replyText.trim()}
                          className="px-3 py-1.5 bg-blue-500 text-white text-xs font-medium rounded-lg hover:bg-blue-600 disabled:opacity-50"
                        >
                          {submitting ? 'Saving...' : 'Save Changes'}
                        </button>
                      </div>
                    </div>
                  ) : (
                    <p className="text-sm text-gray-700">{review.provider_reply}</p>
                  )}
                </div>
              ) : replyingTo === review.id ? (
                <div className="space-y-2">
                  <textarea
                    value={replyText}
                    onChange={(e) => setReplyText(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-orange-500"
                    rows={3}
                    maxLength={2000}
                    placeholder="Write your reply to this review..."
                  />
                  <div className="flex justify-end gap-2">
                    <button
                      onClick={cancelReply}
                      className="px-3 py-1.5 text-xs text-gray-600 hover:text-gray-800"
                    >
                      Cancel
                    </button>
                    <button
                      onClick={() => handleSubmitReply(review.id, false)}
                      disabled={submitting || !replyText.trim()}
                      className="px-3 py-1.5 bg-orange-500 text-white text-xs font-medium rounded-lg hover:bg-orange-600 disabled:opacity-50"
                    >
                      {submitting ? 'Sending...' : 'Send Reply'}
                    </button>
                  </div>
                </div>
              ) : (
                <button
                  onClick={() => startReply(review.id)}
                  className="text-sm text-orange-500 hover:text-orange-600 font-medium"
                >
                  Reply to this review
                </button>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
