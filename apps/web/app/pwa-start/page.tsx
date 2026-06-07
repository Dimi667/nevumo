'use client';

import { useEffect } from 'react';
import { getAuthUser } from '@/lib/auth-store';
import { getCtx } from '@/lib/ctx';

const SUPPORTED_LANGUAGES = ['bg','cs','da','de','el','en','es','et','fi','fr','ga','hr','hu','is','it','lb','lt','lv','mk','mt','nl','no','pl','pt','pt-PT','ro','ru','sk','sl','sq','sr','sv','tr','uk'];

function getCookie(name: string): string | null {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop()?.split(';').shift() ?? null;
  }
  return null;
}

export default function PWAStartPage() {
  useEffect(() => {
    // Step 1: Determine language
    let lang = 'en';
    let redirectUrl: string | null = null;

    const lastUrl = localStorage.getItem('nevumo_last_url');
    if (lastUrl) {
      const segments = lastUrl.split('/').filter(Boolean);
      if (segments.length >= 1 && segments[0] && SUPPORTED_LANGUAGES.includes(segments[0])) {
        lang = segments[0];
        redirectUrl = lastUrl;
      }
    }

    // Fallback: check cookie for nevumo_pwa_ctx (PWA iOS localStorage isolation)
    if (!redirectUrl) {
      const pwaCtx = getCookie('nevumo_pwa_ctx');
      if (pwaCtx && pwaCtx.startsWith('/')) {
        const segments = pwaCtx.split('/').filter(Boolean);
        if (segments.length >= 1 && segments.length <= 4) {
          if (segments[0] && SUPPORTED_LANGUAGES.includes(segments[0])) {
            lang = segments[0];
            redirectUrl = pwaCtx;
          }
        }
      }
    }

    // Fallback: check cookie for lang
    if (lang === 'en') {
      const langCookie = getCookie('lang');
      if (langCookie && SUPPORTED_LANGUAGES.includes(langCookie)) {
        lang = langCookie;
      }
    }

    // Fallback: navigator.language
    if (lang === 'en') {
      const browserLang = navigator.language.split('-')[0];
      if (browserLang && SUPPORTED_LANGUAGES.includes(browserLang)) {
        lang = browserLang;
      }
    }

    // Step 2: Determine redirect
    const user = getAuthUser();

    if (user?.role === 'provider') {
      window.location.replace(`/${lang}/provider/dashboard`);
    } else if (user?.role === 'client') {
      const ctx = getCtx();
      if (ctx?.city) {
        window.location.replace(`/${lang}/${ctx.city}`);
      } else {
        window.location.replace(`/${lang}`);
      }
    } else {
      // No user
      if (redirectUrl) {
        window.location.replace(redirectUrl);
      } else {
        window.location.replace(`/${lang}`);
      }
    }
  }, []);

  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100vh',
      backgroundColor: '#ffffff'
    }}>
      <div style={{
        width: '40px',
        height: '40px',
        border: '4px solid #f3f3f3',
        borderTop: '4px solid #f97316',
        borderRadius: '50%',
        animation: 'spin 1s linear infinite'
      }} />
      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}
