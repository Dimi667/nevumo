from sqlalchemy import text
from apps.api.database import SessionLocal

def main():
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()

def run_seed(db):
    insert_translations(db, ALL_TRANSLATIONS)
    verify(db)

def insert_translations(db, data: dict[str, dict[str, str]]) -> None:
    count = 0
    for lang, keys in data.items():
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
    print(f"Inserted/updated {count} translation rows")

def verify(db) -> None:
    result = db.execute(text("""
        SELECT lang, COUNT(*) as keys
        FROM translations
        WHERE key = 'cta_button'
        GROUP BY lang
        ORDER BY lang
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: cta_button key present")

ALL_TRANSLATIONS: dict[str, dict[str, str]] = {
  "bg": {
    "cta_button": "Свържи ме с",
  },
  "cs": {
    "cta_button": "Spojte mě s",
  },
  "da": {
    "cta_button": "Forbind mig med",
  },
  "de": {
    "cta_button": "Verbinde mich mit",
  },
  "el": {
    "cta_button": "Συνδέστε με με",
  },
  "en": {
    "cta_button": "Connect me with",
  },
  "es": {
    "cta_button": "Conéctame con",
  },
  "et": {
    "cta_button": "Ühenda mind",
  },
  "fi": {
    "cta_button": "Yhdistä minut",
  },
  "fr": {
    "cta_button": "Mettez-moi en contact avec",
  },
  "ga": {
    "cta_button": "Ceangail mé le",
  },
  "hr": {
    "cta_button": "Povežite me s",
  },
  "hu": {
    "cta_button": "Kapcsolj össze vele",
  },
  "is": {
    "cta_button": "Tengdu mig við",
  },
  "it": {
    "cta_button": "Mettimi in contatto con",
  },
  "lb": {
    "cta_button": "Verbannd mech mat",
  },
  "lt": {
    "cta_button": "Sujunk mane su",
  },
  "lv": {
    "cta_button": "Savienojiet mani ar",
  },
  "mk": {
    "cta_button": "Поврзи ме со",
  },
  "mt": {
    "cta_button": "Qabbadni ma'",
  },
  "nl": {
    "cta_button": "Verbind mij met",
  },
  "no": {
    "cta_button": "Koble meg til",
  },
  "pl": {
    "cta_button": "Połącz mnie z",
  },
  "pt": {
    "cta_button": "Conecte-me com",
  },
  "pt-PT": {
    "cta_button": "Ligue-me a",
  },
  "ro": {
    "cta_button": "Conectează-mă cu",
  },
  "ru": {
    "cta_button": "Свяжите меня с",
  },
  "sk": {
    "cta_button": "Spojte ma s",
  },
  "sl": {
    "cta_button": "Povežite me z",
  },
  "sq": {
    "cta_button": "Lidhe mua me",
  },
  "sr": {
    "cta_button": "Повежи ме са",
  },
  "sv": {
    "cta_button": "Koppla mig till",
  },
  "tr": {
    "cta_button": "Beni bağla",
  },
  "uk": {
    "cta_button": "Зв'яжіть мене з",
  },
}

if __name__ == "__main__":
    main()
