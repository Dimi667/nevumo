'use client';
// TODO: i18n

import { useState, useEffect, useRef, useCallback } from "react";
import { useSearchParams } from "next/navigation";
import { trackPageEvent } from "@/lib/tracking";
import { getStoredIntent, clearStoredIntent } from "@/lib/intent";
import { checkEmail, loginWithEmail, registerWithEmail, forgotPassword } from "@/lib/auth-api";
import { saveAuth, isAuthenticated, getAuthUser } from "@/lib/auth-store";
import { ApiError } from "@/lib/api";

function generateStrongPassword(): string {
  const uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  const lowercase = 'abcdefghijklmnopqrstuvwxyz';
  const numbers = '0123456789';
  const symbols = '!@#$%&*_+-=?';
  const all = uppercase + lowercase + numbers + symbols;
  const getRandomChar = (chars: string) => chars[Math.floor(Math.random() * chars.length)];
  const password = [
    getRandomChar(uppercase),
    getRandomChar(lowercase),
    getRandomChar(numbers),
    getRandomChar(symbols),
  ];
  for (let i = password.length; i < 16; i++) password.push(getRandomChar(all));
  for (let i = password.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [password[i], password[j]] = [password[j]!, password[i]!];
  }
  return password.join('');
}

function triggerPasswordSave(email: string, password: string): void {
  const form = document.createElement('form');
  form.method = 'POST';
  form.action = 'about:blank';
  form.target = 'nevumo-auth-frame';
  form.style.display = 'none';

  const emailInput = document.createElement('input');
  emailInput.type = 'email';
  emailInput.name = 'email';
  emailInput.autocomplete = 'username';
  emailInput.value = email;
  form.appendChild(emailInput);

  const passwordInput = document.createElement('input');
  passwordInput.type = 'password';
  passwordInput.name = 'password';
  passwordInput.autocomplete = password.length > 0 ? 'current-password' : 'new-password';
  passwordInput.value = password;
  form.appendChild(passwordInput);

  document.body.appendChild(form);
  form.submit();

  setTimeout(() => {
    document.body.removeChild(form);
  }, 1000);
}

// ---------------------------------------------------------------------------
// Icons (inline SVG — no external deps)
// ---------------------------------------------------------------------------

function GoogleIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M17.64 9.205c0-.639-.057-1.252-.164-1.841H9v3.481h4.844a4.14 4.14 0 0 1-1.796 2.716v2.259h2.908c1.702-1.567 2.684-3.875 2.684-6.615Z" fill="#4285F4"/>
      <path d="M9 18c2.43 0 4.467-.806 5.956-2.18l-2.908-2.259c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332A8.997 8.997 0 0 0 9 18Z" fill="#34A853"/>
      <path d="M3.964 10.71A5.41 5.41 0 0 1 3.682 9c0-.593.102-1.17.282-1.71V4.958H.957A8.996 8.996 0 0 0 0 9c0 1.452.348 2.827.957 4.042l3.007-2.332Z" fill="#FBBC05"/>
      <path d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0A8.997 8.997 0 0 0 .957 4.958L3.964 7.29C4.672 5.163 6.656 3.58 9 3.58Z" fill="#EA4335"/>
    </svg>
  );
}

function FacebookIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect width="18" height="18" rx="4" fill="#1877F2"/>
      <path d="M12.5 9H10.5V15H8V9H6.5V6.5H8V5C8 3.619 8.619 3 10 3H12V5.5H10.75C10.336 5.5 10 5.836 10 6.25V6.5H12L11.75 9H12.5Z" fill="white"/>
    </svg>
  );
}

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

type AuthStep = 'initial' | 'login' | 'register' | 'forgot';

interface AuthState {
  step: AuthStep;
  email: string;
  password: string;
  showPassword: boolean;
  loading: boolean;
  error: string | null;
  forgotSuccess: boolean;
  registerSuccess: boolean;
  socialToast: string | null;
  intent: 'client' | 'provider' | null;
}

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const SESSION_EMAIL_KEY = "nevumo_auth_email";

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

interface LoginClientProps {
  lang: string;
  initialRole: string | null;
}

