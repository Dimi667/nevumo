"""
seed_provider_terms_p16_art9_body.py  —  Nevumo | namespace: provider_terms
Key: art9_body  (1 key x 34 langs = 34 rows)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_provider_terms_p16_art9_body
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
    "art9_body": {
        "en": (
            "9.1 Nevumo is required under applicable law (Digital Services Act, P2B Regulation, and consumer protection law) to verify whether Providers act as traders (businesses) or as private individuals offering occasional services.\n\n"
            "9.2 During registration (or upon request), you must truthfully declare:\n"
            "- whether you are acting as a trader (conducting economic activity) or as a private individual;\n"
            "- if acting as a trader: your business name, tax identification number (NIP/REGON for Poland; VAT number or equivalent for other countries), and country of registration;\n"
            "- whether the services you offer require a professional licence or permit, and if so, confirm that you hold the necessary authorisation.\n\n"
            "9.3 Providers acting as traders in Poland must provide their NIP (tax identification number) and, if applicable, REGON (statistical number).\n\n"
            "9.4 Your trader/non-trader status will be displayed on your public Profile, in accordance with the Omnibus Directive requirements, enabling Clients to know with whom they are contracting.\n\n"
            "9.5 Providing false information in the trader declaration constitutes a material breach of these Provider Terms and may result in immediate account suspension."
        ),
        "bg": (
            "1. Nevumo е задължено съгласно приложимото законодателство (Акт за цифровите услуги, Регламент P2B и законодателство за защита на потребителите) да верифицира дали Доставчиците действат като търговци (стопански субекти) или като физически лица, предлагащи услуги по случаен повод.\n\n"
            "2. При регистрацията (или при поискване) Доставчикът е длъжен да декларира вярно:\n"
            "- дали действа като търговец (извършва стопанска дейност) или като физическо лице;\n"
            "- ако действа като търговец: наименованието на фирмата, данъчния идентификационен номер (NIP/REGON за Полша; ДДС номер или еквивалент за останалите страни) и страната на регистрация;\n"
            "- дали предлаганите услуги изискват професионален лиценз или разрешително и — ако е така — да потвърди, че притежава необходимото разрешение.\n\n"
            "3. Доставчиците, действащи като търговци в Полша, са длъжни да предоставят своя NIP (данъчен идентификационен номер) и — ако е приложимо — REGON (статистически номер).\n\n"
            "4. Статусът на Доставчика като търговец или нетърговец ще бъде видим на неговия публичен Профил в съответствие с изискванията на Директивата Omnibus, давайки възможност на Клиентите да познават субекта, с когото сключват договор.\n\n"
            "5. Предоставянето на неверни данни в декларацията за статус на търговец представлява съществено нарушение на Условията за Доставчици и може да доведе до незабавно спиране на акаунта."
        ),
        "pl": (
            "1. Nevumo jest zobowiązane na podstawie obowiązujących przepisów prawa (Akt o Usługach Cyfrowych, Rozporządzenie P2B, przepisy o ochronie konsumentów) do weryfikacji, czy Dostawcy działają jako przedsiębiorcy czy jako osoby prywatne oferujące usługi sporadycznie.\n\n"
            "2. Podczas rejestracji (lub na żądanie) Dostawca zobowiązany jest zgodnie z prawdą oświadczyć:\n"
            "- czy działa jako przedsiębiorca (prowadzi działalność gospodarczą) czy jako osoba prywatna;\n"
            "- jeżeli działa jako przedsiębiorca: nazwę firmy, numer identyfikacji podatkowej (NIP dla Polski; numer VAT lub odpowiednik dla innych krajów) oraz kraj rejestracji;\n"
            "- czy oferowane usługi wymagają licencji zawodowej lub zezwolenia oraz — jeżeli tak — czy taką licencją lub zezwoleniem dysponuje.\n\n"
            "3. Dostawcy działający jako przedsiębiorcy w Polsce obowiązani są podać swój NIP (numer identyfikacji podatkowej) oraz — jeżeli dotyczy — REGON (numer statystyczny).\n\n"
            "4. Status Dostawcy jako przedsiębiorcy lub osoby niebędącej przedsiębiorcą będzie widoczny na jego publicznym Profilu, zgodnie z wymogami Dyrektywy Omnibus, umożliwiając Klientom poznanie charakteru podmiotu, z którym zawierają umowę.\n\n"
            "5. Podanie nieprawdziwych informacji w oświadczeniu o statusie przedsiębiorcy stanowi istotne naruszenie niniejszego Regulaminu Dostawców i może skutkować natychmiastowym zawieszeniem konta."
        ),
        "de": (
            "9.1 Nevumo ist nach geltendem Recht (Gesetz über digitale Dienste, P2B-Verordnung und Verbraucherschutzrecht) verpflichtet zu überprüfen, ob Anbieter als Händler (Unternehmen) oder als Privatpersonen handeln, die gelegentliche Dienstleistungen anbieten.\n\n"
            "9.2 Bei der Registrierung (oder auf Anfrage) müssen Sie wahrheitsgemäß angeben:\n"
            "- ob Sie als Händler (Ausübung einer Wirtschaftstätigkeit) oder als Privatperson handeln;\n"
            "- falls Sie als Händler handeln: Ihren Firmennamen, Ihre Steueridentifikationsnummer (NIP/REGON für Polen; USt-IdNr. oder Äquivalent für andere Länder) und das Land der Registrierung;\n"
            "- ob die von Ihnen angebotenen Dienstleistungen eine Berufslizenz oder -genehmigung erfordern, und falls ja, bestätigen, dass Sie über die erforderliche Berechtigung verfügen.\n\n"
            "9.3 Anbieter, die als Händler in Polen tätig sind, müssen ihre NIP (Steueridentifikationsnummer) und gegebenenfalls REGON (Statistiknummer) angeben.\n\n"
            "9.4 Ihr Status als Händler/Nicht-Händler wird in Übereinstimmung mit den Anforderungen der Omnibus-Richtlinie in Ihrem öffentlichen Profil angezeigt, damit Kunden wissen, mit wem sie einen Vertrag abschließen.\n\n"
            "9.5 Die Angabe falscher Informationen in der Händlererklärung stellt einen wesentlichen Verstoß gegen diese Anbieterbedingungen dar und kann zur sofortigen Sperrung des Kontos führen."
        ),
        "fr": (
            "9.1 Nevumo est tenu, en vertu du droit applicable (Règlement sur les services numériques, Règlement P2B et droit de la protection des consommateurs), de vérifier si les Fournisseurs agissent en tant que professionnels (entreprises) ou en tant que particuliers proposant des services occasionnels.\n\n"
            "9.2 Lors de l'inscription (ou sur demande), vous devez déclarer de manière véridique :\n"
            "- si vous agissez en tant que professionnel (exerçant une activité économique) ou en tant que particulier ;\n"
            "- si vous agissez en tant que professionnel : le nom de votre entreprise, votre numéro d'identification fiscale (NIP/REGON pour la Pologne ; numéro de TVA ou équivalent pour les autres pays) et le pays d'enregistrement ;\n"
            "- si les services que vous proposez nécessitent une licence ou un permis professionnel, et le cas échéant, confirmer que vous détenez l'autorisation nécessaire.\n\n"
            "9.3 Les Fournisseurs agissant en tant que professionnels en Pologne doivent fournir leur NIP (numéro d'identification fiscale) et, le cas échéant, leur REGON (numéro statistique).\n\n"
            "9.4 Votre statut de professionnel/non-professionnel sera affiché sur votre Profil public, conformément aux exigences de la directive Omnibus, permettant aux Clients de savoir avec qui ils contractent.\n\n"
            "9.5 La fourniture de fausses informations dans la déclaration de professionnel constitue une violation substantielle des présentes Conditions pour les Fournisseurs et peut entraîner la suspension immédiate du compte."
        ),
        "es": (
            "9.1 Nevumo está obligado en virtud de la ley aplicable (Ley de Servicios Digitales, Reglamento P2B y ley de protección al consumidor) a verificar si los Proveedores actúan como comerciantes (empresas) o como particulares que ofrecen servicios ocasionales.\n\n"
            "9.2 Durante el registro (o previa solicitud), debe declarar de forma veraz:\n"
            "- si actúa como comerciante (realizando una actividad económica) o como particular;\n"
            "- si actúa como comerciante: el nombre de su empresa, número de identificación fiscal (NIP/REGON para Polonia; número de IVA o equivalente para otros países) y país de registro;\n"
            "- si los servicios que ofrece requieren una licencia o permiso profesional y, de ser así, confirmar que posee la autorización necesaria.\n\n"
            "9.3 Los Proveedores que actúan como comerciantes en Polonia deben proporcionar su NIP (número de identificación fiscal) y, si corresponde, REGON (número estadístico).\n\n"
            "9.4 Su estado de comerciante/no comerciante se mostrará en su Perfil público, de acuerdo con los requisitos de la Directiva Omnibus, lo que permitirá a los Clientes saber con quién están contratando.\n\n"
            "9.5 Proporcionar información falsa en la declaración de comerciante constituye un incumplimiento sustancial de estas Condiciones para Proveedores y puede dar lugar a la suspensión inmediata de la cuenta."
        ),
        "it": (
            "9.1 Nevumo è tenuta ai sensi della legge applicabile (Legge sui servizi digitali, Regolamento P2B e legge sulla tutela dei consumatori) a verificare se i Fornitori agiscono in qualità di professionisti (imprese) o di privati che offrono servizi occasionali.\n\n"
            "9.2 Durante la registrazione (o su richiesta), è necessario dichiarare in modo veritiero:\n"
            "- se si agisce come professionista (svolgendo un'attività economica) o come privato;\n"
            "- se si agisce come professionista: la ragione sociale, il numero di identificazione fiscale (NIP/REGON per la Polonia; partita IVA o equivalente per gli altri Paesi) e il paese di registrazione;\n"
            "- se i servizi offerti richiedono una licenza o un permesso professionale e, in tal caso, confermare di essere in possesso dell'autorizzazione necessaria.\n\n"
            "9.3 I Fornitori che agiscono come professionisti in Polonia devono fornire il proprio NIP (numero di identificazione fiscale) e, se applicabile, il REGON (numero statistico).\n\n"
            "9.4 Lo stato di professionista/non professionista verrà visualizzato sul Profilo pubblico, in conformità con i requisiti della Direttiva Omnibus, consentendo ai Clienti di sapere con chi stanno stipulando un contratto.\n\n"
            "9.5 Fornire informazioni false nella dichiarazione del professionista costituisce una violazione sostanziale delle presenti Condizioni per i Fornitori e può comportare la sospensione immediata dell'account."
        ),
        "nl": (
            "9.1 Nevumo is op grond van de toepasselijke wetgeving (Wet digitale diensten, P2B-verordening en consumentenbeschermingswetgeving) verplicht om na te gaan of Dienstverleners handelen als handelaren (bedrijven) of als particulieren die incidentele diensten aanbieden.\n\n"
            "9.2 Tijdens de registratie (of op verzoek) dient u naar waarheid te verklaren:\n"
            "- of u handelt als handelaar (het uitoefenen van een economische activiteit) of als particulier;\n"
            "- indien u handelt als handelaar: uw bedrijfsnaam, btw-nummer (NIP/REGON voor Polen; btw-nummer of equivalent voor andere landen) en land van registratie;\n"
            "- of de diensten die u aanbiedt een professionele licentie of vergunning vereisen, en zo ja, bevestigen dat u over de benodigde machtiging beschikt.\n\n"
            "9.3 Dienstverleners die als handelaren in Polen optreden, moeten hun NIP (fiscaal identificatienummer) en, indien van toepassing, REGON (statistisch nummer) opgeven.\n\n"
            "9.4 Uw status als handelaar/niet-handelaar wordt weergegeven op uw openbare Profiel, in overeenstemming met de vereisten van de Omnibus-richtlijn, zodat Klanten weten met wie zij een contract sluiten.\n\n"
            "9.5 Het verstrekken van onjuiste informatie in de verklaring van de handelaar vormt een wezenlijke schending van deze Voorwaarden voor Dienstverleners en kan leiden tot onmiddellijke opschorting van het account."
        ),
        "pt": (
            "9.1 A Nevumo é obrigada pela lei aplicável (Regulamento dos Serviços Digitais, Regulamento P2B e lei de proteção do consumidor) a verificar se os Prestadores atuam como comerciantes (empresas) ou como particulares que oferecem serviços ocasionais.\n\n"
            "9.2 Durante o registo (ou mediante solicitação), deve declarar com veracidade:\n"
            "- se atua como comerciante (exercendo atividade económica) ou como particular;\n"
            "- se atuar como comerciante: o nome da sua empresa, número de identificação fiscal (NIP/REGON para a Polónia; número de IVA ou equivalente para outros países) e país de registo;\n"
            "- se os serviços que oferece requerem licença ou autorização profissional e, em caso afirmativo, confirmar que possui a autorização necessária.\n\n"
            "9.3 Os Prestadores que atuem como comerciantes na Polónia devem fornecer o seu NIP (número de identificação fiscal) e, se aplicável, o REGON (número estatístico).\n\n"
            "9.4 O seu estatuto de comerciante/não comerciante será exibido no seu Perfil público, de acordo com os requisitos da Diretiva Omnibus, permitindo aos Clientes saber com quem estão a contratar.\n\n"
            "9.5 O fornecimento de informações falsas na declaração do comerciante constitui uma violação material destes Termos para Prestadores e pode resultar na suspensão imediata da conta."
        ),
        "pt-PT": (
            "9.1 A Nevumo é obrigada pela lei aplicável (Regulamento dos Serviços Digitais, Regulamento P2B e lei de proteção do consumidor) a verificar se os Prestadores atuam como comerciantes (empresas) ou como particulares que oferecem serviços ocasionais.\n\n"
            "9.2 Durante o registo (ou mediante solicitação), deve declarar com veracidade:\n"
            "- se atua como comerciante (exercendo atividade económica) ou como particular;\n"
            "- se atuar como comerciante: o nome da sua empresa, número de identificação fiscal (NIP/REGON para a Polónia; número de IVA ou equivalente para outros países) e país de registo;\n"
            "- se os serviços que oferece requerem licença ou autorização profissional e, em caso afirmativo, confirmar que possui a autorização necessária.\n\n"
            "9.3 Os Prestadores que atuem como comerciantes na Polónia devem fornecer o seu NIP (número de identificação fiscal) e, se aplicável, o REGON (número estatístico).\n\n"
            "9.4 O seu estatuto de comerciante/não comerciante será exibido no seu Perfil público, de acordo com os requisitos da Diretiva Omnibus, permitindo aos Clientes saber com quem estão a contratar.\n\n"
            "9.5 O fornecimento de informações falsas na declaração do comerciante constitui uma violação material destes Termos para Prestadores e pode resultar na suspensão imediata da conta."
        ),
        "ro": (
            "9.1 Nevumo este obligată în temeiul legii aplicabile (Legea privind serviciile digitale, Regulamentul P2B și legea privind protecția consumatorilor) să verifice dacă Furnizorii acționează în calitate de comercianți (întreprinderi) sau în calitate de persoane fizice care oferă servicii ocazionale.\n\n"
            "9.2 În timpul înregistrării (sau la cerere), trebuie să declarați cu adevărat:\n"
            "- dacă acționați în calitate de comerciant (desfășurând activitate economică) sau ca persoană fizică;\n"
            "- dacă acționați ca comerciant: numele companiei dvs., codul de identificare fiscală (NIP/REGON pentru Polonia; codul de TVA sau echivalentul pentru alte țări) și țara de înregistrare;\n"
            "- dacă serviciile pe care le oferiți necesită o licență sau un permis profesional și, dacă da, să confirmați că dețineți autorizația necesară.\n\n"
            "9.3 Furnizorii care acționează în calitate de comercianți în Polonia trebuie să furnizeze NIP-ul lor (codul de identificare fiscală) și, dacă este cazul, REGON-ul (numărul statistic).\n\n"
            "9.4 Statutul dumneavoastră de comerciant/necomerciant va fi afișat pe Profilul dumneavoastră public, în conformitate cu cerințele Directivei Omnibus, permițând Clienților să știe cu cine încheie contractul.\n\n"
            "9.5 Furnizarea de informații false în declarația comerciantului constituie o încălcare semnificativă a acestor Termeni pentru Furnizori și poate duce la suspendarea imediată a contului."
        ),
        "ru": (
            "9.1 Nevumo обязано в соответствии с применимым законодательством (Закон о цифровых услугах, Регламент P2B и закон о защите прав потребителей) проверять, действуют ли Поставщики как коммерсанты (предприятия) или как частные лица, предлагающие разовые услуги.\n\n"
            "9.2 При регистрации (или по запросу) вы должны правдиво заявить:\n"
            "- действуете ли вы как коммерсант (осуществляя экономическую деятельность) или как частное лицо;\n"
            "- если вы действуете как коммерсант: название вашей компании, идентификационный номер налогоплательщика (NIP/REGON для Польши; номер НДС или эквивалент для других стран) и страну регистрации;\n"
            "- требуют ли предлагаемые вами услуги профессиональной лицензии или разрешения, и если да, подтвердить, что у вас есть необходимое разрешение.\n\n"
            "9.3 Поставщики, действующие в качестве коммерсантов в Польше, должны предоставить свой NIP (идентификационный номер налогоплательщика) и, если применимо, REGON (статистический номер).\n\n"
            "9.4 Ваш статус коммерсанта/некоммерсанта будет отображаться в вашем общедоступном Профиле в соответствии с требованиями Директивы Omnibus, чтобы Клиенты знали, с кем они заключают договор.\n\n"
            "9.5 Предоставление ложной информации в декларации коммерсанта является существенным нарушением настоящих Условий для Поставщиков и может привести к немедленной приостановке действия учетной записи."
        ),
        "uk": (
            "9.1 Nevumo зобов'язане відповідно до чинного законодавства (Закон про цифрові послуги, Регламент P2B та закон про захист прав споживачів) перевіряти, чи діють Постачальники як комерсанти (підприємства) або як приватні особи, що пропонують разові послуги.\n\n"
            "9.2 Під час реєстрації (або за запитом) ви повинні правдиво заявити:\n"
            "- чи дієте ви як комерсант (здійснюючи економічну діяльність) або як приватна особа;\n"
            "- якщо ви дієте як комерсант: назва вашої компанії, ідентифікаційний номер платника податків (NIP/REGON для Польщі; номер ПДВ або еквівалент для інших країн) і країна реєстрації;\n"
            "- чи вимагають пропоновані вами послуги професійної ліцензії або дозволу, і якщо так, підтвердити, що у вас є необхідний дозвіл.\n\n"
            "9.3 Постачальники, що діють як комерсанти в Польщі, повинні надати свій NIP (ідентифікаційний номер платника податків) і, якщо застосовно, REGON (статистичний номер).\n\n"
            "9.4 Ваш статус комерсанта/некомерсанта відображатиметься у вашому загальнодоступному Профілі відповідно до вимог Директиви Omnibus, щоб Клієнти знали, з ким вони укладають договір.\n\n"
            "9.5 Надання неправдивої інформації в декларації комерсанта є істотним порушенням цих Умов для Постачальників і може призвести до негайного призупинення дії облікового запису."
        ),
        "cs": (
            "9.1 Společnost Nevumo je podle platných právních předpisů (zákon o digitálních službách, nařízení P2B a zákony na ochranu spotřebitele) povinna ověřit, zda poskytovatelé jednají jako obchodníci (podniky) nebo jako soukromé osoby nabízející příležitostné služby.\n\n"
            "9.2 Během registrace (nebo na žádost) musíte pravdivě prohlásit:\n"
            "- zda jednáte jako obchodník (vykonávající hospodářskou činnost) nebo jako soukromá osoba;\n"
            "- pokud jednáte jako obchodník: název vaší společnosti, daňové identifikační číslo (NIP/REGON pro Polsko; DIČ nebo ekvivalent pro jiné země) a zemi registrace;\n"
            "- zda vámi nabízené služby vyžadují profesní licenci nebo povolení, a pokud ano, potvrdit, že máte potřebné oprávnění.\n\n"
            "9.3 Poskytovatelé jednající jako obchodníci v Polsku musí uvést své NIP (daňové identifikační číslo) a případně REGON (statistické číslo).\n\n"
            "9.4 Váš status obchodníka/neobchodníka se zobrazí na vašem veřejném profilu v souladu s požadavky směrnice Omnibus, aby klienti věděli, s kým uzavírají smlouvu.\n\n"
            "9.5 Uvedení nepravdivých informací v prohlášení obchodníka představuje závažné porušení těchto podmínek pro poskytovatele a může mít za následek okamžité pozastavení účtu."
        ),
        "da": (
            "9.1 Nevumo er i henhold til gældende lov (forordning om digitale tjenester, P2B-forordning og forbrugerbeskyttelseslovgivning) forpligtet til at verificere, om udbydere optræder som erhvervsdrivende (virksomheder) eller som privatpersoner, der tilbyder lejlighedsvise tjenester.\n\n"
            "9.2 Under registreringen (eller efter anmodning) skal du sandfærdigt erklære:\n"
            "- om du optræder som erhvervsdrivende (udfører økonomisk aktivitet) eller som privatperson;\n"
            "- hvis du optræder som erhvervsdrivende: dit firmanavn, momsregistreringsnummer (NIP/REGON for Polen; momsnummer eller tilsvarende for andre lande) og registreringsland;\n"
            "- om de tjenester, du tilbyder, kræver en professionel licens eller tilladelse, og i bekræftende fald bekræfte, at du har den nødvendige tilladelse.\n\n"
            "9.3 Udbydere, der optræder som erhvervsdrivende i Polen, skal oplyse deres NIP (momsregistreringsnummer) og, hvis relevant, REGON (statistisk nummer).\n\n"
            "9.4 Din status som erhvervsdrivende/ikke-erhvervsdrivende vil blive vist på din offentlige profil i overensstemmelse med Omnibus-direktivets krav, så kunderne ved, hvem de indgår kontrakt med.\n\n"
            "9.5 Afgivelse af falske oplysninger i erklæringen som erhvervsdrivende udgør et væsentligt brud på disse vilkår for udbydere og kan resultere i øjeblikkelig suspension af kontoen."
        ),
        "sv": (
            "9.1 Nevumo är enligt tillämplig lag (förordningen om digitala tjänster, P2B-förordningen och konsumentskyddslagstiftningen) skyldigt att verifiera om leverantörer agerar som näringsidkare (företag) eller som privatpersoner som erbjuder tillfälliga tjänster.\n\n"
            "9.2 Vid registrering (eller på begäran) måste du sanningsenligt intyga:\n"
            "- om du agerar som näringsidkare (bedriver ekonomisk verksamhet) eller som privatperson;\n"
            "- om du agerar som näringsidkare: ditt företagsnamn, skatteregistreringsnummer (NIP/REGON för Polen; momsregistreringsnummer eller motsvarande för andra länder) och registreringsland;\n"
            "- om de tjänster du erbjuder kräver en yrkeslicens eller tillstånd, och i så fall bekräfta att du har nödvändigt tillstånd.\n\n"
            "9.3 Leverantörer som agerar som näringsidkare i Polen måste ange sitt NIP (skatteregistreringsnummer) och, om tillämpligt, REGON (statistiskt nummer).\n\n"
            "9.4 Din status som näringsidkare/icke-näringsidkare kommer att visas på din offentliga profil i enlighet med kraven i omnibusdirektivet, så att kunderna vet vem de ingår avtal med.\n\n"
            "9.5 Att lämna falsk information i näringsidkarintyget utgör ett väsentligt brott mot dessa villkor för leverantörer och kan leda till omedelbar avstängning av kontot."
        ),
        "no": (
            "9.1 Nevumo er i henhold til gjeldende lov (forordningen om digitale tjenester, P2B-forordningen og forbrukervernloven) pålagt å verifisere om leverandører opptrer som næringsdrivende (bedrifter) eller som privatpersoner som tilbyr sporadiske tjenester.\n\n"
            "9.2 Under registreringen (eller på forespørsel) må du sannferdig erklære:\n"
            "- om du opptrer som næringsdrivende (utøver økonomisk aktivitet) eller som privatperson;\n"
            "- hvis du opptrer som næringsdrivende: firmanavnet ditt, organisasjonsnummer (NIP/REGON for Polen; MVA-nummer eller tilsvarende for andre land) og registreringsland;\n"
            "- om tjenestene du tilbyr krever en profesjonell lisens eller tillatelse, og i så fall bekrefte at du har den nødvendige tillatelsen.\n\n"
            "9.3 Leverandører som opptrer som næringsdrivende i Polen, må oppgi sitt NIP (organisasjonsnummer) og, om relevant, REGON (statistisk nummer).\n\n"
            "9.4 Din status som næringsdrivende/ikke-næringsdrivende vil bli vist på din offentlige profil i samsvar med kravene i omnibusdirektivet, slik at kundene vet hvem de inngår kontrakt med.\n\n"
            "9.5 Å oppgi falsk informasjon i næringsdrivendeerklæringen utgjør et vesentlig brudd på disse vilkårene for leverandører og kan føre til umiddelbar suspensjon av kontoen."
        ),
        "fi": (
            "9.1 Nevumo on sovellettavan lain (digitaalisia palveluja koskeva säädös, P2B-asetus ja kuluttajansuojalaki) nojalla velvollinen tarkistamaan, toimivatko palveluntarjoajat elinkeinonharjoittajina (yrityksinä) vai yksityishenkilöinä, jotka tarjoavat satunnaisia palveluita.\n\n"
            "9.2 Rekisteröitymisen yhteydessä (tai pyynnöstä) sinun on ilmoitettava totuudenmukaisesti:\n"
            "- toimitko elinkeinonharjoittajana (harjoitatko taloudellista toimintaa) vai yksityishenkilönä;\n"
            "- jos toimit elinkeinonharjoittajana: yrityksesi nimi, verotunniste (NIP/REGON Puolassa; alv-numero tai vastaava muissa maissa) ja rekisteröintimaa;\n"
            "- edellyttävätkö tarjoamasi palvelut ammattilupaa, ja jos edellyttävät, vahvistettava, että sinulla on tarvittava lupa.\n\n"
            "9.3 Puolassa elinkeinonharjoittajina toimivien palveluntarjoajien on ilmoitettava NIP-numeronsa (verotunniste) ja tarvittaessa REGON-numeronsa (tilastonumero).\n\n"
            "9.4 Elinkeinonharjoittaja-/ei-elinkeinonharjoittaja-statuksesi näkyy julkisessa profiilissasi omnibus-direktiivin vaatimusten mukaisesti, jotta asiakkaat tietävät, kenen kanssa he tekevät sopimuksen.\n\n"
            "9.5 Väärien tietojen antaminen elinkeinonharjoittajan ilmoituksessa on olennainen rikkomus näitä palveluntarjoajien ehtoja vastaan ja voi johtaa tilin välittömään jäädyttämiseen."
        ),
        "et": (
            "9.1 Nevumo on vastavalt kohaldatavatele õigusaktidele (digiteenuste õigusakt, P2B-määrus ja tarbijakaitseseadus) kohustatud kontrollima, kas teenusepakkujad tegutsevad kauplejatena (ettevõtetena) või eraisikutena, kes pakuvad juhuslikke teenuseid.\n\n"
            "9.2 Registreerumisel (või nõudmisel) peate tõepäraselt deklareerima:\n"
            "- kas tegutsete kauplejana (tegelete majandustegevusega) või eraisikuna;\n"
            "- kui tegutsete kauplejana: oma ettevõtte nimi, maksukohustuslase number (Poolas NIP/REGON; käibemaksukohustuslase number või samaväärne teistes riikides) ja registreerimisriik;\n"
            "- kas teie pakutavad teenused nõuavad kutselitsentsi või luba, ja kui jah, kinnitama, et teil on vajalik volitus.\n\n"
            "9.3 Poolas kauplejatena tegutsevad teenusepakkujad peavad esitama oma NIP-i (maksukohustuslase number) ja vajaduse korral REGON-i (statistiline number).\n\n"
            "9.4 Teie kaupleja/mittekaupleja staatus kuvatakse teie avalikul profiilil vastavalt omnibussi direktiivi nõuetele, mis võimaldab klientidel teada, kellega nad lepingu sõlmivad.\n\n"
            "9.5 Valeandmete esitamine kaupleja deklaratsioonis kujutab endast nende teenusepakkujate tingimuste olulist rikkumist ja võib kaasa tuua konto kohese peatamise."
        ),
        "lt": (
            "9.1 Nevumo, remiantis taikomais įstatymais (Skaitmeninių paslaugų aktas, P2B reglamentas ir vartotojų apsaugos įstatymas), privalo patikrinti, ar paslaugų teikėjai veikia kaip prekybininkai (įmonės), ar kaip privatūs asmenys, siūlantys atsitiktines paslaugas.\n\n"
            "9.2 Registracijos metu (arba paprašius) privalote teisingai deklaruoti:\n"
            "- ar veikiate kaip prekybininkas (vykdote ekonominę veiklą), ar kaip privatus asmuo;\n"
            "- jei veikiate kaip prekybininkas: savo įmonės pavadinimą, mokesčių mokėtojo kodą (NIP / REGON Lenkijoje; PVM mokėtojo kodą ar atitikmenį kitose šalyse) ir registracijos šalį;\n"
            "- ar jūsų siūlomoms paslaugoms reikalinga profesinė licencija ar leidimas, ir jei taip, patvirtinti, kad turite reikiamą leidimą.\n\n"
            "9.3 Lenkijoje kaip prekybininkai veikiantys paslaugų teikėjai privalo pateikti savo NIP (mokesčių mokėtojo kodą) ir, jei taikoma, REGON (statistinį numerį).\n\n"
            "9.4 Jūsų prekybininko / ne prekybininko statusas bus rodomas jūsų viešame profilyje pagal „Omnibus“ direktyvos reikalavimus, leidžiančius klientams žinoti, su kuo jie sudaro sutartį.\n\n"
            "9.5 Neteisingos informacijos pateikimas prekybininko deklaracijoje yra esminis šių Paslaugų teikėjų sąlygų pažeidimas ir gali lemti nedelsiamą paskyros sustabdymą."
        ),
        "lv": (
            "9.1 Saskaņā ar piemērojamiem tiesību aktiem (Digitālo pakalpojumu akts, P2B regula un patērētāju tiesību aizsardzības likums) Nevumo ir pienākums pārbaudīt, vai Pakalpojumu sniedzēji darbojas kā tirgotāji (uzņēmumi) vai kā privātpersonas, kas piedāvā neregulārus pakalpojumus.\n\n"
            "9.2 Reģistrācijas laikā (vai pēc pieprasījuma) jums patiesi jādeklarē:\n"
            "- vai jūs darbojaties kā tirgotājs (veicat saimniecisko darbību) vai kā privātpersona;\n"
            "- ja darbojaties kā tirgotājs: uzņēmuma nosaukums, nodokļu maksātāja reģistrācijas numurs (NIP/REGON Polijā; PVN numurs vai ekvivalents citās valstīs) un reģistrācijas valsts;\n"
            "- vai jūsu piedāvātajiem pakalpojumiem ir nepieciešama profesionālā licence vai atļauja, un, ja tā ir, jāapstiprina, ka jums ir nepieciešamā atļauja.\n\n"
            "9.3 Pakalpojumu sniedzējiem, kas Polijā darbojas kā tirgotāji, ir jānorāda savs NIP (nodokļu maksātāja reģistrācijas numurs) un, ja piemērojams, REGON (statistikas numurs).\n\n"
            "9.4 Jūsu tirgotāja/ne-tirgotāja statuss tiks parādīts jūsu publiskajā profilā saskaņā ar Omnibus direktīvas prasībām, ļaujot Klientiem zināt, ar ko viņi slēdz līgumu.\n\n"
            "9.5 Nepatiesas informācijas sniegšana tirgotāja deklarācijā ir būtisks šo Pakalpojumu sniedzēju noteikumu pārkāpums un var izraisīt tūlītēju konta apturēšanu."
        ),
        "hu": (
            "9.1 A Nevumo az alkalmazandó jogszabályok (digitális szolgáltatásokról szóló jogszabály, P2B rendelet és fogyasztóvédelmi törvény) értelmében köteles ellenőrizni, hogy a Szolgáltatók kereskedőként (vállalkozásként) vagy alkalmi szolgáltatásokat nyújtó magánszemélyként járnak-e el.\n\n"
            "9.2 A regisztráció során (vagy kérésre) a valóságnak megfelelően nyilatkoznia kell arról, hogy:\n"
            "- kereskedőként (gazdasági tevékenységet folytatva) vagy magánszemélyként jár-e el;\n"
            "- ha kereskedőként jár el: a cégneve, adószáma (Lengyelországban NIP/REGON; más országokban áfaszám vagy azzal egyenértékű) és a regisztráció országa;\n"
            "- az Ön által kínált szolgáltatásokhoz szükséges-e szakmai engedély, és ha igen, erősítse meg, hogy rendelkezik a szükséges engedéllyel.\n\n"
            "9.3 A Lengyelországban kereskedőként eljáró Szolgáltatóknak meg kell adniuk NIP (adószám) és adott esetben REGON (statisztikai szám) számukat.\n\n"
            "9.4 Az Ön kereskedői/nem kereskedői státusza megjelenik a nyilvános profilján, az Omnibus irányelv követelményeinek megfelelően, lehetővé téve az Ügyfelek számára, hogy tudják, kivel kötnek szerződést.\n\n"
            "9.5 Hamis információk megadása a kereskedői nyilatkozatban a jelen Szolgáltatói Feltételek lényeges megsértésének minősül, és a fiók azonnali felfüggesztését vonhatja maga után."
        ),
        "hr": (
            "9.1 Nevumo je prema primjenjivom zakonu (Zakon o digitalnim uslugama, Uredba P2B i zakon o zaštiti potrošača) dužan provjeriti djeluju li Pružatelji usluga kao trgovci (tvrtke) ili kao privatne osobe koje nude povremene usluge.\n\n"
            "9.2 Tijekom registracije (ili na zahtjev), morate istinito izjaviti:\n"
            "- djelujete li kao trgovac (obavljate gospodarsku djelatnost) ili kao privatna osoba;\n"
            "- ako djelujete kao trgovac: naziv vaše tvrtke, porezni identifikacijski broj (NIP/REGON za Poljsku; PDV broj ili ekvivalent za druge zemlje) i zemlju registracije;\n"
            "- zahtijevaju li usluge koje nudite profesionalnu licencu ili dozvolu i ako da, potvrditi da posjedujete potrebno ovlaštenje.\n\n"
            "9.3 Pružatelji usluga koji djeluju kao trgovci u Poljskoj moraju dostaviti svoj NIP (porezni identifikacijski broj) i, ako je primjenjivo, REGON (statistički broj).\n\n"
            "9.4 Vaš status trgovca/ne-trgovca bit će prikazan na vašem javnom Profilu, u skladu sa zahtjevima Direktive Omnibus, omogućujući Klijentima da znaju s kim sklapaju ugovor.\n\n"
            "9.5 Davanje lažnih podataka u izjavi trgovca predstavlja značajno kršenje ovih Uvjeta za pružatelje usluga i može rezultirati trenutnom suspenzijom računa."
        ),
        "sk": (
            "9.1 Spoločnosť Nevumo je podľa platných právnych predpisov (zákon o digitálnych službách, nariadenie P2B a zákony na ochranu spotrebiteľa) povinná overiť, či poskytovatelia konajú ako obchodníci (podniky) alebo ako súkromné osoby ponúkajúce príležitostné služby.\n\n"
            "9.2 Počas registrácie (alebo na žiadosť) musíte pravdivo vyhlásiť:\n"
            "- či konáte ako obchodník (vykonávajúci hospodársku činnosť) alebo ako súkromná osoba;\n"
            "- ak konáte ako obchodník: názov vašej spoločnosti, daňové identifikačné číslo (NIP/REGON pre Poľsko; IČ DPH alebo ekvivalent pre iné krajiny) a krajinu registrácie;\n"
            "- či vami ponúkané služby vyžadujú profesijnú licenciu alebo povolenie, a ak áno, potvrdiť, že máte potrebné oprávnenie.\n\n"
            "9.3 Poskytovatelia konajúci ako obchodníci v Poľsku musia uviesť svoje NIP (daňové identifikačné číslo) a prípadne REGON (štatistické číslo).\n\n"
            "9.4 Váš status obchodníka/neobchodníka sa zobrazí na vašom verejnom profile v súlade s požiadavkami smernice Omnibus, aby klienti vedeli, s kým uzatvárajú zmluvu.\n\n"
            "9.5 Uvedenie nepravdivých informácií vo vyhlásení obchodníka predstavuje závažné porušenie týchto podmienok pre poskytovateľov a môže mať za následok okamžité pozastavenie účtu."
        ),
        "sl": (
            "9.1 Nevumo mora v skladu z veljavno zakonodajo (Zakon o digitalnih storitvah, Uredba P2B in zakonodaja o varstvu potrošnikov) preveriti, ali ponudniki delujejo kot trgovci (podjetja) ali kot zasebniki, ki ponujajo občasne storitve.\n\n"
            "9.2 Med registracijo (ali na zahtevo) morate resnično izjaviti:\n"
            "- ali delujete kot trgovec (opravljate gospodarsko dejavnost) ali kot zasebnik;\n"
            "- če delujete kot trgovec: ime vašega podjetja, davčno identifikacijsko številko (NIP/REGON za Poljsko; številko DDV ali enakovredno za druge države) in državo registracije;\n"
            "- ali storitve, ki jih ponujate, zahtevajo poklicno licenco ali dovoljenje, in če da, potrditi, da imate potrebno pooblastilo.\n\n"
            "9.3 Ponudniki, ki delujejo kot trgovci na Poljskem, morajo predložiti svoj NIP (davčno identifikacijsko številko) in, če je primerno, REGON (statistično številko).\n\n"
            "9.4 Vaš status trgovca/netrgovca bo prikazan na vašem javnem profilu v skladu z zahtevami Direktive Omnibus, kar bo strankam omogočilo, da vedo, s kom sklepajo pogodbo.\n\n"
            "9.5 Navedba lažnih informacij v izjavi trgovca predstavlja bistveno kršitev teh pogojev za ponudnike in lahko povzroči takojšnjo začasno ustavitev računa."
        ),
        "el": (
            "9.1 Η Nevumo υποχρεούται βάσει της ισχύουσας νομοθεσίας (Πράξη για τις Ψηφιακές Υπηρεσίες, Κανονισμός P2B και νομοθεσία περί προστασίας των καταναλωτών) να επαληθεύει εάν οι Πάροχοι ενεργούν ως έμποροι (επιχειρήσεις) ή ως ιδιώτες που προσφέρουν περιστασιακές υπηρεσίες.\n\n"
            "9.2 Κατά την εγγραφή (ή κατόπιν αιτήματος), πρέπει να δηλώσετε ειλικρινά:\n"
            "- εάν ενεργείτε ως έμπορος (ασκώντας οικονομική δραστηριότητα) ή ως ιδιώτης.\n"
            "- εάν ενεργείτε ως έμπορος: την επωνυμία της επιχείρησής σας, τον αριθμό φορολογικού μητρώου (NIP/REGON για την Πολωνία, ΑΦΜ ή αντίστοιχο για άλλες χώρες) και τη χώρα εγγραφής.\n"
            "- εάν οι υπηρεσίες που προσφέρετε απαιτούν επαγγελματική άδεια και, εάν ναι, να επιβεβαιώσετε ότι διαθέτετε την απαραίτητη εξουσιοδότηση.\n\n"
            "9.3 Οι Πάροχοι που ενεργούν ως έμποροι στην Πολωνία πρέπει να παρέχουν το NIP (αριθμός φορολογικού μητρώου) τους και, κατά περίπτωση, το REGON (στατιστικός αριθμός).\n\n"
            "9.4 Η ιδιότητά σας ως εμπόρου/μη εμπόρου θα εμφανίζεται στο δημόσιο Προφίλ σας, σύμφωνα με τις απαιτήσεις της Οδηγίας Omnibus, επιτρέποντας στους Πελάτες να γνωρίζουν με ποιον συμβάλλονται.\n\n"
            "9.5 Η παροχή ψευδών πληροφοριών στη δήλωση εμπόρου συνιστά ουσιώδη παραβίαση αυτών των Όρων Παρόχου και μπορεί να οδηγήσει σε άμεση αναστολή του λογαριασμού."
        ),
        "tr": (
            "9.1 Nevumo, geçerli yasa (Dijital Hizmetler Yasası, P2B Yönetmeliği ve tüketiciyi koruma yasası) uyarınca, Sağlayıcıların tüccar (işletme) olarak mı yoksa ara sıra hizmet sunan özel şahıslar olarak mı hareket ettiğini doğrulamak zorundadır.\n\n"
            "9.2 Kayıt sırasında (veya talep üzerine), aşağıdakileri doğru bir şekilde beyan etmelisiniz:\n"
            "- tüccar (ekonomik faaliyette bulunan) olarak mı yoksa özel bir şahıs olarak mı hareket ettiğinizi;\n"
            "- tüccar olarak hareket ediyorsanız: işletme adınız, vergi kimlik numaranız (Polonya için NIP/REGON; diğer ülkeler için KDV numarası veya eşdeğeri) ve kayıt ülkeniz;\n"
            "- sunduğunuz hizmetlerin profesyonel bir lisans veya izin gerektirip gerektirmediğini ve gerektiriyorsa gerekli yetkiye sahip olduğunuzu onaylamanız.\n\n"
            "9.3 Polonya'da tüccar olarak hareket eden Sağlayıcılar NIP'lerini (vergi kimlik numarası) ve geçerliyse REGON'larını (istatistiksel numara) sağlamalıdır.\n\n"
            "9.4 Tüccar/tüccar olmayan statünüz, Müşterilerin kiminle sözleşme yaptıklarını bilmelerini sağlayan Omnibus Direktifi gereksinimlerine uygun olarak genel Profilinizde görüntülenecektir.\n\n"
            "9.5 Tüccar beyanında yanlış bilgi verilmesi, bu Sağlayıcı Şartlarının esaslı bir ihlalini teşkil eder ve hesabın derhal askıya alınmasına neden olabilir."
        ),
        "ga": (
            "9.1 Ceanglaítear ar Nevumo faoin dlí is infheidhme (an Gníomh um Sheirbhísí Digiteacha, Rialachán P2B, agus an dlí um chosaint tomhaltóirí) a fhíorú an ngníomhaíonn Soláthraithe mar thrádálaithe (gnólachtaí) nó mar dhaoine príobháideacha a thairgeann seirbhísí ócáideacha.\n\n"
            "9.2 Le linn clárúcháin (nó ar iarratas), ní mór duit a dhearbhú go fírinneach:\n"
            "- an bhfuil tú ag gníomhú mar thrádálaí (ag seoladh gníomhaíocht eacnamaíoch) nó mar dhuine príobháideach;\n"
            "- má tá tú ag gníomhú mar thrádálaí: ainm do ghnó, uimhir aitheantais chánach (NIP/REGON don Pholainn; uimhir CBL nó a comhionann i dtíortha eile), agus tír do chlárúcháin;\n"
            "- an dteastaíonn ceadúnas gairmiúil nó cead uait le haghaidh na seirbhísí a thairgeann tú, agus más amhlaidh, dearbhaigh go bhfuil an t-údarú riachtanach agat.\n\n"
            "9.3 Ní mór do Sholáthraithe atá ag gníomhú mar thrádálaithe sa Pholainn a NIP (uimhir aitheantais chánach) agus, más infheidhme, REGON (uimhir staitistiúil) a sholáthar.\n\n"
            "9.4 Taispeánfar do stádas trádálaí/neamhthrádálaí ar do Phróifíl phoiblí, de réir riachtanais na Treorach Omnibus, rud a chuirfidh ar chumas Cliaint fios a bheith acu cé leis a bhfuil siad ag conradh.\n\n"
            "9.5 Is sárú ábhartha ar na Téarmaí Soláthraí seo é faisnéis bhréagach a sholáthar sa dearbhú trádálaí agus d'fhéadfadh fionraí láithreach an chuntais a bheith mar thoradh air."
        ),
        "is": (
            "9.1 Nevumo er krafist samkvæmt gildandi lögum (lög um stafræna þjónustu, P2B reglugerð og lög um neytendavernd) að sannreyna hvort þjónustuveitendur starfi sem kaupmenn (fyrirtæki) eða sem einstaklingar sem bjóða upp á tilfallandi þjónustu.\n\n"
            "9.2 Við skráningu (eða að beiðni) verður þú að lýsa yfir á sannan hátt:\n"
            "- hvort þú starfar sem kaupmaður (stundar atvinnustarfsemi) eða sem einstaklingur;\n"
            "- ef þú starfar sem kaupmaður: nafn fyrirtækis þíns, skattanúmer (NIP/REGON fyrir Pólland; VSK númer eða sambærilegt fyrir önnur lönd) og skráningarland;\n"
            "- hvort þjónustan sem þú býður upp á krefst faglegs leyfis, og ef svo er, staðfesta að þú hafir nauðsynlega heimild.\n\n"
            "9.3 Þjónustuveitendur sem starfa sem kaupmenn í Póllandi verða að gefa upp NIP sitt (skattanúmer) og, ef við á, REGON (tölfræðilegt númer).\n\n"
            "9.4 Staða þín sem kaupmaður/ekki-kaupmaður verður birt á opinberum prófíl þínum, í samræmi við kröfur Omnibus tilskipunarinnar, sem gerir viðskiptavinum kleift að vita við hvern þeir eru að gera samning.\n\n"
            "9.5 Að veita falskar upplýsingar í yfirlýsingu kaupmanns felur í sér verulegt brot á þessum skilmálum fyrir þjónustuveitendur og getur leitt til tafarlausrar stöðvunar reiknings."
        ),
        "lb": (
            "9.1 Nevumo ass ënner uwendbarem Gesetz verflicht (Gesetz iwwer digital Servicer, P2B-Reglement a Konsumenteschutzgesetz) fir z'iwwerpréiwen ob Ubidder als Händler (Firmen) oder als Privatpersounen optrieden déi geleeëntlech Servicer ubidden.\n\n"
            "9.2 Wärend der Umeldung (oder op Ufro) musst Dir wouerheetsgeméiss deklaréieren:\n"
            "- ob Dir als Händler optried (eng wirtschaftlech Aktivitéit ausüübt) oder als Privatpersoun;\n"
            "- wann Dir als Händler optried: Äre Firmennumm, Steieridentifikatiounsnummer (NIP/REGON fir Polen; TVA-Nummer oder Äquivalent fir aner Länner) an d'Land vun der Registréierung;\n"
            "- ob d'Servicer, déi Dir ubitt, eng professionell Lizenz oder Genehmegung erfuerderen, a wa jo, bestätegt datt Dir déi néideg Autorisatioun hutt.\n\n"
            "9.3 Ubidder, déi als Händler a Polen optrieden, mussen hir NIP (Steieridentifikatiounsnummer) an, wa relevant, REGON (statistesch Nummer) ubidden.\n\n"
            "9.4 Äre Status als Händler/Net-Händler gëtt op Ärem ëffentleche Profil ugewisen, am Aklang mat den Ufuerderunge vun der Omnibus-Direktiv, fir de Clienten z'erméiglechen ze wëssen mat wiem se e Kontrakt ofschléissen.\n\n"
            "9.5 D'Bereetstellung vu falschen Informatiounen an der Händlerdeklaratioun stellt e wesentleche Verstouss géint dës Ubidderbedéngungen duer a kann zu enger direkter Suspensioun vum Kont féieren."
        ),
        "mk": (
            "9.1 Nevumo е должен според применливиот закон (Закон за дигитални услуги, Регулатива P2B и закон за заштита на потрошувачите) да потврди дали Давателите дејствуваат како трговци (бизниси) или како приватни лица кои нудат повремени услуги.\n\n"
            "9.2 За време на регистрацијата (или на барање), мора вистинито да изјавите:\n"
            "- дали дејствувате како трговец (извршувате економска активност) или како приватно лице;\n"
            "- ако дејствувате како трговец: име на вашиот бизнис, даночен идентификациски број (NIP/REGON за Полска; ДДВ број или еквивалент за други земји) и земја на регистрација;\n"
            "- дали услугите што ги нудите бараат професионална лиценца или дозвола, и ако е така, да потврдите дека го поседувате потребното овластување.\n\n"
            "9.3 Давателите кои дејствуваат како трговци во Полска мора да го обезбедат својот NIP (даночен идентификациски број) и, доколку е применливо, REGON (статистички број).\n\n"
            "9.4 Вашиот статус на трговец/не-трговец ќе биде прикажан на вашиот јавен Профил, во согласност со барањата на Директивата Omnibus, овозможувајќи им на Клиентите да знаат со кого склучуваат договор.\n\n"
            "9.5 Обезбедувањето на лажни информации во декларацијата за трговец претставува материјално прекршување на овие Услови за Даватели и може да доведе до итна суспензија на профилот."
        ),
        "mt": (
            "9.1 Nevumo huwa meħtieġ taħt il-liġi applikabbli (l-Att dwar is-Servizzi Diġitali, ir-Regolament P2B, u l-liġi dwar il-protezzjoni tal-konsumatur) li jivverifika jekk il-Fornituri jaġixxux bħala negozjanti (negozji) jew bħala individwi privati li joffru servizzi okkażjonali.\n\n"
            "9.2 Waqt ir-reġistrazzjoni (jew fuq talba), trid tiddikjara bil-verità:\n"
            "- jekk intix qed taġixxi bħala negozjant (twettaq attività ekonomika) jew bħala individwu privat;\n"
            "- jekk taġixxi bħala negozjant: l-isem tan-negozju tiegħek, in-numru ta' identifikazzjoni tat-taxxa (NIP/REGON għall-Polonja; numru tal-VAT jew ekwivalenti għal pajjiżi oħra), u l-pajjiż ta' reġistrazzjoni;\n"
            "- jekk is-servizzi li toffri jeħtiġux liċenzja jew permess professjonali, u jekk iva, ikkonferma li għandek l-awtorizzazzjoni meħtieġa.\n\n"
            "9.3 Fornituri li jaġixxu bħala negozjanti fil-Polonja jridu jipprovdu n-NIP (numru ta' identifikazzjoni tat-taxxa) tagħhom u, jekk applikabbli, ir-REGON (numru statistiku).\n\n"
            "9.4 L-istatus tiegħek ta' negozjant/mhux negozjant se jintwera fuq il-Profil pubbliku tiegħek, skont ir-rekwiżiti tad-Direttiva Omnibus, li jippermetti lill-Klijenti jkunu jafu ma' min qed jikkuntrattaw.\n\n"
            "9.5 Il-provvista ta' informazzjoni falza fid-dikjarazzjoni tan-negozjant tikkostitwixxi ksur materjali ta' dawn it-Termini għall-Fornituri u tista' tirriżulta f'sospensjoni immedjata tal-kont."
        ),
        "sq": (
            "9.1 Nevumo kërkohet sipas ligjit të zbatueshëm (Akti i Shërbimeve Dixhitale, Rregullorja P2B dhe ligji për mbrojtjen e konsumatorit) të verifikojë nëse Ofruesit veprojnë si tregtarë (biznese) ose si individë privatë që ofrojnë shërbime të rastësishme.\n\n"
            "9.2 Gjatë regjistrimit (ose sipas kërkesës), ju duhet të deklaroni me vërtetësi:\n"
            "- nëse veproni si tregtar (duke kryer aktivitet ekonomik) ose si individ privat;\n"
            "- nëse veproni si tregtar: emri i biznesit tuaj, numri i identifikimit tatimor (NIP/REGON për Poloninë; numri i TVSH-së ose ekuivalenti për vendet e tjera) dhe vendi i regjistrimit;\n"
            "- nëse shërbimet që ofroni kërkojnë një licencë ose leje profesionale, dhe nëse po, konfirmoni që keni autorizimin e nevojshëm.\n\n"
            "9.3 Ofruesit që veprojnë si tregtarë në Poloni duhet të japin NIP-in (numrin e identifikimit tatimor) dhe, nëse është e aplikueshme, REGON-in (numrin statistikor).\n\n"
            "9.4 Statusi juaj i tregtarit/jo-tregtarit do të shfaqet në Profilin tuaj publik, në përputhje me kërkesat e Direktivës Omnibus, duke u mundësuar Klientëve të dinë se me kë po kontraktojnë.\n\n"
            "9.5 Dhënia e informacioneve të rreme në deklaratën e tregtarit përbën një shkelje thelbësore të këtyre Kushteve për Ofruesit dhe mund të rezultojë në pezullim të menjëhershëm të llogarisë."
        ),
        "sr": (
            "9.1 Nevumo je u obavezi prema važećem zakonu (Zakon o digitalnim uslugama, Uredba P2B i zakon o zaštiti potrošača) da proveri da li Pružaoci usluga deluju kao trgovci (preduzeća) ili kao privatna lica koja nude povremene usluge.\n\n"
            "9.2 Tokom registracije (ili na zahtev), morate istinito izjaviti:\n"
            "- da li delujete kao trgovac (obavljate ekonomsku aktivnost) ili kao privatno lice;\n"
            "- ako delujete kao trgovac: naziv vašeg poslovanja, poreski identifikacioni broj (NIP/REGON za Poljsku; PDV broj ili ekvivalent za druge zemlje) i zemlju registracije;\n"
            "- da li usluge koje nudite zahtevaju profesionalnu licencu ili dozvolu, i ako je tako, potvrditi da posedujete neophodno ovlašćenje.\n\n"
            "9.3 Pružaoci usluga koji deluju kao trgovci u Poljskoj moraju da dostave svoj NIP (poreski identifikacioni broj) i, ako je primenljivo, REGON (statistički broj).\n\n"
            "9.4 Vaš status trgovca/ne-trgovca biće prikazan na vašem javnom Profilu, u skladu sa zahtevima Direktive Omnibus, omogućavajući Klijentima da znaju sa kim sklapaju ugovor.\n\n"
            "9.5 Pružanje lažnih informacija u izjavi trgovca predstavlja značajno kršenje ovih Uslova za pružaoce usluga i može rezultirati trenutnom suspenzijom naloga."
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
            
            for lang, text_val in lang_values.items():
                query = text("""
                    INSERT INTO translations (key, lang, value)
                    VALUES (:k, :l, :v)
                    ON CONFLICT (key, lang)
                    DO UPDATE SET value = EXCLUDED.value
                """)
                session.execute(query, {"k": db_key, "l": lang, "v": text_val})
                count += 1

        session.commit()
        print(f"✅ Seeded {count} translations for {NAMESPACE}.art9_body")

if __name__ == "__main__":
    seed()
