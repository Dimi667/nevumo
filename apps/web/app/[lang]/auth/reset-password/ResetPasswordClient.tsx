'use client';
// TODO: i18n

import { useState, useEffect, useRef } from "react";
import { trackPageEvent } from "@/lib/tracking";
import { getStoredIntent, clearStoredIntent } from "@/lib/intent";
import { validateResetToken, resetPassword } from "@/lib/auth-api";
import { saveAuth } from "@/lib/auth-store";
import { ApiError } from "@/lib/api";
import { saveCredentials } from '@/lib/password-save';

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// Icons
// ---------------------------------------------------------------------------

function EyeIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
      <circle cx="12" cy="12" r="3"/>
    </svg>
  );
}

function EyeOffIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/>
      <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/>
      <line x1="1" y1="1" x2="23" y2="23"/>
    </svg>
  );
}

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

type PageState = 'loading' | 'valid' | 'expired' | 'used' | 'success';

interface ResetState {
  page: PageState;
  password: string;
  confirm: string;
  showPassword: boolean;
  loading: boolean;
  error: string | null;
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

interface ResetPasswordClientProps {
  lang: string;
  token: string;
}

export default function ResetPasswordClient({ lang, token }: ResetPasswordClientProps) {
  const [state, setState] = useState<ResetState>({
    page: 'loading',
    password: '',
    confirm: '',
    showPassword: false,
    loading: false,
    error: null,
  });

  const passwordRef = useRef<HTMLInputElement>(null);
  const confirmRef = useRef<HTMLInputElement>(null);

  const bothFilled = state.password.length > 0 && state.confirm.length > 0;

  // Validate token on mount
  useEffect(() => {
    validateResetToken(token).then(result => {
      if (result.valid) {
        trackPageEvent('password_reset_view', 'reset-password', { token_valid: 'true' });
        setState(s => ({ ...s, page: 'valid' }));
      } else if (result.error === 'used') {
        trackPageEvent('token_used', 'reset-password', {});
        setState(s => ({ ...s, page: 'used' }));
      } else {
        trackPageEvent('token_expired', 'reset-password', {});
        setState(s => ({ ...s, page: 'expired' }));
      }
    }).catch(() => {
      trackPageEvent('token_expired', 'reset-password', {});
      setState(s => ({ ...s, page: 'expired' }));
    });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Autofocus first password field when form is ready
  useEffect(() => {
    if (state.page === 'valid') {
      passwordRef.current?.focus();
    }
  }, [state.page]);

  // -------------------------------------------------------------------------
  // Handlers
  // -------------------------------------------------------------------------

  async function handleSubmit() {
    if (!bothFilled || state.loading) return;

    if (state.password !== state.confirm) {
      trackPageEvent('password_reset_error', 'reset-password', { error: 'mismatch' });
      setState(s => ({ ...s, error: 'mismatch' }));
      confirmRef.current?.focus();
      return;
    }

    if (state.password.length < 8) {
      trackPageEvent('password_reset_error', 'reset-password', { error: 'too_short' });
      setState(s => ({ ...s, error: 'too_short' }));
      passwordRef.current?.focus();
      return;
    }

    setState(s => ({ ...s, loading: true, error: null }));
    try {
      const result = await resetPassword(token, state.password);
      saveAuth(result.token, result.user);

      // Trigger browser password save using user email from auth result
      await saveCredentials(result.user.email, state.password);

      trackPageEvent('password_reset_success', 'reset-password', {});
      setState(s => ({ ...s, loading: false, page: 'success' }));

      // Auto-redirect after 2 seconds based on intent
      setTimeout(() => {
        // Intent stored server-side in future; for now fallback to localStorage or homepage.
        const { intent } = getStoredIntent();
        clearStoredIntent();
        const role = result.user.role;
        if (role === 'provider' || intent === 'provider') {
          window.location.href = `/${lang}/provider/dashboard`;
        } else {
          window.location.href = `/${lang}`;
        }
      }, 2000);
    } catch (err) {
      if (err instanceof ApiError) {
        if (err.code === 'TOKEN_EXPIRED' || err.code === 'TOKEN_INVALID' || err.message.includes('expired')) {
          setState(s => ({ ...s, loading: false, page: 'expired' }));
        } else if (err.code === 'TOKEN_USED') {
          setState(s => ({ ...s, loading: false, page: 'used' }));
        } else if (err.code === 'VALIDATION_ERROR') {
          setState(s => ({ ...s, loading: false, error: err.message }));
        } else {
          setState(s => ({ ...s, loading: false, error: 'Нещо се обърка. Опитай отново.' }));
        }
      } else {
        setState(s => ({ ...s, loading: false, error: 'Нещо се обърка. Опитай отново.' }));
      }
    }
  }

  function handlePasswordChange(value: string) {
    setState(s => ({ ...s, password: value, error: null }));
  }

  function handleConfirmChange(value: string) {
    setState(s => ({ ...s, confirm: value, error: null }));
  }

  // -------------------------------------------------------------------------
  // Shared layout wrapper
  // -------------------------------------------------------------------------

  const card = (children: React.ReactNode) => (
    <div className="min-h-screen bg-[#f9f9f9] flex flex-col items-center justify-start pt-16 px-4 pb-16">
      <div className="w-full max-w-[400px] bg-white rounded-xl border border-gray-200 p-8">
        {children}
      </div>
    </div>
  );

  // -------------------------------------------------------------------------
  // States
  // -------------------------------------------------------------------------

  if (state.page === 'loading') {
    return card(
      <p className="text-center text-gray-500 text-sm py-4">Зареждане...</p>
    );
  }

  if (state.page === 'expired') {
    return card(
      <div className="text-center">
        <h1 className="text-[18px] font-bold text-[#171717] mb-6">
          Линкът е изтекъл или невалиден
        </h1>
        <button
          onClick={() => { window.location.href = `/${lang}/auth`; }}
          className="w-full py-2.5 rounded-lg text-base font-semibold text-white bg-orange-500 hover:bg-orange-600 transition-colors"
        >
          Изпрати нов линк
        </button>
      </div>
    );
  }

  if (state.page === 'used') {
    return card(
      <div className="text-center">
        <h1 className="text-[18px] font-bold text-[#171717] mb-2">
          Този линк вече е използван
        </h1>
        <p className="text-sm text-gray-500 mb-6">
          Можеш да влезеш с новата си парола
        </p>
        <button
          onClick={() => { window.location.href = `/${lang}/auth`; }}
          className="w-full py-2.5 rounded-lg text-base font-semibold text-white bg-orange-500 hover:bg-orange-600 transition-colors"
        >
          Към вход
        </button>
      </div>
    );
  }

  if (state.page === 'success') {
    return card(
      <div className="bg-green-50 text-green-700 rounded-lg p-5 text-center">
        <p className="font-semibold text-base">Паролата е сменена успешно</p>
        <p className="text-sm mt-1">Логваме те...</p>
      </div>
    );
  }

  // 'valid' — reset form
  return card(
    <>
      <h1 className="text-[20px] font-bold text-[#171717] text-center mb-6">
        Нова парола
      </h1>

      <form onSubmit={e => { e.preventDefault(); handleSubmit(); }}>
        {/* First password field */}
        <div className="relative mb-3">
          <input
            ref={passwordRef}
            type={state.showPassword ? 'text' : 'password'}
            name="new-password"
            autoComplete="new-password"
            placeholder="Нова парола"
            value={state.password}
            onChange={e => handlePasswordChange(e.target.value)}
            className={`w-full border rounded-lg px-3 py-2.5 pr-10 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400
              ${state.error === 'too_short' ? 'border-red-400' : 'border-gray-300'}`}
          />
          <button
            type="button"
            onClick={() => setState(s => ({ ...s, showPassword: !s.showPassword }))}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
            tabIndex={-1}
          >
            {state.showPassword ? <EyeOffIcon /> : <EyeIcon />}
          </button>
        </div>
        {state.error === 'too_short' && (
          <p className="text-red-500 text-xs mb-2">Минимум 8 символа</p>
        )}

        {/* Confirm password field */}
        <div className="mb-1">
          <input
            ref={confirmRef}
            type="password"
            name="confirm-password"
            autoComplete="new-password"
            placeholder="Потвърди паролата"
            value={state.confirm}
            onChange={e => handleConfirmChange(e.target.value)}
            className={`w-full border rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400
              ${state.error === 'mismatch' ? 'border-red-400' : 'border-gray-300'}`}
          />
        </div>
        {state.error === 'mismatch' && (
          <p className="text-red-500 text-xs mb-1">Паролите не съвпадат</p>
        )}

        {/* Hint */}
        <p className="text-gray-400 text-xs mt-1.5 mb-6">Минимум 8 символа</p>

        {/* Submit button */}
        <button
          type="submit"
          disabled={!bothFilled || state.loading}
          className={`w-full py-2.5 rounded-lg text-base font-semibold text-white transition-colors
            ${bothFilled && !state.loading
              ? 'bg-orange-500 hover:bg-orange-600 cursor-pointer'
              : 'bg-gray-300 cursor-not-allowed'}`}
        >
          {state.loading ? 'Запазване...' : 'Потвърди'}
        </button>

        {state.error && state.error !== 'mismatch' && state.error !== 'too_short' && (
          <p className="text-red-500 text-xs mt-2 text-center">
            Нещо се обърка. Опитай отново.
          </p>
        )}
      </form>
    </>
  );
}
