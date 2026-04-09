'use client';

import { useState, useEffect, useCallback } from 'react';

// Type definition for BeforeInstallPromptEvent (not in standard DOM types)
interface BeforeInstallPromptEvent extends Event {
  readonly platforms: string[];
  readonly userChoice: Promise<{ outcome: 'accepted' | 'dismissed'; platform: string }>;
  prompt(): Promise<void>;
}

// Augment WindowEventMap for TypeScript
declare global {
  interface WindowEventMap {
    beforeinstallprompt: BeforeInstallPromptEvent;
    appinstalled: Event;
  }
}

const STORAGE_KEYS = {
  INSTALLED: 'pwa_installed',
  DISMISS_COUNT: 'pwa_prompt_dismissed_count',
};

interface UsePWAInstallReturn {
  canInstall: boolean;
  isIOS: boolean;
  showPrompt: () => void;
  handleDismiss: () => void;
  handleInstalled: () => void;
}

export function usePWAInstall(): UsePWAInstallReturn {
  const [canInstall, setCanInstall] = useState(false);
  const [isIOS, setIsIOS] = useState(false);
  const [deferredPrompt, setDeferredPrompt] = useState<BeforeInstallPromptEvent | null>(null);

  useEffect(() => {
    // Проверка дали е iOS
    const userAgent = window.navigator.userAgent.toLowerCase();
    const isIOSDevice = /iphone|ipad|ipod/.test(userAgent) && !(/crios/.test(userAgent));
    setIsIOS(isIOSDevice);

    // Проверка на localStorage
    const isInstalled = localStorage.getItem(STORAGE_KEYS.INSTALLED) === 'true';
    const dismissCount = parseInt(localStorage.getItem(STORAGE_KEYS.DISMISS_COUNT) || '0', 10);

    if (isInstalled || dismissCount >= 2) {
      setCanInstall(false);
      return;
    }

    // Android: слушаме beforeinstallprompt
    const handleBeforeInstallPrompt = (e: BeforeInstallPromptEvent) => {
      e.preventDefault();
      setDeferredPrompt(e);
      setCanInstall(true);
    };

    // Слушаме за инсталация
    const handleAppInstalled = () => {
      localStorage.setItem(STORAGE_KEYS.INSTALLED, 'true');
      setCanInstall(false);
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    window.addEventListener('appinstalled', handleAppInstalled);

    // iOS: показваме prompt ако не е инсталирано
    if (isIOSDevice && !window.matchMedia('(display-mode: standalone)').matches) {
      setCanInstall(true);
    }

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
      window.removeEventListener('appinstalled', handleAppInstalled);
    };
  }, []);

  const showPrompt = useCallback(async () => {
    if (!deferredPrompt) return;

    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;

    if (outcome === 'accepted') {
      localStorage.setItem(STORAGE_KEYS.INSTALLED, 'true');
      setCanInstall(false);
    }

    setDeferredPrompt(null);
  }, [deferredPrompt]);

  const handleDismiss = useCallback(() => {
    const currentCount = parseInt(localStorage.getItem(STORAGE_KEYS.DISMISS_COUNT) || '0', 10);
    localStorage.setItem(STORAGE_KEYS.DISMISS_COUNT, String(currentCount + 1));

    if (currentCount + 1 >= 2) {
      setCanInstall(false);
    }
  }, []);

  const handleInstalled = useCallback(() => {
    localStorage.setItem(STORAGE_KEYS.INSTALLED, 'true');
    setCanInstall(false);
  }, []);

  return {
    canInstall,
    isIOS,
    showPrompt,
    handleDismiss,
    handleInstalled,
  };
}
