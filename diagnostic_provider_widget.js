const { chromium, webkit, devices } = require('playwright')
const WIDGET_URL = 'https://nevumo.com/bg/sofia/cleaning/lili?embed=1'
const iPhone14 = devices['iPhone 14']

async function runDiagnostic() {
  console.log('Starting ProviderWidget sticky button diagnostic...\n')

  // Test 1 — Desktop Chrome
  console.log('=== Test 1: Desktop Chrome ===')
  const browser1 = await chromium.launch({ headless: false })
  const page1 = await browser1.newPage()
  await page1.setViewportSize({ width: 1280, height: 800 })
  await page1.goto(WIDGET_URL)
  await page1.waitForLoadState('networkidle')
  await page1.waitForTimeout(2000)

  await page1.screenshot({ path: 'desktop_chrome_widget.png' })

  const desktopInfo = await page1.evaluate(() => {
    const fixedEls = Array.from(document.querySelectorAll('*')).filter(el => {
      const cs = window.getComputedStyle(el)
      return cs.position === 'fixed' && cs.bottom === '0px'
    })

    const submitBtns = Array.from(document.querySelectorAll(
      'button[type="submit"]'
    )).map(btn => {
      const cs = window.getComputedStyle(btn)
      return {
        text: btn.textContent?.trim().substring(0, 50),
        visible: cs.display !== 'none' && cs.visibility !== 'hidden',
        display: cs.display,
        parentClass: btn.parentElement?.className?.substring(0, 100),
        grandParentClass: btn.parentElement?.parentElement?.className?.substring(0, 100),
      }
    })

    return {
      fixedBottomElements: fixedEls.map(el => ({
        tag: el.tagName,
        class: (el.className || '').substring(0, 100),
        display: window.getComputedStyle(el).display,
        visibility: window.getComputedStyle(el).visibility,
        innerHTML: el.innerHTML.substring(0, 100),
      })),
      submitButtons: submitBtns,
      bodyChildren: Array.from(document.body.children).map(c => ({
        tag: c.tagName,
        class: (c.className || '').substring(0, 80),
      }))
    }
  })

  console.log(JSON.stringify(desktopInfo, null, 2))
  await browser1.close()

  // Test 2 — Mobile Chrome (non-iOS 26)
  console.log('\n=== Test 2: Mobile Chrome (non-iOS) ===')
  const browser2 = await chromium.launch({ headless: false })
  const ctx2 = await browser2.newContext({ ...iPhone14, hasTouch: true })
  const page2 = await ctx2.newPage()
  await page2.goto(WIDGET_URL)
  await page2.waitForLoadState('networkidle')
  await page2.waitForTimeout(2000)

  await page2.screenshot({ path: 'mobile_chrome_widget.png' })

  const mobileInfo = await page2.evaluate(() => {
    const ua = navigator.userAgent

    const isMobileApple =
      /iPhone|iPod/.test(ua) ||
      /iPad/.test(ua) ||
      (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)

    const safariVersionMatch = ua.match(/Version\/(\d+)/)
    const safariVersion = safariVersionMatch
      ? parseInt(safariVersionMatch[1], 10) : 0
    const isSafariOnIOS26 = safariVersion >= 26

    const osVersionMatch = ua.match(/CPU (?:iPhone )?OS (\d+)/)
    const osVersion = osVersionMatch
      ? parseInt(osVersionMatch[1], 10) : 0
    const isThirdPartyOnIOS26 = osVersion >= 26

    const isIOS26Plus = isMobileApple && (isSafariOnIOS26 || isThirdPartyOnIOS26)

    const submitBtns = Array.from(document.querySelectorAll(
      'button[type="submit"]'
    )).map(btn => {
      const cs = window.getComputedStyle(btn)
      return {
        text: btn.textContent?.trim().substring(0, 50),
        display: cs.display,
        visibility: cs.visibility,
        inDOM: document.body.contains(btn),
      }
    })

    const fixedEls = Array.from(document.querySelectorAll('*')).filter(el => {
      return window.getComputedStyle(el).position === 'fixed'
    }).map(el => ({
      tag: el.tagName,
      class: (el.className || '').substring(0, 80),
      display: window.getComputedStyle(el).display,
    }))

    return {
      userAgent: ua,
      hookSimulation: {
        isMobileApple,
        safariVersion,
        osVersion,
        isSafariOnIOS26,
        isThirdPartyOnIOS26,
        isIOS26PlusResult: isIOS26Plus,
      },
      submitButtons: submitBtns,
      fixedElements: fixedEls,
    }
  })

  console.log(JSON.stringify(mobileInfo, null, 2))
  await browser2.close()

  // Test 3 — WebKit (Safari equivalent)
  console.log('\n=== Test 3: WebKit Safari ===')
  const browser3 = await webkit.launch({ headless: false })
  const ctx3 = await browser3.newContext({ ...iPhone14, hasTouch: true })
  const page3 = await ctx3.newPage()
  await page3.goto(WIDGET_URL)
  await page3.waitForLoadState('networkidle')
  await page3.waitForTimeout(2000)

  await page3.screenshot({ path: 'webkit_safari_widget.png' })

  const safariInfo = await page3.evaluate(() => {
    const ua = navigator.userAgent

    const isMobileApple =
      /iPhone|iPod/.test(ua) ||
      /iPad/.test(ua) ||
      (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)

    const safariVersionMatch = ua.match(/Version\/(\d+)/)
    const safariVersion = safariVersionMatch
      ? parseInt(safariVersionMatch[1], 10) : 0
    const isSafariOnIOS26 = safariVersion >= 26

    const osVersionMatch = ua.match(/CPU (?:iPhone )?OS (\d+)/)
    const osVersion = osVersionMatch
      ? parseInt(osVersionMatch[1], 10) : 0
    const isThirdPartyOnIOS26 = osVersion >= 26

    const isIOS26Plus = isMobileApple && (isSafariOnIOS26 || isThirdPartyOnIOS26)

    const submitBtns = Array.from(document.querySelectorAll(
      'button[type="submit"]'
    )).map(btn => {
      const cs = window.getComputedStyle(btn)
      return {
        text: btn.textContent?.trim().substring(0, 50),
        display: cs.display,
        visibility: cs.visibility,
        inDOM: document.body.contains(btn),
      }
    })

    const fixedEls = Array.from(document.querySelectorAll('*')).filter(el => {
      return window.getComputedStyle(el).position === 'fixed'
    }).map(el => ({
      tag: el.tagName,
      class: (el.className || '').substring(0, 80),
      display: window.getComputedStyle(el).display,
    }))

    return {
      userAgent: ua,
      hookSimulation: {
        isMobileApple,
        safariVersion,
        osVersion,
        isIOS26PlusResult: isIOS26Plus,
      },
      submitButtons: submitBtns,
      fixedElements: fixedEls,
    }
  })

  console.log(JSON.stringify(safariInfo, null, 2))
  await browser3.close()

  console.log('\n=== Diagnostic complete ===')
}

runDiagnostic().catch(console.error)
