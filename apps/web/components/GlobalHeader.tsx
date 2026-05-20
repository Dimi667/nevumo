'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import AuthHeaderButtonWrapper from '@/components/AuthHeaderButtonWrapper';

interface GlobalHeaderProps {
  lang: string;
  hideAuthButton?: boolean;
}

export default function GlobalHeader({ lang, hideAuthButton }: GlobalHeaderProps) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    setVisible(window.self === window.top);
  }, []);

  if (!visible) return null;

  return (
    <header data-global-header className="flex items-center justify-between px-6 py-4 max-w-7xl mx-auto">
      <Link href={`/${lang}`}>
        <Image src="/Nevumo_logo.svg" alt="Nevumo" width={120} height={36} priority />
      </Link>
      {!hideAuthButton && <AuthHeaderButtonWrapper lang={lang} />}
    </header>
  );
}
