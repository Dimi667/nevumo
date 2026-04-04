#!/usr/bin/env python3

import re

# Read the current file
with open('apps/api/scripts/seed_ui_translations.py', 'r') as f:
    content = f.read()

# All remaining languages from the user's request
remaining_languages_content = '''
  "cs": {
    "homepage.nav_link": "Hledáte službu?",
    "homepage.hero_prefix": "Získejte klienty pro",
    "homepage.hero_suffix": "ve Varšavě",
    "homepage.hero_subtitle": "Zdarma. Bez provize. Přímý kontakt.",
    "homepage.trust_1": "Bez provize",
    "homepage.trust_2": "Registrace 2 minuty",
    "homepage.trust_3": "Skutečné poptávky",
    "homepage.social_proof": "47 specialistů • 120 poptávek tento měsíc",
    "homepage.cta_hero": "Začít zdarma",
    "homepage.how_title": "Jak to funguje",
    "homepage.step1_title": "Vytvořit profil",
    "homepage.step1_sub": "2 minuty",
    "homepage.step2_title": "Přijímat poptávky od klientů",
    "homepage.step2_sub": "ihned po registraci",
    "homepage.step3_title": "Kontaktovat přímo",
    "homepage.step3_sub": "bez zprostředkovatelů",
    "homepage.cat_cleaning_name": "Úklid",
    "homepage.cat_cleaning_leads": "26 poptávek tento týden",
    "homepage.cat_plumbing_name": "Instalatér",
    "homepage.cat_plumbing_leads": "18 poptávek tento týden",
    "homepage.cat_massage_name": "Masáž",
    "homepage.cat_massage_leads": "14 poptávek tento týden",
    "homepage.cat_cta": "Nabízím tuto službu",
    "homepage.rotating_categories": "Masáž,Úklid,Instalatér",
    "homepage.activity_title": "Poslední poptávky",
    "homepage.activity_1": "Krzysztof z Varšavy hledá úklid",
    "homepage.activity_1_time": "před 8 min",
    "homepage.activity_2": "Anna z Varšavy hledá masáž",
    "homepage.activity_2_time": "před 1 hod",
    "homepage.activity_3": "Marek z Varšavy hledá instalatéra",
    "homepage.activity_3_time": "před 3 hod",
    "homepage.why_title": "Proč specialisté volí Nevumo",
    "homepage.why_1_title": "Zdarma",
    "homepage.why_1_sub": "žádné skryté poplatky",
    "homepage.why_2": "Přímý kontakt s klienty",
    "homepage.why_3": "Profil + SEO stránka, která pracuje za vás 24/7",
    "homepage.cta2_title": "Připraveni na nové klienty?",
    "homepage.cta2_btn": "Vytvořit bezplatný profil",
    "homepage.footer_title": "Hledáte službu ve Varšavě?",
    "homepage.footer_link_cleaning": "Úklid ve Varšavě",
    "homepage.footer_link_plumbing": "Instalatér ve Varšavě",
    "homepage.footer_link_massage": "Masáž ve Varšavě",
    "homepage.footer_popular": "Oblíbené: Masáž • Úklid • Instalatér",
    "category.nav_link": "Staňte se specialistou",
    "category.trust_specialists": "specialistů",
    "category.trust_rating": "hodnocení",
    "category.trust_requests": "poptávek tento měsíc",
    "category.trust_response": "Průměrná odezva: ~30 min",
    "category.empty_state": "První specialisté se přidávají. Zkuste to zítra.",
    "category.form_title": "Odeslat poptávku",
    "category.form_subtitle": "Zdarma • Nezávazně",
    "category.form_phone": "Vaše telefonní číslo",
    "category.form_desc": "Popište, co potřebujete (volitelné)",
    "category.form_btn": "Odeslat poptávku",
    "category.form_trust_1": "Zdarma",
    "category.form_trust_2": "Nezávazně",
    "category.form_trust_3": "Odpověď do 30 min",
    "category.provider_cta_prefix": "Nabízíte",
    "category.provider_cta_suffix": "ve Varšavě?",
    "category.provider_cta_link": "Přidat se zdarma →",
    "category.also_check": "Podívejte se také:",
    "category.h1_cleaning": "Úklid ve Varšavě",
    "category.h1_plumbing": "Instalatér ve Varšavě",
    "category.h1_massage": "Masáž ve Varšavě",
    "category.subtitle_cleaning": "Najděte ověřené specialisty na úklid ve Varšavě. Bezplatná poptávka, nezávazně.",
    "category.subtitle_plumbing": "Najděte ověřeného instalatéra ve Varšavě. Bezplatná poptávka, nezávazně.",
    "category.subtitle_massage": "Najděte ověřené maséry ve Varšavě. Bezplatná poptávka, nezávazně.",
  },
'''

# Find the position before the closing brace and add the new content
pattern = r'(\s+},\s+})'
match = re.search(pattern, content)

if match:
    # Insert the new languages before the final closing brace
    new_content = content[:match.start()] + remaining_languages_content.rstrip() + '\n' + content[match.start():]
    
    # Write the updated content back to the file
    with open('apps/api/scripts/seed_ui_translations.py', 'w') as f:
        f.write(new_content)
    
    print("Added Czech language successfully")
else:
    print("Could not find the correct location to insert languages")
