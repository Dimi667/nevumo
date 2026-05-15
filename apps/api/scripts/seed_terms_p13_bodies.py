"""
seed_terms_p13_bodies.py  —  Nevumo | namespace: terms
Key: art13_body (34 езика)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_terms_p13_bodies
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
    "art13_body": {
        "en": (
            '13.1 These Terms are governed by the law of Bulgaria.\n\n'
            '13.2 If you are a consumer residing in another EU/EEA member state, the '
            'mandatory consumer protection provisions of your country of residence also '
            'apply and cannot be excluded by these Terms.\n\n'
            '13.3 Any dispute that cannot be resolved through the complaint procedure or '
            'ADR shall be submitted to the competent courts of Bulgaria, without prejudice '
            'to your right to bring proceedings in the courts of your country of residence.'
        ),
        "pl": (
            '13.1 Niniejszy Regulamin podlega prawu bułgarskiemu.\n\n'
            '13.2 W stosunku do Klientów będących konsumentami zamieszkałymi w Polsce lub '
            'innym kraju UE/EOG, zastosowanie mają obligatoryjne przepisy ochrony '
            'konsumentów obowiązujące w kraju zamieszkania Klienta — w zakresie, w jakim '
            'zapewniają Klientowi wyższy poziom ochrony niż prawo bułgarskie.\n\n'
            '13.3 Wszelkie spory, których nie uda się rozwiązać w drodze postępowania '
            'reklamacyjnego lub ADR, rozstrzygane są przez sądy właściwe dla siedziby '
            'Nevumo w Bułgarii — bez uszczerbku dla prawa Klienta będącego konsumentem '
            'do dochodzenia roszczeń przed sądem właściwym dla jego miejsca zamieszkania.'
        ),
        "bg": (
            '13.1 Настоящите ОУ се уреждат от законодателството на Република България.\n\n'
            '13.2 Спрямо Клиенти — потребители с местоживеене в друга държава — членка '
            'на ЕС/ЕИП се прилагат и задължителните разпоредби за защита на потребителите, '
            'действащи в държавата на пребиваване на Клиента, в степента, в която те '
            'осигуряват по-висока защита.\n\n'
            '13.3 Споровете, неразрешени по реда на рекламационната процедура или АРС, '
            'се отнасят за разглеждане от компетентния съд в гр. София, България, без '
            'да се засяга правото на потребителя да предяви иск пред съда по '
            'местоживеенето му.'
        ),
        "cs": (
            '13.1 Tyto podmínky se řídí bulharským právem.\n\n'
            '13.2 Pokud jste spotřebitel s bydlištěm v jiném členském státě EU/EHP, '
            'platí také povinné spotřebitelské ochrany vaší země bydliště v rozsahu, '
            'v jakém poskytují vyšší ochranu.\n\n'
            '13.3 Spory, které nelze vyřešit reklamačním řízením nebo ADR, budou '
            'předloženy příslušným soudům Bulharska, aniž by bylo dotčeno vaše právo '
            'podat žalobu u soudu ve vaší zemi bydliště.'
        ),
        "da": (
            '13.1 Disse vilkår er underlagt bulgarsk ret.\n\n'
            '13.2 Hvis du er forbruger med bopæl i en anden EU/EØS-medlemsstat, '
            'gælder også de obligatoriske forbrugerbeskyttelsesbestemmelser i dit '
            'bopælsland i det omfang, de giver højere beskyttelse.\n\n'
            '13.3 Tvister, der ikke kan løses via klageprocedure eller ADR, indgives '
            'til de kompetente domstole i Bulgarien, dog uden at det berører din ret '
            'til at anlægge sag i dit bopælsland.'
        ),
        "de": (
            '13.1 Diese Bedingungen unterliegen dem bulgarischen Recht.\n\n'
            '13.2 Wenn Sie Verbraucher mit Wohnsitz in einem anderen EU/EWR-Mitgliedstaat '
            'sind, gelten auch die zwingenden Verbraucherschutzbestimmungen Ihres '
            'Wohnsitzlandes, soweit sie einen höheren Schutz bieten.\n\n'
            '13.3 Streitigkeiten, die nicht durch das Beschwerdeverfahren oder ADR '
            'gelöst werden können, werden den zuständigen Gerichten Bulgariens '
            'unterworfen, unbeschadet Ihres Rechts, Klage in Ihrem Wohnsitzland '
            'zu erheben.'
        ),
        "el": (
            '13.1 Οι παρόντες Όροι διέπονται από το δίκαιο της Βουλγαρίας.\n\n'
            '13.2 Εάν είστε καταναλωτής που διαμένει σε άλλο κράτος μέλος ΕΕ/ΕΟΧ, '
            'ισχύουν επίσης οι υποχρεωτικές διατάξεις προστασίας καταναλωτών της '
            'χώρας διαμονής σας, στον βαθμό που παρέχουν υψηλότερη προστασία.\n\n'
            '13.3 Διαφορές που δεν επιλύονται μέσω διαδικασίας παραπόνων ή ADR '
            'υποβάλλονται στα αρμόδια δικαστήρια της Βουλγαρίας, με την επιφύλαξη '
            'του δικαιώματός σας να ασκήσετε αγωγή στη χώρα κατοικίας σας.'
        ),
        "es": (
            '13.1 Estos Términos se rigen por la ley de Bulgaria.\n\n'
            '13.2 Si usted es un consumidor residente en otro estado miembro de la '
            'UE/EEE, también se aplican las disposiciones obligatorias de protección '
            'al consumidor de su país de residencia en la medida en que ofrezcan '
            'mayor protección.\n\n'
            '13.3 Las disputas que no puedan resolverse mediante el procedimiento de '
            'reclamación o ADR se someterán a los tribunales competentes de Bulgaria, '
            'sin perjuicio de su derecho a presentar demanda en los tribunales de '
            'su país de residencia.'
        ),
        "et": (
            '13.1 Need tingimused on reguleeritud Bulgaaria õigusega.\n\n'
            '13.2 Kui olete tarbija, kes elab mõnes teises EL/EMP liikmesriigis, '
            'kohalduvad ka teie elukohariigi kohustuslikud tarbijakaitse sätted '
            'ulatuses, milles need pakuvad kõrgemat kaitset.\n\n'
            '13.3 Vaidlused, mida ei saa lahendada kaebemenetluse ega ADR kaudu, '
            'esitatakse Bulgaaria pädevatele kohtutele, ilma et see piiraks teie '
            'õigust esitada hagi elukohariigi kohtutes.'
        ),
        "fi": (
            '13.1 Nämä ehdot on säädelty Bulgarian lainsäädännöllä.\n\n'
            '13.2 Jos olet kuluttaja, joka asuu toisessa EU/ETA-jäsenvaltiossa, '
            'myös asuinmaasi pakolliset kuluttajansuojasäännökset ovat sovellettavia '
            'siltä osin kuin ne tarjoavat paremman suojan.\n\n'
            '13.3 Riidat, joita ei voida ratkaista valitusmenettelyn tai ADR:n '
            'kautta, toimitetaan Bulgarian toimivaltaisille tuomioistuimille, '
            'rajoittamatta oikeuttasi nostaa kanne asuinmaasi tuomioistuimissa.'
        ),
        "fr": (
            '13.1 Les présentes Conditions sont régies par le droit bulgare.\n\n'
            '13.2 Si vous êtes un consommateur résidant dans un autre État membre '
            'de l\'UE/EEE, les dispositions obligatoires de protection des '
            'consommateurs de votre pays de résidence s\'appliquent également dans '
            'la mesure où elles offrent une protection plus élevée.\n\n'
            '13.3 Les litiges qui ne peuvent être résolus par la procédure de '
            'réclamation ou l\'ADR seront soumis aux juridictions compétentes '
            'bulgares, sans préjudice de votre droit d\'engager une procédure '
            'devant les tribunaux de votre pays de résidence.'
        ),
        "ga": (
            '13.1 Tá na Téarmaí seo rialaithe ag dlí na Bulgáire.\n\n'
            '13.2 Más tomhaltóir thú atá ina chónaí i mballstát eile den AE/LEE, '
            'tá forálacha éigeantacha cosanta tomhaltóirí do thír chónaithe '
            'infheidhme freisin sa mhéid go gcuireann siad cosaint níos airde ar fáil.\n\n'
            '13.3 Díospóidí nach féidir a réiteach trí nós imeachta gearáin nó ADR '
            'cuirfear faoi bhráid cúirteanna inniúla na Bulgáire iad, gan dochar do '
            'do cheart imeachtaí a thionscnamh i gcúirteanna do thíre cónaithe.'
        ),
        "hr": (
            '13.1 Ovi Uvjeti regulirani su bugarskim pravom.\n\n'
            '13.2 Ako ste potrošač s boravištem u drugoj državi članici EU/EGP, '
            'primjenjuju se i obvezne odredbe zaštite potrošača vaše zemlje boravišta '
            'u mjeri u kojoj pružaju veću zaštitu.\n\n'
            '13.3 Sporovi koji se ne mogu riješiti postupkom pritužbe ili ADR-om '
            'podnijet će se nadležnim sudovima Bugarske, ne dovodeći u pitanje '
            'vaše pravo na podnošenje tužbe u sudovima vaše zemlje boravišta.'
        ),
        "hu": (
            '13.1 Jelen feltételekre a bolgár jog irányadó.\n\n'
            '13.2 Ha Ön egy másik EU/EGT tagállamban lakóhellyel rendelkező fogyasztó, '
            'az Ön lakóhelye szerinti ország kötelező fogyasztóvédelmi rendelkezései '
            'is alkalmazandók, amennyiben magasabb szintű védelmet nyújtanak.\n\n'
            '13.3 A panaszeljáráson vagy ADR-en keresztül nem megoldható viták '
            'Bulgária illetékes bíróságai elé kerülnek, anélkül hogy sértené '
            'az Ön jogát lakóhelye szerinti ország bíróságain eljárást indítani.'
        ),
        "is": (
            '13.1 Þessir skilmálar eru stjórnað af lögum Búlgaríu.\n\n'
            '13.2 Ef þú ert neytandi búsettur í öðru ESB/EES-ríki, gilda einnig '
            'lögbundnar neytendaverndarákvæðar þíns búsetulands að því marki '
            'sem þær veita meiri vernd.\n\n'
            '13.3 Deilur sem ekki er hægt að leysa með kvörtunarferli eða ADR '
            'verða lagðar fyrir lögsægar dómstóla Búlgaríu, án þess að skerða '
            'rétt þinn til að höfða mál fyrir dómstólum þíns búsetulands.'
        ),
        "it": (
            '13.1 I presenti Termini sono disciplinati dalla legge bulgara.\n\n'
            '13.2 Se sei un consumatore residente in un altro Stato membro UE/SEE, '
            'si applicano anche le disposizioni obbligatorie di protezione dei '
            'consumatori del tuo paese di residenza nella misura in cui offrano '
            'una protezione più elevata.\n\n'
            '13.3 Le controversie che non possono essere risolte tramite la '
            'procedura di reclamo o ADR saranno sottoposte ai tribunali competenti '
            'della Bulgaria, senza pregiudizio del tuo diritto di adire i tribunali '
            'del tuo paese di residenza.'
        ),
        "lb": (
            '13.1 Dës Bedéngungen ënnerleien dem bulgareschen Recht.\n\n'
            '13.2 Wann Dir Konsument mat Wunnsëtz an engem aneren EU/EWR-Membersstaat '
            'sidd, gëllen och d\'obligatoresch Konsumenteschutzbestëmmungen vun '
            'Ärem Wunnsëtzland, sowäit dës e méi héije Schutz bidden.\n\n'
            '13.3 Sträite, déi net duerch d\'Beschwerdeverfaren oder ADR geléist '
            'kënne ginn, ginn de kompetente Geriichter vu Bulgarien virgeluecht, '
            'ouni Äert Recht ze beaflossen, Kloe virun de Geriichter vun Ärem '
            'Wunnsëtzland anzestellen.'
        ),
        "lt": (
            '13.1 Šios sąlygos reglamentuojamos Bulgarijos teisės aktais.\n\n'
            '13.2 Jei esate vartotojas, gyvenantis kitoje ES/EEE valstybėje narėje, '
            'taip pat taikomos privalomos jūsų gyvenamosios šalies vartotojų '
            'apsaugos nuostatos tiek, kiek jos suteikia didesnę apsaugą.\n\n'
            '13.3 Ginčai, kurių nepavyksta išspręsti skundų nagrinėjimo tvarka arba '
            'per AGS, pateikiami Bulgarijos kompetentingiems teismams, nepažeidžiant '
            'jūsų teisės pareikšti ieškinį gyvenamosios šalies teismuose.'
        ),
        "lv": (
            '13.1 Šie noteikumi tiek regulēti saskaņā ar Bulgārijas tiesību aktiem.\n\n'
            '13.2 Ja esat patērētājs, kas dzīvo citā ES/EEZ dalībvalstī, tiek '
            'piemērotas arī jūsu dzīvesvietas valsts obligātās patērētāju aizsardzības '
            'normas, ciktāl tās nodrošina augstāku aizsardzības līmeni.\n\n'
            '13.3 Strīdi, kurus nevar atrisināt sūdzību izskatīšanas kārtībā vai '
            'ADR ceļā, tiek nodoti Bulgārijas kompetentajām tiesām, neskarot jūsu '
            'tiesības celt prasību dzīvesvietas valsts tiesās.'
        ),
        "mk": (
            '13.1 Овие Услови се уредени со законодавството на Република Бугарија.\n\n'
            '13.2 Доколку сте потрошувач со живеалиште во друга земја-членка на '
            'ЕУ/ЕЕП, се применуваат и задолжителните одредби за заштита на '
            'потрошувачите на земјата на вашето живеалиште во мера во која тие '
            'обезбедуваат повисока заштита.\n\n'
            '13.3 Споровите кои не можат да се решат преку постапката за рекламации '
            'или АРС се упатуваат на надлежните судови на Бугарија, без да се '
            'засегне вашето право да поднесете тужба пред судовите на вашата земја '
            'на живеалиште.'
        ),
        "mt": (
            '13.1 Dawn it-Termini huma rregolati mil-liġi tal-Bulgarija.\n\n'
            '13.2 Jekk inti konsumatur residenti fi Stat Membru ieħor tal-UE/ŻEE, '
            'japplikaw ukoll id-dispożizzjonijiet mandatorji ta\' protezzjoni '
            'tal-konsumatur tal-pajjiż tar-residenza tiegħek sal-punt li joffru '
            'protezzjoni ogħla.\n\n'
            '13.3 Tilwim li ma jistax jiġi solvut permezz tal-proċedura ta\' lment '
            'jew ADR jiġi sottomess lill-qrati kompetenti tal-Bulgarija, mingħajr '
            'preġudizzju għad-dritt tiegħek li tressaq proċedimenti fil-qrati '
            'tal-pajjiż tar-residenza tiegħek.'
        ),
        "nl": (
            '13.1 Deze Voorwaarden worden beheerst door het Bulgaarse recht.\n\n'
            '13.2 Als u een consument bent die verblijft in een andere EU/EER-lidstaat, '
            'zijn ook de dwingende consumentenbeschermingsbepalingen van uw '
            'woonplaatsland van toepassing voor zover ze een hogere bescherming bieden.\n\n'
            '13.3 Geschillen die niet via de klachtenprocedure of ADR kunnen worden '
            'opgelost, worden voorgelegd aan de bevoegde rechtbanken van Bulgarije, '
            'onverminderd uw recht om een procedure aan te spannen bij de rechtbanken '
            'van uw woonplaatsland.'
        ),
        "no": (
            '13.1 Disse Vilkårene er underlagt bulgarsk rett.\n\n'
            '13.2 Hvis du er forbruker bosatt i en annen EU/EØS-medlemsstat, '
            'gjelder også de obligatoriske forbrukerbeskyttelsesbestemmelsene i '
            'ditt bostedsland i den grad de gir høyere beskyttelse.\n\n'
            '13.3 Tvister som ikke kan løses gjennom klageprosedyren eller ADR '
            'vil bli innbragt for de kompetente domstolene i Bulgaria, uten at '
            'dette berører din rett til å reise sak ved domstolene i ditt bostedsland.'
        ),
        "pt": (
            '13.1 Estes Termos são regidos pela lei da Bulgária.\n\n'
            '13.2 Se você é um consumidor residente em outro Estado-Membro da '
            'UE/EEE, as disposições obrigatórias de proteção ao consumidor do seu '
            'país de residência também se aplicam na medida em que ofereçam maior '
            'proteção.\n\n'
            '13.3 Litígios que não possam ser resolvidos pelo procedimento de '
            'reclamação ou ADR serão submetidos aos tribunais competentes da '
            'Bulgária, sem prejuízo do seu direito de propor ação nos tribunais '
            'do seu país de residência.'
        ),
        "pt-PT": (
            '13.1 Estes Termos são regulados pela lei da Bulgária.\n\n'
            '13.2 Se for um consumidor residente noutro Estado-Membro da UE/EEE, '
            'as disposições obrigatórias de protecção do consumidor do seu país '
            'de residência também se aplicam na medida em que ofereçam maior '
            'protecção.\n\n'
            '13.3 Litígios que não possam ser resolvidos por via do procedimento '
            'de reclamação ou ADR serão submetidos aos tribunais competentes da '
            'Bulgária, sem prejuízo do seu direito de propor acção nos tribunais '
            'do seu país de residência.'
        ),
        "ro": (
            '13.1 Acești Termeni sunt guvernați de legea Bulgariei.\n\n'
            '13.2 Dacă sunteți un consumator rezident într-un alt stat membru UE/SEE, '
            'se aplică și dispozițiile obligatorii de protecție a consumatorilor '
            'din țara dvs. de reședință în măsura în care acestea oferă o '
            'protecție mai ridicată.\n\n'
            '13.3 Litigiile care nu pot fi rezolvate prin procedura de reclamație '
            'sau ADR vor fi supuse instanțelor competente din Bulgaria, fără a '
            'aduce atingere dreptului dvs. de a introduce o acțiune la instanțele '
            'din țara dvs. de reședință.'
        ),
        "ru": (
            '13.1 Настоящие условия регулируются законодательством Болгарии.\n\n'
            '13.2 Если вы являетесь потребителем, проживающим в другом государстве '
            'ЕС/ЕЭЗ, также применяются обязательные нормы защиты потребителей '
            'вашей страны проживания в той мере, в которой они обеспечивают '
            'более высокий уровень защиты.\n\n'
            '13.3 Споры, которые не могут быть урегулированы в порядке рассмотрения '
            'жалоб или АУС, передаются в компетентные суды Болгарии без ущерба '
            'для вашего права обратиться в суд по месту проживания.'
        ),
        "sk": (
            '13.1 Tieto podmienky sa riadia bulharským právom.\n\n'
            '13.2 Ak ste spotrebiteľ s bydliskom v inom členskom štáte EÚ/EHP, '
            'platia aj povinné ustanovenia ochrany spotrebiteľa vašej krajiny '
            'bydliska v rozsahu, v akom poskytujú vyššiu ochranu.\n\n'
            '13.3 Spory, ktoré nie je možné vyriešiť reklamačným konaním alebo ARS, '
            'budú predložené príslušným súdom Bulharska, bez toho, aby bolo '
            'dotknuté vaše právo podať žalobu na súdoch vašej krajiny bydliska.'
        ),
        "sl": (
            '13.1 Ti pogoji so urejeni z bolgarskim pravom.\n\n'
            '13.2 Če ste potrošnik s stalnim prebivališčem v drugi državi članici '
            'EU/EGP, se uporabljajo tudi obvezne določbe varstva potrošnikov '
            'vaše države bivanja, v obsegu, v katerem zagotavljajo višjo raven '
            'zaščite.\n\n'
            '13.3 Spori, ki jih ni mogoče rešiti s postopkom pritožb ali ARS, '
            'se predložijo pristojnim sodiščem Bolgarije, brez poseganja v vašo '
            'pravico do vložitve tožbe pri sodiščih vaše države bivanja.'
        ),
        "sq": (
            '13.1 Këto Terma janë të rregulluara nga ligji i Bullgarisë.\n\n'
            '13.2 Nëse jeni konsumator me banim në një shtet tjetër anëtar të '
            'BE-së/SEE, zbatohen gjithashtu dispozitat e detyrueshme të mbrojtjes '
            'së konsumatorit të vendit tuaj të banimit në masën që ofrojnë '
            'mbrojtje më të lartë.\n\n'
            '13.3 Mosmarrëveshjet që nuk mund të zgjidhen nëpërmjet procedurës '
            'së ankesave ose ADR do t\'i drejtohen gjykatave kompetente të '
            'Bullgarisë, pa cenuar të drejtën tuaj për të ngritur padi në '
            'gjykatat e vendit tuaj të banimit.'
        ),
        "sr": (
            '13.1 Ovi Uslovi se regulišu bugarskim pravom.\n\n'
            '13.2 Ako ste potrošač sa boravištem u drugoj državi članici EU/EEP, '
            'primenjuju se i obavezne odredbe zaštite potrošača vaše zemlje '
            'boravišta u meri u kojoj pružaju veću zaštitu.\n\n'
            '13.3 Sporovi koji se ne mogu rešiti postupkom reklamacije ili ARS-om '
            'biće podneseni nadležnim sudovima Bugarske, ne dovodeći u pitanje '
            'vaše pravo da pokrenete postupak pred sudovima vaše zemlje boravišta.'
        ),
        "sv": (
            '13.1 Dessa Villkor regleras av bulgarisk rätt.\n\n'
            '13.2 Om du är en konsument bosatt i en annan EU/EES-medlemsstat '
            'gäller även de tvingande konsumentskyddsbestämmelserna i ditt '
            'bosättningsland i den mån de ger ett högre skydd.\n\n'
            '13.3 Tvister som inte kan lösas genom klagomålsförfarandet eller ADR '
            'ska hänskjutas till behöriga domstolar i Bulgarien, utan att det '
            'påverkar din rätt att väcka talan vid domstolarna i ditt bosättningsland.'
        ),
        "tr": (
            '13.1 Bu Koşullar, Bulgaristan hukukuna tabidir.\n\n'
            '13.2 Başka bir AB/AEA üye devletinde ikamet eden bir tüketiciyseniz, '
            'ikamet ettiğiniz ülkenin zorunlu tüketici koruma hükümleri de daha '
            'yüksek koruma sağladıkları ölçüde uygulanır.\n\n'
            '13.3 Şikayet prosedürü veya AUÇ yoluyla çözülemeyen uyuşmazlıklar, '
            'ikamet ettiğiniz ülkedeki mahkemelerde dava açma hakkınız saklı '
            'kalmak kaydıyla Bulgaristan\'ın yetkili mahkemelerine sunulur.'
        ),
        "uk": (
            '13.1 Ці Умови регулюються законодавством Болгарії.\n\n'
            '13.2 Якщо ви є споживачем, що проживає в іншій державі-члені ЄС/ЄЕП, '
            'також застосовуються обов\'язкові норми захисту споживачів вашої '
            'країни проживання в тій мірі, в якій вони забезпечують вищий рівень '
            'захисту.\n\n'
            '13.3 Спори, які не можуть бути вирішені в порядку розгляду скарг або '
            'через АВС, передаються до компетентних судів Болгарії без шкоди для '
            'вашого права подати позов до судів країни вашого проживання.'
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
        print(f"✅ seed_terms_p13_bodies: {count} rows upserted ({NAMESPACE}, art13_body × 34 langs)")

    engine.dispose()


if __name__ == "__main__":
    seed()
