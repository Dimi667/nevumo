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
        WHERE key LIKE 'privacy.%'
        GROUP BY lang
        ORDER BY lang
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} keys")

ALL_TRANSLATIONS: dict[str, dict[str, str]] = {
  "en": {
    "privacy.col_data": "Data",
    "privacy.col_purpose": "Purpose",
    "privacy.col_legal_basis": "Legal Basis",
    "privacy.col_key": "Key",
    "privacy.col_type": "Type",
    "privacy.col_retention": "Retention",
    "privacy.col_basis": "Basis",
    "privacy.col_processor": "Processor",
    "privacy.col_country": "Country",
    "privacy.col_safeguard": "Safeguard",
    "privacy.legal_contract_b": "Contract — Art. 6(1)(b)",
    "privacy.legal_obligation_c": "Legal obligation — Art. 6(1)(c)",
    "privacy.legal_legitimate_f": "Legitimate interest — Art. 6(1)(f)",
    "privacy.legal_consent_a": "Consent — Art. 6(1)(a)",
  },
  "bg": {
    "privacy.col_data": "Данни",
    "privacy.col_purpose": "Цел",
    "privacy.col_legal_basis": "Правна основа",
    "privacy.col_key": "Ключ",
    "privacy.col_type": "Тип",
    "privacy.col_retention": "Съхранение",
    "privacy.col_basis": "Основа",
    "privacy.col_processor": "Обработващ",
    "privacy.col_country": "Държава",
    "privacy.col_safeguard": "Гаранция",
    "privacy.legal_contract_b": "Договор — чл. 6(1)(б)",
    "privacy.legal_obligation_c": "Законово задължение — чл. 6(1)(в)",
    "privacy.legal_legitimate_f": "Легитимен интерес — чл. 6(1)(е)",
    "privacy.legal_consent_a": "Съгласие — чл. 6(1)(а)",
  },
  "pl": {
    "privacy.col_data": "Dane",
    "privacy.col_purpose": "Cel",
    "privacy.col_legal_basis": "Podstawa prawna",
    "privacy.col_key": "Klucz",
    "privacy.col_type": "Typ",
    "privacy.col_retention": "Okres przechowywania",
    "privacy.col_basis": "Podstawa",
    "privacy.col_processor": "Podmiot przetwarzający",
    "privacy.col_country": "Kraj",
    "privacy.col_safeguard": "Zabezpieczenie",
    "privacy.legal_contract_b": "Umowa — art. 6 ust. 1 lit. b",
    "privacy.legal_obligation_c": "Obowiązek prawny — art. 6 ust. 1 lit. c",
    "privacy.legal_legitimate_f": "Uzasadniony interes — art. 6 ust. 1 lit. f",
    "privacy.legal_consent_a": "Zgoda — art. 6 ust. 1 lit. a",
  },
}

if __name__ == "__main__":
    main()
