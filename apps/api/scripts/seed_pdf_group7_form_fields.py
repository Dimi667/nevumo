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
        "pdf.form_to_label": "To:",
        "pdf.form_date_label": "Date:",
        "pdf.form_i_declare_label": "I hereby declare that I withdraw from my contract concluded with you for the supply of the following service:",
    },
    "bg": {
        "pdf.form_to_label": "До:",
        "pdf.form_date_label": "Дата:",
        "pdf.form_i_declare_label": "С настоящото декларирам, че се отказвам от договора си, сключен с вас за предоставяне на следната услуга:",
    },
    "pl": {
        "pdf.form_to_label": "Do:",
        "pdf.form_date_label": "Data:",
        "pdf.form_i_declare_label": "Niniejszym oświadczam, że odstępuję od umowy zawartej z Państwem na świadczenie następującej usługi:",
    },
    "cs": {
        "pdf.form_to_label": "Komu:",
        "pdf.form_date_label": "Datum:",
        "pdf.form_i_declare_label": "Tímto prohlašuji, že odstupuji od své smlouvy uzavřené s vámi o poskytování následující služby:",
    },
    "da": {
        "pdf.form_to_label": "Til:",
        "pdf.form_date_label": "Dato:",
        "pdf.form_i_declare_label": "Jeg erklærer herved, at jeg ønsker at gøre fortrydelsesretten gældende i forbindelse med min kontrakt med jer om levering af følgende tjenesteydelse:",
    },
    "de": {
        "pdf.form_to_label": "An:",
        "pdf.form_date_label": "Datum:",
        "pdf.form_i_declare_label": "Hiermit widerrufe(n) ich/wir den von mir/uns abgeschlossenen Vertrag über die Erbringung der folgenden Dienstleistung:",
    },
    "el": {
        "pdf.form_to_label": "Προς:",
        "pdf.form_date_label": "Ημερομηνία:",
        "pdf.form_i_declare_label": "Με την παρούσα δηλώνω ότι υπαναχωρώ από τη σύμβασή μου που συνήφθη μαζί σας για την παροχή της ακόλουθης υπηρεσίας:",
    },
    "es": {
        "pdf.form_to_label": "A:",
        "pdf.form_date_label": "Fecha:",
        "pdf.form_i_declare_label": "Por la presente declaro que desisto de mi contrato celebrado con ustedes para la prestación del siguiente servicio:",
    },
    "et": {
        "pdf.form_to_label": "Saaja:",
        "pdf.form_date_label": "Kuupäev:",
        "pdf.form_i_declare_label": "Käesolevaga avaldan soovi taganeda teiega sõlmitud lepingust järgmise teenuse osutamiseks:",
    },
    "fi": {
        "pdf.form_to_label": "Vastaanottaja:",
        "pdf.form_date_label": "Päiväys:",
        "pdf.form_i_declare_label": "Ilmoitan täten, että haluan peruuttaa teidän kanssanne tekemäni sopimuksen seuraavan palvelun toimittamisesta:",
    },
    "fr": {
        "pdf.form_to_label": "À :",
        "pdf.form_date_label": "Date :",
        "pdf.form_i_declare_label": "Je déclare par la présente que je me rétracte de mon contrat conclu avec vous pour la prestation du service suivant :",
    },
    "ga": {
        "pdf.form_to_label": "Chun:",
        "pdf.form_date_label": "Dáta:",
        "pdf.form_i_declare_label": "Dearbhaím leis seo go dtarraingím siar ó mo chonradh a tugadh i gcrích leat maidir le soláthar na seirbhíse seo a leanas:",
    },
    "hr": {
        "pdf.form_to_label": "Za:",
        "pdf.form_date_label": "Datum:",
        "pdf.form_i_declare_label": "Ovime izjavljujem da raskidam svoj ugovor sklopljen s vama za pružanje sljedeće usluge:",
    },
    "hu": {
        "pdf.form_to_label": "Címzett:",
        "pdf.form_date_label": "Dátum:",
        "pdf.form_i_declare_label": "Alulírott kijelentem, hogy elállok az Önökkel kötött, a következő szolgáltatás nyújtására irányuló szerződéstől:",
    },
    "is": {
        "pdf.form_to_label": "Til:",
        "pdf.form_date_label": "Dagsetning:",
        "pdf.form_i_declare_label": "Ég lýsi því hér með yfir að ég hætti við samning minn sem gerður var við ykkur um afhendingu á eftirfarandi þjónustu:",
    },
    "it": {
        "pdf.form_to_label": "A:",
        "pdf.form_date_label": "Data:",
        "pdf.form_i_declare_label": "Con la presente dichiaro di recedere dal mio contratto concluso con voi per la fornitura del seguente servizio:",
    },
    "lb": {
        "pdf.form_to_label": "Un:",
        "pdf.form_date_label": "Datum:",
        "pdf.form_i_declare_label": "Heimat erklären ech, datt ech vu mengem Kontrakt zrécktrieden, deen ech mat Iech iwwer d'Liwwerung vun der folgender Servicer ofgeschloss hunn:",
    },
    "lt": {
        "pdf.form_to_label": "Kam:",
        "pdf.form_date_label": "Data:",
        "pdf.form_i_declare_label": "Šiuo pareiškiu, kad atsisakau su jumis sudarytos sutarties dėl šios paslaugos teikimo:",
    },
    "lv": {
        "pdf.form_to_label": "Kam:",
        "pdf.form_date_label": "Datums:",
        "pdf.form_i_declare_label": "Ar šo es paziņoju, ka es atkāpjos no līguma, ko esmu noslēdzis ar jums par šāda pakalpojuma sniegšanu:",
    },
    "mk": {
        "pdf.form_to_label": "До:",
        "pdf.form_date_label": "Датум:",
        "pdf.form_i_declare_label": "Со ова изјавувам дека се повлекувам од мојот договор склучен со вас за испорака на следнава услуга:",
    },
    "mt": {
        "pdf.form_to_label": "Lil:",
        "pdf.form_date_label": "Data:",
        "pdf.form_i_declare_label": "Jiena hawnhekk niddikjara li nirtira mill-kuntratt tieġi konkluż magħkom għall-provvista tas-servizz li ġej:",
    },
    "nl": {
        "pdf.form_to_label": "Aan:",
        "pdf.form_date_label": "Datum:",
        "pdf.form_i_declare_label": "Hierbij deel ik u mede dat ik onze overeenkomst betreffende de levering van de volgende dienst herroep:",
    },
    "no": {
        "pdf.form_to_label": "Til:",
        "pdf.form_date_label": "Dato:",
        "pdf.form_i_declare_label": "Jeg erklærer herved at jeg går fra min kontrakt inngått med dere om levering av følgende tjeneste:",
    },
    "pt": {
        "pdf.form_to_label": "Para:",
        "pdf.form_date_label": "Data:",
        "pdf.form_i_declare_label": "Pela presente declaro que resolvo o meu contrato celebrado convosco para a prestação do seguinte serviço:",
    },
    "pt-PT": {
        "pdf.form_to_label": "Para:",
        "pdf.form_date_label": "Data:",
        "pdf.form_i_declare_label": "Pela presente declaro que resolvo o meu contrato celebrado convosco para a prestação do seguinte serviço:",
    },
    "ro": {
        "pdf.form_to_label": "Către:",
        "pdf.form_date_label": "Data:",
        "pdf.form_i_declare_label": "Prin prezenta declar că mă retrag din contractul încheiat cu dumneavoastră pentru furnizarea următorului serviciu:",
    },
    "ru": {
        "pdf.form_to_label": "Кому:",
        "pdf.form_date_label": "Дата:",
        "pdf.form_i_declare_label": "Настоящим я заявляю, что отказываюсь от моего договора, заключенного с вами на оказание следующей услуги:",
    },
    "sk": {
        "pdf.form_to_label": "Komu:",
        "pdf.form_date_label": "Dátum:",
        "pdf.form_i_declare_label": "Týmto vyhlasujem, že odstupujem od svojej zmluvy uzavretej s vami o poskytovaní nasledujúcej služby:",
    },
    "sl": {
        "pdf.form_to_label": "Za:",
        "pdf.form_date_label": "Datum:",
        "pdf.form_i_declare_label": "Izjavljam, da odstopam od svoje pogodbe, sklenjene z vami za opravljanje naslednje storitve:",
    },
    "sq": {
        "pdf.form_to_label": "Për:",
        "pdf.form_date_label": "Data:",
        "pdf.form_i_declare_label": "Me anë të kësaj deklaroj se tërhiqem nga kontrata ime e lidhur me ju për ofrimin e shërbimit të mëposhtëm:",
    },
    "sr": {
        "pdf.form_to_label": "Za:",
        "pdf.form_date_label": "Datum:",
        "pdf.form_i_declare_label": "Ovim izjavljujem da odustajem od svog ugovora zaključenog sa vama za pružanje sledeće usluge:",
    },
    "sv": {
        "pdf.form_to_label": "Till:",
        "pdf.form_date_label": "Datum:",
        "pdf.form_i_declare_label": "Härmed meddelar jag att jag frånträder mitt avtal med er rörande följande tjänst:",
    },
    "tr": {
        "pdf.form_to_label": "Alıcı:",
        "pdf.form_date_label": "Tarih:",
        "pdf.form_i_declare_label": "Aşağıdaki hizmetin sunulmasına ilişkin olarak sizinle akdetmiş olduğum sözleşmemden caydığımı işbu belgeyle beyan ederim:",
    },
    "uk": {
        "pdf.form_to_label": "Кому:",
        "pdf.form_date_label": "Дата:",
        "pdf.form_i_declare_label": "Цим я заявляю, що відмовляюся від мого договору, укладеного з вами на надання наступної послуги:",
    },
}

if __name__ == "__main__":
    main()
