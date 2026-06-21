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
    <div className="md:hidden px-6 py-3">
      <button
        onClick={onOpenSheet}
        className="w-full bg-orange-500 hover:bg-orange-600 disabled:bg-orange-300 text-white font-bold py-3 rounded-lg transition-colors text-xl"
      >
        {providerName.length <= 22 ? (
          <span>{label} {providerName}</span>
        ) : (
          <span style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1px', width: '100%' }}>
            <span style={{ fontSize: '0.8em', opacity: 0.85, fontWeight: 400 }}>
              {label}
            </span>
            <span style={{ whiteSpace: 'normal', wordBreak: 'break-word', textAlign: 'center', width: '100%' }}>
              {providerName}
            </span>
          </span>
        )}
      </button>
    </div>
  )
}
