'use client';

import { useEffect, useRef, useState } from 'react';
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
}

type ErrorCode =
  | 'USER_ALREADY_HAS_PROVIDER'
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
}: ClaimProcessorProps) {
  const router = useRouter();
  const hasTriggered = useRef(false);
  const [errorCode, setErrorCode] = useState<ErrorCode>(null);

  useEffect(() => {
    if (hasTriggered.current) return;
    hasTriggered.current = true;

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
          const verifyUrl = sentTo
            ? `/${lang}/claim/${token}/verify?sent_to=${encodeURIComponent(sentTo)}`
            : `/${lang}/claim/${token}/verify`;
          router.push(verifyUrl);
          return;
        }

        if (!res.ok) {
          const code = data?.detail?.code as ErrorCode;
          setErrorCode(code ?? 'NETWORK');
          return;
        }

        // Save auth from response JWT
        saveAuth(data.jwt_token, data.user);

        // Mark as just claimed for welcome heading in wizard
        sessionStorage.setItem('nevumo_just_claimed', '1');

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
