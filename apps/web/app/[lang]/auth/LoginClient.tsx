'use client';
// TODO: i18n

import { useState, useEffect, useRef, useCallback } from "react";
import { useSearchParams, useParams } from "next/navigation";
import Link from "next/link";
import { trackPageEvent } from "@/lib/tracking";
import { getStoredIntent, clearStoredIntent } from "@/lib/intent";
import { checkEmail, loginWithEmail, registerWithEmail, forgotPassword, requestMagicLink } from "@/lib/auth-api";
import { saveAuth, isAuthenticated, getAuthUser } from "@/lib/auth-store";
import { setCtx } from "@/lib/ctx";
import { ApiError, API_BASE, getCityBySlug } from "@/lib/api";
import { saveCredentials } from '@/lib/password-save';
import LegalModal from '@/components/auth/LegalModal';
import { useTranslation } from '@/lib/use-translation';

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

type AuthStep = 'initial' | 'login' | 'register' | 'forgot' | 'select_role';

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
  _pendingGoogle?: boolean;
}

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const SESSION_EMAIL_KEY = "nevumo_auth_email";

function addFromAuthParam(url: string): string {
  if (url.includes('?')) {
    return url + '&from=auth';
  }
  return url + '?from=auth';
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

interface LoginClientProps {
  lang: string;
  initialRole: string | null;
  authDict: Record<string, string>;
  footerDict: Record<string, string>;
  redirectAfterLogin?: string | null;
}

export default function LoginClient({ lang, initialRole, authDict, footerDict, redirectAfterLogin }: LoginClientProps) {
  console.log('[AuthPage] authDict keys:', Object.keys(authDict));
  console.log('[AuthPage] authDict sample:', authDict);
  const t = (dict: Record<string, string>, key: string, fallback: string): string => dict[key] ?? fallback;
  const searchParams = useSearchParams();
  const params = useParams();
  const citySlug = (params?.city as string) || searchParams.get('city') || null;
  const [cityId, setCityId] = useState<number | null>(null);

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

  const [termsAccepted, setTermsAccepted] = useState(false);
  const [legalModalOpen, setLegalModalOpen] = useState(false);
  const [legalModalType, setLegalModalType] = useState<'terms' | 'terms-provider' | 'privacy'>('terms');
  const [showMagicLink, setShowMagicLink] = useState(false);
  const [magicEmail, setMagicEmail] = useState("");
  const [magicStatus, setMagicStatus] = useState<"idle"|"loading"|"success"|"error"|"rate_limit">("idle");

  const { dict: termsDict } = useTranslation('terms', lang);
  const { dict: termsProviderDict } = useTranslation('provider_terms', lang);
  const { dict: privacyDict } = useTranslation('privacy', lang);

  const getDocDict = () => {
    switch (legalModalType) {
      case 'terms':
        return termsDict;
      case 'terms-provider':
        return termsProviderDict;
      case 'privacy':
        return privacyDict;
      default:
        return {};
    }
  };

  const passwordRef = useRef<HTMLInputElement>(null);

  const isEmailValid = EMAIL_RE.test(state.email);

  // On mount: redirect if already authenticated
  useEffect(() => {
    const checkAuth = () => {
      if (isAuthenticated()) {
        const user = getAuthUser();
        window.location.href = user?.role === 'provider'
          ? `/${lang}/provider/dashboard`
          : `/${lang}/client/dashboard`;
      }
    };

    checkAuth();

    // Handle BFCache (back-forward cache)
    window.addEventListener('pageshow', checkAuth);
    return () => window.removeEventListener('pageshow', checkAuth);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [lang]);

  // Reset terms accepted when step changes
  useEffect(() => {
    setTermsAccepted(false);
  }, [state.step]);

  // On mount: restore intent + email, fire auth_view event
  useEffect(() => {
    const stored = getStoredIntent();
    const urlEmail = searchParams.get('email');
    const oauthError = searchParams.get('error');

    // Handle OAuth error
    if (oauthError === 'oauth_failed') {
      setState(s => ({ ...s, socialToast: t(authDict, 'oauth_error', 'OAuth login failed. Please try again.') }));
      setTimeout(() => setState(s => ({ ...s, socialToast: null })), 3000);
    }
    
    // Claim token forces provider intent
    const urlIntent = searchParams.get('intent') as 'client' | 'provider' | null;
    const urlRole = searchParams.get('role') as 'client' | 'provider' | null;
    const storedIntent = (stored.intent === 'client' || stored.intent === 'provider') ? stored.intent : null;
    const resolvedIntent: 'client' | 'provider' | null = claimToken
      ? 'provider'
      : urlIntent ?? urlRole ?? storedIntent ?? (initialRole === 'provider' ? 'provider' : null);

    const savedEmail = (urlEmail || sessionStorage.getItem(SESSION_EMAIL_KEY)) ?? '';

    setState(s => ({ ...s, intent: resolvedIntent, email: savedEmail }));
    if (resolvedIntent && !storedIntent) {
      localStorage.setItem('nevumo_intent', resolvedIntent);
    }
    trackPageEvent('auth_view', 'auth', { intent: resolvedIntent ?? 'unknown' });
    
    // Fetch city ID if city slug is present in URL
    if (citySlug) {
      getCityBySlug(citySlug).then(cityData => {
        if (cityData) {
          setCityId(cityData.id);
        }
      });
    }

    // Auto-advance to password step if email is provided via URL
    if (urlEmail && EMAIL_RE.test(urlEmail)) {
      handleCheckEmailDirectly(urlEmail);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Separate function to handle email check without relying on state update which might be async
  async function handleCheckEmailDirectly(emailToCheck: string) {
    if (!emailToCheck || state.loading) return;

    if (isAuthenticated()) {
      const user = getAuthUser();
      window.location.href = user?.role === 'provider'
        ? `/${lang}/provider/dashboard`
        : `/${lang}/client/dashboard`;
      return;
    }

    setState(s => ({ ...s, loading: true, error: null }));
    try {
      const { exists } = await checkEmail(emailToCheck);
      trackPageEvent('auth_email_entered', 'auth', { is_new: String(!exists) });
      const currentIntent = localStorage.getItem('nevumo_intent');
      const nextStep: AuthStep = exists ? 'login' : (!currentIntent ? 'select_role' : 'register');
      trackPageEvent('auth_password_shown', 'auth', { step: nextStep });
      setState(s => ({ ...s, loading: false, step: nextStep, password: '' }));
    } catch {
      setState(s => ({ ...s, loading: false, error: t(authDict, 'error_generic', 'An error occurred. Please try again.') }));
    }
  }

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

    if (isAuthenticated()) {
      const user = getAuthUser();
      window.location.href = user?.role === 'provider'
        ? `/${lang}/provider/dashboard`
        : `/${lang}/client/dashboard`;
      return;
    }

    setState(s => ({ ...s, loading: true, error: null }));
    try {
      const { exists } = await checkEmail(state.email);
      trackPageEvent('auth_email_entered', 'auth', { is_new: String(!exists) });
      const currentIntent = localStorage.getItem('nevumo_intent');
      const nextStep: AuthStep = exists ? 'login' : (!currentIntent ? 'select_role' : 'register');
      trackPageEvent('auth_password_shown', 'auth', { step: nextStep });
      setState(s => ({ ...s, loading: false, step: nextStep, password: '' }));
    } catch {
      setState(s => ({ ...s, loading: false, error: t(authDict, 'error_generic', 'An error occurred. Please try again.') }));
    }
  }

  async function handleLogin(force = false) {
    if (state.loading && !force) return;

    if (isAuthenticated() && !force) {
      const user = getAuthUser();
      if (user?.role === 'provider') {
        window.location.href = `/${lang}/provider/dashboard`;
      } else {
        const citySlug = (user as any)?.city_slug;
        window.location.href = citySlug ? `/${lang}/${citySlug}` : `/${lang}/izberi-grad`;
      }
      return;
    }

    setState(s => ({ ...s, loading: true, error: null }));
    try {
      const result = await loginWithEmail(state.email, state.password);
      saveAuth(result.token, result.user);
      await saveCredentials(state.email, state.password);
      trackPageEvent('auth_success', 'auth', { method: 'email' });
      sessionStorage.removeItem(SESSION_EMAIL_KEY);
      clearStoredIntent();
      setState(s => ({ ...s, loading: false }));

      // Handle pending claim if exists
      const pendingClaimToken = sessionStorage.getItem('nevumo_claim_token');
      if (pendingClaimToken) {
        try {
          const claimRes = await fetch(
            `${API_BASE}/api/v1/providers/claim`,
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
            window.location.href = addFromAuthParam(`/${lang}/provider/dashboard/profile`);
            return;
          }
        } catch {
          sessionStorage.removeItem('nevumo_claim_token');
        }
      }

      const role = result.user.role;
      const loginRedirectPath = redirectAfterLogin
        ? addFromAuthParam(redirectAfterLogin)
        : role === 'provider'
        ? addFromAuthParam(`/${lang}/provider/dashboard`)
        : addFromAuthParam(`/${lang}/client/dashboard`);
      window.location.href = loginRedirectPath;
    } catch (err) {
      if (err instanceof ApiError) {
        if (err.code === 'INVALID_CREDENTIALS' || err.message.includes('Invalid credentials')) {
          setState(s => ({ ...s, loading: false, error: 'invalid_password' }));
        } else if (err.code === 'RATE_LIMIT_EXCEEDED' || err.message.includes('Too many')) {
          setState(s => ({ ...s, loading: false, error: t(authDict, 'error_rate_limit', 'Too many attempts. Please try later.') }));
        } else if (err.code === 'ACCOUNT_DISABLED') {
          setState(s => ({ ...s, loading: false, error: t(authDict, 'error_account_disabled', 'Account is disabled.') }));
        } else {
          setState(s => ({ ...s, loading: false, error: t(authDict, 'error_generic', 'An error occurred. Please try again.') }));
        }
      } else {
        setState(s => ({ ...s, loading: false, error: t(authDict, 'error_generic', 'An error occurred. Please try again.') }));
      }
    }
  }

  async function handleRegister() {
    if (state.loading) return;

    if (isAuthenticated()) {
      const user = getAuthUser();
      window.location.href = user?.role === 'provider'
        ? `/${lang}/provider/dashboard`
        : `/${lang}/client/dashboard`;
      return;
    }

    // Register both client and provider immediately (no slug step on auth page)
    setState(s => ({ ...s, loading: true, error: null }));
    try {
      const role = state.intent ?? 'client';
      const result = await registerWithEmail(
        state.email, 
        state.password, 
        role, 
        lang, 
        undefined, 
        undefined, 
        undefined, 
        cityId ?? null
      );
      saveAuth(result.token, result.user);
      await saveCredentials(state.email, state.password);
      trackPageEvent('auth_success', 'login', { method: 'email' });
      sessionStorage.removeItem(SESSION_EMAIL_KEY);
      clearStoredIntent();
      setState(s => ({ ...s, loading: false, registerSuccess: true }));

      // Handle pending claim if exists
      const pendingClaimToken = sessionStorage.getItem('nevumo_claim_token');
      if (pendingClaimToken) {
        try {
          const claimRes = await fetch(
            `${API_BASE}/api/v1/providers/claim`,
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
            window.location.href = addFromAuthParam(`/${lang}/provider/dashboard/profile`);
            return;
          }
        } catch {
          sessionStorage.removeItem('nevumo_claim_token');
        }
      }

      // Save city and category to localStorage for providers
      if (result.user.role === 'provider') {
        const cityParam = searchParams.get('city');
        const categoryParam = searchParams.get('category');
        if (cityParam) setCtx({ city: cityParam });
        if (categoryParam) setCtx({ category: categoryParam });
      }

      const redirectPath = redirectAfterLogin
        ? addFromAuthParam(redirectAfterLogin)
        : result.user.role === 'provider'
        ? addFromAuthParam(`/${lang}/provider/dashboard/profile`)
        : addFromAuthParam(`/${lang}/client/dashboard`);
      setTimeout(() => { window.location.href = redirectPath; }, 1000);
    } catch (err) {
      if (err instanceof ApiError) {
        if (err.code === 'EMAIL_ALREADY_EXISTS' || err.message.includes('already registered')) {
          // Auto-login if already registered. Handles the back button case.
          return handleLogin(true);
        } else if (err.code === 'VALIDATION_ERROR') {
          setState(s => ({ ...s, loading: false, error: err.message }));
        } else {
          setState(s => ({ ...s, loading: false, error: t(authDict, 'error_generic', 'An error occurred. Please try again.') }));
        }
      } else {
        setState(s => ({ ...s, loading: false, error: t(authDict, 'error_generic', 'An error occurred. Please try again.') }));
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

  const handleMagicLink = async () => {
    if (!magicEmail.trim()) return;
    setMagicStatus("loading");
    const result = await requestMagicLink(magicEmail.trim(), lang);
    if (result.success) {
      setMagicStatus("success");
    } else if (result.error === "RATE_LIMIT") {
      setMagicStatus("rate_limit");
    } else {
      setMagicStatus("error");
    }
  };

  function handleBack() {
    if (state.step === 'forgot') {
      setState(s => ({ ...s, step: 'login', error: null, forgotSuccess: false }));
    } else {
      setState(s => ({ ...s, step: 'initial', password: '', error: null }));
    }
  }

  function handleSocialClick(_provider: 'google' | 'facebook') {
    // TODO: integrate real OAuth
    setState(s => ({ ...s, socialToast: t(authDict, 'coming_soon', 'Coming soon') }));
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
      {t(authDict, 'back_btn', '← Back')}
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
              {claimToken ? (
                <>
                  <h1 className="text-[20px] font-bold text-[#171717] leading-tight">
                    {t(authDict, 'claim_headline', "Claim your profile on Nevumo")}
                  </h1>
                  <p className="text-sm text-gray-500 mt-1">
                    {t(authDict, 'claim_subtitle', "Register for free and manage your clients")}
                  </p>
                </>
              ) : state.intent === 'provider' ? (
                <>
                  <h1 className="text-[20px] font-bold text-[#171717] leading-tight">
                    {t(authDict, 'hero_title_provider', 'Start getting clients')}
                  </h1>
                </>
              ) : state.intent === 'client' ? (
                <>
                  <h1 className="text-[20px] font-bold text-[#171717] leading-tight">
                    {t(authDict, 'hero_title_client', 'Find a service in minutes')}
                  </h1>
                  <p className="text-sm text-gray-500 mt-1">{t(authDict, 'hero_subtitle_client', 'Free • No obligation')}</p>
                </>
              ) : (
                <>
                  <h1 className="text-[20px] font-bold text-[#171717] leading-tight">
                    {t(authDict, 'hero_title_neutral', 'Nevumo works for you!')}
                  </h1>
                  <p className="text-sm text-gray-500 mt-1">
                    {t(authDict, 'hero_subtitle_neutral_1', 'Looking for a service or offering one — it works both ways')}
                  </p>
                  <p className="text-sm text-orange-500 mt-0.5 font-semibold">
                    {t(authDict, 'hero_subtitle_neutral_2', 'No commission!')}
                  </p>
                </>
              )}
            </div>

            {/* Social buttons */}
            <p className={`text-center text-xs mb-2 transition-colors ${state.socialToast ? 'text-orange-500' : 'text-gray-500'}`}>
              {state.socialToast ?? t(authDict, 'quick_login_label', "Quick login without password")}
            </p>
            <div className="flex flex-col gap-[10px]">
              <button
                onClick={() => {
                  const currentIntent = localStorage.getItem('nevumo_intent');
                  const intent = redirectAfterLogin ? 'provider' : (currentIntent ?? '');
                  const category = searchParams.get('category') ?? '';
                  const city = citySlug ?? '';
                  if (redirectAfterLogin) {
                    localStorage.setItem('nevumo_redirect', redirectAfterLogin);
                  }
                  window.location.href = `${API_BASE}/api/v1/auth/google?lang=${lang}&intent=${intent}&category=${category}&city=${city}`;
                }}
                className="w-full flex items-center justify-center gap-2 py-2.5 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors"
              >
                <GoogleIcon />
                {t(authDict, 'google_btn', "Sign in with Google")}
              </button>
              <button
                onClick={() => handleSocialClick('facebook')}
                className="w-full flex items-center justify-center gap-2 py-2.5 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors"
                style={{ display: 'none' }}
              >
                <FacebookIcon />
                {t(authDict, 'facebook_btn', "Sign in with Facebook")}
              </button>
            </div>

            {/* Divider */}
            <div className="flex items-center gap-3 my-5">
              <div className="flex-1 h-px bg-gray-200" />
              <span className="text-xs text-gray-400">{t(authDict, 'or_with_email', "or with email")}</span>
              <div className="flex-1 h-px bg-gray-200" />
            </div>

            {/* Email input */}
            <input
              type="email"
              autoComplete="email"
              autoFocus
              placeholder="name@email.com"
              aria-label="Email address"
              value={state.email}
              onChange={e => handleEmailChange(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter') handleCheckEmail(); }}
              className="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400"
            />

            {/* Продължи button */}
            {primaryBtn(
              !isEmailValid || state.loading,
              state.loading,
              claimToken ? t(authDict, 'claim_cta_btn', "Claim profile") : t(authDict, 'continue_btn', "Continue"),
              t(authDict, 'checking_btn', 'Checking...'),
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
              <div className="relative mb-4">
                <input
                  type={state.showPassword ? 'text' : 'password'}
                  autoComplete="current-password"
                  placeholder={t(authDict, 'password_placeholder_login', 'Password')}
                  value={state.password}
                  onChange={e => handlePasswordChange(e.target.value)}
                  className={`w-full border rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400
                    ${state.error === 'invalid_password' ? 'border-red-400' : 'border-gray-300'}`}
                />
                <button
                  type="button"
                  onClick={() => setState(s => ({ ...s, showPassword: !s.showPassword }))}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
                  tabIndex={-1}
                >
                  {state.showPassword ? <EyeOffIcon /> : <EyeIcon />}
                </button>
                {state.error === 'invalid_password' && (
                  <p className="text-red-500 text-xs mt-0.5">{t(authDict, 'error_wrong_password', 'Wrong password')}</p>
                )}
              </div>

              <div className="flex justify-end mt-1.5">
                <button
                  type="button"
                  onClick={() => setState(s => ({ ...s, step: 'forgot', error: null }))}
                  className="text-xs text-gray-500 hover:text-gray-700 transition-colors"
                >
                  {t(authDict, 'forgot_password_link', 'Forgot password?')}
                </button>
              </div>

              {!showMagicLink ? (
                <button
                  type="button"
                  onClick={() => setShowMagicLink(true)}
                  className="mt-4 text-sm text-orange-500 hover:underline w-full text-center"
                >
                  {t(authDict, 'magic_link_no_password', "Don't have a password?")}
                </button>
              ) : (
                <div className="mt-4 border-t pt-4">
                  {magicStatus === "success" ? (
                    <div className="text-center space-y-2">
                      <p className="text-sm font-medium text-gray-800">
                        {t(authDict, 'magic_link_success', 'Login link sent to {email}').replace("{email}", magicEmail)}
                      </p>
                      <button
                        type="button"
                        onClick={() => { setShowMagicLink(false); setMagicStatus("idle"); setMagicEmail(""); }}
                        className="text-sm text-orange-500 hover:underline"
                      >
                        {t(authDict, 'magic_link_back_to_login', 'Back to login')}
                      </button>
                    </div>
                  ) : (
                    <div className="space-y-3">
                      <p className="text-sm font-semibold text-gray-800">
                        {t(authDict, 'magic_link_request_title', 'Send me a login link')}
                      </p>
                      <p className="text-xs text-gray-500">
                        {t(authDict, 'magic_link_request_description', 'We\'ll send you a link to sign in to your account')}
                      </p>
                      <input
                        type="email"
                        value={magicEmail}
                        onChange={(e) => setMagicEmail(e.target.value)}
                        placeholder="email@firma.pl"
                        className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400"
                      />
                      {magicStatus === "rate_limit" && (
                        <p className="text-xs text-red-500">{t(authDict, 'magic_link_rate_limit', 'Please wait before requesting another link')}</p>
                      )}
                      {magicStatus === "error" && (
                        <p className="text-xs text-red-500">{t(authDict, 'magic_link_error', 'Something went wrong. Please try again.')}</p>
                      )}
                      <div className="flex gap-2">
                        <button
                          type="button"
                          onClick={() => { setShowMagicLink(false); setMagicStatus("idle"); setMagicEmail(""); }}
                          className="text-sm text-gray-400 hover:underline"
                        >
                          {t(authDict, 'magic_link_back_to_login', 'Back to login')}
                        </button>
                        <button
                          type="button"
                          onClick={handleMagicLink}
                          disabled={magicStatus === "loading" || !magicEmail.trim()}
                          className="ml-auto bg-orange-500 text-white text-sm px-4 py-2 rounded-lg hover:bg-orange-600 disabled:opacity-50"
                        >
                          {magicStatus === "loading"
                            ? t(authDict, 'magic_link_send_button', 'Send link') + "..."
                            : t(authDict, 'magic_link_send_button', 'Send link')}
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              )}

              <button
                type="submit"
                disabled={state.password.length === 0 || state.loading}
                className={`w-full py-2.5 rounded-lg text-base font-semibold text-white transition-colors mt-4
                  ${state.password.length > 0 && !state.loading
                    ? 'bg-orange-500 hover:bg-orange-600 cursor-pointer'
                    : 'bg-gray-400 opacity-50 cursor-not-allowed'}`}
              >
                {state.loading ? t(authDict, 'logging_in_btn', 'Signing in...') : t(authDict, 'login_btn', 'Sign in')}
              </button>
            </form>

            {genericError}
          </>
        )}

        {/* ---- SELECT ROLE STEP ---- */}
        {state.step === 'select_role' && (
          <>
            {backBtn}
            {emailPill}
            <div className="mb-6 text-center">
              <h2 className="text-[18px] font-bold text-[#171717] mb-1">
                {t(authDict, 'select_role_title', 'How do you want to use Nevumo?')}
              </h2>
              <p className="text-sm text-gray-500">
                {t(authDict, 'select_role_subtitle', 'Choose your account type — you can always change it later')}
              </p>
            </div>
            <div className="flex flex-col gap-3">
              <button
                onClick={() => {
                  localStorage.setItem('nevumo_intent', 'client');
                  if (state._pendingGoogle) {
                    const category = searchParams.get('category') ?? '';
                    const city = citySlug ?? '';
                    if (redirectAfterLogin) {
                      localStorage.setItem('nevumo_redirect', redirectAfterLogin);
                    }
                    window.location.href = `${API_BASE}/api/v1/auth/google?lang=${lang}&intent=client&category=${category}&city=${city}`;
                  } else {
                    setState(s => ({ ...s, intent: 'client', step: 'register', _pendingGoogle: false }));
                  }
                }}
                className="w-full py-3 px-4 border-2 border-gray-200 hover:border-orange-400 rounded-xl text-left transition-colors"
              >
                <div className="font-semibold text-[15px] text-[#171717]">
                  {t(authDict, 'select_role_client_title', 'I need a service')}
                </div>
                <div className="text-sm text-gray-500 mt-0.5">
                  {t(authDict, 'select_role_client_subtitle', 'Find trusted professionals near you — fast and free')}
                </div>
              </button>
              <button
                onClick={() => {
                  localStorage.setItem('nevumo_intent', 'provider');
                  if (state._pendingGoogle) {
                    const category = searchParams.get('category') ?? '';
                    const city = citySlug ?? '';
                    if (redirectAfterLogin) {
                      localStorage.setItem('nevumo_redirect', redirectAfterLogin);
                    }
                    window.location.href = `${API_BASE}/api/v1/auth/google?lang=${lang}&intent=provider&category=${category}&city=${city}`;
                  } else {
                    setState(s => ({ ...s, intent: 'provider', step: 'register', _pendingGoogle: false }));
                  }
                }}
                className="w-full py-3 px-4 border-2 border-gray-200 hover:border-orange-400 rounded-xl text-left transition-colors"
              >
                <div className="font-semibold text-[15px] text-[#171717]">
                  {t(authDict, 'select_role_provider_title', 'I offer a service')}
                </div>
                <div className="text-sm text-gray-500 mt-0.5">
                  {t(authDict, 'select_role_provider_subtitle', 'Get clients, grow your business and earn more')}
                </div>
              </button>
            </div>
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
                  {t(authDict, 'claim_headline', "Claim your profile on Nevumo")}
                </h2>
                <p className="text-sm text-gray-500 mb-3">
                  {t(authDict, 'claim_subtitle', "Register for free and manage your clients")}
                </p>
              </>
            ) : (
              <p className="text-xs text-gray-600 mb-3">{t(authDict, 'register_subtitle', "We'll create an account automatically")}</p>
            )}

            <form action="" onSubmit={e => { e.preventDefault(); handleRegister(); }}>
              <input
                type="email"
                name="email"
                autoComplete="username"
                value={state.email}
                readOnly
                style={{ display: 'none' }}
                aria-hidden="true"
              />
              <div className="relative mb-4">
                <input
                  type={state.showPassword ? 'text' : 'password'}
                  autoComplete="new-password"
                  placeholder={t(authDict, 'password_placeholder_register', 'Click to generate a password')}
                  value={state.password}
                  onChange={e => handlePasswordChange(e.target.value)}
                  onInput={e => handlePasswordChange((e.target as HTMLInputElement).value)}
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
                disabled={!state.password || state.loading || !termsAccepted}
                className={`w-full py-2.5 rounded-lg text-base font-semibold text-white transition-colors mt-4
                  ${state.password && !state.loading && termsAccepted ? 'bg-orange-500 hover:bg-orange-600 cursor-pointer' : 'bg-gray-300 cursor-not-allowed'}`}
              >
                {state.loading ? t(authDict, 'registering_btn', 'Creating...') : claimToken ? t(authDict, 'claim_cta_btn', "Claim profile") : t(authDict, 'continue_btn', "Continue")}
              </button>
            </form>

            <div className="mt-3 space-y-2">
              <label className="flex items-start gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={termsAccepted}
                  onChange={(e) => setTermsAccepted(e.target.checked)}
                  className="mt-0.5 h-4 w-4 accent-orange-500 cursor-pointer flex-shrink-0"
                />
                <span className="text-xs text-gray-500">
                  {t(authDict, 'terms_accept_prefix', 'I accept the')}{' '}
                  <button type="button" className="text-orange-500 underline" onClick={() => { setLegalModalType('terms'); setLegalModalOpen(true); }}>
                    {t(authDict, 'terms_link', 'Terms of Service')}
                  </button>
                  {state.intent === 'provider' && (
                    <>
                      {', '}
                      <button type="button" className="text-orange-500 underline" onClick={() => { setLegalModalType('terms-provider'); setLegalModalOpen(true); }}>
                        {t(authDict, 'terms_provider_link', 'Provider Terms')}
                      </button>
                    </>
                  )}
                  {' '}{t(authDict, 'terms_and', 'and')}{' '}
                  <button type="button" className="text-orange-500 underline" onClick={() => { setLegalModalType('privacy'); setLegalModalOpen(true); }}>
                    {t(authDict, 'privacy_link', 'Privacy Policy')}
                  </button>
                </span>
              </label>
            </div>

            <LegalModal
              isOpen={legalModalOpen}
              onClose={() => setLegalModalOpen(false)}
              lang={lang}
              type={legalModalType}
              authDict={authDict}
              docDict={getDocDict()}
            />

            {state.registerSuccess && (
              <div className="bg-green-50 text-green-700 text-sm p-2.5 rounded-lg text-center mt-3">
                {t(authDict, 'register_success', 'Account created successfully')}
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
              <h2 className="text-[17px] font-bold text-[#171717]">{t(authDict, 'forgot_title', 'Forgot password')}</h2>
              <p className="text-sm text-gray-500 mt-1">{t(authDict, 'forgot_subtitle', "We'll send you a link for a new password")}</p>
            </div>

            {emailPill}

            <button
              onClick={handleForgot}
              disabled={state.loading || state.forgotSuccess}
              className={`w-full py-2.5 rounded-lg text-base font-semibold text-white bg-orange-500 transition-colors
                ${(state.loading || state.forgotSuccess) ? 'opacity-50 cursor-not-allowed' : 'hover:bg-orange-600'}`}
            >
              {state.forgotSuccess ? t(authDict, 'forgot_sent_btn', 'Sent') : state.loading ? t(authDict, 'sending_btn', 'Sending...') : t(authDict, 'forgot_send_btn', 'Send link')}
            </button>

            {state.forgotSuccess && (
              <div className="bg-green-50 text-green-700 text-sm p-2.5 rounded-lg text-center mt-3">
                {t(authDict, 'forgot_check_email', 'Check your email')}
              </div>
            )}

            {genericError}
          </>
        )}

      </div>
    </div>
  );
}
