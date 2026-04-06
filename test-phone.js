const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const FRONTEND = 'http://localhost:3000';
const BACKEND = 'http://localhost:8000';
const EMAIL = 'lili@test.bg';
const PASSWORD = '123456789';
const PHONE1 = '+48 123 456 789';
const PHONE2 = '+48 999 888 777';
const outDir = path.join(process.cwd(), 'test-results');
fs.mkdirSync(outDir, { recursive: true });

const results = [];

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  // TEST 1: Anonymous - localStorage
  try {
    await page.goto(`${FRONTEND}/pl/warszawa/sprzatanie`, { timeout: 30000 });
    await page.waitForTimeout(2000);
    const phoneInput = page.locator('input[type="tel"]').first();
    await phoneInput.fill(PHONE1);
    const stored = await page.evaluate(() => localStorage.getItem('nevumo_phone'));
    const pass = stored === PHONE1;
    results.push({ test: 'TEST 1: localStorage persistence', pass, stored });
    await page.screenshot({ path: path.join(outDir, 'test1.png') });
  } catch(e) { results.push({ test: 'TEST 1', pass: false, error: e.message }); }

  // TEST 2: Auto-fill on second visit
  try {
    await page.goto(`${FRONTEND}/pl/warszawa/hydraulik`, { timeout: 30000 });
    await page.waitForTimeout(2000);
    const val = await page.locator('input[type="tel"]').first().inputValue();
    const pass = val === PHONE1;
    results.push({ test: 'TEST 2: Auto-fill second visit', pass, value: val });
    await page.screenshot({ path: path.join(outDir, 'test2.png') });
  } catch(e) { results.push({ test: 'TEST 2', pass: false, error: e.message }); }

  // TEST 3: Login and DB sync
  try {
    await page.goto(`${FRONTEND}/en/auth`, { timeout: 30000 });
    await page.waitForTimeout(2000);
    await page.locator('input[type="email"]').first().fill(EMAIL);
    await page.locator('input[type="email"]').first().press('Enter');
    await page.waitForTimeout(1000);
    await page.locator('input[type="password"]').first().fill(PASSWORD);
    await page.locator('input[type="password"]').first().press('Enter');
    await page.waitForTimeout(3000);
    await page.goto(`${FRONTEND}/en/provider/dashboard/settings`, { timeout: 30000 });
    await page.waitForTimeout(2000);
    const val = await page.locator('input[type="tel"]').first().inputValue();
    const token = await page.evaluate(() => localStorage.getItem('nevumo_auth_token'));
    results.push({ test: 'TEST 3: Login + phone in settings', pass: val.length > 0, value: val, hasToken: !!token });
    await page.screenshot({ path: path.join(outDir, 'test3.png') });
  } catch(e) { results.push({ test: 'TEST 3', pass: false, error: e.message }); }

  // TEST 4: API verification
  try {
    const token = await page.evaluate(() => localStorage.getItem('nevumo_auth_token'));
    const data = await page.evaluate(async ({ BACKEND, token }) => {
      const res = await fetch(`${BACKEND}/api/v1/user/profile`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      return res.json();
    }, { BACKEND, token });
    const pass = data?.data?.phone === PHONE1;
    results.push({ test: 'TEST 4: API phone value', pass, phone: data?.data?.phone });
  } catch(e) { results.push({ test: 'TEST 4', pass: false, error: e.message }); }

  // TEST 5: Update phone from settings
  try {
    await page.goto(`${FRONTEND}/en/provider/dashboard/settings`, { timeout: 30000 });
    await page.waitForTimeout(2000);
    await page.locator('input[type="tel"]').first().fill(PHONE2);
    await page.getByRole('button', { name: /save/i }).first().click();
    await page.waitForTimeout(2000);
    const token = await page.evaluate(() => localStorage.getItem('nevumo_auth_token'));
    const data = await page.evaluate(async ({ BACKEND, token }) => {
      const res = await fetch(`${BACKEND}/api/v1/user/profile`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      return res.json();
    }, { BACKEND, token });
    const pass = data?.data?.phone === PHONE2;
    results.push({ test: 'TEST 5: Update phone', pass, phone: data?.data?.phone });
    await page.screenshot({ path: path.join(outDir, 'test5.png') });
  } catch(e) { results.push({ test: 'TEST 5', pass: false, error: e.message }); }

  await browser.close();

  console.log('\n=== RESULTS ===');
  for (const r of results) {
    console.log(`${r.pass ? 'PASS' : 'FAIL'} - ${r.test}`);
    if (!r.pass) console.log('  Details:', JSON.stringify(r));
  }
})();
