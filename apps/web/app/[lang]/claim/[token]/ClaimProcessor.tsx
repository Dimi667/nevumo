'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { saveAuth } from '@/lib/auth-store';
import { getAuthToken } from '@/lib/auth-store';
import { API_BASE } from '@/lib/api';

interface ClaimProcessorProps {
  token: string;
  lang: string;
  source?: string;
  processingText: string;
  errorText: string;
  errorAlreadyClaimedText: string;
  errorUserHasProviderText: string;
  errorNetworkText: string;
  alreadyClaimedRedirectText: string;
}

type ErrorCode =
  | 'USER_ALREADY_HAS_PROVIDER'
  | 'ALREADY_CLAIMED'
  | 'NOT_FOUND'
  | 'NO_EMAIL'
  | 'NETWORK'
  | null;

export default function ClaimProcessor({
  token,
  lang,
  source,
  processingText,
  errorText,
  errorAlreadyClaimedText,
  errorUserHasProviderText,
  errorNetworkText,
  alreadyClaimedRedirectText,
}: ClaimProcessorProps) {
  const router = useRouter();
  const [errorCode, setErrorCode] = useState<ErrorCode>(null);

  useEffect(() => {
    const claimKey = `claim_${token}`;
    const sentToKey = `claim_sent_to_${token}`;

    // Check if verification code was already sent
    try {
      const claimStatus = sessionStorage.getItem(claimKey);
      if (claimStatus === 'sent') {
        // If already authenticated (has JWT), redirect to dashboard
        const existingToken = getAuthToken();
        if (existingToken) {
          router.push(`/${lang}/provider/dashboard`);
          return;
        }
        // Otherwise redirect to verify page with saved sent_to
        const savedSentTo = sessionStorage.getItem(sentToKey) ?? '';
        const verifyUrl = savedSentTo
          ? `/${lang}/claim/${token}/verify?sent_to=${encodeURIComponent(savedSentTo)}`
          : `/${lang}/claim/${token}/verify`;
        router.push(verifyUrl);
        return;
      }
      // Prevent duplicate requests during processing
      if (claimStatus === 'processing') return;
      sessionStorage.setItem(claimKey, 'processing');
    } catch {
      console.warn('[ClaimProcessor] sessionStorage access failed, continuing claim flow');
    }

    const processClaim = async () => {
      try {
        // Include JWT if already authenticated (returning provider with valid session)
        const existingToken = getAuthToken();
        const headers: Record<string, string> = {
          'Content-Type': 'application/json',
        };
        if (existingToken) {
          headers['Authorization'] = `Bearer ${existingToken}`;
        }

        const res = await fetch(
          `${API_BASE}/api/v1/providers/claim/${token}?lang=${lang}&source=${source ?? 'email'}`,
          { method: 'POST', headers }
        );

        const data = await res.json();

        // Handle 202 — verification code sent (banner flow)
        if (res.status === 202) {
          const sentTo = data?.sent_to ?? '';
          // Save sent_to for redirect after refresh/back
          try {
            sessionStorage.setItem(sentToKey, sentTo);
            sessionStorage.setItem(claimKey, 'sent');
          } catch {
            console.warn('[ClaimProcessor] sessionStorage write failed, continuing redirect');
          }
          const verifyUrl = sentTo
            ? `/${lang}/claim/${token}/verify?sent_to=${encodeURIComponent(sentTo)}`
            : `/${lang}/claim/${token}/verify`;
          router.push(verifyUrl);
          return;
        }

        if (!res.ok) {
          const code = data?.detail?.code as ErrorCode;
          setErrorCode(code ?? 'NETWORK');
          try {
            sessionStorage.removeItem(claimKey);
            sessionStorage.removeItem(sentToKey);
          } catch {
            console.warn('[ClaimProcessor] sessionStorage cleanup failed');
          }
          return;
        }

        // Save auth from response JWT
        saveAuth(data.jwt_token, data.user);

        // Mark as just claimed for welcome heading in wizard
        sessionStorage.setItem('nevumo_just_claimed', '1');
        sessionStorage.removeItem(claimKey);

        // Redirect logic:
        // - New claim → always wizard (profile page)
        // - Returning, onboarding complete → dashboard overview
        // - Returning, onboarding incomplete → wizard (profile page)
        if (data.is_returning && data.is_onboarding_complete) {
          router.push(`/${lang}/provider/dashboard`);
        } else {
          router.push(`/${lang}/provider/dashboard/profile?claimed=success`);
        }
      } catch {
        setErrorCode('NETWORK');
        sessionStorage.removeItem(claimKey);
      }
    };

    processClaim();
  }, [token, lang, source]);

  // ── Error states ─────────────────────────────────────────────────────
  if (errorCode === 'USER_ALREADY_HAS_PROVIDER') {
    return (
      <div className="mt-8 rounded-xl border border-orange-200 bg-orange-50 p-6 text-center">
        <p className="text-sm text-orange-700">{errorUserHasProviderText}</p>
      </div>
    );
  }

  if (errorCode === 'ALREADY_CLAIMED') {
    return (
      <div className="mt-8 rounded-xl border border-orange-200 bg-orange-50 p-6 text-center">
        <p className="text-sm text-orange-700 mb-4">{alreadyClaimedRedirectText}</p>
        <button
          onClick={() => router.push(`/${lang}/provider/dashboard`)}
          className="inline-block bg-orange-500 hover:bg-orange-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
        >
          Go to dashboard
        </button>
      </div>
    );
  }

  if (errorCode === 'NOT_FOUND' || errorCode === 'NO_EMAIL') {
    return (
      <div className="mt-8 rounded-xl border border-red-200 bg-red-50 p-6 text-center">
        <p className="text-sm text-red-700">{errorText}</p>
      </div>
    );
  }

  if (errorCode === 'NETWORK') {
    return (
      <div className="mt-8 rounded-xl border border-gray-200 bg-gray-50 p-6 text-center">
        <p className="text-sm text-gray-600">{errorNetworkText}</p>
      </div>
    );
  }

  // ── Loading state (default) ───────────────────────────────────────────
  return (
    <div className="mt-8 flex flex-col items-center gap-4 py-6">
      <div className="h-10 w-10 animate-spin rounded-full border-4 border-orange-200 border-t-orange-500" />
      <p className="text-sm text-gray-500">{processingText}</p>
    </div>
  );
}
