'use client'

import { useEffect, useRef } from 'react'
import StickyBottomBar from '@/components/ui/StickyBottomBar'

interface StickyProviderCTAProps {
  lang: string
  translations: Record<string, string>
  providerName: string
  onOpenSheet: () => void
}

export default function StickyProviderCTA({
  lang,
  translations,
  providerName,
  onOpenSheet
}: StickyProviderCTAProps) {
  const btnRef = useRef<HTMLDivElement>(null)
  const formId = 'provider-lead-form'

  // Effect: scroll visibility logic
  useEffect(() => {
    const btn = btnRef.current
    if (!btn) return

    const checkScroll = () => {
      const formEl = document.getElementById(formId)
      if (!formEl) {
        if (btnRef.current) {
          btnRef.current.style.transform = 'translateY(0)'
        }
        return
      }
      const rect = formEl.getBoundingClientRect()
      const isFormInView = rect.top < window.innerHeight && rect.bottom > 0
      if (btnRef.current) {
        btnRef.current.style.transform = isFormInView
          ? 'translateY(100%)'
          : 'translateY(0)'
      }
    }

    window.addEventListener('scroll', checkScroll, { passive: true })
    checkScroll()
    return () => {
      window.removeEventListener('scroll', checkScroll)
    }
  }, [formId])

  useEffect(() => {
    const btn = btnRef.current
    if (!btn) return

    // Check if button is visible (mobile only)
    const isMobile = window.getComputedStyle(btn).display !== 'none'
    if (!isMobile) return

    // Get button height and add padding to body
    const height = btn.offsetHeight
    document.body.style.paddingBottom = `${height}px`

    return () => {
      document.body.style.paddingBottom = ''
    }
  }, [])

  return (
    <StickyBottomBar>
      <div
        ref={btnRef}
        style={{
          transform: 'translateY(100%)',
          transition: 'transform 0.3s ease'
        }}
        className="fixed bottom-0 left-0 right-0 z-40 bg-white border-t border-gray-100 px-6 py-4 md:hidden"
      >
        <button
          onClick={onOpenSheet}
          className="w-full bg-orange-500 hover:bg-orange-600 text-white font-bold py-3 rounded-lg text-base truncate"
        >
          {providerName.length <= 22 ? (
            <span>{translations['cta_button']} {providerName}</span>
          ) : (
            <span style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1px', width: '100%' }}>
              <span style={{ fontSize: '0.8em', opacity: 0.85, fontWeight: 400 }}>
                {translations['cta_button']}
              </span>
              <span style={{ whiteSpace: 'normal', wordBreak: 'break-word', textAlign: 'center', width: '100%' }}>
                {providerName}
              </span>
            </span>
          )}
        </button>
      </div>
    </StickyBottomBar>
  )
}
