'use client'

import { useEffect, useState } from 'react'
import { createPortal } from 'react-dom'
import { useVisualViewport } from '@/hooks/useVisualViewport'

interface StickyClaimBarProps {
  href: string
  label: string
}

export default function StickyClaimBar({
  href,
  label,
}: StickyClaimBarProps) {
  const [mounted, setMounted] = useState(false)
  const barRef = useVisualViewport<HTMLDivElement>()

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) return null

  return createPortal(
    <div
      ref={barRef}
      className="fixed bottom-0 left-0 right-0 z-[9999] sm:hidden
                 bg-white border-t border-gray-100 px-4 pt-3
                 pb-[max(0.75rem,env(safe-area-inset-bottom))]"
      style={{ boxShadow: '0 -2px 12px rgba(0,0,0,0.08)' }}
    >
      <a
        href={href}
        className="block w-full bg-orange-500 text-white
                   text-center py-4 rounded-xl font-bold text-lg"
      >
        {label}
      </a>
    </div>,
    document.body
  )
}
