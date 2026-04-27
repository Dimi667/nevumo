'use client';

import { useState, useEffect, useRef } from 'react';
import { createLead, claimLeadEmail } from '@/lib/api';
import { usePhone } from '@/hooks/usePhone';
import PhoneInput from '@/components/ui/PhoneInput';
import { getPhonePrefix } from '@/lib/phoneUtils';
import PWAInstallPrompt from '@/components/pwa/PWAInstallPrompt';

interface ServiceOption {
  id: string;
  title: string;
}

interface LeadFormProps {
  translations: Record<string, string>;
  categorySlug: string;
  citySlug: string;
  lang: string;
  cityName?: string;
  services?: ServiceOption[];
  countryCode?: string;
  title?: string;
  onReset?: () => void;
}

export default function LeadForm({
  translations,
  categorySlug,
  citySlug,
  lang,
  cityName: cityNameProp,
  services,
  countryCode,
  title,
  onReset,
}: LeadFormProps) {
  const [description, setDescription] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [hasError, setHasError] = useState(false);
  const [phoneValue, setPhoneValue] = useState('');
  const [phoneError, setPhoneError] = useState<string | null>(null);
  const [selectedChip, setSelectedChip] = useState<string | null>(null);
  const [showTextarea, setShowTextarea] = useState(true);
  const [leadId, setLeadId] = useState<string | null>(null);
  const [successStep, setSuccessStep] = useState<'sent' | 'email'>('sent');
  const [email, setEmail] = useState('');
  const [isEmailSubmitting, setIsEmailSubmitting] = useState(false);
  const [showPWAPrompt, setShowPWAPrompt] = useState(false);
  const phoneRef = useRef<HTMLDivElement>(null);
  const { phone: savedPhone, savePhone, loading } = usePhone();
  const phonePrefix = getPhonePrefix(countryCode);
  const phoneDigitsCount = phoneValue.replace(/\D/g, '').length;
  const isPhoneValid = phoneDigitsCount >= 7;
  const isPrefixOnlyPhone = phoneValue.trim() === phonePrefix.trim();
  
  useEffect(() => {
    if (
      savedPhone &&
      !phoneValue &&
      savedPhone.trim().startsWith(phonePrefix.trim())
    ) {
      setPhoneValue(savedPhone);
    }
  }, [phonePrefix, phoneValue, savedPhone]);
  
  const resolvedTitle = title ?? translations['form_btn'] ?? 'Get offers';
  
  const handleChange = (value: string) => {
    setPhoneValue(value);

    if (phoneError) {
      setPhoneError(null);
    }
  };

  const handleChipClick = (chipTitle: string) => {
    setSelectedChip(chipTitle);
    setShowTextarea(true);
    const notSureText = translations['chip_not_sure'] || 'Not sure';
    if (chipTitle !== notSureText) {
      setDescription(chipTitle);
    } else {
      setDescription('');
    }
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (isPrefixOnlyPhone || !isPhoneValid) {
      setPhoneError(translations['error_phone_invalid'] || 'Enter a valid phone number');
      setHasError(false);
      
      // Scroll to phone field so user sees the error
      phoneRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' });
      return;
    }

    setIsSubmitting(true);
    setHasError(false);
    setPhoneError(null);

    try {
      const finalDescription = description.trim() || selectedChip || '';
      const result = await createLead({
        category_slug: categorySlug,
        city_slug: citySlug,
        phone: phoneValue.trim(),
        description: finalDescription || undefined,
        source: 'seo',
      });

      if (!result) {
        setHasError(true);
        return;
      }

      // Check for API error response
      if ('success' in result && !result.success) {
        if (result.error?.code === 'RATE_LIMIT_EXCEEDED') {
          if (result.lead_id) setLeadId(result.lead_id);
          setIsSuccess(true);
          setSuccessStep('sent');
        } else {
          console.error('Lead submission error:', result.error?.code, result.error?.message);
          setHasError(true);
        }
        return;
      }

      if ('lead_id' in result) {
        setLeadId(result.lead_id);
        setIsSuccess(true);
        setSuccessStep('sent');
        setDescription('');
        setSelectedChip(null);
        setShowTextarea(true);
        // Don't clear phoneValue yet - we need it for the pending_claim
        // Save phone on successful submit
        if (phoneValue.replace(/\D/g, '').length >= 7) {
          savePhone(phoneValue.trim());
        }
      }
      // Show PWA prompt after 2 seconds
      setTimeout(() => {
        setShowPWAPrompt(true);
      }, 2000);
    } catch (error) {
      console.error('Lead submission failed:', error);
      setHasError(true);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Get city display name - fallback to slug if not provided
  const cityName = cityNameProp || citySlug.charAt(0).toUpperCase() + citySlug.slice(1);

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

    // Get lang from URL
    const currentLang = window.location.pathname.split('/')[1] || 'en';

    // Redirect to auth with email in query string
    const redirectUrl = `/${currentLang}/auth?email=${encodeURIComponent(email)}&intent=client`;
    window.location.href = redirectUrl;
  };

  const handleNoThanks = () => {
    // Reset form to initial state
    setIsSuccess(false);
    setSuccessStep('sent');
    setLeadId(null);
    setEmail('');
    setPhoneValue('');
    setIsEmailSubmitting(false);
    setHasError(false);
    setDescription('');
    setSelectedChip(null);
    setShowTextarea(true);
    setPhoneError(null);
    if (onReset) onReset();
  };

  if (isSuccess && successStep === 'sent') {
    return (
      <div className="flex flex-col items-center justify-center py-8 text-center px-4">
        {/* Large green checkmark */}
        <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-green-100 text-3xl text-green-600">
          ✓
        </div>

        {/* Heading */}
        <h3 className="text-xl font-bold text-gray-900">
          {translations['success_title'] || 'Request sent!'}
        </h3>

        {/* Subtext */}
        <p className="mt-2 mb-4 text-sm text-gray-500">
          {(translations['success_subtitle'] || 'Specialists in {cityName} will contact you.').replace('{cityName}', cityName)}
        </p>

        {/* Separator */}
        <div className="border-t border-gray-200 my-6 w-full"></div>

        {/* Track your request section */}
        <p className="mt-2 text-sm font-medium text-gray-700 mb-3">
          {translations['success_track_title'] || 'Want to track your request?'}
        </p>

        {/* Bullet points */}
        <ul className="text-xs text-gray-500 space-y-1 mb-6 text-left inline-block">
          <li>• {translations['success_bullet_responses'] || 'See who responded'}</li>
          <li>• {translations['success_bullet_manage'] || 'Manage your requests'}</li>
          <li>• {translations['success_bullet_notifications'] || 'Get notifications'}</li>
        </ul>

        {/* Primary CTA */}
        <button
          onClick={handleContinueWithEmail}
          className="w-full rounded-xl bg-orange-500 px-4 py-3 text-base font-bold text-white transition hover:bg-orange-600"
        >
          {translations['success_cta_email'] || 'Continue with email →'}
        </button>

        {/* Free text */}
        <p className="mt-2 text-xs text-gray-400">
          {translations['success_free_label'] || 'Free · No registration required'}
        </p>

        {/* Skip link */}
        <button
          onClick={handleNoThanks}
          className="mt-4 text-sm text-gray-500 underline hover:text-gray-700"
        >
          {translations['success_skip_link'] || 'No thanks'}
        </button>

        {/* PWA Install Prompt */}
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

  if (isSuccess && successStep === 'email') {
    const emailValid = isValidEmail(email);

    return (
      <div className="flex flex-col py-8 px-4">
        {/* Back link */}
        <button
          onClick={handleBackToSent}
          className="mb-6 text-sm text-gray-500 hover:text-gray-700 flex items-center"
        >
          {translations['email_back_link'] || '← Back'}
        </button>

        {/* Email form */}
        <form onSubmit={handleEmailSubmit} className="space-y-4">
          <div>
            <label
              htmlFor="email"
              className="block text-sm font-medium text-gray-700 mb-2"
            >
              {translations['email_label'] || 'Your email address'}
            </label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder={translations['email_placeholder'] || 'your@email.com'}
              autoFocus
              className="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm text-gray-900 placeholder:text-gray-400 focus:border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-200"
            />
          </div>

          <button
            type="submit"
            disabled={!emailValid || isEmailSubmitting}
            className="w-full rounded-xl bg-orange-500 px-4 py-3 text-base font-bold text-white transition hover:bg-orange-600 disabled:cursor-not-allowed disabled:bg-orange-300"
          >
            {isEmailSubmitting ? (translations['email_cta_continue'] || 'Continue →') : (translations['email_cta_continue'] || 'Continue →')}
          </button>
        </form>

        {/* Free text */}
        <p className="mt-3 text-center text-xs text-gray-400">
          {translations['success_free_label'] || 'Free · No registration required'}
        </p>

        {/* Skip link */}
        <button
          onClick={handleNoThanks}
          className="mt-4 text-center text-sm text-gray-500 underline hover:text-gray-700"
        >
          {translations['success_skip_link'] || 'No thanks'}
        </button>
      </div>
    );
  }

  const notSureText = translations['chip_not_sure'] || 'Not sure';
  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Header Section */}
      <div>
        <h2 className="text-xl font-bold text-gray-900">{resolvedTitle}</h2>
        <p className="mt-1 text-sm text-gray-500">{translations['form_subtext']}</p>
      </div>

      {/* How It Works */}
      <div>
        <p className="text-sm font-medium text-gray-700 mb-2">{translations['how_it_works_label']}</p>
        <div className="flex flex-col sm:flex-row gap-2 sm:gap-4 text-xs text-gray-500">
          <span>1️⃣ {translations['how_step_1']}</span>
          <span>2️⃣ {translations['how_step_2']}</span>
          <span>3️⃣ {translations['how_step_3']}</span>
        </div>
      </div>

      {/* What Do You Need - Chips */}
      <div>
        <p className="text-sm font-medium text-gray-700 mb-3">{translations['what_need_label']}</p>
        <div className="flex flex-wrap gap-2">
          {services?.map((service) => (
            <button
              key={service.id}
              type="button"
              onClick={() => handleChipClick(service.title)}
              className={`px-3 py-2 rounded-full text-sm transition-colors ${
                selectedChip === service.title
                  ? 'bg-orange-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {service.title}
            </button>
          ))}
        </div>
      </div>

      {/* Description Textarea - Conditional */}
      {showTextarea && (
        <div>
          <label htmlFor="description" className="sr-only">
            {translations['details_label']}
          </label>
          <textarea
            id="description"
            name="description"
            rows={3}
            value={description}
            onChange={(event) => setDescription(event.target.value)}
            placeholder={translations['details_placeholder']}
            className="w-full resize-none rounded-xl border border-gray-200 px-4 py-3 text-sm text-gray-900 placeholder:text-gray-400 focus:border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-200"
          />
        </div>
      )}

      {/* Phone Field */}
      <div ref={phoneRef}>
        <PhoneInput
          value={phoneValue}
          onChange={handleChange}
          countryCode={countryCode}
          error={phoneError}
          label={translations['form_phone'] || 'Phone'}
          required
        />
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full rounded-xl bg-orange-500 px-4 py-3 text-base font-bold text-white transition hover:bg-orange-600 disabled:cursor-not-allowed disabled:bg-orange-300"
      >
        {isSubmitting ? 'Sending...' : translations['get_offers_btn']}
      </button>

      {/* Error Message */}
      {hasError && (
        <p className="text-sm text-red-600">
          {translations['error_generic'] || 'Something went wrong. Please try again.'}
        </p>
      )}

      {/* Trust Signals */}
      <div className="mt-3 space-y-1 text-center">
        <p className="text-sm text-gray-500">
          ✓ {translations['form_trust_1'] ?? 'Free'} •
          ✓ {translations['form_trust_2'] ?? 'No obligation'}
        </p>
        <p className="text-sm text-gray-500">
          ✓ {translations['trust_multiple'] ?? 'Your request will be sent to multiple providers'}
        </p>
        <p className="text-sm text-gray-500">
          ✓ {translations['trust_response'] ?? 'Response within 30 min'}
        </p>
      </div>
    </form>
  );
}
