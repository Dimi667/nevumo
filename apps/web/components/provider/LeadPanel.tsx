'use client';

import { useState, useRef, useEffect } from 'react';
import { createLead, claimLeadEmail } from '@/lib/api';
import { checkEmail } from '@/lib/auth-api';
import PWAInstallPrompt from '@/components/pwa/PWAInstallPrompt';
import PhoneInput from '@/components/ui/PhoneInput';
import { usePhone } from '@/hooks/usePhone';
import { usePhoneValidation } from '@/hooks/usePhoneValidation';

interface LeadPanelProps {
  providerName: string;
  providerSlug: string;
  categorySlug: string;
  citySlug: string;
  services: Array<{ id: string; title: string; base_price: number | null; price_type: string; currency: string }>;
  verificationLevel: number;
  reviewCount: number;
  jobsCompleted: number;
  cityLeads?: number;
  cityName?: string;
  categoryName?: string;
  latestReview?: { rating: number; comment: string | null; client_name: string } | null;
  latestLeadClientName?: string | null;
  latestLeadCity?: string | null;
  leadsReceived?: number;
  translations: Record<string, string>;
  lang: string;
  selectedService?: string | null;
  onServiceSelect?: (serviceId: string) => void;
  onServiceDeselect?: () => void;
  onServicePreFill?: (serviceId: string) => string | undefined;
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

export default function LeadPanel({
  providerName,
  providerSlug,
  categorySlug,
  citySlug,
  services,
  verificationLevel,
  reviewCount,
  jobsCompleted,
  cityLeads,
  cityName,
  categoryName,
  latestReview,
  latestLeadClientName,
  latestLeadCity,
  leadsReceived,
  translations,
  lang,
  selectedService: externalSelectedService,
  onServiceSelect: externalOnServiceSelect,
  onServiceDeselect: externalOnServiceDeselect,
  onServicePreFill,
}: LeadPanelProps) {
  const t = translations;
  const [internalSelectedService, setInternalSelectedService] = useState<string | null>(null);
  const selectedService = externalSelectedService !== undefined ? externalSelectedService : internalSelectedService;
  const setSelectedService = externalOnServiceSelect ? externalOnServiceSelect : setInternalSelectedService;
  const [phoneValue, setPhoneValue] = useState('');
  const [notes, setNotes] = useState('');
  const { isValid } = usePhoneValidation(phoneValue, citySlug === 'warszawa' ? 'PL' : 'BG');

  // Handle pre-fill from service selection (chip click or external select)
  useEffect(() => {
    if (selectedService !== null) {
      const service = services.find(s => s.id === selectedService);
      if (service) {
        const serviceText = onServicePreFill ? (onServicePreFill(selectedService) ?? '') : `${service.title} - ${formatServicePrice(service, t['price_per_hour'] ?? '/ч', t['price_on_request'] ?? 'По запитване')}`;
        setNotes(serviceText);
      }
    } else {
      // Clear notes on deselect
      setNotes('');
    }
  }, [selectedService, services, onServicePreFill, t]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [serviceNoteError, setServiceNoteError] = useState<string | null>(null);
  const [step, setStep] = useState<'form' | 'success1' | 'success2'>('form');
  const [leadId, setLeadId] = useState<string | null>(null);
  const [email, setEmail] = useState('');
  const [emailError, setEmailError] = useState<string | null>(null);
  const [isEmailSubmitting, setIsEmailSubmitting] = useState(false);
  const [showPWAPrompt, setShowPWAPrompt] = useState(false);
  const phoneRef = useRef<HTMLInputElement>(null);
  const formRef = useRef<HTMLDivElement>(null);
  const [formSubmitted, setFormSubmitted] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // Check if user is logged in
  useEffect(() => {
    const token = localStorage.getItem('nevumo_auth_token');
    setIsLoggedIn(!!token);
  }, []);

  useEffect(() => {
    if (step === 'success1' && formRef.current) {
      formRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }, [step]);

  // Social proof signal cascade logic
  const getSocialProofSignal = () => {
    // 1. reviewCount > 0 && latestReview
    if (reviewCount > 0 && latestReview) {
      const shortComment = latestReview.comment && latestReview.comment.trim()
        ? latestReview.comment.slice(0, 80) + (latestReview.comment.length > 80 ? '...' : '')
        : null;
      const initials = latestReview.client_name.split(' ').map(n => n[0]).join('.');
      return (
        <div className="flex items-start gap-2">
          <span className="text-yellow-400">★★★★★</span>
          <div className="flex-1">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded-full bg-orange-100 flex items-center justify-center shrink-0">
                <span className="text-orange-600 text-xs font-bold">
                  {initials.charAt(0).toUpperCase()}
                </span>
              </div>
              {shortComment && <p className="text-gray-700 text-sm">"{shortComment}"</p>}
            </div>
          </div>
        </div>
      );
    }
    // 2. reviewCount === 0 && jobsCompleted > 0
    if (reviewCount === 0 && jobsCompleted > 0) {
      return <p>✓ {jobsCompleted} {t['completed_jobs']}</p>;
    }
    // 3. reviewCount === 0 && jobsCompleted === 0 && cityLeads > 0
    if (reviewCount === 0 && jobsCompleted === 0 && cityLeads && cityLeads > 0) {
      return <p>{cityLeads} заявки за {categoryName} в {cityName} тази година</p>;
    }
    // 4. leadsReceived > 0 && latestLeadClientName
    if (leadsReceived && leadsReceived > 0 && latestLeadClientName) {
      return <p>{latestLeadClientName} от {latestLeadCity} поръча наскоро</p>;
    }
    // 5. Fallback
    return <p>✓ Безплатна заявка • Без ангажимент • Директен контакт</p>;
  };


  const isValidEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormSubmitted(true);
    setSubmitError(null);
    setServiceNoteError(null);

    // Validation using isValid from usePhone hook
    if (!phoneValue || !isValid) {
      setSubmitError(t['error_phone_invalid'] ?? 'Invalid phone number');
      phoneRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' });
      return;
    }

    // Validate service or note
    if (selectedService === null && notes.trim().length === 0) {
      setServiceNoteError(t['error_service_or_note'] ?? 'Моля изберете услуга или напишете бележка');
      return;
    }

    setIsSubmitting(true);

    try {
      const result = await createLead({
        provider_slug: providerSlug,
        category_slug: categorySlug,
        city_slug: citySlug,
        phone: phoneValue.trim(),
        description: notes || undefined,
        source: 'panel',
      });

      if (result && 'lead_id' in result) {
        setLeadId(result.lead_id);
        setStep('success1');
        setTimeout(() => { setShowPWAPrompt(true); }, 2000);
      } else if (result && 'success' in result && !result.success && result.error.code === 'RATE_LIMIT_EXCEEDED') {
        // Rate limited but still show success
        const leadIdFromError = (result as any).lead_id;
        if (leadIdFromError) {
          setLeadId(leadIdFromError);
        }
        setStep('success1');
        setTimeout(() => { setShowPWAPrompt(true); }, 2000);
      } else {
        setSubmitError(t['error_generic'] ?? 'An error occurred. Please try again.');
      }
    } catch (err) {
      setSubmitError(t['error_generic'] ?? 'An error occurred. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleEmailSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!isValidEmail(email)) {
      setEmailError(t['error_email_invalid'] ?? 'Invalid email address');
      return;
    }

    if (!leadId) return;

    setIsEmailSubmitting(true);
    setEmailError(null);

    try {
      // Check if email already exists
      const { exists } = await checkEmail(email);

      await claimLeadEmail(leadId, email, phoneValue);

      // Save to localStorage
      const pendingClaim = {
        lead_id: leadId,
        email: email,
        phone: phoneValue,
        submitted_at: new Date().toISOString(),
      };
      localStorage.setItem('nevumo_pending_claim', JSON.stringify(pendingClaim));

      // Redirect to auth with mode based on whether user exists
      const mode = exists ? 'login' : 'register';
      window.location.href = `/${lang}/auth?email=${encodeURIComponent(email)}&intent=client&mode=${mode}`;
    } catch (err) {
      setEmailError(t['error_generic'] ?? 'An error occurred. Please try again.');
    } finally {
      setIsEmailSubmitting(false);
    }
  };

  const handleNoThanks = () => {
    setStep('form');
    setPhoneValue('');
    setNotes('');
    setLeadId(null);
    setEmail('');
    setSubmitError(null);
    setEmailError(null);
    setServiceNoteError(null);
    setFormSubmitted(false);
  };

  // Success Screen Step 1
  if (step === 'success1') {
    // If logged in, show simple success message
    if (isLoggedIn) {
      return (
        <div className="rounded-xl border border-gray-100 bg-white shadow-sm overflow-hidden max-h-[calc(100vh-48px)] overflow-y-auto">
          <div className="px-5 py-8 flex flex-col items-center justify-center text-center">
            <div className="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center mb-4">
              <span className="text-green-600 text-3xl">✓</span>
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2">
              {t['success_title'] ?? 'Заявката е изпратена!'}
            </h3>
            <p className="text-sm text-gray-500 mb-6">
              {t['success_subtitle'] ?? 'Специалистите ще се свържат с вас.'}
            </p>
            <button
              onClick={handleNoThanks}
              className="bg-orange-500 hover:bg-orange-600 text-white font-bold py-3 rounded-lg transition-colors text-base px-6"
            >
              {t['new_request_button'] ?? 'Нова заявка'}
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
        </div>
      );
    }

    // If not logged in, show email collection screen
    return (
      <div className="rounded-xl border border-gray-100 bg-white shadow-sm overflow-hidden max-h-[calc(100vh-48px)] overflow-y-auto">
        <div className="px-5 py-8 flex flex-col items-center justify-center text-center">
          <div className="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center mb-4">
            <span className="text-green-600 text-3xl">✓</span>
          </div>
          <h3 className="text-lg font-bold text-gray-900 mb-2">
            {t['success_title'] ?? 'Заявката е изпратена!'}
          </h3>
          <p className="text-sm text-gray-500 mb-6">
            {t['success_subtitle'] ?? 'Специалистите ще се свържат с вас.'}
          </p>
          <div className="border-t border-gray-200 my-4 w-full"></div>
          <p className="text-sm font-medium text-gray-700 mb-3">
            {t['success_track_title'] ?? 'Искате ли да следите заявката си?'}
          </p>
          <ul className="text-xs text-gray-500 space-y-1 mb-6 text-left inline-block">
            <li>• {t['success_bullet_responses'] ?? 'Вижте кой е отговорил'}</li>
            <li>• {t['success_bullet_manage'] ?? 'Управлявайте заявките си'}</li>
            <li>• {t['success_bullet_notifications'] ?? 'Получавайте известия'}</li>
          </ul>
          <button
            onClick={() => setStep('success2')}
            className="w-full rounded-xl bg-orange-500 px-4 py-3 text-base font-bold text-white transition hover:bg-orange-600"
          >
            {t['success_cta_email'] ?? 'Продължи с имейл →'}
          </button>
          <p className="mt-2 text-xs text-gray-400">
            {t['success_free_label'] ?? 'Безплатно • Без регистрация'}
          </p>
          <button
            onClick={handleNoThanks}
            className="mt-4 text-sm text-gray-500 underline hover:text-gray-700"
          >
            {t['success_skip_link'] ?? 'Не, благодаря'}
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
      </div>
    );
  }

  // Success Screen Step 2 - Email Form
  if (step === 'success2') {
    return (
      <div className="rounded-xl border border-gray-100 bg-white shadow-sm overflow-hidden max-h-[calc(100vh-48px)] overflow-y-auto">
        <div className="px-5 py-6">
          <button
            onClick={() => setStep('success1')}
            className="mb-4 text-sm text-gray-500 hover:text-gray-700 flex items-center"
          >
            {t['email_back_link'] ?? '← Назад'}
          </button>
          <form onSubmit={handleEmailSubmit} className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                {t['email_label'] ?? 'Вашият имейл адрес'}
              </label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => {
                  setEmail(e.target.value);
                  if (emailError) setEmailError(null);
                }}
                placeholder={t['email_placeholder'] ?? 'your@email.com'}
                autoFocus
                className="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm text-gray-900 placeholder:text-gray-400 focus:border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-200"
              />
              {emailError && (
                <p className="text-xs text-red-600 mt-1">{emailError}</p>
              )}
            </div>
            <button
              type="submit"
              disabled={isEmailSubmitting}
              className="w-full rounded-xl bg-orange-500 px-4 py-3 text-base font-bold text-white transition hover:bg-orange-600 disabled:cursor-not-allowed disabled:bg-orange-300"
            >
              {isEmailSubmitting ? (t['sending'] ?? 'Изпращане...') : (t['email_cta_continue'] ?? 'Продължи →')}
            </button>
          </form>
          <p className="mt-3 text-center text-xs text-gray-400">
            {t['success_free_label'] ?? 'Безплатно • Без регистрация'}
          </p>
          <button
            onClick={handleNoThanks}
            className="mt-4 text-center text-sm text-gray-500 underline hover:text-gray-700"
          >
            {t['success_skip_link'] ?? 'Не, благодаря'}
          </button>
        </div>
      </div>
    );
  }

  // Form Step
  return (
    <div ref={formRef} className="rounded-xl border border-gray-100 bg-white shadow-sm overflow-hidden max-h-[calc(100vh-48px)] overflow-y-auto">
      {/* 1. Header */}
      <div className="px-5 py-4 border-b border-gray-100">
        <h2 className="text-sm font-semibold text-gray-900">
          {t['request_panel_title'] ?? 'Изпратете заявка на'} {providerName}
        </h2>
        <p className="text-xs text-gray-400 mt-0.5">
          ✓ {t['request_panel_free'] ?? 'Безплатно'} • {t['request_panel_no_commitment'] ?? 'Без ангажимент'}
        </p>
      </div>

      {/* 2. Panel Body */}
      <form onSubmit={handleSubmit} className="px-5 py-4 flex flex-col gap-3">
        {/* ServiceChips */}
        {(services ?? []).length > 0 && (
          <div>
            <div className="flex flex-wrap gap-2 mb-2">
              {(services ?? []).map((service) => (
                <button
                  key={service.id}
                  type="button"
                  onClick={() => {
                    setSelectedService(service.id);
                  }}
                  className={`text-xs px-3 py-1.5 border rounded-full cursor-pointer transition-colors ${
                    selectedService === service.id
                      ? 'bg-orange-500 text-white border-orange-500'
                      : 'border-gray-300 text-gray-600 bg-white hover:border-orange-400 hover:text-orange-500 hover:bg-orange-50 active:border-orange-400 active:bg-orange-50'
                  }`}
                >
                  {service.title}  {formatServicePrice(service, t['price_per_hour'] ?? '/ч', t['price_on_request'] ?? 'По запитване')}
                </button>
              ))}
            </div>
            {serviceNoteError && (
              <p className="text-xs text-red-600 mt-1">{serviceNoteError}</p>
            )}
            <p className="text-xs text-gray-500">
              {t['or_general_request'] ?? 'Or send a general request ↓'}
            </p>
          </div>
        )}

        {/* PhoneField */}
        <div ref={phoneRef}>
          <PhoneInput
            onChange={setPhoneValue}
            countryCode={citySlug === 'warszawa' ? 'PL' : 'BG'}
            required
            label={t['phone_placeholder'] ?? 'Вашият телефон'}
            lang={lang}
            submitted={formSubmitted}
          />
        </div>

        {/* NotesField */}
        <textarea
          rows={3}
          value={notes}
          onChange={(e) => {
            setNotes(e.target.value);
            if (serviceNoteError) setServiceNoteError(null);
          }}
          placeholder={t['notes_placeholder'] ?? 'Опишете накратко какво ви трябва...'}
          className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm bg-white text-gray-900 outline-none focus:border-orange-400 focus:ring-2 focus:ring-orange-400/20 resize-none"
        />

        {/* SocialProofSignal */}
        <div className="bg-gray-50 rounded-xl p-3 text-xs text-gray-600">
          {getSocialProofSignal()}
        </div>

        {/* Error Message */}
        {submitError && (
          <p className="text-xs text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
            {submitError}
          </p>
        )}

        {/* CTAButton */}
        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full py-3.5 bg-orange-500 hover:bg-orange-600 disabled:bg-orange-300 text-white text-base font-semibold rounded-xl transition-colors truncate"
        >
          {isSubmitting ? (t['sending'] ?? 'Изпращане...') : `${t['cta_button']} ${providerName}`}
        </button>
      </form>

      {/* TrustRow */}
      <div className="grid grid-cols-3 border-t border-gray-100">
        <div className="flex flex-col items-center py-3 px-2 text-center text-xs text-gray-400">
          <span>✓ {t['trust_verified'] ?? 'Верифициран'}</span>
        </div>
        <div className="flex flex-col items-center py-3 px-2 text-center text-xs text-gray-400 border-l border-gray-100">
          <span>✓ {t['trust_free'] ?? 'Без такса'}</span>
        </div>
        <div className="flex flex-col items-center py-3 px-2 text-center text-xs text-gray-400 border-l border-gray-100">
          <span>✓ {t['trust_direct'] ?? 'Директен контакт'}</span>
        </div>
      </div>
    </div>
  );
}
