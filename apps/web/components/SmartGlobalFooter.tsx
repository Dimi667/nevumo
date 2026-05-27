'use client';
import { useState, useEffect } from 'react';
import GlobalFooter from '@/components/GlobalFooter';

interface Props { lang: string; isEmbed?: boolean; }

export default function SmartGlobalFooter({ lang, isEmbed }: Props) {
  const [isInIframe, setIsInIframe] = useState(false);

  useEffect(() => {
    setIsInIframe(window.self !== window.top);
  }, []);

  if (isEmbed || isInIframe) return null;

  return <GlobalFooter lang={lang} />;
}
