"""
seed_terms_p6_bodies.py  —  Nevumo | namespace: terms
Key: art6_body (34 езика)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_terms_p6_bodies
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
    "art6_body": {
        "en": (
            '6.1 Prices for services are set by providers, not by Nevumo. All prices displayed '
            'are inclusive of applicable taxes unless otherwise stated by the provider.\n\n'
            '6.2 Payments may be processed through Stripe (credit/debit cards). [PL] For users '
            'in Poland, BLIK and Przelewy24 are also available payment methods.\n\n'
            '6.3 Nevumo acts as a pure intermediary and does not hold your funds. Payment is '
            'made directly to the provider or via a payment processor in accordance with the '
            'provider\'s terms.\n\n'
            '6.4 At the date of these Terms, creating an account and submitting leads on Nevumo '
            'is free of charge for clients. Nevumo reserves the right to introduce paid features '
            'or subscription tiers. Any such change will be communicated with a minimum 30 days\' '
            'notice before taking effect.'
        ),
        "pl": (
            '8.1 Ceny usług ustalają Usługodawcy, nie Nevumo. Wszystkie wyświetlane ceny '
            'zawierają obowiązujące podatki, chyba że Usługodawca wyraźnie zaznaczył inaczej.\n\n'
            '8.2 Płatności mogą być realizowane za pośrednictwem operatora płatności Stripe '
            '(karty kredytowe i debetowe). Dla Klientów w Polsce dostępne są również metody '
            'płatności: BLIK oraz Przelewy24.\n\n'
            '8.3 Nevumo działa wyłącznie jako pośrednik i nie przechowuje środków Klientów. '
            'Płatność trafia bezpośrednio do Usługodawcy lub za pośrednictwem operatora '
            'płatności zgodnie z warunkami Usługodawcy.\n\n'
            '8.4 Na dzień wejścia w życie niniejszego Regulaminu zakładanie konta i składanie '
            'zapytań w serwisie Nevumo jest bezpłatne dla Klientów. Nevumo zastrzega sobie '
            'prawo do wprowadzenia płatnych funkcji lub planów subskrypcyjnych. O takiej '
            'zmianie Klienci zostaną powiadomieni z wyprzedzeniem co najmniej 30 dni przed '
            'jej wejściem w życie.'
        ),
        "bg": (
            '6.1 Цените на услугите се определят от Доставчиците, а не от Nevumo. Всички '
            'показани цени включват приложимите данъци, освен ако Доставчикът изрично е '
            'посочил друго.\n\n'
            '6.2 Плащанията могат да се извършват чрез Stripe (кредитни/дебитни карти).\n\n'
            '6.3 Nevumo действа като чист посредник и не задържа средства на Клиентите. '
            'Плащането постъпва директно при Доставчика или чрез платежен оператор съгласно '
            'условията на Доставчика.\n\n'
            '6.4 Към датата на влизане в сила на настоящите ОУ, регистрацията и подаването '
            'на запитвания в Nevumo са безплатни за Клиентите. Nevumo си запазва правото да '
            'въведе платени функции или абонаментни планове. За такава промяна регистрираните '
            'Клиенти ще бъдат уведомени с не по-малко от 30 дни предизвестие преди влизане '
            'в сила.'
        ),
        "cs": (
            '6.1 Ceny služeb stanovují poskytovatelé, nikoli Nevumo. Všechny zobrazené ceny '
            'zahrnují příslušné daně, pokud poskytovatel výslovně neuvede jinak.\n\n'
            '6.2 Platby mohou být zpracovány prostřednictvím Stripe (kreditní/debetní karty). '
            '[PL] Pro uživatele v Polsku jsou dostupné také platební metody BLIK a Przelewy24.\n\n'
            '6.3 Nevumo působí jako čistý zprostředkovatel a nedrží vaše prostředky. Platba '
            'probíhá přímo poskytovateli nebo prostřednictvím platebního procesoru v souladu '
            's podmínkami poskytovatele.\n\n'
            '6.4 K datu těchto podmínek je vytvoření účtu a odesílání žádostí na Nevumo pro '
            'klienty zdarma. Nevumo si vyhrazuje právo zavést placené funkce nebo úrovně '
            'předplatného. O takové změně bude oznámeno s minimálně 30denním předstihem.'
        ),
        "da": (
            '6.1 Priser for tjenester fastsættes af udbydere, ikke af Nevumo. Alle viste priser '
            'er inklusive gældende skatter, medmindre udbyderen angiver andet.\n\n'
            '6.2 Betalinger kan behandles via Stripe (kredit-/debetkort). [PL] For brugere i '
            'Polen er BLIK og Przelewy24 også tilgængelige betalingsmetoder.\n\n'
            '6.3 Nevumo fungerer som ren formidler og opbevarer ikke dine midler. Betaling '
            'foretages direkte til udbyderen eller via en betalingsprocessor i overensstemmelse '
            'med udbyderens vilkår.\n\n'
            '6.4 På datoen for disse vilkår er det gratis for klienter at oprette en konto og '
            'indsende leads på Nevumo. Nevumo forbeholder sig retten til at indføre betalte '
            'funktioner eller abonnementsniveauer med mindst 30 dages varsel.'
        ),
        "de": (
            '6.1 Preise für Dienstleistungen werden von Anbietern festgelegt, nicht von Nevumo. '
            'Alle angezeigten Preise sind inklusive anfallender Steuern, sofern vom Anbieter '
            'nicht anders angegeben.\n\n'
            '6.2 Zahlungen können über Stripe (Kredit-/Debitkarten) abgewickelt werden. [PL] '
            'Für Nutzer in Polen sind auch BLIK und Przelewy24 verfügbar.\n\n'
            '6.3 Nevumo fungiert als reiner Vermittler und hält keine Gelder. Die Zahlung '
            'erfolgt direkt an den Anbieter oder über einen Zahlungsdienstleister gemäß den '
            'Bedingungen des Anbieters.\n\n'
            '6.4 Zum Datum dieser Bedingungen ist die Kontoerstellung und das Einreichen von '
            'Anfragen für Kunden kostenlos. Nevumo behält sich vor, kostenpflichtige Funktionen '
            'oder Abonnements einzuführen, mit mindestens 30 Tagen Vorankündigung.'
        ),
        "el": (
            '6.1 Οι τιμές των υπηρεσιών καθορίζονται από τους παρόχους, όχι από το Nevumo. '
            'Όλες οι εμφανιζόμενες τιμές περιλαμβάνουν τους ισχύοντες φόρους, εκτός αν ο '
            'πάροχος ορίσει διαφορετικά.\n\n'
            '6.2 Οι πληρωμές μπορούν να γίνουν μέσω Stripe (πιστωτικές/χρεωστικές κάρτες). '
            '[PL] Για χρήστες στην Πολωνία, διαθέσιμες μέθοδοι πληρωμής είναι επίσης BLIK '
            'και Przelewy24.\n\n'
            '6.3 Το Nevumo λειτουργεί ως αμιγής διαμεσολαβητής και δεν κρατά τα χρήματά σας. '
            'Η πληρωμή γίνεται απευθείας στον πάροχο ή μέσω επεξεργαστή πληρωμών σύμφωνα '
            'με τους όρους του παρόχου.\n\n'
            '6.4 Κατά την ημερομηνία αυτών των Όρων, η δημιουργία λογαριασμού και η υποβολή '
            'αιτημάτων στο Nevumo είναι δωρεάν για τους πελάτες. Το Nevumo διατηρεί το '
            'δικαίωμα να εισαγάγει επί πληρωμή λειτουργίες με τουλάχιστον 30 ημέρες '
            'προειδοποίηση.'
        ),
        "es": (
            '6.1 Los precios de los servicios los fijan los proveedores, no Nevumo. Todos los '
            'precios mostrados incluyen los impuestos aplicables, salvo que el proveedor '
            'indique lo contrario.\n\n'
            '6.2 Los pagos pueden procesarse a través de Stripe (tarjetas de crédito/débito). '
            '[PL] Para usuarios en Polonia, BLIK y Przelewy24 también están disponibles.\n\n'
            '6.3 Nevumo actúa como puro intermediario y no retiene sus fondos. El pago se '
            'realiza directamente al proveedor o a través de un procesador de pagos de acuerdo '
            'con los términos del proveedor.\n\n'
            '6.4 En la fecha de estos Términos, crear una cuenta y enviar leads en Nevumo es '
            'gratuito para los clientes. Nevumo se reserva el derecho de introducir funciones '
            'de pago con un mínimo de 30 días de aviso.'
        ),
        "et": (
            '6.1 Teenuste hinnad määravad teenusepakkujad, mitte Nevumo. Kõik kuvatud hinnad '
            'sisaldavad kohaldatavaid makse, välja arvatud juhul, kui pakkuja märgib teisiti.\n\n'
            '6.2 Makseid saab töödelda Stripe\'i kaudu (kredit-/deebetkaardid). [PL] Poola '
            'kasutajatele on saadaval ka BLIK ja Przelewy24.\n\n'
            '6.3 Nevumo tegutseb puhta vahendajana ega hoia teie raha. Makse tehakse otse '
            'teenusepakkujale või makseprotsessori kaudu vastavalt pakkuja tingimustele.\n\n'
            '6.4 Käesolevate tingimuste kuupäeval on konto loomine ja päringute esitamine '
            'Nevumol klientidele tasuta. Nevumo jätab endale õiguse lisada tasulisi funktsioone '
            'vähemalt 30-päevase etteteatamisega.'
        ),
        "fi": (
            '6.1 Palvelujen hinnat asettavat palveluntarjoajat, eivät Nevumo. Kaikki näytetyt '
            'hinnat sisältävät sovellettavat verot, ellei palveluntarjoaja toisin ilmoita.\n\n'
            '6.2 Maksuja voidaan käsitellä Strapen kautta (luotto-/pankkikortit). [PL] '
            'Puolan käyttäjille BLIK ja Przelewy24 ovat myös käytettävissä.\n\n'
            '6.3 Nevumo toimii puhtaana välittäjänä eikä pidä hallussaan varojasi. Maksu '
            'suoritetaan suoraan palveluntarjoajalle tai maksupalvelun kautta palveluntarjoajan '
            'ehtojen mukaisesti.\n\n'
            '6.4 Näiden ehtojen päivämäärästä tilin luominen ja liidien lähettäminen Nevumossa '
            'on asiakkaille ilmaista. Nevumo pidättää oikeuden ottaa käyttöön maksullisia '
            'ominaisuuksia vähintään 30 päivän ilmoitusajalla.'
        ),
        "fr": (
            '6.1 Les prix des services sont fixés par les prestataires, pas par Nevumo. Tous '
            'les prix affichés incluent les taxes applicables, sauf indication contraire du '
            'prestataire.\n\n'
            '6.2 Les paiements peuvent être traités via Stripe (cartes de crédit/débit). [PL] '
            'Pour les utilisateurs en Pologne, BLIK et Przelewy24 sont également disponibles.\n\n'
            '6.3 Nevumo agit en tant que pur intermédiaire et ne détient pas vos fonds. Le '
            'paiement est effectué directement au prestataire ou via un processeur de paiement '
            'conformément aux conditions du prestataire.\n\n'
            '6.4 À la date des présentes Conditions, la création d\'un compte et la soumission '
            'de leads sur Nevumo est gratuite pour les clients. Nevumo se réserve le droit '
            'd\'introduire des fonctionnalités payantes avec un préavis minimum de 30 jours.'
        ),
        "ga": (
            '6.1 Socraíonn soláthróirí praghsanna seirbhísí, ní Nevumo. Tá gach praghas '
            'atá le feiceáil cuimsitheach de chánacha infheidhme mura sonraíonn an soláthróir '
            'a mhalairt.\n\n'
            '6.2 Is féidir íocaíochtaí a phróiseáil trí Stripe (cártaí creidmheasa/dochair). '
            '[PL] D\'úsáideoirí sa Pholainn, tá BLIK agus Przelewy24 ar fáil freisin.\n\n'
            '6.3 Gníomhaíonn Nevumo mar idirghabhálaí íon agus ní choinníonn sé do chistí. '
            'Déantar íocaíocht go díreach leis an soláthróir nó trí phróiseálaí íocaíochta '
            'de réir choinníollacha an tsoláthróra.\n\n'
            '6.4 Ag dáta na dTéarmaí seo, tá cruthú cuntais agus cur isteach leads ar Nevumo '
            'saor in aisce do chliaint. Féadfaidh Nevumo gnéithe íoctha a thabhairt isteach '
            'le fógra 30 lá ar a laghad.'
        ),
        "hr": (
            '6.1 Cijene usluga određuju davatelji, a ne Nevumo. Sve prikazane cijene uključuju '
            'primjenjive poreze osim ako davatelj ne navede drugačije.\n\n'
            '6.2 Plaćanja se mogu obrađivati putem Stripe (kreditne/debitne kartice). [PL] Za '
            'korisnike u Poljskoj dostupni su i BLIK i Przelewy24.\n\n'
            '6.3 Nevumo djeluje kao čisti posrednik i ne čuva vaša sredstva. Plaćanje ide '
            'izravno davatelju ili putem procesora plaćanja prema uvjetima davatelja.\n\n'
            '6.4 Na datum ovih Uvjeta, kreiranje računa i slanje zahtjeva na Nevumo je '
            'besplatno za klijente. Nevumo zadržava pravo uvođenja plaćenih funkcionalnosti '
            's najmanje 30 dana obavijesti.'
        ),
        "hu": (
            '6.1 A szolgáltatások árait a szolgáltatók határozzák meg, nem a Nevumo. Az összes '
            'feltüntetett ár tartalmazza az alkalmazandó adókat, kivéve, ha a szolgáltató '
            'másként jelzi.\n\n'
            '6.2 A fizetések feldolgozhatók a Stripe-on keresztül (hitel-/betéti kártyák). '
            '[PL] Lengyelországi felhasználók számára a BLIK és a Przelewy24 is elérhető.\n\n'
            '6.3 A Nevumo tiszta közvetítőként működik és nem tárolja az Ön pénzét. A fizetés '
            'közvetlenül a szolgáltatónak vagy fizetési processzoron keresztül történik.\n\n'
            '6.4 Jelen feltételek dátumán a Nevumón a fiókregisztráció és leadek küldése '
            'ingyenes az ügyfelek számára. A Nevumo fenntartja a jogot fizetős funkciók '
            'bevezetésére, legalább 30 napos előzetes értesítéssel.'
        ),
        "is": (
            '6.1 Þjónustuaðilar ákvarða verð þjónustu, ekki Nevumo. Öll sýnd verð eru '
            'innifalin gjöld nema þjónustuaðili tilgreini annað.\n\n'
            '6.2 Hægt er að afgreiða greiðslur í gegnum Stripe (kredit-/debetkort). [PL] '
            'Fyrir notendur í Póllandi eru BLIK og Przelewy24 einnig í boði.\n\n'
            '6.3 Nevumo starfar sem hreinn milliliður og geymir ekki fé þitt. Greiðsla fer '
            'beint til þjónustuaðila eða í gegnum greiðsluaðila í samræmi við skilmála '
            'þjónustuaðila.\n\n'
            '6.4 Á dagsetningu þessara skilmála er stofnun reiknings og sending leads á '
            'Nevumo ókeypis fyrir viðskiptavini. Nevumo áskilur sér rétt til að kynna greiddar '
            'eiginleika með að minnsta kosti 30 daga fyrirvara.'
        ),
        "it": (
            '6.1 I prezzi dei servizi sono stabiliti dai prestatori, non da Nevumo. Tutti i '
            'prezzi visualizzati includono le tasse applicabili, salvo diversa indicazione '
            'del prestatore.\n\n'
            '6.2 I pagamenti possono essere elaborati tramite Stripe (carte di credito/debito). '
            '[PL] Per gli utenti in Polonia sono disponibili anche BLIK e Przelewy24.\n\n'
            '6.3 Nevumo agisce come puro intermediario e non trattiene i fondi dell\'utente. '
            'Il pagamento viene effettuato direttamente al prestatore o tramite un elaboratore '
            'di pagamenti in conformità con i termini del prestatore.\n\n'
            '6.4 Alla data di questi Termini, la creazione di un account e l\'invio di lead '
            'su Nevumo è gratuito per i clienti. Nevumo si riserva il diritto di introdurre '
            'funzionalità a pagamento con un preavviso minimo di 30 giorni.'
        ),
        "lb": (
            '6.1 Präisser fir Servicer ginn vun de Prestatairën festgeluegt, net vun Nevumo. '
            'All affichéiert Präisser enthalen d\'Steieren, ausser de Prestataire gëtt '
            'eppes anescht un.\n\n'
            '6.2 Bezuelungen kënne via Stripe (Kredit-/Debetkarten) verrechent ginn. [PL] '
            'Fir Benotzer a Polen sinn och BLIK an Przelewy24 verfügbar.\n\n'
            '6.3 Nevumo handelt als reine Vermëttler a hält keng Gelder. D\'Bezuelung geet '
            'direkt un de Prestataire oder via Bezuelungsprocessor geméiss senge Bedéngungen.\n\n'
            '6.4 Zum Datum vun dësen Bedéngungen ass d\'Erstelle vun engem Kont an d\'Aschreiwe '
            'vu Leads op Nevumo gratis fir Klienten. Nevumo behält sech vir, bezuelte '
            'Fonktiounen mat mindestens 30 Deeg Virankënnegung anzefoueren.'
        ),
        "lt": (
            '6.1 Paslaugų kainas nustato teikėjai, o ne Nevumo. Visos rodomos kainos apima '
            'taikytinus mokesčius, jei teikėjas nenurodo kitaip.\n\n'
            '6.2 Mokėjimai gali būti apdorojami per Stripe (kredito/debeto kortelės). [PL] '
            'Lenkijos vartotojams taip pat prieinami BLIK ir Przelewy24.\n\n'
            '6.3 Nevumo veikia kaip grynas tarpininkas ir nelaiko jūsų lėšų. Mokėjimas '
            'atliekamas tiesiogiai teikėjui arba per mokėjimo procesorių pagal teikėjo sąlygas.\n\n'
            '6.4 Šių sąlygų dieną paskyros kūrimas ir užklausų teikimas Nevumo platformoje '
            'klientams yra nemokamas. Nevumo pasilieka teisę įvesti mokamas funkcijas su '
            'bent 30 dienų išankstinio įspėjimo.'
        ),
        "lv": (
            '6.1 Pakalpojumu cenas nosaka pakalpojumu sniedzēji, nevis Nevumo. Visas rādītās '
            'cenas ietver piemērojamos nodokļus, ja sniedzējs nenorāda citādi.\n\n'
            '6.2 Maksājumus var apstrādāt, izmantojot Stripe (kredīt-/debetkartes). [PL] '
            'Polijas lietotājiem ir pieejamas arī BLIK un Przelewy24.\n\n'
            '6.3 Nevumo darbojas kā tīrs starpnieks un neuztur jūsu līdzekļus. Maksājums '
            'tiek veikts tieši sniedzējam vai caur maksājumu procesoru saskaņā ar sniedzēja '
            'noteikumiem.\n\n'
            '6.4 Šo noteikumu datumā konta izveide un pieprasījumu iesniegšana Nevumo ir '
            'bezmaksas klientiem. Nevumo patur tiesības ieviest maksas funkcijas ar vismaz '
            '30 dienu iepriekšēju paziņojumu.'
        ),
        "mk": (
            '6.1 Цените на услугите ги одредуваат Давателите, а не Nevumo. Сите прикажани '
            'цени вклучуваат применливи даноци, освен ако Давателот изрично не наведе '
            'поинаку.\n\n'
            '6.2 Плаќањата може да се вршат преку Stripe (кредитни/дебитни картички). [PL] '
            'За корисниците во Полска се достапни и BLIK и Przelewy24.\n\n'
            '6.3 Nevumo делува како чист посредник и не задржува ваши средства. Плаќањето '
            'оди директно кон Давателот или преку платежен процесор согласно условите на '
            'Давателот.\n\n'
            '6.4 На датумот на овие Услови, создавањето акаунт и поднесувањето на leads на '
            'Nevumo е бесплатно за клиентите. Nevumo го задржува правото да воведе платени '
            'функции со најмалку 30 дена известување.'
        ),
        "mt": (
            '6.1 Il-prezzijiet għas-servizzi jiġu stabbiliti mill-fornituri, mhux minn Nevumo. '
            'Il-prezzijiet kollha murija jinkludu t-taxxi applikabbli sakemm il-fornitur ma '
            'jiddikjarax mod ieħor.\n\n'
            '6.2 Il-pagamenti jistgħu jiġu pproċessati permezz ta\' Stripe (karti ta\' '
            'kreditu/debitu). [PL] Għall-utenti fil-Polonja, BLIK u Przelewy24 huma wkoll '
            'disponibbli.\n\n'
            '6.3 Nevumo jaġixxi bħala intermedjarji puri u ma jżommx il-fondi tiegħek. '
            'Il-pagament isir direttament lill-fornitur jew permezz ta\' proċessur ta\' pagament '
            'skont it-termini tal-fornitur.\n\n'
            '6.4 Fid-data ta\' dawn it-Termini, il-ħolqien ta\' kont u s-sottomissjoni ta\' '
            'leads fuq Nevumo huwa bla ħlas għall-klijenti. Nevumo jiriserva d-dritt li '
            'jintroduċi karatteristiċi mħallsa b\'avviż minimu ta\' 30 jum.'
        ),
        "nl": (
            '6.1 Prijzen voor diensten worden door providers vastgesteld, niet door Nevumo. '
            'Alle weergegeven prijzen zijn inclusief toepasselijke belastingen, tenzij de '
            'provider anders aangeeft.\n\n'
            '6.2 Betalingen kunnen worden verwerkt via Stripe (credit-/debetkaarten). [PL] '
            'Voor gebruikers in Polen zijn ook BLIK en Przelewy24 beschikbaar.\n\n'
            '6.3 Nevumo fungeert als pure tussenpersoon en houdt uw gelden niet vast. Betaling '
            'geschiedt rechtstreeks aan de provider of via een betalingsverwerker overeenkomstig '
            'de voorwaarden van de provider.\n\n'
            '6.4 Op de datum van deze Voorwaarden is het aanmaken van een account en het '
            'indienen van leads op Nevumo gratis voor klanten. Nevumo behoudt zich het recht '
            'voor om betaalde functies in te voeren met minimaal 30 dagen kennisgeving.'
        ),
        "no": (
            '6.1 Priser for tjenester fastsettes av leverandørene, ikke av Nevumo. Alle viste '
            'priser er inkl. gjeldende avgifter med mindre leverandøren angir noe annet.\n\n'
            '6.2 Betalinger kan behandles via Stripe (kreditt-/debetkort). [PL] For brukere '
            'i Polen er også BLIK og Przelewy24 tilgjengelige betalingsmetoder.\n\n'
            '6.3 Nevumo fungerer som ren formidler og holder ikke dine midler. Betaling skjer '
            'direkte til leverandøren eller via en betalingsprosessor i samsvar med '
            'leverandørens vilkår.\n\n'
            '6.4 På datoen for disse Vilkårene er det gratis for klienter å opprette konto og '
            'sende inn leads på Nevumo. Nevumo forbeholder seg retten til å innføre betalte '
            'funksjoner med minst 30 dagers varsel.'
        ),
        "pt": (
            '6.1 Os preços dos serviços são definidos pelos prestadores, não pelo Nevumo. '
            'Todos os preços exibidos incluem os impostos aplicáveis, salvo indicação contrária '
            'do prestador.\n\n'
            '6.2 Os pagamentos podem ser processados via Stripe (cartões de crédito/débito). '
            '[PL] Para usuários na Polônia, BLIK e Przelewy24 também estão disponíveis.\n\n'
            '6.3 O Nevumo atua como puro intermediário e não retém seus fundos. O pagamento '
            'é feito diretamente ao prestador ou via processador de pagamentos de acordo com '
            'os termos do prestador.\n\n'
            '6.4 Na data destes Termos, criar uma conta e enviar leads no Nevumo é gratuito '
            'para clientes. O Nevumo reserva-se o direito de introduzir recursos pagos com '
            'aviso mínimo de 30 dias.'
        ),
        "pt-PT": (
            '6.1 Os preços dos serviços são definidos pelos prestadores, não pelo Nevumo. '
            'Todos os preços apresentados incluem os impostos aplicáveis, salvo indicação '
            'contrária do prestador.\n\n'
            '6.2 Os pagamentos podem ser processados via Stripe (cartões de crédito/débito). '
            '[PL] Para utilizadores na Polónia, BLIK e Przelewy24 também estão disponíveis.\n\n'
            '6.3 O Nevumo actua como puro intermediário e não retém os seus fundos. O '
            'pagamento é efectuado directamente ao prestador ou via processador de pagamentos '
            'de acordo com os termos do prestador.\n\n'
            '6.4 Na data destes Termos, criar uma conta e submeter leads no Nevumo é gratuito '
            'para clientes. O Nevumo reserva-se o direito de introduzir funcionalidades pagas '
            'com aviso mínimo de 30 dias.'
        ),
        "ro": (
            '6.1 Prețurile serviciilor sunt stabilite de prestatori, nu de Nevumo. Toate '
            'prețurile afișate includ taxele aplicabile, dacă prestatorul nu specifică altfel.\n\n'
            '6.2 Plățile pot fi procesate prin Stripe (carduri de credit/debit). [PL] Pentru '
            'utilizatorii din Polonia, BLIK și Przelewy24 sunt de asemenea disponibile.\n\n'
            '6.3 Nevumo acționează ca intermediar pur și nu reține fondurile dvs. Plata se '
            'efectuează direct prestatorului sau prin intermediul unui procesator de plăți '
            'conform termenilor prestatorului.\n\n'
            '6.4 La data acestor Termeni, crearea unui cont și trimiterea de leads pe Nevumo '
            'este gratuită pentru clienți. Nevumo își rezervă dreptul de a introduce '
            'funcționalități plătite cu un preaviz minim de 30 de zile.'
        ),
        "ru": (
            '6.1 Цены на услуги устанавливаются исполнителями, а не Nevumo. Все отображаемые '
            'цены включают применимые налоги, если исполнитель не указал иное.\n\n'
            '6.2 Оплата возможна через Stripe (кредитные/дебетовые карты). [PL] Для '
            'пользователей в Польше также доступны BLIK и Przelewy24.\n\n'
            '6.3 Nevumo является чистым посредником и не удерживает ваши средства. Оплата '
            'производится напрямую исполнителю или через платёжный процессор согласно '
            'условиям исполнителя.\n\n'
            '6.4 На дату настоящих условий регистрация и отправка заявок на Nevumo бесплатны '
            'для клиентов. Nevumo оставляет за собой право ввести платные функции с '
            'уведомлением не менее чем за 30 дней.'
        ),
        "sk": (
            '6.1 Ceny služieb stanovujú poskytovatelia, nie Nevumo. Všetky zobrazené ceny '
            'zahŕňajú príslušné dane, pokiaľ poskytovateľ výslovne neuvádza inak.\n\n'
            '6.2 Platby môžu byť spracované cez Stripe (kreditné/debetné karty). [PL] Pre '
            'používateľov v Poľsku sú dostupné aj BLIK a Przelewy24.\n\n'
            '6.3 Nevumo pôsobí ako čistý sprostredkovateľ a nedrží vaše prostriedky. Platba '
            'prechádza priamo poskytovateľovi alebo cez platobný procesor podľa podmienok '
            'poskytovateľa.\n\n'
            '6.4 K dátumu týchto podmienok je vytvorenie účtu a odosielanie leadov na Nevumo '
            'pre klientov bezplatné. Nevumo si vyhradzuje právo zaviesť platené funkcie s '
            'minimálne 30-dňovým predstihom.'
        ),
        "sl": (
            '6.1 Cene storitev določajo ponudniki, ne Nevumo. Vse prikazane cene vključujejo '
            'veljavne davke, razen če ponudnik navede drugače.\n\n'
            '6.2 Plačila se lahko obdelajo prek Stripe (kreditne/debetne kartice). [PL] Za '
            'uporabnike na Poljskem sta na voljo tudi BLIK in Przelewy24.\n\n'
            '6.3 Nevumo deluje kot čisti posrednik in ne zadržuje vaših sredstev. Plačilo '
            'gre neposredno ponudniku ali prek plačilnega procesorja v skladu s pogoji '
            'ponudnika.\n\n'
            '6.4 Na datum teh pogojev je ustvarjanje računa in oddaja leadov na Nevumo '
            'brezplačno za stranke. Nevumo si pridržuje pravico uvesti plačljive funkcije '
            'z vsaj 30-dnevnim obvestilom.'
        ),
        "sq": (
            '6.1 Çmimet e shërbimeve caktohen nga ofruesit, jo nga Nevumo. Të gjitha çmimet '
            'e shfaqura përfshijnë taksat e zbatueshme, nëse ofruesi nuk tregon ndryshe.\n\n'
            '6.2 Pagesat mund të procesohen nëpërmjet Stripe (karta krediti/debiti). [PL] '
            'Për përdoruesit në Poloni, BLIK dhe Przelewy24 janë gjithashtu të disponueshme.\n\n'
            '6.3 Nevumo vepron si ndërmjetës i pastër dhe nuk mban fondet tuaja. Pagesa '
            'kryhet drejtpërdrejt tek ofruesi ose nëpërmjet një procesori pagese sipas '
            'kushteve të ofruesit.\n\n'
            '6.4 Në datën e këtyre Termave, krijimi i llogarisë dhe dërgimi i leads në '
            'Nevumo është falas për klientët. Nevumo rezervon të drejtën të prezantojë '
            'funksione me pagesë me njoftim minimal prej 30 ditësh.'
        ),
        "sr": (
            '6.1 Cene usluga određuju pružaoci, a ne Nevumo. Sve prikazane cene uključuju '
            'primenjive poreze osim ako pružalac ne navede drugačije.\n\n'
            '6.2 Plaćanja se mogu vršiti putem Stripe (kreditne/debitne kartice). [PL] Za '
            'korisnike u Poljskoj dostupni su i BLIK i Przelewy24.\n\n'
            '6.3 Nevumo deluje kao čisti posrednik i ne čuva vaša sredstva. Plaćanje ide '
            'direktno pružaocu ili putem procesora plaćanja prema uslovima pružaoca.\n\n'
            '6.4 Na datum ovih Uslova, kreiranje naloga i slanje leads-a na Nevumo je '
            'besplatno za klijente. Nevumo zadržava pravo uvođenja plaćenih funkcija sa '
            'najmanje 30 dana obaveštenja.'
        ),
        "sv": (
            '6.1 Priser för tjänster fastställs av leverantörer, inte av Nevumo. Alla visade '
            'priser är inklusive tillämpliga skatter om inte leverantören anger annat.\n\n'
            '6.2 Betalningar kan behandlas via Stripe (kredit-/betalkort). [PL] För användare '
            'i Polen är även BLIK och Przelewy24 tillgängliga betalningsmetoder.\n\n'
            '6.3 Nevumo agerar som ren förmedlare och innehar inte dina medel. Betalning sker '
            'direkt till leverantören eller via en betalningsprocessor i enlighet med '
            'leverantörens villkor.\n\n'
            '6.4 På datumet för dessa Villkor är det gratis för kunder att skapa ett konto '
            'och skicka in leads på Nevumo. Nevumo förbehåller sig rätten att införa '
            'betalfunktioner med minst 30 dagars förvarning.'
        ),
        "tr": (
            '6.1 Hizmet fiyatları sağlayıcılar tarafından belirlenir, Nevumo tarafından değil. '
            'Gösterilen tüm fiyatlar, sağlayıcı aksi belirtmedikçe geçerli vergileri içerir.\n\n'
            '6.2 Ödemeler Stripe (kredi/banka kartları) aracılığıyla işlenebilir. [PL] Polonya '
            'kullanıcıları için BLIK ve Przelewy24 da kullanılabilir.\n\n'
            '6.3 Nevumo saf bir aracı olarak hareket eder ve fonlarınızı tutmaz. Ödeme '
            'doğrudan sağlayıcıya veya sağlayıcının koşullarına göre bir ödeme işlemcisi '
            'aracılığıyla yapılır.\n\n'
            '6.4 Bu Koşulların tarihinde Nevumo\'da hesap oluşturmak ve lead göndermek '
            'müşteriler için ücretsizdir. Nevumo, en az 30 günlük önceden bildirimle ücretli '
            'özellikler sunma hakkını saklı tutar.'
        ),
        "uk": (
            '6.1 Ціни на послуги встановлюються виконавцями, а не Nevumo. Усі відображені '
            'ціни включають застосовні податки, якщо виконавець не вказав інше.\n\n'
            '6.2 Оплата можлива через Stripe (кредитні/дебетові картки). [PL] Для '
            'користувачів у Польщі також доступні BLIK та Przelewy24.\n\n'
            '6.3 Nevumo є чистим посередником і не утримує ваші кошти. Оплата здійснюється '
            'безпосередньо виконавцю або через платіжний процесор відповідно до умов '
            'виконавця.\n\n'
            '6.4 На дату цих Умов реєстрація та надсилання запитів на Nevumo є безкоштовними '
            'для клієнтів. Nevumo залишає за собою право ввести платні функції з '
            'повідомленням щонайменше за 30 днів.'
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
        print(f"✅ seed_terms_p6_bodies: {count} rows upserted ({NAMESPACE}, art6_body × 34 langs)")

    engine.dispose()


if __name__ == "__main__":
    seed()
