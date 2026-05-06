#!/usr/bin/env python3
"""
Seed script to add FAQ title key for all 34 languages (Phase 4)
Run: python -m apps.api.scripts.seed_faq_title_key
"""
from sqlalchemy import text
from apps.api.database import SessionLocal

FAQ_TITLE_TRANSLATIONS = {
    "bg": "Често задавани въпроси",
    "cs": "Často kladené otázky",
    "da": "Ofte stillede spørgsmål",
    "de": "Häufig gestellte Fragen",
    "el": "Συχνές ερωτήσεις",
    "en": "Frequently Asked Questions",
    "es": "Preguntas frecuentes",
    "et": "Korduma kippuvad küsimused",
    "fi": "Usein kysytyt kysymykset",
    "fr": "Foire aux questions",
    "ga": "Ceisteanna Coitianta",
    "hr": "Često postavljana pitanja",
    "hu": "Gyakran Ismételt Kérdések",
    "is": "Algengar spurningar",
    "it": "Domande frequenti",
    "lb": "Oft gestallte Froen",
    "lt": "Dažnai užduodami klausimai",
    "lv": "Biežāk uzdotie jautājumi",
    "mk": "Често поставувани прашања",
    "mt": "Mistoqsijiet Frekwenti",
    "nl": "Veelgestelde vragen",
    "no": "Ofte stilte spørsmål",
    "pl": "Często zadawane pytania",
    "pt": "Perguntas frequentes",
    "pt-PT": "Perguntas frequentes",
    "ro": "Întrebări frecvente",
    "ru": "Часто задаваемые вопросы",
    "sk": "Často kladené otázky",
    "sl": "Pogosta vprašanja",
    "sq": "Pyetjet e shpeshta",
    "sr": "Često postavljana pitanja",
    "sv": "Vanliga frågor",
    "tr": "Sıkça Sorulan Sorular",
    "uk": "Часті запитання"
}

def main():
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()

def run_seed(db):
    key = "category.faq_title"
    
    print(f"Seeding FAQ title key: {key}")
    print(f"Languages to update: {len(FAQ_TITLE_TRANSLATIONS)}")
    
    updated_count = 0
    skipped_count = 0
    
    for lang, translation in FAQ_TITLE_TRANSLATIONS.items():
        # Use UPSERT to insert or update
        query = text("""
            INSERT INTO translations (key, lang, value)
            VALUES (:key, :lang, :value)
            ON CONFLICT (key, lang) 
            DO UPDATE SET value = :value
        """)
        
        db.execute(query, {"key": key, "lang": lang, "value": translation})
        updated_count += 1
        print(f"  ✓ {lang}: {translation}")
    
    db.commit()
    
    # Verification
    print("\n" + "="*50)
    print("VERIFICATION")
    print("="*50)
    
    verify_query = text("""
        SELECT lang, value 
        FROM translations 
        WHERE key = :key 
        ORDER BY lang
    """)
    
    result = db.execute(verify_query, {"key": key}).fetchall()
    
    print(f"\nTotal records for {key}: {len(result)}")
    print(f"Expected: 34 languages")
    
    if len(result) == 34:
        print("✓ All 34 languages have the FAQ title key")
    else:
        print(f"✗ Missing {34 - len(result)} languages")
    
    print("\n" + "="*50)
    print(f"Phase 4 Complete: {updated_count} languages updated")
    print("="*50)

if __name__ == "__main__":
    main()
