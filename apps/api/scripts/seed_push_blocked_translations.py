#!/usr/bin/env python3
"""
Seed script to add push notification blocked state translations for all 34 languages.
"""

import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://nevumo:nevumo@nevumo-postgres:5432/nevumo_leads")

TRANSLATIONS = [
    ("bg", "settings.push_blocked_title", "Известията са блокирани"),
    ("bg", "settings.push_blocked_description", "Известията за nevumo.com са блокирани в браузъра. За да ги активирате, отидете в настройките на браузъра и разрешете известията за този сайт."),
    ("cs", "settings.push_blocked_title", "Oznámení jsou zablokována"),
    ("cs", "settings.push_blocked_description", "Oznámení pro nevumo.com jsou zablokována ve vašem prohlížeči. Chcete-li je povolit, přejděte do nastavení prohlížeče a povolte oznámení pro tento web."),
    ("da", "settings.push_blocked_title", "Notifikationer er blokeret"),
    ("da", "settings.push_blocked_description", "Notifikationer fra nevumo.com er blokeret i din browser. For at aktivere dem skal du gå til browserindstillingerne og tillade notifikationer for dette websted."),
    ("de", "settings.push_blocked_title", "Benachrichtigungen sind blockiert"),
    ("de", "settings.push_blocked_description", "Benachrichtigungen von nevumo.com sind in Ihrem Browser blockiert. Um sie zu aktivieren, öffnen Sie die Browsereinstellungen und erlauben Sie Benachrichtigungen für diese Website."),
    ("el", "settings.push_blocked_title", "Οι ειδοποιήσεις είναι αποκλεισμένες"),
    ("el", "settings.push_blocked_description", "Οι ειδοποιήσεις για το nevumo.com έχουν αποκλειστεί στο πρόγραμμα περιήγησής σας. Για να τις ενεργοποιήσετε, μεταβείτε στις ρυθμίσεις του προγράμματος περιήγησης και επιτρέψτε τις ειδοποιήσεις για αυτόν τον ιστότοπο."),
    ("en", "settings.push_blocked_title", "Notifications are blocked"),
    ("en", "settings.push_blocked_description", "Notifications for nevumo.com are blocked in your browser. To enable them, go to your browser settings and allow notifications for this site."),
    ("es", "settings.push_blocked_title", "Las notificaciones están bloqueadas"),
    ("es", "settings.push_blocked_description", "Las notificaciones de nevumo.com están bloqueadas en tu navegador. Para activarlas, ve a la configuración del navegador y permite las notificaciones para este sitio."),
    ("et", "settings.push_blocked_title", "Teavitused on blokeeritud"),
    ("et", "settings.push_blocked_description", "nevumo.com teavitused on teie brauseris blokeeritud. Nende lubamiseks avage brauseri seaded ja lubage teavitused selle saidi jaoks."),
    ("fi", "settings.push_blocked_title", "Ilmoitukset on estetty"),
    ("fi", "settings.push_blocked_description", "nevumo.com-ilmoitukset on estetty selaimessasi. Ota ne käyttöön siirtymällä selaimen asetuksiin ja sallimalla ilmoitukset tälle sivustolle."),
    ("fr", "settings.push_blocked_title", "Les notifications sont bloquées"),
    ("fr", "settings.push_blocked_description", "Les notifications de nevumo.com sont bloquées dans votre navigateur. Pour les activer, accédez aux paramètres du navigateur et autorisez les notifications pour ce site."),
    ("ga", "settings.push_blocked_title", "Tá fógraí blocáilte"),
    ("ga", "settings.push_blocked_description", "Tá fógraí nevumo.com blocáilte i do bhrabhsálaí. Chun iad a chumasú, téigh go socruithe an bhrabhsálaí agus ceadaigh fógraí don suíomh seo."),
    ("hr", "settings.push_blocked_title", "Obavijesti su blokirane"),
    ("hr", "settings.push_blocked_description", "Obavijesti za nevumo.com blokirane su u vašem pregledniku. Da biste ih omogućili, idite u postavke preglednika i dopustite obavijesti za ovu stranicu."),
    ("hu", "settings.push_blocked_title", "Az értesítések le vannak tiltva"),
    ("hu", "settings.push_blocked_description", "A nevumo.com értesítések le vannak tiltva a böngészőjében. Az engedélyezéshez nyissa meg a böngésző beállításait, és engedélyezze az értesítéseket erre a webhelyre."),
    ("is", "settings.push_blocked_title", "Tilkynningar eru bannaðar"),
    ("is", "settings.push_blocked_description", "Tilkynningar frá nevumo.com eru bannaðar í vafranum þínum. Til að virkja þær skaltu fara í stillingar vafrans og leyfa tilkynningar fyrir þessa síðu."),
    ("it", "settings.push_blocked_title", "Le notifiche sono bloccate"),
    ("it", "settings.push_blocked_description", "Le notifiche di nevumo.com sono bloccate nel tuo browser. Per attivarle, vai nelle impostazioni del browser e consenti le notifiche per questo sito."),
    ("lb", "settings.push_blocked_title", "Notifikatiounen si gespaart"),
    ("lb", "settings.push_blocked_description", "Notifikatiounen vu nevumo.com si gespaart an ärem Browser. Fir se z'aktivéieren, gitt an d'Browser-Astellungen a erlaabt Notifikatiounen fir dës Säit."),
    ("lt", "settings.push_blocked_title", "Pranešimai užblokuoti"),
    ("lt", "settings.push_blocked_description", "nevumo.com pranešimai užblokuoti jūsų naršyklėje. Norėdami juos įjungti, eikite į naršyklės nustatymus ir leiskite pranešimus šiai svetainei."),
    ("lv", "settings.push_blocked_title", "Paziņojumi ir bloķēti"),
    ("lv", "settings.push_blocked_description", "nevumo.com paziņojumi ir bloķēti jūsu pārlūkprogrammā. Lai tos iespējotu, dodieties uz pārlūkprogrammas iestatījumiem un atļaujiet paziņojumus šai vietnei."),
    ("mk", "settings.push_blocked_title", "Известувањата се блокирани"),
    ("mk", "settings.push_blocked_description", "Известувањата за nevumo.com се блокирани во вашиот прелистувач. За да ги овозможите, одете во поставките на прелистувачот и дозволете известувања за оваа страница."),
    ("mt", "settings.push_blocked_title", "In-notifiki huma mblukati"),
    ("mt", "settings.push_blocked_description", "In-notifiki ta' nevumo.com huma mblukati fil-browser tiegħek. Biex tippermettihom, mur għas-settings tal-browser u permetti n-notifiki għal dan is-sit."),
    ("nl", "settings.push_blocked_title", "Meldingen zijn geblokkeerd"),
    ("nl", "settings.push_blocked_description", "Meldingen van nevumo.com zijn geblokkeerd in uw browser. Om ze in te schakelen, gaat u naar de browserinstellingen en staat u meldingen toe voor deze website."),
    ("no", "settings.push_blocked_title", "Varsler er blokkert"),
    ("no", "settings.push_blocked_description", "Varsler fra nevumo.com er blokkert i nettleseren din. For å aktivere dem, gå til nettleserinnstillingene og tillat varsler for dette nettstedet."),
    ("pl", "settings.push_blocked_title", "Powiadomienia są zablokowane"),
    ("pl", "settings.push_blocked_description", "Powiadomienia dla nevumo.com są zablokowane w Twojej przeglądarce. Aby je włączyć, przejdź do ustawień przeglądarki i zezwól na powiadomienia dla tej strony."),
    ("pt", "settings.push_blocked_title", "As notificações estão bloqueadas"),
    ("pt", "settings.push_blocked_description", "As notificações do nevumo.com estão bloqueadas no seu navegador. Para ativá-las, acesse as configurações do navegador e permita notificações para este site."),
    ("pt-PT", "settings.push_blocked_title", "As notificações estão bloqueadas"),
    ("pt-PT", "settings.push_blocked_description", "As notificações do nevumo.com estão bloqueadas no seu browser. Para as ativar, aceda às definições do browser e permita notificações para este site."),
    ("ro", "settings.push_blocked_title", "Notificările sunt blocate"),
    ("ro", "settings.push_blocked_description", "Notificările pentru nevumo.com sunt blocate în browserul dvs. Pentru a le activa, accesați setările browserului și permiteți notificările pentru acest site."),
    ("ru", "settings.push_blocked_title", "Уведомления заблокированы"),
    ("ru", "settings.push_blocked_description", "Уведомления для nevumo.com заблокированы в вашем браузере. Чтобы их включить, перейдите в настройки браузера и разрешите уведомления для этого сайта."),
    ("sk", "settings.push_blocked_title", "Oznámenia sú zablokované"),
    ("sk", "settings.push_blocked_description", "Oznámenia pre nevumo.com sú zablokované vo vašom prehliadači. Ak ich chcete povoliť, prejdite do nastavení prehliadača a povoľte oznámenia pre túto stránku."),
    ("sl", "settings.push_blocked_title", "Obvestila so blokirana"),
    ("sl", "settings.push_blocked_description", "Obvestila za nevumo.com so blokirana v vašem brskalniku. Če jih želite omogočiti, pojdite v nastavitve brskalnika in dovolite obvestila za to spletno mesto."),
    ("sq", "settings.push_blocked_title", "Njoftimet janë të bllokuara"),
    ("sq", "settings.push_blocked_description", "Njoftimet për nevumo.com janë të bllokuara në shfletuesin tuaj. Për t'i aktivizuar, shkoni te cilësimet e shfletuesit dhe lejoni njoftimet për këtë faqe."),
    ("sr", "settings.push_blocked_title", "Obaveštenja su blokirana"),
    ("sr", "settings.push_blocked_description", "Obaveštenja za nevumo.com su blokirana u vašem pregledaču. Da biste ih omogućili, idite u podešavanja pregledača i dozvolite obaveštenja za ovaj sajt."),
    ("sv", "settings.push_blocked_title", "Aviseringar är blockerade"),
    ("sv", "settings.push_blocked_description", "Aviseringar från nevumo.com är blockerade i din webbläsare. För att aktivera dem, gå till webbläsarinställningarna och tillåt aviseringar för den här webbplatsen."),
    ("tr", "settings.push_blocked_title", "Bildirimler engellendi"),
    ("tr", "settings.push_blocked_description", "nevumo.com bildirimleri tarayıcınızda engellenmiş durumda. Etkinleştirmek için tarayıcı ayarlarına gidin ve bu site için bildirimlere izin verin."),
    ("uk", "settings.push_blocked_title", "Сповіщення заблоковано"),
    ("uk", "settings.push_blocked_description", "Сповіщення для nevumo.com заблоковано у вашому браузері. Щоб їх увімкнути, перейдіть до налаштувань браузера та дозвольте сповіщення для цього сайту."),
]

def seed_push_blocked_translations():
    """Insert push notification blocked state translations for all languages."""
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    for lang, key, value in TRANSLATIONS:
        cursor.execute("""
            INSERT INTO translations (lang, key, value)
            VALUES (%s, %s, %s)
            ON CONFLICT (lang, key) 
            DO UPDATE SET value = EXCLUDED.value
        """, (lang, key, value))
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✓ Added push_blocked translations for {len(TRANSLATIONS)} languages")

if __name__ == "__main__":
    seed_push_blocked_translations()
