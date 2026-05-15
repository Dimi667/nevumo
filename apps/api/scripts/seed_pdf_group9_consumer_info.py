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
        WHERE key LIKE 'pdf.consumer_%_label'
        GROUP BY lang
        ORDER BY lang
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} keys")

ALL_TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "pdf.consumer_name_label": "Name of consumer(s)",
        "pdf.consumer_address_label": "Address of consumer(s)",
        "pdf.consumer_signature_label": "Signature of consumer(s)",
    },
    "bg": {
        "pdf.consumer_name_label": "Име на потребителя/-ите",
        "pdf.consumer_address_label": "Адрес на потребителя/-ите",
        "pdf.consumer_signature_label": "Подпис на потребителя/-ите",
    },
    "pl": {
        "pdf.consumer_name_label": "Imię i nazwisko konsumenta(-ów)",
        "pdf.consumer_address_label": "Adres konsumenta(-ów)",
        "pdf.consumer_signature_label": "Podpis konsumenta(-ów)",
    },
    "cs": {
        "pdf.consumer_name_label": "Jméno spotřebitele (spotřebitelů)",
        "pdf.consumer_address_label": "Adresa spotřebitele (spotřebitelů)",
        "pdf.consumer_signature_label": "Podpis spotřebitele (spotřebitelů)",
    },
    "da": {
        "pdf.consumer_name_label": "Forbrugerens/forbrugernes navn(e)",
        "pdf.consumer_address_label": "Forbrugerens/forbrugernes adresse(r)",
        "pdf.consumer_signature_label": "Forbrugerens/forbrugernes underskrift(er)",
    },
    "de": {
        "pdf.consumer_name_label": "Name des/der Verbraucher(s)",
        "pdf.consumer_address_label": "Anschrift des/der Verbraucher(s)",
        "pdf.consumer_signature_label": "Unterschrift des/der Verbraucher(s)",
    },
    "el": {
        "pdf.consumer_name_label": "Όνομα καταναλωτή(-ών)",
        "pdf.consumer_address_label": "Διεύθυνση καταναλωτή(-ών)",
        "pdf.consumer_signature_label": "Υπογραφή καταναλωτή(-ών)",
    },
    "es": {
        "pdf.consumer_name_label": "Nombre del consumidor o de los consumidores",
        "pdf.consumer_address_label": "Dirección del consumidor o de los consumidores",
        "pdf.consumer_signature_label": "Firma del consumidor o de los consumidores",
    },
    "et": {
        "pdf.consumer_name_label": "Tarbija(te) nimi",
        "pdf.consumer_address_label": "Tarbija(te) aadress",
        "pdf.consumer_signature_label": "Tarbija(te) allkiri",
    },
    "fi": {
        "pdf.consumer_name_label": "Kuluttajan/kuluttajien nimi (nimet)",
        "pdf.consumer_address_label": "Kuluttajan/kuluttajien osoite (osoitteet)",
        "pdf.consumer_signature_label": "Kuluttajan/kuluttajien allekirjoitus (allekirjoitukset)",
    },
    "fr": {
        "pdf.consumer_name_label": "Nom du (des) consommateur(s)",
        "pdf.consumer_address_label": "Adresse du (des) consommateur(s)",
        "pdf.consumer_signature_label": "Signature du (des) consommateur(s)",
    },
    "ga": {
        "pdf.consumer_name_label": "Ainm an tomhaltóra/na dtomhaltóirí",
        "pdf.consumer_address_label": "Seoladh an tomhaltóra/na dtomhaltóirí",
        "pdf.consumer_signature_label": "Síniú an tomhaltóra/na dtomhaltóirí",
    },
    "hr": {
        "pdf.consumer_name_label": "Ime potrošača",
        "pdf.consumer_address_label": "Adresa potrošača",
        "pdf.consumer_signature_label": "Potpis potrošača",
    },
    "hu": {
        "pdf.consumer_name_label": "A fogyasztó(k) neve",
        "pdf.consumer_address_label": "A fogyasztó(k) címe",
        "pdf.consumer_signature_label": "A fogyasztó(k) aláírása",
    },
    "is": {
        "pdf.consumer_name_label": "Nafn neytanda/neytenda",
        "pdf.consumer_address_label": "Heimilisfang neytanda/neytenda",
        "pdf.consumer_signature_label": "Undirskrift neytanda/neytenda",
    },
    "it": {
        "pdf.consumer_name_label": "Nome del consumatore (o dei consumatori)",
        "pdf.consumer_address_label": "Indirizzo del consumatore (o dei consumatori)",
        "pdf.consumer_signature_label": "Firma del consumatore (o dei consumatori)",
    },
    "lt": {
        "pdf.consumer_name_label": "Vartotojo (-ų) vardas ir pavardė",
        "pdf.consumer_address_label": "Vartotojo (-ų) adresas",
        "pdf.consumer_signature_label": "Vartotojo (-ų) parašas (-ai)",
    },
    "lv": {
        "pdf.consumer_name_label": "Patērētāja(-u) vārds(-i) un uzvārds(-i)",
        "pdf.consumer_address_label": "Patērētāja(-u) adrese(-es)",
        "pdf.consumer_signature_label": "Patērētāja(-u) paraksts(-i)",
    },
    "mt": {
        "pdf.consumer_name_label": "Isem tal-konsumatur(i)",
        "pdf.consumer_address_label": "Indirizz tal-konsumatur(i)",
        "pdf.consumer_signature_label": "Firma tal-konsumatur(i)",
    },
    "nl": {
        "pdf.consumer_name_label": "Naam van consument(en)",
        "pdf.consumer_address_label": "Adres van consument(en)",
        "pdf.consumer_signature_label": "Handtekening van consument(en)",
    },
    "no": {
        "pdf.consumer_name_label": "Forbrukerens navn",
        "pdf.consumer_address_label": "Forbrukerens adresse",
        "pdf.consumer_signature_label": "Forbrukerens underskrift",
    },
    "pt": {
        "pdf.consumer_name_label": "Nome do(s) consumidor(es)",
        "pdf.consumer_address_label": "Endereço do(s) consumidor(es)",
        "pdf.consumer_signature_label": "Assinatura do(s) consumidor(es)",
    },
    "ro": {
        "pdf.consumer_name_label": "Numele consumatorului (consumatorilor)",
        "pdf.consumer_address_label": "Adresa consumatorului (consumatorilor)",
        "pdf.consumer_signature_label": "Semnătura consumatorului (consumatorilor)",
    },
    "sk": {
        "pdf.consumer_name_label": "Meno spotrebiteľa (spotrebiteľov)",
        "pdf.consumer_address_label": "Adresa spotrebiteľa (spotrebiteľov)",
        "pdf.consumer_signature_label": "Podpis spotrebiteľa (spotrebiteľov)",
    },
    "sl": {
        "pdf.consumer_name_label": "Ime potrošnika (potrošnikov)",
        "pdf.consumer_address_label": "Naslov potrošnika (potrošnikov)",
        "pdf.consumer_signature_label": "Podpis potrošnika (potrošnikov)",
    },
    "sv": {
        "pdf.consumer_name_label": "Konsumentens/konsumenternas namn",
        "pdf.consumer_address_label": "Konsumentens/konsumenternas adress",
        "pdf.consumer_signature_label": "Konsumentens/konsumenternas underskrift(er)",
    },
    "tr": {
        "pdf.consumer_name_label": "Tüketicinin (tüketicilerin) adı",
        "pdf.consumer_address_label": "Tüketicinin (tüketicilerin) adresi",
        "pdf.consumer_signature_label": "Tüketicinin (tüketicilerin) imzası",
    },
    "uk": {
        "pdf.consumer_name_label": "Ім'я споживача(-ів)",
        "pdf.consumer_address_label": "Адреса споживача(-ів)",
        "pdf.consumer_signature_label": "Підпис споживача(-ів)",
    },
    "ru": {
        "pdf.consumer_name_label": "Имя потребителя(-ей)",
        "pdf.consumer_address_label": "Адрес потребителя(-ей)",
        "pdf.consumer_signature_label": "Подпись потребителя(-ей)",
    },
    "sr": {
        "pdf.consumer_name_label": "Ime potrošača",
        "pdf.consumer_address_label": "Adresa potrošača",
        "pdf.consumer_signature_label": "Potpis potrošača",
    },
    "mk": {
        "pdf.consumer_name_label": "Име на потрошувачот/-ите",
        "pdf.consumer_address_label": "Адреса на потрошувачот/-ите",
        "pdf.consumer_signature_label": "Подпис на потрошувачот/-ите",
    },
    "sq": {
        "pdf.consumer_name_label": "Emri i konsumatorit(ëve)",
        "pdf.consumer_address_label": "Adresa e konsumatorit(ëve)",
        "pdf.consumer_signature_label": "Nënshkrimi i konsumatorit(ëve)",
    },
    "bs": {
        "pdf.consumer_name_label": "Ime potrošača",
        "pdf.consumer_address_label": "Adresa potrošača",
        "pdf.consumer_signature_label": "Potpis potrošača",
    },
    "me": {
        "pdf.consumer_name_label": "Ime potrošača",
        "pdf.consumer_address_label": "Adresa potrošača",
        "pdf.consumer_signature_label": "Potpis potrošača",
    },
}

if __name__ == "__main__":
    main()
