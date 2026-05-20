'use client';
import dynamic from 'next/dynamic';

const AuthHeaderButton = dynamic(() => import('@/components/AuthHeaderButton'), { ssr: false });

export default function AuthHeaderButtonWrapper({ lang }: { lang: string }) {
  return <AuthHeaderButton lang={lang} />;
}
