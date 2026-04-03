'use client';

import { useState, useEffect } from 'react';
import { createLead, type ProviderDetail, getCityBySlug, type CityOut } from '@/lib/api';
import { validatePhone, getPhonePlaceholder } from '@/lib/phoneUtils';

interface ProviderWidgetProps {
  provider: ProviderDetail;
  categoryName: string;
  categorySlug: string;
  citySlug: string;
}

// Helper for compact relative time
function getRelativeTime(dateString: string, locale: string = 'en'): string {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
  const diffMinutes = Math.floor(diffMs / (1000 * 60));

  // Bulgarian translations
  if (locale === 'bg') {
    if (diffMinutes < 1) return 'преди минута';
    if (diffMinutes < 60) return `преди ${diffMinutes} мин`;
    if (diffHours < 24) return `преди ${diffHours} ч`;
    if (diffDays === 1) return 'преди 1 ден';
    if (diffDays < 7) return `преди ${diffDays} дни`;
    if (diffDays < 30) return `преди ${Math.floor(diffDays / 7)} седмици`;
    return `преди ${Math.floor(diffDays / 30)} месеца`;
  }

  // Default English
  if (diffMinutes < 1) return 'just now';
  if (diffMinutes < 60) return `${diffMinutes}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays === 1) return '1 day ago';
  if (diffDays < 7) return `${diffDays} days ago`;
  if (diffDays < 30) return `${Math.floor(diffDays / 7)}w ago`;
  return `${Math.floor(diffDays / 30)}mo ago`;
}

// Star rating component
function StarRating({ rating }: { rating: number }) {
  return (
    <span className="inline-flex items-center">
      {[1, 2, 3, 4, 5].map((star) => (
        <svg
          key={star}
          className={`w-3.5 h-3.5 ${star <= rating ? 'text-yellow-400' : 'text-gray-200'}`}
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
      ))}
    </span>
  );
}

function getInitial(value: string): string {
  return value.trim().charAt(0).toUpperCase() || 'C';
}

function formatTranslation(template: string, replacements: Record<string, string>): string {
  return Object.entries(replacements).reduce(
    (result, [key, value]) => result.replace(new RegExp(`\\{${key}\\}`, 'g'), value),
    template,
  );
}

function RecentRequestBlock({
  latestLeadPreview,
  locale,
  text,
}: {
  latestLeadPreview: NonNullable<ProviderDetail['latest_lead_preview']>;
  locale: string;
  text: string;
}) {
  const timeAgo = getRelativeTime(latestLeadPreview.created_at, locale);

  return (
    <div className="bg-gray-50 rounded-xl p-4 mb-3 border border-gray-100 text-left max-w-sm mx-auto">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-orange-100 flex items-center justify-center overflow-hidden flex-shrink-0">
          {latestLeadPreview.client_image_url ? (
            <img
              src={latestLeadPreview.client_image_url}
              alt={latestLeadPreview.client_name}
              className="w-full h-full object-cover"
            />
          ) : (
            <span className="text-orange-600 text-sm font-bold">
              {getInitial(latestLeadPreview.client_name)}
            </span>
          )}
        </div>
        <div className="min-w-0">
          <p className="text-sm font-semibold text-gray-900 leading-snug">{text}</p>
          <p className="text-xs text-gray-400 mt-1">{timeAgo}</p>
        </div>
      </div>
    </div>
  );
}

function CityDemandBlock({ text }: { text: string }) {
  return (
    <div className="bg-gray-50 rounded-xl p-4 mb-4 border border-gray-100">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-orange-100 flex items-center justify-center flex-shrink-0 text-lg">
          👥
        </div>
        <p className="text-sm font-semibold text-gray-900 leading-snug text-left">{text}</p>
      </div>
    </div>
  );
}

function ChecklistBlock({ items }: { items: string[] }) {
  return (
    <div className="bg-gray-50 rounded-xl p-4 mb-4 border border-gray-100 space-y-2">
      {items.map((item) => (
        <div key={item} className="flex items-start gap-2 text-left">
          <span className="text-green-600 font-bold">✓</span>
          <span className="text-sm font-medium text-gray-900 leading-snug">{item}</span>
        </div>
      ))}
    </div>
  );
}

// Social Proof block component
function SocialProofBlock({ review, locale }: { review: ProviderDetail['latest_review']; locale: string }) {
  if (!review) return null;

  const initial = getInitial(review.client_name);
  const timeAgo = getRelativeTime(review.created_at, locale);

  return (
    <div className="bg-gray-50 rounded-xl p-4 mb-4 border border-gray-100">
      <div className="flex items-start gap-3">
        {/* Avatar with initial */}
        <div className="w-9 h-9 rounded-full bg-orange-100 flex items-center justify-center flex-shrink-0">
          <span className="text-orange-600 text-sm font-bold">{initial}</span>
        </div>
        
        {/* Content */}
        <div className="flex-1 min-w-0">
          {/* Header: name, stars, time */}
          <div className="flex items-center gap-2 flex-wrap mb-1">
            <span className="font-semibold text-gray-900 text-sm">{review.client_name}</span>
            <StarRating rating={review.rating} />
            <span className="text-xs text-gray-400">{timeAgo}</span>
          </div>

          {review.comment_preview && (
            <p className="text-sm text-gray-600 line-clamp-2">
              &ldquo;{review.comment_preview}&rdquo;
            </p>
          )}
        </div>
      </div>
    </div>
  );
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
  const locale = (typeof document !== 'undefined' && document.documentElement.lang) || 'en';
  const cityName = cityInfo?.name ?? citySlug;
  const jobsLabel = t.jobs_label || 'jobs completed';
  const cityLeadsText = formatTranslation(
    t.city_leads_label || '{count} requests for {category} in {city} this year',
    {
      count: new Intl.NumberFormat(locale).format(provider.city_leads),
      category: categoryName.toLocaleLowerCase(locale),
      city: cityName,
    },
  );
  const recentRequestText = provider.latest_lead_preview
    ? formatTranslation(
        t.recent_request_label || '{name} from {city} requested recently',
        {
          name: provider.latest_lead_preview.client_name,
          city: provider.latest_lead_preview.city_name,
        },
      )
    : null;
  const checklistItems = [
    t.free_request_no_obligation || 'Free request, no obligation',
    t.no_registration || 'No registration',
    t.direct_contact_with_provider || 'Direct contact with the provider',
  ];

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
        <p className="text-sm text-gray-500 mb-6">
          {provider.business_name}{t.success_message_received || ' received your request and will contact you by phone.'}
        </p>
        <button
          onClick={() => setSubmitted(false)}
          className="bg-orange-500 hover:bg-orange-600 text-white font-bold py-3 rounded-lg transition-colors text-base px-6"
        >
          {t.new_request_button || 'New Request'}
        </button>
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

        {provider.rating > 0 ? (
          <div className="flex items-center justify-center gap-2 flex-wrap text-sm mb-2">
            <span className="text-gray-700 font-bold text-base">
              ⭐ {provider.rating.toFixed(1)} {t.rating_label || 'rating'}
            </span>
            <span className="text-gray-400">•</span>
            <span className="text-gray-700 font-bold text-base">
              {provider.jobs_completed} {jobsLabel}
            </span>
          </div>
        ) : provider.jobs_completed > 0 ? (
          <div className="flex items-center justify-center text-sm mb-2">
            <span className="text-gray-700 font-bold text-base">
              {provider.jobs_completed} {jobsLabel}
            </span>
          </div>
        ) : provider.leads_received > 0 && provider.latest_lead_preview && recentRequestText ? (
          <RecentRequestBlock
            latestLeadPreview={provider.latest_lead_preview}
            locale={locale}
            text={recentRequestText}
          />
        ) : (
          <div className="flex items-center justify-center gap-2 flex-wrap text-sm mb-2">
            <span className="text-gray-700 font-bold text-base">{t.new_badge || 'New'}</span>
            <span className="text-gray-400">·</span>
            <span className="text-gray-700 font-bold text-base">{t.no_reviews_yet || 'No reviews yet'}</span>
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

          {provider.review_count > 0 && provider.latest_review ? (
            <SocialProofBlock review={provider.latest_review} locale={locale} />
          ) : provider.city_leads > 0 ? (
            <CityDemandBlock text={cityLeadsText} />
          ) : (
            <ChecklistBlock items={checklistItems} />
          )}

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
