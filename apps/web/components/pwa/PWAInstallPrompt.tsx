'use client';

import { useEffect, useState } from 'react';
import { usePWAInstall } from '@/hooks/usePWAInstall';
import { trackPageEvent } from '@/lib/tracking';

interface PWAInstallPromptProps {
  trigger: 'lead_submit' | 'onboarding_complete' | 'return_user';
  role: 'client' | 'provider';
  onClose: () => void;
  lang?: string;
}


export default function PWAInstallPrompt({
  trigger,
  role,
  onClose,
  lang = 'en',
}: PWAInstallPromptProps) {
  const { canInstall, isIOS, showPrompt, handleDismiss, handleInstalled } = usePWAInstall();
  const [hasTracked, setHasTracked] = useState(false);
  const [dict, setDict] = useState<Record<string, string>>({});
  const platform = isIOS ? 'ios' : 'android';

  // Fetch translations on mount
  useEffect(() => {
    fetch(`/api/v1/translations/pwa?lang=${lang}`)
      .then((res) => res.json())
      .then((data) => {
        if (data && typeof data === 'object') {
          setDict(data);
        }
      })
      .catch(() => {
        // Fallback to empty dict if fetch fails
        setDict({});
      });
  }, [lang]);

  // Translation helper
  const t = (key: string, fallback: string) => dict[key] || fallback;

  // Track when prompt is shown
  useEffect(() => {
    if (canInstall && !hasTracked) {
      trackPageEvent('pwa_prompt_shown', 'pwa', {
        trigger,
        role,
        platform,
      });
      setHasTracked(true);
    }
  }, [canInstall, hasTracked, trigger, role, platform]);

  // Listen for appinstalled event (Android only)
  useEffect(() => {
    if (isIOS) return;

    const handleAppInstalled = () => {
      trackPageEvent('pwa_installed', 'pwa', {
        trigger,
        role,
        platform: 'android',
      });
      handleInstalled();
      onClose();
    };

    window.addEventListener('appinstalled', handleAppInstalled);
    return () => window.removeEventListener('appinstalled', handleAppInstalled);
  }, [isIOS, trigger, role, handleInstalled, onClose]);

  if (!canInstall) {
    return null;
  }

  const handleInstallClick = () => {
    trackPageEvent('pwa_install_accepted', 'pwa', {
      trigger,
      role,
      platform,
    });

    if (isIOS) {
      // For iOS, just close after they read instructions
      handleInstalled();
      onClose();
    } else {
      // For Android, trigger the install prompt
      showPrompt();
    }
  };

  const handleDismissClick = () => {
    trackPageEvent('pwa_install_dismissed', 'pwa', {
      trigger,
      role,
      platform,
    });
    handleDismiss();
    onClose();
  };

  // iOS UI - Bottom sheet with instructions
  if (isIOS) {
    return (
      <div className="fixed inset-0 z-50 flex items-end justify-center bg-black/50">
        <div
          className="w-full rounded-t-2xl bg-white shadow-xl py-5 px-6 pb-8 max-h-[80vh] overflow-y-auto text-center"
        >
          <div className="mb-4 flex items-center justify-center relative">
            <h3 className="text-lg font-semibold text-gray-900">
              {t('install_title', 'Install Nevumo')}
            </h3>
            <button
              onClick={handleDismissClick}
              className="absolute right-0 text-gray-400 hover:text-gray-600"
              aria-label="Close"
            >
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </div>

          <p className="mb-6 text-sm text-gray-600">
            {role === 'client'
              ? t('client_subtitle', 'Track requests without opening a browser')
              : t('provider_subtitle', 'See new requests instantly')}
          </p>

          <div className="mb-6 space-y-3">
            <p className="text-sm text-gray-700">
              1. {t('ios_step1', 'Tap Share in the bottom toolbar')}{' '}
              <span className="inline-flex items-center gap-1 font-medium text-orange-600">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8" />
                  <polyline points="16 6 12 2 8 6" />
                  <line x1="12" y1="2" x2="12" y2="15" />
                </svg>
              </span>
            </p>
            <p className="text-sm text-gray-700">
              2. {t('ios_step2', 'Select "Add to Home Screen"')}
            </p>
          </div>

          <div className="sticky bottom-0 bg-white pt-3">
            <button
              onClick={handleDismissClick}
              className="w-full rounded-xl bg-orange-500 px-4 py-3 text-base font-semibold text-white transition hover:bg-orange-600"
            >
              {t('dismiss_button', 'Got it')}
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Android UI - Bottom banner
  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 border-t border-gray-200 bg-white p-4 shadow-lg">
      <div className="mx-auto flex max-w-lg items-center justify-between gap-4">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-900">
            {role === 'client'
              ? t('client_subtitle', 'Track requests without opening a browser')
              : t('provider_subtitle', 'See new requests instantly')}
          </p>
          <p className="text-xs text-gray-500">{t('install_title', 'Install Nevumo')}</p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleInstallClick}
            className="rounded-lg bg-orange-500 px-4 py-2 text-sm font-semibold text-white transition hover:bg-orange-600"
          >
            {t('dismiss_button', 'Got it')}
          </button>
          <button
            onClick={handleDismissClick}
            className="p-2 text-gray-400 hover:text-gray-600"
            aria-label="Dismiss"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}
