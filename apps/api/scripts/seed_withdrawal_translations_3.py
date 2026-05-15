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
        WHERE key LIKE 'withdrawal.%' OR key LIKE 'withdrawal_%'
        GROUP BY lang
        ORDER BY lang
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} keys")

ALL_TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "bg": {
        "withdrawal.form_submission_date_label": "Дата",
        "withdrawal.form_submit_button": "Изпрати формуляр за отказ",
        "withdrawal.form_success_message": "Формулярът ви за отказ е изпратен успешно. Ще ви изпратим потвърждение по имейл скоро.",
        "withdrawal.form_error_message": "Възникна грешка при изпращането на формуляра. Моля, опитайте отново.",
    },
    "pl": {
        "withdrawal.form_submission_date_label": "Data",
        "withdrawal.form_submit_button": "Wyślij formularz odstąpienia od umowy",
        "withdrawal.form_success_message": "Twój formularz odstąpienia od umowy został przesłany pomyślnie. Wkrótce wyślemy Ci e-mail z potwierdzeniem.",
        "withdrawal.form_error_message": "Wystąpił błąd podczas przesyłania formularza. Spróbuj ponownie.",
    },
    "cs": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "da": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "de": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "el": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "es": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "et": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "fi": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "fr": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "ga": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "hr": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "hu": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "is": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "it": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "lb": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "lt": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "lv": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "mk": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "mt": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "nl": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "no": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "pt": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "pt-PT": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "ro": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "ru": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "sk": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "sl": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "sq": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "sr": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "sv": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "tr": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
    "uk": {
        "withdrawal.form_submission_date_label": "Date",
        "withdrawal.form_submit_button": "Submit withdrawal form",
        "withdrawal.form_success_message": "Your withdrawal form has been submitted successfully. We will send you a confirmation email shortly.",
        "withdrawal.form_error_message": "There was an error submitting your form. Please try again.",
    },
}

if __name__ == "__main__":
    main()
