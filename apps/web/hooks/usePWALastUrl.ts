'use client';

import { usePathname } from 'next/navigation';
import { useEffect } from 'react';

const DIRTY_PATTERNS = ['/auth', '/dashboard', '/pwa-start', '/izberi-grad'];

export function usePWALastUrl(): void {
  const pathname = usePathname();

  useEffect(() => {
    // Check if pathname contains any dirty patterns
    const isDirty = DIRTY_PATTERNS.some(pattern => pathname.includes(pattern));
    if (isDirty) return;

    // Check if pathname has 1-4 segments
    const segments = pathname.split('/').filter(Boolean);
    if (segments.length < 1 || segments.length > 4) return;

    // Save to localStorage
    localStorage.setItem('nevumo_last_url', pathname);
  }, [pathname]);
}
