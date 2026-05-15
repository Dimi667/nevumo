"""
seed_terms_p9_bodies.py  —  Nevumo | namespace: terms
Key: art9_body (34 езика)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_terms_p9_bodies
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
    "art9_body": {
        "en": (
            '9.1 You must not use the Nevumo platform to:\n'
            '• Violate any applicable law or regulation;\n'
            '• Post false, misleading, or defamatory content;\n'
            '• Harass, threaten, or abuse other users or providers;\n'
            '• Engage in fraud or impersonation;\n'
            '• Circumvent the platform by contacting providers off-platform for the sole '
            'purpose of avoiding platform terms;\n'
            '• Submit fake reviews or manipulate the rating system;\n'
            '• Use automated tools (scrapers, bots) to access or collect data from the '
            'platform without authorisation;\n'
            '• Transmit malware, spam, or other harmful content.'
        ),
        "pl": (
            '5.1 Zabrania się dostarczania za pośrednictwem serwisu Nevumo treści o '
            'charakterze bezprawnym, w szczególności:\n'
            '• treści naruszających prawa autorskie, znaki towarowe lub inne prawa '
            'własności intelektualnej;\n'
            '• treści zniesławiających, obraźliwych, dyskryminujących lub nawołujących '
            'do nienawiści;\n'
            '• treści promujących lub ułatwiających działalność nielegalną;\n'
            '• danych osobowych osób trzecich bez ich zgody;\n'
            '• treści stanowiących spam lub niezamówiony przekaz handlowy;\n'
            '• szkodliwego oprogramowania lub kodu.\n\n'
            '5.2 W przypadku zamieszczenia treści bezprawnych Nevumo uprawnione jest do '
            'ich niezwłocznego usunięcia lub zablokowania, bez konieczności uprzedniego '
            'powiadomienia Klienta, jeżeli wymaga tego prawo lub bezpieczeństwo innych '
            'użytkowników.'
        ),
        "bg": (
            '9.1 Клиентът е длъжен да не използва платформата за:\n'
            '• нарушаване на закон или подзаконов акт;\n'
            '• публикуване на неверно, заблуждаващо или клеветническо съдържание;\n'
            '• тормоз, заплашване или злоупотреба с права на потребители или Доставчици;\n'
            '• измама или фалшиво представяне;\n'
            '• подаване на фалшиви отзиви или манипулиране на системата за оценяване;\n'
            '• автоматизиран достъп до платформата (скрейпъри, ботове) без разрешение;\n'
            '• изпращане на зловреден код, спам или вредно съдържание.'
        ),
        "cs": (
            '9.1 Platformu Nevumo nesmíte používat k:\n'
            '• porušování jakéhokoli platného zákona nebo předpisu;\n'
            '• zveřejňování nepravdivého, zavádějícího nebo hanlivého obsahu;\n'
            '• obtěžování, vyhrožování nebo zneužívání jiných uživatelů nebo poskytovatelů;\n'
            '• podvodům nebo vydávání se za jiné osoby;\n'
            '• obcházení platformy kontaktováním poskytovatelů mimo platformu za účelem '
            'vyhnutí se podmínkám;\n'
            '• odesílání falešných recenzí nebo manipulaci se systémem hodnocení;\n'
            '• používání automatizovaných nástrojů (scraperů, botů) bez povolení;\n'
            '• šíření malwaru, spamu nebo jiného škodlivého obsahu.'
        ),
        "da": (
            '9.1 Du må ikke bruge Nevumo-platformen til at:\n'
            '• Overtræde gældende lovgivning eller regulering;\n'
            '• Offentliggøre falsk, vildledende eller ærekrænkende indhold;\n'
            '• Chikanere, true eller misbruge andre brugere eller udbydere;\n'
            '• Begå bedrageri eller udgive dig for at være en anden;\n'
            '• Omgå platformen ved at kontakte udbydere uden for platformen for at undgå '
            'platformens vilkår;\n'
            '• Indsende falske anmeldelser eller manipulere vurderingssystemet;\n'
            '• Bruge automatiserede værktøjer (scrapere, bots) uden tilladelse;\n'
            '• Overføre malware, spam eller andet skadeligt indhold.'
        ),
        "de": (
            '9.1 Sie dürfen die Nevumo-Plattform nicht nutzen, um:\n'
            '• gegen geltende Gesetze oder Vorschriften zu verstoßen;\n'
            '• falsche, irreführende oder verleumderische Inhalte zu veröffentlichen;\n'
            '• andere Nutzer oder Anbieter zu belästigen, zu bedrohen oder zu missbrauchen;\n'
            '• Betrug zu begehen oder sich als eine andere Person auszugeben;\n'
            '• die Plattform zu umgehen, indem Sie Anbieter außerhalb der Plattform '
            'kontaktieren, um Plattformbedingungen zu umgehen;\n'
            '• gefälschte Bewertungen einzureichen oder das Bewertungssystem zu manipulieren;\n'
            '• automatisierte Tools (Scraper, Bots) ohne Genehmigung zu verwenden;\n'
            '• Malware, Spam oder andere schädliche Inhalte zu übertragen.'
        ),
        "el": (
            '9.1 Απαγορεύεται να χρησιμοποιείτε την πλατφόρμα Nevumo για:\n'
            '• Παραβίαση οποιουδήποτε ισχύοντος νόμου ή κανονισμού;\n'
            '• Δημοσίευση ψευδούς, παραπλανητικού ή δυσφημιστικού περιεχομένου;\n'
            '• Παρενόχληση, απειλή ή κατάχρηση άλλων χρηστών ή παρόχων;\n'
            '• Απάτη ή πλαστοπροσωπία;\n'
            '• Παράκαμψη της πλατφόρμας επικοινωνώντας με παρόχους εκτός πλατφόρμας;\n'
            '• Υποβολή ψευδών αξιολογήσεων ή χειραγώγηση του συστήματος βαθμολόγησης;\n'
            '• Χρήση αυτοματοποιημένων εργαλείων (scrapers, bots) χωρίς εξουσιοδότηση;\n'
            '• Μετάδοση κακόβουλου λογισμικού, spam ή άλλου επιβλαβούς περιεχομένου.'
        ),
        "es": (
            '9.1 No debe utilizar la plataforma Nevumo para:\n'
            '• Infringir cualquier ley o regulación aplicable;\n'
            '• Publicar contenido falso, engañoso o difamatorio;\n'
            '• Acosar, amenazar o abusar de otros usuarios o proveedores;\n'
            '• Cometer fraude o hacerse pasar por otra persona;\n'
            '• Eludir la plataforma contactando a proveedores fuera de ella para evitar '
            'sus términos;\n'
            '• Enviar reseñas falsas o manipular el sistema de calificación;\n'
            '• Utilizar herramientas automatizadas (scrapers, bots) sin autorización;\n'
            '• Transmitir malware, spam u otro contenido dañino.'
        ),
        "et": (
            '9.1 Te ei tohi Nevumo platvormi kasutada:\n'
            '• mis tahes kohaldatava seaduse või eeskirja rikkumiseks;\n'
            '• vale, eksitava või laimava sisu avaldamiseks;\n'
            '• teiste kasutajate või teenusepakkujate ahistamiseks, ähvardamiseks '
            'või kuritarvitamiseks;\n'
            '• pettuse sooritamiseks või kellena teisena esinemiseks;\n'
            '• platvormi tingimuste vältimiseks teenusepakkujatega väljaspool platvormi '
            'ühendust võttes;\n'
            '• võltsarvustuste esitamiseks või hindamissüsteemi manipuleerimiseks;\n'
            '• automatiseeritud tööriistade (scrapers, botid) kasutamiseks ilma loata;\n'
            '• pahavara, rämpsposti või muu kahjuliku sisu edastamiseks.'
        ),
        "fi": (
            '9.1 Et saa käyttää Nevumo-alustaa:\n'
            '• minkään sovellettavan lain tai säädöksen rikkomiseen;\n'
            '• väärien, harhaanjohtavien tai herjaavien sisältöjen julkaisemiseen;\n'
            '• muiden käyttäjien tai palveluntarjoajien häirintään, uhkaamiseen tai '
            'väärinkäyttöön;\n'
            '• petokseen tai henkilöllisyyden väärentämiseen;\n'
            '• alustan kiertämiseen ottamalla yhteyttä palveluntarjoajiin alustan '
            'ulkopuolella ehtojen välttämiseksi;\n'
            '• väärennösarvostelujen lähettämiseen tai arviointijärjestelmän '
            'manipuloimiseen;\n'
            '• automatisoitujen työkalujen (scrapers, botit) käyttämiseen ilman lupaa;\n'
            '• haittaohjelmien, roskapostin tai muun haitallisen sisällön lähettämiseen.'
        ),
        "fr": (
            '9.1 Vous ne devez pas utiliser la plateforme Nevumo pour :\n'
            '• Violer toute loi ou réglementation applicable ;\n'
            '• Publier du contenu faux, trompeur ou diffamatoire ;\n'
            '• Harceler, menacer ou abuser d\'autres utilisateurs ou prestataires ;\n'
            '• Commettre une fraude ou usurper l\'identité d\'une autre personne ;\n'
            '• Contourner la plateforme en contactant des prestataires hors plateforme '
            'pour éviter ses conditions ;\n'
            '• Soumettre de faux avis ou manipuler le système de notation ;\n'
            '• Utiliser des outils automatisés (scrapers, bots) sans autorisation ;\n'
            '• Transmettre des logiciels malveillants, du spam ou d\'autres contenus '
            'nuisibles.'
        ),
        "ga": (
            '9.1 Ní ceadaítear duit ardán Nevumo a úsáid chun:\n'
            '• Aon dlí nó rialachán infheidhmithe a shárú;\n'
            '• Ábhar bréagach, míthreorach nó clúmhilleach a phostáil;\n'
            '• Úsáideoirí nó soláthróirí eile a chiapadh, a bhagairt nó a mhí-úsáid;\n'
            '• Calaois a dhéanamh nó tú féin a chur i láthair mar dhuine éigin eile;\n'
            '• An t-ardán a sheachaint trí theagmháil a dhéanamh le soláthróirí lasmuigh;\n'
            '• Léirmheasanna bréige a chur isteach nó an córas rátála a ionramháil;\n'
            '• Uirlisí uathoibríocha (scrapers, bots) a úsáid gan údarú;\n'
            '• Malware, turscar nó ábhar díobhálach eile a tharchur.'
        ),
        "hr": (
            '9.1 Ne smijete koristiti platformu Nevumo za:\n'
            '• Kršenje bilo kojeg primjenjivog zakona ili propisa;\n'
            '• Objavljivanje lažnog, obmanjujućeg ili klevetnačkog sadržaja;\n'
            '• Uznemiravanje, prijetnje ili zlostavljanje korisnika ili davatelja usluga;\n'
            '• Prijevaru ili lažno predstavljanje;\n'
            '• Zaobilaženje platforme kontaktiranjem davatelja izvan platforme;\n'
            '• Slanje lažnih recenzija ili manipuliranje sustavom ocjenjivanja;\n'
            '• Korištenje automatiziranih alata (scraperi, botovi) bez dopuštenja;\n'
            '• Prenošenje zlonamjernog softvera, neželjene pošte ili drugog štetnog sadržaja.'
        ),
        "hu": (
            '9.1 A Nevumo platformot tilos a következőkre használni:\n'
            '• Bármely alkalmazandó törvény vagy szabályozás megsértése;\n'
            '• Hamis, félrevezető vagy rágalmazó tartalom közzététele;\n'
            '• Más felhasználók vagy szolgáltatók zaklatása, fenyegetése;\n'
            '• Csalás vagy más személy megszemélyesítése;\n'
            '• A platform megkerülése a feltételek elkerülése céljából;\n'
            '• Hamis értékelések benyújtása vagy az értékelési rendszer manipulálása;\n'
            '• Automatizált eszközök (scrapperek, botok) jogosulatlan használata;\n'
            '• Kártékony szoftverek, spam vagy más káros tartalmak továbbítása.'
        ),
        "is": (
            '9.1 Þér er óheimilt að nota Nevumo vettvanginn til að:\n'
            '• Brjóta í bága við gildandi lög eða reglur;\n'
            '• Birta rangar, villandi eða meiðandi efni;\n'
            '• Þjóna, ógna eða misbeita öðrum notendum eða þjónustuaðilum;\n'
            '• Fremja svik eða þykjast vera annar;\n'
            '• Sniðganga vettvanginn með því að hafa samband við þjónustuaðila utan hans;\n'
            '• Senda inn falskar umsagnir eða meðhöndla einkunnakerfi;\n'
            '• Nota sjálfvirk tæki (scrapers, bots) án leyfis;\n'
            '• Senda spilliforrit, ruslpóst eða annað skaðlegt efni.'
        ),
        "it": (
            '9.1 Non devi utilizzare la piattaforma Nevumo per:\n'
            '• Violare qualsiasi legge o regolamento applicabile;\n'
            '• Pubblicare contenuti falsi, fuorvianti o diffamatori;\n'
            '• Molestare, minacciare o abusare di altri utenti o prestatori;\n'
            '• Commettere frodi o impersonare altri;\n'
            '• Aggirare la piattaforma contattando i prestatori al di fuori di essa;\n'
            '• Inviare recensioni false o manipolare il sistema di valutazione;\n'
            '• Utilizzare strumenti automatizzati (scraper, bot) senza autorizzazione;\n'
            '• Trasmettere malware, spam o altri contenuti dannosi.'
        ),
        "lb": (
            '9.1 Dir däerft d\'Nevumo-Plattform net benotzen fir:\n'
            '• Géint gëltend Gesetzer oder Virschrëften ze verstoussen;\n'
            '• Falsch, täuschend oder verleemderegen Inhalt ze verëffentlechen;\n'
            '• Aner Benotzer oder Prestatairë ze belästigen, ze bedrohen oder ze mëssbrauchen;\n'
            '• Betrug oder Identitéitsdéifstall ze maachen;\n'
            '• D\'Plattform z\'ëmgoen andeems Dir Prestatairë ausserhalb kontaktéiert;\n'
            '• Falsch Bewäertungen anzeschreiwen oder d\'Bewäertungssystem ze manipuléieren;\n'
            '• Automatiséiert Wierkszeig (Scraper, Bots) ouni Erlabnis ze benotzen;\n'
            '• Malware, Spam oder aner schiedlechen Inhalt ze vermëttelen.'
        ),
        "lt": (
            '9.1 Negalite naudoti Nevumo platformos:\n'
            '• Pažeisti bet kokių taikomų įstatymų ar taisyklių;\n'
            '• Skelbti netikros, klaidinančios ar šmeižikiškos turinio;\n'
            '• Persekioti, grasinti ar piktnaudžiauti kitais naudotojais ar teikėjais;\n'
            '• Sukčiauti ar apsimesti kitu asmeniu;\n'
            '• Apeiti platformą susisiekiant su teikėjais už jos ribų;\n'
            '• Teikti netikrus atsiliepimus ar manipuliuoti vertinimo sistema;\n'
            '• Naudoti automatizuotus įrankius (scraperius, botus) be leidimo;\n'
            '• Perduoti kenkėjiškas programas, šlamštą ar kitą kenksmingą turinį.'
        ),
        "lv": (
            '9.1 Jums nav atļauts izmantot Nevumo platformu:\n'
            '• Jebkādu piemērojamo likumu vai noteikumu pārkāpšanai;\n'
            '• Nepatiesa, maldinošā vai apmelojošā satura publicēšanai;\n'
            '• Citu lietotāju vai sniedzēju uzmākšanās, draudēšanas vai ļaunprātīgas '
            'izmantošanas nolūkos;\n'
            '• Krāpšanai vai citas personas uzdošanās;\n'
            '• Platformas apiešanai, sazinoties ar sniedzējiem ārpus tās;\n'
            '• Viltotu atsauksmju iesniegšanai vai vērtēšanas sistēmas manipulēšanai;\n'
            '• Automatizētu rīku (scraper, botu) izmantošanai bez atļaujas;\n'
            '• Ļaunprogrammatūras, surogātpasta vai citu kaitīgu saturu pārsūtīšanai.'
        ),
        "mk": (
            '9.1 Не смеете да ја користите платформата Nevumo за:\n'
            '• Кршење на закони или прописи;\n'
            '• Објавување лажна, заблудувачка или клеветничка содржина;\n'
            '• Вознемирување, закануවање или злоупотреба на корисници или Даватели;\n'
            '• Измама или лажно претставување;\n'
            '• Заобиколување на платформата со контактирање на Даватели надвор од неа;\n'
            '• Поднесување лажни рецензии или манипулирање со системот за оценување;\n'
            '• Употреба на автоматизирани алатки (scrapers, botovi) без дозвола;\n'
            '• Пренос на малвер, спам или друга штетна содржина.'
        ),
        "mt": (
            '9.1 M\'għandekx tuża l-pjattaforma Nevumo biex:\n'
            '• Tikser kwalunkwe liġi jew regolament applikabbli;\n'
            '• Tippubblika kontenut falz, qarrieqi jew malafamanti;\n'
            '• Tħokkor, thedded jew tabbużja utenti jew fornituri oħra;\n'
            '• Tikkommetti frodi jew tippretendi li tkun xi ħadd ieħor;\n'
            '• Tagħmel il-bypass tal-pjattaforma billi tikkuntattja fornituri barra minnha;\n'
            '• Tissottometti reviżjonijiet foloz jew timmanipola s-sistema ta\' klassifikazzjoni;\n'
            '• Tuża għodod awtomatizzati (scrapers, bots) mingħajr awtorizzazzjoni;\n'
            '• Tgħaddi malware, spam jew kontenut dannuż ieħor.'
        ),
        "nl": (
            '9.1 U mag het Nevumo-platform niet gebruiken om:\n'
            '• Toepasselijke wetten of regelgeving te schenden;\n'
            '• Valse, misleidende of lasterlijke inhoud te plaatsen;\n'
            '• Andere gebruikers of providers te intimideren, bedreigen of misbruiken;\n'
            '• Fraude te plegen of zich voor te doen als iemand anders;\n'
            '• Het platform te omzeilen door providers buiten het platform te contacteren;\n'
            '• Nep-beoordelingen in te dienen of het beoordelingssysteem te manipuleren;\n'
            '• Geautomatiseerde tools (scrapers, bots) zonder toestemming te gebruiken;\n'
            '• Malware, spam of andere schadelijke inhoud te verzenden.'
        ),
        "no": (
            '9.1 Du må ikke bruke Nevumo-plattformen til å:\n'
            '• Bryte gjeldende lover eller forskrifter;\n'
            '• Publisere falsk, villedende eller ærekrenkende innhold;\n'
            '• Trakassere, true eller misbruke andre brukere eller leverandører;\n'
            '• Begå svindel eller utgi deg for å være noen andre;\n'
            '• Omgå plattformen ved å kontakte leverandører utenfor den;\n'
            '• Sende inn falske anmeldelser eller manipulere vurderingssystemet;\n'
            '• Bruke automatiserte verktøy (scrapere, bots) uten tillatelse;\n'
            '• Overføre skadevare, søppelpost eller annet skadelig innhold.'
        ),
        "pt": (
            '9.1 Você não deve usar a plataforma Nevumo para:\n'
            '• Violar qualquer lei ou regulamento aplicável;\n'
            '• Publicar conteúdo falso, enganoso ou difamatório;\n'
            '• Assediar, ameaçar ou abusar de outros usuários ou prestadores;\n'
            '• Cometer fraude ou se passar por outra pessoa;\n'
            '• Contornar a plataforma contactando prestadores fora dela;\n'
            '• Enviar avaliações falsas ou manipular o sistema de classificação;\n'
            '• Usar ferramentas automatizadas (scrapers, bots) sem autorização;\n'
            '• Transmitir malware, spam ou outro conteúdo prejudicial.'
        ),
        "pt-PT": (
            '9.1 Não deve utilizar a plataforma Nevumo para:\n'
            '• Violar qualquer lei ou regulamento aplicável;\n'
            '• Publicar conteúdo falso, enganoso ou difamatório;\n'
            '• Assediar, ameaçar ou abusar de outros utilizadores ou prestadores;\n'
            '• Cometer fraude ou fazer-se passar por outra pessoa;\n'
            '• Contornar a plataforma contactando prestadores fora dela;\n'
            '• Submeter avaliações falsas ou manipular o sistema de classificação;\n'
            '• Utilizar ferramentas automatizadas (scrapers, bots) sem autorização;\n'
            '• Transmitir malware, spam ou outro conteúdo prejudicial.'
        ),
        "ro": (
            '9.1 Nu trebuie să utilizați platforma Nevumo pentru:\n'
            '• Încălcarea oricărei legi sau reglementări aplicabile;\n'
            '• Publicarea de conținut fals, înșelător sau defăimător;\n'
            '• Hărțuirea, amenințarea sau abuzarea altor utilizatori sau prestatori;\n'
            '• Comiterea de fraudă sau uzurparea identității altei persoane;\n'
            '• Ocolirea platformei prin contactarea prestatorilor în afara acesteia;\n'
            '• Trimiterea de recenzii false sau manipularea sistemului de evaluare;\n'
            '• Utilizarea instrumentelor automate (scrapere, boți) fără autorizare;\n'
            '• Transmiterea de malware, spam sau alt conținut dăunător.'
        ),
        "ru": (
            '9.1 Вы не вправе использовать платформу Nevumo для:\n'
            '• нарушения применимых законов или нормативных актов;\n'
            '• публикации ложного, вводящего в заблуждение или клеветнического контента;\n'
            '• преследования, угроз или злоупотреблений в отношении пользователей и '
            'исполнителей;\n'
            '• мошенничества или выдачи себя за другое лицо;\n'
            '• обхода платформы путём контакта с исполнителями за её пределами;\n'
            '• публикации поддельных отзывов или манипулирования рейтинговой системой;\n'
            '• использования автоматизированных инструментов (scrapers, боты) без '
            'разрешения;\n'
            '• распространения вредоносных программ, спама или иного вредного контента.'
        ),
        "sk": (
            '9.1 Platformu Nevumo nesmíte používať na:\n'
            '• porušovanie akýchkoľvek platných zákonov alebo predpisov;\n'
            '• zverejňovanie nepravdivého, zavádzajúceho alebo hanlivého obsahu;\n'
            '• obťažovanie, vyhrážanie alebo zneužívanie iných používateľov alebo '
            'poskytovateľov;\n'
            '• podvody alebo vydávanie sa za inú osobu;\n'
            '• obchádzanie platformy kontaktovaním poskytovateľov mimo platformy;\n'
            '• odosielanie falošných recenzií alebo manipuláciu so systémom hodnotenia;\n'
            '• používanie automatizovaných nástrojov (scrapers, boty) bez povolenia;\n'
            '• šírenie malvéru, spamu alebo iného škodlivého obsahu.'
        ),
        "sl": (
            '9.1 Platforme Nevumo ne smete uporabljati za:\n'
            '• kršitev katerega koli veljavnega zakona ali predpisa;\n'
            '• objavljanje lažnih, zavajajočih ali žaljivih vsebin;\n'
            '• nadlegovanje, grožnje ali zlorabo drugih uporabnikov ali ponudnikov;\n'
            '• goljufijo ali lažno predstavljanje;\n'
            '• zaobidenje platforme z neposrednim stikanjem s ponudniki zunaj nje;\n'
            '• oddajanje lažnih ocen ali manipuliranje z ocenjevalnim sistemom;\n'
            '• uporabo avtomatiziranih orodij (scraperji, boti) brez dovoljenja;\n'
            '• prenos zlonamerne programske opreme, neželene pošte ali druge škodljive vsebine.'
        ),
        "sq": (
            '9.1 Nuk duhet të përdorni platformën Nevumo për:\n'
            '• Shkeljen e çdo ligji ose rregullimi të zbatueshëm;\n'
            '• Publikimin e përmbajtjes false, mashtruese ose shpifëse;\n'
            '• Ngacmimin, kërcënimin ose abuzimin e përdoruesve ose ofruesve të tjerë;\n'
            '• Kryerjen e mashtrimit ose paraqitjen si dikush tjetër;\n'
            '• Anashkalimin e platformës duke kontaktuar ofruesit jashtë saj;\n'
            '• Dërgimin e vlerësimeve false ose manipulimin e sistemit të vlerësimit;\n'
            '• Përdorimin e mjeteve të automatizuara (scrapers, bots) pa autorizim;\n'
            '• Transmetimin e malware, spam ose përmbajtjes tjetër të dëmshme.'
        ),
        "sr": (
            '9.1 Ne smete koristiti platformu Nevumo za:\n'
            '• Kršenje bilo kog primenjivog zakona ili propisa;\n'
            '• Objavljivanje lažnog, obmanjujućeg ili klevetničkog sadržaja;\n'
            '• Uznemiravanje, pretnje ili zlostavljanje korisnika ili pružalaca;\n'
            '• Prevaru ili lažno predstavljanje;\n'
            '• Zaobilaženje platforme kontaktiranjem pružalaca izvan nje;\n'
            '• Slanje lažnih recenzija ili manipulisanje sistemom ocenjivanja;\n'
            '• Korišćenje automatizovanih alata (scraperi, botovi) bez dozvole;\n'
            '• Prenošenje malvera, neželjene pošte ili drugog štetnog sadržaja.'
        ),
        "sv": (
            '9.1 Du får inte använda Nevumo-plattformen för att:\n'
            '• Bryta mot tillämpliga lagar eller förordningar;\n'
            '• Publicera falskt, vilseledande eller ärekränkande innehåll;\n'
            '• Trakassera, hota eller missbruka andra användare eller leverantörer;\n'
            '• Begå bedrägeri eller utge dig för att vara någon annan;\n'
            '• Kringgå plattformen genom att kontakta leverantörer utanför den;\n'
            '• Skicka in falska recensioner eller manipulera betygssystemet;\n'
            '• Använda automatiserade verktyg (scrapers, bottar) utan tillstånd;\n'
            '• Överföra skadlig programvara, skräppost eller annat skadligt innehåll.'
        ),
        "tr": (
            '9.1 Nevumo platformunu aşağıdaki amaçlarla kullanamazsınız:\n'
            '• Herhangi bir geçerli yasa veya yönetmeliği ihlal etmek;\n'
            '• Yanlış, yanıltıcı veya iftira niteliğinde içerik yayımlamak;\n'
            '• Diğer kullanıcıları veya sağlayıcıları taciz etmek, tehdit etmek;\n'
            '• Dolandırıcılık yapmak veya başka biri gibi davranmak;\n'
            '• Sağlayıcılarla platform dışında iletişim kurarak platformu atlatmak;\n'
            '• Sahte değerlendirme göndermek veya puanlama sistemini manipüle etmek;\n'
            '• Yetkisiz otomatik araçlar (scrapers, botlar) kullanmak;\n'
            '• Kötü amaçlı yazılım, spam veya zararlı içerik iletmek.'
        ),
        "uk": (
            '9.1 Вам забороняється використовувати платформу Nevumo для:\n'
            '• порушення будь-яких застосовних законів або нормативних актів;\n'
            '• публікації неправдивого, оманливого або наклепницького контенту;\n'
            '• переслідування, погроз або зловживань щодо інших користувачів чи виконавців;\n'
            '• шахрайства або видавання себе за іншу особу;\n'
            '• обходу платформи шляхом контакту з виконавцями поза нею;\n'
            '• надсилання фальшивих відгуків або маніпулювання системою оцінювання;\n'
            '• використання автоматизованих інструментів (scrapers, боти) без дозволу;\n'
            '• поширення шкідливих програм, спаму або іншого шкідливого контенту.'
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
        print(f"✅ seed_terms_p9_bodies: {count} rows upserted ({NAMESPACE}, art9_body × 34 langs)")

    engine.dispose()


if __name__ == "__main__":
    seed()
