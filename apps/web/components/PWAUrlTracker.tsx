'use client';

import { usePWALastUrl } from '@/hooks/usePWALastUrl';

export default function PWAUrlTracker(): null {
  usePWALastUrl();
  return null;
}
