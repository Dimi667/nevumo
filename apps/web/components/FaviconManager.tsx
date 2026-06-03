'use client';
import { useEffect } from 'react';
import { usePathname } from 'next/navigation';

export function FaviconManager() {
  const pathname = usePathname();

  useEffect(() => {
    const icons = [
      { rel: 'apple-touch-icon', href: '/apple-touch-icon.png' },
      { rel: 'apple-touch-icon', sizes: '76x76', href: '/apple-touch-icon-76x76.png' },
      { rel: 'apple-touch-icon', sizes: '120x120', href: '/apple-touch-icon-120x120.png' },
      { rel: 'apple-touch-icon', sizes: '152x152', href: '/apple-touch-icon-152x152.png' },
      { rel: 'apple-touch-icon', sizes: '180x180', href: '/apple-touch-icon.png' },
      { rel: 'icon', type: 'image/png', sizes: '32x32', href: '/favicon-32x32.png' },
    ];

    icons.forEach(({ rel, href, sizes, type }) => {
      const existing = document.querySelector(
        `link[rel="${rel}"]${sizes ? `[sizes="${sizes}"]` : ''}${type ? `[type="${type}"]` : ''}` 
      );
      if (!existing) {
        const link = document.createElement('link');
        link.rel = rel;
        link.href = href;
        if (sizes) link.setAttribute('sizes', sizes);
        if (type) link.setAttribute('type', type);
        document.head.appendChild(link);
      }
    });
  }, [pathname]);

  return null;
}
