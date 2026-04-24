import { test, expect } from '@playwright/test';

test.describe('Lead Reject Test', () => {
  test('should reject first New lead and capture PATCH request', async ({ page }) => {
    test.setTimeout(60000);
    const baseURL = 'http://192.168.0.15:3000';
    
    // 1. Open login page directly
    await page.goto(`${baseURL}/bg/login`);
    
    // 2. Log in as provider (if not already logged in)
    const emailInput = page.locator('input[type="email"]');
    if (await emailInput.isVisible()) {
      await emailInput.fill('lili@test.bg');
      await page.fill('input[type="password"]', '123456789');
      await page.click('button[type="submit"]');
      await page.waitForURL(/.*provider\/dashboard.*/, { timeout: 15000 });
    }
    
    // 3. Go to Leads page and filter by "New" status
    await page.goto(`${baseURL}/bg/provider/dashboard/leads?status=new`);
    await page.waitForLoadState('networkidle');
    
    // Debug: Take screenshot and check page content
    console.log('Current URL:', page.url());
    await page.screenshot({ path: 'test-debug-leads-page.png' });
    
    // Check if any rows exist in the table
    const allRows = page.locator('tbody tr');
    const rowCount = await allRows.count();
    console.log('Total rows in table:', rowCount);
    
    // Check if "Ново" text exists anywhere on page
    const hasNewoText = await page.locator('text=Ново').count();
    console.log('Count of "Ново" text on page:', hasNewoText);
    
    // 4. Find the first lead with status "Ново" (New in Bulgarian)
    const newLeadRow = page.locator('tr').filter({ hasText: 'Ново' }).first();
    const newLeadCount = await newLeadRow.count();
    console.log('Count of rows with "Ново":', newLeadCount);
    
    if (newLeadCount === 0) {
      console.log('No leads with "Ново" status found. Checking all statuses...');
      // List all visible status texts
      const statusCells = page.locator('td:nth-child(6)');
      const statusCount = await statusCells.count();
      for (let i = 0; i < Math.min(statusCount, 5); i++) {
        const statusText = await statusCells.nth(i).textContent();
        console.log(`Status ${i}:`, statusText);
      }
    }
    
    await expect(newLeadRow).toBeVisible();
    
    // Store the lead row for later verification
    const leadRowBefore = await newLeadRow.innerHTML();
    
    // 5. Find and click "Отхвърли" (Reject in Bulgarian) button in that row
    const rejectButton = newLeadRow.locator('button:has-text("Отхвърли")').first();
    await expect(rejectButton).toBeVisible();
    
    // 6. Capture PATCH request
    let patchRequestUrl: string | null = null;
    let patchResponseStatus: number | null = null;
    let patchResponseBody: string | null = null;
    
    page.on('request', request => {
      if (request.method() === 'PATCH') {
        patchRequestUrl = request.url();
      }
    });
    
    page.on('response', async response => {
      if (response.request().method() === 'PATCH') {
        patchResponseStatus = response.status();
        patchResponseBody = await response.text();
      }
    });
    
    // Click the reject button
    await rejectButton.click();
    
    // Wait for the PATCH request to complete
    await page.waitForTimeout(2000);
    
    // Log the PATCH request details
    console.log('=== PATCH Request Details ===');
    console.log('URL:', patchRequestUrl);
    console.log('HTTP Status:', patchResponseStatus);
    console.log('Response Body:', patchResponseBody);
    console.log('============================');
    
    // 7. Check if the status in UI changed
    await page.waitForTimeout(1000);
    
    // Verify the lead status is no longer "New" or is now "Rejected"
    const leadRowAfter = await newLeadRow.innerHTML();
    const statusChanged = leadRowBefore !== leadRowAfter;
    
    console.log('Status changed:', statusChanged);
    
    // Check for "Отказана" (Rejected in Bulgarian) status or verify "Ново" is gone
    const hasRejectedStatus = await newLeadRow.locator('text=Отказана').count() > 0;
    const hasNewStatus = await newLeadRow.locator('text=Ново').count() > 0;
    
    console.log('Has Rejected (Отказана) status:', hasRejectedStatus);
    console.log('Has New (Ново) status:', hasNewStatus);
    
    // Log results
    console.log('=== Test Results ===');
    console.log('PATCH request captured:', !!patchRequestUrl);
    console.log('Expected status 200, got:', patchResponseStatus);
    console.log('UI status changed:', statusChanged);
    console.log('===================');
    
    // Assertions
    expect(patchRequestUrl).toBeTruthy();
    expect(patchResponseStatus).toBe(200);
    expect(statusChanged || hasRejectedStatus || !hasNewStatus).toBeTruthy();
  });
});
