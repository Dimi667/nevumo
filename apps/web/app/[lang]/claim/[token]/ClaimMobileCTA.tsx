'use client'

import { useIsIOS26Plus } from '@/hooks/useIsIOS26Plus'

interface ClaimMobileCTAProps {
  href: string
  label: string
}

/**
 * CTA button visible ONLY on iOS 26+ mobile devices.
 * Replaces the sticky bar which doesn't work on iOS 26 Safari.
 * Hidden on desktop (sm:hidden) and on non-iOS 26 mobile.
 */
export default function ClaimMobileCTA({
  href,
  label,
}: ClaimMobileCTAProps) {
  const isIOS26Plus = useIsIOS26Plus()

  if (!isIOS26Plus) return null

  return (
    <div className="sm:hidden px-4 py-3">
      <a
        href={href}
        style={{
          display: 'block',
          width: '100%',
          background: '#f97316',
          color: 'white',
          textAlign: 'center',
          padding: '1rem',
          borderRadius: '0.75rem',
          fontWeight: 700,
          fontSize: '1.125rem',
          textDecoration: 'none',
          lineHeight: '1.4',
        }}
      >
        {label}
      </a>
    </div>
  )
}
