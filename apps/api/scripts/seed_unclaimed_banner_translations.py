#!/usr/bin/env python3
"""Seed provider_page namespace unclaimed banner translations into the translations table."""

import os
import psycopg2
from psycopg2.extras import execute_values

# Database connection string
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://nevumo:nevumo@localhost:5433/nevumo_leads")

# Translations: language -> dict of keys
TRANSLATIONS = {
    "bg": {
        "unclaimed_banner_title": "Ваша ли е тази фирма?",
        "unclaimed_banner_subtitle": "Вземете безплатния си профил за {businessName}",
        "unclaimed_banner_desc": "{count} Клиенти търсят {category} в {city}. Не ги изпускай!",
        "unclaimed_banner_cta": "Вземи профила безплатно →",
        "unclaimed_banner_trust": "Без ангажимент • Отнема 2 минути",
    },
    "cs": {
        "unclaimed_banner_title": "Je to vaše firma?",
        "unclaimed_banner_subtitle": "Převezměte bezplatný profil pro {businessName}",
        "unclaimed_banner_desc": "{count} Zákazníků hledá {category} v {city}. Nenechte je ujít!",
        "unclaimed_banner_cta": "Převzít profil zdarma →",
        "unclaimed_banner_trust": "Bez závazků • Zabere 2 minuty",
    },
    "da": {
        "unclaimed_banner_title": "Er det din virksomhed?",
        "unclaimed_banner_subtitle": "Overtag din gratis profil for {businessName}",
        "unclaimed_banner_desc": "{count} Kunder søger {category} i {city}. Gå ikke glip af dem!",
        "unclaimed_banner_cta": "Overtag profilen gratis →",
        "unclaimed_banner_trust": "Ingen forpligtelse • Tager 2 minutter",
    },
    "de": {
        "unclaimed_banner_title": "Ist das Ihr Unternehmen?",
        "unclaimed_banner_subtitle": "Übernehmen Sie Ihr kostenloses Profil für {businessName}",
        "unclaimed_banner_desc": "{count} Kunden suchen {category} in {city}. Lassen Sie sie nicht entgehen!",
        "unclaimed_banner_cta": "Profil kostenlos übernehmen →",
        "unclaimed_banner_trust": "Keine Verpflichtung • Dauert 2 Minuten",
    },
    "el": {
        "unclaimed_banner_title": "Είναι η επιχείρησή σας;",
        "unclaimed_banner_subtitle": "Αποκτήστε το δωρεάν προφίλ σας για {businessName}",
        "unclaimed_banner_desc": "{count} Πελάτες αναζητούν {category} στην {city}. Μην τους χάσετε!",
        "unclaimed_banner_cta": "Αποκτήστε το προφίλ δωρεάν →",
        "unclaimed_banner_trust": "Χωρίς δέσμευση • 2 λεπτά",
    },
    "en": {
        "unclaimed_banner_title": "Is this your business?",
        "unclaimed_banner_subtitle": "Claim your free profile for {businessName}",
        "unclaimed_banner_desc": "{count} Clients are looking for {category} in {city}. Don't miss out!",
        "unclaimed_banner_cta": "Claim your profile for free →",
        "unclaimed_banner_trust": "No commitment • Takes 2 minutes",
    },
    "es": {
        "unclaimed_banner_title": "¿Es esta su empresa?",
        "unclaimed_banner_subtitle": "Reclame su perfil gratuito para {businessName}",
        "unclaimed_banner_desc": "{count} Clientes buscan {category} en {city}. ¡No los deje escapar!",
        "unclaimed_banner_cta": "Reclamar perfil gratis →",
        "unclaimed_banner_trust": "Sin compromiso • Tarda 2 minutos",
    },
    "et": {
        "unclaimed_banner_title": "Kas see on teie ettevõte?",
        "unclaimed_banner_subtitle": "Haarake oma tasuta profiil ettevõttele {businessName}",
        "unclaimed_banner_desc": "{count} Klienti otsivad {category} linnas {city}. Ärge jätke neid maha!",
        "unclaimed_banner_cta": "Haarake profiil tasuta →",
        "unclaimed_banner_trust": "Ilma kohustuseta • Võtab 2 minutit",
    },
    "fi": {
        "unclaimed_banner_title": "Onko tämä yrityksesi?",
        "unclaimed_banner_subtitle": "Lunasta ilmainen profiilisi yritykselle {businessName}",
        "unclaimed_banner_desc": "{count} Asiakasta etsii {category} kaupungissa {city}. Älä anna heidän mennä!",
        "unclaimed_banner_cta": "Lunasta profiili ilmaiseksi →",
        "unclaimed_banner_trust": "Ei sitoutumista • Kestää 2 minuuttia",
    },
    "fr": {
        "unclaimed_banner_title": "C'est votre entreprise ?",
        "unclaimed_banner_subtitle": "Réclamez votre profil gratuit pour {businessName}",
        "unclaimed_banner_desc": "{count} Clients recherchent {category} à {city}. Ne les laissez pas partir !",
        "unclaimed_banner_cta": "Réclamer le profil gratuitement →",
        "unclaimed_banner_trust": "Sans engagement • 2 minutes suffisent",
    },
    "ga": {
        "unclaimed_banner_title": "An é seo do ghnólacht?",
        "unclaimed_banner_subtitle": "Éiligh do phróifíl saor in aisce do {businessName}",
        "unclaimed_banner_desc": "Tá {count} Cliant ag lorg {category} i {city}. Ná lig dóibh dul!",
        "unclaimed_banner_cta": "Éiligh an próifíl saor in aisce →",
        "unclaimed_banner_trust": "Gan gealltanas • 2 nóiméad",
    },
    "hr": {
        "unclaimed_banner_title": "Je li ovo vaša tvrtka?",
        "unclaimed_banner_subtitle": "Preuzmite besplatni profil za {businessName}",
        "unclaimed_banner_desc": "{count} Klijenata traži {category} u {city}. Ne propustite ih!",
        "unclaimed_banner_cta": "Preuzmi profil besplatno →",
        "unclaimed_banner_trust": "Bez obveza • Traje 2 minute",
    },
    "hu": {
        "unclaimed_banner_title": "Ez az Ön vállalkozása?",
        "unclaimed_banner_subtitle": "Igényelje ingyenes profilját a(z) {businessName} számára",
        "unclaimed_banner_desc": "{count} Ügyfél keres {category} szolgáltatót {city} városában. Ne hagyja elmenni őket!",
        "unclaimed_banner_cta": "Profil igénylése ingyenesen →",
        "unclaimed_banner_trust": "Kötelezettség nélkül • 2 perc",
    },
    "is": {
        "unclaimed_banner_title": "Er þetta fyrirtæki þitt?",
        "unclaimed_banner_subtitle": "Taktu yfir ókeypis prófílinn þinn fyrir {businessName}",
        "unclaimed_banner_desc": "{count} Viðskiptavinir leita að {category} í {city}. Ekki missa þá af!",
        "unclaimed_banner_cta": "Taktu yfir prófílinn ókeypis →",
        "unclaimed_banner_trust": "Engar skuldbindingar • Tekur 2 mínútur",
    },
    "it": {
        "unclaimed_banner_title": "È la sua azienda?",
        "unclaimed_banner_subtitle": "Rivendica il tuo profilo gratuito per {businessName}",
        "unclaimed_banner_desc": "{count} Clienti cercano {category} a {city}. Non lasciarli scappare!",
        "unclaimed_banner_cta": "Rivendica il profilo gratis →",
        "unclaimed_banner_trust": "Nessun impegno • Ci vogliono 2 minuti",
    },
    "lb": {
        "unclaimed_banner_title": "Ass dat Äert Betrib?",
        "unclaimed_banner_subtitle": "Huelt Äre gratis Profil fir {businessName}",
        "unclaimed_banner_desc": "{count} Clienten sichen {category} zu {city}. Loosst se net fortgoen!",
        "unclaimed_banner_cta": "Profil gratis huelen →",
        "unclaimed_banner_trust": "Keng Verpflichtung • 2 Minutten",
    },
    "lt": {
        "unclaimed_banner_title": "Ar tai jūsų įmonė?",
        "unclaimed_banner_subtitle": "Perimkite nemokamą profilį {businessName}",
        "unclaimed_banner_desc": "{count} Klientų ieško {category} mieste {city}. Nepraleiskite jų!",
        "unclaimed_banner_cta": "Perimti profilį nemokamai →",
        "unclaimed_banner_trust": "Be įsipareigojimų • Užtrunka 2 minutes",
    },
    "lv": {
        "unclaimed_banner_title": "Vai šis ir jūsu uzņēmums?",
        "unclaimed_banner_subtitle": "Pārņemiet bezmaksas profilu uzņēmumam {businessName}",
        "unclaimed_banner_desc": "{count} Klienti meklē {category} pilsētā {city}. Nepalaidiet tos garām!",
        "unclaimed_banner_cta": "Pārņemt profilu bez maksas →",
        "unclaimed_banner_trust": "Bez saistībām • Aizņem 2 minūtes",
    },
    "mk": {
        "unclaimed_banner_title": "Ова ли е вашата фирма?",
        "unclaimed_banner_subtitle": "Земете го бесплатниот профил за {businessName}",
        "unclaimed_banner_desc": "{count} Клиенти бараат {category} во {city}. Не ги испуштајте!",
        "unclaimed_banner_cta": "Земи го профилот бесплатно →",
        "unclaimed_banner_trust": "Без обврски • Трае 2 минути",
    },
    "mt": {
        "unclaimed_banner_title": "Din hija l-kumpanija tiegħek?",
        "unclaimed_banner_subtitle": "Ħu l-profil b'xejn tiegħek għal {businessName}",
        "unclaimed_banner_desc": "{count} Klijenti qed ifittxu {category} f'{city}. Tħallihomx imorru!",
        "unclaimed_banner_cta": "Ħu l-profil b'xejn →",
        "unclaimed_banner_trust": "Mingħajr impenn • 2 minuti",
    },
    "nl": {
        "unclaimed_banner_title": "Is dit uw bedrijf?",
        "unclaimed_banner_subtitle": "Claim uw gratis profiel voor {businessName}",
        "unclaimed_banner_desc": "{count} Klanten zoeken {category} in {city}. Laat ze niet weggaan!",
        "unclaimed_banner_cta": "Profiel gratis claimen →",
        "unclaimed_banner_trust": "Geen verplichting • Duurt 2 minuten",
    },
    "no": {
        "unclaimed_banner_title": "Er dette din bedrift?",
        "unclaimed_banner_subtitle": "Overta din gratis profil for {businessName}",
        "unclaimed_banner_desc": "{count} Kunder søker {category} i {city}. Ikke la dem gå!",
        "unclaimed_banner_cta": "Overta profilen gratis →",
        "unclaimed_banner_trust": "Ingen forpliktelse • Tar 2 minutter",
    },
    "pl": {
        "unclaimed_banner_title": "Czy to Twoja firma?",
        "unclaimed_banner_subtitle": "Odbierz bezpłatny profil dla {businessName}",
        "unclaimed_banner_desc": "{count} Klientów szuka {category} w {city}. Nie trać ich!",
        "unclaimed_banner_cta": "Odbierz profil bezpłatnie →",
        "unclaimed_banner_trust": "Bez zobowiązań • Zajmuje 2 minuty",
    },
    "pt": {
        "unclaimed_banner_title": "Esta é a sua empresa?",
        "unclaimed_banner_subtitle": "Reivindique seu perfil gratuito para {businessName}",
        "unclaimed_banner_desc": "{count} Clientes estão procurando {category} em {city}. Não os perca!",
        "unclaimed_banner_cta": "Reivindicar perfil grátis →",
        "unclaimed_banner_trust": "Sem compromisso • Leva 2 minutos",
    },
    "pt-PT": {
        "unclaimed_banner_title": "Esta é a sua empresa?",
        "unclaimed_banner_subtitle": "Reclame o seu perfil gratuito para {businessName}",
        "unclaimed_banner_desc": "{count} Clientes procuram {category} em {city}. Não os deixe escapar!",
        "unclaimed_banner_cta": "Reclamar perfil gratuitamente →",
        "unclaimed_banner_trust": "Sem compromisso • Demora 2 minutos",
    },
    "ro": {
        "unclaimed_banner_title": "Aceasta este compania dvs.?",
        "unclaimed_banner_subtitle": "Revendicați profilul gratuit pentru {businessName}",
        "unclaimed_banner_desc": "{count} Clienți caută {category} în {city}. Nu îi lăsați să plece!",
        "unclaimed_banner_cta": "Revendicați profilul gratuit →",
        "unclaimed_banner_trust": "Fără angajament • Durează 2 minute",
    },
    "ru": {
        "unclaimed_banner_title": "Это ваша компания?",
        "unclaimed_banner_subtitle": "Получите бесплатный профиль для {businessName}",
        "unclaimed_banner_desc": "{count} Клиентов ищут {category} в {city}. Не упустите их!",
        "unclaimed_banner_cta": "Получить профиль бесплатно →",
        "unclaimed_banner_trust": "Без обязательств • Займёт 2 минуты",
    },
    "sk": {
        "unclaimed_banner_title": "Je to vaša firma?",
        "unclaimed_banner_subtitle": "Prevzite bezplatný profil pre {businessName}",
        "unclaimed_banner_desc": "{count} Zákazníkov hľadá {category} v {city}. Nenechajte ich ujsť!",
        "unclaimed_banner_cta": "Prevziať profil bezplatne →",
        "unclaimed_banner_trust": "Bez záväzkov • Trvá 2 minúty",
    },
    "sl": {
        "unclaimed_banner_title": "Je to vaše podjetje?",
        "unclaimed_banner_subtitle": "Prevzemite brezplačni profil za {businessName}",
        "unclaimed_banner_desc": "{count} Strank išče {category} v {city}. Ne zamudite jih!",
        "unclaimed_banner_cta": "Prevzemi profil brezplačno →",
        "unclaimed_banner_trust": "Brez obveznosti • Traja 2 minuti",
    },
    "sq": {
        "unclaimed_banner_title": "Kjo është kompania juaj?",
        "unclaimed_banner_subtitle": "Merrni profilin tuaj falas për {businessName}",
        "unclaimed_banner_desc": "{count} Klientë kërkojnë {category} në {city}. Mos i humbisni!",
        "unclaimed_banner_cta": "Merrni profilin falas →",
        "unclaimed_banner_trust": "Pa angazhim • Zgjat 2 minuta",
    },
    "sr": {
        "unclaimed_banner_title": "Ово ли је ваша фирма?",
        "unclaimed_banner_subtitle": "Преузмите бесплатни профил за {businessName}",
        "unclaimed_banner_desc": "{count} Клијената тражи {category} у {city}. Не пропустите их!",
        "unclaimed_banner_cta": "Преузми профил бесплатно →",
        "unclaimed_banner_trust": "Без обавеза • Траје 2 минута",
    },
    "sv": {
        "unclaimed_banner_title": "Är det ditt företag?",
        "unclaimed_banner_subtitle": "Ta över din kostnadsfria profil för {businessName}",
        "unclaimed_banner_desc": "{count} Kunder söker {category} i {city}. Låt dem inte gå!",
        "unclaimed_banner_cta": "Ta över profilen gratis →",
        "unclaimed_banner_trust": "Ingen förpliktelse • Tar 2 minuter",
    },
    "tr": {
        "unclaimed_banner_title": "Bu sizin işletmeniz mi?",
        "unclaimed_banner_subtitle": "{businessName} için ücretsiz profilinizi alın",
        "unclaimed_banner_desc": "{count} müşteri {city} şehrinde {category} arıyor. Onları kaçırmayın!",
        "unclaimed_banner_cta": "Profili ücretsiz alın →",
        "unclaimed_banner_trust": "Taahhüt yok • 2 dakika",
    },
    "uk": {
        "unclaimed_banner_title": "Це ваша компанія?",
        "unclaimed_banner_subtitle": "Отримайте безкоштовний профіль для {businessName}",
        "unclaimed_banner_desc": "{count} Клієнтів шукають {category} у {city}. Не втрачайте їх!",
        "unclaimed_banner_cta": "Отримати профіль безкоштовно →",
        "unclaimed_banner_trust": "Без зобов'язань • Займе 2 хвилини",
    },
}


def seed_translations():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    rows_to_upsert = []
    total_keys = 0

    for lang, keys_dict in TRANSLATIONS.items():
        for key, value in keys_dict.items():
            full_key = f"provider_page.{key}"
            rows_to_upsert.append((lang, full_key, value))
        print(f"Seeded {lang}: {len(keys_dict)} keys")
        total_keys += len(keys_dict)

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
    print(f"\n✓ Seeded {count} translation rows for provider_page namespace")
