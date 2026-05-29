'use client';

import { useSearchParams } from 'next/navigation';
import { Suspense } from 'react';
import GlobalHeader from '@/components/GlobalHeader';
import SmartGlobalFooter from '@/components/SmartGlobalFooter';

interface LayoutShellProps {
  lang: string;
  children: React.ReactNode;
}

function LayoutShellInner({ lang, children }: LayoutShellProps) {
  const searchParams = useSearchParams();
  const modal = searchParams.get('modal');
  const embed = searchParams.get('embed');

  return (
    <>
      {modal !== 'true' && embed !== '1' && <GlobalHeader lang={lang} />}
      {children}
      {modal !== 'true' && <SmartGlobalFooter lang={lang} isEmbed={embed === '1'} />}
    </>
  );
}

export default function LayoutShell({ lang, children }: LayoutShellProps) {
  return (
    <Suspense fallback={<>{children}</>}>
      <LayoutShellInner lang={lang}>{children}</LayoutShellInner>
    </Suspense>
  );
}
