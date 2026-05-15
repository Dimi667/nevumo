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
        "withdrawal.page_title": "Withdrawal Form",
        "withdrawal.page_description": "Complete this form to withdraw from your Nevumo contract",
        "withdrawal.form_service_description_label": "Description of service / contract",
        "withdrawal.form_contract_date_label": "Date of conclusion of contract / Date of account registration",
    },
    "bg": {
        "withdrawal.page_title": "Формуляр за отказ",
        "withdrawal.page_description": "Попълнете този формуляр, за да се откажете от договора си с Nevumo",
        "withdrawal.form_service_description_label": "Описание на услугата / договора",
        "withdrawal.form_contract_date_label": "Дата на сключване на договора / Дата на регистрация на акаунта",
    },
    "pl": {
        "withdrawal.page_title": "Formularz odstąpienia od umowy",
        "withdrawal.page_description": "Wypełnij ten formularz, aby odstąpić od umowy z Nevumo",
        "withdrawal.form_service_description_label": "Opis usługi / umowy",
        "withdrawal.form_contract_date_label": "Data zawarcia umowy / Data rejestracji konta",
    },
    "cs": {
        "withdrawal.page_title": "Formulář pro odstoupení",
        "withdrawal.page_description": "Vyplněním tohoto formuláře odstoupíte od smlouvy s Nevumo",
        "withdrawal.form_service_description_label": "Popis služby / smlouvy",
        "withdrawal.form_contract_date_label": "Datum uzavření smlouvy / Datum registrace účtu",
    },
    "da": {
        "withdrawal.page_title": "Fortrydelsesformular",
        "withdrawal.page_description": "Udfyld denne formular for at fortryde din Nevumo-kontrakt",
        "withdrawal.form_service_description_label": "Beskrivelse af tjenesteydelsen / kontrakten",
        "withdrawal.form_contract_date_label": "Dato for indgåelse af kontrakt / Dato for kontoregistrering",
    },
    "de": {
        "withdrawal.page_title": "Widerrufsformular",
        "withdrawal.page_description": "Füllen Sie dieses Formular aus, um von Ihrem Nevumo-Vertrag zurückzutreten",
        "withdrawal.form_service_description_label": "Beschreibung der Dienstleistung / des Vertrags",
        "withdrawal.form_contract_date_label": "Datum des Vertragsabschlusses / Datum der Kontoregistrierung",
    },
    "el": {
        "withdrawal.page_title": "Έντυπο Υπαναχώρησης",
        "withdrawal.page_description": "Συμπληρώστε αυτό το έντυπο για να υπαναχωρήσετε από τη σύμβασή σας με τη Nevumo",
        "withdrawal.form_service_description_label": "Περιγραφή υπηρεσίας / σύμβασης",
        "withdrawal.form_contract_date_label": "Ημερομηνία σύναψης σύμβασης / Ημερομηνία εγγραφής λογαριασμού",
    },
    "es": {
        "withdrawal.page_title": "Formulario de Desistimiento",
        "withdrawal.page_description": "Complete este formulario para desistir de su contrato con Nevumo",
        "withdrawal.form_service_description_label": "Descripción del servicio / contrato",
        "withdrawal.form_contract_date_label": "Fecha de celebración del contrato / Fecha de registro de la cuenta",
    },
    "et": {
        "withdrawal.page_title": "Taganemisavaldus",
        "withdrawal.page_description": "Täitke see vorm Nevumo lepingust taganemiseks",
        "withdrawal.form_service_description_label": "Teenuse / lepingu kirjeldus",
        "withdrawal.form_contract_date_label": "Lepingu sõlmimise kuupäev / Konto registreerimise kuupäev",
    },
    "fi": {
        "withdrawal.page_title": "Peruuttamislomake",
        "withdrawal.page_description": "Täytä tämä lomake peruuttaaksesi Nevumo-sopimuksesi",
        "withdrawal.form_service_description_label": "Palvelun / sopimuksen kuvaus",
        "withdrawal.form_contract_date_label": "Sopimuksen tekopäivä / Tilin rekisteröintipäivä",
    },
    "fr": {
        "withdrawal.page_title": "Formulaire de Rétractation",
        "withdrawal.page_description": "Remplissez ce formulaire pour vous rétracter de votre contrat Nevumo",
        "withdrawal.form_service_description_label": "Description du service / contrat",
        "withdrawal.form_contract_date_label": "Date de conclusion du contrat / Date d'inscription du compte",
    },
    "ga": {
        "withdrawal.page_title": "Foirm Tharraingthe Siar",
        "withdrawal.page_description": "Comhlánaigh an fhoirm seo chun tarraingt siar ó do chonradh Nevumo",
        "withdrawal.form_service_description_label": "Cur síos ar an tseirbhís / conradh",
        "withdrawal.form_contract_date_label": "Dáta tugtha chun críche an chonartha / Dáta clárúcháin an chuntais",
    },
    "hr": {
        "withdrawal.page_title": "Obrazac za odustajanje",
        "withdrawal.page_description": "Ispunite ovaj obrazac kako biste odustali od svog ugovora s Nevumom",
        "withdrawal.form_service_description_label": "Opis usluge / ugovora",
        "withdrawal.form_contract_date_label": "Datum sklapanja ugovora / Datum registracije računa",
    },
    "hu": {
        "withdrawal.page_title": "Elállási nyilatkozat",
        "withdrawal.page_description": "Töltse ki ezt az űrlapot a Nevumo szerződéstől való elálláshoz",
        "withdrawal.form_service_description_label": "A szolgáltatás / szerződés leírása",
        "withdrawal.form_contract_date_label": "Szerződéskötés dátuma / Fiók regisztrációjának dátuma",
    },
    "is": {
        "withdrawal.page_title": "Uppsagnareyðublað",
        "withdrawal.page_description": "Fylltu út þetta eyðublað til að segja upp Nevumo samningnum þínum",
        "withdrawal.form_service_description_label": "Lýsing á þjónustu / samningi",
        "withdrawal.form_contract_date_label": "Dagsetning samningsgerðar / Dagsetning nýskráningar",
    },
    "it": {
        "withdrawal.page_title": "Modulo di Recesso",
        "withdrawal.page_description": "Compila questo modulo per recedere dal tuo contratto Nevumo",
        "withdrawal.form_service_description_label": "Descrizione del servicio / contratto",
        "withdrawal.form_contract_date_label": "Data di conclusione del contratto / Data di registrazione dell'account",
    },
    "lb": {
        "withdrawal.page_title": "Récktrëttsformular",
        "withdrawal.page_description": "Fëllt dëse Formular aus, fir vun Ärem Nevumo-Kontrakt zeréckzetrieden",
        "withdrawal.form_service_description_label": "Beschreiwung vum Service / Kontrakt",
        "withdrawal.form_contract_date_label": "Datum vum Ofschloss vum Kontrakt / Datum vun der Kontoregistréierung",
    },
    "lt": {
        "withdrawal.page_title": "Sutarties atsisakymo forma",
        "withdrawal.page_description": "Užpildykite šią formą, kad atsisakytumėte „Nevumo“ sutarties",
        "withdrawal.form_service_description_label": "Paslaugos / sutarties aprašymas",
        "withdrawal.form_contract_date_label": "Sutarties sudarymo data / Paskyros registracijos data",
    },
    "lv": {
        "withdrawal.page_title": "Atteikuma veidlapa",
        "withdrawal.page_description": "Aizpildiet šo veidlapu, lai atteiktos no sava Nevumo līguma",
        "withdrawal.form_service_description_label": "Pakalpojuma / līguma apraksts",
        "withdrawal.form_contract_date_label": "Līguma noslēgšanas datums / Konta reģistrācijas datums",
    },
    "mk": {
        "withdrawal.page_title": "Формулар за повлекување",
        "withdrawal.page_description": "Пополнете го овој формуляр за да се повлечете од вашиот договор со Nevumo",
        "withdrawal.form_service_description_label": "Опис на услугата / договорот",
        "withdrawal.form_contract_date_label": "Датум на склучување на договорот / Датум на регистрација на сметката",
    },
    "mt": {
        "withdrawal.page_title": "Formola ta' Reċess",
        "withdrawal.page_description": "Imla din il-formola biex tirtira mill-kuntratt tiegħek ta' Nevumo",
        "withdrawal.form_service_description_label": "Deskrizzjoni tas-servizz / kuntratt",
        "withdrawal.form_contract_date_label": "Data tal-konklużjoni tal-kuntratt / Data tar-reġistrazzjoni tal-kont",
    },
    "nl": {
        "withdrawal.page_title": "Herroepingsformulier",
        "withdrawal.page_description": "Vul dit formulier in om uw Nevumo-contract te herroepen",
        "withdrawal.form_service_description_label": "Beschrijving van dienst / contract",
        "withdrawal.form_contract_date_label": "Datum van sluiting van contract / Datum van accountregistratie",
    },
    "no": {
        "withdrawal.page_title": "Angreskjema",
        "withdrawal.page_description": "Fyll ut dette skjemaet for å gå gå fra din Nevumo-kontrakt",
        "withdrawal.form_service_description_label": "Beskrivelse av tjeneste / kontrakt",
        "withdrawal.form_contract_date_label": "Dato for inngåelse av kontrakt / Dato for kontoregistrering",
    },
    "pt": {
        "withdrawal.page_title": "Formulário de Livre Resolução",
        "withdrawal.page_description": "Preencha este formulário para rescindir o seu contrato Nevumo",
        "withdrawal.form_service_description_label": "Descrição do serviço / contrato",
        "withdrawal.form_contract_date_label": "Data de celebração do contrato / Data de registo da conta",
    },
    "pt-PT": {
        "withdrawal.page_title": "Formulário de Livre Resolução",
        "withdrawal.page_description": "Preencha este formulário para rescindir o seu contrato Nevumo",
        "withdrawal.form_service_description_label": "Descrição do serviço / contrato",
        "withdrawal.form_contract_date_label": "Data de celebração do contrato / Data de registo da conta",
    },
    "ro": {
        "withdrawal.page_title": "Formular de retragere",
        "withdrawal.page_description": "Completați acest formular pentru a vă retrage din contractul Nevumo",
        "withdrawal.form_service_description_label": "Descrierea serviciului / contractului",
        "withdrawal.form_contract_date_label": "Data încheierii contractului / Data înregistrării contului",
    },
    "ru": {
        "withdrawal.page_title": "Форма отказа",
        "withdrawal.page_description": "Заполните эту форму, чтобы расторгнуть договор с Nevumo",
        "withdrawal.form_service_description_label": "Описание услуги / договора",
        "withdrawal.form_contract_date_label": "Дата заключения договора / Дата регистрации аккаунта",
    },
    "sk": {
        "withdrawal.page_title": "Formulár na odstúpenie",
        "withdrawal.page_description": "Vyplnením tohto formulára odstúpite od zmluvy s Nevumo",
        "withdrawal.form_service_description_label": "Popis služby / zmluvy",
        "withdrawal.form_contract_date_label": "Dátum uzavretia zmluvy / Dátum registrácie účtu",
    },
    "sl": {
        "withdrawal.page_title": "Obrazec za odstop",
        "withdrawal.page_description": "Izpolnite ta obrazec za odstop od pogodbe z Nevumom",
        "withdrawal.form_service_description_label": "Opis storitve / pogodbe",
        "withdrawal.form_contract_date_label": "Datum sklenitve pogodbe / Datum registracije računa",
    },
    "sq": {
        "withdrawal.page_title": "Formulari i tërheqjes",
        "withdrawal.page_description": "Plotësoni këtı formular për t'u tërhequr nga kontrata juaj Nevumo",
        "withdrawal.form_service_description_label": "Përshkrimi i shërbimit / kontratës",
        "withdrawal.form_contract_date_label": "Data e lidhjes së kontratës / Data e regjistrimit të llogarisë",
    },
    "sr": {
        "withdrawal.page_title": "Obrazac za odustanak",
        "withdrawal.page_description": "Popunite ovaj obrazac da biste odustali od ugovora sa Nevumom",
        "withdrawal.form_service_description_label": "Opis usluge / ugovora",
        "withdrawal.form_contract_date_label": "Datum zaključenja ugovora / Datum registracije naloga",
    },
    "sv": {
        "withdrawal.page_title": "Frånträdesblankett",
        "withdrawal.page_description": "Fyll i denna blankett för att frånträda ditt Nevumo-avtal",
        "withdrawal.form_service_description_label": "Beskrivning av tjänst / avtal",
        "withdrawal.form_contract_date_label": "Datum för ingående av avtal / Datum för kontoregistrering",
    },
    "tr": {
        "withdrawal.page_title": "Cayma Formu",
        "withdrawal.page_description": "Nevumo sözleşmenizden caymak için bu formu doldurun",
        "withdrawal.form_service_description_label": "Hizmet / sözleşme açıklaması",
        "withdrawal.form_contract_date_label": "Sözleşmenin kurulma tarihi / Hesap kayıt tarihi",
    },
    "uk": {
        "withdrawal.page_title": "Форма відмови",
        "withdrawal.page_description": "Заповніть цю форму, щоб розірвати договір з Nevumo",
        "withdrawal.form_service_description_label": "Опис послуги / договору",
        "withdrawal.form_contract_date_label": "Дата укладення договору / Дата реєстрації акаунта",
    },
}

if __name__ == "__main__":
    main()
