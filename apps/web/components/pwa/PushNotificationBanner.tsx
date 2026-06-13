'use client';

import { useState, useEffect } from 'react';
import { Bell, BellOff, Smartphone } from 'lucide-react';
import { usePushNotifications } from '@/hooks/usePushNotifications';

interface PushNotificationBannerProps {
  lang: string;
  role: 'provider' | 'client';
}

export default function PushNotificationBanner({ lang, role }: PushNotificationBannerProps) {
  const { isSupported, isSubscribed, isLoading, permissionState, subscribe } = usePushNotifications();
  const [pwaT, setPwaT] = useState<Record<string, string>>({});
  const [pushPromptT, setPushPromptT] = useState<Record<string, string>>({});
  const [settingsT, setSettingsT] = useState<Record<string, string>>({});
  const [translationsLoaded, setTranslationsLoaded] = useState(false);

  // iOS detection
  const isIOS = typeof navigator !== 'undefined' && /iPad|iPhone|iPod/.test(navigator.userAgent);
  const isStandalone = typeof window !== 'undefined' && Boolean((window.navigator as any).standalone);
  const isIOSWithoutPWA = isIOS && !isStandalone;

  // Fetch translations from 3 endpoints
  useEffect(() => {
    Promise.all([
      fetch(`/api/v1/translations/pwa?lang=${lang}`).then((res) => res.json()),
      fetch(`/api/v1/translations/push_prompt?lang=${lang}`).then((res) => res.json()),
      fetch(`/api/v1/translations/settings?lang=${lang}`).then((res) => res.json()),
    ])
      .then(([pwaData, pushPromptData, settingsData]) => {
        setPwaT(pwaData);
        setPushPromptT(pushPromptData);
        setSettingsT(settingsData);
        setTranslationsLoaded(true);
      })
      .catch(() => {
        setTranslationsLoaded(true);
      });
  }, [lang]);

  // Return null while translations are loading
  if (!translationsLoaded) {
    return null;
  }

  // STATE 1: Already subscribed
  if (isSubscribed) {
    return null;
  }

  // STATE 2: iOS without PWA
  if (isIOSWithoutPWA) {
    const text = role === 'provider'
      ? pwaT['install_for_notifications_provider'] || 'Install the app to receive notifications for new requests'
      : pwaT['install_for_notifications_client'] || 'Install the app to receive notifications about the status of your requests';

    return (
      <div className="w-full mb-4 px-4 py-3 rounded-lg border bg-blue-50 border-blue-200 flex items-start gap-3">
        <Smartphone className="text-blue-500 mt-0.5 shrink-0" size={20} />
        <div className="flex-1 flex flex-col gap-0.5">
          <p className="text-sm text-blue-800">{text}</p>
        </div>
      </div>
    );
  }

  // STATE 3: Blocked
  if (isSupported && !isSubscribed && permissionState === 'denied') {
    const title = settingsT['push_blocked_title'] || 'Notifications are blocked';
    const body = settingsT['push_blocked_description'] || 'Notifications for nevumo.com are blocked in your browser. To enable them, go to your browser settings and allow notifications for this site.';

    return (
      <div className="w-full mb-4 px-4 py-3 rounded-lg border bg-amber-50 border-amber-200 flex items-start gap-3">
        <BellOff className="text-amber-500 mt-0.5 shrink-0" size={20} />
        <div className="flex-1 flex flex-col gap-0.5">
          <h3 className="text-sm font-semibold text-amber-900">{title}</h3>
          <p className="text-sm text-amber-700">{body}</p>
        </div>
      </div>
    );
  }

  // STATE 4: Enable notifications
  if (isSupported && !isSubscribed && permissionState !== 'denied') {
    const title = pushPromptT['title'] || '🔔 Get notifications instantly!';
    const body = role === 'provider'
      ? (pushPromptT['provider_body'] || "Don't miss new client requests while your phone is in your pocket.")
      : (pushPromptT['client_body'] || "We'll notify you instantly when a provider responds to your request.");
    const ctaButton = pushPromptT['cta_button'] || 'Enable notifications';

    return (
      <div className="w-full mb-4 px-4 py-3 rounded-lg border bg-amber-50 border-amber-200 flex items-start gap-3">
        <Bell className="text-amber-500 mt-0.5 shrink-0" size={20} />
        <div className="flex-1 flex flex-col gap-0.5">
          <h3 className="text-sm font-semibold text-amber-900">{title}</h3>
          <p className="text-sm text-amber-700">{body}</p>
          <button
            type="button"
            disabled={isLoading}
            onClick={subscribe}
            className="mt-2 self-start bg-orange-500 hover:bg-orange-600 text-white text-sm font-medium px-4 py-1.5 rounded-lg disabled:opacity-50"
          >
            {isLoading ? '...' : ctaButton}
          </button>
        </div>
      </div>
    );
  }

  // No condition matched
  return null;
}
