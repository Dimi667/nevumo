"""
seed_terms_p12_bodies.py  —  Nevumo | namespace: terms
Key: art12_body (34 езика)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_terms_p12_bodies
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
    "art12_body": {
        "en": (
            '12.1 In the event of an unresolved dispute between you and Nevumo, you may '
            'seek alternative dispute resolution.\n\n'
            '12.2 [PL] Polish consumers may turn to Inspekcja Handlowa (IH) — the Trade '
            'Inspectorate — for free out-of-court dispute resolution. The Warsaw regional '
            'Trade Inspectorate is at ul. Sienkiewicza 3, 00-015 Warszawa. '
            'Further information: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo agrees to participate in ADR proceedings when required by '
            'applicable law.\n\n'
            '12.4 Note: The European Commission\'s Online Dispute Resolution (ODR) platform '
            'was permanently closed on 20 July 2025 and is no longer available.'
        ),
        "pl": (
            '12.1 W przypadku nierozwiązanego sporu między Klientem będącym konsumentem '
            'a Nevumo, Klient uprawniony jest do skorzystania z pozasądowych metod '
            'rozwiązywania sporów.\n\n'
            '12.2 Klienci w Polsce mogą zwrócić się do Inspekcji Handlowej (IH), '
            'w szczególności do Mazowieckiego Wojewódzkiego Inspektora Inspekcji Handlowej '
            'w Warszawie (ul. Sienkiewicza 3, 00-015 Warszawa), w celu wszczęcia '
            'postępowania mediacyjnego lub przed stałym polubownym sądem konsumenckim. '
            'Więcej informacji: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo zobowiązuje się do uczestnictwa w postępowaniach ADR wymaganych '
            'przez obowiązujące przepisy prawa.\n\n'
            '12.4 Platforma ODR prowadzona przez Komisję Europejską została trwale '
            'zamknięta w dniu 20 lipca 2025 r. i nie jest dostępna.'
        ),
        "bg": (
            '12.1 При неразрешен спор между Клиент и Nevumo, потребителят може да '
            'прибегне до алтернативни способи за решаване на спорове.\n\n'
            '12.2 Потребителите в България могат да се обърнат към Помирителните комисии '
            'към Комисията за защита на потребителите (КЗП) или към Националната онлайн '
            'платформа за АРС: www.kzp.bg\n\n'
            '12.3 Nevumo се ангажира да участва в АРС производства, когато се изисква '
            'от приложимото законодателство.\n\n'
            '12.4 Платформата на ЕК за решаване на спорове онлайн (ODR) е закрита '
            'окончателно на 20 юли 2025 г. и не е достъпна.'
        ),
        "cs": (
            '12.1 V případě nevyřešeného sporu mezi vámi a Nevumo můžete využít '
            'alternativní řešení sporů.\n\n'
            '12.2 [PL] Polští spotřebitelé se mohou obrátit na Inspekcja Handlowa (IH) '
            'pro mimosoudní řešení sporů. ul. Sienkiewicza 3, 00-015 Varšava. '
            'Další informace: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo souhlasí s účastí v řízení ADR, pokud to vyžaduje platné právo.\n\n'
            '12.4 Platforma ODR Evropské komise byla trvale uzavřena 20. července 2025 '
            'a již není dostupná.'
        ),
        "da": (
            '12.1 I tilfælde af en uløst tvist mellem dig og Nevumo kan du søge '
            'alternativ tvistbilæggelse.\n\n'
            '12.2 [PL] Polske forbrugere kan henvende sig til Inspekcja Handlowa (IH) '
            'for gratis udenretlig tvistbilæggelse. ul. Sienkiewicza 3, 00-015 Warszawa. '
            'Yderligere info: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo accepterer at deltage i ADR-procedurer, når det kræves af '
            'gældende lov.\n\n'
            '12.4 EU-Kommissionens ODR-platform blev permanent lukket den 20. juli 2025 '
            'og er ikke længere tilgængelig.'
        ),
        "de": (
            '12.1 Bei einem ungelösten Streit zwischen Ihnen und Nevumo können Sie eine '
            'alternative Streitbeilegung in Anspruch nehmen.\n\n'
            '12.2 [PL] Polnische Verbraucher können sich an die Inspekcja Handlowa (IH) '
            'für kostenlose außergerichtliche Streitbeilegung wenden. '
            'ul. Sienkiewicza 3, 00-015 Warschau. '
            'Weitere Infos: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo erklärt sich bereit, an ADR-Verfahren teilzunehmen, wenn dies '
            'vom geltenden Recht gefordert wird.\n\n'
            '12.4 Die ODR-Plattform der Europäischen Kommission wurde am 20. Juli 2025 '
            'dauerhaft geschlossen und steht nicht mehr zur Verfügung.'
        ),
        "el": (
            '12.1 Σε περίπτωση αδιευθέτητης διαφοράς μεταξύ εσάς και του Nevumo, '
            'μπορείτε να αναζητήσετε εναλλακτική επίλυση διαφοράς.\n\n'
            '12.2 [PL] Οι Πολωνοί καταναλωτές μπορούν να απευθυνθούν στην '
            'Inspekcja Handlowa (IH) για δωρεάν εξωδικαστική επίλυση. '
            'ul. Sienkiewicza 3, 00-015 Βαρσοβία. '
            'Περισσότερες πληροφορίες: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Το Nevumo συμφωνεί να συμμετέχει σε διαδικασίες ADR όταν απαιτείται '
            'από το εφαρμοστέο δίκαιο.\n\n'
            '12.4 Η πλατφόρμα ODR της Ευρωπαϊκής Επιτροπής έκλεισε οριστικά στις '
            '20 Ιουλίου 2025 και δεν είναι πλέον διαθέσιμη.'
        ),
        "es": (
            '12.1 En caso de disputa no resuelta entre usted y Nevumo, puede recurrir '
            'a la resolución alternativa de conflictos.\n\n'
            '12.2 [PL] Los consumidores polacos pueden acudir a la Inspekcja Handlowa (IH) '
            'para resolución extrajudicial gratuita. '
            'ul. Sienkiewicza 3, 00-015 Varsovia. '
            'Más información: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo acepta participar en procedimientos ADR cuando lo exija la '
            'legislación aplicable.\n\n'
            '12.4 La plataforma ODR de la Comisión Europea se cerró permanentemente el '
            '20 de julio de 2025 y ya no está disponible.'
        ),
        "et": (
            '12.1 Lahendamata vaidluse korral teie ja Nevumo vahel võite taotleda '
            'alternatiivset vaidluste lahendamist.\n\n'
            '12.2 [PL] Poola tarbijad võivad pöörduda Inspekcja Handlowa (IH) poole '
            'tasuta kohtuväliseks lahendamiseks. '
            'ul. Sienkiewicza 3, 00-015 Varssavi. '
            'Lisateave: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo nõustub osalema ADR menetlustes, kui kohaldatav õigus seda nõuab.\n\n'
            '12.4 Euroopa Komisjoni ODR platvorm suleti püsivalt 20. juulil 2025 '
            'ja ei ole enam kättesaadav.'
        ),
        "fi": (
            '12.1 Ratkaisemattoman riidan tapauksessa sinun ja Nevumon välillä voit '
            'hakea vaihtoehtoista riidanratkaisua.\n\n'
            '12.2 [PL] Puolalaiset kuluttajat voivat kääntyä Inspekcja Handlowa (IH) -'
            'elimen puoleen maksuttomaan tuomioistuimen ulkopuoliseen ratkaisuun. '
            'ul. Sienkiewicza 3, 00-015 Varsova. '
            'Lisätietoja: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo suostuu osallistumaan ADR-menettelyihin sovellettavan '
            'lainsäädännön niin vaatiessa.\n\n'
            '12.4 Euroopan komission ODR-alusta suljettiin pysyvästi 20. heinäkuuta 2025 '
            'eikä se ole enää käytettävissä.'
        ),
        "fr": (
            '12.1 En cas de litige non résolu entre vous et Nevumo, vous pouvez recourir '
            'au règlement alternatif des litiges.\n\n'
            '12.2 [PL] Les consommateurs polonais peuvent s\'adresser à l\'Inspekcja '
            'Handlowa (IH) pour une résolution amiable gratuite. '
            'ul. Sienkiewicza 3, 00-015 Varsovie. '
            'Plus d\'informations : www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo s\'engage à participer aux procédures ADR lorsque la '
            'législation applicable l\'exige.\n\n'
            '12.4 La plateforme ODR de la Commission européenne a été définitivement '
            'fermée le 20 juillet 2025 et n\'est plus disponible.'
        ),
        "ga": (
            '12.1 I gcás díospóide neamhréitithe idir tú agus Nevumo, féadfaidh tú '
            'réiteach malartach díospóidí a lorg.\n\n'
            '12.2 [PL] Féadfaidh tomhaltóirí Polannach dul chuig Inspekcja Handlowa (IH) '
            'le haghaidh réiteach saor in aisce lasmuigh den chúirt. '
            'ul. Sienkiewicza 3, 00-015 Vársá. '
            'Tuilleadh eolais: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Aontaíonn Nevumo páirt a ghlacadh i nósanna imeachta ADR nuair a '
            'éilítear é faoin dlí infheidhmithe.\n\n'
            '12.4 Dúnadh ardán ODR an Choimisiúin Eorpaigh go buan ar 20 Iúil 2025 '
            'agus níl sé ar fáil a thuilleadh.'
        ),
        "hr": (
            '12.1 U slučaju neriješenog spora između vas i Nevumo, možete potražiti '
            'alternativno rješavanje sporova.\n\n'
            '12.2 [PL] Poljski potrošači mogu se obratiti Inspekcja Handlowa (IH) '
            'za besplatno izvansudsko rješavanje. '
            'ul. Sienkiewicza 3, 00-015 Varšava. '
            'Više informacija: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo pristaje sudjelovati u ADR postupcima kada to zahtijeva '
            'primjenjivo pravo.\n\n'
            '12.4 ODR platforma Europske komisije trajno je zatvorena 20. srpnja 2025. '
            'i više nije dostupna.'
        ),
        "hu": (
            '12.1 Ön és a Nevumo között fennálló megoldatlan vita esetén alternatív '
            'vitarendezést vehet igénybe.\n\n'
            '12.2 [PL] A lengyel fogyasztók ingyenes bírósági vitarendezés céljából '
            'fordulhatnak az Inspekcja Handlowa (IH) szervhez. '
            'ul. Sienkiewicza 3, 00-015 Varsó. '
            'További információ: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 A Nevumo vállalja, hogy részt vesz az ADR eljárásokban, ha azt az '
            'alkalmazandó jog megköveteli.\n\n'
            '12.4 Az Európai Bizottság ODR platformja 2025. július 20-án véglegesen '
            'bezárt és többé nem érhető el.'
        ),
        "is": (
            '12.1 Við óleystar deilu milli þín og Nevumo getur þú leitað '
            'óformlegrar deilulausnar.\n\n'
            '12.2 [PL] Pólskir neytendur geta leitað til Inspekcja Handlowa (IH) '
            'fyrir ókeypis lausn utan dómstóla. '
            'ul. Sienkiewicza 3, 00-015 Varsjá. '
            'Frekari upplýsingar: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo samþykkir að taka þátt í ADR-málsmeðferð þegar gildandi lög '
            'krefjast þess.\n\n'
            '12.4 ODR-vettvangur Evrópusambandsins var lokaður að varanlegu í '
            '20. júlí 2025 og er ekki lengur tiltækur.'
        ),
        "it": (
            '12.1 In caso di controversia non risolta tra te e Nevumo, puoi richiedere '
            'una risoluzione alternativa delle controversie.\n\n'
            '12.2 [PL] I consumatori polacchi possono rivolgersi all\'Inspekcja Handlowa '
            '(IH) per la risoluzione stragiudiziale gratuita. '
            'ul. Sienkiewicza 3, 00-015 Varsavia. '
            'Ulteriori informazioni: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo accetta di partecipare alle procedure ADR quando richiesto '
            'dalla normativa applicabile.\n\n'
            '12.4 La piattaforma ODR della Commissione europea è stata chiusa '
            'definitivamente il 20 luglio 2025 e non è più disponibile.'
        ),
        "lb": (
            '12.1 Bei engem ongeléiste Sträit tëschent Iech a Nevumo kënnt Dir '
            'alternativ Sträitbäilegung sichen.\n\n'
            '12.2 [PL] Polnesch Konsumenten kënnen sech un d\'Inspekcja Handlowa (IH) '
            'fir gratis aussergerichtlech Léisung wenden. '
            'ul. Sienkiewicza 3, 00-015 Warschau. '
            'Méi Informatiounen: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo erkläert sech bereet un ADR-Verfahren deelzehuelen, wa '
            'dat vum gëltege Recht erfuerdert gëtt.\n\n'
            '12.4 D\'ODR-Plattform vun der Europäescher Kommissioun gouf den '
            '20. Juli 2025 permanent zougemaach an ass net méi verfügbar.'
        ),
        "lt": (
            '12.1 Nesant neišspręstam ginčui tarp jūsų ir Nevumo, galite kreiptis '
            'dėl alternatyvaus ginčų sprendimo.\n\n'
            '12.2 [PL] Lenkijos vartotojai gali kreiptis į Inspekcja Handlowa (IH) '
            'dėl nemokamo neteisminio sprendimo. '
            'ul. Sienkiewicza 3, 00-015 Varšuva. '
            'Daugiau informacijos: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo sutinka dalyvauti AGS procesuose, kai to reikalauja '
            'taikytina teisė.\n\n'
            '12.4 Europos Komisijos ODR platforma buvo nuolat uždaryta 2025 m. '
            'liepos 20 d. ir nebėra prieinama.'
        ),
        "lv": (
            '12.1 Neatrisināta strīda gadījumā starp jums un Nevumo varat meklēt '
            'alternatīvu strīdu izšķiršanu.\n\n'
            '12.2 [PL] Polijas patērētāji var vērsties pie Inspekcja Handlowa (IH) '
            'bezmaksas ārpustiesas risinājumam. '
            'ul. Sienkiewicza 3, 00-015 Varšava. '
            'Sīkāka informācija: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo piekrīt piedalīties ADR procedūrās, kad to prasa piemērojamie '
            'tiesību akti.\n\n'
            '12.4 Eiropas Komisijas ODR platforma tika pastāvīgi slēgta 2025. gada '
            '20. jūlijā un vairs nav pieejama.'
        ),
        "mk": (
            '12.1 Во случај на нерешен спор меѓу вас и Nevumo, можете да побарате '
            'алтернативно решавање на спорот.\n\n'
            '12.2 [PL] Полските потрошувачи можат да се обратат до Inspekcja Handlowa '
            '(IH) за бесплатно вонсудско решавање. '
            'ul. Sienkiewicza 3, 00-015 Варшава. '
            'Повеќе информации: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo се согласува да учествува во АРС постапки кога тоа е '
            'барано од применливото право.\n\n'
            '12.4 ODR платформата на Европската комисија е трајно затворена на '
            '20 јули 2025 г. и повеќе не е достапна.'
        ),
        "mt": (
            '12.1 F\'każ ta\' tilwima mhux riżolta bejnek u Nevumo, tista\' tfittex '
            'riżoluzzjoni alternattiva tat-tilwim.\n\n'
            '12.2 [PL] Il-konsumaturi Pollakki jistgħu jduru lejn Inspekcja Handlowa '
            '(IH) għal riżoluzzjoni barra mill-qorti bla ħlas. '
            'ul. Sienkiewicza 3, 00-015 Varsavja. '
            'Aktar informazzjoni: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo jaqbel li jipparteċipa f\'proċedimenti ADR meta meħtieġ '
            'mil-liġi applikabbli.\n\n'
            '12.4 Il-pjattaforma ODR tal-Kummissjoni Ewropea ngħalqet b\'mod permanenti '
            'fl-20 ta\' Lulju 2025 u mhix aktar disponibbli.'
        ),
        "nl": (
            '12.1 Bij een onopgeloste geschil tussen u en Nevumo kunt u alternatieve '
            'geschillenbeslechting zoeken.\n\n'
            '12.2 [PL] Poolse consumenten kunnen zich wenden tot Inspekcja Handlowa (IH) '
            'voor gratis buitengerechtelijke geschillenbeslechting. '
            'ul. Sienkiewicza 3, 00-015 Warschau. '
            'Meer informatie: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo stemt ermee in deel te nemen aan ADR-procedures wanneer '
            'toepasselijke wetgeving dit vereist.\n\n'
            '12.4 Het ODR-platform van de Europese Commissie werd op 20 juli 2025 '
            'permanent gesloten en is niet langer beschikbaar.'
        ),
        "no": (
            '12.1 Ved en uløst tvist mellom deg og Nevumo kan du søke alternativ '
            'tvisteløsning.\n\n'
            '12.2 [PL] Polske forbrugere kan henvende seg til Inspekcja Handlowa (IH) '
            'for gratis utenrettslig løsning. '
            'ul. Sienkiewicza 3, 00-015 Warszawa. '
            'Mer informasjon: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo er enig i å delta i ADR-prosedyrer når gjeldende lovgivning '
            'krever det.\n\n'
            '12.4 EU-kommisjonens ODR-plattform ble permanent stengt 20. juli 2025 '
            'og er ikke lenger tilgjengelig.'
        ),
        "pt": (
            '12.1 Em caso de litígio não resolvido entre você e o Nevumo, pode recorrer '
            'à resolução alternativa de litígios.\n\n'
            '12.2 [PL] Os consumidores polacos podem recorrer à Inspekcja Handlowa (IH) '
            'para resolução extrajudicial gratuita. '
            'ul. Sienkiewicza 3, 00-015 Varsóvia. '
            'Mais informações: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 O Nevumo concorda em participar em procedimentos ADR quando exigido '
            'pela legislação aplicável.\n\n'
            '12.4 A plataforma ODR da Comissão Europeia foi encerrada permanentemente '
            'em 20 de julho de 2025 e já não está disponível.'
        ),
        "pt-PT": (
            '12.1 Em caso de litígio não resolvido entre si e o Nevumo, pode recorrer '
            'à resolução alternativa de litígios.\n\n'
            '12.2 [PL] Os consumidores polacos podem recorrer à Inspekcja Handlowa (IH) '
            'para resolução extrajudicial gratuita. '
            'ul. Sienkiewicza 3, 00-015 Varsóvia. '
            'Mais informações: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 O Nevumo aceita participar em procedimentos ADR quando exigido pela '
            'legislação aplicável.\n\n'
            '12.4 A plataforma ODR da Comissão Europeia foi encerrada permanentemente '
            'em 20 de julho de 2025 e já não está disponível.'
        ),
        "ro": (
            '12.1 În cazul unui litigiu nerezolvat între dvs. și Nevumo, puteți solicita '
            'soluționarea alternativă a litigiului.\n\n'
            '12.2 [PL] Consumatorii polonezi se pot adresa Inspekcja Handlowa (IH) '
            'pentru soluționare extrajudiciară gratuită. '
            'ul. Sienkiewicza 3, 00-015 Varșovia. '
            'Mai multe informații: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo este de acord să participe la proceduri ADR atunci când '
            'legislația aplicabilă o impune.\n\n'
            '12.4 Platforma ODR a Comisiei Europene a fost închisă permanent la '
            '20 iulie 2025 și nu mai este disponibilă.'
        ),
        "ru": (
            '12.1 При неурегулированном споре между вами и Nevumo вы можете обратиться '
            'к альтернативному урегулированию споров.\n\n'
            '12.2 [PL] Польские потребители могут обратиться в Inspekcja Handlowa (IH) '
            'для бесплатного внесудебного урегулирования. '
            'ul. Sienkiewicza 3, 00-015 Варшава. '
            'Дополнительная информация: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo соглашается участвовать в процедурах АУС, если этого требует '
            'применимое законодательство.\n\n'
            '12.4 Платформа ODR Европейской комиссии была окончательно закрыта '
            '20 июля 2025 года и более не доступна.'
        ),
        "sk": (
            '12.1 V prípade nevyriešeného sporu medzi vami a Nevumo môžete využiť '
            'alternatívne riešenie sporov.\n\n'
            '12.2 [PL] Poľskí spotrebitelia sa môžu obrátiť na Inspekcja Handlowa (IH) '
            'pre bezplatné mimosúdne riešenie. '
            'ul. Sienkiewicza 3, 00-015 Varšava. '
            'Ďalšie informácie: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo súhlasí s účasťou v konaniach ARS, keď to vyžaduje platné '
            'právo.\n\n'
            '12.4 Platforma ODR Európskej komisie bola natrvalo uzavretá 20. júla 2025 '
            'a viac nie je dostupná.'
        ),
        "sl": (
            '12.1 V primeru nerešenega spora med vami in Nevumo lahko poiščete '
            'alternativno reševanje sporov.\n\n'
            '12.2 [PL] Poljski potrošniki se lahko obrnejo na Inspekcja Handlowa (IH) '
            'za brezplačno izvensodno reševanje. '
            'ul. Sienkiewicza 3, 00-015 Varšava. '
            'Več informacij: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo se strinja, da bo sodeloval v postopkih ARS, ko to zahteva '
            'veljavna zakonodaja.\n\n'
            '12.4 Platforma ODR Evropske komisije je bila trajno zaprta 20. julija 2025 '
            'in ni več na voljo.'
        ),
        "sq": (
            '12.1 Në rast të një mosmarrëveshjeje të pazgjidhur midis jush dhe Nevumo, '
            'mund të kërkoni zgjidhje alternative të mosmarrëveshjes.\n\n'
            '12.2 [PL] Konsumatorët polakë mund të drejtohen tek Inspekcja Handlowa (IH) '
            'për zgjidhje jashtëgjyqësore falas. '
            'ul. Sienkiewicza 3, 00-015 Varshavë. '
            'Më shumë informacion: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo pranon të marrë pjesë në procedurat ADR kur kërkohet nga '
            'legjislacioni i zbatueshëm.\n\n'
            '12.4 Platforma ODR e Komisionit Europian u mbyll përgjithmonë më '
            '20 korrik 2025 dhe nuk është më e disponueshme.'
        ),
        "sr": (
            '12.1 U slučaju nerešenog spora između vas i Nevumo, možete potražiti '
            'alternativno rešavanje sporova.\n\n'
            '12.2 [PL] Poljski potrošači mogu se obratiti Inspekcja Handlowa (IH) '
            'za besplatno vansudsko rešavanje. '
            'ul. Sienkiewicza 3, 00-015 Varšava. '
            'Više informacija: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo pristaje da učestvuje u ARS postupcima kada to zahteva '
            'primenjivo pravo.\n\n'
            '12.4 ODR platforma Evropske komisije trajno je zatvorena 20. jula 2025. '
            'i više nije dostupna.'
        ),
        "sv": (
            '12.1 Vid en olöst tvist mellan dig och Nevumo kan du söka alternativ '
            'tvistlösning.\n\n'
            '12.2 [PL] Svenska konsumenter kan vända sig till Inspekcja Handlowa (IH) '
            'för kostnadsfri utomrättslig lösning. '
            'ul. Sienkiewicza 3, 00-015 Warszawa. '
            'Mer information: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo accepterar att delta i ADR-förfaranden när tillämplig lagstiftning '
            'kräver det.\n\n'
            '12.4 EU-kommissionens ODR-plattform stängdes permanent den 20 juli 2025 '
            'och är inte längre tillgänglig.'
        ),
        "tr": (
            '12.1 Sizinle Nevumo arasında çözüme kavuşturulamamış bir uyuşmazlık '
            'durumunda alternatif uyuşmazlık çözümü yoluna başvurabilirsiniz.\n\n'
            '12.2 [PL] Polonyalı tüketiciler ücretsiz mahkeme dışı çözüm için '
            'Inspekcja Handlowa\'ya (IH) başvurabilir. '
            'ul. Sienkiewicza 3, 00-015 Varşova. '
            'Daha fazla bilgi: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo, yürürlükteki mevzuat gerektirdiğinde AUÇ süreçlerine '
            'katılmayı kabul eder.\n\n'
            '12.4 Avrupa Komisyonu\'nun ODR platformu 20 Temmuz 2025 tarihinde '
            'kalıcı olarak kapatılmış ve artık kullanılamamaktadır.'
        ),
        "uk": (
            '12.1 У разі невирішеного спору між вами та Nevumo ви можете звернутися '
            'до альтернативного вирішення спорів.\n\n'
            '12.2 [PL] Польські споживачі можуть звернутися до Inspekcja Handlowa (IH) '
            'для безкоштовного позасудового вирішення. '
            'ul. Sienkiewicza 3, 00-015 Варшава. '
            'Додаткова інформація: www.uokik.gov.pl/wazne_adresy.php\n\n'
            '12.3 Nevumo погоджується брати участь у процедурах АВС, коли цього '
            'вимагає застосовне законодавство.\n\n'
            '12.4 Платформа ODR Європейської комісії була остаточно закрита '
            '20 липня 2025 р. і більше не доступна.'
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
        print(f"✅ seed_terms_p12_bodies: {count} rows upserted ({NAMESPACE}, art12_body × 34 langs)")

    engine.dispose()


if __name__ == "__main__":
    seed()
