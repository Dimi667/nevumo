'use client';

import React, { useEffect, useRef, useState } from 'react';

interface MobileStickyCTAProps {
  children: React.ReactNode;
}

export default function MobileStickyCTA({ children }: MobileStickyCTAProps) {
  const [isMounted, setIsMounted] = useState(false);
  const [transform, setTransform] = useState('translateY(0)');
  const mobileRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setIsMounted(true);

    const secondCTA = document.getElementById('second-cta');
    if (!secondCTA || !mobileRef.current) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          setTransform(entry.isIntersecting ? 'translateY(100%)' : 'translateY(0)');
        });
      },
      { threshold: 0.1 }
    );

    observer.observe(secondCTA);

    return () => {
      observer.disconnect();
    };
  }, []);

  return (
    <div
      ref={mobileRef}
      className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-4 z-50 transition-transform duration-300"
      style={{ transform }}
    >
      {children}
    </div>
  );
}
