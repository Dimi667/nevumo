import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Override database URL to use port 5433
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://nevumo:nevumo@localhost:5433/nevumo_leads",
)

engine = create_engine(
    DATABASE_URL,
    connect_args={"options": "-c client_encoding=utf8"},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def main():
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()


def run_seed(db):
    insert_translations(db, FAQ_TRANSLATIONS)
    verify(db)


def insert_translations(db, data: list[dict]) -> None:
    count = 0
    for item in data:
        lang = item["lang"]
        translations = item["translations"]
        for key, value in translations.items():
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
    print(f"Inserted/updated {count} FAQ translation rows")


def verify(db) -> None:
    result = db.execute(text("""
        SELECT lang, COUNT(*) as keys
        FROM translations
        WHERE key LIKE 'faq_cleaning%'
        GROUP BY lang
        ORDER BY lang
    """))
    rows = result.fetchall()
    print("\nFAQ Translation Verification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} keys")


FAQ_TRANSLATIONS = [
    {
        "lang": "lv",
        "translations": {
            "faq_cleaning_q1": "{category_name} pilsētā {city} — kas jāzina?",
            "faq_cleaning_a1": "Profesionāli {category_name} speciālisti pilsētā {city} piedāvā visaptverošus pakalpojumus mājām, dzīvokļiem un birojiem. Nevumo platformā atradīsiet pārbaudītus profesionāļus visā {city}.",
            "faq_cleaning_q2": "Kā izvēlēties {category_name} speciālistu?",
            "faq_cleaning_a2": "Izvēloties {category_name} speciālistu pilsētā {city}, pievērsiet uzmanību atsauksmēm, pakalpojumu klāstam un eksperta pieredzei.",
            "faq_cleaning_q3": "Cik maksā {category_name} pilsētā {city}?",
            "faq_cleaning_a3": "{category_name} cenas pilsētā {city} nosaka darba apjoms, un tās ir no {min_price} līdz {max_price} {currency}."
        }
    },
    {
        "lang": "mk",
        "translations": {
            "faq_cleaning_q1": "{category_name} во {city} — што треба да знаете?",
            "faq_cleaning_a1": "Професионални специјалисти за {category_name} во {city} нудат сеопфатни услуги за куќи, станови и канцеларии. На Nevumo ќе најдете проверени професионалци достапни низ цела {city}.",
            "faq_cleaning_q2": "Како да изберете специјалист за {category_name}?",
            "faq_cleaning_a2": "При избор на специјалист за {category_name} во {city}, обрнете внимание на препораките, опсегот на услуги и искуството на експертот.",
            "faq_cleaning_q3": "Колку чини {category_name} во {city}?",
            "faq_cleaning_a3": "Цените за {category_name} во {city} се одредуваат според обемот на работа и се движат од {min_price} до {max_price} {currency}."
        }
    },
    {
        "lang": "mt",
        "translations": {
            "faq_cleaning_q1": "{category_name} f'{city} — x'inhu tajjeb li tkun taf?",
            "faq_cleaning_a1": "Speċjalisti professjonali tal-{category_name} f'{city} joffru servizzi komprensivi għal djar, appartamenti u uffiċċji. Fuq Nevumo ssib professjonisti vverifikati disponibbli madwar {city}.",
            "faq_cleaning_q2": "Kif tagħżel speċjalista tal-{category_name}?",
            "faq_cleaning_a2": "Meta tagħżel speċjalista tal-{category_name} f'{city}, oqgħod attent għar-reviżjonijiet tal-klijenti, l-ambitu tas-servizzi u l-esperjenza tal-espert.",
            "faq_cleaning_q3": "Kemm jiswa l-{category_name} f'{city}?",
            "faq_cleaning_a3": "Il-prezzijiet għal {category_name} f'{city} huma determinati mill-ambitu tax-xogħol u jvarjaw minn {min_price} sa {max_price} {currency}."
        }
    },
    {
        "lang": "no",
        "translations": {
            "faq_cleaning_q1": "{category_name} i {city} — hva er verdt å vite?",
            "faq_cleaning_a1": "Profesjonelle {category_name}-spesialister i {city} tilbyr omfattende tjenester for hjem, leiligheter og kontorer. På Nevumo finner du verifiserte fagfolk tilgjengelig i hele {city}.",
            "faq_cleaning_q2": "Hvordan velge en {category_name}-spesialist?",
            "faq_cleaning_a2": "Når du velger en {category_name}-spesialist i {city}, vær oppmerksom på kundeanmeldelser, omfanget av tjenester og ekspertens erfaring.",
            "faq_cleaning_q3": "Hva koster {category_name} i {city}?",
            "faq_cleaning_a3": "Prisene for {category_name} i {city} bestemmes av arbeidets omfang og ligger mellom {min_price} og {max_price} {currency}."
        }
    },
    {
        "lang": "pt",
        "translations": {
            "faq_cleaning_q1": "{category_name} em {city} — o que é importante saber?",
            "faq_cleaning_a1": "Especialistas profissionais de {category_name} em {city} oferecem serviços abrangentes para casas, apartamentos e escritórios. No Nevumo você encontrará profissionais verificados disponíveis em toda a {city}.",
            "faq_cleaning_q2": "Como escolher um especialista em {category_name}?",
            "faq_cleaning_a2": "Ao escolher um especialista em {category_name} em {city}, preste atenção às avaliações dos clientes, ao escopo dos serviços e à experiência do profissional.",
            "faq_cleaning_q3": "Quanto custa o {category_name} em {city}?",
            "faq_cleaning_a3": "Os preços para {category_name} em {city} são determinados pelo volume de trabalho e variam de {min_price} a {max_price} {currency}."
        }
    },
    {
        "lang": "pt-PT",
        "translations": {
            "faq_cleaning_q1": "{category_name} em {city} — o que é importante saber?",
            "faq_cleaning_a1": "Especialistas profissionais de {category_name} em {city} oferecem serviços abrangentes para casas, apartamentos e escritórios. No Nevumo encontrará profissionais verificados disponíveis em toda a {city}.",
            "faq_cleaning_q2": "Como escolher um especialista em {category_name}?",
            "faq_cleaning_a2": "Ao escolher um especialista em {category_name} em {city}, preste atenção às avaliações dos clientes, ao âmbito dos serviços e à experiência do profissional.",
            "faq_cleaning_q3": "Quanto custa o {category_name} em {city}?",
            "faq_cleaning_a3": "Os preços para {category_name} em {city} são determinados pelo volume de trabalho e variam de {min_price} a {max_price} {currency}."
        }
    },
    {
        "lang": "sk",
        "translations": {
            "faq_cleaning_q1": "{category_name} v {city} — čo je dobré vedieť?",
            "faq_cleaning_a1": "Profesionálni špecialisti na {category_name} v {city} ponúkajú komplexné služby pre domy, byty a kancelárie. Na Nevumo nájdete overených profesionálov dostupných v celom {city}.",
            "faq_cleaning_q2": "Ako si vybrať špecialistu na {category_name}?",
            "faq_cleaning_a2": "Pri výbere špecialistu na {category_name} v {city} venujte pozornosť recenziám klientov, rozsahu služieb a skúsenostiam odborníka.",
            "faq_cleaning_q3": "Koľko stojí {category_name} v {city}?",
            "faq_cleaning_a3": "Ceny za {category_name} v {city} sú určené rozsahom prác a pohybujú sa od {min_price} do {max_price} {currency}."
        }
    },
    {
        "lang": "sl",
        "translations": {
            "faq_cleaning_q1": "{category_name} v {city} — kaj je dobro vedeti?",
            "faq_cleaning_a1": "Profesionalni strokovnjaki za {category_name} v {city} ponujajo celovite storitve za hiše, stanovanja in pisarne. Na Nevumo boste našli preverjene strokovnjake, ki so na voljo po vsem {city}.",
            "faq_cleaning_q2": "Kako izbrati strokovnjaka za {category_name}?",
            "faq_cleaning_a2": "Pri izbiri strokovnjaka za {category_name} v {city} bodite pozorni na ocene strank, obseg storitev in izkušnje strokovnjaka.",
            "faq_cleaning_q3": "Koliko stane {category_name} v {city}?",
            "faq_cleaning_a3": "Cene za {category_name} v {city} so določene z obsegom dela in se gibljejo od {min_price} do {max_price} {currency}."
        }
    },
    {
        "lang": "sq",
        "translations": {
            "faq_cleaning_q1": "{category_name} në {city} — çfarë duhet të dini?",
            "faq_cleaning_a1": "Specialistët profesionistë të {category_name} në {city} ofrojnë shërbime gjithëpërfshirëse për shtëpi, apartamente dhe zyra. Në Nevumo do të gjeni profesionistë të verifikuar në të gjithë {city}.",
            "faq_cleaning_q2": "Si të zgjidhni një specialist {category_name}?",
            "faq_cleaning_a2": "Kur zgjidhni një specialist {category_name} në {city}, kushtojini vëmendje rishikimeve të klientëve, fushëveprimit të shërbimeve dhe përvojës së ekspertit.",
            "faq_cleaning_q3": "Sa kushton {category_name} në {city}?",
            "faq_cleaning_a3": "Çmimet për {category_name} në {city} përcaktohen nga vëllimi i punës dhe lëvizin nga {min_price} deri në {max_price} {currency}."
        }
    },
    {
        "lang": "sr",
        "translations": {
            "faq_cleaning_q1": "{category_name} u {city} — šta je važno znati?",
            "faq_cleaning_a1": "Profesionalni stručnjaci za {category_name} u {city} nude sveobuhvatne usluge za kuće, stanove i kancelarije. Na Nevumo platformi ćete pronaći proverene stručnjake dostupne u celom {city}.",
            "faq_cleaning_q2": "Kako odabrati stručnjaka za {category_name}?",
            "faq_cleaning_a2": "Pri odabiru stručnjaka za {category_name} u {city}, obratite pažnju na recenzije klijenata, obim usluga i iskustvo stručnjaka.",
            "faq_cleaning_q3": "Koliko košta {category_name} u {city}?",
            "faq_cleaning_a3": "Cene za {category_name} u {city} određene su obimom posla i kreću se od {min_price} do {max_price} {currency}."
        }
    },
    {
        "lang": "sv",
        "translations": {
            "faq_cleaning_q1": "{category_name} i {city} — vad är bra att veta?",
            "faq_cleaning_a1": "Professionella {category_name}-specialister i {city} erbjuder heltäckande tjänster för hem, lägenheter och kontor. På Nevumo hittar du verifierade yrkesmän tillgängliga i hela {city}.",
            "faq_cleaning_q2": "Hur väljer man en {category_name}-specialist?",
            "faq_cleaning_a2": "När du väljer en {category_name}-specialist i {city}, var uppmärksam på kundrecensioner, tjänsternas omfattning och expertens erfarenhet.",
            "faq_cleaning_q3": "Vad kostar {category_name} i {city}?",
            "faq_cleaning_a3": "Priserna för {category_name} i {city} fastställs av arbetets omfattning och varierar från {min_price} do {max_price} {currency}."
        }
    }
]


if __name__ == "__main__":
    main()
