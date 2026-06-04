'use client'

import { useState, useEffect } from 'react'
import { Smartphone, Link2, Check } from 'lucide-react'
import PWAInstallPrompt from '@/components/pwa/PWAInstallPrompt'
import { getAuthUser } from '@/lib/auth-store'

// Type definition for BeforeInstallPromptEvent (not in standard DOM types)
interface BeforeInstallPromptEvent extends Event {
  readonly platforms: string[];
  readonly userChoice: Promise<{ outcome: 'accepted' | 'dismissed'; platform: string }>;
  prompt(): Promise<void>;
}

// Augment WindowEventMap for TypeScript
declare global {
  interface WindowEventMap {
    beforeinstallprompt: BeforeInstallPromptEvent;
    appinstalled: Event;
  }
}

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
  const [deferredPrompt, setDeferredPrompt] = useState<BeforeInstallPromptEvent | null>(null)
  const [canInstall, setCanInstall] = useState(false)
  const [isIOS, setIsIOS] = useState(false)
  const [showIOSSheet, setShowIOSSheet] = useState(false)
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    if (typeof window === 'undefined') return

    // If already installed — hide button
    const installed = localStorage.getItem('pwa_installed') === 'true'
    const isStandalone = window.matchMedia('(display-mode: standalone)').matches
    if (installed || isStandalone) return

    // iOS detection (no beforeinstallprompt on iOS)
    const ua = navigator.userAgent.toLowerCase()
    const ios = /iphone|ipad|ipod/.test(ua) && !/crios/.test(ua)
    if (ios) {
      setIsIOS(true)
      setCanInstall(true)
      return
    }

    // Android / Chrome desktop — listen for beforeinstallprompt
    const handler = (e: Event) => {
      e.preventDefault()
      setDeferredPrompt(e as BeforeInstallPromptEvent)
      setCanInstall(true)
    }
    window.addEventListener('beforeinstallprompt', handler)
    return () => window.removeEventListener('beforeinstallprompt', handler)
  }, [])

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
      <div className="flex items-center justify-center gap-3 py-4">
        {(canInstall || isIOS) && (
          <div className="md:hidden flex items-center gap-3">
            <button
              className="flex items-center gap-1.5 text-sm text-gray-600 hover:text-gray-800 border border-gray-300 hover:border-gray-400 rounded-full px-4 py-1.5 transition-colors cursor-pointer bg-transparent"
              onClick={() => {
                if (isIOS) {
                  setShowIOSSheet(true)
                } else if (deferredPrompt) {
                  deferredPrompt.prompt()
                  deferredPrompt.userChoice.then((choiceResult) => {
                    setDeferredPrompt(null)
                    setCanInstall(false)
                    if (choiceResult.outcome === 'accepted') {
                      localStorage.setItem('pwa_installed', 'true')
                    }
                    // If dismissed: do NOT write to localStorage
                    // Button will reappear on next page load when
                    // browser fires beforeinstallprompt again
                  })
                }
              }}
            >
              <Smartphone size={16} />
              {installLabel}
            </button>
          </div>
        )}
        <button
          className="flex items-center gap-1.5 text-sm text-gray-600 hover:text-gray-800 border border-gray-300 hover:border-gray-400 rounded-full px-4 py-1.5 transition-colors cursor-pointer bg-transparent"
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
