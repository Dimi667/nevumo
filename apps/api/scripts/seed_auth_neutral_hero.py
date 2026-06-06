#!/usr/bin/env python3
"""
Seed script for auth neutral hero translation keys.
Adds 3 keys: hero_title_neutral, hero_subtitle_neutral_1, hero_subtitle_neutral_2
for all 34 supported languages in the auth namespace.
"""

import os

from sqlalchemy import text
from apps.api.database import engine
from apps.api.dependencies import get_redis

NAMESPACE = "auth"

# All 34 translations for the 3 keys
TRANSLATIONS = {
    "bg": {
        "hero_title_neutral": "Nevumo работи за теб!",
        "hero_subtitle_neutral_1": "Търсиш услуга или предлагаш услуга — става и в двата случая",
        "hero_subtitle_neutral_2": "Без комисионни!",
    },
    "cs": {
        "hero_title_neutral": "Nevumo pracuje pro tebe!",
        "hero_subtitle_neutral_1": "Hledáš službu nebo ji nabízíš — funguje to v obou případech",
        "hero_subtitle_neutral_2": "Bez provizí!",
    },
    "da": {
        "hero_title_neutral": "Nevumo arbejder for dig!",
        "hero_subtitle_neutral_1": "Søger du en service eller tilbyder du en — det virker begge veje",
        "hero_subtitle_neutral_2": "Uden provision!",
    },
    "de": {
        "hero_title_neutral": "Nevumo arbeitet für dich!",
        "hero_subtitle_neutral_1": "Du suchst eine Dienstleistung oder bietest eine an — funktioniert in beiden Fällen",
        "hero_subtitle_neutral_2": "Ohne Provision!",
    },
    "el": {
        "hero_title_neutral": "Το Nevumo δουλεύει για σένα!",
        "hero_subtitle_neutral_1": "Ψάχνεις υπηρεσία ή προσφέρεις — λειτουργεί και στις δύο περιπτώσεις",
        "hero_subtitle_neutral_2": "Χωρίς προμήθεια!",
    },
    "en": {
        "hero_title_neutral": "Nevumo works for you!",
        "hero_subtitle_neutral_1": "Looking for a service or offering one — it works both ways",
        "hero_subtitle_neutral_2": "No commission!",
    },
    "es": {
        "hero_title_neutral": "¡Nevumo trabaja para ti!",
        "hero_subtitle_neutral_1": "¿Buscas un servicio o lo ofreces? — funciona en ambos casos",
        "hero_subtitle_neutral_2": "¡Sin comisiones!",
    },
    "et": {
        "hero_title_neutral": "Nevumo töötab sinu heaks!",
        "hero_subtitle_neutral_1": "Otsid teenust või pakud seda — toimib mõlemal juhul",
        "hero_subtitle_neutral_2": "Ilma komisjonitasuta!",
    },
    "fi": {
        "hero_title_neutral": "Nevumo toimii sinulle!",
        "hero_subtitle_neutral_1": "Etsitpä palvelua tai tarjoat sitä — toimii molemmilla tavoilla",
        "hero_subtitle_neutral_2": "Ilman provisiota!",
    },
    "fr": {
        "hero_title_neutral": "Nevumo travaille pour vous !",
        "hero_subtitle_neutral_1": "Vous cherchez un service ou en proposez un — ça marche dans les deux cas",
        "hero_subtitle_neutral_2": "Sans commission !",
    },
    "ga": {
        "hero_title_neutral": "Oibríonn Nevumo duit!",
        "hero_subtitle_neutral_1": "An bhfuil seirbhís á lorg agat nó á tairiscint — oibríonn sé ar an dá bhealach",
        "hero_subtitle_neutral_2": "Gan coimisiún!",
    },
    "hr": {
        "hero_title_neutral": "Nevumo radi za tebe!",
        "hero_subtitle_neutral_1": "Tražiš uslugu ili je nudiš — radi u oba slučaja",
        "hero_subtitle_neutral_2": "Bez provizije!",
    },
    "hu": {
        "hero_title_neutral": "A Nevumo dolgozik érted!",
        "hero_subtitle_neutral_1": "Szolgáltatást keresel vagy kínálsz — mindkét esetben működik",
        "hero_subtitle_neutral_2": "Jutalék nélkül!",
    },
    "is": {
        "hero_title_neutral": "Nevumo vinnur fyrir þig!",
        "hero_subtitle_neutral_1": "Ertu að leita að þjónustu eða bjóða upp á hana — virkar í báðum tilvikum",
        "hero_subtitle_neutral_2": "Án þóknunar!",
    },
    "it": {
        "hero_title_neutral": "Nevumo lavora per te!",
        "hero_subtitle_neutral_1": "Cerchi un servizio o ne offri uno — funziona in entrambi i casi",
        "hero_subtitle_neutral_2": "Senza commissioni!",
    },
    "lb": {
        "hero_title_neutral": "Nevumo schafft fir dech!",
        "hero_subtitle_neutral_1": "Du séchs en Déngscht oder bids en un — fonctionnéiert a béide Fäll",
        "hero_subtitle_neutral_2": "Ouni Kommissioun!",
    },
    "lt": {
        "hero_title_neutral": "Nevumo dirba už tave!",
        "hero_subtitle_neutral_1": "Ieškai paslaugos ar ją siūlai — veikia abiem atvejais",
        "hero_subtitle_neutral_2": "Be komisinių!",
    },
    "lv": {
        "hero_title_neutral": "Nevumo strādā tavā labā!",
        "hero_subtitle_neutral_1": "Meklē pakalpojumu vai piedāvā to — darbojas abos gadījumos",
        "hero_subtitle_neutral_2": "Bez komisijas!",
    },
    "mk": {
        "hero_title_neutral": "Nevumo работи за тебе!",
        "hero_subtitle_neutral_1": "Барате услуга или нудите — функционира во двата случаи",
        "hero_subtitle_neutral_2": "Без провизија!",
    },
    "mt": {
        "hero_title_neutral": "Nevumo jaħdem għalik!",
        "hero_subtitle_neutral_1": "Qed tfittex servizz jew toffri wieħed — jaħdem fiż-żewġ każijiet",
        "hero_subtitle_neutral_2": "Mingħajr kummissjoni!",
    },
    "nl": {
        "hero_title_neutral": "Nevumo werkt voor jou!",
        "hero_subtitle_neutral_1": "Op zoek naar een dienst of bied je er een aan — het werkt in beide gevallen",
        "hero_subtitle_neutral_2": "Zonder commissie!",
    },
    "no": {
        "hero_title_neutral": "Nevumo jobber for deg!",
        "hero_subtitle_neutral_1": "Leter du etter en tjeneste eller tilbyr du en — det fungerer begge veier",
        "hero_subtitle_neutral_2": "Uten provisjon!",
    },
    "pl": {
        "hero_title_neutral": "Nevumo działa dla Ciebie!",
        "hero_subtitle_neutral_1": "Szukasz usługi lub ją oferujesz — działa w obu przypadkach",
        "hero_subtitle_neutral_2": "Bez prowizji!",
    },
    "pt": {
        "hero_title_neutral": "Nevumo trabalha por você!",
        "hero_subtitle_neutral_1": "Está procurando um serviço ou oferecendo um — funciona nos dois casos",
        "hero_subtitle_neutral_2": "Sem comissão!",
    },
    "pt-PT": {
        "hero_title_neutral": "Nevumo trabalha para si!",
        "hero_subtitle_neutral_1": "Procura um serviço ou oferece um — funciona nos dois casos",
        "hero_subtitle_neutral_2": "Sem comissão!",
    },
    "ro": {
        "hero_title_neutral": "Nevumo lucrează pentru tine!",
        "hero_subtitle_neutral_1": "Cauți un serviciu sau îl oferi — funcționează în ambele cazuri",
        "hero_subtitle_neutral_2": "Fără comision!",
    },
    "ru": {
        "hero_title_neutral": "Nevumo работает для тебя!",
        "hero_subtitle_neutral_1": "Ищешь услугу или предлагаешь — работает в обоих случаях",
        "hero_subtitle_neutral_2": "Без комиссии!",
    },
    "sk": {
        "hero_title_neutral": "Nevumo pracuje pre teba!",
        "hero_subtitle_neutral_1": "Hľadáš službu alebo ju ponúkaš — funguje v oboch prípadoch",
        "hero_subtitle_neutral_2": "Bez provízií!",
    },
    "sl": {
        "hero_title_neutral": "Nevumo dela za tebe!",
        "hero_subtitle_neutral_1": "Iščeš storitev ali jo ponujaš — deluje v obeh primerih",
        "hero_subtitle_neutral_2": "Brez provizije!",
    },
    "sq": {
        "hero_title_neutral": "Nevumo punon për ty!",
        "hero_subtitle_neutral_1": "Kërkon një shërbim apo ofron një — funksionon në të dy rastet",
        "hero_subtitle_neutral_2": "Pa komision!",
    },
    "sr": {
        "hero_title_neutral": "Nevumo radi za tebe!",
        "hero_subtitle_neutral_1": "Tražiš uslugu ili je nudiš — radi u oba slučaja",
        "hero_subtitle_neutral_2": "Bez provizije!",
    },
    "sv": {
        "hero_title_neutral": "Nevumo jobbar för dig!",
        "hero_subtitle_neutral_1": "Letar du efter en tjänst eller erbjuder du en — fungerar åt båda hållen",
        "hero_subtitle_neutral_2": "Utan provision!",
    },
    "tr": {
        "hero_title_neutral": "Nevumo senin için çalışır!",
        "hero_subtitle_neutral_1": "Hizmet mi arıyorsun yoksa sunuyor musun — her iki durumda da işe yarar",
        "hero_subtitle_neutral_2": "Komisyon yok!",
    },
    "uk": {
        "hero_title_neutral": "Nevumo працює для тебе!",
        "hero_subtitle_neutral_1": "Шукаєш послугу чи пропонуєш — працює в обох випадках",
        "hero_subtitle_neutral_2": "Без комісії!",
    },
}


