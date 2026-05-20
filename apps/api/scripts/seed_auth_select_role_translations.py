#!/usr/bin/env python3
"""Seed auth select role translations into the translations table."""

import os
import psycopg2
from psycopg2.extras import execute_values

# Database connection string
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://nevumo:nevumo@localhost:5433/nevumo_leads")

# Translations: language -> list of values in order
TRANSLATIONS = {
    "bg":    ["Как искаш да използваш Nevumo?", "Избери тип акаунт — можеш да го смениш по-късно", "Търся услуга", "Намери проверени специалисти близо до теб — бързо и безплатно", "Предлагам услуга", "Намери клиенти, развий бизнеса си и спечели повече"],
    "cs":    ["Jak chceš používat Nevumo?", "Zvol typ účtu — kdykoli ho můžeš změnit", "Hledám službu", "Najdi ověřené odborníky ve svém okolí — rychle a zdarma", "Nabízím službu", "Získej klienty, rozvíjej podnikání a vydělávej více"],
    "da":    ["Hvordan vil du bruge Nevumo?", "Vælg din kontotype — du kan altid ændre den senere", "Jeg søger en tjeneste", "Find betroede fagfolk nær dig — hurtigt og gratis", "Jeg tilbyder en tjeneste", "Få kunder, vækst din forretning og tjen mere"],
    "de":    ["Wie möchtest du Nevumo nutzen?", "Wähle deinen Kontotyp — du kannst ihn jederzeit ändern", "Ich suche einen Service", "Finde vertrauenswürdige Fachleute in deiner Nähe — schnell und kostenlos", "Ich biete einen Service an", "Gewinne Kunden, erweitere dein Geschäft und verdiene mehr"],
    "el":    ["Πώς θέλεις να χρησιμοποιήσεις το Nevumo;", "Επίλεξε τύπο λογαριασμού — μπορείς να τον αλλάξεις αργότερα", "Ψάχνω υπηρεσία", "Βρες αξιόπιστους επαγγελματίες κοντά σου — γρήγορα και δωρεάν", "Προσφέρω υπηρεσία", "Απόκτησε πελάτες, ανάπτυξε την επιχείρησή σου και κέρδισε περισσότερα"],
    "en":    ["How do you want to use Nevumo?", "Choose your account type — you can always change it later", "I need a service", "Find trusted professionals near you — fast and free", "I offer a service", "Get clients, grow your business and earn more"],
    "es":    ["¿Cómo quieres usar Nevumo?", "Elige el tipo de cuenta — siempre puedes cambiarlo después", "Busco un servicio", "Encuentra profesionales de confianza cerca de ti — rápido y gratis", "Ofrezco un servicio", "Consigue clientes, haz crecer tu negocio y gana más"],
    "et":    ["Kuidas soovid Nevumot kasutada?", "Vali konto tüüp — saad seda alati hiljem muuta", "Otsin teenust", "Leia usaldusväärseid spetsialiste enda lähedalt — kiiresti ja tasuta", "Pakun teenust", "Hangi kliente, kasvatage oma äri ja teeni rohkem"],
    "fi":    ["Miten haluat käyttää Nevumoa?", "Valitse tilityyppisi — voit aina muuttaa sen myöhemmin", "Tarvitsen palvelun", "Löydä luotettavia ammattilaisia läheltäsi — nopeasti ja ilmaiseksi", "Tarjoan palvelun", "Hanki asiakkaita, kasvata liiketoimintaasi ja ansaitse enemmän"],
    "fr":    ["Comment veux-tu utiliser Nevumo ?", "Choisis ton type de compte — tu peux toujours le changer plus tard", "Je cherche un service", "Trouve des professionnels de confiance près de chez toi — rapide et gratuit", "Je propose un service", "Obtiens des clients, développe ton activité et gagne plus"],
    "ga":    ["Conas is mian leat Nevumo a úsáid?", "Roghnaigh do chineál cuntais — is féidir leat é a athrú am ar bith", "Tá seirbhís uaim", "Aimsigh gairmithe iontaofa in aice leat — tapa agus saor in aisce", "Tairgim seirbhís", "Faigh cliaint, fás do ghnó agus tuilleamh níos mó"],
    "hr":    ["Kako želiš koristiti Nevumo?", "Odaberi vrstu računa — uvijek ga možeš promijeniti", "Tražim uslugu", "Pronađi pouzdane stručnjake u blizini — brzo i besplatno", "Nudim uslugu", "Pronađi klijente, razvij posao i zaradi više"],
    "hu":    ["Hogyan szeretnéd használni a Nevumót?", "Válaszd ki a fiók típusát — bármikor megváltoztathatod", "Szolgáltatást keresek", "Találj megbízható szakembereket a közeledben — gyorsan és ingyen", "Szolgáltatást kínálok", "Szerezz ügyfeleket, fejleszd vállalkozásodat és keress többet"],
    "is":    ["Hvernig viltu nota Nevumo?", "Veldu tegund reiknings — þú getur alltaf breytt honum síðar", "Ég þarf þjónustu", "Finndu traustar sérfræðingar nálægt þér — hratt og ókeypis", "Ég bjóð upp á þjónustu", "Fáðu viðskiptavini, stækkaðu fyrirtæki þitt og þjónaðu meira"],
    "it":    ["Come vuoi usare Nevumo?", "Scegli il tipo di account — puoi sempre cambiarlo in seguito", "Ho bisogno di un servizio", "Trova professionisti di fiducia vicino a te — veloce e gratuito", "Offro un servizio", "Ottieni clienti, fai crescere il tuo business e guadagna di più"],
    "lb":    ["Wéi wëlls du Nevumo benotzen?", "Wiel däin Kontotyp — du kanns en ëmmer méi spéit änneren", "Ech sichen e Service", "Fannt vertrauenswürdeg Fachleit an denger Géigend — séier a gratis", "Ech bidden e Service un", "Kritt Clienten, entwéckelt däi Geschäft a verdéngt méi"],
    "lt":    ["Kaip nori naudoti Nevumo?", "Pasirink paskyros tipą — visada galėsi jį pakeisti", "Ieškau paslaugos", "Rask patikimus specialistus šalia savęs — greitai ir nemokamai", "Siūlau paslaugą", "Gauk klientų, plėtok verslą ir uždirbk daugiau"],
    "lv":    ["Kā vēlies izmantot Nevumo?", "Izvēlies konta veidu — vienmēr vari to mainīt vēlāk", "Meklēju pakalpojumu", "Atrodi uzticamus speciālistus tuvumā — ātri un bez maksas", "Piedāvāju pakalpojumu", "Iegūsti klientus, attīsti biznesu un pelni vairāk"],
    "mk":    ["Како сакаш да го користиш Nevumo?", "Избери тип на сметка — секогаш можеш да го промениш подоцна", "Барам услуга", "Најди доверливи стручњаци блиску до тебе — брзо и бесплатно", "Нудам услуга", "Добиј клиенти, развиј бизнис и заработи повеќе"],
    "mt":    ["Kif trid tuża Nevumo?", "Agħżel it-tip ta' kont — tista' dejjem tibdlu aktar tard", "Għandi bżonn servizz", "Sib professjonisti fidati qriebek — malajr u b'xejn", "Noffri servizz", "Ikseb klijenti, ikber in-negozju tiegħek u qla' aktar"],
    "nl":    ["Hoe wil je Nevumo gebruiken?", "Kies je accounttype — je kunt het altijd later wijzigen", "Ik zoek een dienst", "Vind betrouwbare professionals bij jou in de buurt — snel en gratis", "Ik bied een dienst aan", "Krijg klanten, laat je bedrijf groeien en verdien meer"],
    "no":    ["Hvordan vil du bruke Nevumo?", "Velg kontotype — du kan alltid endre den senere", "Jeg trenger en tjeneste", "Finn pålitelige fagfolk nær deg — raskt og gratis", "Jeg tilbyr en tjeneste", "Få kunder, vokst virksomheten din og tjen mer"],
    "pl":    ["Jak chcesz korzystać z Nevumo?", "Wybierz typ konta — zawsze możesz go zmienić później", "Szukam usługi", "Znajdź zaufanych specjalistów w pobliżu — szybko i bezpłatnie", "Oferuję usługę", "Zdobądź klientów, rozwijaj firmę i zarabiaj więcej"],
    "pt":    ["Como você quer usar o Nevumo?", "Escolha o tipo de conta — você pode sempre mudar depois", "Preciso de um serviço", "Encontre profissionais de confiança perto de você — rápido e gratuito", "Ofereço um serviço", "Conquiste clientes, expanda seu negócio e ganhe mais"],
    "pt-PT": ["Como queres usar o Nevumo?", "Escolhe o tipo de conta — podes sempre mudar mais tarde", "Preciso de um serviço", "Encontra profissionais de confiança perto de ti — rápido e gratuito", "Ofereço um serviço", "Consegue clientes, expande o teu negócio e ganha mais"],
    "ro":    ["Cum vrei să folosești Nevumo?", "Alege tipul de cont — îl poți schimba oricând mai târziu", "Caut un serviciu", "Găsește profesioniști de încredere în apropierea ta — rapid și gratuit", "Ofer un serviciu", "Obține clienți, dezvoltă-ți afacerea și câștigă mai mult"],
    "ru":    ["Как ты хочешь использовать Nevumo?", "Выбери тип аккаунта — его всегда можно изменить позже", "Мне нужна услуга", "Найди проверенных специалистов рядом — быстро и бесплатно", "Я предлагаю услугу", "Привлекай клиентов, развивай бизнес и зарабатывай больше"],
    "sk":    ["Ako chceš používať Nevumo?", "Vyber typ účtu — vždy ho môžeš zmeniť neskôr", "Hľadám službu", "Nájdi overených odborníkov vo svojom okolí — rýchlo a zadarmo", "Ponúkam službu", "Získaj klientov, rozvíjaj podnikanie a zarábaj viac"],
    "sl":    ["Kako želiš uporabljati Nevumo?", "Izberi vrsto računa — vedno jo lahko pozneje spremenite", "Iščem storitev", "Najdi zaupanja vredne strokovnjake v bližini — hitro in brezplačno", "Ponujam storitev", "Pridobi stranke, razvij posel in zasluži več"],
    "sq":    ["Si dëshironi të përdorni Nevumo?", "Zgjidhni llojin e llogarisë — gjithmonë mund ta ndryshoni më vonë", "Kërkoj një shërbim", "Gjeni profesionistë të besueshëm afër jush — shpejt dhe falas", "Ofroj një shërbim", "Fitoni klientë, rritni biznesin tuaj dhe fitoni më shumë"],
    "sr":    ["Како желиш да користиш Nevumo?", "Изабери тип налога — увек га можеш променити касније", "Тражим услугу", "Пронађи поуздане стручњаке у близини — брзо и бесплатно", "Нудим услугу", "Нађи клијенте, развиј пословање и зарађуј више"],
    "sv":    ["Hur vill du använda Nevumo?", "Välj din kontotyp — du kan alltid ändra den senare", "Jag söker en tjänst", "Hitta pålitliga proffs nära dig — snabbt och gratis", "Jag erbjuder en tjänst", "Skaffa kunder, väx ditt företag och tjäna mer"],
    "tr":    ["Nevumo'yu nasıl kullanmak istiyorsun?", "Hesap türünü seç — istediğin zaman değiştirebilirsin", "Bir hizmet arıyorum", "Yakınınızdaki güvenilir profesyonelleri bulun — hızlı ve ücretsiz", "Bir hizmet sunuyorum", "Müşteri kazan, işini büyüt ve daha fazla kazan"],
    "uk":    ["Як ти хочеш використовувати Nevumo?", "Вибери тип акаунту — його завжди можна змінити пізніше", "Мені потрібна послуга", "Знайди перевірених фахівців поруч — швидко та безкоштовно", "Я пропоную послугу", "Залучай клієнтів, розвивай бізнес і заробляй більше"],
}

# Keys in order corresponding to the values per language
KEYS = [
    "auth.select_role_title",
    "auth.select_role_subtitle",
    "auth.select_role_client_title",
    "auth.select_role_client_subtitle",
    "auth.select_role_provider_title",
    "auth.select_role_provider_subtitle",
]


def seed_translations() -> int:
    """Seed auth select role translations and return the number of rows upserted."""
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    rows_to_upsert = []
    for lang, values in TRANSLATIONS.items():
        for key, value in zip(KEYS, values):
            rows_to_upsert.append((lang, key, value))

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
    print(f"Upserted {count} rows (6 keys × 34 languages)")

