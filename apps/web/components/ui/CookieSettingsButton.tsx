'use client';

import { ReactNode } from 'react';

interface CookieSettingsButtonProps {
  children: ReactNode;
  className?: string;
  onOpen?: () => void;
}

export function CookieSettingsButton({ children, className, onOpen }: CookieSettingsButtonProps) {
  const handleClick = () => {
    if (onOpen) {
      onOpen();
    }
  };

  return (
    <button onClick={handleClick} className={className}>
      {children}
    </button>
  );
}
