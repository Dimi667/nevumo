# Fix verified_label Translation Display

## Summary
Add missing widget translation records to database so the embed page shows translated text instead of raw keys like "verified_label".

## Root Cause Analysis
- The frontend correctly requests translations from `/api/v1/providers/{slug}?lang=bg`
- The API fetches translations using `fetch_translations()` and includes `verified_label` in widget keys
- However, the database lacks the actual translation records for widget-specific keys
- Only login-related translations exist (`login.findService.label`, `login.offerService.label`)
- Result: Frontend displays raw keys ("verified_label", "jobs_label", "button_text") instead of translated text

## Implementation Plan

### Step 1: Create Translation Insertion Script
- Create a script to insert all 32 language translations for widget keys
- Include all keys needed by the frontend: `verified_label`, `jobs_label`, `rating_label`, `phone_label`, `phone_placeholder`, `notes_label`, `notes_placeholder`, `response_time`, `button_text`, `disclaimer`, `success_title`, `success_message`, `new_request_button`
- Use the exact translations from `seed_translations.py` which contains complete 32-language data

### Step 2: Execute Translation Insertion
- Run the script to populate database with missing widget translations
- Verify all 32 languages are inserted for each key (416 total translation records: 13 keys × 32 languages)

### Step 3: Test the Fix
- Refresh the embed page to confirm translations display properly
- Test multiple languages to ensure i18n works correctly
- Verify the API returns proper translated values

## Files to Modify
- **NEW**: `/apps/api/insert_widget_translations.py` - Script to insert missing translations
- **NO CHANGES** to frontend code (it's already correct)
- **NO CHANGES** to API code (it's already correct)

## Expected Outcome
After implementation, the embed page will show:
- "✓ Потвърден професионалист" instead of "✓ verified_label" (for Bulgarian)
- Properly translated text for all UI elements in all 32 supported languages
- No raw translation keys visible to users
