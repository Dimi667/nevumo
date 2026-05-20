#!/usr/bin/env python3
"""
Seed contact DSA translations - Part 2.
Namespace: contact_dsa
Keys: 9 | Languages: 34
Run: docker exec nevumo-api python -m apps.api.scripts.seed_contact_dsa_p2
"""

import os

from sqlalchemy import create_engine, text

NAMESPACE = "contact_dsa"

# Language dictionaries with full keys (including namespace)
TRANSLATIONS_BY_LANG = {
    "bg": {
        "contact_dsa.s3_title": "Как да подадете сигнал за незаконно съдържание",
        "contact_dsa.s3_what_to_include_title": "Уведомлението Ви трябва да съдържа:",
        "contact_dsa.s4_title": "Какво се случва след подаване на сигнал",
        "contact_dsa.s5_title": "Поддържани езици",
        "contact_dsa.back_to_home": "Начало",
        "contact_dsa.s3_body": "Ако смятате, че съдържание в Nevumo е незаконно съгласно правото на ЕС или националното право, изпратете уведомление на legal@nevumo.com. За да можем да обработим сигнала Ви ефективно, моля включете следната информация:",
        "contact_dsa.s3_what_to_include_body": "1. Описание на съдържанието, което смятате за незаконно, и точното му местоположение в платформата (URL адрес или описание).\n2. Правното основание, поради което смятате, че съдържанието е незаконно.\n3. Вашето име и имейл адрес (с изключение на сигнали, свързани с материали за сексуално насилие над деца).\n4. Декларация, потвърждаваща, че информацията в уведомлението Ви е точна и пълна според Вашите знания.",
        "contact_dsa.s4_body": "При получаване на Вашето уведомление ние ще:\n• Изпратим автоматично потвърждение за получаване незабавно.\n• Разгледаме сигнала Ви своевременно, старателно и безпристрастно.\n• Предприемем действие в срок до 72 часа при спешни случаи (напр. съдържание, свързано с насилие, безопасност на деца или непосредствена заплаха).\n• Предприемем действие в срок до 7 работни дни при стандартни сигнали.\n• Уведомим Ви за нашето решение и основанията за него.\n• Информираме Ви за правото Ви да обжалвате решението ни.",
        "contact_dsa.s5_body": "Nevumo приема уведомления по DSA и комуникации от власти на следните езици: английски, български, полски. Когато е възможно, ще отговаряме на езика на Вашата комуникация.",
    },
    "cs": {
        "contact_dsa.s3_title": "Jak nahlásit nezákonný obsah",
        "contact_dsa.s3_what_to_include_title": "Vaše oznámení by mělo obsahovat:",
        "contact_dsa.s4_title": "Co se stane po nahlášení",
        "contact_dsa.s5_title": "Podporované jazyky",
        "contact_dsa.back_to_home": "Zpět na úvod",
        "contact_dsa.s3_body": "Pokud se domníváte, že obsah na platformě Nevumo je podle práva EU nebo vnitrostátního práva nezákonný, zašlete prosím oznámení na adresu legal@nevumo.com. Abychom mohli vaše nahlášení efektivně zpracovat, uveďte prosím následující informace:",
        "contact_dsa.s3_what_to_include_body": "1. Popis obsahu, který považujete za nezákonný, a jeho přesné umístění na platformě (URL nebo popis).\n2. Právní důvod, proč se domníváte, že je obsah nezákonný.\n3. Vaše jméno a e-mailovou adresu (s výjimkou hlášení týkajících se materiálů pohlavního zneužívání dětí).\n4. Prohlášení potvrzující, že informace ve vašem oznámení jsou podle vašeho nejlepšího vědomí přesné a úplné.",
        "contact_dsa.s4_body": "Po obdržení vašeho oznámení:\n• Okamžitě zašleme automatické potvrzení o přijetí.\n• Vaše nahlášení včas, pečlivě a nestranně přezkoumáme.\n• V naléhavých případech zakročíme do 72 hodin (např. obsah zahrnující násilí, bezpečnost dětí nebo bezprostřední hrozbu).\n• U standardních hlášení zakročíme do 7 pracovních dnů.\n• Budeme vás informovat o našem rozhodnutí a jeho důvodech.\n• Budeme vás informovat o vašem právu odvolat se proti našemu rozhodnutí.",
        "contact_dsa.s5_body": "Nevumo přijímá oznámení DSA a komunikaci od úřadů v následujících jazycích: angličtina, bulharština, polština. Pokud to bude možné, odpovíme v jazyce vaší komunikace.",
    },
    "da": {
        "contact_dsa.s3_title": "Sådan anmelder du ulovligt indhold",
        "contact_dsa.s3_what_to_include_title": "Din anmeldelse bør indeholde:",
        "contact_dsa.s4_title": "Hvad sker der efter din anmeldelse",
        "contact_dsa.s5_title": "Understøttede sprog",
        "contact_dsa.back_to_home": "Tilbage til forsiden",
        "contact_dsa.s3_body": "Hvis du mener, at indhold på Nevumo er ulovligt i henhold til EU-lovgivning eller national lovgivning, bedes du sende en meddelelse til legal@nevumo.com. For at vi effektivt kan behandle din anmeldelse, bedes du inkludere følgende oplysninger:",
        "contact_dsa.s3_what_to_include_body": "1. En beskrivelse af det indhold, du mener er ulovligt, og dets nøjagtige placering på platformen (URL eller beskrivelse).\n2. Den juridiske årsag til, at du mener, at indholdet er ulovligt.\n3. Dit navn og din e-mailadresse (undtagen for rapporter, der involverer materiale om seksuelt misbrug af børn).\n4. En erklæring, der bekræfter, at oplysningerne i din meddelelse er nøjagtige og fuldstændige efter din bedste overbevisning.",
        "contact_dsa.s4_body": "Ved modtagelse af din meddelelse vil vi:\n• Sende en automatisk bekræftelse på modtagelsen med det samme.\n• Gennemgå din rapport rettidigt, omhyggeligt og ikke-vilkårligt.\n• Træffe foranstaltninger inden for 72 timer i hastende tilfælde (f.eks. indhold, der involverer vold, børns sikkerhed eller overhængende fare).\n• Træffe foranstaltninger inden for 7 arbejdsdage for standardrapporter.\n• Underrette dig om vores beslutning og årsagerne til den.\n• Informere dig om din ret til at appellere vores beslutning.",
        "contact_dsa.s5_body": "Nevumo accepterer DSA-meddelelser og myndighedskommunikation på følgende sprog: engelsk, bulgarsk, polsk. Vi vil svare på sproget i din kommunikation, hvor det er muligt.",
    },
    "de": {
        "contact_dsa.s3_title": "So melden Sie rechtswidrige Inhalte",
        "contact_dsa.s3_what_to_include_title": "Ihre Meldung sollte enthalten:",
        "contact_dsa.s4_title": "Was nach Ihrer Meldung passiert",
        "contact_dsa.s5_title": "Unterstützte Sprachen",
        "contact_dsa.back_to_home": "Zurück zur Startseite",
        "contact_dsa.s3_body": "Wenn Sie der Ansicht sind, dass Inhalte auf Nevumo nach EU- oder nationalem Recht rechtswidrig sind, senden Sie bitte eine Meldung an legal@nevumo.com. Damit wir Ihre Meldung effektiv bearbeiten können, fügen Sie bitte folgende Informationen bei:",
        "contact_dsa.s3_what_to_include_body": "1. Eine Beschreibung des Inhalts, den Sie für rechtswidrig halten, und seinen genauen Speicherort auf der Plattform (URL oder Beschreibung).\n2. Den rechtlichen Grund, warum Sie den Inhalt für rechtswidrig halten.\n3. Ihren Namen und Ihre E-Mail-Adresse (außer bei Meldungen über Material über sexuellen Missbrauch von Kindern).\n4. Eine Erklärung, die bestätigt, dass die Informationen in Ihrer Meldung nach bestem Wissen und Gewissen richtig und vollständig sind.",
        "contact_dsa.s4_body": "Nach Erhalt Ihrer Meldung werden wir:\n• Umgehend eine automatische Empfangsbestätigung senden.\n• Ihre Meldung zeitnah, sorgfältig und nicht willkürlich prüfen.\n• In dringenden Fällen (z. B. Inhalte, die Gewalt, die Sicherheit von Kindern oder eine drohende Gefahr betreffen) innerhalb von 72 Stunden Maßnahmen ergreifen.\n• Bei Standardmeldungen innerhalb von 7 Werktagen Maßnahmen ergreifen.\n• Sie über unsere Entscheidung und die Gründe dafür benachrichtigen.\n• Sie über Ihr Recht informieren, gegen unsere Entscheidung Berufung einzulegen.",
        "contact_dsa.s5_body": "Nevumo akzeptiert DSA-Meldungen und Behördenkommunikation in den folgenden Sprachen: Englisch, Bulgarisch, Polnisch. Wir werden nach Möglichkeit in der Sprache Ihrer Kommunikation antworten.",
    },
    "el": {
        "contact_dsa.s3_title": "Πώς να αναφέρετε παράνομο περιεχόμενο",
        "contact_dsa.s3_what_to_include_title": "Η ειδοποίησή σας πρέπει να περιλαμβάνει:",
        "contact_dsa.s4_title": "Τι γίνεται μετά την αναφορά",
        "contact_dsa.s5_title": "Υποστηριζόμενες γλώσσες",
        "contact_dsa.back_to_home": "Επιστροφή στην αρχική",
        "contact_dsa.s3_body": "Εάν πιστεύετε ότι το περιεχόμενο στο Nevumo είναι παράνομο βάσει της νομοθεσίας της ΕΕ ή της εθνικής νομοθεσίας, στείλτε μια ειδοποίηση στο legal@nevumo.com. Για να μπορέσουμε να επεξεργαστούμε αποτελεσματικά την αναφορά σας, συμπεριλάβετε τις ακόλουθες πληροφορίες:",
        "contact_dsa.s3_what_to_include_body": "1. Περιγραφή του περιεχομένου που θεωρείτε παράνομο και την ακριβή τοποθεσία του στην πλατφόρμα (URL ή περιγραφή).\n2. Τον νομικό λόγο για τον οποίο πιστεύετε ότι το περιεχόμενο είναι παράνομο.\n3. Το όνομα και τη διεύθυνση ηλεκτρονικού ταχυδρομείου σας (εκτός από αναφορές που αφορούν υλικό σεξουαλικής κακοποίησης παιδιών).\n4. Μια δήλωση που επιβεβαιώνει ότι οι πληροφορίες στην ειδοποίησή σας είναι ακριβείς και πλήρεις εξ όσων γνωρίζετε.",
        "contact_dsa.s4_body": "Μετά τη λήψη της ειδοποίησής σας, θα:\n• Στείλουμε αμέσως αυτόματη επιβεβαίωση παραλαβής.\n• Εξετάσουμε την αναφορά σας έγκαιρα, επιμελώς και χωρίς αυθαιρεσίες.\n• Λάβουμε μέτρα εντός 72 ωρών για επείγουσες περιπτώσεις (π.χ. περιεχόμενο που αφορά βία, ασφάλεια παιδιών ή επικείμενο κίνδυνο).\n• Λάβουμε μέτρα εντός 7 εργάσιμων ημερών για τυπικές αναφορές.\n• Σας ειδοποιήσουμε για την απόφασή μας και τους λόγους αυτής.\n• Σας ενημερώσουμε για το δικαίωμά σας να ασκήσετε έφεση κατά της απόφασής μας.",
        "contact_dsa.s5_body": "Το Nevumo δέχεται ειδοποιήσεις DSA και επικοινωνίες αρχών στις ακόλουθες γλώσσες: Αγγλικά, Βουλγαρικά, Πολωνικά. Θα απαντήσουμε στη γλώσσα επικοινωνίας σας όπου είναι δυνατόν.",
    },
    "en": {
        "contact_dsa.s3_title": "How to Report Illegal Content",
        "contact_dsa.s3_what_to_include_title": "Your notice should include:",
        "contact_dsa.s4_title": "What Happens After You Report",
        "contact_dsa.s5_title": "Supported Languages",
        "contact_dsa.back_to_home": "Back to Home",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_body": "1. A description of the content you believe to be illegal and its exact location on the platform (URL or description).\n2. The legal reason why you believe the content is illegal.\n3. Your name and email address (except for reports involving child sexual abuse material).\n4. A statement confirming that the information in your notice is accurate and complete to the best of your knowledge.",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
    },
    "es": {
        "contact_dsa.s3_title": "Cómo denunciar contenido ilegal",
        "contact_dsa.s3_what_to_include_title": "Su aviso debe incluir:",
        "contact_dsa.s4_title": "Qué sucede después de su denuncia",
        "contact_dsa.s5_title": "Idiomas admitidos",
        "contact_dsa.back_to_home": "Volver al inicio",
        "contact_dsa.s3_body": "Si cree que el contenido en Nevumo es ilegal según la legislación de la UE o nacional, envíe un aviso a legal@nevumo.com. Para permitirnos procesar su denuncia de manera efectiva, incluya la siguiente información:",
        "contact_dsa.s3_what_to_include_body": "1. Una descripción del contenido que considera ilegal y su ubicación exacta en la plataforma (URL o descripción).\n2. El motivo legal por el que cree que el contenido es ilegal.\n3. Su nombre y dirección de correo electrónico (excepto en denuncias que involucren material de abuso sexual infantil).\n4. Una declaración que confirme que la información en su aviso es precisa y completa según su leal saber y entender.",
        "contact_dsa.s4_body": "Una vez recibido su aviso, nosotros:\n• Enviaremos una confirmación automática de recepción de inmediato.\n• Revisaremos su denuncia de manera oportuna, diligente y no arbitraria.\n• Tomaremos medidas dentro de las 72 horas para casos urgentes (por ejemplo, contenido que implique violencia, seguridad infantil o daño inminente).\n• Tomaremos medidas dentro de los 7 días hábiles para denuncias estándar.\n• Le notificaremos nuestra decisión y los motivos de la misma.\n• Le informaremos de su derecho a apelar nuestra decisión.",
        "contact_dsa.s5_body": "Nevumo acepta avisos de la DSA y comunicaciones de autoridades en los siguientes idiomas: inglés, búlgaro, polaco. Responderemos en el idioma de su comunicación siempre que sea posible.",
    },
    "et": {
        "contact_dsa.s3_title": "Kuidas teatada ebaseaduslikust sisust",
        "contact_dsa.s3_what_to_include_title": "Teie teatis peaks sisaldama:",
        "contact_dsa.s4_title": "Mis juhtub pärast teatamist",
        "contact_dsa.s5_title": "Toetatud keeled",
        "contact_dsa.back_to_home": "Tagasi avalehele",
        "contact_dsa.s3_body": "Kui arvate, et Nevumo sisu on ELi või siseriikliku õiguse kohaselt ebaseaduslik, saatke palun teade aadressile legal@nevumo.com. Et saaksime teie aruannet tõhusalt töödelda, lisage palun järgmine teave:",
        "contact_dsa.s3_what_to_include_body": "1. Ebaseaduslikuks peetava sisu kirjeldus ja selle täpne asukoht platvormil (URL või kirjeldus).\n2. Õiguslik põhjus, miks te arvate, et sisu on ebaseaduslik.\n3. Teie nimi ja e-posti aadress (välja arvatud laste seksuaalset kuritarvitamist sisaldavate materjalide teadete puhul).\n4. Kinnitus selle kohta, et teie teatises esitatud teave on teie parimate teadmiste kohaselt täpne ja täielik.",
        "contact_dsa.s4_body": "Teie teatise saamisel me:\n• Saadame kohe automaatse kättesaamise kinnituse.\n• Vaatame teie aruande üle õigeaegselt, hoolikalt ja meelevaldselt.\n• Võtame meetmeid 72 tunni jooksul kiireloomuliste juhtumite korral (nt sisu, mis on seotud vägivalla, laste ohutuse või otsese ohuga).\n• Võtame meetmeid 7 tööpäeva jooksul standardsete aruannete puhul.\n• Teavitame teid oma otsusest ja selle põhjustest.\n• Teavitame teid õigusest meie otsus edasi kaevata.",
        "contact_dsa.s5_body": "Nevumo võtab DSA teateid ja asutuste teateid vastu järgmistes keeltes: inglise, bulgaaria, poola. Võimaluse korral vastame teie suhtluskeeles.",
    },
    "fi": {
        "contact_dsa.s3_title": "Kuinka ilmoittaa laittomasta sisällöstä",
        "contact_dsa.s3_what_to_include_title": "Ilmoituksesi tulee sisältää:",
        "contact_dsa.s4_title": "Mitä tapahtuu ilmoituksen jälkeen",
        "contact_dsa.s5_title": "Tuetut kielet",
        "contact_dsa.back_to_home": "Takaisin etusivulle",
        "contact_dsa.s3_body": "Jos uskot, että Nevumo-palvelun sisältö on EU:n tai kansallisen lainsäädännön mukaan laitonta, lähetä ilmoitus osoitteeseen legal@nevumo.com. Jotta voimme käsitellä ilmoituksesi tehokkaasti, sisällytä seuraavat tiedot:",
        "contact_dsa.s3_what_to_include_body": "1. Kuvaus laittomana pitämästäsi sisällöstä ja sen tarkka sijainti alustalla (URL tai kuvaus).\n2. Oikeudellinen syy, miksi uskot sisällön olevan laitonta.\n3. Nimesi ja sähköpostiosoitteesi (lukuun ottamatta ilmoituksia, jotka koskevat lasten seksuaalista hyväksikäyttöä sisältävää materiaalia).\n4. Lausunto, joka vahvistaa, että ilmoituksesi tiedot ovat parhaan tietämyksesi mukaan tarkkoja ja täydellisiä.",
        "contact_dsa.s4_body": "Saatuamme ilmoituksesi me:\n• Lähetämme automaattisen vastaanottokuittauksen välittömästi.\n• Tarkistamme ilmoituksesi oikea-aikaisesti, huolellisesti ja ei-mielivaltaisesti.\n• Ryhdymme toimenpiteisiin 72 tunnin kuluessa kiireellisissä tapauksissa (esim. sisältö, joka liittyy väkivaltaan, lasten turvallisuuteen tai välittömään vaaraan).\n• Ryhdymme toimenpiteisiin 7 työpäivän kuluessa vakioilmoitusten osalta.\n• Ilmoitamme sinulle päätöksestämme ja sen perusteluista.\n• Kerromme sinulle oikeudestasi valittaa päätöksestämme.",
        "contact_dsa.s5_body": "Nevumo hyväksyy DSA-ilmoitukset ja viranomaisviestinnän seuraavilla kielillä: englanti, bulgaria, puola. Vastaamme mahdollisuuksien mukaan viestintäsi kielellä.",
    },
    "fr": {
        "contact_dsa.s3_title": "Comment signaler un contenu illicite",
        "contact_dsa.s3_what_to_include_title": "Votre notification doit inclure :",
        "contact_dsa.s4_title": "Que se passe-t-il après votre signalement",
        "contact_dsa.s5_title": "Langues prises en charge",
        "contact_dsa.back_to_home": "Retour à l'accueil",
        "contact_dsa.s3_body": "Si vous pensez qu'un contenu sur Nevumo est illégal en vertu du droit européen ou national, veuillez envoyer un signalement à legal@nevumo.com. Afin de nous permettre de traiter efficacement votre signalement, veuillez inclure les informations suivantes :",
        "contact_dsa.s3_what_to_include_body": "1. Une description du contenu que vous considérez comme illégal et son emplacement exact sur la plateforme (URL ou description).\n2. Le motif légal pour lequel vous pensez que le contenu est illégal.\n3. Votre nom et votre adresse e-mail (sauf pour les signalements impliquant du matériel pédopornographique).\n4. Une déclaration confirmant que les informations contenues dans votre signalement sont exactes et complètes à votre connaissance.",
        "contact_dsa.s4_body": "Dès réception de votre signalement, nous allons :\n• Envoyer immédiatement une confirmation de réception automatique.\n• Examiner votre signalement de manière opportune, diligente et non arbitraire.\n• Prendre des mesures dans les 72 heures pour les cas urgents (par ex. contenu impliquant de la violence, la sécurité des enfants ou un préjudice imminent).\n• Prendre des mesures dans les 7 jours ouvrables pour les signalements standard.\n• Vous informer de notre décision et de ses motifs.\n• Vous informer de votre droit de faire appel de notre décision.",
        "contact_dsa.s5_body": "Nevumo accepte les signalements DSA et les communications des autorités dans les langues suivantes : anglais, bulgare, polonais. Nous répondrons dans la langue de votre communication dans la mesure du possible.",
    },
    "ga": {
        "contact_dsa.s3_title": "Conas Ábhar Neamhdhleathach a Thuairisciú",
        "contact_dsa.s3_what_to_include_title": "Ba cheart go n-áireofaí i d'fhógra:",
        "contact_dsa.s4_title": "Cad a Tharlaíonn Tar éis Tuairisciú",
        "contact_dsa.s5_title": "Teangacha Tacaithe",
        "contact_dsa.back_to_home": "Ar ais go dtí an Baile",
        "contact_dsa.s3_body": "Má chreideann tú go bhfuil ábhar ar Nevumo neamhdhleathach faoi dhlí an AE nó faoin dlí náisiúnta, seol fógra chuig legal@nevumo.com le do thoil. Chun ligean dúinn do thuairisc a phróiseáil go héifeachtach, cuir an fhaisnéis seo a leanas san áireamh:",
        "contact_dsa.s3_what_to_include_body": "1. Cur síos ar an ábhar a chreideann tú a bheith neamhdhleathach agus a shuíomh cruinn ar an ardán (URL nó cur síos).\n2. An chúis dhlíthiúil a chreideann tú go bhfuil an t-ábhar neamhdhleathach.\n3. D'ainm agus do sheoladh ríomhphoist (seachas tuairiscí a bhaineann le hábhar mí-úsáide gnéasaí leanaí).\n4. Ráiteas a dheimhníonn go bhfuil an fhaisnéis i d'fhógra cruinn agus iomlán chomh fada agus is eol duit.",
        "contact_dsa.s4_body": "Ar fháil d'fhógra, déanfaimid:\n• Dearbhú uathoibríoch fála a sheoladh láithreach.\n• Do thuairisc a athbhreithniú ar bhealach tráthúil, dícheallach agus neamh-threallach.\n• Gníomh a ghlacadh laistigh de 72 uair an chloig i gcásanna práinneacha (m.sh. ábhar a bhaineann le foréigean, sábháilteacht leanaí, nó dochar atá le teacht).\n• Gníomh a ghlacadh laistigh de 7 lá oibre le haghaidh tuairiscí caighdeánacha.\n• Do chinneadh agus na cúiseanna atá leis a chur in iúl duit.\n• Do cheart chun achomharc a dhéanamh i gcoinne ár gcinneadh a chur in iúl duit.",
        "contact_dsa.s5_body": "Glacann Nevumo le fógraí DSA agus cumarsáid údaráis sna teangacha seo a leanas: Béarla, Bulgáiris, Polainnis. Tabharfaimid freagra i dteanga do chumarsáide nuair is féidir.",
    },
    "hr": {
        "contact_dsa.s3_title": "Kako prijaviti nezakoniti sadržaj",
        "contact_dsa.s3_what_to_include_title": "Vaša prijava treba sadržavati:",
        "contact_dsa.s4_title": "Što se događa nakon prijave",
        "contact_dsa.s5_title": "Podržani jezici",
        "contact_dsa.back_to_home": "Natrag na početnu",
        "contact_dsa.s3_body": "Ako smatrate da je sadržaj na Nevumu nezakonit prema pravu EU-a ili nacionalnom pravu, pošaljite prijavu na legal@nevumo.com. Kako bismo vašu prijavu mogli učinkovito obraditi, molimo vas da uključite sljedeće podatke:",
        "contact_dsa.s3_what_to_include_body": "1. Opis sadržaja za koji smatrate da je nezakonit i njegovu točnu lokaciju na platformi (URL ili opis).\n2. Pravni razlog zašto smatrate da je sadržaj nezakonit.\n3. Vaše ime i e-mail adresu (osim za prijave koje se odnose na materijale dječjeg seksualnog zlostavljanja).\n4. Izjavu kojom potvrđujete da su podaci u vašoj prijavi točni i potpuni prema vašem najboljem saznanju.",
        "contact_dsa.s4_body": "Po primitku vaše prijave, mi ćemo:\n• Odmah poslati automatsku potvrdu o primitku.\n• Pregledati vašu prijavu pravovremeno, pažljivo i neproizvoljno.\n• Poduzeti mjere u roku od 72 sata za hitne slučajeve (npr. sadržaj koji uključuje nasilje, sigurnost djece ili neposrednu štetu).\n• Poduzeti mjere u roku od 7 radnih dana za standardne prijave.\n• Obavijestiti vas o našoj odluci i razlozima za nju.\n• Obavijestiti vas o vašem pravu na žalbu na našu odluku.",
        "contact_dsa.s5_body": "Nevumo prihvaća DSA prijave i komunikaciju od tijela vlasti na sljedećim jezicima: engleski, bugarski, poljski. Odgovorit ćemo na jeziku vaše komunikacije gdje god je to moguće.",
    },
    "hu": {
        "contact_dsa.s3_title": "Hogyan jelentsen illegális tartalmat",
        "contact_dsa.s3_what_to_include_title": "Az értesítésnek tartalmaznia kell:",
        "contact_dsa.s4_title": "Mi történik a bejelentés után",
        "contact_dsa.s5_title": "Támogatott nyelvek",
        "contact_dsa.back_to_home": "Vissza a főoldalra",
        "contact_dsa.s3_body": "Ha úgy gondolja, hogy a Nevumo oldalon található tartalom az EU vagy a nemzeti jog szerint illegális, kérjük, küldjön értesítést a legal@nevumo.com címre. Annak érdekében, hogy bejelentését hatékonyan fel tudjuk dolgozni, kérjük, adja meg a következő információkat:",
        "contact_dsa.s3_what_to_include_body": "1. Az Ön által illegálisnak tartott tartalom leírása és annak pontos helye a platformon (URL vagy leírás).\n2. A jogi ok, amiért Ön illegálisnak tartja a tartalmat.\n3. Az Ön neve és e-mail címe (kivéve a gyermekek szexuális zaklatását ábrázoló anyagokkal kapcsolatos bejelentéseket).\n4. Egy nyilatkozat, amely megerősíti, hogy az értesítésben szereplő információk az Ön legjobb tudása szerint pontosak és teljesek.",
        "contact_dsa.s4_body": "Az Ön értesítésének kézhezvételét követően mi:\n• Azonnal automatikus visszaigazolást küldünk a kézhezvételről.\n• Bejelentését időszerűen, gondosan és nem önkényes módon felülvizsgáljuk.\n• Sürgős esetekben (pl. erőszakot, gyermekbiztonságot vagy közvetlen kárt okozó tartalom) 72 órán belül intézkedünk.\n• Standard bejelentések esetén 7 munkanapon belül intézkedünk.\n• Értesítjük Önt a döntésünkről és annak okairól.\n• Tájékoztatjuk Önt a döntésünk elleni fellebbezés jogáról.",
        "contact_dsa.s5_body": "A Nevumo a DSA-értesítéseket és a hatósági kommunikációkat a következő nyelveken fogadja el: angol, bolgár, lengyel. Lehetőség szerint az Ön kommunikációjának nyelvén válaszolunk.",
    },
    "is": {
        "contact_dsa.s3_title": "Hvernig á að tilkynna um ólöglegt efni",
        "contact_dsa.s3_what_to_include_title": "Tilkynning þín ætti að innihalda:",
        "contact_dsa.s4_title": "Hvað gerist eftir að þú tilkynnir",
        "contact_dsa.s5_title": "Studdar tungumál",
        "contact_dsa.back_to_home": "Aftur á forsíðu",
        "contact_dsa.s3_body": "Ef þú telur að efni á Nevumo sé ólöglegt samkvæmt ESB- eða landslögum, vinsamlegast sendu tilkynningu á legal@nevumo.com. Til að við getum afgreitt skýrslu þína á áhrifaríkan hátt, vinsamlegast láttu eftirfarandi upplýsingar fylgja með:",
        "contact_dsa.s3_what_to_include_body": "1. Lýsing á efninu sem þú telur að sé ólöglegt og nákvæm staðsetning þess á pallinum (URL eða lýsing).\n2. Lagaleg ástæða þess að þú telur að efnið sé ólöglegt.\n3. Nafn þitt og netfang (nema fyrir skýrslur sem fela í sér kynferðislega misnotkun á börnum).\n4. Yfirlýsing sem staðfestir að upplýsingarnar í tilkynningu þinni séu réttar og fullkomnar eftir bestu vitund.",
        "contact_dsa.s4_body": "Við móttöku tilkynningar þinnar munum við:\n• Senda sjálfvirka staðfestingu á móttöku strax.\n• Fara yfir skýrslu þína tímanlega, af kostgæfni og ekki af geðþótta.\n• Grípa til aðgerða innan 72 klukkustunda vegna brýnna mála (t.d. efni sem varðar ofbeldi, öryggi barna eða yfirvofandi skaða).\n• Grípa til aðgerða innan 7 virkra daga vegna hefðbundinna skýrslna.\n• Láta þig vita af ákvörðun okkar og ástæðum hennar.\n• Upplýsa þig um rétt þinn til að áfrýja ákvörðun okkar.",
        "contact_dsa.s5_body": "Nevumo samþykkir DSA tilkynningar og samskipti yfirvalda á eftirfarandi tungumálum: ensku, búlgörsku, pólsku. Við munum svara á tungumáli samskipta þinna þar sem það er mögulegt.",
    },
    "it": {
        "contact_dsa.s3_title": "Come segnalare contenuti illegali",
        "contact_dsa.s3_what_to_include_title": "La sua segnalazione deve includere:",
        "contact_dsa.s4_title": "Cosa succede dopo la segnalazione",
        "contact_dsa.s5_title": "Lingue supportate",
        "contact_dsa.back_to_home": "Torna alla home",
        "contact_dsa.s3_body": "Se ritieni che i contenuti su Nevumo siano illegali ai sensi del diritto dell'UE o nazionale, invia una segnalazione a legal@nevumo.com. Per consentirci di elaborare la tua segnalazione in modo efficace, includi le seguenti informazioni:",
        "contact_dsa.s3_what_to_include_body": "1. Una descrizione dei contenuti che ritieni illegali e la loro esatta posizione sulla piattaforma (URL o descrizione).\n2. Il motivo legale per cui ritieni che i contenuti siano illegali.\n3. Il tuo nome e indirizzo e-mail (tranne per le segnalazioni che coinvolgono materiale pedopornografico).\n4. Una dichiarazione che conferma che le informazioni nella tua segnalazione sono accurate e complete al meglio delle tue conoscenze.",
        "contact_dsa.s4_body": "Al ricevimento della tua segnalazione, provvederemo a:\n• Inviare immediatamente una conferma automatica di ricezione.\n• Esaminare la tua segnalazione in modo tempestivo, diligente e non arbitrario.\n• Intervenire entro 72 ore per i casi urgenti (es. contenuti che coinvolgono violenza, sicurezza dei minori o danno imminente).\n• Intervenire entro 7 giorni lavorativi per le segnalazioni standard.\n• Informarti della nostra decisione e dei relativi motivi.\n• Informarti del tuo diritto di ricorrere in appello contro la nostra decisione.",
        "contact_dsa.s5_body": "Nevumo accetta le segnalazioni DSA e le comunicazioni delle autorità nelle seguenti lingue: inglese, bulgaro, polacco. Risponderemo nella lingua della tua comunicazione ove possibile.",
    },
    "lb": {
        "contact_dsa.s3_title": "Wéi ee illegalen Inhalt mellt",
        "contact_dsa.s3_what_to_include_title": "Är Meldung soll enthalen:",
        "contact_dsa.s4_title": "Wat geschitt no Ärer Meldung",
        "contact_dsa.s5_title": "Ënnerstëtzte Sproochen",
        "contact_dsa.back_to_home": "Zréck zur Haaptsäit",
        "contact_dsa.s3_body": "Wann Dir mengt datt Inhalt op Nevumo ënner EU- oder nationalem Recht illegal ass, schéckt w.e.g. eng Meldung op legal@nevumo.com. Fir eis z'erméiglechen Äre Rapport effektiv ze veraarbechten, gitt w.e.g. déi folgend Informatiounen un:",
        "contact_dsa.s3_what_to_include_body": "1. Eng Beschreiwung vum Inhalt, deen Dir als illegal betruecht, a seng genee Plaz op der Plattform (URL oder Beschreiwung).\n2. De legale Grond firwat Dir mengt datt den Inhalt illegal ass.\n3. Ären Numm an E-Mail Adress (ausser fir Berichter mat Kannerpornographie).\n4. Eng Ausso, déi bestätegt datt d'Informatioun an Ärer Meldung no Ärem beschte Wëssen richteg a komplett ass.",
        "contact_dsa.s4_body": "Beim Empfang vun Ärer Meldung wäerte mir:\n• Direkt eng automatesch Empfangsbestätegung schécken.\n• Äre Rapport an der Zäit, suergfälteg an net-arbiträr iwwerpréiwen.\n• Bannent 72 Stonnen an dréngende Fäll handelen (z.B. Inhalt iwwer Gewalt, Kannersécherheet oder direkten Schued).\n• Bannent 7 Aarbechtsdeeg fir Standardberichter handelen.\n• Iech iwwer eis Entscheedung an hir Grënn informéieren.\n• Iech iwwer Äert Recht informéieren, géint eis Entscheedung anzespriechen.",
        "contact_dsa.s5_body": "Nevumo akzeptéiert DSA Meldungen an Autoritéitskommunikatiounen an de folgende Sproochen: Englesch, Bulgaresch, Polnesch. Mir äntweren an der Sprooch vun Ärer Kommunikatioun wa méiglech.",
    },
    "lt": {
        "contact_dsa.s3_title": "Kaip pranešti apie neteisėtą turinį",
        "contact_dsa.s3_what_to_include_title": "Jūsų pranešime turėtų būti:",
        "contact_dsa.s4_title": "Kas nutinka po pranešimo",
        "contact_dsa.s5_title": "Palaikomos kalbos",
        "contact_dsa.back_to_home": "Grįžti į pradžią",
        "contact_dsa.s3_body": "Jei manote, kad turinys „Nevumo“ platformoje yra neteisėtas pagal ES ar nacionalinę teisę, atsiųskite pranešimą adresu legal@nevumo.com. Kad galėtume veiksmingai apdoroti jūsų pranešimą, pateikite šią informaciją:",
        "contact_dsa.s3_what_to_include_body": "1. Turinio, kurį laikote neteisėtu, aprašymas ir tiksli jo vieta platformoje (URL arba aprašymas).\n2. Teisinė priežastis, dėl kurios manote, kad turinys yra neteisėtas.\n3. Jūsų vardas, pavardė ir el. pašto adresas (išskyrus pranešimus, susijusius su vaikų seksualinio išnaudojimo medžiaga).\n4. Pareiškimas, patvirtinantis, kad jūsų pranešime pateikta informacija, jūsų žiniomis, yra tiksli ir išsami.",
        "contact_dsa.s4_body": "Gavę jūsų pranešimą, mes:\n• Nedelsdami išsiųsime automatinį gavimo patvirtinimą.\n• Laiku, atidžiai ir ne savavališkai peržiūrėsime jūsų pranešimą.\n• Imsimės veiksmų per 72 valandas skubiais atvejais (pvz., turinys, susijęs su smurtu, vaikų saugumu ar neišvengiama žala).\n• Imsimės veiksmų per 7 darbo dienas dėl standartinių pranešimų.\n• Pranešime jums apie mūsų sprendimą ir jo priežastis.\n• Informuosime jus apie teisę apskųsti mūsų sprendimą.",
        "contact_dsa.s5_body": "„Nevumo“ priima DSA pranešimus ir institucijų pranešimus šiomis kalbomis: anglų, bulgarų, lenkų. Kur įmanoma, atsakysime jūsų komunikacijos kalba.",
    },
    "lv": {
        "contact_dsa.s3_title": "Kā ziņot par nelikumīgu saturu",
        "contact_dsa.s3_what_to_include_title": "Jūsu paziņojumā jāiekļauj:",
        "contact_dsa.s4_title": "Kas notiek pēc ziņošanas",
        "contact_dsa.s5_title": "Atbalstītās valodas",
        "contact_dsa.back_to_home": "Atpakaļ uz sākumu",
        "contact_dsa.s3_body": "Ja uzskatāt, ka saturs Nevumo ir nelikumīgs saskaņā ar ES vai valsts tiesību aktiem, lūdzu, nosūtiet paziņojumu uz legal@nevumo.com. Lai mēs varētu efektīvi apstrādāt jūsu ziņojumu, lūdzu, iekļaujiet šādu informāciju:",
        "contact_dsa.s3_what_to_include_body": "1. Tā satura apraksts, kuru uzskatāt par nelikumīgu, un tā precīza atrašanās vieta platformā (URL vai apraksts).\n2. Juridiskais iemesls, kāpēc uzskatāt, ka saturs ir nelikumīgs.\n3. Jūsu vārds un e-pasta adrese (izņemot ziņojumus, kas saistīti ar bērnu seksuālas izmantošanas materiāliem).\n4. Paziņojums, kas apliecina, ka jūsu paziņojumā sniegtā informācija, cik jums zināms, ir precīza un pilnīga.",
        "contact_dsa.s4_body": "Pēc jūsu paziņojuma saņemšanas mēs:\n• Nekavējoties nosūtīsim automātisku saņemšanas apstiprinājumu.\n• Pārskatīsim jūsu ziņojumu savlaicīgi, rūpīgi un patvaļīgi.\n• Steidzamos gadījumos (piemēram, saturs, kas saistīts ar vardarbību, bērnu drošību vai nenovēršamu kaitējumu) rīkosimies 72 stundu laikā.\n• Standarta ziņojumu gadījumā rīkosimies 7 darba dienu laikā.\n• Paziņosim jums par mūsu lēmumu un tā iemesliem.\n• Informēsim jūs par tiesībām pārsūdzēt mūsu lēmumu.",
        "contact_dsa.s5_body": "Nevumo pieņem DSA paziņojumus un iestāžu saziņu šādās valodās: angļu, bulgāru, poļu. Mēs atbildēsim jūsu saziņas valodā, kur vien iespējams.",
    },
    "mk": {
        "contact_dsa.s3_title": "Како да пријавите незаконита содржина",
        "contact_dsa.s3_what_to_include_title": "Вашата пријава треба да содржи:",
        "contact_dsa.s4_title": "Што се случува по пријавата",
        "contact_dsa.s5_title": "Поддржани јазици",
        "contact_dsa.back_to_home": "Назад кон почетна",
        "contact_dsa.s3_body": "Доколку сметате дека содржината на Nevumo е незаконита според правото на ЕУ или националното право, ве молиме испратете известување на legal@nevumo.com. За да ни овозможите ефективно да ја обработиме вашата пријава, ве молиме вклучете ги следните информации:",
        "contact_dsa.s3_what_to_include_body": "1. Опис на содржината што ја сметате за незаконита и нејзината точна локација на платформата (URL или опис).\n2. Правната причина поради која сметате дека содржината е незаконита.\n3. Вашето име и адреса на е-пошта (освен за пријави кои вклучуваат материјали за сексуална злоупотреба на деца).\n4. Изјава со која потврдувате дека информациите во вашето известување се точни и целосни според вашето најдобро знаење.",
        "contact_dsa.s4_body": "По приемот на вашето известување, ние ќе:\n• Испратиме автоматска потврда за прием веднаш.\n• Ја разгледаме вашата пријава навремено, внимателно и неарбитрарно.\n• Преземеме акција во рок од 72 часа за итни случаи (на пр. содржина што вклучува насилство, безбедност на децата или неминовна штета).\n• Преземеме акција во рок од 7 работни дена за стандардни пријави.\n• Ве известиме за нашата одлука и причините за неа.\n• Ве информираме за вашето право на жалба на нашата одлука.",
        "contact_dsa.s5_body": "Nevumo прифаќа DSA известувања и комуникации од органите на следните јазици: англиски, бугарски, полски. Ќе одговориме на јазикот на вашата комуникација каде што е можно.",
    },
    "mt": {
        "contact_dsa.s3_title": "Kif Tirrapporta Kontenut Illegali",
        "contact_dsa.s3_what_to_include_title": "L-avviż tiegħek għandu jinkludi:",
        "contact_dsa.s4_title": "X'jiġri Wara li Tirrapporta",
        "contact_dsa.s5_title": "Lingwi Appoġġjati",
        "contact_dsa.back_to_home": "Lura għad-Dar",
        "contact_dsa.s3_body": "Jekk temmen li l-kontenut fuq Nevumo huwa illegali taħt il-liġi tal-UE jew dik nazzjonali, jekk jogħġbok ibgħat avviż lil legal@nevumo.com. Biex inkunu nistgħu nipproċessaw ir-rapport tiegħek b'mod effettiv, jekk jogħġbok inkludi l-informazzjoni li ġejja:",
        "contact_dsa.s3_what_to_include_body": "1. Deskrizzjoni tal-kontenut li temmen li huwa illegali u l-post eżatt tiegħu fuq il-pjattaforma (URL jew deskrizzjoni).\n2. Ir-raġuni legali għaliex temmen li l-kontenut huwa illegali.\n3. Ismek u l-indirizz tal-email tiegħek (ħlief għal rapporti li jinvolvu materjal ta' abbuż sesswali tat-tfal).\n4. Dikjarazzjoni li tikkonferma li l-informazzjoni fl-avviż tiegħek hija preċiża u sħiħa sa fejn taf int.",
        "contact_dsa.s4_body": "Malli nirċievu l-avviż tiegħek, aħna se:\n• Nibagħtu konferma awtomatika tal-wasla immedjatament.\n• Nirrevedu r-rapport tiegħek b'mod f'waqtu, diliġenti u mhux arbitrarju.\n• Nieħdu azzjoni fi żmien 72 siegħa għal każijiet urġenti (eż. kontenut li jinvolvi vjolenza, sigurtà tat-tfal, jew ħsara imminenti).\n• Nieħdu azzjoni fi żmien 7 ijiem tax-xogħol għal rapporti standard.\n• Ninnotifikawk bid-deċiżjoni tagħna u r-raġunijiet għaliha.\n• Ninfurmawk bid-dritt tiegħek li tappella d-deċiżjoni tagħna.",
        "contact_dsa.s5_body": "Nevumo jaċċetta avviżi tad-DSA u komunikazzjonijiet tal-awtoritajiet fil-lingwi li ġejjin: Ingliż, Bulgaru, Pollakk. Aħna se nwieġbu fil-lingwa tal-komunikazzjoni tiegħek fejn possibbli.",
    },
    "nl": {
        "contact_dsa.s3_title": "Hoe illegale inhoud te melden",
        "contact_dsa.s3_what_to_include_title": "Uw melding moet het volgende bevatten:",
        "contact_dsa.s4_title": "Wat er na uw melding gebeurt",
        "contact_dsa.s5_title": "Ondersteunde talen",
        "contact_dsa.back_to_home": "Terug naar home",
        "contact_dsa.s3_body": "Als u van mening bent dat inhoud op Nevumo illegaal is onder de EU- of nationale wetgeving, stuur dan een melding naar legal@nevumo.com. Om ons in staat te stellen uw rapport effectief te verwerken, verzoeken wij u de volgende informatie op te nemen:",
        "contact_dsa.s3_what_to_include_body": "1. Een beschrijving van de inhoud die u als illegaal beschouwt en de exacte locatie ervan op het platform (URL of beschrijving).\n2. De juridische reden waarom u van mening bent dat de inhoud illegaal is.\n3. Uw naam en e-mailadres (behalve bij meldingen met betrekking tot materiaal van seksueel misbruik van kinderen).\n4. Een verklaring die bevestigt dat de informatie in uw melding naar uw beste weten juist en volledig is.",
        "contact_dsa.s4_body": "Na ontvangst van uw melding zullen wij:\n• Onmiddellijk een automatische ontvangstbevestiging sturen.\n• Uw rapport tijdig, zorgvuldig en niet-willekeurig beoordelen.\n• Binnen 72 uur actie ondernemen voor urgente gevallen (bijv. inhoud met betrekking tot geweld, kinderveiligheid of dreigende schade).\n• Binnen 7 werkdagen actie ondernemen voor standaardrapporten.\n• U op de hoogte stellen van onze beslissing en de redenen daarvoor.\n• U informeren over uw recht om tegen onze beslissing in beroep te gaan.",
        "contact_dsa.s5_body": "Nevumo accepteert DSA-meldingen en communicatie van autoriteiten in de volgende talen: Engels, Bulgaars, Pools. Waar mogelijk zullen wij antwoorden in de taal van uw communicatie.",
    },
    "no": {
        "contact_dsa.s3_title": "Slik rapporterer du ulovlig innhold",
        "contact_dsa.s3_what_to_include_title": "Meldingen din bør inneholde:",
        "contact_dsa.s4_title": "Hva skjer etter at du rapporterer",
        "contact_dsa.s5_title": "Støttede språk",
        "contact_dsa.back_to_home": "Tilbake til forsiden",
        "contact_dsa.s3_body": "Hvis du mener at innhold på Nevumo er ulovlig i henhold til EU-lovgivning eller nasjonal lovgivning, vennligst send en melding til legal@nevumo.com. For at vi skal kunne behandle rapporten din effektivt, vennligst inkluder følgende informasjon:",
        "contact_dsa.s3_what_to_include_body": "1. En beskrivelse av innholdet du mener er ulovlig, og dets nøyaktige plassering på plattformen (URL eller beskrivelse).\n2. Den juridiske grunnen til at du mener innholdet er ulovlig.\n3. Ditt navn og e-postadresse (unntatt for rapporter som involverer materiale om seksuelt misbruk av barn).\n4. En uttalelse som bekrefter at informasjonen i varselet ditt er nøyaktig og fullstendig etter din beste viten.",
        "contact_dsa.s4_body": "Ved mottak av varselet ditt vil vi:\n• Sende en automatisk bekreftelse på mottak umiddelbart.\n• Gjennomgå rapporten din på en rettidig, nøye og ikke-vilkårlig måte.\n• Iverksette tiltak innen 72 timer i hastesaker (f.eks. innhold som involverer vold, barns sikkerhet eller overhengende fare).\n• Iverksette tiltak innen 7 virkedager for standardrapporter.\n• Varsle deg om vår beslutning og årsakene til den.\n• Informere deg om din rett til å anke beslutningen vår.",
        "contact_dsa.s5_body": "Nevumo aksepterer DSA-varsler og myndighetskommunikasjon på følgende språk: engelsk, bulgarsk, polsk. Vi vil svare på språket i kommunikasjonen din der det er mulig.",
    },
    "pl": {
        "contact_dsa.s3_title": "Jak zgłosić nielegalne treści",
        "contact_dsa.s3_what_to_include_title": "Zgłoszenie powinno zawierać:",
        "contact_dsa.s4_title": "Co dzieje się po zgłoszeniu",
        "contact_dsa.s5_title": "Obsługiwane języki",
        "contact_dsa.back_to_home": "Powrót do strony głównej",
        "contact_dsa.s3_body": "Jeśli uważasz, że treści w serwisie Nevumo są nielegalne zgodnie z prawem UE lub prawem krajowym, wyślij zgłoszenie na adres legal@nevumo.com. Aby umożliwić nam skuteczne rozpatrzenie zgłoszenia, prosimy o podanie następujących informacji:",
        "contact_dsa.s3_what_to_include_body": "1. Opis treści, które uważasz za nielegalne, oraz dokładna lokalizacja w serwisie (adres URL lub opis).\n2. Podstawa prawna, na której opierasz się, twierdząc, że treść jest nielegalna.\n3. Twoje imię i nazwisko oraz adres e-mail (z wyjątkiem zgłoszeń dotyczących materiałów przedstawiających seksualne wykorzystywanie dzieci).\n4. Oświadczenie potwierdzające, że informacje zawarte w zgłoszeniu są zgodne z Twoją najlepszą wiedzą.",
        "contact_dsa.s4_body": "Po otrzymaniu zgłoszenia:\n• Niezwłocznie wyślemy automatyczne potwierdzenie odbioru.\n• Rozpatrzymy zgłoszenie terminowo, starannie i bezstronnie.\n• Podejmiemy działania w ciągu 72 godzin w pilnych przypadkach (np. treści związane z przemocą, bezpieczeństwem dzieci lub bezpośrednim zagrożeniem).\n• Podejmiemy działania w ciągu 7 dni roboczych w przypadku standardowych zgłoszeń.\n• Poinformujemy Cię o naszej decyzji i jej uzasadnieniu.\n• Poinformujemy Cię o prawie do odwołania od naszej decyzji.",
        "contact_dsa.s5_body": "Nevumo przyjmuje zgłoszenia DSA i komunikację od organów w następujących językach: angielskim, bułgarskim i polskim. W miarę możliwości będziemy odpowiadać w języku Twojej wiadomości.",
    },
    "pt": {
        "contact_dsa.s3_title": "Como Denunciar Conteúdo Ilegal",
        "contact_dsa.s3_what_to_include_title": "Seu aviso deve incluir:",
        "contact_dsa.s4_title": "O Que Acontece Após a Denúncia",
        "contact_dsa.s5_title": "Idiomas Suportados",
        "contact_dsa.back_to_home": "Voltar ao início",
        "contact_dsa.s3_body": "Se você acredita que o conteúdo no Nevumo é ilegal de acordo com a legislação da UE ou nacional, envie um aviso para legal@nevumo.com. Para nos permitir processar sua denúncia de forma eficaz, inclua as seguintes informações:",
        "contact_dsa.s3_what_to_include_body": "1. Uma descrição do conteúdo que você considera ilegal e sua localização exata na plataforma (URL ou descrição).\n2. O motivo legal pelo qual você acredita que o conteúdo é ilegal.\n3. Seu nome e endereço de e-mail (exceto para denúncias envolvendo material de abuso sexual infantil).\n4. Uma declaração confirmando que as informações em seu aviso são precisas e completas, de acordo com o seu melhor conhecimento.",
        "contact_dsa.s4_body": "Após o recebimento de seu aviso, nós iremos:\n• Enviar uma confirmação automática de recebimento imediatamente.\n• Analisar sua denúncia de forma oportuna, diligente e não arbitrária.\n• Tomar medidas dentro de 72 horas para casos urgentes (por exemplo, conteúdo envolvendo violência, segurança infantil ou dano iminente).\n• Tomar medidas dentro de 7 dias úteis para denúncias padrão.\n• Notificá-lo sobre nossa decisão e os motivos dela.\n• Informá-lo sobre seu direito de recorrer de nossa decisão.",
        "contact_dsa.s5_body": "O Nevumo aceita avisos da DSA e comunicações de autoridades nos seguintes idiomas: inglês, búlgaro, polonês. Responderemos no idioma de sua comunicação sempre que possível.",
    },
    "pt_PT": {
        "contact_dsa.s3_title": "Como Denunciar Conteúdo Ilegal",
        "contact_dsa.s3_what_to_include_title": "O seu aviso deve incluir:",
        "contact_dsa.s4_title": "O Que Acontece Após a Denúncia",
        "contact_dsa.s5_title": "Idiomas Suportados",
        "contact_dsa.back_to_home": "Voltar ao início",
        "contact_dsa.s3_body": "Se acredita que o conteúdo no Nevumo é ilegal ao abrigo da legislação da UE ou nacional, envie um aviso para legal@nevumo.com. Para nos permitir processar a sua denúncia de forma eficaz, inclua as seguintes informações:",
        "contact_dsa.s3_what_to_include_body": "1. Uma descrição do conteúdo que considera ilegal e a sua localização exata na plataforma (URL ou descrição).\n2. O motivo legal pelo qual acredita que o conteúdo é ilegal.\n3. O seu nome e endereço de e-mail (exceto para denúncias envolvendo material de abuso sexual infantil).\n4. Uma declaração confirmando que as informações no seu aviso são precisas e completas, com o seu melhor conhecimento.",
        "contact_dsa.s4_body": "Após a receção do seu aviso, iremos:\n• Enviar uma confirmação automática de receção imediatamente.\n• Analisar a sua denúncia de forma atempada, diligente e não arbitrária.\n• Tomar medidas no prazo de 72 horas para casos urgentes (por exemplo, conteúdo que envolva violência, segurança infantil ou dano iminente).\n• Tomar medidas no prazo de 7 dias úteis para denúncias padrão.\n• Notificá-lo da nossa decisão e dos motivos da mesma.\n• Informá-lo do seu direito de recorrer da nossa decisão.",
        "contact_dsa.s5_body": "O Nevumo aceita avisos da DSA e comunicações de autoridades nos seguintes idiomas: inglês, búlgaro, polaco. Responderemos no idioma da sua comunicação sempre que possível.",
    },
    "ro": {
        "contact_dsa.s3_title": "Cum să raportați conținut ilegal",
        "contact_dsa.s3_what_to_include_title": "Notificarea dvs. trebuie să includă:",
        "contact_dsa.s4_title": "Ce se întâmplă după raportare",
        "contact_dsa.s5_title": "Limbi acceptate",
        "contact_dsa.back_to_home": "Înapoi la pagina principală",
        "contact_dsa.s3_body": "Dacă considerați că un conținut de pe Nevumo este ilegal conform legislației UE sau naționale, vă rugăm să trimiteți o notificare la legal@nevumo.com. Pentru a ne permite să procesăm raportul dvs. în mod eficient, vă rugăm să includeți următoarele informații:",
        "contact_dsa.s3_what_to_include_body": "1. O descriere a conținutului pe care îl considerați ilegal și locația sa exactă pe platformă (URL sau descriere).\n2. Motivul legal pentru care considerați că acest conținut este ilegal.\n3. Numele și adresa dvs. de e-mail (cu excepția rapoartelor care implică materiale privind abuzul sexual asupra copiilor).\n4. O declarație care confirmă că informațiile din notificarea dvs. sunt exacte și complete, din câte cunoașteți.",
        "contact_dsa.s4_body": "La primirea notificării dvs., vom:\n• Trimite imediat o confirmare automată de primire.\n• Examina raportul dvs. în mod oportun, diligent și non-arbitrar.\n• Lua măsuri în termen de 72 de ore pentru cazuri urgente (de ex., conținut care implică violență, siguranța copiilor sau vătămare iminentă).\n• Lua măsuri în termen de 7 zile lucrătoare pentru rapoarte standard.\n• Vă vom notifica decizia noastră și motivele acesteia.\n• Vă vom informa despre dreptul de a face apel la decizia noastră.",
        "contact_dsa.s5_body": "Nevumo acceptă notificări DSA și comunicări ale autorităților în următoarele limbi: engleză, bulgară, poloneză. Vom răspunde în limba comunicării dvs. acolo unde este posibil.",
    },
    "ru": {
        "contact_dsa.s3_title": "Как сообщить о незаконном контенте",
        "contact_dsa.s3_what_to_include_title": "Ваше уведомление должно содержать:",
        "contact_dsa.s4_title": "Что происходит после подачи сообщения",
        "contact_dsa.s5_title": "Поддерживаемые языки",
        "contact_dsa.back_to_home": "На главную",
        "contact_dsa.s3_body": "Если вы считаете, что контент на Nevumo является незаконным в соответствии с законодательством ЕС или национальным законодательством, отправьте уведомление по адресу legal@nevumo.com. Чтобы мы могли эффективно обработать ваше сообщение, пожалуйста, укажите следующую информацию:",
        "contact_dsa.s3_what_to_include_body": "1. Описание контента, который вы считаете незаконным, и его точное местоположение на платформе (URL или описание).\n2. Юридическая причина, по которой вы считаете контент незаконным.\n3. Ваше имя и адрес электронной почты (за исключением сообщений о материалах с сексуальным насилием над детьми).\n4. Заявление, подтверждающее, что информация в вашем уведомлении является точной и полной, насколько вам известно.",
        "contact_dsa.s4_body": "По получении вашего уведомления мы:\n• Немедленно отправим автоматическое подтверждение получения.\n• Рассмотрим ваше сообщение своевременно, тщательно и непроизвольно.\n• Примем меры в течение 72 часов в экстренных случаях (например, контент, связанный с насилием, безопасностью детей или неминуемой угрозой).\n• Примем меры в течение 7 рабочих дней по стандартным сообщениям.\n• Уведомим вас о нашем решении и его причинах.\n• Сообщим вам о вашем праве обжаловать наше решение.",
        "contact_dsa.s5_body": "Nevumo принимает уведомления DSA и сообщения от органов власти на следующих языках: английский, болгарский, польский. По возможности мы ответим на языке вашего обращения.",
    },
    "sk": {
        "contact_dsa.s3_title": "Ako nahlásiť nezákonný obsah",
        "contact_dsa.s3_what_to_include_title": "Vaše oznámenie by malo obsahovať:",
        "contact_dsa.s4_title": "Čo sa stane po nahlásení",
        "contact_dsa.s5_title": "Podporované jazyky",
        "contact_dsa.back_to_home": "Späť na úvod",
        "contact_dsa.s3_body": "Ak sa domnievate, že obsah na platforme Nevumo je podľa práva EÚ alebo vnútroštátneho práva nezákonný, zašlite prosím oznámenie na adresu legal@nevumo.com. Aby sme mohli vaše nahlásenie efektívne spracovať, uveďte prosím nasledujúce informácie:",
        "contact_dsa.s3_what_to_include_body": "1. Popis obsahu, ktorý považujete za nezákonný, a jeho presné umiestnenie na platforme (URL alebo popis).\n2. Právny dôvod, prečo sa domnievate, že obsah je nezákonný.\n3. Vaše meno a e-mailovú adresu (s výnimkou hlásení týkajúcich sa materiálov sexuálneho zneužívania detí).\n4. Vyhlásenie potvrdzujúce, že informácie vo vašom oznámení sú podľa vášho najlepšieho vedomia presné a úplné.",
        "contact_dsa.s4_body": "Po obdržaní vášho oznámenia:\n• Okamžite zašleme automatické potvrdenie o prijatí.\n• Vaše nahlásenie včas, dôkladne a nestranne preskúmame.\n• V naliehavých prípadoch zakročíme do 72 hodín (napr. obsah zahŕňajúci násilie, bezpečnosť detí alebo bezprostrednú hrozbu).\n• V prípade štandardných hlásení zakročíme do 7 pracovných dní.\n• Budeme vás informovať o našom rozhodnutí a jeho dôvodoch.\n• Budeme vás informovať o vašom práve odvolať sa proti nášmu rozhodnutiu.",
        "contact_dsa.s5_body": "Nevumo prijíma oznámenia DSA a komunikáciu od úradov v nasledujúcich jazykoch: angličtina, bulharčina, poľština. Pokiaľ to bude možné, odpovieme v jazyku vašej komunikácie.",
    },
    "sl": {
        "contact_dsa.s3_title": "Kako prijaviti nezakonito vsebino",
        "contact_dsa.s3_what_to_include_title": "Vaše obvestilo mora vsebovati:",
        "contact_dsa.s4_title": "Kaj se zgodi po prijavi",
        "contact_dsa.s5_title": "Podprti jeziki",
        "contact_dsa.back_to_home": "Nazaj na začetek",
        "contact_dsa.s3_body": "Če menite, da je vsebina na platformi Nevumo nezakonita v skladu s pravom EU ali nacionalnim pravom, pošljite obvestilo na legal@nevumo.com. Da bomo lahko vašo prijavo učinkovito obdelali, vas prosimo, da vključite naslednje podatke:",
        "contact_dsa.s3_what_to_include_body": "1. Opis vsebine, za katero menite, da je nezakonita, in njeno natančno lokacijo na platformi (URL ali opis).\n2. Pravni razlog, zakaj menite, da je vsebina nezakonita.\n3. Vaše ime in e-poštni naslov (razen za prijave, ki vključujejo gradivo o spolni zlorabi otrok).\n4. Izjavo, ki potrjuje, da so podatki v vašem obvestilu po vašem najboljšem vedenju točni in popolni.",
        "contact_dsa.s4_body": "Po prejemu vašega obvestila bomo:\n• Takoj poslali samodejno potrditev prejema.\n• Pravočasno, skrbno in nepristransko pregledali vašo prijavo.\n• Ukrepali v 72 urah v nujnih primerih (npr. vsebina, ki vključuje nasilje, varnost otrok ali neposredno škodo).\n• Ukrepali v 7 delovnih dneh pri standardnih prijavah.\n• Vas obvestili o naši odločitvi in razlogih zanjo.\n• Vas obvestili o vaši pravici do pritožbe na našo odločitev.",
        "contact_dsa.s5_body": "Nevumo sprejema obvestila DSA in komunikacijo organov v naslednjih jezikih: angleščina, bolgarščina, poljščina. Kjer bo to mogoče, bomo odgovorili v jeziku vaše komunikacije.",
    },
    "sq": {
        "contact_dsa.s3_title": "Si të raportoni përmbajtje ilegale",
        "contact_dsa.s3_what_to_include_title": "Njoftimi juaj duhet të përfshijë:",
        "contact_dsa.s4_title": "Çfarë ndodh pas raportimit",
        "contact_dsa.s5_title": "Gjuhët e mbështetura",
        "contact_dsa.back_to_home": "Kthehu në faqen kryesore",
        "contact_dsa.s3_body": "Nëse besoni se përmbajtja në Nevumo është ilegale sipas ligjit të BE-së ose ligjit kombëtar, ju lutemi dërgoni një njoftim në legal@nevumo.com. Për të na mundësuar të procesojmë raportin tuaj në mënyrë efektive, ju lutemi përfshini informacionin e mëposhtëm:",
        "contact_dsa.s3_what_to_include_body": "1. Një përshkrim i përmbajtjes që ju besoni se është e jashtëligjshme dhe vendndodhja e saktë e saj në platformë (URL ose përshkrim).\n2. Arsyeja ligjore pse besoni se përmbajtja është e jashtëligjshme.\n3. Emrin dhe adresën tuaj të email-it (përveç raporteve që përfshijnë materiale të abuzimit seksual të fëmijëve).\n4. Një deklaratë që konfirmon se informacioni në njoftimin tuaj është i saktë dhe i plotë me sa keni dijeni.",
        "contact_dsa.s4_body": "Pas marrjes së njoftimit tuaj, ne do të:\n• Dërgojmë një konfirmim automatik të marrjes menjëherë.\n• Shqyrtojmë raportin tuaj në një mënyrë në kohë, të zellshme dhe jo arbitrare.\n• Marrim masa brenda 72 orëve për rastet urgjente (p.sh. përmbajtje që përfshin dhunë, sigurinë e fëmijëve ose dëm të pashmangshëm).\n• Marrim masa brenda 7 ditëve të punës për raportet standarde.\n• Ju njoftojmë për vendimin tonë dhe arsyet e tij.\n• Ju informojmë për të drejtën tuaj për të apeluar vendimin tonë.",
        "contact_dsa.s5_body": "Nevumo pranon njoftimet e DSA-së dhe komunikimet e autoriteteve në gjuhët e mëposhtme: anglisht, bullgarisht, polonisht. Ne do t'ju përgjigjemi në gjuhën e komunikimit tuaj aty ku është e mundur.",
    },
    "sr": {
        "contact_dsa.s3_title": "Kako prijaviti nezakoniti sadržaj",
        "contact_dsa.s3_what_to_include_title": "Vaša prijava treba da sadrži:",
        "contact_dsa.s4_title": "Šta se dešava nakon prijave",
        "contact_dsa.s5_title": "Podržani jezici",
        "contact_dsa.back_to_home": "Nazad na početnu",
        "contact_dsa.s3_body": "Ako smatrate da je sadržaj na platformi Nevumo nezakonit prema pravu EU ili nacionalnom pravu, pošaljite prijavu na legal@nevumo.com. Da bismo mogli efikasno da obradimo vašu prijavu, molimo vas da uključite sledeće informacije:",
        "contact_dsa.s3_what_to_include_body": "1. Opis sadržaja za koji smatrate da je nezakonit i njegovu tačnu lokaciju na platformi (URL ili opis).\n2. Pravni razlog zašto smatrate da je sadržaj nezakonit.\n3. Vaše ime i e-mail adresu (osim za prijave koje se odnose na materijale dečjeg seksualnog zlostavljanja).\n4. Izjavu kojom potvrđujete da su informacije u vašoj prijavi tačne i potpune prema vašem najboljem saznanju.",
        "contact_dsa.s4_body": "Po prijemu vaše prijave, mi ćemo:\n• Odmah poslati automatsku potvrdu o prijemu.\n• Pregledati vašu prijavu blagovremeno, pažljivo i neproizvoljno.\n• Preduzeti mere u roku od 72 sata za hitne slučajeve (npr. sadržaj koji uključuje nasilje, bezbednost dece ili neposrednu štetu).\n• Preduzeti mere u roku od 7 radnih dana za standardne prijave.\n• Obavestiti vas o našoj odluci i razlozima za nju.\n• Obavestiti vas o vašem pravu na žalbu na našu odluku.",
        "contact_dsa.s5_body": "Nevumo prihvata DSA prijave i komunikaciju od organa vlasti na sledećim jezicima: engleski, bugarski, poljski. Odgovorićemo na jeziku vaše komunikacije gde god je to moguće.",
    },
    "sv": {
        "contact_dsa.s3_title": "Hur du anmäler olagligt innehåll",
        "contact_dsa.s3_what_to_include_title": "Din anmälan bör innehålla:",
        "contact_dsa.s4_title": "Vad händer efter att du rapporterar",
        "contact_dsa.s5_title": "Språk som stöds",
        "contact_dsa.back_to_home": "Tillbaka till startsidan",
        "contact_dsa.s3_body": "Om du anser att innehåll på Nevumo är olagligt enligt EU-lagstiftning eller nationell lagstiftning, vänligen skicka ett meddelande till legal@nevumo.com. För att vi ska kunna behandla din anmälan effektivt, vänligen inkludera följande information:",
        "contact_dsa.s3_what_to_include_body": "1. En beskrivning av det innehåll du anser vara olagligt och dess exakta plats på plattformen (URL eller beskrivning).\n2. Den juridiska anledningen till varför du anser att innehållet är olagligt.\n3. Ditt namn och e-postadress (utom för anmälningar som rör material med sexuella övergrepp mot barn).\n4. Ett uttalande som bekräftar att informationen i ditt meddelande är korrekt och fullständig enligt din bästa vetskap.",
        "contact_dsa.s4_body": "Vid mottagandet av ditt meddelande kommer vi att:\n• Skicka en automatisk mottagningsbekräftelse omedelbart.\n• Granska din anmälan på ett lägligt, noggrant och icke-godtyckligt sätt.\n• Vidta åtgärder inom 72 timmar för brådskande ärenden (t.ex. innehåll som rör våld, barns säkerhet eller överhängande skada).\n• Vidta åtgärder inom 7 arbetsdagar för standardanmälningar.\n• Meddela dig om vårt beslut och orsakerna till det.\n• Informera dig om din rätt att överklaga vårt beslut.",
        "contact_dsa.s5_body": "Nevumo accepterar DSA-meddelanden och myndighetskommunikation på följande språk: engelska, bulgariska, polska. Vi kommer att svara på språket i din kommunikation där det är möjligt.",
    },
    "tr": {
        "contact_dsa.s3_title": "Yasadışı İçerik Nasıl Bildirilir",
        "contact_dsa.s3_what_to_include_title": "Bildiriminiz şunları içermelidir:",
        "contact_dsa.s4_title": "Bildirimin Ardından Ne Olur",
        "contact_dsa.s5_title": "Desteklenen Diller",
        "contact_dsa.back_to_home": "Ana Sayfaya Dön",
        "contact_dsa.s3_body": "Nevumo'daki içeriğin AB veya ulusal yasalar uyarınca yasadışı olduğuna inanıyorsanız, lütfen legal@nevumo.com adresine bir bildirim gönderin. Raporunuzu etkili bir şekilde işleme koyabilmemiz için lütfen aşağıdaki bilgileri ekleyin:",
        "contact_dsa.s3_what_to_include_body": "1. Yasadışı olduğuna inandığınız içeriğin bir açıklaması ve platformdaki tam konumu (URL veya açıklama).\n2. İçeriğin yasadışı olduğuna inanmanızın hukuki nedeni.\n3. Adınız ve e-posta adresiniz (çocuk cinsel istismarı materyali içeren raporlar hariç).\n4. Bildiriminizdeki bilgilerin, bildiğiniz kadarıyla doğru ve eksiksiz olduğunu teyit eden bir beyan.",
        "contact_dsa.s4_body": "Bildiriminiz alındıktan sonra şunları yapacağız:\n• Derhal otomatik bir alındı onayı göndereceğiz.\n• Raporunuzu zamanında, özenli ve keyfi olmayan bir şekilde inceleyeceğiz.\n• Acil durumlar için (örneğin şiddet, çocuk güvenliği veya yakın zarar içeren içerik) 72 saat içinde işlem yapacağız.\n• Standart raporlar için 7 iş günü içinde işlem yapacağız.\n• Kararımızı ve nedenlerini size bildireceğiz.\n• Kararımıza itiraz etme hakkınız konusunda sizi bilgilendireceğiz.",
        "contact_dsa.s5_body": "Nevumo, aşağıdaki dillerde DSA bildirimlerini ve yetkili iletişimlerini kabul etmektedir: İngilizce, Bulgarca, Lehçe. Mümkün olduğunda iletişiminizin dilinde yanıt vereceğiz.",
    },
    "uk": {
        "contact_dsa.s3_title": "Як повідомити про незаконний вміст",
        "contact_dsa.s3_what_to_include_title": "Ваше повідомлення має містити:",
        "contact_dsa.s4_title": "Що відбувається після повідомлення",
        "contact_dsa.s5_title": "Підтримувані мови",
        "contact_dsa.back_to_home": "На головну",
        "contact_dsa.s3_body": "Якщо ви вважаєте, що вміст на Nevumo є незаконним відповідно до законодавства ЄС або національного законодавства, надішліть сповіщення на адресу legal@nevumo.com. Щоб ми могли ефективно обробити ваше повідомлення, будь ласка, додайте таку інформацію:",
        "contact_dsa.s3_what_to_include_body": "1. Опис вмісту, який ви вважаєте незаконним, і його точне місцезнаходження на платформі (URL або опис).\n2. Юридична причина, чому ви вважаєте вміст незаконним.\n3. Ваше ім'я та адреса електронної пошти (за винятком повідомлень, що стосуються матеріалів сексуального насильства над дітьми).\n4. Заява, що підтверджує, що інформація у вашому повідомленні є точною та повною, наскільки вам відомо.",
        "contact_dsa.s4_body": "Після отримання вашого повідомлення ми:\n• Негайно надішлемо автоматичне підтвердження отримання.\n• Розглянемо ваше повідомлення своєчасно, ретельно та небезпідставно.\n• Вживемо заходів протягом 72 годин для термінових випадків (наприклад, вміст, що стосується насильства, безпеки дітей або неминучої шкоди).\n• Вживемо заходів протягом 7 робочих днів для стандартних повідомлень.\n• Повідомимо вас про наше рішення та його причини.\n• Поінформуємо вас про ваше право оскаржити наше рішення.",
        "contact_dsa.s5_body": "Nevumo приймає повідомлення DSA та повідомлення від органів влади такими мовами: англійська, болгарська, польська. За можливості ми відповідатимемо мовою вашого звернення.",
    },
}

def run_seed():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("Error: DATABASE_URL not set")
        return

    # Create engine
    engine = create_engine(db_url)
    
    # Query to insert/update translation
    upsert_query = text("""
        INSERT INTO translations (lang, key, value)
        VALUES (:lang, :key, :value)
        ON CONFLICT (lang, key) 
        DO UPDATE SET value = EXCLUDED.value;
    """)
    
    total_processed = 0
    
    with engine.connect() as conn:
        for lang, trans_dict in TRANSLATIONS_BY_LANG.items():
            for key, value in trans_dict.items():
                conn.execute(
                    upsert_query,
                    {
                        "key": key,
                        "lang": lang,
                        "value": value
                    }
                )
                total_processed += 1
        
        conn.commit()
                
    print(f"✅ Successfully seeded {total_processed} translations for '{NAMESPACE}' namespace")

if __name__ == "__main__":
    run_seed()
