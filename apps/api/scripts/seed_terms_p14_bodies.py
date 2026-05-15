"""
seed_terms_p14_bodies.py  —  Nevumo | namespace: terms
Key: art14_body (34 езика)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_terms_p14_bodies
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
    "art14_body": {
        "en": (
            '14.1 Nevumo may amend these Terms at any time. We will notify registered '
            'clients by email at least 30 days before any change takes effect.\n\n'
            '14.2 If you do not accept the amended Terms, you may close your account '
            'before the effective date. Continued use of the platform after the '
            'effective date constitutes acceptance of the amended Terms.\n\n'
            '14.3 [PL] For Polish consumers, amendments to these Terms are governed by '
            'Article 384 of the Polish Civil Code. The 30-day notice period applies.'
        ),
        "pl": (
            '14.1 Nevumo zastrzega sobie prawo do zmiany niniejszego Regulaminu. '
            'Zarejestrowani Klienci zostaną powiadomieni o każdej zmianie pocztą '
            'elektroniczną co najmniej 30 dni przed jej wejściem w życie.\n\n'
            '14.2 Jeżeli Klient nie akceptuje zmienionego Regulaminu, może usunąć '
            'swoje konto przed datą wejścia zmian w życie. Dalsze korzystanie z '
            'serwisu po tej dacie jest równoznaczne z akceptacją zmienionego '
            'Regulaminu.\n\n'
            '14.3 Zmiany Regulaminu dokonywane są zgodnie z art. 384 Kodeksu '
            'cywilnego. Termin wypowiedzenia wynosi 30 dni.'
        ),
        "bg": (
            '14.1 Nevumo може да изменя настоящите ОУ по всяко време. '
            'Регистрираните Клиенти ще бъдат уведомявани по имейл най-малко '
            '30 дни преди влизане в сила на изменението.\n\n'
            '14.2 Ако Клиентът не приема изменените ОУ, може да закрие акаунта '
            'си преди датата на влизане в сила. Продължаването на използването '
            'на платформата след тази дата означава приемане на изменените ОУ.\n\n'
            '14.3 [PL] За полски потребители измененията се уреждат от чл. 384 '
            'от Полския граждански кодекс. Срокът на предизвестие е 30 дни.'
        ),
        "cs": (
            '14.1 Nevumo může tyto podmínky kdykoli změnit. Registrovaní klienti '
            'budou informováni e-mailem nejméně 30 dní před vstupem změny v platnost.\n\n'
            '14.2 Pokud změněné podmínky nepřijmete, můžete svůj účet před datem '
            'účinnosti smazat. Další používání platformy po datu účinnosti znamená '
            'přijetí změněných podmínek.\n\n'
            '14.3 [PL] Pro polské spotřebitele se změny řídí článkem 384 '
            'polského občanského zákoníku. Platí 30denní výpovědní lhůta.'
        ),
        "da": (
            '14.1 Nevumo kan til enhver tid ændre disse vilkår. Registrerede klienter '
            'vil blive underrettet pr. e-mail mindst 30 dage før en ændring træder i kraft.\n\n'
            '14.2 Hvis du ikke accepterer de ændrede vilkår, kan du lukke din konto '
            'før ikrafttrædelsesdatoen. Fortsat brug efter ikrafttrædelsesdatoen '
            'udgør accept af de ændrede vilkår.\n\n'
            '14.3 [PL] For polske forbrugere reguleres ændringer af artikel 384 '
            'i den polske civillov. 30-dages varsel gælder.'
        ),
        "de": (
            '14.1 Nevumo kann diese Bedingungen jederzeit ändern. Registrierte '
            'Kunden werden per E-Mail mindestens 30 Tage vor Inkrafttreten einer '
            'Änderung benachrichtigt.\n\n'
            '14.2 Wenn Sie die geänderten Bedingungen nicht akzeptieren, können Sie '
            'Ihr Konto vor dem Inkrafttreten schließen. Die weitere Nutzung der '
            'Plattform nach diesem Datum gilt als Zustimmung zu den geänderten '
            'Bedingungen.\n\n'
            '14.3 [PL] Für polnische Verbraucher richten sich Änderungen nach '
            'Artikel 384 des polnischen Zivilgesetzbuchs. Die 30-Tage-Frist gilt.'
        ),
        "el": (
            '14.1 Το Nevumo μπορεί να τροποποιεί τους παρόντες Όρους ανά πάσα '
            'στιγμή. Οι εγγεγραμμένοι πελάτες θα ειδοποιούνται μέσω email '
            'τουλάχιστον 30 ημέρες πριν από κάθε αλλαγή.\n\n'
            '14.2 Εάν δεν αποδέχεστε τους τροποποιημένους Όρους, μπορείτε να '
            'κλείσετε τον λογαριασμό σας πριν από την ημερομηνία έναρξης ισχύος. '
            'Η συνέχιση χρήσης αποτελεί αποδοχή των τροποποιημένων Όρων.\n\n'
            '14.3 [PL] Για Πολωνούς καταναλωτές, οι τροποποιήσεις διέπονται '
            'από το άρθρο 384 του Πολωνικού Αστικού Κώδικα. Ισχύει '
            'προθεσμία 30 ημερών.'
        ),
        "es": (
            '14.1 Nevumo puede modificar estos Términos en cualquier momento. '
            'Los clientes registrados serán notificados por correo electrónico '
            'al menos 30 días antes de que cualquier cambio entre en vigor.\n\n'
            '14.2 Si no acepta los Términos modificados, puede cerrar su cuenta '
            'antes de la fecha de entrada en vigor. El uso continuado de la '
            'plataforma después de esa fecha constituye aceptación.\n\n'
            '14.3 [PL] Para los consumidores polacos, las modificaciones se '
            'rigen por el artículo 384 del Código Civil polaco. '
            'Se aplica un preaviso de 30 días.'
        ),
        "et": (
            '14.1 Nevumo võib neid tingimusi igal ajal muuta. Registreeritud kliente '
            'teavitatakse e-posti teel vähemalt 30 päeva enne muudatuse jõustumist.\n\n'
            '14.2 Kui te muudetud tingimustega ei nõustu, saate konto enne '
            'jõustumiskuupäeva sulgeda. Platvormi edasine kasutamine pärast seda '
            'kuupäeva tähendab muudetud tingimuste aktsepteerimist.\n\n'
            '14.3 [PL] Poola tarbijate puhul reguleeritakse muudatusi Poola '
            'tsiviilseadustiku artikliga 384. Kehtib 30-päevane etteteatamisaeg.'
        ),
        "fi": (
            '14.1 Nevumo voi muuttaa näitä ehtoja milloin tahansa. Rekisteröityneille '
            'asiakkaille ilmoitetaan sähköpostitse vähintään 30 päivää ennen '
            'muutoksen voimaantuloa.\n\n'
            '14.2 Jos et hyväksy muutettuja ehtoja, voit sulkea tilisi ennen '
            'voimaantulopäivää. Alustan jatkokäyttö voimaantulopäivän jälkeen '
            'merkitsee muutettujen ehtojen hyväksymistä.\n\n'
            '14.3 [PL] Puolalaisten kuluttajien osalta muutoksia säätelee '
            'Puolan siviililain 384 artikla. 30 päivän ilmoitusaika pätee.'
        ),
        "fr": (
            '14.1 Nevumo peut modifier les présentes Conditions à tout moment. '
            'Les clients inscrits seront informés par e-mail au moins 30 jours '
            'avant l\'entrée en vigueur de toute modification.\n\n'
            '14.2 Si vous n\'acceptez pas les Conditions modifiées, vous pouvez '
            'fermer votre compte avant la date d\'entrée en vigueur. L\'utilisation '
            'continue de la plateforme après cette date vaut acceptation.\n\n'
            '14.3 [PL] Pour les consommateurs polonais, les modifications sont '
            'régies par l\'article 384 du Code civil polonais. '
            'Le délai de préavis de 30 jours s\'applique.'
        ),
        "ga": (
            '14.1 Féadfaidh Nevumo na Téarmaí seo a leasú ag am ar bith. '
            'Cuirfear cliaint chláraithe ar an eolas trí ríomhphost ar a laghad '
            '30 lá roimh aon athrú a theacht i bhfeidhm.\n\n'
            '14.2 Mura nglacann tú leis na Téarmaí leasaithe, féadfaidh tú do '
            'chuntas a dhúnadh roimh an dáta éifeachtach. Ciallaíonn leanúint '
            'ag úsáid na hardáin tar éis an dáta sin glacadh leis na Téarmaí '
            'leasaithe.\n\n'
            '14.3 [PL] Do thomhaltóirí Polannach, rialaítear leasuithe ag Airteagal '
            '384 den Chód Sibhialta Polannach. Tá an tréimhse fógra 30 lá i bhfeidhm.'
        ),
        "hr": (
            '14.1 Nevumo može u svakom trenutku izmijeniti ove Uvjete. Registrirani '
            'klijenti bit će obaviješteni e-poštom najmanje 30 dana prije stupanja '
            'na snagu bilo koje promjene.\n\n'
            '14.2 Ako ne prihvaćate izmijenjene Uvjete, možete zatvoriti račun '
            'prije datuma stupanja na snagu. Nastavak korištenja platforme nakon '
            'tog datuma znači prihvaćanje izmijenjenih Uvjeta.\n\n'
            '14.3 [PL] Za poljske potrošače izmjene se uređuju člankom 384 '
            'Poljskog građanskog zakonika. Primjenjuje se otkazni rok od 30 dana.'
        ),
        "hu": (
            '14.1 A Nevumo bármikor módosíthatja jelen feltételeket. A regisztrált '
            'ügyfeleket e-mailben értesítjük minden módosítás hatályba lépése '
            'előtt legalább 30 nappal.\n\n'
            '14.2 Ha nem fogadja el a módosított feltételeket, a hatályba lépés '
            'előtt lezárhatja fiókját. A hatályba lépés utáni folyamatos használat '
            'a módosított feltételek elfogadásának minősül.\n\n'
            '14.3 [PL] Lengyel fogyasztók esetén a módosításokat a lengyel Polgári '
            'Törvénykönyv 384. cikke szabályozza. A 30 napos felmondási idő érvényes.'
        ),
        "is": (
            '14.1 Nevumo getur breytt þessum skilmálum hvenær sem er. Skráðir '
            'viðskiptavinir fá tilkynningu í tölvupósti að minnsta kosti 30 dögum '
            'áður en breyting tekur gildi.\n\n'
            '14.2 Ef þú samþykkir ekki breytta skilmála, getur þú lokað reikningi '
            'þínum áður en gildistökudagurinn rennur upp. Áframhaldandi notkun '
            'eftir gildistökudag telst samþykki á breyttum skilmálum.\n\n'
            '14.3 [PL] Fyrir pólska neytendur eru breytingar stjórnaðar af '
            'grein 384 í pólska lögum um samninga. 30 daga uppsagnarfrestur gildir.'
        ),
        "it": (
            '14.1 Nevumo può modificare i presenti Termini in qualsiasi momento. '
            'I clienti registrati saranno avvisati via e-mail almeno 30 giorni '
            'prima che qualsiasi modifica entri in vigore.\n\n'
            '14.2 Se non accetti i Termini modificati, puoi chiudere il tuo account '
            'prima della data di entrata in vigore. Il continuo utilizzo della '
            'piattaforma dopo tale data costituisce accettazione dei Termini '
            'modificati.\n\n'
            '14.3 [PL] Per i consumatori polacchi, le modifiche sono disciplinate '
            'dall\'articolo 384 del Codice civile polacco. '
            'Si applica il preavviso di 30 giorni.'
        ),
        "lb": (
            '14.1 Nevumo kann dës Bedéngungen zu all Zäit änneren. Registréiert '
            'Klienten ginn per E-Mail mindestens 30 Deeg virum Inkrafttrieden '
            'vun enger Ännerung informéiert.\n\n'
            '14.2 Wann Dir d\'geännert Bedéngungen net akzeptéiert, kënnt Dir '
            'Äre Kont virum Gëltegkeetsdatum zoumaachen. D\'weiderhi Benotze '
            'vun der Plattform no deem Datum gëlt als Akzeptanz.\n\n'
            '14.3 [PL] Fir polnesch Konsumenten ginn Ännerungen duerch Artikel 384 '
            'vum polneschen Zivilgesetzbuch geregelt. D\'30-Deeg-Frist gëlt.'
        ),
        "lt": (
            '14.1 Nevumo gali bet kada keisti šias sąlygas. Registruoti klientai '
            'bus informuoti el. paštu ne vėliau kaip likus 30 dienų iki bet kokio '
            'pakeitimo įsigaliojimo.\n\n'
            '14.2 Jei nepritariate pakeistoms sąlygoms, galite uždaryti paskyrą '
            'iki įsigaliojimo datos. Tolimesnis platformos naudojimas po tos datos '
            'reiškia pakeistų sąlygų priėmimą.\n\n'
            '14.3 [PL] Lenkijos vartotojams pakeitimai reglamentuojami Lenkijos '
            'Civilinio kodekso 384 straipsniu. Taikomas 30 dienų pranešimo terminas.'
        ),
        "lv": (
            '14.1 Nevumo var jebkurā laikā grozīt šos noteikumus. Reģistrētie '
            'klienti tiks informēti pa e-pastu vismaz 30 dienas pirms jebkādu '
            'izmaiņu stāšanās spēkā.\n\n'
            '14.2 Ja nepiekrītat grozītajiem noteikumiem, varat slēgt kontu pirms '
            'spēkā stāšanās datuma. Turpinot izmantot platformu pēc šī datuma, '
            'tiek uzskatīts, ka esat piekrituši grozītajiem noteikumiem.\n\n'
            '14.3 [PL] Polijas patērētājiem izmaiņas regulē Polijas Civilkodeksa '
            '384. pants. Tiek piemērots 30 dienu paziņošanas termiņš.'
        ),
        "mk": (
            '14.1 Nevumo може во секое време да ги измени овие Услови. '
            'Регистрираните Клиенти ќе бидат известени по е-пошта '
            'најмалку 30 дена пред влегување во сила на секоја промена.\n\n'
            '14.2 Ако не ги прифаќате изменетите Услови, можете да го '
            'затворите акаунтот пред датумот на стапување во сила. '
            'Продолженото користење на платформата после тој датум '
            'значи прифаќање на изменетите Услови.\n\n'
            '14.3 [PL] За полски потрошувачи, измените се уредени со '
            'член 384 од Полскиот граѓански законик. '
            'Рокот на известување од 30 дена се применува.'
        ),
        "mt": (
            '14.1 Nevumo jista\' jemenda dawn it-Termini fi kwalunkwe ħin. '
            'Il-klijenti rreġistrati jiġu avżati bl-e-mail minn tal-inqas 30 jum '
            'qabel ma kwalunkwe bidla tidħol fis-seħħ.\n\n'
            '14.2 Jekk ma taqbilx mat-Termini emendati, tista\' tagħlaq il-kont '
            'tiegħek qabel id-data effettiva. L-użu kontinwat tal-pjattaforma '
            'wara dik id-data jikkostitwixxi aċċettazzjoni.\n\n'
            '14.3 [PL] Għall-konsumaturi Pollakki, l-emendi huma rregolati '
            'mill-Artikolu 384 tal-Kodiċi Ċivili Pollakk. '
            'Il-perjodu ta\' avviż ta\' 30 jum japplika.'
        ),
        "nl": (
            '14.1 Nevumo kan deze Voorwaarden te allen tijde wijzigen. '
            'Geregistreerde klanten worden per e-mail op de hoogte gesteld '
            'minimaal 30 dagen voordat een wijziging van kracht wordt.\n\n'
            '14.2 Als u de gewijzigde Voorwaarden niet accepteert, kunt u uw '
            'account sluiten vóór de ingangsdatum. Voortgezet gebruik van het '
            'platform na die datum geldt als aanvaarding.\n\n'
            '14.3 [PL] Voor Poolse consumenten worden wijzigingen geregeld door '
            'artikel 384 van het Pools Burgerlijk Wetboek. '
            'De opzegtermijn van 30 dagen is van toepassing.'
        ),
        "no": (
            '14.1 Nevumo kan endre disse Vilkårene når som helst. Registrerte '
            'klienter vil bli varslet via e-post minst 30 dager før en endring '
            'trer i kraft.\n\n'
            '14.2 Hvis du ikke godtar de endrede Vilkårene, kan du lukke kontoen '
            'din før ikrafttredelsdatoen. Fortsatt bruk etter den datoen utgjør '
            'aksept av de endrede Vilkårene.\n\n'
            '14.3 [PL] For polske forbrugere reguleres endringer av artikkel 384 '
            'i den polske sivilloven. 30-dagers varsel gjelder.'
        ),
        "pt": (
            '14.1 O Nevumo pode alterar estes Termos a qualquer momento. '
            'Os clientes registrados serão notificados por e-mail com pelo menos '
            '30 dias de antecedência antes de qualquer alteração entrar em vigor.\n\n'
            '14.2 Se não aceitar os Termos alterados, pode encerrar a sua conta '
            'antes da data de entrada em vigor. O uso continuado da plataforma '
            'após essa data constitui aceitação.\n\n'
            '14.3 [PL] Para os consumidores polacos, as alterações são regidas '
            'pelo artigo 384 do Código Civil polaco. '
            'Aplica-se o prazo de aviso de 30 dias.'
        ),
        "pt-PT": (
            '14.1 O Nevumo pode alterar estes Termos a qualquer momento. '
            'Os clientes registados serão notificados por e-mail com pelo menos '
            '30 dias de antecedência antes de qualquer alteração entrar em vigor.\n\n'
            '14.2 Se não aceitar os Termos alterados, pode encerrar a sua conta '
            'antes da data de entrada em vigor. A utilização continuada da '
            'plataforma após essa data constitui aceitação.\n\n'
            '14.3 [PL] Para os consumidores polacos, as alterações são regidas '
            'pelo artigo 384 do Código Civil polaco. '
            'Aplica-se o prazo de aviso de 30 dias.'
        ),
        "ro": (
            '14.1 Nevumo poate modifica acești Termeni în orice moment. '
            'Clienții înregistrați vor fi notificați prin e-mail cu cel puțin '
            '30 de zile înainte ca orice modificare să intre în vigoare.\n\n'
            '14.2 Dacă nu acceptați Termenii modificați, puteți închide contul '
            'înainte de data intrării în vigoare. Utilizarea continuă a '
            'platformei după acea dată constituie acceptare.\n\n'
            '14.3 [PL] Pentru consumatorii polonezi, modificările sunt reglementate '
            'de Articolul 384 din Codul Civil polonez. '
            'Se aplică termenul de preaviz de 30 de zile.'
        ),
        "ru": (
            '14.1 Nevumo может изменять настоящие условия в любое время. '
            'Зарегистрированные клиенты будут уведомлены по электронной почте '
            'не менее чем за 30 дней до вступления изменений в силу.\n\n'
            '14.2 Если вы не принимаете изменённые условия, вы можете закрыть '
            'аккаунт до даты вступления в силу. Продолжение использования '
            'платформы после этой даты означает принятие изменённых условий.\n\n'
            '14.3 [PL] Для польских потребителей изменения регулируются '
            'статьёй 384 Гражданского кодекса Польши. '
            'Применяется 30-дневный срок уведомления.'
        ),
        "sk": (
            '14.1 Nevumo môže tieto podmienky kedykoľvek zmeniť. Registrovaní '
            'klienti budú informovaní e-mailom najmenej 30 dní pred nadobudnutím '
            'účinnosti akejkoľvek zmeny.\n\n'
            '14.2 Ak zmenené podmienky neprijmete, môžete svoj účet pred dátumom '
            'účinnosti zrušiť. Ďalšie používanie platformy po tomto dátume '
            'znamená akceptáciu zmenených podmienok.\n\n'
            '14.3 [PL] Pre poľských spotrebiteľov sa zmeny riadia článkom 384 '
            'poľského Občianskeho zákonníka. Platí 30-dňová výpovedná lehota.'
        ),
        "sl": (
            '14.1 Nevumo lahko te pogoje kadar koli spremeni. Registrirani stranki '
            'bodo obveščene po e-pošti vsaj 30 dni pred uveljavitvijo katere koli '
            'spremembe.\n\n'
            '14.2 Če ne sprejmete spremenjenih pogojev, lahko zaprete račun pred '
            'datumom uveljavitve. Nadaljnja uporaba platforme po tem datumu pomeni '
            'sprejetje spremenjenih pogojev.\n\n'
            '14.3 [PL] Za poljske potrošnike se spremembe urejajo s 384. členom '
            'Poljskega civilnega zakonika. Velja 30-dnevni odpovedni rok.'
        ),
        "sq": (
            '14.1 Nevumo mund të ndryshojë këto Terma në çdo kohë. Klientët e '
            'regjistruar do të njoftohen me email të paktën 30 ditë para se '
            'çdo ndryshim të hyjë në fuqi.\n\n'
            '14.2 Nëse nuk pranoni Termat e ndryshuar, mund të mbyllni llogarinë '
            'tuaj para datës efektive. Vazhdimi i përdorimit të platformës pas '
            'asaj date përbën pranim.\n\n'
            '14.3 [PL] Për konsumatorët polakë, ndryshimet rregullohen nga '
            'neni 384 i Kodit Civil polak. Aplikohet periudha e njoftimit prej 30 ditësh.'
        ),
        "sr": (
            '14.1 Nevumo može u svakom trenutku izmeniti ove Uslove. '
            'Registrovani klijenti biće obavešteni e-poštom najmanje 30 dana '
            'pre stupanja na snagu bilo koje izmene.\n\n'
            '14.2 Ako ne prihvatate izmenjene Uslove, možete zatvoriti nalog '
            'pre datuma stupanja na snagu. Nastavak korišćenja platforme posle '
            'tog datuma znači prihvatanje izmenjenih Uslova.\n\n'
            '14.3 [PL] Za poljske potrošače izmene se uređuju članom 384 '
            'Poljskog građanskog zakonika. Primenjuje se otkazni rok od 30 dana.'
        ),
        "sv": (
            '14.1 Nevumo kan när som helst ändra dessa Villkor. Registrerade '
            'kunder meddelas via e-post minst 30 dagar innan en ändring träder '
            'i kraft.\n\n'
            '14.2 Om du inte accepterar de ändrade Villkoren kan du stänga ditt '
            'konto innan ikraftträdandedatumet. Fortsatt användning av plattformen '
            'efter det datumet utgör godkännande.\n\n'
            '14.3 [PL] För polska konsumenter regleras ändringar av artikel 384 '
            'i den polska civillagen. 30-dagars uppsägningstid gäller.'
        ),
        "tr": (
            '14.1 Nevumo bu Koşulları istediği zaman değiştirebilir. Kayıtlı '
            'müşteriler, herhangi bir değişiklik yürürlüğe girmeden en az 30 gün '
            'önce e-posta yoluyla bilgilendirilecektir.\n\n'
            '14.2 Değiştirilen Koşulları kabul etmiyorsanız, yürürlük tarihinden '
            'önce hesabınızı kapatabilirsiniz. Bu tarihten sonra platformu '
            'kullanmaya devam etmek kabul anlamına gelir.\n\n'
            '14.3 [PL] Polonyalı tüketiciler için değişiklikler, Polonya Medeni '
            'Kanunu\'nun 384. maddesiyle düzenlenir. 30 günlük bildirim süresi uygulanır.'
        ),
        "uk": (
            '14.1 Nevumo може в будь-який час вносити зміни до цих Умов. '
            'Зареєстровані клієнти будуть повідомлені електронною поштою '
            'не менш ніж за 30 днів до набрання чинності будь-якої зміни.\n\n'
            '14.2 Якщо ви не приймаєте змінені Умови, ви можете закрити '
            'обліковий запис до дати набрання чинності. Продовження використання '
            'платформи після цієї дати означає прийняття змінених Умов.\n\n'
            '14.3 [PL] Для польських споживачів зміни регулюються статтею 384 '
            'Цивільного кодексу Польщі. Застосовується 30-денний строк повідомлення.'
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
        print(f"✅ seed_terms_p14_bodies: {count} rows upserted ({NAMESPACE}, art14_body × 34 langs)")

    engine.dispose()


if __name__ == "__main__":
    seed()
