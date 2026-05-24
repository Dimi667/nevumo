from sqlalchemy import text
from apps.api.database import SessionLocal

SUPPORTED_LANGUAGES = [
  "bg", "cs", "da", "de", "el", "en", "es", "et", "fi", "fr", "ga", "hr", "hu",
  "is", "it", "lb", "lt", "lv", "mk", "mt", "nl", "no", "pl", "pt", "pt-PT",
  "ro", "ru", "sk", "sl", "sq", "sr", "sv", "tr", "uk"
]

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
        WHERE key LIKE 'legal_%' OR key LIKE 't36_%'
        GROUP BY lang
        ORDER BY lang
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} keys")

ALL_TRANSLATIONS: dict[str, dict[str, str]] = {}

# legal_contract_b - за всички 34 езика
for lang in SUPPORTED_LANGUAGES:
    if lang == "en":
        ALL_TRANSLATIONS[lang] = {"legal_contract_b": "Contract — Art. 6(1)(b) GDPR"}
    elif lang == "bg":
        ALL_TRANSLATIONS[lang] = {"legal_contract_b": "Договор — чл. 6(1)(б) ОРЗД"}
    elif lang == "pl":
        ALL_TRANSLATIONS[lang] = {"legal_contract_b": "Umowa — art. 6 ust. 1 lit. b RODO"}
    else:
        ALL_TRANSLATIONS[lang] = {"legal_contract_b": "Contract — Art. 6(1)(b) GDPR"}

# t36_* ключове - само en/bg/pl
ALL_TRANSLATIONS["en"].update({
    "t36_transactional_data": "Transactional emails (account confirmation, lead notifications, password reset)",
    "t36_transactional_purpose": "Service delivery",
    "t36_marketing_data": "Marketing emails (platform updates, tips)",
    "t36_marketing_purpose": "Marketing",
})

ALL_TRANSLATIONS["bg"].update({
    "t36_transactional_data": "Транзакционни имейли (потвърждение на акаунт, известия за заявки, смяна на парола)",
    "t36_transactional_purpose": "Предоставяне на услугата",
    "t36_marketing_data": "Маркетингови имейли (новини, съвети)",
    "t36_marketing_purpose": "Маркетинг",
})

ALL_TRANSLATIONS["pl"].update({
    "t36_transactional_data": "E-maile transakcyjne (potwierdzenie konta, powiadomienia o zleceniach, reset hasła)",
    "t36_transactional_purpose": "Świadczenie usługi",
    "t36_marketing_data": "E-maile marketingowe (aktualizacje, wskazówki)",
    "t36_marketing_purpose": "Marketing",
})

# legal_consent_a - за всички 34 езика
for lang in SUPPORTED_LANGUAGES:
    if lang == "en":
        ALL_TRANSLATIONS[lang]["legal_consent_a"] = "Consent — Art. 6(1)(a) GDPR"
    elif lang == "bg":
        ALL_TRANSLATIONS[lang]["legal_consent_a"] = "Съгласие — чл. 6(1)(а) ОРЗД"
    elif lang == "pl":
        ALL_TRANSLATIONS[lang]["legal_consent_a"] = "Zgoda — art. 6 ust. 1 lit. a RODO"
    else:
        ALL_TRANSLATIONS[lang]["legal_consent_a"] = "Consent — Art. 6(1)(a) GDPR"

# legal_obligation_c - за всички 34 езика
for lang in SUPPORTED_LANGUAGES:
    if lang == "en":
        ALL_TRANSLATIONS[lang]["legal_obligation_c"] = "Legal obligation — Art. 6(1)(c) GDPR"
    elif lang == "bg":
        ALL_TRANSLATIONS[lang]["legal_obligation_c"] = "Законово задължение — чл. 6(1)(в) ОРЗД"
    elif lang == "pl":
        ALL_TRANSLATIONS[lang]["legal_obligation_c"] = "Obowiązek prawny — art. 6 ust. 1 lit. c RODO"
    else:
        ALL_TRANSLATIONS[lang]["legal_obligation_c"] = "Legal obligation — Art. 6(1)(c) GDPR"

# legal_legitimate_f - за всички 34 езика
for lang in SUPPORTED_LANGUAGES:
    if lang == "en":
        ALL_TRANSLATIONS[lang]["legal_legitimate_f"] = "Legitimate interest — Art. 6(1)(f) GDPR"
    elif lang == "bg":
        ALL_TRANSLATIONS[lang]["legal_legitimate_f"] = "Легитимен интерес — чл. 6(1)(е) ОРЗД"
    elif lang == "pl":
        ALL_TRANSLATIONS[lang]["legal_legitimate_f"] = "Uzasadniony interes — art. 6 ust. 1 lit. f RODO"
    else:
        ALL_TRANSLATIONS[lang]["legal_legitimate_f"] = "Legitimate interest — Art. 6(1)(f) GDPR"

if __name__ == "__main__":
    main()
