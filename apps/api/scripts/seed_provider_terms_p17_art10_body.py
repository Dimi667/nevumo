"""
seed_provider_terms_p17_art10_body.py  —  Nevumo | namespace: provider_terms
Key: art10_body  (1 key x 34 langs = 34 rows)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_provider_terms_p17_art10_body
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
    "art10_body": {
        "en": (
            "10.1 Nevumo may amend these Provider Terms at any time. Any amendments will be communicated to you at least 15 days before they take effect, via:\n"
            "- email to your registered address;\n"
            "- a prominent notice in your Provider dashboard.\n\n"
            "10.2 If you do not accept the amended Terms, you may terminate your account before the effective date of the amendment. Continued use of the Platform after the effective date constitutes acceptance of the amended Terms.\n\n"
            "10.3 The 15-day notice period may be shortened where Nevumo is required to amend the Terms by law or regulation. In such cases, Nevumo will notify you as soon as reasonably practicable."
        ),
        "bg": (
            "1. Nevumo може по всяко време да внася изменения в настоящите Условия за Доставчици. За всякакви изменения Доставчикът ще бъде уведомен най-малко 15 дни преди влизането им в сила чрез:\n"
            "- имейл до регистрирания адрес;\n"
            "- ясно известие в доставчическия панел (табло за управление).\n\n"
            "2. Ако Доставчикът не приема изменените Условия, той може да прекрати своя акаунт преди датата на влизане в сила на измененията. Продължаването на ползването на Платформата след тази дата се счита за приемане на изменените Условия.\n\n"
            "3. Петнадесетдневният срок за предизвестие може да бъде съкратен, когато Nevumo е задължено да измени Условията въз основа на законодателна или регулаторна норма. В такива случаи Nevumo ще уведоми Доставчика при първа разумна възможност."
        ),
        "pl": (
            "1. Nevumo może w każdym czasie dokonywać zmian niniejszego Regulaminu Dostawców. O wszelkich zmianach Dostawca zostanie poinformowany co najmniej 15 dni przed ich wejściem w życie, za pośrednictwem:\n"
            "- wiadomości e-mail na zarejestrowany adres;\n"
            "- wyraźnego komunikatu w panelu Dostawcy (dashboardzie).\n\n"
            "2. Jeżeli Dostawca nie akceptuje zmienionego Regulaminu, może rozwiązać swoje konto przed datą wejścia w życie zmian. Kontynuowanie korzystania z Platformy po tej dacie jest równoznaczne z akceptacją zmienionego Regulaminu.\n\n"
            "3. Termin 15-dniowego powiadomienia może zostać skrócony w przypadku, gdy Nevumo jest zobowiązane do zmiany Regulaminu na podstawie przepisów prawa lub przepisów regulacyjnych. W takich przypadkach Nevumo powiadomi Dostawcę tak szybko, jak będzie to możliwe."
        ),
        "de": (
            "10.1 Nevumo kann diese Anbieterbedingungen jederzeit ändern. Alle Änderungen werden Ihnen mindestens 15 Tage vor ihrem Inkrafttreten mitgeteilt, und zwar über:\n"
            "- eine E-Mail an Ihre registrierte Adresse;\n"
            "- einen deutlich sichtbaren Hinweis in Ihrem Anbieter-Dashboard.\n\n"
            "10.2 Wenn Sie die geänderten Bedingungen nicht akzeptieren, können Sie Ihr Konto vor dem Datum des Inkrafttretens der Änderung kündigen. Die fortgesetzte Nutzung der Plattform nach dem Datum des Inkrafttretens gilt als Annahme der geänderten Bedingungen.\n\n"
            "10.3 Die 15-tägige Kündigungsfrist kann verkürzt werden, wenn Nevumo gesetzlich oder behördlich zur Änderung der Bedingungen verpflichtet ist. In solchen Fällen wird Nevumo Sie so schnell wie vernünftigerweise möglich benachrichtigen."
        ),
        "fr": (
            "10.1 Nevumo peut modifier les présentes Conditions pour les Fournisseurs à tout moment. Toute modification vous sera communiquée au moins 15 jours avant son entrée en vigueur, via :\n"
            "- un e-mail à votre adresse enregistrée ;\n"
            "- un avis bien en vue dans votre tableau de bord Fournisseur.\n\n"
            "10.2 Si vous n'acceptez pas les Conditions modifiées, vous pouvez résilier votre compte avant la date d'entrée en vigueur de la modification. L'utilisation continue de la Plateforme après la date d'entrée en vigueur constitue une acceptation des Conditions modifiées.\n\n"
            "10.3 Le délai de préavis de 15 jours peut être raccourci lorsque Nevumo est tenu de modifier les Conditions par la loi ou la réglementation. Dans de tels cas, Nevumo vous en informera dès que raisonnablement possible."
        ),
        "es": (
            "10.1 Nevumo puede modificar estas Condiciones para Proveedores en cualquier momento. Cualquier modificación se le comunicará al menos 15 días antes de que entre en vigor, a través de:\n"
            "- un correo electrónico a su dirección registrada;\n"
            "- un aviso destacado en su panel de control de Proveedor.\n\n"
            "10.2 Si no acepta las Condiciones modificadas, puede cancelar su cuenta antes de la fecha de entrada en vigor de la modificación. El uso continuado de la Plataforma después de la fecha de entrada en vigor constituye la aceptación de las Condiciones modificadas.\n\n"
            "10.3 El período de notificación de 15 días puede acortarse cuando Nevumo esté obligado a modificar las Condiciones por ley o regulación. En tales casos, Nevumo le notificará tan pronto como sea razonablemente posible."
        ),
        "it": (
            "10.1 Nevumo può modificare le presenti Condizioni per i Fornitori in qualsiasi momento. Eventuali modifiche ti saranno comunicate almeno 15 giorni prima della loro entrata in vigore, tramite:\n"
            "- e-mail al tuo indirizzo registrato;\n"
            "- un avviso in evidenza nella dashboard del Fornitore.\n\n"
            "10.2 Se non accetti le Condizioni modificate, puoi chiudere il tuo account prima della data di entrata in vigore della modifica. L'uso continuato della Piattaforma dopo la data di entrata in vigore costituisce accettazione delle Condizioni modificate.\n\n"
            "10.3 Il periodo di preavviso di 15 giorni può essere abbreviato qualora Nevumo sia tenuta a modificare le Condizioni per legge o regolamento. In tali casi, Nevumo ti avviserà non appena ragionevolmente possibile."
        ),
        "nl": (
            "10.1 Nevumo kan deze Voorwaarden voor Dienstverleners te allen tijde wijzigen. Eventuele wijzigingen worden uiterlijk 15 dagen voordat ze van kracht worden aan u meegedeeld, via:\n"
            "- een e-mail naar uw geregistreerde adres;\n"
            "- een opvallende kennisgeving in uw Dienstverlener-dashboard.\n\n"
            "10.2 Als u de gewijzigde Voorwaarden niet accepteert, kunt u uw account beëindigen voorafgaand aan de ingangsdatum van de wijziging. Voortgezet gebruik van het Platform na de ingangsdatum houdt acceptatie in van de gewijzigde Voorwaarden.\n\n"
            "10.3 De opzegtermijn van 15 dagen kan worden verkort indien Nevumo wettelijk of reglementair verplicht is de Voorwaarden te wijzigen. In dergelijke gevallen zal Nevumo u zo snel als redelijkerwijs mogelijk is op de hoogte stellen."
        ),
        "pt": (
            "10.1 A Nevumo pode alterar estes Termos para Prestadores a qualquer momento. Quaisquer alterações ser-lhe-ão comunicadas pelo menos 15 dias antes de entrarem em vigor, através de:\n"
            "- e-mail para o seu endereço registado;\n"
            "- um aviso de destaque no seu painel de Prestador.\n\n"
            "10.2 Se não aceitar os Termos alterados, poderá encerrar a sua conta antes da data de entrada em vigor da alteração. O uso continuado da Plataforma após a data de entrada em vigor constitui a aceitação dos Termos alterados.\n\n"
            "10.3 O período de aviso de 15 dias pode ser encurtado quando a Nevumo for obrigada a alterar os Termos por lei ou regulamento. Nesses casos, a Nevumo notificá-lo-á o mais rapidamente possível."
        ),
        "pt-PT": (
            "10.1 A Nevumo pode alterar estes Termos para Prestadores a qualquer momento. Quaisquer alterações ser-lhe-ão comunicadas pelo menos 15 dias antes de entrarem em vigor, através de:\n"
            "- e-mail para o seu endereço registado;\n"
            "- um aviso de destaque no seu painel de Prestador.\n\n"
            "10.2 Se não aceitar os Termos alterados, poderá encerrar a sua conta antes da data de entrada em vigor da alteração. O uso continuado da Plataforma após a data de entrada em vigor constitui a aceitação dos Termos alterados.\n\n"
            "10.3 O período de aviso de 15 dias pode ser encurtado quando a Nevumo for obrigada a alterar os Termos por lei ou regulamento. Nesses casos, a Nevumo notificá-lo-á o mais rapidamente possível."
        ),
        "ro": (
            "10.1 Nevumo poate modifica acești Termeni pentru Furnizori în orice moment. Orice modificare vă va fi comunicată cu cel puțin 15 zile înainte ca aceasta să intre în vigoare, prin intermediul:\n"
            "- unui e-mail la adresa dvs. înregistrată;\n"
            "- unei notificări vizibile în tabloul de bord al Furnizorului.\n\n"
            "10.2 Dacă nu acceptați Termenii modificați, vă puteți rezilia contul înainte de data intrării în vigoare a modificării. Utilizarea continuă a Platformei după data intrării în vigoare constituie acceptarea Termenilor modificați.\n\n"
            "10.3 Perioada de preaviz de 15 zile poate fi scurtată în cazul în care Nevumo este obligată să modifice Termenii prin lege sau reglementare. În astfel de cazuri, Nevumo vă va notifica cât mai curând posibil."
        ),
        "ru": (
            "10.1 Nevumo может изменить настоящие Условия для Поставщиков в любое время. О любых изменениях вам сообщат не менее чем за 15 дней до их вступления в силу посредством:\n"
            "- электронного письма на ваш зарегистрированный адрес;\n"
            "- заметного уведомления на панели инструментов Поставщика.\n\n"
            "10.2 Если вы не принимаете измененные Условия, вы можете закрыть свою учетную запись до даты вступления изменений в силу. Дальнейшее использование Платформы после даты вступления в силу означает принятие измененных Условий.\n\n"
            "10.3 15-дневный период уведомления может быть сокращен, если Nevumo обязано изменить Условия по закону или нормативному акту. В таких случаях Nevumo уведомит вас как можно скорее."
        ),
        "uk": (
            "10.1 Nevumo може змінити ці Умови для Постачальників у будь-який час. Про будь-які зміни вас повідомлять щонайменше за 15 днів до їх набрання чинності через:\n"
            "- електронний лист на вашу зареєстровану адресу;\n"
            "- помітне повідомлення на панелі інструментів Постачальника.\n\n"
            "10.2 Якщо ви не приймаєте змінені Умови, ви можете закрити свій обліковий запис до дати набрання чинності змінами. Подальше використання Платформи після дати набрання чинності означає прийняття змінених Умов.\n\n"
            "10.3 15-денний період повідомлення може бути скорочений, якщо Nevumo зобов'язане змінити Умови за законом або нормативним актом. У таких випадках Nevumo повідомить вас якомога швидше."
        ),
        "cs": (
            "10.1 Společnost Nevumo může tyto podmínky pro poskytovatele kdykoli změnit. Jakékoli změny vám budou sděleny nejméně 15 dní před nabytím účinnosti, a to prostřednictvím:\n"
            "- e-mailu na vaši registrovanou adresu;\n"
            "- nápadného oznámení na vašem řídicím panelu poskytovatele.\n\n"
            "10.2 Pokud nesouhlasíte s upravenými podmínkami, můžete svůj účet před datem účinnosti změny ukončit. Další používání platformy po datu účinnosti představuje přijetí upravených podmínek.\n\n"
            "10.3 Patnáctidenní výpovědní lhůta může být zkrácena, pokud je společnost Nevumo povinna změnit podmínky ze zákona nebo nařízení. V takových případech vás bude společnost Nevumo informovat co nejdříve."
        ),
        "da": (
            "10.1 Nevumo kan til enhver tid ændre disse vilkår for udbydere. Enhver ændring vil blive meddelt dig mindst 15 dage før de træder i kraft, via:\n"
            "- en e-mail til din registrerede adresse;\n"
            "- en tydelig meddelelse på dit udbyder-dashboard.\n\n"
            "10.2 Hvis du ikke accepterer de ændrede vilkår, kan du opsige din konto inden ændringens ikrafttrædelsesdato. Fortsat brug af platformen efter ikrafttrædelsesdatoen udgør accept af de ændrede vilkår.\n\n"
            "10.3 Varslet på 15 dage kan forkortes, hvis Nevumo er forpligtet til at ændre vilkårene i henhold til lov eller regler. I sådanne tilfælde vil Nevumo underrette dig hurtigst muligt."
        ),
        "sv": (
            "10.1 Nevumo kan ändra dessa villkor för leverantörer när som helst. Eventuella ändringar kommer att meddelas dig minst 15 dagar innan de träder i kraft, via:\n"
            "- ett e-postmeddelande till din registrerade adress;\n"
            "- ett tydligt meddelande på din leverantörsinstrumentpanel.\n\n"
            "10.2 Om du inte accepterar de ändrade villkoren kan du säga upp ditt konto före ändringens ikraftträdandedatum. Fortsatt användning av plattformen efter ikraftträdandedatumet utgör acceptans av de ändrade villkoren.\n\n"
            "10.3 Varselperioden på 15 dagar kan förkortas om Nevumo är skyldigt att ändra villkoren enligt lag eller förordning. I sådana fall kommer Nevumo att meddela dig så snart som rimligen är möjligt."
        ),
        "no": (
            "10.1 Nevumo kan endre disse vilkårene for leverandører når som helst. Eventuelle endringer vil bli meddelt deg minst 15 dager før de trer i kraft, via:\n"
            "- en e-post til din registrerte adresse;\n"
            "- en tydelig melding på leverandørdashbordet ditt.\n\n"
            "10.2 Hvis du ikke aksepterer de endrede vilkårene, kan du si opp kontoen din før endringens ikrafttredelsesdato. Fortsatt bruk av plattformen etter ikrafttredelsesdatoen utgjør aksept av de endrede vilkårene.\n\n"
            "10.3 Varslingsperioden på 15 dager kan forkortes der Nevumo er pålagt å endre vilkårene ved lov eller forskrift. I slike tilfeller vil Nevumo varsle deg så snart det er praktisk mulig."
        ),
        "fi": (
            "10.1 Nevumo voi muuttaa näitä palveluntarjoajien ehtoja milloin tahansa. Kaikista muutoksista ilmoitetaan sinulle vähintään 15 päivää ennen niiden voimaantuloa seuraavilla tavoilla:\n"
            "- sähköpostitse rekisteröityyn osoitteeseesi;\n"
            "- näkyvällä ilmoituksella palveluntarjoajan hallintapaneelissasi.\n\n"
            "10.2 Jos et hyväksy muutettuja ehtoja, voit irtisanoa tilisi ennen muutoksen voimaantulopäivää. Alustan käytön jatkaminen voimaantulopäivän jälkeen merkitsee muutettujen ehtojen hyväksymistä.\n\n"
            "10.3 15 päivän ilmoitusaikaa voidaan lyhentää, jos lakisääteinen velvoite edellyttää Nevumoa muuttamaan ehtoja. Tällaisissa tapauksissa Nevumo ilmoittaa asiasta sinulle mahdollisimman pian."
        ),
        "et": (
            "10.1 Nevumo võib neid teenusepakkujate tingimusi igal ajal muuta. Kõigist muudatustest teatatakse teile vähemalt 15 päeva enne nende jõustumist järgmistel viisidel:\n"
            "- e-kiri teie registreeritud aadressile;\n"
            "- silmatorkav teade teie teenusepakkuja juhtpaneelil.\n\n"
            "10.2 Kui te ei nõustu muudetud tingimustega, võite oma konto lõpetada enne muudatuse jõustumise kuupäeva. Platvormi jätkuv kasutamine pärast jõustumiskuupäeva kujutab endast muudetud tingimustega nõustumist.\n\n"
            "10.3 15-päevast etteteatamistähtaega võib lühendada, kui Nevumo on seaduse või määrusega kohustatud tingimusi muutma. Sellistel juhtudel teavitab Nevumo teid sellest esimesel võimalusel."
        ),
        "lt": (
            "10.1 Nevumo gali bet kada pakeisti šias Paslaugų teikėjų sąlygas. Apie bet kokius pakeitimus jums bus pranešta likus bent 15 dienų iki jų įsigaliojimo, per:\n"
            "- el. laišką jūsų registruotu adresu;\n"
            "- matomą pranešimą jūsų paslaugų teikėjo prietaisų skydelyje.\n\n"
            "10.2 Jei nesutinkate su pakeistomis sąlygomis, galite nutraukti savo paskyrą iki pakeitimo įsigaliojimo dienos. Tolesnis platformos naudojimas po įsigaliojimo datos reiškia pakeistų sąlygų priėmimą.\n\n"
            "10.3 15 dienų įspėjimo laikotarpis gali būti sutrumpintas, jei Nevumo privalo pakeisti sąlygas pagal įstatymą ar kitą teisės aktą. Tokiais atvejais Nevumo kuo greičiau jums apie tai praneš."
        ),
        "lv": (
            "10.1 Nevumo var jebkurā laikā grozīt šos Pakalpojumu sniedzēju noteikumus. Par jebkādiem grozījumiem jums tiks paziņots vismaz 15 dienas pirms to stāšanās spēkā, izmantojot:\n"
            "- e-pastu uz jūsu reģistrēto adresi;\n"
            "- redzamu paziņojumu jūsu Pakalpojumu sniedzēja informācijas panelī.\n\n"
            "10.2 Ja nepiekrītat grozītajiem noteikumiem, varat izbeigt sava konta darbību pirms grozījumu spēkā stāšanās dienas. Turpmāka Platformas izmantošana pēc spēkā stāšanās dienas nozīmē grozīto noteikumu pieņemšanu.\n\n"
            "10.3 15 dienu brīdinājuma termiņu var saīsināt, ja Nevumo ir pienākums grozīt noteikumus saskaņā ar tiesību aktiem vai noteikumiem. Šādos gadījumos Nevumo par to paziņos jums pēc iespējas ātrāk."
        ),
        "hu": (
            "10.1 A Nevumo bármikor módosíthatja ezeket a Szolgáltatói Feltételeket. Minden módosításról legalább 15 nappal azok hatálybalépése előtt értesítjük a következő módokon:\n"
            "- a regisztrált címére küldött e-mailben;\n"
            "- a Szolgáltatói irányítópultján megjelenő jól látható értesítéssel.\n\n"
            "10.2 Ha nem fogadja el a módosított feltételeket, a módosítás hatálybalépésének dátuma előtt megszüntetheti fiókját. A Platform hatálybalépés dátumát követő további használata a módosított feltételek elfogadásának minősül.\n\n"
            "10.3 A 15 napos felmondási idő lerövidíthető, ha a Nevumo-t törvény vagy rendelet kötelezi a Feltételek módosítására. Ilyen esetekben a Nevumo a lehető leghamarabb értesíti Önt."
        ),
        "hr": (
            "10.1 Nevumo može izmijeniti ove Uvjete za pružatelje usluga u bilo kojem trenutku. Sve izmjene bit će vam priopćene najmanje 15 dana prije stupanja na snagu, putem:\n"
            "- e-pošte na vašu registriranu adresu;\n"
            "- istaknute obavijesti na vašoj nadzornoj ploči za Pružatelje usluga.\n\n"
            "10.2 Ako ne prihvatite izmijenjene Uvjete, možete zatvoriti svoj račun prije datuma stupanja na snagu izmjene. Nastavak korištenja Platforme nakon datuma stupanja na snagu predstavlja prihvaćanje izmijenjenih Uvjeta.\n\n"
            "10.3 Otkazni rok od 15 dana može se skratiti kada se od tvrtke Nevumo zahtijeva promjena Uvjeta zakonom ili propisom. U takvim slučajevima Nevumo će vas obavijestiti čim to bude razumno izvedivo."
        ),
        "sk": (
            "10.1 Spoločnosť Nevumo môže tieto podmienky pre poskytovateľov kedykoľvek zmeniť. Akékoľvek zmeny vám budú oznámené najmenej 15 dní pred nadobudnutím účinnosti, a to prostredníctvom:\n"
            "- e-mailu na vašu registrovanú adresu;\n"
            "- nápadného oznámenia na vašom riadiacom paneli poskytovateľa.\n\n"
            "10.2 Ak nesúhlasíte s upravenými podmienkami, môžete svoj účet pred dátumom účinnosti zmeny ukončiť. Ďalšie používanie platformy po dátume účinnosti predstavuje prijatie upravených podmienok.\n\n"
            "10.3 Pätnásťdňová výpovedná lehota sa môže skrátiť, ak je spoločnosť Nevumo povinná zmeniť podmienky na základe zákona alebo nariadenia. V takýchto prípadoch vás bude spoločnosť Nevumo informovať čo najskôr."
        ),
        "sl": (
            "10.1 Nevumo lahko kadar koli spremeni te pogoje za ponudnike. O vseh spremembah vas bomo obvestili vsaj 15 dni pred začetkom njihove veljavnosti prek:\n"
            "- e-pošte na vaš registrirani naslov;\n"
            "- vidnega obvestila na vaši nadzorni plošči ponudnika.\n\n"
            "10.2 Če spremenjenih pogojev ne sprejemate, lahko zaprete svoj račun pred datumom začetka veljavnosti spremembe. Nadaljnja uporaba platforme po datumu začetka veljavnosti predstavlja sprejetje spremenjenih pogojev.\n\n"
            "10.3 15-dnevni odpovedni rok se lahko skrajša, če mora Nevumo spremeniti pogoje na podlagi zakona ali predpisa. V takih primerih vas bo Nevumo obvestil takoj, ko bo to razumno mogoče."
        ),
        "el": (
            "10.1 Η Nevumo μπορεί να τροποποιήσει αυτούς τους Όρους Παρόχου ανά πάσα στιγμή. Οποιεσδήποτε τροποποιήσεις θα σας κοινοποιούνται τουλάχιστον 15 ημέρες πριν τεθούν σε ισχύ, μέσω:\n"
            "- ηλεκτρονικού ταχυδρομείου στην καταχωρημένη διεύθυνσή σας.\n"
            "- μίας ευδιάκριτης ειδοποίησης στον πίνακα ελέγχου Παρόχου σας.\n\n"
            "10.2 Εάν δεν αποδέχεστε τους τροποποιημένους Όρους, μπορείτε να τερματίσετε τον λογαριασμό σας πριν από την ημερομηνία έναρξης ισχύος της τροποποίησης. Η συνεχής χρήση της Πλατφόρμας μετά την ημερομηνία έναρξης ισχύος συνιστά αποδοχή των τροποποιημένων Όρων.\n\n"
            "10.3 Η περίοδος ειδοποίησης των 15 ημερών μπορεί να συντομευτεί εάν η Nevumo υποχρεούται να τροποποιήσει τους Όρους από το νόμο ή τους κανονισμούς. Σε τέτοιες περιπτώσεις, η Nevumo θα σας ειδοποιήσει το συντομότερο δυνατόν."
        ),
        "tr": (
            "10.1 Nevumo bu Sağlayıcı Şartlarını istediği zaman değiştirebilir. Herhangi bir değişiklik, yürürlüğe girmeden en az 15 gün önce aşağıdakiler aracılığıyla size bildirilecektir:\n"
            "- kayıtlı adresinize e-posta;\n"
            "- Sağlayıcı kontrol panelinizde belirgin bir bildirim.\n\n"
            "10.2 Değiştirilen Şartları kabul etmiyorsanız, değişikliğin yürürlüğe girme tarihinden önce hesabınızı feshedebilirsiniz. Yürürlüğe girme tarihinden sonra Platformun kullanılmaya devam edilmesi, değiştirilen Şartların kabul edildiği anlamına gelir.\n\n"
            "10.3 15 günlük bildirim süresi, Nevumo'nun Şartları kanun veya yönetmelik gereği değiştirmesi gerektiğinde kısaltılabilir. Böyle durumlarda Nevumo sizi en kısa sürede bilgilendirecektir."
        ),
        "ga": (
            "10.1 Féadfaidh Nevumo na Téarmaí Soláthraí seo a leasú amhálacha. Cuirfear aon leasuithe in iúl duit ar a laghad 15 lá sula dtiocfaidh siad i bhfeidhm, trí:\n"
            "- ríomhphost chuig do sheoladh cláraithe;\n"
            "- fógra feiceálach i do dheais Soláthraí.\n\n"
            "10.2 Mura nglacann tú leis na Téarmaí leasaithe, is féidir leat do chuntas a fhoirceannadh roimh dháta éifeachtach an leasaithe. Is ionann úsáid leanúnach an Ardáin tar éis an dáta éifeachtaigh agus glacadh leis na Téarmaí leasaithe.\n\n"
            "10.3 Féadfar an tréimhse fógra 15 lá a ghiorrú nuair a theastaíonn ó Nevumo na Téarmaí a leasú le dlí nó rialachán. I gcásanna den sórt sin, tabharfaidh Nevumo fógra duit a luaithe agus is indéanta go réasúnach."
        ),
        "is": (
            "10.1 Nevumo getur breytt þessum skilmálum fyrir þjónustuveitendur hvenær sem er. Allar breytingar munu verða tilkynntar þér að minnsta kosti 15 dögum áður en þær taka gildi, með:\n"
            "- tölvupósti á skráð netfang þitt;\n"
            "- áberandi tilkynningu á stjórnborði þjónustuveitanda þíns.\n\n"
            "10.2 Ef þú samþykkir ekki breyttu skilmálana geturðu sagt upp reikningi þínum fyrir gildistökudag breytingarinnar. Áframhaldandi notkun á vettvangnum eftir gildistökudag telst vera samþykki á breyttum skilmálum.\n\n"
            "10.3 15 daga uppsagnarfresturinn gæti verið styttur þar sem Nevumo er skylt að breyta skilmálunum samkvæmt lögum eða reglugerðum. Í slíkum tilfellum mun Nevumo tilkynna þér eins fljótt og auðið er."
        ),
        "lb": (
            "10.1 Nevumo kann dës Ubidderbedéngungen zu all Moment änneren. All Ännerunge ginn Iech op d'mannst 15 Deeg ier se a Kraaft trieden matgedeelt, via:\n"
            "- E-Mail un Är registréiert Adress;\n"
            "- eng däitlech Notiz op Ärem Ubidder-Dashboard.\n\n"
            "10.2 Wann Dir déi geännert Bedéngungen net akzeptéiert, kënnt Dir Äre Kont virum Datum wou d'Ännerung a Kraaft trëtt kënnegen. Déi weider Notzung vun der Plattform nom Datum vum a Kraaft trieden stellt eng Akzeptanz vun de geännerte Bedéngungen duer.\n\n"
            "10.3 D'Frist vu 15 Deeg kann verkierzt ginn wou Nevumo gesetzlech oder reglementaresch verpflicht ass d'Bedéngungen z'änneren. An esou Fäll wäert Nevumo Iech esou séier wéi méiglech informéieren."
        ),
        "mk": (
            "10.1 Nevumo може да ги измени овие Услови за Даватели во кое било време. Сите измени ќе ви бидат соопштени најмалку 15 дена пред да стапат на сила, преку:\n"
            "- е-пошта на вашата регистрирана адреса;\n"
            "- истакнато известување на вашата контролна табла на Давател.\n\n"
            "10.2 Доколку не ги прифаќате изменетите Услови, можете да го раскинете вашиот профил пред датумот на стапување на сила на измената. Продолжената употреба на Платформата по датумот на стапување на сила претставува прифаќање на изменетите Услови.\n\n"
            "10.3 Периодот на известување од 15 дена може да се скрати каде што од Nevumo се бара да ги измени Условите според закон или регулатива. Во такви случаи, Nevumo ќе ве извести што е можно поскоро."
        ),
        "mt": (
            "10.1 Nevumo jista' jemenda dawn it-Termini għall-Fornituri fi kwalunkwe ħin. Kwalunkwe emenda tiġi kkomunikata lilek mill-inqas 15-il jum qabel ma tidħol fis-seħħ, permezz ta':\n"
            "- e-mail lill-indirizz irreġistrat tiegħek;\n"
            "- avviż prominenti fid-dashboard tal-Fornitur tiegħek.\n\n"
            "10.2 Jekk ma taċċettax it-Termini emendati, tista' tittermina l-kont tiegħek qabel id-data effettiva tal-emenda. L-użu kontinwu tal-Pjattaforma wara d-data effettiva jikkostitwixxi aċċettazzjoni tat-Termini emendati.\n\n"
            "10.3 Il-perjodu ta' avviż ta' 15-il jum jista' jitqassar fejn Nevumo huwa meħtieġ jemenda t-Termini mil-liġi jew ir-regolament. F'każijiet bħal dawn, Nevumo ser jinnotifikak kemm jista' jkun malajr b'mod raġonevoli."
        ),
        "sq": (
            "10.1 Nevumo mund të ndryshojë këto Kushte për Ofruesit në çdo kohë. Çdo ndryshim do t'ju komunikohet të paktën 15 ditë para se të hyjë në fuqi, përmes:\n"
            "- email-it në adresën tuaj të regjistruar;\n"
            "- një njoftimi të dukshëm në panelin tuaj të Ofruesit.\n\n"
            "10.2 Nëse nuk i pranoni Kushtet e ndryshuara, ju mund ta përfundoni llogarinë tuaj para datës së hyrjes në fuqi të ndryshimit. Përdorimi i vazhdueshëm i Platformës pas datës së hyrjes në fuqi përbën pranim të Kushteve të ndryshuara.\n\n"
            "10.3 Periudha e njoftimit prej 15 ditësh mund të shkurtohet kur Nevumo kërkohet t'i ndryshojë Kushtet me ligj ose rregullore. Në raste të tilla, Nevumo do t'ju njoftojë sa më shpejt të jetë e mundur në mënyrë të arsyeshme."
        ),
        "sr": (
            "10.1 Nevumo može da izmeni ove Uslove za pružaoce usluga u bilo kom trenutku. Sve izmene biće vam saopštene najmanje 15 dana pre stupanja na snagu, putem:\n"
            "- e-pošte na vašu registrovanu adresu;\n"
            "- istaknutog obaveštenja na vašoj kontrolnoj tabli Pružaoca usluga.\n\n"
            "10.2 Ako ne prihvatite izmenjene Uslove, možete da zatvorite svoj nalog pre datuma stupanja na snagu izmene. Nastavak korišćenja Platforme nakon datuma stupanja na snagu predstavlja prihvatanje izmenjenih Uslova.\n\n"
            "10.3 Otkazni rok od 15 dana može se skratiti kada se od kompanije Nevumo zahteva promena Uslova zakonom ili propisom. U takvim slučajevima Nevumo će vas obavestiti čim to bude razumno izvodljivo."
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
        print(f"✅ Seeded {count} translations for {NAMESPACE}.art10_body")

if __name__ == "__main__":
    seed()
