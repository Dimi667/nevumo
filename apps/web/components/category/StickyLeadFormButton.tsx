'use client'

import { useEffect, useRef } from 'react'

interface Props {
  label: string
  formId?: string
}

export default function StickyLeadFormButton({ 
  label, 
  formId = 'lead-form-anchor' 
}: Props) {
  const btnRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const btn = btnRef.current
    const formEl = document.getElementById(formId)
    if (!btn || !formEl) return

    const checkScroll = () => {
      const rect = formEl.getBoundingClientRect()
      const isFormInView = rect.top < window.innerHeight && rect.bottom > 0
      if (btnRef.current) {
        btnRef.current.style.transform = isFormInView ? 'translateY(100%)' : 'translateY(0)'
      }
    }

    window.addEventListener('scroll', checkScroll, { passive: true })
    checkScroll()
    return () => window.removeEventListener('scroll', checkScroll)
  }, [formId])

  return (
    <div
      ref={btnRef}
      style={{ 
        transform: 'translateY(100%)',
        transition: 'transform 0.3s ease'
      }}
      className="fixed bottom-0 left-0 right-0 z-[9999] bg-white border-t border-gray-100 p-4 md:hidden"
    >
      <button
        onClick={() => {
          const formEl = document.getElementById(formId)
          if (formEl) {
            formEl.scrollIntoView({ behavior: 'smooth', block: 'start' })
          }
        }}
        className="w-full bg-orange-500 hover:bg-orange-600 text-white font-bold py-3 rounded-lg text-base"
      >
        {label}
      </button>
    </div>
  )
}
