import { ImageResponse } from '@vercel/og';
import fs from 'fs';
import path from 'path';

export interface BaseOGImageProps {
  title: string;
  description: string;
  ctaText?: string;
  logoUrl?: string;
}

/**
 * Base OG Image generator component with Noto Sans Bold font
 */
export async function BaseOGImage({
  title,
  description,
  ctaText,
  logoUrl,
}: BaseOGImageProps): Promise<ImageResponse> {
  // Load Noto Sans Bold font using fs.readFileSync (Node.js runtime)
  const fontData = fs.readFileSync(
    path.join(process.cwd(), 'public/fonts/NotoSans-Bold.ttf')
  );

  // Use absolute URL for logo (@vercel/og requires absolute URLs)
  const defaultLogoUrl = 'http://localhost:3000/Nevumo_logo.svg';

  return new ImageResponse(
    (
      <div
        style={{
          height: '100%',
          width: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: '#ffffff',
          backgroundImage: 'linear-gradient(135deg, #fff5eb 0%, #ffffff 100%)',
          fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        }}
      >
        {/* Header with brand logo */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            marginBottom: '60px',
          }}
        >
          <img
            src={logoUrl || defaultLogoUrl}
            width="180"
            height="30"
            alt="Nevumo"
          />
        </div>

        {/* Main content */}
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            textAlign: 'center',
            padding: '0 80px',
          }}
        >
          {/* Title */}
          <div
            style={{
              fontSize: '64px',
              fontWeight: '800',
              color: '#1a1a1a',
              lineHeight: '1.1',
              marginBottom: '32px',
              maxWidth: '900px',
            }}
          >
            {title}
          </div>

          {/* Description */}
          <div
            style={{
              fontSize: '28px',
              color: '#666666',
              lineHeight: '1.4',
              maxWidth: '800px',
              marginBottom: '40px',
            }}
          >
            {description}
          </div>

          {/* CTA Button with Noto Sans Bold font */}
          {ctaText && (
            <div
              style={{
                backgroundColor: '#f97316',
                color: '#ffffff',
                padding: '32px 80px',
                borderRadius: '9999px',
                fontSize: '42px',
                fontWeight: 700,
                fontFamily: 'Noto Sans',
                boxShadow: '0 10px 30px rgba(249, 115, 22, 0.7)',
              }}
            >
              {ctaText}
            </div>
          )}
        </div>
      </div>
    ),
    {
      width: 1200,
      height: 630,
      fonts: [
        {
          name: 'Noto Sans',
          data: fontData,
          style: 'normal',
          weight: 700,
        },
      ],
    }
  );
}
