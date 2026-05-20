'use client';

import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import Image from "next/image";
const API_BASE = '';
import { saveAuth } from "@/lib/auth-store";
import LegalModal from '@/components/auth/LegalModal';

interface OAuthTermsClientProps {
  lang: string;
  authDict: Record<string, string>;
}

export default function OAuthTermsClient({ lang, authDict }: OAuthTermsClientProps) {
  const t = (dict: Record<string, string>, key: string, fallback: string): string => dict[key] ?? fallback;
  const searchParams = useSearchParams();
  
  const email = searchParams.get('email') || '';
  const name = searchParams.get('name') || '';
  const oauth_id = searchParams.get('oauth_id') || '';
  const rawIntent = searchParams.get('intent');
  const [intent, setIntent] = useState<'client' | 'provider' | null>(
    rawIntent === 'client' || rawIntent === 'provider' ? rawIntent : null
  );
  const category = searchParams.get('category') || '';
  const city = searchParams.get('city') || '';
  
  const [termsAccepted, setTermsAccepted] = useState(false);
  const [legalModalOpen, setLegalModalOpen] = useState(false);
  const [legalModalType, setLegalModalType] = useState<'terms' | 'terms-provider' | 'privacy'>('terms');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Redirect if missing required params
  useEffect(() => {
    if (!email || !oauth_id) {
      window.location.href = `/${lang}/auth`;
    }
  }, [email, oauth_id, lang]);

  async function handleContinue() {
    if (loading || !termsAccepted) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const res = await fetch(`${API_BASE}/api/v1/auth/google/complete`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          name,
          oauth_id,
          lang,
          intent,
        }),
      });

      if (!res.ok) {
        throw new Error('Failed to complete OAuth');
      }

      const result = await res.json();
      saveAuth(result.data.token, result.data.user);
      if (city) localStorage.setItem('nevumo_selected_city', city);
      if (category) localStorage.setItem('nevumo_selected_category', category);
      window.location.href = intent === 'provider' ? `/${lang}/provider/dashboard` : `/${lang}/client/dashboard`;
    } catch {
      setError(t(authDict, 'oauth_error_generic', 'An error occurred. Please try again.'));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-[#f9f9f9] flex flex-col items-center justify-start pt-16 px-4 pb-16">
      <div className="w-full max-w-[400px] bg-white rounded-xl border border-gray-200 p-8">
        {!intent && (
          <div className="mb-6">
            <h2 className="text-[18px] font-bold text-[#171717] mb-1 text-center">
              {t(authDict, 'select_role_title', 'How do you want to use Nevumo?')}
            </h2>
            <p className="text-sm text-gray-500 text-center mb-4">
              {t(authDict, 'select_role_subtitle', 'Choose your account type — you can always change it later')}
            </p>
            <div className="flex flex-col gap-3">
              <button
                onClick={() => { localStorage.setItem('nevumo_intent', 'client'); setIntent('client'); }}
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
                onClick={() => { localStorage.setItem('nevumo_intent', 'provider'); setIntent('provider'); }}
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
          </div>
        )}
        {intent && (
          <>
        {/* Nevumo Logo */}
        <div className="flex justify-center mb-6">
          <Image src="/Nevumo_logo.svg" alt="Nevumo" width={120} height={36} priority />
        </div>

        {/* Title */}
        <div className="text-center mb-6">
          <h1 className="text-[20px] font-bold text-[#171717] leading-tight mb-2">
            {t(authDict, 'oauth_terms_title', 'Before you continue')}
          </h1>
          <p className="text-sm text-gray-500">
            {t(authDict, 'oauth_terms_subtitle', 'Please read and accept the terms and conditions')}
          </p>
        </div>

        {/* Terms Checkbox */}
        <div className="mt-4 space-y-2">
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
              {intent === 'provider' && (
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

        {/* Continue Button */}
        <button
          onClick={handleContinue}
          disabled={!termsAccepted || loading}
          className={`w-full py-2.5 rounded-lg text-base font-semibold text-white transition-colors mt-6
            ${termsAccepted && !loading ? 'bg-orange-500 hover:bg-orange-600 cursor-pointer' : 'bg-gray-300 cursor-not-allowed'}`}
        >
          {loading ? 'Processing...' : t(authDict, 'oauth_continue_google', 'Continue with Google')}
        </button>

        {/* Error Message */}
        {error && (
          <p className="text-red-500 text-xs mt-3 text-center">
            {error}
          </p>
        )}

        {/* Legal Modal */}
        <LegalModal
          isOpen={legalModalOpen}
          onClose={() => setLegalModalOpen(false)}
          lang={lang}
          type={legalModalType}
          authDict={authDict}
        />
          </>
        )}
      </div>
    </div>
  );
}
