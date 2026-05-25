#!/usr/bin/env python3
"""
Seed script for "Show more" button translations (category namespace)
Key: category.show_more
Languages: 34
Run: docker exec nevumo-api python -m apps.api.scripts.seed_show_more_translations
"""
from sqlalchemy import text
from apps.api.database import SessionLocal

RAW_DATA = {
    "bg": "Покажи още",
    "cs": "Zobrazit více",
    "da": "Vis mere",
    "de": "Mehr anzeigen",
    "el": "Δείτε περισσότερα",
    "en": "Show more",
    "es": "Mostrar más",
    "et": "Näita rohkem",
    "fi": "Näytä lisää",
    "fr": "Afficher plus",
    "ga": "Taispeáin níos mó",
    "hr": "Prikaži više",
    "hu": "Mutass többet",
    "is": "Sýna meira",
    "it": "Mostra altro",
    "lb": "Méi weisen",
    "lt": "Rodyti daugiau",
    "lv": "Rādīt vairāk",
    "mk": "Прикажи повеќе",
    "mt": "Uri aktar",
    "nl": "Meer tonen",
    "no": "Vis mer",
    "pl": "Pokaż więcej",
    "pt": "Mostrar mais",
    "pt-PT": "Mostrar mais",
    "ro": "Afișează mai mult",
    "ru": "Показать ещё",
    "sk": "Zobraziť viac",
    "sl": "Prikaži več",
    "sq": "Shiko më shumë",
    "sr": "Prikaži više",
    "sv": "Visa mer",
    "tr": "Daha fazla göster",
    "uk": "Показати ще"
}

def main():
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()

def run_seed(db):
    insert_translations(db, RAW_DATA)
    verify(db)

def insert_translations(db, data: dict[str, str]) -> None:
    count = 0
    for lang, value in data.items():
        db.execute(
            text("""
                INSERT INTO translations (lang, key, value)
                VALUES (:lang, :key, :value)
                ON CONFLICT (lang, key)
                DO UPDATE SET value = EXCLUDED.value
            """),
            {"lang": lang, "key": "category.show_more", "value": value}
        )
        count += 1
    db.commit()
    print(f"Inserted/updated {count} translation rows")

def verify(db) -> None:
    result = db.execute(text("""
        SELECT lang, key, value
        FROM translations
        WHERE key = 'category.show_more'
        ORDER BY lang
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[2]}")

if __name__ == "__main__":
    main()
