const { chromium, webkit, devices } = require('playwright');

const PROVIDER_URL = 'https://nevumo.com/bg/sofia/cleaning/lili';
const FALLBACK_URL = 'https://nevumo.com/bg/sofia/cleaning';
const iPhone14 = devices['iPhone 14'];

async function runDiagnostic() {
  console.log('=== STARTING BOTTOMSHEET SCROLL DIAGNOSTIC ===\n');

  // Test 1 — Chrome Mobile (Chromium)
  console.log('TEST 1: Chrome Mobile (Chromium)');
  console.log('=====================================\n');
  await testChromeMobile();

  // Test 2 — WebKit (Safari equivalent)
  console.log('\n\nTEST 2: WebKit (Safari equivalent)');
  console.log('=====================================\n');
  await testWebkitSafari();

  console.log('\n=== DIAGNOSTIC COMPLETE ===');
}

async function testChromeMobile() {
  const browser = await chromium.launch({ headless: false });
  const ctx = await browser.newContext({
    ...iPhone14,
    hasTouch: true,
  });
  const page = await ctx.newPage();

  try {
    let url = PROVIDER_URL;
    console.log('Navigating to:', url);
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });

    // Debug: check page title and URL
    const title = await page.title();
    const currentUrl = page.url();
    console.log('Page title:', title);
    console.log('Current URL:', currentUrl);

    // Debug: check if page has content
    const bodyText = await page.evaluate(() => document.body.innerText.substring(0, 200));
    console.log('Body text preview:', bodyText);

    // First, accept cookies to get them out of the way
    await page.waitForTimeout(2000);
    const buttons = await page.locator('button').all();
    console.log('Initial buttons count:', buttons.length);

    for (const btn of buttons) {
      const text = await btn.textContent().catch(() => '');
      if (text && text.includes('Приеми всички')) {
        console.log('Accepting cookies');
        await btn.click();
        break;
      }
    }
    await page.waitForTimeout(1000);

    // Now look for the mobile CTA button to open the form
    // Try to find a button with specific classes or text
    const allButtons = await page.locator('button').all();
    console.log('Total buttons found after cookie accept:', allButtons.length);

    // Try clicking on the "Свържи ме с Лили" button directly first
    let clicked = false;
    const connectButton = page.locator('button').filter({ hasText: 'Свържи ме с Лили' }).first();
    if (await connectButton.count() > 0) {
      console.log('Clicking on "Свържи ме с Лили" button');
      await connectButton.click();
      clicked = true;
    }

    if (!clicked) {
      // Try clicking on the provider name or a sticky CTA
      // Look for orange buttons or buttons with specific classes
      for (const btn of allButtons) {
        const className = await btn.getAttribute('class').catch(() => '');
        const text = await btn.textContent().catch(() => '');

        // Look for orange buttons (bg-orange-500) that are visible (not hidden)
        if (className && className.includes('bg-orange') && !className.includes('hidden') && !className.includes('opacity-0')) {
          console.log('Found visible CTA button, clicking...');
          await btn.click();
          clicked = true;
          break;
        }
      }
    }

    if (!clicked) {
      console.log('Could not find button to open form, trying to scroll and find');
      await page.evaluate(() => window.scrollTo(0, 500));
      await page.waitForTimeout(500);

      const buttonsAfterScroll = await page.locator('button').all();
      const connectButtonAfterScroll = page.locator('button').filter({ hasText: 'Свържи ме с Лили' }).first();
      if (await connectButtonAfterScroll.count() > 0) {
        console.log('Clicking on "Свържи ме с Лили" button after scroll');
        await connectButtonAfterScroll.click();
        clicked = true;
      }

      if (!clicked) {
        for (const btn of buttonsAfterScroll) {
          const text = await btn.textContent().catch(() => '');
          const className = await btn.getAttribute('class').catch(() => '');
          if (className && className.includes('bg-orange') && !className.includes('hidden') && !className.includes('opacity-0')) {
            console.log('Found CTA after scroll, clicking...');
            await btn.click();
            clicked = true;
            break;
          }
        }
      }
    }

    await page.waitForTimeout(800);

    // Take screenshot — form open
    await page.screenshot({ path: 'chrome_mobile_form_open.png' });

    // Debug: check what fixed bottom elements exist
    const debugElements = await page.evaluate(() => {
      const fixedBottom = document.querySelectorAll('.fixed.bottom-0');
      return Array.from(fixedBottom).map(el => ({
        tag: el.tagName,
        class: el.className,
        style: el.getAttribute('style'),
      }));
    });
    console.log('=== DEBUG: Fixed bottom elements ===');
    console.log(JSON.stringify(debugElements, null, 2));

    // Inspect ALL elements inside the sheet
    const scrollInfo = await page.evaluate(() => {
      const sheet = document.querySelector(
        '[style*="translateY(0)"], .fixed.bottom-0.rounded-t-2xl, .fixed.bottom-0.bg-white'
      );
      if (!sheet) return { error: 'Sheet not found' };

      const inspect = (el, depth = 0) => {
        if (depth > 5) return null;
        const cs = window.getComputedStyle(el);
        const className = typeof el.className === 'string' ? el.className : el.className?.toString() || '';
        return {
          depth,
          tag: el.tagName,
          id: el.id || null,
          class: className.substring(0, 100),
          computed: {
            overflow: cs.overflow,
            overflowY: cs.overflowY,
            overflowX: cs.overflowX,
            height: cs.height,
            maxHeight: cs.maxHeight,
            minHeight: cs.minHeight,
            display: cs.display,
            flexDirection: cs.flexDirection,
            flex: cs.flex,
            position: cs.position,
            webkitOverflowScrolling: cs.webkitOverflowScrolling,
            touchAction: cs.touchAction,
          },
          scroll: {
            scrollHeight: el.scrollHeight,
            clientHeight: el.clientHeight,
            scrollTop: el.scrollTop,
            canScroll: el.scrollHeight > el.clientHeight,
          },
          childCount: el.children.length,
          children: Array.from(el.children).slice(0, 6).map(
            c => inspect(c, depth + 1)
          ).filter(Boolean),
        };
      };

      return inspect(sheet);
    });

    console.log('=== CHROME MOBILE SCROLL INFO ===');
    console.log(JSON.stringify(scrollInfo, null, 2));

    // Try programmatic scroll on EACH element
    const scrollAttempt = await page.evaluate(() => {
      const results = [];
      const sheet = document.querySelector(
        '[style*="translateY(0)"], .fixed.bottom-0.rounded-t-2xl, .fixed.bottom-0.bg-white'
      );
      if (!sheet) return [{ error: 'no sheet' }];

      const tryScroll = (el) => {
        const before = el.scrollTop;
        el.scrollTop = 200;
        const after = el.scrollTop;
        const className = typeof el.className === 'string' ? el.className : el.className?.toString() || '';
        return {
          tag: el.tagName,
          class: className.substring(0, 80),
          scrolledFrom: before,
          scrolledTo: after,
          success: after > before,
        };
      };

      // Try the sheet and all descendants
      const walk = (el) => {
        results.push(tryScroll(el));
        Array.from(el.children).forEach(c => walk(c));
      };
      walk(sheet);
      return results;
    });

    console.log('\n=== CHROME SCROLL ATTEMPT RESULTS ===');
    console.log(JSON.stringify(scrollAttempt, null, 2));

  } finally {
    await browser.close();
  }
}

