const { chromium } = require('playwright');

const FRONTEND = 'http://localhost:3000';
const BACKEND = 'http://localhost:8000';
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
  
  // Get token
  const token = await page.evaluate(() => localStorage.getItem('nevumo_auth_token'));
  console.log('Token:', token ? 'exists' : 'missing');
  
  // Test API call
  try {
    const data = await page.evaluate(async ({ BACKEND, token }) => {
      console.log('Making API call to:', `${BACKEND}/api/v1/user/profile`);
      console.log('Token:', token);
      
      const res = await fetch(`${BACKEND}/api/v1/user/profile`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      console.log('Response status:', res.status);
      console.log('Response ok:', res.ok);
      
      if (!res.ok) {
        const errorText = await res.text();
        console.log('Error response:', errorText);
        return { error: errorText, status: res.status };
      }
      
      return res.json();
    }, { BACKEND, token });
    
    console.log('API result:', JSON.stringify(data, null, 2));
  } catch (error) {
    console.log('API error:', error.message);
  }
  
  await browser.close();
})();
