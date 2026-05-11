'use client';
import { usePathname } from 'next/navigation';
import GlobalFooter from '@/components/GlobalFooter';

interface Props { lang: string; }

export default function SmartGlobalFooter({ lang }: Props) {
  const pathname = usePathname();
  const isDashboard = pathname.includes('/dashboard');
  return <GlobalFooter lang={lang} minimal={isDashboard} />;
}
