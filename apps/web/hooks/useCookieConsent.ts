'use client';

import { useState, useEffect, useCallback } from 'react';

export interface ConsentCategories {
  necessary: true;
  functional: boolean;
  analytics: boolean;
  marketing: boolean;
}

export interface ConsentData {
  v: 2;
  ts: number;
  categories: ConsentCategories;
  policy_version: string;
}

const POLICY_VERSION = '2026-05-01';
const COOKIE_NAME = 'nevumo_consent';
const COOKIE_MAX_AGE = 365 * 24 * 60 * 60; // 365 days in seconds
const RE_PROMPT_DAYS = 365;

export function useCookieConsent() {
  const [consentData, setConsentData] = useState<ConsentData | null>(null);
  const [showBanner, setShowBanner] = useState(false);
  const [mounted, setMounted] = useState(false);

  const updateGtag = (categories: ConsentCategories): void => {
    if (typeof window === 'undefined' || typeof (window as Window & { gtag?: Function }).gtag !== 'function') return;
    const gtag = (window as Window & { gtag: Function }).gtag;
    gtag('consent', 'update', {
      analytics_storage: categories.analytics ? 'granted' : 'denied',
      ad_storage: categories.marketing ? 'granted' : 'denied',
      ad_user_data: categories.marketing ? 'granted' : 'denied',
      ad_personalization: categories.marketing ? 'granted' : 'denied',
    });
  };

  const getCookie = (name: string): string | null => {
    if (typeof window === 'undefined') return null;
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()?.split(';').shift() || null;
    return null;
  };

  const setCookie = (name: string, value: string, maxAge: number) => {
    if (typeof window === 'undefined') return;
    document.cookie = `${name}=${value}; path=/; max-age=${maxAge}; SameSite=Lax`;
  };

  const deleteCookie = (name: string) => {
    if (typeof window === 'undefined') return;
    document.cookie = `${name}=; path=/; max-age=0; SameSite=Lax`;
  };

  useEffect(() => {
    setMounted(true);
    const cookie = getCookie(COOKIE_NAME);
    if (!cookie) {
      setShowBanner(true);
      return;
    }

    try {
      const data: ConsentData = JSON.parse(decodeURIComponent(cookie));
      const timeSinceConsent = Date.now() - data.ts;
      const twelveMonthsInMs = 365 * 24 * 60 * 60 * 1000;
      
      if (timeSinceConsent > twelveMonthsInMs || data.v !== 2) {
        deleteCookie(COOKIE_NAME);
        setShowBanner(true);
      } else {
        setConsentData(data);
        setShowBanner(false);
      }
    } catch (e) {
      console.error('Failed to parse cookie consent:', e);
      setShowBanner(true);
    }
  }, []);

  const saveConsent = useCallback(async (categories: ConsentCategories) => {
    const data: ConsentData = {
      v: 2,
      ts: Date.now(),
      categories,
      policy_version: POLICY_VERSION,
    };

    setConsentData(data);
    setCookie(COOKIE_NAME, encodeURIComponent(JSON.stringify(data)), COOKIE_MAX_AGE);
    setShowBanner(false);

    // POST to /api/v1/consent (fire-and-forget)
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('nevumo_auth_token');
      const apiBase = '';

      fetch(`${apiBase}/api/v1/consent`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({
          categories,
          policy_version: POLICY_VERSION,
        }),
      }).catch(err => {
        console.error('Failed to save consent to server:', err);
      });
    }

    updateGtag(categories);
  }, []);

  const acceptAll = useCallback(async () => {
    await saveConsent({
      necessary: true,
      functional: true,
      analytics: true,
      marketing: true,
    });
  }, [saveConsent]);

  const rejectAll = useCallback(async () => {
    await saveConsent({
      necessary: true,
      functional: false,
      analytics: false,
      marketing: false,
    });
  }, [saveConsent]);

  const openSettings = useCallback(() => {
    setShowBanner(true);
  }, []);

  return {
    consentData,
    showBanner: mounted && showBanner,
    saveConsent,
    acceptAll,
    rejectAll,
    openSettings,
  };
}
