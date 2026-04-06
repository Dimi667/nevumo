const { chromium } = require('playwright');

const FRONTEND = 'http://localhost:3000';

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  // Navigate to a category page
  await page.goto(`${FRONTEND}/pl/warszawa/sprzatanie`, { timeout: 30000 });
  await page.waitForTimeout(3000);
  
  // Take a screenshot to see what's on the page
  await page.screenshot({ path: 'debug-page.png', fullPage: true });
  
  // Check for phone inputs
  const phoneInputs = await page.locator('input[type="tel"]').count();
  console.log(`Found ${phoneInputs} phone inputs`);
  
  // Check all inputs
  const allInputs = await page.locator('input').count();
  console.log(`Found ${allInputs} total inputs`);
  
  // Get page content to debug
  const content = await page.content();
  console.log('Page contains phone input:', content.includes('type="tel"'));
  console.log('Page contains PhoneInput:', content.includes('PhoneInput'));
  
  await browser.close();
})();
