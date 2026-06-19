'use client'

import { type ReactNode } from 'react'
import { useIsIOS26Plus } from '@/hooks/useIsIOS26Plus'

interface StickyBottomBarProps {
  /** The sticky content (fixed bottom bar) */
  children: ReactNode
  /**
   * Optional fallback rendered on iOS 26+ instead of the sticky bar.
   * If not provided, nothing is rendered on iOS 26+.
   */
  fallback?: ReactNode
}

/**
 * Global wrapper for all sticky bottom bars.
 *
 * On iOS 26+: Safari's Liquid Glass toolbar covers position:fixed
 * bottom elements. This wrapper hides the sticky bar and optionally
 * renders an inline fallback instead.
 *
 * When Apple fixes this in a future iOS version, update ONLY this
 * file — all sticky bars across the site are fixed automatically.
 *
 * Usage:
 *   <StickyBottomBar fallback={<InlineCTA />}>
 *     <div className="fixed bottom-0 ...">...</div>
 *   </StickyBottomBar>
 *
 * Without fallback (just hide on iOS 26):
 *   <StickyBottomBar>
 *     <div className="fixed bottom-0 ...">...</div>
 *   </StickyBottomBar>
 */
export default function StickyBottomBar({
  children,
  fallback,
}: StickyBottomBarProps) {
  const isIOS26Plus = useIsIOS26Plus()

  if (isIOS26Plus) return fallback ? <>{fallback}</> : null

  return <>{children}</>
}
