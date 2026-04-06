'use client';

import { useState, useEffect } from 'react';
import { createLead } from '@/lib/api';
import { usePhone } from '@/hooks/usePhone';
import PhoneInput from '@/components/ui/PhoneInput';
import { getPhonePrefix } from '@/lib/phoneUtils';

type CategorySlug = 'massage' | 'cleaning' | 'plumbing';

interface LeadFormProps {
  categorySlug: CategorySlug;
  citySlug: string;
  countryCode?: string;
  title?: string;
  subtitle?: string;
  phonePlaceholder?: string;
  descPlaceholder?: string;
  buttonText?: string;
  trustItems?: string[];
}

export default function LeadForm({
  categorySlug,
  citySlug,
  countryCode,
  title,
  subtitle,
  phonePlaceholder,
  descPlaceholder,
  buttonText,
  trustItems,
}: LeadFormProps) {
  const [description, setDescription] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [hasError, setHasError] = useState(false);
  const [phoneValue, setPhoneValue] = useState('');
  const [phoneError, setPhoneError] = useState<string | null>(null);
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
  
  const resolvedTitle = title ?? 'Send a request';
  const resolvedSubtitle = subtitle ?? 'Free • No obligation';
  const resolvedDescPlaceholder = descPlaceholder ?? 'Describe what you need (optional)';
  const resolvedButtonText = buttonText ?? 'Send request';
  const handleChange = (value: string) => {
    setPhoneValue(value);

    if (phoneError) {
      setPhoneError(null);
    }
  };
  
  const resolvedTrustItems = trustItems ?? ['Free', 'No obligation', 'Reply within 30 min'];

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
      const result = await createLead({
        category_slug: categorySlug,
        city_slug: citySlug,
        phone: phoneValue.trim(),
        description: description.trim() || undefined,
        source: 'seo',
      });

      if (!result) {
        setHasError(true);
        return;
      }

      setIsSuccess(true);
      setDescription('');
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

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <h2 className="text-xl font-bold text-gray-900">{resolvedTitle}</h2>
        <p className="mt-1 text-sm text-gray-500">{resolvedSubtitle}</p>
      </div>

      <PhoneInput
        value={phoneValue}
        onChange={handleChange}
        countryCode={countryCode}
        error={phoneError}
        placeholder={phonePlaceholder}
        required
      />

      <div>
        <label htmlFor="description" className="sr-only">
          {resolvedDescPlaceholder}
        </label>
        <textarea
          id="description"
          name="description"
          rows={3}
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          placeholder={resolvedDescPlaceholder}
          className="w-full resize-none rounded-xl border border-gray-200 px-4 py-3 text-sm text-gray-900 placeholder:text-gray-400 focus:border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-200"
        />
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full rounded-xl bg-orange-500 px-4 py-3.5 text-base font-semibold text-white transition hover:bg-orange-600 disabled:cursor-not-allowed disabled:bg-orange-300"
      >
        {isSubmitting ? 'Sending...' : resolvedButtonText}
      </button>

      {hasError && (
        <p className="text-sm text-red-600">
          Something went wrong. Please try again.
        </p>
      )}

      <div className="flex flex-wrap items-center gap-x-3 gap-y-2 text-xs text-gray-500">
        {resolvedTrustItems.map((item) => (
          <span key={item}>✓ {item}</span>
        ))}
      </div>
    </form>
  );
}
