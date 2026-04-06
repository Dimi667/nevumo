'use client';

import { useState, useEffect } from 'react';
import { createLead } from '@/lib/api';
import { usePhone } from '@/hooks/usePhone';
import PhoneInput from '@/components/ui/PhoneInput';
import { getPhonePrefix } from '@/lib/phoneUtils';

interface ServiceOption {
  id: string;
  title: string;
}

interface LeadFormProps {
  translations: Record<string, string>;
  categorySlug: string;
  citySlug: string;
  lang: string;
  services?: ServiceOption[];
  countryCode?: string;
  title?: string;
}

export default function LeadForm({
  translations,
  categorySlug,
  citySlug,
  lang,
  services,
  countryCode,
  title,
}: LeadFormProps) {
  const [description, setDescription] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [hasError, setHasError] = useState(false);
  const [phoneValue, setPhoneValue] = useState('');
  const [phoneError, setPhoneError] = useState<string | null>(null);
  const [selectedChip, setSelectedChip] = useState<string | null>(null);
  const [showTextarea, setShowTextarea] = useState(false);
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
      setPhoneError('Enter a valid phone number');
      setHasError(false);
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

      setIsSuccess(true);
      setDescription('');
      setSelectedChip(null);
      setShowTextarea(false);
      setPhoneValue('');
      // Save phone on successful submit
      if (phoneValue.replace(/\D/g, '').length >= 7) {
        savePhone(phoneValue.trim());
      }
    } catch {
      setHasError(true);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isSuccess) {
    return (
      <div className="flex flex-col items-center justify-center py-8 text-center">
        <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-green-100 text-2xl text-green-600">
          ✓
        </div>
        <p className="text-lg font-bold text-gray-900">Request sent!</p>
        <p className="mt-2 text-sm text-gray-500">Specialists will contact you soon.</p>
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
          <button
            type="button"
            onClick={() => handleChipClick(notSureText)}
            className={`px-3 py-2 rounded-full text-sm transition-colors border ${
              selectedChip === notSureText
                ? 'bg-orange-500 text-white border-orange-500'
                : 'bg-white text-gray-700 border-solid border-gray-300 hover:border-gray-400'
            }`}
          >
            {notSureText}
          </button>
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
      <PhoneInput
        value={phoneValue}
        onChange={handleChange}
        countryCode={countryCode}
        error={phoneError}
        required
      />

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
          Something went wrong. Please try again.
        </p>
      )}

      {/* Trust Signals */}
      <div className="mt-3 space-y-1 text-center">
        <p className="text-sm text-gray-500">
          {translations['form_free'] ?? '✓ Free'}{' '}
          {translations['form_no_obligation'] ?? '✓ No obligation'}
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
