#!/usr/bin/env python3
"""
Seed footer translations (Part 2).
Namespace: footer
Keys: 2 (provider_terms_link, withdrawal_link) | Languages: 34
Run: docker exec nevumo-api python -m apps.api.scripts.seed_footer_translations_p2
"""

import os

from sqlalchemy import create_engine, text

NAMESPACE = "footer"

# Language dictionaries with full keys (including namespace)
TRANSLATIONS_BY_LANG = {
    "en": {
        "footer.provider_terms_link": "Terms for Providers",
        "footer.withdrawal_link": "Withdrawal Form",
    },
    "bg": {
        "footer.provider_terms_link": "Условия за доставчици",
        "footer.withdrawal_link": "Формуляр за отказ",
    },
    "cs": {
        "footer.provider_terms_link": "Podmínky pro poskytovatele",
        "footer.withdrawal_link": "Formulář pro odstoupení",
    },
    "da": {
        "footer.provider_terms_link": "Vilkår for udbydere",
        "footer.withdrawal_link": "Fortrydelsesformular",
    },
    "de": {
        "footer.provider_terms_link": "AGB für Anbieter",
        "footer.withdrawal_link": "Widerrufsformular",
    },
    "el": {
        "footer.provider_terms_link": "Όροι για παρόχους",
        "footer.withdrawal_link": "Έντυπο υπαναχώρησης",
    },
    "es": {
        "footer.provider_terms_link": "Condiciones para proveedores",
        "footer.withdrawal_link": "Formulario de desistimiento",
    },
    "et": {
        "footer.provider_terms_link": "Tingimused teenusepakkujatele",
        "footer.withdrawal_link": "Taganemisvorm",
    },
    "fi": {
        "footer.provider_terms_link": "Ehdot palveluntarjoajille",
        "footer.withdrawal_link": "Peruutuslomake",
    },
    "fr": {
        "footer.provider_terms_link": "CGU Prestataires",
        "footer.withdrawal_link": "Formulaire de rétractation",
    },
    "ga": {
        "footer.provider_terms_link": "Téarmaí d'Fheidhmeannais",
        "footer.withdrawal_link": "Foirm Aistarraingthe",
    },
    "hr": {
        "footer.provider_terms_link": "Uvjeti za pružatelje usluga",
        "footer.withdrawal_link": "Obrazac za odustanak",
    },
    "hu": {
        "footer.provider_terms_link": "Feltételek szolgáltatóknak",
        "footer.withdrawal_link": "Elállási nyilatkozat",
    },
    "is": {
        "footer.provider_terms_link": "Skilmálar fyrir þjónustuveitendur",
        "footer.withdrawal_link": "Afturköllunarbeiðni",
    },
    "it": {
        "footer.provider_terms_link": "Termini per i fornitori",
        "footer.withdrawal_link": "Modulo di recesso",
    },
    "lb": {
        "footer.provider_terms_link": "Konditioune fir Ubidder",
        "footer.withdrawal_link": "Récktrëttsformular",
    },
    "lt": {
        "footer.provider_terms_link": "Taisyklės paslaugų teikėjams",
        "footer.withdrawal_link": "Atsisakymo forma",
    },
    "lv": {
        "footer.provider_terms_link": "Noteikumi pakalpojumu sniedzējiem",
        "footer.withdrawal_link": "Atteikuma veidlapa",
    },
    "mk": {
        "footer.provider_terms_link": "Услови за даватели на услуги",
        "footer.withdrawal_link": "Образец за откажување",
    },
    "mt": {
        "footer.provider_terms_link": "Termini għall-fornituri",
        "footer.withdrawal_link": "Formola ta' rtirar",
    },
    "nl": {
        "footer.provider_terms_link": "Voorwaarden voor aanbieders",
        "footer.withdrawal_link": "Herroepingsformulier",
    },
    "no": {
        "footer.provider_terms_link": "Vilkår for leverandører",
        "footer.withdrawal_link": "Angrerettskjema",
    },
    "pl": {
        "footer.provider_terms_link": "Regulamin dla usługodawców",
        "footer.withdrawal_link": "Formularz odstąpienia",
    },
    "pt": {
        "footer.provider_terms_link": "Termos para Prestadores",
        "footer.withdrawal_link": "Formulário de desistência",
    },
    "pt-PT": {
        "footer.provider_terms_link": "Termos para Prestadores",
        "footer.withdrawal_link": "Formulário de desistência",
    },
    "ro": {
        "footer.provider_terms_link": "Termeni pentru furnizori",
        "footer.withdrawal_link": "Formular de retragere",
    },
    "ru": {
        "footer.provider_terms_link": "Условия для поставщиков",
        "footer.withdrawal_link": "Форма отказа от услуг",
    },
    "sk": {
        "footer.provider_terms_link": "Podmienky pre poskytovateľov",
        "footer.withdrawal_link": "Formulár na odstúpenie",
    },
    "sl": {
        "footer.provider_terms_link": "Pogoji za ponudnike",
        "footer.withdrawal_link": "Obrazec za odstop",
    },
    "sq": {
        "footer.provider_terms_link": "Kushtet për ofruesit",
        "footer.withdrawal_link": "Formular tërheqjeje",
    },
    "sr": {
        "footer.provider_terms_link": "Uslovi za pružaoce usluga",
        "footer.withdrawal_link": "Obrazac za odustanak",
    },
    "sv": {
        "footer.provider_terms_link": "Villkor för leverantörer",
        "footer.withdrawal_link": "Ångerblankett",
    },
    "tr": {
        "footer.provider_terms_link": "Hizmet Sağlayıcı Koşulları",
        "footer.withdrawal_link": "Cayma Formu",
    },
    "uk": {
        "footer.provider_terms_link": "Умови для постачальників",
        "footer.withdrawal_link": "Форма відмови від послуги",
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
