'use client'

import { useState, useEffect } from 'react'
import { usePushNotifications } from '@/hooks/usePushNotifications'

interface PushPermissionPromptProps {
  lang: string
  role: 'provider' | 'client'
  show: boolean
  onDismiss: () => void
}

const FALLBACK = {
  title: '🔔 Get notifications instantly!',
  provider_body: "Don't miss new client requests while your phone is in your pocket.",
  client_body: "We'll notify you instantly when a provider responds to your request.",
  cta_button: 'Enable notifications',
  dismiss_button: 'Not now',
}

export default function PushPermissionPrompt({ lang, role, show, onDismiss }: PushPermissionPromptProps) {
  const [t, setT] = useState<Record<string, string>>({})
  const [tLoaded, setTLoaded] = useState(false)
  const [visible, setVisible] = useState(false)
  const { isSupported, isSubscribed, isLoading, subscribe } = usePushNotifications()

  // Fetch translations
  useEffect(() => {
    fetch(`/api/v1/translations/push_prompt?lang=${lang}`)
      .then((res) => res.json())
      .then((data) => {
        setT(data)
        setTLoaded(true)
      })
      .catch(() => {
        setTLoaded(true) // Use fallback values on error
      })
  }, [lang])

  // Animate in after delay
  useEffect(() => {
    if (show) {
      const timer = setTimeout(() => setVisible(true), 100)
      return () => clearTimeout(timer)
    } else {
      setVisible(false)
    }
  }, [show])

  // Track shown count
  useEffect(() => {
    if (!visible) return

    try {
      const shownCount = parseInt(localStorage.getItem('push_prompt_shown_count') ?? '0', 10)
      localStorage.setItem('push_prompt_shown_count', (shownCount + 1).toString())
    } catch {
      // localStorage access failed
    }
  }, [visible])

  // Anti-spam check
  let shouldShow = false
  try {
    const dismissedAt = parseInt(localStorage.getItem('push_prompt_dismissed_at') ?? '0', 10)
    const shownCount = parseInt(localStorage.getItem('push_prompt_shown_count') ?? '0', 10)
    const threeDaysMs = 3 * 24 * 60 * 60 * 1000

    shouldShow =
      tLoaded &&
      isSupported &&
      !isSubscribed &&
      show &&
      (typeof Notification === 'undefined' || Notification.permission !== 'denied') &&
      shownCount < 2 &&
      Date.now() - dismissedAt >= threeDaysMs
  } catch {
    // localStorage access failed - don't show
    shouldShow = false
  }

  if (!shouldShow) return null

  const handleEnable = async () => {
    try {
      await Promise.race([
        subscribe(),
        new Promise<void>((resolve) => setTimeout(resolve, 15000))
      ])
    } finally {
      onDismiss()
      try {
        localStorage.removeItem('push_prompt_dismissed_at')
        localStorage.removeItem('push_prompt_shown_count')
      } catch {}
    }
  }

  const handleDismiss = () => {
    try {
      localStorage.setItem('push_prompt_dismissed_at', Date.now().toString())
    } catch {
      // localStorage access failed
    }
    onDismiss()
  }

  const title = t['title'] || FALLBACK.title
  const body = role === 'provider' 
    ? (t['provider_body'] || FALLBACK.provider_body)
    : (t['client_body'] || FALLBACK.client_body)
  const ctaButton = t['cta_button'] || FALLBACK.cta_button
  const dismissButton = t['dismiss_button'] || FALLBACK.dismiss_button

  return (
    <div className="fixed inset-0 z-50">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/40"
        onClick={handleDismiss}
      />

      {/* Sheet */}
      <div
        className={`fixed bottom-0 left-0 right-0 bg-white rounded-t-2xl p-6 max-w-lg mx-auto transition-transform duration-300 ${
          visible ? 'translate-y-0' : 'translate-y-full'
        }`}
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
        <p className="text-sm text-gray-600 mb-6">{body}</p>

        <button
          onClick={handleEnable}
          disabled={isLoading}
          className="w-full bg-orange-500 hover:bg-orange-600 text-white font-semibold py-3 px-4 rounded-xl mb-3 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {isLoading ? (
            <span className="inline-flex items-center gap-2">
              <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              {ctaButton}
            </span>
          ) : (
            ctaButton
          )}
        </button>

        <button
          onClick={handleDismiss}
          className="w-full text-sm text-gray-500 py-2 text-center cursor-pointer hover:text-gray-700 transition-colors"
        >
          {dismissButton}
        </button>
      </div>
    </div>
  )
}
