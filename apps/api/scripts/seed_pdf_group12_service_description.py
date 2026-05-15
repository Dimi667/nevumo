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
        "pdf.service_description_label": "Description of service",
        "pdf.service_description_placeholder": "Please describe the service you wish to withdraw from",
    },
    "bg": {
        "pdf.service_description_label": "Описание на услугата",
        "pdf.service_description_placeholder": "Моля опишете услугата, от която искате да се откажете",
    },
    "pl": {
        "pdf.service_description_label": "Opis usługi",
        "pdf.service_description_placeholder": "Proszę opisać usługę, od której chcesz odstąpić",
    },
    "cs": {
        "pdf.service_description_label": "Popis služby",
        "pdf.service_description_placeholder": "Popište prosím službu, od které chcete odstoupit",
    },
    "da": {
        "pdf.service_description_label": "Beskrivelse af tjenesten",
        "pdf.service_description_placeholder": "Beskriv venligst den tjeneste, du ønsker at fortryde",
    },
    "de": {
        "pdf.service_description_label": "Beschreibung der Dienstleistung",
        "pdf.service_description_placeholder": "Bitte beschreiben Sie die Dienstleistung, die Sie widerrufen möchten",
    },
    "el": {
        "pdf.service_description_label": "Περιγραφή της υπηρεσίας",
        "pdf.service_description_placeholder": "Παρακαλούμε περιγράψτε την υπηρεσία από την οποία επιθυμείτε να υπαναχωρήσετε",
    },
    "es": {
        "pdf.service_description_label": "Descripción del servicio",
        "pdf.service_description_placeholder": "Por favor, describa el servicio del que desea desistir",
    },
    "et": {
        "pdf.service_description_label": "Teenuse kirjeldus",
        "pdf.service_description_placeholder": "Palun kirjeldage teenust, millest soovite taganeda",
    },
    "fi": {
        "pdf.service_description_label": "Palvelun kuvaus",
        "pdf.service_description_placeholder": "Kuvaile palvelu, josta haluat peruuttaa sopimuksen",
    },
    "fr": {
        "pdf.service_description_label": "Description du service",
        "pdf.service_description_placeholder": "Veuillez décrire le service dont vous souhaitez vous rétracter",
    },
    "ga": {
        "pdf.service_description_label": "Cur síos ar an tseirbhís",
        "pdf.service_description_placeholder": "Déan cur síos le do thoil ar an tseirbhís ar mian leat tarraingt siar aisti",
    },
    "hr": {
        "pdf.service_description_label": "Opis usluge",
        "pdf.service_description_placeholder": "Opišite uslugu od koje želite odustati",
    },
    "hu": {
        "pdf.service_description_label": "A szolgáltatás leírása",
        "pdf.service_description_placeholder": "Kérjük, írja le a szolgáltatást, amelytől el kíván állni",
    },
    "is": {
        "pdf.service_description_label": "Lýsing á þjónustu",
        "pdf.service_description_placeholder": "Vinsamlegast lýstu þjónustunni sem þú vilt hætta við",
    },
    "it": {
        "pdf.service_description_label": "Descrizione del servizio",
        "pdf.service_description_placeholder": "Descrivere il servizio da cui si desidera recedere",
    },
    "lb": {
        "pdf.service_description_label": "Beschreiwung vum Service",
        "pdf.service_description_placeholder": "Beschreift w.e.g. de Service, vun deem Dir wëllt zerécktrieden",
    },
    "lt": {
        "pdf.service_description_label": "Paslaugos aprašymas",
        "pdf.service_description_placeholder": "Aprašykite paslaugą, kurios norite atsisakyti",
    },
    "lv": {
        "pdf.service_description_label": "Pakalpojuma apraksts",
        "pdf.service_description_placeholder": "Lūdzu, aprakstiet pakalpojumu, no kura vēlaties atteikties",
    },
    "mk": {
        "pdf.service_description_label": "Опис на услугата",
        "pdf.service_description_placeholder": "Ве молиме опишете ја услугата од која сакате да се откажете",
    },
    "mt": {
        "pdf.service_description_label": "Deskrizzjoni tas-servizz",
        "pdf.service_description_placeholder": "Jekk jogħġbok iddeskrivi s-servizz li tixtieq tirtira minnu",
    },
    "nl": {
        "pdf.service_description_label": "Beschrijving van de dienst",
        "pdf.service_description_placeholder": "Beschrijf de dienst waarvan u wilt afzien",
    },
    "no": {
        "pdf.service_description_label": "Beskrivelse af tjenesten",
        "pdf.service_description_placeholder": "Vennligst beskriv tjenesten du ønsker å gå fra",
    },
    "pt": {
        "pdf.service_description_label": "Descrição do serviço",
        "pdf.service_description_placeholder": "Descreva o serviço do qual pretende desistir",
    },
    "pt-PT": {
        "pdf.service_description_label": "Descrição do serviço",
        "pdf.service_description_placeholder": "Descreva o serviço do qual pretende desistir",
    },
    "ro": {
        "pdf.service_description_label": "Descrierea serviciului",
        "pdf.service_description_placeholder": "Vă rugăm să descrieți serviciul de la care doriți să vă retrageți",
    },
    "ru": {
        "pdf.service_description_label": "Описание услуги",
        "pdf.service_description_placeholder": "Пожалуйста, опишите услугу, от которой вы хотите отказаться",
    },
    "sk": {
        "pdf.service_description_label": "Popis služby",
        "pdf.service_description_placeholder": "Popíšte, prosím, službu, od ktorej chcete odstúpiť",
    },
    "sl": {
        "pdf.service_description_label": "Opis storitve",
        "pdf.service_description_placeholder": "Opišite storitev, od katere želite odstopiti",
    },
    "sq": {
        "pdf.service_description_label": "Përshkrimi i shërbimit",
        "pdf.service_description_placeholder": "Ju lutem përshkruani shërbimin nga i cili dëshironi të tërhiqeni",
    },
    "sr": {
        "pdf.service_description_label": "Opis usluge",
        "pdf.service_description_placeholder": "Molimo opišite uslugu od koje želite da odustanete",
    },
    "sv": {
        "pdf.service_description_label": "Beskrivning av tjänsten",
        "pdf.service_description_placeholder": "Beskriv tjänsten som du vill frånträda",
    },
    "tr": {
        "pdf.service_description_label": "Hizmetin açıklaması",
        "pdf.service_description_placeholder": "Lütfen vazgeçmek istediğiniz hizmeti tanımlayın",
    },
    "uk": {
        "pdf.service_description_label": "Опис послуги",
        "pdf.service_description_placeholder": "Будь ласка, опишіть послугу, від якої ви хочете відмовитися",
    },
}

if __name__ == "__main__":
    main()
