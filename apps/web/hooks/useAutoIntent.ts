'use client';
import { usePathname } from 'next/navigation';
import { useEffect } from 'react';
import { setStoredIntent } from '@/lib/intent';
import { PROVIDER_ROUTES } from '@/lib/intent-config';

export function useAutoIntent(): void {
  const pathname = usePathname();
  useEffect(() => {
    if (!pathname) return;
    // Skip homepage, auth and dashboard routes
    const segments = pathname.split('/').filter(Boolean);
    if (
      segments.length <= 1 ||
      pathname.includes('/auth') ||
      pathname.includes('/provider/dashboard') ||
      pathname.includes('/client/dashboard')
    ) return;
    // Check if provider route
    const isProvider = PROVIDER_ROUTES.some(route => pathname.includes(route));
    setStoredIntent(isProvider ? 'provider' : 'client');
  }, [pathname]);
}
