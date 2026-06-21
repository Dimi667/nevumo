'use client'

import { useIsIOS26Plus } from '@/hooks/useIsIOS26Plus'

interface ProviderMobileCTAProps {
  label: string
  providerName: string
  onOpenSheet: () => void
}

/**
 * CTA button visible ONLY on iOS 26+ mobile devices.
 * Replaces StickyProviderCTA which doesn't work on iOS 26 Safari.
 */
export default function ProviderMobileCTA({
  label,
  providerName,
  onOpenSheet,
}: ProviderMobileCTAProps) {
  const isIOS26Plus = useIsIOS26Plus()

  if (!isIOS26Plus) return null

  return (
    <div className="md:hidden px-4 py-3">
      <button
        onClick={onOpenSheet}
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
          lineHeight: '1.4',
          border: 'none',
          cursor: 'pointer',
        }}
      >
        {providerName.length <= 22 ? (
          <span>{label} {providerName}</span>
        ) : (
          <span style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1px' }}>
            <span style={{ fontSize: '0.8em', opacity: 0.85, fontWeight: 400 }}>
              {label}
            </span>
            <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', maxWidth: '100%' }}>
              {providerName}
            </span>
          </span>
        )}
      </button>
    </div>
  )
}
