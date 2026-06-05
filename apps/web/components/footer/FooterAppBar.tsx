'use client'

import { useState, useEffect } from 'react'
import { Smartphone, Link2, Check } from 'lucide-react'
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
  const [pwaDict, setPwaDict] = useState<Record<string, string>>({})

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

  useEffect(() => {
    if (!lang) return
    fetch(`/api/v1/translations/pwa?lang=${lang}`)
      .then(res => res.json())
      .then(data => {
        if (data && typeof data === 'object') setPwaDict(data)
      })
      .catch(() => setPwaDict({}))
  }, [lang])

  const pt = (key: string, fallback: string): string =>
    pwaDict[key] || fallback

  const handleIOSDismiss = async (closeFn: () => void) => {
    try {
      if (typeof navigator !== 'undefined' && navigator.share) {
        await navigator.share({ url: window.location.href })
      }
    } catch {
      // ignore AbortError silently
    }
    closeFn()
  }

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
        <div className="fixed inset-0 z-50 flex items-end justify-center bg-black/50">
          <div className="w-full rounded-t-2xl bg-white shadow-xl py-5 px-6 pb-8 max-h-[80vh] overflow-y-auto text-center">
            <div className="mb-4 flex items-center justify-center relative">
              <h3 className="text-lg font-semibold text-gray-900">
                {pt('install_title', 'Install Nevumo')}
              </h3>
              <button
                onClick={() => setShowIOSSheet(false)}
                className="absolute right-0 text-gray-400 hover:text-gray-600"
                aria-label="Close"
              >
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <line x1="18" y1="6" x2="6" y2="18" />
                  <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
              </button>
            </div>
            <p className="mb-6 text-sm text-gray-600">
              {role === 'provider'
                ? pt('provider_subtitle', 'See new requests instantly')
                : pt('client_subtitle', 'Track requests without opening a browser')}
            </p>
            <div className="mb-6 space-y-3">
              <p className="text-sm text-gray-700">
                1. {pt('ios_step1', 'Tap Share in the bottom toolbar')}{' '}
                <span className="inline-flex items-center gap-1 font-medium text-orange-600">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8" />
                    <polyline points="16 6 12 2 8 6" />
                    <line x1="12" y1="2" x2="12" y2="15" />
                  </svg>
                </span>
              </p>
              <p className="text-sm text-gray-700">
                2. {pt('ios_step2', 'Select "Add to Home Screen"')}
              </p>
            </div>
            <div className="sticky bottom-0 bg-white pt-3">
              <button
                onClick={() => handleIOSDismiss(() => setShowIOSSheet(false))}
                className="w-full rounded-xl bg-orange-500 px-4 py-3 text-base font-semibold text-white transition hover:bg-orange-600"
              >
                {pt('dismiss_button', 'Got it')}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
