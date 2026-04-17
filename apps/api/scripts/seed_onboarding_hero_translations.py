#!/usr/bin/env python3
"""Seed onboarding hero translations for all 34 supported languages."""

import psycopg2

# Connection string
import os
DB_URL = os.environ.get("DATABASE_URL", "postgresql://nevumo:nevumo@nevumo-postgres:5432/nevumo_leads")

# Translation keys
KEYS = [
    "provider_dashboard.setup_title",
    "provider_dashboard.setup_subtitle",
    "provider_dashboard.btn_complete_setup",
    "provider_dashboard.setup_title_1step",
    "provider_dashboard.setup_subtitle_1step",
    "provider_dashboard.btn_add_service",
    "provider_dashboard.step_profile",
    "provider_dashboard.step_service",
]

# Translations for all 34 languages
TRANSLATIONS = {
    "en": [
        "You're 2 steps away from getting clients",
        "Complete your profile to start receiving requests",
        "Complete your profile",
        "You're 1 step away from getting clients",
        "Add your first service to start receiving requests",
        "Add your first service",
        "Profile",
        "Service",
    ],
    "bg": [
        "Само 2 стъпки до първите клиенти",
        "Попълнете профила си, за да започнете да получавате запитвания",
        "Попълни профила",
        "Само 1 стъпка до първите клиенти",
        "Добавете първата си услуга, за да получавате запитвания",
        "Добави услуга",
        "Профил",
        "Услуга",
    ],
    "cs": [
        "Jste 2 kroky od prvních klientů",
        "Doplňte svůj profil a začněte přijímat poptávky",
        "Doplnit profil",
        "Jste 1 krok od prvních klientů",
        "Přidejte svou první službu a začněte přijímat poptávky",
        "Přidat službu",
        "Profil",
        "Služba",
    ],
    "da": [
        "Du er 2 trin fra dine første kunder",
        "Udfyld din profil for at begynde at modtage forespørgsler",
        "Udfyld profil",
        "Du er 1 trin fra dine første kunder",
        "Tilføj din første ydelse for at begynde at modtage forespørgsler",
        "Tilføj ydelse",
        "Profil",
        "Ydelse",
    ],
    "de": [
        "Sie sind 2 Schritte von Ihren ersten Kunden entfernt",
        "Vervollständigen Sie Ihr Profil, um Anfragen zu erhalten",
        "Profil vervollständigen",
        "Sie sind 1 Schritt von Ihren ersten Kunden entfernt",
        "Fügen Sie Ihren ersten Service hinzu, um Anfragen zu erhalten",
        "Service hinzufügen",
        "Profil",
        "Leistung",
    ],
    "el": [
        "Είστε 2 βήματα από τους πρώτους πελάτες σας",
        "Συμπληρώστε το προφίλ σας για να λαμβάνετε αιτήματα",
        "Συμπλήρωση προφίλ",
        "Είστε 1 βήμα από τους πρώτους πελάτες σας",
        "Προσθέστε την πρώτη σας υπηρεσία για να λαμβάνετε αιτήματα",
        "Προσθήκη υπηρεσίας",
        "Προφίλ",
        "Υπηρεσία",
    ],
    "es": [
        "Estás a 2 pasos de tus primeros clientes",
        "Completa tu perfil para empezar a recibir solicitudes",
        "Completar perfil",
        "Estás a 1 paso de tus primeros clientes",
        "Añade tu primer servicio para empezar a recibir solicitudes",
        "Añadir servicio",
        "Perfil",
        "Servicio",
    ],
    "et": [
        "Olete 2 sammu kaugusel esimestest klientidest",
        "Täitke oma profiil, et hakata päringuid saama",
        "Täida profiil",
        "Olete 1 samm kaugusel esimestest klientidest",
        "Lisage oma esimene teenus, et hakata päringuid saama",
        "Lisa teenus",
        "Profiil",
        "Teenus",
    ],
    "fi": [
        "Olet 2 askelta ensimmäisistä asiakkaistasi",
        "Täytä profiilisi aloittaaksesi pyyntöjen vastaanottamisen",
        "Täytä profiili",
        "Olet 1 askel ensimmäisistä asiakkaistasi",
        "Lisää ensimmäinen palvelusi aloittaaksesi pyyntöjen vastaanottamisen",
        "Lisää palvelu",
        "Profiili",
        "Palvelu",
    ],
    "fr": [
        "Vous êtes à 2 étapes de vos premiers clients",
        "Complétez votre profil pour commencer à recevoir des demandes",
        "Compléter le profil",
        "Vous êtes à 1 étape de vos premiers clients",
        "Ajoutez votre premier service pour commencer à recevoir des demandes",
        "Ajouter un service",
        "Profil",
        "Service",
    ],
    "ga": [
        "Tá tú 2 chéim ó do chéad chliaint",
        "Críochnaigh do phróifíl chun tús a chur le hiarratais a fháil",
        "Críochnaigh próifíl",
        "Tá tú 1 chéim ó do chéad chliaint",
        "Cuir do chéad seirbhís leis chun tús a chur le hiarratais a fháil",
        "Cuir seirbhís leis",
        "Próifíl",
        "Seirbhís",
    ],
    "hr": [
        "Samo 2 koraka do prvih klijenata",
        "Dopunite profil kako biste počeli primati upite",
        "Dopuni profil",
        "Samo 1 korak do prvih klijenata",
        "Dodajte prvu uslugu kako biste počeli primati upite",
        "Dodaj uslugu",
        "Profil",
        "Usluga",
    ],
    "hu": [
        "2 lépésre van az első ügyfelektől",
        "Töltse ki profilját a megkeresések fogadásához",
        "Profil kitöltése",
        "1 lépésre van az első ügyfelektől",
        "Adja hozzá első szolgáltatását a megkeresések fogadásához",
        "Szolgáltatás hozzáadása",
        "Profil",
        "Szolgáltatás",
    ],
    "is": [
        "Þú ert 2 skref frá fyrstu viðskiptavinum þínum",
        "Fylltu út prófílinn þinn til að byrja að fá beiðnir",
        "Fylla út prófíl",
        "Þú ert 1 skref frá fyrstu viðskiptavinum þínum",
        "Bættu við fyrstu þjónustunni þinni til að byrja að fá beiðnir",
        "Bæta við þjónustu",
        "Prófíll",
        "Þjónusta",
    ],
    "it": [
        "Sei a 2 passi dai tuoi primi clienti",
        "Completa il tuo profilo per iniziare a ricevere richieste",
        "Completa profilo",
        "Sei a 1 passo dai tuoi primi clienti",
        "Aggiungi il tuo primo servizio per iniziare a ricevere richieste",
        "Aggiungi servizio",
        "Profilo",
        "Servizio",
    ],
    "lb": [
        "Dir sidd 2 Schrëtt vun Äre éischte Clienten ewech",
        "Fëllt Äre Profil aus fir Ufroe ze kréien",
        "Profil fäerdegstellen",
        "Dir sidd 1 Schrëtt vun Äre éischte Clienten ewech",
        "Füügt Äre éischte Service bäi fir Ufroe ze kréien",
        "Service bäifügen",
        "Profil",
        "Service",
    ],
    "lt": [
        "Jūs esate 2 žingsnius nuo pirmųjų klientų",
        "Užpildykite profilį, kad pradėtumėte gauti užklausas",
        "Užpildyti profilį",
        "Jūs esate 1 žingsnį nuo pirmųjų klientų",
        "Pridėkite pirmąją paslaugą, kad pradėtumėte gauti užklausas",
        "Pridėti paslaugą",
        "Profilis",
        "Paslauga",
    ],
    "lv": [
        "Jūs esat 2 soļus no pirmajiem klientiem",
        "Aizpildiet savu profilu, lai sāktu saņemt pieprasījumus",
        "Aizpildīt profilu",
        "Jūs esat 1 soli no pirmajiem klientiem",
        "Pievienojiet savu pirmo pakalpojumu, lai sāktu saņemt pieprasījumus",
        "Pievienot pakalpojumu",
        "Profils",
        "Pakalpojums",
    ],
    "mk": [
        "Само 2 чекори до првите клиенти",
        "Пополнете го профилот за да почнете да примате барања",
        "Пополни профил",
        "Само 1 чекор до првите клиенти",
        "Додајте ја вашата прва услуга за да почнете да примате барања",
        "Додај услуга",
        "Профил",
        "Услуга",
    ],
    "mt": [
        "Inti 2 passi bogħod mill-ewwel klijenti tiegħek",
        "Lesti l-profil tiegħek biex tibda tirċievi talbiet",
        "Lesti l-profil",
        "Inti pass wieħed bogħod mill-ewwel klijenti tiegħek",
        "Żid l-ewwel servizz tiegħek biex tibda tirċievi talbiet",
        "Żid servizz",
        "Profil",
        "Servizz",
    ],
    "nl": [
        "U bent 2 stappen verwijderd van uw eerste klanten",
        "Vul uw profiel in om aanvragen te ontvangen",
        "Profiel invullen",
        "U bent 1 stap verwijderd van uw eerste klanten",
        "Voeg uw eerste dienst toe om aanvragen te ontvangen",
        "Dienst toevoegen",
        "Profiel",
        "Dienst",
    ],
    "no": [
        "Du er 2 steg unna dine første kunder",
        "Fyll ut profilen din for å begynne å motta forespørgsler",
        "Fyll ut profil",
        "Du er 1 steg unna dine første kunder",
        "Legg til din første tjeneste for å begynne å motta forespørsler",
        "Legg til tjeneste",
        "Profil",
        "Tjeneste",
    ],
    "pl": [
        "Jesteś 2 kroki od pierwszych klientów",
        "Uzupełnij profil, aby zacząć otrzymywać zapytania",
        "Uzupełnij profil",
        "Jesteś 1 krok od pierwszych klientów",
        "Dodaj pierwszą usługę, aby zacząć otrzymywać zapytania",
        "Dodaj usługę",
        "Profil",
        "Usługa",
    ],
    "pt": [
        "Você está a 2 passos dos seus primeiros clientes",
        "Complete seu perfil para começar a receber solicitações",
        "Completar perfil",
        "Você está a 1 passo dos seus primeiros clientes",
        "Adicione seu primeiro serviço para começar a receber solicitações",
        "Adicionar serviço",
        "Perfil",
        "Serviço",
    ],
    "pt-PT": [
        "Está a 2 passos dos seus primeiros clientes",
        "Complete o seu perfil para começar a receber pedidos",
        "Completar perfil",
        "Está a 1 passo dos seus primeiros clientes",
        "Adicione o seu primeiro serviço para começar a receber pedidos",
        "Adicionar serviço",
        "Perfil",
        "Serviço",
    ],
    "ro": [
        "Ești la 2 pași de primii tăi clienți",
        "Completează-ți profilul pentru a începe să primești solicitări",
        "Completează profilul",
        "Ești la 1 pas de primii tăi clienți",
        "Adaugă primul tău serviciu pentru a începe să primești solicitări",
        "Adaugă serviciu",
        "Profil",
        "Serviciu",
    ],
    "ru": [
        "Вы в 2 шагах от первых клиентов",
        "Заполните профиль, чтобы начать получать заявки",
        "Заполнить профиль",
        "Вы в 1 шаге от первых клиентов",
        "Добавьте первую услугу, чтобы начать получать заявки",
        "Добавить услугу",
        "Профиль",
        "Услуга",
    ],
    "sk": [
        "Ste 2 kroky od prvých klientov",
        "Doplňte profil a začnite prijímať dopyty",
        "Doplniť profil",
        "Ste 1 krok od prvých klientov",
        "Pridajte prvú službu a začnite prijímať dopyty",
        "Pridať službu",
        "Profil",
        "Služba",
    ],
    "sl": [
        "2 koraka vas ločita od prvih strank",
        "Dopolnite profil, da začnete prejemati povpraševanja",
        "Dopolni profil",
        "1 korak vas loči od prvih strank",
        "Dodajte prvo storitev, da začnete prejemati povpraševanja",
        "Dodaj storitev",
        "Profil",
        "Storitev",
    ],
    "sq": [
        "Jeni 2 hapa larg klientëve tuaj të parë",
        "Plotësoni profilin tuaj për të filluar të merrni kërkesa",
        "Plotëso profilin",
        "Jeni 1 hap larg klientëve tuaj të parë",
        "Shtoni shërbimin tuaj të parë për të filluar të merrni kërkesa",
        "Shto shërbim",
        "Profil",
        "Shërbim",
    ],
    "sr": [
        "Само 2 корака до првих клијената",
        "Попуните профил да бисте почели да примате упите",
        "Попуни профил",
        "Само 1 корак до првих клијената",
        "Додајте прву услугу да бисте почели да примате упите",
        "Додај услугу",
        "Профил",
        "Услуга",
    ],
    "sv": [
        "Du är 2 steg från dina första kunder",
        "Fyll i din profil för att börja ta emot förfrågningar",
        "Fyll i profil",
        "Du är 1 steg från dina första kunder",
        "Lägg till din första tjänst för att börja ta emot förfrågningar",
        "Lägg till tjänst",
        "Profil",
        "Tjänst",
    ],
    "tr": [
        "İlk müşterilerinize 2 adım uzaklıktasınız",
        "İstek almaya başlamak için profilinizi tamamlayın",
        "Profili tamamla",
        "İlk müşterilerinize 1 adım uzaklıktasınız",
        "İstek almaya başlamak için ilk hizmetinizi ekleyin",
        "Hizmet ekle",
        "Profil",
        "Hizmet",
    ],
    "uk": [
        "Ви в 2 кроках від перших клієнтів",
        "Заповніть профіль, щоб почати отримувати запити",
        "Заповнити профіль",
        "Ви в 1 кроці від перших клієнтів",
        "Додайте першу послугу, щоб почати отримувати запити",
        "Додати послугу",
        "Профіль",
        "Послуга",
    ],
}


def seed_translations() -> None:
    """Upsert all onboarding hero translations into the database."""
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO translations (lang, key, value)
        VALUES (%s, %s, %s)
        ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
    """

    count = 0
    for lang, values in TRANSLATIONS.items():
        for key, value in zip(KEYS, values):
            cursor.execute(insert_query, (lang, key, value))
            count += 1

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Seeded onboarding hero translations: {count} rows")


if __name__ == "__main__":
    seed_translations()
