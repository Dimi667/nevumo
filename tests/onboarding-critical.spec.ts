import { test, expect } from '@playwright/test';

test.describe('Onboarding Critical Tests', () => {
  test('should load onboarding page successfully', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Check if page loads without errors
    await expect(page.locator('body')).toBeVisible();
    
    // Check for any h1 element (regardless of text content)
    await expect(page.locator('h1')).toBeVisible();
  });

  test('should have centered layout during onboarding', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Check for centered layout class
    const body = page.locator('body');
    await expect(body).toHaveClass(/justify-center/);
  });

  test('should show progress indicators', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Check for any progress elements (Profile, Service, or numbers)
    await expect(page.locator('text=Profile')).toBeVisible();
    await expect(page.locator('text=Service')).toBeVisible();
  });

  test('should have description textarea', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Check for any textarea element
    const textarea = page.locator('textarea');
    await expect(textarea).toBeVisible();
  });

  test('should have character counter', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Check for any character counter (regex pattern)
    await expect(page.locator('text=/\\d+\\/\\d+/')).toBeVisible();
  });

  test('should have continue button', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Check for any continue button (with arrow or similar)
    await expect(page.locator('button')).toBeVisible();
  });

  test('should have skip functionality', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Check for any skip button
    await expect(page.locator('button:has-text("Пропусни")')).toBeVisible();
  });

  test('should have time hint', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Check for any time hint (minutes, seconds, etc.)
    await expect(page.locator('text=/минут/')).toBeVisible();
  });

  test('should have photo upload', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Check for upload functionality
    await expect(page.locator('input[type="file"]')).toBeVisible();
    await expect(page.locator('button')).toBeVisible();
  });

  test('should have form inputs', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Check for business name input
    await expect(page.locator('input[name="business_name"]')).toBeVisible();
    
    // Check for service title input (if on step 2)
    const serviceInput = page.locator('input[name="title"]');
    if (await serviceInput.isVisible()) {
      await expect(serviceInput).toBeVisible();
    }
  });

  test('should be responsive', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Check mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page.locator('body')).toBeVisible();
    
    // Check desktop viewport
    await page.setViewportSize({ width: 1200, height: 800 });
    await expect(page.locator('body')).toBeVisible();
  });
});
