import { test, expect } from '@playwright/test';

test.describe('Onboarding Basic Tests', () => {
  test('should load onboarding page', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Check if we're on onboarding (not dashboard) - Bulgarian text
    await expect(page.locator('h1')).toContainText('Намери услуга за минути');
  });

  test('should have centered layout', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Check for centered layout class
    const body = page.locator('body');
    await expect(body).toHaveClass(/justify-center/);
  });

  test('should show progress bar elements', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Check for progress indicators
    await expect(page.locator('text=Profile')).toBeVisible();
    await expect(page.locator('text=Service')).toBeVisible();
  });

  test('should have improved description field', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Check for description textarea with new placeholder
    const description = page.locator('textarea[placeholder*="услуги, опит"]');
    await expect(description).toBeVisible();
  });

  test('should have character counter', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Check for character counter
    await expect(page.locator('text=/\\d+\\/50 minimum characters/')).toBeVisible();
  });

  test('should have continue button', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Check for continue button
    await expect(page.locator('button:has-text("Продължи →")')).toBeVisible();
  });

  test('should have skip option', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Check for skip button
    await expect(page.locator('button:has-text("Пропусни за сега")')).toBeVisible();
  });

  test('should show time hint', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Check for time hint
    await expect(page.locator('text=Отнема по-малко от 1 минута')).toBeVisible();
  });

  test('should have photo upload functionality', async ({ page }) => {
    await page.goto('/bg/provider/dashboard');
    
    // Check for upload button and file input
    await expect(page.locator('button:has-text("Качи снимка")')).toBeVisible();
    await expect(page.locator('input[type="file"]')).toBeVisible();
  });
});
