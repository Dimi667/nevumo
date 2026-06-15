#!/usr/bin/env python3.13
"""
CEIDG NIP Search Diagnostic
Tests different approaches to search by NIP on CEIDG.
"""

import asyncio
from playwright.async_api import async_playwright

# Test NIP from the CSV
TEST_NIP = "9511604749"
SEARCH_URL = "https://aplikacja.ceidg.gov.pl/CEIDG/CEIDG.Public.UI/Search.aspx"

# Same settings as original script
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


async def main():
    print("="*60)
    print("CEIDG NIP SEARCH DIAGNOSTIC")
    print("="*60)
    print(f"Search URL: {SEARCH_URL}")
    print(f"NIP: {TEST_NIP}")
    print("="*60)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent=USER_AGENT
        )
        page = await context.new_page()
        
        print("\n[1] Navigating to search page...")
        await page.goto(SEARCH_URL, timeout=30000)
        await page.wait_for_load_state("networkidle", timeout=15000)
        
        print("[2] Looking for NIP-specific input field...")
        # Try to find NIP-specific field
        nip_selectors = [
            "input[id*='NIP']",
            "input[id*='Nip']",
            "input[name*='NIP']",
            "input[name*='Nip']",
            "input[placeholder*='NIP']",
            "input[placeholder*='nip']",
        ]
        
        nip_input = None
        for selector in nip_selectors:
            try:
                element = page.locator(selector).first
                if await element.count() > 0:
                    print(f"  Found NIP input with selector: {selector}")
                    nip_input = element
                    break
            except:
                pass
        
        if nip_input:
            print("[3] Filling NIP field...")
            await nip_input.fill(TEST_NIP)
            
            print("[4] Looking for search button...")
            search_button = page.locator("input[type='submit']").first
            if await search_button.count() > 0:
                print("  Found search button")
                await search_button.click()
            else:
                print("  No search button found, trying Enter")
                await nip_input.press("Enter")
            
            print("[5] Waiting for results...")
            await page.wait_for_load_state("networkidle", timeout=15000)
            await page.wait_for_timeout(3000)
            
            print("[6] Checking results...")
            body_text = await page.inner_text("body")
            print(f"  Body text (first 500 chars): {body_text[:500]}")
            
            # Check for profile links
            profile_links = page.locator("a[href*='SearchDetails']")
            link_count = await profile_links.count()
            print(f"  Found {link_count} profile links")
            
            if link_count > 0:
                print("  ✅ NIP search works!")
            else:
                print("  ❌ No profile links found")
        else:
            print("  ❌ No NIP-specific field found")
            print("[3] Trying generic text input approach...")
            
            # Try the first text input
            text_input = page.locator("input[type='text']").first
            if await text_input.count() > 0:
                print("  Found text input, filling with NIP...")
                await text_input.fill(TEST_NIP)
                
                search_button = page.locator("input[type='submit']").first
                if await search_button.count() > 0:
                    await search_button.click()
                else:
                    await text_input.press("Enter")
                
                await page.wait_for_load_state("networkidle", timeout=15000)
                await page.wait_for_timeout(3000)
                
                body_text = await page.inner_text("body")
                print(f"  Body text (first 500 chars): {body_text[:500]}")
                
                profile_links = page.locator("a[href*='SearchDetails']")
                link_count = await profile_links.count()
                print(f"  Found {link_count} profile links")
        
        await browser.close()
        
        print("[2] Waiting for network idle...")
        await page.wait_for_load_state("networkidle", timeout=30000)
        
        print("[3] Looking for NIP input field...")
        # Try different possible selectors for NIP input
        nip_selectors = [
            "input[name*='nip']",
            "input[id*='nip']",
            "input[placeholder*='NIP']",
            "input[placeholder*='nip']",
            "input[type='text']"
        ]
        
        nip_input = None
        for selector in nip_selectors:
            try:
                element = page.locator(selector).first
                if await element.count() > 0:
                    print(f"  Found NIP input with selector: {selector}")
                    nip_input = element
                    break
            except:
                pass
        
        if not nip_input:
            print("  ❌ Could not find NIP input field")
            await browser.close()
            return
        
        print("[4] Entering NIP...")
        await nip_input.fill(TEST_NIP)
        
        print("[5] Looking for search button...")
        # Try different possible selectors for search button
        button_selectors = [
            "button[type='submit']",
            "input[type='submit']",
            "button:has-text('Szukaj')",
            "button:has-text('Search')",
            "input[value*='Szukaj']"
        ]
        
        search_button = None
        for selector in button_selectors:
            try:
                element = page.locator(selector).first
                if await element.count() > 0:
                    print(f"  Found search button with selector: {selector}")
                    search_button = element
                    break
            except:
                pass
        
        if not search_button:
            print("  ❌ Could not find search button")
            await browser.close()
            return
        
        print("[6] Submitting search...")
        await search_button.click()
        
        print("[7] Waiting for results...")
        await page.wait_for_load_state("networkidle", timeout=30000)
        await page.wait_for_timeout(3000)
        
        print("[8] Checking for CAPTCHA or error...")
        body_text = await page.inner_text("body")
        print(f"  Body text (first 500 chars): {body_text[:500]}")
        
        if "captcha" in body_text.lower() or "recaptcha" in body_text.lower():
            print("  ❌ CAPTCHA detected - search approach won't work")
            await browser.close()
            return
        
        if "brak" in body_text.lower() or "nie znaleziono" in body_text.lower():
            print("  ❌ No results found for this NIP")
            await browser.close()
            return
        
        print("[9] Looking for profile links...")
        profile_links = page.locator("a[href*='SearchDetails.aspx']")
        link_count = await profile_links.count()
        print(f"  Found {link_count} profile links with SearchDetails.aspx")
        
        if link_count == 0:
            # Try alternative selector
            profile_links = page.locator("a[href*='SearchDetails']")
            link_count = await profile_links.count()
            print(f"  Found {link_count} profile links with SearchDetails")
        
        if link_count == 0:
            # Log all links for debugging
            all_links = await page.locator("a").all()
            print(f"  Total links on page: {len(all_links)}")
            for i, link in enumerate(all_links[:15]):
                href = await link.get_attribute("href") or ""
                text = await link.inner_text()
                print(f"    Link {i}: href='{href}' text='{text[:50]}'")
            print("  ❌ No profile links found")
            await browser.close()
            return
        
        print("[10] Clicking first profile link...")
        first_link = profile_links.first
        href = await first_link.get_attribute("href")
        print(f"  Profile URL: {href}")
        
        await first_link.click()
        
        print("[11] Waiting for profile page to load...")
        await page.wait_for_load_state("networkidle", timeout=30000)
        await page.wait_for_timeout(5000)
        
        print("\n[12] Counting structural elements...")
        section_count = await page.locator("section").count()
        section_block_count = await page.locator("section.block").count()
        dl_count = await page.locator("dl").count()
        dt_count = await page.locator("dt").count()
        dd_count = await page.locator("dd").count()
        table_count = await page.locator("table").count()
        
        print(f"  section elements: {section_count}")
        print(f"  section.block elements: {section_block_count}")
        print(f"  dl elements: {dl_count}")
        print(f"  dt elements: {dt_count}")
        print(f"  dd elements: {dd_count}")
        print(f"  table elements: {table_count}")
        
        print("\n[13] Searching for elements with website-related text...")
        search_terms = ["strona", "www", "http", "Strona"]
        
        for term in search_terms:
            print(f"\n  Searching for '{term}':")
            elements = await page.locator(f"text={term}").all()
            print(f"    Found {len(elements)} elements containing '{term}'")
            
            for i, elem in enumerate(elements[:5]):  # Show first 5
                try:
                    text = await elem.inner_text()
                    tag = await elem.evaluate("el => el.tagName")
                    class_attr = await elem.get_attribute("class") or ""
                    id_attr = await elem.get_attribute("id") or ""
                    print(f"      [{i}] <{tag}> class='{class_attr}' id='{id_attr}'")
                    print(f"          Text: {text[:100]}")
                except:
                    pass
        
        print("\n[14] Full body text (first 2000 chars)...")
        body_text = await page.inner_text("body")
        print(body_text[:2000])
        
        print("\n[15] Raw HTML (first 3000 chars)...")
        html_content = await page.content()
        print(html_content[:3000])
        
        print("\n[16] Testing specific selectors...")
        
        # Test section.block
        print("  Testing selector: section.block")
        try:
            await page.wait_for_selector("section.block", timeout=10000)
            print("    ✅ section.block found!")
        except:
            print("    ❌ section.block timeout")
        
        # Test alternative selectors
        alternative_selectors = [
            "dl",
            "table", 
            ".detail",
            "[class*='detail']",
            "[class*='data']",
            "[class*='block']",
            "div[class*='detail']",
            "div[class*='data']"
        ]
        
        for selector in alternative_selectors:
            count = await page.locator(selector).count()
            if count > 0:
                print(f"  Selector '{selector}': {count} elements found")
            else:
                print(f"  Selector '{selector}': 0 elements")
        
        print("\n[17] Looking for dt/dd pairs with website-related content...")
        if dl_count > 0:
            print(f"  Found {dl_count} dl elements, inspecting first one...")
            first_dl = page.locator("dl").first
            dl_text = await first_dl.inner_text()
            print(f"  First dl text: {dl_text[:500]}")
            
            # Get all dt elements
            dts = await page.locator("dt").all()
            print(f"  Total dt elements: {len(dts)}")
            
            for i, dt in enumerate(dts[:10]):  # Check first 10
                try:
                    dt_text = await dt.inner_text()
                    if any(term.lower() in dt_text.lower() for term in search_terms):
                        print(f"    DT[{i}]: {dt_text}")
                        # Try to get next sibling dd
                        dd = page.locator("dt").nth(i).locator("following-sibling::dd").first
                        if await dd.count() > 0:
                            dd_text = await dd.inner_text()
                            print(f"      DD: {dd_text}")
                except:
                    pass
        
        print("\n[18] Checking for any URL patterns in the page...")
        import re
        urls = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', body_text)
        print(f"  Found {len(urls)} URLs in body text")
        for url in urls[:10]:
            print(f"    {url}")
        
        print("\n[19] Testing section.block approach (like original script)...")
        if section_block_count > 0:
            print(f"  Found {section_block_count} section.block elements")
            sections = page.locator("section.block")
            for i in range(min(section_block_count, 3)):  # Check first 3
                section = sections.nth(i)
                section_text = await section.inner_text()
                print(f"  Section {i} text (first 300 chars): {section_text[:300]}")
                
                # Look for dt/dd pairs within this section
                dts_in_section = section.locator("dt")
                dt_count_in_section = await dts_in_section.count()
                print(f"    DT elements in section {i}: {dt_count_in_section}")
                
                for j in range(min(dt_count_in_section, 5)):
                    dt = dts_in_section.nth(j)
                    dt_text = await dt.inner_text()
                    if any(term.lower() in dt_text.lower() for term in search_terms):
                        print(f"      DT[{j}]: {dt_text}")
                        # Try to get next sibling dd using JavaScript
                        dd = await dt.evaluate_handle("el => el.nextElementSibling")
                        if dd:
                            dd_element = dd.as_element()
                            if dd_element:
                                dd_text = await dd_element.inner_text()
                                print(f"        DD: {dd_text}")
        
        print("\n" + "="*60)
        print("DIAGNOSTIC COMPLETE")
        print("="*60)
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
