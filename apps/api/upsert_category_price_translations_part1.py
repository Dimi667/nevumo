import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://localhost/nevumo_leads")

NAMESPACE = "category"

TRANSLATIONS = {
    "bg": {
        "price_meta_none": "Сравнете цени от местни изпълнители",
        "price_meta_single": "от {price} {currency}",
        "price_meta_range": "от {min} до {max} {currency}",
        "price_faq_none": "Цените варират в зависимост от обхвата и площта на работата.",
        "price_faq_single": "Услугата струва около {price} {currency}, в зависимост от обхвата на работата.",
        "price_faq_range": "Услугата струва от {min} до {max} {currency}, в зависимост от обхвата и площта на работата.",
        "price_text_none": "Цените варират в зависимост от обхвата и площта на работата.",
        "price_text_single": "Услугата струва около {price} {currency}, в зависимост от обхвата на работата.",
        "price_text_range": "Услугата струва от {min} до {max} {currency}, в зависимост от обхвата и площта на работата.",
    },
    "cs": {
        "price_meta_none": "Porovnejte ceny místních poskytovatelů",
        "price_meta_single": "od {price} {currency}",
        "price_meta_range": "od {min} do {max} {currency}",
        "price_faq_none": "Ceny se liší v závislosti na rozsahu a ploše práce.",
        "price_faq_single": "Služba stojí přibližně {price} {currency}, v závislosti na rozsahu prací.",
        "price_faq_range": "Služba stojí od {min} do {max} {currency}, v závislosti na rozsahu a ploše práce.",
        "price_text_none": "Ceny se liší v závislosti na rozsahu a ploše práce.",
        "price_text_single": "Služba stojí přibližně {price} {currency}, v závislosti na rozsahu prací.",
        "price_text_range": "Služba stojí od {min} do {max} {currency}, v závislosti na rozsahu a ploše práce.",
    },
    "da": {
        "price_meta_none": "Sammenlign priser fra lokale udbydere",
        "price_meta_single": "fra {price} {currency}",
        "price_meta_range": "fra {min} til {max} {currency}",
        "price_faq_none": "Priserne varierer afhængigt af arbejdets omfang og størrelse.",
        "price_faq_single": "Tjenesten koster ca. {price} {currency}, afhængigt af arbejdets omfang.",
        "price_faq_range": "Tjenesten koster fra {min} til {max} {currency}, afhængigt af arbejdets omfang og størrelse.",
        "price_text_none": "Priserne varierer afhængigt af arbejdets omfang og størrelse.",
        "price_text_single": "Tjenesten koster ca. {price} {currency}, afhængigt af arbejdets omfang.",
        "price_text_range": "Tjenesten koster fra {min} til {max} {currency}, afhængigt af arbejdets omfang og størrelse.",
    },
    "de": {
        "price_meta_none": "Preise lokaler Anbieter vergleichen",
        "price_meta_single": "ab {price} {currency}",
        "price_meta_range": "von {min} bis {max} {currency}",
        "price_faq_none": "Die Preise variieren je nach Umfang und Fläche der Arbeit.",
        "price_faq_single": "Die Dienstleistung kostet ca. {price} {currency}, je nach Umfang der Arbeiten.",
        "price_faq_range": "Die Dienstleistung kostet von {min} bis {max} {currency}, je nach Umfang und Fläche.",
        "price_text_none": "Die Preise variieren je nach Umfang und Fläche der Arbeit.",
        "price_text_single": "Die Dienstleistung kostet ca. {price} {currency}, je nach Umfang der Arbeiten.",
        "price_text_range": "Die Dienstleistung kostet von {min} bis {max} {currency}, je nach Umfang und Fläche.",
    },
    "el": {
        "price_meta_none": "Συγκρίνετε τιμές από τοπικούς παρόχους",
        "price_meta_single": "από {price} {currency}",
        "price_meta_range": "από {min} έως {max} {currency}",
        "price_faq_none": "Οι τιμές ποικίλλουν ανάλογα με το εύρος και την επιφάνεια της εργασίας.",
        "price_faq_single": "Η υπηρεσία κοστίζει περίπου {price} {currency}, ανάλογα με το εύρος των εργασιών.",
        "price_faq_range": "Η υπηρεσία κοστίζει από {min} έως {max} {currency}, ανάλογα με το εύρος και την επιφάνεια.",
        "price_text_none": "Οι τιμές ποικίλλουν ανάλογα με το εύρος και την επιφάνεια της εργασίας.",
        "price_text_single": "Η υπηρεσία κοστίζει περίπου {price} {currency}, ανάλογα με το εύρος των εργασιών.",
        "price_text_range": "Η υπηρεσία κοστίζει από {min} έως {max} {currency}, ανάλογα με το εύρος και την επιφάνεια.",
    },
    "en": {
        "price_meta_none": "Compare prices from local providers",
        "price_meta_single": "from {price} {currency}",
        "price_meta_range": "from {min} to {max} {currency}",
        "price_faq_none": "Prices vary depending on the scope and size of the work.",
        "price_faq_single": "The service costs around {price} {currency}, depending on the scope of work.",
        "price_faq_range": "The service costs from {min} to {max} {currency}, depending on the scope and size of the work.",
        "price_text_none": "Prices vary depending on the scope and size of the work.",
        "price_text_single": "The service costs around {price} {currency}, depending on the scope of work.",
        "price_text_range": "The service costs from {min} to {max} {currency}, depending on the scope and size of the work.",
    },
    "es": {
        "price_meta_none": "Compare precios de proveedores locales",
        "price_meta_single": "desde {price} {currency}",
        "price_meta_range": "desde {min} hasta {max} {currency}",
        "price_faq_none": "Los precios varían según el alcance y el área del trabajo.",
        "price_faq_single": "El servicio cuesta alrededor de {price} {currency}, según el alcance del trabajo.",
        "price_faq_range": "El servicio cuesta desde {min} hasta {max} {currency}, según el alcance y el área.",
        "price_text_none": "Los precios varían según el alcance y el área del trabajo.",
        "price_text_single": "El servicio cuesta alrededor de {price} {currency}, según el alcance del trabajo.",
        "price_text_range": "El servicio cuesta desde {min} hasta {max} {currency}, según el alcance y el área.",
    },
    "et": {
        "price_meta_none": "Võrrelge kohalike teenusepakkujate hindasid",
        "price_meta_single": "alates {price} {currency}",
        "price_meta_range": "alates {min} kuni {max} {currency}",
        "price_faq_none": "Hinnad varieeruvad sõltuvalt töö mahust ja pindalast.",
        "price_faq_single": "Teenus maksab umbes {price} {currency}, sõltuvalt töö mahust.",
        "price_faq_range": "Teenus maksab {min} kuni {max} {currency}, sõltuvalt töö mahust ja pindalast.",
        "price_text_none": "Hinnad varieeruvad sõltuvalt töö mahust ja pindalast.",
        "price_text_single": "Teenus maksab umbes {price} {currency}, sõltuvalt töö mahust.",
        "price_text_range": "Teenus maksab {min} kuni {max} {currency}, sõltuvalt töö mahust ja pindalast.",
    },
    "fi": {
        "price_meta_none": "Vertaa paikallisten palveluntarjoajien hintoja",
        "price_meta_single": "alkaen {price} {currency}",
        "price_meta_range": "{min}–{max} {currency}",
        "price_faq_none": "Hinnat vaihtelevat työn laajuuden ja pinta-alan mukaan.",
        "price_faq_single": "Palvelu maksaa noin {price} {currency}, työn laajuudesta riippuen.",
        "price_faq_range": "Palvelu maksaa {min}–{max} {currency}, työn laajuudesta ja pinta-alasta riippuen.",
        "price_text_none": "Hinnat vaihtelevat työn laajuuden ja pinta-alan mukaan.",
        "price_text_single": "Palvelu maksaa noin {price} {currency}, työn laajuudesta riippuen.",
        "price_text_range": "Palvelu maksaa {min}–{max} {currency}, työn laajuudesta ja pinta-alasta riippuen.",
    },
    "fr": {
        "price_meta_none": "Comparez les prix des prestataires locaux",
        "price_meta_single": "à partir de {price} {currency}",
        "price_meta_range": "de {min} à {max} {currency}",
        "price_faq_none": "Les prix varient selon l'étendue et la superficie du travail.",
        "price_faq_single": "Le service coûte environ {price} {currency}, selon l'étendue des travaux.",
        "price_faq_range": "Le service coûte de {min} à {max} {currency}, selon l'étendue et la superficie.",
        "price_text_none": "Les prix varient selon l'étendue et la superficie du travail.",
        "price_text_single": "Le service coûte environ {price} {currency}, selon l'étendue des travaux.",
        "price_text_range": "Le service coûte de {min} à {max} {currency}, selon l'étendue et la superficie.",
    },
    "ga": {
        "price_meta_none": "Cuir praghsanna soláthraithe áitiúla i gcomparáid",
        "price_meta_single": "ó {price} {currency}",
        "price_meta_range": "ó {min} go {max} {currency}",
        "price_faq_none": "Athraíonn praghsanna de réir scóipe agus achar an oibre.",
        "price_faq_single": "Cosnaíonn an tseirbhís thart ar {price} {currency}, de réir scóipe an oibre.",
        "price_faq_range": "Cosnaíonn an tseirbhís ó {min} go {max} {currency}, de réir scóipe agus achar.",
        "price_text_none": "Athraíonn praghsanna de réir scóipe agus achar an oibre.",
        "price_text_single": "Cosnaíonn an tseirbhís thart ar {price} {currency}, de réir scóipe an oibre.",
        "price_text_range": "Cosnaíonn an tseirbhís ó {min} go {max} {currency}, de réir scóipe agus achar.",
    },
    "hr": {
        "price_meta_none": "Usporedite cijene lokalnih pružatelja usluga",
        "price_meta_single": "od {price} {currency}",
        "price_meta_range": "od {min} do {max} {currency}",
        "price_faq_none": "Cijene variraju ovisno o opsegu i površini rada.",
        "price_faq_single": "Usluga košta oko {price} {currency}, ovisno o opsegu radova.",
        "price_faq_range": "Usluga košta od {min} do {max} {currency}, ovisno o opsegu i površini.",
        "price_text_none": "Cijene variraju ovisno o opsegu i površini rada.",
        "price_text_single": "Usluga košta oko {price} {currency}, ovisno o opsegu radova.",
        "price_text_range": "Usluga košta od {min} do {max} {currency}, ovisno o opsegu i površini.",
    },
    "hu": {
        "price_meta_none": "Hasonlítsa össze a helyi szolgáltatók árait",
        "price_meta_single": "{price} {currency}-tól",
        "price_meta_range": "{min}–{max} {currency}",
        "price_faq_none": "Az árak a munka terjedelmétől és területétől függően változnak.",
        "price_faq_single": "A szolgáltatás kb. {price} {currency}-ba kerül, a munka terjedelmétől függően.",
        "price_faq_range": "A szolgáltatás {min}–{max} {currency}-ba kerül, a terjedelem és terület függvényében.",
        "price_text_none": "Az árak a munka terjedelmétől és területétől függően változnak.",
        "price_text_single": "A szolgáltatás kb. {price} {currency}-ba kerül, a munka terjedelmétől függően.",
        "price_text_range": "A szolgáltatás {min}–{max} {currency}-ba kerül, a terjedelem és terület függvényében.",
    },
    "is": {
        "price_meta_none": "Berðu saman verð frá staðbundnum þjónustuaðilum",
        "price_meta_single": "frá {price} {currency}",
        "price_meta_range": "frá {min} til {max} {currency}",
        "price_faq_none": "Verð er breytilegt eftir umfangi og flatarmáli verksins.",
        "price_faq_single": "Þjónustan kostar um {price} {currency}, eftir umfangi verksins.",
        "price_faq_range": "Þjónustan kostar frá {min} til {max} {currency}, eftir umfangi og flatarmáli.",
        "price_text_none": "Verð er breytilegt eftir umfangi og flatarmáli verksins.",
        "price_text_single": "Þjónustan kostar um {price} {currency}, eftir umfangi verksins.",
        "price_text_range": "Þjónustan kostar frá {min} til {max} {currency}, eftir umfangi og flatarmáli.",
    },
    "it": {
        "price_meta_none": "Confronta i prezzi dei fornitori locali",
        "price_meta_single": "da {price} {currency}",
        "price_meta_range": "da {min} a {max} {currency}",
        "price_faq_none": "I prezzi variano in base all'entità e alla superficie del lavoro.",
        "price_faq_single": "Il servizio costa circa {price} {currency}, in base all'entità dei lavori.",
        "price_faq_range": "Il servizio costa da {min} a {max} {currency}, in base all'entità e alla superficie.",
        "price_text_none": "I prezzi variano in base all'entità e alla superficie del lavoro.",
        "price_text_single": "Il servizio costa circa {price} {currency}, in base all'entità dei lavori.",
        "price_text_range": "Il servizio costa da {min} a {max} {currency}, in base all'entità e alla superficie.",
    },
    "lb": {
        "price_meta_none": "Verglitt Präisser vu lokale Prestatairen",
        "price_meta_single": "vun {price} {currency}",
        "price_meta_range": "vun {min} bis {max} {currency}",
        "price_faq_none": "D'Präisser variéieren je no Ëmfang an Fläch vun der Aarbecht.",
        "price_faq_single": "De Service kascht ongeféier {price} {currency}, je no Ëmfang vun den Aarbechten.",
        "price_faq_range": "De Service kascht vun {min} bis {max} {currency}, je no Ëmfang an Fläch.",
        "price_text_none": "D'Präisser variéieren je no Ëmfang an Fläch vun der Aarbecht.",
        "price_text_single": "De Service kascht ongeféier {price} {currency}, je no Ëmfang vun den Aarbechten.",
        "price_text_range": "De Service kascht vun {min} bis {max} {currency}, je no Ëmfang an Fläch.",
    },
    "lt": {
        "price_meta_none": "Palyginkite vietinių paslaugų teikėjų kainas",
        "price_meta_single": "nuo {price} {currency}",
        "price_meta_range": "nuo {min} iki {max} {currency}",
        "price_faq_none": "Kainos skiriasi priklausomai nuo darbo apimties ir ploto.",
        "price_faq_single": "Paslauga kainuoja apie {price} {currency}, priklausomai nuo darbo apimties.",
        "price_faq_range": "Paslauga kainuoja nuo {min} iki {max} {currency}, priklausomai nuo apimties ir ploto.",
        "price_text_none": "Kainos skiriasi priklausomai nuo darbo apimties ir ploto.",
        "price_text_single": "Paslauga kainuoja apie {price} {currency}, priklausomai nuo darbo apimties.",
        "price_text_range": "Paslauga kainuoja nuo {min} iki {max} {currency}, priklausomai nuo apimties ir ploto.",
    },
}


def run():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    count = 0
    for lang, keys in TRANSLATIONS.items():
        for key, value in keys.items():
            db_key = f"{NAMESPACE}.{key}"
            cur.execute(
                """
                INSERT INTO translations (lang, key, value)
                VALUES (%s, %s, %s)
                ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
                """,
                (lang, db_key, value),
            )
            count += 1
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Part 1 done: {count} rows upserted ({len(TRANSLATIONS)} languages)")


if __name__ == "__main__":
    run()
