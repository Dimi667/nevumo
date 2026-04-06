const { chromium } = require('playwright');

const logs = [];
const consoleErrors = [];

async function debugFormSubmission() {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

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
      console.log('--- NETWORK REQUEST ---');
      console.log('URL:', request.url());
      console.log('Method:', request.method());
      console.log('Request Body:', postData);
    }

    // Continue and capture response
    const response = await route.fetch();
    log.responseStatus = response.status();
    const responseBody = await response.text();
    log.responseBody = responseBody;

    console.log('--- NETWORK RESPONSE ---');
    console.log('Status:', response.status());
    console.log('Response Body:', responseBody);

    logs.push(log);
    await route.fulfill({ response });
  });

  console.log('=== STEP 1: Navigate to page ===');
  await page.goto('http://localhost:3000/bg/warszawa/sprzatanie');
  await page.waitForTimeout(3000);

  console.log('=== STEP 2: First form submission ===');
  
  // Find phone input and scroll into view
  const phoneInput = await page.locator('input[type="tel"]').first();
  await phoneInput.scrollIntoViewIfNeeded();
  await phoneInput.waitFor({ state: 'visible' });
  await phoneInput.fill('+48 700 100 200', { force: true });
  console.log('Filled phone: +48 700 100 200');

  // Find and click submit button
  const submitButton = await page.locator('button[type="submit"]').first();
  await submitButton.click({ force: true });
  console.log('Clicked submit button');

  await page.waitForTimeout(3000);

  // Check for success screen
  const successText = await page.locator('text=Запитването е изпратено').first();
  const isSuccessVisible = await successText.isVisible().catch(() => false);
  console.log('First submission success visible:', isSuccessVisible);

  console.log('=== STEP 3: Click No thanks ===');
  const noThanksButton = await page.locator('text=No thanks, text=Не благодаря').first();
  await noThanksButton.click();
  console.log('Clicked No thanks');

  await page.waitForTimeout(2000);

  // Check form is visible again
  const formVisible = await phoneInput.isVisible().catch(() => false);
  console.log('Form visible after reset:', formVisible);

  console.log('=== STEP 4: Second form submission ===');
  
  // Fill with different phone
  await phoneInput.scrollIntoViewIfNeeded();
  await phoneInput.waitFor({ state: 'visible' });
  await phoneInput.fill('+48 700 100 333', { force: true });
  console.log('Filled phone: +48 700 100 333');

  await submitButton.click({ force: true });
  console.log('Clicked submit button (second time)');

  await page.waitForTimeout(3000);

  console.log('=== CAPTURE SCREEN STATE ===');
  const pageContent = await page.content();
  const visibleText = await page.locator('body').innerText();
  console.log('Current page text:', visibleText.substring(0, 1000));

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

  await browser.close();
}

debugFormSubmission().catch(console.error);
