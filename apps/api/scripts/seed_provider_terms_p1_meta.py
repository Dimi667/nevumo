"""
seed_provider_terms_p1_meta.py  —  Nevumo | namespace: provider_terms
Keys: page_title, meta_description, effective_date, version  (4 keys × 34 langs = 136 rows)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_provider_terms_p1_meta
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
    "page_title": {
        "bg":    "Общи условия за Доставчици на Услуги",
        "cs":    "Podmínky pro Poskytovatele Služeb",
        "da":    "Vilkår og betingelser for tjenesteudbydere",
        "de":    "Nutzungsbedingungen für Dienstleister",
        "el":    "Όροι και Προϋποθέσεις για Παρόχους Υπηρεσιών",
        "en":    "Terms & Conditions for Service Providers",
        "es":    "Términos y Condiciones para Proveedores de Servicios",
        "et":    "Teenusepakkujate tingimused",
        "fi":    "Palveluntarjoajien käyttöehdot",
        "fr":    "Conditions générales pour les Prestataires de Services",
        "ga":    "Téarmaí agus Coinníollacha do Sholáthróirí Seirbhíse",
        "hr":    "Uvjeti poslovanja za pružatelje usluga",
        "hu":    "Szolgáltatók felhasználási feltételei",
        "is":    "Skilmálar og skilyrði fyrir þjónustuaðila",
        "it":    "Termini e Condizioni per i Fornitori di Servizi",
        "lb":    "Konditiounen fir Servicepresser",
        "lt":    "Paslaugų teikėjų naudojimosi sąlygos",
        "lv":    "Pakalpojumu sniedzēju lietošanas noteikumi",
        "mk":    "Услови за Давачи на Услуги",
        "mt":    "Termini u Kundizzjonijiet għall-Fornituri tas-Servizz",
        "nl":    "Algemene voorwaarden voor dienstverleners",
        "no":    "Vilkår og betingelser for tjenesteleverandører",
        "pl":    "Regulamin dla Dostawców Usług",
        "pt":    "Termos e Condições para Prestadores de Serviços",
        "pt-PT": "Termos e Condições para Prestadores de Serviços",
        "ro":    "Termeni și condiții pentru Furnizorii de Servicii",
        "ru":    "Условия использования для Поставщиков Услуг",
        "sk":    "Podmienky pre Poskytovateľov Služieb",
        "sl":    "Pogoji za ponudnike storitev",
        "sq":    "Termat dhe Kushtet për Ofruesit e Shërbimeve",
        "sr":    "Услови коришћења за Пружаоце Услуга",
        "sv":    "Villkor för tjänsteleverantörer",
        "tr":    "Hizmet Sağlayıcılar için Kullanım Koşulları",
        "uk":    "Умови використання для Постачальників Послуг",
    },
    "meta_description": {
        "bg":    "Общи условия за доставчици на услуги в платформата Nevumo. Прочетете за вашите права, задължения и начина ни на сътрудничество.",
        "cs":    "Podmínky pro poskytovatele služeb na platformě Nevumo. Přečtěte si o svých právech, povinnostech a způsobu spolupráce.",
        "da":    "Vilkår og betingelser for tjenesteudbydere på Nevumo-platformen. Læs om dine rettigheder, forpligtelser og samarbejdsformen.",
        "de":    "Nutzungsbedingungen für Dienstleister auf der Nevumo-Plattform. Lesen Sie über Ihre Rechte, Pflichten und die Zusammenarbeit.",
        "el":    "Όροι και Προϋποθέσεις για παρόχους υπηρεσιών στην πλατφόρμα Nevumo. Διαβάστε για τα δικαιώματα, τις υποχρεώσεις και τη συνεργασία.",
        "en":    "Terms & Conditions for service providers on the Nevumo platform. Read about your rights, obligations, and how we work together.",
        "es":    "Términos y condiciones para los proveedores de servicios en la plataforma Nevumo. Conozca sus derechos, obligaciones y cómo trabajamos juntos.",
        "et":    "Teenusepakkujate tingimused Nevumo platvormil. Lugege oma õiguste, kohustuste ja koostöö kohta.",
        "fi":    "Palveluntarjoajien käyttöehdot Nevumo-alustalla. Lue oikeuksistasi, velvollisuuksistasi ja yhteistyöstä.",
        "fr":    "Conditions générales pour les prestataires de services sur la plateforme Nevumo. Consultez vos droits, obligations et notre mode de collaboration.",
        "ga":    "Téarmaí agus Coinníollacha do sholáthróirí seirbhíse ar ardán Nevumo. Léigh faoi do chearta, d'oibleagáidí agus conas a oibrímid le chéile.",
        "hr":    "Uvjeti poslovanja za pružatelje usluga na platformi Nevumo. Pročitajte o vašim pravima, obvezama i načinu suradnje.",
        "hu":    "Felhasználási feltételek a Nevumo platform szolgáltatói számára. Olvassa el jogairól, kötelezettségeiről és együttműködésünkről.",
        "is":    "Skilmálar og skilyrði fyrir þjónustuaðila á Nevumo-pallinum. Lestu um réttindi þín, skyldur og samstarf.",
        "it":    "Termini e condizioni per i fornitori di servizi sulla piattaforma Nevumo. Leggi i tuoi diritti, obblighi e il nostro modo di collaborare.",
        "lb":    "Konditiounen fir Servicepresser op der Nevumo-Plattform. Liest méi iwwer Är Rechter, Verpflichtungen an d'Zesummenaarbecht.",
        "lt":    "Paslaugų teikėjų naudojimosi sąlygos Nevumo platformoje. Skaitykite apie savo teises, pareigas ir bendradarbiavimą.",
        "lv":    "Pakalpojumu sniedzēju lietošanas noteikumi Nevumo platformā. Lasiet par savām tiesībām, pienākumiem un sadarbību.",
        "mk":    "Услови за давачи на услуги на платформата Nevumo. Прочитајте за вашите права, обврски и начинот на соработка.",
        "mt":    "Termini u kundizzjonijiet għall-fornituri tas-servizz fuq il-pjattaforma Nevumo. Aqra dwar id-drittijiet, obbligi u kif naħdmu flimkien.",
        "nl":    "Algemene voorwaarden voor dienstverleners op het Nevumo-platform. Lees over uw rechten, verplichtingen en samenwerking.",
        "no":    "Vilkår og betingelser for tjenesteleverandører på Nevumo-plattformen. Les om dine rettigheter, forpliktelser og samarbeid.",
        "pl":    "Regulamin dla dostawców usług na platformie Nevumo. Zapoznaj się ze swoimi prawami, obowiązkami i zasadami współpracy.",
        "pt":    "Termos e condições para prestadores de serviços na plataforma Nevumo. Leia sobre seus direitos, obrigações e como trabalhamos juntos.",
        "pt-PT": "Termos e condições para prestadores de serviços na plataforma Nevumo. Leia sobre os seus direitos, obrigações e como trabalhamos juntos.",
        "ro":    "Termeni și condiții pentru furnizorii de servicii pe platforma Nevumo. Citiți despre drepturile, obligațiile și modul de colaborare.",
        "ru":    "Условия использования для поставщиков услуг на платформе Nevumo. Ознакомьтесь со своими правами, обязанностями и сотрудничеством.",
        "sk":    "Podmienky pre poskytovateľov služieb na platforme Nevumo. Prečítajte si o svojich právach, povinnostiach a spôsobe spolupráce.",
        "sl":    "Pogoji za ponudnike storitev na platformi Nevumo. Preberite o svojih pravicah, obveznostih in načinu sodelovanja.",
        "sq":    "Termat dhe kushtet për ofruesit e shërbimeve në platformën Nevumo. Lexoni rreth të drejtave, detyrimeve dhe mënyrës së bashkëpunimit.",
        "sr":    "Услови коришћења за пружаоце услуга на платформи Nevumo. Прочитајте о вашим правима, обавезама и начину сарадње.",
        "sv":    "Villkor för tjänsteleverantörer på Nevumo-plattformen. Läs om dina rättigheter, skyldigheter och samarbetet.",
        "tr":    "Nevumo platformunda hizmet sağlayıcılar için kullanım koşulları. Haklarınız, yükümlülükleriniz ve birlikte çalışma şeklimiz hakkında okuyun.",
        "uk":    "Умови використання для постачальників послуг на платформі Nevumo. Ознайомтеся зі своїми правами, обов'язками та співпрацею.",
    },
    "effective_date": {
        "bg":    "Дата на влизане в сила: 1 юни 2026 г.",
        "cs":    "Datum platnosti: 1. června 2026",
        "da":    "Ikrafttrædelsesdato: 1. juni 2026",
        "de":    "Gültig ab: 1. Juni 2026",
        "el":    "Ημερομηνία έναρξης ισχύος: 1 Ιουνίου 2026",
        "en":    "Effective date: 1 June 2026",
        "es":    "Fecha de entrada en vigor: 1 de junio de 2026",
        "et":    "Jõustumiskuupäev: 1. juuni 2026",
        "fi":    "Voimaantulopäivä: 1. kesäkuuta 2026",
        "fr":    "Date d'entrée en vigueur : 1er juin 2026",
        "ga":    "Dáta éifeachta: 1 Meitheamh 2026",
        "hr":    "Datum stupanja na snagu: 1. lipnja 2026.",
        "hu":    "Hatálybalépés dátuma: 2026. június 1.",
        "is":    "Gildistökudagur: 1. júní 2026",
        "it":    "Data di entrata in vigore: 1° giugno 2026",
        "lb":    "Datum vum Akraafttriede: 1. Juni 2026",
        "lt":    "Įsigaliojimo data: 2026 m. birželio 1 d.",
        "lv":    "Spēkā stāšanās datums: 2026. gada 1. jūnijs",
        "mk":    "Датум на влегување во сила: 1 јуни 2026 г.",
        "mt":    "Data ta' dħul fis-seħħ: 1 ta' Ġunju 2026",
        "nl":    "Ingangsdatum: 1 juni 2026",
        "no":    "Ikrafttredelsesdato: 1. juni 2026",
        "pl":    "Data wejścia w życie: 1 czerwca 2026 r.",
        "pt":    "Data de vigência: 1º de junho de 2026",
        "pt-PT": "Data de entrada em vigor: 1 de junho de 2026",
        "ro":    "Data intrării în vigoare: 1 iunie 2026",
        "ru":    "Дата вступления в силу: 1 июня 2026 г.",
        "sk":    "Dátum účinnosti: 1. júna 2026",
        "sl":    "Datum veljavnosti: 1. junija 2026",
        "sq":    "Data e hyrjes në fuqi: 1 qershor 2026",
        "sr":    "Датум ступања на снагу: 1. јуна 2026. г.",
        "sv":    "Ikraftträdandedatum: 1 juni 2026",
        "tr":    "Yürürlük tarihi: 1 Haziran 2026",
        "uk":    "Дата набрання чинності: 1 червня 2026 р.",
    },
    "version": {
        "bg":    "Версия: 1.0",
        "cs":    "Verze: 1.0",
        "da":    "Version: 1.0",
        "de":    "Version: 1.0",
        "el":    "Έκδοση: 1.0",
        "en":    "Version: 1.0",
        "es":    "Versión: 1.0",
        "et":    "Versioon: 1.0",
        "fi":    "Versio: 1.0",
        "fr":    "Version : 1.0",
        "ga":    "Leagan: 1.0",
        "hr":    "Verzija: 1.0",
        "hu":    "Verzió: 1.0",
        "is":    "Útgáfa: 1.0",
        "it":    "Versione: 1.0",
        "lb":    "Versioun: 1.0",
        "lt":    "Versija: 1.0",
        "lv":    "Versija: 1.0",
        "mk":    "Верзија: 1.0",
        "mt":    "Verżjoni: 1.0",
        "nl":    "Versie: 1.0",
        "no":    "Versjon: 1.0",
        "pl":    "Wersja: 1.0",
        "pt":    "Versão: 1.0",
        "pt-PT": "Versão: 1.0",
        "ro":    "Versiunea: 1.0",
        "ru":    "Версия: 1.0",
        "sk":    "Verzia: 1.0",
        "sl":    "Različica: 1.0",
        "sq":    "Versioni: 1.0",
        "sr":    "Верзија: 1.0",
        "sv":    "Version: 1.0",
        "tr":    "Sürüm: 1.0",
        "uk":    "Версія: 1.0",
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
            f"✅ seed_provider_terms_p1_meta: {count} rows upserted "
            f"({NAMESPACE}: page_title, meta_description, effective_date, version × 34 langs)"
        )

    engine.dispose()


if __name__ == "__main__":
    seed()