async function testWebkitSafari() {
  const browser = await webkit.launch({ headless: false });
  const ctx = await browser.newContext({
    ...iPhone14,
    hasTouch: true,
  });
  const page = await ctx.newPage();

  try {
    let url = PROVIDER_URL;
    console.log('Navigating to:', url);
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });

    // Debug: check page title and URL
    const title = await page.title();
    const currentUrl = page.url();
    console.log('Page title:', title);
    console.log('Current URL:', currentUrl);

    // Debug: check if page has content
    const bodyText = await page.evaluate(() => document.body.innerText.substring(0, 200));
    console.log('Body text preview:', bodyText);

    // Accept cookies
    await page.waitForTimeout(2000);
    const buttons = await page.locator('button').all();
    console.log('Initial buttons count:', buttons.length);

    for (const btn of buttons) {
      const text = await btn.textContent().catch(() => '');
      if (text && text.includes('Приеми всички')) {
        console.log('Accepting cookies');
        await btn.click();
        break;
      }
    }
    await page.waitForTimeout(1000);

    // Find CTA button
    const allButtons = await page.locator('button').all();
    console.log('Total buttons found after cookie accept:', allButtons.length);

    // Try clicking on the "Свържи ме с Лили" button directly first
    let clicked = false;
    const connectButton = page.locator('button').filter({ hasText: 'Свържи ме с Лили' }).first();
    if (await connectButton.count() > 0) {
      console.log('Clicking on "Свържи ме с Лили" button');
      await connectButton.click();
      clicked = true;
    }

    if (!clicked) {
      for (const btn of allButtons) {
        const className = await btn.getAttribute('class').catch(() => '');
        const text = await btn.textContent().catch(() => '');

        if (className && className.includes('bg-orange') && !className.includes('hidden') && !className.includes('opacity-0')) {
          console.log('Found visible CTA button, clicking...');
          await btn.click();
          clicked = true;
          break;
        }
      }
    }

    if (!clicked) {
      await page.evaluate(() => window.scrollTo(0, 500));
      await page.waitForTimeout(500);

      const buttonsAfterScroll = await page.locator('button').all();
      const connectButtonAfterScroll = page.locator('button').filter({ hasText: 'Свържи ме с Лили' }).first();
      if (await connectButtonAfterScroll.count() > 0) {
        console.log('Clicking on "Свържи ме с Лили" button after scroll');
        await connectButtonAfterScroll.click();
        clicked = true;
      }

      if (!clicked) {
        for (const btn of buttonsAfterScroll) {
          const className = await btn.getAttribute('class').catch(() => '');
          if (className && className.includes('bg-orange') && !className.includes('hidden') && !className.includes('opacity-0')) {
            console.log('Found CTA after scroll, clicking...');
            await btn.click();
            clicked = true;
            break;
          }
        }
      }
    }

    await page.waitForTimeout(800);

    await page.screenshot({ path: 'webkit_safari_form_open.png' });

    // Debug: check what fixed bottom elements exist
    const debugElements = await page.evaluate(() => {
      const fixedBottom = document.querySelectorAll('.fixed.bottom-0');
      return Array.from(fixedBottom).map(el => ({
        tag: el.tagName,
        class: el.className,
        style: el.getAttribute('style'),
      }));
    });
    console.log('=== DEBUG: Fixed bottom elements ===');
    console.log(JSON.stringify(debugElements, null, 2));

    // Same scroll inspection
    const scrollInfo = await page.evaluate(() => {
      const sheet = document.querySelector(
        '[style*="translateY(0)"], .fixed.bottom-0.rounded-t-2xl, .fixed.bottom-0.bg-white'
      );
      if (!sheet) return { error: 'Sheet not found' };

      const inspect = (el, depth = 0) => {
        if (depth > 5) return null;
        const cs = window.getComputedStyle(el);
        const className = typeof el.className === 'string' ? el.className : el.className?.toString() || '';
        return {
          depth,
          tag: el.tagName,
          id: el.id || null,
          class: className.substring(0, 100),
          computed: {
            overflow: cs.overflow,
            overflowY: cs.overflowY,
            height: cs.height,
            maxHeight: cs.maxHeight,
            minHeight: cs.minHeight,
            display: cs.display,
            flexDirection: cs.flexDirection,
            flex: cs.flex,
            position: cs.position,
            webkitOverflowScrolling: cs.webkitOverflowScrolling,
            touchAction: cs.touchAction,
          },
          scroll: {
            scrollHeight: el.scrollHeight,
            clientHeight: el.clientHeight,
            scrollTop: el.scrollTop,
            canScroll: el.scrollHeight > el.clientHeight,
          },
          children: Array.from(el.children).slice(0, 6).map(
            c => inspect(c, depth + 1)
          ).filter(Boolean),
        };
      };
      return inspect(sheet);
    });

    console.log('=== WEBKIT SAFARI SCROLL INFO ===');
    console.log(JSON.stringify(scrollInfo, null, 2));

    // Check body styles (body scroll lock side effects)
    const bodyStyles = await page.evaluate(() => {
      const bs = document.body.style;
      const cs = window.getComputedStyle(document.body);
      return {
        bodyInlineStyles: {
          position: bs.position,
          overflow: bs.overflow,
          top: bs.top,
          left: bs.left,
          right: bs.right,
        },
        bodyComputed: {
          position: cs.position,
          overflow: cs.overflow,
          height: cs.height,
        }
      };
    });

    console.log('\n=== WEBKIT BODY STYLES ===');
    console.log(JSON.stringify(bodyStyles, null, 2));

    // Scroll attempt
    const scrollAttempt = await page.evaluate(() => {
      const results = [];
      const sheet = document.querySelector(
        '[style*="translateY(0)"], .fixed.bottom-0.rounded-t-2xl, .fixed.bottom-0.bg-white'
      );
      if (!sheet) return [{ error: 'no sheet' }];

      const walk = (el) => {
        const before = el.scrollTop;
        el.scrollTop = 200;
        const after = el.scrollTop;
        const className = typeof el.className === 'string' ? el.className : el.className?.toString() || '';
        results.push({
          tag: el.tagName,
          class: className.substring(0, 80),
          scrolledFrom: before,
          scrolledTo: after,
          canScroll: el.scrollHeight > el.clientHeight,
          success: after > before,
        });
        Array.from(el.children).forEach(c => walk(c));
      };
      walk(sheet);
      return results;
    });

    console.log('\n=== WEBKIT SCROLL ATTEMPT RESULTS ===');
    console.log(JSON.stringify(scrollAttempt, null, 2));

    await page.screenshot({ path: 'webkit_safari_after_scroll.png' });

  } finally {
    await browser.close();
  }
}

runDiagnostic().catch(console.error);
