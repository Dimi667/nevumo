'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { usePathname } from 'next/navigation';
import AuthHeaderButtonWrapper from '@/components/AuthHeaderButtonWrapper';
import { isDashboardPath } from '@/lib/dashboard-path';

interface GlobalHeaderProps {
  lang: string;
  hideAuthButton?: boolean;
}

export default function GlobalHeader({ lang, hideAuthButton }: GlobalHeaderProps) {
  const [visible, setVisible] = useState(false);
  const [forceUpdate, setForceUpdate] = useState(0);
  const pathname = usePathname();
  const isDashboard = isDashboardPath(pathname);

  useEffect(() => {
    setVisible(window.self === window.top);
  }, []);

  useEffect(() => {
    setForceUpdate(prev => prev + 1);
  }, [pathname]);

  if (!visible) return null;
  if (isDashboard) return null;

  return (
    <header key={forceUpdate} data-global-header className="flex items-center justify-between px-6 py-4 max-w-7xl mx-auto">
      <Link href={`/${lang}`}>
        <Image src="/Nevumo_logo.svg" alt="Nevumo" width={120} height={36} priority />
      </Link>
      {!hideAuthButton && <AuthHeaderButtonWrapper lang={lang} />}
    </header>
  );
}
