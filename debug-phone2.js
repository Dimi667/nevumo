const { chromium } = require('playwright');

const FRONTEND = 'http://localhost:3000';
const PHONE1 = '+48 123 456 789';

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  // Navigate to a category page
  await page.goto(`${FRONTEND}/pl/warszawa/sprzatanie`, { timeout: 30000 });
  await page.waitForTimeout(3000);
  
  // Check phone input
  const phoneInput = page.locator('input[type="tel"]').first();
  const isVisible = await phoneInput.isVisible();
  console.log('Phone input visible:', isVisible);
  
  if (isVisible) {
    // Fill the phone input
    await phoneInput.fill(PHONE1);
    console.log('Filled phone with:', PHONE1);
    
    // Check localStorage immediately
    const stored1 = await page.evaluate(() => localStorage.getItem('nevumo_phone'));
    console.log('localStorage after fill:', stored1);
    
    // Trigger change event
    await phoneInput.dispatchEvent('change');
    console.log('Triggered change event');
    
    // Check localStorage again
    const stored2 = await page.evaluate(() => localStorage.getItem('nevumo_phone'));
    console.log('localStorage after change event:', stored2);
    
    // Wait a bit and check again
    await page.waitForTimeout(2000);
    const stored3 = await page.evaluate(() => localStorage.getItem('nevumo_phone'));
    console.log('localStorage after 2 seconds:', stored3);
    
    // Check current input value
    const currentValue = await phoneInput.inputValue();
    console.log('Current input value:', currentValue);
  }
  
  await browser.close();
})();
