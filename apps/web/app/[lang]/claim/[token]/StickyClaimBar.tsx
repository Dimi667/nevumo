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
  const [visible, setVisible] = useState(true)

  useEffect(() => {
    setMounted(true)

    let lastY = window.scrollY

    const onScroll = () => {
      const y = window.scrollY
      const delta = y - lastY

      // Always show near the top of the page
      if (y < 80) {
        setVisible(true)
        lastY = y
        return
      }

      // Show when scrolling UP (iOS toolbar hides — bar appears)
      // Hide when scrolling DOWN (iOS toolbar shows — bar hides)
      if (delta < -6) setVisible(true)
      if (delta > 6) setVisible(false)

      lastY = y
    }

    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

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
        transform: visible ? 'translateY(0)' : 'translateY(110%)',
        transition: 'transform 0.25s ease',
        willChange: 'transform',
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
