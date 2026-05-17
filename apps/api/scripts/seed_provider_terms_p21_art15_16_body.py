"""
seed_provider_terms_p21_art15_16_body.py  —  Nevumo | namespace: provider_terms
Key: art15_body, art16_body  (2 keys x 34 langs = 68 rows)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_provider_terms_p21_art15_16_body
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
    "art15_body": {
        "en": (
            "15.1 By publishing content on the Platform (photos, descriptions, service information), you grant Nevumo a non-exclusive, royalty-free, worldwide licence to use, display, reproduce, and adapt that content for the purpose of operating and promoting the Platform.\n\n"
            "15.2 This licence terminates upon deletion of the relevant content or termination of your account, except where the content has been shared in reviews or other records that must be retained for legal purposes.\n\n"
            "15.3 You warrant that you hold all necessary rights to the content you publish and that its publication does not infringe any third-party rights."
        ),
        "bg": (
            "1. Публикувайки съдържание в Платформата (снимки, описания, информация за услуги), Доставчикът предоставя на Nevumo неизключителен, безвъзмезден, световен лиценз за използване, показване, възпроизвеждане и адаптиране на това съдържание с цел управление и промоция на Платформата.\n\n"
            "2. Лицензът изтича при изтриване на съответното съдържание или прекратяване на акаунта на Доставчика, освен в случаите когато съдържанието е включено в отзиви или други записи, които трябва да бъдат съхранявани по правни причини.\n\n"
            "3. Доставчикът гарантира, че притежава всички необходими права върху публикуваното съдържание и че публикуването му не нарушава права на трети лица."
        ),
        "pl": (
            "1. Publikując treści na Platformie (zdjęcia, opisy, informacje o usługach), Dostawca udziela Nevumo niewyłącznej, bezpłatnej, ogólnoświatowej licencji na korzystanie, wyświetlanie, powielanie i adaptację tych treści w celu prowadzenia i promocji Platformy.\n\n"
            "2. Licencja wygasa z chwilą usunięcia danej treści lub rozwiązania konta Dostawcy, z wyjątkiem treści zawartych w opiniach lub innych dokumentach, które muszą być przechowywane z przyczyn prawnych.\n\n"
            "3. Dostawca zapewnia, że posiada wszelkie niezbędne prawa do publikowanych treści oraz że ich publikacja nie narusza żadnych praw osób trzecich."
        ),
        "de": (
            "15.1 Durch die Veröffentlichung von Inhalten auf der Plattform (Fotos, Beschreibungen, Serviceinformationen) gewähren Sie Nevumo eine nicht exklusive, gebührenfreie, weltweite Lizenz zur Nutzung, Anzeige, Vervielfältigung und Anpassung dieser Inhalte zum Zweck des Betriebs und der Bewerbung der Plattform.\n\n"
            "15.2 Diese Lizenz erlischt mit der Löschung des betreffenden Inhalts oder der Kündigung Ihres Kontos, es sei denn, der Inhalt wurde in Bewertungen oder anderen Aufzeichnungen geteilt, die aus rechtlichen Gründen aufbewahrt werden müssen.\n\n"
            "15.3 Sie garantieren, dass Sie alle erforderlichen Rechte an den von Ihnen veröffentlichten Inhalten besitzen und dass deren Veröffentlichung keine Rechte Dritter verletzt."
        ),
        "fr": (
            "15.1 En publiant du contenu sur la Plateforme (photos, descriptions, informations sur les services), vous accordez à Nevumo une licence non exclusive, libre de droits et mondiale pour utiliser, afficher, reproduire et adapter ce contenu aux fins d'exploitation et de promotion de la Plateforme.\n\n"
            "15.2 Cette licence prend fin lors de la suppression du contenu concerné ou de la résiliation de votre compte, sauf lorsque le contenu a été partagé dans des avis ou d'autres enregistrements qui doivent être conservés à des fins légales.\n\n"
            "15.3 Vous garantissez que vous détenez tous les droits nécessaires sur le contenu que vous publiez et que sa publication n'enfreint aucun droit de tiers."
        ),
        "es": (
            "15.1 Al publicar contenido en la Plataforma (fotos, descripciones, información de servicios), usted otorga a Nevumo una licencia no exclusiva, libre de regalías y mundial para usar, mostrar, reproducir y adaptar ese contenido con el fin de operar y promover la Plataforma.\n\n"
            "15.2 Esta licencia termina con la eliminación del contenido relevante o la cancelación de su cuenta, excepto cuando el contenido se haya compartido en reseñas u otros registros que deban conservarse por motivos legales.\n\n"
            "15.3 Usted garantiza que posee todos los derechos necesarios sobre el contenido que publica y que su publicación no infringe ningún derecho de terceros."
        ),
        "it": (
            "15.1 Pubblicando contenuti sulla Piattaforma (foto, descrizioni, informazioni sui servizi), concedi a Nevumo una licenza non esclusiva, gratuita e mondiale per utilizzare, visualizzare, riprodurre e adattare tali contenuti allo scopo di gestire e promuovere la Piattaforma.\n\n"
            "15.2 Questa licenza termina con l'eliminazione dei contenuti pertinenti o la chiusura del tuo account, tranne nel caso in cui i contenuti siano stati condivisi in recensioni o altri record che devono essere conservati per motivi legali.\n\n"
            "15.3 Garantisci di detenere tutti i diritti necessari sui contenuti che pubblichi e che la loro pubblicazione non viola i diritti di terzi."
        ),
        "nl": (
            "15.1 Door inhoud op het Platform te publiceren (foto's, beschrijvingen, dienstinformatie), verleent u Nevumo een niet-exclusieve, royaltyvrije, wereldwijde licentie om die inhoud te gebruiken, weer te geven, te reproduceren en aan te passen voor het exploiteren en promoten van het Platform.\n\n"
            "15.2 Deze licentie eindigt bij verwijdering van de betreffende inhoud of beëindiging van uw account, behalve wanneer de inhoud is gedeeld in beoordelingen of andere gegevens die om juridische redenen moeten worden bewaard.\n\n"
            "15.3 U garandeert dat u over alle noodzakelijke rechten beschikt op de inhoud die u publiceert en dat de publicatie ervan geen inbreuk maakt op de rechten van derden."
        ),
        "pt": (
            "15.1 Ao publicar conteúdo na Plataforma (fotos, descrições, informações de serviços), concede à Nevumo uma licença não exclusiva, isenta de royalties e mundial para usar, exibir, reproduzir e adaptar esse conteúdo com o propósito de operar e promover a Plataforma.\n\n"
            "15.2 Esta licença termina com a eliminação do conteúdo relevante ou com a rescisão da sua conta, exceto quando o conteúdo tiver sido partilhado em avaliações ou outros registos que devam ser retidos por motivos legais.\n\n"
            "15.3 Garante que detém todos os direitos necessários sobre o conteúdo que publica e que a sua publicação não infringe quaisquer direitos de terceiros."
        ),
        "pt-PT": (
            "15.1 Ao publicar conteúdo na Plataforma (fotos, descrições, informações de serviços), concede à Nevumo uma licença não exclusiva, isenta de royalties e mundial para usar, exibir, reproduzir e adaptar esse conteúdo com o propósito de operar e promover a Plataforma.\n\n"
            "15.2 Esta licença termina com a eliminação do conteúdo relevante ou com a rescisão da sua conta, exceto quando o conteúdo tiver sido partilhado em avaliações ou outros registos que devam ser retidos por motivos legais.\n\n"
            "15.3 Garante que detém todos os direitos necessários sobre o conteúdo que publica e que a sua publicação não infringe quaisquer direitos de terceiros."
        ),
        "ro": (
            "15.1 Prin publicarea de conținut pe Platformă (fotografii, descrieri, informații despre servicii), acordați Nevumo o licență neexclusivă, gratuită și la nivel mondial pentru a utiliza, afișa, reproduce și adapta acel conținut în scopul operării și promovării Platformei.\n\n"
            "15.2 Această licență se termină la ștergerea conținutului relevant sau la închiderea contului dumneavoastră, cu excepția cazului în care conținutul a fost partajat în recenzii sau alte înregistrări care trebuie păstrate din motive legale.\n\n"
            "15.3 Garantați că dețineți toate drepturile necesare asupra conținutului pe care îl publicați și că publicarea acestuia nu încalcă niciun drept al terților."
        ),
        "ru": (
            "15.1 Публикуя контент на Платформе (фотографии, описания, информацию об услугах), вы предоставляете Nevumo неисключительную, бесплатную, всемирную лицензию на использование, отображение, воспроизведение и адаптацию этого контента в целях работы и продвижения Платформы.\n\n"
            "15.2 Эта лицензия прекращает свое действие после удаления соответствующего контента или закрытия вашей учетной записи, за исключением случаев, когда контент был опубликован в отзывах или других записях, которые должны сохраняться в юридических целях.\n\n"
            "15.3 Вы гарантируете, что обладаете всеми необходимыми правами на публикуемый вами контент и что его публикация не нарушает права третьих лиц."
        ),
        "uk": (
            "15.1 Публікуючи контент на Платформі (фотографії, описи, інформацію про послуги), ви надаєте Nevumo невиключну, безоплатну, всесвітню ліцензію на використання, відображення, відтворення та адаптацію цього контенту з метою роботи та просування Платформи.\n\n"
            "15.2 Ця ліцензія припиняє свою дію після видалення відповідного контенту або закриття вашого облікового запису, за винятком випадків, коли контент був опублікований у відгуках або інших записах, які повинні зберігатися з юридичною метою.\n\n"
            "15.3 Ви гарантуєте, що володієте всіма необхідними правами на контент, який публікуєте, і що його публікація не порушує права третіх осіб."
        ),
        "cs": (
            "15.1 Publikováním obsahu na platformě (fotografie, popisy, informace o službách) udělujete společnosti Nevumo nevýhradní, bezplatnou, celosvětovou licenci k používání, zobrazování, reprodukování a úpravám tohoto obsahu za účelem provozování a propagace platformy.\n\n"
            "15.2 Tato licence končí po smazání příslušného obsahu nebo ukončení vašeho účtu, s výjimkou případů, kdy byl obsah sdílen v recenzích nebo jiných záznamech, které musí být uchovávány z právních důvodů.\n\n"
            "15.3 Zaručujete, že vlastníte veškerá nezbytná práva k obsahu, který publikujete, a že jeho zveřejnění neporušuje žádná práva třetích stran."
        ),
        "da": (
            "15.1 Ved at offentliggøre indhold på platformen (fotos, beskrivelser, tjenesteoplysninger) giver du Nevumo en ikke-eksklusiv, royaltyfri, verdensomspændende licens til at bruge, vise, reproducere og tilpasse dette indhold med det formål at drive og promovere platformen.\n\n"
            "15.2 Denne licens ophører ved sletning af det relevante indhold eller opsigelse af din konto, undtagen hvor indholdet er blevet delt i anmeldelser eller andre optegnelser, der skal opbevares af juridiske årsager.\n\n"
            "15.3 Du garanterer, at du har alle nødvendige rettigheder til det indhold, du offentliggør, og at dets offentliggørelse ikke krænker nogen tredjeparts rettigheder."
        ),
        "sv": (
            "15.1 Genom att publicera innehåll på plattformen (foton, beskrivningar, tjänsteinformation) ger du Nevumo en icke-exklusiv, royaltyfri, global licens att använda, visa, reproducera och anpassa detta innehåll i syfte att driva och marknadsföra plattformen.\n\n"
            "15.2 Denna licens upphör att gälla vid radering av relevant innehåll eller uppsägning av ditt konto, förutom när innehållet har delats i recensioner eller andra register som måste sparas av juridiska skäl.\n\n"
            "15.3 Du garanterar att du innehar alla nödvändiga rättigheter till det innehåll du publicerar och att dess publicering inte gör intrång i tredje parts rättigheter."
        ),
        "no": (
            "15.1 Ved å publisere innhold på plattformen (bilder, beskrivelser, tjenesteinformasjon), gir du Nevumo en ikke-eksklusiv, avgiftsfri, verdensomspennende lisens til å bruke, vise, reprodusere og tilpasse slikt innhold for formålet med å drifte og markedsføre plattformen.\n\n"
            "15.2 Denne lisensen opphører ved sletting av relevant innhold eller oppsigelse av kontoen din, unntatt der innholdet har blitt delt i anmeldelser eller andre registre som må beholdes av juridiske årsaker.\n\n"
            "15.3 Du garanterer at du innehar alle nødvendige rettigheter til innholdet du publiserer, og at publiseringen ikke krenker tredjeparts rettigheter."
        ),
        "fi": (
            "15.1 Julkaisemalla sisältöä alustalla (valokuvia, kuvauksia, palvelutietoja) myönnät Nevumolle ei-yksinomaisen, rojaltivapaan, maailmanlaajuisen lisenssin käyttää, näyttää, jäljentää ja muokata tätä sisältöä alustan ylläpitämistä ja markkinointia varten.\n\n"
            "15.2 Tämä lisenssi päättyy asianomaisen sisällön poistamisen tai tilisi irtisanomisen yhteydessä, paitsi silloin, kun sisältö on jaettu arvosteluissa tai muissa tietueissa, jotka on säilytettävä oikeudellisista syistä.\n\n"
            "15.3 Takaat, että sinulla on kaikki tarvittavat oikeudet julkaisemaasi sisältöön ja että sen julkaiseminen ei loukkaa kolmansien osapuolten oikeuksia."
        ),
        "et": (
            "15.1 Avaldades platvormil sisu (fotod, kirjeldused, teenusteave), annate Nevumole mitteeksklusiivse, kasutustasuta, ülemaailmse litsentsi selle sisu kasutamiseks, kuvamiseks, reprodutseerimiseks ja kohandamiseks platvormi haldamise ja reklaamimise eesmärgil.\n\n"
            "15.2 See litsents lõpeb asjakohase sisu kustutamisel või teie konto lõpetamisel, välja arvatud juhul, kui sisu on jagatud arvustustes või muudes dokumentides, mis tuleb õiguslikel põhjustel säilitada.\n\n"
            "15.3 Garanteerite, et teil on kõik vajalikud õigused avaldatavale sisule ja et selle avaldamine ei riku kolmandate isikute õigusi."
        ),
        "lt": (
            "15.1 Skelbdami turinį platformoje (nuotraukas, aprašymus, paslaugų informaciją), suteikiate „Nevumo“ neišimtinę, nemokamą, pasaulinę licenciją naudoti, rodyti, atgaminti ir pritaikyti šį turinį siekiant valdyti ir reklamuoti platformą.\n\n"
            "15.2 Ši licencija baigiasi ištrynus atitinkamą turinį arba nutraukus jūsų paskyrą, išskyrus atvejus, kai turinys buvo bendrinamas atsiliepimuose ar kituose įrašuose, kurie turi būti saugomi dėl teisinių priežasčių.\n\n"
            "15.3 Jūs garantuojate, kad turite visas būtinas teises į skelbiamą turinį ir kad jo paskelbimas nepažeidžia jokių trečiųjų šalių teisių."
        ),
        "lv": (
            "15.1 Publicējot saturu Platformā (fotoattēlus, aprakstus, informāciju par pakalpojumiem), jūs piešķirat Nevumo neekskluzīvu, bezmaksas, vispasaules licenci izmantot, parādīt, reproducēt un pielāgot šo saturu Platformas darbības un popularizēšanas nolūkā.\n\n"
            "15.2 Šī licence beidzas, izdzēšot attiecīgo saturu vai izbeidzot jūsu kontu, izņemot gadījumus, kad saturs ir kopīgots atsauksmēs vai citos ierakstos, kas jāsaglabā juridisku iemeslu dēļ.\n\n"
            "15.3 Jūs garantējat, ka jums pieder visas nepieciešamās tiesības uz jūsu publicēto saturu un ka tā publicēšana nepārkāpj nevienas trešās puses tiesības."
        ),
        "hu": (
            "15.1 Ha tartalmat (fotókat, leírásokat, szolgáltatási információkat) tesz közzé a Platformon, nem kizárólagos, jogdíjmentes, világméretű licencet ad a Nevumo-nak arra, hogy ezt a tartalmat a Platform működtetése és népszerűsítése céljából felhasználja, megjelenítse, reprodukálja és átdolgozza.\n\n"
            "15.2 Ez a licenc a vonatkozó tartalom törlésekor vagy a fiók megszüntetésekor jár le, kivéve, ha a tartalmat olyan véleményekben vagy egyéb nyilvántartásokban osztották meg, amelyeket jogi okokból meg kell őrizni.\n\n"
            "15.3 Ön garantálja, hogy rendelkezik a közzétett tartalomhoz szükséges összes joggal, és hogy annak közzététele nem sérti harmadik felek jogait."
        ),
        "hr": (
            "15.1 Objavljivanjem sadržaja na Platformi (fotografije, opisi, informacije o uslugama), dajete tvrtki Nevumo neekskluzivnu, besplatnu, globalnu licencu za korištenje, prikazivanje, reprodukciju i prilagodbu tog sadržaja u svrhu rada i promocije Platforme.\n\n"
            "15.2 Ova licenca prestaje brisanjem relevantnog sadržaja ili zatvaranjem vašeg računa, osim ako je sadržaj podijeljen u recenzijama ili drugim zapisima koji se moraju zadržati iz pravnih razloga.\n\n"
            "15.3 Jamčite da posjedujete sva potrebna prava na sadržaj koji objavljujete i da njegova objava ne krši prava trećih strana."
        ),
        "sk": (
            "15.1 Publikovaním obsahu na platforme (fotografie, popisy, informácie o službách) udeľujete spoločnosti Nevumo nevýhradnú, bezplatnú, celosvetovú licenciu na používanie, zobrazovanie, reprodukovanie a úpravu tohto obsahu na účely prevádzkovania a propagácie platformy.\n\n"
            "15.2 Táto licencia končí po vymazaní príslušného obsahu alebo ukončení vášho účtu, s výnimkou prípadov, keď bol obsah zdieľaný v recenziách alebo iných záznamoch, ktoré sa musia uchovávať z právnych dôvodov.\n\n"
            "15.3 Zaručujete, že vlastníte všetky potrebné práva na obsah, ktorý publikujete, a že jeho zverejnenie neporušuje žiadne práva tretích strán."
        ),
        "sl": (
            "15.1 Z objavo vsebine na platformi (fotografije, opisi, informacije o storitvah) dajete podjetju Nevumo neizključno, brezplačno, svetovno licenco za uporabo, prikazovanje, reprodukcijo in prilagajanje te vsebine z namenom upravljanja in promocije platforme.\n\n"
            "15.2 Ta licenca preneha ob izbrisu zadevne vsebine ali prekinitvi vašega računa, razen če je bila vsebina deljena v ocenah ali drugih evidencah, ki jih je treba hraniti iz pravnih razlogov.\n\n"
            "15.3 Zagotavljate, da imate vse potrebne pravice do vsebine, ki jo objavite, in da njena objava ne krši nobenih pravic tretjih oseb."
        ),
        "el": (
            "15.1 Δημοσιεύοντας περιεχόμενο στην Πλατφόρμα (φωτογραφίες, περιγραφές, πληροφορίες υπηρεσιών), παραχωρείτε στη Nevumo μια μη αποκλειστική, χωρίς δικαιώματα, παγκόσμια άδεια χρήσης, προβολής, αναπαραγωγής και προσαρμογής αυτού του περιεχομένου με σκοπό τη λειτουργία και την προώθηση της Πλατφόρμας.\n\n"
            "15.2 Αυτή η άδεια τερματίζεται με τη διαγραφή του σχετικού περιεχομένου ή τον τερματισμό του λογαριασμού σας, εκτός από περιπτώσεις όπου το περιεχόμενο έχει κοινοποιηθεί σε κριτικές ή άλλα αρχεία που πρέπει να διατηρηθούν για νομικούς λόγους.\n\n"
            "15.3 Εγγυάστε ότι διαθέτετε όλα τα απαραίτητα δικαιώματα για το περιεχόμενο που δημοσιεύετε και ότι η δημοσίευσή του δεν παραβιάζει δικαιώματα τρίτων."
        ),
        "tr": (
            "15.1 Platformda içerik (fotoğraflar, açıklamalar, hizmet bilgileri) yayınlayarak, Nevumo'ya bu içeriği Platformu işletmek ve tanıtmak amacıyla kullanmak, görüntülemek, çoğaltmak ve uyarlamak için münhasır olmayan, telifsiz, dünya çapında bir lisans vermiş olursunuz.\n\n"
            "15.2 Bu lisans, içeriğin yasal nedenlerle saklanması gereken incelemelerde veya diğer kayıtlarda paylaşıldığı durumlar hariç, ilgili içeriğin silinmesi veya hesabınızın feshedilmesi üzerine sona erer.\n\n"
            "15.3 Yayınladığınız içerik için gerekli tüm haklara sahip olduğunuzu ve yayınlanmasının herhangi bir üçüncü tarafın haklarını ihlal etmediğini garanti edersiniz."
        ),
        "ga": (
            "15.1 Trí ábhar a fhoilsiú ar an Ardán (grianghraif, tuairiscí, faisnéis seirbhíse), deonaíonn tú ceadúnas neamheisiach, saor ó ríchíosanna, domhanda do Nevumo chun an t-ábhar sin a úsáid, a thaispeáint, a atáirgeadh agus a oiriúnú chun an tArdán a oibriú agus a chur chun cinn.\n\n"
            "15.2 Críochnaíonn an ceadúnas seo nuair a scriostar an t-ábhar ábhartha nó nuair a fhoirceanntar do chuntas, ach amháin i gcás ina roinneadh an t-ábhar i léirmheasanna nó i dtaifid eile nach mór a choinneáil chun críocha dlíthiúla.\n\n"
            "15.3 Bheir tú barántas go bhfuil gach ceart riachtanach agat ar an ábhar a fhoilsíonn tú agus nach sáraíonn a fhoilsiú aon chearta tríú páirtí."
        ),
        "is": (
            "15.1 Með því að birta efni á vettvangnum (ljósmyndir, lýsingar, þjónustuupplýsingar) veitirðu Nevumo ótímabundið, gjaldfrjálst og alþjóðlegt leyfi til að nota, sýna, afrita og aðlaga það efni í þeim tilgangi að reka og kynna vettvanginn.\n\n"
            "15.2 Þetta leyfi rennur út þegar viðkomandi efni er eytt eða reikningi þínum sagt upp, nema efnið hafi verið deilt í umsögnum eða öðrum skrám sem þarf að varðveita af lagalegum ástæðum.\n\n"
            "15.3 Þú ábyrgist að þú eigir öll nauðsynleg réttindi að því efni sem þú birtir og að birting þess brjóti ekki í bága við réttindi þriðja aðila."
        ),
        "lb": (
            "15.1 Andeems Dir Inhalt op der Plattform publizéiert (Fotoen, Beschreiwungen, Serviceinformatiounen), gitt Dir Nevumo eng net-exklusiv, lizenzfräi, weltwäit Lizenz fir dësen Inhalt ze benotzen, ze weisen, ze reproduzéieren an unzepassen fir den Zweck d'Plattform ze bedreiwen an ze promoten.\n\n"
            "15.2 Dës Lizenz hält op mat der Läschung vum relevanten Inhalt oder der Kënnegung vun Ärem Kont, ausser wou den Inhalt a Bewäertungen oder aner records gedeelt gouf, déi fir legal Zwecker erhale musse ginn.\n\n"
            "15.3 Dir garantéiert, datt Dir all néideg Rechter un deem vun Iech publizéierten Inhalt besëtzt an datt seng Verëffentlechung keng Rechter vun Drëtten verletzt."
        ),
        "mk": (
            "15.1 Со објавување содржина на Платформата (фотографии, описи, информации за услуги), вие му доделувате на Nevumo неексклузивна, бесплатна, светска лиценца за користење, прикажување, репродуцирање и прилагодување на таа содржина со цел управување и промоција на Платформата.\n\n"
            "15.2 Оваа лиценца престанува по бришењето на соодветната содржина или раскинувањето на вашиот профил, освен каде што содржината е споделена во прегледи или други записи кои мора да се задржат од правни причини.\n\n"
            "15.3 Вие гарантирате дека ги имате сите потребни права за содржината што ја објавувате и дека нејзиното објавување не прекршува права на трети страни."
        ),
        "mt": (
            "15.1 Billi tippubblika kontenut fuq il-Pjattaforma (ritratti, deskrizzjonijiet, informazzjoni dwar is-servizz), int tagħti lil Nevumo liċenzja mhux esklussiva, mingħajr royalties, mad-dinja kollha biex tuża, turi, tirriproduċi, u tadatta dak il-kontenut għall-iskop ta' tħaddim u promozzjoni tal-Pjattaforma.\n\n"
            "15.2 Din il-liċenzja tittermina mat-tħassir tal-kontenut rilevanti jew it-terminazzjoni tal-kont tiegħek, ħlief fejn il-kontenut ikun ġie maqsum f'reviżjonijiet jew rekords oħra li għandhom jinżammu għal skopijiet legali.\n\n"
            "15.3 Int tiggarantixxi li inti għandek id-drittijiet kollha meħtieġa għall-kontenut li tippubblika u li l-pubblikazzjoni tiegħu ma tiksirx id-drittijiet ta' kwalunkwe parti terza."
        ),
        "sq": (
            "15.1 Duke publikuar përmbajtje në Platformë (foto, përshkrime, informacione për shërbimet), ju i jepni Nevumo një licencë jo-ekskluzive, pa pagesë, mbarëbotërore për të përdorur, shfaqur, riprodhuar dhe përshtatur atë përmbajtje me qëllim operimin dhe promovimin e Platformës.\n\n"
            "15.2 Kjo licencë përfundon pas fshirjes së përmbajtjes përkatëse ose përfundimit të llogarisë suaj, përveç rasteve kur përmbajtja është ndarë në rishikime ose të dhëna të tjera që duhet të mbahen për arsye ligjore.\n\n"
            "15.3 Ju garantoni se i keni të gjitha të drejtat e nevojshme për përmbajtjen që publikoni dhe se publikimi i saj nuk cenon asnjë të drejtë të palëve të treta."
        ),
        "sr": (
            "15.1 Objavljivanjem sadržaja na Platformi (fotografije, opisi, informacije o uslugama), dajete kompaniji Nevumo neekskluzivnu, besplatnu, globalnu licencu za korišćenje, prikazivanje, reprodukciju i prilagođavanje tog sadržaja u svrhu rada i promocije Platforme.\n\n"
            "15.2 Ova licenca prestaje brisanjem relevantnog sadržaja ili zatvaranjem vašeg naloga, osim kada je sadržaj podeljen u recenzijama ili drugim zapisima koji se moraju zadržati iz pravnih razloga.\n\n"
            "15.3 Garantujete da posedujete sva neophodna prava na sadržaj koji objavljujete i da njegovo objavljivanje ne krši prava trećih lica."
        ),
    },
    "art16_body": {
        "en": (
            "16.1 Nevumo processes Provider personal data as a data controller in accordance with the Privacy Policy available at nevumo.com/privacy.\n\n"
            "16.2 Nevumo's processing of Provider personal data is based on:\n"
            "- the performance of the contractual relationship established by these Provider Terms (Article 6(1)(b) GDPR);\n"
            "- compliance with legal obligations (Article 6(1)(c) GDPR);\n"
            "- Nevumo's legitimate interests in operating and improving the Platform (Article 6(1)(f) GDPR).\n\n"
            "16.3 Providers acting as traders and using the Platform to collect and process Client personal data act as independent data controllers in respect of that data. Nevumo is not a joint controller for such processing."
        ),
        "bg": (
            "1. Nevumo обработва личните данни на Доставчиците в качеството си на администратор на лични данни в съответствие с Политиката за поверителност, достъпна на nevumo.com/privacy.\n\n"
            "2. Правните основания за обработване на лични данни на Доставчиците от Nevumo са:\n"
            "- изпълнение на договорното правоотношение, установено с настоящите Условия за Доставчици (чл. 6, пар. 1, б. „б“ от ОРЗД);\n"
            "- изпълнение на правни задължения (чл. 6, пар. 1, б. „в“ от ОРЗД);\n"
            "- легитимните интереси на Nevumo, свързани с управлението и подобряването на Платформата (чл. 6, пар. 1, б. „е“ от ОРЗД).\n\n"
            "3. Доставчиците, действащи като търговци и използващи Платформата за събиране и обработване на лични данни на Клиенти, действат като независими администратори на лични данни по отношение на такова обработване. Nevumo не е съвместен администратор на лични данни за тази обработка."
        ),
        "pl": (
            "1. Nevumo przetwarza dane osobowe Dostawców jako administrator danych zgodnie z Polityką Prywatności dostępną pod adresem nevumo.com/privacy.\n\n"
            "2. Podstawy prawne przetwarzania danych osobowych Dostawców przez Nevumo:\n"
            "- wykonanie umowy wynikającej z niniejszego Regulaminu Dostawców (art. 6 ust. 1 lit. b RODO);\n"
            "- wypełnienie obowiązków prawnych (art. 6 ust. 1 lit. c RODO);\n"
            "- uzasadnione interesy Nevumo polegające na prowadzeniu i doskonaleniu Platformy (art. 6 ust. 1 lit. f RODO).\n\n"
            "3. Dostawcy działający jako przedsiębiorcy i korzystający z Platformy w celu gromadzenia i przetwarzania danych osobowych Klientów działają jako niezależni administratorzy danych w odniesieniu do takiego przetwarzania. Nevumo nie jest wspólnym administratorem danych w zakresie tego przetwarzania."
        ),
        "de": (
            "16.1 Nevumo verarbeitet personenbezogene Daten von Anbietern als Verantwortlicher in Übereinstimmung mit der unter nevumo.com/privacy verfügbaren Datenschutzrichtlinie.\n\n"
            "16.2 Die Verarbeitung der personenbezogenen Daten von Anbietern durch Nevumo basiert auf:\n"
            "- der Erfüllung des durch diese Anbieterbedingungen begründeten Vertragsverhältnisses (Art. 6 Abs. 1 lit. b DSGVO);\n"
            "- der Erfüllung rechtlicher Verpflichtungen (Art. 6 Abs. 1 lit. c DSGVO);\n"
            "- den berechtigten Interessen von Nevumo am Betrieb und an der Verbesserung der Plattform (Art. 6 Abs. 1 lit. f DSGVO).\n\n"
            "16.3 Anbieter, die als Händler handeln und die Plattform zur Erhebung und Verarbeitung personenbezogener Daten von Kunden nutzen, handeln in Bezug auf diese Daten als unabhängige Verantwortliche. Nevumo ist für diese Verarbeitung kein gemeinsam Verantwortlicher."
        ),
        "fr": (
            "16.1 Nevumo traite les données personnelles des Fournisseurs en tant que responsable du traitement conformément à la Politique de confidentialité disponible sur nevumo.com/privacy.\n\n"
            "16.2 Le traitement par Nevumo des données personnelles des Fournisseurs est basé sur :\n"
            "- l'exécution de la relation contractuelle établie par les présentes Conditions pour les Fournisseurs (Article 6(1)(b) du RGPD) ;\n"
            "- le respect des obligations légales (Article 6(1)(c) du RGPD) ;\n"
            "- les intérêts légitimes de Nevumo dans l'exploitation et l'amélioration de la Plateforme (Article 6(1)(f) du RGPD).\n\n"
            "16.3 Les Fournisseurs agissant en tant que professionnels et utilisant la Plateforme pour collecter et traiter les données personnelles des Clients agissent en tant que responsables du traitement indépendants à l'égard de ces données. Nevumo n'est pas un responsable conjoint pour ce traitement."
        ),
        "es": (
            "16.1 Nevumo procesa los datos personales de los Proveedores como controlador de datos de acuerdo con la Política de privacidad disponible en nevumo.com/privacy.\n\n"
            "16.2 El procesamiento por parte de Nevumo de los datos personales de los Proveedores se basa en:\n"
            "- la ejecución de la relación contractual establecida por estas Condiciones para Proveedores (Artículo 6(1)(b) del RGPD);\n"
            "- el cumplimiento de las obligaciones legales (Artículo 6(1)(c) del RGPD);\n"
            "- los intereses legítimos de Nevumo en la operación y mejora de la Plataforma (Artículo 6(1)(f) del RGPD).\n\n"
            "16.3 Los Proveedores que actúan como comerciantes y utilizan la Plataforma para recopilar y procesar datos personales de Clientes actúan como controladores de datos independientes con respecto a esos datos. Nevumo no es un controlador conjunto para dicho procesamiento."
        ),
        "it": (
            "16.1 Nevumo tratta i dati personali dei Fornitori in qualità di titolare del trattamento in conformità con l'Informativa sulla privacy disponibile su nevumo.com/privacy.\n\n"
            "16.2 Il trattamento dei dati personali dei Fornitori da parte di Nevumo si basa su:\n"
            "- l'esecuzione del rapporto contrattuale stabilito dalle presenti Condizioni per i Fornitori (Articolo 6, paragrafo 1, lettera b) del GDPR);\n"
            "- il rispetto degli obblighi legali (Articolo 6, paragrafo 1, lettera c) del GDPR);\n"
            "- i legittimi interessi di Nevumo nella gestione e nel miglioramento della Piattaforma (Articolo 6, paragrafo 1, lettera f) del GDPR).\n\n"
            "16.3 I Fornitori che agiscono in qualità di professionisti e utilizzano la Piattaforma per raccogliere e trattare i dati personali dei Clienti agiscono in qualità di titolari del trattamento indipendenti rispetto a tali dati. Nevumo non è un contitolare del trattamento per tale trattamento."
        ),
        "nl": (
            "16.1 Nevumo verwerkt persoonsgegevens van Dienstverleners als verwerkingsverantwoordelijke in overeenstemming met het Privacybeleid dat beschikbaar is op nevumo.com/privacy.\n\n"
            "16.2 De verwerking van persoonsgegevens van Dienstverleners door Nevumo is gebaseerd op:\n"
            "- de uitvoering van de contractuele relatie die is vastgesteld door deze Voorwaarden voor Dienstverleners (artikel 6, lid 1, onder b, van de AVG);\n"
            "- naleving van wettelijke verplichtingen (artikel 6, lid 1, onder c, van de AVG);\n"
            "- de gerechtvaardigde belangen van Nevumo bij de exploitatie en verbetering van het Platform (artikel 6, lid 1, onder f, van de AVG).\n\n"
            "16.3 Dienstverleners die als handelaren optreden en het Platform gebruiken om persoonsgegevens van Klanten te verzamelen en te verwerken, treden op als onafhankelijke verwerkingsverantwoordelijken met betrekking tot die gegevens. Nevumo is geen gezamenlijke verwerkingsverantwoordelijke voor dergelijke verwerking."
        ),
        "pt": (
            "16.1 A Nevumo trata os dados pessoais dos Prestadores enquanto responsável pelo tratamento de acordo com a Política de Privacidade disponível em nevumo.com/privacy.\n\n"
            "16.2 O tratamento dos dados pessoais dos Prestadores por parte da Nevumo baseia-se:\n"
            "- na execução da relação contratual estabelecida por estes Termos para Prestadores (Artigo 6.º, n.º 1, alínea b) do RGPD);\n"
            "- no cumprimento de obrigações legais (Artigo 6.º, n.º 1, alínea c) do RGPD);\n"
            "- nos interesses legítimos da Nevumo em operar e melhorar a Plataforma (Artigo 6.º, n.º 1, alínea f) do RGPD).\n\n"
            "16.3 Os Prestadores que atuam como comerciantes e utilizam a Plataforma para recolher e tratar dados pessoais dos Clientes atuam como responsáveis independentes pelo tratamento no que diz respeito a esses dados. A Nevumo não é responsável conjunta por tal tratamento."
        ),
        "pt-PT": (
            "16.1 A Nevumo trata os dados pessoais dos Prestadores enquanto responsável pelo tratamento de acordo com a Política de Privacidade disponível em nevumo.com/privacy.\n\n"
            "16.2 O tratamento dos dados pessoais dos Prestadores por parte da Nevumo baseia-se:\n"
            "- na execução da relação contratual estabelecida por estes Termos para Prestadores (Artigo 6.º, n.º 1, alínea b) do RGPD);\n"
            "- no cumprimento de obrigações legais (Artigo 6.º, n.º 1, alínea c) do RGPD);\n"
            "- nos interesses legítimos da Nevumo em operar e melhorar a Plataforma (Artigo 6.º, n.º 1, alínea f) do RGPD).\n\n"
            "16.3 Os Prestadores que atuam como comerciantes e utilizam a Plataforma para recolher e tratar dados pessoais dos Clientes atuam como responsáveis independentes pelo tratamento no que diz respeito a esses dados. A Nevumo não é responsável conjunta por tal tratamento."
        ),
        "ro": (
            "16.1 Nevumo prelucrează datele cu caracter personal ale Furnizorilor în calitate de operator de date în conformitate cu Politica de confidențialitate disponibilă la nevumo.com/privacy.\n\n"
            "16.2 Prelucrarea de către Nevumo a datelor cu caracter personal ale Furnizorilor se bazează pe:\n"
            "- executarea relației contractuale stabilite prin acești Termeni pentru Furnizori (Articolul 6 alineatul (1) litera (b) din GDPR);\n"
            "- respectarea obligațiilor legale (Articolul 6 alineatul (1) litera (c) din GDPR);\n"
            "- interesele legitime ale Nevumo în operarea și îmbunătățirea Platformei (Articolul 6 alineatul (1) litera (f) din GDPR).\n\n"
            "16.3 Furnizorii care acționează în calitate de comercianți și utilizează Platforma pentru a colecta și prelucra date cu caracter personal ale Clienților acționează în calitate de operatori de date independenți în ceea ce privește acele date. Nevumo nu este operator asociat pentru o astfel de prelucrare."
        ),
        "ru": (
            "16.1 Nevumo обрабатывает персональные данные Поставщиков как контролер данных в соответствии с Политикой конфиденциальности, доступной на nevumo.com/privacy.\n\n"
            "16.2 Обработка персональных данных Поставщиков со стороны Nevumo основана на:\n"
            "- исполнении договорных отношений, установленных настоящими Условиями для Поставщиков (статья 6(1)(b) GDPR);\n"
            "- соблюдении юридических обязательств (статья 6(1)(c) GDPR);\n"
            "- законных интересах Nevumo в работе и улучшении Платформы (статья 6(1)(f) GDPR).\n\n"
            "16.3 Поставщики, действующие в качестве коммерсантов и использующие Платформу для сбора и обработки персональных данных Клиентов, действуют как независимые контролеры данных в отношении этих данных. Nevumo не является совместным контролером для такой обработки."
        ),
        "uk": (
            "16.1 Nevumo обробляє персональні дані Постачальників як контролер даних відповідно до Політики конфіденційності, доступної на nevumo.com/privacy.\n\n"
            "16.2 Обробка персональних даних Постачальників з боку Nevumo ґрунтується на:\n"
            "- виконанні договірних відносин, встановлених цими Умовами для Постачальників (стаття 6(1)(b) GDPR);\n"
            "- дотриманні юридичних зобов'язань (стаття 6(1)(c) GDPR);\n"
            "- законних інтересах Nevumo в роботі та покращенні Платформи (стаття 6(1)(f) GDPR).\n\n"
            "16.3 Постачальники, що діють як комерсанти і використовують Платформу для збору та обробки персональних даних Клієнтів, діють як незалежні контролери даних щодо цих даних. Nevumo не є спільним контролером для такої обробки."
        ),
        "cs": (
            "16.1 Společnost Nevumo zpracovává osobní údaje poskytovatelů jako správce údajů v souladu se Zásadami ochrany osobních údajů dostupnými na nevumo.com/privacy.\n\n"
            "16.2 Zpracování osobních údajů poskytovatelů společností Nevumo je založeno na:\n"
            "- plnění smluvního vztahu založeného těmito podmínkami pro poskytovatele (čl. 6 odst. 1 písm. b) GDPR);\n"
            "- plnění zákonných povinností (čl. 6 odst. 1 písm. c) GDPR);\n"
            "- oprávněných zájmech společnosti Nevumo na provozování a zlepšování platformy (čl. 6 odst. 1 písm. f) GDPR).\n\n"
            "16.3 Poskytovatelé jednající jako obchodníci a používající platformu ke shromažďování a zpracování osobních údajů klientů jednají jako nezávislí správci údajů ve vztahu k těmto údajům. Společnost Nevumo není společným správcem pro takové zpracování."
        ),
        "da": (
            "16.1 Nevumo behandler udbyderes personoplysninger som dataansvarlig i overensstemmelse med privatlivspolitikken tilgængelig på nevumo.com/privacy.\n\n"
            "16.2 Nevumos behandling af udbyderes personoplysninger er baseret på:\n"
            "- opfyldelsen af kontraktforholdet etableret ved disse vilkår for udbydere (GDPR artikel 6(1)(b));\n"
            "- overholdelse af juridiske forpligtelser (GDPR artikel 6(1)(c));\n"
            "- Nevumos legitime interesser i at drive og forbedre platformen (GDPR artikel 6(1)(f)).\n\n"
            "16.3 Udbydere, der optræder som erhvervsdrivende og bruger platformen til at indsamle og behandle kunders personoplysninger, optræder som uafhængige dataansvarlige med hensyn til disse data. Nevumo er ikke en fælles dataansvarlig for en sådan behandling."
        ),
        "sv": (
            "16.1 Nevumo behandlar leverantörers personuppgifter som personuppgiftsansvarig i enlighet med integritetspolicyn som finns tillgänglig på nevumo.com/privacy.\n\n"
            "16.2 Nevumos behandling av leverantörers personuppgifter baseras på:\n"
            "- fullgörandet av det avtalsförhållande som upprättats genom dessa villkor för leverantörer (artikel 6.1 b i GDPR);\n"
            "- efterlevnad av rättsliga skyldigheter (artikel 6.1 c i GDPR);\n"
            "- Nevumos berättigade intressen att driva och förbättra plattformen (artikel 6.1 f i GDPR).\n\n"
            "16.3 Leverantörer som agerar som näringsidkare och använder plattformen för att samla in och behandla kunders personuppgifter agerar som oberoende personuppgiftsansvariga för dessa uppgifter. Nevumo är inte gemensamt personuppgiftsansvarig för sådan behandling."
        ),
        "no": (
            "16.1 Nevumo behandler leverandørers personopplysninger som behandlingsansvarlig i samsvar med personvernerklæringen som er tilgjengelig på nevumo.com/privacy.\n\n"
            "16.2 Nevumos behandling av leverandørers personopplysninger er basert på:\n"
            "- oppfyllelsen av kontraktsforholdet etablert ved disse vilkårene for leverandører (GDPR artikkel 6(1)(b));\n"
            "- overholdelse av juridiske forpliktelser (GDPR artikkel 6(1)(c));\n"
            "- Nevumos legitime interesser i å drifte og forbedre plattformen (GDPR artikkel 6(1)(f)).\n\n"
            "16.3 Leverandører som opptrer som næringsdrivende og bruker plattformen til å samle inn og behandle kunders personopplysninger, opptrer som uavhengige behandlingsansvarlige for disse dataene. Nevumo er ikke felles behandlingsansvarlig for slik behandling."
        ),
        "fi": (
            "16.1 Nevumo käsittelee palveluntarjoajien henkilötietoja rekisterinpitäjänä tietosuojakäytännön mukaisesti, joka on saatavilla osoitteessa nevumo.com/privacy.\n\n"
            "16.2 Nevumon suorittama palveluntarjoajien henkilötietojen käsittely perustuu:\n"
            "- näiden palveluntarjoajien ehtojen perustaman sopimussuhteen täyttämiseen (GDPR:n 6 artiklan 1 kohdan b alakohta);\n"
            "- lakisääteisten velvoitteiden noudattamiseen (GDPR:n 6 artiklan 1 kohdan c alakohta);\n"
            "- Nevumon oikeutettuihin etuihin alustan ylläpitämisessä ja parantamisessa (GDPR:n 6 artiklan 1 kohdan f alakohta).\n\n"
            "16.3 Palveluntarjoajat, jotka toimivat elinkeinonharjoittajina ja käyttävät alustaa asiakkaiden henkilötietojen keräämiseen ja käsittelyyn, toimivat näiden tietojen osalta itsenäisinä rekisterinpitäjinä. Nevumo ei ole yhteisrekisterinpitäjä tällaisessa käsittelyssä."
        ),
        "et": (
            "16.1 Nevumo töötleb teenusepakkujate isikuandmeid vastutava töötlejana vastavalt privaatsuspoliitikale, mis on saadaval aadressil nevumo.com/privacy.\n\n"
            "16.2 Nevumo poolne teenusepakkujate isikuandmete töötlemine põhineb:\n"
            "- nende teenusepakkujate tingimustega loodud lepingulise suhte täitmisel (GDPR-i artikli 6 lõike 1 punkt b);\n"
            "- juriidiliste kohustuste täitmisel (GDPR-i artikli 6 lõike 1 punkt c);\n"
            "- Nevumo õigustatud huvidel platvormi käitamisel ja täiustamisel (GDPR-i artikli 6 lõike 1 punkt f).\n\n"
            "16.3 Teenusepakkujad, kes tegutsevad kauplejatena ja kasutavad platvormi klientide isikuandmete kogumiseks ja töötlemiseks, tegutsevad nende andmete suhtes sõltumatute vastutavate töötlejatena. Nevumo ei ole sellise töötlemise puhul kaasvastutav töötleja."
        ),
        "lt": (
            "16.1 „Nevumo“ tvarko paslaugų teikėjų asmens duomenis kaip duomenų valdytojas pagal privatumo politiką, kurią galima rasti adresu nevumo.com/privacy.\n\n"
            "16.2 „Nevumo“ paslaugų teikėjų asmens duomenų tvarkymas grindžiamas:\n"
            "- šių Paslaugų teikėjų sąlygų nustatytų sutartinių santykių vykdymu (BDAR 6 straipsnio 1 dalies b punktas);\n"
            "- teisinių įsipareigojimų laikymusi (BDAR 6 straipsnio 1 dalies c punktas);\n"
            "- „Nevumo“ teisėtais interesais valdyti ir tobulinti platformą (BDAR 6 straipsnio 1 dalies f punktas).\n\n"
            "16.3 Paslaugų teikėjai, veikiantys kaip prekybininkai ir naudojantys platformą klientų asmens duomenims rinkti ir tvarkyti, tų duomenų atžvilgiu veikia kaip nepriklausomi duomenų valdytojai. „Nevumo“ nėra bendras duomenų valdytojas tokiam tvarkymui."
        ),
        "lv": (
            "16.1 Nevumo apstrādā Pakalpojumu sniedzēju personas datus kā datu pārzinis saskaņā ar Konfidencialitātes politiku, kas pieejama vietnē nevumo.com/privacy.\n\n"
            "16.2 Nevumo veiktā Pakalpojumu sniedzēju personas datu apstrāde ir balstīta uz:\n"
            "- ar šiem Pakalpojumu sniedzēju noteikumiem izveidoto līgumattiecību izpildi (VDAR 6. panta 1. punkta b) apakšpunkts);\n"
            "- juridisko pienākumu izpildi (VDAR 6. panta 1. punkta c) apakšpunkts);\n"
            "- Nevumo leģitīmajām interesēm Platformas darbībā un uzlabošanā (VDAR 6. panta 1. punkta f) apakšpunkts).\n\n"
            "16.3 Pakalpojumu sniedzēji, kas darbojas kā tirgotāji un izmanto Platformu, lai apkopotu un apstrādātu Klientu personas datus, attiecībā uz šiem datiem darbojas kā neatkarīgi datu pārziņi. Nevumo nav kopīgs datu pārzinis šādai apstrādei."
        ),
        "hu": (
            "16.1 A Nevumo adatkezelőként kezeli a Szolgáltatók személyes adatait a nevumo.com/privacy címen elérhető Adatvédelmi irányelvnek megfelelően.\n\n"
            "16.2 A Nevumo általi Szolgáltatói személyes adatok kezelése a következőken alapul:\n"
            "- a jelen Szolgáltatói Feltételek által létrehozott szerződéses kapcsolat teljesítése (GDPR 6. cikk (1) bekezdés b) pont);\n"
            "- jogi kötelezettségek betartása (GDPR 6. cikk (1) bekezdés c) pont);\n"
            "- a Nevumo jogos érdekei a Platform működtetésében és fejlesztésében (GDPR 6. cikk (1) bekezdés f) pont).\n\n"
            "16.3 Azok a Szolgáltatók, akik kereskedőként járnak el, és a Platformot Ügyfelek személyes adatainak gyűjtésére és kezelésére használják, ezen adatok tekintetében független adatkezelőként járnak el. A Nevumo nem közös adatkezelő az ilyen adatkezelés tekintetében."
        ),
        "hr": (
            "16.1 Nevumo obrađuje osobne podatke Pružatelja usluga kao voditelj obrade podataka u skladu s Politikom privatnosti dostupnom na nevumo.com/privacy.\n\n"
            "16.2 Obrada osobnih podataka Pružatelja usluga od strane tvrtke Nevumo temelji se na:\n"
            "- izvršavanju ugovornog odnosa uspostavljenog ovim Uvjetima za pružatelje usluga (Članak 6(1)(b) GDPR-a);\n"
            "- poštivanju zakonskih obveza (Članak 6(1)(c) GDPR-a);\n"
            "- legitimnim interesima tvrtke Nevumo u radu i poboljšanju Platforme (Članak 6(1)(f) GDPR-a).\n\n"
            "16.3 Pružatelji usluga koji djeluju kao trgovci i koriste Platformu za prikupljanje i obradu osobnih podataka Klijenata djeluju kao neovisni voditelji obrade podataka u odnosu na te podatke. Nevumo nije zajednički voditelj obrade za takvu obradu."
        ),
        "sk": (
            "16.1 Spoločnosť Nevumo spracúva osobné údaje poskytovateľov ako prevádzkovateľ v súlade so Zásadami ochrany osobných údajov dostupnými na nevumo.com/privacy.\n\n"
            "16.2 Spracúvanie osobných údajov poskytovateľov spoločnosťou Nevumo je založené na:\n"
            "- plnení zmluvného vzťahu založeného týmito podmienkami pre poskytovateľov (čl. 6 ods. 1 písm. b) GDPR);\n"
            "- plnení zákonných povinností (čl. 6 ods. 1 písm. c) GDPR);\n"
            "- oprávnených záujmoch spoločnosti Nevumo na prevádzkovaní a zlepšovaní platformy (čl. 6 ods. 1 písm. f) GDPR).\n\n"
            "16.3 Poskytovatelia konajúci ako obchodníci a používajúci platformu na zhromažďovanie a spracúvanie osobných údajov klientov konajú ako nezávislí prevádzkovatelia vo vzťahu k týmto údajom. Spoločnosť Nevumo nie je spoločným prevádzkovateľom pre takéto spracúvanie."
        ),
        "sl": (
            "16.1 Nevumo obdeluje osebne podatke ponudnikov kot upravljavec podatkov v skladu s Pravilnikom o zasebnosti, ki je na voljo na nevumo.com/privacy.\n\n"
            "16.2 Obdelava osebnih podatkov ponudnikov s strani podjetja Nevumo temelji na:\n"
            "- izvajanju pogodbenega razmerja, vzpostavljenega s temi pogoji za ponudnike (člen 6(1)(b) GDPR);\n"
            "- izpolnjevanju zakonskih obveznosti (člen 6(1)(c) GDPR);\n"
            "- zakonitih interesih podjetja Nevumo pri upravljanju in izboljšanju platforme (člen 6(1)(f) GDPR).\n\n"
            "16.3 Ponudniki, ki delujejo kot trgovci in uporabljajo platformo za zbiranje in obdelavo osebnih podatkov strank, delujejo kot neodvisni upravljavci podatkov v zvezi s temi podatki. Nevumo ni skupni upravljavec za takšno obdelavo."
        ),
        "el": (
            "16.1 Η Nevumo επεξεργάζεται τα προσωπικά δεδομένα των Παρόχων ως υπεύθυνος επεξεργασίας δεδομένων σύμφωνα με την Πολιτική Απορρήτου που διατίθεται στο nevumo.com/privacy.\n\n"
            "16.2 Η επεξεργασία των προσωπικών δεδομένων των Παρόχων από τη Nevumo βασίζεται σε:\n"
            "- την εκτέλεση της συμβατικής σχέσης που καθορίζεται από αυτούς τους Όρους Παρόχου (Άρθρο 6(1)(β) του ΓΚΠΔ).\n"
            "- τη συμμόρφωση με νομικές υποχρεώσεις (Άρθρο 6(1)(γ) του ΓΚΠΔ).\n"
            "- τα έννομα συμφέροντα της Nevumo για τη λειτουργία και τη βελτίωση της Πλατφόρμας (Άρθρο 6(1)(στ) του ΓΚΠΔ).\n\n"
            "16.3 Οι Πάροχοι που ενεργούν ως έμποροι και χρησιμοποιούν την Πλατφόρμα για τη συλλογή και επεξεργασία προσωπικών δεδομένων Πελατών ενεργούν ως ανεξάρτητοι υπεύθυνοι επεξεργασίας δεδομένων σε σχέση με αυτά τα δεδομένα. Η Nevumo δεν είναι από κοινού υπεύθυνος επεξεργασίας για τέτοια επεξεργασία."
        ),
        "tr": (
            "16.1 Nevumo, Sağlayıcıların kişisel verilerini nevumo.com/privacy adresinde bulunan Gizlilik Politikasına uygun olarak veri sorumlusu sıfatıyla işler.\n\n"
            "16.2 Nevumo'nun Sağlayıcı kişisel verilerini işlemesi şunlara dayanmaktadır:\n"
            "- bu Sağlayıcı Şartları tarafından kurulan sözleşme ilişkisinin ifası (GDPR Madde 6(1)(b));\n"
            "- yasal yükümlülüklere uyum (GDPR Madde 6(1)(c));\n"
            "- Nevumo'nun Platformu işletme ve iyileştirme konusundaki meşru menfaatleri (GDPR Madde 6(1)(f)).\n\n"
            "16.3 Tüccar olarak hareket eden ve Müşteri kişisel verilerini toplamak ve işlemek için Platformu kullanan Sağlayıcılar, bu verilerle ilgili olarak bağımsız veri sorumluları olarak hareket ederler. Nevumo, bu tür işlemler için ortak veri sorumlusu değildir."
        ),
        "ga": (
            "16.1 Próiseálann Nevumo sonraí pearsanta Soláthraithe mar rialaitheoir sonraí de réir an Bheartais Príobháideachais atá ar fáil ag nevumo.com/privacy.\n\n"
            "16.2 Tá próiseáil Nevumo ar shonraí pearsanta Soláthraithe bunaithe ar:\n"
            "- comhlíonadh an chaidrimh chonarthaigh a bhunaítear leis na Téarmaí Soláthraí seo (Airteagal 6(1)(b) den GDPR);\n"
            "- comhlíonadh oibleagáidí dlíthiúla (Airteagal 6(1)(c) den GDPR);\n"
            "- leasanna dlisteanacha Nevumo maidir leis an Ardán a oibriú agus a fheabhsú (Airteagal 6(1)(f) den GDPR).\n\n"
            "16.3 Gníomhaíonn Soláthraithe atá ag gníomhú mar thrádálaithe agus a úsáideann an tArdán chun sonraí pearsanta Cliaint a bhailiú agus a phróiseáil mar rialaitheoirí sonraí neamhspleácha i leith na sonraí sin. Níl Nevumo ina chomhrialaitheoir don phróiseáil sin."
        ),
        "is": (
            "16.1 Nevumo vinnur persónuupplýsingar þjónustuveitenda sem ábyrgðaraðili í samræmi við persónuverndarstefnuna sem er aðgengileg á nevumo.com/privacy.\n\n"
            "16.2 Vinnsla Nevumo á persónuupplýsingum þjónustuveitenda byggir á:\n"
            "- framkvæmd samningssambandsins sem stofnað er til með þessum skilmálum fyrir þjónustuveitendur (GDPR 6. grein (1)(b));\n"
            "- að fylgja lagalegum skyldum (GDPR 6. grein (1)(c));\n"
            "- lögmætum hagsmunum Nevumo af því að reka og bæta vettvanginn (GDPR 6. grein (1)(f)).\n\n"
            "16.3 Þjónustuveitendur sem starfa sem kaupmenn og nota vettvanginn til að safna og vinna úr persónuupplýsingum viðskiptavina starfa sem sjálfstæðir ábyrgðaraðilar varðandi þau gögn. Nevumo er ekki sameiginlegur ábyrgðaraðili að slíkri vinnslu."
        ),
        "lb": (
            "16.1 Nevumo veraarbecht perséinlech Daten vun Ubidder als Datekontroller am Aklang mat der Dateschutzrichtlinn verfügbar op nevumo.com/privacy.\n\n"
            "16.2 D'Veraarbechtung vu perséinlechen Date vun Ubidder duerch Nevumo baséiert op:\n"
            "- der Erfëllung vun der vertraglecher Relatioun, déi duerch dës Ubidderbedéngungen etabléiert gouf (Artikel 6(1)(b) GDPR);\n"
            "- der Konformitéit mat gesetzleche Verpflichtungen (Artikel 6(1)(c) GDPR);\n"
            "- de legitimen Interesse vum Nevumo beim Betrib a Verbesserung vun der Plattform (Artikel 6(1)(f) GDPR).\n\n"
            "16.3 Ubidder, déi als Händler optrieden an d'Plattform benotzen fir perséinlech Date vu Clienten ze sammelen an ze veraarbechten, handelen als onofhängeg Datekontroller a Bezuch op dës Daten. Nevumo ass kee gemeinsame Kontroller fir sou eng Veraarbechtung."
        ),
        "mk": (
            "16.1 Nevumo ги обработува личните податоци на Давателите како контролор на податоци во согласност со Политиката за приватност достапна на nevumo.com/privacy.\n\n"
            "16.2 Обработката на личните податоци на Давателите од страна на Nevumo се заснова на:\n"
            "- извршување на договорниот однос воспоставен со овие Услови за Даватели (Член 6(1)(б) од ГДПР);\n"
            "- усогласеност со законските обврски (Член 6(1)(в) од ГДПР);\n"
            "- легитимните интереси на Nevumo за управување и подобрување на Платформата (Член 6(1)(ѓ) од ГДПР).\n\n"
            "16.3 Давателите кои дејствуваат како трговци и ја користат Платформата за собирање и обработка на лични податоци на Клиентите дејствуваат како независни контролори на податоци во однос на тие податоци. Nevumo не е заеднички контролор за таквата обработка."
        ),
        "mt": (
            "16.1 Nevumo jipproċessa dejta personali tal-Fornitur bħala kontrollur tad-dejta skont il-Politika tal-Privatezza disponibbli fuq nevumo.com/privacy.\n\n"
            "16.2 L-ipproċessar minn Nevumo tad-dejta personali tal-Fornitur huwa bbażat fuq:\n"
            "- it-twettiq tar-relazzjoni kuntrattwali stabbilita minn dawn it-Termini għall-Fornituri (Artikolu 6(1)(b) tal-GDPR);\n"
            "- il-konformità mal-obbligi legali (Artikolu 6(1)(c) tal-GDPR);\n"
            "- l-interessi leġittimi ta' Nevumo fit-tħaddim u t-titjib tal-Pjattaforma (Artikolu 6(1)(f) tal-GDPR).\n\n"
            "16.3 Fornituri li jaġixxu bħala negozjanti u li jużaw il-Pjattaforma biex jiġbru u jipproċessaw dejta personali tal-Klijent jaġixxu bħala kontrolluri tad-dejta indipendenti fir-rigward ta' dik id-dejta. Nevumo mhuwiex kontrollur konġunt għal tali pproċessar."
        ),
        "sq": (
            "16.1 Nevumo përpunon të dhënat personale të Ofruesve si një kontrollues të dhënash në përputhje me Politikën e Privatësisë të disponueshme në nevumo.com/privacy.\n\n"
            "16.2 Përpunimi i të dhënave personale të Ofruesve nga Nevumo bazohet në:\n"
            "- performancën e marrëdhënies kontraktuale të krijuar nga këto Kushte për Ofruesit (Neni 6(1)(b) i GDPR);\n"
            "- pajtueshmërinë me detyrimet ligjore (Neni 6(1)(c) i GDPR);\n"
            "- interesat legjitime të Nevumo në operimin dhe përmirësimin e Platformës (Neni 6(1)(f) i GDPR).\n\n"
            "16.3 Ofruesit që veprojnë si tregtarë dhe përdorin Platformën për të mbledhur dhe përpunuar të dhëna personale të Klientëve veprojnë si kontrollues të pavarur të dhënash në lidhje me ato të dhëna. Nevumo nuk është një kontrollues i përbashkët për një përpunim të tillë."
        ),
        "sr": (
            "16.1 Nevumo obrađuje lične podatke Pružaoca usluga kao kontrolor podataka u skladu sa Politikom privatnosti dostupnom na nevumo.com/privacy.\n\n"
            "16.2 Obrada ličnih podataka Pružaoca usluga od strane kompanije Nevumo zasniva se na:\n"
            "- izvršenju ugovornog odnosa uspostavljenog ovim Uslovima za pružaoce usluga (Član 6(1)(b) GDPR-a);\n"
            "- poštovanju zakonskih obaveza (Član 6(1)(c) GDPR-a);\n"
            "- legitimnim interesima kompanije Nevumo u radu i poboljšanju Platforme (Član 6(1)(f) GDPR-a).\n\n"
            "16.3 Pružaoci usluga koji deluju kao trgovci i koriste Platformu za prikupljanje i obradu ličnih podataka Klijenata deluju kao nezavisni kontrolori podataka u odnosu na te podatke. Nevumo nije zajednički kontrolor za takvu obradu."
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
        print(f"✅ Seeded {count} translations for {NAMESPACE}.art15_body and {NAMESPACE}.art16_body")

if __name__ == "__main__":
    seed()
