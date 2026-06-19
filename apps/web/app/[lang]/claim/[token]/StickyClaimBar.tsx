'use client'

import { useEffect, useState } from 'react'
import { createPortal } from 'react-dom'
import { useIsIOS26Plus } from '@/hooks/useIsIOS26Plus'
import { useStickyBar } from '@/contexts/StickyBarContext'

interface StickyClaimBarProps {
  href: string
  label: string
}

export default function StickyClaimBar({
  href,
  label,
}: StickyClaimBarProps) {
  const [mounted, setMounted] = useState(false)
  const isIOS26Plus = useIsIOS26Plus()
  const { register } = useStickyBar()

  // Effect 1: mount only
  useEffect(() => {
    setMounted(true)
  }, [])

  // Effect 2: register sticky bar ONLY when actually visible
  // isIOS26Plus starts false, becomes true after hydration on iOS 26
  // When it becomes true: cleanup unregisters, new run returns early
  useEffect(() => {
    if (isIOS26Plus) return
    const unregister = register()
    return () => unregister()
  }, [register, isIOS26Plus])

  if (isIOS26Plus) return null
  if (!mounted) return null

  return createPortal(
    <div
      className="sm:hidden"
      style={{
        position: 'fixed',
        bottom: 0,
        left: 0,
        right: 0,
        zIndex: 9999,
        background: 'white',
        borderTop: '0.5px solid #e5e7eb',
        paddingTop: '0.75rem',
        paddingLeft: '1rem',
        paddingRight: '1rem',
        paddingBottom: 'max(0.75rem, env(safe-area-inset-bottom))',
        boxShadow: '0 -2px 12px rgba(0,0,0,0.08)',
      }}
    >
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
    </div>,
    document.body
  )
}
