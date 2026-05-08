import { test, expect } from '@playwright/test';

test('cookie banner touch targets are at least 44x44px on mobile', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 });
  await page.goto('/en');

  // Изчакай banner
  await page.waitForSelector('[data-testid="cookie-banner"]', { timeout: 5000 });

  const selectors = [
    '[data-testid="cookie-accept-all"]',
    '[data-testid="cookie-reject-all"]',
    '[data-testid="cookie-customize"]',
    '[data-testid="cookie-close"]',
    '[data-testid="cookie-settings-link"]',
  ];

  for (const sel of selectors) {
    const el = page.locator(sel).first();
    const exists = await el.count();
    if (!exists) continue;

    const box = await el.boundingBox();
    expect(box!.width, `${sel} width`).toBeGreaterThanOrEqual(44);
    expect(box!.height, `${sel} height`).toBeGreaterThanOrEqual(44);
  }

  // Toggles в customize панела
  await page.click('[data-testid="cookie-customize"]');
  await page.waitForSelector('[data-testid="cookie-toggle-functional"]', { timeout: 3000 });

  const toggleSelectors = [
    '[data-testid="cookie-toggle-functional"]',
    '[data-testid="cookie-toggle-analytics"]',
    '[data-testid="cookie-toggle-marketing"]',
  ];

  for (const sel of toggleSelectors) {
    const el = page.locator(sel).first();
    const box = await el.boundingBox();
    expect(box!.width, `${sel} width`).toBeGreaterThanOrEqual(44);
    expect(box!.height, `${sel} height`).toBeGreaterThanOrEqual(44);
  }
});

test('cookie banner re-appears after 12 months', async ({ page }) => {
  await page.goto('/en');

  // Инжектирай изтекъл consent cookie (ts = 13 месеца назад)
  const expiredTs = Date.now() - (13 * 30 * 24 * 60 * 60 * 1000);
  const expiredConsent = JSON.stringify({
    v: 2,
    ts: expiredTs,
    categories: { necessary: true, functional: true, analytics: true, marketing: false },
    policy_version: '2026-05-01'
  });

  await page.context().addCookies([{
    name: 'nevumo_consent',
    value: encodeURIComponent(expiredConsent),
    domain: 'localhost',
    path: '/',
  }]);

  // Рестартирай страницата с изтекъл cookie
  await page.reload();
  await page.waitForTimeout(2500); // Next.js hydration

  // Banner трябва да се покаже
  const banner = page.locator('[data-testid="cookie-banner"]');
  await expect(banner).toBeVisible({ timeout: 5000 });
});
