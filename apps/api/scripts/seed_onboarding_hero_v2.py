import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://nevumo:nevumo@nevumo-postgres:5432/nevumo_leads")
engine = create_engine(DATABASE_URL)

# (lang, setup_title, setup_subtitle, btn_complete_setup, setup_title_1step, setup_subtitle_1step, btn_add_service, step_profile, step_service)
ROWS = [
    ("bg", "На 2 стъпки от първите си клиенти", "Попълни профила си, за да започнеш да получаваш запитвания", "Завърши настройката", "На 1 стъпка от първите си клиенти", "Добави услуга, за да започнеш да получаваш запитвания", "Добави услуга", "Профил", "Услуга"),
    ("cs", "Jste 2 kroky od získání klientů", "Dokončete svůj profil a začněte přijímat poptávky", "Dokončit nastavení", "Jste 1 krok od získání klientů", "Přidejte službu a začněte přijímat poptávky", "Přidat službu", "Profil", "Služba"),
    ("da", "Du er 2 skridt fra at få kunder", "Fuldfør din profil for at begynde at modtage forespørgsler", "Fuldfør opsætning", "Du er 1 skridt fra at få kunder", "Tilføj en ydelse for at begynde at modtage forespørgsler", "Tilføj en ydelse", "Profil", "Ydelse"),
    ("de", "Sie sind 2 Schritte davon entfernt, Kunden zu gewinnen", "Vervollständigen Sie Ihr Profil, um Anfragen zu erhalten", "Einrichtung abschließen", "Sie sind 1 Schritt davon entfernt, Kunden zu gewinnen", "Fügen Sie einen Dienst hinzu, um Anfragen zu erhalten", "Dienst hinzufügen", "Profil", "Dienst"),
    ("el", "Είστε 2 βήματα μακριά από τους πρώτους πελάτες σας", "Συμπληρώστε το προφίλ σας για να αρχίσετε να λαμβάνετε αιτήματα", "Ολοκλήρωση ρύθμισης", "Είστε 1 βήμα μακριά από τους πρώτους πελάτες σας", "Προσθέστε μια υπηρεσία για να αρχίσετε να λαμβάνετε αιτήματα", "Προσθήκη υπηρεσίας", "Προφίλ", "Υπηρεσία"),
    ("en", "You're 2 steps away from getting clients", "Complete your profile to start receiving requests", "Complete setup", "You're 1 step away from getting clients", "Add a service to start receiving requests", "Add a service", "Profile", "Service"),
    ("es", "Estás a 2 pasos de conseguir clientes", "Completa tu perfil para empezar a recibir solicitudes", "Completar configuración", "Estás a 1 paso de conseguir clientes", "Añade un servicio para empezar a recibir solicitudes", "Añadir servicio", "Perfil", "Servicio"),
    ("et", "Oled 2 sammu kaugusel esimestest klientidest", "Täida oma profiil, et hakata päringuid vastu võtma", "Lõpeta seadistamine", "Oled 1 sammu kaugusel esimestest klientidest", "Lisa teenus, et hakata päringuid vastu võtma", "Lisa teenus", "Profiil", "Teenus"),
    ("fi", "Olet 2 askeleen päässä ensimmäisistä asiakkaistasi", "Täytä profiilisi saadaksesi pyyntöjä", "Viimeistele asetukset", "Olet 1 askeleen päässä ensimmäisistä asiakkaistasi", "Lisää palvelu saadaksesi pyyntöjä", "Lisää palvelu", "Profiili", "Palvelu"),
    ("fr", "Vous êtes à 2 étapes de vos premiers clients", "Complétez votre profil pour commencer à recevoir des demandes", "Terminer la configuration", "Vous êtes à 1 étape de vos premiers clients", "Ajoutez un service pour commencer à recevoir des demandes", "Ajouter un service", "Profil", "Service"),
    ("ga", "Tá tú 2 chéim ó do chéad chliaint", "Comhlánaigh do phróifíl chun tosaigh ag fáil iarratas", "Críochnaigh an socrú", "Tá tú 1 chéim ó do chéad chliaint", "Cuir seirbhís leis chun tosaigh ag fáil iarratas", "Cuir seirbhís leis", "Próifíl", "Seirbhís"),
    ("hr", "Dva ste koraka od prvih klijenata", "Dovršite profil kako biste počeli primati upite", "Dovrši postavljanje", "Jedan ste korak od prvih klijenata", "Dodajte uslugu kako biste počeli primati upite", "Dodaj uslugu", "Profil", "Usluga"),
    ("hu", "2 lépésre van az első ügyfelektől", "Töltse ki profilját, hogy elkezdjen megkereséseket kapni", "Beállítás befejezése", "1 lépésre van az első ügyfelektől", "Adjon hozzá egy szolgáltatást a megkeresések fogadásához", "Szolgáltatás hozzáadása", "Profil", "Szolgáltatás"),
    ("is", "Þú ert 2 skref frá fyrstu viðskiptavinum", "Fylltu út prófílinn þinn til að byrja að fá beiðnir", "Ljúka uppsetningu", "Þú ert 1 skref frá fyrstu viðskiptavinum", "Bættu við þjónustu til að byrja að fá beiðnir", "Bæta við þjónustu", "Prófíll", "Þjónusta"),
    ("it", "Sei a 2 passi dai tuoi primi clienti", "Completa il tuo profilo per iniziare a ricevere richieste", "Completa la configurazione", "Sei a 1 passo dai tuoi primi clienti", "Aggiungi un servizio per iniziare a ricevere richieste", "Aggiungi servizio", "Profilo", "Servizio"),
    ("lb", "Dir sidd 2 Schrëtt vun Äre Clienten ewech", "Fëllt Äre Profil aus fir Ufroe ze kréien", "Astellung ofschléissen", "Dir sidd 1 Schrëtt vun Äre Clienten ewech", "Füügt e Service bäi fir Ufroe ze kréien", "Service bäifügen", "Profil", "Service"),
    ("lt", "Esate 2 žingsniai nuo pirmųjų klientų", "Užpildykite profilį, kad pradėtumėte gauti užklausas", "Baigti nustatymą", "Esate 1 žingsnis nuo pirmųjų klientų", "Pridėkite paslaugą, kad pradėtumėte gauti užklausas", "Pridėti paslaugą", "Profilis", "Paslauga"),
    ("lv", "Esat 2 soļus attālu no pirmajiem klientiem", "Aizpildiet savu profilu, lai sāktu saņemt pieprasījumus", "Pabeigt iestatīšanu", "Esat 1 soli attālu no pirmajiem klientiem", "Pievienojiet pakalpojumu, lai sāktu saņemt pieprasījumus", "Pievienot pakalpojumu", "Profils", "Pakalpojums"),
    ("mk", "Сте на 2 чекори од вашите први клиенти", "Пополнете го профилот за да почнете да примате барања", "Заврши поставувањето", "Сте на 1 чекор од вашите први клиенти", "Додајте услуга за да почнете да примате барања", "Додај услуга", "Профил", "Услуга"),
    ("mt", "Inti 2 passi 'l bogħod mill-ewwel klijenti tiegħek", "Tlesta l-profil tiegħek biex tibda tirċievi talbiet", "Tlesta l-konfigurazzjoni", "Inti 1 pass 'l bogħod mill-ewwel klijenti tiegħek", "Żid servizz biex tibda tirċievi talbiet", "Żid servizz", "Profil", "Servizz"),
    ("nl", "Je bent 2 stappen verwijderd van je eerste klanten", "Vul je profiel in om aanvragen te ontvangen", "Configuratie voltooien", "Je bent 1 stap verwijderd van je eerste klanten", "Voeg een dienst toe om aanvragen te ontvangen", "Dienst toevoegen", "Profiel", "Dienst"),
    ("no", "Du er 2 steg unna dine første kunder", "Fullfør profilen din for å begynne å motta forespørsler", "Fullfør oppsett", "Du er 1 steg unna dine første kunder", "Legg til en tjeneste for å begynne å motta forespørsler", "Legg til tjeneste", "Profil", "Tjeneste"),
    ("pl", "Jesteś 2 kroki od pierwszych klientów", "Uzupełnij profil, aby zacząć otrzymywać zapytania", "Zakończ konfigurację", "Jesteś 1 krok od pierwszych klientów", "Dodaj usługę, aby zacząć otrzymywać zapytania", "Dodaj usługę", "Profil", "Usługa"),
    ("pt", "Você está a 2 passos de conseguir clientes", "Complete seu perfil para começar a receber solicitações", "Concluir configuração", "Você está a 1 passo de conseguir clientes", "Adicione um serviço para começar a receber solicitações", "Adicionar serviço", "Perfil", "Serviço"),
    ("pt-PT", "Está a 2 passos de conseguir clientes", "Complete o seu perfil para começar a receber pedidos", "Concluir configuração", "Está a 1 passo de conseguir clientes", "Adicione um serviço para começar a receber pedidos", "Adicionar serviço", "Perfil", "Serviço"),
    ("ro", "Ești la 2 pași de primii tăi clienți", "Completează-ți profilul pentru a începe să primești cereri", "Finalizează configurarea", "Ești la 1 pas de primii tăi clienți", "Adaugă un serviciu pentru a începe să primești cereri", "Adaugă serviciu", "Profil", "Serviciu"),
    ("ru", "Вы в 2 шагах от первых клиентов", "Заполните профиль, чтобы начать получать запросы", "Завершить настройку", "Вы в 1 шаге от первых клиентов", "Добавьте услугу, чтобы начать получать запросы", "Добавить услугу", "Профиль", "Услуга"),
    ("sk", "Ste 2 kroky od prvých klientov", "Dokončite profil a začnite prijímať požiadavky", "Dokončiť nastavenie", "Ste 1 krok od prvých klientov", "Pridajte službu a začnite prijímať požiadavky", "Pridať službu", "Profil", "Služba"),
    ("sl", "Ste 2 koraka stran od prvih strank", "Dokončajte profil, da začnete prejemati povpraševanja", "Dokončaj nastavitev", "Ste 1 korak stran od prvih strank", "Dodajte storitev, da začnete prejemati povpraševanja", "Dodaj storitev", "Profil", "Storitev"),
    ("sq", "Jeni 2 hapa larg klientëve të parë", "Plotësoni profilin tuaj për të filluar të merrni kërkesa", "Përfundo konfigurimin", "Jeni 1 hap larg klientëve të parë", "Shtoni një shërbim për të filluar të merrni kërkesa", "Shto shërbim", "Profil", "Shërbim"),
    ("sr", "На 2 корака сте од првих клијената", "Попуните профил да бисте почели да примате упите", "Заврши подешавање", "На 1 корак сте од првих клијената", "Додајте услугу да бисте почели да примате упите", "Додај услугу", "Профил", "Услуга"),
    ("sv", "Du är 2 steg från att få kunder", "Slutför din profil för att börja ta emot förfrågningar", "Slutför inställning", "Du är 1 steg från att få kunder", "Lägg till en tjänst för att börja ta emot förfrågningar", "Lägg till tjänst", "Profil", "Tjänst"),
    ("tr", "Müşterilerinize 2 adım uzaktasınız", "Talep almaya başlamak için profilinizi tamamlayın", "Kurulumu tamamla", "Müşterilerinize 1 adım uzaktasınız", "Talep almaya başlamak için bir hizmet ekleyin", "Hizmet ekle", "Profil", "Hizmet"),
    ("uk", "Ви в 2 кроках від перших клієнтів", "Заповніть профіль, щоб починати отримувати запити", "Завершити налаштування", "Ви в 1 кроці від перших клієнтів", "Додайте послугу, щоб починати отримувати запити", "Додати послугу", "Профіль", "Послуга"),
]

KEYS = ["setup_title", "setup_subtitle", "btn_complete_setup", "setup_title_1step", "setup_subtitle_1step", "btn_add_service", "step_profile", "step_service"]

def seed():
    with engine.begin() as conn:
        count = 0
        for row in ROWS:
            lang = row[0]
            for i, key in enumerate(KEYS):
                conn.execute(text("""
                    INSERT INTO translations (lang, key, value)
                    VALUES (:lang, :key, :value)
                    ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
                """), {"lang": lang, "key": f"provider_dashboard.{key}", "value": row[i + 1]})
                count += 1
        print(f"✅ Seeded {count} rows")

if __name__ == "__main__":
    seed()
