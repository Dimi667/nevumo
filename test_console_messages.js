const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  // Collect console messages
  const consoleMessages = [];
  page.on('console', msg => {
    consoleMessages.push({
      type: msg.type(),
      text: msg.text(),
      location: msg.location()
    });
  });
  
  // Collect network errors
  const networkErrors = [];
  page.on('response', response => {
    if (response.status() >= 400) {
      networkErrors.push({
        url: response.url(),
        status: response.status(),
        statusText: response.statusText()
      });
    }
  });
  
  try {
    console.log('Navigating to http://localhost:3000/bg/provider/dashboard...');
    await page.goto('http://localhost:3000/bg/provider/dashboard', { waitUntil: 'networkidle' });
    console.log('Waiting 3000ms for page to load...');
    await page.waitForTimeout(3000);
    
    console.log('\n=== ALL CONSOLE MESSAGES ===');
    consoleMessages.forEach(msg => {
      console.log(`[${msg.type()}] ${msg.text}`);
      if (msg.location) {
        console.log(`  Location: ${msg.location.url}:${msg.location.lineNumber}`);
      }
    });
    
    console.log('\n=== FILTERED MESSAGES (use-translation, setup_title, apiBase, translations, fetch, MISSING) ===');
    const keywords = ['use-translation', 'setup_title', 'apiBase', 'translations', 'fetch', 'MISSING'];
    consoleMessages.forEach(msg => {
      const text = msg.text.toLowerCase();
      if (keywords.some(kw => text.includes(kw.toLowerCase()))) {
        console.log(`[${msg.type()}] ${msg.text}`);
      }
    });
    
    console.log('\n=== NETWORK ERRORS ===');
    if (networkErrors.length === 0) {
      console.log('No network errors found.');
    } else {
      networkErrors.forEach(err => {
        console.log(`[${err.status}] ${err.statusText} - ${err.url}`);
      });
    }
    
  } catch (error) {
    console.error('Error:', error);
  } finally {
    await browser.close();
  }
})();
