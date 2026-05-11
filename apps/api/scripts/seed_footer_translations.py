#!/usr/bin/env python3
"""
Seed footer translations.
Namespace: footer
Keys: 5 | Languages: 34
Run: docker exec nevumo-api python -m apps.api.scripts.seed_footer_translations
"""

import os

from sqlalchemy import create_engine, text

NAMESPACE = "footer"

# Language dictionaries with full keys (including namespace)
TRANSLATIONS_BY_LANG = {
    "en": {
        "footer.privacy_policy_link": "Privacy Policy",
        "footer.cookies_link": "Cookie Policy",
        "footer.terms_link": "Terms & Conditions",
        "footer.register_privacy_note": "By registering you agree to our",
        "footer.register_privacy_link": "Privacy Policy",
    },
    "bg": {
        "footer.privacy_policy_link": "Политика за поверителност",
        "footer.cookies_link": "Политика за бисквитки",
        "footer.terms_link": "Общи условия",
        "footer.register_privacy_note": "С регистрацията се съгласявате с нашата",
        "footer.register_privacy_link": "Политика за поверителност",
    },
    "cs": {
        "footer.privacy_policy_link": "Zásady ochrany osobních údajů",
        "footer.cookies_link": "Zásady cookies",
        "footer.terms_link": "Obchodní podmínky",
        "footer.register_privacy_note": "Registrací souhlasíte s našimi",
        "footer.register_privacy_link": "Zásadami ochrany osobních údajů",
    },
    "da": {
        "footer.privacy_policy_link": "Privatlivspolitik",
        "footer.cookies_link": "Cookiepolitik",
        "footer.terms_link": "Vilkår og betingelser",
        "footer.register_privacy_note": "Ved registrering accepterer du vores",
        "footer.register_privacy_link": "Privatlivspolitik",
    },
    "de": {
        "footer.privacy_policy_link": "Datenschutzerklärung",
        "footer.cookies_link": "Cookie-Richtlinie",
        "footer.terms_link": "Nutzungsbedingungen",
        "footer.register_privacy_note": "Mit der Registrierung stimmen Sie unserer",
        "footer.register_privacy_link": "Datenschutzerklärung",
    },
    "el": {
        "footer.privacy_policy_link": "Πολιτική Απορρήτου",
        "footer.cookies_link": "Πολιτική Cookies",
        "footer.terms_link": "Όροι Χρήσης",
        "footer.register_privacy_note": "Με την εγγραφή συμφωνείτε με την",
        "footer.register_privacy_link": "Πολιτική Απορρήτου",
    },
    "es": {
        "footer.privacy_policy_link": "Política de privacidad",
        "footer.cookies_link": "Política de cookies",
        "footer.terms_link": "Términos y condiciones",
        "footer.register_privacy_note": "Al registrarte aceptas nuestra",
        "footer.register_privacy_link": "Política de privacidad",
    },
    "et": {
        "footer.privacy_policy_link": "Privaatsuspoliitika",
        "footer.cookies_link": "Küpsiste poliitika",
        "footer.terms_link": "Kasutustingimused",
        "footer.register_privacy_note": "Registreerudes nõustute meie",
        "footer.register_privacy_link": "Privaatsuspoliitikaga",
    },
    "fi": {
        "footer.privacy_policy_link": "Tietosuojakäytäntö",
        "footer.cookies_link": "Evästekäytäntö",
        "footer.terms_link": "Käyttöehdot",
        "footer.register_privacy_note": "Rekisteröitymällä hyväksyt meidän",
        "footer.register_privacy_link": "Tietosuojakäytännön",
    },
    "fr": {
        "footer.privacy_policy_link": "Politique de confidentialité",
        "footer.cookies_link": "Politique de cookies",
        "footer.terms_link": "Conditions d'utilisation",
        "footer.register_privacy_note": "En vous inscrivant, vous acceptez notre",
        "footer.register_privacy_link": "Politique de confidentialité",
    },
    "ga": {
        "footer.privacy_policy_link": "Polasaí Príobháideachais",
        "footer.cookies_link": "Polasaí Fianán",
        "footer.terms_link": "Téarmaí agus Coinníollacha",
        "footer.register_privacy_note": "Trí chlárú, aontaíonn tú lenár",
        "footer.register_privacy_link": "Polasaí Príobháideachais",
    },
    "hr": {
        "footer.privacy_policy_link": "Politika privatnosti",
        "footer.cookies_link": "Politika kolačića",
        "footer.terms_link": "Uvjeti korištenja",
        "footer.register_privacy_note": "Registracijom prihvaćate našu",
        "footer.register_privacy_link": "Politiku privatnosti",
    },
    "hu": {
        "footer.privacy_policy_link": "Adatvédelmi irányelvek",
        "footer.cookies_link": "Cookie-szabályzat",
        "footer.terms_link": "Felhasználási feltételek",
        "footer.register_privacy_note": "A regisztrációval elfogadja az",
        "footer.register_privacy_link": "Adatvédelmi irányelveinket",
    },
    "is": {
        "footer.privacy_policy_link": "Persónuverndarstefna",
        "footer.cookies_link": "Vafrakökustefna",
        "footer.terms_link": "Skilmálar og skilyrði",
        "footer.register_privacy_note": "Með skráningu samþykkir þú",
        "footer.register_privacy_link": "Persónuverndarstefnu okkar",
    },
    "it": {
        "footer.privacy_policy_link": "Informativa sulla privacy",
        "footer.cookies_link": "Politica dei cookie",
        "footer.terms_link": "Termini e condizioni",
        "footer.register_privacy_note": "Registrandoti accetti la nostra",
        "footer.register_privacy_link": "Informativa sulla privacy",
    },
    "lb": {
        "footer.privacy_policy_link": "Datenschutzerklärung",
        "footer.cookies_link": "Cookie-Richtlinie",
        "footer.terms_link": "Allgemeng Geschäftsbedingungen",
        "footer.register_privacy_note": "Mat der Registréierung stëmmt dir eiser",
        "footer.register_privacy_link": "Datenschutzerklärung",
    },
    "lt": {
        "footer.privacy_policy_link": "Privatumo politika",
        "footer.cookies_link": "Slapukų politika",
        "footer.terms_link": "Naudojimo sąlygos",
        "footer.register_privacy_note": "Registruodamiesi sutinkate su mūsų",
        "footer.register_privacy_link": "Privatumo politika",
    },
    "lv": {
        "footer.privacy_policy_link": "Privātuma politika",
        "footer.cookies_link": "Sīkdatņu politika",
        "footer.terms_link": "Lietošanas noteikumi",
        "footer.register_privacy_note": "Reģistrējoties jūs piekrītat mūsu",
        "footer.register_privacy_link": "Privātuma politikai",
    },
    "mk": {
        "footer.privacy_policy_link": "Политика за приватност",
        "footer.cookies_link": "Политика за колачиња",
        "footer.terms_link": "Услови за користење",
        "footer.register_privacy_note": "Со регистрација се согласувате со нашата",
        "footer.register_privacy_link": "Политика за приватност",
    },
    "mt": {
        "footer.privacy_policy_link": "Politika tal-Privatezza",
        "footer.cookies_link": "Politika tal-Cookies",
        "footer.terms_link": "Termini u Kondizzjonijiet",
        "footer.register_privacy_note": "Billi tirreġistra taqbel mal-",
        "footer.register_privacy_link": "Politika tal-Privatezza tagħna",
    },
    "nl": {
        "footer.privacy_policy_link": "Privacybeleid",
        "footer.cookies_link": "Cookiebeleid",
        "footer.terms_link": "Algemene voorwaarden",
        "footer.register_privacy_note": "Door te registreren ga je akkoord met ons",
        "footer.register_privacy_link": "Privacybeleid",
    },
    "no": {
        "footer.privacy_policy_link": "Personvernpolicy",
        "footer.cookies_link": "Cookiepolicy",
        "footer.terms_link": "Vilkår og betingelser",
        "footer.register_privacy_note": "Ved å registrere deg godtar du vår",
        "footer.register_privacy_link": "Personvernpolicy",
    },
    "pl": {
        "footer.privacy_policy_link": "Polityka prywatności",
        "footer.cookies_link": "Polityka cookies",
        "footer.terms_link": "Regulamin",
        "footer.register_privacy_note": "Rejestrując się, akceptujesz naszą",
        "footer.register_privacy_link": "Politykę prywatności",
    },
    "pt": {
        "footer.privacy_policy_link": "Política de privacidade",
        "footer.cookies_link": "Política de cookies",
        "footer.terms_link": "Termos e condições",
        "footer.register_privacy_note": "Ao se registrar você concorda com nossa",
        "footer.register_privacy_link": "Política de privacidade",
    },
    "pt-PT": {
        "footer.privacy_policy_link": "Política de privacidade",
        "footer.cookies_link": "Política de cookies",
        "footer.terms_link": "Termos e condições",
        "footer.register_privacy_note": "Ao registar-se, aceita a nossa",
        "footer.register_privacy_link": "Política de privacidade",
    },
    "ro": {
        "footer.privacy_policy_link": "Politica de confidențialitate",
        "footer.cookies_link": "Politica de cookies",
        "footer.terms_link": "Termeni și condiții",
        "footer.register_privacy_note": "Prin înregistrare ești de acord cu",
        "footer.register_privacy_link": "Politica noastră de confidențialitate",
    },
    "ru": {
        "footer.privacy_policy_link": "Политика конфиденциальности",
        "footer.cookies_link": "Политика cookies",
        "footer.terms_link": "Условия использования",
        "footer.register_privacy_note": "Регистрируясь, вы соглашаетесь с нашей",
        "footer.register_privacy_link": "Политикой конфиденциальности",
    },
    "sk": {
        "footer.privacy_policy_link": "Zásady ochrany osobných údajov",
        "footer.cookies_link": "Zásady cookies",
        "footer.terms_link": "Obchodné podmienky",
        "footer.register_privacy_note": "Registráciou súhlasíte s našimi",
        "footer.register_privacy_link": "Zásadami ochrany osobných údajov",
    },
    "sl": {
        "footer.privacy_policy_link": "Politika zasebnosti",
        "footer.cookies_link": "Politika piškotkov",
        "footer.terms_link": "Pogoji uporabe",
        "footer.register_privacy_note": "Z registracijo se strinjate z našo",
        "footer.register_privacy_link": "Politiko zasebnosti",
    },
    "sq": {
        "footer.privacy_policy_link": "Politika e privatësisë",
        "footer.cookies_link": "Politika e cookies",
        "footer.terms_link": "Kushtet e shërbimit",
        "footer.register_privacy_note": "Duke u regjistruar pranoni",
        "footer.register_privacy_link": "Politikën tonë të privatësisë",
    },
    "sr": {
        "footer.privacy_policy_link": "Политика приватности",
        "footer.cookies_link": "Политика колачића",
        "footer.terms_link": "Услови коришћења",
        "footer.register_privacy_note": "Регистрацијом прихватате нашу",
        "footer.register_privacy_link": "Политику приватности",
    },
    "sv": {
        "footer.privacy_policy_link": "Integritetspolicy",
        "footer.cookies_link": "Cookiepolicy",
        "footer.terms_link": "Användarvillkor",
        "footer.register_privacy_note": "Genom att registrera dig godkänner du vår",
        "footer.register_privacy_link": "Integritetspolicy",
    },
    "tr": {
        "footer.privacy_policy_link": "Gizlilik Politikası",
        "footer.cookies_link": "Çerez Politikası",
        "footer.terms_link": "Kullanım Koşulları",
        "footer.register_privacy_note": "Kayıt olarak kabul etmiş olursunuz",
        "footer.register_privacy_link": "Gizlilik Politikamızı",
    },
    "uk": {
        "footer.privacy_policy_link": "Політика конфіденційності",
        "footer.cookies_link": "Політика cookies",
        "footer.terms_link": "Умови використання",
        "footer.register_privacy_note": "Реєструючись, ви погоджуєтеся з нашою",
        "footer.register_privacy_link": "Політикою конфіденційності",
    },
}


