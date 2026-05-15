"""
seed_terms_p10_bodies.py  —  Nevumo | namespace: terms
Key: art10_body (34 езика)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_terms_p10_bodies
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
    "art10_body": {
        "en": (
            '10.1 Nevumo provides the platform on an "as is" basis. While we strive for '
            'continuous availability, we do not guarantee uninterrupted access.\n\n'
            '10.2 Nevumo is not liable for:\n'
            '• The quality, safety, or outcome of services provided by third-party providers;\n'
            '• Loss of data or business interruption caused by platform unavailability;\n'
            '• Actions or omissions of service providers.\n\n'
            '10.3 [PL] Nothing in these Terms limits the mandatory consumer protection rights '
            'under Polish law (CRA — Ustawa o prawach konsumenta, as amended by the Omnibus '
            'Act 2023).\n\n'
            '10.4 Nevumo\'s total aggregate liability to you shall not exceed the total fees '
            'paid by you to Nevumo in the 12 months preceding the claim, or EUR 100, '
            'whichever is higher.'
        ),
        "pl": (
            '10.1 Nevumo udostępnia platformę w stanie "takim, jakim jest". Dążymy do '
            'zapewnienia ciągłej dostępności, ale nie gwarantujemy nieprzerwanego dostępu.\n\n'
            '10.2 Nevumo nie ponosi odpowiedzialności za:\n'
            '• jakość, bezpieczeństwo ani wynik usług świadczonych przez Usługodawców;\n'
            '• utratę danych lub przerwy w działalności spowodowane niedostępnością platformy;\n'
            '• działania lub zaniechania Usługodawców.\n\n'
            '10.3 Żadne postanowienie niniejszego Regulaminu nie ogranicza obowiązkowych '
            'praw konsumentów wynikających z ustawy o prawach konsumenta (CRA) zmienionej '
            'ustawą Omnibus 2023.\n\n'
            '10.4 Łączna odpowiedzialność Nevumo wobec Klienta nie może przekroczyć łącznych '
            'opłat uiszczonych przez Klienta na rzecz Nevumo w ciągu 12 miesięcy '
            'poprzedzających roszczenie lub kwoty 100 EUR — w zależności od tego, '
            'która kwota jest wyższa.'
        ),
        "bg": (
            '10.1 Nevumo предоставя платформата "такава, каквато е". Полагаме усилия за '
            'непрекъсната достъпност, но не гарантираме безпрепятствен достъп.\n\n'
            '10.2 Nevumo не носи отговорност за:\n'
            '• качеството, безопасността или резултата от услугите на Доставчиците;\n'
            '• загуба на данни или прекъсване на бизнес дейност поради недостъпност;\n'
            '• действия или бездействия на Доставчиците.\n\n'
            '10.3 Нищо в настоящите ОУ не ограничава задължителните права на '
            'потребителите по ЗЗП и ЗЕТ.\n\n'
            '10.4 Съвкупната отговорност на Nevumo към Клиента не може да надвишава '
            'сумата от таксите, заплатени от Клиента на Nevumo за последните 12 месеца '
            'преди предявяване на иска, или равностойността на 100 EUR — в зависимост '
            'от това коя сума е по-висока.'
        ),
        "cs": (
            '10.1 Nevumo poskytuje platformu ve stavu "tak, jak je". Usilujeme o nepřetržitou '
            'dostupnost, ale nezaručujeme nepřerušený přístup.\n\n'
            '10.2 Nevumo neodpovídá za:\n'
            '• kvalitu, bezpečnost ani výsledek služeb třetích poskytovatelů;\n'
            '• ztrátu dat nebo přerušení provozu způsobené nedostupností platformy;\n'
            '• jednání nebo opomenutí poskytovatelů služeb.\n\n'
            '10.3 [PL] Nic v těchto podmínkách neomezuje povinná práva spotřebitelů '
            'podle polského práva.\n\n'
            '10.4 Celková odpovědnost Nevumo vůči vám nepřesáhne celkové poplatky zaplacené '
            'Nevumo za 12 měsíců před nárokem, nebo 100 EUR, podle toho, co je vyšší.'
        ),
        "da": (
            '10.1 Nevumo leverer platformen "som den er". Vi stræber efter kontinuerlig '
            'tilgængelighed, men garanterer ikke uafbrudt adgang.\n\n'
            '10.2 Nevumo er ikke ansvarlig for:\n'
            '• kvaliteten, sikkerheden eller resultatet af tjenester leveret af tredjeparter;\n'
            '• tab af data eller forretningsafbrydelse forårsaget af platformens '
            'utilgængelighed;\n'
            '• tjenesteudbyderes handlinger eller undladelser.\n\n'
            '10.3 [PL] Intet i disse vilkår begrænser de obligatoriske '
            'forbrugerbeskyttelsesrettigheder i henhold til polsk ret.\n\n'
            '10.4 Nevumos samlede ansvar over for dig må ikke overstige de samlede gebyrer '
            'betalt til Nevumo i de 12 måneder forud for kravet, eller EUR 100, '
            'alt efter hvad der er højest.'
        ),
        "de": (
            '10.1 Nevumo stellt die Plattform "wie besehen" zur Verfügung. Wir streben '
            'eine ununterbrochene Verfügbarkeit an, garantieren jedoch keinen '
            'unterbrechungsfreien Zugang.\n\n'
            '10.2 Nevumo haftet nicht für:\n'
            '• die Qualität, Sicherheit oder das Ergebnis von Leistungen Dritter;\n'
            '• Datenverlust oder Betriebsunterbrechung durch Plattformausfälle;\n'
            '• Handlungen oder Unterlassungen von Dienstleistern.\n\n'
            '10.3 [PL] Nichts in diesen Bedingungen schränkt die zwingenden '
            'Verbraucherschutzrechte nach polnischem Recht ein.\n\n'
            '10.4 Die Gesamthaftung von Nevumo Ihnen gegenüber übersteigt nicht die in den '
            '12 Monaten vor dem Anspruch an Nevumo gezahlten Gebühren oder EUR 100, '
            'je nachdem, welcher Betrag höher ist.'
        ),
        "el": (
            '10.1 Το Nevumo παρέχει την πλατφόρμα "ως έχει". Φροντίζουμε για συνεχή '
            'διαθεσιμότητα, αλλά δεν εγγυόμαστε αδιάλειπτη πρόσβαση.\n\n'
            '10.2 Το Nevumo δεν φέρει ευθύνη για:\n'
            '• την ποιότητα, ασφάλεια ή αποτέλεσμα υπηρεσιών τρίτων παρόχων;\n'
            '• απώλεια δεδομένων ή διακοπή λειτουργίας λόγω μη διαθεσιμότητας;\n'
            '• ενέργειες ή παραλείψεις παρόχων υπηρεσιών.\n\n'
            '10.3 [PL] Κανένα στοιχείο αυτών των Όρων δεν περιορίζει τα υποχρεωτικά '
            'δικαιώματα καταναλωτών βάσει πολωνικού δικαίου.\n\n'
            '10.4 Η συνολική ευθύνη του Nevumo δεν υπερβαίνει τα συνολικά τέλη που '
            'καταβλήθηκαν στο Nevumo κατά τους 12 μήνες πριν από την αξίωση ή 100 EUR, '
            'όποιο ποσό είναι υψηλότερο.'
        ),
        "es": (
            '10.1 Nevumo proporciona la plataforma "tal como está". Nos esforzamos por '
            'mantener una disponibilidad continua, pero no garantizamos un acceso '
            'ininterrumpido.\n\n'
            '10.2 Nevumo no es responsable de:\n'
            '• la calidad, seguridad o resultado de los servicios de proveedores terceros;\n'
            '• pérdida de datos o interrupción del negocio por indisponibilidad;\n'
            '• acciones u omisiones de los proveedores.\n\n'
            '10.3 [PL] Nada en estos Términos limita los derechos obligatorios de '
            'protección del consumidor conforme a la ley polaca.\n\n'
            '10.4 La responsabilidad total de Nevumo no excederá las tarifas pagadas a '
            'Nevumo en los 12 meses anteriores a la reclamación, o 100 EUR, '
            'lo que sea mayor.'
        ),
        "et": (
            '10.1 Nevumo pakub platvormi "sellisena, nagu see on". Püüame tagada pideva '
            'kättesaadavuse, kuid ei garanteeri katkematut juurdepääsu.\n\n'
            '10.2 Nevumo ei vastuta:\n'
            '• kolmandate teenusepakkujate teenuste kvaliteedi, ohutuse ega tulemuse eest;\n'
            '• andmekao ega äritegevuse katkestuse eest platvormi mittetoimimise tõttu;\n'
            '• teenusepakkujate tegude ega tegematajätmiste eest.\n\n'
            '10.3 [PL] Käesolevad tingimused ei piira Poola õiguse kohaseid kohustuslikke '
            'tarbijakaitse õigusi.\n\n'
            '10.4 Nevumo kogu vastutus teie ees ei ületa Nevumole eelneva 12 kuu jooksul '
            'makstud tasusid või 100 eurot, olenevalt sellest, kumb on suurem.'
        ),
        "fi": (
            '10.1 Nevumo tarjoaa alustan "sellaisenaan". Pyrimme jatkuvaan saatavuuteen, '
            'mutta emme takaa keskeytymätöntä pääsyä.\n\n'
            '10.2 Nevumo ei ole vastuussa:\n'
            '• kolmansien palveluntarjoajien palveluiden laadusta, turvallisuudesta '
            'tai tuloksesta;\n'
            '• tietohäviöstä tai liiketoiminnan keskeytymisestä alustan '
            'saatavuusongelmien vuoksi;\n'
            '• palveluntarjoajien toimista tai laiminlyönneistä.\n\n'
            '10.3 [PL] Nämä ehdot eivät rajoita Puolan lain mukaisia pakollisia '
            'kuluttajansuojaoikeuksia.\n\n'
            '10.4 Nevumon kokonaisvastuu sinulle ei ylitä Nevumolle vaatimusta edeltävien '
            '12 kuukauden aikana maksettuja maksuja tai 100 euroa, sen mukaan, kumpi '
            'on suurempi.'
        ),
        "fr": (
            '10.1 Nevumo fournit la plateforme "en l\'état". Nous nous efforçons d\'assurer '
            'une disponibilité continue, mais ne garantissons pas un accès ininterrompu.\n\n'
            '10.2 Nevumo n\'est pas responsable de :\n'
            '• la qualité, la sécurité ou le résultat des services de prestataires tiers ;\n'
            '• la perte de données ou l\'interruption d\'activité due à l\'indisponibilité ;\n'
            '• les actes ou omissions des prestataires.\n\n'
            '10.3 [PL] Rien dans les présentes Conditions ne limite les droits obligatoires '
            'de protection des consommateurs en vertu du droit polonais.\n\n'
            '10.4 La responsabilité totale de Nevumo envers vous ne dépassera pas les frais '
            'totaux payés à Nevumo au cours des 12 mois précédant la réclamation, '
            'ou 100 EUR, le montant le plus élevé étant retenu.'
        ),
        "ga": (
            '10.1 Cuireann Nevumo an t-ardán ar fáil "mar atá sé". Déanaimid iarracht '
            'infhaighteacht leanúnach a chinntiú, ach ní ráthaímid rochtain neamhbhriste.\n\n'
            '10.2 Ní bhíonn Nevumo faoi dhliteanas as:\n'
            '• cáilíocht, sábháilteacht nó toradh seirbhísí soláthróirí tríú páirtí;\n'
            '• caillteanas sonraí nó cur isteach ar ghnó de bharr neamhinfhaighteachta;\n'
            '• gníomhartha nó neamhghníomhartha soláthróirí.\n\n'
            '10.3 [PL] Ní chuireann aon ní sna Téarmaí seo teorainn le cearta éigeantacha '
            'cosanta tomhaltóirí faoi dhlí na Polainne.\n\n'
            '10.4 Ní rachaidh dliteanas iomlán Nevumo chugat thar na táillí iomlána '
            'íoctha le Nevumo sna 12 mhí roimh an éileamh, nó EUR 100, '
            'cibé acu is airde.'
        ),
        "hr": (
            '10.1 Nevumo pruža platformu "kakva jest". Nastojimo osigurati kontinuiranu '
            'dostupnost, ali ne jamčimo neprekinut pristup.\n\n'
            '10.2 Nevumo nije odgovoran za:\n'
            '• kvalitetu, sigurnost ili ishod usluga trećih davatelja;\n'
            '• gubitak podataka ili prekid poslovanja zbog nedostupnosti platforme;\n'
            '• radnje ili propuste davatelja usluga.\n\n'
            '10.3 [PL] Ništa u ovim Uvjetima ne ograničava obvezna prava zaštite '
            'potrošača prema poljskom pravu.\n\n'
            '10.4 Ukupna odgovornost Nevumo prema vama ne prelazi ukupne naknade plaćene '
            'Nevumo u 12 mjeseci prije potraživanja ili 100 EUR, '
            'ovisno o tome što je više.'
        ),
        "hu": (
            '10.1 A Nevumo a platformot "ahogy van" alapon nyújtja. Törekszünk a folyamatos '
            'elérhetőségre, de nem garantáljuk a megszakítás nélküli hozzáférést.\n\n'
            '10.2 A Nevumo nem felel:\n'
            '• harmadik fél szolgáltatók szolgáltatásainak minőségéért, biztonságáért '
            'vagy eredményéért;\n'
            '• a platform elérhetetlensége miatti adatvesztésért vagy üzleti kiesésért;\n'
            '• a szolgáltatók cselekedeteiért vagy mulasztásaiért.\n\n'
            '10.3 [PL] Jelen feltételek semmilyen rendelkezése nem korlátozza a lengyel '
            'jog szerinti kötelező fogyasztóvédelmi jogokat.\n\n'
            '10.4 A Nevumo teljes összesített felelőssége nem haladja meg a követelést '
            'megelőző 12 hónapban Nevumónak fizetett díjak összegét vagy 100 EUR-t, '
            'attól függően, melyik összeg magasabb.'
        ),
        "is": (
            '10.1 Nevumo veitir vettvanginn "eins og hann er". Við leitumst við að tryggja '
            'stöðuga aðgengi, en ábyrgumst ekki óslitið aðgengi.\n\n'
            '10.2 Nevumo ber ekki ábyrgð á:\n'
            '• gæðum, öryggi eða niðurstöðum þjónustu þriðja aðila;\n'
            '• tapi gagna eða truflunum á rekstri vegna óaðgengis vettvangsins;\n'
            '• athöfnum eða vanrækslu þjónustuaðila.\n\n'
            '10.3 [PL] Ekkert í þessum skilmálum takmarkar lögbundin neytendaverndarréttindi '
            'samkvæmt pólskum lögum.\n\n'
            '10.4 Heildarábyrgð Nevumo gagnvart þér skal ekki vera hærri en heildargjald '
            'sem þú greiddir Nevumo á 12 mánuðunum fyrir kröfuna, eða EUR 100, '
            'hvort sem er hærra.'
        ),
        "it": (
            '10.1 Nevumo fornisce la piattaforma "così com\'è". Puntiamo alla disponibilità '
            'continua, ma non garantiamo un accesso ininterrotto.\n\n'
            '10.2 Nevumo non è responsabile per:\n'
            '• la qualità, la sicurezza o l\'esito dei servizi di terzi;\n'
            '• la perdita di dati o l\'interruzione dell\'attività causata da '
            'indisponibilità;\n'
            '• le azioni od omissioni dei prestatori.\n\n'
            '10.3 [PL] Nulla in questi Termini limita i diritti obbligatori di protezione '
            'dei consumatori ai sensi del diritto polacco.\n\n'
            '10.4 La responsabilità totale di Nevumo nei vostri confronti non supererà le '
            'commissioni totali pagate a Nevumo nei 12 mesi precedenti la richiesta, '
            'o 100 EUR, a seconda di quale importo sia maggiore.'
        ),
        "lb": (
            '10.1 Nevumo stellt d\'Plattform "wéi se ass" zur Verfügung. Mir streeven no '
            'kontinuéierlecher Verfügbarkeet, garantéieren awer keen onënnerbrochenen '
            'Zougang.\n\n'
            '10.2 Nevumo hafft net fir:\n'
            '• Qualitéit, Sécherheet oder Resultat vun Drëttparteiservice;\n'
            '• Dateverlust oder Betribsënnerbriechung duerch Plattformausfall;\n'
            '• Handlungen oder Ënnerlossungen vu Serviceprestatairen.\n\n'
            '10.3 [PL] Näischt an dësen Bedéngungen schränkt obligatoresch '
            'Konsumenteschutzrechter no poleschem Recht an.\n\n'
            '10.4 D\'Gesamthaftung vu Nevumo Iech géigeniwwer iwwerschreift net d\'Gesamtgebühren '
            'bezuelt u Nevumo an den 12 Méint virun der Fuerderung oder EUR 100, '
            'wat och ëmmer méi héich ass.'
        ),
        "lt": (
            '10.1 Nevumo teikia platformą "tokią, kokia ji yra". Siekiame užtikrinti '
            'nepertraukiamą prieinamumą, tačiau negarantuojame nepertraukiamos prieigos.\n\n'
            '10.2 Nevumo neatsako už:\n'
            '• trečiųjų šalių teikėjų paslaugų kokybę, saugumą ar rezultatą;\n'
            '• duomenų praradimą ar veiklos pertraukimą dėl platformos neprieinamumo;\n'
            '• paslaugų teikėjų veiksmus ar neveikimą.\n\n'
            '10.3 [PL] Šios sąlygos neapriboja privalomų vartotojų apsaugos teisių '
            'pagal Lenkijos teisę.\n\n'
            '10.4 Bendra Nevumo atsakomybė jums neviršys bendros sumos, sumokėtos Nevumo '
            'per 12 mėnesių iki reikalavimo, arba 100 EUR, atsižvelgiant į tai, '
            'kuri suma didesnė.'
        ),
        "lv": (
            '10.1 Nevumo nodrošina platformu "kāda tā ir". Mēs tiecamies pēc nepārtrauktas '
            'pieejamības, taču negarantējam nepārtrauktu piekļuvi.\n\n'
            '10.2 Nevumo neatbild par:\n'
            '• trešo pušu sniedzēju pakalpojumu kvalitāti, drošību vai rezultātu;\n'
            '• datu zudumu vai biznesa darbības pārtraukšanu platformas nepieejamības dēļ;\n'
            '• pakalpojumu sniedzēju rīcību vai bezdarbību.\n\n'
            '10.3 [PL] Nekas šajos noteikumos neierobežo obligātās patērētāju tiesības '
            'saskaņā ar Polijas tiesību aktiem.\n\n'
            '10.4 Nevumo kopējā atbildība pret jums nepārsniegs kopējos maksumus, '
            'samaksātus Nevumo 12 mēnešos pirms prasības, vai 100 EUR, '
            'atkarībā no tā, kurš ir lielāks.'
        ),
        "mk": (
            '10.1 Nevumo ја обезбедува платформата "каква што е". Настојуваме да '
            'обезбедиме непрекината достапност, но не гарантираме непречен пристап.\n\n'
            '10.2 Nevumo не сноси одговорност за:\n'
            '• квалитетот, безбедноста или резултатот на услугите на Давателите;\n'
            '• загуба на податоци или прекин на деловна дејност поради недостапност;\n'
            '• дејствија или пропусти на Давателите.\n\n'
            '10.3 [PL] Ништо во овие Услови не ги ограничува задолжителните права на '
            'потрошувачите според полското право.\n\n'
            '10.4 Вкупната одговорност на Nevumo не може да го надмине вкупниот износ '
            'на надоместоци платени на Nevumo во 12-те месеци пред барањето '
            'или 100 EUR, во зависност од тоа кој износ е поголем.'
        ),
        "mt": (
            '10.1 Nevumo jipprovdi l-pjattaforma "kif inhi". Nisforza biex niżguraw '
            'disponibbiltà kontinwa, iżda ma ngarantixxux aċċess mingħajr interruzzjoni.\n\n'
            '10.2 Nevumo mhuwiex responsabbli għal:\n'
            '• il-kwalità, is-sigurtà jew ir-riżultat tas-servizzi ta\' fornituri terzi;\n'
            '• telf ta\' data jew interruzzjoni tan-negozju minħabba nuqqas ta\' disponibbiltà;\n'
            '• azzjonijiet jew ommissjonijiet tal-fornituri.\n\n'
            '10.3 [PL] Xejn f\'dawn it-Termini ma jillimita d-drittijiet mandatorji ta\' '
            'protezzjoni tal-konsumatur skont il-liġi Pollakka.\n\n'
            '10.4 Ir-responsabbiltà aggregata totali ta\' Nevumo lejk ma taqbiżx it-tariffi '
            'totali mħallsa lil Nevumo fl-12-il xahar qabel it-talba, jew EUR 100, '
            'skont liema huwa ogħla.'
        ),
        "nl": (
            '10.1 Nevumo biedt het platform aan "zoals het is". We streven naar continue '
            'beschikbaarheid, maar garanderen geen ononderbroken toegang.\n\n'
            '10.2 Nevumo is niet aansprakelijk voor:\n'
            '• de kwaliteit, veiligheid of het resultaat van diensten van derde providers;\n'
            '• gegevensverlies of bedrijfsonderbreking door platformonbeschikbaarheid;\n'
            '• handelingen of nalatigheden van serviceproviders.\n\n'
            '10.3 [PL] Niets in deze Voorwaarden beperkt de verplichte '
            'consumentenbeschermingsrechten op grond van Pools recht.\n\n'
            '10.4 De totale aansprakelijkheid van Nevumo jegens u zal de totale '
            'vergoedingen die aan Nevumo zijn betaald in de 12 maanden voorafgaand aan '
            'de vordering niet overschrijden, of EUR 100, afhankelijk van welk bedrag '
            'hoger is.'
        ),
        "no": (
            '10.1 Nevumo tilbyr plattformen "som den er". Vi streber etter kontinuerlig '
            'tilgjengelighet, men garanterer ikke uavbrutt tilgang.\n\n'
            '10.2 Nevumo er ikke ansvarlig for:\n'
            '• kvaliteten, sikkerheten eller resultatet av tjenester fra tredjeparts '
            'leverandører;\n'
            '• tap av data eller driftsavbrudd forårsaket av plattformens utilgjengelighet;\n'
            '• handlinger eller unnlatelser fra tjenesteleverandører.\n\n'
            '10.3 [PL] Ingenting i disse Vilkårene begrenser de obligatoriske '
            'forbrukerbeskyttelsesrettighetene etter polsk rett.\n\n'
            '10.4 Nevumos samlede ansvar overfor deg skal ikke overstige de totale '
            'gebyrene betalt til Nevumo i de 12 månedene før kravet, eller EUR 100, '
            'avhengig av hva som er høyest.'
        ),
        "pt": (
            '10.1 O Nevumo fornece a plataforma "como está". Nos esforçamos para garantir '
            'disponibilidade contínua, mas não garantimos acesso ininterrupto.\n\n'
            '10.2 O Nevumo não é responsável por:\n'
            '• qualidade, segurança ou resultado dos serviços de terceiros;\n'
            '• perda de dados ou interrupção do negócio por indisponibilidade;\n'
            '• ações ou omissões dos prestadores.\n\n'
            '10.3 [PL] Nada nestes Termos limita os direitos obrigatórios de proteção '
            'do consumidor ao abrigo da lei polaca.\n\n'
            '10.4 A responsabilidade total do Nevumo não excederá as taxas pagas ao '
            'Nevumo nos 12 meses anteriores à reclamação ou 100 EUR, '
            'o que for mais elevado.'
        ),
        "pt-PT": (
            '10.1 O Nevumo fornece a plataforma "tal como está". Esforçamo-nos para '
            'assegurar disponibilidade contínua, mas não garantimos acesso ininterrupto.\n\n'
            '10.2 O Nevumo não é responsável por:\n'
            '• qualidade, segurança ou resultado dos serviços de terceiros;\n'
            '• perda de dados ou interrupção do negócio por indisponibilidade;\n'
            '• actos ou omissões dos prestadores.\n\n'
            '10.3 [PL] Nada nestes Termos limita os direitos obrigatórios de protecção '
            'do consumidor ao abrigo da lei polaca.\n\n'
            '10.4 A responsabilidade total do Nevumo não excederá as taxas pagas ao '
            'Nevumo nos 12 meses anteriores à reclamação ou 100 EUR, '
            'o que for mais elevado.'
        ),
        "ro": (
            '10.1 Nevumo furnizează platforma "ca atare". Depunem eforturi pentru '
            'disponibilitate continuă, dar nu garantăm acces neîntrerupt.\n\n'
            '10.2 Nevumo nu este responsabil pentru:\n'
            '• calitatea, siguranța sau rezultatul serviciilor furnizorilor terți;\n'
            '• pierderea de date sau întreruperea activității din cauza indisponibilității;\n'
            '• acțiunile sau omisiunile prestatorilor.\n\n'
            '10.3 [PL] Nimic din acești Termeni nu limitează drepturile obligatorii de '
            'protecție a consumatorilor conform legislației poloneze.\n\n'
            '10.4 Responsabilitatea totală a Nevumo față de dvs. nu va depăși taxele '
            'totale plătite Nevumo în cele 12 luni anterioare cererii, sau 100 EUR, '
            'în funcție de care sumă este mai mare.'
        ),
        "ru": (
            '10.1 Nevumo предоставляет платформу "как есть". Мы стремимся к непрерывной '
            'доступности, но не гарантируем бесперебойный доступ.\n\n'
            '10.2 Nevumo не несёт ответственности за:\n'
            '• качество, безопасность или результат услуг сторонних исполнителей;\n'
            '• потерю данных или перебои в работе из-за недоступности платформы;\n'
            '• действия или бездействие исполнителей услуг.\n\n'
            '10.3 [PL] Ничто в настоящих условиях не ограничивает обязательные права '
            'потребителей по законодательству Польши.\n\n'
            '10.4 Совокупная ответственность Nevumo перед вами не превысит сумму '
            'платежей, уплаченных Nevumo за 12 месяцев до предъявления претензии, '
            'или 100 евро — в зависимости от того, какая сумма выше.'
        ),
        "sk": (
            '10.1 Nevumo poskytuje platformu "tak, ako je". Usilujeme o nepretržitú '
            'dostupnosť, ale nezaručujeme neprerušený prístup.\n\n'
            '10.2 Nevumo nenesie zodpovednosť za:\n'
            '• kvalitu, bezpečnosť ani výsledok služieb tretích poskytovateľov;\n'
            '• stratu dát alebo prerušenie prevádzky spôsobené nedostupnosťou platformy;\n'
            '• konanie alebo opomenutia poskytovateľov.\n\n'
            '10.3 [PL] Nič v týchto podmienkach neobmedzuje povinné spotrebiteľské práva '
            'podľa poľského práva.\n\n'
            '10.4 Celková zodpovednosť Nevumo voči vám neprekročí celkové poplatky '
            'zaplatené Nevumo za 12 mesiacov pred nárokom alebo 100 EUR, '
            'podľa toho, čo je vyššie.'
        ),
        "sl": (
            '10.1 Nevumo zagotavlja platformo "kot je". Prizadevamo si za neprekinjeno '
            'razpoložljivost, vendar ne jamčimo za neprekinjeno dostopnost.\n\n'
            '10.2 Nevumo ne odgovarja za:\n'
            '• kakovost, varnost ali izid storitev tretjih ponudnikov;\n'
            '• izgubo podatkov ali prekinitev poslovanja zaradi nedostopnosti platforme;\n'
            '• dejanja ali opustitve ponudnikov storitev.\n\n'
            '10.3 [PL] Nič v teh pogojih ne omejuje obveznih pravic varstva potrošnikov '
            'po poljski zakonodaji.\n\n'
            '10.4 Skupna odgovornost Nevumo do vas ne bo presegla skupnih plačil '
            'Nevumo v 12 mesecih pred zahtevkom ali 100 EUR, '
            'odvisno od tega, kateri znesek je višji.'
        ),
        "sq": (
            '10.1 Nevumo ofron platformën "si është". Përpiqemi për disponueshmëri '
            'të vazhdueshme, por nuk garantojmë akses të pandërprerë.\n\n'
            '10.2 Nevumo nuk është përgjegjës për:\n'
            '• cilësinë, sigurinë ose rezultatin e shërbimeve të ofruesve të palëve të treta;\n'
            '• humbjen e të dhënave ose ndërprerjen e biznesit për shkak të '
            'padisponueshmërisë;\n'
            '• veprimet ose mosveprimet e ofruesve.\n\n'
            '10.3 [PL] Asgjë në këto Terma nuk kufizon të drejtat e detyrueshme të '
            'mbrojtjes së konsumatorit sipas ligjit polak.\n\n'
            '10.4 Përgjegjësia totale e Nevumo ndaj jush nuk do të tejkalojë tarifat '
            'totale të paguara Nevumo gjatë 12 muajve para kërkesës ose 100 EUR, '
            'cilado qoftë më e lartë.'
        ),
        "sr": (
            '10.1 Nevumo pruža platformu "kakva jeste". Trudimo se da obezbedimo '
            'kontinuiranu dostupnost, ali ne garantujemo neprekidan pristup.\n\n'
            '10.2 Nevumo nije odgovoran za:\n'
            '• kvalitet, bezbednost ili ishod usluga pružalaca trećih strana;\n'
            '• gubitak podataka ili prekid poslovanja usled nedostupnosti platforme;\n'
            '• radnje ili propuste pružalaca usluga.\n\n'
            '10.3 [PL] Ništa u ovim Uslovima ne ograničava obavezna prava zaštite '
            'potrošača prema poljskom pravu.\n\n'
            '10.4 Ukupna odgovornost Nevumo prema vama neće preći ukupne naknade '
            'plaćene Nevumo u 12 meseci pre potraživanja ili 100 EUR, '
            'u zavisnosti od toga šta je više.'
        ),
        "sv": (
            '10.1 Nevumo tillhandahåller plattformen "som den är". Vi strävar efter '
            'kontinuerlig tillgänglighet men garanterar inte oavbruten åtkomst.\n\n'
            '10.2 Nevumo ansvarar inte för:\n'
            '• kvaliteten, säkerheten eller resultatet av tredjepartsleverantörers tjänster;\n'
            '• dataförlust eller driftsavbrott orsakat av plattformens otillgänglighet;\n'
            '• tjänsteleverantörers handlingar eller underlåtenhet.\n\n'
            '10.3 [PL] Ingenting i dessa Villkor begränsar de obligatoriska '
            'konsumentskyddsrättigheterna enligt polsk rätt.\n\n'
            '10.4 Nevumos totala ansvar gentemot dig ska inte överstiga de totala '
            'avgifter som betalats till Nevumo under de 12 månader som föregår anspråket, '
            'eller EUR 100, beroende på vilket belopp som är högst.'
        ),
        "tr": (
            '10.1 Nevumo platformu "olduğu gibi" sunar. Sürekli erişilebilirlik için '
            'çaba gösteririz, ancak kesintisiz erişim garantisi vermeyiz.\n\n'
            '10.2 Nevumo aşağıdakilerden sorumlu değildir:\n'
            '• üçüncü taraf sağlayıcıların hizmetlerinin kalitesi, güvenliği veya sonucu;\n'
            '• platformun kullanılamaması nedeniyle veri kaybı veya iş kesintisi;\n'
            '• hizmet sağlayıcıların eylemleri veya ihmalleri.\n\n'
            '10.3 [PL] Bu Koşulların hiçbir hükmü, Polonya hukuku kapsamındaki zorunlu '
            'tüketici koruma haklarını kısıtlamaz.\n\n'
            '10.4 Nevumo\'nun size karşı toplam sorumluluğu, talep tarihinden önceki '
            '12 ay içinde Nevumo\'ya ödenen toplam ücretleri veya 100 EUR\'yu aşmayacaktır; '
            'hangisi daha yüksekse o geçerlidir.'
        ),
        "uk": (
            '10.1 Nevumo надає платформу "як є". Ми прагнемо до безперервної доступності, '
            'але не гарантуємо безперебійний доступ.\n\n'
            '10.2 Nevumo не несе відповідальності за:\n'
            '• якість, безпеку або результат послуг сторонніх виконавців;\n'
            '• втрату даних або перебої в роботі через недоступність платформи;\n'
            '• дії або бездіяльність виконавців послуг.\n\n'
            '10.3 [PL] Жодне положення цих Умов не обмежує обов\'язкових прав '
            'споживачів за законодавством Польщі.\n\n'
            '10.4 Сукупна відповідальність Nevumo перед вами не перевищить суму '
            'платежів, сплачених Nevumo за 12 місяців до подання претензії, '
            'або 100 євро — залежно від того, яка сума є вищою.'
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
        print(f"✅ seed_terms_p10_bodies: {count} rows upserted ({NAMESPACE}, art10_body × 34 langs)")

    engine.dispose()


if __name__ == "__main__":
    seed()
