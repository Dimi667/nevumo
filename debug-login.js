const { chromium } = require('playwright');

const FRONTEND = 'http://localhost:3000';
const EMAIL = 'lili@test.bg';
const PASSWORD = '123456789';

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  // Navigate to auth page
  await page.goto(`${FRONTEND}/en/auth`, { timeout: 30000 });
  await page.waitForTimeout(2000);
  
  // Take screenshot to see the page
  await page.screenshot({ path: 'debug-auth.png', fullPage: true });
  
  // Check if email input exists
  const emailInputs = await page.locator('input[type="email"]').count();
  console.log(`Found ${emailInputs} email inputs`);
  
  // Check if password input exists
  const passwordInputs = await page.locator('input[type="password"]').count();
  console.log(`Found ${passwordInputs} password inputs`);
  
  // Try to fill and submit
  if (emailInputs > 0) {
    await page.locator('input[type="email"]').first().fill(EMAIL);
    await page.locator('input[type="email"]').first().press('Enter');
    await page.waitForTimeout(1000);
    
    if (passwordInputs > 0) {
      await page.locator('input[type="password"]').first().fill(PASSWORD);
      await page.locator('input[type="password"]').first().press('Enter');
      await page.waitForTimeout(3000);
      
      // Check if login succeeded
      const token = await page.evaluate(() => localStorage.getItem('nevumo_auth_token'));
      const user = await page.evaluate(() => {
        const userRaw = localStorage.getItem('nevumo_auth_user');
        return userRaw ? JSON.parse(userRaw) : null;
      });
      
      console.log('Token exists:', !!token);
      console.log('User:', user);
      
      // Check current URL
      const currentUrl = page.url();
      console.log('Current URL:', currentUrl);
    }
  }
  
  await browser.close();
})();
