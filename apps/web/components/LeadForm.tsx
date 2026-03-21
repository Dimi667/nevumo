'use client';
import { useState } from 'react';
import { createLead } from '@/lib/api';

interface Props {
  categorySlug: string;
  citySlug: string;
  providerSlug: string;
}

export default function LeadForm({ categorySlug, citySlug, providerSlug }: Props) {
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(false);
    const formData = new FormData(e.currentTarget);
    try {
      const result = await createLead({
        category_slug: categorySlug,
        city_slug: citySlug,
        provider_slug: providerSlug,
        phone: formData.get('phone') as string,
        description: (formData.get('description') as string) || undefined,
        source: 'seo',
      });
      if (result) setSubmitted(true);
      else setError(true);
    } catch {
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <div className="text-center py-6">
        <p className="text-3xl mb-3">✅</p>
        <p className="font-semibold text-gray-900 text-lg">Request sent successfully!</p>
        <p className="text-sm text-gray-500 mt-1">The provider will contact you soon.</p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-semibold text-gray-700 mb-1">
          Phone number
        </label>
        <input
          name="phone"
          type="tel"
          required
          placeholder="+359 888 123 456"
          className="w-full border border-gray-300 rounded-lg px-4 py-3 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent"
        />
      </div>

      <div>
        <label className="block text-sm font-semibold text-gray-700 mb-1">
          Description (optional)
        </label>
        <textarea
          name="description"
          rows={3}
          placeholder="Describe what service you need..."
          className="w-full border border-gray-300 rounded-lg px-4 py-3 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent resize-none"
        />
      </div>

      {error && (
        <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-4 py-2">
          Something went wrong. Please try again.
        </p>
      )}

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-orange-500 hover:bg-orange-600 disabled:bg-orange-300 text-white font-bold py-3 rounded-lg transition-colors text-base"
      >
        {loading ? 'Sending...' : 'Send Request'}
      </button>
    </form>
  );
}
