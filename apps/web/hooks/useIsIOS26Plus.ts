'use client'

import { useEffect, useState } from 'react'

/**
 * Detects iOS 26+ devices where Safari's Liquid Glass toolbar
 * breaks position:fixed bottom elements.
 *
 * Two UA patterns to handle:
 *
 * 1. Safari on iOS 26 — Apple froze the OS version string,
 *    so we detect via Safari Version number (Version/26):
 *    "CPU iPhone OS 18_6 ... Version/26.0 Mobile/15E148 Safari/604.1"
 *
 * 2. Chrome/Brave/other WebKit browsers on iOS 26 — they still
 *    report real OS version (CPU iPhone OS 26_x):
 *    "CPU iPhone OS 26_3_0 ... CriOS/..."
 *
 * Returns false during SSR (safe default).
 *
 * Usage:
 *   const isIOS26Plus = useIsIOS26Plus()
 *   if (isIOS26Plus) return <InlineCTA />
 *   return <StickyBar />
 */
export function useIsIOS26Plus(): boolean {
  const [isIOS26Plus, setIsIOS26Plus] = useState(false)

  useEffect(() => {
    const ua = navigator.userAgent

    // Must be a mobile Apple device
    const isMobileApple =
      /iPhone|iPod/.test(ua) ||
      /iPad/.test(ua) ||
      (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)

    if (!isMobileApple) return

    // Pattern 1: Safari on iOS 26 — check Safari Version number
    // (Apple froze "CPU iPhone OS" at 18_x in Safari UA on iOS 26)
    const safariVersionMatch = ua.match(/Version\/(\d+)/)
    const safariVersion = safariVersionMatch
      ? parseInt(safariVersionMatch[1], 10)
      : 0
    const isSafariOnIOS26 = safariVersion >= 26

    // Pattern 2: Chrome/Brave/other WebKit browsers on iOS 26
    // (they still report real OS version in CPU string)
    const osVersionMatch = ua.match(/CPU (?:iPhone )?OS (\d+)/)
    const osVersion = osVersionMatch
      ? parseInt(osVersionMatch[1], 10)
      : 0
    const isThirdPartyOnIOS26 = osVersion >= 26

    setIsIOS26Plus(isSafariOnIOS26 || isThirdPartyOnIOS26)
  }, [])

  return isIOS26Plus
}
