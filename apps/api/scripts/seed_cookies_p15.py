# -*- coding: utf-8 -*-
"""
seed_cookies_p15.py — namespace 'cookies'
cookies.s5_col_provider, cookies.controller_block
Run: docker exec nevumo-api python -m apps.api.scripts.seed_cookies_p15
"""

import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)

TRANSLATIONS = {
    "cookies.s5_col_provider": {
        "en": "Provider", "bg": "Dostavchik", "cs": "Poskytovatel",
        "da": "Udbyder", "de": "Anbieter", "el": "Parochos",
        "es": "Proveedor", "et": "Pakkuja", "fi": "Palveluntarjoaja",
        "fr": "Fournisseur", "ga": "Solathrai", "hr": "Pruzatelj",
        "hu": "Szolgaltato", "is": "Thjonustuadili", "it": "Fornitore",
        "lb": "Ubidder", "lt": "Teikёjas", "lv": "Sniedzejs",
        "mk": "Provajder", "mt": "Fornitur", "nl": "Aanbieder",
        "no": "Leverandor", "pl": "Dostawca", "pt": "Fornecedor",
        "pt-PT": "Fornecedor", "ro": "Furnizor", "ru": "Postavshchik",
        "sk": "Poskytovatel", "sl": "Ponudnik", "sq": "Ofruesi",
        "sr": "Dobavljac", "sv": "Leverantor", "tr": "Saglayici",
        "uk": "Postachalnnyk",
    },
    "cookies.controller_block": {
        "en": "Controller: \"PHILIPS CENTRE BULGARIA\" Ltd. (trading as Nevumo) - EIK: 175369610 - 77 Petko Karavelov Blvd., Entrance A, Apt. 19, Triaditza District, 1408 Sofia, Bulgaria - privacy@nevumo.com",
        "bg": "Administrator: \"FILIPS TSENTUR BULGARIYA\" OOD (targovski mark Nevumo) - EIK: 175369610 - bul. Petko Karavelov bl. 77, vkh. A, ap. 19, r-n Triadica, p.k. 1408, gr. Sofia, Bulgaria - privacy@nevumo.com",
        "cs": "Spravce: \"PHILIPS CENTRE BULGARIA\" s.r.o. (obchodni znacka Nevumo) - EIK: 175369610 - 77 Petko Karavelov Blvd., vchod A, byt 19, ctvrt Triaditza, 1408 Sofia, Bulharsko - privacy@nevumo.com",
        "da": "Dataansvarlig: \"PHILIPS CENTRE BULGARIA\" Ltd. (handelsnavn Nevumo) - EIK: 175369610 - 77 Petko Karavelov Blvd., indgang A, lejl. 19, Triaditza-kvarter, 1408 Sofia, Bulgarien - privacy@nevumo.com",
        "de": "Verantwortlicher: \"PHILIPS CENTRE BULGARIA\" GmbH (Handelsmarke Nevumo) - EIK: 175369610 - Petko-Karavelov-Blvd. 77, Eingang A, App. 19, Bezirk Triaditza, 1408 Sofia, Bulgarien - privacy@nevumo.com",
        "el": "Ypefthynos: \"PHILIPS CENTRE BULGARIA\" Ltd. (emporiki eponyimia Nevumo) - EIK: 175369610 - 77 Petko Karavelov Blvd., Eisodos A, Diam. 19, Synoikia Triaditza, 1408 Sofia, Voulgaria - privacy@nevumo.com",
        "es": "Responsable: \"PHILIPS CENTRE BULGARIA\" Ltd. (marca comercial Nevumo) - EIK: 175369610 - 77 Petko Karavelov Blvd., Entrada A, Apto. 19, Distrito Triaditza, 1408 Sofia, Bulgaria - privacy@nevumo.com",
        "et": "Vastutav tootleja: \"PHILIPS CENTRE BULGARIA\" OU (kaubamärk Nevumo) - EIK: 175369610 - Petko Karavelov pst 77, sissepääs A, korter 19, Triaditza linnaosa, 1408 Sofia, Bulgaaria - privacy@nevumo.com",
        "fi": "Rekisterinpitaja: \"PHILIPS CENTRE BULGARIA\" Oy (tavaramerkki Nevumo) - EIK: 175369610 - 77 Petko Karavelov Blvd., sisaankaynti A, huoneisto 19, Triaditza, 1408 Sofia, Bulgaria - privacy@nevumo.com",
        "fr": "Responsable du traitement : \"PHILIPS CENTRE BULGARIA\" SARL (marque commerciale Nevumo) - EIK : 175369610 - 77 boulevard Petko Karavelov, entree A, app. 19, quartier Triaditza, 1408 Sofia, Bulgarie - privacy@nevumo.com",
        "ga": "Rialatheoir: \"PHILIPS CENTRE BULGARIA\" Teo. (tradmharc Nevumo) - EIK: 175369610 - 77 Petko Karavelov Blvd., Bealach Isteach A, Arasan 19, Ceantar Triaditza, 1408 Sofia, An Bhulgair - privacy@nevumo.com",
        "hr": "Voditelj obrade: \"PHILIPS CENTRE BULGARIA\" d.o.o. (trgovacka marka Nevumo) - EIK: 175369610 - 77 Petko Karavelov Blvd., ulaz A, stan 19, cetvrt Triaditza, 1408 Sofija, Bugarska - privacy@nevumo.com",
        "hu": "Adatkezelo: \"PHILIPS CENTRE BULGARIA\" Kft. (Nevumo vedjegy) - EIK: 175369610 - 77 Petko Karavelov Blvd., A bejarat, 19. lakas, Triaditza kerület, 1408 Szofia, Bulgaria - privacy@nevumo.com",
        "is": "Abyrgdaradili: \"PHILIPS CENTRE BULGARIA\" ehf. (vorumerki Nevumo) - EIK: 175369610 - 77 Petko Karavelov Blvd., inngangur A, ibuд 19, Triaditza-hverfi, 1408 Sofia, Bulgaría - privacy@nevumo.com",
        "it": "Titolare del trattamento: \"PHILIPS CENTRE BULGARIA\" S.r.l. (marchio commerciale Nevumo) - EIK: 175369610 - 77 Petko Karavelov Blvd., ingresso A, app. 19, quartiere Triaditza, 1408 Sofia, Bulgaria - privacy@nevumo.com",
        "lb": "Verantwortlechen: \"PHILIPS CENTRE BULGARIA\" GmbH (Handelsbrand Nevumo) - EIK: 175369610 - 77 Petko Karavelov Blvd., Agreen A, App. 19, Triaditza-Quartier, 1408 Sofia, Bulgarien - privacy@nevumo.com",
        "lt": "Duomenu valdytojas: \"PHILIPS CENTRE BULGARIA\" UAB (preke zenklas Nevumo) - EIK: 175369610 - Petko Karavelov g. 77, A iejimas, 19 butas, Triadicos rajonas, 1408 Sofija, Bulgarija - privacy@nevumo.com",
        "lv": "Parzinis: \"PHILIPS CENTRE BULGARIA\" SIA (tirdzniecibas zime Nevumo) - EIK: 175369610 - Petko Karavelov bulv. 77, ieeja A, 19. dzivoklis, Triaditzas rajons, 1408 Sofija, Bulgarija - privacy@nevumo.com",
        "mk": "Administrator: \"PHILIPS CENTRE BULGARIA\" DOO (targhovska marka Nevumo) - EIK: 175369610 - bul. Petko Karavelov 77, vl. A, st. 19, r-n Trijadica, 1408 Sofija, Bugarija - privacy@nevumo.com",
        "mt": "Kontrollur: \"PHILIPS CENTRE BULGARIA\" Ltd. (marka kummercjali Nevumo) - EIK: 175369610 - 77 Petko Karavelov Blvd., Dahla A, App. 19, Distrett Triaditza, 1408 Sofia, il-Bulgarija - privacy@nevumo.com",
        "nl": "Verwerkingsverantwoordelijke: \"PHILIPS CENTRE BULGARIA\" BV (handelsmerk Nevumo) - EIK: 175369610 - 77 Petko Karavelov Blvd., ingang A, app. 19, wijk Triaditza, 1408 Sofia, Bulgarije - privacy@nevumo.com",
        "no": "Behandlingsansvarlig: \"PHILIPS CENTRE BULGARIA\" AS (varemerke Nevumo) - EIK: 175369610 - 77 Petko Karavelov Blvd., inngang A, leil. 19, Triaditza-bydel, 1408 Sofia, Bulgaria - privacy@nevumo.com",
        "pl": "Administrator: \"PHILIPS CENTRE BULGARIA\" sp. z o.o. (marka handlowa Nevumo) - EIK: 175369610 - 77 Petko Karavelov Blvd., wejscie A, mieszk. 19, dzielnica Triaditza, 1408 Sofia, Bulgaria - privacy@nevumo.com",
        "pt": "Responsavel: \"PHILIPS CENTRE BULGARIA\" Ltda. (marca comercial Nevumo) - EIK: 175369610 - 77 Petko Karavelov Blvd., Entrada A, Apto. 19, Bairro Triaditza, 1408 Sofia, Bulgaria - privacy@nevumo.com",
        "pt-PT": "Responsavel: \"PHILIPS CENTRE BULGARIA\" Lda. (marca comercial Nevumo) - EIK: 175369610 - 77 Petko Karavelov Blvd., Entrada A, Apto. 19, Bairro Triaditza, 1408 Sofia, Bulgaria - privacy@nevumo.com",
        "ro": "Operator: \"PHILIPS CENTRE BULGARIA\" SRL (marca comerciala Nevumo) - EIK: 175369610 - 77 Petko Karavelov Blvd., intrarea A, ap. 19, cartierul Triaditza, 1408 Sofia, Bulgaria - privacy@nevumo.com",
        "ru": "Operator dannykh: \"PHILIPS CENTRE BULGARIA\" OOO (torgovaya marka Nevumo) - EIK: 175369610 - bul. Petko Karavelov 77, vkh. A, kv. 19, r-n Triadica, 1408 Sofiya, Bolgariya - privacy@nevumo.com",
        "sk": "Prevadzkovatel: \"PHILIPS CENTRE BULGARIA\" s.r.o. (obchodna znacka Nevumo) - EIK: 175369610 - 77 Petko Karavelov Blvd., vchod A, byt 19, stvrt Triaditza, 1408 Sofia, Bulharsko - privacy@nevumo.com",
        "sl": "Upravljavec: \"PHILIPS CENTRE BULGARIA\" d.o.o. (blagovna znamka Nevumo) - EIK: 175369610 - 77 Petko Karavelov Blvd., vhod A, stan 19, cetrt Triaditza, 1408 Sofija, Bolgarija - privacy@nevumo.com",
        "sq": "Kontrollues: \"PHILIPS CENTRE BULGARIA\" Sh.p.k. (marke tregtare Nevumo) - EIK: 175369610 - 77 Petko Karavelov Blvd., Hyrja A, Ap. 19, Lagja Triaditza, 1408 Sofia, Bullgari - privacy@nevumo.com",
        "sr": "Rukovalac: \"PHILIPS CENTRE BULGARIA\" d.o.o. (trgovacka marka Nevumo) - EIK: 175369610 - bul. Petko Karavelov 77, ul. A, st. 19, cet. Trijadica, 1408 Sofija, Bugarska - privacy@nevumo.com",
        "sv": "Personuppgiftsansvarig: \"PHILIPS CENTRE BULGARIA\" AB (varumarke Nevumo) - EIK: 175369610 - 77 Petko Karavelov Blvd., ingang A, lgh. 19, stadsdelen Triaditza, 1408 Sofia, Bulgarien - privacy@nevumo.com",
        "tr": "Veri Sorumlusu: \"PHILIPS CENTRE BULGARIA\" Ltd. Sti. (ticari marka Nevumo) - EIK: 175369610 - 77 Petko Karavelov Blvd., Giris A, Daire 19, Triaditza Bolgesi, 1408 Sofya, Bulgaristan - privacy@nevumo.com",
        "uk": "Kontroler danykh: \"PHILIPS CENTRE BULGARIA\" TOV (torgova marka Nevumo) - EIK: 175369610 - bul. Petko Karavelov 77, vkh. A, kv. 19, r-n Triadytsia, 1408 Sofiya, Bolhariya - privacy@nevumo.com",
    },
}


def seed():
    with engine.begin() as conn:
        for key, translations in TRANSLATIONS.items():
            for lang, value in translations.items():
                conn.execute(
                    text("""
                        INSERT INTO translations (key, lang, value)
                        VALUES (:key, :lang, :value)
                        ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
                    """),
                    {"key": key, "lang": lang, "value": value},
                )
    print(f"Seeded {len(TRANSLATIONS)} keys x 34 languages")


if __name__ == "__main__":
    seed()