export default function LoginClient({ lang, initialRole }: LoginClientProps) {
  const searchParams = useSearchParams();
  const claimToken = searchParams.get('claim');
  const [state, setState] = useState<AuthState>({
    step: 'initial',
    email: '',
    password: '',
    showPassword: false,
    loading: false,
    error: null,
    forgotSuccess: false,
    registerSuccess: false,
    socialToast: null,
    intent: null,
  });

  const [authDict, setAuthDict] = useState<Record<string, string>>({});

  const passwordRef = useRef<HTMLInputElement>(null);

  const isEmailValid = EMAIL_RE.test(state.email);

  // On mount: redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated()) {
      const user = getAuthUser();
      window.location.href = user?.role === 'provider'
        ? `/${lang}/provider/dashboard`
        : `/${lang}/client/dashboard`;
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // On mount: restore intent + email, fire auth_view event
  useEffect(() => {
    const stored = getStoredIntent();
    // Claim token forces provider intent
    const resolvedIntent: 'client' | 'provider' | null = claimToken
      ? 'provider'
      : stored.intent === 'client' || stored.intent === 'provider'
        ? stored.intent
        : initialRole === 'provider'
        ? 'provider'
        : 'client';

    const savedEmail = sessionStorage.getItem(SESSION_EMAIL_KEY) ?? '';

    setState(s => ({ ...s, intent: resolvedIntent, email: savedEmail }));
    trackPageEvent('auth_view', 'auth', { intent: resolvedIntent ?? 'unknown' });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Fetch auth namespace translations
  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/translations?lang=${lang}&namespace=auth`)
      .then(r => r.json())
      .then(json => { if (json.success) setAuthDict(json.data) })
      .catch(() => {})
  }, [lang]);

  // Store claim token on mount
  useEffect(() => {
    if (claimToken) {
      sessionStorage.setItem('nevumo_claim_token', claimToken);
    }
  }, [claimToken]);

  // -------------------------------------------------------------------------
  // Handlers
  // -------------------------------------------------------------------------

  function handleEmailChange(value: string) {
    sessionStorage.setItem(SESSION_EMAIL_KEY, value);
    setState(s => ({ ...s, email: value, error: null }));
  }

  function handlePasswordChange(value: string) {
    setState(s => ({ ...s, password: value, error: null }));
  }

  async function handleCheckEmail() {
    if (!isEmailValid || state.loading) return;
    setState(s => ({ ...s, loading: true, error: null }));
    try {
      const { exists } = await checkEmail(state.email);
      trackPageEvent('auth_email_entered', 'auth', { is_new: String(!exists) });
      const nextStep: AuthStep = exists ? 'login' : 'register';
      trackPageEvent('auth_password_shown', 'auth', { step: nextStep });
      setState(s => ({ ...s, loading: false, step: nextStep, password: '' }));
    } catch {
      setState(s => ({ ...s, loading: false, error: 'Възникна грешка. Опитай отново.' }));
    }
  }

  async function handleLogin() {
    if (state.loading) return;
    setState(s => ({ ...s, loading: true, error: null }));
    try {
      const result = await loginWithEmail(state.email, state.password);
      saveAuth(result.token, result.user);
      triggerPasswordSave(state.email, state.password);
      trackPageEvent('auth_success', 'auth', { method: 'email' });
      sessionStorage.removeItem(SESSION_EMAIL_KEY);
      clearStoredIntent();
      setState(s => ({ ...s, loading: false }));

      // Handle pending claim if exists
      const pendingClaimToken = sessionStorage.getItem('nevumo_claim_token');
      if (pendingClaimToken) {
        try {
          const claimRes = await fetch(
            `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/providers/claim`,
            {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${result.token}`
              },
              body: JSON.stringify({ claim_token: pendingClaimToken })
            }
          );
          sessionStorage.removeItem('nevumo_claim_token');
          if (claimRes.ok) {
            window.location.href = `/${lang}/provider/dashboard/profile`;
            return;
          }
        } catch {
          sessionStorage.removeItem('nevumo_claim_token');
        }
      }

      const role = result.user.role;
      window.location.href = role === 'provider'
        ? `/${lang}/provider/dashboard`
        : `/${lang}/client/dashboard`;
    } catch (err) {
      if (err instanceof ApiError) {
        if (err.code === 'INVALID_CREDENTIALS' || err.message.includes('Invalid credentials')) {
          setState(s => ({ ...s, loading: false, error: 'invalid_password' }));
        } else if (err.code === 'RATE_LIMIT_EXCEEDED' || err.message.includes('Too many')) {
          setState(s => ({ ...s, loading: false, error: 'Твърде много опити. Опитай по-късно.' }));
        } else if (err.code === 'ACCOUNT_DISABLED') {
          setState(s => ({ ...s, loading: false, error: 'Акаунтът е деактивиран.' }));
        } else {
          setState(s => ({ ...s, loading: false, error: 'Възникна грешка. Опитай отново.' }));
        }
      } else {
        setState(s => ({ ...s, loading: false, error: 'Възникна грешка. Опитай отново.' }));
      }
    }
  }

  async function handleRegister() {
    if (state.loading) return;

    // Register both client and provider immediately (no slug step on auth page)
    setState(s => ({ ...s, loading: true, error: null }));
    try {
      const role = state.intent ?? 'client';
      const result = await registerWithEmail(state.email, state.password, role, lang);
      saveAuth(result.token, result.user);
      triggerPasswordSave(state.email, state.password);
      trackPageEvent('auth_success', 'login', { method: 'email' });
      sessionStorage.removeItem(SESSION_EMAIL_KEY);
      clearStoredIntent();
      setState(s => ({ ...s, loading: false, registerSuccess: true }));

      // Handle pending claim if exists
      const pendingClaimToken = sessionStorage.getItem('nevumo_claim_token');
      if (pendingClaimToken) {
        try {
          const claimRes = await fetch(
            `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/providers/claim`,
            {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${result.token}`
              },
              body: JSON.stringify({ claim_token: pendingClaimToken })
            }
          );
          sessionStorage.removeItem('nevumo_claim_token');
          if (claimRes.ok) {
            window.location.href = `/${lang}/provider/dashboard/profile`;
            return;
          }
        } catch {
          sessionStorage.removeItem('nevumo_claim_token');
        }
      }

      const redirectPath = result.user.role === 'provider'
        ? `/${lang}/provider/dashboard/profile`
        : `/${lang}/client/dashboard`;
      setTimeout(() => { window.location.href = redirectPath; }, 1000);
    } catch (err) {
      if (err instanceof ApiError) {
        if (err.code === 'EMAIL_ALREADY_EXISTS' || err.message.includes('already registered')) {
          setState(s => ({ ...s, loading: false, error: 'Този имейл вече е регистриран.' }));
        } else if (err.code === 'VALIDATION_ERROR') {
          setState(s => ({ ...s, loading: false, error: err.message }));
        } else {
          setState(s => ({ ...s, loading: false, error: 'Възникна грешка. Опитай отново.' }));
        }
      } else {
        setState(s => ({ ...s, loading: false, error: 'Възникна грешка. Опитай отново.' }));
      }
    }
  }


  async function handleForgot() {
    if (state.loading || state.forgotSuccess) return;
    setState(s => ({ ...s, loading: true, error: null }));
    try {
      await forgotPassword(state.email);
      setState(s => ({ ...s, loading: false, forgotSuccess: true }));
    } catch {
      // Always show success — don't reveal if email exists (security)
      setState(s => ({ ...s, loading: false, forgotSuccess: true }));
    }
  }

  function handleBack() {
    if (state.step === 'forgot') {
      setState(s => ({ ...s, step: 'login', error: null, forgotSuccess: false }));
    } else {
      setState(s => ({ ...s, step: 'initial', password: '', error: null }));
    }
  }

  function handleSocialClick(_provider: 'google' | 'facebook') {
    // TODO: integrate real OAuth
    setState(s => ({ ...s, socialToast: 'Очаквайте скоро' }));
    setTimeout(() => setState(s => ({ ...s, socialToast: null })), 2000);
  }

  // -------------------------------------------------------------------------
  // Shared UI pieces
  // -------------------------------------------------------------------------

  const primaryBtn = (
    disabled: boolean,
    loading: boolean,
    label: string,
    loadingLabel: string,
    onClick: () => void
  ) => (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`w-full py-2.5 rounded-lg text-base font-semibold text-white transition-colors mt-4
        ${disabled ? 'bg-gray-300 cursor-not-allowed' : 'bg-orange-500 hover:bg-orange-600'}`}
    >
      {loading ? loadingLabel : label}
    </button>
  );

  const emailPill = (
    <div className="bg-gray-100 rounded-lg px-3 py-2 text-sm text-gray-500 mb-4 break-all">
      {state.email}
    </div>
  );

  const backBtn = (
    <button
      onClick={handleBack}
      className="text-sm text-gray-500 hover:text-gray-700 mb-5 transition-colors"
    >
      ← {state.step === 'forgot' ? 'Назад' : 'Назад'}
    </button>
  );

  const genericError = state.error && state.error !== 'invalid_password' && (
    <p className="text-red-500 text-xs mt-2 text-center">
      {state.error}
    </p>
  );

  // -------------------------------------------------------------------------
  // Render
  // -------------------------------------------------------------------------

  return (
    <div className="min-h-screen bg-[#f9f9f9] flex flex-col items-center justify-start pt-16 px-4 pb-16">
      <div className="w-full max-w-[400px] bg-white rounded-xl border border-gray-200 p-8">

        {/* ---- INITIAL STEP ---- */}
        {state.step === 'initial' && (
          <>
            {/* Intent-based header (or claim-specific when claim token present) */}
            <div className="mb-6 text-center">
              <h1 className="text-[20px] font-bold text-[#171717] leading-tight">
                {claimToken
                  ? authDict['claim_headline'] || "Claim your profile on Nevumo"
                  : state.intent === 'provider'
                  ? 'Започни да получаваш клиенти'
                  : 'Намери услуга за минути'}
              </h1>
              {claimToken ? (
                <p className="text-sm text-gray-500 mt-1">
                  {authDict['claim_subtitle'] || "Register for free and manage your clients"}
                </p>
              ) : state.intent !== 'provider' && (
                <p className="text-sm text-gray-500 mt-1">Безплатно • Без ангажимент</p>
              )}
            </div>

            {/* Social buttons */}
            <p className="text-center text-xs mb-2 transition-colors"
               style={{ color: state.socialToast ? '#f97316' : '#6b7280' }}>
              {state.socialToast ?? (authDict['quick_login_label'] || "Quick login without password")}
            </p>
            <div className="flex flex-col gap-[10px]">
              <button
                onClick={() => handleSocialClick('google')}
                className="w-full flex items-center justify-center gap-2 py-2.5 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors"
              >
                <GoogleIcon />
                {authDict['google_btn'] || "Sign in with Google"}
              </button>
              <button
                onClick={() => handleSocialClick('facebook')}
                className="w-full flex items-center justify-center gap-2 py-2.5 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors"
              >
                <FacebookIcon />
                {authDict['facebook_btn'] || "Sign in with Facebook"}
              </button>
            </div>

            {/* Divider */}
            <div className="flex items-center gap-3 my-5">
              <div className="flex-1 h-px bg-gray-200" />
              <span className="text-xs text-gray-400">{authDict['or_with_email'] || "or with email"}</span>
              <div className="flex-1 h-px bg-gray-200" />
            </div>

            {/* Email input */}
            <input
              type="email"
              autoComplete="email"
              autoFocus
              placeholder="name@email.com"
              value={state.email}
              onChange={e => handleEmailChange(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter') handleCheckEmail(); }}
              className="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400"
            />

            {/* Продължи button */}
            {primaryBtn(
              !isEmailValid || state.loading,
              state.loading,
              claimToken ? (authDict['claim_cta_btn'] || "Claim profile") : (authDict['continue_btn'] || "Continue"),
              'Проверка...',
              handleCheckEmail
            )}

            {genericError}
          </>
        )}

        {/* ---- LOGIN STEP ---- */}
        {state.step === 'login' && (
          <>
            {backBtn}
            {emailPill}

            <form onSubmit={e => { e.preventDefault(); handleLogin(); }}>
              <input type="email" name="email" value={state.email} readOnly autoComplete="username" onChange={() => {}} style={{ position: 'absolute', opacity: 0, height: 0, width: 0, overflow: 'hidden' }} />
              <div className="flex flex-col gap-1">
                <input
                  ref={passwordRef}
                  type="password"
                  name="password"
                  autoComplete="current-password"
                  placeholder="Парола"
                  value={state.password}
                  onChange={e => handlePasswordChange(e.target.value)}
                  className={`w-full border rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400
                    ${state.error === 'invalid_password' ? 'border-red-400' : 'border-gray-300'}`}
                />
                {state.error === 'invalid_password' && (
                  <p className="text-red-500 text-xs mt-0.5">Грешна парола</p>
                )}
              </div>

              <div className="flex justify-end mt-1.5">
                <button
                  type="button"
                  onClick={() => setState(s => ({ ...s, step: 'forgot', error: null }))}
                  className="text-xs text-gray-500 hover:text-gray-700 transition-colors"
                >
                  Забравена парола?
                </button>
              </div>

              <button
                type="submit"
                disabled={state.password.length === 0 || state.loading}
                className={`w-full py-2.5 rounded-lg text-base font-semibold text-white transition-colors mt-4
                  ${state.password.length > 0 && !state.loading
                    ? 'bg-orange-500 hover:bg-orange-600 cursor-pointer'
                    : 'bg-gray-400 opacity-50 cursor-not-allowed'}`}
              >
                {state.loading ? 'Влизане...' : 'Вход'}
              </button>
            </form>

            {genericError}
          </>
        )}

        {/* ---- REGISTER STEP ---- */}
        {state.step === 'register' && (
          <>
            {backBtn}
            {emailPill}

            {claimToken ? (
              <>
                <h2 className="text-[17px] font-bold text-[#171717] mb-1">
                  {authDict['claim_headline'] || "Claim your profile on Nevumo"}
                </h2>
                <p className="text-sm text-gray-500 mb-3">
                  {authDict['claim_subtitle'] || "Register for free and manage your clients"}
                </p>
              </>
            ) : (
              <p className="text-xs text-gray-600 mb-3">Ще създадем акаунт автоматично</p>
            )}

            <form onSubmit={e => { e.preventDefault(); handleRegister(); }}>
              <input type="email" name="email" value={state.email} readOnly autoComplete="username" onChange={() => {}} style={{ position: 'absolute', opacity: 0, height: 0, width: 0, overflow: 'hidden' }} />
              <div className="relative mb-6">
                <input
                  ref={passwordRef}
                  type={state.showPassword ? 'text' : 'password'}
                  name="password"
                  autoComplete="new-password"
                  placeholder="Кликни тук за генериране на парола"
                  value={state.password}
                  onChange={e => handlePasswordChange(e.target.value)}
                  onClick={() => {
                    if (!state.password) {
                      setState(s => ({ ...s, password: generateStrongPassword(), showPassword: true, error: null }));
                    }
                  }}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2.5 pr-10 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400"
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

              <button
                type="submit"
                disabled={state.password.length === 0 || state.loading}
                className={`w-full py-2.5 rounded-lg text-base font-semibold text-white transition-colors mt-4
                  ${state.password.length > 0 && !state.loading ? 'bg-orange-500 hover:bg-orange-600 cursor-pointer' : 'bg-gray-300 cursor-not-allowed'}`}
              >
                {state.loading ? 'Създаване...' : claimToken ? (authDict['claim_cta_btn'] || "Claim profile") : (authDict['continue_btn'] || "Continue")}
              </button>
            </form>

            {state.registerSuccess && (
              <div className="bg-green-50 text-green-700 text-sm p-2.5 rounded-lg text-center mt-3">
                Акаунтът е създаден успешно
              </div>
            )}

            {genericError}
          </>
        )}

        {/* ---- FORGOT STEP ---- */}
        {state.step === 'forgot' && (
          <>
            {backBtn}

            <div className="mb-5">
              <h2 className="text-[17px] font-bold text-[#171717]">Забравена парола</h2>
              <p className="text-sm text-gray-500 mt-1">Ще изпратим линк за нова парола</p>
            </div>

            {emailPill}

            <button
              onClick={handleForgot}
              disabled={state.loading || state.forgotSuccess}
              className={`w-full py-2.5 rounded-lg text-base font-semibold text-white bg-orange-500 transition-colors
                ${(state.loading || state.forgotSuccess) ? 'opacity-50 cursor-not-allowed' : 'hover:bg-orange-600'}`}
            >
              {state.forgotSuccess ? 'Изпратено' : state.loading ? 'Изпращане...' : 'Изпрати линк'}
            </button>

            {state.forgotSuccess && (
              <div className="bg-green-50 text-green-700 text-sm p-2.5 rounded-lg text-center mt-3">
                Провери имейла си
              </div>
            )}

            {genericError}
          </>
        )}

      </div>

      {/* Hidden iframe for browser password save trigger */}
      <iframe
        name="nevumo-auth-frame"
        style={{ display: 'none', width: 0, height: 0, position: 'absolute' }}
        tabIndex={-1}
        aria-hidden="true"
      />
    </div>
  );
}
