'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';

interface ObjectionConfirmButtonProps {
  token: string;
  lang: string;
  children: React.ReactNode;
}

export default function ObjectionConfirmButton({ token, lang, children }: ObjectionConfirmButtonProps) {
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://api.nevumo.com';
      const response = await fetch(`${apiUrl}/api/v1/outreach/objection?token=${encodeURIComponent(token)}`, {
        method: 'POST',
      });

      if (response.ok) {
        // Success - redirect to success status
        router.push(`/${lang}/outreach/objection?status=success`);
      } else if (response.status === 409) {
        // Already processed - redirect to already_done status
        router.push(`/${lang}/outreach/objection?status=already_done`);
      } else if (response.status === 404) {
        // Invalid token - redirect to invalid status
        router.push(`/${lang}/outreach/objection?status=invalid`);
      } else {
        // Other error
        setError('Something went wrong. Please try again.');
      }
    } catch (err) {
      setError('Network error. Please check your connection and try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <button
        type="submit"
        disabled={isSubmitting}
        className="inline-block bg-orange-500 hover:bg-orange-600 disabled:bg-orange-300 text-white font-semibold px-6 py-3 rounded-xl transition-colors duration-150 w-full"
      >
        {isSubmitting ? 'Processing...' : children}
      </button>
      {error && (
        <p className="text-red-600 text-sm mt-2">{error}</p>
      )}
    </form>
  );
}
