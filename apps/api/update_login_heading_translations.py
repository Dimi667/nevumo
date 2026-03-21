import os

import psycopg2
from psycopg2.extras import execute_batch

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/nevumo"
)

HEADING_TRANSLATIONS = {
    "bg": "Намери услуга или започни да предлагаш услуги!",
    "en": "Find a service or start offering services!",
    "tr": "Bir hizmet bul veya hizmet sunmaya başla!",
    "da": "Find en service eller begynd at tilbyde tjenester!",
    "no": "Finn en tjeneste eller begynn å tilby tjenester!",
    "sr": "Пронађи услугу или почни да нудиш услуге!",
    "mk": "Најди услуга или почни да нудиш услуги!",
    "de": "Finde eine Dienstleistung oder beginne, Dienstleistungen anzubieten!",
    "fr": "Trouvez un service ou commencez à proposer des services !",
    "es": "Encuentra un servicio o empieza a ofrecer servicios!",
    "it": "Trova un servizio o inizia a offrire servizi!",
    "pt": "Encontra um serviço ou começa a oferecer serviços!",
    "nl": "Vind een dienst of begin diensten aan te bieden!",
    "sv": "Hitta en tjänst eller börja erbjuda tjänster!",
    "fi": "Löydä palvelu tai ala tarjota palveluja!",
    "pl": "Znajdź usługę lub zacznij oferować usługi!",
    "cs": "Najdi službu nebo začni nabízet služby!",
    "sk": "Nájdi službu alebo začni ponúkať služby!",
    "hu": "Találj szolgáltatást vagy kezdj el kínálni szolgáltatásokat!",
    "ro": "Găsește un serviciu sau începe să oferi servicii!",
    "el": "Βρες μια υπηρεσία ή ξεκίνα να προσφέρεις υπηρεσίες!",
    "et": "Leia teenus või alusta teenuste pakkumist!",
    "lv": "Atrodi pakalpojumu vai sāc piedāvāt pakalpojumus!",
    "lt": "Raskite paslaugą arba pradėkite siūlyti paslaugas!",
    "sl": "Poišči storitev ali začni ponujati storitve!",
    "hr": "Pronađi uslugu ili počni nuditi usluge!",
    "sq": "Gjej një shërbim ose fillo të ofrosh shërbime!",
    "is": "Finndu þjónustu eða byrjaðu að bjóða þjónustu!",
    "ga": "Faigh seirbhís nó tosaigh ag tairiscint seirbhísí!",
    "mt": "Sib servizz jew ibda toffri servizzi!",
}

def main() -> None:
    conn = psycopg2.connect(DATABASE_URL)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT DISTINCT lang FROM translations ORDER BY lang;")
            langs = [row[0] for row in cursor.fetchall()]
            print("Detected languages:", ", ".join(langs))

            rows = []
            for lang, value in HEADING_TRANSLATIONS.items():
                if lang not in langs:
                    print(f"  • skipping {lang}: not present in translations table")
                    continue
                rows.append((lang, value))

            if not rows:
                print("No matching languages found; nothing to update.")
                return

            query = """
                INSERT INTO translations (lang, key, value)
                VALUES (%s, 'login:heading', %s)
                ON CONFLICT (lang, key)
                DO UPDATE SET value = EXCLUDED.value;
            """
            execute_batch(cursor, query, rows)
            conn.commit()
            print(f"Upserted {len(rows)} rows for `login:heading`.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