def main():
    """Main entry point for the seed script."""
    with engine.connect() as conn:
        # Insert translations
        insert_translations(conn)
        
        # Verify count
        for key_name in ["hero_title_neutral", "hero_subtitle_neutral_1", "hero_subtitle_neutral_2"]:
            full_key = f"{NAMESPACE}.{key_name}"
            result = conn.execute(
                text("SELECT COUNT(*) FROM translations WHERE key = :key"),
                {"key": full_key}
            )
            count = result.scalar()
            print(f"✓ '{full_key}': {count} translations in database")
    
    # Clear Redis cache for auth namespace
    try:
        r = get_redis()
        if not r:
            print("✓ Redis not available, skipping cache clear")
            return

        # Delete all keys matching the pattern for auth namespace
        # The key format in translation_service.py is trans:{lang}:{namespace}
        pattern = f"trans:*:{NAMESPACE}"
        keys = list(r.scan_iter(match=pattern))
        if keys:
            r.delete(*keys)
            print(f"✓ Cleared {len(keys)} keys from Redis cache for '{NAMESPACE}' namespace")
        else:
            # Also try the older pattern just in case
            old_pattern = f"i18n:{NAMESPACE}:*"
            old_keys = list(r.scan_iter(match=old_pattern))
            if old_keys:
                r.delete(*old_keys)
                print(f"✓ Cleared {len(old_keys)} legacy keys from Redis cache")
            else:
                print("✓ No Redis keys found to clear")
    except Exception as e:
        print(f"⚠ Could not clear Redis cache: {e}")


def insert_translations(conn) -> None:
    """Insert or update translations in the database."""
    count = 0
    for lang, translations in TRANSLATIONS.items():
        for key_name, value in translations.items():
            full_key = f"{NAMESPACE}.{key_name}"
            conn.execute(
                text("""
                    INSERT INTO translations (lang, key, value)
                    VALUES (:lang, :key, :value)
                    ON CONFLICT (lang, key)
                    DO UPDATE SET value = EXCLUDED.value
                """),
                {"lang": lang, "key": full_key, "value": value}
            )
            count += 1
    conn.commit()
    print(f"Inserted/updated {count} translation rows")


if __name__ == "__main__":
    main()
