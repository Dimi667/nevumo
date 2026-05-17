"""
seed_provider_terms_p18_art11_body.py  —  Nevumo | namespace: provider_terms
Key: art11_body  (1 key x 34 langs = 34 rows)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_provider_terms_p18_art11_body
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
    "art11_body": {
        "en": (
            "11.1 You have the right to access data you have submitted to the Platform, including your Profile data, Service Listings, Lead history, and reviews received, at any time through your account dashboard.\n\n"
            "11.2 **Data portability:** You may request a machine-readable export of your account data at any time via the account settings (GDPR Article 20). A maximum of one export request per 24-hour period is permitted.\n\n"
            "11.3 Nevumo will not provide access to any aggregated or anonymised data about other Providers or Clients.\n\n"
            "11.4 Upon account termination, your Profile data will be deleted or anonymised within **30 days** (except for data retained under legal obligations — see the Privacy Policy for details)."
        ),
        "bg": (
            "1. Доставчикът има право на достъп до данните, предоставени в Платформата, включително данните на Профила, Обявите за услуги, историята на Запитванията и получените отзиви, по всяко време чрез таблото за управление на акаунта.\n\n"
            "2. **Преносимост на данните:** Доставчикът може по всяко време да поиска машинно четим експорт на данните от своя акаунт чрез настройките на акаунта (чл. 20 от ОРЗД). Допустима е максимум една заявка за експорт на 24 часа.\n\n"
            "3. Nevumo няма да предоставя достъп до агрегирани или анонимизирани данни за други Доставчици или Клиенти.\n\n"
            "4. След прекратяване на акаунта данните на Профила ще бъдат изтрити или анонимизирани в рамките на **30 дни** (с изключение на данните, съхранявани на основание правни задължения — вижте Политиката за поверителност за подробности)."
        ),
        "pl": (
            "1. Dostawca ma prawo dostępu do danych przesłanych do Platformy, w tym do danych Profilu, Ofert Usług, historii Zapytań i otrzymanych opinii, w dowolnym czasie za pośrednictwem panelu konta.\n\n"
            "2. **Przenośność danych:** Dostawca może w dowolnym czasie zażądać eksportu swoich danych konta w formie nadającej się do odczytu maszynowego za pośrednictwem ustawień konta (art. 20 RODO). Dopuszczalne jest maksymalnie jedno żądanie eksportu na dobę.\n\n"
            "3. Nevumo nie udostępni żadnych zagregowanych ani zanonimizowanych danych dotyczących innych Dostawców lub Klientów.\n\n"
            "4. Po rozwiązaniu konta dane Profilu zostaną usunięte lub zanonimizowane w ciągu **30 dni** (z wyjątkiem danych przechowywanych na podstawie obowiązków prawnych — szczegóły w Polityce Prywatności)."
        ),
        "de": (
            "11.1 Sie haben das Recht, jederzeit über das Dashboard Ihres Kontos auf Daten zuzugreifen, die Sie auf der Plattform übermittelt haben, einschließlich Ihrer Profildaten, Dienstleistungsangebote, Lead-Historie und erhaltenen Bewertungen.\n\n"
            "11.2 **Datenübertragbarkeit:** Sie können jederzeit über die Kontoeinstellungen einen maschinenlesbaren Export Ihrer Kontodaten anfordern (Art. 20 DSGVO). Es ist maximal eine Exportanfrage pro 24-Stunden-Zeitraum zulässig.\n\n"
            "11.3 Nevumo gewährt keinen Zugriff auf aggregierte oder anonymisierte Daten über andere Anbieter oder Kunden.\n\n"
            "11.4 Nach Beendigung des Kontos werden Ihre Profildaten innerhalb von **30 Tagen** gelöscht oder anonymisiert (mit Ausnahme von Daten, die aufgrund gesetzlicher Verpflichtungen aufbewahrt werden — weitere Informationen finden Sie in der Datenschutzrichtlinie)."
        ),
        "fr": (
            "11.1 Vous avez le droit d'accéder aux données que vous avez soumises à la Plateforme, y compris vos données de Profil, vos annonces de services, l'historique des Leads et les avis reçus, à tout moment via le tableau de bord de votre compte.\n\n"
            "11.2 **Portabilité des données :** Vous pouvez demander une exportation lisible par machine des données de votre compte à tout moment via les paramètres du compte (Article 20 du RGPD). Un maximum d'une demande d'exportation par période de 24 heures est autorisé.\n\n"
            "11.3 Nevumo ne fournira pas d'accès à des données agrégées ou anonymisées concernant d'autres Fournisseurs ou Clients.\n\n"
            "11.4 Lors de la résiliation du compte, vos données de Profil seront supprimées ou anonymisées dans les **30 jours** (à l'exception des données conservées en vertu d'obligations légales — voir la Politique de confidentialité pour plus de détails)."
        ),
        "es": (
            "11.1 Tiene derecho a acceder a los datos que ha enviado a la Plataforma, incluidos los datos de su Perfil, los Anuncios de servicios, el historial de Clientes potenciales y las reseñas recibidas, en cualquier momento a través del panel de control de su cuenta.\n\n"
            "11.2 **Portabilidad de los datos:** Puede solicitar una exportación legible por máquina de los datos de su cuenta en cualquier momento a través de la configuración de la cuenta (Artículo 20 del RGPD). Se permite un máximo de una solicitud de exportación por período de 24 horas.\n\n"
            "11.3 Nevumo no proporcionará acceso a ningún dato agregado o anonimizado sobre otros Proveedores o Clientes.\n\n"
            "11.4 Tras la cancelación de la cuenta, los datos de su Perfil se eliminarán o anonimizarán en un plazo de **30 días** (a excepción de los datos conservados en virtud de obligaciones legales; consulte la Política de privacidad para obtener más detalles)."
        ),
        "it": (
            "11.1 Hai il diritto di accedere ai dati che hai inviato alla Piattaforma, inclusi i dati del tuo Profilo, le Offerte di Servizi, la cronologia dei Lead e le recensioni ricevute, in qualsiasi momento tramite la dashboard del tuo account.\n\n"
            "11.2 **Portabilità dei dati:** Puoi richiedere un'esportazione leggibile da dispositivo automatico dei dati del tuo account in qualsiasi momento tramite le impostazioni dell'account (Articolo 20 del GDPR). È consentita al massimo una richiesta di esportazione ogni 24 ore.\n\n"
            "11.3 Nevumo non fornirà l'accesso ad alcun dato aggregato o anonimizzato su altri Fornitori o Clienti.\n\n"
            "11.4 In seguito alla chiusura dell'account, i dati del tuo Profilo verranno eliminati o anonimizzati entro **30 giorni** (ad eccezione dei dati conservati in base a obblighi legali — consulta l'Informativa sulla privacy per i dettagli)."
        ),
        "nl": (
            "11.1 U heeft het recht om toegang te krijgen tot de gegevens die u op het Platform heeft ingediend, inclusief uw Profielgegevens, Dienstenvermeldingen, Lead-geschiedenis en ontvangen beoordelingen, op elk gewenst moment via uw account-dashboard.\n\n"
            "11.2 **Gegevensoverdraagbaarheid:** U kunt op elk gewenst moment via de accountinstellingen een machineleesbare export van uw accountgegevens aanvragen (AVG artikel 20). Maximaal één exportverzoek per periode van 24 uur is toegestaan.\n\n"
            "11.3 Nevumo zal geen toegang verlenen tot enige geaggregeerde of geanonimiseerde gegevens over andere Dienstverleners of Klanten.\n\n"
            "11.4 Bij beëindiging van het account worden uw Profielgegevens binnen **30 dagen** verwijderd of geanonimiseerd (met uitzondering van gegevens die op grond van wettelijke verplichtingen worden bewaard — zie het Privacybeleid voor details)."
        ),
        "pt": (
            "11.1 Tem o direito de aceder aos dados que enviou para a Plataforma, incluindo os dados do seu Perfil, Anúncios de Serviços, histórico de Leads e avaliações recebidas, a qualquer momento através do painel da sua conta.\n\n"
            "11.2 **Portabilidade de dados:** Pode solicitar uma exportação legível por máquina dos dados da sua conta a qualquer momento através das configurações da conta (Artigo 20.º do RGPD). É permitido um máximo de um pedido de exportação por período de 24 horas.\n\n"
            "11.3 A Nevumo não fornecerá acesso a quaisquer dados agregados ou anonimizados sobre outros Prestadores ou Clientes.\n\n"
            "11.4 Após a rescisão da conta, os dados do seu Perfil serão eliminados ou anonimizados num prazo de **30 dias** (exceto para dados retidos ao abrigo de obrigações legais — consulte a Política de Privacidade para mais detalhes)."
        ),
        "pt-PT": (
            "11.1 Tem o direito de aceder aos dados que enviou para a Plataforma, incluindo os dados do seu Perfil, Anúncios de Serviços, histórico de Leads e avaliações recebidas, a qualquer momento através do painel da sua conta.\n\n"
            "11.2 **Portabilidade de dados:** Pode solicitar uma exportação legível por máquina dos dados da sua conta a qualquer momento através das configurações da conta (Artigo 20.º do RGPD). É permitido um máximo de um pedido de exportação por período de 24 horas.\n\n"
            "11.3 A Nevumo não fornecerá acesso a quaisquer dados agregados ou anonimizados sobre outros Prestadores ou Clientes.\n\n"
            "11.4 Após a rescisão da conta, os dados do seu Perfil serão eliminados ou anonimizados num prazo de **30 dias** (exceto para dados retidos ao abrigo de obrigações legais — consulte a Política de Privacidade para mais detalhes)."
        ),
        "ro": (
            "11.1 Aveți dreptul de a accesa datele pe care le-ați trimis Platformei, inclusiv datele Profilului dvs., Listele de servicii, istoricul Lead-urilor și recenziile primite, în orice moment, prin intermediul tabloului de bord al contului dvs.\n\n"
            "11.2 **Portabilitatea datelor:** Puteți solicita un export care poate fi citit de mașină al datelor contului dvs. în orice moment prin setările contului (Articolul 20 GDPR). Este permisă o solicitare de export maximă per perioadă de 24 de ore.\n\n"
            "11.3 Nevumo nu va oferi acces la nicio dată agregată sau anonimizată despre alți Furnizori sau Clienți.\n\n"
            "11.4 La închiderea contului, datele Profilului dumneavoastră vor fi șterse sau anonimizate în termen de **30 de zile** (cu excepția datelor reținute în temeiul obligațiilor legale — consultați Politica de confidențialitate pentru detalii)."
        ),
        "ru": (
            "11.1 Вы имеете право доступа к данным, которые вы предоставили Платформе, включая данные вашего Профиля, Списки услуг, историю Лидов и полученные отзывы, в любое время через панель управления вашей учетной записи.\n\n"
            "11.2 **Переносимость данных:** Вы можете запросить машиночитаемый экспорт данных вашей учетной записи в любое время через настройки учетной записи (статья 20 GDPR). Разрешается не более одного запроса на экспорт в течение 24 часов.\n\n"
            "11.3 Nevumo не будет предоставлять доступ к любым агрегированным или анонимизированным данным о других Поставщиках или Клиентах.\n\n"
            "11.4 При закрытии учетной записи данные вашего Профиля будут удалены или анонимизированы в течение **30 дней** (за исключением данных, сохраняемых в соответствии с юридическими обязательствами — подробности см. в Политике конфиденциальности)."
        ),
        "uk": (
            "11.1 Ви маєте право доступу до даних, які ви надали Платформі, включаючи дані вашого Профілю, Списки послуг, історію Лідів і отримані відгуки, в будь-який час через панель керування вашого облікового запису.\n\n"
            "11.2 **Переносимість даних:** Ви можете запросити машинозчитуваний експорт даних вашого облікового запису в будь-який час через налаштування облікового запису (стаття 20 GDPR). Дозволяється не більше одного запиту на експорт протягом 24 годин.\n\n"
            "11.3 Nevumo не надаватиме доступ до будь-яких агрегованих або анонімізованих даних про інших Постачальників або Клієнтів.\n\n"
            "11.4 Після закриття облікового запису дані вашого Профілю будуть видалені або анонімізовані протягом **30 днів** (за винятком даних, збережених відповідно до юридичних зобов'язань — подробиці див. у Політиці конфіденційності)."
        ),
        "cs": (
            "11.1 Máte právo kdykoli prostřednictvím řídicího panelu svého účtu přistupovat k údajům, které jste poskytli platformě, včetně údajů o vašem profilu, nabídek služeb, historie potenciálních zákazníků a obdržených recenzí.\n\n"
            "11.2 **Přenositelnost údajů:** Prostřednictvím nastavení účtu můžete kdykoli požádat o strojově čitelný export údajů o svém účtu (článek 20 GDPR). Je povolen maximálně jeden požadavek na export za 24 hodin.\n\n"
            "11.3 Společnost Nevumo neposkytne přístup k žádným agregovaným nebo anonymizovaným údajům o jiných poskytovatelích nebo klientech.\n\n"
            "11.4 Po ukončení účtu budou údaje o vašem profilu smazány nebo anonymizovány do **30 dnů** (s výjimkou údajů uchovávaných na základě zákonných povinností – podrobnosti viz Zásady ochrany osobních údajů)."
        ),
        "da": (
            "11.1 Du har til enhver tid ret til at få adgang til de data, du har indsendt til platformen, herunder dine profildata, tjenesteopslag, lead-historik og modtagne anmeldelser, via dit konto-dashboard.\n\n"
            "11.2 **Dataportabilitet:** Du kan til enhver tid anmode om en maskinlæsbar eksport af dine kontodata via kontoindstillingerne (GDPR artikel 20). Der tillades maksimalt én eksportanmodning pr. 24-timers periode.\n\n"
            "11.3 Nevumo giver ikke adgang til nogen aggregerede eller anonymiserede data om andre udbydere eller kunder.\n\n"
            "11.4 Ved kontoopsigelse vil dine profildata blive slettet eller anonymiseret inden for **30 dage** (bortset fra data opbevaret i henhold til juridiske forpligtelser — se privatlivspolitikken for detaljer)."
        ),
        "sv": (
            "11.1 Du har rätt att när som helst komma åt data som du har skickat in till plattformen, inklusive din profildata, tjänsteannonser, lead-historik och mottagna recensioner, via din kontoinstrumentpanel.\n\n"
            "11.2 **Dataportabilitet:** Du kan begära en maskinläsbar export av din kontodata när som helst via kontoinställningarna (GDPR artikel 20). Max en exportbegäran per 24-timmarsperiod är tillåten.\n\n"
            "11.3 Nevumo kommer inte att ge tillgång till någon aggregerad eller anonymiserad data om andra leverantörer eller kunder.\n\n"
            "11.4 Vid kontouppsägning kommer din profildata att raderas eller anonymiseras inom **30 dagar** (förutom data som behålls enligt juridiska skyldigheter — se integritetspolicyn för mer information)."
        ),
        "no": (
            "11.1 Du har rett til å få tilgang til data du har sendt inn til plattformen, inkludert profildataene dine, tjenesteoppføringer, lead-historikk og mottatte anmeldelser, når som helst via kontodashbordet ditt.\n\n"
            "11.2 **Dataportabilitet:** Du kan når som helst be om en maskinlesbar eksport av kontodataene dine via kontoinnstillingene (GDPR artikkel 20). Maksimalt én eksportforespørsel per 24-timers periode er tillatt.\n\n"
            "11.3 Nevumo vil ikke gi tilgang til noen aggregerte eller anonymiserte data om andre leverandører eller kunder.\n\n"
            "11.4 Ved kontooppsigelse vil profildataene dine bli slettet eller anonymisert innen **30 dager** (unntatt data som beholdes under juridiske forpliktelser — se personvernerklæringen for detaljer)."
        ),
        "fi": (
            "11.1 Sinulla on oikeus saada pääsy alustalle lähettämiisi tietoihin, mukaan lukien profiilitietosi, palveluilmoituksesi, liidihistoriasi ja saamasi arvostelut, milloin tahansa tilisi hallintapaneelin kautta.\n\n"
            "11.2 **Tietojen siirrettävyys:** Voit pyytää tilisi tietojen koneellisesti luettavaa vientiä milloin tahansa tilin asetusten kautta (GDPR:n artikla 20). Enintään yksi vientipyyntö 24 tunnin aikana on sallittu.\n\n"
            "11.3 Nevumo ei tarjoa pääsyä muihin palveluntarjoajiin tai asiakkaisiin liittyviin koottuihin tai anonymisoituihin tietoihin.\n\n"
            "11.4 Tilin irtisanomisen jälkeen profiilitietosi poistetaan tai anonymisoidaan **30 päivän** kuluessa (lukuun ottamatta lakisääteisten velvoitteiden nojalla säilytettäviä tietoja — katso lisätietoja tietosuojakäytännöstä)."
        ),
        "et": (
            "11.1 Teil on õigus pääseda juurde andmetele, mille olete platvormile esitanud, sealhulgas oma profiiliandmetele, teenuste loenditele, müügivihjete ajaloole ja saadud arvustustele igal ajal oma konto juhtpaneeli kaudu.\n\n"
            "11.2 **Andmete ülekantavus:** Võite igal ajal konto seadete kaudu taotleda oma konto andmete masinloetavat eksporti (GDPR artikkel 20). Lubatud on maksimaalselt üks eksporditaotlus 24-tunnise perioodi jooksul.\n\n"
            "11.3 Nevumo ei paku juurdepääsu muude teenusepakkujate või klientide koond- või anonüümseks muudetud andmetele.\n\n"
            "11.4 Konto lõpetamisel kustutatakse või muudetakse teie profiiliandmed anonüümseks **30 päeva** jooksul (välja arvatud andmed, mida säilitatakse seadusest tulenevate kohustuste alusel — üksikasju vaadake privaatsuspoliitikast)."
        ),
        "lt": (
            "11.1 Jūs turite teisę bet kada per savo paskyros prietaisų skydelį pasiekti duomenis, kuriuos pateikėte platformai, įskaitant savo profilio duomenis, paslaugų sąrašus, potencialių klientų istoriją ir gautus atsiliepimus.\n\n"
            "11.2 **Duomenų perkeliamumas:** Bet kuriuo metu per paskyros nustatymus galite paprašyti kompiuterio skaitomo jūsų paskyros duomenų eksporto (BDAR 20 straipsnis). Leidžiama pateikti ne daugiau kaip vieną eksporto prašymą per 24 valandų laikotarpį.\n\n"
            "11.3 Nevumo nesuteiks prieigos prie jokių apibendrintų ar anonimizuotų duomenų apie kitus paslaugų teikėjus ar klientus.\n\n"
            "11.4 Nutraukus paskyrą, jūsų profilio duomenys bus ištrinti arba anonimizuoti per **30 dienų** (išskyrus duomenis, saugomus pagal teisinius įsipareigojimus — daugiau informacijos rasite privatumo politikoje)."
        ),
        "lv": (
            "11.1 Jums ir tiesības jebkurā laikā, izmantojot sava konta informācijas paneli, piekļūt datiem, kurus esat iesniedzis Platformai, tostarp sava Profila datiem, Pakalpojumu sarakstiem, Interesentu vēsturei un saņemtajām atsauksmēm.\n\n"
            "11.2 **Datu pārnesamība:** Jūs jebkurā laikā, izmantojot konta iestatījumus, varat pieprasīt sava konta datu mašīnlasāmu eksportu (VDAR 20. pants). Ir atļauts ne vairāk kā viens eksporta pieprasījums 24 stundu periodā.\n\n"
            "11.3 Nevumo nenodrošinās piekļuvi nekādiem apkopotiem vai anonimizētiem datiem par citiem Pakalpojumu sniedzējiem vai Klientiem.\n\n"
            "11.4 Pēc konta darbības izbeigšanas jūsu Profila dati tiks dzēsti vai anonimizēti **30 dienu** laikā (izņemot datus, kas tiek saglabāti saskaņā ar juridiskajām saistībām — sīkāku informāciju skatiet Konfidencialitātes politikā)."
        ),
        "hu": (
            "11.1 Bármikor, a fiókja irányítópultján keresztül jogosult hozzáférni a Platformra feltöltött adataihoz, beleértve a profiladatait, a szolgáltatáslistáit, a leadek előzményeit és a kapott véleményeket.\n\n"
            "11.2 **Adathordozhatóság:** Fiókja beállításain keresztül bármikor kérheti fiókadatai géppel olvasható formátumú exportálását (GDPR 20. cikk). 24 óránként legfeljebb egy exportálási kérés megengedett.\n\n"
            "11.3 A Nevumo nem biztosít hozzáférést a többi Szolgáltatóra vagy Ügyfélre vonatkozó összesített vagy anonimizált adatokhoz.\n\n"
            "11.4 A fiók megszüntetésekor profiladatait **30 napon** belül törlik vagy anonimizálják (kivéve a jogi kötelezettségek miatt megőrzött adatokat — a részletekért lásd az Adatvédelmi irányelvet)."
        ),
        "hr": (
            "11.1 Imate pravo u bilo kojem trenutku putem nadzorne ploče svog računa pristupiti podacima koje ste unijeli na Platformu, uključujući podatke o vašem Profilu, Popisima usluga, povijesti potencijalnih klijenata i primljenim recenzijama.\n\n"
            "11.2 **Prenosivost podataka:** Možete zatražiti strojno čitljiv izvoz podataka sa svog računa u bilo kojem trenutku putem postavki računa (GDPR članak 20.). Dopušten je najviše jedan zahtjev za izvoz u razdoblju od 24 sata.\n\n"
            "11.3 Nevumo neće omogućiti pristup nikakvim agregiranim ili anonimiziranim podacima o drugim Pružateljima usluga ili Klijentima.\n\n"
            "11.4 Nakon zatvaranja računa, podaci o vašem Profilu bit će izbrisani ili anonimizirani u roku od **30 dana** (osim podataka koji se zadržavaju pod zakonskim obvezama — pogledajte Politiku privatnosti za detalje)."
        ),
        "sk": (
            "11.1 Máte právo kedykoľvek prostredníctvom riadiaceho panela svojho účtu pristupovať k údajom, ktoré ste poskytli platforme, vrátane údajov o vašom profile, ponúk služieb, histórie potenciálnych zákazníkov a prijatých recenzií.\n\n"
            "11.2 **Prenositeľnosť údajov:** Prostredníctvom nastavení účtu môžete kedykoľvek požiadať o strojovo čitateľný export údajov o svojom účte (článok 20 GDPR). Je povolená maximálne jedna žiadosť o export za 24 hodín.\n\n"
            "11.3 Spoločnosť Nevumo neposkytne prístup k žiadnym agregovaným alebo anonymizovaným údajom o iných poskytovateľoch alebo klientoch.\n\n"
            "11.4 Po ukončení účtu budú údaje o vašom profile vymazané alebo anonymizované do **30 dní** (s výnimkou údajov uchovávaných na základe zákonných povinností – podrobnosti nájdete v Zásadách ochrany osobných údajov)."
        ),
        "sl": (
            "11.1 Pravico imate, da kadar koli prek nadzorne plošče svojega računa dostopate do podatkov, ki ste jih predložili platformi, vključno s podatki o svojem profilu, seznami storitev, zgodovino potencialnih strank in prejetimi ocenami.\n\n"
            "11.2 **Prenosljivost podatkov:** Preko nastavitev računa lahko kadar koli zahtevate strojno berljiv izvoz podatkov svojega računa (člen 20 GDPR). Dovoljena je največ ena zahteva za izvoz v 24 urah.\n\n"
            "11.3 Nevumo ne bo omogočil dostopa do nobenih združenih ali anonimiziranih podatkov o drugih ponudnikih ali strankah.\n\n"
            "11.4 Po prekinitvi računa bodo podatki vašega profila izbrisani ali anonimizirani v **30 dneh** (razen za podatke, ki se hranijo na podlagi pravnih obveznosti — za podrobnosti glejte Pravilnik o zasebnosti)."
        ),
        "el": (
            "11.1 Έχετε το δικαίωμα πρόσβασης στα δεδομένα που έχετε υποβάλει στην Πλατφόρμα, συμπεριλαμβανομένων των δεδομένων του Προφίλ σας, των Καταχωρίσεων Υπηρεσιών, του ιστορικού Πελατών και των κριτικών που έχετε λάβει, ανά πάσα στιγμή μέσω του πίνακα ελέγχου του λογαριασμού σας.\n\n"
            "11.2 **Φορητότητα δεδομένων:** Μπορείτε να ζητήσετε μια μηχανικώς αναγνώσιμη εξαγωγή των δεδομένων του λογαριασμού σας ανά πάσα στιγμή μέσω των ρυθμίσεων του λογαριασμού (Άρθρο 20 του ΓΚΠΔ). Επιτρέπεται κατ' ανώτατο όριο ένα αίτημα εξαγωγής ανά περίοδο 24 ωρών.\n\n"
            "11.3 Η Nevumo δεν θα παρέχει πρόσβαση σε συγκεντρωτικά ή ανωνυμοποιημένα δεδομένα σχετικά με άλλους Παρόχους ή Πελάτες.\n\n"
            "11.4 Κατά τον τερματισμό του λογαριασμού, τα δεδομένα του Προφίλ σας θα διαγραφούν ή θα ανωνυμοποιηθούν εντός **30 ημερών** (εκτός από τα δεδομένα που διατηρούνται βάσει νομικών υποχρεώσεων — δείτε την Πολιτική Απορρήτου για λεπτομέρειες)."
        ),
        "tr": (
            "11.1 Profil verileriniz, Hizmet İlanlarınız, Potansiyel Müşteri geçmişiniz ve alınan incelemeler dahil olmak üzere Platforma gönderdiğiniz verilere hesap kontrol paneliniz aracılığıyla istediğiniz zaman erişme hakkına sahipsiniz.\n\n"
            "11.2 **Veri taşınabilirliği:** Hesap ayarları aracılığıyla istediğiniz zaman hesap verilerinizin makine tarafından okunabilir bir şekilde dışa aktarılmasını talep edebilirsiniz (GDPR Madde 20). Her 24 saatlik dönemde en fazla bir dışa aktarma talebine izin verilir.\n\n"
            "11.3 Nevumo, diğer Sağlayıcılar veya Müşteriler hakkında toplanmış veya anonimleştirilmiş verilere erişim sağlamayacaktır.\n\n"
            "11.4 Hesabın feshedilmesi üzerine, Profil verileriniz **30 gün** içinde silinecek veya anonimleştirilecektir (yasal yükümlülükler uyarınca tutulan veriler hariç — ayrıntılar için Gizlilik Politikasına bakın)."
        ),
        "ga": (
            "11.1 Tá deart agat rochtain a fháil ar shonraí atá curtha isteach agat chuig an Ardán, lena n-áirítear do shonraí Próifíle, Liostaí Seirbhíse, stair Luaidhe, agus léirmheasanna a fuarthas, amhálacha trí dheais do chuntais.\n\n"
            "11.2 **Iniomparthacht sonraí:** Féadfaidh tú onnmhairiú atá inléite ag meaisín de shonraí do chuntais a iarraidh amhálacha trí na socruithe cuntais (Airteagal 20 den GDPR). Ceadaítear uasmhéid iarratais onnmhairithe amháin in aghaidh na tréimhse 24 uair an chloig.\n\n"
            "11.3 Ní sholáthróidh Nevumo rochtain ar aon sonraí comhiomlánaithe nó gan ainm faoi Sholáthraithe nó Cliaint eile.\n\n"
            "11.4 Ar fhoirceannadh an chuntais, scriosfar nó déanfar do shonraí Próifíle gan ainm laistigh de **30 lá** (seachas sonraí a choinnítear faoi oibleagáidí dlíthiúla — féach an Beartas Príobháideachais le haghaidh sonraí)."
        ),
        "is": (
            "11.1 Þú hefur rétt til aðgangs að gögnum sem þú hefur sent inn á vettvanginn, þar á meðal prófílgögn, þjónustuskráningar, sögu áhugasamra og mótteknar umsagnir, hvenær sem er í gegnum stjórnborð reikningsins þíns.\n\n"
            "11.2 **Gagnaflutningur:** Þú getur óskað eftir véllesanlegum útflutningi á gögnum reikningsins þíns hvenær sem er í gegnum reikningsstillingarnar (GDPR 20. grein). Að hámarki er leyfð ein beiðni um útflutning á hverju 24 klukkustunda tímabili.\n\n"
            "11.3 Nevumo mun ekki veita aðgang að neinum uppsöfnuðum eða nafnlausum gögnum um aðra þjónustuveitendur eða viðskiptavini.\n\n"
            "11.4 Við uppsögn reiknings verða prófílgögnin þín eytt eða gerð nafnlaus innan **30 daga** (að undanskildum gögnum sem geymd eru vegna lagalegra skyldna — sjá persónuverndarstefnuna fyrir nánari upplýsingar)."
        ),
        "lb": (
            "11.1 Dir hutt d'Recht Zougang zu Daten ze kréien déi Dir op d'Plattform agereecht hutt, inklusiv Är Profildaten, Serviceoplëschtungen, Lead-Historie an erhalen Bewäertungen, zu all Moment iwwer Äre Kont-Dashboard.\n\n"
            "11.2 **Dateportabilitéit:** Dir kënnt zu all Moment iwwer d'Kontastellungen e maschinne-liesbaren Export vun Äre Kontdaten ufroen (GDPR Artikel 20). Maximal eng Exportufro pro 24-Stonnen-Period ass erlaabt.\n\n"
            "11.3 Nevumo wäert keen Zougang zu aggregéierten oder anonymiséierten Daten iwwer aner Ubidder oder Clienten ubidden.\n\n"
            "11.4 Bei der Kënnegung vum Kont ginn Är Profildaten bannent **30 Deeg** geläscht oder anonymiséiert (ausser fir Daten déi ënner gesetzleche Verpflichtungen zeréckbehale ginn — kuckt d'Dateschutzrichtlinn fir Detailer)."
        ),
        "mk": (
            "11.1 Имате право на пристап до податоците што сте ги поднеле до Платформата, вклучувајќи ги вашите податоци на Профилот, Листите на услуги, историјата на Потенцијални клиенти и добиените прегледи, во кое било време преку контролната табла на вашиот профил.\n\n"
            "11.2 **Преносливост на податоци:** Можете да побарате машински читлив извоз на податоците од вашиот профил во кое било време преку поставките на профилот (Член 20 од ГДПР). Дозволено е најмногу едно барање за извоз на период од 24 часа.\n\n"
            "11.3 Nevumo нема да обезбеди пристап до какви било агрегирани или анонимизирани податоци за други Даватели или Клиенти.\n\n"
            "11.4 По раскинувањето на профилот, вашите податоци на Профилот ќе бидат избришани или анонимизирани во рок од **30 дена** (со исклучок на податоците што се задржуваат според законски обврски — видете ја Политиката за приватност за детали)."
        ),
        "mt": (
            "11.1 Għandek id-dritt li taċċessa d-dejta li tkun issottomettejt lill-Pjattaforma, inkluż id-dejta tal-Profil tiegħek, Listi tas-Servizzi, istorja ta' Leads, u reviżjonijiet riċevuti, fi kwalunkwe ħin permezz tad-dashboard tal-kont tiegħek.\n\n"
            "11.2 **Portabbiltà tad-dejta:** Tista' titlob esportazzjoni li tinqara mill-magni tad-dejta tal-kont tiegħek fi kwalunkwe ħin permezz tas-settings tal-kont (Artikolu 20 tal-GDPR). Massimu ta' talba ta' esportazzjoni waħda għal kull perjodu ta' 24 siegħa huwa permess.\n\n"
            "11.3 Nevumo mhux se jipprovdi aċċess għal kwalunkwe dejta aggregata jew anonimizzata dwar Fornituri jew Klijenti oħra.\n\n"
            "11.4 Mat-terminazzjoni tal-kont, id-dejta tal-Profil tiegħek se titħassar jew issir anonima fi żmien **30 jum** (ħlief għal dejta miżmuma taħt obbligi legali — ara l-Politika tal-Privatezza għad-dettalji)."
        ),
        "sq": (
            "11.1 Ju keni të drejtë të aksesoni të dhënat që keni dërguar në Platformë, duke përfshirë të dhënat e Profilin tuaj, Listimet e Shërbimeve, historinë e Klientëve potencialë dhe rishikimet e marra, në çdo kohë përmes panelit të llogarisë suaj.\n\n"
            "11.2 **Transportueshmëria e të dhënave:** Ju mund të kërkoni një eksport të lexueshëm nga makina të të dhënave të llogarisë suaj në çdo kohë përmes cilësimeve të llogarisë (Neni 20 i GDPR). Lejohet maksimumi një kërkesë eksporti për periudhë 24-orëshe.\n\n"
            "11.3 Nevumo nuk do të ofrojë akses në asnjë të dhënë të grumbulluar ose të anonimizuar në lidhje me Ofruesit ose Klientët e tjerë.\n\n"
            "11.4 Pas përfundimit të llogarisë, të dhënat e Profilin tuaj do të fshihen ose do të anonimizohen brenda **30 ditëve** (përveç të dhënave të mbajtura sipas detyrimeve ligjore — shih Politikën e Privatësisë për detaje)."
        ),
        "sr": (
            "11.1 Imate pravo da u bilo kom trenutku putem kontrolne table svog naloga pristupite podacima koje ste dostavili Platformi, uključujući podatke o vašem Profilu, Oglase usluga, istoriju potencijalnih klijenata i primljene recenzije.\n\n"
            "11.2 **Prenosivost podataka:** Možete da zatražite mašinski čitljiv izvoz podataka sa svog naloga u bilo kom trenutku putem podešavanja naloga (Član 20 GDPR-a). Dozvoljen je najviše jedan zahtev za izvoz u periodu od 24 sata.\n\n"
            "11.3 Nevumo neće obezbediti pristup bilo kakvim agregiranim ili anonimizovanim podacima o drugim Pružaocima usluga ili Klijentima.\n\n"
            "11.4 Nakon zatvaranja naloga, podaci o vašem Profilu biće izbrisani ili anonimizovani u roku od **30 dana** (osim podataka koji se zadržavaju pod zakonskim obavezama — pogledajte Politiku privatnosti za detalje)."
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
        print(f"✅ Seeded {count} translations for {NAMESPACE}.art11_body")

if __name__ == "__main__":
    seed()
