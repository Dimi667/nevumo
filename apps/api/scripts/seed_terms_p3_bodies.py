"""
seed_terms_p3_bodies.py  —  Nevumo | namespace: terms
Key: art3_body (34 езика)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_terms_p3_bodies
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
    "art3_body": {
        "en": (
            '3.1 To use the platform as a client, you must:\n'
            '• Be at least 18 years of age;\n'
            '• Provide accurate and complete registration information;\n'
            '• Have the legal capacity to enter into binding contracts.\n\n'
            '3.2 You are responsible for maintaining the confidentiality of your account '
            'credentials. You must notify Nevumo immediately at privacy@nevumo.com if you '
            'suspect unauthorised access to your account.\n\n'
            '3.3 One person may hold both a client and a provider role under the same account.\n\n'
            '3.4 Nevumo may suspend or terminate your account if you breach these Terms, '
            'provide false information, or if required by applicable law.'
        ),
        "pl": (
            '4.1 Korzystanie z pełnych funkcji platformy wymaga rejestracji i utworzenia konta. '
            'Konto może założyć wyłącznie osoba, która:\n'
            '• ukończyła 18 lat;\n'
            '• podała prawdziwe i kompletne dane rejestracyjne;\n'
            '• posiada zdolność do czynności prawnych.\n\n'
            '4.2 Klient jest zobowiązany do zachowania w poufności danych dostępowych do konta. '
            'W przypadku podejrzenia nieuprawnionego dostępu Klient zobowiązany jest '
            'niezwłocznie powiadomić Nevumo na adres privacy@nevumo.com.\n\n'
            '4.3 Jedna osoba może posiadać zarówno konto Klienta, jak i konto Usługodawcy '
            'w ramach tego samego konta głównego.\n\n'
            '4.4 Nevumo zastrzega sobie prawo do zawieszenia lub usunięcia konta Klienta '
            'w przypadku naruszenia niniejszego Regulaminu, podania nieprawdziwych danych '
            'lub gdy wymaga tego obowiązujące prawo.'
        ),
        "bg": (
            '3.1 За да използва платформата като Клиент, лицето трябва да:\n'
            '• е навършило 18 години;\n'
            '• е предоставило вярна и пълна информация при регистрация;\n'
            '• притежава правоспособност за сключване на договори.\n\n'
            '3.2 Клиентът е длъжен да пази в тайна данните за достъп до акаунта си и '
            'незабавно да уведоми Nevumo на privacy@nevumo.com при съмнение за '
            'неоторизиран достъп.\n\n'
            '3.3 Едно лице може да притежава едновременно акаунт на Клиент и акаунт на '
            'Доставчик в рамките на един общ акаунт.\n\n'
            '3.4 Nevumo може да спре или прекрати акаунта на Клиент при нарушение на '
            'настоящите ОУ, предоставяне на неверни данни или при изискване от '
            'приложимото законодателство.'
        ),
        "cs": (
            '3.1 Chcete-li platformu používat jako klient, musíte:\n'
            '• být alespoň 18 let;\n'
            '• poskytnout přesné a úplné registrační údaje;\n'
            '• být způsobilí uzavírat závazné smlouvy.\n\n'
            '3.2 Jste odpovědni za zachování důvěrnosti svých přihlašovacích údajů. '
            'Pokud máte podezření na neoprávněný přístup k vašemu účtu, musíte o tom '
            'neprodleně informovat Nevumo na adrese privacy@nevumo.com.\n\n'
            '3.3 Jedna osoba může mít zároveň roli klienta i poskytovatele v rámci '
            'stejného účtu.\n\n'
            '3.4 Nevumo může váš účet pozastavit nebo zrušit, pokud porušíte tyto '
            'podmínky, poskytnete nepravdivé informace nebo to bude vyžadovat platné '
            'právní předpisy.'
        ),
        "da": (
            '3.1 For at bruge platformen som klient skal du:\n'
            '• være mindst 18 år gammel;\n'
            '• give nøjagtige og fuldstændige registreringsoplysninger;\n'
            '• have den retslige kapacitet til at indgå bindende kontrakter.\n\n'
            '3.2 Du er ansvarlig for at opretholde fortroligheden af dine '
            'kontologinoplysninger. Du skal straks underrette Nevumo på '
            'privacy@nevumo.com, hvis du har mistanke om uautoriseret adgang til '
            'din konto.\n\n'
            '3.3 En person kan have både en klient- og en udbyderolle under den '
            'samme konto.\n\n'
            '3.4 Nevumo kan suspendere eller opsige din konto, hvis du overtræder '
            'disse vilkår, giver falske oplysninger, eller hvis det kræves af '
            'gældende lovgivning.'
        ),
        "de": (
            '3.1 Um die Plattform als Kunde zu nutzen, müssen Sie:\n'
            '• mindestens 18 Jahre alt sein;\n'
            '• genaue und vollständige Registrierungsdaten angeben;\n'
            '• die Rechtsfähigkeit zur Eingehung verbindlicher Verträge besitzen.\n\n'
            '3.2 Sie sind verantwortlich für die Vertraulichkeit Ihrer Zugangsdaten. '
            'Bei Verdacht auf unbefugten Zugriff auf Ihr Konto müssen Sie Nevumo '
            'unverzüglich unter privacy@nevumo.com benachrichtigen.\n\n'
            '3.3 Eine Person kann unter demselben Konto sowohl die Rolle eines Kunden '
            'als auch eines Anbieters innehaben.\n\n'
            '3.4 Nevumo kann Ihr Konto sperren oder kündigen, wenn Sie gegen diese '
            'Bedingungen verstoßen, falsche Angaben machen oder dies von geltendem '
            'Recht verlangt wird.'
        ),
        "el": (
            '3.1 Για να χρησιμοποιείτε την πλατφόρμα ως πελάτης, πρέπει:\n'
            '• να είστε τουλάχιστον 18 ετών;\n'
            '• να παρέχετε ακριβή και πλήρη στοιχεία εγγραφής;\n'
            '• να έχετε νομική ικανότητα σύναψης δεσμευτικών συμβάσεων.\n\n'
            '3.2 Είστε υπεύθυνοι για τη διαφύλαξη της εμπιστευτικότητας των '
            'διαπιστευτηρίων του λογαριασμού σας. Σε περίπτωση υποψίας μη '
            'εξουσιοδοτημένης πρόσβασης, πρέπει να ενημερώσετε άμεσα το Nevumo '
            'στη διεύθυνση privacy@nevumo.com.\n\n'
            '3.3 Ένα πρόσωπο μπορεί να έχει ταυτόχρονα ρόλο πελάτη και παρόχου '
            'υπηρεσιών στον ίδιο λογαριασμό.\n\n'
            '3.4 Το Nevumo μπορεί να αναστείλει ή να τερματίσει τον λογαριασμό σας '
            'εάν παραβιάσετε τους παρόντες Όρους, παράσχετε ψευδείς πληροφορίες ή '
            'εάν το απαιτεί η εφαρμοστέα νομοθεσία.'
        ),
        "es": (
            '3.1 Para utilizar la plataforma como cliente, debe:\n'
            '• tener al menos 18 años de edad;\n'
            '• proporcionar información de registro precisa y completa;\n'
            '• tener capacidad legal para suscribir contratos vinculantes.\n\n'
            '3.2 Es responsable de mantener la confidencialidad de sus credenciales de '
            'acceso. Debe notificar a Nevumo de inmediato en privacy@nevumo.com si '
            'sospecha de acceso no autorizado a su cuenta.\n\n'
            '3.3 Una misma persona puede ostentar tanto el rol de cliente como el de '
            'proveedor bajo la misma cuenta.\n\n'
            '3.4 Nevumo podrá suspender o cancelar su cuenta si incumple estos Términos, '
            'facilita información falsa o si así lo requiere la legislación aplicable.'
        ),
        "et": (
            '3.1 Platvormi kliendina kasutamiseks peate:\n'
            '• olema vähemalt 18-aastane;\n'
            '• esitama täpsed ja täielikud registreerimisandmed;\n'
            '• omama õiguslikku teovõimet siduvate lepingute sõlmimiseks.\n\n'
            '3.2 Te vastutate oma kontole juurdepääsu andmete konfidentsiaalsuse '
            'säilitamise eest. Peate viivitamata teavitama Nevumot aadressil '
            'privacy@nevumo.com, kui kahtlustate volitamata juurdepääsu oma kontole.\n\n'
            '3.3 Üks isik võib omada sama konto raames nii kliendi kui ka '
            'teenusepakkuja rolli.\n\n'
            '3.4 Nevumo võib teie konto peatada või lõpetada, kui rikute käesolevaid '
            'tingimusi, esitate valeandmeid või kui kohaldatav seadus seda nõuab.'
        ),
        "fi": (
            '3.1 Käyttääksesi alustaa asiakkaana sinun on:\n'
            '• oltava vähintään 18-vuotias;\n'
            '• annettava täsmälliset ja täydelliset rekisteröintitiedot;\n'
            '• omattava oikeustoimikelpoisuus sitovien sopimusten tekemiseen.\n\n'
            '3.2 Olet vastuussa tilisi tunnistetietojen luottamuksellisuuden '
            'säilyttämisestä. Sinun on välittömästi ilmoitettava Nevumolle osoitteessa '
            'privacy@nevumo.com, jos epäilet luvatonta pääsyä tilillesi.\n\n'
            '3.3 Yksi henkilö voi pitää sekä asiakas- että palveluntarjoajaroolia '
            'saman tilin alla.\n\n'
            '3.4 Nevumo voi keskeyttää tai irtisanoa tilisi, jos rikot näitä ehtoja, '
            'annat väärää tietoa tai jos sovellettava lainsäädäntö niin vaatii.'
        ),
        "fr": (
            '3.1 Pour utiliser la plateforme en tant que client, vous devez :\n'
            '• avoir au moins 18 ans ;\n'
            '• fournir des informations d\'inscription exactes et complètes ;\n'
            '• avoir la capacité juridique de conclure des contrats contraignants.\n\n'
            '3.2 Vous êtes responsable de la confidentialité de vos identifiants de '
            'connexion. Vous devez notifier immédiatement Nevumo à l\'adresse '
            'privacy@nevumo.com si vous soupçonnez un accès non autorisé à votre compte.\n\n'
            '3.3 Une même personne peut détenir à la fois le rôle de client et de '
            'prestataire sous le même compte.\n\n'
            '3.4 Nevumo peut suspendre ou résilier votre compte si vous enfreignez les '
            'présentes Conditions, fournissez de fausses informations, ou si la '
            'législation applicable l\'exige.'
        ),
        "ga": (
            '3.1 Chun an t-ardán a úsáid mar chliant, ní mór duit:\n'
            '• a bheith ar a laghad 18 mbliana d\'aois;\n'
            '• faisnéis chlárúcháin chruinn agus iomlán a sholáthar;\n'
            '• cumas dlíthiúil a bheith agat chun conarthaí ceangailteacha a dhéanamh.\n\n'
            '3.2 Tá tú freagrach as rúndacht d\'aithinte cuntais a chothabháil. Ní mór '
            'duit Nevumo a chur ar an eolas láithreach ag privacy@nevumo.com má bhíonn '
            'amhras ort faoi rochtain neamhúdaraithe ar do chuntas.\n\n'
            '3.3 Is féidir le duine amháin ról cliant agus ról soláthróra a bheith aige '
            'faoin gcuntas céanna.\n\n'
            '3.4 Féadfaidh Nevumo do chuntas a chur ar fionraí nó a fhoirceannadh má '
            'shároíonn tú na Téarmaí seo, má sholáthraíonn tú faisnéis bhréagach, nó '
            'má iarrann dlí infheidhmithe é.'
        ),
        "hr": (
            '3.1 Za korištenje platforme kao klijent morate:\n'
            '• imati najmanje 18 godina;\n'
            '• navesti točne i potpune registracijske podatke;\n'
            '• imati pravnu sposobnost za sklapanje obvezujućih ugovora.\n\n'
            '3.2 Odgovorni ste za čuvanje povjerljivosti podataka za pristup svom računu. '
            'Morate odmah obavijestiti Nevumo na privacy@nevumo.com ako posumnjate na '
            'neovlašteni pristup vašem računu.\n\n'
            '3.3 Jedna osoba može imati i ulogu klijenta i ulogu davatelja usluga pod '
            'istim računom.\n\n'
            '3.4 Nevumo može suspendirati ili ukinuti vaš račun ako prekršite ove Uvjete, '
            'date lažne podatke ili ako to zahtijeva primjenjivo pravo.'
        ),
        "hu": (
            '3.1 A platform ügyfélként való használatához:\n'
            '• legalább 18 évesnek kell lennie;\n'
            '• pontos és teljes regisztrációs adatokat kell megadnia;\n'
            '• rendelkeznie kell a kötelező erejű szerződések megkötéséhez szükséges '
            'jogi cselekvőképességgel.\n\n'
            '3.2 Ön felelős a fiókjához tartozó hozzáférési adatok bizalmas kezeléséért. '
            'Ha gyanítja, hogy illetéktelen hozzáférés történt a fiókjához, '
            'haladéktalanul értesítenie kell a Nevumot a privacy@nevumo.com '
            'e-mail-címen.\n\n'
            '3.3 Egy személy ugyanazon a fiókon belül egyszerre tölthet be ügyfél- és '
            'szolgáltatói szerepet.\n\n'
            '3.4 A Nevumo felfüggesztheti vagy törölheti fiókját, ha megsérti jelen '
            'feltételeket, hamis adatokat ad meg, vagy ha az alkalmazandó jogszabályok '
            'ezt megkövetelik.'
        ),
        "is": (
            '3.1 Til að nota vettvanginn sem viðskiptavinur verður þú:\n'
            '• að vera að minnsta kosti 18 ára;\n'
            '• að gefa upp nákvæmar og fullnægjandi skráningarupplýsingar;\n'
            '• að hafa lögræði til að gera bindandi samninga.\n\n'
            '3.2 Þú ert ábyrgur fyrir trúnaðarlegum meðferð innskráningargagna þinna. '
            'Þú verður tafarlaust að tilkynna Nevumo á privacy@nevumo.com ef þú grunar '
            'óleyfislegan aðgang að reikningi þínum.\n\n'
            '3.3 Ein manneskja getur haft bæði hlutverk viðskiptavinar og þjónustuaðila '
            'undir sama reikningi.\n\n'
            '3.4 Nevumo getur lagt bann við eða sagt upp reikningi þínum ef þú brýtur '
            'gegn þessum skilmálum, gefur upp rangar upplýsingar eða ef gildandi lög '
            'krefjast þess.'
        ),
        "it": (
            '3.1 Per utilizzare la piattaforma come cliente, è necessario:\n'
            '• avere almeno 18 anni;\n'
            '• fornire informazioni di registrazione accurate e complete;\n'
            '• avere la capacità giuridica di concludere contratti vincolanti.\n\n'
            '3.2 Lei è responsabile della riservatezza delle sue credenziali di accesso. '
            'Deve notificare immediatamente Nevumo all\'indirizzo privacy@nevumo.com in '
            'caso di sospetto accesso non autorizzato al suo account.\n\n'
            '3.3 Una stessa persona può ricoprire allo stesso tempo il ruolo di cliente '
            'e di prestatore di servizi nello stesso account.\n\n'
            '3.4 Nevumo può sospendere o chiudere il suo account in caso di violazione '
            'dei presenti Termini, di fornitura di informazioni false o se richiesto '
            'dalla normativa applicabile.'
        ),
        "lb": (
            '3.1 Fir d\'Plattform als Klient ze benotzen, musst Dir:\n'
            '• mindestens 18 Joer al sinn;\n'
            '• korrekt a vollstänneg Registratiounsinformatiounen uginn;\n'
            '• d\'Rechtsfäegkeet hunn fir verbindlech Kontrakter ofzeschléissen.\n\n'
            '3.2 Dir sidd responsabel fir d\'Geheimhaalung vun Ären Zougangsdate fir '
            'Äre Kont. Dir musst Nevumo direkt op privacy@nevumo.com informéieren, '
            'wann Dir e Virdacht op onbefugten Zougang zu Ärem Kont hutt.\n\n'
            '3.3 Eng Persoun kann ënner demselwechte Kont souwuel d\'Clientsrolle wéi '
            'och d\'Prestatairerolle hunn.\n\n'
            '3.4 Nevumo kann Äre Kont suspendinéieren oder ofschaffen, wann Dir géint '
            'dës Bedéngungen verstooss, falsch Angaben mécht oder wann dat vum '
            'gültege Recht gefuerdert gëtt.'
        ),
        "lt": (
            '3.1 Norint naudotis platforma kaip klientui, reikia:\n'
            '• būti bent 18 metų amžiaus;\n'
            '• pateikti tikslią ir išsamią registracijos informaciją;\n'
            '• turėti teisinį veiksnumą sudaryti privalomąsias sutartis.\n\n'
            '3.2 Jūs atsakote už savo paskyros prisijungimo duomenų konfidencialumą. '
            'Paaiškėjus neteisėtai prieigai prie jūsų paskyros, nedelsdami informuokite '
            'Nevumo adresu privacy@nevumo.com.\n\n'
            '3.3 Vienas asmuo toje pačioje paskyroje gali turėti tiek kliento, tiek '
            'paslaugų teikėjo vaidmenį.\n\n'
            '3.4 Nevumo gali sustabdyti arba panaikinti jūsų paskyrą, jei pažeisite '
            'šias sąlygas, pateiksite klaidingą informaciją arba jei to reikalauja '
            'taikytina teisė.'
        ),
        "lv": (
            '3.1 Lai izmantotu platformu kā klients, Jums jābūt:\n'
            '• vismaz 18 gadus vecam;\n'
            '• jāsniedz precīza un pilnīga reģistrācijas informācija;\n'
            '• juridiskai spējai noslēgt saistošus līgumus.\n\n'
            '3.2 Jūs atbildat par sava konta pieejas datu konfidencialitāti. Jums '
            'nekavējoties jāpaziņo Nevumo uz privacy@nevumo.com, ja esat aizdomīgi '
            'par nesankcionētu piekļuvi savam kontam.\n\n'
            '3.3 Viena persona var vienlaikus būt gan klients, gan pakalpojumu '
            'sniedzējs vienā kontā.\n\n'
            '3.4 Nevumo var apturēt vai dzēst jūsu kontu, ja pārkāpjat šos '
            'noteikumus, sniedzat nepatiesu informāciju vai ja to prasa '
            'piemērojamie tiesību akti.'
        ),
        "mk": (
            '3.1 За да ја користите платформата како клиент, мора да:\n'
            '• имате навршено 18 години;\n'
            '• дадете точни и потполни информации при регистрација;\n'
            '• поседувате правна способност за склучување обврзувачки договори.\n\n'
            '3.2 Одговорни сте за чување на доверливоста на вашите акредитиви за '
            'пристап. Мора веднаш да го известите Nevumo на privacy@nevumo.com ако '
            'посомневате неовластен пристап до вашиот акаунт.\n\n'
            '3.3 Едно лице може да ги задржи и улогата на клиент и улогата на давател '
            'на услуги под истиот акаунт.\n\n'
            '3.4 Nevumo може да го суспендира или откаже вашиот акаунт ако ги '
            'прекршите овие Услови, дадете лажни информации или ако тоа го бара '
            'применливото право.'
        ),
        "mt": (
            '3.1 Biex tuża l-pjattaforma bħala klijent, għandek:\n'
            '• ikollok mill-inqas 18-il sena;\n'
            '• tipprovdi informazzjoni ta\' reġistrazzjoni preċiża u sħiħa;\n'
            '• ikollok il-kapaċità legali biex tagħmel kuntratti vinkolanti.\n\n'
            '3.2 Inti responsabbli biex iżżomm il-kunfidenzjalità tal-kredenzjali tal-kont '
            'tiegħek. Inti għandek tinnotifika lil Nevumo immedjatament fuq '
            'privacy@nevumo.com jekk tissuspetta aċċess mhux awtorizzat.\n\n'
            '3.3 Persuna waħda tista\' żżomm kemm ir-rwol ta\' klijent kif ukoll tar-rwol '
            'ta\' fornitur taħt l-istess kont.\n\n'
            '3.4 Nevumo jista\' jissospendi jew itemm il-kont tiegħek jekk tikser dawn '
            'it-Termini, tipprovdi informazzjoni falza, jew jekk il-liġi applikabbli '
            'titlob hekk.'
        ),
        "nl": (
            '3.1 Om het platform als klant te gebruiken, moet u:\n'
            '• minimaal 18 jaar oud zijn;\n'
            '• nauwkeurige en volledige registratiegegevens verstrekken;\n'
            '• juridisch handelingsbekwaam zijn om bindende contracten te sluiten.\n\n'
            '3.2 U bent verantwoordelijk voor de geheimhouding van uw inloggegevens. '
            'U moet Nevumo onmiddellijk informeren via privacy@nevumo.com als u '
            'ongeautoriseerde toegang tot uw account vermoedt.\n\n'
            '3.3 Eén persoon kan zowel de rol van klant als van serviceprovider hebben '
            'onder hetzelfde account.\n\n'
            '3.4 Nevumo kan uw account opschorten of beëindigen als u deze Voorwaarden '
            'schendt, onjuiste informatie verstrekt, of als de geldende wetgeving '
            'dit vereist.'
        ),
        "no": (
            '3.1 For å bruke plattformen som kunde, må du:\n'
            '• være minst 18 år gammel;\n'
            '• oppgi nøyaktig og fullstendig registreringsinformasjon;\n'
            '• ha rettslig handleevne til å inngå bindende kontrakter.\n\n'
            '3.2 Du er ansvarlig for å opprettholde konfidensialiteten av '
            'kontopassordet ditt. Du må umiddelbart varsle Nevumo på '
            'privacy@nevumo.com hvis du mistenker uautorisert tilgang til kontoen.\n\n'
            '3.3 Én person kan ha både klientrollen og leverandørrollen under '
            'samme konto.\n\n'
            '3.4 Nevumo kan suspendere eller avslutte kontoen din dersom du bryter '
            'disse Vilkårene, gir falsk informasjon, eller hvis gjeldende lovgivning '
            'krever det.'
        ),
        "pt": (
            '3.1 Para utilizar a plataforma como cliente, você deve:\n'
            '• ter pelo menos 18 anos de idade;\n'
            '• fornecer informações de cadastro precisas e completas;\n'
            '• ter capacidade legal para celebrar contratos vinculantes.\n\n'
            '3.2 Você é responsável por manter a confidencialidade das suas credenciais '
            'de acesso. Deve notificar o Nevumo imediatamente pelo endereço '
            'privacy@nevumo.com caso suspeite de acesso não autorizado à sua conta.\n\n'
            '3.3 Uma mesma pessoa pode ter tanto o papel de cliente quanto o de '
            'prestador de serviços na mesma conta.\n\n'
            '3.4 O Nevumo poderá suspender ou encerrar a sua conta caso você viole '
            'estes Termos, forneça informações falsas, ou quando a legislação '
            'aplicável assim exigir.'
        ),
        "pt-PT": (
            '3.1 Para utilizar a plataforma como cliente, deve:\n'
            '• ter pelo menos 18 anos de idade;\n'
            '• fornecer informações de registo exactas e completas;\n'
            '• ter capacidade legal para celebrar contratos vinculativos.\n\n'
            '3.2 É responsável por manter a confidencialidade das suas credenciais de '
            'acesso. Deve notificar o Nevumo imediatamente através do endereço '
            'privacy@nevumo.com caso suspeite de acesso não autorizado à sua conta.\n\n'
            '3.3 Uma mesma pessoa pode ter simultaneamente o papel de cliente e o de '
            'prestador de serviços na mesma conta.\n\n'
            '3.4 O Nevumo pode suspender ou encerrar a sua conta caso viole estes '
            'Termos, forneça informações falsas, ou quando a legislação aplicável '
            'assim o exigir.'
        ),
        "ro": (
            '3.1 Pentru a utiliza platforma ca și client, trebuie:\n'
            '• să aveți cel puțin 18 ani;\n'
            '• să furnizați informații de înregistrare corecte și complete;\n'
            '• să aveți capacitate juridică de a încheia contracte obligatorii.\n\n'
            '3.2 Sunteți responsabil pentru menținerea confidențialității datelor de '
            'acces la contul dumneavoastră. Trebuie să notificați imediat Nevumo la '
            'adresa privacy@nevumo.com dacă suspectați un acces neautorizat.\n\n'
            '3.3 O singură persoană poate deține atât rolul de client, cât și cel de '
            'prestator de servicii în cadrul aceluiași cont.\n\n'
            '3.4 Nevumo poate suspenda sau închide contul dumneavoastră dacă încălcați '
            'acești Termeni, furnizați informații false sau dacă legislația aplicabilă '
            'impune acest lucru.'
        ),
        "ru": (
            '3.1 Для использования платформы в качестве клиента необходимо:\n'
            '• быть не моложе 18 лет;\n'
            '• предоставить точные и полные данные при регистрации;\n'
            '• обладать правоспособностью для заключения обязательных договоров.\n\n'
            '3.2 Вы несёте ответственность за конфиденциальность своих учётных данных. '
            'При подозрении на несанкционированный доступ к вашему аккаунту следует '
            'немедленно уведомить Nevumo по адресу privacy@nevumo.com.\n\n'
            '3.3 Одно лицо может одновременно выступать в роли клиента и исполнителя '
            'в рамках одного аккаунта.\n\n'
            '3.4 Nevumo вправе заблокировать или удалить ваш аккаунт в случае '
            'нарушения настоящих условий, предоставления ложных данных или требований '
            'применимого законодательства.'
        ),
        "sk": (
            '3.1 Na používanie platformy ako klient musíte:\n'
            '• mať aspoň 18 rokov;\n'
            '• poskytnúť presné a úplné registračné údaje;\n'
            '• mať právnu spôsobilosť uzavierať záväzné zmluvy.\n\n'
            '3.2 Zodpovedáte za zachovanie dôvernosti svojich prihlasovacích údajov. '
            'V prípade podozrenia z neoprávneného prístupu k vášmu účtu musíte okamžite '
            'informovať Nevumo na adrese privacy@nevumo.com.\n\n'
            '3.3 Jedna osoba môže mať zároveň rolu klienta aj poskytovateľa v rámci '
            'rovnakého účtu.\n\n'
            '3.4 Nevumo môže váš účet pozastaviť alebo zrušiť, ak porušíte tieto '
            'podmienky, poskytnete nepravdivé informácie alebo to bude vyžadovať '
            'platné právne predpisy.'
        ),
        "sl": (
            '3.1 Za uporabo platforme kot stranka morate:\n'
            '• biti stari vsaj 18 let;\n'
            '• navesti natančne in popolne podatke za registracijo;\n'
            '• imeti pravno sposobnost za sklepanje zavezujočih pogodb.\n\n'
            '3.2 Odgovorni ste za varovanje zaupnosti vaših prijavnih podatkov. Nevumo '
            'morate nemudoma obvestiti na privacy@nevumo.com, če sumite na '
            'nepooblaščen dostop do vašega računa.\n\n'
            '3.3 Ena oseba ima lahko v okviru istega računa tako vlogo stranke kot '
            'vlogo ponudnika storitev.\n\n'
            '3.4 Nevumo lahko vaš račun začasno prekine ali ukine, če kršite te '
            'Pogoje, posredujete napačne podatke ali če to zahteva veljavna zakonodaja.'
        ),
        "sq": (
            '3.1 Për të përdorur platformën si klient, duhet:\n'
            '• të keni të paktën 18 vjeç;\n'
            '• të jepni informacion të saktë dhe të plotë regjistrimor;\n'
            '• të keni kapacitet ligjor për të lidhur kontrata detyruese.\n\n'
            '3.2 Jeni përgjegjës për ruajtjen e konfidencialitetit të kredencialeve '
            'tuaja të llogarisë. Duhet të njoftoni menjëherë Nevumo në '
            'privacy@nevumo.com nëse dyshoni akses të paautorizuar në llogarinë tuaj.\n\n'
            '3.3 Një person mund të mbajë njëkohësisht rolin e klientit dhe të '
            'ofruesit të shërbimeve nën të njëjtën llogari.\n\n'
            '3.4 Nevumo mund të pezullojë ose mbyllë llogarinë tuaj nëse shkelni '
            'këto Terma, jepni informacion të rremë, ose nëse legjislacioni i '
            'zbatueshëm e kërkon.'
        ),
        "sr": (
            '3.1 Da biste koristili platformu kao klijent, morate:\n'
            '• imati najmanje 18 godina;\n'
            '• pružiti tačne i potpune podatke za registraciju;\n'
            '• imati pravnu sposobnost za zaključivanje obavezujućih ugovora.\n\n'
            '3.2 Odgovorni ste za čuvanje poverljivosti pristupnih podataka svog '
            'naloga. Morate odmah da obavestite Nevumo na privacy@nevumo.com ako '
            'posumnjate na neovlašćen pristup vašem nalogu.\n\n'
            '3.3 Jedna osoba može imati i ulogu klijenta i ulogu pružaoca usluga '
            'pod istim nalogom.\n\n'
            '3.4 Nevumo može suspendovati ili ukinuti vaš nalog ako prekršite ove '
            'Uslove, date lažne podatke ili ako to zahteva primenjivo pravo.'
        ),
        "sv": (
            '3.1 För att använda plattformen som kund måste du:\n'
            '• vara minst 18 år gammal;\n'
            '• tillhandahålla korrekta och fullständiga registreringsuppgifter;\n'
            '• ha den rättsliga kapaciteten att ingå bindande avtal.\n\n'
            '3.2 Du ansvarar för att hålla dina inloggningsuppgifter konfidentiella. '
            'Du måste omedelbart meddela Nevumo på privacy@nevumo.com om du '
            'misstänker obehörig åtkomst till ditt konto.\n\n'
            '3.3 En person kan inneha både kundroll och leverantörsroll under '
            'samma konto.\n\n'
            '3.4 Nevumo kan stänga av eller avsluta ditt konto om du bryter mot '
            'dessa Villkor, lämnar falska uppgifter, eller om gällande lagstiftning '
            'kräver det.'
        ),
        "tr": (
            '3.1 Platformu müşteri olarak kullanmak için:\n'
            '• en az 18 yaşında olmalısınız;\n'
            '• doğru ve eksiksiz kayıt bilgileri sağlamalısınız;\n'
            '• bağlayıcı sözleşmeler yapma konusunda hukuki ehliyete sahip '
            'olmalısınız.\n\n'
            '3.2 Hesap kimlik bilgilerinizin gizliliğini korumaktan sorumlusunuz. '
            'Hesabınıza yetkisiz erişim şüphesi duyduğunuzda, derhal '
            'privacy@nevumo.com adresinden Nevumo\'yu bilgilendirmelisiniz.\n\n'
            '3.3 Bir kişi aynı hesap altında hem müşteri hem de hizmet sağlayıcı '
            'rolüne sahip olabilir.\n\n'
            '3.4 Bu Koşulları ihlal etmeniz, yanlış bilgi vermeniz veya yürürlükteki '
            'mevzuatın gerektirmesi halinde Nevumo hesabınızı askıya alabilir ya da '
            'sonlandırabilir.'
        ),
        "uk": (
            '3.1 Для використання платформи як клієнт необхідно:\n'
            '• бути не молодше 18 років;\n'
            '• надати точну та повну реєстраційну інформацію;\n'
            '• мати правоздатність для укладення обов\'язкових договорів.\n\n'
            '3.2 Ви несете відповідальність за збереження конфіденційності ваших '
            'облікових даних. При підозрі на несанкціонований доступ до вашого '
            'облікового запису слід негайно повідомити Nevumo за адресою '
            'privacy@nevumo.com.\n\n'
            '3.3 Одна особа може одночасно мати роль клієнта та виконавця послуг '
            'в рамках одного облікового запису.\n\n'
            '3.4 Nevumo може призупинити або закрити ваш обліковий запис у разі '
            'порушення цих Умов, надання недостовірних даних або вимог '
            'застосовного законодавства.'
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
        print(f"✅ seed_terms_p3_bodies: {count} rows upserted ({NAMESPACE}, art3_body × 34 langs)")

    engine.dispose()


if __name__ == "__main__":
    seed()
