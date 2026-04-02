# Add 4 New Languages and Fix Translation Consistency

## Summary
Add 4 new languages (uk, ru, is, lb) to reach total of 34 languages and update all translation files and documentation to be consistent.

## Current State Analysis
- **i18n.py**: 30 languages (missing uk, ru, is, lb)
- **seed_translations.py**: 30 languages (same 30 as i18n.py)
- **Documentation**: Claims 32 languages (incorrect)
- **Database**: Only has login translations for existing 30 languages

## Implementation Plan

### Step 1: Update Language Support in i18n.py
- Add 4 new languages to SUPPORTED_LANGUAGES tuple:
  - `uk` - Ukrainian
  - `ru` - Russian  
  - `is` - Icelandic
  - `lb` - Luxembourgish
- Update total from 30 to 34 languages

### Step 2: Add Translations for New Languages
- Update seed_translations.py with translations for all 13 widget keys
- Add translations for new languages following existing patterns
- Ensure all 34 languages have complete translations

### Step 3: Update Documentation
- Update AGENTS.md to reflect 34 supported languages (not 32)
- Update any other documentation mentioning language count

### Step 4: Insert Missing Widget Translations
- Create script to insert all widget translations for all 34 languages
- Insert 442 translation records (13 keys × 34 languages)
- Focus specifically on verified_label and other widget keys

### Step 5: Verify and Test
- Test API returns proper translations for new languages
- Verify frontend displays correctly for new languages
- Confirm database has all 442 translation records

## Files to Modify
- **i18n.py** - Add 4 new languages to SUPPORTED_LANGUAGES
- **seed_translations.py** - Add translations for new languages  
- **AGENTS.md** - Update language count from 32 to 34
- **NEW**: Script to insert widget translations for all 34 languages

## Expected Outcome
- Consistent support for 34 languages across entire system
- verified_label displays properly in all 34 languages
- Documentation matches actual implementation
- No raw translation keys visible to users
