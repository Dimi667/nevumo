import type { Metadata } from 'next';

export const baseIcons: Metadata['icons'] = {
  apple: [
    { url: '/apple-touch-icon.png' },
    { url: '/apple-touch-icon-76x76.png', sizes: '76x76' },
    { url: '/apple-touch-icon-120x120.png', sizes: '120x120' },
    { url: '/apple-touch-icon-152x152.png', sizes: '152x152' },
    { url: '/apple-touch-icon.png', sizes: '180x180' },
  ],
  icon: [
    { url: '/favicon-32x32.png', sizes: '32x32', type: 'image/png' },
  ],
};
