import { ImageResponse } from 'next/og';

/**
 * SINGLE SOURCE OF TRUTH for the Nevumo brand mark.
 *
 * The brand mark is an orange (#f97316) rounded square with a white "N".
 * The "N" is drawn from geometric shapes (not a font glyph) so we have full
 * control over the design:
 *   - horizontal stretch       -> STEM_LEFT / STEM_RIGHT (gap between stems)
 *   - diagonal thicker than the verticals -> DIAG_W vs STEM_W
 *   - perfectly centered        -> the letter box is symmetric around the center
 *
 * Edit the constants below and every icon (favicon, apple-touch-icon and PWA
 * icons) updates everywhere automatically — including any new pages, since
 * these are emitted via Next.js file conventions on every route.
 */
export const BRAND_COLOR = '#f97316';

// All values are fractions of the icon size (0..1), so the mark scales
// identically at 32px (favicon), 180px (apple-icon) and 512px (PWA).
const RADIUS = 0.125; // rounded-square corner radius
const STEM_W = 0.13; // vertical stroke width
const DIAG_W = 0.18; // diagonal stroke width (thicker than the verticals)
const STEM_LEFT = 0.3; // x-center of the left vertical (smaller = wider / more stretched)
const STEM_RIGHT = 0.7; // x-center of the right vertical
const TOP = 0.25; // top of the letter box
const HEIGHT = 0.5; // height of the letter box (bottom = TOP + HEIGHT, centered around 0.5)
const DIAG_OFFSET_Y = 0; // vertical offset of the diagonal (positive = down)
const DIAG_ANGLE = -47; // diagonal angle in degrees (negative = clockwise)
const DIAG_RADIUS = 0.027; // corner radius of the diagonal (fraction of icon size)
const DIAG_LEN_OFFSET = 0.006; // additional length of the diagonal (fraction of icon size)

/**
 * Renders the brand mark at the requested size as a PNG ImageResponse.
 * Used by app/icon.tsx, app/apple-icon.tsx and the PWA icon route handlers.
 */
export function renderBrandIcon(size: number): ImageResponse {
  const stemW = size * STEM_W;
  const diagW = size * DIAG_W;
  const top = size * TOP;
  const letterH = size * HEIGHT;
  const leftX = size * STEM_LEFT;
  const rightX = size * STEM_RIGHT;
  const diagOffsetY = size * DIAG_OFFSET_Y;
  const diagLenOffset = size * DIAG_LEN_OFFSET;

  // Diagonal goes from the inner corner of the left stem to the inner corner
  // of the right stem (so its corners align with the verticals).
  const leftInnerX = leftX + stemW / 2;
  const rightInnerX = rightX - stemW / 2;
  const dx = rightInnerX - leftInnerX;
  const dy = letterH;
  const diagLen = Math.sqrt(dx * dx + dy * dy) + diagLenOffset;
  const angle = DIAG_ANGLE;

  return new ImageResponse(
    (
      <div
        style={{
          position: 'relative',
          display: 'flex',
          width: '100%',
          height: '100%',
          backgroundColor: BRAND_COLOR,
          borderRadius: `${size * RADIUS}px`,
        }}
      >
        {/* left vertical */}
        <div
          style={{
            position: 'absolute',
            left: leftX - stemW / 2,
            top,
            width: stemW,
            height: letterH,
            backgroundColor: '#ffffff',
          }}
        />
        {/* right vertical */}
        <div
          style={{
            position: 'absolute',
            left: rightX - stemW / 2,
            top,
            width: stemW,
            height: letterH,
            backgroundColor: '#ffffff',
          }}
        />
        {/* diagonal (slightly thicker) */}
        <div
          style={{
            position: 'absolute',
            left: size * 0.5 - diagW / 2,
            top: size * 0.5 - diagLen / 2 + diagOffsetY,
            width: diagW,
            height: diagLen,
            backgroundColor: '#ffffff',
            borderRadius: `${size * DIAG_RADIUS}px`,
            transform: `rotate(${angle}deg)`,
          }}
        />
      </div>
    ),
    { width: size, height: size },
  );
}
