'use client'

import { useState } from 'react'
import { Smartphone, Link2, Check } from 'lucide-react'
import { usePWAInstall } from '@/hooks/usePWAInstall'
import PWAInstallPrompt from '@/components/pwa/PWAInstallPrompt'
import { getAuthUser } from '@/lib/auth-store'

interface FooterAppBarProps {
  lang: string
  installLabel: string
  shareLabel: string
}

function detectRole(): 'client' | 'provider' {
  if (typeof window === 'undefined') return 'client'

  // 1. Logged-in user — most reliable signal
  const user = getAuthUser()
  if (user?.role === 'provider') return 'provider'
  if (user?.role === 'client') return 'client'

  // 2. Declared intent (set when user clicks role card on homepage)
  const intent = localStorage.getItem('nevumo_intent')
  if (intent === 'provider') return 'provider'
  if (intent === 'client') return 'client'

  // 3. Behavioral signal from current URL path
  const path = window.location.pathname
  if (path.includes('/dolacz') || path.includes('/provider/')) return 'provider'

  // 4. Default
  return 'client'
}

export default function FooterAppBar({ lang, installLabel, shareLabel }: FooterAppBarProps) {
  const role = detectRole()
  const { canInstall, isIOS, showPrompt } = usePWAInstall()
  const [showIOSSheet, setShowIOSSheet] = useState(false)
  const [copied, setCopied] = useState(false)

  const handleShareClick = async () => {
    if (typeof navigator !== 'undefined' && navigator.share) {
      try {
        await navigator.share({ title: document.title, url: window.location.href })
      } catch {
        // ignore AbortError silently
      }
    } else {
      try {
        await navigator.clipboard.writeText(window.location.href)
        setCopied(true)
        setTimeout(() => setCopied(false), 2000)
      } catch {
        // ignore silently
      }
    }
  }

  return (
    <>
      <div className="flex items-center justify-center gap-3 py-3">
        {(canInstall || isIOS) && (
          <div className="md:hidden flex items-center gap-3">
            <button
              className="flex items-center gap-1.5 text-sm text-gray-500 hover:text-gray-700 transition-colors cursor-pointer bg-transparent border-0 p-0"
              onClick={() => {
                if (isIOS) {
                  setShowIOSSheet(true)
                } else if (canInstall) {
                  showPrompt()
                }
              }}
            >
              <Smartphone size={16} />
              {installLabel}
            </button>
            <span className="w-px h-4 bg-gray-200" />
          </div>
        )}
        <button
          className="flex items-center gap-1.5 text-sm text-gray-500 hover:text-gray-700 transition-colors cursor-pointer bg-transparent border-0 p-0"
          onClick={handleShareClick}
        >
          {copied ? <Check size={16} /> : <Link2 size={16} />}
          {shareLabel}
        </button>
      </div>

      {showIOSSheet && (
        <PWAInstallPrompt
          trigger="return_user"
          role={role}
          onClose={() => setShowIOSSheet(false)}
          lang={lang}
        />
      )}
    </>
  )
}
