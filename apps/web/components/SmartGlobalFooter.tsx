'use client';
import { useState, useEffect } from 'react';
import { usePathname } from 'next/navigation';
import GlobalFooter from '@/components/GlobalFooter';
import { isDashboardPath } from '@/lib/dashboard-path';

interface Props { lang: string; isEmbed?: boolean; }

export default function SmartGlobalFooter({ lang, isEmbed }: Props) {
  const pathname = usePathname();
  const [isInIframe, setIsInIframe] = useState(false);

  useEffect(() => {
    setIsInIframe(window.self !== window.top);
  }, []);

  if (isEmbed || isInIframe || isDashboardPath(pathname)) return null;

  return <GlobalFooter lang={lang} />;
}
