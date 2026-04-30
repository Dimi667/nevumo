#!/usr/bin/env python3
"""
Seed script for widget relative time translations (8 keys in widget namespace)
Run: python scripts/seed_widget_relative_time.py
"""
import os
import psycopg2

TRANSLATIONS = {
    "bg": {
        "widget.time_just_now": "току-що",
        "widget.time_min_ago_one": "преди минута",
        "widget.time_min_ago_many": "преди {count} мин",
        "widget.time_hour_ago_many": "преди {count} ч",
        "widget.time_day_ago_one": "преди 1 ден",
        "widget.time_day_ago_many": "преди {count} дни",
        "widget.time_week_ago_many": "преди {count} седмици",
        "widget.time_month_ago_many": "преди {count} месеца",
    },
    "en": {
        "widget.time_just_now": "just now",
        "widget.time_min_ago_one": "1m ago",
        "widget.time_min_ago_many": "{count}m ago",
        "widget.time_hour_ago_many": "{count}h ago",
        "widget.time_day_ago_one": "1 day ago",
        "widget.time_day_ago_many": "{count} days ago",
        "widget.time_week_ago_many": "{count}w ago",
        "widget.time_month_ago_many": "{count}mo ago",
    },
    "de": {
        "widget.time_just_now": "gerade eben",
        "widget.time_min_ago_one": "vor 1 Min.",
        "widget.time_min_ago_many": "vor {count} Min.",
        "widget.time_hour_ago_many": "vor {count} Std.",
        "widget.time_day_ago_one": "vor 1 Tag",
        "widget.time_day_ago_many": "vor {count} Tagen",
        "widget.time_week_ago_many": "vor {count} Wochen",
        "widget.time_month_ago_many": "vor {count} Monaten",
    },
    "fr": {
        "widget.time_just_now": "à l'instant",
        "widget.time_min_ago_one": "il y a 1 min",
        "widget.time_min_ago_many": "il y a {count} min",
        "widget.time_hour_ago_many": "il y a {count} h",
        "widget.time_day_ago_one": "il y a 1 jour",
        "widget.time_day_ago_many": "il y a {count} jours",
        "widget.time_week_ago_many": "il y a {count} sem",
        "widget.time_month_ago_many": "il y a {count} mois",
    },
    "it": {
        "widget.time_just_now": "proprio ora",
        "widget.time_min_ago_one": "1 min fa",
        "widget.time_min_ago_many": "{count} min fa",
        "widget.time_hour_ago_many": "{count} ore fa",
        "widget.time_day_ago_one": "1 giorno fa",
        "widget.time_day_ago_many": "{count} giorni fa",
        "widget.time_week_ago_many": "{count} sett fa",
        "widget.time_month_ago_many": "{count} mesi fa",
    },
    "es": {
        "widget.time_just_now": "ahora mismo",
        "widget.time_min_ago_one": "hace 1 min",
        "widget.time_min_ago_many": "hace {count} min",
        "widget.time_hour_ago_many": "hace {count} h",
        "widget.time_day_ago_one": "hace 1 día",
        "widget.time_day_ago_many": "hace {count} días",
        "widget.time_week_ago_many": "hace {count} sem",
        "widget.time_month_ago_many": "hace {count} meses",
    },
    "sr": {
        "widget.time_just_now": "управо сада",
        "widget.time_min_ago_one": "пре 1 минут",
        "widget.time_min_ago_many": "пре {count} мин",
        "widget.time_hour_ago_many": "пре {count} ч",
        "widget.time_day_ago_one": "пре 1 дан",
        "widget.time_day_ago_many": "пре {count} дана",
        "widget.time_week_ago_many": "пре {count} недеља",
        "widget.time_month_ago_many": "пре {count} месеци",
    },
    "mk": {
        "widget.time_just_now": "тукушто",
        "widget.time_min_ago_one": "пред 1 минута",
        "widget.time_min_ago_many": "пред {count} мин",
        "widget.time_hour_ago_many": "пред {count} ч",
        "widget.time_day_ago_one": "пред 1 ден",
        "widget.time_day_ago_many": "пред {count} дена",
        "widget.time_week_ago_many": "пред {count} недели",
        "widget.time_month_ago_many": "пред {count} месеци",
    },
    "tr": {
        "widget.time_just_now": "az önce",
        "widget.time_min_ago_one": "1 dk önce",
        "widget.time_min_ago_many": "{count} dk önce",
        "widget.time_hour_ago_many": "{count} sa önce",
        "widget.time_day_ago_one": "1 gün önce",
        "widget.time_day_ago_many": "{count} gün önce",
        "widget.time_week_ago_many": "{count} hf önce",
        "widget.time_month_ago_many": "{count} ay önce",
    },
    "ru": {
        "widget.time_just_now": "только что",
        "widget.time_min_ago_one": "1 мин. назад",
        "widget.time_min_ago_many": "{count} мин. назад",
        "widget.time_hour_ago_many": "{count} ч. назад",
        "widget.time_day_ago_one": "1 день назад",
        "widget.time_day_ago_many": "{count} дн. назад",
        "widget.time_week_ago_many": "{count} нед. назад",
        "widget.time_month_ago_many": "{count} мес. назад",
    },
    "pl": {
        "widget.time_just_now": "przed chwilą",
        "widget.time_min_ago_one": "1 min temu",
        "widget.time_min_ago_many": "{count} min temu",
        "widget.time_hour_ago_many": "{count} godz. temu",
        "widget.time_day_ago_one": "1 dzień temu",
        "widget.time_day_ago_many": "{count} dni temu",
        "widget.time_week_ago_many": "{count} tyg. temu",
        "widget.time_month_ago_many": "{count} mies. temu",
    },
    "cs": {
        "widget.time_just_now": "právě teď",
        "widget.time_min_ago_one": "před minutou",
        "widget.time_min_ago_many": "před {count} min",
        "widget.time_hour_ago_many": "před {count} h",
        "widget.time_day_ago_one": "před 1 dnem",
        "widget.time_day_ago_many": "před {count} dny",
        "widget.time_week_ago_many": "před {count} týdny",
        "widget.time_month_ago_many": "před {count} měsíci",
    },
    "sk": {
        "widget.time_just_now": "práve teraz",
        "widget.time_min_ago_one": "pred minútou",
        "widget.time_min_ago_many": "pred {count} min",
        "widget.time_hour_ago_many": "pred {count} h",
        "widget.time_day_ago_one": "pred 1 dňom",
        "widget.time_day_ago_many": "pred {count} dňami",
        "widget.time_week_ago_many": "pred {count} týždňami",
        "widget.time_month_ago_many": "pred {count} mesiacmi",
    },
    "hu": {
        "widget.time_just_now": "éppen most",
        "widget.time_min_ago_one": "1 perce",
        "widget.time_min_ago_many": "{count} perce",
        "widget.time_hour_ago_many": "{count} órája",
        "widget.time_day_ago_one": "1 napja",
        "widget.time_day_ago_many": "{count} napja",
        "widget.time_week_ago_many": "{count} hete",
        "widget.time_month_ago_many": "{count} hónapja",
    },
    "ro": {
        "widget.time_just_now": "chiar acum",
        "widget.time_min_ago_one": "acum 1 min",
        "widget.time_min_ago_many": "acum {count} min",
        "widget.time_hour_ago_many": "acum {count} ore",
        "widget.time_day_ago_one": "acum 1 zi",
        "widget.time_day_ago_many": "acum {count} zile",
        "widget.time_week_ago_many": "acum {count} săpt",
        "widget.time_month_ago_many": "acum {count} luni",
    },
    "uk": {
        "widget.time_just_now": "щойно",
        "widget.time_min_ago_one": "1 хв. тому",
        "widget.time_min_ago_many": "{count} хв. тому",
        "widget.time_hour_ago_many": "{count} год. тому",
        "widget.time_day_ago_one": "1 день тому",
        "widget.time_day_ago_many": "{count} дн. тому",
        "widget.time_week_ago_many": "{count} тиж. тому",
        "widget.time_month_ago_many": "{count} міс. тому",
    },
    "nl": {
        "widget.time_just_now": "zojuist",
        "widget.time_min_ago_one": "1 min geleden",
        "widget.time_min_ago_many": "{count} min geleden",
        "widget.time_hour_ago_many": "{count} uur geleden",
        "widget.time_day_ago_one": "1 dag geleden",
        "widget.time_day_ago_many": "{count} dagen geleden",
        "widget.time_week_ago_many": "{count} w geleden",
        "widget.time_month_ago_many": "{count} mnd geleden",
    },
    "da": {
        "widget.time_just_now": "lige nu",
        "widget.time_min_ago_one": "1 min siden",
        "widget.time_min_ago_many": "{count} min siden",
        "widget.time_hour_ago_many": "{count} t siden",
        "widget.time_day_ago_one": "1 dag siden",
        "widget.time_day_ago_many": "{count} dage siden",
        "widget.time_week_ago_many": "{count} uger siden",
        "widget.time_month_ago_many": "{count} mdr siden",
    },
    "no": {
        "widget.time_just_now": "akkurat nå",
        "widget.time_min_ago_one": "1 min siden",
        "widget.time_min_ago_many": "{count} min siden",
        "widget.time_hour_ago_many": "{count} t siden",
        "widget.time_day_ago_one": "1 dag siden",
        "widget.time_day_ago_many": "{count} dager siden",
        "widget.time_week_ago_many": "{count} uker siden",
        "widget.time_month_ago_many": "{count} mnd siden",
    },
    "sv": {
        "widget.time_just_now": "just nu",
        "widget.time_min_ago_one": "1 min sedan",
        "widget.time_min_ago_many": "{count} min sedan",
        "widget.time_hour_ago_many": "{count} tim sedan",
        "widget.time_day_ago_one": "1 dag sedan",
        "widget.time_day_ago_many": "{count} dagar sedan",
        "widget.time_week_ago_many": "{count} v sedan",
        "widget.time_month_ago_many": "{count} mån sedan",
    },
    "fi": {
        "widget.time_just_now": "juuri nyt",
        "widget.time_min_ago_one": "1 min sitten",
        "widget.time_min_ago_many": "{count} min sitten",
        "widget.time_hour_ago_many": "{count} t sitten",
        "widget.time_day_ago_one": "1 päivä sitten",
        "widget.time_day_ago_many": "{count} päivää sitten",
        "widget.time_week_ago_many": "{count} vk sitten",
        "widget.time_month_ago_many": "{count} kk sitten",
    },
    "el": {
        "widget.time_just_now": "μόλις τώρα",
        "widget.time_min_ago_one": "πριν 1 λεπτό",
        "widget.time_min_ago_many": "πριν {count} λεπτά",
        "widget.time_hour_ago_many": "πριν {count} ώρες",
        "widget.time_day_ago_one": "πριν 1 ημέρα",
        "widget.time_day_ago_many": "πριν {count} ημέρες",
        "widget.time_week_ago_many": "πριν {count} εβδ.",
        "widget.time_month_ago_many": "πριν {count} μήνες",
    },
    "pt": {
        "widget.time_just_now": "agora mesmo",
        "widget.time_min_ago_one": "há 1 min",
        "widget.time_min_ago_many": "há {count} min",
        "widget.time_hour_ago_many": "há {count} h",
        "widget.time_day_ago_one": "há 1 dia",
        "widget.time_day_ago_many": "há {count} dias",
        "widget.time_week_ago_many": "há {count} sem",
        "widget.time_month_ago_many": "há {count} meses",
    },
    "pt-PT": {
        "widget.time_just_now": "agora mesmo",
        "widget.time_min_ago_one": "há 1 min",
        "widget.time_min_ago_many": "há {count} min",
        "widget.time_hour_ago_many": "há {count} h",
        "widget.time_day_ago_one": "há 1 dia",
        "widget.time_day_ago_many": "há {count} dias",
        "widget.time_week_ago_many": "há {count} sem",
        "widget.time_month_ago_many": "há {count} meses",
    },
    "et": {
        "widget.time_just_now": "just nüüd",
        "widget.time_min_ago_one": "1 min tagasi",
        "widget.time_min_ago_many": "{count} min tagasi",
        "widget.time_hour_ago_many": "{count} t tagasi",
        "widget.time_day_ago_one": "1 päev tagasi",
        "widget.time_day_ago_many": "{count} päeva tagasi",
        "widget.time_week_ago_many": "{count} näd tagasi",
        "widget.time_month_ago_many": "{count} kuu tagasi",
    },
    "lv": {
        "widget.time_just_now": "tikko",
        "widget.time_min_ago_one": "pirms 1 min",
        "widget.time_min_ago_many": "pirms {count} min",
        "widget.time_hour_ago_many": "pirms {count} st",
        "widget.time_day_ago_one": "pirms 1 dienas",
        "widget.time_day_ago_many": "pirms {count} dienām",
        "widget.time_week_ago_many": "pirms {count} ned",
        "widget.time_month_ago_many": "pirms {count} mēn",
    },
    "lt": {
        "widget.time_just_now": "ką tik",
        "widget.time_min_ago_one": "prieš 1 min",
        "widget.time_min_ago_many": "prieš {count} min",
        "widget.time_hour_ago_many": "prieš {count} val",
        "widget.time_day_ago_one": "prieš 1 d.",
        "widget.time_day_ago_many": "prieš {count} d.",
        "widget.time_week_ago_many": "prieš {count} sav",
        "widget.time_month_ago_many": "prieš {count} mėn",
    },
    "sl": {
        "widget.time_just_now": "ravnokar",
        "widget.time_min_ago_one": "pred 1 min",
        "widget.time_min_ago_many": "pred {count} min",
        "widget.time_hour_ago_many": "pred {count} h",
        "widget.time_day_ago_one": "pred 1 dnem",
        "widget.time_day_ago_many": "pred {count} dnevi",
        "widget.time_week_ago_many": "pred {count} tedni",
        "widget.time_month_ago_many": "pred {count} meseci",
    },
    "hr": {
        "widget.time_just_now": "upravo sada",
        "widget.time_min_ago_one": "prije 1 min",
        "widget.time_min_ago_many": "prije {count} min",
        "widget.time_hour_ago_many": "prije {count} h",
        "widget.time_day_ago_one": "prije 1 dan",
        "widget.time_day_ago_many": "prije {count} dana",
        "widget.time_week_ago_many": "prije {count} tjedna",
        "widget.time_month_ago_many": "prije {count} mjeseci",
    },
    "sq": {
        "widget.time_just_now": "tani",
        "widget.time_min_ago_one": "1 min më parë",
        "widget.time_min_ago_many": "{count} min më parë",
        "widget.time_hour_ago_many": "{count} orë më parë",
        "widget.time_day_ago_one": "1 ditë më parë",
        "widget.time_day_ago_many": "{count} ditë më parë",
        "widget.time_week_ago_many": "{count} javë më parë",
        "widget.time_month_ago_many": "{count} muaj më parë",
    },
    "is": {
        "widget.time_just_now": "rétt í þessu",
        "widget.time_min_ago_one": "fyrir 1 mín",
        "widget.time_min_ago_many": "fyrir {count} mín",
        "widget.time_hour_ago_many": "fyrir {count} klst",
        "widget.time_day_ago_one": "fyrir 1 degi",
        "widget.time_day_ago_many": "fyrir {count} dögum",
        "widget.time_week_ago_many": "fyrir {count} vikum",
        "widget.time_month_ago_many": "fyrir {count} mánuðum",
    },
    "ga": {
        "widget.time_just_now": "díreach anois",
        "widget.time_min_ago_one": "1 nóim ó shin",
        "widget.time_min_ago_many": "{count} nóim ó shin",
        "widget.time_hour_ago_many": "{count} uair ó shin",
        "widget.time_day_ago_one": "1 lá ó shin",
        "widget.time_day_ago_many": "{count} lá ó shin",
        "widget.time_week_ago_many": "{count} seacht ó shin",
        "widget.time_month_ago_many": "{count} mí ó shin",
    },
    "mt": {
        "widget.time_just_now": "issa f'dan il-mument",
        "widget.time_min_ago_one": "minuta ilu",
        "widget.time_min_ago_many": "{count} minuti ilu",
        "widget.time_hour_ago_many": "{count} sigħat ilu",
        "widget.time_day_ago_one": "ġurnata ilu",
        "widget.time_day_ago_many": "{count} ġranet ilu",
        "widget.time_week_ago_many": "{count} ġimgħat ilu",
        "widget.time_month_ago_many": "{count} xhur ilu",
    },
    "lb": {
        "widget.time_just_now": "just elo",
        "widget.time_min_ago_one": "virun 1 Min",
        "widget.time_min_ago_many": "virun {count} Min",
        "widget.time_hour_ago_many": "virun {count} St",
        "widget.time_day_ago_one": "virun 1 Dag",
        "widget.time_day_ago_many": "virun {count} Deeg",
        "widget.time_week_ago_many": "virun {count} Wochen",
        "widget.time_month_ago_many": "virun {count} Méint",
    },
}


def main():
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("ERROR: DATABASE_URL environment variable not set")
        return

    print("Seeding widget relative time translations...")

    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    count = 0

    for lang, keys in TRANSLATIONS.items():
        for key, value in keys.items():
            cur.execute("""
                INSERT INTO translations (lang, key, value)
                VALUES (%s, %s, %s)
                ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
            """, (lang, key, value))
            count += 1

    conn.commit()
    cur.close()
    conn.close()

    print(f"Seeded widget relative time translations: {count} rows")


if __name__ == '__main__':
    main()
