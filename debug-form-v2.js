const { chromium } = require('playwright');

const logs = [];
const consoleErrors = [];

async function debugFormSubmission() {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.setViewportSize({ width: 1280, height: 800 });

  // Intercept console errors
  page.on('console', (msg) => {
    if (msg.type() === 'error') {
      const errorText = `[${new Date().toISOString()}] ${msg.type()}: ${msg.text()}`;
      consoleErrors.push(errorText);
      console.log('CONSOLE ERROR:', errorText);
    }
  });

  // Intercept network requests
  await page.route('http://localhost:8000/api/v1/leads', async (route, request) => {
    const log = {
      url: request.url(),
      method: request.method(),
      timestamp: new Date().toISOString(),
    };

    const postData = request.postData();
    if (postData) {
      log.requestBody = postData;
      console.log('');
      console.log('=== NETWORK REQUEST ===');
      console.log('URL:', request.url());
      console.log('Method:', request.method());
      console.log('Request Body:', postData);
    }

    // Continue and capture response
    const response = await route.fetch();
    log.responseStatus = response.status();
    const responseBody = await response.text();
    log.responseBody = responseBody;

    console.log('=== NETWORK RESPONSE ===');
    console.log('Status:', response.status());
    console.log('Response Body:', responseBody);
    console.log('');

    logs.push(log);
    await route.fulfill({ response });
  });

  console.log('=== STEP 1: Navigate to page ===');
  await page.goto('http://localhost:3000/bg/warszawa/sprzatanie');
  await page.waitForTimeout(3000);

  // Scroll down to find the form
  console.log('Scrolling to find form...');
  await page.evaluate(() => window.scrollTo(0, 800));
  await page.waitForTimeout(1000);

  console.log('=== STEP 2: First form submission ===');
  
  // Fill phone using evaluate
  await page.evaluate((phone) => {
    const input = document.querySelector('input[type="tel"]');
    if (input) {
      input.value = phone;
      input.dispatchEvent(new Event('input', { bubbles: true }));
      input.dispatchEvent(new Event('change', { bubbles: true }));
    }
  }, '+48 700 100 200');
  console.log('Filled phone: +48 700 100 200');

  // Click submit
  await page.evaluate(() => {
    const btn = document.querySelector('button[type="submit"]');
    if (btn) btn.click();
  });
  console.log('Clicked submit button');

  await page.waitForTimeout(3000);

  // Check for success screen
  const successText = await page.locator('text=Запитването е изпратено').first().isVisible().catch(() => false);
  console.log('First submission success visible:', successText);

  console.log('=== STEP 3: Click No thanks ===');
  await page.evaluate(() => {
    const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent?.includes('thanks'));
    if (btn) btn.click();
  });
  console.log('Clicked No thanks');

  await page.waitForTimeout(2000);

  // Check form is visible again
  const phoneInputExists = await page.locator('input[type="tel"]').first().isVisible().catch(() => false);
  console.log('Form visible after reset:', phoneInputExists);

  console.log('=== STEP 4: Second form submission ===');
  
  // Fill with different phone
  await page.evaluate((phone) => {
    const input = document.querySelector('input[type="tel"]');
    if (input) {
      input.value = phone;
      input.dispatchEvent(new Event('input', { bubbles: true }));
      input.dispatchEvent(new Event('change', { bubbles: true }));
    }
  }, '+48 700 100 333');
  console.log('Filled phone: +48 700 100 333');

  // Click submit
  await page.evaluate(() => {
    const btn = document.querySelector('button[type="submit"]');
    if (btn) btn.click();
  });
  console.log('Clicked submit button (second time)');

  await page.waitForTimeout(3000);

  console.log('=== CAPTURE SCREEN STATE ===');
  const visibleText = await page.locator('body').innerText();
  console.log('Current page text (first 2000 chars):');
  console.log(visibleText.substring(0, 2000));

  console.log('');
  console.log('=== NETWORK LOGS SUMMARY ===');
  logs.forEach((log, idx) => {
    console.log(`\n--- Request ${idx + 1} ---`);
    console.log('URL:', log.url);
    console.log('Method:', log.method);
    console.log('Request Body:', log.requestBody);
    console.log('Response Status:', log.responseStatus);
    console.log('Response Body:', log.responseBody);
  });

  console.log('\n=== CONSOLE ERRORS ===');
  if (consoleErrors.length === 0) {
    console.log('No console errors captured');
  } else {
    consoleErrors.forEach(e => console.log(e));
  }

  // Take screenshot for debugging
  await page.screenshot({ path: '/Users/dimitardimitrov/nevumo/debug-screenshot.png' });
  console.log('\nScreenshot saved to debug-screenshot.png');

  await browser.close();
}

debugFormSubmission().catch(console.error);
