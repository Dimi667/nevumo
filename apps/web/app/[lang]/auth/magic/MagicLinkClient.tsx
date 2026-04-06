'use client';
// TODO: i18n

import { useState, useEffect } from "react";
import { trackPageEvent } from "@/lib/tracking";
import { magicLinkAuth } from "@/lib/auth-api";
import { saveAuth } from "@/lib/auth-store";
import { ApiError } from "@/lib/api";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

type PageState = 'loading' | 'success' | 'error';

interface MagicState {
  page: PageState;
  loading: boolean;
  errorCode: string | null;
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

interface MagicLinkClientProps {
  lang: string;
  token: string;
}

export default function MagicLinkClient({ lang, token }: MagicLinkClientProps) {
  const [state, setState] = useState<MagicState>({
    page: 'loading',
    loading: false,
    errorCode: null,
  });

  // Process magic link on mount
  useEffect(() => {
    if (!token) {
      setState(s => ({ ...s, page: 'error', errorCode: 'TOKEN_INVALID' }));
      return;
    }

    setState(s => ({ ...s, loading: true }));
    
    magicLinkAuth(token).then(result => {
      saveAuth(result.token, result.user);
      trackPageEvent('magic_link_success', 'magic-link', {});
      setState(s => ({ ...s, loading: false, page: 'success' }));

      // Auto-redirect after 2 seconds
      setTimeout(() => {
        window.location.href = `/${lang}/client/dashboard`;
      }, 2000);
    }).catch(err => {
      if (err instanceof ApiError) {
        trackPageEvent('magic_link_error', 'magic-link', { error_code: err.code });
        setState(s => ({ ...s, loading: false, page: 'error', errorCode: err.code }));
      } else {
        trackPageEvent('magic_link_error', 'magic-link', { error_code: 'UNKNOWN' });
        setState(s => ({ ...s, loading: false, page: 'error', errorCode: 'UNKNOWN' }));
      }
    });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

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
      <div className="text-center">
        <p className="text-gray-500 text-sm py-4">Зареждане...</p>
      </div>
    );
  }

  if (state.page === 'success') {
    return card(
      <div className="bg-green-50 text-green-700 rounded-lg p-5 text-center">
        <p className="font-semibold text-base">Успешен вход</p>
        <p className="text-sm mt-1">Пренасочваме те...</p>
      </div>
    );
  }

  if (state.page === 'error') {
    const getErrorMessage = (code: string | null) => {
      switch (code) {
        case 'TOKEN_EXPIRED':
          return "Линкът е изтекъл. Моля изпратете ново запитване.";
        case 'TOKEN_USED':
          return "Линкът вече е използван. Моля влезте в профила си.";
        case 'TOKEN_INVALID':
          return "Невалиден линк. Моля изпратете ново запитване.";
        default:
          return "Нещо се обърка. Моля опитайте отново.";
      }
    };

    return card(
      <div className="text-center">
        <h1 className="text-[18px] font-bold text-[#171717] mb-4">
          Грешка
        </h1>
        <p className="text-sm text-gray-600 mb-6">
          {getErrorMessage(state.errorCode)}
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

  return card(
    <div className="text-center">
      <p className="text-gray-500 text-sm py-4">Зареждане...</p>
    </div>
  );
}
