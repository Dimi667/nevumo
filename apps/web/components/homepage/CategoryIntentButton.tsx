'use client';

import { useRouter } from 'next/navigation';
import { setCtx } from '@/lib/ctx';

interface Props {
  href: string;
  category: string;
  className?: string;
  children: React.ReactNode;
}

export default function CategoryIntentButton({ href, category, className, children }: Props) {
  const router = useRouter();

  const handleClick = () => {
    setCtx({ category });
    localStorage.setItem('nevumo_intent', 'provider');
    router.push(href);
  };

  return (
    <button onClick={handleClick} className={className}>
      {children}
    </button>
  );
}
