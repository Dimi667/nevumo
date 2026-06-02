import { ImageResponse } from 'next/og';

/**
 * SINGLE SOURCE OF TRUTH for the Nevumo brand mark.
 *
 * The brand mark is an orange (#f97316) rounded square with a white bold "N".
 * Edit the values below and every icon (favicon, apple-touch-icon and PWA
 * icons) updates everywhere automatically — including any new pages, since
 * these are emitted via Next.js file conventions on every route.
 */
export const BRAND_COLOR = '#f97316';
export const BRAND_LETTER = 'N';

/**
 * Renders the brand mark at the requested size as a PNG ImageResponse.
 * Used by app/icon.tsx, app/apple-icon.tsx and the PWA icon route handlers.
 */
export function renderBrandIcon(size: number): ImageResponse {
  return new ImageResponse(
    (
      <div
        style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: BRAND_COLOR,
          borderRadius: `${Math.round(size * 0.125)}px`,
          color: '#ffffff',
          fontSize: `${Math.round(size * 0.72)}px`,
          fontWeight: 900,
          fontFamily: 'sans-serif',
          lineHeight: 1,
        }}
      >
        {BRAND_LETTER}
      </div>
    ),
    { width: size, height: size },
  );
}
