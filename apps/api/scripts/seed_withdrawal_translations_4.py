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
        WHERE key LIKE 'withdrawal.label_%' OR key LIKE 'withdrawal.cancel' OR key LIKE 'withdrawal.submit' OR key LIKE 'withdrawal.optional' OR key LIKE 'withdrawal.error_%' OR key LIKE 'withdrawal.success_%'
        GROUP BY lang
        ORDER BY lang
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} keys")

ALL_TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "withdrawal.label_service_description": "Service Description",
        "withdrawal.label_contract_date": "Contract Date",
        "withdrawal.label_consumer_name": "Consumer Name",
        "withdrawal.label_consumer_address": "Consumer Address",
        "withdrawal.label_account_id": "Account ID",
        "withdrawal.label_email": "Email",
        "withdrawal.label_submission_date": "Submission Date",
        "withdrawal.optional": "optional",
        "withdrawal.cancel": "Cancel",
        "withdrawal.submit": "Submit Form",
        "withdrawal.submitting": "Submitting...",
        "withdrawal.error_service_description_required": "Service description is required",
        "withdrawal.error_contract_date_required": "Contract date is required",
        "withdrawal.error_consumer_name_required": "Consumer name is required",
        "withdrawal.error_consumer_address_required": "Consumer address is required",
        "withdrawal.error_email_required": "Email is required",
        "withdrawal.error_email_invalid": "Invalid email format",
        "withdrawal.error_submission_date_required": "Submission date is required",
        "withdrawal.success_title": "Form Submitted Successfully",
        "withdrawal.success_message": "Your withdrawal form has been submitted and sent to our legal team.",
    },
    "bg": {
        "withdrawal.label_service_description": "Описание на услугата",
        "withdrawal.label_contract_date": "Дата на сключване на договора",
        "withdrawal.label_consumer_name": "Име на потребителя",
        "withdrawal.label_consumer_address": "Адрес на потребителя",
        "withdrawal.label_account_id": "Идентификатор на акаунт",
        "withdrawal.label_email": "Имейл адрес",
        "withdrawal.label_submission_date": "Дата на подаване",
        "withdrawal.optional": "(по избор)",
        "withdrawal.cancel": "Отказ",
        "withdrawal.submit": "Изпрати формуляр",
        "withdrawal.submitting": "Изпращане...",
        "withdrawal.error_service_description_required": "Описанието на услугата е задължително",
        "withdrawal.error_contract_date_required": "Датата на договора е задължителна",
        "withdrawal.error_consumer_name_required": "Името на потребителя е задължително",
        "withdrawal.error_consumer_address_required": "Адресът на потребителя е задължителен",
        "withdrawal.error_email_required": "Имейл адресът е задължителен",
        "withdrawal.error_email_invalid": "Невалиден формат на имейл",
        "withdrawal.error_submission_date_required": "Датата на подаване е задължителна",
        "withdrawal.success_title": "Формулярът е изпратен успешно",
        "withdrawal.success_message": "Формулярът ви за отказ е изпратен и изпратен до нашия правен екип.",
    },
    "pl": {
        "withdrawal.label_service_description": "Opis usługi",
        "withdrawal.label_contract_date": "Data zawarcia umowy",
        "withdrawal.label_consumer_name": "Imię i nazwisko konsumenta",
        "withdrawal.label_consumer_address": "Adres konsumenta",
        "withdrawal.label_account_id": "Numer konta",
        "withdrawal.label_email": "Adres e-mail",
        "withdrawal.label_submission_date": "Data złożenia",
        "withdrawal.optional": "(opcjonalnie)",
        "withdrawal.cancel": "Anuluj",
        "withdrawal.submit": "Wyślij formularz",
        "withdrawal.submitting": "Wysyłanie...",
        "withdrawal.error_service_description_required": "Opis usługi jest wymagany",
        "withdrawal.error_contract_date_required": "Data zawarcia umowy jest wymagana",
        "withdrawal.error_consumer_name_required": "Imię i nazwisko konsumenta są wymagane",
        "withdrawal.error_consumer_address_required": "Adres konsumenta jest wymagany",
        "withdrawal.error_email_required": "Adres e-mail jest wymagany",
        "withdrawal.error_email_invalid": "Nieprawidłowy format adresu e-mail",
        "withdrawal.error_submission_date_required": "Data złożenia jest wymagana",
        "withdrawal.success_title": "Formularz wysłany pomyślnie",
        "withdrawal.success_message": "Twój formularz odstąpienia od umowy został przesłany i wysłany do naszego zespołu prawnego.",
    },
}

ALL_LANGUAGES = ["en", "bg", "pl", "cs", "da", "de", "el", "es", "et", "fi", "fr", "ga", "hr", "hu", "is", "it", "lb", "lt", "lv", "mk", "mt", "nl", "no", "pt", "pt-PT", "ro", "ru", "sk", "sl", "sq", "sr", "sv", "tr", "uk"]

for lang in ALL_LANGUAGES:
    if lang not in ALL_TRANSLATIONS:
        ALL_TRANSLATIONS[lang] = ALL_TRANSLATIONS["en"]

if __name__ == "__main__":
    main()
