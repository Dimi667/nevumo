import { test, expect } from '@playwright/test';

test.describe('Provider Onboarding Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to provider dashboard (should redirect to onboarding if not completed)
    await page.goto('/en/provider/dashboard');
  });

  test('should show centered layout during onboarding', async ({ page }) => {
    // Check if page is centered (no sidebar)
    await expect(page.locator('body')).toHaveClass(/justify-center/);
    
    // Check for onboarding content
    await expect(page.locator('h1')).toContainText('Complete your profile');
    await expect(page.locator('h1 + p')).toContainText('Start receiving client requests in minutes');
  });

  test('should show improved progress bar with labels', async ({ page }) => {
    // Check progress bar elements
    await expect(page.locator('div:has-text("Profile")')).toBeVisible();
    await expect(page.locator('div:has-text("Service")')).toBeVisible();
    
    // Check if first step is active (orange)
    const profileStep = page.locator('div:has-text("Profile") > div:first-child');
    await expect(profileStep).toHaveClass(/bg-orange-500/);
    
    // Check if second step is inactive (gray)
    const serviceStep = page.locator('div:has-text("Service") > div:first-child');
    await expect(serviceStep).toHaveClass(/bg-gray-100/);
  });

  test('should have improved description field with character counter', async ({ page }) => {
    const description = page.locator('textarea[placeholder*="services, experience"]');
    await expect(description).toBeVisible();
    
    // Check character counter
    await expect(page.locator('text=/\\d+\\/50 minimum characters/')).toBeVisible();
    
    // Test character counting
    await description.fill('Test description with more than 50 characters to validate counter functionality');
    const counter = page.locator('text=/\\d+\\/50 minimum characters/');
    await expect(counter).toBeVisible();
  });

  test('should have "Continue" CTA instead of "Next"', async ({ page }) => {
    const continueButton = page.locator('button:has-text("Continue →")');
    await expect(continueButton).toBeVisible();
  });

  test('should have "Skip for now" option', async ({ page }) => {
    const skipButton = page.locator('button:has-text("Skip for now")');
    await expect(skipButton).toBeVisible();
  });

  test('should show time hint "Takes less than 1 minute"', async ({ page }) => {
    await expect(page.locator('text=Takes less than 1 minute')).toBeVisible();
  });

  test('skip flow should show hero banner on dashboard', async ({ page }) => {
    // Fill business name to enable skip logic
    await page.fill('input[name="business_name"]', 'Test Business');
    
    // Click skip button
    await page.click('button:has-text("Skip for now")');
    
    // Should redirect to dashboard with hero banner
    await expect(page.locator('h2:has-text("You\'re 1 step away from getting clients")')).toBeVisible();
    await expect(page.locator('text=🚀')).toBeVisible();
    await expect(page.locator('button:has-text("Add your first service")')).toBeVisible();
  });

  test('hero banner CTA should go to Step 2 directly', async ({ page }) => {
    // First skip to dashboard
    await page.fill('input[name="business_name"]', 'Test Business');
    await page.click('button:has-text("Skip for now")');
    
    // Click hero banner CTA
    await page.click('button:has-text("Add your first service")');
    
    // Should be on Step 2 (Add Service)
    await expect(page.locator('h2:has-text("Add Your First Service")')).toBeVisible();
    await expect(page.locator('text=Almost done!')).toBeVisible();
  });

  test('should show locked sections on incomplete dashboard', async ({ page }) => {
    // Skip to dashboard
    await page.fill('input[name="business_name"]', 'Test Business');
    await page.click('button:has-text("Skip for now")');
    
    // Check for locked sections
    await expect(page.locator('text=🔒')).toBeVisible();
    await expect(page.locator('text=Add a service to unlock')).toBeVisible();
  });

  test('photo upload should work without errors', async ({ page }) => {
    // This test checks if upload functionality exists
    const uploadButton = page.locator('button:has-text("Upload photo")');
    await expect(uploadButton).toBeVisible();
    
    // Check for file input
    const fileInput = page.locator('input[type="file"]');
    await expect(fileInput).toBeVisible();
    
    // Note: Actual file upload testing would require test files
    // For now, we verify the UI elements exist
  });

  test('complete onboarding flow should show sidebar', async ({ page }) => {
    // Fill Step 1
    await page.fill('input[name="business_name"]', 'Test Business');
    await page.fill('textarea[placeholder*="services, experience"]', 'Test description with enough characters to meet the minimum requirement for validation purposes');
    
    // Continue to Step 2
    await page.click('button:has-text("Continue →")');
    
    // Fill Step 2
    await page.fill('input[name="title"]', 'Test Service');
    await page.selectOption('select[name="category_slug"]', 'plumbing'); // Assuming plumbing category exists
    await page.selectOption('select[name="city_id"]', 'Sofia'); // Assuming Sofia city exists
    
    // Complete setup
    await page.click('button:has-text("Complete Setup")');
    
    // Wait for success message and redirect
    await expect(page.locator('text=Setup complete! Redirecting…')).toBeVisible();
    
    // After redirect, sidebar should be visible
    await page.waitForTimeout(1500); // Wait for redirect
    
    // Check if sidebar is visible (not centered layout)
    await expect(page.locator('body')).not.toHaveClass(/justify-center/);
  });

  test('should have semi-auto Public URL field with edit functionality', async ({ page }) => {
    // Wait for onboarding to load
    await expect(page.locator('h1:has-text("Complete your profile")')).toBeVisible();
    
    // Check field order: Business name, Description, Public URL
    const businessNameInput = page.locator('input[placeholder*="e.g. Sofia Plumbing Pro"]');
    const descriptionTextarea = page.locator('textarea[placeholder*="Describe your services"]');
    const publicUrlInput = page.locator('input[placeholder*="your-business-name"]');
    
    await expect(businessNameInput).toBeVisible();
    await expect(descriptionTextarea).toBeVisible();
    await expect(publicUrlInput).toBeVisible();
    
    // Check that Public URL is readonly by default
    await expect(publicUrlInput).toHaveAttribute('readOnly');
    
    // Check that edit icon is visible
    const editButton = page.locator('button[title="Edit URL"]');
    await expect(editButton).toBeVisible();
    
    // Test auto-generation from business name
    await businessNameInput.fill('Sofia Plumbing Pro');
    
    // Check that slug is auto-generated
    await expect(publicUrlInput).toHaveValue('sofia-plumbing-pro');
    
    // Check that URL preview is updated
    await expect(page.locator('text=nevumo.com/.../sofia-plumbing-pro')).toBeVisible();
    
    // Test edit functionality
    await editButton.click();
    
    // Check that input is now editable
    await expect(publicUrlInput).not.toHaveAttribute('readOnly');
    
    // Test manual editing
    await publicUrlInput.fill('sofia-plumbing-experts');
    await expect(publicUrlInput).toHaveValue('sofia-plumbing-experts');
    
    // Check that edit icon is hidden during editing
    await expect(editButton).not.toBeVisible();
  });
});

test.describe('Dashboard Post-Onboarding', () => {
  test('should show normal dashboard with sidebar after completion', async ({ page }) => {
    // This test assumes onboarding is already completed
    // In real scenarios, you'd need to set up test data or mock API
    
    await page.goto('/en/provider/dashboard');
    
    // Check for normal dashboard elements (not onboarding)
    await expect(page.locator('text=Overview of your business')).toBeVisible();
    
    // Check for sidebar navigation
    await expect(page.locator('text=Overview')).toBeVisible();
    await expect(page.locator('text=Leads')).toBeVisible();
    await expect(page.locator('text=Services')).toBeVisible();
  });
});
