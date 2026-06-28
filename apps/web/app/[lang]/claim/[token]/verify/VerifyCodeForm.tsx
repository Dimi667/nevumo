'use client';

import { useState, useEffect } from 'react';
import { saveAuth } from '@/lib/auth-store';

interface VerifyCodeFormProps {
  lang: string;
  token: string;
  dict: Record<string, string>;
  sentTo?: string;
}

export default function VerifyCodeForm({ lang, token, dict, sentTo }: VerifyCodeFormProps) {
  const [code, setCode] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [resendCooldown, setResendCooldown] = useState(0);
  const [showResend, setShowResend] = useState(false);
  const [resending, setResending] = useState(false);

  const t = (key: string, fallback: string = ''): string => dict[key] || fallback;

  // 60-second timer to show resend button on mount
  useEffect(() => {
    const timer = setTimeout(() => setShowResend(true), 60000);
    return () => clearTimeout(timer);
  }, []);

  // Cooldown timer for resend button
  useEffect(() => {
    if (resendCooldown <= 0) return;
    const interval = setInterval(() => {
      setResendCooldown(prev => {
        if (prev <= 1) {
          clearInterval(interval);
          setShowResend(true);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [resendCooldown]);

  const handleCodeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    // Strip non-digits and limit to 6 characters
    const digitsOnly = e.target.value.replace(/\D/g, '').slice(0, 6);
    setCode(digitsOnly);
    setError(null);
  };

  const handleResend = async () => {
    if (resendCooldown > 0 || resending) return;

    setResending(true);
    try {
      const API_BASE = typeof window === 'undefined' ? process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || '' : process.env.NEXT_PUBLIC_API_URL || '';
      const res = await fetch(`${API_BASE}/api/v1/providers/claim/${token}?lang=${lang}&source=banner`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (res.ok) {
        const data = await res.json();
        // Update sessionStorage with new sent_to
        try {
          sessionStorage.setItem(`claim_sent_to_${token}`, data.sent_to ?? '');
        } catch {}
        setError(null);
        setShowResend(false);
        // Start 30-second cooldown
        setResendCooldown(30);
      } else {
        setError(t('verify_error_network'));
        setShowResend(true);
      }
    } catch {
      setError(t('verify_error_network'));
      setShowResend(true);
    } finally {
      setResending(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Client-side validation
    const cleanCode = code.replace(/\D/g, '');
    if (cleanCode.length !== 6) {
      setError(t('verify_error_format', 'Code must be exactly 6 digits.'));
      setShowResend(true);
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      const API_BASE = typeof window === 'undefined' ? process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || '' : process.env.NEXT_PUBLIC_API_URL || '';
      
      const response = await fetch(`${API_BASE}/api/v1/providers/claim/${token}/verify?lang=${lang}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: cleanCode }),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        setSuccess(true);
        // Save JWT from backend response and redirect
        saveAuth(data.token, data.user);
        window.location.replace(data.redirect);
        return;
      }

      // Handle errors
      if (response.status === 400) {
        const code = data?.detail?.code;
        if (code === 'CODE_INVALID') {
          setError(t('verify_error_invalid'));
        } else if (code === 'CODE_EXPIRED') {
          setError(t('verify_error_expired'));
        } else if (data.detail === 'invalid_code_format') {
          setError(t('verify_error_format'));
        } else {
          setError(t('verify_error_invalid'));
        }
        setShowResend(true);
      } else if (response.status === 409) {
        // Already claimed - redirect back to claim page with error
        window.location.href = `/${lang}/claim/${token}?error=already_claimed`;
        return;
      } else {
        setError(t('verify_error_invalid'));
        setShowResend(true);
      }
    } catch {
      setError(t('verify_error_network'));
      setShowResend(true);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {sentTo && (
        <p className="text-sm text-gray-600 mb-4">
          Kod weryfikacyjny został wysłany na adres:{' '}
          <span className="font-medium text-gray-900">{sentTo}</span>
        </p>
      )}

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
          {showResend && (
            <button
              onClick={handleResend}
              disabled={resending || resendCooldown > 0}
              className="mt-3 text-sm text-blue-600 hover:underline disabled:text-gray-400 disabled:no-underline"
            >
              {resendCooldown > 0
                ? `${t('resend_cooldown')} ${resendCooldown}s`
                : t('resend_code')}
            </button>
          )}
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
