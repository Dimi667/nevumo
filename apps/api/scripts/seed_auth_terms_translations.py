#!/usr/bin/env python3
"""Seed auth terms translations into the translations table."""

import os
import psycopg2
from psycopg2.extras import execute_values

# Database connection string
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://nevumo:nevumo@localhost:5433/nevumo_leads")

# Translations: language -> dict of key -> value
TRANSLATIONS = {
  "bg": {
    "auth.terms_accept_prefix": "Прочетох и приемам",
    "auth.terms_link": "Общи условия",
    "auth.terms_provider_link": "Условия за доставчици",
    "auth.terms_and": "и",
    "auth.privacy_link": "Политика за поверителност",
    "auth.modal_title_terms": "Общи условия за клиенти на Nevumo",
    "auth.modal_title_terms_provider": "Общи условия за Доставчици на Услуги",
    "auth.modal_title_privacy": "Политика за поверителност"
  },
  "cs": {
    "auth.terms_accept_prefix": "Přečetl jsem si a akceptuji",
    "auth.terms_link": "Všeobecné obchodní podmínky",
    "auth.terms_provider_link": "Podmínky pro poskytovatele",
    "auth.terms_and": "a",
    "auth.privacy_link": "Zásady ochrany osobních údajů",
    "auth.modal_title_terms": "Obchodní podmínky pro klienty Nevumo",
    "auth.modal_title_terms_provider": "Podmínky pro Poskytovatele Služeb",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "da": {
    "auth.terms_accept_prefix": "Jeg har læst og accepterer",
    "auth.terms_link": "Generelle vilkår",
    "auth.terms_provider_link": "Vilkår for leverandører",
    "auth.terms_and": "og",
    "auth.privacy_link": "Privatlivspolitik",
    "auth.modal_title_terms": "Betingelser for klienter på Nevumo",
    "auth.modal_title_terms_provider": "Vilkår og betingelser for tjenesteudbydere",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "de": {
    "auth.terms_accept_prefix": "Ich habe gelesen und akzeptiere",
    "auth.terms_link": "Allgemeine Geschäftsbedingungen",
    "auth.terms_provider_link": "Bedingungen für Anbieter",
    "auth.terms_and": "und",
    "auth.privacy_link": "Datenschutzrichtlinie",
    "auth.modal_title_terms": "Allgemeine Geschäftsbedingungen für Kunden von Nevumo",
    "auth.modal_title_terms_provider": "Nutzungsbedingungen für Dienstleister",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "el": {
    "auth.terms_accept_prefix": "Έχω διαβάσει και αποδέχομαι",
    "auth.terms_link": "Όροι και Προϋποθέσεις",
    "auth.terms_provider_link": "Όροι για παρόχους",
    "auth.terms_and": "και",
    "auth.privacy_link": "Πολιτική απορρήτου",
    "auth.modal_title_terms": "Όροι και Προϋποθέσεις για Πελάτες του Nevumo",
    "auth.modal_title_terms_provider": "Όροι και Προϋποθέσεις για Παρόχους Υπηρεσιών",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "en": {
    "auth.terms_accept_prefix": "I have read and accept",
    "auth.terms_link": "Terms and Conditions",
    "auth.terms_provider_link": "Provider Terms",
    "auth.terms_and": "and",
    "auth.privacy_link": "Privacy Policy",
    "auth.modal_title_terms": "Terms & Conditions for Clients",
    "auth.modal_title_terms_provider": "Terms & Conditions for Service Providers",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "es": {
    "auth.terms_accept_prefix": "He leído y acepto",
    "auth.terms_link": "Términos y condiciones",
    "auth.terms_provider_link": "Términos para proveedores",
    "auth.terms_and": "y",
    "auth.privacy_link": "Política de privacidad",
    "auth.modal_title_terms": "Términos y Condiciones para Clientes de Nevumo",
    "auth.modal_title_terms_provider": "Términos y Condiciones para Proveedores de Servicios",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "et": {
    "auth.terms_accept_prefix": "Olen lugenud ja nõustun",
    "auth.terms_link": "Kasutustingimused",
    "auth.terms_provider_link": "Tingimused teenusepakkujatele",
    "auth.terms_and": "ja",
    "auth.privacy_link": "Privaatsuspoliitika",
    "auth.modal_title_terms": "Nevumo klientide kasutustingimused",
    "auth.modal_title_terms_provider": "Teenusepakkujate tingimused",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "fi": {
    "auth.terms_accept_prefix": "Olen lukenut ja hyväksyn",
    "auth.terms_link": "Käyttöehdot",
    "auth.terms_provider_link": "Ehdot palveluntarjoajille",
    "auth.terms_and": "ja",
    "auth.privacy_link": "Tietosuojakäytäntö",
    "auth.modal_title_terms": "Käyttöehdot Nevumon asiakkaille",
    "auth.modal_title_terms_provider": "Palveluntarjoajien käyttöehdot",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "fr": {
    "auth.terms_accept_prefix": "J'ai lu et j'accepte",
    "auth.terms_link": "Conditions générales",
    "auth.terms_provider_link": "Conditions pour les prestataires",
    "auth.terms_and": "et",
    "auth.privacy_link": "Politique de confidentialité",
    "auth.modal_title_terms": "Conditions générales d'utilisation pour les clients de Nevumo",
    "auth.modal_title_terms_provider": "Conditions générales pour les Prestataires de Services",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "ga": {
    "auth.terms_accept_prefix": "Léigh mé agus glacaim le",
    "auth.terms_link": "Téarmaí agus Coinníollacha",
    "auth.terms_provider_link": "Téarmaí Soláthraí",
    "auth.terms_and": "agus",
    "auth.privacy_link": "Polasaí Príobháideachais",
    "auth.modal_title_terms": "Téarmaí agus Coinníollacha do Chliaint Nevumo",
    "auth.modal_title_terms_provider": "Téarmaí agus Coinníollacha do Sholáthróirí Seirbhíse",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "hr": {
    "auth.terms_accept_prefix": "Pročitao sam i prihvaćam",
    "auth.terms_link": "Opći uvjeti",
    "auth.terms_provider_link": "Uvjeti za pružatelje",
    "auth.terms_and": "i",
    "auth.privacy_link": "Pravila o privatnosti",
    "auth.modal_title_terms": "Uvjeti korištenja za klijente Nevumo",
    "auth.modal_title_terms_provider": "Uvjeti poslovanja za pružatelje usluga",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "hu": {
    "auth.terms_accept_prefix": "Elolvastam és elfogadom",
    "auth.terms_link": "Általános Szerződési Feltételek",
    "auth.terms_provider_link": "Szolgáltatói feltételek",
    "auth.terms_and": "és",
    "auth.privacy_link": "Adatvédelmi irányelvek",
    "auth.modal_title_terms": "Általános Szerződési Feltételek Nevumo ügyfelek számára",
    "auth.modal_title_terms_provider": "Szolgáltatók felhasználási feltételei",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "is": {
    "auth.terms_accept_prefix": "Ég hef lesið og samþykki",
    "auth.terms_link": "Skilmálar",
    "auth.terms_provider_link": "Skilmálar fyrir þjónustuveitendur",
    "auth.terms_and": "og",
    "auth.privacy_link": "Persónuverndarstefna",
    "auth.modal_title_terms": "Skilmálar fyrir viðskiptavini Nevumo",
    "auth.modal_title_terms_provider": "Skilmálar og skilyrði fyrir þjónustuaðila",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "it": {
    "auth.terms_accept_prefix": "Ho letto e accetto",
    "auth.terms_link": "Termini e condizioni",
    "auth.terms_provider_link": "Termini per i fornitori",
    "auth.terms_and": "e",
    "auth.privacy_link": "Informativa sulla privacy",
    "auth.modal_title_terms": "Termini e Condizioni per i Clienti di Nevumo",
    "auth.modal_title_terms_provider": "Termini e Condizioni per i Fornitori di Servizi",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "lb": {
    "auth.terms_accept_prefix": "Ech hu gelies an akzeptéieren",
    "auth.terms_link": "Allgemeng Geschäftsbedéngungen",
    "auth.terms_provider_link": "Conditioune fir Ubidder",
    "auth.terms_and": "an",
    "auth.privacy_link": "Dateschutzrichtlinn",
    "auth.modal_title_terms": "Allgemeng Geschäftsbedéngungen fir Klienten vu Nevumo",
    "auth.modal_title_terms_provider": "Konditiounen fir Servicepresser",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "lt": {
    "auth.terms_accept_prefix": "Perskaičiau ir sutinku su",
    "auth.terms_link": "Bendrosios sąlygos",
    "auth.terms_provider_link": "Sąlygos paslaugų teikėjams",
    "auth.terms_and": "ir",
    "auth.privacy_link": "Privatumo politika",
    "auth.modal_title_terms": "Nevumo klientų naudojimo sąlygos",
    "auth.modal_title_terms_provider": "Paslaugų teikėjų naudojimosi sąlygos",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "lv": {
    "auth.terms_accept_prefix": "Esmu izlasījis un piekrītu",
    "auth.terms_link": "Vispārījie noteikumi",
    "auth.terms_provider_link": "Noteikumi pakalpojumu sniedzējiem",
    "auth.terms_and": "un",
    "auth.privacy_link": "Privātuma politika",
    "auth.modal_title_terms": "Nevumo klientu lietošanas noteikumi",
    "auth.modal_title_terms_provider": "Pakalpojumu sniedzēju lietošanas noteikumi",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "mk": {
    "auth.terms_accept_prefix": "Прочитав и прифаќам",
    "auth.terms_link": "Општи услови",
    "auth.terms_provider_link": "Услови за добавувачи",
    "auth.terms_and": "и",
    "auth.privacy_link": "Политика за приватност",
    "auth.modal_title_terms": "Општи услови за клиенти на Nevumo",
    "auth.modal_title_terms_provider": "Услови за Давачи на Услуги",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "mt": {
    "auth.terms_accept_prefix": "Qrajt u naċċetta",
    "auth.terms_link": "Termini u Kundizzjonijiet",
    "auth.terms_provider_link": "Termini tal-Fornitur",
    "auth.terms_and": "u",
    "auth.privacy_link": "Politika tal-Privatezza",
    "auth.modal_title_terms": "Termini u Kundizzjonijiet għall-Klijenti ta' Nevumo",
    "auth.modal_title_terms_provider": "Termini u Kundizzjonijiet għall-Fornituri tas-Servizz",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "nl": {
    "auth.terms_accept_prefix": "Ik heb gelezen en accepteer",
    "auth.terms_link": "Algemene voorwaarden",
    "auth.terms_provider_link": "Voorwaarden voor aanbieders",
    "auth.terms_and": "en",
    "auth.privacy_link": "Privacybeleid",
    "auth.modal_title_terms": "Algemene Voorwaarden voor Klanten van Nevumo",
    "auth.modal_title_terms_provider": "Algemene voorwaarden voor dienstverleners",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "no": {
    "auth.terms_accept_prefix": "Jeg har lest og godtar",
    "auth.terms_link": "Generelle vilkår",
    "auth.terms_provider_link": "Vilkår for leverandører",
    "auth.terms_and": "og",
    "auth.privacy_link": "Personvernerklæring",
    "auth.modal_title_terms": "Vilkår og betingelser for kunder av Nevumo",
    "auth.modal_title_terms_provider": "Vilkår og betingelser for tjenesteleverandører",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "pl": {
    "auth.terms_accept_prefix": "Przeczytałem i akceptuję",
    "auth.terms_link": "Regulamin",
    "auth.terms_provider_link": "Warunki dla dostawców",
    "auth.terms_and": "i",
    "auth.privacy_link": "Polityka prywatności",
    "auth.modal_title_terms": "Regulamin serwisu Nevumo dla Klientów",
    "auth.modal_title_terms_provider": "Regulamin dla Dostawców Usług",
    "auth.modal_title_privacy": "Polityka prywatności"
  },
  "pt": {
    "auth.terms_accept_prefix": "Li e aceito",
    "auth.terms_link": "Termos e condições",
    "auth.terms_provider_link": "Termos para fornecedores",
    "auth.terms_and": "e",
    "auth.privacy_link": "Política de privacidade",
    "auth.modal_title_terms": "Termos e Condições para Clientes da Nevumo",
    "auth.modal_title_terms_provider": "Termos e Condições para Prestadores de Serviços",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "pt-PT": {
    "auth.terms_accept_prefix": "Li e aceito",
    "auth.terms_link": "Termos e condições",
    "auth.terms_and": "e",
    "auth.privacy_link": "Política de privacidade",
    "auth.terms_provider_link": "Termos para fornecedores",
    "auth.modal_title_terms": "Termos e Condições para Clientes da Nevumo",
    "auth.modal_title_terms_provider": "Termos e Condições para Prestadores de Serviços",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "ro": {
    "auth.terms_accept_prefix": "Am citit și accept",
    "auth.terms_link": "Termeni și condiții",
    "auth.terms_provider_link": "Termeni pentru furnizori",
    "auth.terms_and": "și",
    "auth.privacy_link": "Politica de confidențialitate",
    "auth.modal_title_terms": "Termeni și Condiții pentru Clienții Nevumo",
    "auth.modal_title_terms_provider": "Termeni și condiții pentru Furnizorii de Servicii",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "ru": {
    "auth.terms_accept_prefix": "Я прочитал и принимаю",
    "auth.terms_link": "Условия использования",
    "auth.terms_provider_link": "Условия для поставщиков",
    "auth.terms_and": "и",
    "auth.privacy_link": "Политика конфиденциальности",
    "auth.modal_title_terms": "Пользовательское соглашение для клиентов Nevumo",
    "auth.modal_title_terms_provider": "Условия использования для Поставщиков Услуг",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "sk": {
    "auth.terms_accept_prefix": "Prečítal som si a súhlasím s",
    "auth.terms_link": "Všeobecné obchodné podmienky",
    "auth.terms_provider_link": "Podmienky pre poskytovateľov",
    "auth.terms_and": "a",
    "auth.privacy_link": "Zásady ochrony danych osobowych",
    "auth.modal_title_terms": "Všeobecné obchodné podmienky pre klientov Nevumo",
    "auth.modal_title_terms_provider": "Podmienky pre Poskytovateľov Služieb",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "sl": {
    "auth.terms_accept_prefix": "Prebral sem in sprejemam",
    "auth.terms_link": "Splošni pogoji",
    "auth.terms_provider_link": "Pogoji za ponudnike",
    "auth.terms_and": "in",
    "auth.privacy_link": "Pravilnik o zasebnosti",
    "auth.modal_title_terms": "Splošni pogoji za stranke Nevumo",
    "auth.modal_title_terms_provider": "Pogoji za ponudnike storitev",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "sq": {
    "auth.terms_accept_prefix": "Kam lexuar dhe pranoj",
    "auth.terms_link": "Termat dhe Kushtet",
    "auth.terms_provider_link": "Termat për ofruesit",
    "auth.terms_and": "dhe",
    "auth.privacy_link": "Politika e privatësisë",
    "auth.modal_title_terms": "Termat dhe Kushtet për Klientët e Nevumo",
    "auth.modal_title_terms_provider": "Termat dhe Kushtet për Ofruesit e Shërbimeve",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "sr": {
    "auth.terms_accept_prefix": "Pročitao sam i prihvatam",
    "auth.terms_link": "Opšti uslovi",
    "auth.terms_provider_link": "Uslovi za dobavljače",
    "auth.terms_and": "i",
    "auth.privacy_link": "Politika privatnosti",
    "auth.modal_title_terms": "Opšti uslovi korišćenja za klijente Nevumo",
    "auth.modal_title_terms_provider": "Услови коришћења за Пружаоце Услуга",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "sv": {
    "auth.terms_accept_prefix": "Jag har läst och godkänner",
    "auth.terms_link": "Allmänna villkor",
    "auth.terms_provider_link": "Villkor för leverantörer",
    "auth.terms_and": "och",
    "auth.privacy_link": "Integritetspolicy",
    "auth.modal_title_terms": "Allmänna villkor för kunder hos Nevumo",
    "auth.modal_title_terms_provider": "Villkor för tjänsteleverantörer",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "tr": {
    "auth.terms_accept_prefix": "Okudum ve kabul ediyorum",
    "auth.terms_link": "Şartlar ve Koşullar",
    "auth.terms_provider_link": "Sağlayıcı Şartları",
    "auth.terms_and": "ve",
    "auth.privacy_link": "Gizlilik Politikası",
    "auth.modal_title_terms": "Nevumo Müşterileri için Hüküm ve Koşullar",
    "auth.modal_title_terms_provider": "Hizmet Sağlayıcılar için Kullanım Koşulları",
    "auth.modal_title_privacy": "Privacy Policy"
  },
  "uk": {
    "auth.terms_accept_prefix": "Я прочитав і приймаю",
    "auth.terms_link": "Умови та положення",
    "auth.terms_provider_link": "Умови для постачальників",
    "auth.terms_and": "та",
    "auth.privacy_link": "Політика конфіденційності",
    "auth.modal_title_terms": "Загальні умови для клієнтів Nevumo",
    "auth.modal_title_terms_provider": "Умови використання для Постачальників Послуг",
    "auth.modal_title_privacy": "Privacy Policy"
  }
}


def seed_translations() -> int:
    """Seed auth terms translations and return the number of rows upserted."""
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    rows_to_upsert = []
    for lang, translations in TRANSLATIONS.items():
        for key, value in translations.items():
            rows_to_upsert.append((lang, key, value))

    execute_values(
        cursor,
        """
        INSERT INTO translations (lang, key, value)
        VALUES %s
        ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
        """,
        rows_to_upsert,
        template="(%s, %s, %s)",
    )

    conn.commit()
    cursor.close()
    conn.close()

    return len(rows_to_upsert)


if __name__ == "__main__":
    count = seed_translations()
    print(f"Upserted {count} rows (8 keys × 34 languages)")