def get_database_url() -> str:
    """Get database URL from environment or use default."""
    return os.getenv("DATABASE_URL", "postgresql://nevumo:nevumo@localhost:5432/nevumo_leads")


def seed_translations() -> None:
    """Seed all footer translations into the database."""
    engine = create_engine(get_database_url())

    with engine.connect() as conn:
        count = 0
        for lang, translations in TRANSLATIONS_BY_LANG.items():
            for key, value in translations.items():
                conn.execute(
                    text("""
                        INSERT INTO translations (lang, key, value)
                        VALUES (:lang, :key, :value)
                        ON CONFLICT (lang, key)
                        DO UPDATE SET value = EXCLUDED.value
                    """),
                    {"lang": lang, "key": key, "value": value}
                )
                count += 1

        conn.commit()
        print(f"Inserted/updated {count} translation rows for namespace '{NAMESPACE}'")


def verify_translations() -> None:
    """Verify the translations were inserted correctly."""
    engine = create_engine(get_database_url())

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT lang, COUNT(*) as keys
                FROM translations
                WHERE key LIKE :pattern
                GROUP BY lang
                ORDER BY lang
            """),
            {"pattern": f"{NAMESPACE}.%"}
        )
        rows = result.fetchall()
        print(f"\nVerification for namespace '{NAMESPACE}':")
        for row in rows:
            print(f"  {row[0]}: {row[1]} keys")


if __name__ == "__main__":
    seed_translations()
    verify_translations()
