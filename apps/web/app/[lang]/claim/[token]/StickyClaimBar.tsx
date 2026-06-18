'use client'

import { useEffect, useState } from 'react'
import { createPortal } from 'react-dom'

interface StickyClaimBarProps {
  href: string
  label: string
}

export default function StickyClaimBar({
  href,
  label,
}: StickyClaimBarProps) {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) return null

  return createPortal(
    <div
      className="sm:hidden"
      style={{
        position: 'fixed',
        // iOS Safari toolbar fix — pure CSS, no JS needed.
        // 100lvh = full layout height (stable, ignores toolbar)
        // 100dvh = dynamic visible height (shrinks with toolbar)
        // calc(100lvh - 100dvh) = exactly the toolbar height
        // When toolbar hidden: bottom = 0. When shown: bottom = toolbar height.
        bottom: 'calc(100lvh - 100dvh)',
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
