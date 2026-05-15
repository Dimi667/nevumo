"""
seed_terms_p7_bodies.py  —  Nevumo | namespace: terms
Key: art7_body (34 езика)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_terms_p7_bodies
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
    "art7_body": {
        "en": (
            '7.1 If you are a consumer (a natural person acting outside the scope of a '
            'professional or trade activity), you have the right to withdraw from a distance '
            'contract with a service provider within 14 calendar days of the conclusion of '
            'the contract, without giving any reason.\n\n'
            '7.2 The right of withdrawal may be lost if the service has been fully performed '
            'before the withdrawal period has expired and you gave your express consent to '
            'performance beginning before the withdrawal period ended.\n\n'
            '7.3 To exercise your right of withdrawal from a service contract, you must inform '
            'the service provider directly. You may use the standard withdrawal form in '
            'Annex 1 to these Terms.\n\n'
            '7.4 [PL] Polish consumers also have the right to withdraw from any contract '
            'concluded with Nevumo for platform services (e.g. a future paid subscription) '
            'under the same 14-day period. To do so, notify Nevumo at privacy@nevumo.com '
            'or use Annex 1.'
        ),
        "pl": (
            '9.1 Klientowi będącemu konsumentem przysługuje prawo do odstąpienia od umowy '
            'zawartej na odległość z Usługodawcą w terminie 14 dni kalendarzowych od dnia '
            'jej zawarcia, bez podawania przyczyny, zgodnie z ustawą z dnia 30 maja 2014 r. '
            'o prawach konsumenta i Dyrektywą 2011/83/UE.\n\n'
            '9.2 Prawo odstąpienia od umowy wygasa przed upływem terminu 14 dni, jeżeli '
            'usługa została w pełni wykonana za wyraźną zgodą konsumenta i po przekazaniu mu '
            'informacji o utracie prawa odstąpienia.\n\n'
            '9.3 W celu odstąpienia od umowy z Usługodawcą należy poinformować Usługodawcę '
            'bezpośrednio. Odstąpienie od umowy z Usługodawcą nie jest objęte Załącznikiem '
            'nr 1 do niniejszego Regulaminu.\n\n'
            '9.4 W celu odstąpienia od umowy zawartej z Nevumo (np. dotyczącej przyszłych '
            'płatnych usług platformy lub subskrypcji), Klient zobowiązany jest powiadomić '
            'Nevumo na adres privacy@nevumo.com lub pisemnie na adres siedziby, z '
            'zachowaniem terminu 14 dni. W tym celu można skorzystać z Załącznika nr 1.'
        ),
        "bg": (
            '7.1 Клиент, действащ като потребител по смисъла на ЗЗП, има право да се откаже '
            'от договор от разстояние с Доставчика в срок от 14 календарни дни от '
            'сключването му, без да посочва причина.\n\n'
            '7.2 Правото на отказ отпада, ако услугата е изпълнена изцяло преди изтичане '
            'на 14-дневния срок с изричното съгласие на потребителя и след уведомяването му '
            'за загубата на правото на отказ.\n\n'
            '7.3 За упражняване на правото на отказ от договор с Доставчика, Клиентът трябва '
            'да уведоми Доставчика пряко. Отказът от услуга на Доставчик не е обхванат от '
            'Приложение 1 към настоящите ОУ.\n\n'
            '7.4 За упражняване на правото на отказ от договор с Nevumo (напр. бъдещ платен '
            'абонамент), Клиентът уведомява Nevumo на privacy@nevumo.com в срок от 14 дни. '
            'За целта може да се използва Приложение 1.'
        ),
        "cs": (
            '7.1 Pokud jste spotřebitel (fyzická osoba jednající mimo rámec své podnikatelské '
            'nebo profesní činnosti), máte právo odstoupit od smlouvy uzavřené na dálku s '
            'poskytovatelem do 14 kalendářních dnů od uzavření smlouvy, bez udání důvodu.\n\n'
            '7.2 Právo na odstoupení může zaniknout, pokud byla služba plně poskytnuta před '
            'uplynutím lhůty a vy jste výslovně souhlasili se zahájením plnění před jejím '
            'uplynutím.\n\n'
            '7.3 Pro uplatnění práva na odstoupení musíte informovat poskytovatele přímo. '
            'Můžete použít vzorový formulář pro odstoupení v Příloze 1 těchto podmínek.\n\n'
            '7.4 [PL] Polští spotřebitelé mají také právo odstoupit od jakékoli smlouvy '
            'uzavřené s Nevumo za platformní služby ve stejné 14denní lhůtě. Kontaktujte '
            'Nevumo na privacy@nevumo.com nebo použijte Přílohu 1.'
        ),
        "da": (
            '7.1 Hvis du er forbruger (en fysisk person, der handler uden for sine erhvervs- '
            'eller handelsmæssige aktiviteter), har du ret til at fortryde en fjernsalgskontrakt '
            'med en serviceudbyder inden for 14 kalenderdage fra kontraktens indgåelse, uden '
            'at angive nogen grund.\n\n'
            '7.2 Fortrydelsesretten kan gå tabt, hvis tjenesten er fuldt ud leveret inden '
            'fortrydelsesperiodens udløb, og du har givet dit udtrykkelige samtykke til, at '
            'levering begyndte inden periodens udløb.\n\n'
            '7.3 For at udøve din fortrydelsesret skal du underrette tjenesteudbyderen direkte. '
            'Du kan bruge standardfortrydelsesformularen i Bilag 1.\n\n'
            '7.4 [PL] Polske forbrugere har også ret til at fortryde en kontrakt med Nevumo '
            'om platformtjenester inden for den samme 14-dages periode. Kontakt Nevumo på '
            'privacy@nevumo.com eller brug Bilag 1.'
        ),
        "de": (
            '7.1 Wenn Sie Verbraucher sind (eine natürliche Person, die außerhalb ihrer '
            'gewerblichen oder beruflichen Tätigkeit handelt), haben Sie das Recht, einen '
            'Fernabsatzvertrag mit einem Dienstleister innerhalb von 14 Kalendertagen nach '
            'Vertragsschluss ohne Angabe von Gründen zu widerrufen.\n\n'
            '7.2 Das Widerrufsrecht erlischt, wenn die Dienstleistung vollständig erbracht '
            'wurde, bevor die Widerrufsfrist abgelaufen ist, und Sie ausdrücklich zugestimmt '
            'haben, dass die Leistung vor Ablauf der Frist beginnt.\n\n'
            '7.3 Um Ihr Widerrufsrecht auszuüben, müssen Sie den Dienstleister direkt '
            'informieren. Sie können das Muster-Widerrufsformular in Anhang 1 verwenden.\n\n'
            '7.4 [PL] Polnische Verbraucher haben auch das Recht, jeden mit Nevumo für '
            'Plattformdienste geschlossenen Vertrag innerhalb derselben 14-Tage-Frist zu '
            'widerrufen. Kontaktieren Sie Nevumo unter privacy@nevumo.com oder nutzen Sie '
            'Anhang 1.'
        ),
        "el": (
            '7.1 Εάν είστε καταναλωτής (φυσικό πρόσωπο που ενεργεί εκτός πλαισίου '
            'επαγγελματικής δραστηριότητας), έχετε δικαίωμα υπαναχώρησης από σύμβαση εξ '
            'αποστάσεως με πάροχο υπηρεσιών εντός 14 ημερολογιακών ημερών από τη σύναψή '
            'της, χωρίς αιτιολόγηση.\n\n'
            '7.2 Το δικαίωμα υπαναχώρησης χάνεται εάν η υπηρεσία εκτελεστεί πλήρως πριν '
            'τη λήξη της προθεσμίας και έχετε δώσει ρητή συγκατάθεσή σας.\n\n'
            '7.3 Για άσκηση του δικαιώματος υπαναχώρησης από σύμβαση με πάροχο, ενημερώστε '
            'τον πάροχο άμεσα. Μπορείτε να χρησιμοποιήσετε το τυποποιημένο έντυπο του '
            'Παραρτήματος 1.\n\n'
            '7.4 [PL] Οι Πολωνοί καταναλωτές έχουν επίσης δικαίωμα υπαναχώρησης από '
            'συμβάσεις με το Nevumo για υπηρεσίες πλατφόρμας εντός 14 ημερών. Επικοινωνήστε '
            'στο privacy@nevumo.com ή χρησιμοποιήστε το Παράρτημα 1.'
        ),
        "es": (
            '7.1 Si es un consumidor (persona física que actúa fuera del ámbito de su '
            'actividad profesional), tiene derecho a desistir de un contrato a distancia con '
            'un proveedor de servicios en un plazo de 14 días naturales desde su celebración, '
            'sin necesidad de justificación.\n\n'
            '7.2 El derecho de desistimiento puede perderse si el servicio se ha ejecutado '
            'completamente antes del vencimiento del plazo y usted dio su consentimiento '
            'expreso para el inicio de la ejecución.\n\n'
            '7.3 Para ejercer su derecho de desistimiento, debe informar directamente al '
            'proveedor. Puede utilizar el formulario estándar del Anexo 1.\n\n'
            '7.4 [PL] Los consumidores polacos también tienen derecho a desistir de cualquier '
            'contrato celebrado con Nevumo para servicios de plataforma en el mismo plazo de '
            '14 días. Contacte a Nevumo en privacy@nevumo.com o use el Anexo 1.'
        ),
        "et": (
            '7.1 Kui olete tarbija (füüsiline isik, kes tegutseb väljaspool oma kutsetegevust), '
            'on teil õigus taganeda teenusepakkujaga sõlmitud kauglepingust 14 kalendripäeva '
            'jooksul lepingu sõlmimisest, ilma põhjust esitamata.\n\n'
            '7.2 Taganemisõigus võib kaduda, kui teenus on täielikult osutatud enne tähtaja '
            'lõppu ja olete andnud selgesõnalise nõusoleku teenuse alustamiseks.\n\n'
            '7.3 Taganemisõiguse kasutamiseks teavitage teenusepakkujat otse. Võite kasutada '
            'Lisa 1 standardset taganemisteadet.\n\n'
            '7.4 [PL] Poola tarbijatel on ka õigus taganeda Nevumoga sõlmitud '
            'platvormiteenuste lepingutest sama 14-päevase tähtaja jooksul. Võtke ühendust '
            'privacy@nevumo.com või kasutage Lisa 1.'
        ),
        "fi": (
            '7.1 Jos olet kuluttaja (luonnollinen henkilö, joka toimii ammatillisen '
            'toimintansa ulkopuolella), sinulla on oikeus peruuttaa palveluntarjoajan kanssa '
            'etäsopimus 14 kalenteripäivän kuluessa sopimuksen tekemisestä ilman '
            'perusteluja.\n\n'
            '7.2 Peruuttamisoikeus voi raueta, jos palvelu on suoritettu kokonaan ennen '
            'peruuttamisajan päättymistä ja olet antanut nimenomaisen suostumuksesi '
            'suorituksen aloittamiseen.\n\n'
            '7.3 Käyttääksesi peruuttamisoikeutta sinun on ilmoitettava palveluntarjoajalle '
            'suoraan. Voit käyttää liitteen 1 vakiolomaketta.\n\n'
            '7.4 [PL] Puolalaisilla kuluttajilla on myös oikeus peruuttaa Nevumon kanssa '
            'tehty alustapalvelusopimus saman 14 päivän kuluessa. Ota yhteyttä '
            'privacy@nevumo.com tai käytä Liitettä 1.'
        ),
        "fr": (
            '7.1 Si vous êtes un consommateur (personne physique agissant en dehors de son '
            'activité professionnelle), vous avez le droit de vous rétracter d\'un contrat à '
            'distance avec un prestataire dans un délai de 14 jours calendaires suivant la '
            'conclusion du contrat, sans motif.\n\n'
            '7.2 Le droit de rétractation peut être perdu si le service a été entièrement '
            'exécuté avant la fin du délai et que vous avez expressément consenti au début '
            'de l\'exécution.\n\n'
            '7.3 Pour exercer votre droit de rétractation d\'un contrat de service, vous devez '
            'informer directement le prestataire. Vous pouvez utiliser le formulaire standard '
            'de l\'Annexe 1.\n\n'
            '7.4 [PL] Les consommateurs polonais ont également le droit de se rétracter de '
            'tout contrat conclu avec Nevumo pour des services de plateforme dans le même '
            'délai de 14 jours. Contactez Nevumo à privacy@nevumo.com ou utilisez l\'Annexe 1.'
        ),
        "ga": (
            '7.1 Más tomhaltóir thú (duine nádúrtha ag gníomhú lasmuigh de ghníomhaíocht '
            'ghairmiúil), tá ceart agat aistarraingt ó chonradh cianda le soláthróir seirbhíse '
            'laistigh de 14 lá féilire ó thabhairt i gcrích an chonartha, gan fáth a lua.\n\n'
            '7.2 Féadfaidh an ceart aistarraingthe a bheith caillte má rinneadh an tseirbhís '
            'go hiomlán roimh dheireadh na tréimhse agus gur thug tú toiliú sainráite.\n\n'
            '7.3 Chun do cheart aistarraingthe a fheidhmiú, caithfidh tú an soláthróir a '
            'chur ar an eolas go díreach. Is féidir leat an fhoirm chaighdeánach in Aguisín '
            '1 a úsáid.\n\n'
            '7.4 [PL] Tá ceart ag tomhaltóirí Polannach freisin aistarraingt ó aon chonradh '
            'le Nevumo do sheirbhísí ardáin laistigh den tréimhse 14 lá chéanna. Déan '
            'teagmháil le Nevumo ag privacy@nevumo.com nó úsáid Aguisín 1.'
        ),
        "hr": (
            '7.1 Ako ste potrošač (fizička osoba koja djeluje izvan okvira svoje poslovne '
            'djelatnosti), imate pravo odustati od ugovora sklopljenog na daljinu s '
            'davateljem usluge u roku od 14 kalendarskih dana od sklapanja ugovora, bez '
            'navođenja razloga.\n\n'
            '7.2 Pravo na odustanak može biti izgubljeno ako je usluga u cijelosti izvršena '
            'prije isteka roka i vi ste izričito pristali na početak izvršavanja.\n\n'
            '7.3 Za ostvarivanje prava na odustanak morate izravno obavijestiti davatelja '
            'usluge. Možete koristiti standardni obrazac iz Priloga 1.\n\n'
            '7.4 [PL] Poljski potrošači imaju i pravo odustati od ugovora s Nevumo za '
            'usluge platforme u istom roku od 14 dana. Kontaktirajte Nevumo na '
            'privacy@nevumo.com ili koristite Prilog 1.'
        ),
        "hu": (
            '7.1 Ha fogyasztó (szakmai tevékenységén kívül eljáró természetes személy), '
            'jogosult elállni a szolgáltatóval kötött, távollevők között létrejött '
            'szerződéstől a szerződés megkötésétől számított 14 naptári napon belül, '
            'indoklás nélkül.\n\n'
            '7.2 Az elállási jog elveszhet, ha a szolgáltatást teljes egészében teljesítették '
            'a határidő lejárta előtt, és Ön kifejezetten hozzájárult a teljesítés '
            'megkezdéséhez.\n\n'
            '7.3 Az elállási jog gyakorlásához közvetlenül a szolgáltatót kell értesítenie. '
            'Használhatja az 1. mellékletben található minta elállási nyilatkozatot.\n\n'
            '7.4 [PL] A lengyel fogyasztóknak is joguk van elállni a Nevumóval '
            'platformszolgáltatásokra kötött bármely szerződéstől ugyanazon 14 napos '
            'határidőn belül. Értesítse a Nevumot a privacy@nevumo.com e-mail-címen vagy '
            'használja az 1. mellékletet.'
        ),
        "is": (
            '7.1 Ef þú ert neytandi (einstaklingur sem starfar utan sinna faglegra athafna) '
            'hefur þú rétt til að afturboða fjarsamning við þjónustuaðila innan 14 '
            'almanaksdaga frá gerð samningsins, án þess að gefa ástæðu.\n\n'
            '7.2 Afturköllunartétturinn getur fallið niður ef þjónustan hefur verið að fullu '
            'veitt áður en frestinum lýkur og þú gafst skýrt samþykki þitt.\n\n'
            '7.3 Til að nýta þér afturköllunartéttinn verður þú að tilkynna þjónustuaðilanum '
            'beint. Þú getur notað staðlaðar eyðublaðið í Viðauka 1.\n\n'
            '7.4 [PL] Pólskir neytendur hafa einnig rétt til að afturkalla samninga við '
            'Nevumo um vettvangþjónustu innan sama 14 daga frests. Hafðu samband við Nevumo '
            'á privacy@nevumo.com eða notaðu Viðauka 1.'
        ),
        "it": (
            '7.1 Se sei un consumatore (persona fisica che agisce al di fuori della propria '
            'attività professionale), hai il diritto di recedere da un contratto a distanza '
            'con un prestatore di servizi entro 14 giorni di calendario dalla conclusione '
            'del contratto, senza fornire alcuna motivazione.\n\n'
            '7.2 Il diritto di recesso può essere perso se il servizio è stato completamente '
            'eseguito prima della scadenza del periodo e hai espressamente acconsentito '
            'all\'inizio dell\'esecuzione.\n\n'
            '7.3 Per esercitare il diritto di recesso da un contratto di servizio, devi '
            'informare direttamente il prestatore. Puoi utilizzare il modulo standard '
            'dell\'Allegato 1.\n\n'
            '7.4 [PL] I consumatori polacchi hanno anche il diritto di recedere da qualsiasi '
            'contratto concluso con Nevumo per servizi di piattaforma entro lo stesso '
            'periodo di 14 giorni. Contatta Nevumo a privacy@nevumo.com o usa l\'Allegato 1.'
        ),
        "lb": (
            '7.1 Wann Dir Konsument sidd (eng natierleche Persoun, déi ausserhalb vun '
            'hirer berufflecher Aktivitéit handelt), hutt Dir d\'Recht, e Fernabsazkontrakt '
            'mat engem Serviceprestataire bannent 14 Kalennerdaag no Ofschloss vum Kontrakt '
            'z\'widderruffen, ouni Grënn unzeginn.\n\n'
            '7.2 D\'Widderhollungsrecht kann erlöschen, wann de Service vollständig erbracht '
            'gouf ier d\'Frist ofgelaf ass a Dir ausdrécklech zougestëmmt hutt.\n\n'
            '7.3 Fir Äert Widderhollungsrecht auszeüben, musst Dir de Prestataire direkt '
            'informéieren. Dir kënnt de Formulaire aus dem Anhang 1 benotzen.\n\n'
            '7.4 [PL] Polnesch Konsumenten hunn och d\'Recht, Kontrakter mat Nevumo fir '
            'Plattformservicer bannent 14 Deeg z\'widderruffen. Kontaktéiert Nevumo op '
            'privacy@nevumo.com oder benotzt Anhang 1.'
        ),
        "lt": (
            '7.1 Jei esate vartotojas (fizinis asmuo, veikiantis ne pagal profesinę '
            'veiklą), turite teisę atsisakyti nuotolinės sutarties su paslaugų teikėju '
            'per 14 kalendorinių dienų nuo sutarties sudarymo, nenurodydami priežasties.\n\n'
            '7.2 Teisė atsisakyti gali būti prarasta, jei paslauga buvo visiškai suteikta '
            'iki termino pabaigos ir jūs aiškiai sutikote su vykdymo pradžia.\n\n'
            '7.3 Norėdami pasinaudoti teise atsisakyti, turite tiesiogiai informuoti '
            'paslaugų teikėją. Galite naudoti 1 priedo standartinę formą.\n\n'
            '7.4 [PL] Lenkijos vartotojai taip pat turi teisę atsisakyti bet kokios '
            'sutarties su Nevumo dėl platformos paslaugų per tą patį 14 dienų laikotarpį. '
            'Susisiekite su Nevumo privacy@nevumo.com arba naudokite 1 priedą.'
        ),
        "lv": (
            '7.1 Ja esat patērētājs (fiziska persona, kas darbojas ārpus savas profesionālās '
            'darbības), jums ir tiesības atsaukt distances līgumu ar pakalpojumu sniedzēju '
            '14 kalendāro dienu laikā no līguma noslēgšanas, nenorādot iemeslu.\n\n'
            '7.2 Atteikuma tiesības var tikt zaudētas, ja pakalpojums ir pilnīgi izpildīts '
            'pirms termiņa beigām un jūs esat skaidri piekritis izpildes uzsākšanai.\n\n'
            '7.3 Lai izmantotu atteikuma tiesības, jums jāinformē pakalpojumu sniedzējs '
            'tieši. Varat izmantot standarta veidlapu 1. pielikumā.\n\n'
            '7.4 [PL] Polijas patērētājiem arī ir tiesības atsaukt jebkuru ar Nevumo '
            'noslēgtu platformas pakalpojumu līgumu tajā pašā 14 dienu termiņā. Sazinieties '
            'ar Nevumo privacy@nevumo.com vai izmantojiet 1. pielikumu.'
        ),
        "mk": (
            '7.1 Ако сте потрошувач (физичко лице кое дејствува надвор од рамките на '
            'својата деловна дејност), имате право да се откажете од договор склучен на '
            'далечина со Давателот во рок од 14 календарски дена од склучувањето, без '
            'наведување причина.\n\n'
            '7.2 Правото на отстапување може да отпадне ако услугата е целосно извршена '
            'пред истекот на рокот и сте дале изрична согласност за почеток на '
            'извршувањето.\n\n'
            '7.3 За да го искористите правото на отстапување, мора директно да го '
            'известите Давателот. Можете да го користите стандардниот образец од '
            'Прилог 1.\n\n'
            '7.4 [PL] Полските потрошувачи исто така имаат право да се откажат од '
            'договори со Nevumo за услуги на платформата во ист рок од 14 дена. '
            'Контактирајте го Nevumo на privacy@nevumo.com или користете го Прилог 1.'
        ),
        "mt": (
            '7.1 Jekk inti konsumatur (persuna naturali li taġixxi barra mill-attività '
            'professjonali tagħha), għandek id-dritt li tirtira minn kuntratt mill-bogħod '
            'ma\' fornitur ta\' servizz fi żmien 14-il jum tal-kalendarju mill-konklużjoni '
            'tal-kuntratt, mingħajr ma tagħti raġuni.\n\n'
            '7.2 Id-dritt tal-irtirar jista\' jintilef jekk is-servizz ikun ġie esegwit '
            'kompletament qabel tmiem il-perjodu u tkun tajt il-kunsens espliċitu tiegħek.\n\n'
            '7.3 Biex teżerċita d-dritt tal-irtirar minn kuntratt ta\' servizz, trid tgħarraf '
            'lill-fornitur direttament. Tista\' tuża l-formola standard tal-Anness 1.\n\n'
            '7.4 [PL] Il-konsumaturi Pollakki għandhom ukoll id-dritt li jirtiraw minn '
            'kwalunkwe kuntratt ma\' Nevumo għal servizzi tal-pjattaforma fi żmien l-istess '
            '14-il jum. Ikkuntattja lil Nevumo fuq privacy@nevumo.com jew uża l-Anness 1.'
        ),
        "nl": (
            '7.1 Als u een consument bent (een natuurlijke persoon die buiten zijn '
            'beroeps- of handelsactiviteiten handelt), heeft u het recht om een '
            'overeenkomst op afstand met een serviceprovider binnen 14 kalenderdagen na '
            'het sluiten van de overeenkomst te herroepen, zonder opgave van redenen.\n\n'
            '7.2 Het herroepingsrecht kan verloren gaan als de dienst volledig is verricht '
            'voor het verstrijken van de herroepingstermijn en u uitdrukkelijk heeft '
            'ingestemd met de aanvang van de dienstverlening.\n\n'
            '7.3 Om uw herroepingsrecht uit te oefenen, moet u de serviceprovider rechtstreeks '
            'informeren. U kunt het standaardformulier in Bijlage 1 gebruiken.\n\n'
            '7.4 [PL] Poolse consumenten hebben ook het recht om elk contract met Nevumo '
            'voor platformdiensten binnen dezelfde periode van 14 dagen te herroepen. '
            'Neem contact op met Nevumo via privacy@nevumo.com of gebruik Bijlage 1.'
        ),
        "no": (
            '7.1 Hvis du er forbruker (en fysisk person som handler utenfor sin nærings- '
            'eller yrkesvirksomhet), har du rett til å trekke deg fra en fjernsalgskontrakt '
            'med en tjenesteleverandør innen 14 kalenderdager fra avtalens inngåelse, uten '
            'å oppgi noen grunn.\n\n'
            '7.2 Angreretten kan gå tapt dersom tjenesten er fullstendig levert før '
            'angrefristen er utløpt og du ga ditt uttrykkelige samtykke til at levering '
            'begynte.\n\n'
            '7.3 For å benytte deg av angreretten må du informere tjenesteleverandøren '
            'direkte. Du kan bruke standardskjemaet i Vedlegg 1.\n\n'
            '7.4 [PL] Polske forbrukere har også rett til å trekke seg fra enhver kontrakt '
            'inngått med Nevumo om plattformtjenester innen den samme 14-dagersperioden. '
            'Kontakt Nevumo på privacy@nevumo.com eller bruk Vedlegg 1.'
        ),
        "pt": (
            '7.1 Se você é consumidor (pessoa física agindo fora de sua atividade profissional), '
            'tem o direito de se arrepender de um contrato à distância com um prestador de '
            'serviços no prazo de 14 dias corridos a partir da celebração do contrato, sem '
            'necessidade de justificativa.\n\n'
            '7.2 O direito de arrependimento pode ser perdido se o serviço tiver sido '
            'completamente prestado antes do término do prazo e você tiver dado consentimento '
            'expresso para o início da execução.\n\n'
            '7.3 Para exercer seu direito de arrependimento, você deve informar diretamente '
            'o prestador. Pode usar o formulário padrão do Anexo 1.\n\n'
            '7.4 [PL] Os consumidores poloneses também têm o direito de se arrepender de '
            'qualquer contrato celebrado com o Nevumo para serviços da plataforma no mesmo '
            'prazo de 14 dias. Contate o Nevumo em privacy@nevumo.com ou use o Anexo 1.'
        ),
        "pt-PT": (
            '7.1 Se for um consumidor (pessoa singular que actua fora da sua actividade '
            'profissional), tem o direito de se retratar de um contrato à distância com um '
            'prestador de serviços no prazo de 14 dias de calendário a contar da celebração '
            'do contrato, sem necessidade de justificação.\n\n'
            '7.2 O direito de retractação pode ser perdido se o serviço tiver sido '
            'completamente prestado antes do término do prazo e tiver dado consentimento '
            'expresso para o início da execução.\n\n'
            '7.3 Para exercer o seu direito de retractação, deve informar directamente o '
            'prestador. Pode utilizar o formulário-tipo do Anexo 1.\n\n'
            '7.4 [PL] Os consumidores polacos têm também o direito de se retratar de qualquer '
            'contrato celebrado com o Nevumo para serviços da plataforma no mesmo prazo de '
            '14 dias. Contacte o Nevumo em privacy@nevumo.com ou utilize o Anexo 1.'
        ),
        "ro": (
            '7.1 Dacă sunteți un consumator (persoană fizică care acționează în afara '
            'activității sale profesionale), aveți dreptul de a vă retrage dintr-un contract '
            'la distanță cu un prestator de servicii în termen de 14 zile calendaristice de '
            'la încheierea contractului, fără a indica niciun motiv.\n\n'
            '7.2 Dreptul de retragere poate fi pierdut dacă serviciul a fost executat '
            'integral înainte de expirarea perioadei și ați acordat consimțământul expres.\n\n'
            '7.3 Pentru a vă exercita dreptul de retragere, trebuie să informați direct '
            'prestatorul. Puteți folosi formularul standard din Anexa 1.\n\n'
            '7.4 [PL] Consumatorii polonezi au, de asemenea, dreptul de a se retrage din '
            'orice contract încheiat cu Nevumo pentru servicii de platformă în același '
            'termen de 14 zile. Contactați Nevumo la privacy@nevumo.com sau utilizați '
            'Anexa 1.'
        ),
        "ru": (
            '7.1 Если вы являетесь потребителем (физическим лицом, действующим вне рамок '
            'профессиональной деятельности), вы вправе отказаться от дистанционного '
            'договора с исполнителем в течение 14 календарных дней с момента заключения '
            'договора без указания причин.\n\n'
            '7.2 Право на отказ может быть утрачено, если услуга была полностью оказана '
            'до истечения срока и вы дали явное согласие на начало исполнения.\n\n'
            '7.3 Для реализации права на отказ от договора с исполнителем уведомите его '
            'напрямую. Можно воспользоваться стандартной формой из Приложения 1.\n\n'
            '7.4 [PL] Польские потребители также вправе отказаться от любого договора с '
            'Nevumo на платформенные услуги в тот же 14-дневный срок. Свяжитесь с Nevumo '
            'по адресу privacy@nevumo.com или используйте Приложение 1.'
        ),
        "sk": (
            '7.1 Ak ste spotrebiteľ (fyzická osoba konajúca mimo rámca svojej obchodnej '
            'alebo profesionálnej činnosti), máte právo odstúpiť od zmluvy uzatvorenej na '
            'diaľku s poskytovateľom do 14 kalendárnych dní od uzatvorenia zmluvy, bez '
            'udania dôvodu.\n\n'
            '7.2 Právo na odstúpenie môže zaniknúť, ak bola služba úplne poskytnutá pred '
            'uplynutím lehoty a vy ste výslovne súhlasili so začatím plnenia.\n\n'
            '7.3 Pre uplatnenie práva na odstúpenie musíte informovať poskytovateľa priamo. '
            'Môžete použiť vzorový formulár v Prílohe 1.\n\n'
            '7.4 [PL] Poľskí spotrebitelia majú tiež právo odstúpiť od akejkoľvek zmluvy '
            's Nevumo na platformové služby v rovnakej 14-dňovej lehote. Kontaktujte Nevumo '
            'na privacy@nevumo.com alebo použite Prílohu 1.'
        ),
        "sl": (
            '7.1 Če ste potrošnik (fizična oseba, ki deluje zunaj svoje poklicne dejavnosti), '
            'imate pravico odstopiti od pogodbe na daljavo s ponudnikom storitev v 14 '
            'koledarskih dneh od sklenitve pogodbe, brez navedbe razloga.\n\n'
            '7.2 Pravica do odstopa je lahko izgubljena, če je bila storitev v celoti '
            'izvedena pred potekom roka in ste izrecno privolili v začetek izvajanja.\n\n'
            '7.3 Za uveljavljanje pravice do odstopa morate neposredno obvestiti ponudnika. '
            'Lahko uporabite standardni obrazec iz Priloge 1.\n\n'
            '7.4 [PL] Poljski potrošniki imajo tudi pravico do odstopa od katere koli '
            'pogodbe z Nevumo za storitve platforme v istem roku 14 dni. Kontaktirajte '
            'Nevumo na privacy@nevumo.com ali uporabite Prilogo 1.'
        ),
        "sq": (
            '7.1 Nëse jeni konsumator (person fizik që vepron jashtë veprimtarisë '
            'profesionale), keni të drejtën të tërhiqeni nga një kontratë në distancë me '
            'një ofrues shërbimi brenda 14 ditëve kalendarike nga lidhja e kontratës, pa '
            'dhënë arsye.\n\n'
            '7.2 E drejta e tërheqjes mund të humbasë nëse shërbimi është kryer plotësisht '
            'para mbarimit të afatit dhe keni dhënë pëlqimin tuaj të shprehur.\n\n'
            '7.3 Për të ushtruar të drejtën e tërheqjes, duhet të informoni ofruesin '
            'drejtpërdrejt. Mund të përdorni formularin standard të Shtojcës 1.\n\n'
            '7.4 [PL] Konsumatorët polakë kanë gjithashtu të drejtën të tërhiqen nga '
            'çdo kontratë me Nevumo për shërbime të platformës brenda të njëjtit afat '
            '14-ditor. Kontaktoni Nevumo në privacy@nevumo.com ose përdorni Shtojcën 1.'
        ),
        "sr": (
            '7.1 Ako ste potrošač (fizičko lice koje deluje van okvira svoje poslovne '
            'delatnosti), imate pravo da odustanete od ugovora zaključenog na daljinu sa '
            'pružaocem usluga u roku od 14 kalendarskih dana od zaključenja ugovora, bez '
            'navođenja razloga.\n\n'
            '7.2 Pravo na odustanak može biti izgubljeno ako je usluga u potpunosti '
            'izvršena pre isteka roka i dali ste izričitu saglasnost za početak izvršenja.\n\n'
            '7.3 Za ostvarivanje prava na odustanak morate direktno obavestiti pružaoca. '
            'Možete koristiti standardni obrazac iz Priloga 1.\n\n'
            '7.4 [PL] Poljski potrošači imaju i pravo da odustanu od bilo kog ugovora sa '
            'Nevumo za usluge platforme u istom roku od 14 dana. Kontaktirajte Nevumo na '
            'privacy@nevumo.com ili koristite Prilog 1.'
        ),
        "sv": (
            '7.1 Om du är konsument (en fysisk person som agerar utanför sin yrkesmässiga '
            'verksamhet) har du rätt att ångra ett distansavtal med en tjänsteleverantör '
            'inom 14 kalenderdagar från avtalets ingående, utan att ange skäl.\n\n'
            '7.2 Ångerrätten kan gå förlorad om tjänsten har utförts fullständigt innan '
            'ångerfristen löpt ut och du uttryckligen samtyckt till att utförandet påbörjades.\n\n'
            '7.3 För att utöva din ångerrätt måste du informera tjänsteleverantören direkt. '
            'Du kan använda standardformuläret i Bilaga 1.\n\n'
            '7.4 [PL] Polska konsumenter har också rätt att ångra avtal med Nevumo om '
            'plattformstjänster inom samma 14-dagarsperiod. Kontakta Nevumo på '
            'privacy@nevumo.com eller använd Bilaga 1.'
        ),
        "tr": (
            '7.1 Tüketici iseniz (mesleki faaliyeti dışında hareket eden gerçek kişi), '
            'bir hizmet sağlayıcıyla yapılan mesafeli sözleşmeden sözleşmenin kurulmasından '
            'itibaren 14 takvim günü içinde herhangi bir gerekçe göstermeksizin cayma '
            'hakkınız bulunmaktadır.\n\n'
            '7.2 Cayma hakkı, hizmet süre dolmadan tamamen ifa edilmişse ve siz ifanın '
            'başlaması için açık rızanızı vermişseniz ortadan kalkabilir.\n\n'
            '7.3 Cayma hakkınızı kullanmak için hizmet sağlayıcıyı doğrudan bilgilendirmeniz '
            'gerekmektedir. Ek 1\'deki standart formu kullanabilirsiniz.\n\n'
            '7.4 [PL] Polonyalı tüketiciler aynı 14 günlük süre içinde Nevumo ile platform '
            'hizmetleri için akdedilen herhangi bir sözleşmeden de cayma hakkına sahiptir. '
            'Nevumo\'ya privacy@nevumo.com adresinden ulaşın veya Ek 1\'i kullanın.'
        ),
        "uk": (
            '7.1 Якщо ви є споживачем (фізичною особою, що діє поза межами своєї '
            'професійної діяльності), ви маєте право відмовитися від дистанційного договору '
            'з виконавцем протягом 14 календарних днів з моменту укладення договору без '
            'зазначення причин.\n\n'
            '7.2 Право на відмову може бути втрачено, якщо послуга була повністю надана '
            'до закінчення строку і ви дали явну згоду на початок виконання.\n\n'
            '7.3 Для реалізації права на відмову від договору з виконавцем повідомте його '
            'безпосередньо. Можна скористатися стандартною формою з Додатку 1.\n\n'
            '7.4 [PL] Польські споживачі також мають право відмовитися від будь-якого '
            'договору з Nevumo щодо послуг платформи у той самий 14-денний строк. '
            'Зв\'яжіться з Nevumo на privacy@nevumo.com або скористайтесь Додатком 1.'
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
        print(f"✅ seed_terms_p7_bodies: {count} rows upserted ({NAMESPACE}, art7_body × 34 langs)")

    engine.dispose()


if __name__ == "__main__":
    seed()
