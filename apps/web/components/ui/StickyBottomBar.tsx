'use client'

import { useEffect, type ReactNode } from 'react'
import { useIsIOS26Plus } from '@/hooks/useIsIOS26Plus'
import { useStickyBar } from '@/contexts/StickyBarContext'

interface StickyBottomBarProps {
  children: ReactNode
  fallback?: ReactNode
}

/**
 * Global wrapper for all sticky bottom bars.
 *
 * Handles TWO concerns in one place:
 * 1. iOS 26+ detection — hides sticky, shows fallback
 * 2. StickyBarContext registration — cookie banner offset
 *
 * On iOS 26+: does NOT register (bar not shown → no offset needed)
 * On other devices: registers → cookie banner gets bottom-24
 *
 * When Apple fixes iOS sticky behavior → update useIsIOS26Plus.ts only.
 */
export default function StickyBottomBar({
  children,
  fallback,
}: StickyBottomBarProps) {
  const isIOS26Plus = useIsIOS26Plus()
  const { register } = useStickyBar()

  useEffect(() => {
    if (isIOS26Plus) return
    const unregister = register()
    return () => unregister()
  }, [register, isIOS26Plus])

  if (isIOS26Plus) return fallback ? <>{fallback}</> : null
  return <>{children}</>
}
