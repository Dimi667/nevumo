"""Upsert login meta translations and clear the related Redis cache."""

from typing import Dict

import redis

from apps.api.database import SessionLocal, init_db
from apps.api.i18n import SUPPORTED_LANGUAGES, upsert_translation_values


LOGIN_META_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "login:metaTitle": {
        "bg": "Nevumo – Намери услуги или започни да предлагаш услуги",
        "cs": "Nevumo – Najdi služby nebo začni nabízet služby",
        "da": "Nevumo – Find tjenester eller begynd at tilbyde tjenester",
        "de": "Nevumo – Finde Dienstleistungen oder biete deine an",
        "el": "Nevumo – Βρες υπηρεσίες ή ξεκίνα να προσφέρεις υπηρεσίες",
        "en": "Nevumo – Find Services or Start Offering Yours",
        "es": "Nevumo – Encuentra servicios o empieza a ofrecer los tuyos",
        "et": "Nevumo – Leia teenuseid või hakka oma teenuseid pakkuma",
        "fi": "Nevumo – Löydä palveluja tai ala tarjota omia",
        "fr": "Nevumo – Trouvez des services ou commencez à proposer les vôtres",
        "ga": "Nevumo – Aimsigh Seirbhísí nó Tosaigh ag Tairiscint Seirbhísí",
        "hr": "Nevumo – Pronađi usluge ili počni nuditi svoje usluge",
        "hu": "Nevumo – Találj szolgáltatásokat vagy kezdj el szolgáltatást nyújtani",
        "it": "Nevumo – Trova servizi o inizia a offrire i tuoi",
        "lt": "Nevumo – Rask paslaugas arba pradėk siūlyti savo paslaugas",
        "lv": "Nevumo – Atrodi pakalpojumus vai sāc piedāvāt savus",
        "mk": "Nevumo – Најди услуги или почни да нудиш услуги",
        "mt": "Nevumo – Sib servizzi jew ibda toffri s-servizzi tiegħek",
        "nl": "Nevumo – Vind diensten of begin met het aanbieden van jouw diensten",
        "no": "Nevumo – Finn tjenester eller begynn å tilby tjenester",
        "pl": "Nevumo – Znajdź usługi lub zacznij oferować swoje",
        "pt": "Nevumo – Encontre serviços ou comece a oferecer os seus",
        "pt-PT": "Nevumo – Encontre serviços ou comece a oferecer os seus",
        "ro": "Nevumo – Găsește servicii sau începe să oferi serviciile tale",
        "sk": "Nevumo – Nájdi služby alebo začni ponúkať svoje služby",
        "sl": "Nevumo – Poišči storitve ali začni ponujati svoje storitve",
        "sq": "Nevumo – Gjej shërbime ose fillo të ofrosh shërbimet e tua",
        "sr": "Nevumo – Пронађи услуге или почни да нудиш услуге",
        "sv": "Nevumo – Hitta tjänster eller börja erbjuda dina tjänster",
        "tr": "Nevumo – Hizmet Bul veya Hizmet Sunmaya Başla",
    },
    "login:metaDescription": {
        "bg": "Открий и резервирай услуги или започни да предлагаш своите в Nevumo. Безплатна регистрация и бърз старт за клиенти и доставчици.",
        "cs": "Objevuj a rezervuj služby nebo začni nabízet své vlastní na Nevumo. Bezplatná registrace a rychlý start pro klienty i poskytovatele.",
        "da": "Opdag og book tjenester eller begynd at tilbyde dine egne på Nevumo. Gratis registrering og hurtig start for kunder og udbydere.",
        "de": "Entdecke und buche Dienstleistungen oder biete deine eigenen auf Nevumo an. Kostenlose Registrierung und schneller Start für Kunden und Anbieter.",
        "el": "Ανακάλυψε και κράτησε υπηρεσίες ή ξεκίνα να προσφέρεις τις δικές σου στο Nevumo. Δωρεάν εγγραφή και γρήγορη εκκίνηση για πελάτες και παρόχους.",
        "en": "Discover and book services or start offering yours on Nevumo. Free registration and quick start for clients and providers.",
        "es": "Descubre y reserva servicios o empieza a ofrecer los tuyos en Nevumo. Registro gratuito e inicio rápido para clientes y proveedores.",
        "et": "Avasta ja broneeri teenuseid või hakka oma teenuseid pakkuma Nevumos. Tasuta registreerimine ja kiire alustamine klientidele ja teenusepakkujatele.",
        "fi": "Löydä ja varaa palveluja tai ala tarjota omiasi Nevumossa. Ilmainen rekisteröityminen ja nopea aloitus asiakkaille ja palveluntarjoajille.",
        "fr": "Découvrez et réservez des services ou commencez à proposer les vôtres sur Nevumo. Inscription gratuite et démarrage rapide pour les clients et les prestataires.",
        "ga": "Aimsigh agus áirigh seirbhísí nó tosaigh ag tairiscint do chuid féin ar Nevumo. Clárú saor in aisce agus tús tapa do chliaint agus soláthróirí.",
        "hr": "Otkrij i rezerviraj usluge ili počni nuditi svoje na Nevumo. Besplatna registracija i brz početak za klijente i pružatelje usluga.",
        "hu": "Fedezz fel és foglalj szolgáltatásokat, vagy kezdj el saját szolgáltatásokat nyújtani a Nevumón. Ingyenes regisztráció és gyors kezdés ügyfeleknek és szolgáltatóknak.",
        "it": "Scopri e prenota servizi o inizia a offrire i tuoi su Nevumo. Registrazione gratuita e avvio rapido per clienti e fornitori.",
        "lt": "Atrask ir rezervuok paslaugas arba pradėk siūlyti savo Nevumo platformoje. Nemokama registracija ir greita pradžia klientams ir paslaugų teikėjams.",
        "lv": "Atklāj un rezervē pakalpojumus vai sāc piedāvāt savus Nevumo. Bezmaksas reģistrācija un ātra sākšana klientiem un pakalpojumu sniedzējiem.",
        "mk": "Откријте и резервирајте услуги или почнете да ги нудите вашите на Nevumo. Бесплатна регистрација и брз старт за клиенти и даватели на услуги.",
        "mt": "Skopri u ibbukkja servizzi jew ibda toffri tiegħek fuq Nevumo. Reġistrazzjoni bla ħlas u bidu rapidu għal klijenti u fornituri.",
        "nl": "Ontdek en boek diensten of begin met het aanbieden van jouw diensten op Nevumo. Gratis registratie en snel aan de slag voor klanten en aanbieders.",
        "no": "Oppdag og bestill tjenester eller begynn å tilby dine egne på Nevumo. Gratis registrering og rask start for kunder og tilbydere.",
        "pl": "Odkryj i rezerwuj usługi lub zacznij oferować swoje na Nevumo. Bezpłatna rejestracja i szybki start dla klientów i dostawców.",
        "pt": "Descubra e reserve serviços ou comece a oferecer os seus no Nevumo. Cadastro gratuito e início rápido para clientes e prestadores.",
        "pt-PT": "Descubra e reserve serviços ou comece a oferecer os seus no Nevumo. Registo gratuito e início rápido para clientes e prestadores.",
        "ro": "Descoperă și rezervă servicii sau începe să oferi serviciile tale pe Nevumo. Înregistrare gratuită și start rapid pentru clienți și furnizori.",
        "sk": "Objavuj a rezervuj služby alebo začni ponúkať svoje na Nevumo. Bezplatná registrácia a rýchly štart pre klientov aj poskytovateľov.",
        "sl": "Odkrij in rezerviraj storitve ali začni ponujati svoje na Nevumo. Brezplačna registracija in hiter začetek za stranke in ponudnike.",
        "sq": "Zbulo dhe rezervo shërbime ose fillo të ofrosh të tuat në Nevumo. Regjistrim falas dhe fillim i shpejtë për klientët dhe ofruesit.",
        "sr": "Откријте и резервишите услуге или почните да нудите своје на Nevumo. Бесплатна регистрација и брз почетак за клијенте и пружаоце услуга.",
        "sv": "Upptäck och boka tjänster eller börja erbjuda dina egna på Nevumo. Gratis registrering och snabb start för kunder och leverantörer.",
        "tr": "Nevumo'da hizmetleri keşfet ve rezerve et veya kendi hizmetlerini sunmaya başla. Müşteriler ve sağlayıcılar için ücretsiz kayıt ve hızlı başlangıç.",
    },
}


def clear_translation_cache() -> None:
    try:
        redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
        redis_client.ping()
    except redis.RedisError:
        return

    for lang in SUPPORTED_LANGUAGES:
        redis_client.delete(f"translations:{lang}")


def main() -> None:
    db = SessionLocal()
    init_db()
    try:
        for key, translations in LOGIN_META_TRANSLATIONS.items():
            upsert_translation_values(db, key, translations)
        db.commit()
    finally:
        db.close()

    clear_translation_cache()


if __name__ == "__main__":
    main()
