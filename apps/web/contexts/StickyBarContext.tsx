'use client'

import {
  createContext,
  useContext,
  useState,
  useCallback,
  useRef,
  type ReactNode,
} from 'react'

interface StickyBarContextValue {
  register: () => () => void
  hasStickyBar: boolean
}

const StickyBarContext = createContext<StickyBarContextValue>({
  register: () => () => {},
  hasStickyBar: false,
})

export function StickyBarProvider({ children }: { children: ReactNode }) {
  const countRef = useRef(0)
  const [hasStickyBar, setHasStickyBar] = useState(false)

  const register = useCallback(() => {
    countRef.current += 1
    setHasStickyBar(true)

    return () => {
      countRef.current -= 1
      if (countRef.current === 0) setHasStickyBar(false)
    }
  }, [])

  return (
    <StickyBarContext.Provider value={{ register, hasStickyBar }}>
      {children}
    </StickyBarContext.Provider>
  )
}

export function useStickyBar() {
  return useContext(StickyBarContext)
}
