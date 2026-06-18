'use client'

import { useEffect, useRef } from 'react'

/**
 * Fixes iOS Safari dynamic toolbar hiding position:fixed elements.
 *
 * Strategy: keep bottom:0 (layout viewport), compensate with
 * translateY by the difference between layout and visual viewport.
 * This is the approach recommended by Google Chrome team.
 *
 * Ref: https://developer.chrome.com/blog/visual-viewport-api
 */
export function useVisualViewport<T extends HTMLElement>() {
  const ref = useRef<T>(null)

  useEffect(() => {
    const vv = window.visualViewport
    if (!vv) return

    const update = () => {
      const el = ref.current
      if (!el) return
      // Distance toolbar takes from visual viewport
      const offset = window.innerHeight - vv.height - vv.offsetTop
      el.style.transform = `translateY(${-Math.max(0, offset)}px)` 
    }

    vv.addEventListener('resize', update, { passive: true })
    vv.addEventListener('scroll', update, { passive: true })
    update()

    return () => {
      vv.removeEventListener('resize', update)
      vv.removeEventListener('scroll', update)
    }
  }, [])

  return ref
}
