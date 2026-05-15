"""
seed_terms_p5_bodies.py  —  Nevumo | namespace: terms
Key: art5_body (34 езика)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_terms_p5_bodies
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
    "art5_body": {
        "en": (
            '5.1 As a client, you may submit a service request ("lead") describing the '
            'service you need, your location, budget expectations, and preferred timing.\n\n'
            '5.2 Nevumo forwards your request to relevant providers in your area. Providers '
            'may respond with offers, questions, or confirmations.\n\n'
            '5.3 Submitting a lead does not create a binding contract. A contract is formed '
            'only when you and the provider expressly agree on the terms of the service.\n\n'
            '5.4 You must not submit requests for services that are illegal, dangerous, or '
            'that violate these Terms.'
        ),
        "pl": (
            '7.1 Klient może złożyć zapytanie o usługę ("zapytanie/lead") opisując zakres '
            'usługi, lokalizację, oczekiwany budżet i preferowany termin.\n\n'
            '7.2 Nevumo przekazuje zapytanie odpowiednim Usługodawcom w danej lokalizacji. '
            'Usługodawcy mogą odpowiedzieć ofertą, pytaniami lub potwierdzeniem dostępności.\n\n'
            '7.3 Złożenie zapytania nie stanowi zawarcia umowy. Umowa o świadczenie usługi '
            'powstaje wyłącznie w wyniku wyraźnego porozumienia Klienta i Usługodawcy co do '
            'warunków usługi.\n\n'
            '7.4 Klient nie może składać zapytań dotyczących usług nielegalnych, '
            'niebezpiecznych lub naruszających niniejszy Regulamin.'
        ),
        "bg": (
            '5.1 Клиентът може да подаде запитване ("lead"), описващо необходимата услуга, '
            'местоположение, бюджетни очаквания и предпочитан срок.\n\n'
            '5.2 Nevumo препраща запитването до подходящи Доставчици в района. Доставчиците '
            'могат да отговорят с оферта, въпроси или потвърждение.\n\n'
            '5.3 Подаването на запитване не представлява сключване на договор. Договорът за '
            'услуга се сключва само при изрично споразумение между Клиента и Доставчика.\n\n'
            '5.4 Клиентът не може да подава запитвания за незаконни, опасни или нарушаващи '
            'настоящите ОУ услуги.'
        ),
        "cs": (
            '5.1 Jako klient můžete podat žádost o službu (tzv. "lead"), která popisuje '
            'požadovanou službu, vaši polohu, rozpočtová očekávání a preferovaný termín.\n\n'
            '5.2 Nevumo přepošle váš požadavek relevantním poskytovatelům ve vaší oblasti. '
            'Poskytovatelé mohou reagovat nabídkami, dotazy nebo potvrzeními.\n\n'
            '5.3 Odeslání leadu nevytváří závaznou smlouvu. Smlouva vzniká pouze tehdy, když '
            'vy a poskytovatel výslovně souhlasíte s podmínkami služby.\n\n'
            '5.4 Nesmíte podávat žádosti o služby, které jsou nezákonné, nebezpečné nebo '
            'porušují tyto podmínky.'
        ),
        "da": (
            '5.1 Som klient kan du indsende en serviceanmodning ("lead"), der beskriver den '
            'service, du har brug for, din placering, budgetforventninger og foretrukket '
            'timing.\n\n'
            '5.2 Nevumo videresender din anmodning til relevante udbydere i dit område. '
            'Udbydere kan svare med tilbud, spørgsmål eller bekræftelser.\n\n'
            '5.3 Indsendelse af et lead skaber ikke en bindende kontrakt. En kontrakt dannes '
            'kun, når du og udbyderen udtrykkeligt er enige om betingelserne for tjenesten.\n\n'
            '5.4 Du må ikke indsende anmodninger om tjenester, der er ulovlige, farlige eller '
            'overtræder disse vilkår.'
        ),
        "de": (
            '5.1 Als Kunde können Sie eine Dienstleistungsanfrage ("Lead") einreichen, in der '
            'Sie die benötigte Dienstleistung, Ihren Standort, Budgeterwartungen und den '
            'bevorzugten Zeitpunkt beschreiben.\n\n'
            '5.2 Nevumo leitet Ihre Anfrage an relevante Anbieter in Ihrer Umgebung weiter. '
            'Anbieter können mit Angeboten, Fragen oder Bestätigungen antworten.\n\n'
            '5.3 Das Einreichen eines Leads begründet keinen bindenden Vertrag. Ein Vertrag '
            'kommt nur zustande, wenn Sie und der Anbieter die Bedingungen der Dienstleistung '
            'ausdrücklich vereinbaren.\n\n'
            '5.4 Sie dürfen keine Anfragen für Dienstleistungen einreichen, die illegal, '
            'gefährlich oder mit diesen Bedingungen unvereinbar sind.'
        ),
        "el": (
            '5.1 Ως πελάτης, μπορείτε να υποβάλετε ένα αίτημα υπηρεσίας ("lead") που '
            'περιγράφει την υπηρεσία που χρειάζεστε, την τοποθεσία σας, τις προσδοκίες '
            'προϋπολογισμού και τον προτιμώμενο χρόνο.\n\n'
            '5.2 Το Nevumo προωθεί το αίτημά σας σε σχετικούς παρόχους στην περιοχή σας. '
            'Οι πάροχοι μπορούν να απαντήσουν με προσφορές, ερωτήσεις ή επιβεβαιώσεις.\n\n'
            '5.3 Η υποβολή ενός lead δεν δημιουργεί δεσμευτική σύμβαση. Σύμβαση συνάπτεται '
            'μόνο όταν εσείς και ο πάροχος συμφωνήσετε ρητά στους όρους της υπηρεσίας.\n\n'
            '5.4 Δεν πρέπει να υποβάλλετε αιτήματα για υπηρεσίες που είναι παράνομες, '
            'επικίνδυνες ή παραβιάζουν τους παρόντες Όρους.'
        ),
        "es": (
            '5.1 Como cliente, puede enviar una solicitud de servicio ("lead") describiendo '
            'el servicio que necesita, su ubicación, expectativas de presupuesto y horario '
            'preferido.\n\n'
            '5.2 Nevumo reenvía su solicitud a proveedores relevantes en su área. Los '
            'proveedores pueden responder con ofertas, preguntas o confirmaciones.\n\n'
            '5.3 Enviar un lead no crea un contrato vinculante. Un contrato se forma solo '
            'cuando usted y el proveedor acuerdan expresamente los términos del servicio.\n\n'
            '5.4 No debe enviar solicitudes de servicios que sean ilegales, peligrosos o '
            'que violen estos Términos.'
        ),
        "et": (
            '5.1 Kliendina võite esitada teenusepäringu ("lead"), mis kirjeldab vajalikku '
            'teenust, teie asukohta, eelarvelist ootust ja eelistatud ajastust.\n\n'
            '5.2 Nevumo edastab teie päringu asjakohastele teenusepakkujatele teie piirkonnas. '
            'Pakkujad võivad vastata pakkumuste, küsimuste või kinnitustega.\n\n'
            '5.3 Päringu esitamine ei loo sidusat lepingut. Leping sõlmitakse ainult siis, '
            'kui teie ja pakkuja lepivad teenuse tingimused selgesõnaliselt kokku.\n\n'
            '5.4 Te ei tohi esitada päringuid teenuste kohta, mis on ebaseaduslikud, '
            'ohtlikud või rikuvad käesolevaid tingimusi.'
        ),
        "fi": (
            '5.1 Asiakkaana voit lähettää palvelupyynnön ("liidi"), jossa kuvaat tarvitsemaasi '
            'palvelua, sijaintiasi, budjettiodotuksiasi ja haluamaasi ajankohtaa.\n\n'
            '5.2 Nevumo välittää pyyntösi asiaankuuluville palveluntarjoajille alueellasi. '
            'Palveluntarjoajat voivat vastata tarjouksilla, kysymyksillä tai vahvistuksilla.\n\n'
            '5.3 Liidin lähettäminen ei luo sitovaa sopimusta. Sopimus syntyy vain, kun '
            'sinä ja palveluntarjoaja nimenomaisesti sovitte palvelun ehdoista.\n\n'
            '5.4 Et saa lähettää pyyntöjä palveluista, jotka ovat laittomia, vaarallisia tai '
            'rikkovat näitä ehtoja.'
        ),
        "fr": (
            '5.1 En tant que client, vous pouvez soumettre une demande de service ("lead") '
            'décrivant le service dont vous avez besoin, votre localisation, vos attentes '
            'budgétaires et le calendrier souhaité.\n\n'
            '5.2 Nevumo transmet votre demande aux prestataires pertinents de votre zone. '
            'Les prestataires peuvent répondre par des offres, des questions ou des '
            'confirmations.\n\n'
            '5.3 La soumission d\'un lead ne crée pas de contrat contraignant. Un contrat '
            'n\'est formé que lorsque vous et le prestataire convenez expressément des '
            'conditions du service.\n\n'
            '5.4 Vous ne devez pas soumettre de demandes pour des services illégaux, '
            'dangereux ou contraires aux présentes Conditions.'
        ),
        "ga": (
            '5.1 Mar chliant, féadfaidh tú iarratas seirbhíse ("lead") a chur isteach ag '
            'cur síos ar an tseirbhís a theastaíonn uait, do shuíomh, do bhúiséad ionchasach '
            'agus do thimthriall roghnach.\n\n'
            '5.2 Cuireann Nevumo do iarratas ar aghaidh chuig soláthróirí ábhartha i do '
            'cheantar. Féadfaidh soláthróirí freagra a thabhairt le tairiscintí, ceisteanna '
            'nó deimhnithe.\n\n'
            '5.3 Ní chruthaíonn cur isteach leaid conradh ceangailteach. Ní fhoirmítear '
            'conradh ach nuair a chomhaontaíonn tú féin agus an soláthróir go sainráite ar '
            'théarmaí na seirbhíse.\n\n'
            '5.4 Ní cheadaítear duit iarratais a chur isteach ar sheirbhísí atá neamhdhleathach, '
            'contúirteach nó a sháraíonn na Téarmaí seo.'
        ),
        "hr": (
            '5.1 Kao klijent možete podnijeti zahtjev za uslugom ("lead") opisujući uslugu '
            'koja vam je potrebna, vašu lokaciju, budžetska očekivanja i preferirani termin.\n\n'
            '5.2 Nevumo prosljeđuje vaš zahtjev relevantnim davateljima u vašem području. '
            'Davatelji mogu odgovoriti ponudama, pitanjima ili potvrdama.\n\n'
            '5.3 Podnošenje leada ne stvara obvezujući ugovor. Ugovor se sklapa samo kada vi '
            'i davatelj usluge izričito dogovorite uvjete usluge.\n\n'
            '5.4 Ne smijete podnositi zahtjeve za usluge koje su nezakonite, opasne ili '
            'krše ove Uvjete.'
        ),
        "hu": (
            '5.1 Ügyfélként benyújthat egy szolgáltatáskérést ("lead"), amelyben leírja a '
            'szükséges szolgáltatást, tartózkodási helyét, költségvetési elvárásait és '
            'preferált időpontját.\n\n'
            '5.2 A Nevumo továbbítja kérését a releváns szolgáltatóknak az ön területén. '
            'A szolgáltatók ajánlatokkal, kérdésekkel vagy visszaigazolásokkal válaszolhatnak.\n\n'
            '5.3 A lead benyújtása nem hoz létre kötelező érvényű szerződést. Szerződés csak '
            'akkor jön létre, ha ön és a szolgáltató kifejezetten megállapodik a szolgáltatás '
            'feltételeiben.\n\n'
            '5.4 Nem nyújthat be kérelmeket olyan szolgáltatásokra, amelyek illegálisak, '
            'veszélyesek vagy sértik jelen feltételeket.'
        ),
        "is": (
            '5.1 Sem viðskiptavinur getur þú sent þjónustubeiðni ("lead") sem lýsir þeirri '
            'þjónustu sem þú þarfnast, staðsetningu þinni, fjárhagslegum væntingum og '
            'valinn tíma.\n\n'
            '5.2 Nevumo sendir beiðni þína til viðeigandi þjónustuaðila á þínu svæði. '
            'Þjónustuaðilar geta svarað með tilboðum, spurningum eða staðfestingum.\n\n'
            '5.3 Sending á leadi skapar ekki bindandi samning. Samningur myndast aðeins þegar '
            'þú og þjónustuaðilinn samþykkja skilmála þjónustunnar sérstaklega.\n\n'
            '5.4 Þú mátt ekki senda beiðnir um þjónustur sem eru ólöglegar, hættulegar eða '
            'brjóta í bága við þessa skilmála.'
        ),
        "it": (
            '5.1 Come cliente, puoi inviare una richiesta di servizio ("lead") descrivendo il '
            'servizio di cui hai bisogno, la tua posizione, le aspettative di budget e i '
            'tempi preferiti.\n\n'
            '5.2 Nevumo inoltra la tua richiesta ai prestatori pertinenti nella tua area. I '
            'prestatori possono rispondere con offerte, domande o conferme.\n\n'
            '5.3 L\'invio di un lead non crea un contratto vincolante. Un contratto si forma '
            'solo quando tu e il prestatore concordate espressamente i termini del servizio.\n\n'
            '5.4 Non devi inviare richieste per servizi illegali, pericolosi o che violano '
            'i presenti Termini.'
        ),
        "lb": (
            '5.1 Als Klient kënnt Dir eng Serviceanfro ("Lead") aschreiwen, déi d\'Servicer '
            'beschreift, déi Dir braucht, Är Lokatioun, Budgeterwaardungen an den '
            'bevorzugten Termin.\n\n'
            '5.2 Nevumo leede Är Ufro un relevante Prestatairë an Ärem Gebitt weider. '
            'Prestatairë kënne mat Offer, Froen oder Bestätegunge äntwerten.\n\n'
            '5.3 D\'Aschreiwe vun engem Lead schafft kee bindende Kontrakt. E Kontrakt '
            'gëtt nëmme geschloss wann Dir an de Prestataire sech ausdrécklech iwwer d\'Konditiounen '
            'vum Service eeneg sinn.\n\n'
            '5.4 Dir däerft keng Ufroen fir Servicer aschreiwen, déi illegal, geféierlech '
            'oder géint dës Bedéngungen sinn.'
        ),
        "lt": (
            '5.1 Kaip klientas galite pateikti paslaugos užklausą ("lead"), kurioje aprašote '
            'reikiamą paslaugą, vietą, biudžeto lūkesčius ir pageidaujamą laiką.\n\n'
            '5.2 Nevumo persiunčia jūsų užklausą atitinkamiems teikėjams jūsų rajone. '
            'Teikėjai gali atsakyti pasiūlymais, klausimais ar patvirtinimais.\n\n'
            '5.3 Užklausos pateikimas nesudaro privalomosios sutarties. Sutartis sudaroma '
            'tik tada, kai jūs ir teikėjas aiškiai susitariate dėl paslaugos sąlygų.\n\n'
            '5.4 Negalite teikti užklausų dėl paslaugų, kurios yra neteisėtos, pavojingos '
            'arba pažeidžia šias sąlygas.'
        ),
        "lv": (
            '5.1 Kā klients varat iesniegt pakalpojuma pieprasījumu ("lead"), aprakstot '
            'nepieciešamo pakalpojumu, jūsu atrašanās vietu, budžeta cerības un vēlamo laiku.\n\n'
            '5.2 Nevumo pārsūta jūsu pieprasījumu attiecīgajiem pakalpojumu sniedzējiem jūsu '
            'apkārtnē. Sniedzēji var atbildēt ar piedāvājumiem, jautājumiem vai apstiprinājumiem.\n\n'
            '5.3 Pieprasījuma iesniegšana nerada saistošu līgumu. Līgums tiek noslēgts tikai '
            'tad, kad jūs un sniedzējs skaidri vienojas par pakalpojuma noteikumiem.\n\n'
            '5.4 Jums nav atļauts iesniegt pieprasījumus par pakalpojumiem, kas ir nelikumīgi, '
            'bīstami vai pārkāpj šos noteikumus.'
        ),
        "mk": (
            '5.1 Како клиент, можете да поднесете барање за услуга ("lead") описувајќи ја '
            'потребната услуга, вашата локација, буџетски очекувања и саканиот рок.\n\n'
            '5.2 Nevumo го препраќа вашето барање до соодветни Даватели во вашата област. '
            'Давателите можат да одговорат со понуди, прашања или потврди.\n\n'
            '5.3 Поднесувањето на lead не претставува склучување договор. Договор се склучува '
            'само при изрично споразумување меѓу Клиентот и Давателот за условите на услугата.\n\n'
            '5.4 Клиентот не смее да поднесува барања за незаконски, опасни или услуги кои '
            'го кршат овој договор.'
        ),
        "mt": (
            '5.1 Bħala klijent, tista\' tissottometti talba għal servizz ("lead") li tiddeskrivi '
            's-servizz li teħtieġ, il-post tiegħek, l-aspettattivi tal-baġit u l-ħin '
            'preferut.\n\n'
            '5.2 Nevumo jgħaddi t-talba tiegħek lill-fornituri rilevanti fl-area tiegħek. '
            'Il-fornituri jistgħu jirrispondu b\'offerti, mistoqsijiet jew konfermi.\n\n'
            '5.3 Is-sottomissjoni ta\' lead ma toħloqx kuntratt vinkolanti. Kuntratt jiffurma '
            'biss meta inti u l-fornitur jaqblu b\'mod espliċitu fuq il-kundizzjonijiet '
            'tas-servizz.\n\n'
            '5.4 M\'għandekx tissottometti talbiet għal servizzi li huma illegali, perikolużi '
            'jew li jiksru dawn it-Termini.'
        ),
        "nl": (
            '5.1 Als klant kunt u een serviceverzoek ("lead") indienen waarin u de gewenste '
            'dienst, uw locatie, budgetverwachtingen en gewenste timing beschrijft.\n\n'
            '5.2 Nevumo stuurt uw verzoek door naar relevante providers in uw omgeving. '
            'Providers kunnen reageren met aanbiedingen, vragen of bevestigingen.\n\n'
            '5.3 Het indienen van een lead creëert geen bindend contract. Een contract komt '
            'alleen tot stand wanneer u en de provider uitdrukkelijk instemmen met de '
            'voorwaarden van de dienst.\n\n'
            '5.4 U mag geen verzoeken indienen voor diensten die illegaal, gevaarlijk zijn of '
            'deze Voorwaarden schenden.'
        ),
        "no": (
            '5.1 Som kunde kan du sende inn en tjenesteforespørsel ("lead") som beskriver '
            'tjenesten du trenger, din plassering, budsjettforventninger og foretrukket '
            'tidspunkt.\n\n'
            '5.2 Nevumo videresender forespørselen din til relevante leverandører i ditt '
            'område. Leverandører kan svare med tilbud, spørsmål eller bekreftelser.\n\n'
            '5.3 Å sende inn en lead oppretter ikke en bindende kontrakt. En kontrakt dannes '
            'bare når du og leverandøren uttrykkelig er enige om vilkårene for tjenesten.\n\n'
            '5.4 Du må ikke sende inn forespørsler om tjenester som er ulovlige, farlige '
            'eller som bryter disse Vilkårene.'
        ),
        "pt": (
            '5.1 Como cliente, você pode enviar uma solicitação de serviço ("lead") '
            'descrevendo o serviço de que precisa, sua localização, expectativas de '
            'orçamento e horário preferido.\n\n'
            '5.2 O Nevumo encaminha sua solicitação aos prestadores relevantes em sua área. '
            'Os prestadores podem responder com ofertas, perguntas ou confirmações.\n\n'
            '5.3 Enviar um lead não cria um contrato vinculante. Um contrato é formado apenas '
            'quando você e o prestador concordam expressamente com os termos do serviço.\n\n'
            '5.4 Você não deve enviar solicitações para serviços que sejam ilegais, perigosos '
            'ou que violem estes Termos.'
        ),
        "pt-PT": (
            '5.1 Como cliente, pode submeter um pedido de serviço ("lead") descrevendo o '
            'serviço de que necessita, a sua localização, expectativas de orçamento e '
            'horário preferido.\n\n'
            '5.2 O Nevumo encaminha o seu pedido para os prestadores relevantes na sua área. '
            'Os prestadores podem responder com propostas, perguntas ou confirmações.\n\n'
            '5.3 A submissão de um lead não cria um contrato vinculativo. Um contrato forma-se '
            'apenas quando você e o prestador acordam expressamente nos termos do serviço.\n\n'
            '5.4 Não deve submeter pedidos para serviços que sejam ilegais, perigosos ou que '
            'violem estes Termos.'
        ),
        "ro": (
            '5.1 Ca și client, puteți trimite o cerere de serviciu ("lead") descriind '
            'serviciul de care aveți nevoie, locația dvs., așteptările bugetare și '
            'calendarul preferat.\n\n'
            '5.2 Nevumo transmite cererea dvs. prestatorilor relevanți din zona dvs. '
            'Prestatorii pot răspunde cu oferte, întrebări sau confirmări.\n\n'
            '5.3 Trimiterea unui lead nu creează un contract obligatoriu. Un contract se '
            'formează numai când dvs. și prestatorul conveniți în mod expres asupra '
            'condițiilor serviciului.\n\n'
            '5.4 Nu trebuie să trimiteți cereri pentru servicii care sunt ilegale, '
            'periculoase sau care încalcă acești Termeni.'
        ),
        "ru": (
            '5.1 Как клиент вы можете отправить запрос на услугу ("лид"), описывающий '
            'необходимую услугу, ваше местоположение, бюджетные ожидания и предпочтительные '
            'сроки.\n\n'
            '5.2 Nevumo пересылает ваш запрос подходящим исполнителям в вашем районе. '
            'Исполнители могут ответить предложениями, вопросами или подтверждениями.\n\n'
            '5.3 Отправка лида не создаёт обязательного договора. Договор заключается только '
            'тогда, когда вы и исполнитель явно договариваются об условиях услуги.\n\n'
            '5.4 Вы не должны отправлять запросы на услуги, которые являются незаконными, '
            'опасными или нарушают настоящие условия.'
        ),
        "sk": (
            '5.1 Ako klient môžete podať žiadosť o službu ("lead"), v ktorej opíšete '
            'požadovanú službu, svoju polohu, rozpočtové očakávania a preferovaný termín.\n\n'
            '5.2 Nevumo prepošle vašu žiadosť relevantným poskytovateľom vo vašej oblasti. '
            'Poskytovatelia môžu reagovať ponukami, otázkami alebo potvrdeniami.\n\n'
            '5.3 Odoslanie leadu nevytvára záväznú zmluvu. Zmluva vzniká iba vtedy, keď vy '
            'a poskytovateľ sa výslovne dohodnú na podmienkach služby.\n\n'
            '5.4 Nesmíte podávať žiadosti o služby, ktoré sú nezákonné, nebezpečné alebo '
            'porušujú tieto podmienky.'
        ),
        "sl": (
            '5.1 Kot stranka lahko oddate zahtevek za storitev ("lead"), ki opisuje storitev, '
            'ki jo potrebujete, vašo lokacijo, proračunska pričakovanja in zaželeni čas.\n\n'
            '5.2 Nevumo posreduje vaš zahtevek ustreznim ponudnikom v vaši bližini. Ponudniki '
            'lahko odgovorijo s ponudbami, vprašanji ali potrditvami.\n\n'
            '5.3 Oddaja leada ne ustvari zavezujoče pogodbe. Pogodba nastane le takrat, ko '
            'vi in ponudnik izrecno dogovorita pogoje storitve.\n\n'
            '5.4 Ne smete oddajati zahtevkov za storitve, ki so nezakonite, nevarne ali '
            'kršijo te pogoje.'
        ),
        "sq": (
            '5.1 Si klient, mund të dërgoni një kërkesë shërbimi ("lead") duke përshkruar '
            'shërbimin që nevojitni, vendndodhjen tuaj, pritshmëritë e buxhetit dhe '
            'kohën e preferuar.\n\n'
            '5.2 Nevumo i dërgon kërkesën tuaj ofruesve relevant në zonën tuaj. Ofruesit '
            'mund të përgjigjen me oferta, pyetje ose konfirmime.\n\n'
            '5.3 Dërgimi i një lead nuk krijon një kontratë detyruese. Kontrata formohet '
            'vetëm kur ju dhe ofruesi bien dakord shprehimisht për kushtet e shërbimit.\n\n'
            '5.4 Nuk duhet të dërgoni kërkesa për shërbime që janë të paligjshme, të '
            'rrezikshme ose që shkelin këto Terma.'
        ),
        "sr": (
            '5.1 Kao klijent možete poslati zahtev za uslugu ("lead") opisujući uslugu '
            'koja vam je potrebna, vašu lokaciju, budžetska očekivanja i željeno vreme.\n\n'
            '5.2 Nevumo prosleđuje vaš zahtev relevantnim pružaocima u vašoj oblasti. '
            'Pružaoci mogu da odgovore ponudama, pitanjima ili potvrđivanjima.\n\n'
            '5.3 Slanje leada ne kreira obavezujući ugovor. Ugovor nastaje samo kada vi i '
            'pružalac izričito dogovorite uslove usluge.\n\n'
            '5.4 Ne smete slati zahteve za usluge koje su nezakonite, opasne ili krše '
            'ove Uslove.'
        ),
        "sv": (
            '5.1 Som kund kan du skicka in en tjänsteförfrågan ("lead") som beskriver den '
            'tjänst du behöver, din plats, budgetförväntningar och önskat schema.\n\n'
            '5.2 Nevumo vidarebefordrar din förfrågan till relevanta leverantörer i ditt '
            'område. Leverantörer kan svara med erbjudanden, frågor eller bekräftelser.\n\n'
            '5.3 Att skicka in en lead skapar inte ett bindande avtal. Ett avtal ingås bara '
            'när du och leverantören uttryckligen kommer överens om villkoren för tjänsten.\n\n'
            '5.4 Du får inte skicka in förfrågningar om tjänster som är olagliga, farliga '
            'eller som bryter mot dessa Villkor.'
        ),
        "tr": (
            '5.1 Müşteri olarak, ihtiyaç duyduğunuz hizmeti, konumunuzu, bütçe beklentilerinizi '
            've tercih ettiğiniz zamanlamayı açıklayan bir hizmet talebi ("lead") '
            'gönderebilirsiniz.\n\n'
            '5.2 Nevumo talebinizi bölgenizdeki ilgili sağlayıcılara iletir. Sağlayıcılar '
            'teklifler, sorular veya onaylarla yanıt verebilir.\n\n'
            '5.3 Lead göndermek bağlayıcı bir sözleşme oluşturmaz. Sözleşme yalnızca siz ve '
            'sağlayıcı hizmetin koşulları üzerinde açıkça anlaştığınızda oluşur.\n\n'
            '5.4 Yasadışı, tehlikeli olan veya bu Koşulları ihlal eden hizmetler için talepte '
            'bulunmamalısınız.'
        ),
        "uk": (
            '5.1 Як клієнт ви можете надіслати запит на послугу ("лід"), описавши необхідну '
            'послугу, вашу локацію, бюджетні очікування та бажані строки.\n\n'
            '5.2 Nevumo пересилає ваш запит відповідним виконавцям у вашому районі. '
            'Виконавці можуть відповісти пропозиціями, питаннями або підтвердженнями.\n\n'
            '5.3 Надсилання ліду не створює обов\'язкового договору. Договір укладається '
            'лише тоді, коли ви та виконавець прямо домовляються про умови послуги.\n\n'
            '5.4 Ви не повинні надсилати запити на послуги, які є незаконними, небезпечними '
            'або порушують ці Умови.'
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
        print(f"✅ seed_terms_p5_bodies: {count} rows upserted ({NAMESPACE}, art5_body × 34 langs)")

    engine.dispose()


if __name__ == "__main__":
    seed()
