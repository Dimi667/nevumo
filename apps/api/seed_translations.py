# -*- coding: utf-8 -*-
from apps.api.database import SessionLocal, init_db
from apps.api.i18n import (
    MASSAGE_PROVIDER_CATEGORY_KEY,
    provider_category_seed_data,
)
from apps.api.models import Translation, Provider

def seed():
    db = SessionLocal()
    init_db()

    # 1. Добавяне/Обновяване на данните за Мария Петрова
    maria = db.query(Provider).filter_by(business_name="Maria Petrova").first()
    if not maria:
        maria = Provider(business_name="Maria Petrova")
        db.add(maria)
    
    maria.job_title = "job_title_massage" # Използваме ключ за превод вместо твърд низ
    maria.category = MASSAGE_PROVIDER_CATEGORY_KEY
    maria.city = "Sofia"
    maria.rating = 4.9
    maria.jobs_completed = 120
    maria.is_verified = True
    maria.slug = "maria-petrova"

    # 2. Пълен речник с преводи (30 езика)
    translations_data = {
        "bg": {
            "job_title_massage": "Масажист",
            "rating_label": "рейтинг",
            "jobs_label": "завършени поръчки",
            "verified_label": "✓ Потвърден професионалист",
            "phone_label": "Телефон",
            "phone_placeholder": "напр. +359 888 123 456",
            "notes_label": "Бележки",
            "notes_placeholder": "Опишете заявката си (час, адрес, детайли)",
            "response_time": "⏱ Доставчикът обикновено отговаря до 30 минути",
            "button_text": "Заяви услуга",
            "disclaimer": "Безплатна заявка • Без ангажимент",
            "success_title": "✓ Заявката е изпратена!",
            "success_message": "Ще се свържем с вас скоро.",
            "success_message_received": " получи заявката ти и ще се свърже с теб по телефона.",
            "new_request_button": "Нова заявка"
        },
        "en": {
            "job_title_massage": "Massage Therapist",
            "rating_label": "rating",
            "jobs_label": "jobs completed",
            "verified_label": "✓ Verified professional",
            "phone_label": "Phone",
            "phone_placeholder": "e.g. +359 888 123 456",
            "notes_label": "Notes",
            "notes_placeholder": "Describe your request (time, address, details)",
            "response_time": "⏱ Provider usually responds within 30 minutes",
            "button_text": "Request Service",
            "disclaimer": "Free request • No obligation",
            "success_title": "✓ Request sent!",
            "success_message": "We will contact you soon.",
            "success_message_received": " received your request and will contact you by phone.",
            "new_request_button": "New Request"
        },
        "sr": {
            "rating_label": "rejting",
            "jobs_label": "обављених послова",
            "verified_label": "✓ Provereni profesionalac",
            "phone_label": "Telefon",
            "phone_placeholder": "npr. +381...",
            "notes_label": "Napomene",
            "notes_placeholder": "Opišite svoj zahtev (vreme, adresa, detalji)",
            "response_time": "⏱ Pružalac obično odgovara u roku od 30 minuta",
            "button_text": "Zakažite uslugu",
            "disclaimer": "Besplatan zahtev • Bez obaveza",
            "success_title": "✓ Zahtev je poslat!",
            "success_message_received": " je zaprimio/la vaš zahtjev i kontaktiraće vas telefonom."
        },
        "mk": {
            "rating_label": "рејтинг",
            "jobs_label": "завршени работи",
            "verified_label": "✓ Потврден професионалец",
            "phone_label": "Телефон",
            "phone_placeholder": "на пр. +389...",
            "notes_label": "Белешки",
            "notes_placeholder": "Опишете го вашето барање (време, адреса, детали)",
            "response_time": "⏱ Пружателот обично одговара во рок од 30 минути",
            "button_text": "Закажи услуга",
            "disclaimer": "Бесплатно барање • Без обврска",
            "success_title": "✓ Барањето е испратено!",
            "success_message_received": " го прими вашето барање и ќе ве контактира преку телефон."
        },
        "tr": {
            "rating_label": "puan",
            "jobs_label": "tamamlanan iş",
            "verified_label": "✓ Doğrulanmış profesyonel",
            "phone_label": "Telefon",
            "phone_placeholder": "örn. +90...",
            "notes_label": "Notlar",
            "notes_placeholder": "Talebinizi açıklayın (zaman, adres, detaylar)",
            "response_time": "⏱ Sağlayıcı genellikle 30 dakika içinde yanıt verir",
            "button_text": "Hizmet Talep Et",
            "disclaimer": "Ücretsiz talep • Yükümlülük yok",
            "success_title": "✓ İstek gönderildi!",
            "success_message_received": " talebinizi aldı, sizinle telefonla iletişime geçecek."
        },
        "da": {
            "rating_label": "bedømmelse",
            "jobs_label": "fuldførte opgaver",
            "verified_label": "✓ Verificeret professionel",
            "phone_label": "Telefon",
            "phone_placeholder": "f.eks. +45...",
            "notes_label": "Noter",
            "notes_placeholder": "Beskriv din anmodning (tid, adresse, detaljer)",
            "response_time": "⏱ Udbyderen svarer normalt inden for 30 minutter",
            "button_text": "Bestil service",
            "disclaimer": "Gratis anmodning • Ingen forpligtelse",
            "success_title": "✓ Anmodningen er sendt!",
            "success_message_received": " har modtaget din anmodning og vil kontakte dig via telefon."
        },
        "no": {
            "rating_label": "vurdering",
            "jobs_label": "fullførte jobber",
            "verified_label": "✓ Verifisert profesjonell",
            "phone_label": "Telefon",
            "phone_placeholder": "f.eks. +47...",
            "notes_label": "Notater",
            "notes_placeholder": "Beskriv forespørselen din (tid, adresse, detaljer)",
            "response_time": "⏱ Leverandøren svarer vanligvis innen 30 minutter",
            "button_text": "Be om tjeneste",
            "disclaimer": "Gratis forespørsel • Ingen forpliktelse",
            "success_title": "✓ Forespørsel sendt!",
            "success_message_received": " har mottatt din forespørsel og vil kontakte deg per telefon.",
        },
        "de": {
            "rating_label": "Bewertung",
            "jobs_label": "abgeschlossene Jobs",
            "verified_label": "✓ Verifizierter Profi",
            "phone_label": "Telefon",
            "phone_placeholder": "z.B. +49...",
            "notes_label": "Notizen",
            "notes_placeholder": "Beschreiben Sie Ihre Anfrage (Zeit, Adresse, Details)",
            "response_time": "⏱ Anbieter antwortet in der Regel innerhalb von 30 Minuten",
            "button_text": "Dienstleistung anfordern",
            "disclaimer": "Kostenlose Anfrage • Unverbindlich",
            "success_title": "✓ Anfrage gesendet!",
            "success_message_received": " hat Ihre Anfrage erhalten und wird Sie telefonisch kontaktieren.",
        },
        "fr": {
            "rating_label": "note",
            "jobs_label": "missions terminées",
            "verified_label": "✓ Professionnel vérifié",
            "phone_label": "Téléphone",
            "phone_placeholder": "ex. +33...",
            "notes_label": "Notes",
            "notes_placeholder": "Décrivez votre demande (heure, adresse, détails)",
            "response_time": "⏱ Le prestataire répond généralement sous 30 minutes",
            "button_text": "Demander un service",
            "disclaimer": "Demande gratuite • Sans engagement",
            "success_title": "✓ Demande envoyée !",
            "success_message_received": " a reçu votre demande et vous contactera par téléphone.",
        },
        "it": {
            "rating_label": "valutazione",
            "jobs_label": "lavori completati",
            "verified_label": "✓ Professionista verificato",
            "phone_label": "Telefono",
            "phone_placeholder": "es. +39...",
            "notes_label": "Note",
            "notes_placeholder": "Descrivi la tua richiesta (orario, indirizzo, dettagli)",
            "response_time": "⏱ Il fornitore risponde solitamente entro 30 minuti",
            "button_text": "Richiedi servizio",
            "disclaimer": "Richiesta gratuita • Senza impegno",
            "success_title": "✓ Richiesta inviata!",
            "success_message_received": " ha ricevuto la tua richiesta e ti contatterà telefonicamente.",
        },
        "es": {
            "rating_label": "calificación",
            "jobs_label": "trabajos completados",
            "verified_label": "✓ Profesional verificado",
            "phone_label": "Teléfono",
            "phone_placeholder": "ej. +34...",
            "notes_label": "Notas",
            "notes_placeholder": "Describa su solicitud (hora, dirección, detalles)",
            "response_time": "⏱ El proveedor suele responder en 30 minutos",
            "button_text": "Solicitar servicio",
            "disclaimer": "Solicitud gratuita • Sin compromiso",
            "success_title": "✓ ¡Solicitud enviada!",
            "success_message_received": " recibió su solicitud y le contactará por teléfono.",
        },
        "pt": {
            "rating_label": "avaliação",
            "jobs_label": "trabalhos concluídos",
            "verified_label": "✓ Profissional verificado",
            "phone_label": "Telefone",
            "phone_placeholder": "ex. +351...",
            "notes_label": "Notas",
            "notes_placeholder": "Descreva o seu pedido (hora, morada, detalhes)",
            "response_time": "⏱ O provedor costuma responder em 30 minutos",
            "button_text": "Solicitar serviço",
            "disclaimer": "Pedido gratuito • Sem compromisso",
            "success_title": "✓ Solicitação enviada!",
            "success_message_received": " recebeu sua solicitação e entrará em contato por telefone."
        },
        "nl": {
            "rating_label": "beoordeling",
            "jobs_label": "voltooide opdrachten",
            "verified_label": "✓ Geverifieerde professional",
            "phone_label": "Telefoon",
            "phone_placeholder": "bijv. +31...",
            "notes_label": "Notities",
            "notes_placeholder": "Beschrijf je verzoek (tijd, adres, details)",
            "response_time": "⏱ Aanbieder reageert meestal binnen 30 minuten",
            "button_text": "Service aanvragen",
            "disclaimer": "Gratis aanvraag • Geen verplichting",
            "success_title": "✓ Aanvraag verzonden!",
            "success_message_received": " heeft uw aanvraag ontvangen en neemt telefonisch contact op.",
        },
        "pl": {
            "rating_label": "ocena",
            "jobs_label": "ukończone zlecenia",
            "verified_label": "✓ Zweryfikowany profesjonalista",
            "phone_label": "Telefon",
            "phone_placeholder": "np. +48...",
            "notes_label": "Notatki",
            "notes_placeholder": "Opisz swoją prośbę (czas, adres, szczegóły)",
            "response_time": "⏱ Dostawca zazwyczaj odpowiada w ciągu 30 minut",
            "button_text": "Zamów usługę",
            "disclaimer": "Bezpłatne zapytanie • Bez zobowiązań",
            "success_title": "✓ Prośba została wysłana!",
            "success_message_received": " otrzymał(a) Twoje zgłoszenie i skontaktuje się telefonicznie."
        },
        "cs": {
            "rating_label": "hodnocení",
            "jobs_label": "dokončených prací",
            "verified_label": "✓ Ověřený profesionál",
            "phone_label": "Telefon",
            "phone_placeholder": "např. +420...",
            "notes_label": "Poznámky",
            "notes_placeholder": "Popište svůj požadavek (čas, adresa, podrobnosti)",
            "response_time": "⏱ Poskytovatel obvykle odpovídá do 30 minut",
            "button_text": "Objednat službu",
            "disclaimer": "Bezplatná žádost • Bez závazků",
            "success_title": "✓ Žádost byla odeslána!",
            "success_message_received": " přijal(a) vaši žádost a kontaktuje vás telefonicky."
        },
        "sk": {
            "rating_label": "hodnotenie",
            "jobs_label": "dokončených prác",
            "verified_label": "✓ Overený profesionál",
            "phone_label": "Telefón",
            "phone_placeholder": "napr. +421...",
            "notes_label": "Poznámky",
            "notes_placeholder": "Popíšte svoju požiadavku (čas, adresa, podrobnosti)",
            "response_time": "⏱ Poskytovateľ zvyčajne odpovedá do 30 minút",
            "button_text": "Objednať službu",
            "disclaimer": "Bezplatná žiadosť • Bez záväzkov",
            "success_title": "✓ Žiadosť bola odoslaná!",
            "success_message_received": " prijal(a) vašu žiadosť a bude vás kontaktovať telefonicky."
        },
        "hu": {
            "rating_label": "értékelés",
            "jobs_label": "elvégzett munka",
            "verified_label": "✓ Ellenőrzött szakember",
            "phone_label": "Telefon",
            "phone_placeholder": "pl. +36...",
            "notes_label": "Jegyzetek",
            "notes_placeholder": "Írja le kérését (időpont, cím, részletek)",
            "response_time": "⏱ A szolgáltató általában 30 percen belül válaszol",
            "button_text": "Szolgáltatás igénylése",
            "disclaimer": "Ingyenes kérés • Kötelezettség nélkül",
            "success_title": "✓ Kérés elküldve!",
            "success_message_received": " megkapta a kérését, és telefonon felveszi Önnel a kapcsolatot."
        },
        "ro": {
            "rating_label": "evaluare",
            "jobs_label": "lucrări finalizate",
            "verified_label": "✓ Profesionist verificat",
            "phone_label": "Telefon",
            "phone_placeholder": "ex. +40...",
            "notes_label": "Note",
            "notes_placeholder": "Descrieți cererea (ora, adresa, detalii)",
            "response_time": "⏱ Furnizorul răspunde de obicei în 30 de minute",
            "button_text": "Solicită serviciu",
            "disclaimer": "Cerere gratuită • Fără obligații",
            "success_title": "✓ Cererea a fost trimisă!",
            "success_message_received": " a primit cererea dumneavoastră și vă va contacta telefonic."
        },
        "sv": {
            "rating_label": "betyg",
            "jobs_label": "utförda jobb",
            "verified_label": "✓ Verifierad professionell",
            "phone_label": "Telefon",
            "phone_placeholder": "t.ex. +46...",
            "notes_label": "Anteckningar",
            "notes_placeholder": "Beskriv din förfrågan (tid, adresse, detaljer)",
            "response_time": "⏱ Leverantören svarar vanligtvis inom 30 minuter",
            "button_text": "Beställ tjänst",
            "disclaimer": "Gratis förfrågan • Inga förpliktelser",
            "success_title": "✓ Begäran har skickats!",
            "success_message_received": " har tagit emot din begäran och kontaktar dig per telefon."
        },
        "fi": {
            "rating_label": "arvio",
            "jobs_label": "suoritettua työtä",
            "verified_label": "✓ Vahvistettu ammattilainen",
            "phone_label": "Puhelin",
            "phone_placeholder": "esim. +358...",
            "notes_label": "Muistiinpanot",
            "notes_placeholder": "Kuvaile pyyntösi (aika, osoite, tiedot)",
            "response_time": "⏱ Palveluntarjoaja vastaa yleensä 30 minuutissa",
            "button_text": "Pyydä palvelua",
            "disclaimer": "Ilmainen pyyntö • Ei sitoumusta",
            "success_title": "✓ Pyyntö lähetetty!",
            "success_message_received": " on vastaanottanut pyyntösi ja ottaa sinuun yhteyttä puhelimitse."
        },
        "et": {
            "rating_label": "hinnang",
            "jobs_label": "tehtud tööd",
            "verified_label": "✓ Kinnitatud professionaal",
            "phone_label": "Telefon",
            "phone_placeholder": "nt. +372...",
            "notes_label": "Märkmed",
            "notes_placeholder": "Kirjeldage oma soovi (aeg, aadress, üksikasjad)",
            "response_time": "⏱ Pakkuja vastab tavaliselt 30 minuti jooksul",
            "button_text": "Telli teenus",
            "disclaimer": "Tasuta päring • Ilma kohustuseta",
            "success_title": "✓ Päring on saadetud!",
            "success_message_received": " sai teie päringu kätte ja võtab teiega ühendust telefoni teel."
        },
        "lv": {
            "rating_label": "vērtējums",
            "jobs_label": "pabeigti darbi",
            "verified_label": "✓ Verificēts profesionālis",
            "phone_label": "Tālrunis",
            "phone_placeholder": "piem. +371...",
            "notes_label": "Piezīmes",
            "notes_placeholder": "Aprakstiet savu pieprasījumu (laiks, adrese, detaļas)",
            "response_time": "⏱ Pakalpojuma sniedzējs parasti atbild 30 minūšu laikā",
            "button_text": "Pieteikties pakalpojumam",
            "disclaimer": "Bezmaksas pieprasījums • Bez saistībām",
            "success_title": "✓ Pieprasījums nosūtīts!",
            "success_message_received": " saņēma jūsu pieprasījumu un sazināsies ar jums pa tālruni."
        },
        "lt": {
            "rating_label": "įvertinimas",
            "jobs_label": "atlikti darbai",
            "verified_label": "✓ Patvirtintas profesionalas",
            "phone_label": "Telefonas",
            "phone_placeholder": "pvz. +370...",
            "notes_label": "Užrašai",
            "notes_placeholder": "Aprašykite savo užklausą (laikas, adresas, detalės)",
            "response_time": "⏱ Teikėjas paprastai atsako per 30 minučių",
            "button_text": "Užsakyti paslaugą",
            "disclaimer": "Nemokama užklausa • Be įsipareigojimų",
            "success_title": "✓ Užklausa išsiųsta!",
            "success_message_received": " gavo jūsų užklausą ir susisieks su jumis telefonu."
        },
        "sl": {
            "rating_label": "ocena",
            "jobs_label": "opravljenih del",
            "verified_label": "✓ Preverjen strokovnjak",
            "phone_label": "Telefon",
            "phone_placeholder": "npr. +386...",
            "notes_label": "Opombe",
            "notes_placeholder": "Opišite svojo zahtevo (čas, naslov, podrobnosti)",
            "response_time": "⏱ Ponudnik običajno odgovori v 30 minutah",
            "button_text": "Naroči storitev",
            "disclaimer": "Brezplačna zahteva • Brez obveznosti",
            "success_title": "✓ Zahtevek je poslan!",
            "success_message_received": " je prejel(a) vaš zahtevek in vas bo kontaktiral(a) po telefonu."
        },
        "hr": {
            "rating_label": "ocjena",
            "jobs_label": "dovršenih poslova",
            "verified_label": "✓ Provjereni profesionalac",
            "phone_label": "Telefon",
            "phone_placeholder": "npr. +385...",
            "notes_label": "Napomene",
            "notes_placeholder": "Opišite svoj zahtjev (vrijeme, adresa, detalji)",
            "response_time": "⏱ Pružatelj obično odgovara u roku od 30 minuta",
            "button_text": "Zatražite uslugu",
            "disclaimer": "Besplatan upit • Bez obaveza",
            "success_title": "✓ Zahtjev je poslan!",
            "success_message_received": " je zaprimio/la vaš zahtjev i kontaktirat će vas telefonom."
        },
        "el": {
            "rating_label": "βαθμολογία",
            "jobs_label": "ολοκληρωμένες εργασίες",
            "verified_label": "✓ Επαληθευμένος επαγγελματίας",
            "phone_label": "Τηλέφωνο",
            "phone_placeholder": "π.χ. +30...",
            "notes_label": "Σημειώσεις",
            "notes_placeholder": "Περιγράψτε το αίτημά σας (ώρα, διεύθυνση, λεπτομέρειες)",
            "response_time": "⏱ Ο πάροχος απαντά συνήθως εντός 30 λεπτών",
            "button_text": "Ζητήστε υπηρεσία",
            "disclaimer": "Δωρεάν αίτημα • Χωρίς υποχρέωση",
            "success_title": "✓ Το αίτημα εστάλη!",
            "success_message_received": " έλαβε το αίτημά σας και θα επικοινωνήσει μαζί σας τηλεφωνικά."
        },
        "ga": {
            "rating_label": "rátáil",
            "jobs_label": "poist críochnaithe",
            "verified_label": "✓ Gairmí fíoraithe",
            "phone_label": "Fón",
            "phone_placeholder": "m.sh. +353...",
            "notes_label": "Nótaí",
            "notes_placeholder": "Déan cur síos ar d'iarratas (am, seoladh, sonraí)",
            "response_time": "⏱ Freagraíonn an soláthraí de ghnáth laistigh de 30 nóiméad",
            "button_text": "Iarr seirbhís",
            "disclaimer": "Iarratas saor in aisce • Gan oibleagáid",
            "success_title": "✓ Iarratas seolta!",
            "success_message_received": " a fuair d'iarratas agus déanfaimid teagmháil leat ar an bhfón."
        },
        "mt": {
            "rating_label": "klassifikazzjoni",
            "jobs_label": "xogħlijiet lesti",
            "verified_label": "✓ Professjonist ivverifikat",
            "phone_label": "Telefon",
            "phone_placeholder": "eż. +356...",
            "notes_label": "Noti",
            "notes_placeholder": "Iddeskrivi t-talba tiegħek (ħin, indirizz, dettalji)",
            "response_time": "⏱ Il-fornitur normalment iwieġeb fi żmien 30 minuta",
            "button_text": "Itlob servizz",
            "disclaimer": "Talba b'xejn • L-ebda obbligu",
            "success_title": "✓ It-talba ntbagħtet!",
            "success_message_received": " irċieva t-talba tiegħek u se jikkuntattjak bit-telefown."
        },
        "sq": {
            "rating_label": "rating",
            "jobs_label": "punë të kryera",
            "verified_label": "✓ Profesionist i verifikuar",
            "phone_label": "Numri i telefonit",
            "phone_placeholder": "p.sh. +355...",
            "notes_label": "Shënime",
            "notes_placeholder": "p.sh. më telefononi pas orës 14:00...",
            "response_time": "⏱ Zakonisht përgjigjet brenda 30 minutave",
            "button_text": "Kërko shërbim",
            "disclaimer": "Kërkesë falas • Pa obligim",
            "success_title": "✓ Kërkesa u dërgua!",
            "success_message_received": " e mori kërkesën tuaj dhe do t'ju kontaktojë në telefon."
        },
        "pt-PT": {
            "rating_label": "avaliação",
            "jobs_label": "trabalhos concluídos",
            "verified_label": "✓ Profissional verificado",
            "phone_label": "Telemóvel",
            "phone_placeholder": "ex. +351...",
            "notes_label": "Notas",
            "notes_placeholder": "Descreva o seu pedido (hora, morada, detalhes)",
            "response_time": "⏱ O prestador responde geralmente em 30 minutos",
            "button_text": "Solicitar serviço",
            "disclaimer": "Pedido gratuito • Sem compromisso",
            "success_title": "✓ Pedido enviado!",
            "success_message_received": " recebeu o seu pedido e entrará em contacto por telefone."
        },
        "uk": {
            "rating_label": "рейтинг",
            "jobs_label": "завершені роботи",
            "verified_label": "✓ Перевірений професіонал",
            "phone_label": "Телефон",
            "phone_placeholder": "напр. +380...",
            "notes_label": "Нотатки",
            "notes_placeholder": "Опишіть ваш запит (час, адрес, деталі)",
            "response_time": "⏱ Постачальник зазвичай відповідає протягом 30 хвилин",
            "button_text": "Замовити послугу",
            "disclaimer": "Безкоштовний запит • Без зобов'язань",
            "success_title": "✓ Запит надіслано!",
            "success_message_received": " отримав(ла) вашу заявку і зв'яжеться з вами по телефону."
        },
        "ru": {
            "rating_label": "рейтинг",
            "jobs_label": "выполненные работы",
            "verified_label": "✓ Проверенный профессионал",
            "phone_label": "Телефон",
            "phone_placeholder": "напр. +7...",
            "notes_label": "Заметки",
            "notes_placeholder": "Опишите ваш запрос (время, адрес, детали)",
            "response_time": "⏱ Поставщик обычно отвечает в течение 30 минут",
            "button_text": "Заказать услугу",
            "disclaimer": "Бесплатный запрос • Без обязательств",
            "success_title": "✓ Запрос отправлен!",
            "success_message_received": " получил(а) вашу заявку и свяжется с вами по телефону."
        },
        "is": {
            "rating_label": "einkunn",
            "jobs_label": "lokað verkefni",
            "verified_label": "✓ Staðfestur atvinnurekstur",
            "phone_label": "Sími",
            "phone_placeholder": "t.d. +354...",
            "notes_label": "Athugasemdir",
            "notes_placeholder": "Lýsið beiðni þína (tími, heimilisfang, nánar)",
            "response_time": "⏱ Þjónustuveitandi svarar venjulega innan 30 mínútna",
            "button_text": "Pækja þjónustu",
            "disclaimer": "Ókeypis beiðni • Ábyrgðalaust",
            "success_title": "✓ Beiðni send!",
            "success_message_received": " hefur móttekið beiðni þína og mun hafa samband í síma."
        },
        "lb": {
            "rating_label": "Bewertung",
            "jobs_label": "fäerdeg Aufgaben",
            "verified_label": "✓ Verifizéierte Beruffsberuffer",
            "phone_label": "Telefon",
            "phone_placeholder": "z.B. +352...",
            "notes_label": "Notizen",
            "notes_placeholder": "Beschreiwen Är Ufro (Zäit, Adress, Detailer)",
            "response_time": "⏱ Ubidder reagéiert normalerweis bann 30 Minutten",
            "button_text": "Service ufroen",
            "disclaimer": "Käschent Ufro • oun Verflichtung",
            "success_title": "✓ Demande geschéckt!",
            "success_message_received": " huet Är Demande kritt a kontaktéiert Iech iwwer Telefon."
        }
    }

    for lang, category_keys in provider_category_seed_data().items():
        translations_data.setdefault(lang, {}).update(category_keys)

    # 3. Изпълнение на записа в базата
    for lang, keys in translations_data.items():
        for key, value in keys.items():
            exists = db.query(Translation).filter_by(lang=lang, key=key).first()
            if exists:
                exists.value = value
            else:
                db.add(Translation(lang=lang, key=key, value=value))

    db.commit()
    db.close()
    print("✅ Успешно заредени 30 езика и преводите за categories!")

if __name__ == "__main__":
    seed()
