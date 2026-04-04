'use client';

import { useId, useRef, useState } from 'react';
import { createLead } from '@/lib/api';

type CategorySlug = 'massage' | 'cleaning' | 'plumbing';

interface LeadFormProps {
  categorySlug: CategorySlug;
  citySlug?: string;
}

export default function LeadForm({ categorySlug, citySlug = 'warszawa' }: LeadFormProps) {
  const [phone, setPhone] = useState('');
  const [description, setDescription] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [hasError, setHasError] = useState(false);
  const phoneInputId = useId();
  const descriptionId = useId();
  const phoneInputRef = useRef<HTMLInputElement | null>(null);

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
        <p className="text-lg font-bold text-gray-900">Zapytanie wysłane!</p>
        <p className="mt-2 text-sm text-gray-500">Specjaliści skontaktują się z Tobą wkrótce.</p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor={phoneInputId} className="sr-only">
          Twój numer telefonu
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
          placeholder="Twój numer telefonu"
          className="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm text-gray-900 placeholder:text-gray-400 focus:border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-200"
        />
      </div>

      <div>
        <label htmlFor={descriptionId} className="sr-only">
          Opisz czego potrzebujesz
        </label>
        <textarea
          id={descriptionId}
          name="description"
          rows={3}
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          placeholder="Opisz czego potrzebujesz (opcjonalnie)"
          className="w-full resize-none rounded-xl border border-gray-200 px-4 py-3 text-sm text-gray-900 placeholder:text-gray-400 focus:border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-200"
        />
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full rounded-xl bg-orange-500 px-4 py-3.5 text-base font-semibold text-white transition hover:bg-orange-600 disabled:cursor-not-allowed disabled:bg-orange-300"
      >
        {isSubmitting ? 'Wysyłanie...' : '🔵 Wyślij zapytanie'}
      </button>

      {hasError && (
        <p className="text-sm text-red-600">
          Coś poszło nie tak. Spróbuj ponownie.
        </p>
      )}

      <div className="flex flex-wrap items-center gap-x-3 gap-y-2 text-xs text-gray-500">
        <span>✓ Bezpłatne</span>
        <span>✓ Bez zobowiązań</span>
        <span>✓ Odpowiedź nawet w 30 min</span>
      </div>
    </form>
  );
}
