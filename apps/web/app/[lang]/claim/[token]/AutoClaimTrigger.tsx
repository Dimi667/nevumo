'use client';

import { useEffect, useRef, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useTranslation } from '@/lib/use-translation';
import { API_BASE } from '@/lib/api';

interface AutoClaimTriggerProps {
  token: string;
  isAuthenticated: boolean;
  isClaimed: boolean;
  lang: string;
}

type AutoClaimState = 'idle' | 'loading' | 'success' | 'error';

export default function AutoClaimTrigger({ token, isAuthenticated, isClaimed, lang }: AutoClaimTriggerProps) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { t, dict: claimT, isLoading: isDictLoading } = useTranslation('claim', lang);
  const [state, setState] = useState<AutoClaimState>('idle');
  const [errorCode, setErrorCode] = useState<string | null>(null);
  const hasTriggered = useRef(false);

  useEffect(() => {
    // Only trigger if:
    // - Authenticated
    // - URL contains ?from=auth or &from=auth
    // - Not already claimed
    // - Haven't triggered before (idempotency)
    // - Dictionary is loaded
    if (
      isAuthenticated &&
      !isClaimed &&
      !hasTriggered.current &&
      !isDictLoading
    ) {
      const fromAuth = searchParams.get('from') === 'auth';
      
      if (fromAuth) {
        hasTriggered.current = true;
        performAutoClaim();
      }
    }
  }, [isAuthenticated, isClaimed, isDictLoading, searchParams]);

  async function performAutoClaim() {
    setState('loading');
    setErrorCode(null);
    window.dispatchEvent(new CustomEvent('auto-claim-start'));

    try {
      // Get auth token from cookie
      const cookies = document.cookie.split(';').reduce((acc, cookie) => {
        const parts = cookie.trim().split('=');
        if (parts.length >= 2) {
          const key = parts[0] || '';
          const value = parts.slice(1).join('=');
          if (key) {
            acc[key] = value;
          }
        }
        return acc;
      }, {} as Record<string, string>);
      
      const authToken = cookies['nevumo_auth_token'];
      
      if (!authToken) {
        setErrorCode('auth_expired');
        setState('error');
        return;
      }

      const response = await fetch(`${API_BASE}/api/v1/providers/claim/${token}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authToken}`,
        },
      });

      if (!response.ok) {
        if (response.status === 401) {
          setErrorCode('auth_expired');
        } else if (response.status === 422) {
          const errorData = await response.json().catch(() => ({}));
          if (errorData?.detail === 'cannot_verify_ownership') {
            window.location.href = `/${lang}/claim/${token}?error=ownership_blocked`;
            return;
          }
          setErrorCode('network');
        } else {
          const errorData = await response.json().catch(() => ({}));
          const code = errorData?.detail?.code || '';
          
          if (code === 'ALREADY_CLAIMED') {
            setErrorCode('already_claimed');
          } else if (code === 'USER_ALREADY_HAS_PROVIDER') {
            setErrorCode('user_has_provider');
          } else if (response.status === 404) {
            setErrorCode('not_found');
          } else {
            setErrorCode('network');
          }
        }
        setState('error');
        window.dispatchEvent(new CustomEvent('auto-claim-end'));
        return;
      }

      // Check for pending_verification (202 status)
      if (response.status === 202) {
        const data = await response.json().catch(() => ({}));
        if (data?.status === 'pending_verification') {
          window.location.href = `/${lang}/claim/${token}/verify`;
          return;
        }
      }

      // Success
      setState('success');
      window.dispatchEvent(new CustomEvent('auto-claim-end'));
      // Redirect to dashboard with claimed=success
      router.push(`/${lang}/provider/dashboard/profile?claimed=success`);
    } catch (error) {
      setErrorCode('network');
      setState('error');
      window.dispatchEvent(new CustomEvent('auto-claim-end'));
    }
  }

  function handleRetry() {
    performAutoClaim();
  }

  // Idle state - render nothing
  if (state === 'idle') {
    return null;
  }

  // Loading state
  if (state === 'loading') {
    return (
      <div className="flex items-center justify-center gap-3 py-4">
        <div className="w-5 h-5 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
        <span className="text-sm text-gray-600">
          {t('auto_claim_loading', 'Claiming your profile...')}
        </span>
      </div>
    );
  }

  // Error state
  if (state === 'error') {
    return (
      <div className="rounded-xl border border-orange-200 bg-orange-50 p-4 mb-6">
        {errorCode === 'already_claimed' && (
          <p className="text-sm text-orange-800">
            {t('auto_claim_error_already_claimed', 'This profile has already been claimed.')}
          </p>
        )}
        
        {errorCode === 'user_has_provider' && (
          <div className="space-y-3">
            <p className="text-sm text-orange-800">
              {t('auto_claim_error_user_has_provider', 'You already have an active profile on Nevumo.')}
            </p>
            <a
              href={`/${lang}/provider/dashboard`}
              className="inline-block rounded-lg bg-orange-500 px-4 py-2 text-sm font-semibold text-white hover:bg-orange-600"
            >
              {t('auto_claim_error_user_has_provider_cta', 'Go to my dashboard')}
            </a>
          </div>
        )}
        
        {errorCode === 'auth_expired' && (
          <div className="space-y-3">
            <p className="text-sm text-orange-800">
              {t('auto_claim_error_auth_expired', 'Your session has expired. Log in again.')}
            </p>
            <a
              href={`/${lang}/auth?redirect=/${lang}/claim/${token}`}
              className="inline-block rounded-lg bg-orange-500 px-4 py-2 text-sm font-semibold text-white hover:bg-orange-600"
            >
              {t('auto_claim_error_auth_expired_cta', 'Log in again')}
            </a>
          </div>
        )}
        
        {errorCode === 'network' && (
          <div className="space-y-3">
            <p className="text-sm text-orange-800">
              {t('auto_claim_error_network', 'Network error. Please check your connection.')}
            </p>
            <button
              onClick={handleRetry}
              className="inline-block rounded-lg bg-orange-500 px-4 py-2 text-sm font-semibold text-white hover:bg-orange-600"
            >
              {t('auto_claim_retry', 'Try again')}
            </button>
          </div>
        )}
        
        {errorCode === 'not_found' && (
          <p className="text-sm text-orange-800">
            {t('auto_claim_error_generic', 'This invitation is no longer valid.')}
          </p>
        )}
        
        {!errorCode && (
          <div className="space-y-3">
            <p className="text-sm text-orange-800">
              {t('auto_claim_error_generic', 'Something went wrong. Please try again.')}
            </p>
            <button
              onClick={handleRetry}
              className="inline-block rounded-lg bg-orange-500 px-4 py-2 text-sm font-semibold text-white hover:bg-orange-600"
            >
              {t('auto_claim_retry', 'Try again')}
            </button>
          </div>
        )}
      </div>
    );
  }

  // Success state - redirect is handled, but render nothing while redirecting
  if (state === 'success') {
    return null;
  }

  return null;
}
