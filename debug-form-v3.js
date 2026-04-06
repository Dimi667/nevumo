const { chromium } = require('playwright');

const logs = [];
const consoleErrors = [];

async function debugFormSubmission() {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.setViewportSize({ width: 1280, height: 900 });

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
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(1000);

  console.log('=== STEP 2: First form submission ===');
  
  // Wait for phone input and fill
  const phoneInput = page.locator('input[type="tel"]').first();
  await phoneInput.waitFor({ state: 'attached' });
  await phoneInput.fill('+48 700 100 200', { force: true });
  console.log('Filled phone: +48 700 100 200');

  // Wait for submit button and click
  const submitButton = page.locator('button[type="submit"]').first();
  await submitButton.waitFor({ state: 'attached' });
  await submitButton.click({ force: true });
  console.log('Clicked submit button');

  await page.waitForTimeout(3000);

  // Check for success screen - look for the green checkmark or success text
  const hasSuccess = await page.locator('text=Запитването е изпратено').count() > 0 || 
                     await page.locator('.bg-green-100').count() > 0;
  console.log('First submission success indicators found:', hasSuccess);

  // Take screenshot after first submit
  await page.screenshot({ path: '/Users/dimitardimitrov/nevumo/debug-after-first-submit.png' });

  console.log('=== STEP 3: Click No thanks ===');
  
  // Look for "No thanks" button by text
  const noThanksButton = page.getByText(/No thanks|Не благодаря/i);
  const noThanksCount = await noThanksButton.count();
  console.log('No thanks buttons found:', noThanksCount);
  
  if (noThanksCount > 0) {
    await noThanksButton.first().click({ force: true });
    console.log('Clicked No thanks');
  } else {
    console.log('No "No thanks" button found - checking page content');
    const bodyText = await page.locator('body').innerText();
    console.log('Page text snippet:', bodyText.substring(0, 500));
  }

  await page.waitForTimeout(2000);

  // Take screenshot after No thanks
  await page.screenshot({ path: '/Users/dimitardimitrov/nevumo/debug-after-no-thanks.png' });

  // Check form is back
  const phoneVisible = await phoneInput.isVisible().catch(() => false);
  console.log('Phone input visible after reset:', phoneVisible);

  console.log('=== STEP 4: Second form submission ===');
  
  if (phoneVisible) {
    // Fill with different phone
    await phoneInput.fill('+48 700 100 333', { force: true });
    console.log('Filled phone: +48 700 100 333');

    // Click submit
    await submitButton.click({ force: true });
    console.log('Clicked submit button (second time)');

    await page.waitForTimeout(3000);
  } else {
    console.log('Phone input not visible - cannot submit second time');
  }

  // Take screenshot after second submit
  await page.screenshot({ path: '/Users/dimitardimitrov/nevumo/debug-after-second-submit.png' });

  console.log('=== CAPTURE SCREEN STATE ===');
  const visibleText = await page.locator('body').innerText();
  console.log('Current page text (first 2000 chars):');
  console.log(visibleText.substring(0, 2000));

  console.log('');
  console.log('=== NETWORK LOGS SUMMARY ===');
  if (logs.length === 0) {
    console.log('No network requests to /api/v1/leads were captured');
  } else {
    logs.forEach((log, idx) => {
      console.log(`\n--- Request ${idx + 1} ---`);
      console.log('URL:', log.url);
      console.log('Method:', log.method);
      console.log('Request Body:', log.requestBody);
      console.log('Response Status:', log.responseStatus);
      console.log('Response Body:', log.responseBody);
    });
  }

  console.log('\n=== CONSOLE ERRORS ===');
  if (consoleErrors.length === 0) {
    console.log('No console errors captured');
  } else {
    consoleErrors.forEach(e => console.log(e));
  }

  // Final screenshot
  await page.screenshot({ path: '/Users/dimitardimitrov/nevumo/debug-final.png' });
  console.log('\nScreenshots saved:');
  console.log('- debug-after-first-submit.png');
  console.log('- debug-after-no-thanks.png');
  console.log('- debug-after-second-submit.png');
  console.log('- debug-final.png');

  await browser.close();
}

debugFormSubmission().catch(console.error);
