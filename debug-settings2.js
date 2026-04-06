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
  
  // Check user info
  const user = await page.evaluate(() => {
    const userRaw = localStorage.getItem('nevumo_auth_user');
    return userRaw ? JSON.parse(userRaw) : null;
  });
  console.log('User:', JSON.stringify(user, null, 2));
  
  // Navigate to settings
  await page.goto(`${FRONTEND}/en/provider/dashboard/settings`, { timeout: 30000 });
  await page.waitForTimeout(2000);
  
  // Check page content
  const pageTitle = await page.title();
  console.log('Page title:', pageTitle);
  
  const pageText = await page.locator('body').textContent();
  console.log('Page contains "Settings":', pageText.includes('Settings'));
  console.log('Page contains "Phone":', pageText.includes('Phone'));
  console.log('Page contains "Account":', pageText.includes('Account'));
  
  // Take screenshot
  await page.screenshot({ path: 'debug-settings2.png', fullPage: true });
  
  await browser.close();
})();
