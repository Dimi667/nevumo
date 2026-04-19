#!/usr/bin/env python3
"""
Seed script for City Page translations (city namespace)
Covers EN, BG, PL with fallback to EN for other languages.
Run: python3 -m apps.api.scripts.seed_city_translations
"""
from sqlalchemy import text
from apps.api.database import SessionLocal

# 34 supported languages
LANGUAGES = [
    'en', 'bg', 'pl', 'de', 'fr', 'es', 'it', 'nl', 'pt', 'pt-PT', 
    'ro', 'cs', 'sk', 'hu', 'hr', 'sl', 'sr', 'mk', 'sq', 'el', 
    'tr', 'ru', 'uk', 'lv', 'lt', 'et', 'fi', 'sv', 'da', 'no', 
    'is', 'lb', 'ga', 'mt'
]

EN_DATA = {
    "city.nav_link": "Become a specialist",
    "city.hero_title": "Find services in {city}",
    "city.search_placeholder": "What service do you need?",
    "city.search_btn": "Search",
    "city.cta_request": "Get offers",
    "city.categories_title": "Popular services in {city}",
    "city.cat_cleaning_leads": "Available now",
    "city.cat_plumbing_leads": "Available now",
    "city.cat_massage_leads": "Available now",
    "city.cat_cta": "View providers",
    "city.empty_title": "Can’t find the right service?",
    "city.empty_subtitle": "Describe your request and we will connect you with the right specialists.",
    "city.empty_cta": "Request any service",
    "city.how_title": "How it works",
    "city.how_step_1": "Describe your request",
    "city.how_step_1_sub": "Takes 2 minutes",
    "city.how_step_2": "Get offers from specialists",
    "city.how_step_2_sub": "Usually within 30 minutes",
    "city.how_step_3": "Choose and connect directly",
    "city.how_step_3_sub": "No commission, no middlemen",
    "city.seo_title": "Services in {city}",
    "city.seo_description": "Looking for reliable services in {city}? Nevumo connects you with verified local specialists. From home cleaning to plumbing repairs and professional massage therapy, find the right provider for your needs.",
    "city.seo_p2": "All specialists on our platform are reviewed by real customers. Send a free request, compare offers, and choose the best match for your project. No hidden fees, no obligations.",
    "city.seo_p3": "Whether you need a one-time service or ongoing support, our network of professionals in {city} is ready to help. Get started with a simple request and receive responses within hours.",
    "city.footer_title": "Nevumo — Connecting you with local specialists",
    "city.footer_in": "in"
}

BG_DATA = {
    "city.nav_link": "Стани специалист",
    "city.hero_title": "Намери услуги в {city}",
    "city.search_placeholder": "Каква услуга търсиш?",
    "city.search_btn": "Търси",
    "city.cta_request": "Получи оферти",
    "city.categories_title": "Популярни услуги в {city}",
    "city.cat_cleaning_leads": "Достъпно сега",
    "city.cat_plumbing_leads": "Достъпно сега",
    "city.cat_massage_leads": "Достъпно сега",
    "city.cat_cta": "Виж изпълнители",
    "city.empty_title": "Не намираш точната услуга?",
    "city.empty_subtitle": "Опиши какво търсиш и ние ще те свържем с правилните специалисти.",
    "city.empty_cta": "Изпрати заявка — ще те свържем с изпълнител",
    "city.how_title": "Как работи",
    "city.how_step_1": "Опиши какво търсиш",
    "city.how_step_1_sub": "Отнема 2 минути",
    "city.how_step_2": "Получи оферти от специалисти",
    "city.how_step_2_sub": "Обикновено до 30 минути",
    "city.how_step_3": "Избери и се свържи директно",
    "city.how_step_3_sub": "Без комисионна, без посредници",
    "city.seo_title": "Услуги в {city}",
    "city.seo_description": "Намери надеждни специалисти в {city}. Nevumo те свързва с проверени местни специалисти. От почистване до ремонт на водопровод и професионални масажи, намери правилния изпълнител.",
    "city.seo_p2": "Всички специалисти в нашата платформа са оценени от реални клиенти. Изпрати безплатна заявка, сравни оферти и избери най-добрия за твоя проект. Без скрити такси и ангажименти.",
    "city.seo_p3": "Независимо дали имаш нужда от еднократна услуга или дългосрочна подкрепа, нашата мрежа от професионалисти в {city} е готова да помогне. Започни с лесна заявка и получи отговори до часове.",
    "city.footer_title": "Nevumo — Свързваме те с местни специалисти",
    "city.footer_in": "в"
}

