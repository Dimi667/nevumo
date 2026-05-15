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
        WHERE key LIKE 'pdf.%'
        GROUP BY lang
        ORDER BY lang
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} keys")

ALL_TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "pdf.account_id_label": "Account ID",
        "pdf.email_label": "Email",
        "pdf.withdrawal_date_label": "Date of withdrawal",
        "pdf.contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "bg": {
        "pdf.account_id_label": "ID на акаунт",
        "pdf.email_label": "Имейл",
        "pdf.withdrawal_date_label": "Дата на отказ",
        "pdf.contract_date_label": "Дата на сключване на договора / Дата на регистрация на акаунта",
    },
    "pl": {
        "pdf.account_id_label": "ID konta",
        "pdf.email_label": "E-mail",
        "pdf.withdrawal_date_label": "Data odstąpienia",
        "pdf.contract_date_label": "Data zawarcia umowy / Data rejestracji konta",
    },
    "cs": {
        "pdf.account_id_label": "ID účtu",
        "pdf.email_label": "E-mail",
        "pdf.withdrawal_date_label": "Datum odstoupení",
        "pdf.contract_date_label": "Datum uzavření smlouvy / Datum registrace účtu",
    },
    "da": {
        "pdf.account_id_label": "Konto-ID",
        "pdf.email_label": "E-mail",
        "pdf.withdrawal_date_label": "Fortrydelsesdato",
        "pdf.contract_date_label": "Dato for indgåelse af kontrakt / Dato for kontoregistrering",
    },
    "de": {
        "pdf.account_id_label": "Konto-ID",
        "pdf.email_label": "E-Mail",
        "pdf.withdrawal_date_label": "Widerrufsdatum",
        "pdf.contract_date_label": "Datum des Vertragsabschlusses / Datum der Kontoregistrierung",
    },
    "el": {
        "pdf.account_id_label": "ID λογαριασμού",
        "pdf.email_label": "Email",
        "pdf.withdrawal_date_label": "Ημερομηνία υπαναχώρησης",
        "pdf.contract_date_label": "Ημερομηνία σύναψης συμβολαίου / Ημερομηνία εγγραφής λογαριασμού",
    },
    "es": {
        "pdf.account_id_label": "ID de la cuenta",
        "pdf.email_label": "Correo electrónico",
        "pdf.withdrawal_date_label": "Fecha de desistimiento",
        "pdf.contract_date_label": "Fecha de celebración del contrato / Fecha de registro de la cuenta",
    },
    "et": {
        "pdf.account_id_label": "Konto ID",
        "pdf.email_label": "E-post",
        "pdf.withdrawal_date_label": "Taganemise kuupäev",
        "pdf.contract_date_label": "Lepingu sõlmimise kuupäev / Konto registreerimise kuupäev",
    },
    "fi": {
        "pdf.account_id_label": "Tilin tunnus",
        "pdf.email_label": "Sähköposti",
        "pdf.withdrawal_date_label": "Peruuttamispäivä",
        "pdf.contract_date_label": "Sopimuksen solmimispäivä / Tilin rekisteröintipäivä",
    },
    "fr": {
        "pdf.account_id_label": "ID du compte",
        "pdf.email_label": "E-mail",
        "pdf.withdrawal_date_label": "Date de rétractation",
        "pdf.contract_date_label": "Date de conclusion du contrat / Date d'enregistrement du compte",
    },
    "ga": {
        "pdf.account_id_label": "ID cunta",
        "pdf.email_label": "Ríomhphost",
        "pdf.withdrawal_date_label": "Dáta tarraingthe siar",
        "pdf.contract_date_label": "Dáta dhéanta an chonarthaigh / Dáta cláraithe an chuntais",
    },
    "hr": {
        "pdf.account_id_label": "ID računa",
        "pdf.email_label": "E-mail",
        "pdf.withdrawal_date_label": "Datum odustajanja",
        "pdf.contract_date_label": "Datum zaključenja ugovora / Datum registracije računa",
    },
    "hu": {
        "pdf.account_id_label": "Fiókazonosító",
        "pdf.email_label": "E-mail",
        "pdf.withdrawal_date_label": "Elállás dátuma",
        "pdf.contract_date_label": "A szerződés megkötésének dátuma / A fiók regisztrációjának dátuma",
    },
    "is": {
        "pdf.account_id_label": "Auðkenni reiknings",
        "pdf.email_label": "Netfang",
        "pdf.withdrawal_date_label": "Dagsetning uppsagnar",
        "pdf.contract_date_label": "Dagsetning samningsgerðar / Dagsetning reikningsskráningar",
    },
    "it": {
        "pdf.account_id_label": "ID account",
        "pdf.email_label": "E-mail",
        "pdf.withdrawal_date_label": "Data di recesso",
        "pdf.contract_date_label": "Data di conclusione del contratto / Data di registrazione dell'account",
    },
    "lb": {
        "pdf.account_id_label": "Kont-ID",
        "pdf.email_label": "E-Mail",
        "pdf.withdrawal_date_label": "Datum vum Widderruff",
        "pdf.contract_date_label": "Datum vun der Vertragsabschloss / Datum vun der Kontoregistréierung",
    },
    "lt": {
        "pdf.account_id_label": "Paskyros ID",
        "pdf.email_label": "El. paštas",
        "pdf.withdrawal_date_label": "Atsisakymo data",
        "pdf.contract_date_label": "Sutarties sudarymo data / Paskyros registracijos data",
    },
    "lv": {
        "pdf.account_id_label": "Konta ID",
        "pdf.email_label": "E-pasts",
        "pdf.withdrawal_date_label": "Atteikuma datums",
        "pdf.contract_date_label": "Līguma noslēgšanas datums / Konta reģistrācijas datums",
    },
    "mk": {
        "pdf.account_id_label": "ID на сметка",
        "pdf.email_label": "Е-пошта",
        "pdf.withdrawal_date_label": "Датум на повлекување",
        "pdf.contract_date_label": "Датум на склучување на договор / Датум на регистрација на сметка",
    },
    "mt": {
        "pdf.account_id_label": "ID tal-kont",
        "pdf.email_label": "Email",
        "pdf.withdrawal_date_label": "Data tal-irtirar",
        "pdf.contract_date_label": "Data tal-konklużjoni tal-kuntratt / Data tar-reġistrazzjoni tal-kont",
    },
    "nl": {
        "pdf.account_id_label": "Account-ID",
        "pdf.email_label": "E-mail",
        "pdf.withdrawal_date_label": "Datum van herroeping",
        "pdf.contract_date_label": "Datum van afsluiting van het contract / Datum van accountregistratie",
    },
    "no": {
        "pdf.account_id_label": "Konto-ID",
        "pdf.email_label": "E-post",
        "pdf.withdrawal_date_label": "Angredato",
        "pdf.contract_date_label": "Dato for kontraktinngåelse / Dato for kontoregistrering",
    },
    "pt": {
        "pdf.account_id_label": "ID da conta",
        "pdf.email_label": "E-mail",
        "pdf.withdrawal_date_label": "Data de livre resolução",
        "pdf.contract_date_label": "Data de celebração do contrato / Data de registro da conta",
    },
    "pt-PT": {
        "pdf.account_id_label": "ID da conta",
        "pdf.email_label": "E-mail",
        "pdf.withdrawal_date_label": "Data de livre resolução",
        "pdf.contract_date_label": "Data de celebração do contrato / Data de registo da conta",
    },
    "ro": {
        "pdf.account_id_label": "ID cont",
        "pdf.email_label": "E-mail",
        "pdf.withdrawal_date_label": "Data retragerii",
        "pdf.contract_date_label": "Data încheierii contractului / Data înregistrării contului",
    },
    "ru": {
        "pdf.account_id_label": "ID аккаунта",
        "pdf.email_label": "Электронная почта",
        "pdf.withdrawal_date_label": "Дата отказа",
        "pdf.contract_date_label": "Дата заключения договора / Дата регистрации аккаунта",
    },
    "sk": {
        "pdf.account_id_label": "ID účtu",
        "pdf.email_label": "E-mail",
        "pdf.withdrawal_date_label": "Dátum odstúpenia",
        "pdf.contract_date_label": "Dátum uzavretia zmluvy / Dátum registrácie účtu",
    },
    "sl": {
        "pdf.account_id_label": "ID računa",
        "pdf.email_label": "E-pošta",
        "pdf.withdrawal_date_label": "Datum odstopa",
        "pdf.contract_date_label": "Datum sklenitve pogodbe / Datum registracije računa",
    },
    "sq": {
        "pdf.account_id_label": "ID-ja e llogarisë",
        "pdf.email_label": "Email",
        "pdf.withdrawal_date_label": "Data e tërheqjes",
        "pdf.contract_date_label": "Data e përfundimit të kontratës / Data e regjistrimit të llogarisë",
    },
    "sr": {
        "pdf.account_id_label": "ID naloga",
        "pdf.email_label": "E-mail",
        "pdf.withdrawal_date_label": "Datum odustanka",
        "pdf.contract_date_label": "Datum zaključenja ugovora / Datum registracije naloga",
    },
    "sv": {
        "pdf.account_id_label": "Konto-ID",
        "pdf.email_label": "E-post",
        "pdf.withdrawal_date_label": "Datum för frånträdande",
        "pdf.contract_date_label": "Datum för avtalets ingåelse / Datum för kontoregistrering",
    },
    "tr": {
        "pdf.account_id_label": "Hesap ID'si",
        "pdf.email_label": "E-posta",
        "pdf.withdrawal_date_label": "Cayma tarihi",
        "pdf.contract_date_label": "Sözleşmenin imzalanma tarihi / Hesap kayıt tarihi",
    },
    "uk": {
        "pdf.account_id_label": "ID акаунта",
        "pdf.email_label": "Електронна пошта",
        "pdf.withdrawal_date_label": "Дата відмови",
        "pdf.contract_date_label": "Дата укладення договору / Дата реєстрації облікового запису",
    },
}

if __name__ == "__main__":
    main()
