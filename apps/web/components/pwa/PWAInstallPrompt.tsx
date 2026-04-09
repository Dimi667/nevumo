'use client';

import { useEffect, useState } from 'react';
import { usePWAInstall } from '@/hooks/usePWAInstall';
import { trackPageEvent } from '@/lib/tracking';

interface PWAInstallPromptProps {
  trigger: 'lead_submit' | 'onboarding_complete' | 'return_user';
  role: 'client' | 'provider';
  onClose: () => void;
}

const COPY_TEXT = {
  client: 'Следи заявките без да отваряш браузър',
  provider: 'Виж нови заявки веднага',
};

export default function PWAInstallPrompt({
  trigger,
  role,
  onClose,
}: PWAInstallPromptProps) {
  const { canInstall, isIOS, showPrompt, handleDismiss, handleInstalled } = usePWAInstall();
  const [hasTracked, setHasTracked] = useState(false);
  const platform = isIOS ? 'ios' : 'android';

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
        <div className="w-full max-w-md rounded-t-2xl bg-white p-6 shadow-xl">
          <div className="mb-4 flex items-center justify-between">
            <h3 className="text-lg font-semibold text-gray-900">
              Инсталирай Nevumo
            </h3>
            <button
              onClick={handleDismissClick}
              className="text-gray-400 hover:text-gray-600"
              aria-label="Close"
            >
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </div>

          <p className="mb-6 text-sm text-gray-600">{COPY_TEXT[role]}</p>

          <div className="mb-6 space-y-3">
            <p className="text-sm text-gray-700">
              1. Натисни{' '}
              <span className="inline-flex items-center gap-1 font-medium text-orange-600">
                Share
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8" />
                  <polyline points="16 6 12 2 8 6" />
                  <line x1="12" y1="2" x2="12" y2="15" />
                </svg>
              </span>{' '}
              в долната лента на браузъра
            </p>
            <p className="text-sm text-gray-700">
              2. Избери &quot;Add to Home Screen&quot;
            </p>
          </div>

          <button
            onClick={handleInstallClick}
            className="w-full rounded-xl bg-orange-500 px-4 py-3 text-base font-semibold text-white transition hover:bg-orange-600"
          >
            Разбрах
          </button>
        </div>
      </div>
    );
  }

  // Android UI - Bottom banner
  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 border-t border-gray-200 bg-white p-4 shadow-lg">
      <div className="mx-auto flex max-w-lg items-center justify-between gap-4">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-900">{COPY_TEXT[role]}</p>
          <p className="text-xs text-gray-500">Инсталирай приложението за по-бърз достъп</p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleInstallClick}
            className="rounded-lg bg-orange-500 px-4 py-2 text-sm font-semibold text-white transition hover:bg-orange-600"
          >
            Инсталирай
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
