'use client';

import { useRouter } from 'next/navigation';
import { ReactNode } from 'react';

interface AuthIntentButtonProps {
  href: string;
  intent: 'provider' | 'client';
  children: ReactNode;
  className?: string;
}

export function AuthIntentButton({ href, intent, children, className }: AuthIntentButtonProps) {
  const router = useRouter();

  const handleClick = () => {
    localStorage.setItem('nevumo_intent', intent);
    router.push(href);
  };

  return (
    <button onClick={handleClick} className={className}>
      {children}
    </button>
  );
}
