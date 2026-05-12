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
        WHERE key IN (
            'privacy.legal_contract_b',
            'privacy.legal_obligation_c',
            'privacy.legal_legitimate_f',
            'privacy.legal_consent_a',
            'privacy.col_safeguard',
            'privacy.col_processor',
            'privacy.t32_phone_purpose',
            'privacy.t33_status_data'
        )
        GROUP BY lang
        ORDER BY lang
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} keys")

ALL_TRANSLATIONS: dict[str, dict[str, str]] = {
  "bg": {
    "privacy.legal_contract_b": "Договор — чл. 6(1)(б)",
    "privacy.legal_obligation_c": "Законово задължение — чл. 6(1)(в)",
    "privacy.legal_legitimate_f": "Легитимен интерес — чл. 6(1)(е)",
    "privacy.legal_consent_a": "Съгласие — чл. 6(1)(а)",
    "privacy.col_safeguard": "Гаранция",
    "privacy.col_processor": "Обработващ",
    "privacy.t32_phone_purpose": "Доставка на заявки, комуникация",
    "privacy.t33_status_data": "История на статуса на заявката",
  },
  "pl": {
    "privacy.legal_contract_b": "Umowa — art. 6 ust. 1 lit. b",
    "privacy.legal_obligation_c": "Obowiązek prawny — art. 6 ust. 1 lit. c",
    "privacy.legal_legitimate_f": "Uzasadniony interes — art. 6 ust. 1 lit. f",
    "privacy.legal_consent_a": "Zgoda — art. 6 ust. 1 lit. a",
    "privacy.col_safeguard": "Zabezpieczenie",
    "privacy.col_processor": "Podmiot przetwarzający",
    "privacy.t32_phone_purpose": "Przekazywanie zapytań, komunikacja",
    "privacy.t33_status_data": "Historia statusu zapytania",
  },
}

if __name__ == "__main__":
    main()
