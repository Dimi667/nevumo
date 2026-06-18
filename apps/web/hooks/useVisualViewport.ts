'use client'

import { useEffect, useRef } from 'react'

/**
 * Fixes iOS Safari dynamic toolbar hiding position:fixed elements.
 * Attaches Visual Viewport API listeners to dynamically adjust
 * the bottom position of a fixed element.
 *
 * Usage:
 *   const ref = useVisualViewport<HTMLDivElement>()
 *   <div ref={ref} className="fixed bottom-0 ...">
 */
export function useVisualViewport<T extends HTMLElement>() {
  const ref = useRef<T>(null)

  useEffect(() => {
    const vv = window.visualViewport
    if (!vv) return

    const update = () => {
      const el = ref.current
      if (!el) return
      const offsetBottom =
        window.innerHeight - vv.height - vv.offsetTop
      el.style.bottom = `${Math.max(0, offsetBottom)}px` 
    }

    vv.addEventListener('resize', update)
    vv.addEventListener('scroll', update)
    update()

    return () => {
      vv.removeEventListener('resize', update)
      vv.removeEventListener('scroll', update)
    }
  }, [])

  return ref
}
