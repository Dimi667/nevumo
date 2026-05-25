"""
seed_provider_terms_p10_art3_body.py  —  Nevumo | namespace: provider_terms
Key: art3_body  (1 key x 34 langs = 34 rows)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_provider_terms_p10_art3_body
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
    "art3_body": {
        "en": (
            "3.1 Registration on the Platform as a Provider is open to:\n"
            "- Natural persons who are at least 18 years of age at the time of registration;\n"
            "- Legal entities acting through their duly authorised representatives.\n\n"
            "3.2 You must provide accurate, complete, and up-to-date information during registration. You are responsible for maintaining the accuracy of your data at all times.\n\n"
            "3.3 Each Provider may hold only one Provider account. Creating multiple accounts to circumvent restrictions or suspensions is prohibited.\n\n"
            "3.4 You are responsible for maintaining the confidentiality of your account credentials and for all activity occurring under your account.\n\n"
            "3.5 The same user account may be used in both Provider and Client roles simultaneously. Switching between roles does not require separate registration."
        ),
        "pl": (
            "3.1 Rejestracja na Platformie jako Dostawca jest dostępna dla:\n"
            "- osób fizycznych, które w chwili rejestracji ukończyły 18 lat;\n"
            "- podmiotów prawnych działających przez należycie umocowanych przedstawicieli.\n\n"
            "3.2 Podczas rejestracji Dostawca obowiązany jest podać prawdziwe, pełne i aktualne informacje. Dostawca ponosi odpowiedzialność za bieżące utrzymywanie aktualności swoich danych.\n\n"
            "3.3 Każdy Dostawca może posiadać wyłącznie jedno konto Dostawcy. Zakładanie wielu kont w celu obejścia ograniczeń lub zawieszeń jest zabronione.\n\n"
            "3.4 Dostawca odpowiada za zachowanie poufności danych logowania do swojego konta oraz za wszelkie działania podejmowane w ramach tego konta.\n\n"
            "3.5 To samo konto użytkownika może być używane jednocześnie w roli Dostawcy i Klienta. Zmiana roli nie wymaga odrębnej rejestracji."
        ),
        "bg": (
            "3.1 Регистрацията на Платформата като Доставчик е достъпна за:\n"
            "- физически лица, навършили 18 години към момента на регистрацията;\n"
            "- юридически лица, действащи чрез надлежно упълномощени представители.\n\n"
            "3.2 При регистрацията трябва да предоставите точна, пълна и актуална информация. Вие носите отговорност за поддържането на точността на данните си по всяко време.\n\n"
            "3.3 Всеки Доставчик може да притежава само един доставчически акаунт. Забранено е създаването на множество акаунти с цел заобикаляне на ограничения или спирания.\n\n"
            "3.4 Вие носите отговорност за запазването на поверителността на данните за достъп до акаунта си и за всички дейности, извършвани в него.\n\n"
            "3.5 Един и същ потребителски акаунт може да се използва едновременно в ролята на Доставчик и Клиент. Превключването между ролите не изисква отделна регистрация."
        ),
        "de": (
            "3.1 Die Registrierung auf der Plattform als Dienstleister steht offen für:\n"
            "- natürliche Personen, die zum Zeitpunkt der Registrierung mindestens 18 Jahre alt sind;\n"
            "- juristische Personen, die durch ihre ordnungsgemäß bevollmächtigten Vertreter handeln.\n\n"
            "3.2 Sie müssen bei der Registrierung genaue, vollständige und aktuelle Informationen angeben. Sie sind dafür verantwortlich, die Richtigkeit Ihrer Daten jederzeit zu gewährleisten.\n\n"
            "3.3 Jeder Dienstleister darf nur ein Dienstleisterkonto führen. Das Erstellen mehrerer Konten zur Umgehung von Einschränkungen oder Sperren ist verboten.\n\n"
            "3.4 Sie sind für die Vertraulichkeit Ihrer Anmeldedaten und alle unter Ihrem Konto stattfindenden Aktivitäten verantwortlich.\n\n"
            "3.5 Dasselbe Nutzerkonto kann gleichzeitig in der Rolle als Dienstleister und als Kunde verwendet werden. Ein Rollenwechsel erfordert keine separate Registrierung."
        ),
        "fr": (
            "3.1 L'inscription sur la Plateforme en tant que Prestataire est ouverte aux :\n"
            "- personnes physiques ayant au moins 18 ans au moment de l'inscription ;\n"
            "- personnes morales agissant par l'intermediaire de leurs representants dument autorises.\n\n"
            "3.2 Vous devez fournir des informations exactes, completes et a jour lors de l'inscription. Vous etes responsable du maintien de l'exactitude de vos donnees a tout moment.\n\n"
            "3.3 Chaque Prestataire ne peut detenir qu'un seul compte Prestataire. La creation de plusieurs comptes pour contourner des restrictions ou des suspensions est interdite.\n\n"
            "3.4 Vous etes responsable de la confidentialite de vos identifiants de connexion et de toutes les activites effectuees sous votre compte.\n\n"
            "3.5 Le meme compte utilisateur peut etre utilise a la fois dans les roles de Prestataire et de Client. Passer d'un role a l'autre ne necessite pas d'inscription separee."
        ),
        "es": (
            "3.1 El registro en la Plataforma como Proveedor esta abierto a:\n"
            "- personas fisicas que tengan al menos 18 anos en el momento del registro;\n"
            "- personas juridicas que actuen a traves de sus representantes debidamente autorizados.\n\n"
            "3.2 Debe proporcionar informacion precisa, completa y actualizada durante el registro. Usted es responsable de mantener la exactitud de sus datos en todo momento.\n\n"
            "3.3 Cada Proveedor solo puede tener una cuenta de Proveedor. Esta prohibido crear multiples cuentas para eludir restricciones o suspensiones.\n\n"
            "3.4 Usted es responsable de mantener la confidencialidad de sus credenciales de acceso y de todas las actividades realizadas en su cuenta.\n\n"
            "3.5 La misma cuenta de usuario puede usarse simultaneamente en los roles de Proveedor y Cliente. Cambiar entre roles no requiere un registro separado."
        ),
        "it": (
            "3.1 La registrazione sulla Piattaforma come Fornitore e aperta a:\n"
            "- persone fisiche di almeno 18 anni al momento della registrazione;\n"
            "- persone giuridiche che agiscono tramite i loro rappresentanti debitamente autorizzati.\n\n"
            "3.2 E necessario fornire informazioni accurate, complete e aggiornate durante la registrazione. Sei responsabile del mantenimento dell'accuratezza dei tuoi dati in ogni momento.\n\n"
            "3.3 Ogni Fornitore puo avere un solo account Fornitore. E vietato creare piu account per aggirare restrizioni o sospensioni.\n\n"
            "3.4 Sei responsabile del mantenimento della riservatezza delle credenziali del tuo account e di tutte le attivita svolte tramite il tuo account.\n\n"
            "3.5 Lo stesso account utente puo essere utilizzato contemporaneamente nei ruoli di Fornitore e Cliente. Il cambio di ruolo non richiede una registrazione separata."
        ),
        "nl": (
            "3.1 Registratie op het Platform als Dienstverlener staat open voor:\n"
            "- natuurlijke personen die op het moment van registratie minimaal 18 jaar oud zijn;\n"
            "- rechtspersonen die handelen via hun naar behoren gemachtigde vertegenwoordigers.\n\n"
            "3.2 U moet tijdens de registratie nauwkeurige, volledige en actuele informatie verstrekken. U bent verantwoordelijk voor het te allen tijde actueel houden van uw gegevens.\n\n"
            "3.3 Elke Dienstverlener mag slechts één Dienstverleneraccount hebben. Het aanmaken van meerdere accounts om beperkingen of schorsingen te omzeilen is verboden.\n\n"
            "3.4 U bent verantwoordelijk voor de vertrouwelijkheid van uw accountgegevens en voor alle activiteiten die onder uw account plaatsvinden.\n\n"
            "3.5 Hetzelfde gebruikersaccount kan tegelijkertijd worden gebruikt in de rollen van Dienstverlener en Klant. Wisselen tussen rollen vereist geen afzonderlijke registratie."
        ),
        "pt": (
            "3.1 O registo na Plataforma como Prestador esta aberto a:\n"
            "- pessoas singulares com pelo menos 18 anos de idade no momento do registo;\n"
            "- pessoas coletivas que atuem atraves dos seus representantes devidamente autorizados.\n\n"
            "3.2 Deve fornecer informacoes precisas, completas e atualizadas durante o registo. E responsavel por manter a exatidao dos seus dados em todo o momento.\n\n"
            "3.3 Cada Prestador so pode ter uma conta de Prestador. E proibido criar multiplas contas para contornar restricoes ou suspensoes.\n\n"
            "3.4 E responsavel por manter a confidencialidade das suas credenciais de conta e por todas as atividades realizadas na sua conta.\n\n"
            "3.5 A mesma conta de utilizador pode ser usada simultaneamente nos papeis de Prestador e Cliente. A mudanca entre papeis nao requer um registo separado."
        ),
        "pt-PT": (
            "3.1 O registo na Plataforma como Prestador esta aberto a:\n"
            "- pessoas singulares com pelo menos 18 anos de idade no momento do registo;\n"
            "- pessoas colectivas que actuem atraves dos seus representantes devidamente autorizados.\n\n"
            "3.2 Deve fornecer informacoes exactas, completas e actualizadas durante o registo. E responsavel por manter a exactidao dos seus dados em todo o momento.\n\n"
            "3.3 Cada Prestador so pode ter uma conta de Prestador. E proibido criar multiplas contas para contornar restricoes ou suspensoes.\n\n"
            "3.4 E responsavel por manter a confidencialidade das suas credenciais de conta e por todas as actividades realizadas na sua conta.\n\n"
            "3.5 A mesma conta de utilizador pode ser utilizada simultaneamente nos papeis de Prestador e Cliente. A mudanca entre papeis nao requer um registo separado."
        ),
        "ro": (
            "3.1 Inregistrarea pe Platforma ca Furnizor este deschisa pentru:\n"
            "- persoane fizice care au cel putin 18 ani la momentul inregistrarii;\n"
            "- persoane juridice care actioneaza prin reprezentantii lor autorizati in mod corespunzator.\n\n"
            "3.2 Trebuie sa furnizati informatii precise, complete si actualizate in timpul inregistrarii. Sunteti responsabil pentru mentinerea exactitatii datelor dvs. in orice moment.\n\n"
            "3.3 Fiecare Furnizor poate detine un singur cont de Furnizor. Crearea mai multor conturi pentru a eluda restrictii sau suspendari este interzisa.\n\n"
            "3.4 Sunteti responsabil pentru mentinerea confidentialitatii acreditivelor contului dvs. si pentru toate activitatile desfasurate in contul dvs.\n\n"
            "3.5 Acelasi cont de utilizator poate fi folosit simultan in rolurile de Furnizor si Client. Trecerea de la un rol la altul nu necesita o inregistrare separata."
        ),
        "ru": (
            "3.1 Registratsiya na Platforme v kachestve Postavshchika otkryta dlya:\n"
            "- fizicheskikh lits, dostigshikh vozrasta 18 let na moment registratsii;\n"
            "- yuridicheskikh lits, deystvuyushchikh cherez dolzhnым obrazom upolnomochennykh predstaviteley.\n\n"
            "3.2 Pri registratsii vy dolzhny predostavit tochnuyu, polnuyu i aktualnuyu informatsiyu. Vy nesete otvetstvennost za podderzhaniе aktualnosti vashikh dannykh v lyuboye vremya.\n\n"
            "3.3 Kazhdyy Postavshchik mozhet imet tolko odnu uchetnyyu zapis Postavshchika. Sozdaniye neskollkikh uchetynkh zapisey dlya obkhoda ogranicheniy ili blokirovok zapreshcheno.\n\n"
            "3.4 Vy nesete otvetstvennost za sokhraneniye konfidentsialnosti uchetynkh dannykh vashego akkaunta i za vsyu deyatelnost, osushchestvlyayemuyu pod vashim akkаuntom.\n\n"
            "3.5 Odin i tot zhe akkaunt polzovatelya mozhet ispolzovatsya odnovremenno v rolyakh Postavshchika i Klienta. Pereklyucheniye mezhdu rolyami ne trebuyet otdelnoy registratsii."
        ),
        "uk": (
            "3.1 Reyestratsiya na Platformi yak Postachalnyk vidkryta dlya:\n"
            "- fizychnykh osib, yaki dosyahly 18 rokiv na moment reyestratsiyi;\n"
            "- yurydychnykh osib, yaki diyut cherez nalezho upovnovazhenykh predstavnykiv.\n\n"
            "3.2 Pid chas reyestratsiyi neobkhidno nadaty tochnu, povnu ta aktualnu informatsiyu. Vy nesete vidpovidalnist za pidtrymannya tochnosti danykh u bud-yakyy chas.\n\n"
            "3.3 Kozhen Postachalnyk mozhe maty lyshe odyn oblikovyy zapis Postachalnika. Stvorennya kilkokh oblіkovykh zapysiv dlya obkhodu obmezhen abo blokyvan zaboroneno.\n\n"
            "3.4 Vy nesete vidpovidalnist za zberezhennya konfidentsiynosti oblikovykh danykh i za vsyu diyalnist, shcho zdiisnyyetsya pid vashym oblіkovym zapysom.\n\n"
            "3.5 Odyn i toy samyy oblikovyy zapis korystuvacha mozhe vykorystovuvatysya odnochasno v rolyakh Postachalnika i Kliyenta. Peremykannya mizh rolyamy ne vymagaye okremoi reyestratsiyi."
        ),
        "cs": (
            "3.1 Registrace na Platforme jako Poskytovatel je otevrena pro:\n"
            "- fyzicke osoby, ktere jsou v dobe registrace alespon 18 let;\n"
            "- pravnicke osoby jednajici prostrednictvim svych radne poverenykh zastupcu.\n\n"
            "3.2 Behem registrace musíte poskytnout presne, uplne a aktualni informace. Jste zodpovedni za zachovani presnosti svych udaju po celou dobu.\n\n"
            "3.3 Kazdy Poskytovatel muze mit pouze jeden ucet Poskytovatele. Vytvareni vice uctu s cilem obejit omezeni nebo pozastaveni je zakazano.\n\n"
            "3.4 Jste zodpovedni za zachovani duverne povahy svych prihlasovacich udaju a za vsechen provoz probihajici pod vasim uctem.\n\n"
            "3.5 Stejny uzivatelsky ucet lze pouzivat zaroven v rolích Poskytovatele i Klienta. Prepinani mezi rolemi nevyzaduje samostatnou registraci."
        ),
        "da": (
            "3.1 Registrering pa Platformen som Udbyder er aaben for:\n"
            "- fysiske personer, der er mindst 18 ar pa registreringstidspunktet;\n"
            "- juridiske personer, der handler ved deres behoerigt bemyndigede repraesentanter.\n\n"
            "3.2 Du skal angive noejagtige, komplette og opdaterede oplysninger under registreringen. Du er ansvarlig for at opretholde noejagtigheden af dine data til enhver tid.\n\n"
            "3.3 Hver Udbyder maa kun have en Udbyderkonti. Det er forbudt at oprette flere konti for at omgaa begraensninger eller suspensioner.\n\n"
            "3.4 Du er ansvarlig for at opretholde fortroligheden af dine kontooplysninger og for al aktivitet under din konto.\n\n"
            "3.5 Den samme brugerkonto kan bruges i baade Udbyder- og Kunderollen samtidigt. Skift mellem roller kraever ikke separat registrering."
        ),
        "sv": (
            "3.1 Registrering pa Plattformen som Leverantor ar oppen for:\n"
            "- fysiska personer som ar minst 18 ar gamla vid registreringstillfallet;\n"
            "- juridiska personer som agerar genom sina behorigen bemyndigade representanter.\n\n"
            "3.2 Du maste ange korrekt, fullstandig och aktuell information vid registreringen. Du ansvarar for att halla dina uppgifter korrekta vid alla tidpunkter.\n\n"
            "3.3 Varje Leverantor far bara ha ett Leveranторskonto. Det ar forbjudet att skapa flera konton for att kringgå begransningar eller avstandningar.\n\n"
            "3.4 Du ansvarar for att halla dina kontoinloggningsuppgifter konfidentiella och for all aktivitet som sker under ditt konto.\n\n"
            "3.5 Samma anvandarkonto kan anvandas i bade Leverantor- och Kundrollen samtidigt. Att byta roll kraver ingen separat registrering."
        ),
        "no": (
            "3.1 Registrering pa Plattformen som Leverandor er aapen for:\n"
            "- fysiske personer som er minst 18 ar pa registreringstidspunktet;\n"
            "- juridiske personer som handler gjennom sine behorig bemyndigede representanter.\n\n"
            "3.2 Du ma oppgi noeyaktige, fullstendige og oppdaterte opplysninger under registreringen. Du er ansvarlig for a opprettholde noeyaktigheten av dataene dine til enhver tid.\n\n"
            "3.3 Hver Leverandor kan bare ha en Leverandorkonto. Det er forbudt a opprette flere kontoer for a omga begrensninger eller suspensjoner.\n\n"
            "3.4 Du er ansvarlig for a opprettholde konfidensialiteten til kontolegitimasjonen din og for all aktivitet som foregaar under kontoen din.\n\n"
            "3.5 Den samme brukerkontoen kan brukes i bade Leverandor- og Kunderollen samtidig. Bytte mellom roller krever ikke separat registrering."
        ),
        "fi": (
            "3.1 Rekisteroityminen Alustalle Palveluntarjoajana on avoinna:\n"
            "- luonnollisille henkiloille, jotka ovat vahintaan 18-vuotiaita rekisteroitymishetkella;\n"
            "- oikeushenkiloille, jotka toimivat asianmukaisesti valtuutettujen edustajiensa kautta.\n\n"
            "3.2 Sinun on annettava tarkkoja, taydellisia ja ajantasaisia tietoja rekisteroitymisen aikana. Olet vastuussa tietojesi tarkkuuden yllapitamisesta jatkuvasti.\n\n"
            "3.3 Jokaisella Palveluntarjoajalla voi olla vain yksi Palveluntarjoajatili. Useiden tilien luominen rajoitusten tai keskeytysten kiertamiseksi on kielletty.\n\n"
            "3.4 Olet vastuussa tilisi kirjautumistietojen luottamuksellisuuden yllapitamisesta ja kaikesta tilisi alla tapahtuvasta toiminnasta.\n\n"
            "3.5 Samaa kayttajatilia voidaan kayttaa samanaikaisesti seka Palveluntarjoajan etta Asiakkaan rooleissa. Roolin vaihtaminen ei vaadi erillistа rekisteroitymista."
        ),
        "et": (
            "3.1 Platvormil Teenusepakkujana registreerimine on avatud:\n"
            "- fuusilisele isikutele, kes on registreerimise hetkel vahemalt 18-aastased;\n"
            "- juriidilistele isikutele, kes tegutsevad oma nouetekohaselt volitatud esindajate kaudu.\n\n"
            "3.2 Peate registreerimisel esitama tapsed, taiеlikud ja ajakohased andmed. Vastutate oma andmete tapsuse sаilitamise eest kogu aeg.\n\n"
            "3.3 Igal Teenusepakkujal vib olla ainult uks Teenusepakkuja konto. Mitme konto loomine piirangute или peatamiste vältimiseks on keelatud.\n\n"
            "3.4 Vastutate oma konto sisselogimisandmete konfidentsiaalsuse hoidmise ja kogu konto all toimuva tegevuse eest.\n\n"
            "3.5 Sama kasutajakontot saab kasutada samaaegselt nii Teenusepakkuja kui ka Kliendi rollis. Rollide vahetamine ei nouda eraldi registreerimist."
        ),
        "lt": (
            "3.1 Registracija Platformoje kaip Teikejas yra atvira:\n"
            "- fiziniams asmenims, kuriems registracijos metu yra sueje ne maziau kaip 18 metu;\n"
            "- juridiniams asmenims, veikiantiems per savo tinkamai igaliotus atstovus.\n\n"
            "3.2 Registracijos metu turite pateikti tikslius, isamius ir atnaujintus duomenis. Esate atsakingi uz savo duomenu tikslumo palaikymą visą laiką.\n\n"
            "3.3 Kiekvienas Teikejas gali tureti tik viena Teikejo paskyra. Draudziama kurti kelias paskyras siekiant apeiti apribojimus arba sustabdymus.\n\n"
            "3.4 Esate atsakingi uz paskyros prisijungimo duomenu konfidencialumo palaikymą ir uz visą veiklą, vykdomą per jusu paskyra.\n\n"
            "3.5 Ta pati naudotojo paskyra gali buti naudojama tuo pat metu Teikejo ir Kliento vaidmenyse. Persijungimas tarp vaidmenu nereikalauja atskiros registracijos."
        ),
        "lv": (
            "3.1 Registracija Platforma ka Sniedzejam ir pieejama:\n"
            "- fiziskam personam, kuras registracijas bridi ir vismaz 18 gadus vecas;\n"
            "- juridiskam personam, kuras darbojas caur saviem pilnvarotajiem parstavjiem.\n\n"
            "3.2 Registracijas laika jums jаsniedz precizi, pilnigi un aktuali dati. Jus atbildat par savu datu precizitates uztureshanu visu laiku.\n\n"
            "3.3 Katram Sniedzejam drīkst but tikai viens Sniedzeja konts. Vairaku kontu izveide, lai apietu ierobezojumus vai aptureshanas, ir aizliegta.\n\n"
            "3.4 Jus atbildat par sava konta pieteikshanas akreditivu konfidencialitates saglabashanu un par visu darbību, kas notiek jusu konta.\n\n"
            "3.5 Vienu un to pashu lietotaja kontu var izmantot vienlaicigi gan Sniedzeja, gan Klienta lomas. Lomu mainishana neprasa atsevishu registraciju."
        ),
        "hu": (
            "3.1 A Platformon Szolgaltatokent torteno regisztracio a kovetkezokre nyitott:\n"
            "- 18. elettevet betoltott termeszetes szemelyekre;\n"
            "- jogszeruen meghatalmazott kepviselőikon keresztul eljaro jogi szemelyekre.\n\n"
            "3.2 A regisztracio soran pontos, teljes es naprakesz informaciokat kell megadnia. On felelos adatainak pontossaganak folyamatos fenntartasaert.\n\n"
            "3.3 Minden Szolgaltato csak egy Szolgaltatoi fiokot tarthat. Tilos tobb fiok letrehozasa a korlatozasok vagy felfüggesztesek megkerülése celjabol.\n\n"
            "3.4 On felelos a fiokja bejelentkezesi adatainak titkossagaert es a fiokja alatt vegzett osszes tevekenysegert.\n\n"
            "3.5 Ugyanaz a felhasznaloi fiok egyszerre hasznalhato Szolgaltato es Ugyfel szerepkoreben. A szerepkorok kozott valtashoz nem szükseges kulön regisztracio."
        ),
        "hr": (
            "3.1 Registracija na Platformi kao Pruzatelj otvorena je za:\n"
            "- fizicke osobe koje u trenutku registracije imaju najmanje 18 godina;\n"
            "- pravne osobe koje djeluju putem svojih uredno ovlastenih zastupnika.\n\n"
            "3.2 Morate navesti tocne, potpune i azurne informacije pri registraciji. Odgovorni ste za odrzavanje tocnosti svojih podataka u svakom trenutku.\n\n"
            "3.3 Svaki Pruzatelj moze imati samo jedan racun Pruzatelja. Zabranjena je izrada vishe racuna radi zaobilazenja ogranicenja ili suspenzija.\n\n"
            "3.4 Odgovorni ste za cuvanje povjerljivosti vjerodajnica vasheg racuna i za sve aktivnosti koje se odvijaju pod vasim racunom.\n\n"
            "3.5 Isti korisnicki racun moze se koristiti istovremeno u ulogama Pruzatelja i Klijenta. Prelazak izmedju uloga ne zahtijeva zasebnu registraciju."
        ),
        "sk": (
            "3.1 Registracia na Platforme ako Poskytovatel je otvorena pre:\n"
            "- fyzicke osoby, ktore su v case registracie vo veku aspon 18 rokov;\n"
            "- pravnicke osoby konajuce prostredníctvom svojich radne poverenych zastüpcov.\n\n"
            "3.2 Pocas registracie musíte poskytnút presne, uplne a aktualne informacie. Ste zodpovedni za udrzanie spravnosti vasich udajov po celü dobu.\n\n"
            "3.3 Kazdy Poskytovatel moze mat iba jeden ucet Poskytovatela. Vytvaranie viacerych uctov s cielom obist obmedzenia alebo pozastavenia je zakazane.\n\n"
            "3.4 Ste zodpovedni za zachovanie doverne povahy prihlasovacich udajov vasho uctu a za vsetku cinnost prebiegajucu pod vasim uctom.\n\n"
            "3.5 Rovnaky pouzivatelsky uцet mozno pouzivat zaroven v roliach Poskytovatela aj Zakaznika. Prepinanie medzi rolami nevyzaduje samostatnu registraciu."
        ),
        "sl": (
            "3.1 Registracija na Platformi kot Ponudnik je odprta za:\n"
            "- fizicne osebe, ki so ob registraciji stare vsaj 18 let;\n"
            "- pravne osebe, ki delujejo prek svojih ustrezno pooblascenih predstavnikov.\n\n"
            "3.2 Med registracijo morate navesti tocne, popolne in posodobljene podatke. Odgovorni ste za ohranjanje tocnosti svojih podatkov ves cas.\n\n"
            "3.3 Vsak Ponudnik ima lahko samo en racun Ponudnika. Ustvarjanje vec racunov za obhod omejitev ali blokad je prepovedano.\n\n"
            "3.4 Odgovorni ste za varovanje zaupnosti poverilnic racuna in za vse dejavnosti, ki potekajo pod vasim racunom.\n\n"
            "3.5 Isti uporabniski racun se lahko hkrati uporablja v vlogah Ponudnika in Stranke. Preklop med vlogami ne zahteva locene registracije."
        ),
        "el": (
            "3.1 I eggrafi stin Platforma os Párochos einai anoichti gia:\n"
            "- fysika prosopa pou einai touláchiston 18 eton kata tin eggrafí;\n"
            "- nomika prosopa pou energoun meso ton nomimon ekprosopon tous.\n\n"
            "3.2 Prepei na parechete akriveis, pliries kai enimerwmenes plirofories kata tin eggrafí. Eiste ypéfthynos gia tin diatirísi tis akribeias ton dedomenon sas se kathe stigmí.\n\n"
            "3.3 Kathe Párochos mporei na echei mono ena logo Paróchou. Apagorévontai i dimiourgia perissoteron logariasmón gia tin parákaampsi periorismón i anastolón.\n\n"
            "3.4 Eiste ypéfthynos gia ti diatirísi tis empisteytikotitas ton stóichion prósvasís sas kai gia oles tis drastiriotites pou ginontai ypo ton logariasmó sas.\n\n"
            "3.5 O idios logariasmós chrísti mporei na chrisimopoiíthei tautóchronos sti rolo Paróchou kai Peláti. I epallagi metaxý rólón den apaitei xechiristí eggrafí."
        ),
        "tr": (
            "3.1 Platformda Saglayici olarak kayit asagidakilere aciktir:\n"
            "- kayit sirasinda en az 18 yasinda olan gercek kisiler;\n"
            "- usulune uygun sekilde yetkilendirilmis temsilcileri araciligiyla hareket eden tuzel kisiler.\n\n"
            "3.2 Kayit sirasinda dogru, eksiksiz ve guncel bilgi saglamalisiniz. Verilerinizin her zaman dogru kalmasini saglamaktan siz sorumlusunuz.\n\n"
            "3.3 Her Saglayici yalnizca bir Saglayici hesabina sahip olabilir. Kisitlamalari veya askiya almalari asip gecmek icin birden fazla hesap olusturmak yasaktir.\n\n"
            "3.4 Hesap bilgilerinizin gizliligini korumaktan ve hesabiniz altinda gerceklesen tum etkinliklerden siz sorumlusunuz.\n\n"
            "3.5 Ayni kullanici hesabi hem Saglayici hem de Musteri rollerinde ayni anda kullanilabilir. Roller arasinda gecis yapmak ayri bir kayit gerektirmez."
        ),
        "ga": (
            "3.1 Ta claru ar an Ardan mar Sholathroir oscailte do:\n"
            "- daoine nadurtha ata ar a laghad 18 mbliana d'aois ag am an chlaraithe;\n"
            "- eintitis dhlithiula a ghniomhaionn tri na n-ionadaithe ceart-udaraithe.\n\n"
            "3.2 Ni mor duit faisneis chruinn, iomlan agus naprakesh a sholáthar le linn an chlaraithe. Ta tu freagrach as cruinneas do chuid sonraí a choinneail i gcónaí.\n\n"
            "3.3 Ni chead ach cunntas amhain Solathraio a bheith ag gach Solathroir. Tá cosc ar chunntais iolra a chruthu chun srianta no fionraithe a sheachaint.\n\n"
            "3.4 Ta tu freagrach as rúndacht do dhintiure cuntais a choinneail agus as gach gniomhaiocht a tharlaionn faoi do chuntas.\n\n"
            "3.5 Is feidir an cunntas usaideora ceanna a usaid i roil an tSolathraio agus an Chustoimeara ag an am ceanna. Ni gа clarú ar leith chun athrú idir rólanna."
        ),
        "is": (
            "3.1 Skraning a Vettvangi sem Veituadili er opin fyrir:\n"
            "- einstaklinga sem eru minnst 18 ara a skrningartima;\n\n"
            "- logadila sem starfa í gegnum umbodsmann sinn.\n\n"
            "3.2 Thú verður að veita nakvaemar, fullnaðarlegar og uppfaerðar upplysingar við skráningu. Þú berð ábyrgð á því að halda gögnum þínum nákvæmum á hverjum tíma.\n\n"
            "3.3 Hvert Veituadili ma aðeins hafa einn Veituaðila reikning. Bannað er að búa til marga reikninga til að komast hjá takmörkunum eða frestun.\n\n"
            "3.4 Þú berð ábyrgð á því að halda leyndarmáli innskráningarskilríkja þinna og öllum starfsemi sem fer fram undir reikningnum þínum.\n\n"
            "3.5 Sami notendareikningur má nota í hlutverki bæði Veituaðila og Viðskiptavinar á sama tíma. Skipti á milli hlutverka krefst ekki sérstakrar skráningar."
        ),
        "lb": (
            "3.1 D'Registréierung op der Plattform als Presser ass oppen fir:\n"
            "- natierleche Persounen, déi zum Zeitpunkt vun der Registréierung mindestens 18 Joer al sinn;\n"
            "- Gesellschaften, déi duerch hir ordentlech bevollmächtigte Vertreter handelen.\n\n"
            "3.2 Dir musst bei der Registréierung accurate, vollstänneg an aktuell Informatiounen ubidden. Dir sidd verantwortlech fir d'Richtegkeet vun Äre Daten zu all Moment ze erhalen.\n\n"
            "3.3 Jide Presser darf nëmmen een Presser-Kont hunn. Et ass verbueden, méi Konten ze erstellen fir Aschränkungen oder Suspendéierungen ze ëmgoen.\n\n"
            "3.4 Dir sidd verantwortlech fir d'Vertraulechkeet vun Äre Kontodaten an fir all Aktivitéit, déi ënner Ärem Kont stattfënnt.\n\n"
            "3.5 Dee selwechte Benotzerkont kann gläichzäiteg a béide Rollen als Presser a Client benotzt ginn. D'Wiesselen tëschent Rollen erfuerdert keng separat Registréierung."
        ),
        "mk": (
            "3.1 Registracijata na Platformata kako Davac e otvorena za:\n"
            "- fizicki lica koi imaat najmalku 18 godini vo momentot na registracijata;\n"
            "- pravni lica koi dejstvuvaat preku nivnite ovlasteni zastapnici.\n\n"
            "3.2 Morate da navedete tocni, celосни i azurni informacii pri registracijata. Ste odgovorni za odrzuvanje na tocnosta na vasите podatoci vo sekoe vreme.\n\n"
            "3.3 Sekoj Davac moze da ima samo edna smetka na Davac. Zabraneto e kreiranje na poveke smetki so cel zaobikaluvanje na ogranicuvanjata ili suspenzii.\n\n"
            "3.4 Ste odgovorni za zachuvuvanjeto na doverlivos ta na podatocite za pristap kon vasata smetka i za site aktivnosti koi se odvivaat pod vasata smetka.\n\n"
            "3.5 Istata korisnichka smetka moze da se koristi istovremeno vo ulogite na Davac i Klient. Prelostot megu ulogite ne baraat oddelna registracija."
        ),
        "mt": (
            "3.1 Ir-registrazzjoni fuq il-Pjattaforma bhala Fornitur hija miftuha ghal:\n"
            "- persuni fiżici li ghandhom mill-inqas 18-il sena fil-hin tar-registrazzjoni;\n"
            "- entitajiet legali li jaghmel il-haga taghhom permezz tar-rappreżentanti debitament awtorizzati taghhom.\n\n"
            "3.2 Trid tipprovdi informazzjonit precizа, sħiħa u aggornatа waqt ir-registrazzjonі. Inti responsabbli biex żżomm l-accuratezza tad-data tiegħek fil-ħin kollu.\n\n"
            "3.3 Kull Fornitur jista' jkollu biss kont wieħed ta' Fornitur. Huwa projbit li tinħoloq aktar minn kont wieħed biex jiġu evitati restrizzjoniet jew sospensjonijiet.\n\n"
            "3.4 Inti responsabbli biex żżomm il-konfidenzjalita' tal-kredenzjali tal-kont tiegħek u ghal kull attivita li tseħħ taħt il-kont tiegħek.\n\n"
            "3.5 L-istess kont ta' utent jista' jintuza fl-irwol ta' Fornitur u Klijent fl-istess ħin. Il-bdil bejn l-irwol ma jeħtieġx registrazzjonі separata."
        ),
        "sq": (
            "3.1 Regjistrimi ne Platform si Ofrues eshte i hapur per:\n"
            "- personat fizike qe jane te pakten 18 vjecçare ne momentin e regjistrimit;\n"
            "- personat juridike qe veprojne nepermjet perfaqesuesve te tyre te autorizuar sic duhet.\n\n"
            "3.2 Duhet te jepni informacion te sakte, te plote dhe te perditesuar gjate regjistrimit. Jeni pergjegjes per ruajtjen e saktesise se te dhenave tuaja ne cdo kohe.\n\n"
            "3.3 Cdo Ofrues mund te kete vetem nje llogari Ofruesi. Krijimi i llogarive te shumta per te anashkaluar kufizimet ose pezullimet eshte i ndaluar.\n\n"
            "3.4 Jeni pergjegjes per ruajtjen e konfidencialitetit te kredencialeve te llogarise suaj dhe per te gjitha aktivitetet qe ndodhin nen llogarinë tuaj.\n\n"
            "3.5 I njejti llogari perdoruesi mund te perdoret njekohesisht ne rolet e Ofruesit dhe Klientit. Kalimi ndermjet roleve nuk kerkon regjistrim te veçante."
        ),
        "sr": (
            "3.1 Registracija na Platformi kao Pruzalac je otvorena za:\n"
            "- fizicka lica koja imaju najmanje 18 godina u trenutku registracije;\n"
            "- pravna lica koja deluju putem svojih uredno ovlascenih zastupnika.\n\n"
            "3.2 Morate navesti tacne, potpune i azurne informacije tokom registracije. Odgovorni ste za odrzavanje tacnosti svojih podataka u svakom trenutku.\n\n"
            "3.3 Svaki Pruzalac moze imati samo jedan nalog Pruzaoca. Zabranjeno je kreiranje vise naloga radi zaobilazenja ogranicenja ili suspenzija.\n\n"
            "3.4 Odgovorni ste za cuvanje poverljivosti akreditivavaseg naloga i za sve aktivnosti koje se odvijaju pod vasim nalogom.\n\n"
            "3.5 Isti korisnicki nalog se moze koristiti istovremeno u ulogama Pruzaoca i Klijenta. Prelaz izmedju uloga ne zahteva odvojenu registraciju."
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
            f"✅ seed_provider_terms_p10_art3_body: {count} rows upserted "
            f"({NAMESPACE}: art3_body x 34 langs)"
        )

    engine.dispose()


if __name__ == "__main__":
    seed()
