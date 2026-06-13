'use client';

import { useState, useEffect } from 'react';
import { Bell, X } from 'lucide-react';
import { usePushNotifications } from '@/hooks/usePushNotifications';

interface PushNotificationBannerProps {
  lang: string;
  role: 'provider' | 'client';
}

export default function PushNotificationBanner({ lang, role }: PushNotificationBannerProps) {
  const { isSupported, isSubscribed, isLoading, permissionState, subscribe } = usePushNotifications();
  const [t, setT] = useState<Record<string, string>>({});
  const [tLoaded, setTLoaded] = useState(false);
  const [dismissed, setDismissed] = useState(false);

  // Check session dismiss on mount
  useEffect(() => {
    try {
      if (sessionStorage.getItem('push_banner_dismissed') === 'true') {
        setDismissed(true);
      }
    } catch {
      // sessionStorage access failed
    }
  }, []);

  // Fetch translations
  useEffect(() => {
    fetch(`/api/v1/translations/push_prompt?lang=${lang}`)
      .then((res) => res.json())
      .then((data) => {
        setT(data);
        setTLoaded(true);
      })
      .catch(() => {
        setTLoaded(true); // Use fallback values on error
      });
  }, [lang]);

  const handleDismiss = () => {
    try {
      sessionStorage.setItem('push_banner_dismissed', 'true');
    } catch {
      // sessionStorage access failed
    }
    setDismissed(true);
  };

  // Render condition
  if (
    !isSupported ||
    isSubscribed ||
    permissionState === 'denied' ||
    dismissed ||
    !tLoaded
  ) {
    return null;
  }

  const title = t['title'] || '🔔 Get notifications instantly!';
  const body = role === 'provider'
    ? (t['provider_body'] || "Don't miss new client requests while your phone is in your pocket.")
    : (t['client_body'] || "We'll notify you instantly when a provider responds to your request.");
  const ctaButton = t['cta_button'] || 'Enable notifications';
  const dismissButton = t['dismiss_button'] || 'Not now';

  return (
    <div className="w-full mb-4 px-4 py-3 rounded-lg border bg-amber-50 border-amber-200 flex items-start gap-3">
      <Bell className="text-amber-500 mt-0.5 shrink-0" size={20} />
      <div className="flex-1">
        <h3 className="font-semibold text-amber-900 text-sm">{title}</h3>
        <p className="text-amber-700 text-sm mt-0.5">{body}</p>
      </div>
      <div className="flex row gap-2 items-center">
        <button
          type="button"
          disabled={isLoading}
          onClick={subscribe}
          className="bg-orange-500 hover:bg-orange-600 text-white text-sm font-medium px-4 py-1.5 rounded-lg shrink-0 disabled:opacity-50"
        >
          {isLoading ? '...' : ctaButton}
        </button>
        <button
          type="button"
          onClick={handleDismiss}
          className="text-amber-400 hover:text-amber-600 shrink-0"
          aria-label={dismissButton}
        >
          <X size={16} />
        </button>
      </div>
    </div>
  );
}
