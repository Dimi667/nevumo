'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { clearAuth } from '@/lib/auth-store'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  const router = useRouter()

  useEffect(() => {
    console.error('[RouteError]', error)
    // Ако грешката е свързана с auth/localStorage → clear и redirect
    if (
      error.message?.includes('JSON') ||
      error.message?.includes('localStorage') ||
      error.message?.includes('token')
    ) {
      clearAuth()
      router.replace('/auth')
    }
  }, [error, router])

  return (
    <div style={{ padding: '2rem', textAlign: 'center' }}>
      <h2>Нещо се обърка</h2>
      <button onClick={reset}>Опитай отново</button>
    </div>
  )
}
