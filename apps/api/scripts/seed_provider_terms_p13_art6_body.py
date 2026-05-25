"""
seed_provider_terms_p13_art6_body.py  —  Nevumo | namespace: provider_terms
Key: art6_body  (1 key x 34 langs = 34 rows)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_provider_terms_p13_art6_body
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://nevumo:nevumo@postgres:5432/nevumo_leads",
)

NAMESPACE = "provider_terms"

TRANSLATIONS: dict[str, dict[str, str]] = {
    "art6_body": {
        "en": (
            "6.1 The Platform is currently free of charge for Providers during the launch phase. "
            "The current Price List is available at nevumo.com/pricing.\n\n"
            "6.2 Nevumo reserves the right to introduce a commission or paid features. Any such "
            "introduction will be announced with at least 30 days written notice sent to your "
            "registered email address before taking effect.\n\n"
            "6.3 If Nevumo introduces payment processing for services concluded through the "
            "Platform, payments will be processed by Stripe Inc. acting as a payment processor. "
            "In Poland, BLIK and Przelewy24 will be available as payment methods.\n\n"
            "6.4 Nevumo does not hold Client funds on its own accounts. All financial "
            "intermediation is handled exclusively through Stripe.\n\n"
            "6.5 Providers are solely responsible for issuing invoices, collecting taxes (VAT, "
            "income tax), and complying with all applicable fiscal obligations in their country "
            "of establishment and in the country where services are provided."
        ),
        "pl": (
            "6.1 Platforma jest obecnie dla Dostawców bezpłatna w fazie startowej. Aktualny "
            "Cennik dostępny jest pod adresem nevumo.com/pricing.\n\n"
            "6.2 Nevumo zastrzega sobie prawo do wprowadzenia prowizji lub płatnych "
            "funkcjonalności. O takim wprowadzeniu Dostawcy zostaną poinformowani z co najmniej "
            "30-dniowym wyprzedzeniem w formie pisemnej przed datą wejścia w życie zmian.\n\n"
            "6.3 W przypadku wdrożenia obsługi płatności za usługi zawierane za pośrednictwem "
            "Platformy, płatności będą przetwarzane przez Stripe Inc. działający jako operator "
            "płatności. Dla Dostawców i Klientów w Polsce dostępne będą metody płatności BLIK oraz "
            "Przelewy24.\n\n"
            "6.4 Nevumo nie przechowuje środków Klientów na własnych rachunkach. Wszelkie "
            "pośrednictwo finansowe realizowane jest wyłącznie za pośrednictwem Stripe.\n\n"
            "6.5 Dostawcy ponoszą wyłączną odpowiedzialność za wystawianie faktur, rozliczanie "
            "podatków (VAT, podatek dochodowy) i przestrzeganie wszystkich obowiązujących "
            "przepisów podatkowych w kraju prowadzenia działalności oraz w kraju świadczenia "
            "usług."
        ),
        "bg": (
            "6.1 Платформата е понастоящем безплатна за Доставчиците по време на стартовата "
            "фаза. Актуалният Ценоразпис е достъпен на nevumo.com/pricing.\n\n"
            "6.2 Nevumo си запазва правото да въведе комисионна или платени функции. Всяко "
            "такова въвеждане ще бъде обявено с поне 30 дни писмено предизвестие, изпратено "
            "на регистрирания ви имейл адрес, преди да влезе в сила.\n\n"
            "6.3 Ако Nevumo въведе обработка на плащания за услуги, сключени чрез Платформата, "
            "плащанията ще се обработват от Stripe Inc. като оператор на плащания. В Полша "
            "BLIK и Przelewy24 ще бъдат налични като методи за плащане.\n\n"
            "6.4 Nevumo не съхранява средства на Клиентите по собствени сметки. Цялото "
            "финансово посредничество се извършва изключително чрез Stripe.\n\n"
            "6.5 Доставчиците носят единствена отговорност за издаване на фактури, събиране "
            "на данъци (ДДС, данък върху дохода) и спазване на всички приложими фискални "
            "задължения в страната на регистрация и в страната, в която се предоставят "
            "услугите."
        ),
        "de": (
            "6.1 Die Plattform ist fuer Dienstleister waehrend der Startphase kostenlos. "
            "Die aktuelle Preisliste ist unter nevumo.com/pricing verfuegbar.\n\n"
            "6.2 Nevumo behaelt sich das Recht vor, eine Provision oder kostenpflichtige "
            "Funktionen einzufuehren. Jede Einfuehrung wird mit mindestens 30 Tagen "
            "schriftlicher Vorankundigung per E-Mail bekannt gegeben.\n\n"
            "6.3 Wenn Nevumo Zahlungsverarbeitung fuer ueber die Plattform abgeschlossene "
            "Dienstleistungen einfuehrt, werden Zahlungen von Stripe Inc. abgewickelt. In "
            "Polen werden BLIK und Przelewy24 als Zahlungsmethoden verfuegbar sein.\n\n"
            "6.4 Nevumo haelt keine Kundengelder auf eigenen Konten. Die gesamte "
            "Finanzvermittlung wird ausschliesslich ueber Stripe abgewickelt.\n\n"
            "6.5 Dienstleister sind allein verantwortlich fuer die Ausstellung von Rechnungen, "
            "die Erhebung von Steuern (MwSt., Einkommensteuer) und die Einhaltung aller "
            "anwendbaren steuerlichen Pflichten in ihrem Niederlassungsland und im Land, in "
            "dem Dienstleistungen erbracht werden."
        ),
        "fr": (
            "6.1 La Plateforme est actuellement gratuite pour les Prestataires pendant la phase "
            "de lancement. La Grille tarifaire est disponible sur nevumo.com/pricing.\n\n"
            "6.2 Nevumo se reserve le droit d'introduire une commission ou des fonctionnalites "
            "payantes. Toute introduction sera annoncee avec un preavis ecrit d'au moins 30 "
            "jours avant d'entrer en vigueur.\n\n"
            "6.3 Si Nevumo introduit le traitement des paiements, les paiements seront traites "
            "par Stripe Inc. En Pologne, BLIK et Przelewy24 seront disponibles comme moyens "
            "de paiement.\n\n"
            "6.4 Nevumo ne conserve pas les fonds des Clients sur ses propres comptes. Toute "
            "intermediation financiere est geree exclusivement via Stripe.\n\n"
            "6.5 Les Prestataires sont seuls responsables de l'emission des factures, de la "
            "collecte des taxes (TVA, impot sur le revenu) et du respect de toutes les "
            "obligations fiscales applicables dans leur pays d'etablissement et dans le pays "
            "ou les services sont fournis."
        ),
        "es": (
            "6.1 La Plataforma es actualmente gratuita para los Proveedores durante la fase de "
            "lanzamiento. La Lista de precios vigente esta disponible en nevumo.com/pricing.\n\n"
            "6.2 Nevumo se reserva el derecho de introducir una comision o funciones de pago. "
            "Cualquier introduccion se anunciara con al menos 30 dias de aviso escrito antes "
            "de entrar en vigor.\n\n"
            "6.3 Si Nevumo introduce el procesamiento de pagos, los pagos seran procesados por "
            "Stripe Inc. En Polonia, BLIK y Przelewy24 estaran disponibles como metodos de "
            "pago.\n\n"
            "6.4 Nevumo no retiene fondos de Clientes en sus propias cuentas. Toda la "
            "intermediacion financiera se gestiona exclusivamente a traves de Stripe.\n\n"
            "6.5 Los Proveedores son los unicos responsables de emitir facturas, recaudar "
            "impuestos (IVA, impuesto sobre la renta) y cumplir con todas las obligaciones "
            "fiscales aplicables en su pais de establecimiento y en el pais donde se prestan "
            "los servicios."
        ),
        "it": (
            "6.1 La Piattaforma e attualmente gratuita per i Fornitori durante la fase di "
            "lancio. Il Listino prezzi vigente e disponibile su nevumo.com/pricing.\n\n"
            "6.2 Nevumo si riserva il diritto di introdurre una commissione o funzionalita a "
            "pagamento. Qualsiasi introduzione sara annunciata con almeno 30 giorni di preavviso "
            "scritto prima dell'entrata in vigore.\n\n"
            "6.3 Se Nevumo introduce l'elaborazione dei pagamenti, i pagamenti saranno elaborati "
            "da Stripe Inc. In Polonia, BLIK e Przelewy24 saranno disponibili come metodi di "
            "pagamento.\n\n"
            "6.4 Nevumo non trattiene i fondi dei Clienti sui propri conti. Tutta "
            "l'intermediazione finanziaria e gestita esclusivamente tramite Stripe.\n\n"
            "6.5 I Fornitori sono i soli responsabili dell'emissione di fatture, della "
            "riscossione delle imposte (IVA, imposta sul reddito) e del rispetto di tutti gli "
            "obblighi fiscali applicabili nel loro paese di stabilimento e nel paese in cui "
            "vengono forniti i servizi."
        ),
        "nl": (
            "6.1 Het Platform is momenteel gratis voor Dienstverleners tijdens de opstartfase. "
            "De huidige Prijslijst is beschikbaar op nevumo.com/pricing.\n\n"
            "6.2 Nevumo behoudt zich het recht voor een commissie of betaalde functies in te "
            "voeren. Een dergelijke invoering wordt ten minste 30 dagen van tevoren schriftelijk "
            "aangekondigd voor inwerkingtreding.\n\n"
            "6.3 Als Nevumo betalingsverwerking introduceert, worden betalingen verwerkt door "
            "Stripe Inc. In Polen zijn BLIK en Przelewy24 beschikbaar als betaalmethoden.\n\n"
            "6.4 Nevumo houdt geen klantgeld aan op eigen rekeningen. Alle financiele "
            "intermediatie wordt uitsluitend via Stripe afgehandeld.\n\n"
            "6.5 Dienstverleners zijn als enige verantwoordelijk voor het uitsturen van "
            "facturen, het innen van belastingen (btw, inkomstenbelasting) en het naleven van "
            "alle toepasselijke fiscale verplichtingen."
        ),
        "pt": (
            "6.1 A Plataforma e atualmente gratuita para os Prestadores durante a fase de "
            "lancamento. A Lista de precos vigente esta disponivel em nevumo.com/pricing.\n\n"
            "6.2 A Nevumo reserva-se o direito de introduzir uma comissao ou funcionalidades "
            "pagas. Qualquer introducao sera anunciada com pelo menos 30 dias de aviso escrito "
            "antes de entrar em vigor.\n\n"
            "6.3 Se a Nevumo introduzir processamento de pagamentos, os pagamentos serao "
            "processados pela Stripe Inc. Na Polonia, BLIK e Przelewy24 estao disponiveis como "
            "metodos de pagamento.\n\n"
            "6.4 A Nevumo nao reten fundos de Clientes em contas proprias. Toda a intermediacao "
            "financeira e gerida exclusivamente atraves da Stripe.\n\n"
            "6.5 Os Prestadores sao os unicos responsaveis pela emissao de faturas, cobranca de "
            "impostos (IVA, imposto sobre o rendimento) e cumprimento de todas as obrigacoes "
            "fiscais aplicaveis."
        ),
        "pt-PT": (
            "6.1 A Plataforma e actualmente gratuita para os Prestadores durante a fase de "
            "lancamento. A Lista de precos em vigor esta disponivel em nevumo.com/pricing.\n\n"
            "6.2 A Nevumo reserva-se o direito de introduzir uma comissao ou funcionalidades "
            "pagas. Qualquer introducao sera anunciada com pelo menos 30 dias de aviso previo "
            "escrito antes de entrar em vigor.\n\n"
            "6.3 Se a Nevumo introduzir processamento de pagamentos, os pagamentos serao "
            "processados pela Stripe Inc. Na Polonia, BLIK e Przelewy24 estao disponiveis como "
            "metodos de pagamento.\n\n"
            "6.4 A Nevumo nao deten fundos de Clientes em contas proprias. Toda a intermediacao "
            "financeira e gerida exclusivamente atraves da Stripe.\n\n"
            "6.5 Os Prestadores sao os unicos responsaveis pela emissao de faturas, cobranca de "
            "impostos (IVA, imposto sobre o rendimento) e cumprimento de todas as obrigacoes "
            "fiscais aplicaveis."
        ),
        "ro": (
            "6.1 Platforma este in prezent gratuita pentru Furnizori in timpul fazei de "
            "lansare. Lista de preturi actuala este disponibila la nevumo.com/pricing.\n\n"
            "6.2 Nevumo isi rezerva dreptul de a introduce un comision sau functionalitati "
            "platite. Orice introducere va fi anuntata cu cel putin 30 de zile notificare "
            "scrisa inainte de intrarea in vigoare.\n\n"
            "6.3 Daca Nevumo introduce procesarea platilor, platile vor fi procesate de "
            "Stripe Inc. In Polonia, BLIK si Przelewy24 vor fi disponibile ca metode de "
            "plata.\n\n"
            "6.4 Nevumo nu retine fondurile Clientilor in conturile proprii. Toata "
            "intermedierea financiara este gestionata exclusiv prin Stripe.\n\n"
            "6.5 Furnizorii sunt singurii responsabili pentru emiterea facturilor, colectarea "
            "taxelor (TVA, impozit pe venit) si respectarea tuturor obligatiilor fiscale "
            "aplicabile."
        ),
        "ru": (
            "6.1 Platforma v nastoyashcheye vremya besplatnа dlya Postavshchikov vo vremya "
            "startovoy fazy. Tekushchiy Preyskurant dostupеn na nevumo.com/pricing.\n\n"
            "6.2 Nevumo ostavlyayet za soboy pravo vvesti komissiyu ili platnye funktsii. "
            "Lyuboye vvedeniye budet ob'yavleno s preduprezhdeniyet ne meneye 30 dney do "
            "vstupleniya v silu.\n\n"
            "6.3 Yesli Nevumo vvedet obrabotku platezhey, platezhi budut obrabatyvatsya "
            "Stripe Inc. V Polshe BLIK i Przelewy24 budut dostupny kak sposoby oplaty.\n\n"
            "6.4 Nevumo ne khranit sredstva Klientov na sobstvennykh schetakh. Vsyo "
            "finansovoye posrednichestvo osushchestvlyaetsya isklyuchitelno cherez Stripe.\n\n"
            "6.5 Postavshchiki nesut edinstvennuyu otvetstvennost za vystavleniye schetov, "
            "sbor nalogov (NDS, podokhodnyy nalog) i soblyudeniye vsekh primenimoykh "
            "nalogovykh obyazatelstv."
        ),
        "uk": (
            "6.1 Platforma zaraz bezkoshtovna dlya Postachalnikiv pid chas startovoi fazy. "
            "Aktualnyy Preyskurant dostupnyy na nevumo.com/pricing.\n\n"
            "6.2 Nevumo zalyshaye za soboyu pravo vvesty komisiyu abo platni funktsiyi. "
            "Bud-yake vprovadzhennia bude anonsovano z poperedzhennyam ne menshe 30 dniv "
            "pered nabrannyam chynnosti.\n\n"
            "6.3 Yakshcho Nevumo vprovadyt obrobku platezhiv, platezhi obrobyatymutsia "
            "Stripe Inc. U Polshchi BLIK i Przelewy24 budut dostupni yak sposoby oplaty.\n\n"
            "6.4 Nevumo ne zberihaie koshty Kliyentiv na vlasnykh rakhunkakh. Vse finansove "
            "poserednytsvo zdiisnyyetsya vyklyuchno cherez Stripe.\n\n"
            "6.5 Postachalnyki nesut yedynu vidpovidalnist za vystavlennia rakhunkiv, zbir "
            "podatkiv (PDV, prybuttkovyy podatok) ta dotrymannia vsikh zastosvovnykh "
            "podatkovykh zobov'yazan."
        ),
        "cs": (
            "6.1 Platforma je v soucasne dobe pro Poskytovatele bezblatna behem spusteni. "
            "Aktualny Cenik je dostupny na nevumo.com/pricing.\n\n"
            "6.2 Nevumo si vyhrazuje pravo zavest provizi nebo placene funkce. Kazde zavedeni "
            "bude oznameno s predstihom nejmeně 30 dni pisemnym upozornenim pred nabytim "
            "ucinnosti.\n\n"
            "6.3 Pokud Nevumo zavede zpracovani plateb, platby budou zpracovavany Stripe Inc. "
            "V Polsku budou BLIK a Przelewy24 dostupne jako platebni metody.\n\n"
            "6.4 Nevumo nespravuje prostredky Klientu na vlastnich uctech. Veskera financni "
            "sprostredkovani je riseno vyhradne prostrednictvim Stripe.\n\n"
            "6.5 Poskytovatelé jsou vyhradne zodpovedni za vystavovani faktur, vybir dani "
            "(DPH, dan z prijmu) a dodrzovani vsech platnych danovych povinnosti."
        ),
        "da": (
            "6.1 Platformen er i ojeblikket gratis for Udbydere i lanceringsperioden. Den "
            "aktuelle Prisliste er tilgaengelig paa nevumo.com/pricing.\n\n"
            "6.2 Nevumo forbeholder sig retten til at indfoere provision eller betalte "
            "funktioner med mindst 30 dages skriftligt varsel foer ikrafttraedelse.\n\n"
            "6.3 Hvis Nevumo indfoerer betalingsbehandling, vil betalinger blive behandlet af "
            "Stripe Inc. I Polen vil BLIK og Przelewy24 vaere tilgaengelige som "
            "betalingsmetoder.\n\n"
            "6.4 Nevumo holder ikke klientmidler paa egne konti. Al finansiel formidling "
            "haandteres udelukkende via Stripe.\n\n"
            "6.5 Udbydere er alene ansvarlige for at udstede fakturaer, opkraeve afgifter "
            "(moms, indkomstskat) og overholde alle gaeldende skattemaessige forpligtelser."
        ),
        "sv": (
            "6.1 Plattformen ar for narvarande gratis for Leverantorer under lanseringsfasen. "
            "Den aktuella Prislistan finns pa nevumo.com/pricing.\n\n"
            "6.2 Nevumo forbehaller sig ratten att infora provision eller betalda funktioner "
            "med minst 30 dagars skriftlig forvaning innan ikraftträdande.\n\n"
            "6.3 Om Nevumo infor betalningshantering, kommer betalningar att behandlas av "
            "Stripe Inc. I Polen kommer BLIK och Przelewy24 att finnas som "
            "betalningsmetoder.\n\n"
            "6.4 Nevumo innehar inte kundmedel pa egna konton. All finansiell formedling "
            "hanteras uteslutande via Stripe.\n\n"
            "6.5 Leverantorer ar ensamt ansvariga for att utfarda fakturor, uppbara skatter "
            "(moms, inkomstskatt) och efterleva alla tillampliga skattemassiga skyldigheter."
        ),
        "no": (
            "6.1 Plattformen er for oyeblikket gratis for Leverandorer i lanseringsfasen. "
            "Gjeldende Prisliste er tilgjengelig pa nevumo.com/pricing.\n\n"
            "6.2 Nevumo forbeholder seg retten til a innfore provisjon eller betalte "
            "funksjoner med minst 30 dagers skriftlig varsel for ikrafttredelse.\n\n"
            "6.3 Hvis Nevumo innforer betalingsbehandling, vil betalinger bli behandlet av "
            "Stripe Inc. I Polen vil BLIK og Przelewy24 vaere tilgjengelige som "
            "betalingsmetoder.\n\n"
            "6.4 Nevumo holder ikke klientmidler pa egne kontoer. All finansiell formidling "
            "haandteres utelukkende via Stripe.\n\n"
            "6.5 Leverandorer er alene ansvarlige for a utstede fakturaer, innkreve avgifter "
            "(moms, inntektsskatt) og overholde alle gjeldende skattemessige forpliktelser."
        ),
        "fi": (
            "6.1 Alusta on tällä hetkellä ilmainen Palveluntarjoajille käynnistysvaiheessa. "
            "Nykyinen Hinnasto on saatavilla osoitteessa nevumo.com/pricing.\n\n"
            "6.2 Nevumo pidättää oikeuden ottaa käyttöön provision tai maksullisia "
            "ominaisuuksia vähintään 30 päivän kirjallisella ilmoituksella ennen "
            "voimaantuloa.\n\n"
            "6.3 Jos Nevumo ottaa käyttöön maksukäsittelyn, maksut käsittelee Stripe Inc. "
            "Puolassa BLIK ja Przelewy24 ovat käytettävissä maksutapoina.\n\n"
            "6.4 Nevumo ei pidä asiakasvaroja omilla tileillään. Kaikki rahoituksen välitys "
            "hoidetaan yksinomaan Stripen kautta.\n\n"
            "6.5 Palveluntarjoajat ovat yksin vastuussa laskujen kirjoittamisesta, verojen "
            "(ALV, tulovero) perimisestä ja kaikkien sovellettavien verovelvoitteiden "
            "noudattamisesta."
        ),
        "et": (
            "6.1 Platvorm on praegu Teenusepakkujatele tasuta käivitusfaasis. Kehtiv Hinnakiri "
            "on saadaval aadressil nevumo.com/pricing.\n\n"
            "6.2 Nevumo jätab endale õiguse võtta kasutusele vahendustasu või tasulisi "
            "funktsioone vähemalt 30 päeva ette teatisega enne jõustumist.\n\n"
            "6.3 Kui Nevumo võtab kasutusele maksete töötlemise, töötleb makseid Stripe Inc. "
            "Poolas on BLIK ja Przelewy24 saadaval makseviisidena.\n\n"
            "6.4 Nevumo ei hoia klientide vahendeid oma kontodel. Kogu rahaline vahendamine "
            "toimub eranditult Stripe kaudu.\n\n"
            "6.5 Teenusepakkujad vastutavad ainuisikuliselt arvete väljastamise, maksude "
            "(käibemaks, tulumaks) kogumise ja kõigi kohaldatavate maksuõiguslike kohustuste "
            "täitmise eest."
        ),
        "lt": (
            "6.1 Platforma šiuo metu yra nemokama Teikejams paleidimo fazeje. Dabartinis "
            "Kainyne prieinama nevumo.com/pricing.\n\n"
            "6.2 Nevumo pasilieka teise ivesti komisini atlyginima ar mokamas funkcijas su "
            "ne maziau kaip 30 dienu raštišku pranesumu pries isigaliojima.\n\n"
            "6.3 Jei Nevumo ivedys mokejimo apdorojima, mokejimus apdoros Stripe Inc. "
            "Lenkijoje BLIK ir Przelewy24 bus prieinami kaip mokejimo budai.\n\n"
            "6.4 Nevumo nelaiko Klientu lesu savo sąskaitose. Visas finansinis tarpininkavimas "
            "vykdomas iskirtinai per Stripe.\n\n"
            "6.5 Teikejai yra iskirtinai atsakingi uz sąskaitų faktūrų israsymą, mokesciu "
            "(PVM, pajamu mokestis) surinkimą ir visu taikomu fiskalinių pareigų laikymąsi."
        ),
        "lv": (
            "6.1 Platforma pašlaik ir bezmaksas Sniedzejiem palaišanas faze. Pašreizejais "
            "Cenradis pieejams nevumo.com/pricing.\n\n"
            "6.2 Nevumo patur tiesibas ieviest komisijas maksu vai maksas funkcijas vismaz "
            "30 dienas iepriekš ar rakstisku pazinojumu pirms stašanas speka.\n\n"
            "6.3 Ja Nevumo ievies maksajumu apstradi, maksajumus apstrades Stripe Inc. "
            "Polija BLIK un Przelewy24 bus pieejami ka maksajumu metodes.\n\n"
            "6.4 Nevumo neglaba Klientu lidzeklus savos kontos. Visi finansialie starpniecibas "
            "dariji tiek veikti izkartingi caur Stripe.\n\n"
            "6.5 Sniedzaji ir vienigie atbildigi par rēķinu izrakstišanu, nodoklu iekasešanu "
            "un visu piemerojamo nodoklu saistību ievērošanu."
        ),
        "hu": (
            "6.1 A Platform jelenleg ingyenes a Szolgáltatok számára az indulási fázisban. "
            "Az aktuális Árlista elérhető a nevumo.com/pricing oldalon.\n\n"
            "6.2 A Nevumo fenntartja a jogot jutalék vagy fizetős funkciók bevezetésére "
            "legalább 30 napos írásbeli értesítéssel a hatálybalépés előtt.\n\n"
            "6.3 Ha a Nevumo bevezeti a fizetések feldolgozását, a fizetéseket a Stripe Inc. "
            "kezeli. Lengyelországban a BLIK és a Przelewy24 elérhető fizetési módként.\n\n"
            "6.4 A Nevumo nem tart Ügyfelektől érkező pénzeszközöket saját számlákon. Az "
            "összes pénzügyi közvetítés kizárólag a Stripe-on keresztül történik.\n\n"
            "6.5 A Szolgáltatók kizárólag felelősek a számlák kiállításáért, az adók "
            "(áfa, jövedelemadó) beszedéséért és az összes alkalmazható adóügyi kötelezettség "
            "betartásáért."
        ),
        "hr": (
            "6.1 Platforma je trenutno besplatna za Pruzatelje u fazi pokretanja. Aktualni "
            "Cjenik dostupan je na nevumo.com/pricing.\n\n"
            "6.2 Nevumo zadrzava pravo uvesti proviziju ili placene funkcije s najmanje 30 "
            "dana pisanog prethodnog obavijesti prije stupanja na snagu.\n\n"
            "6.3 Ako Nevumo uvede obradu placanja, placanja ce procesirati Stripe Inc. U "
            "Poljskoj BLIK i Przelewy24 bit ce dostupni kao nacini placanja.\n\n"
            "6.4 Nevumo ne drzi sredstva Klijenata na vlastitim racunima. Sve financijsko "
            "posredovanje obavlja se iskljucivo putem Stripe-a.\n\n"
            "6.5 Pruzatelji su iskljucivo odgovorni za izdavanje racuna, naplatu poreza "
            "(PDV, porez na dohodak) i postivanje svih primjenjivih fiskalnih obveza."
        ),
        "sk": (
            "6.1 Platforma je v sucasnosti bezplatna pre Poskytovatelov pocas fazy spustenia. "
            "Aktualny Cennik je dostupny na nevumo.com/pricing.\n\n"
            "6.2 Nevumo si vyhrazuje pravo zaviest provizii alebo platene funkcie s "
            "najmenej 30-dennym pisomnym upozornenim pred nabytim ucinnosti.\n\n"
            "6.3 Ak Nevumo zavedie spracovanie platob, platby bude spracovávat Stripe Inc. "
            "V Polsku budu BLIK a Przelewy24 dostupne ako platobne metody.\n\n"
            "6.4 Nevumo nespravuje prostriedky Zákaznikov na vlastnych uctoch. Vsetko "
            "financne sprostredkovanie sa vykonáva výhradne prostrednictvom Stripe.\n\n"
            "6.5 Poskytovatelia su vyhradne zodpovedni za vystavovanie faktur, vyber dani "
            "(DPH, dan z prijmov) a dodrzovanie vsetkych platnych danovych povinnosti."
        ),
        "sl": (
            "6.1 Platforma je za Ponudnike v fazi zagona brezplacna. Veljavni Cenik je na "
            "voljo na nevumo.com/pricing.\n\n"
            "6.2 Nevumo si pridrzuje pravico uvesti provizijo ali placljive funkcije z "
            "vsaj 30-dnevnim pisnim obvestilom pred uveljavitvijo.\n\n"
            "6.3 Ce Nevumo uvede obdelavo placil, bodo placila obdelana pri Stripe Inc. Na "
            "Poljskem sta BLIK in Przelewy24 na voljo kot nacina placila.\n\n"
            "6.4 Nevumo ne hrani sredstev Strank na lastnih racunih. Vse financno "
            "posredovanje poteka izkljucno prek Stripe.\n\n"
            "6.5 Ponudniki so izkljucno odgovorni za izdajanje racunov, pobiranje davkov "
            "(DDV, dohodnina) in spoštovanje vseh veljavnih davčnih obveznosti."
        ),
        "el": (
            "6.1 I Platforma einai epí tou parontos dorean gia tous Parochous kata ti fasi "
            "ekkinisis. I Timokatalogos einai diathesimi sto nevumo.com/pricing.\n\n"
            "6.2 I Nevumo diatirei to dikaioma na eisagei provmitheia i pliromes leitourgies "
            "me toulachiton 30 imeron eggrapho proeídopisi prin tin enargeia.\n\n"
            "6.3 An i Nevumo eisagei epexergasia pliromon, oi pliromes tha epexergastoun apo "
            "tin Stripe Inc. Stin Polonia, BLIK kai Przelewy24 tha einai diathesima os "
            "methodoi pliromon.\n\n"
            "6.4 I Nevumo den diatirei kefalaia Pelatonon sta dika tis logistika. Ola ta "
            "oikonomika diamesolabisi diacheirizontai meso tis Stripe.\n\n"
            "6.5 Oi Párochoi einai mono ypéfthynoi gia tin ekdosi timologion, tin eispraxí "
            "foron (FPA, forologias eisodimatos) kai ti symmorfosi me oles tis efarmostees "
            "dimosionomikaes ypochreoseis."
        ),
        "tr": (
            "6.1 Platform, lansman aşamasında Saglayicilar için ücretsizdir. Güncel Fiyat "
            "Listesi nevumo.com/pricing adresinde mevcuttur.\n\n"
            "6.2 Nevumo, yürürlüge girmeden en az 30 gün önce yazılı bildirimle komisyon "
            "veya ücretli özellikler getirme hakkini saklı tutar.\n\n"
            "6.3 Nevumo ödeme işlemi başlatırsa, ödemeler Stripe Inc. tarafından işlenecektir. "
            "Polonya'da BLIK ve Przelewy24 ödeme yöntemi olarak mevcut olacaktir.\n\n"
            "6.4 Nevumo, kendi hesaplarında müşteri fonları bulundurmaz. Tüm finansal "
            "aracilik yalnizca Stripe üzerinden yürütülür.\n\n"
            "6.5 Saglayicilar, fatura düzenlemekten, vergi (KDV, gelir vergisi) tahsil "
            "etmekten ve tüm geçerli mali yükümlülüklere uymaktan münhasiran sorumludur."
        ),
        "ga": (
            "6.1 Ta an tArdan saor in aisce faoi lathair do Sholathroir le linn na ceim "
            "seolta. Ta an Liosta Praghsanna reatha ar fail ag nevumo.com/pricing.\n\n"
            "6.2 Coimeadann Nevumo an ceart coimisiun no gneíthe inloctha a thabhairt "
            "isteach le nios mo na 30 la fógra scríofa roimh theacht i bhfeidhm.\n\n"
            "6.3 Ma thugann Nevumo isteach próiseáil íocaíochtaí, próiseálfar íocaíochtaí "
            "ag Stripe Inc. Sa Pholainn, beidh BLIK agus Przelewy24 ar fáil mar mhodhanna "
            "íocaíochta.\n\n"
            "6.4 Ní chothaíonn Nevumo cistí Custaimeri ar a cuntais féin. Déileáiltear le "
            "gach idirghabháil airgeadais go heisiach tríd Stripe.\n\n"
            "6.5 Tá Solathroir freagrach go heisiach as sonraisc a eisiúint, as cánacha "
            "(CBL, cáin ioncaim) a bhailiú, agus as gach oibleagáid fhioscach infheidhme "
            "a chomhlíonadh."
        ),
        "is": (
            "6.1 Vettvangurinn er sem stendur gjaldfrjals fyrir Veituadila a raesingstigi. "
            "Gildandi Verdskra er faanleg a nevumo.com/pricing.\n\n"
            "6.2 Nevumo askilur ser rett til ad innleida thoknun eda greiddar adgerdir med "
            "minnst 30 daga skriflegum fyrirvara adur en thad tekur gildi.\n\n"
            "6.3 Ef Nevumo innleidur greidslumedferd, verda greidslur unnar af Stripe Inc. "
            "I Pollandi verda BLIK og Przelewy24 taelkaer sem greidslumatar.\n\n"
            "6.4 Nevumo geymir ekki fjaermuni vidskiptavina a eigin reikningum. Allar "
            "fjarhagslegar milligangu eru afgreiddar eingongu i gegnum Stripe.\n\n"
            "6.5 Veituadilar bera eina abyrgd a utgafu reikninga, innheimtu skatta (VSK, "
            "tekjuskatts) og ad fylgja ollum gildandi skattalegum skyldum."
        ),
        "lb": (
            "6.1 D'Plattform ass momentan fir Presser wärend der Startphase gratis. "
            "D'aktuell Präislëschte ass ënner nevumo.com/pricing verfügbar.\n\n"
            "6.2 Nevumo behält sech d'Recht, eng Kommissioun oder bezuelte Funktiounen "
            "mat mindestens 30 Deeg Virankündigung virum Akraafttriede anzefüren.\n\n"
            "6.3 Wann Nevumo Zahlungsbehandlung agefouert gëtt, ginn d'Bezuelungen vun "
            "Stripe Inc. behandelt. A Polen ginn BLIK a Przelewy24 als Bezuelungsmethod "
            "disponibel sinn.\n\n"
            "6.4 Nevumo hält keng Clientmëttelen op eegene Konten. All Finanzvermittlung "
            "gëtt ausschliesslich via Stripe ofgewickelt.\n\n"
            "6.5 Presser sinn alleng verantwortlech fir d'Ausstelle vun Rechnungen, "
            "d'Asammele vun Steieren (MwSt., Akommessteier) an d'Ahalten vun allen "
            "gëlltende Steierflichten."
        ),
        "mk": (
            "6.1 Platformata e momentalno besplatna za Davacite vo tekot na startovata "
            "faza. Tekochniot Cenovnik e dostapen na nevumo.com/pricing.\n\n"
            "6.2 Nevumo go zadrзuva pravoto da vovede provizija ili plateni funkcii so "
            "najmalku 30 dena pisano predizvestuvanje pred vleguvanje vo sila.\n\n"
            "6.3 Ako Nevumo vovede obrabotka na placanjata, placanjata ke gi obrabotuva "
            "Stripe Inc. Vo Polska, BLIK i Przelewy24 ke bidat dostapni kako nacini na "
            "placanje.\n\n"
            "6.4 Nevumo ne cuva sredstva na Klientite na sopstveni smetki. Сeto finansisko "
            "posrednistvo se vrshi iskljucivo preku Stripe.\n\n"
            "6.5 Davacite se iskljucivo odgovorni za izdavanje smetki, naplata danoci "
            "(DDV, danok na prihod) i spazuvanje na site primenljivi fiskalni obvrski."
        ),
        "mt": (
            "6.1 Il-Pjattaforma hija bhalissa bla hlas ghall-Fornituri matul il-fazi "
            "tal-varar. Il-Lista tal-Prezz kurrenti hija disponibbli fuq nevumo.com/pricing.\n\n"
            "6.2 Nevumo tizzomm id-dritt li tintroduci kummissjoni jew karatteristici mhallsa "
            "b'avviz bil-miktub ta mhux anqas minn 30 jum qabel ma jidhal fis-sehh.\n\n"
            "6.3 Jekk Nevumo tintroduci l-ipproċessar ta pagamenti, il-hlasijiet jigu "
            "pproċessati minn Stripe Inc. Fil-Polonja, BLIK u Przelewy24 se jkunu disponibbli "
            "bhala metodi ta hlas.\n\n"
            "6.4 Nevumo ma zzommx fondi tal-Klijenti fil-kontijiet taghha stess. "
            "L-intermedijazzjonifinanzjarja kollha tiġi ttrattata permezz ta Stripe.\n\n"
            "6.5 Il-Fornituri huma l-uniċi responsabbli biex johorgu fatturi, jiġbru "
            "t-taxxi (VAT, taxxa fuq l-introjtu) u jikkonformaw mal-obbligi fiskaċi "
            "applikabbli kollha."
        ),
        "sq": (
            "6.1 Platforma eshte aktualisht falas per Ofruesit gjate fazes se nisjes. "
            "Lista aktuale e Cmimeve eshte e disponueshme ne nevumo.com/pricing.\n\n"
            "6.2 Nevumo ruan te drejten te prezantoje nje komision ose funksione te paguara "
            "me se pakten 30 dite paralajmerim me shkrim para hyrjes ne fuqi.\n\n"
            "6.3 Nese Nevumo prezanton perпunimin e pagesave, pagesat do te perpunohen nga "
            "Stripe Inc. Ne Poloni, BLIK dhe Przelewy24 do te jene te disponueshme si "
            "metoda pagese.\n\n"
            "6.4 Nevumo nuk mban fonde te Klienteve ne llogarite e veta. E gjitha "
            "ndermjetesimi financiar trajtohet ekskluzivisht nepermjet Stripe.\n\n"
            "6.5 Ofruesit jane vetem pergjegjese per leshimin e faturave, mbledhjen e "
            "taksave (TVSH, tatim mbi te ardhurat) dhe respektimin e te gjitha detyrimeve "
            "fiskale te zbatueshme."
        ),
        "sr": (
            "6.1 Platforma je trenutno besplatna za Pruzaoce u fazi pokretanja. Aktuelni "
            "Cenovnik dostupan je na nevumo.com/pricing.\n\n"
            "6.2 Nevumo zadrzava pravo da uvede proviziju ili placene funkcije sa najmanje "
            "30 dana pisanog prethodnog obavestenja pre stupanja na snagu.\n\n"
            "6.3 Ako Nevumo uvede obradu placanja, placanja ce obradivati Stripe Inc. U "
            "Poljskoj, BLIK i Przelewy24 bice dostupni kao nacini placanja.\n\n"
            "6.4 Nevumo ne cuva sredstva Klijenata na sopstvenim racunima. Sve finansijsko "
            "posredovanje obavlja se iskljucivo putem Stripe-a.\n\n"
            "6.5 Pruzaoci su iskljucivo odgovorni za izdavanje racuna, naplatu poreza "
            "(PDV, porez na dohodak) i postivanje svih primenljivih fiskalnih obaveza."
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
        print(
            f"✅ seed_provider_terms_p13_art6_body: {count} rows upserted "
            f"({NAMESPACE}: art6_body x 34 langs)"
        )

    engine.dispose()


if __name__ == "__main__":
    seed()
