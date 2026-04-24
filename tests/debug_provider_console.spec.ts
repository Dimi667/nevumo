import { test } from '@playwright/test';

test('capture console errors on lead button clicks', async ({ page, request }) => {
  const errors: string[] = [];
  page.on('console', msg => {
    const text = msg.text();
    if (msg.type() === 'error' || text.includes('Error') || text.includes('NETWORK') || text.includes('PATCH') || text.includes('failed') || text.includes('transition') || text.includes('invalid')) {
      errors.push(`[${msg.type()}] ${text}`);
    }
  });

  // Get token via API request (not page.evaluate)
  const loginRes = await request.post('http://192.168.0.15:8000/api/v1/auth/login', {
    data: { email: 'lili@test.bg', password: '123456789' }
  });
  const loginData = await loginRes.json();
  const token = loginData?.data?.token;
  if (!token) { console.log('LOGIN FAILED'); return; }
  console.log('TOKEN OK');

  // Inject token before page load
  await page.addInitScript((t: string) => {
    localStorage.setItem('nevumo_auth_token', t);
    localStorage.setItem('nevumo_auth_user', JSON.stringify({ role: 'provider' }));
  }, token);

  await page.goto('http://192.168.0.15:3000/bg/provider/dashboard/leads');
  await page.waitForTimeout(4000);

  // Count buttons
  const contactBtns = page.locator('button').filter({ hasText: /Свържи се/i });
  const rejectBtns = page.locator('button').filter({ hasText: /Отхвърли/i });
  const c1 = await contactBtns.count();
  const r1 = await rejectBtns.count();
  console.log('CONTACT BUTTONS:', c1, '| REJECT BUTTONS:', r1);

  if (c1 === 0 && r1 === 0) { console.log('NO BUTTONS FOUND - check page loaded'); return; }

  // Click 1st contact button
  if (c1 > 0) {
    errors.length = 0;
    await contactBtns.first().click();
    await page.waitForTimeout(2000);
    console.log('=== AFTER 1ST CLICK errors:', JSON.stringify(errors));
    const c2 = await contactBtns.count();
    console.log('CONTACT BUTTONS AFTER 1ST CLICK:', c2);

    // Click 2nd contact button  
    if (c2 > 0) {
      errors.length = 0;
      await contactBtns.first().click();
      await page.waitForTimeout(2000);
      console.log('=== AFTER 2ND CLICK errors:', JSON.stringify(errors));
    }
  }

  // Click reject button
  const r2 = await rejectBtns.count();
  if (r2 > 0) {
    errors.length = 0;
    await rejectBtns.first().click();
    await page.waitForTimeout(2000);
    console.log('=== AFTER REJECT CLICK errors:', JSON.stringify(errors));
  }
});
