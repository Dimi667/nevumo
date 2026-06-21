'use client';

import { useState, useEffect, useRef } from 'react';
import Image from 'next/image';
import { createLead, claimLeadEmail, type ProviderDetail, getCityBySlug, type CityOut } from '@/lib/api';
import { checkEmail } from '@/lib/auth-api';
import { usePhone } from '@/hooks/usePhone';
import { usePhoneValidation } from '@/hooks/usePhoneValidation';
import { useIsIOS26Plus } from '@/hooks/useIsIOS26Plus';
import PhoneInput from '@/components/ui/PhoneInput';
import { getPhonePrefix } from '@/lib/phoneUtils';
import PWAInstallPrompt from '@/components/pwa/PWAInstallPrompt';
import PushPermissionPrompt from '@/components/push/PushPermissionPrompt';
import { getCurrency, formatCurrency } from '@/lib/currency';
import { JsonLd } from '@/components/JsonLd';
import { resolveStaticUrl } from '@/lib/urlUtils';
import LegalModal from '@/components/auth/LegalModal';
import { useTranslation } from '@/lib/use-translation';
import { getAuthUser } from '@/lib/auth-store';
import StickyBottomBar from '@/components/ui/StickyBottomBar';

interface ProviderWidgetProps {
  provider: ProviderDetail;
  categoryName: string;
  categorySlug: string;
  citySlug: string;
  countryCode?: string;
  isEmbed?: boolean;
  translations?: Record<string, string>;
  lang?: string;
}