PL_DATA = {
    "city.nav_link": "Zostań specjalistą",
    "city.hero_title": "Znajdź usługi w {city}",
    "city.search_placeholder": "Jakiej usługi potrzebujesz?",
    "city.search_btn": "Szukaj",
    "city.cta_request": "Otrzymaj oferty",
    "city.categories_title": "Popularne usługi w {city}",
    "city.cat_cleaning_leads": "Dostępne teraz",
    "city.cat_plumbing_leads": "Dostępne teraz",
    "city.cat_massage_leads": "Dostępne teraz",
    "city.cat_cta": "Zobacz wykonawców",
    "city.empty_title": "Nie możesz znaleźć odpowiedniej usługi?",
    "city.empty_subtitle": "Opisz swoje zapytanie, a my skontaktujemy Cię z odpowiednimi specjalistami.",
    "city.empty_cta": "Wyślij zapytanie — znajdziemy wykonawcę dla Ciebie",
    "city.how_title": "Jak to działa",
    "city.how_step_1": "Opisz czego potrzebujesz",
    "city.how_step_1_sub": "Zajmuje 2 minuty",
    "city.how_step_2": "Otrzymaj oferty od specjalistów",
    "city.how_step_2_sub": "Zazwyczaj w ciągu 30 minut",
    "city.how_step_3": "Wybierz i połącz się bezpośrednio",
    "city.how_step_3_sub": "Bez prowizji, bez pośredników",
    "city.seo_title": "Usługi w {city}",
    "city.seo_description": "Znajdź sprawdzonych specjalistów w {city}. Nevumo łączy Cię ze zweryfikowanymi lokalnymi fachowcami. Od sprzątania po hydraulikę i masaże, znajdź odpowiedniego wykonawcę.",
    "city.seo_p2": "Wszyscy specjaliści na naszej platformie są oceniani przez prawdziwych klientów. Wyślij bezpłatne zapytanie, porównaj oferty i wybierz najlepszą dla swojego projektu. Bez ukrytych opłat i zobowiązań.",
    "city.seo_p3": "Niezależnie od tego, czy potrzebujesz jednorazowej usługi, czy stałego wsparcia, nasza sieć profesjonalistów w {city} jest gotowa do pomocy. Zacznij od prostego zapytania i otrzymaj odpowiedzi w ciągu kilku godzin.",
    "city.footer_title": "Nevumo — Łączymy Cię z lokalnymi specjalistami",
    "city.footer_in": "w"
}

def get_all_translations():
    all_data = {}
    for lang in LANGUAGES:
        if lang == 'bg':
            all_data[lang] = BG_DATA
        elif lang == 'pl':
            all_data[lang] = PL_DATA
        else:
            # EN and all other fallbacks
            all_data[lang] = EN_DATA
    return all_data

def main():
    db = SessionLocal()
    try:
        translations = get_all_translations()
        count = 0
        for lang, keys in translations.items():
            for key, value in keys.items():
                db.execute(
                    text("""
                        INSERT INTO translations (lang, key, value)
                        VALUES (:lang, :key, :value)
                        ON CONFLICT (lang, key)
                        DO UPDATE SET value = EXCLUDED.value
                    """),
                    {"lang": lang, "key": key, "value": value}
                )
                count += 1
        db.commit()
        print(f"✅ Successfully seeded {count} translation rows for 'city' namespace.")
        
        # Verification
        result = db.execute(text("SELECT lang, COUNT(*) FROM translations WHERE key LIKE 'city.%' GROUP BY lang"))
        print("\nVerification (keys per language):")
        for row in result:
            print(f"  {row[0]}: {row[1]}")
            
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding translations: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
