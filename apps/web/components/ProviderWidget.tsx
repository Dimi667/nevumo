'use client';

import { useState, useEffect } from 'react';
import { createLead, type ProviderDetail, getCityBySlug, type CityOut } from '@/lib/api';
import { validatePhone, getPhonePlaceholder, COUNTRY_PHONE_CODES } from '@/lib/phoneUtils';

interface ProviderWidgetProps {
  provider: ProviderDetail;
  categoryName: string;
  categorySlug: string;
  citySlug: string;
}

export default function ProviderWidget({
  provider,
  categoryName,
  categorySlug,
  citySlug,
}: ProviderWidgetProps) {
  const t = provider.translations;
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState(false);
  const [phoneError, setPhoneError] = useState<string | null>(null);
  const [cityInfo, setCityInfo] = useState<CityOut | null>(null);
  const [phoneValue, setPhoneValue] = useState('');

  const hasStats = provider.rating > 0 || provider.jobs_completed > 0;

  useEffect(() => {
    const fetchCityInfo = async () => {
      const city = await getCityBySlug(citySlug);
      setCityInfo(city);
    };
    fetchCityInfo();
  }, [citySlug]);

  const handlePhoneChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setPhoneValue(value);
    
    if (value.trim().length > 0) {
      const validation = validatePhone(value, cityInfo?.country_code);
      setPhoneError(validation.isValid ? null : validation.error ?? null);
    } else {
      setPhoneError(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    // Validate phone before submission
    const validation = validatePhone(phoneValue, cityInfo?.country_code);
    if (!validation.isValid) {
      setPhoneError(validation.error ?? null);
      return;
    }
    
    setLoading(true);
    setError(false);
    const formData = new FormData(e.currentTarget);
    try {
      const result = await createLead({
        category_slug: categorySlug,
        city_slug: citySlug,
        provider_slug: provider.slug,
        phone: formData.get('phone') as string,
        description: (formData.get('description') as string) || undefined,
        source: 'widget',
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
      <div className="text-center py-8">
        <div className="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center mx-auto mb-4">
          <span className="text-green-600 text-3xl">✓</span>
        </div>
        <p className="font-bold text-gray-900 text-lg mb-1">
          {t.success_title || '✓ Successfully sent!'}
        </p>
        <p className="text-sm text-gray-500">
          {t.success_message || 'We will contact you soon.'}
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
      {/* Logo */}
      <div className="px-4 pt-6 pb-2 text-center">
        <img 
          src="/Nevumo_logo.svg" 
          alt="Nevumo" 
          className="mx-auto opacity-70 mb-4"
          style={{ height: '28px' }}
        />
      </div>

      {/* Provider Info */}
      <div className="px-6 pt-4 text-center">
        {/* Avatar */}
        <div className="w-[200px] h-[200px] rounded-full bg-orange-100 flex items-center justify-center mx-auto mb-4 overflow-hidden">
          {provider.profile_image_url ? (
            <img
              src={provider.profile_image_url}
              alt={provider.business_name}
              className="w-full h-full object-cover"
            />
          ) : (
            <span className="text-orange-600 text-4xl font-bold">
              {provider.business_name.charAt(0).toUpperCase()}
            </span>
          )}
        </div>

        <h1 className="text-2xl font-bold text-gray-900 mb-1">
          {provider.business_name}
        </h1>

        {/* Job Title from category */}
        <p className="text-base font-bold text-gray-500 mb-3">{categoryName}</p>

        {/* Rating & Jobs - only if > 0 */}
        {hasStats && (
          <div className="flex items-center justify-center gap-2 flex-wrap text-sm mb-2">
            {provider.rating > 0 && (
              <span className="text-gray-700 font-bold text-base">
                ⭐ {provider.rating.toFixed(1)} {t.rating_label || 'rating'}
              </span>
            )}
            {provider.rating > 0 && provider.jobs_completed > 0 && (
              <span className="text-gray-400">•</span>
            )}
            {provider.jobs_completed > 0 && (
              <span className="text-gray-700 font-bold text-base">
                {provider.jobs_completed} {t.jobs_label || 'jobs completed'}
              </span>
            )}
          </div>
        )}

        {/* Verified badge */}
        {provider.verified && (
          <span className="inline-flex items-center gap-1 text-base font-bold text-green-600">
            {t.verified_label || 'Verified professional'}
          </span>
        )}
      </div>

      {/* Form */}
      <div className="px-6 py-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4 text-center">
          {t.button_text || 'Request Service'}
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-1">
              {t.phone_label || 'Phone'}
            </label>
            <input
              name="phone"
              type="tel"
              required
              value={phoneValue}
              onChange={handlePhoneChange}
              placeholder={getPhonePlaceholder(cityInfo?.country_code)}
              className={`w-full border rounded-lg px-4 py-3 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent text-base ${
                phoneError 
                  ? 'border-red-300 focus:ring-red-400' 
                  : 'border-gray-300'
              }`}
            />
          </div>

          <div>
            <label className="block text-sm font-bold text-gray-700 mb-1">
              {t.notes_label || 'Notes'}
            </label>
            <textarea
              name="description"
              rows={3}
              placeholder={
                t.notes_placeholder ||
                'Describe your request (time, address, details)'
              }
              className="w-full border border-gray-300 rounded-lg px-4 py-3 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent resize-none text-base"
            />
          </div>

          <p className="text-sm text-gray-700 italic text-center">
            {t.response_time || '⏱ Provider usually responds within 30 minutes'}
          </p>

          {phoneError && (
            <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
              {phoneError}
            </p>
          )}

          {error && (
            <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
              Something went wrong. Please try again.
            </p>
          )}

          {/* Sticky button mobile / inline desktop */}
          <div className="fixed bottom-0 left-0 right-0 z-50 p-4 bg-white border-t border-gray-100 md:static md:p-0 md:bg-transparent md:border-0">
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-orange-500 hover:bg-orange-600 disabled:bg-orange-300 text-white font-bold py-3 rounded-lg transition-colors text-xl"
            >
              {loading ? 'Sending...' : t.button_text || 'Request Service'}
            </button>
          </div>
        </form>

        <p className="text-sm text-gray-400 text-center mt-4 md:mt-4 pb-16 md:pb-0">
          {t.disclaimer || 'Free request • No obligation'}
        </p>
      </div>
    </div>
  );
}
