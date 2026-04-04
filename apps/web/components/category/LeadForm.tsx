'use client';

import { useId, useRef, useState } from 'react';
import { createLead } from '@/lib/api';

type CategorySlug = 'massage' | 'cleaning' | 'plumbing';

interface LeadFormProps {
  categorySlug: CategorySlug;
  citySlug: string;
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
  title,
  subtitle,
  phonePlaceholder,
  descPlaceholder,
  buttonText,
  trustItems,
}: LeadFormProps) {
  const [phone, setPhone] = useState('');
  const [description, setDescription] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [hasError, setHasError] = useState(false);
  const phoneInputId = useId();
  const descriptionId = useId();
  const phoneInputRef = useRef<HTMLInputElement | null>(null);
  const resolvedTitle = title ?? 'Send a request';
  const resolvedSubtitle = subtitle ?? 'Free • No obligation';
  const resolvedPhonePlaceholder = phonePlaceholder ?? 'Your phone number';
  const resolvedDescPlaceholder = descPlaceholder ?? 'Describe what you need (optional)';
  const resolvedButtonText = buttonText ?? 'Send request';
  const resolvedTrustItems = trustItems ?? ['Free', 'No obligation', 'Reply within 30 min'];

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!phone.trim()) {
      phoneInputRef.current?.focus();
      return;
    }

    setIsSubmitting(true);
    setHasError(false);

    try {
      const result = await createLead({
        category_slug: categorySlug,
        city_slug: citySlug,
        phone: phone.trim(),
        description: description.trim() || undefined,
        source: 'seo',
      });

      if (!result) {
        setHasError(true);
        return;
      }

      setIsSuccess(true);
      setPhone('');
      setDescription('');
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

      <div>
        <label htmlFor={phoneInputId} className="sr-only">
          {resolvedPhonePlaceholder}
        </label>
        <input
          id={phoneInputId}
          ref={phoneInputRef}
          name="phone"
          type="tel"
          autoFocus={typeof window !== 'undefined' && window.location.hash === '#lead-form-phone'}
          required
          value={phone}
          onChange={(event) => setPhone(event.target.value)}
          placeholder={resolvedPhonePlaceholder}
          className="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm text-gray-900 placeholder:text-gray-400 focus:border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-200"
        />
      </div>

      <div>
        <label htmlFor={descriptionId} className="sr-only">
          {resolvedDescPlaceholder}
        </label>
        <textarea
          id={descriptionId}
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
