'use client';
import { useState, useEffect } from 'react';
import { usePathname } from 'next/navigation';
import GlobalFooter from '@/components/GlobalFooter';

interface Props { lang: string; }

export default function SmartGlobalFooter({ lang }: Props) {
  const [isInIframe, setIsInIframe] = useState(false);
  const pathname = usePathname();
  const isDashboard = pathname.includes('/dashboard');

  useEffect(() => {
    setIsInIframe(window.self !== window.top);
  }, []);

  if (isInIframe) return null;

  return <GlobalFooter lang={lang} minimal={isDashboard} />;
}
