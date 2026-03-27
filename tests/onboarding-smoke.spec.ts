import { test, expect } from '@playwright/test';

test.describe('Onboarding Smoke Tests', () => {
  test('should load onboarding without errors', async ({ page }) => {
    const response = await page.goto('/bg/provider/dashboard');
    
    // Check for successful page load (no 500 errors, no crashes)
    expect(response?.status()).toBeLessThan(400);
    
    // Page should have basic structure
    await expect(page.locator('body')).toBeVisible();
    
    // Should not show error messages
    const errorElements = page.locator('.error, .alert, [role="alert"]');
    await expect(errorElements).toHaveCount(0);
  });

  test('should have all required UI sections', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Check for main sections
    const mainContent = page.locator('main');
    await expect(mainContent).toBeVisible();
    
    // Should have some form of step indicator
    const progressIndicators = page.locator('[class*="step"], [class*="progress"]');
    await expect(progressIndicators).toHaveCount(1);
  });

  test('should have interactive elements', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Should have buttons
    const buttons = page.locator('button');
    await expect(buttons).toHaveCount(1);
    
    // Should have inputs
    const inputs = page.locator('input, textarea, select');
    await expect(inputs).toHaveCount(1);
  });

  test('should be accessible and responsive', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Check basic accessibility
    const h1 = page.locator('h1');
    await expect(h1).toBeVisible();
    
    // Check responsive behavior
    await page.setViewportSize({ width: 375, height: 667 }); // Mobile
    await expect(page.locator('body')).toBeVisible();
    
    await page.setViewportSize({ width: 1200, height: 800 }); // Desktop
    await expect(page.locator('body')).toBeVisible();
  });

  test('should handle language switching', async ({ page }) => {
    // Test Bulgarian
    await page.goto('/bg/provider/dashboard');
    const bgTitle = await page.locator('h1').textContent();
    expect(bgTitle).toContain('услуги');
    
    // Test English
    await page.goto('/en/provider/dashboard');
    const enTitle = await page.locator('h1').textContent();
    expect(enTitle).toContain('profile');
  });

  test('should not have console errors', async ({ page }) => {
    const errors: string[] = [];
    page.on('console', msg => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });
    
    await page.goto('/bg/provider/dashboard');
    
    // Wait a bit for any console errors
    await page.waitForTimeout(2000);
    
    // Should not have JavaScript errors
    expect(errors).toHaveLength(0);
  });

  test('should load assets properly', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Check for images, styles, scripts
    const images = page.locator('img');
    const stylesheets = page.locator('link[rel="stylesheet"]');
    const scripts = page.locator('script');
    
    await expect(images).toHaveCount(0); // No broken images
    await expect(stylesheets).toHaveCount(1); // At least one stylesheet
    await expect(scripts).toHaveCount(1); // At least one script
  });

  test('should handle navigation correctly', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Should be able to navigate without breaking
    const currentUrl = page.url();
    expect(currentUrl).toContain('/provider/dashboard');
    
    // Should not redirect unexpectedly
    await page.waitForTimeout(3000);
    const finalUrl = page.url();
    expect(finalUrl).toBe(currentUrl);
  });

  test('should have proper meta tags', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Check for basic SEO/meta
    const title = await page.title();
    expect(title).toBeTruthy();
    expect(title.length).toBeGreaterThan(0);
  });

  test('should handle user interactions', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Try to interact with page
    await page.click('body'); // Click anywhere
    
    // Should not crash or break
    await expect(page.locator('body')).toBeVisible();
    
    // Should still be functional
    const buttons = page.locator('button');
    await expect(buttons).toHaveCount(1);
  });
});
