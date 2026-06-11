'use client';

import { useState, useEffect, useCallback } from 'react';
import { getAuthToken } from '@/lib/auth-store';

function urlBase64ToUint8Array(base64String: string): Uint8Array {
  const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);
  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

interface UsePushNotificationsReturn {
  isSupported: boolean;
  isSubscribed: boolean;
  isLoading: boolean;
  permissionState: NotificationPermission;
  subscribe: () => Promise<void>;
  unsubscribe: () => Promise<void>;
}

export function usePushNotifications(): UsePushNotificationsReturn {
  const [isSupported, setIsSupported] = useState(false);
  const [isSubscribed, setIsSubscribed] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [permissionState, setPermissionState] = useState<NotificationPermission>('default');

  useEffect(() => {
    const isIOS =
      typeof navigator !== 'undefined' &&
      /iPad|iPhone|iPod/.test(navigator.userAgent);

    const isIOSStandalone =
      typeof window !== 'undefined' &&
      Boolean((window.navigator as any).standalone);

    const supported =
      typeof navigator !== 'undefined' &&
      'serviceWorker' in navigator &&
      typeof window !== 'undefined' &&
      'PushManager' in window &&
      (!isIOS || isIOSStandalone);
    setIsSupported(supported);

    if (typeof Notification !== 'undefined') {
      setPermissionState(Notification.permission);
    }

    if (!supported) return;

    navigator.serviceWorker.ready.then((reg) => {
      reg.pushManager.getSubscription().then(async (sub) => {
        if (!sub) {
          setIsSubscribed(false)
          return
        }
        setIsSubscribed(true)
        // Auto-sync: if browser has subscription but user is now logged in,
        // silently send to backend so DB record is created for this user_id
        const token = getAuthToken()
        if (token) {
          try {
            const { endpoint, keys } = sub.toJSON() as {
              endpoint: string
              keys: { p256dh: string; auth: string }
            }
            await fetch('/api/v1/push/subscribe', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
              },
              credentials: 'include',
              body: JSON.stringify({
                endpoint,
                p256dh: keys.p256dh,
                auth: keys.auth,
              }),
            })
          } catch {
            // Silent — auto-sync is best-effort, not critical
          }
        }
      })
    });
  }, []);

  const subscribe = useCallback(async () => {
    setIsLoading(true);
    try {
      if (typeof Notification === 'undefined') {
        console.warn('[Push] Notification API not available');
        return;
      }
      const permission = await Notification.requestPermission();
      setPermissionState(permission);
      if (permission !== 'granted') {
        console.warn('[Push] Notification permission not granted:', permission);
        return;
      }

      const res = await fetch('/api/v1/push/vapid-public-key');
      const { public_key } = await res.json();

      const reg = await Promise.race([
        navigator.serviceWorker.ready,
        new Promise<never>((_, reject) =>
          setTimeout(() => reject(new Error('[Push] serviceWorker.ready timeout')), 10000)
        )
      ]);
      const subscription = await reg.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: urlBase64ToUint8Array(public_key) as unknown as ArrayBuffer,
      });

      const { endpoint, keys } = subscription.toJSON() as {
        endpoint: string;
        keys: { p256dh: string; auth: string };
      };

      const token = getAuthToken();
      if (!token) {
        console.log('[Push] No auth token — skipping subscribe, will retry after login');
        return;
      }
      await fetch('/api/v1/push/subscribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        },
        credentials: 'include',
        body: JSON.stringify({
          endpoint,
          p256dh: keys.p256dh,
          auth: keys.auth,
        }),
      });

      setIsSubscribed(true);
    } catch (err) {
      console.error('Push subscribe error:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const unsubscribe = useCallback(async () => {
    setIsLoading(true);
    try {
      const reg = await navigator.serviceWorker.ready;
      const subscription = await reg.pushManager.getSubscription();
      if (!subscription) return;

      const { endpoint, keys } = subscription.toJSON() as {
        endpoint: string;
        keys: { p256dh: string; auth: string };
      };

      const token = getAuthToken()
      await fetch('/api/v1/push/unsubscribe', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        },
        credentials: 'include',
        body: JSON.stringify({
          endpoint,
          p256dh: keys.p256dh,
          auth: keys.auth,
        }),
      });

      await subscription.unsubscribe();
      setIsSubscribed(false);
    } catch (err) {
      console.error('Push unsubscribe error:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { isSupported, isSubscribed, isLoading, permissionState, subscribe, unsubscribe };
}
