'use client';

import { useState } from 'react';

interface VerifyCodeFormProps {
  lang: string;
  token: string;
  authToken: string;
  dict: Record<string, string>;
}

export default function VerifyCodeForm({ lang, token, authToken, dict }: VerifyCodeFormProps) {
  const [code, setCode] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const t = (key: string, fallback: string = ''): string => dict[key] || fallback;

  const handleCodeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    // Strip non-digits and limit to 6 characters
    const digitsOnly = e.target.value.replace(/\D/g, '').slice(0, 6);
    setCode(digitsOnly);
    setError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Client-side validation
    const cleanCode = code.replace(/\D/g, '');
    if (cleanCode.length !== 6) {
      setError(t('verify_error_format', 'Code must be exactly 6 digits.'));
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      const API_BASE = typeof window === 'undefined' ? process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || '' : process.env.NEXT_PUBLIC_API_URL || '';
      
      const response = await fetch(`${API_BASE}/api/v1/providers/claim/${token}/verify`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authToken}`,
        },
        body: JSON.stringify({ code: cleanCode }),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        setSuccess(true);
        // Redirect to dashboard on success
        window.location.href = `/${lang}/provider/dashboard`;
        return;
      }

      // Handle errors
      if (response.status === 400) {
        if (data.detail === 'invalid_or_expired_code') {
          setError(t('verify_error_invalid', 'Invalid or expired code. Check your business email inbox.'));
        } else if (data.detail === 'invalid_code_format') {
          setError(t('verify_error_format', 'Code must be exactly 6 digits.'));
        } else {
          setError(t('verify_error_invalid', 'Invalid or expired code. Check your business email inbox.'));
        }
      } else if (response.status === 409) {
        // Already claimed - redirect back to claim page with error
        window.location.href = `/${lang}/claim/${token}?error=already_claimed`;
        return;
      } else {
        setError(t('verify_error_invalid', 'Invalid or expired code. Check your business email inbox.'));
      }
    } catch (err) {
      setError(t('verify_error_invalid', 'Invalid or expired code. Check your business email inbox.'));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label htmlFor="code" className="block text-sm font-medium text-gray-700 mb-2">
          {t('verify_code_label', 'Verification code')}
        </label>
        <input
          id="code"
          type="text"
          inputMode="numeric"
          pattern="[0-9]*"
          maxLength={6}
          placeholder={t('verify_code_placeholder', '000000')}
          value={code}
          onChange={handleCodeChange}
          disabled={submitting || success}
          className="w-full text-center text-3xl tracking-widest font-semibold px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 disabled:opacity-50 disabled:cursor-not-allowed"
          style={{ letterSpacing: '0.15em' }}
        />
      </div>

      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      <button
        type="submit"
        disabled={submitting || code.length < 6 || success}
        className="w-full bg-orange-500 hover:bg-orange-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-semibold py-3 px-6 rounded-xl transition-colors"
      >
        {submitting ? t('verify_submitting', 'Verifying...') : t('verify_submit', 'Confirm and claim profile')}
      </button>
    </form>
  );
}
