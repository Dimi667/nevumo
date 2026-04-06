const { chromium } = require('playwright');

const FRONTEND = 'http://localhost:3000';
const EMAIL = 'lili@test.bg';
const PASSWORD = '123456789';

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  // Enable console logging
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('request', req => console.log('REQUEST:', req.url()));
  page.on('response', res => console.log('RESPONSE:', res.url(), res.status()));

  // Login
  console.log('Navigating to auth page...');
  await page.goto(`${FRONTEND}/en/auth`, { timeout: 30000 });
  await page.waitForTimeout(3000);
  
  // Check if we're on auth page
  const currentUrl = page.url();
  console.log('Current URL after navigation:', currentUrl);
  
  // Try manual login
  const emailInput = await page.locator('input[type="email"]').first();
  const isVisible = await emailInput.isVisible();
  console.log('Email input visible:', isVisible);
  
  if (isVisible) {
    await emailInput.fill(EMAIL);
    await emailInput.press('Enter');
    await page.waitForTimeout(2000);
    
    // Check for password input
    const passwordInput = await page.locator('input[type="password"]').first();
    const passwordVisible = await passwordInput.isVisible();
    console.log('Password input visible:', passwordVisible);
    
    if (passwordVisible) {
      await passwordInput.fill(PASSWORD);
      await passwordInput.press('Enter');
      await page.waitForTimeout(5000);
      
      // Check login result
      const token = await page.evaluate(() => localStorage.getItem('nevumo_auth_token'));
      const user = await page.evaluate(() => {
        const userRaw = localStorage.getItem('nevumo_auth_user');
        return userRaw ? JSON.parse(userRaw) : null;
      });
      
      console.log('Login result - Token exists:', !!token);
      console.log('Login result - User:', user);
      
      // Navigate to settings
      console.log('Navigating to settings...');
      await page.goto(`${FRONTEND}/en/provider/dashboard/settings`, { timeout: 30000 });
      await page.waitForTimeout(3000);
      
      const settingsUrl = page.url();
      console.log('Settings URL:', settingsUrl);
      
      // Check for phone input
      const phoneInputs = await page.locator('input[type="tel"]').count();
      console.log(`Found ${phoneInputs} phone inputs on settings page`);
      
      // Take screenshot
      await page.screenshot({ path: 'debug-settings3.png', fullPage: true });
    }
  }
  
  await browser.close();
})();
