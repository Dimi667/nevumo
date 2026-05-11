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
    const heroSection = document.getElementById('hero-section');
    const footer = document.querySelector('footer');
    if (!mobileRef.current) return;

    let heroSectionVisible = false;
    let footerVisible = false;

    const update = () => {
      if (footerVisible) {
        setTransform('translateY(0)');
      } else if (heroSectionVisible) {
        setTransform('translateY(100%)');
      } else {
        setTransform('translateY(0)');
      }
    };

    const ctaObserver = heroSection ? new IntersectionObserver(
      (entries) => {
        heroSectionVisible = entries[0]?.isIntersecting ?? false;
        update();
      },
      { threshold: 0.1 }
    ) : null;

    const footerObserver = footer ? new IntersectionObserver(
      (entries) => {
        footerVisible = entries[0]?.isIntersecting ?? false;
        update();
      },
      { threshold: 0.01 }
    ) : null;

    if (heroSection && ctaObserver) ctaObserver.observe(heroSection);
    if (footer && footerObserver) footerObserver.observe(footer);

    return () => {
      ctaObserver?.disconnect();
      footerObserver?.disconnect();
    };
  }, []);

  useEffect(() => {
    const btn = mobileRef.current;
    if (!btn) return;

    // Check if button is visible (mobile only)
    const isMobile = window.getComputedStyle(btn).display !== 'none';
    if (!isMobile) return;

    // Get button height and add padding to body
    const height = btn.offsetHeight;
    document.body.style.paddingBottom = `${height}px`;

    return () => {
      document.body.style.paddingBottom = '';
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
