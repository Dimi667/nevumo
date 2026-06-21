'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { claimProfileAction } from './actions';

interface ClaimCTAWrapperProps {
  isAuthenticated: boolean;
  token: string;
  normalizedLang: string;
  claimT: Record<string, string>;
  authToken: string;
}

export default function ClaimCTAWrapper({ isAuthenticated, token, normalizedLang, claimT, authToken }: ClaimCTAWrapperProps) {
  const [isAutoClaiming, setIsAutoClaiming] = useState(false);

  useEffect(() => {
    const handleAutoClaimStart = () => setIsAutoClaiming(true);
    const handleAutoClaimEnd = () => setIsAutoClaiming(false);

    window.addEventListener('auto-claim-start', handleAutoClaimStart);
    window.addEventListener('auto-claim-end', handleAutoClaimEnd);

    return () => {
      window.removeEventListener('auto-claim-start', handleAutoClaimStart);
      window.removeEventListener('auto-claim-end', handleAutoClaimEnd);
    };
  }, []);

  // Hide CTAs during auto-claim
  if (isAutoClaiming) {
    return null;
  }

  return (
    <>
      {/* Primary CTA */}
      {isAuthenticated ? (
        <form action={claimProfileAction.bind(null, token, authToken, normalizedLang)}>
          <button
            type="submit"
            className="w-full bg-orange-500 hover:bg-orange-600 text-white font-semibold py-4 rounded-xl text-lg transition-colors"
          >
            {claimT['cta_claim'] ?? 'Claim your profile for free'}
          </button>
        </form>
      ) : (
        <Link
          href={`/${normalizedLang}/auth?role=provider&redirect=/${normalizedLang}/claim/${token}`}
          className="block w-full bg-orange-500 hover:bg-orange-600 text-white font-semibold py-4 rounded-xl text-lg transition-colors text-center"
        >
          {claimT['cta_register'] ?? 'Register and claim this profile for free'}
        </Link>
      )}
    </>
  );
}
