'use client';
import { useState, useEffect } from 'react';
import { createLead } from '@/lib/api';
import { usePhone } from '@/hooks/usePhone';
import PhoneInput from '@/components/ui/PhoneInput';

interface Props {
  categorySlug: string;
  citySlug: string;
  providerSlug: string;
  countryCode?: string;
}

export default function LeadForm({ categorySlug, citySlug, providerSlug, countryCode }: Props) {
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState(false);
  const [phoneValue, setPhoneValue] = useState('');
  const { phone: savedPhone, savePhone, loading: phoneLoading } = usePhone();

  useEffect(() => {
    if (savedPhone && !phoneValue) {
      setPhoneValue(savedPhone);
    }
  }, [savedPhone]);

  const handleChange = (value: string) => {
    setPhoneValue(value);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(false);
    
    try {
      const result = await createLead({
        category_slug: categorySlug,
        city_slug: citySlug,
        provider_slug: providerSlug,
        phone: phoneValue,
        description: (e.currentTarget.description as HTMLTextAreaElement)?.value || undefined,
        source: 'seo',
      });
      if (result) {
        setSubmitted(true);
        // Save phone on successful submit
        savePhone(phoneValue);
      } else {
        setError(true);
      }
    } catch {
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <div className="text-center py-6">
        <div className="w-14 h-14 rounded-full bg-green-100 flex items-center justify-center mx-auto mb-3">
          <span className="text-green-600 text-2xl">✓</span>
        </div>
        <p className="font-bold text-gray-900 text-base mb-1">Request sent successfully!</p>
        <p className="text-sm text-gray-500">The provider will contact you soon.</p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <PhoneInput
        value={phoneValue}
        onChange={handleChange}
        countryCode={countryCode}
        label="Phone"
        required
      />

      <div>
        <label className="block text-sm font-bold text-gray-700 mb-1">Notes</label>
        <textarea
          name="description"
          rows={3}
          placeholder="Describe your request (time, address, details)"
          className="w-full border border-gray-300 rounded-lg px-4 py-3 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent resize-none text-sm"
        />
      </div>

      <p className="text-xs text-gray-400 italic flex items-center gap-1">
        <span>⏱</span>
        <span>Provider usually responds within 30 minutes</span>
      </p>

      {error && (
        <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
          Something went wrong. Please try again.
        </p>
      )}

      {/* Mobile: sticky fixed at bottom. Desktop: inline */}
      <div className="fixed bottom-0 left-0 right-0 z-50 p-4 bg-white border-t border-gray-100 md:static md:p-0 md:bg-transparent md:border-0">
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-orange-500 hover:bg-orange-600 disabled:bg-orange-300 text-white font-semibold py-3 rounded-lg transition-colors text-base"
        >
          {loading ? 'Sending...' : 'Request Service'}
        </button>
      </div>
    </form>
  );
}
