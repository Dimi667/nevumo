"""
seed_provider_terms_p22_art17_18_body.py  —  Nevumo | namespace: provider_terms
Key: art17_body, art18_body  (2 keys x 34 langs = 68 rows)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_provider_terms_p22_art17_18_body
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
    "art17_body": {
        "en": (
            "17.1 These Provider Terms are governed by the law of Bulgaria.\n\n"
            "17.2 For Providers acting as businesses (traders), any dispute arising from these Provider Terms that cannot be resolved by mediation shall be subject to the exclusive jurisdiction of the competent courts of Sofia, Bulgaria.\n\n"
            "17.3 Nothing in this section overrides any mandatory consumer or business protection rights under the law of the Provider's country of establishment, to the extent that such rights cannot be waived by contract."
        ),
        "bg": (
            "1. Настоящите Условия за Доставчици се уреждат от правото на Република България.\n\n"
            "2. За Доставчиците, действащи като търговци, всички спорове, произтичащи от настоящите Условия за Доставчици, които не могат да бъдат разрешени чрез медиация, са в изключителната подсъдност на компетентните съдилища в гр. София, България.\n\n"
            "3. Нищо в настоящия член не отменя задължителни разпоредби за защита на потребителите и предприемачите, приложими в страната на установяване на Доставчика, доколкото такива разпоредби не могат да бъдат изключени по договор."
        ),
        "pl": (
            "1. Niniejszy Regulamin Dostawców podlega prawu bułgarskiemu.\n\n"
            "2. W przypadku Dostawców działających jako przedsiębiorcy wszelkie spory wynikające z niniejszego Regulaminu Dostawców, których nie uda się rozwiązać w drodze mediacji, będą rozstrzygane przez właściwy sąd w Sofii, Bułgaria.\n\n"
            "3. Żadne postanowienie niniejszego paragrafu nie narusza bezwzględnie obowiązujących przepisów ochrony konsumentów i przedsiębiorców obowiązujących w kraju siedziby Dostawcy, w zakresie, w jakim nie można ich wyłączyć umownie."
        ),
        "de": (
            "17.1 Diese Anbieterbedingungen unterliegen dem Recht Bulgariens.\n\n"
            "17.2 Für Anbieter, die als Unternehmen (Händler) handeln, unterliegt jede Streitigkeit, die sich aus diesen Anbieterbedingungen ergibt und nicht durch Mediation gelöst werden kann, der ausschließlichen Zuständigkeit der zuständigen Gerichte in Sofia, Bulgarien.\n\n"
            "17.3 Nichts in diesem Abschnitt setzt zwingende Verbraucher- oder Unternehmensschutzrechte nach dem Recht des Niederlassungslandes des Anbieters außer Kraft, soweit auf solche Rechte nicht vertraglich verzichtet werden kann."
        ),
        "fr": (
            "17.1 Les présentes Conditions pour les Fournisseurs sont régies par le droit bulgare.\n\n"
            "17.2 Pour les Fournisseurs agissant en tant qu'entreprises (professionnels), tout litige découlant de ces Conditions pour les Fournisseurs qui ne peut être résolu par la médiation sera soumis à la juridiction exclusive des tribunaux compétents de Sofia, Bulgarie.\n\n"
            "17.3 Rien dans cette section ne déroge aux droits obligatoires de protection des consommateurs ou des entreprises en vertu du droit du pays d'établissement du Fournisseur, dans la mesure où ces droits ne peuvent faire l'objet d'une renonciation contractuelle."
        ),
        "es": (
            "17.1 Estas Condiciones para Proveedores se rigen por la ley de Bulgaria.\n\n"
            "17.2 Para los Proveedores que actúen como empresas (comerciantes), cualquier disputa derivada de estas Condiciones para Proveedores que no pueda resolverse mediante mediación estará sujeta a la jurisdicción exclusiva de los tribunales competentes de Sofía, Bulgaria.\n\n"
            "17.3 Nada en esta sección anula ningún derecho obligatorio de protección del consumidor o de la empresa en virtud de la ley del país de establecimiento del Proveedor, en la medida en que no se pueda renunciar a dichos derechos por contrato."
        ),
        "it": (
            "17.1 Le presenti Condizioni per i Fornitori sono regolate dalla legge della Bulgaria.\n\n"
            "17.2 Per i Fornitori che agiscono come imprese (professionisti), qualsiasi controversia derivante dalle presenti Condizioni per i Fornitori che non possa essere risolta tramite mediazione sarà soggetta alla giurisdizione esclusiva dei tribunali competenti di Sofia, Bulgaria.\n\n"
            "17.3 Nulla nella presente sezione prevale su qualsiasi diritto inderogabile di protezione dei consumatori o delle imprese ai sensi della legge del paese di stabilimento del Fornitore, nella misura in cui a tali diritti non si possa rinunciare contrattualmente."
        ),
        "nl": (
            "17.1 Deze Voorwaarden voor Dienstverleners worden beheerst door het recht van Bulgarije.\n\n"
            "17.2 Voor Dienstverleners die als bedrijven (handelaren) optreden, is elk geschil dat voortvloeit uit deze Voorwaarden voor Dienstverleners en dat niet kan worden opgelost door bemiddeling, onderworpen aan de exclusieve bevoegdheid van de bevoegde rechtbanken van Sofia, Bulgarije.\n\n"
            "17.3 Niets in deze sectie doet afbreuk aan dwingende rechten inzake consumenten- of bedrijfsbescherming krachtens de wet van het land van vestiging van de Dienstverlener, voor zover van dergelijke rechten niet bij contract kan worden afgeweken."
        ),
        "pt": (
            "17.1 Estes Termos para Prestadores são regidos pela lei da Bulgária.\n\n"
            "17.2 Para os Prestadores que atuam como empresas (comerciantes), qualquer litígio decorrente destes Termos para Prestadores que não possa ser resolvido por mediação estará sujeito à jurisdição exclusiva dos tribunais competentes de Sófia, Bulgária.\n\n"
            "17.3 Nada nesta secção anula quaisquer direitos obrigatórios de proteção do consumidor ou da empresa ao abrigo da lei do país de estabelecimento do Prestador, na medida em que tais direitos não possam ser renunciados por contrato."
        ),
        "pt-PT": (
            "17.1 Estes Termos para Prestadores são regidos pela lei da Bulgária.\n\n"
            "17.2 Para os Prestadores que atuam como empresas (comerciantes), qualquer litígio decorrente destes Termos para Prestadores que não possa ser resolvido por mediação estará sujeito à jurisdição exclusiva dos tribunais competentes de Sófia, Bulgária.\n\n"
            "17.3 Nada nesta secção anula quaisquer direitos obrigatórios de proteção do consumidor ou da empresa ao abrigo da lei do país de estabelecimento do Prestador, na medida em que tais direitos não possam ser renunciados por contrato."
        ),
        "ro": (
            "17.1 Acești Termeni pentru Furnizori sunt guvernați de legea Bulgariei.\n\n"
            "17.2 Pentru Furnizorii care acționează ca întreprinderi (comercianți), orice litigiu care decurge din acești Termeni pentru Furnizori și care nu poate fi soluționat prin mediere va fi supus jurisdicției exclusive a instanțelor competente din Sofia, Bulgaria.\n\n"
            "17.3 Nimic din această secțiune nu anulează drepturile obligatorii de protecție a consumatorilor sau a întreprinderilor în temeiul legii țării de stabilire a Furnizorului, în măsura în care la astfel de drepturi nu se poate renunța prin contract."
        ),
        "ru": (
            "17.1 Настоящие Условия для Поставщиков регулируются законодательством Болгарии.\n\n"
            "17.2 Для Поставщиков, действующих как предприятия (коммерсанты), любые споры, вытекающие из настоящих Условий для Поставщиков, которые не могут быть разрешены путем посредничества, подлежат исключительной юрисдикции компетентных судов Софии, Болгария.\n\n"
            "17.3 Ничто в этом разделе не отменяет обязательные права на защиту потребителей или предприятий в соответствии с законодательством страны учреждения Поставщика, в той степени, в которой от таких прав нельзя отказаться по договору."
        ),
        "uk": (
            "17.1 Ці Умови для Постачальників регулюються законодавством Болгарії.\n\n"
            "17.2 Для Постачальників, які діють як підприємства (комерсанти), будь-які спори, що випливають з цих Умов для Постачальників і які не можуть бути вирішені шляхом медіації, підлягають виключній юрисдикції компетентних судів Софії, Болгарія.\n\n"
            "17.3 Ніщо в цьому розділі не скасовує обов'язкові права на захист споживачів або підприємств відповідно до законодавства країни заснування Постачальника тією мірою, якою від таких прав не можна відмовитися за договором."
        ),
        "cs": (
            "17.1 Tyto podmínky pro poskytovatele se řídí právem Bulharska.\n\n"
            "17.2 Pro poskytovatele, kteří jednají jako podniky (obchodníci), podléhá jakýkoli spor vyplývající z těchto podmínek pro poskytovatele, který nelze vyřešit mediací, výlučné jurisdikci příslušných soudů v Sofii, Bulharsko.\n\n"
            "17.3 Nic v tomto oddílu nepřepisuje žádná závazná práva na ochranu spotřebitele nebo podniku podle práva země sídla poskytovatele v rozsahu, v jakém se takových práv nelze smluvně vzdát."
        ),
        "da": (
            "17.1 Disse vilkår for udbydere er underlagt Bulgariens lovgivning.\n\n"
            "17.2 For udbydere, der optræder som virksomheder (erhvervsdrivende), skal enhver tvist, der opstår som følge af disse vilkår for udbydere, som ikke kan løses ved mægling, være underlagt den eksklusive jurisdiktion hos de kompetente domstole i Sofia, Bulgarien.\n\n"
            "17.3 Intet i dette afsnit tilsidesætter ufravigelige forbruger- eller virksomhedsbeskyttelsesrettigheder i henhold til lovgivningen i udbyderens etableringsland, i det omfang der ikke kan gives afkald på sådanne rettigheder ved kontrakt."
        ),
        "sv": (
            "17.1 Dessa villkor för leverantörer styrs av bulgarisk lag.\n\n"
            "17.2 För leverantörer som agerar som företag (näringsidkare) ska alla tvister som uppstår från dessa villkor för leverantörer, som inte kan lösas genom medling, vara underkastade den exklusiva jurisdiktionen av de behöriga domstolarna i Sofia, Bulgarien.\n\n"
            "17.3 Inget i detta avsnitt åsidosätter några obligatoriska konsument- eller företagsskyddsrättigheter enligt lagen i det land där leverantören är etablerad, i den utsträckning sådana rättigheter inte kan avtalas bort."
        ),
        "no": (
            "17.1 Disse vilkårene for leverandører er underlagt bulgarsk lov.\n\n"
            "17.2 For leverandører som opptrer som bedrifter (næringsdrivende), skal enhver tvist som oppstår fra disse vilkårene for leverandører, som ikke kan løses ved mekling, være underlagt den eksklusive jurisdiksjonen til de kompetente domstolene i Sofia, Bulgaria.\n\n"
            "17.3 Ingenting i denne delen overstyrer eventuelle obligatoriske forbruker- eller bedriftsbeskyttelsesrettigheter under loven i leverandørens etableringsland, i den grad slike rettigheter ikke kan fravikes ved kontrakt."
        ),
        "fi": (
            "17.1 Näihin palveluntarjoajien ehtoihin sovelletaan Bulgarian lakia.\n\n"
            "17.2 Yrityksinä (elinkeinonharjoittajina) toimivien palveluntarjoajien osalta kaikki näistä palveluntarjoajien ehdoista johtuvat riidat, joita ei voida ratkaista sovittelulla, kuuluvat Sofian, Bulgarian, toimivaltaisten tuomioistuinten yksinomaiseen toimivaltaan.\n\n"
            "17.3 Mikään tässä osiossa ei syrjäytä pakottavia kuluttajan- tai yrityssuojanoikeuksia palveluntarjoajan sijoittautumismaan lain nojalla siinä määrin kuin tällaisista oikeuksista ei voida sopimuksella luopua."
        ),
        "et": (
            "17.1 Neid teenusepakkujate tingimusi reguleerib Bulgaaria seadus.\n\n"
            "17.2 Teenusepakkujate jaoks, kes tegutsevad ettevõtetena (kauplejatena), alluvad kõik nendest teenusepakkujate tingimustest tulenevad vaidlused, mida ei saa lahendada lepituse teel, Sofia, Bulgaaria pädevate kohtute ainupädevusele.\n\n"
            "17.3 Miski selles jaotises ei tühista kohustuslikke tarbija- või ettevõttekaitse õigusi, mis tulenevad teenusepakkuja asukohariigi seadusest, ulatuses, milles sellistest õigustest ei saa lepinguga loobuda."
        ),
        "lt": (
            "17.1 Šioms Paslaugų teikėjų sąlygoms taikomi Bulgarijos įstatymai.\n\n"
            "17.2 Paslaugų teikėjams, veikiantiems kaip įmonės (prekybininkai), bet koks ginčas, kylantis iš šių Paslaugų teikėjų sąlygų, kurio negalima išspręsti tarpininkaujant, priklauso išimtinei Bulgarijos, Sofijos, kompetentingų teismų jurisdikcijai.\n\n"
            "17.3 Niekas šiame skirsnyje nepanaikina jokių privalomų vartotojų ar verslo apsaugos teisių pagal paslaugų teikėjo įsisteigimo šalies įstatymus tiek, kiek tokių teisių negalima atsisakyti sutartimi."
        ),
        "lv": (
            "17.1 Šiem Pakalpojumu sniedzēju noteikumiem piemērojami Bulgārijas tiesību akti.\n\n"
            "17.2 Attiecībā uz Pakalpojumu sniedzējiem, kas darbojas kā uzņēmumi (tirgotāji), jebkurš strīds, kas izriet no šiem Pakalpojumu sniedzēju noteikumiem un ko nevar atrisināt ar mediāciju, ir pakļauts tikai kompetento tiesu jurisdikcijai Sofijā, Bulgārijā.\n\n"
            "17.3 Nekas šajā sadaļā neatceļ nekādas obligātās patērētāju vai uzņēmējdarbības aizsardzības tiesības saskaņā ar Pakalpojumu sniedzēja reģistrācijas valsts tiesību aktiem tiktāl, ciktāl no šādām tiesībām nevar atteikties ar līgumu."
        ),
        "hu": (
            "17.1 Jelen Szolgáltatói Feltételekre Bulgária jogszabályai az irányadók.\n\n"
            "17.2 A vállalkozásként (kereskedőként) eljáró Szolgáltatók esetében a jelen Szolgáltatói Feltételekből eredő minden olyan vita, amelyet nem lehet közvetítéssel megoldani, a bulgáriai Szófia illetékes bíróságainak kizárólagos joghatósága alá tartozik.\n\n"
            "17.3 Ez a szakasz nem bírálja felül a Szolgáltató letelepedése szerinti ország joga szerinti kötelező fogyasztó- vagy vállalkozásvédelmi jogokat, amennyiben ezen jogokról szerződésben nem lehet lemondani."
        ),
        "hr": (
            "17.1 Ovi Uvjeti za pružatelje usluga podliježu zakonima Bugarske.\n\n"
            "17.2 Za Pružatelje usluga koji djeluju kao poduzeća (trgovci), bilo koji spor koji proizlazi iz ovih Uvjeta za pružatelje usluga, a koji se ne može riješiti mirenjem, bit će u isključivoj nadležnosti nadležnih sudova u Sofiji, Bugarska.\n\n"
            "17.3 Ništa u ovom odjeljku ne poništava nikakva obvezna prava na zaštitu potrošača ili poduzeća prema zakonu zemlje osnivanja Pružatelja usluga, u mjeri u kojoj se takva prava ne mogu odreći ugovorom."
        ),
        "sk": (
            "17.1 Tieto podmienky pre poskytovateľov sa riadia právom Bulharska.\n\n"
            "17.2 Pre poskytovateľov, ktorí konajú ako podniky (obchodníci), podlieha akýkoľvek spor vyplývajúci z týchto podmienok pre poskytovateľov, ktorý nemožno vyriešiť mediáciou, výlučnej jurisdikcii príslušných súdov v Sofii, Bulharsko.\n\n"
            "17.3 Nič v tomto oddiele neprepisuje žiadne záväzné práva na ochranu spotrebiteľa alebo podniku podľa práva krajiny sídla poskytovateľa v rozsahu, v akom sa takýchto práv nemožno zmluvne vzdať."
        ),
        "sl": (
            "17.1 Te pogoje za ponudnike ureja bolgarska zakonodaja.\n\n"
            "17.2 Za ponudnike, ki delujejo kot podjetja (trgovci), vsak spor, ki izhaja iz teh pogojev za ponudnike in ga ni mogoče rešiti z mediacijo, spada v izključno pristojnost pristojnih sodišč v Sofiji, Bolgarija.\n\n"
            "17.3 Nič v tem razdelku ne prevlada nad obveznimi pravicami za zaščito potrošnikov ali podjetij v skladu z zakonodajo države ustanovitve ponudnika, v obsegu, v katerem se tem pravicam ni mogoče odpovedati s pogodbo."
        ),
        "el": (
            "17.1 Αυτοί οι Όροι Παρόχου διέπονται από τη νομοθεσία της Βουλγαρίας.\n\n"
            "17.2 Για Παρόχους που ενεργούν ως επιχειρήσεις (έμποροι), οποιαδήποτε διαφορά προκύψει από αυτούς τους Όρους Παρόχου που δεν μπορεί να επιλυθεί με διαμεσολάβηση θα υπόκειται στην αποκλειστική δικαιοδοσία των αρμόδιων δικαστηρίων της Σόφιας, Βουλγαρία.\n\n"
            "17.3 Τίποτα σε αυτή την ενότητα δεν παρακάμπτει τυχόν υποχρεωτικά δικαιώματα προστασίας καταναλωτών ή επιχειρήσεων σύμφωνα με τη νομοθεσία της χώρας εγκατάστασης του Παρόχου, στο βαθμό που δεν είναι δυνατή η παραίτηση από τέτοια δικαιώματα μέσω σύμβασης."
        ),
        "tr": (
            "17.1 Bu Sağlayıcı Şartları, Bulgaristan yasalarına tabidir.\n\n"
            "17.2 İşletme (tüccar) olarak hareket eden Sağlayıcılar için, bu Sağlayıcı Şartlarından kaynaklanan ve arabuluculuk yoluyla çözülemeyen herhangi bir anlaşmazlık, Sofya, Bulgaristan'ın yetkili mahkemelerinin münhasır yargı yetkisine tabi olacaktır.\n\n"
            "17.3 Bu bölümdeki hiçbir şey, Sağlayıcının kuruluş ülkesinin yasaları kapsamındaki hiçbir zorunlu tüketici veya işletme koruma hakkını, sözleşme yoluyla feragat edilemeyecek ölçüde geçersiz kılmaz."
        ),
        "ga": (
            "17.1 Tá na Téarmaí Soláthraí seo faoi rialú dhlí na Bulgáire.\n\n"
            "17.2 I gcás Soláthraithe atá ag gníomhú mar ghnólachtaí (trádálaithe), beidh aon díospóid a éiríonn as na Téarmaí Soláthraí seo nach féidir a réiteach le hidirghabháil faoi dhlínse eisiach chúirteanna inniúla Shóifia, an Bhulgáir.\n\n"
            "17.3 Ní sháraíonn aon rud sa roinn seo aon chearta éigeantacha cosanta tomhaltóirí nó gnó faoi dhlí thír bhunaithe an tSoláthraí, a mhéid nach féidir cearta den sórt sin a tharscaoileadh trí chonradh."
        ),
        "is": (
            "17.1 Þessir skilmálar fyrir þjónustuveitendur stjórnast af lögum í Búlgaríu.\n\n"
            "17.2 Fyrir þjónustuveitendur sem starfa sem fyrirtæki (kaupmenn), skal sérhver ágreiningur sem rís af þessum skilmálum fyrir þjónustuveitendur og sem ekki er hægt að leysa með sáttameðferð heyra undir einkalögsögu bærra dómstóla í Sófíu, Búlgaríu.\n\n"
            "17.3 Ekkert í þessum hluta gengur framar bindandi neytenda- eða fyrirtækjaverndarréttindum samkvæmt lögum í stofnlandi þjónustuveitandans, að því marki sem ekki er hægt að afsala sér slíkum réttindum með samningi."
        ),
        "lb": (
            "17.1 Dës Ubidderbedéngungen ënnerleien dem Gesetz vu Bulgarien.\n\n"
            "17.2 Fir Ubidder déi als Geschäfter (Händler) handelen, ënnerläit all Sträit, deen aus dësen Ubidderbedéngungen entsteet an net duerch Mediatioun geléist ka ginn, der exklusiver Juridictioun vun den zoustännege Geriichter vu Sofia, Bulgarien.\n\n"
            "17.3 Näischt an dëser Sektioun setzt zéngend Konsumente- oder Firmeschutzrechter ënner dem Gesetz vum Etablissementsland vum Ubidder ausser Kraaft, souwäit sou Rechter net vertraglech verzicht kënne ginn."
        ),
        "mk": (
            "17.1 Овие Услови за Даватели се регулирани според законите на Бугарија.\n\n"
            "17.2 За Давателите кои дејствуваат како бизниси (трговци), секој спор што произлегува од овие Услови за Даватели и што не може да се реши со медијација ќе подлежи на ексклузивната јурисдикција на надлежните судови во Софија, Бугарија.\n\n"
            "17.3 Ништо во овој дел не ги отфрла какви било задолжителни права за заштита на потрошувачите или бизнисите според законот на земјата на основање на Давателот, до тој степен што од таквите права не може да се откаже со договор."
        ),
        "mt": (
            "17.1 Dawn it-Termini għall-Fornituri huma rregolati mil-liġi tal-Bulgarija.\n\n"
            "17.2 Għal Fornituri li jaġixxu bħala negozji (negozjanti), kwalunkwe tilwima li tirriżulta minn dawn it-Termini għall-Fornituri li ma tistax tiġi riżolta permezz ta' medjazzjoni għandha tkun soġġetta għall-ġuriżdizzjoni esklużiva tal-qrati kompetenti f'Sofia, il-Bulgarija.\n\n"
            "17.3 Xejn f'din it-taqsima ma jipprevali fuq xi drittijiet mandatorji ta' protezzjoni tal-konsumatur jew tan-negozju taħt il-liġi tal-pajjiż ta' stabbiliment tal-Fornitur, sal-punt li tali drittijiet ma jistgħux jiġu rrinunzjati b'kuntratt."
        ),
        "sq": (
            "17.1 Këto Kushte për Ofruesit rregullohen nga ligji i Bullgarisë.\n\n"
            "17.2 Për Ofruesit që veprojnë si biznese (tregtarë), çdo mosmarrëveshje që rrjedh nga këto Kushte për Ofruesit që nuk mund të zgjidhet me ndërmjetësim do t'i nënshtrohet juridiksionit ekskluziv të gjykatave kompetente të Sofjes, Bullgari.\n\n"
            "17.3 Asgjë në këtë seksion nuk i mbivendoset asnjë të drejte të detyrueshme për mbrojtjen e konsumatorit ose biznesit sipas ligjit të vendit të themelimit të Ofruesit, deri në masën që të drejta të tilla nuk mund të hiqen me kontratë."
        ),
        "sr": (
            "17.1 Ovi Uslovi za pružaoce usluga regulisani su zakonom Bugarske.\n\n"
            "17.2 Za Pružaoce usluga koji deluju kao preduzeća (trgovci), bilo koji spor koji proizilazi iz ovih Uslova za pružaoce usluga koji se ne može rešiti posredovanjem biće u isključivoj nadležnosti nadležnih sudova u Sofiji, Bugarska.\n\n"
            "17.3 Ništa u ovom odeljku ne poništava bilo kakva obavezna prava na zaštitu potrošača ili poslovanja prema zakonu zemlje osnivanja Pružaoca usluga, u meri u kojoj se takva prava ne mogu odreći ugovorom."
        ),
    },
    "art18_body": {
        "en": (
            "18.1 If any provision of these Provider Terms is found to be invalid or unenforceable, the remaining provisions shall continue in full force and effect.\n\n"
            "18.2 Nevumo's failure to enforce any provision does not constitute a waiver of the right to enforce it in the future.\n\n"
            "18.3 These Provider Terms, together with the Privacy Policy, Cookie Policy, and the Price List (where applicable), constitute the entire agreement between you and Nevumo regarding your use of the Platform as a Provider.\n\n"
            "18.4 The authoritative language version of these Provider Terms for legal purposes is Polish for Providers based in Poland, and English for Providers in all other countries."
        ),
        "bg": (
            "1. Ако някоя разпоредба на настоящите Условия за Доставчици бъде обявена за невалидна или неприложима, останалите разпоредби продължават да действат в пълна сила.\n\n"
            "2. Неупражняването от страна на Nevumo на дадена разпоредба не представлява отказ от правото да я прилага в бъдеще.\n\n"
            "3. Настоящите Условия за Доставчици, заедно с Политиката за поверителност, Политиката за бисквитки и Ценоразписа (когато е приложимо), представляват цялостното споразумение между Доставчика и Nevumo по отношение на ползването на Платформата като Доставчик.\n\n"
            "4. Меродавната езикова версия на настоящите Условия за Доставчици за правни цели е полската за Доставчиците, установени в Полша, и английската за Доставчиците в останалите страни."
        ),
        "pl": (
            "1. Jeżeli jakiekolwiek postanowienie niniejszego Regulaminu Dostawców zostanie uznane za nieważne lub niewykonalne, pozostałe postanowienia pozostają w pełnej mocy.\n\n"
            "2. Zaniechanie przez Nevumo egzekwowania jakiegokolwiek postanowienia nie stanowi zrzeczenia się prawa do jego egzekwowania w przyszłości.\n\n"
            "3. Niniejszy Regulamin Dostawców, łącznie z Polityką Prywatności, Polityką Cookies i Cennikiem (jeżeli ma zastosowanie), stanowi całość porozumienia pomiędzy Dostawcą a Nevumo w zakresie korzystania z Platformy jako Dostawca.\n\n"
            "4. Wersją wiążącą prawnie niniejszego Regulaminu Dostawców dla Dostawców z siedzibą w Polsce jest wersja polska, a dla Dostawców we wszystkich pozostałych krajach - wersja angielska."
        ),
        "de": (
            "18.1 Sollte sich eine Bestimmung dieser Anbieterbedingungen als ungültig oder undurchsetzbar erweisen, bleiben die übrigen Bestimmungen vollumfänglich in Kraft und wirksam.\n\n"
            "18.2 Das Versäumnis von Nevumo, eine Bestimmung durchzusetzen, stellt keinen Verzicht auf das Recht dar, sie in Zukunft durchzusetzen.\n\n"
            "18.3 Diese Anbieterbedingungen, zusammen mit der Datenschutzrichtlinie, der Cookie-Richtlinie und der Preisliste (falls zutreffend), bilden die gesamte Vereinbarung zwischen Ihnen und Nevumo bezüglich Ihrer Nutzung der Plattform als Anbieter.\n\n"
            "18.4 Die maßgebliche Sprachversion dieser Anbieterbedingungen für rechtliche Zwecke ist Polnisch für Anbieter mit Sitz in Polen und Englisch für Anbieter in allen anderen Ländern."
        ),
        "fr": (
            "18.1 Si l'une des dispositions des présentes Conditions pour les Fournisseurs s'avère invalide ou inapplicable, les dispositions restantes continueront de s'appliquer pleinement.\n\n"
            "18.2 Le fait que Nevumo ne fasse pas appliquer une disposition ne constitue pas une renonciation au droit de la faire appliquer à l'avenir.\n\n"
            "18.3 Ces Conditions pour les Fournisseurs, ainsi que la Politique de confidentialité, la Politique en matière de cookies et la Liste de prix (le cas échéant), constituent l'intégralité de l'accord entre vous et Nevumo concernant votre utilisation de la Plateforme en tant que Fournisseur.\n\n"
            "18.4 La version linguistique faisant foi de ces Conditions pour les Fournisseurs à des fins juridiques est le polonais pour les Fournisseurs basés en Pologne, et l'anglais pour les Fournisseurs dans tous les autres pays."
        ),
        "es": (
            "18.1 Si alguna disposición de estas Condiciones para Proveedores resulta ser inválida o inaplicable, las disposiciones restantes continuarán en pleno vigor y efecto.\n\n"
            "18.2 El hecho de que Nevumo no haga cumplir alguna disposición no constituye una renuncia al derecho de hacerla cumplir en el futuro.\n\n"
            "18.3 Estas Condiciones para Proveedores, junto con la Política de Privacidad, la Política de Cookies y la Lista de Precios (donde corresponda), constituyen el acuerdo completo entre usted y Nevumo con respecto a su uso de la Plataforma como Proveedor.\n\n"
            "18.4 La versión en el idioma autoritativo de estas Condiciones para Proveedores para fines legales es el polaco para los Proveedores con sede en Polonia, y el inglés para los Proveedores en todos los demás países."
        ),
        "it": (
            "18.1 Qualora una qualsiasi disposizione delle presenti Condizioni per i Fornitori venga ritenuta non valida o inapplicabile, le restanti disposizioni continueranno ad avere pieno vigore ed efficacia.\n\n"
            "18.2 La mancata applicazione da parte di Nevumo di qualsiasi disposizione non costituisce una rinuncia al diritto di farla valere in futuro.\n\n"
            "18.3 Le presenti Condizioni per i Fornitori, insieme all'Informativa sulla privacy, alla Cookie Policy e al Listino prezzi (ove applicabile), costituiscono l'intero accordo tra te e Nevumo in merito all'uso della Piattaforma come Fornitore.\n\n"
            "18.4 La versione linguistica facente fede delle presenti Condizioni per i Fornitori a fini legali è il polacco per i Fornitori con sede in Polonia e l'inglese per i Fornitori in tutti gli altri paesi."
        ),
        "nl": (
            "18.1 Indien enige bepaling van deze Voorwaarden voor Dienstverleners ongeldig of niet-afdwingbaar blijkt te zijn, blijven de overige bepalingen volledig van kracht.\n\n"
            "18.2 Het nalaten van Nevumo om enige bepaling af te dwingen vormt geen afstand van het recht om deze in de toekomst af te dwingen.\n\n"
            "18.3 Deze Voorwaarden voor Dienstverleners vormen, samen met het Privacybeleid, het Cookiebeleid en de Prijslijst (indien van toepassing), de volledige overeenkomst tussen u en Nevumo met betrekking tot uw gebruik van het Platform als Dienstverlener.\n\n"
            "18.4 De bindende taalversie van deze Voorwaarden voor Dienstverleners voor juridische doeleinden is het Pools voor Dienstverleners gevestigd in Polen, en het Engels voor Dienstverleners in alle andere landen."
        ),
        "pt": (
            "18.1 Caso qualquer disposição destes Termos para Prestadores seja considerada inválida ou inexequível, as restantes disposições continuarão em pleno vigor e efeito.\n\n"
            "18.2 A não aplicação por parte da Nevumo de qualquer disposição não constitui uma renúncia ao direito de a aplicar no futuro.\n\n"
            "18.3 Estes Termos para Prestadores, juntamente com a Política de Privacidade, a Política de Cookies e o Preçário (onde aplicável), constituem o acordo integral entre o utilizador e a Nevumo no que diz respeito ao uso da Plataforma como Prestador.\n\n"
            "18.4 A versão linguística autoritária destes Termos para Prestadores para fins legais é o polaco para os Prestadores com sede na Polónia e o inglês para os Prestadores em todos os outros países."
        ),
        "pt-PT": (
            "18.1 Caso qualquer disposição destes Termos para Prestadores seja considerada inválida ou inexequível, as restantes disposições continuarão em pleno vigor e efeito.\n\n"
            "18.2 A não aplicação por parte da Nevumo de qualquer disposição não constitui uma renúncia ao direito de a aplicar no futuro.\n\n"
            "18.3 Estes Termos para Prestadores, juntamente com a Política de Privacidade, a Política de Cookies e o Preçário (onde aplicável), constituem o acordo integral entre o utilizador e a Nevumo no que diz respeito ao uso da Plataforma como Prestador.\n\n"
            "18.4 A versão linguística autoritária destes Termos para Prestadores para fins legais é o polaco para os Prestadores com sede na Polónia e o inglês para os Prestadores em todos os outros países."
        ),
        "ro": (
            "18.1 Dacă o prevedere a acestor Termeni pentru Furnizori se dovedește a fi invalidă sau inaplicabilă, prevederile rămase vor continua să fie pe deplin în vigoare și aplicabile.\n\n"
            "18.2 Neaplicarea de către Nevumo a unei dispoziții nu constituie o renunțare la dreptul de a o pune în aplicare pe viitor.\n\n"
            "18.3 Acești Termeni pentru Furnizori, împreună cu Politica de confidențialitate, Politica privind cookie-urile și Lista de prețuri (dacă este cazul), constituie întregul acord dintre dvs. și Nevumo în ceea ce privește utilizarea Platformei ca Furnizor.\n\n"
            "18.4 Versiunea lingvistică oficială a acestor Termeni pentru Furnizori din punct de vedere legal este poloneza pentru Furnizorii cu sediul în Polonia și engleza pentru Furnizorii din toate celelalte țări."
        ),
        "ru": (
            "18.1 Если какое-либо положение настоящих Условий для Поставщиков будет признано недействительным или не имеющим исковой силы, остальные положения останутся в полной силе и действии.\n\n"
            "18.2 Неприменение Nevumo какого-либо положения не означает отказа от права применять его в будущем.\n\n"
            "18.3 Настоящие Условия для Поставщиков вместе с Политикой конфиденциальности, Политикой использования файлов cookie и Прайс-листом (где это применимо) составляют полное соглашение между вами и Nevumo относительно использования вами Платформы в качестве Поставщика.\n\n"
            "18.4 Официальной языковой версией настоящих Условий для Поставщиков в юридических целях является польская для Поставщиков из Польши и английская для Поставщиков из всех остальных стран."
        ),
        "uk": (
            "18.1 Якщо будь-яке положення цих Умов для Постачальників буде визнано недійсним або таким, що не має позовної сили, решта положень залишаться в повній силі і дії.\n\n"
            "18.2 Незастосування Nevumo будь-якого положення не означає відмови від права застосовувати його в майбутньому.\n\n"
            "18.3 Ці Умови для Постачальників разом з Політикою конфіденційності, Політикою використання файлів cookie та Прайс-листом (де це застосовно) становлять повну угоду між вами і Nevumo щодо використання вами Платформи як Постачальника.\n\n"
            "18.4 Офіційною мовною версією цих Умов для Постачальників у юридичних цілях є польська для Постачальників з Польщі та англійська для Постачальників з усіх інших країн."
        ),
        "cs": (
            "18.1 Pokud bude některé ustanovení těchto podmínek pro poskytovatele shledáno neplatným nebo nevymahatelným, zbývající ustanovení zůstávají v plné platnosti a účinnosti.\n\n"
            "18.2 Skutečnost, že společnost Nevumo neuplatní jakékoli ustanovení, nepředstavuje vzdání se práva na jeho uplatnění v budoucnu.\n\n"
            "18.3 Tyto podmínky pro poskytovatele spolu se Zásadami ochrany osobních údajů, Zásadami používání souborů cookie a Ceníkem (pokud je to relevantní) tvoří celou smlouvu mezi vámi a společností Nevumo ohledně vašeho používání platformy jako poskytovatele.\n\n"
            "18.4 Autoritativní jazyková verze těchto podmínek pro poskytovatele pro právní účely je polština pro poskytovatele se sídlem v Polsku a angličtina pro poskytovatele ve všech ostatních zemích."
        ),
        "da": (
            "18.1 Hvis en bestemmelse i disse vilkår for udbydere findes ugyldig eller uden retskraft, skal de resterende bestemmelser fortsat være fuldt gyldige og have fuld retskraft.\n\n"
            "18.2 Nevumos manglende håndhævelse af en bestemmelse udgør ikke et afkald på retten til at håndhæve den i fremtiden.\n\n"
            "18.3 Disse vilkår for udbydere udgør sammen med privatlivspolitikken, cookiepolitikken og prislisten (hvor det er relevant) hele aftalen mellem dig og Nevumo vedrørende din brug af platformen som udbyder.\n\n"
            "18.4 Den autoritative sprogversion af disse vilkår for udbydere til juridiske formål er polsk for udbydere baseret i Polen og engelsk for udbydere i alle andre lande."
        ),
        "sv": (
            "18.1 Om någon bestämmelse i dessa villkor för leverantörer befinns vara ogiltig eller icke verkställbar, ska de återstående bestämmelserna fortsätta att gälla fullt ut.\n\n"
            "18.2 Nevumos underlåtenhet att upprätthålla en bestämmelse utgör inte ett avstående från rätten att upprätthålla den i framtiden.\n\n"
            "18.3 Dessa villkor för leverantörer, tillsammans med integritetspolicyn, cookiepolicyn och prislistan (i tillämpliga fall), utgör hela avtalet mellan dig och Nevumo angående din användning av plattformen som leverantör.\n\n"
            "18.4 Den auktoritativa språkversionen av dessa villkor för leverantörer för juridiska syften är polska för leverantörer baserade i Polen och engelska för leverantörer i alla andra länder."
        ),
        "no": (
            "18.1 Hvis en bestemmelse i disse vilkårene for leverandører finnes å være ugyldig eller ikke kan håndheves, skal de gjenværende bestemmelsene fortsette å gjelde fullt ut.\n\n"
            "18.2 Nevumos manglende håndhevelse av en bestemmelse utgjør ikke et frafall av retten til å håndheve den i fremtiden.\n\n"
            "18.3 Disse vilkårene for leverandører, sammen med personvernerklæringen, informasjonskapselerklæringen og prislisten (der det er aktuelt), utgjør hele avtalen mellom deg og Nevumo angående din bruk av plattformen som leverandør.\n\n"
            "18.4 Den autoritative språkversjonen av disse vilkårene for leverandører for juridiske formål er polsk for leverandører basert i Polen, og engelsk for leverandører i alle andre land."
        ),
        "fi": (
            "18.1 Jos jokin näiden palveluntarjoajien ehtojen määräys todetaan pätemättömäksi tai täytäntöönpanokelvottomaksi, muut määräykset pysyvät täysin voimassa.\n\n"
            "18.2 Se, että Nevumo ei pane täytäntöön jotakin määräystä, ei merkitse oikeudesta luopumista panna se täytäntöön tulevaisuudessa.\n\n"
            "18.3 Nämä palveluntarjoajien ehdot yhdessä tietosuojakäytännön, evästekäytännön ja hinnaston (tarvittaessa) kanssa muodostavat koko sopimuksen sinun ja Nevumon välillä koskien alustan käyttöäsi palveluntarjoajana.\n\n"
            "18.4 Näiden palveluntarjoajien ehtojen virallinen kieliversio oikeudellisiin tarkoituksiin on puola Puolassa sijaitseville palveluntarjoajille ja englanti kaikissa muissa maissa sijaitseville palveluntarjoajille."
        ),
        "et": (
            "18.1 Kui mõni nende teenusepakkujate tingimuste säte tunnistatakse kehtetuks või jõustamatuks, jäävad ülejäänud sätted täies ulatuses kehtima.\n\n"
            "18.2 Nevumo suutmatus mõnda sätet jõustada ei kujuta endast loobumist õigusest seda tulevikus jõustada.\n\n"
            "18.3 Need teenusepakkujate tingimused koos privaatsuspoliitika, küpsistepoliitika ja hinnakirjaga (vajaduse korral) moodustavad kogu lepingu teie ja Nevumo vahel seoses teie platvormi kasutamisega teenusepakkujana.\n\n"
            "18.4 Nende teenusepakkujate tingimuste autoriteetne keeleversioon juriidilistel eesmärkidel on Poolas asuvatele teenusepakkujatele poola keel ja kõigi teiste riikide teenusepakkujatele inglise keel."
        ),
        "lt": (
            "18.1 Jei kuri nors šių Paslaugų teikėjų sąlygų nuostata bus pripažinta negaliojančia ar neįgyvendinama, likusios nuostatos toliau galios ir veiks visa apimtimi.\n\n"
            "18.2 Tai, kad „Nevumo“ neįgyvendina kokios nors nuostatos, nereiškia, kad atsisakoma teisės jos reikalauti ateityje.\n\n"
            "18.3 Šios Paslaugų teikėjų sąlygos, kartu su privatumo politika, slapukų politika ir kainoraščiu (jei taikoma), sudaro visą sutartį tarp jūsų ir „Nevumo“ dėl platformos naudojimo kaip paslaugų teikėjui.\n\n"
            "18.4 Autoritetinga šių Paslaugų teikėjų sąlygų kalbos versija teisiniais tikslais yra lenkų kalba Lenkijoje įsisteigusiems paslaugų teikėjams ir anglų kalba paslaugų teikėjams visose kitose šalyse."
        ),
        "lv": (
            "18.1 Ja kāds no šiem Pakalpojumu sniedzēju noteikumiem tiek atzīts par nederīgu vai neizpildāmu, atlikušie noteikumi turpina būt pilnībā spēkā esoši.\n\n"
            "18.2 Nevumo nespēja izpildīt kādu no noteikumiem nenozīmē atteikšanos no tiesībām to izpildīt nākotnē.\n\n"
            "18.3 Šie Pakalpojumu sniedzēju noteikumi kopā ar Konfidencialitātes politiku, Sīkfailu politiku un Cenrādi (ja piemērojams) veido visu vienošanos starp jums un Nevumo par jūsu Platformas izmantošanu kā Pakalpojumu sniedzējam.\n\n"
            "18.4 Šo Pakalpojumu sniedzēju noteikumu autoritatīvā valodas versija juridiskiem mērķiem ir poļu valoda Pakalpojumu sniedzējiem, kas atrodas Polijā, un angļu valoda Pakalpojumu sniedzējiem visās citās valstīs."
        ),
        "hu": (
            "18.1 Ha a jelen Szolgáltatói Feltételek bármely rendelkezése érvénytelennek vagy végrehajthatatlannak bizonyul, a fennmaradó rendelkezések továbbra is teljes mértékben hatályosak maradnak.\n\n"
            "18.2 Ha a Nevumo nem hajt végre valamilyen rendelkezést, az nem jelenti a jövőbeli végrehajtáshoz való jogról való lemondást.\n\n"
            "18.3 Jelen Szolgáltatói Feltételek az Adatvédelmi irányelvvel, a Cookie-szabályzattal és az Árlistával (adott esetben) együtt alkotják a teljes megállapodást Ön és a Nevumo között a Platform Szolgáltatóként történő használatára vonatkozóan.\n\n"
            "18.4 A jelen Szolgáltatói Feltételek jogi szempontból irányadó nyelvi verziója Lengyelországban székhellyel rendelkező Szolgáltatók esetében a lengyel, minden más országban lévő Szolgáltató esetében pedig az angol."
        ),
        "hr": (
            "18.1 Ako se bilo koja odredba ovih Uvjeta za pružatelje usluga proglasi nevažećom ili neprovedivom, preostale odredbe i dalje će biti na snazi i u potpunosti važeće.\n\n"
            "18.2 Ako Nevumo ne provede neku odredbu, to ne predstavlja odricanje od prava da je provede u budućnosti.\n\n"
            "18.3 Ovi Uvjeti za pružatelje usluga, zajedno s Politikom privatnosti, Politikom kolačića i Cjenikom (gdje je primjenjivo), čine cjelokupni ugovor između vas i tvrtke Nevumo u pogledu vaše upotrebe Platforme kao Pružatelja usluga.\n\n"
            "18.4 Mjerodavna jezična verzija ovih Uvjeta za pružatelje usluga u pravne svrhe je poljska za Pružatelje usluga sa sjedištem u Poljskoj i engleska za Pružatelje usluga u svim drugim zemljama."
        ),
        "sk": (
            "18.1 Ak sa niektoré ustanovenie týchto podmienok pre poskytovateľov bude považovať za neplatné alebo nevymožiteľné, zostávajúce ustanovenia zostávajú v plnej platnosti a účinnosti.\n\n"
            "18.2 Skutočnosť, že spoločnosť Nevumo neuplatní akékoľvek ustanovenie, nepredstavuje vzdanie sa práva na jeho uplatnenie v budúcnosti.\n\n"
            "18.3 Tieto podmienky pre poskytovateľov spolu so Zásadami ochrany osobných údajov, Zásadami používania súborov cookie a Cenníkom (ak je to relevantné) tvoria celú zmluvu medzi vami a spoločnosťou Nevumo týkajúcu sa vášho používania platformy ako poskytovateľa.\n\n"
            "18.4 Autoritárna jazyková verzia týchto podmienok pre poskytovateľov na právne účely je poľština pre poskytovateľov so sídlom v Poľsku a angličtina pre poskytovateľov vo všetkých ostatných krajinách."
        ),
        "sl": (
            "18.1 Če je katera koli določba teh pogojev za ponudnike neveljavna ali neizvršljiva, ostale določbe ostanejo v celoti veljavne in učinkovite.\n\n"
            "18.2 Če Nevumo ne uveljavi katere koli določbe, to ne pomeni, da se odreka pravici do njene uveljavitve v prihodnosti.\n\n"
            "18.3 Ti pogoji za ponudnike skupaj s Pravilnikom o zasebnosti, Pravilnikom o piškotkih in Cenikom (kjer je to primerno) tvorijo celotno pogodbo med vami in podjetjem Nevumo glede vaše uporabe platforme kot ponudnika.\n\n"
            "18.4 Verodostojna jezikovna različica teh pogojev za ponudnike v pravne namene je poljska za ponudnike s sedežem na Poljskem in angleška za ponudnike v vseh drugih državah."
        ),
        "el": (
            "18.1 Εάν οποιαδήποτε διάταξη αυτών των Όρων Παρόχου κριθεί άκυρη ή μη εκτελεστή, οι υπόλοιπες διατάξεις θα συνεχίσουν να ισχύουν πλήρως.\n\n"
            "18.2 Η παράλειψη της Nevumo να επιβάλει οποιαδήποτε διάταξη δεν αποτελεί παραίτηση από το δικαίωμα επιβολής της στο μέλλον.\n\n"
            "18.3 Αυτοί οι Όροι Παρόχου, μαζί με την Πολιτική Απορρήτου, την Πολιτική Cookies και τον Τιμοκατάλογο (όπου ισχύει), αποτελούν τη συνολική συμφωνία μεταξύ εσάς και της Nevumo σχετικά με τη χρήση της Πλατφόρμας από εσάς ως Πάροχος.\n\n"
            "18.4 Η αυθεντική γλωσσική έκδοση αυτών των Όρων Παρόχου για νομικούς σκοπούς είναι τα Πολωνικά για Παρόχους με έδρα την Πολωνία και τα Αγγλικά για Παρόχους σε όλες τις άλλες χώρες."
        ),
        "tr": (
            "18.1 Bu Sağlayıcı Şartlarının herhangi bir hükmünün geçersiz veya uygulanamaz olduğu tespit edilirse, kalan hükümler tam olarak yürürlükte kalmaya devam edecektir.\n\n"
            "18.2 Nevumo'nun herhangi bir hükmü uygulamaması, gelecekte bunu uygulama hakkından feragat ettiği anlamına gelmez.\n\n"
            "18.3 Bu Sağlayıcı Şartları, Gizlilik Politikası, Çerez Politikası ve Fiyat Listesi (varsa) ile birlikte, Platformu bir Sağlayıcı olarak kullanımınızla ilgili olarak sizinle Nevumo arasındaki sözleşmenin tamamını oluşturur.\n\n"
            "18.4 Hukuki amaçlar için bu Sağlayıcı Şartlarının geçerli dil sürümü, Polonya merkezli Sağlayıcılar için Lehçe ve diğer tüm ülkelerdeki Sağlayıcılar için İngilizcedir."
        ),
        "ga": (
            "18.1 Má mheastar go bhfuil aon fhoráil de na Téarmaí Soláthraí seo neamhbhailí nó neamhfhorfheidhmithe, leanfaidh na forálacha eile i bhfeidhm agus in éifeacht go hiomlán.\n\n"
            "18.2 Ní chiallaíonn mainneachtain Nevumo aon fhoráil a fhorfheidhmiú go dtarscaoiltear an ceart chun í a fhorfheidhmiú sa todhchaí.\n\n"
            "18.3 Is iad na Téarmaí Soláthraí seo, mar aon leis an mBeartas Príobháideachais, Beartas Fianán, agus an Liosta Praghsanna (nuair is infheidhme), an comhaontú iomlán idir tú féin agus Nevumo maidir le húsáid an Ardáin mar Sholáthraí.\n\n"
            "18.4 Is é an leagan teanga údarásach de na Téarmaí Soláthraí seo chun críocha dlíthiúla ná Polainnis do Sholáthraithe atá bunaithe sa Pholainn, agus Béarla do Sholáthraithe i ngach tír eile."
        ),
        "is": (
            "18.1 Ef eitthvert ákvæði þessara skilmála fyrir þjónustuveitendur reynist ógilt eða óframkvæmanlegt, skulu eftirstandandi ákvæði halda fullu gildi og áhrifum.\n\n"
            "18.2 Þótt Nevumo mistakist að framfylgja einhverju ákvæði, þá felur það ekki í sér afsal á réttinum til að framfylgja því í framtíðinni.\n\n"
            "18.3 Þessir skilmálar fyrir þjónustuveitendur, ásamt persónuverndarstefnunni, vafrakökustefnunni og verðskránni (þar sem við á), mynda allan samninginn milli þín og Nevumo varðandi notkun þína á vettvangnum sem þjónustuveitandi.\n\n"
            "18.4 Gildandi tungumálaútgáfa þessara skilmála fyrir þjónustuveitendur í lagalegum tilgangi er pólska fyrir þjónustuveitendur með aðsetur í Póllandi, og enska fyrir þjónustuveitendur í öllum öðrum löndum."
        ),
        "lb": (
            "18.1 Wann eng Bestëmmung vun dësen Ubidderbedéngungen als ongëlteg oder net ëmsetzbar fonnt gëtt, bleiwen déi verbleiwen Bestëmmunge voll a Kraaft an effektiv.\n\n"
            "18.2 D'Net-Ëmsetze vum Nevumo vun enger Bestëmmung ass keng Verzichterklärung vum Recht, se an Zukunft ëmzesetzen.\n\n"
            "18.3 Dës Ubidderbedéngungen, zesumme mat der Dateschutzrichtlinn, der Cookie-Richtlinn an der Präislëscht (wou applicabel), bilden déi ganz Ofkommes tëscht Iech an Nevumo betreffend Är Notzung vun der Plattform als Ubidder.\n\n"
            "18.4 Déi autoritär Versioun vun dësen Ubidderbedéngunge fir juristesch Zwecker ass Polnesch fir Ubidder mat Sëtz a Polen, an Englesch fir Ubidder an allen anere Länner."
        ),
        "mk": (
            "18.1 Ако некоја одредба од овие Услови за Даватели се утврди дека е неважечка или неприменлива, преостанатите одредби ќе продолжат да бидат во целосна сила и дејство.\n\n"
            "18.2 Неизвршувањето на која било одредба од страна на Nevumo не претставува одрекување од правото таа да се спроведува во иднина.\n\n"
            "18.3 Овие Услови за Даватели, заедно со Политиката за приватност, Политиката за колачиња и Ценовникот (каде што е применливо), го сочинуваат целиот договор помеѓу вас и Nevumo во врска со вашата употреба на Платформата како Давател.\n\n"
            "18.4 Меродавната јазична верзија на овие Услови за Даватели за правни цели е полската за Даватели со седиште во Полска и англиската за Даватели во сите други земји."
        ),
        "mt": (
            "18.1 Jekk kwalunkwe dispożizzjoni ta' dawn it-Termini għall-Fornituri tinstab li hija invalida jew mhux infurzabbli, id-dispożizzjonijiet li jifdal għandhom ikomplu jkunu fis-seħħ u jkollhom effett sħiħ.\n\n"
            "18.2 In-nuqqas ta' Nevumo li jinforza kwalunkwe dispożizzjoni ma jikkostitwixxix rinunzja għad-dritt li jinforzaha fil-futur.\n\n"
            "18.3 Dawn it-Termini għall-Fornituri, flimkien mal-Politika tal-Privatezza, il-Politika dwar il-Cookies, u l-Lista tal-Prezzijiet (fejn applikabbli), jikkostitwixxu l-ftehim sħiħ bejnek u Nevumo dwar l-użu tiegħek tal-Pjattaforma bħala Fornitur.\n\n"
            "18.4 Il-verżjoni lingwistika awtorevoli ta' dawn it-Termini għall-Fornituri għal skopijiet legali hija l-Pollakk għal Fornituri bbażati fil-Polonja, u l-Ingliż għal Fornituri fil-pajjiżi l-oħra kollha."
        ),
        "sq": (
            "18.1 Nëse ndonjë dispozitë e këtyre Kushteve për Ofruesit konsiderohet e pavlefshme ose e pazbatueshme, dispozitat e mbetura do të vazhdojnë të jenë në fuqi dhe veprim të plotë.\n\n"
            "18.2 Dështimi i Nevumo për të zbatuar ndonjë dispozitë nuk përbën një heqje dorë nga e drejta për ta zbatuar atë në të ardhmen.\n\n"
            "18.3 Këto Kushte për Ofruesit, së bashku me Politikën e Privatësisë, Politikën e Cookies dhe Listën e Çmimeve (ku zbatohet), përbëjnë të gjithë marrëveshjen midis jush dhe Nevumo në lidhje me përdorimin tuaj të Platformës si Ofrues.\n\n"
            "18.4 Versioni gjuhësor autoritar i këtyre Kushteve për Ofruesit për qëllime ligjore është polonisht për Ofruesit me bazë në Poloni dhe anglisht për Ofruesit në të gjitha vendet e tjera."
        ),
        "sr": (
            "18.1 Ako se za bilo koju odredbu ovih Uslova za pružaoce usluga utvrdi da je nevažeća ili neprimenljiva, preostale odredbe će i dalje ostati na snazi i u potpunosti važeće.\n\n"
            "18.2 Ako Nevumo ne sprovede neku odredbu, to ne predstavlja odricanje od prava da je sprovede u budućnosti.\n\n"
            "18.3 Ovi Uslovi za pružaoce usluga, zajedno sa Politikom privatnosti, Politikom kolačića i Cenovnikom (gde je primenljivo), čine celokupan ugovor između vas i kompanije Nevumo u vezi sa vašim korišćenjem Platforme kao Pružaoca usluga.\n\n"
            "18.4 Merodavna jezička verzija ovih Uslova za pružaoce usluga u pravne svrhe je poljska za Pružaoce usluga sa sedištem u Poljskoj, a engleska za Pružaoce usluga u svim ostalim zemljama."
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
        print(f"✅ Seeded {count} translations for {NAMESPACE}.art17_body and {NAMESPACE}.art18_body")

if __name__ == "__main__":
    seed()
