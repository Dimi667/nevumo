"""
seed_terms_p11_bodies.py  —  Nevumo | namespace: terms
Key: art11_body (34 езика)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_terms_p11_bodies
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://nevumo:nevumo@postgres:5432/nevumo_leads",
)

NAMESPACE = "terms"

TRANSLATIONS: dict[str, dict[str, str]] = {
    "art11_body": {
        "en": (
            '11.1 If you have a complaint about the platform or a provider interaction '
            'facilitated by Nevumo, contact us at privacy@nevumo.com with a description '
            'of the issue.\n\n'
            '11.2 Nevumo will acknowledge your complaint within 5 business days and provide '
            'a substantive response within 14 calendar days.\n\n'
            '11.3 [PL] Polish consumers may also submit complaints directly to Nevumo under '
            'the procedures required by the PKE and the CRA. Response within 14 days is '
            'mandatory; failure to respond is deemed acceptance of the complaint.'
        ),
        "pl": (
            '11.1 Reklamacje dotyczące działania platformy Nevumo należy kierować na adres '
            'privacy@nevumo.com z opisem problemu.\n\n'
            '11.2 Nevumo potwierdzi otrzymanie reklamacji w terminie 5 dni roboczych i '
            'udzieli odpowiedzi merytorycznej w terminie 14 dni kalendarzowych od dnia '
            'otrzymania reklamacji.\n\n'
            '11.3 Brak odpowiedzi w terminie 14 dni jest równoznaczny z uznaniem reklamacji '
            'zgodnie z art. 7a ustawy o prawach konsumenta.\n\n'
            '11.4 Klient będący konsumentem może skorzystać z pozasądowych sposobów '
            'rozpatrywania reklamacji opisanych w §12 niniejszego Regulaminu.'
        ),
        "bg": (
            '11.1 Рекламации относно работата на платформата се подават на '
            'privacy@nevumo.com с описание на проблема.\n\n'
            '11.2 Nevumo потвърждава получаването на рекламацията в срок от 5 работни дни '
            'и предоставя отговор по същество в срок от 14 календарни дни.\n\n'
            '11.3 [PL] Полските потребители могат да подават рекламации по реда на PKE '
            'и CRA. Неотговарянето в срок от 14 дни се счита за приемане на рекламацията.'
        ),
        "cs": (
            '11.1 Pokud máte stížnost ohledně platformy nebo interakce s poskytovatelem, '
            'kontaktujte nás na privacy@nevumo.com s popisem problému.\n\n'
            '11.2 Nevumo potvrdí přijetí vaší stížnosti do 5 pracovních dnů a poskytne '
            'věcnou odpověď do 14 kalendářních dnů.\n\n'
            '11.3 [PL] Polští spotřebitelé mohou podávat stížnosti podle postupů PKE '
            'a CRA. Neodpovězení do 14 dnů se považuje za přijetí stížnosti.'
        ),
        "da": (
            '11.1 Hvis du har en klage over platformen eller en leverandørinteraktion, '
            'kontakt os på privacy@nevumo.com med en beskrivelse af problemet.\n\n'
            '11.2 Nevumo bekræfter modtagelsen af din klage inden for 5 arbejdsdage og '
            'giver et substantielt svar inden for 14 kalenderdage.\n\n'
            '11.3 [PL] Polske forbrugere kan også indgive klager i henhold til PKE og CRA. '
            'Manglende svar inden 14 dage anses som accept af klagen.'
        ),
        "de": (
            '11.1 Bei Beschwerden über die Plattform oder eine durch Nevumo vermittelte '
            'Anbieterinteraktion wenden Sie sich an privacy@nevumo.com mit einer '
            'Beschreibung des Problems.\n\n'
            '11.2 Nevumo bestätigt den Eingang Ihrer Beschwerde innerhalb von 5 '
            'Werktagen und gibt eine inhaltliche Antwort innerhalb von 14 Kalendertagen.\n\n'
            '11.3 [PL] Polnische Verbraucher können Beschwerden auch gemäß PKE und CRA '
            'einreichen. Eine fehlende Antwort innerhalb von 14 Tagen gilt als Annahme.'
        ),
        "el": (
            '11.1 Για παράπονα σχετικά με την πλατφόρμα ή αλληλεπίδραση με πάροχο, '
            'επικοινωνήστε μαζί μας στο privacy@nevumo.com με περιγραφή του ζητήματος.\n\n'
            '11.2 Το Nevumo θα επιβεβαιώσει το παράπονό σας εντός 5 εργάσιμων ημερών '
            'και θα δώσει ουσιαστική απάντηση εντός 14 ημερολογιακών ημερών.\n\n'
            '11.3 [PL] Οι Πολωνοί καταναλωτές μπορούν να υποβάλλουν παράπονα βάσει '
            'PKE και CRA. Η μη απάντηση εντός 14 ημερών θεωρείται αποδοχή.'
        ),
        "es": (
            '11.1 Si tiene una reclamación sobre la plataforma o una interacción con un '
            'proveedor, contáctenos en privacy@nevumo.com con una descripción del problema.\n\n'
            '11.2 Nevumo acusará recibo de su reclamación en 5 días hábiles y proporcionará '
            'una respuesta sustantiva en 14 días naturales.\n\n'
            '11.3 [PL] Los consumidores polacos pueden presentar reclamaciones según PKE '
            'y CRA. La falta de respuesta en 14 días se considera aceptación.'
        ),
        "et": (
            '11.1 Kui teil on kaebus platvormi või Nevumo vahendatud teenusepakkuja '
            'suhtluse kohta, võtke meiega ühendust aadressil privacy@nevumo.com.\n\n'
            '11.2 Nevumo kinnitab kaebuse kättesaamist 5 tööpäeva jooksul ja esitab '
            'sisulise vastuse 14 kalendripäeva jooksul.\n\n'
            '11.3 [PL] Poola tarbijad võivad esitada kaebusi vastavalt PKE ja CRA '
            'menetlustele. Vastamata jätmine 14 päeva jooksul loetakse kaebuse '
            'aktsepteerimiseks.'
        ),
        "fi": (
            '11.1 Jos sinulla on valitus alustasta tai palveluntarjoajan vuorovaikutuksesta, '
            'ota meihin yhteyttä osoitteessa privacy@nevumo.com ongelman kuvauksella.\n\n'
            '11.2 Nevumo kuittaa valituksesi 5 arkipäivän kuluessa ja antaa asiallisen '
            'vastauksen 14 kalenteripäivän kuluessa.\n\n'
            '11.3 [PL] Puolalaiset kuluttajat voivat jättää valituksia PKE:n ja CRA:n '
            'mukaisesti. Vastaamattomuus 14 päivän kuluessa katsotaan valituksen '
            'hyväksymiseksi.'
        ),
        "fr": (
            '11.1 Si vous avez une réclamation concernant la plateforme ou une interaction '
            'avec un prestataire facilitée par Nevumo, contactez-nous à privacy@nevumo.com '
            'avec une description du problème.\n\n'
            '11.2 Nevumo accusera réception de votre réclamation dans les 5 jours ouvrables '
            'et fournira une réponse de fond dans les 14 jours calendaires.\n\n'
            '11.3 [PL] Les consommateurs polonais peuvent soumettre des réclamations selon '
            'les procédures PKE et CRA. L\'absence de réponse dans les 14 jours est '
            'réputée acceptation.'
        ),
        "ga": (
            '11.1 Má tá gearán agat faoin ardán nó idirghníomhú le soláthróir, déan '
            'teagmháil linn ag privacy@nevumo.com le cur síos ar an gceist.\n\n'
            '11.2 Admhóidh Nevumo do ghearán laistigh de 5 lá oibre agus cuirfidh sé '
            'freagra substainteach ar fáil laistigh de 14 lá féilire.\n\n'
            '11.3 [PL] Féadfaidh tomhaltóirí Polannach gearáin a chur isteach de réir '
            'nósanna imeachta PKE agus CRA. Meastar nach bhfuil freagra laistigh de '
            '14 lá mar ghlacadh.'
        ),
        "hr": (
            '11.1 Ako imate pritužbu na platformu ili interakciju s davateljem, '
            'kontaktirajte nas na privacy@nevumo.com s opisom problema.\n\n'
            '11.2 Nevumo će potvrditi primitak vaše pritužbe u roku od 5 radnih dana '
            'i dati sadržajan odgovor u roku od 14 kalendarskih dana.\n\n'
            '11.3 [PL] Poljski potrošači mogu podnositi pritužbe prema postupcima PKE '
            'i CRA. Nedavanje odgovora u 14 dana smatra se prihvaćanjem pritužbe.'
        ),
        "hu": (
            '11.1 Ha panasza van a platformmal vagy egy Nevumo által közvetített '
            'szolgáltatói interakcióval kapcsolatban, lépjen kapcsolatba velünk a '
            'privacy@nevumo.com címen a probléma leírásával.\n\n'
            '11.2 A Nevumo 5 munkanapon belül visszaigazolja panaszát, és 14 naptári '
            'napon belül érdemi választ ad.\n\n'
            '11.3 [PL] A lengyel fogyasztók a PKE és a CRA eljárásai szerint is '
            'benyújthatnak panaszt. A 14 napon belüli válasz elmaradása elfogadásnak minősül.'
        ),
        "is": (
            '11.1 Ef þú hefur kvörtun varðandi vettvanginn eða samskipti við '
            'þjónustuaðila, hafðu samband við okkur á privacy@nevumo.com með lýsingu.\n\n'
            '11.2 Nevumo staðfestir kvörtunina innan 5 virkra daga og gefur efnislegt '
            'svar innan 14 almanaksdaga.\n\n'
            '11.3 [PL] Pólskir neytendur geta einnig lagt fram kvartanir samkvæmt '
            'PKE og CRA. Að svara ekki innan 14 daga telst vera samþykki.'
        ),
        "it": (
            '11.1 Se hai un reclamo riguardo alla piattaforma o a un\'interazione con un '
            'prestatore facilitata da Nevumo, contattaci a privacy@nevumo.com con una '
            'descrizione del problema.\n\n'
            '11.2 Nevumo accuserà ricevuta del tuo reclamo entro 5 giorni lavorativi e '
            'fornirà una risposta sostanziale entro 14 giorni di calendario.\n\n'
            '11.3 [PL] I consumatori polacchi possono presentare reclami secondo le '
            'procedure PKE e CRA. La mancata risposta entro 14 giorni è ritenuta accettazione.'
        ),
        "lb": (
            '11.1 Wann Dir eng Beschwerd iwwer d\'Plattform oder eng Prestatairinteraktioun '
            'hutt, kontaktéiert eis op privacy@nevumo.com mat enger Beschreiwung.\n\n'
            '11.2 Nevumo bestätegt d\'Beschwerd innerhalb vu 5 Aarbechtsdeeg an gëtt '
            'eng inhaltlech Äntwert innerhalb vu 14 Kalennerdaag.\n\n'
            '11.3 [PL] Polnesch Konsumenten kënnen Beschwerden no PKE a CRA Prozeduren '
            'aschreiwen. Keng Äntwert innerhalb 14 Deeg gëlt als Akzeptanz.'
        ),
        "lt": (
            '11.1 Jei turite skundą dėl platformos ar paslaugų teikėjo sąveikos, '
            'susisiekite su mumis adresu privacy@nevumo.com su problemos aprašymu.\n\n'
            '11.2 Nevumo patvirtins skundo gavimą per 5 darbo dienas ir pateiks '
            'esminį atsakymą per 14 kalendorinių dienų.\n\n'
            '11.3 [PL] Lenkijos vartotojai taip pat gali pateikti skundus pagal PKE ir '
            'CRA procedūras. Neatsakymas per 14 dienų laikomas skundu priimtu.'
        ),
        "lv": (
            '11.1 Ja jums ir sūdzība par platformu vai Nevumo starpniecībā notikušu '
            'mijiedarbību ar sniedzēju, sazinieties ar mums pa privacy@nevumo.com.\n\n'
            '11.2 Nevumo apliecinās sūdzības saņemšanu 5 darba dienu laikā un sniegs '
            'saturīgu atbildi 14 kalendāro dienu laikā.\n\n'
            '11.3 [PL] Polijas patērētāji var iesniegt sūdzības arī saskaņā ar PKE '
            'un CRA procedūrām. Neatbildēšana 14 dienu laikā tiek uzskatīta par '
            'sūdzības pieņemšanu.'
        ),
        "mk": (
            '11.1 Ако имате рекламација за платформата или интеракција со Давател, '
            'контактирајте не на privacy@nevumo.com со опис на проблемот.\n\n'
            '11.2 Nevumo ќе ја потврди рекламацијата во рок од 5 работни дена и ќе '
            'даде суштински одговор во рок од 14 календарски дена.\n\n'
            '11.3 [PL] Полските потрошувачи можат да поднесат рекламации по PKE и '
            'CRA процедурите. Неодговарањето во 14 дена се смета за прифаќање.'
        ),
        "mt": (
            '11.1 Jekk għandek ilment dwar il-pjattaforma jew interazzjoni ma\' fornitur, '
            'ikkuntattjana fuq privacy@nevumo.com b\'deskrizzjoni tal-problema.\n\n'
            '11.2 Nevumo jirrikonoxxi l-ilment tiegħek fi żmien 5 ijiem tax-xogħol u '
            'jipprovdi risposta sostantiva fi żmien 14-il jum tal-kalendarju.\n\n'
            '11.3 [PL] Il-konsumaturi Pollakki jistgħu jissottomettu lmenti skont '
            'il-proċeduri PKE u CRA. Nuqqas ta\' risposta fi żmien 14-il jum jitqies '
            'bħala aċċettazzjoni.'
        ),
        "nl": (
            '11.1 Als u een klacht heeft over het platform of een door Nevumo gefaciliteerde '
            'providerinteractie, neem dan contact met ons op via privacy@nevumo.com met '
            'een beschrijving van het probleem.\n\n'
            '11.2 Nevumo bevestigt uw klacht binnen 5 werkdagen en geeft een inhoudelijk '
            'antwoord binnen 14 kalenderdagen.\n\n'
            '11.3 [PL] Poolse consumenten kunnen ook klachten indienen conform PKE en '
            'CRA-procedures. Geen reactie binnen 14 dagen geldt als aanvaarding.'
        ),
        "no": (
            '11.1 Hvis du har en klage om plattformen eller en leverandørinteraksjon '
            'tilrettelagt av Nevumo, kontakt oss på privacy@nevumo.com med en beskrivelse.\n\n'
            '11.2 Nevumo bekrefter mottak av klagen din innen 5 virkedager og gir et '
            'saklig svar innen 14 kalenderdager.\n\n'
            '11.3 [PL] Polske forbrugere kan også sende inn klager i henhold til PKE '
            'og CRA-prosedyrer. Manglende svar innen 14 dager anses som aksept.'
        ),
        "pt": (
            '11.1 Se tiver uma reclamação sobre a plataforma ou interação com prestador, '
            'contacte-nos em privacy@nevumo.com com uma descrição do problema.\n\n'
            '11.2 O Nevumo acusará recibo da sua reclamação em 5 dias úteis e fornecerá '
            'uma resposta substantiva em 14 dias corridos.\n\n'
            '11.3 [PL] Os consumidores polacos podem apresentar reclamações de acordo '
            'com os procedimentos PKE e CRA. A falta de resposta em 14 dias é considerada '
            'aceitação.'
        ),
        "pt-PT": (
            '11.1 Se tiver uma reclamação sobre a plataforma ou interacção com prestador, '
            'contacte-nos em privacy@nevumo.com com uma descrição do problema.\n\n'
            '11.2 O Nevumo acusará recepção da sua reclamação em 5 dias úteis e fornecerá '
            'uma resposta substantiva em 14 dias de calendário.\n\n'
            '11.3 [PL] Os consumidores polacos podem apresentar reclamações de acordo '
            'com os procedimentos PKE e CRA. A falta de resposta em 14 dias é considerada '
            'aceitação.'
        ),
        "ro": (
            '11.1 Dacă aveți o reclamație privind platforma sau o interacțiune cu un '
            'prestator facilitată de Nevumo, contactați-ne la privacy@nevumo.com cu o '
            'descriere a problemei.\n\n'
            '11.2 Nevumo va confirma primirea reclamației în 5 zile lucrătoare și va '
            'oferi un răspuns substanțial în 14 zile calendaristice.\n\n'
            '11.3 [PL] Consumatorii polonezi pot depune reclamații conform procedurilor '
            'PKE și CRA. Lipsa răspunsului în 14 zile este considerată acceptare.'
        ),
        "ru": (
            '11.1 Если у вас есть жалоба на платформу или взаимодействие с исполнителем, '
            'свяжитесь с нами по адресу privacy@nevumo.com с описанием проблемы.\n\n'
            '11.2 Nevumo подтвердит получение жалобы в течение 5 рабочих дней и даст '
            'содержательный ответ в течение 14 календарных дней.\n\n'
            '11.3 [PL] Польские потребители могут также подавать жалобы в соответствии '
            'с процедурами PKE и CRA. Отсутствие ответа в течение 14 дней '
            'считается принятием жалобы.'
        ),
        "sk": (
            '11.1 Ak máte sťažnosť na platformu alebo interakciu s poskytovateľom, '
            'kontaktujte nás na privacy@nevumo.com s popisom problému.\n\n'
            '11.2 Nevumo potvrdí prijatie vašej sťažnosti do 5 pracovných dní a poskytne '
            'vecnú odpoveď do 14 kalendárnych dní.\n\n'
            '11.3 [PL] Poľskí spotrebitelia môžu podávať sťažnosti podľa postupov PKE '
            'a CRA. Neodpovedzanie do 14 dní sa považuje za akceptáciu.'
        ),
        "sl": (
            '11.1 Če imate pritožbo glede platforme ali ponudnikovega delovanja, '
            'nas kontaktirajte na privacy@nevumo.com z opisom težave.\n\n'
            '11.2 Nevumo bo potrdil prejem pritožbe v 5 delovnih dneh in podal '
            'vsebinski odgovor v 14 koledarskih dneh.\n\n'
            '11.3 [PL] Poljski potrošniki lahko pritožbe vložijo tudi po postopkih PKE '
            'in CRA. Neodgovor v 14 dneh se šteje kot sprejetje pritožbe.'
        ),
        "sq": (
            '11.1 Nëse keni një ankesë për platformën ose ndërveprim me ofrues, '
            'na kontaktoni në privacy@nevumo.com me një përshkrim të problemit.\n\n'
            '11.2 Nevumo do të konfirmojë ankesën tuaj brenda 5 ditëve pune dhe do të '
            'japë një përgjigje thelbësore brenda 14 ditëve kalendarike.\n\n'
            '11.3 [PL] Konsumatorët polakë mund të paraqesin ankesa sipas procedurave '
            'PKE dhe CRA. Mospërgjigjja brenda 14 ditëve konsiderohet pranim.'
        ),
        "sr": (
            '11.1 Ako imate reklamaciju u vezi sa platformom ili interakcijom sa '
            'pružaocem, kontaktirajte nas na privacy@nevumo.com sa opisom problema.\n\n'
            '11.2 Nevumo će potvrditi reklamaciju u roku od 5 radnih dana i dati '
            'sadržajan odgovor u roku od 14 kalendarskih dana.\n\n'
            '11.3 [PL] Poljski potrošači mogu podnositi reklamacije po PKE i CRA '
            'procedurama. Neodgovor u 14 dana smatra se prihvatanjem reklamacije.'
        ),
        "sv": (
            '11.1 Om du har ett klagomål om plattformen eller en leverantörsinteraktion '
            'förmedlad av Nevumo, kontakta oss på privacy@nevumo.com med en beskrivning.\n\n'
            '11.2 Nevumo bekräftar ditt klagomål inom 5 arbetsdagar och ger ett '
            'substantiellt svar inom 14 kalenderdagar.\n\n'
            '11.3 [PL] Polska konsumenter kan också lämna in klagomål enligt PKE och '
            'CRA-procedurerna. Utebliven respons inom 14 dagar anses som godkännande.'
        ),
        "tr": (
            '11.1 Platform veya Nevumo aracılığıyla gerçekleştirilen sağlayıcı '
            'etkileşimiyle ilgili bir şikayetiniz varsa privacy@nevumo.com adresine '
            'sorunun açıklamasıyla ulaşın.\n\n'
            '11.2 Nevumo şikayetinizi 5 iş günü içinde alındığını onaylayacak ve '
            '14 takvim günü içinde esaslı bir yanıt verecektir.\n\n'
            '11.3 [PL] Polonyalı tüketiciler PKE ve CRA prosedürlerine göre de şikayet '
            'sunabilir. 14 gün içinde yanıt verilmemesi şikayetin kabul edilmesi '
            'sayılır.'
        ),
        "uk": (
            '11.1 Якщо у вас є скарга щодо платформи або взаємодії з виконавцем, '
            'зверніться до нас на privacy@nevumo.com з описом проблеми.\n\n'
            '11.2 Nevumo підтвердить отримання скарги протягом 5 робочих днів і надасть '
            'змістовну відповідь протягом 14 календарних днів.\n\n'
            '11.3 [PL] Польські споживачі можуть також подавати скарги відповідно до '
            'процедур PKE та CRA. Відсутність відповіді протягом 14 днів вважається '
            'прийняттям скарги.'
        ),
    },
}


def seed() -> None:
    engine = create_engine(DATABASE_URL, echo=False)
    Session = sessionmaker(bind=engine)

    with Session() as session:
        count = 0
        for key, lang_values in TRANSLATIONS.items():
            db_key = f"{NAMESPACE}.{key}"
            for lang, value in lang_values.items():
                session.execute(
                    text(
                        "INSERT INTO translations (lang, key, value) "
                        "VALUES (:lang, :key, :value) "
                        "ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value"
                    ),
                    {"lang": lang, "key": db_key, "value": value},
                )
                count += 1
        session.commit()
        print(f"✅ seed_terms_p11_bodies: {count} rows upserted ({NAMESPACE}, art11_body × 34 langs)")

    engine.dispose()


if __name__ == "__main__":
    seed()
