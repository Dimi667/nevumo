#!/usr/bin/env python3
"""
Seed script for widget error translations (2 keys in widget namespace)
Run: python -m apps.api.scripts.seed_widget_errors
"""
from sqlalchemy import text
from apps.api.database import SessionLocal

def main():
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()

def run_seed(db):
    insert_translations(db, ERROR_DATA)
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
        WHERE key LIKE 'widget.%'
        GROUP BY lang
        ORDER BY lang
    """))
    rows = result.fetchall()
    print("\nVerification - widget namespace:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} keys")

ERROR_DATA: dict[str, dict[str, str]] = {
    "bg": {
        "widget.phone_error": "Въведете валиден телефонен номер",
        "widget.error_message": "Нещо се обърка. Моля, опитайте отново.",
    },
    "cs": {
        "widget.phone_error": "Zadejte platné telefonní číslo",
        "widget.error_message": "Něco se nepovedlo. Zkuste to prosím znovu.",
    },
    "da": {
        "widget.phone_error": "Indtast et gyldigt telefonnummer",
        "widget.error_message": "Noget gik galt. Prøv venligst igen.",
    },
    "de": {
        "widget.phone_error": "Geben Sie eine gültige Telefonnummer ein",
        "widget.error_message": "Etwas ist schief gelaufen. Bitte versuchen Sie es erneut.",
    },
    "el": {
        "widget.phone_error": "Εισαγάγετε έναν έγκυρο αριθμό τηλεφώνου",
        "widget.error_message": "Κάτι πήγε στραβά. Παρακαλώ προσπαθήστε ξανά.",
    },
    "en": {
        "widget.phone_error": "Enter a valid phone number",
        "widget.error_message": "Something went wrong. Please try again.",
    },
    "es": {
        "widget.phone_error": "Ingrese un número de teléfono válido",
        "widget.error_message": "Algo salió mal. Por favor, inténtelo de nuevo.",
    },
    "et": {
        "widget.phone_error": "Sisestage kehtiv telefoninumber",
        "widget.error_message": "Midagi läks valesti. Palun proovige uuesti.",
    },
    "fi": {
        "widget.phone_error": "Anna voimassa oleva puhelinnumero",
        "widget.error_message": "Jokin meni vikaan. Yritä uudelleen.",
    },
    "fr": {
        "widget.phone_error": "Entrez un numéro de téléphone valide",
        "widget.error_message": "Un problème est survenu. Veuillez réessayer.",
    },
    "ga": {
        "widget.phone_error": "Iontráil uimhir theileafóin bhailí",
        "widget.error_message": "Tharla botún. Bain triail as arís, le do thoil.",
    },
    "hr": {
        "widget.phone_error": "Unesite važeći telefonski broj",
        "widget.error_message": "Nešto je pošlo po zlu. Molimo pokušajte ponovno.",
    },
    "hu": {
        "widget.phone_error": "Adjon meg egy érvényes telefonszámot",
        "widget.error_message": "Valami hiba történt. Kérjük, próbálja újra.",
    },
    "is": {
        "widget.phone_error": "Sláðu inn gilt símanúmer",
        "widget.error_message": "Eitthvað fór úrskeiðis. Vinsamlegast reyndu aftur.",
    },
    "it": {
        "widget.phone_error": "Inserisci un numero di telefono valido",
        "widget.error_message": "Qualcosa è andato storto. Riprova.",
    },
    "lb": {
        "widget.phone_error": "Gitt eng valabel Telefonsnummer an",
        "widget.error_message": "Eppes ass schif gaangen. Probéiert w.e.g. nach eng Kéier.",
    },
    "lt": {
        "widget.phone_error": "Įveskite galiojantį telefono numerį",
        "widget.error_message": "Kažkas nepavyko. Bandykite dar kartą.",
    },
    "lv": {
        "widget.phone_error": "Ievadiet derīgu tālruņa numuru",
        "widget.error_message": "Kaut kas nogāja greizi. Lūdzu, mēģiniet vēlreiz.",
    },
    "mk": {
        "widget.phone_error": "Внесете валиден телефонски број",
        "widget.error_message": "Нешто тргна наопаку. Ве молиме обидете се повторно.",
    },
    "mt": {
        "widget.phone_error": "Daħħal numru tat-telefon validu",
        "widget.error_message": "Xi ħaġa marret ħażin. Jekk jogħġbok erġa' pprova.",
    },
    "nl": {
        "widget.phone_error": "Voer een geldig telefoonnummer in",
        "widget.error_message": "Er is iets misgegaan. Probeer het opnieuw.",
    },
    "no": {
        "widget.phone_error": "Oppgi et gyldig telefonnummer",
        "widget.error_message": "Noe gikk galt. Vennligst prøv igjen.",
    },
    "pl": {
        "widget.phone_error": "Wprowadź poprawny numer telefonu",
        "widget.error_message": "Coś poszło nie tak. Spróbuj ponownie.",
    },
    "pt": {
        "widget.phone_error": "Insira um número de telefone válido",
        "widget.error_message": "Algo deu errado. Por favor, tente novamente.",
    },
    "pt-PT": {
        "widget.phone_error": "Introduza um um número de telefone válido",
        "widget.error_message": "Ocorreu um erro. Por favor, tente novamente.",
    },
    "ro": {
        "widget.phone_error": "Introduceți un număr de telefon valid",
        "widget.error_message": "Ceva nu a mers bine. Vă rugăm să încercați din nou.",
    },
    "ru": {
        "widget.phone_error": "Введите действительный номер телефона",
        "widget.error_message": "Что-то пошло не так. Пожалуйста, попробуйте еще раз.",
    },
    "sk": {
        "widget.phone_error": "Zadajte platné telefónne číslo",
        "widget.error_message": "Niečo sa pokazilo. Skúste to znova.",
    },
    "sl": {
        "widget.phone_error": "Vnesite veljavno telefonsko številko",
        "widget.error_message": "Nekaj je šlo narobe. Prosimo, poskusite znova.",
    },
    "sq": {
        "widget.phone_error": "Vendosni një numër telefoni të vlefshëm",
        "widget.error_message": "Diçka shkoi keq. Ju lutem provoni përsëri.",
    },
    "sr": {
        "widget.phone_error": "Унесите важећи број телефона",
        "widget.error_message": "Нешто је пошло наопаку. Молимо покушајте поново.",
    },
    "sv": {
        "widget.phone_error": "Ange ett giltigt telefonnummer",
        "widget.error_message": "Något gick fel. Försök igen.",
    },
    "tr": {
        "widget.phone_error": "Geçerli bir telefon numarası girin",
        "widget.error_message": "Bir şeyler yanlış gitti. Lütfen tekrar deneyin.",
    },
    "uk": {
        "widget.phone_error": "Введіть дійсний номер телефону",
        "widget.error_message": "Щось пішло не так. Будь ласка, спробуйте ще раз.",
    },
}

if __name__ == "__main__":
    main()
