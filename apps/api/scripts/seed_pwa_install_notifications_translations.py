#!/usr/bin/env python3
"""
Seed script to add PWA install notification translations for all 34 languages.
Keys: pwa.install_for_notifications_provider, pwa.install_for_notifications_client
"""

import os
from psycopg2.extras import execute_values

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://nevumo:nevumo@nevumo-postgres:5432/nevumo_leads")

TRANSLATIONS = [
    # pwa.install_for_notifications_provider
    ('bg', 'pwa.install_for_notifications_provider', 'Инсталирай приложението за да получаваш известия за нови заявки'),
    ('cs', 'pwa.install_for_notifications_provider', 'Nainstaluj aplikaci a dostávej oznámení o nových poptávkách'),
    ('da', 'pwa.install_for_notifications_provider', 'Installer appen for at modtage notifikationer om nye forespørgsler'),
    ('de', 'pwa.install_for_notifications_provider', 'Installiere die App, um Benachrichtigungen über neue Anfragen zu erhalten'),
    ('el', 'pwa.install_for_notifications_provider', 'Εγκατέστησε την εφαρμογή για να λαμβάνεις ειδοποιήσεις για νέα αιτήματα'),
    ('en', 'pwa.install_for_notifications_provider', 'Install the app to receive notifications for new requests'),
    ('es', 'pwa.install_for_notifications_provider', 'Instala la app para recibir notificaciones de nuevas solicitudes'),
    ('et', 'pwa.install_for_notifications_provider', 'Installi rakendus, et saada teateid uute päringute kohta'),
    ('fi', 'pwa.install_for_notifications_provider', 'Asenna sovellus saadaksesi ilmoituksia uusista pyynnöistä'),
    ('fr', 'pwa.install_for_notifications_provider', "Installe l'application pour recevoir des notifications sur les nouvelles demandes"),
    ('ga', 'pwa.install_for_notifications_provider', 'Suiteáil an aip chun fógraí a fháil faoi iarratais nua'),
    ('hr', 'pwa.install_for_notifications_provider', 'Instaliraj aplikaciju kako bi primao obavijesti o novim upitima'),
    ('hu', 'pwa.install_for_notifications_provider', 'Telepítsd az alkalmazást, hogy értesítéseket kapj az új megkeresésekről'),
    ('is', 'pwa.install_for_notifications_provider', 'Settu upp forritið til að fá tilkynningar um nýjar beiðnir'),
    ('it', 'pwa.install_for_notifications_provider', "Installa l'app per ricevere notifiche sulle nuove richieste"),
    ('lb', 'pwa.install_for_notifications_provider', "Installéier d'App fir Notifikatiounen iwwer nei Ufroe ze kréien"),
    ('lt', 'pwa.install_for_notifications_provider', 'Įdiek programėlę, kad gautum pranešimus apie naujus užklausimus'),
    ('lv', 'pwa.install_for_notifications_provider', 'Instalē lietotni, lai saņemtu paziņojumus par jauniem pieprasījumiem'),
    ('mk', 'pwa.install_for_notifications_provider', 'Инсталирај ја апликацијата за да добиваш известувања за нови барања'),
    ('mt', 'pwa.install_for_notifications_provider', 'Installa l-app biex tirċievi notifiki dwar talbiet ġodda'),
    ('nl', 'pwa.install_for_notifications_provider', 'Installeer de app om meldingen te ontvangen over nieuwe aanvragen'),
    ('no', 'pwa.install_for_notifications_provider', 'Installer appen for å motta varsler om nye forespørsler'),
    ('pl', 'pwa.install_for_notifications_provider', 'Zainstaluj aplikację, aby otrzymywać powiadomienia o nowych zapytaniach'),
    ('pt', 'pwa.install_for_notifications_provider', 'Instale o aplicativo para receber notificações sobre novas solicitações'),
    ('pt-PT', 'pwa.install_for_notifications_provider', 'Instala a aplicação para receber notificações sobre novos pedidos'),
    ('ro', 'pwa.install_for_notifications_provider', 'Instalează aplicația pentru a primi notificări despre cereri noi'),
    ('ru', 'pwa.install_for_notifications_provider', 'Установи приложение, чтобы получать уведомления о новых заявках'),
    ('sk', 'pwa.install_for_notifications_provider', 'Nainštaluj aplikáciu a dostávaj upozornenia o nových dopytoch'),
    ('sl', 'pwa.install_for_notifications_provider', 'Namesti aplikacijo, da prejemaš obvestila o novih povpraševanjih'),
    ('sq', 'pwa.install_for_notifications_provider', 'Instalo aplikacionin për të marrë njoftime për kërkesa të reja'),
    ('sr', 'pwa.install_for_notifications_provider', 'Инсталирај апликацију да би добијао обавештења о новим захтевима'),
    ('sv', 'pwa.install_for_notifications_provider', 'Installera appen för att få aviseringar om nya förfrågningar'),
    ('tr', 'pwa.install_for_notifications_provider', 'Yeni talepler için bildirim almak üzere uygulamayı yükle'),
    ('uk', 'pwa.install_for_notifications_provider', 'Встанови додаток, щоб отримувати сповіщення про нові заявки'),

    # pwa.install_for_notifications_client
    ('bg', 'pwa.install_for_notifications_client', 'Инсталирай приложението за да получаваш известия за статуса на заявките си'),
    ('cs', 'pwa.install_for_notifications_client', 'Nainstaluj aplikaci a dostávej oznámení o stavu svých poptávek'),
    ('da', 'pwa.install_for_notifications_client', 'Installer appen for at modtage notifikationer om status på dine forespørgsler'),
    ('de', 'pwa.install_for_notifications_client', 'Installiere die App, um Benachrichtigungen über den Status deiner Anfragen zu erhalten'),
    ('el', 'pwa.install_for_notifications_client', 'Εγκατέστησε την εφαρμογή για να λαμβάνεις ειδοποιήσεις για την κατάσταση των αιτημάτων σου'),
    ('en', 'pwa.install_for_notifications_client', 'Install the app to receive notifications about the status of your requests'),
    ('es', 'pwa.install_for_notifications_client', 'Instala la app para recibir notificaciones sobre el estado de tus solicitudes'),
    ('et', 'pwa.install_for_notifications_client', 'Installi rakendus, et saada teateid oma päringute oleku kohta'),
    ('fi', 'pwa.install_for_notifications_client', 'Asenna sovellus saadaksesi ilmoituksia pyyntöjesi tilasta'),
    ('fr', 'pwa.install_for_notifications_client', "Installe l'application pour recevoir des notifications sur le statut de tes demandes"),
    ('ga', 'pwa.install_for_notifications_client', 'Suiteáil an aip chun fógraí a fháil faoi stádas do chuid iarratas'),
    ('hr', 'pwa.install_for_notifications_client', 'Instaliraj aplikaciju kako bi primao obavijesti o statusu svojih upita'),
    ('hu', 'pwa.install_for_notifications_client', 'Telepítsd az alkalmazást, hogy értesítéseket kapj kéréseid állapotáról'),
    ('is', 'pwa.install_for_notifications_client', 'Settu upp forritið til að fá tilkynningar um stöðu beiðna þinna'),
    ('it', 'pwa.install_for_notifications_client', "Installa l'app per ricevere notifiche sullo stato delle tue richieste"),
    ('lb', 'pwa.install_for_notifications_client', "Installéier d'App fir Notifikatiounen iwwer de Status vun denge Ufroe ze kréien"),
    ('lt', 'pwa.install_for_notifications_client', 'Įdiek programėlę, kad gautum pranešimus apie savo užklausimų būseną'),
    ('lv', 'pwa.install_for_notifications_client', 'Instalē lietotni, lai saņemtu paziņojumus par savu pieprasījumu statusu'),
    ('mk', 'pwa.install_for_notifications_client', 'Инсталирај ја апликацијата за да добиваш известувања за статусот на твоите барања'),
    ('mt', 'pwa.install_for_notifications_client', "Installa l-app biex tirċievi notifiki dwar l-istat tat-talbiet tiegħek"),
    ('nl', 'pwa.install_for_notifications_client', 'Installeer de app om meldingen te ontvangen over de status van jouw aanvragen'),
    ('no', 'pwa.install_for_notifications_client', 'Installer appen for å motta varsler om statusen på dine forespørsler'),
    ('pl', 'pwa.install_for_notifications_client', 'Zainstaluj aplikację, aby otrzymywać powiadomienia o statusie swoich zapytań'),
    ('pt', 'pwa.install_for_notifications_client', 'Instale o aplicativo para receber notificações sobre o status das suas solicitações'),
    ('pt-PT', 'pwa.install_for_notifications_client', 'Instala a aplicação para receber notificações sobre o estado dos teus pedidos'),
    ('ro', 'pwa.install_for_notifications_client', 'Instalează aplicația pentru a primi notificări despre statusul cererilor tale'),
    ('ru', 'pwa.install_for_notifications_client', 'Установи приложение, чтобы получать уведомления о статусе своих заявок'),
    ('sk', 'pwa.install_for_notifications_client', 'Nainštaluj aplikáciu a dostávaj upozornenia o stave svojich dopytov'),
    ('sl', 'pwa.install_for_notifications_client', 'Namesti aplikacijo, da prejemaš obvestila o stanju svojih povpraševanj'),
    ('sq', 'pwa.install_for_notifications_client', 'Instalo aplikacionin për të marrë njoftime për statusin e kërkesave tuaja'),
    ('sr', 'pwa.install_for_notifications_client', 'Инсталирај апликацију да би добијао обавештења о статусу твојих захтева'),
    ('sv', 'pwa.install_for_notifications_client', 'Installera appen för att få aviseringar om statusen på dina förfrågningar'),
    ('tr', 'pwa.install_for_notifications_client', 'Taleplerinizin durumu hakkında bildirim almak için uygulamayı yükle'),
    ('uk', 'pwa.install_for_notifications_client', 'Встанови додаток, щоб отримувати сповіщення про статус своїх заявок'),
]

def seed_translations():
    import psycopg2
    conn = psycopg2.connect(DATABASE_URL)
    try:
        with conn.cursor() as cur:
            execute_values(
                cur,
                """
                INSERT INTO translations (lang, key, value)
                VALUES %s
                ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
                """,
                TRANSLATIONS
            )
        conn.commit()
        print(f"Seeded {len(TRANSLATIONS)} translations")
    except Exception as e:
        conn.rollback()
        print(f"Error seeding translations: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    seed_translations()
