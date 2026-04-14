#!/bin/bash
# Nevumo Database Restore Script
# Run this script after database reset to restore all seed data
# Usage: ./restore_nevumo.sh

# Database URL for local execution
export DATABASE_URL="postgresql://nevumo:nevumo@localhost:5432/nevumo_leads"

# Add PYTHONPATH for module imports
export PYTHONPATH=/Users/dimitardimitrov/nevumo:$PYTHONPATH

echo "=========================================="
echo "Nevumo Database Restore Script"
echo "=========================================="
echo ""

# Change to apps/api directory
cd apps/api

echo "STEP 1: Seeding Categories and Locations (Warsaw Launch)"
echo "--------------------------------------------------------"
python3 -m scripts.seed_warsaw_launch
echo ""

echo "STEP 2: Seeding Location Translations"
echo "--------------------------------------------------------"
python3 -m scripts.seed_location_translations
echo ""

echo "STEP 3: Seeding UI Translations (homepage, category)"
echo "--------------------------------------------------------"
python3 -m scripts.seed_ui_translations
echo ""

echo "STEP 4: Seeding Category Form Translations (Part 1)"
echo "--------------------------------------------------------"
python3 -m scripts.seed_category_form_part1
echo ""

echo "STEP 5: Seeding Category Form Translations (Part 2)"
echo "--------------------------------------------------------"
python3 -m scripts.seed_category_form_part2
echo ""

echo "STEP 6: Seeding Category Form Translations (Part 3)"
echo "--------------------------------------------------------"
python3 -m scripts.seed_category_form_part3
echo ""

echo "STEP 7: Seeding Category Form Translations (Part 4)"
echo "--------------------------------------------------------"
python3 -m scripts.seed_category_form_part4
echo ""

echo "STEP 8: Seeding Widget Translations"
echo "--------------------------------------------------------"
python3 -m scripts.seed_widget_translations
echo ""

echo "STEP 9: Seeding Auth Translations"
echo "--------------------------------------------------------"
python3 -m scripts.seed_auth_translations
echo ""

echo "STEP 10: Seeding Auth Hero Translations"
echo "--------------------------------------------------------"
python3 -m scripts.seed_auth_hero_translations
echo ""

echo "STEP 11: Seeding Onboarding Hero Translations"
echo "--------------------------------------------------------"
python3 -m scripts.seed_onboarding_hero_translations
echo ""

echo "STEP 12: Seeding Provider Card Translations"
echo "--------------------------------------------------------"
python3 -m scripts.seed_provider_card_translations
echo ""

echo "STEP 13: Seeding Provider Dashboard Translations"
echo "--------------------------------------------------------"
python3 -m scripts.seed_provider_dashboard_translations
echo ""

echo "STEP 14: Seeding Client Dashboard Translations"
echo "--------------------------------------------------------"
python3 -m scripts.seed_client_dashboard_translations
echo ""

echo "STEP 15: Seeding Review Translations"
echo "--------------------------------------------------------"
python3 -m scripts.seed_review_translations
echo ""

echo "STEP 16: Seeding PWA Translations"
echo "--------------------------------------------------------"
python3 -m scripts.seed_pwa_translations
echo ""

echo "STEP 17: Seeding Success Screen Translations"
echo "--------------------------------------------------------"
python3 -m scripts.seed_success_screen_translations
echo ""

echo "STEP 18: Seeding Notes Privacy Translations"
echo "--------------------------------------------------------"
python3 -m scripts.seed_notes_privacy_translations
echo ""

echo "STEP 19: Seeding QR Translations"
echo "--------------------------------------------------------"
python3 seed_qr_translations.py
echo ""

echo "STEP 20: Seeding Legacy Translations (if needed)"
echo "--------------------------------------------------------"
python3 seed_translations.py
echo ""

echo "STEP 21: Seeding Missing Leads Translations"
echo "--------------------------------------------------------"
python3 seed_missing_leads_translations.py
echo ""

echo "=========================================="
echo "Database Restore Completed!"
echo "=========================================="
echo ""
echo "Optional: Add test provider and leads"
echo "Run: python3 add_test_provider.py"
echo "Run: python3 add_test_leads.py"
echo ""
