"""
seed_provider_terms_p2_ui.py  —  Nevumo | namespace: provider_terms
Keys: pl_notice, back_to_home, operator_info, contact_legal  (4 keys × 34 langs = 136 rows)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_provider_terms_p2_ui
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
    "pl_notice": {
        "bg":    "Ако сте доставчик на услуги, установен в Полша, правно обвързващата версия на настоящите Условия е полската версия (Regulamin dla Dostawcow Uslug).",
        "cs":    "Pokud jste poskytovatel sluzeb se sidlem v Polsku, pravne zavaznou verzi techto podminek je polska verze (Regulamin dla Dostawcow Uslug).",
        "da":    "Hvis du er en tjenesteudbyder med hjemsted i Polen, er den polske version af disse vilkaar (Regulamin dla Dostawcow Uslug) den juridisk bindende version.",
        "de":    "Wenn Sie ein Dienstleister mit Sitz in Polen sind, ist die polnische Version dieser Bedingungen (Regulamin dla Dostawcow Uslug) die rechtlich verbindliche Version.",
        "el":    "Eán eísai párochos ypireción egkatestimenos stin Polónia, i nomikó desmeytikí écdosi ton parónton Óron eínai i polonikí écdosi (Regulamin dla Dostawcow Uslug).",
        "en":    "If you are a service provider based in Poland, the Polish version of these Terms (Regulamin dla Dostawcow Uslug) is the legally binding version.",
        "es":    "Si es un proveedor de servicios establecido en Polonia, la version polaca de estos Terminos (Regulamin dla Dostawcow Uslug) es la version legalmente vinculante.",
        "et":    "Kui olete Poolas asuv teenusepakkuja, on nende tingimuste poola keelne versioon (Regulamin dla Dostawcow Uslug) oiguslikult siduv.",
        "fi":    "Jos olet Puolassa toimiva palveluntarjoaja, naiden ehtojen puolankielinen versio (Regulamin dla Dostawcow Uslug) on oikeudellisesti sitova.",
        "fr":    "Si vous etes un prestataire de services etabli en Pologne, la version polonaise des presentes Conditions (Regulamin dla Dostawcow Uslug) est la version juridiquement contraignante.",
        "ga":    "Ma ta tu i do sholathroir seirbhise atа bunaithe sa Pholainn, is i leagan Polainnis na dTearmai seo (Regulamin dla Dostawcow Uslug) an leagan ata ceangailteach o thaobh dli.",
        "hr":    "Ako ste pruzatelj usluga sa sjedistvom u Poljskoj, pravno obvezujuca verzija ovih Uvjeta je poljska verzija (Regulamin dla Dostawcow Uslug).",
        "hu":    "Ha On Lengyelorszagban szekhellyel rendelkezo szolgaltato, jelen Feltetelek lengyel nyelvu valtozata (Regulamin dla Dostawcow Uslug) a jogilag kotelezo ervenyu valtozat.",
        "is":    "Ef thu ert thjonustuadili med stadfestu i Pollandi er polska utgafan af thessum skilmalum (Regulamin dla Dostawcow Uslug) logbindandi utgafan.",
        "it":    "Se sei un fornitore di servizi con sede in Polonia, la versione polacca di questi Termini (Regulamin dla Dostawcow Uslug) e la versione legalmente vincolante.",
        "lb":    "Wann Dir e Servicepresser mat Setz a Polen sidd, ass dei polnesch Versioun vun dese Konditiounen (Regulamin dla Dostawcow Uslug) dei rechtlech bindend Versioun.",
        "lt":    "Jei esate Lenkijoje isisteiges paslaugu teikejas, teisiskai privaloma siu salygu versija yra lenkiska versija (Regulamin dla Dostawcow Uslug).",
        "lv":    "Ja esat Polija registrets pakalpojumu sniedzejs, so noteikumu polu valodas versija (Regulamin dla Dostawcow Uslug) ir juridiski saistosa versija.",
        "mk":    "Ako ste davac na uslugi so sediste vo Polska, pravno obvrzbuvackata verzija na ovie Uslovi e polskata verzija (Regulamin dla Dostawcow Uslug).",
        "mt":    "Jekk inti fornitur ta servizz ibbazat fil-Polonja, il-verzjoni Pollakka ta dawn it-Termini (Regulamin dla Dostawcow Uslug) hija l-verzjoni legalment vinkolanti.",
        "nl":    "Als u een dienstverlener bent gevestigd in Polen, is de Poolse versie van deze Voorwaarden (Regulamin dla Dostawcow Uslug) de juridisch bindende versie.",
        "no":    "Hvis du er en tjenesteleverandor med sete i Polen, er den polske versjonen av disse vilkarene (Regulamin dla Dostawcow Uslug) den juridisk bindende versjonen.",
        "pl":    "Jezeli jestes Dostawca uslug z siedziba w Polsce, wiazaca prawnie wersja niniejszych warunkow jest wersja polska (Regulamin dla Dostawcow Uslug).",
        "pt":    "Se voce e um prestador de servicos sediado na Polonia, a versao polonesa destes Termos (Regulamin dla Dostawcow Uslug) e a versao juridicamente vinculante.",
        "pt-PT": "Se e um prestador de servicos com sede na Polonia, a versao polaca destes Termos (Regulamin dla Dostawcow Uslug) e a versao juridicamente vinculativa.",
        "ro":    "Daca esti un furnizor de servicii cu sediul in Polonia, versiunea polona a acestor Termeni (Regulamin dla Dostawcow Uslug) este versiunea obligatorie din punct de vedere juridic.",
        "ru":    "Esli vy yavlyaetes' postavshchikom uslug, zaregistrirovannym v Pol'she, yuridicheski obyazatel'noy versiey nastoyashchikh Usloviy yavlyaetsya pol'skaya versiya (Regulamin dla Dostawcow Uslug).",
        "sk":    "Ak ste poskytovatel sluzieb so sidlom v Polsku, pravne zavaznou verziou tychto podmienok je polska verzia (Regulamin dla Dostawcow Uslug).",
        "sl":    "Ce ste ponudnik storitev s sedecem na Poljskem, je pravno zavezujoca razlicica teh Pogojev poljska razlicica (Regulamin dla Dostawcow Uslug).",
        "sq":    "Nese jeni ofrues sherbimesh i bazuar ne Poloni, versioni polonez i ketyre Termave (Regulamin dla Dostawcow Uslug) eshte versioni juridikisht detyrues.",
        "sr":    "Ako ste pruzalac usluga sa sedistem u Poljskoj, pravno obavezujuca verzija ovih Uslova je poljska verzija (Regulamin dla Dostawcow Uslug).",
        "sv":    "Om du ar en tjanstelevarantor baserad i Polen ar den polska versionen av dessa Villkor (Regulamin dla Dostawcow Uslug) den juridiskt bindande versionen.",
        "tr":    "Polonya'da yerlesik bir hizmet saglayicisiyysaniz, bu Kosullarin Lehce versiyonu (Regulamin dla Dostawcow Uslug) yasal olarak baglazyici versiyondur.",
        "uk":    "Yakshcho vy ye postachalnikom posluh, zareyestrovanym u Pol'shchi, yurydychno obov'yazkovoyu versiyeyu tsykh Umov ye pol's'ka versiya (Regulamin dla Dostawcow Uslug).",
    },
    "back_to_home": {
        "bg":    "Начална страница",
        "cs":    "Domovska stranka",
        "da":    "Startside",
        "de":    "Startseite",
        "el":    "Arxiki selida",
        "en":    "Back to Home",
        "es":    "Volver al inicio",
        "et":    "Avaleht",
        "fi":    "Etusivu",
        "fr":    "Retour a l'accueil",
        "ga":    "Ar ais go dti an Baile",
        "hr":    "Natrag na pocetnu",
        "hu":    "Vissza a fooldalra",
        "is":    "Til baka a forsidu",
        "it":    "Torna alla home",
        "lb":    "Zreck zur Haaptsait",
        "lt":    "Grizti i pradzią",
        "lv":    "Atpakal uz sakumu",
        "mk":    "Nazad na pocetna",
        "mt":    "Lura ghall-pagna ewlenija",
        "nl":    "Terug naar home",
        "no":    "Tilbake til forsiden",
        "pl":    "Powrot do strony glownej",
        "pt":    "Voltar ao inicio",
        "pt-PT": "Voltar ao inicio",
        "ro":    "Inapoi la pagina principala",
        "ru":    "Na glavnuyu",
        "sk":    "Spat na domovsku stranku",
        "sl":    "Nazaj na domaco stran",
        "sq":    "Kthehu ne kryefaqe",
        "sr":    "Nazad na pocetnu",
        "sv":    "Tillbaka till startsidan",
        "tr":    "Ana sayfaya don",
        "uk":    "Na holovnu",
    },
    "operator_info": {
        "bg":    "FILIPHS TSENTAR BULGARIA OOD | EIK 175369610 | legal@nevumo.com",
        "cs":    "FILIPHS TSENTAR BULGARIA OOD | EIK 175369610 | legal@nevumo.com",
        "da":    "FILIPHS TSENTAR BULGARIA OOD | EIK 175369610 | legal@nevumo.com",
        "de":    "FILIPHS TSENTAR BULGARIA OOD | EIK 175369610 | legal@nevumo.com",
        "el":    "FILIPHS TSENTAR BULGARIA OOD | EIK 175369610 | legal@nevumo.com",
        "en":    "FILIPHS TSENTAR BULGARIA OOD | EIC 175369610 | legal@nevumo.com",
        "es":    "FILIPHS TSENTAR BULGARIA OOD | EIC 175369610 | legal@nevumo.com",
        "et":    "FILIPHS TSENTAR BULGARIA OOD | EIK 175369610 | legal@nevumo.com",
        "fi":    "FILIPHS TSENTAR BULGARIA OOD | EIK 175369610 | legal@nevumo.com",
        "fr":    "FILIPHS TSENTAR BULGARIA OOD | EIC 175369610 | legal@nevumo.com",
        "ga":    "FILIPHS TSENTAR BULGARIA OOD | EIC 175369610 | legal@nevumo.com",
        "hr":    "FILIPHS TSENTAR BULGARIA OOD | EIK 175369610 | legal@nevumo.com",
        "hu":    "FILIPHS TSENTAR BULGARIA OOD | EIK 175369610 | legal@nevumo.com",
        "is":    "FILIPHS TSENTAR BULGARIA OOD | EIK 175369610 | legal@nevumo.com",
        "it":    "FILIPHS TSENTAR BULGARIA OOD | EIC 175369610 | legal@nevumo.com",
        "lb":    "FILIPHS TSENTAR BULGARIA OOD | EIK 175369610 | legal@nevumo.com",
        "lt":    "FILIPHS TSENTAR BULGARIA OOD | EIK 175369610 | legal@nevumo.com",
        "lv":    "FILIPHS TSENTAR BULGARIA OOD | EIK 175369610 | legal@nevumo.com",
        "mk":    "FILIPHS TSENTAR BULGARIA OOD | EIK 175369610 | legal@nevumo.com",
        "mt":    "FILIPHS TSENTAR BULGARIA OOD | EIC 175369610 | legal@nevumo.com",
        "nl":    "FILIPHS TSENTAR BULGARIA OOD | EIK 175369610 | legal@nevumo.com",
        "no":    "FILIPHS TSENTAR BULGARIA OOD | EIK 175369610 | legal@nevumo.com",
        "pl":    "FILIPHS TSENTAR BULGARIA OOD | EIK 175369610 | legal@nevumo.com",
        "pt":    "FILIPHS TSENTAR BULGARIA OOD | EIC 175369610 | legal@nevumo.com",
        "pt-PT": "FILIPHS TSENTAR BULGARIA OOD | EIC 175369610 | legal@nevumo.com",
        "ro":    "FILIPHS TSENTAR BULGARIA OOD | EIC 175369610 | legal@nevumo.com",
        "ru":    "FILIPHS TSENTAR BULGARIA OOD | EIK 175369610 | legal@nevumo.com",
        "sk":    "FILIPHS TSENTAR BULGARIA OOD | EIK 175369610 | legal@nevumo.com",
        "sl":    "FILIPHS TSENTAR BULGARIA OOD | EIK 175369610 | legal@nevumo.com",
        "sq":    "FILIPHS TSENTAR BULGARIA OOD | EIC 175369610 | legal@nevumo.com",
        "sr":    "FILIPHS TSENTAR BULGARIA OOD | EIK 175369610 | legal@nevumo.com",
        "sv":    "FILIPHS TSENTAR BULGARIA OOD | EIK 175369610 | legal@nevumo.com",
        "tr":    "FILIPHS TSENTAR BULGARIA OOD | EIK 175369610 | legal@nevumo.com",
        "uk":    "FILIPHS TSENTAR BULGARIA OOD | EIK 175369610 | legal@nevumo.com",
    },
    "contact_legal": {
        "bg":    "Pravni vaprosi: legal@nevumo.com | Lichni danni: privacy@nevumo.com",
        "cs":    "Pravni dotazy: legal@nevumo.com | Osobni udaje: privacy@nevumo.com",
        "da":    "Juridiske sporgsmal: legal@nevumo.com | Personoplysninger: privacy@nevumo.com",
        "de":    "Rechtliche Fragen: legal@nevumo.com | Datenschutz: privacy@nevumo.com",
        "el":    "Nomika zitimata: legal@nevumo.com | Prosopika dedomena: privacy@nevumo.com",
        "en":    "Legal matters: legal@nevumo.com | Personal data: privacy@nevumo.com",
        "es":    "Asuntos legales: legal@nevumo.com | Datos personales: privacy@nevumo.com",
        "et":    "Juriidilised kusimused: legal@nevumo.com | Isikuandmed: privacy@nevumo.com",
        "fi":    "Juridiset asiat: legal@nevumo.com | Henkilotiedot: privacy@nevumo.com",
        "fr":    "Questions juridiques: legal@nevumo.com | Donnees personnelles: privacy@nevumo.com",
        "ga":    "Cursai dli: legal@nevumo.com | Sonrai pearsanta: privacy@nevumo.com",
        "hr":    "Pravna pitanja: legal@nevumo.com | Osobni podaci: privacy@nevumo.com",
        "hu":    "Jogi kerdesek: legal@nevumo.com | Szemelyes adatok: privacy@nevumo.com",
        "is":    "Lagaleg malefni: legal@nevumo.com | Personuupplysingar: privacy@nevumo.com",
        "it":    "Questioni legali: legal@nevumo.com | Dati personali: privacy@nevumo.com",
        "lb":    "Rechtlech Froen: legal@nevumo.com | Perseenlech Daten: privacy@nevumo.com",
        "lt":    "Teisiniai klausimai: legal@nevumo.com | Asmens duomenys: privacy@nevumo.com",
        "lv":    "Juridiskie jautajumi: legal@nevumo.com | Personas dati: privacy@nevumo.com",
        "mk":    "Pravni prasanja: legal@nevumo.com | Lichni podatoci: privacy@nevumo.com",
        "mt":    "Kwistjonijiet legali: legal@nevumo.com | Data personali: privacy@nevumo.com",
        "nl":    "Juridische zaken: legal@nevumo.com | Persoonsgegevens: privacy@nevumo.com",
        "no":    "Juridiske sporsmal: legal@nevumo.com | Personopplysninger: privacy@nevumo.com",
        "pl":    "Sprawy prawne: legal@nevumo.com | Dane osobowe: privacy@nevumo.com",
        "pt":    "Assuntos juridicos: legal@nevumo.com | Dados pessoais: privacy@nevumo.com",
        "pt-PT": "Assuntos juridicos: legal@nevumo.com | Dados pessoais: privacy@nevumo.com",
        "ro":    "Chestiuni legale: legal@nevumo.com | Date personale: privacy@nevumo.com",
        "ru":    "Yuridicheskie voprosy: legal@nevumo.com | Personal'nye dannye: privacy@nevumo.com",
        "sk":    "Pravne zalezitosti: legal@nevumo.com | Osobne udaje: privacy@nevumo.com",
        "sl":    "Pravna vprasanja: legal@nevumo.com | Osebni podatki: privacy@nevumo.com",
        "sq":    "Ceshtje ligjore: legal@nevumo.com | Te dhena personale: privacy@nevumo.com",
        "sr":    "Pravna pitanja: legal@nevumo.com | Licni podaci: privacy@nevumo.com",
        "sv":    "Juridiska fragor: legal@nevumo.com | Personuppgifter: privacy@nevumo.com",
        "tr":    "Hukuki konular: legal@nevumo.com | Kisisel veriler: privacy@nevumo.com",
        "uk":    "Yurydychni pytannya: legal@nevumo.com | Personal'ni dani: privacy@nevumo.com",
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
            f"✅ seed_provider_terms_p2_ui: {count} rows upserted "
            f"({NAMESPACE}: pl_notice, back_to_home, operator_info, contact_legal x 34 langs)"
        )

    engine.dispose()


if __name__ == "__main__":
    seed()