// Helper for compact relative time
function getRelativeTime(dateString: string, t: (key: string, params?: Record<string, string | number>) => string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMinutes = Math.floor(diffMs / (1000 * 60));
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

  if (diffMinutes < 1) return t('time_just_now');
  if (diffMinutes < 60) {
    if (diffMinutes === 1) return t('time_min_ago_one');
    return t('time_min_ago_many', { count: diffMinutes });
  }
  if (diffHours < 24) {
    return t('time_hour_ago_many', { count: diffHours });
  }
  if (diffDays === 1) return t('time_day_ago_one');
  if (diffDays < 7) return t('time_day_ago_many', { count: diffDays });
  if (diffDays < 30) return t('time_week_ago_many', { count: Math.floor(diffDays / 7) });
  return t('time_month_ago_many', { count: Math.floor(diffDays / 30) });
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

function formatServicePrice(
  service: { base_price: number | null; price_type: string; currency: string },
  perHour: string,
  onRequest: string
): string {
  if (!service.base_price || service.price_type === 'request') return onRequest;
  if (service.price_type === 'hourly') return `${service.base_price} ${service.currency}${perHour}`;
  if (service.price_type === 'per_sqm') return `${service.base_price} ${service.currency}/m²`;
  return `${service.base_price} ${service.currency}`;
}

function RecentRequestBlock({
  latestLeadPreview,
  t,
  text,
}: {
  latestLeadPreview: NonNullable<ProviderDetail['latest_lead_preview']>;
  t: (key: string, params?: Record<string, string | number>) => string;
  text: string;
}) {
  const timeAgo = getRelativeTime(latestLeadPreview.created_at, t);

  return (
    <div className="bg-gray-50 rounded-xl p-4 mb-3 border border-gray-100 text-left max-w-sm mx-auto">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-orange-100 flex items-center justify-center overflow-hidden flex-shrink-0 relative">
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
          <p className="text-xs text-gray-400 mt-1" suppressHydrationWarning>{timeAgo}</p>
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
function SocialProofBlock({ review, t }: { review: ProviderDetail['latest_review']; t: (key: string, params?: Record<string, string | number>) => string }) {
  if (!review) return null;

  const initial = getInitial(review.client_name);
  const timeAgo = getRelativeTime(review.created_at, t);

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
            <span className="text-xs text-gray-400" suppressHydrationWarning>{timeAgo}</span>
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
  countryCode,
  isEmbed,
  translations: externalTranslations,
  lang: propLang,
}: ProviderWidgetProps) {
  const translations = externalTranslations || provider.translations || {};
  const t = (key: string, replacements?: Record<string, string | number>, defaultValue?: string) => {
    const template = translations[`widget.${key}`] || translations[key] || defaultValue || key;
    if (!replacements) return template;
    return formatTranslation(template, Object.fromEntries(
      Object.entries(replacements).map(([k, v]) => [k, String(v)])
    ));
  };

  console.log('[ProviderWidget DEBUG]', { 
    hasTranslations: !!provider.translations,
    translationsType: typeof provider.translations,
    translationKeys: Object.keys(provider.translations || {}),
    buttonText: t('button_text'),
    providerSlug: provider.slug
  });
  const [loading, setLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [leadId, setLeadId] = useState<string | null>(null);
  const [successStep, setSuccessStep] = useState<'sent' | 'email'>('sent');
  const [email, setEmail] = useState('');
  const [isEmailSubmitting, setIsEmailSubmitting] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [error, setError] = useState(false);
  const [cityInfo, setCityInfo] = useState<CityOut | null>(null);
  const [phoneValue, setPhoneValue] = useState('');
  const phoneRef = useRef<HTMLDivElement>(null);
  const stickyDivRef = useRef<HTMLDivElement>(null);
  const { isValid } = usePhoneValidation(phoneValue, cityInfo?.country_code || 'BG');
  const isIOS26Plus = useIsIOS26Plus();
  const [selectedServiceId, setSelectedServiceId] = useState<string | null>(null);
  const [descriptionValue, setDescriptionValue] = useState('');
  const [serviceNoteError, setServiceNoteError] = useState<string | null>(null);
  const [showPWAPrompt, setShowPWAPrompt] = useState(false);
  const [showPushPrompt, setShowPushPrompt] = useState(false);
  const [legalModalOpen, setLegalModalOpen] = useState(false);
  const [legalModalType, setLegalModalType] = useState<'terms' | 'terms-provider' | 'privacy'>('terms');
  const [formSubmitted, setFormSubmitted] = useState(false);
  const lang = propLang || (typeof document !== 'undefined' && document.documentElement.lang) || 'en';
  const { dict: termsDict } = useTranslation('terms', lang);
  const { dict: termsProviderDict } = useTranslation('provider_terms', lang);
  
  const user = getAuthUser();
  const role = (user?.role === 'provider' ? 'provider' : 'client') as 'provider' | 'client';
  const { dict: privacyDict } = useTranslation('privacy', lang);

  const getDocDict = () => {
    switch (legalModalType) {
      case 'terms':
        return termsDict;
      case 'terms-provider':
        return termsProviderDict;
      case 'privacy':
        return privacyDict;
      default:
        return {};
    }
  };
  const effectiveCountryCode = countryCode ?? cityInfo?.country_code;
  const currency = provider.services[0]?.currency || getCurrency(effectiveCountryCode, cityInfo?.currency);

  // Use runtime URL resolution for provider image
  const profileImageUrl = resolveStaticUrl(provider.profile_image_url);

  // Debug log
  console.log('[ProviderWidget Image URL]', { 
    original: provider.profile_image_url,
    final: profileImageUrl,
  });

  const handleChange = (value: string) => {
    setPhoneValue(value);
  };
  const cityName = cityInfo?.city ?? citySlug;
  const jobsLabel = t('jobs_label', undefined, 'jobs completed');
  const cityLeadsText = t('city_leads_label', {
      count: new Intl.NumberFormat(lang).format(provider.city_leads),
      category: categoryName.toLocaleLowerCase(lang),
      city: cityName,
    }, '{count} requests for {category} in {city} this year');

  const recentRequestText = provider.latest_lead_preview
    ? t('recent_request_label', {
          name: provider.latest_lead_preview.client_name,
          city: provider.latest_lead_preview.city_name,
        }, '{name} from {city} requested recently')
    : null;
  const checklistItems = [
    translations['trust_verified'] ?? 'Без регистрация',
    translations['trust_free'] ?? 'Без разходи!',
    translations['trust_direct'] ?? 'Директен контакт',
  ];

  // Show all provider services (no category filter)
  const filteredServices = provider.services;

  const serviceJsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Service',
    name: `${categoryName} - ${provider.business_name}`,
    provider: {
      '@type': 'LocalBusiness',
      name: provider.business_name,
      image: provider.profile_image_url || undefined,
      address: {
        '@type': 'PostalAddress',
        addressLocality: cityName,
        addressCountry: countryCode || cityInfo?.country_code || 'BG',
      },
    },
    areaServed: {
      '@type': 'City',
      name: cityName,
    },
    offers: filteredServices.map((s) => ({
      '@type': 'Offer',
      itemOffered: {
        '@type': 'Service',
        name: s.title,
      },
      price: s.base_price || undefined,
      priceCurrency: currency,
    })),
  };

  // Handle service chip click with toggle logic
  const handleServiceClick = (serviceId: string) => {
    setServiceNoteError(null);
    if (selectedServiceId === serviceId) {
      // Deselect if already selected
      setSelectedServiceId(null);
      setDescriptionValue('');
    } else {
      // Select and auto-fill
      setSelectedServiceId(serviceId);
      const service = filteredServices.find(s => s.id === serviceId);
      if (service) {
        const serviceText = `${service.title} - ${formatServicePrice(service, t('price_per_hour', undefined, '/h'), t('price_on_request', undefined, 'Price on request'))}`;
        setDescriptionValue(serviceText);
      }
      document.getElementById('widget-form')?.scrollIntoView({ behavior: 'smooth' });
    }
  };
  
  // Handle manual textarea input
  const handleDescriptionChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setDescriptionValue(e.target.value);
    setServiceNoteError(null);
  };

  useEffect(() => {
    const fetchCityInfo = async () => {
      const city = await getCityBySlug(citySlug);
      setCityInfo(city);
    };
    fetchCityInfo();

    // Check if user is logged in
    const token = localStorage.getItem('nevumo_auth_token');
    setIsLoggedIn(!!token);
  }, [citySlug]);

  // Set body padding for sticky element on mobile
  useEffect(() => {
    const stickyDiv = stickyDivRef.current;
    if (!stickyDiv) return;

    const setBodyPadding = () => {
      if (window.innerWidth < 768) {
        const height = stickyDiv.offsetHeight;
        document.body.style.paddingBottom = height + 'px';
      }
    };

    setBodyPadding();

    return () => {
      document.body.style.paddingBottom = '';
    };
  }, []);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setFormSubmitted(true);

    // Validation using isValid from usePhone hook
    if (!phoneValue || !isValid) {
      phoneRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' });
      setError(false);
      return;
    }

    // Validate service or note
    if (selectedServiceId === null && descriptionValue.trim().length === 0) {
      setServiceNoteError(t('error_service_or_note') ?? 'Моля изберете услуга или напишете бележка');
      return;
    }

    setLoading(true);
    setError(false);
    
    try {
      const result = await createLead({
        category_slug: categorySlug,
        city_slug: citySlug,
        provider_slug: provider.slug,
        phone: phoneValue.trim(),
        description: descriptionValue || undefined,
        source: 'widget',
      });
      if (result) {
        if ('lead_id' in result) {
          setLeadId(result.lead_id);
        }
        setIsSuccess(true);
        setSuccessStep('sent');
        // Show push prompt after 2 seconds
        setTimeout(() => setShowPushPrompt(true), 2000);
        // Show PWA prompt after 2 seconds
        setTimeout(() => { setShowPWAPrompt(true); }, 2000);
      } else {
        setError(true);
      }
    } catch {
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  const handleContinueWithEmail = () => {
    setSuccessStep('email');
  };

  const handleBackToSent = () => {
    setSuccessStep('sent');
    setEmail('');
  };

  const isValidEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleEmailSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isValidEmail(email) || !leadId) return;

    setIsEmailSubmitting(true);

    try {
      // Check if email already exists
      const { exists } = await checkEmail(email);

      // Call API to register the claim email
      await claimLeadEmail(leadId, email, phoneValue);

      // Save to localStorage
      const pendingClaim = {
        lead_id: leadId,
        email: email,
        phone: phoneValue,
        submitted_at: Date.now(),
      };
      localStorage.setItem('nevumo_pending_claim', JSON.stringify(pendingClaim));

      // Get lang from URL or state
      const currentLang = lang;

      // Redirect to auth with email and mode based on whether user exists
      const mode = exists ? 'login' : 'register';
      const redirectUrl = `/${currentLang}/auth?email=${encodeURIComponent(email)}&intent=client&mode=${mode}`;
      window.location.href = redirectUrl;
    } catch {
      setIsEmailSubmitting(false);
    }
  };

  const handleNoThanks = () => {
    setIsSuccess(false);
    setSuccessStep('sent');
    setLeadId(null);
    setEmail('');
    setIsEmailSubmitting(false);
    setError(false);
    setSelectedServiceId(null);
    setDescriptionValue('');
    setPhoneValue('');
    setFormSubmitted(false);
  };

  if (isSuccess) {
    // If logged in, show simple success message
    if (isLoggedIn) {
      return (
        <div className="text-center py-8">
          <JsonLd data={serviceJsonLd} />
          <div className="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center mx-auto mb-4">
            <span className="text-green-600 text-3xl">✓</span>
          </div>
          <p className="font-bold text-gray-900 text-lg mb-1">
            {t('success_title', undefined, '✓ Successfully sent!')}
          </p>
          <p className="text-sm text-gray-500 mb-6">
            {provider.business_name}{t('success_message_received', undefined, ' received your request and will contact you by phone.')}
          </p>
          <button
            onClick={handleNoThanks}
            className="bg-orange-500 hover:bg-orange-600 text-white font-bold py-3 rounded-lg transition-colors text-base px-6"
          >
            {t('new_request_button', undefined, 'New Request')}
          </button>

          {showPWAPrompt && (
            <PWAInstallPrompt
              trigger="lead_submit"
              role="client"
              onClose={() => setShowPWAPrompt(false)}
              lang={lang}
            />
          )}
        </div>
      );
    }

    // If NOT logged in, show two-step nudge flow
    if (successStep === 'sent') {
      return (
        <div className="flex flex-col items-center justify-center py-8 text-center px-4">
          <JsonLd data={serviceJsonLd} />
          <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-green-100 text-3xl text-green-600">
            ✓
          </div>
          <h3 className="text-xl font-bold text-gray-900">
            {t('success_title', undefined, 'Request sent!')}
          </h3>
          <p className="mt-2 mb-4 text-sm text-gray-500">
            {t('success_subtitle', { cityName }, 'Specialists in {cityName} will contact you.')}
          </p>
          <div className="border-t border-gray-200 my-6 w-full"></div>
          <p className="mt-2 text-sm font-medium text-gray-700 mb-3">
            {t('success_track_title', undefined, 'Want to track your request?')}
          </p>
          <ul className="text-xs text-gray-500 space-y-1 mb-6 text-left inline-block">
            <li>• {t('success_bullet_responses', undefined, 'See who responded')}</li>
            <li>• {t('success_bullet_manage', undefined, 'Manage your requests')}</li>
            <li>• {t('success_bullet_notifications', undefined, 'Get notifications')}</li>
          </ul>
          <button
            onClick={handleContinueWithEmail}
            className="w-full rounded-xl bg-orange-500 px-4 py-3 text-base font-bold text-white transition hover:bg-orange-600"
          >
            {t('success_cta_email', undefined, 'Continue with email →')}
          </button>
          <p className="mt-2 text-xs text-gray-400">
            {t('success_free_label', undefined, 'Free · No registration required')}
          </p>
          <button
            onClick={handleNoThanks}
            className="mt-4 text-sm text-gray-500 underline hover:text-gray-700"
          >
            {t('success_skip_link', undefined, 'No thanks')}
          </button>
          {showPWAPrompt && (
            <PWAInstallPrompt
              trigger="lead_submit"
              role="client"
              onClose={() => setShowPWAPrompt(false)}
              lang={lang}
            />
          )}
        </div>
      );
    }

    if (successStep === 'email') {
      const emailValid = isValidEmail(email);
      return (
        <div className="flex flex-col py-8 px-4">
          <button
            onClick={handleBackToSent}
            className="mb-6 text-sm text-gray-500 hover:text-gray-700 flex items-center"
          >
            {t('email_back_link', undefined, '← Back')}
          </button>
          <form onSubmit={handleEmailSubmit} className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                {t('email_label', undefined, 'Your email address')}
              </label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder={t('email_placeholder', undefined, 'your@email.com')}
                autoFocus
                className="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm text-gray-900 placeholder:text-gray-400 focus:border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-200"
              />
            </div>
            <button
              type="submit"
              disabled={!emailValid || isEmailSubmitting}
              className="w-full rounded-xl bg-orange-500 px-4 py-3 text-base font-bold text-white transition hover:bg-orange-600 disabled:cursor-not-allowed disabled:bg-orange-300"
            >
              {t('email_cta_continue', undefined, 'Continue →')}
            </button>
          </form>
          <p className="mt-3 text-center text-xs text-gray-400">
            {t('success_free_label', undefined, 'Free · No registration required')}
          </p>
          <button
            onClick={handleNoThanks}
            className="mt-4 text-center text-sm text-gray-500 underline hover:text-gray-700"
          >
            {t('success_skip_link', undefined, 'No thanks')}
          </button>
        </div>
      );
    }
  }

  return (
    <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
      <JsonLd data={serviceJsonLd} />
      {/* Logo */}
      {isEmbed && (
        <div className="px-4 pt-6 pb-2 text-center">
          <Image
            src="/Nevumo_logo.svg"
            alt="Nevumo"
            width={120}
            height={28}
            className="mx-auto opacity-70 mb-4"
            unoptimized
          />
        </div>
      )}

      {/* Provider Info */}
      <div className="px-6 pt-4 text-center">
        {/* Avatar */}
        <div className="w-[200px] h-[200px] rounded-full bg-orange-100 flex items-center justify-center mx-auto mb-4 overflow-hidden relative">
          {profileImageUrl ? (
            <img
              src={profileImageUrl}
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
              ⭐ {provider.rating.toFixed(1)} {t('rating_label', undefined, 'rating')}
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
            t={t}
            text={recentRequestText}
          />
        ) : null}

        {/* Badge */}
        {(() => {
          if (provider.verification_level === 0) {
            return (
              <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-blue-50 text-blue-400 text-sm font-medium">
                ⚡ {t('badge_new_provider', undefined, 'New in Nevumo')}
              </span>
            );
          }
          if (provider.verification_level === 1) {
            return (
              <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-green-100 text-green-700 text-sm font-medium">
                ✓ {t('badge_verified', undefined, 'Verified')}
              </span>
            );
          }
          if (provider.verification_level === 2) {
            const displayText = (t('badge_top_specialist', undefined, 'Top specialist') + ' – ' + cityName);
            return (
              <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-orange-100 text-orange-700 text-sm font-medium">
                ★ {displayText}
              </span>
            );
          }
          return null;
        })()}
      </div>

      {provider.description && provider.description.trim() !== '' && (
        <p className="text-sm text-gray-600 leading-relaxed px-6 mt-3 mb-1">
          {provider.description}
        </p>
      )}

      {/* Form Header */}
      <div className="px-6 py-4 border-b border-gray-100">
        {isIOS26Plus && (
          <button
            type="submit"
            form="widget-lead-form"
            disabled={loading}
            className="w-full bg-orange-500 hover:bg-orange-600 disabled:bg-orange-300 text-white font-bold py-3 rounded-lg transition-colors text-xl"
          >
            {loading
              ? (translations['sending'] ?? 'Изпращане...')
              : provider.business_name.length <= 22 ? (
                  <span>{`${translations['cta_button'] ?? 'Свържи ме с'} ${provider.business_name}`}</span>
                ) : (
                  <span style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1px', width: '100%' }}>
                    <span style={{ fontSize: '0.8em', opacity: 0.85, fontWeight: 400 }}>{translations['cta_button'] ?? 'Свържи ме с'}</span>
                    <span style={{ whiteSpace: 'normal', wordBreak: 'break-word', textAlign: 'center', width: '100%' }}>
                      {provider.business_name}
                    </span>
                  </span>
                )}
          </button>
        )}
        <p className="text-sm text-gray-400 text-center mt-2">
          {t('disclaimer', undefined, 'Free request • No obligation')}
        </p>
      </div>

      {/* ServiceChips */}
      {filteredServices.length > 0 && (
        <div className="px-6 py-4 mt-4">
          <div className="flex flex-wrap gap-2 mb-2">
            {filteredServices.map((service) => (
              <button
                key={service.id}
                type="button"
                onClick={() => handleServiceClick(service.id)}
                className={`text-xs px-3 py-1.5 border rounded-full cursor-pointer transition-colors ${
                  selectedServiceId === service.id
                    ? 'bg-orange-500 text-white border-orange-500'
                    : 'border-gray-300 text-gray-600 bg-white hover:border-orange-400 hover:text-orange-500 hover:bg-orange-50 active:border-orange-400 active:bg-orange-50'
                }`}
              >
                {service.title} · {formatServicePrice(service, t('price_per_hour', undefined, '/h'), t('price_on_request', undefined, 'Price on request'))}
              </button>
            ))}
          </div>
          {serviceNoteError && (
            <p className="text-xs text-red-600 mt-1">{serviceNoteError}</p>
          )}
          <p className="text-xs text-gray-500">
            {t('or_general_request', undefined, 'Or send a general request ↓')}
          </p>
        </div>
      )}

      {/* Form */}
      <div id="widget-form" className="px-6 py-6">

        <form id="widget-lead-form" onSubmit={handleSubmit} className="space-y-4">
          <div ref={phoneRef}>
            <PhoneInput
              onChange={handleChange}
              countryCode={countryCode ?? cityInfo?.country_code}
              label={t('phone_label', undefined, 'Phone')}
              required
              lang={lang}
              submitted={formSubmitted}
            />
          </div>

          <div>
            <label className="block text-sm font-bold text-gray-700 mb-1">
              {t('notes_label', undefined, 'Notes')}
            </label>
            <textarea
              name="description"
              rows={3}
              value={descriptionValue}
              onChange={handleDescriptionChange}
              placeholder={
                t('notes_placeholder', undefined, 'Describe your request (time, address, details)')
              }
              className="w-full border border-gray-300 rounded-lg px-4 py-3 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent resize-none text-base"
            />
          </div>

          <p className="text-sm text-gray-700 italic text-center">
            {t('response_time', undefined, '⏱ Provider usually responds within 30 minutes')}
          </p>

          {provider.review_count > 0 && provider.latest_review ? (
            <SocialProofBlock review={provider.latest_review} t={t} />
          ) : provider.city_leads > 0 ? (
            <CityDemandBlock text={cityLeadsText} />
          ) : (
            <ChecklistBlock items={checklistItems} />
          )}

          {error && (
            <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
              {t('error_message')}
            </p>
          )}
        </form>

        {/* Sticky button mobile / inline desktop */}
        <StickyBottomBar
          fallback={
            <div className="px-0 py-4">
              <button
                type="submit"
                form="widget-lead-form"
                disabled={loading}
                className="w-full bg-orange-500 hover:bg-orange-600 disabled:bg-orange-300 text-white font-bold py-3 rounded-lg transition-colors text-xl"
              >
                {loading
                  ? (translations['sending'] ?? 'Изпращане...')
                  : provider.business_name.length <= 22 ? (
                      <span>{`${translations['cta_button'] ?? 'Свържи ме с'} ${provider.business_name}`}</span>
                    ) : (
                      <span style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1px', width: '100%' }}>
                        <span style={{ fontSize: '0.8em', opacity: 0.85, fontWeight: 400 }}>{translations['cta_button'] ?? 'Свържи ме с'}</span>
                        <span style={{ whiteSpace: 'normal', wordBreak: 'break-word', textAlign: 'center', width: '100%' }}>
                          {provider.business_name}
                        </span>
                      </span>
                    )}
              </button>
            </div>
          }
        >
          <div ref={stickyDivRef} className="fixed bottom-0 left-0 right-0 z-50 px-6 py-4 bg-white border-t border-gray-100">
            <button
              type="submit"
              form="widget-lead-form"
              disabled={loading}
              className="w-full bg-orange-500 hover:bg-orange-600 disabled:bg-orange-300 text-white font-bold py-3 rounded-lg transition-colors text-xl"
            >
              {loading
                ? (translations['sending'] ?? 'Изпращане...')
                : provider.business_name.length <= 22 ? (
                    <span>{`${translations['cta_button'] ?? 'Свържи ме с'} ${provider.business_name}`}</span>
                  ) : (
                    <span style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1px', width: '100%' }}>
                      <span style={{ fontSize: '0.8em', opacity: 0.85, fontWeight: 400 }}>{translations['cta_button'] ?? 'Свържи ме с'}</span>
                      <span style={{ whiteSpace: 'normal', wordBreak: 'break-word', textAlign: 'center', width: '100%' }}>
                        {provider.business_name}
                      </span>
                    </span>
                  )}
            </button>
          </div>
        </StickyBottomBar>
      </div>

      {/* TrustRow */}
      <div className="grid grid-cols-3 border-t border-gray-100">
        <div className="flex flex-col items-center py-3 px-2 text-center text-xs text-gray-400">
          <span>✓ {translations['trust_verified'] ?? 'Verified'}</span>
        </div>
        <div className="flex flex-col items-center py-3 px-2 text-center text-xs text-gray-400 border-l border-gray-100">
          <span>✓ {translations['trust_free'] ?? 'Free'}</span>
        </div>
        <div className="flex flex-col items-center py-3 px-2 text-center text-xs text-gray-400 border-l border-gray-100">
          <span>✓ {translations['trust_direct'] ?? 'Direct contact'}</span>
        </div>
      </div>

      {/* Privacy Notice */}
      <div className="text-[10px] text-center text-gray-400 py-2.5 px-[18px]">
        <button
          onClick={() => { setLegalModalType('terms'); setLegalModalOpen(true); }}
          className="underline hover:text-gray-600 mr-3 bg-transparent border-none cursor-pointer"
        >
          {t('terms_link', undefined, 'Terms & Conditions')}
        </button>
        <button
          onClick={() => { setLegalModalType('privacy'); setLegalModalOpen(true); }}
          className="underline hover:text-gray-600 bg-transparent border-none cursor-pointer"
        >
          {t('privacy_policy_link', undefined, 'Privacy Policy')}
        </button>
      </div>

      {/* Legal Modal */}
      <LegalModal
        isOpen={legalModalOpen}
        onClose={() => setLegalModalOpen(false)}
        lang={lang}
        type={legalModalType}
        authDict={translations}
        docDict={getDocDict()}
      />

      <PushPermissionPrompt
        lang={lang}
        role={role}
        show={showPushPrompt}
        onDismiss={() => setShowPushPrompt(false)}
      />
    </div>
  );
}
