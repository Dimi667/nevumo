"""
seed_provider_terms_p3_titles1.py  —  Nevumo | namespace: provider_terms
Keys: art1_title, art2_title, art3_title, art4_title  (4 keys x 34 langs = 136 rows)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_provider_terms_p3_titles1
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://nevumo:nevumo@postgres:5432/nevumo_leads",
)

NAMESPACE = "provider_terms"

TRANSLATIONS: dict[str, dict[str, str]] = {
    "art1_title": {
        "bg":    "1. Общи разпоредби",
        "cs":    "1. Obecna ustanoveni",
        "da":    "1. Generelle bestemmelser",
        "de":    "1. Allgemeine Bestimmungen",
        "el":    "1. Genikes Diataxeis",
        "en":    "1. General Provisions",
        "es":    "1. Disposiciones generales",
        "et":    "1. Uldised satted",
        "fi":    "1. Yleiset maaraykset",
        "fr":    "1. Dispositions generales",
        "ga":    "1. Foralacha Ginearalta",
        "hr":    "1. Opce odredbe",
        "hu":    "1. Altalanos rendelkezesek",
        "is":    "1. Almennar reglur",
        "it":    "1. Disposizioni generali",
        "lb":    "1. Allgemeng Bestemmungen",
        "lt":    "1. Bendrosios nuostatos",
        "lv":    "1. Vispareji noteikumi",
        "mk":    "1. Opsti odredbi",
        "mt":    "1. Dispozizzjonijiet Generali",
        "nl":    "1. Algemene bepalingen",
        "no":    "1. Generelle bestemmelser",
        "pl":    "1. Postanowienia ogolne",
        "pt":    "1. Disposicoes gerais",
        "pt-PT": "1. Disposicoes gerais",
        "ro":    "1. Dispozitii generale",
        "ru":    "1. Obshchie polozheniya",
        "sk":    "1. Vseobecne ustanovenia",
        "sl":    "1. Splosne dolocbe",
        "sq":    "1. Dispozita te pergjithshme",
        "sr":    "1. Opste odredbe",
        "sv":    "1. Allmanna bestammelser",
        "tr":    "1. Genel Hukumler",
        "uk":    "1. Zahalni polozhennya",
    },
    "art2_title": {
        "bg":    "2. Определения",
        "cs":    "2. Definice",
        "da":    "2. Definitioner",
        "de":    "2. Begriffsbestimmungen",
        "el":    "2. Orismoi",
        "en":    "2. Definitions",
        "es":    "2. Definiciones",
        "et":    "2. Maaratlused",
        "fi":    "2. Maaritelmät",
        "fr":    "2. Definitions",
        "ga":    "2. Sainmhiniti",
        "hr":    "2. Definicije",
        "hu":    "2. Fogalommeghatarozasok",
        "is":    "2. Skilgreiningar",
        "it":    "2. Definizioni",
        "lb":    "2. Definitiounen",
        "lt":    "2. Apibrezimai",
        "lv":    "2. Definicijas",
        "mk":    "2. Definicii",
        "mt":    "2. Definizzjonijiet",
        "nl":    "2. Definities",
        "no":    "2. Definisjoner",
        "pl":    "2. Definicje",
        "pt":    "2. Definicoes",
        "pt-PT": "2. Definicoes",
        "ro":    "2. Definitii",
        "ru":    "2. Opredeleniya",
        "sk":    "2. Definicie",
        "sl":    "2. Opredelitve",
        "sq":    "2. Perkufizime",
        "sr":    "2. Definicije",
        "sv":    "2. Definitioner",
        "tr":    "2. Tanimlar",
        "uk":    "2. Vyznachennya",
    },
    "art3_title": {
        "bg":    "3. Регистрация и акаунт",
        "cs":    "3. Registrace a ucet",
        "da":    "3. Registrering og konto",
        "de":    "3. Registrierung und Konto",
        "el":    "3. Eggrafí kai Logariasmós",
        "en":    "3. Registration and Account",
        "es":    "3. Registro y cuenta",
        "et":    "3. Registreerimine ja konto",
        "fi":    "3. Rekisteroityminen ja tili",
        "fr":    "3. Inscription et compte",
        "ga":    "3. Clarú agus Cuntas",
        "hr":    "3. Registracija i racun",
        "hu":    "3. Regisztracio es fiok",
        "is":    "3. Skraning og reikningur",
        "it":    "3. Registrazione e account",
        "lb":    "3. Registrierung an Kont",
        "lt":    "3. Registracija ir paskyra",
        "lv":    "3. Registracija un konts",
        "mk":    "3. Registracija i smetka",
        "mt":    "3. Registrazzjoni u Kont",
        "nl":    "3. Registratie en account",
        "no":    "3. Registrering og konto",
        "pl":    "3. Rejestracja i konto",
        "pt":    "3. Registro e conta",
        "pt-PT": "3. Registo e conta",
        "ro":    "3. Inregistrare si cont",
        "ru":    "3. Registratsiya i uchetnaya zapis",
        "sk":    "3. Registracia a ucet",
        "sl":    "3. Registracija in racun",
        "sq":    "3. Regjistrimi dhe llogaria",
        "sr":    "3. Registracija i nalog",
        "sv":    "3. Registrering och konto",
        "tr":    "3. Kayit ve Hesap",
        "uk":    "3. Reyestratsiia ta oblikovyi zapis",
    },
    "art4_title": {
        "bg":    "4. Профил на Доставчика и Обяви за Услуги",
        "cs":    "4. Profil Poskytovatele a Nabídky Sluzeb",
        "da":    "4. Udbyderens profil og serviceopslag",
        "de":    "4. Dienstleisterprofil und Serviceangebote",
        "el":    "4. Profil Parohou kai Kathalogoi Ypirésion",
        "en":    "4. Provider Profile and Service Listings",
        "es":    "4. Perfil del proveedor y listados de servicios",
        "et":    "4. Teenusepakkuja profiil ja teenuste loetelu",
        "fi":    "4. Palveluntarjoajan profiili ja palveluluettelot",
        "fr":    "4. Profil du prestataire et annonces de services",
        "ga":    "4. Proifil an tSolathraio agus Liostaí Seirbhísí",
        "hr":    "4. Profil pruzatelja i ponude usluga",
        "hu":    "4. Szolgaltatoi profil es szolgaltataslistak",
        "is":    "4. Notandasnid veituadila og thjonustuskrar",
        "it":    "4. Profilo del fornitore e annunci di servizi",
        "lb":    "4. Profil vum Presser a Serviceangeboten",
        "lt":    "4. Paslaugu teikeojo profilis ir paslaugu sarasai",
        "lv":    "4. Pakalpojumu sniedzeja profils un pakalpojumu saraksti",
        "mk":    "4. Profil na davacot i oglasi za uslugi",
        "mt":    "4. Profil tal-Fornitur u Listati tas-Servizzi",
        "nl":    "4. Profiel van de dienstverlener en serviceaanbiedingen",
        "no":    "4. Leverandorprofil og tjenestelister",
        "pl":    "4. Profil Dostawcy i Oferty Uslug",
        "pt":    "4. Perfil do prestador e listagens de servicos",
        "pt-PT": "4. Perfil do prestador e listagens de servicos",
        "ro":    "4. Profilul furnizorului si listele de servicii",
        "ru":    "4. Profil postavshchika i ob'yavleniya ob uslugakh",
        "sk":    "4. Profil poskytovatel'a a zoznamy sluzieb",
        "sl":    "4. Profil ponudnika in oglasi storitev",
        "sq":    "4. Profili i ofruesit dhe listat e sherbimeve",
        "sr":    "4. Profil pruzaoca i oglasi usluga",
        "sv":    "4. Leverantorens profil och tjänstelistor",
        "tr":    "4. Saglayici Profili ve Hizmet Listelemeleri",
        "uk":    "4. Profil postachalnika ta perelik posluh",
    },
}


def seed() -> None:
    engine = create_engine(DATABASE_URL, echo=False)
    Session = sessionmaker(bind=engine)

    with Session() as session:
        count = 0
        for key, lang_values in TRANSLATIONS.items():
            db_key = f"{NAMESPACE}.{key}"
            for lang, value in lang_values.items():
                session.execute(
                    text(
                        "INSERT INTO translations (lang, key, value) "
                        "VALUES (:lang, :key, :value) "
                        "ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value"
                    ),
                    {"lang": lang, "key": db_key, "value": value},
                )
                count += 1
        session.commit()
        print(
            f"✅ seed_provider_terms_p3_titles1: {count} rows upserted "
            f"({NAMESPACE}: art1_title, art2_title, art3_title, art4_title x 34 langs)"
        )

    engine.dispose()


if __name__ == "__main__":
    seed()
