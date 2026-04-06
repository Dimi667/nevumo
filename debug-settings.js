const { chromium } = require('playwright');

const FRONTEND = 'http://localhost:3000';
const EMAIL = 'lili@test.bg';
const PASSWORD = '123456789';

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  // Login
  await page.goto(`${FRONTEND}/en/auth`, { timeout: 30000 });
  await page.waitForTimeout(2000);
  await page.locator('input[type="email"]').first().fill(EMAIL);
  await page.locator('input[type="email"]').first().press('Enter');
  await page.waitForTimeout(1000);
  await page.locator('input[type="password"]').first().fill(PASSWORD);
  await page.locator('input[type="password"]').first().press('Enter');
  await page.waitForTimeout(3000);
  
  // Navigate to settings
  await page.goto(`${FRONTEND}/en/provider/dashboard/settings`, { timeout: 30000 });
  await page.waitForTimeout(2000);
  
  // Take screenshot
  await page.screenshot({ path: 'debug-settings.png', fullPage: true });
  
  // Check for phone inputs
  const phoneInputs = await page.locator('input[type="tel"]').count();
  console.log(`Found ${phoneInputs} phone inputs on settings page`);
  
  // Check all inputs
  const allInputs = await page.locator('input').count();
  console.log(`Found ${allInputs} total inputs on settings page`);
  
  // Get page content
  const content = await page.content();
  console.log('Page contains phone input:', content.includes('type="tel"'));
  console.log('Page contains PhoneInput:', content.includes('PhoneInput'));
  console.log('Page contains phone:', content.includes('phone'));
  
  await browser.close();
})();
