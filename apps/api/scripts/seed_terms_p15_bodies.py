"""
seed_terms_p15_bodies.py  —  Nevumo | namespace: terms
Key: art15_body (34 езика)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_terms_p15_bodies
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
    "art15_body": {
        "en": (
            '15.1 If any provision of these Terms is found to be invalid or '
            'unenforceable, the remaining provisions will continue in full force.\n\n'
            '15.2 Nevumo\'s failure to enforce any right or provision does not '
            'constitute a waiver of that right or provision.\n\n'
            '15.3 These Terms constitute the entire agreement between you and '
            'Nevumo regarding the use of the platform and supersede any prior '
            'agreements on the same subject.\n\n'
            '15.4 You may not transfer your rights or obligations under these Terms '
            'to any third party without prior written consent from Nevumo. Nevumo '
            'may transfer its rights and obligations to a successor entity, provided '
            'that your rights are not diminished.'
        ),
        "pl": (
            '15.1 Jeżeli którekolwiek z postanowień niniejszego Regulaminu okaże '
            'się nieważne lub niewykonalne, pozostałe postanowienia pozostają '
            'w mocy w pełnym zakresie.\n\n'
            '15.2 Nieskorzystanie przez Nevumo z jakiegokolwiek uprawnienia lub '
            'postanowienia Regulaminu nie stanowi zrzeczenia się tego uprawnienia '
            'ani postanowienia.\n\n'
            '15.3 Niniejszy Regulamin stanowi całość umowy pomiędzy Klientem '
            'a Nevumo dotyczącej korzystania z serwisu i zastępuje wszelkie '
            'wcześniejsze umowy w tym zakresie.\n\n'
            '15.4 Klient nie może przenosić swoich praw ani obowiązków wynikających '
            'z niniejszego Regulaminu na osoby trzecie bez uprzedniej pisemnej '
            'zgody Nevumo. Nevumo może przenosić swoje prawa i obowiązki na '
            'podmiot następczy, pod warunkiem że prawa Klienta nie zostaną '
            'w związku z tym ograniczone.'
        ),
        "bg": (
            '15.1 Ако някоя разпоредба на настоящите ОУ бъде обявена за '
            'недействителна или неприложима, останалите разпоредби запазват '
            'пълната си сила и действие.\n\n'
            '15.2 Неупражняването от страна на Nevumo на дадено право или '
            'разпоредба не представлява отказ от него.\n\n'
            '15.3 Настоящите ОУ представляват цялостното споразумение между '
            'Клиента и Nevumo относно ползването на платформата и заменят '
            'всички предходни споразумения по същия предмет.\n\n'
            '15.4 Клиентът не може да прехвърля права или задължения по '
            'настоящите ОУ на трети лица без предварително писмено съгласие '
            'на Nevumo. Nevumo може да прехвърля правата и задълженията си '
            'на правоприемник, при условие че правата на Клиента не се '
            'накърняват.'
        ),
        "cs": (
            '15.1 Pokud bude jakékoli ustanovení těchto podmínek shledáno '
            'neplatným nebo nevymahatelným, ostatní ustanovení zůstávají v '
            'plné platnosti.\n\n'
            '15.2 Neudělení jakéhokoli práva nebo ustanovení ze strany Nevumo '
            'nepředstavuje vzdání se tohoto práva.\n\n'
            '15.3 Tyto podmínky tvoří úplnou dohodu mezi vámi a Nevumo ohledně '
            'používání platformy a nahrazují všechny předchozí dohody.\n\n'
            '15.4 Svá práva ani povinnosti z těchto podmínek nesmíte převádět '
            'na třetí strany bez předchozího písemného souhlasu Nevumo. Nevumo '
            'může převést svá práva na nástupnický subjekt za podmínky, '
            'že vaše práva nebudou zkrácena.'
        ),
        "da": (
            '15.1 Hvis en bestemmelse i disse vilkår anses for ugyldig eller '
            'uigennemtvingelig, forbliver de resterende bestemmelser i fuld kraft.\n\n'
            '15.2 Nevumos undladelse af at håndhæve en rettighed udgør ikke '
            'et afkald på den pågældende rettighed.\n\n'
            '15.3 Disse vilkår udgør den fulde aftale mellem dig og Nevumo '
            'vedrørende brugen af platformen og erstatter eventuelle tidligere aftaler.\n\n'
            '15.4 Du må ikke overdrage dine rettigheder eller forpligtelser til '
            'tredjepart uden forudgående skriftligt samtykke fra Nevumo. Nevumo '
            'kan overdrage sine rettigheder til en successorenhed forudsat, '
            'at dine rettigheder ikke formindskes.'
        ),
        "de": (
            '15.1 Sollte eine Bestimmung dieser Bedingungen für ungültig oder '
            'nicht durchsetzbar befunden werden, bleiben die übrigen Bestimmungen '
            'in vollem Umfang in Kraft.\n\n'
            '15.2 Die Nichtdurchsetzung eines Rechts oder einer Bestimmung durch '
            'Nevumo stellt keinen Verzicht auf dieses Recht dar.\n\n'
            '15.3 Diese Bedingungen stellen die gesamte Vereinbarung zwischen '
            'Ihnen und Nevumo bezüglich der Nutzung der Plattform dar und ersetzen '
            'alle früheren Vereinbarungen zum selben Gegenstand.\n\n'
            '15.4 Sie dürfen Ihre Rechte oder Pflichten aus diesen Bedingungen '
            'nicht ohne vorherige schriftliche Zustimmung von Nevumo auf Dritte '
            'übertragen. Nevumo darf seine Rechte auf ein Nachfolgeunternehmen '
            'übertragen, sofern Ihre Rechte nicht beeinträchtigt werden.'
        ),
        "el": (
            '15.1 Εάν οποιαδήποτε διάταξη των παρόντων Όρων κριθεί άκυρη ή '
            'μη εκτελεστή, οι υπόλοιπες διατάξεις παραμένουν σε πλήρη ισχύ.\n\n'
            '15.2 Η μη επιβολή οποιουδήποτε δικαιώματος από το Nevumo δεν '
            'συνιστά παραίτηση από το δικαίωμα αυτό.\n\n'
            '15.3 Οι παρόντες Όροι αποτελούν τη συνολική συμφωνία μεταξύ εσάς '
            'και του Nevumo σχετικά με τη χρήση της πλατφόρμας.\n\n'
            '15.4 Δεν επιτρέπεται να μεταβιβάσετε τα δικαιώματα ή τις '
            'υποχρεώσεις σας σε τρίτους χωρίς προηγούμενη γραπτή συγκατάθεση '
            'του Nevumo. Το Nevumo μπορεί να μεταβιβάσει τα δικαιώματά του '
            'σε διάδοχο φορέα υπό τον όρο ότι τα δικαιώματά σας δεν μειώνονται.'
        ),
        "es": (
            '15.1 Si alguna disposición de estos Términos se considera inválida '
            'o inaplicable, las disposiciones restantes seguirán en plena vigencia.\n\n'
            '15.2 El hecho de que Nevumo no ejerza algún derecho no constituye '
            'una renuncia a dicho derecho.\n\n'
            '15.3 Estos Términos constituyen el acuerdo completo entre usted y '
            'Nevumo sobre el uso de la plataforma y reemplazan cualquier acuerdo '
            'previo sobre el mismo asunto.\n\n'
            '15.4 No puede transferir sus derechos u obligaciones a terceros sin '
            'el consentimiento previo y por escrito de Nevumo. Nevumo puede '
            'transferir sus derechos a una entidad sucesora siempre que sus '
            'derechos no se vean disminuidos.'
        ),
        "et": (
            '15.1 Kui mõni käesolevate tingimuste säte tunnistatakse kehtetuks '
            'või mittetäidetavaks, jäävad ülejäänud sätted täiel määral jõusse.\n\n'
            '15.2 Nevumo poolne õiguse mittetäitmine ei tähenda loobumist '
            'sellest õigusest.\n\n'
            '15.3 Need tingimused moodustavad tervikliku kokkuleppe teie ja '
            'Nevumo vahel platvormi kasutamise osas ning asendavad kõik '
            'varasemad kokkulepped samas küsimuses.\n\n'
            '15.4 Te ei tohi käesolevate tingimuste alusel oma õigusi ega '
            'kohustusi ilma Nevumo eelneva kirjaliku nõusolekuta kolmandatele '
            'isikutele üle anda. Nevumo võib oma õigused üle anda '
            'õigusjärglasele tingimusel, et teie õigused ei vähene.'
        ),
        "fi": (
            '15.1 Jos jokin näiden ehtojen määräys todetaan pätemättömäksi tai '
            'täytäntöönpanokelvottomaksi, muut määräykset pysyvät täydessä '
            'voimassa.\n\n'
            '15.2 Nevumon laiminlyönti jonkin oikeuden käyttämisessä ei '
            'merkitse luopumista kyseisestä oikeudesta.\n\n'
            '15.3 Nämä ehdot muodostavat täydellisen sopimuksen sinun ja '
            'Nevumon välillä alustan käytöstä ja korvaavat kaikki aiemmat '
            'sopimukset samasta aiheesta.\n\n'
            '15.4 Et voi siirtää oikeuksiasi tai velvollisuuksiasi kolmansille '
            'osapuolille ilman Nevumon etukäteistä kirjallista suostumusta. '
            'Nevumo voi siirtää oikeutensa seuraajalle edellyttäen, '
            'ettei oikeuksiasi vähennetä.'
        ),
        "fr": (
            '15.1 Si une disposition des présentes Conditions est jugée invalide '
            'ou inapplicable, les autres dispositions restent pleinement en vigueur.\n\n'
            '15.2 Le fait que Nevumo n\'applique pas un droit ou une disposition '
            'ne constitue pas une renonciation à ce droit.\n\n'
            '15.3 Les présentes Conditions constituent l\'intégralité de l\'accord '
            'entre vous et Nevumo concernant l\'utilisation de la plateforme et '
            'remplacent tout accord antérieur.\n\n'
            '15.4 Vous ne pouvez pas transférer vos droits ou obligations à des '
            'tiers sans le consentement écrit préalable de Nevumo. Nevumo peut '
            'transférer ses droits à une entité successeur à condition que vos '
            'droits ne soient pas diminués.'
        ),
        "ga": (
            '15.1 Má mheastar aon fhoráil de na Téarmaí seo a bheith neamhbhailí '
            'nó neamhinfheidhmithe, fanann na forálacha eile i bhfeidhm iomlán.\n\n'
            '15.2 Teip Nevumo aon cheart nó foráil a fhorfheidhmiú ní chiallaíonn '
            'sé sin tarscaoileadh an chirt sin.\n\n'
            '15.3 Ionann na Téarmaí seo agus an comhaontú iomlán idir tú féin '
            'agus Nevumo maidir le húsáid na hardáin agus cuireann siad ionad '
            'gach comhaontú roimhe sin.\n\n'
            '15.4 Ní féidir leat do chearta ná d\'oibleagáidí a aistriú chuig '
            'tríú páirtí gan toiliú scríofa roimh ré ó Nevumo. Féadfaidh Nevumo '
            'a chearta a aistriú chuig eintiteas comharba ar choinníoll nach '
            'gcuirtear do chearta ar lagú.'
        ),
        "hr": (
            '15.1 Ako se neka odredba ovih Uvjeta utvrdi nevažećom ili '
            'neprovedivom, preostale odredbe ostaju na snazi u potpunosti.\n\n'
            '15.2 Propust Nevumo da primijeni neko pravo ne predstavlja odricanje '
            'od tog prava.\n\n'
            '15.3 Ovi Uvjeti čine cjelokupan sporazum između vas i Nevumo '
            'o korištenju platforme i zamjenjuju sve prethodne sporazume.\n\n'
            '15.4 Ne možete prenositi svoja prava ni obveze na treće strane '
            'bez prethodnog pisanog pristanka Nevumo. Nevumo može prenijeti '
            'svoja prava na subjekt nasljednika pod uvjetom da vaša prava '
            'ne budu umanjena.'
        ),
        "hu": (
            '15.1 Ha jelen feltételek bármely rendelkezése érvénytelennek vagy '
            'végrehajthatatlannak bizonyul, a többi rendelkezés teljes hatályban '
            'marad.\n\n'
            '15.2 Az, hogy a Nevumo nem érvényesít valamely jogot, nem jelenti '
            'az adott jogról való lemondást.\n\n'
            '15.3 Jelen feltételek teljes megállapodást alkotnak Ön és a Nevumo '
            'között a platform használatával kapcsolatban, és felváltják az '
            'ugyanerre vonatkozó korábbi megállapodásokat.\n\n'
            '15.4 Jogait vagy kötelezettségeit nem ruházhatja át harmadik félre '
            'a Nevumo előzetes írásbeli hozzájárulása nélkül. A Nevumo '
            'átruházhatja jogait egy jogutód szervezetre, feltéve, hogy '
            'az Ön jogai nem csökkennek.'
        ),
        "is": (
            '15.1 Ef einhver ákvæði þessara skilmála eru talin ógild eða '
            'óframkvæmanleg, gilda önnur ákvæði að fullu.\n\n'
            '15.2 Þótt Nevumo beiti ekki réttindum sínum felur það ekki í sér '
            'að þeim sé vikið til hliðar.\n\n'
            '15.3 Þessir skilmálar mynda heildarsamning milli þín og Nevumo '
            'um notkun vettvangsins og koma í stað fyrri samninga.\n\n'
            '15.4 Þú getur ekki framselt réttindi þín eða skyldur til þriðja '
            'aðila án skriflegs samþykkis Nevumo. Nevumo getur framselt '
            'réttindi sín til erfingjaeiningar að því tilskildu að réttindi '
            'þín skerðist ekki.'
        ),
        "it": (
            '15.1 Se una disposizione dei presenti Termini è ritenuta non valida '
            'o inapplicabile, le restanti disposizioni rimangono in piena vigenza.\n\n'
            '15.2 Il mancato esercizio di un diritto da parte di Nevumo non '
            'costituisce rinuncia a tale diritto.\n\n'
            '15.3 I presenti Termini costituiscono l\'intero accordo tra te e '
            'Nevumo sull\'utilizzo della piattaforma e sostituiscono qualsiasi '
            'accordo precedente sulla stessa materia.\n\n'
            '15.4 Non puoi trasferire i tuoi diritti o obblighi a terzi senza '
            'il previo consenso scritto di Nevumo. Nevumo può trasferire i propri '
            'diritti a un\'entità successore a condizione che i tuoi diritti '
            'non vengano ridotti.'
        ),
        "lb": (
            '15.1 Wann eng Bestëmmung vun dësen Bedéngungen fir ongëlteg oder '
            'net durchsetzbau erkläert gëtt, bleiwe déi aner Bestëmmungen a '
            'voller Kraaft.\n\n'
            '15.2 D\'Nichtdurchsetzung vun engem Recht duerch Nevumo stellt '
            'keen Verzicht op dëst Recht duer.\n\n'
            '15.3 Dës Bedéngungen bilden d\'Gesamtvereenbarung tëschent Iech '
            'a Nevumo iwwer d\'Benotze vun der Plattform an ersetzen all '
            'fréier Abkommen.\n\n'
            '15.4 Dir kënnt Är Rechter oder Pflichten ouni viregt schriftlecht '
            'Averstäendnis vu Nevumo net op Drëttpartei iwwerdroe. Nevumo kann '
            'seng Rechter op eng Nofolgorganisatioun iwwerdroe, virausgesat '
            'datt Är Rechter net geschmälert ginn.'
        ),
        "lt": (
            '15.1 Jei kuri nors šių sąlygų nuostata pripažįstama negaliojančia '
            'ar nevykdytina, likusios nuostatos išlieka visapusiškai galiojančios.\n\n'
            '15.2 Nevumo susilaikymas nuo teisės įgyvendinimo nereiškia '
            'atsisakymo nuo tos teisės.\n\n'
            '15.3 Šios sąlygos sudaro visapusišką susitarimą tarp jūsų ir '
            'Nevumo dėl platformos naudojimo ir pakeičia visus ankstesnius '
            'susitarimus tuo pačiu klausimu.\n\n'
            '15.4 Negalite perduoti savo teisių ar pareigų trečiosioms šalims '
            'be išankstinio Nevumo rašytinio sutikimo. Nevumo gali perduoti '
            'savo teises teisių perėmėjui su sąlyga, kad jūsų teisės '
            'nebus sumažintos.'
        ),
        "lv": (
            '15.1 Ja kāds šo noteikumu pants tiek atzīts par spēkā neesošu vai '
            'neizpildāmu, pārējie panti paliek pilnībā spēkā.\n\n'
            '15.2 Nevumo neizmantotas tiesības nenozīmē atteikšanos no tām.\n\n'
            '15.3 Šie noteikumi veido pilnīgu vienošanos starp jums un Nevumo '
            'par platformas izmantošanu un aizstāj visas iepriekšējās vienošanās '
            'par to pašu.\n\n'
            '15.4 Jūs nevarat nodot savas tiesības vai pienākumus trešajām pusēm '
            'bez Nevumo iepriekšējas rakstiskas piekrišanas. Nevumo var nodot '
            'savas tiesības pēctecim ar noteikumu, ka jūsu tiesības '
            'netiek mazinātas.'
        ),
        "mk": (
            '15.1 Ако некоја одредба на овие Услови се прогласи за неважечка '
            'или неизвршлива, останатите одредби остануваат во полна сила.\n\n'
            '15.2 Непримената на некое право од страна на Nevumo не претставува '
            'одрекување од тоа право.\n\n'
            '15.3 Овие Услови претставуваат целосен договор меѓу вас и Nevumo '
            'за користењето на платформата и ги заменуваат сите претходни '
            'договори за истата тема.\n\n'
            '15.4 Не можете да ги пренесувате вашите права или обврски на '
            'трети лица без претходна писмена согласност на Nevumo. Nevumo '
            'може да ги пренесе своите права на правен следбеник под услов '
            'вашите права да не се намалат.'
        ),
        "mt": (
            '15.1 Jekk kwalunkwe dispożizzjoni ta\' dawn it-Termini titqies '
            'invalida jew mhux infurzabbli, id-dispożizzjonijiet li jifdal '
            'jibqgħu fis-seħħ bis-sħiħ.\n\n'
            '15.2 Nuqqas ta\' Nevumo li jinforza dritt ma jikkostitwixxix '
            'rinunzja għal dak id-dritt.\n\n'
            '15.3 Dawn it-Termini jikkostitwixxu l-ftehim sħiħ bejnek u '
            'Nevumo dwar l-użu tal-pjattaforma u jissostitwixxu kwalunkwe '
            'ftehim preċedenti.\n\n'
            '15.4 Ma tistax tittrasferixxi d-drittijiet jew l-obbligi tiegħek '
            'lil partijiet terzi mingħajr il-kunsens bil-miktub minn qabel '
            'ta\' Nevumo. Nevumo jista\' jittrasferixxi d-drittijiet tiegħu '
            'lil entità suċċessuri sakemm id-drittijiet tiegħek ma jitnaqqsux.'
        ),
        "nl": (
            '15.1 Als een bepaling van deze Voorwaarden ongeldig of '
            'niet-afdwingbaar wordt bevonden, blijven de overige bepalingen '
            'volledig van kracht.\n\n'
            '15.2 Het niet handhaven van een recht door Nevumo vormt geen '
            'afstand van dat recht.\n\n'
            '15.3 Deze Voorwaarden vormen de volledige overeenkomst tussen u '
            'en Nevumo met betrekking tot het gebruik van het platform en '
            'vervangen alle eerdere overeenkomsten over hetzelfde onderwerp.\n\n'
            '15.4 U kunt uw rechten of verplichtingen niet overdragen aan '
            'derden zonder voorafgaande schriftelijke toestemming van Nevumo. '
            'Nevumo kan zijn rechten overdragen aan een rechtsopvolger mits '
            'uw rechten niet worden verminderd.'
        ),
        "no": (
            '15.1 Hvis noen bestemmelse i disse Vilkårene anses ugyldig eller '
            'ikke-håndhevbar, forblir de resterende bestemmelsene i full kraft.\n\n'
            '15.2 Nevumos unnlatelse av å håndheve en rettighet utgjør ikke '
            'et avkall på den rettigheten.\n\n'
            '15.3 Disse Vilkårene utgjør den fullstendige avtalen mellom deg '
            'og Nevumo om bruk av plattformen og erstatter alle tidligere '
            'avtaler om samme emne.\n\n'
            '15.4 Du kan ikke overdra dine rettigheter eller forpliktelser til '
            'tredjepart uten forutgående skriftlig samtykke fra Nevumo. Nevumo '
            'kan overdra sine rettigheter til en etterfølgerenhet forutsatt '
            'at dine rettigheter ikke reduseres.'
        ),
        "pt": (
            '15.1 Se alguma disposição destes Termos for considerada inválida ou '
            'inexequível, as demais disposições permanecerão em plena vigência.\n\n'
            '15.2 A não aplicação de qualquer direito pelo Nevumo não constitui '
            'renúncia a esse direito.\n\n'
            '15.3 Estes Termos constituem o acordo integral entre você e o '
            'Nevumo sobre o uso da plataforma e substituem quaisquer acordos '
            'anteriores sobre o mesmo assunto.\n\n'
            '15.4 Você não pode transferir seus direitos ou obrigações a '
            'terceiros sem o consentimento prévio por escrito do Nevumo. O '
            'Nevumo pode transferir seus direitos a uma entidade sucessora, '
            'desde que seus direitos não sejam reduzidos.'
        ),
        "pt-PT": (
            '15.1 Se alguma disposição destes Termos for considerada inválida '
            'ou inexequível, as restantes disposições permanecerão em plena '
            'vigência.\n\n'
            '15.2 A não aplicação de qualquer direito pelo Nevumo não constitui '
            'renúncia a esse direito.\n\n'
            '15.3 Estes Termos constituem o acordo integral entre si e o Nevumo '
            'sobre a utilização da plataforma e substituem quaisquer acordos '
            'anteriores sobre o mesmo assunto.\n\n'
            '15.4 Não pode transferir os seus direitos ou obrigações a terceiros '
            'sem o consentimento prévio por escrito do Nevumo. O Nevumo pode '
            'transferir os seus direitos para uma entidade sucessora, desde que '
            'os seus direitos não sejam reduzidos.'
        ),
        "ro": (
            '15.1 Dacă o dispoziție a acestor Termeni este considerată invalidă '
            'sau neaplicabilă, celelalte dispoziții rămân în deplină vigoare.\n\n'
            '15.2 Neaplicarea unui drept de către Nevumo nu constituie o '
            'renunțare la acel drept.\n\n'
            '15.3 Acești Termeni constituie acordul integral dintre dvs. și '
            'Nevumo privind utilizarea platformei și înlocuiesc orice acorduri '
            'anterioare pe același subiect.\n\n'
            '15.4 Nu puteți transfera drepturile sau obligațiile dvs. unor '
            'terți fără consimțământul prealabil scris al Nevumo. Nevumo poate '
            'transfera drepturile sale unui succesor cu condiția ca drepturile '
            'dvs. să nu fie diminuate.'
        ),
        "ru": (
            '15.1 Если какое-либо положение настоящих условий признано '
            'недействительным или не подлежащим исполнению, остальные '
            'положения сохраняют полную силу.\n\n'
            '15.2 Неприменение Nevumo какого-либо права не означает '
            'отказа от него.\n\n'
            '15.3 Настоящие условия составляют полное соглашение между '
            'вами и Nevumo в отношении использования платформы и заменяют '
            'все предыдущие соглашения по тому же предмету.\n\n'
            '15.4 Вы не можете передавать свои права или обязательства '
            'третьим лицам без предварительного письменного согласия Nevumo. '
            'Nevumo вправе передать свои права правопреемнику при условии, '
            'что ваши права не ущемляются.'
        ),
        "sk": (
            '15.1 Ak sa niektoré ustanovenie týchto podmienok ukáže ako neplatné '
            'alebo nevymáhateľné, ostatné ustanovenia zostávajú v plnej platnosti.\n\n'
            '15.2 Neuplatnenie práva zo strany Nevumo nepredstavuje vzdanie sa '
            'tohto práva.\n\n'
            '15.3 Tieto podmienky tvoria úplnú dohodu medzi vami a Nevumo '
            'o používaní platformy a nahrádzajú všetky predchádzajúce dohody '
            'v tej istej veci.\n\n'
            '15.4 Svoje práva ani povinnosti nemôžete previesť na tretie strany '
            'bez predchádzajúceho písomného súhlasu Nevumo. Nevumo môže previesť '
            'svoje práva na nástupnický subjekt za podmienky, '
            'že vaše práva nebudú znížené.'
        ),
        "sl": (
            '15.1 Če je katera koli določba teh pogojev neveljavna ali '
            'neizterljiva, preostale določbe ostanejo v polni veljavi.\n\n'
            '15.2 Nevumo neuveljavljanje pravice ne pomeni odpovedi tej pravici.\n\n'
            '15.3 Ti pogoji predstavljajo celoten dogovor med vami in Nevumo '
            'glede uporabe platforme in nadomeščajo vse prejšnje dogovore '
            'o isti temi.\n\n'
            '15.4 Svojih pravic ali obveznosti ne smete prenesti na tretje '
            'strani brez predhodnega pisnega soglasja Nevumo. Nevumo lahko '
            'prenese svoje pravice na pravnega naslednika pod pogojem, '
            'da vaše pravice niso zmanjšane.'
        ),
        "sq": (
            '15.1 Nëse ndonjë dispozitë e këtyre Termave gjendet e pavlefshme '
            'ose e pazbatueshme, dispozitat e mbetura vazhdojnë me fuqi të plotë.\n\n'
            '15.2 Moszbatimi i ndonjë të drejte nga Nevumo nuk përbën heqje '
            'dorë nga ajo e drejtë.\n\n'
            '15.3 Këto Terma përbëjnë marrëveshjen e plotë midis jush dhe '
            'Nevumo për përdorimin e platformës dhe zëvendësojnë çdo marrëveshje '
            'të mëparshme mbi të njëjtën çështje.\n\n'
            '15.4 Nuk mund të transferoni të drejtat ose detyrimet tuaja tek '
            'palë të treta pa miratimin paraprak me shkrim të Nevumo. Nevumo '
            'mund të transferojë të drejtat e tij tek një entitet pasues me '
            'kusht që të drejtat tuaja të mos zvogëlohen.'
        ),
        "sr": (
            '15.1 Ako se neka odredba ovih Uslova utvrdi nevažećom ili '
            'nesprovodivom, preostale odredbe ostaju na snazi u celosti.\n\n'
            '15.2 Propust Nevumo da primeni neko pravo ne predstavlja '
            'odricanje od tog prava.\n\n'
            '15.3 Ovi Uslovi čine ceo sporazum između vas i Nevumo o '
            'korišćenju platforme i zamenjuju sve prethodne sporazume '
            'o istoj temi.\n\n'
            '15.4 Ne možete prenositi svoja prava niti obaveze na treća lica '
            'bez prethodnog pisanog pristanka Nevumo. Nevumo može preneti '
            'svoja prava na pravnog sledbenika pod uslovom da vaša prava '
            'ne budu umanjena.'
        ),
        "sv": (
            '15.1 Om någon bestämmelse i dessa Villkor befinns ogiltig eller '
            'inte verkställbar, förblir de återstående bestämmelserna i full '
            'kraft.\n\n'
            '15.2 Nevumos underlåtenhet att tillämpa en rättighet utgör inte '
            'ett avstående från den rättigheten.\n\n'
            '15.3 Dessa Villkor utgör det fullständiga avtalet mellan dig och '
            'Nevumo avseende användningen av plattformen och ersätter alla '
            'tidigare avtal om samma ämne.\n\n'
            '15.4 Du får inte överlåta dina rättigheter eller skyldigheter till '
            'tredje part utan Nevumos föregående skriftliga samtycke. Nevumo '
            'får överlåta sina rättigheter till en efterträdare förutsatt att '
            'dina rättigheter inte minskas.'
        ),
        "tr": (
            '15.1 Bu Koşulların herhangi bir hükmünün geçersiz veya '
            'uygulanamaz olduğu tespit edilirse, kalan hükümler tam olarak '
            'yürürlükte kalmaya devam eder.\n\n'
            '15.2 Nevumo\'nun herhangi bir hakkı kullanmaması, o haktan '
            'feragat anlamına gelmez.\n\n'
            '15.3 Bu Koşullar, platformun kullanımına ilişkin sizinle Nevumo '
            'arasındaki tam anlaşmayı oluşturur ve aynı konudaki önceki '
            'tüm anlaşmaların yerini alır.\n\n'
            '15.4 Haklarınızı veya yükümlülüklerinizi Nevumo\'nun önceden '
            'yazılı onayı olmaksızın üçüncü taraflara devredemezsiniz. '
            'Nevumo, haklarınızın azaltılmaması koşuluyla haklarını bir '
            'halef kuruluşa devredebilir.'
        ),
        "uk": (
            '15.1 Якщо будь-яке положення цих Умов визнано недійсним або '
            'таким, що не підлягає виконанню, решта положень залишаються '
            'в повній силі.\n\n'
            '15.2 Незастосування Nevumo будь-якого права не означає '
            'відмови від нього.\n\n'
            '15.3 Ці Умови є повною угодою між вами та Nevumo щодо '
            'використання платформи і замінюють усі попередні угоди '
            'з цього ж питання.\n\n'
            '15.4 Ви не можете передавати свої права або обов\'язки '
            'третім особам без попередньої письмової згоди Nevumo. '
            'Nevumo може передати свої права правонаступнику за умови, '
            'що ваші права не зменшуватимуться.'
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
        print(f"✅ seed_terms_p15_bodies: {count} rows upserted ({NAMESPACE}, art15_body × 34 langs)")

    engine.dispose()


if __name__ == "__main__":
    seed()
