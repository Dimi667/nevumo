# -*- coding: utf-8 -*-
"""
seed_cookies_p13.py — namespace 'cookies'
cookies.s4_text, cookies.s5_title, cookies.s5_col_name,
cookies.s5_col_type, cookies.s5_col_purpose
Run: docker exec nevumo-api python -m apps.api.scripts.seed_cookies_p13
"""

import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)

TRANSLATIONS = {
    "cookies.s4_text": {
        "en": "When you provide a phone number on the platform (e.g., when submitting a service request), we temporarily store it in your browser's local storage under the key nevumo_phone. This enables autofill on subsequent visits so you do not have to type it again. Legal basis: Art. 6(1)(f) GDPR - legitimate interest in reducing friction and improving user experience. This data never leaves your device unless you explicitly submit a form. You can delete it at any time by clearing your browser's local storage or via your account settings.",
        "bg": "Kogato predostavite telefonen nomer na platformata (napr. pri izprashtane na zapitane za usluga), go sukhranjavame vremenno v lokalnoto khranilishte na brauzara vi pod klyuch nevumo_phone. Tova pozvolyava avtomatichnoto populvane pri sledvashti poseshtenia. Pravno osnovanie: Chl. 6, al. 1, b. e) GDPR - legitimen interes za namalyavane na zatrudneniya i podobryavane na potrebitelskoto izzhivyavane. Tezi danni nikoga ne napuskat vashe ustroystvo, osven ako izrichno ne izpratite formular. Mozhete da gi iztriete po vsyako vreme, kato izchistitе local storage na brauzara ili chrez nastroykite na profila.",
        "cs": "Kdyz na platforme zadite telefonni cislo (napr. pri odesilani zadosti o sluzbu), docasne jej ulozime do lokalniho uloziste vasaho prohlizece pod klicem nevumo_phone. To umoznuje automaticke vyplneni pri dalsich navstevach. Pravni zaklad: Cl. 6(1)(f) GDPR - opravneny zajem na snizeni zateze a zlepseni uzivatelského zazitku. Tato data nikdy neopusti vase zarizeni, pokud vyslovne neodeslete formular. Kdykoliv je muzete smazat vymazanim lokalniho uloziste prohlizece nebo v nastaveni uctu.",
        "da": "Nar du angiver et telefonnummer pa platformen (f.eks. ved indsendelse af en serviceanmodning), gemmer vi det midlertidigt i din browsers lokale lagring under noglen nevumo_phone. Dette muliggor automatisk udfyldelse ved efterfolgende besog. Retsgrundlag: Art. 6(1)(f) GDPR - legitim interesse i at reducere friktion og forbedre brugeroplevelsen. Disse data forlader aldrig din enhed, medmindre du eksplicit indsender en formular. Du kan slette dem til enhver tid ved at rydde din browsers lokale lagring eller via dine kontoindstillinger.",
        "de": "Wenn Sie auf der Plattform eine Telefonnummer angeben (z. B. beim Einreichen einer Serviceanfrage), speichern wir diese vorubergehend im lokalen Speicher Ihres Browsers unter dem Schlussel nevumo_phone. Dies ermoglicht die automatische Vorausfullung bei spateren Besuchen. Rechtsgrundlage: Art. 6(1)(f) DSGVO - berechtigtes Interesse an der Reduzierung von Reibung und der Verbesserung der Nutzererfahrung. Diese Daten verlassen Ihr Gerat nie, es sei denn, Sie senden explizit ein Formular ab. Sie konnen sie jederzeit loschen, indem Sie den lokalen Speicher Ihres Browsers leeren oder uber Ihre Kontoeinstellungen.",
        "el": "Otan parechete arithmo tilefono stin platforma (p.ch. kata tin ypovolh aitimatos ypiresias), to apothikeyoume prosorino stin topiki apothikeysis toy progrmmatos perigisis sas ypo to kleidi nevumo_phone. Ayto epitrepei tin automatiki symplirosi se epomenes episkepseis. Nomiki vasi: Arthro 6(1)(f) GDPR - ennomo symferon gia meiwsi trivias kai beltiwsi empeirias christi. Ayta ta dedomena den afinos pote ti syskeyi sas ektos an ypovaleite rofita mia forma. Boreite na ta diagrapsete opoiadipote stigmi katharizontas tin topiki apothikeysis toy progrmmatos perigisis i meso twn rythmiseon logariasmou.",
        "es": "Cuando proporciona un numero de telefono en la plataforma (p. ej., al enviar una solicitud de servicio), lo almacenamos temporalmente en el almacenamiento local de su navegador bajo la clave nevumo_phone. Esto permite el autocompletado en visitas posteriores. Base juridica: Art. 6(1)(f) RGPD - interes legitimo en reducir la friccion y mejorar la experiencia del usuario. Estos datos nunca abandonan su dispositivo a menos que envie explicitamente un formulario. Puede eliminarlos en cualquier momento borrando el almacenamiento local de su navegador o a traves de la configuracion de su cuenta.",
        "et": "Kui esitate platvormil telefoninumbri (nt teenusepäringu esitamisel), salvestame selle ajutiselt oma brauseri kohalikku salvestusruumi voti nevumo_phone alla. See voimaldab automaatset taitamist jargnervatel kulastatustel. Oiguslik alus: Art. 6(1)(f) GDPR - oigustatud huvi hookdumise vahendamise ja kasutajakogemuse parandamise vastu. Need andmed ei lahku kunagi teie seadmest, valja arvatud juhul, kui esitate vormi selgesõnaliselt. Saate need igal ajal kustutada, tuhjendades oma brauseri kohaliku salvestusruumi voi oma konto seadete kaudu.",
        "fi": "Kun annat puhelinnumeron alustalla (esim. palvelupyyntoa lahettaessasi), tallennamme sen valiaikaisesti selaimesi paikalliseen tallennustilaan avaimen nevumo_phone alle. Tama mahdollistaa automaattisen tayyton tulevilla vierailuilla. Oikeusperuste: Art. 6(1)(f) GDPR - oikeutettu etu kitkan vahentamisessa ja kayttajakokemuksen parantamisessa. Nama tiedot eivat koskaan poistu laitteeltasi, ellei sina nimenomaisesti laheta lomaketta. Voit poistaa ne milloin tahansa tyhjentamalla selaimesi paikallisen tallennustilan tai tilin asetusten kautta.",
        "fr": "Lorsque vous fournissez un numero de telephone sur la plateforme (p. ex. lors de la soumission d'une demande de service), nous le stockons temporairement dans le stockage local de votre navigateur sous la cle nevumo_phone. Cela permet le remplissage automatique lors des visites suivantes. Base juridique : Art. 6(1)(f) RGPD - interet legitime a reduire les frictions et a ameliorer l'experience utilisateur. Ces donnees ne quittent jamais votre appareil sauf si vous soumettez explicitement un formulaire. Vous pouvez les supprimer a tout moment en effacant le stockage local de votre navigateur ou via les parametres de votre compte.",
        "ga": "Nuair a sholathraonn tu uimhir ghuthain ar an ardan (m.sh. agus iarratas seirbhise a chur isteach), storeailimid go sealadach e i storailt aitiuil do bhrabhsalai faoin eochair nevumo_phone. Cumasaionn se seo uathlionadh ar chuairteanna ina dhiaidh sin. Banus dlí: Alt 6(1)(f) GDPR - leas dlisteanach in fhrithchuimilt a laghdú agus an eispeireas usaideora a fheabhsu. Ni fhagann na sonrai seo do ghlear riamh ach amhain ma chuireann tu foirm isteach go sainraite. Is feidir leat iad a scriosadh am ar bith tri storailt aitiuil do bhrabhsalai a ghlanadh no tri shocruithe do chuntais.",
        "hr": "Kada navedete telefonski broj na platformi (npr. pri slanju zahtjeva za uslugom), privremeno ga pohranjujemo u lokalnu pohranu vaseg preglednika pod kljucem nevumo_phone. To omogucuje automatsko popunjavanje pri naknadnim posjetima. Pravna osnova: cl. 6(1)(f) GDPR - legitimni interes za smanjenje trenja i poboljsanje korisnickog iskustva. Ovi podaci nikad ne napustaju vase uredaj osim ako izricito ne podnesete obrazac. Mozete ih obrisati u bilo koje vrijeme brisanjem lokalne pohrane preglednika ili putem postavki racuna.",
        "hu": "Amikor telefonszamot ad meg a platformon (pl. szolgaltatasi kerelem benyujtasakor), ideiglenesen taroljuk azt a bongeszo helyi tarhelyn a nevumo_phone kulcs alatt. Ez lehetove teszi az automatikus kitoltest a kovetkezo latogatasokon. Jogalap: 6. cikk (1) bek. f) pont GDPR - jogos erdek a surlodas csokkentese es a felhasznaloi elmeny javitasa erdekeben. Ezek az adatok soha nem hagyja el az eszkozt, kiveve, ha kifejezetten benyujt egy urlapot. Barmikor torolheti azokat a bongeszo helyi tarhelyn torlesen vagy a fiokbeallitasok segitsegevel.",
        "is": "Thegar thu gefur upp simanumer a gattinni (t.d. thegar thjonustubeidni er send), geymsum vid thad timabundid i stadbundinni geymslu vafrans thins undir lykilnum nevumo_phone. Thetta gerir kleift ad sjálfvirkt fylla ut vid sidari heimsoknir. Lagagrundvollur: Gr. 6(1)(f) GDPR - logmaetir hagsmunir af thu ad draga ur niningi og baeta notendaupplifun. Thessi gogn fara aldrei fra taekinu thinu nema thu sendirdu form serstakliga. Thu getur eytt theim hvenær sem er med thy ad hreinsa stadbundna geymslu vafrans thins egir gegnum reikningsstillingar.",
        "it": "Quando fornisci un numero di telefono sulla piattaforma (es. inviando una richiesta di servizio), lo memorizziamo temporaneamente nel local storage del tuo browser sotto la chiave nevumo_phone. Questo consente la compilazione automatica nelle visite successive. Base giuridica: Art. 6(1)(f) GDPR - interesse legittimo a ridurre le frizioni e migliorare l'esperienza utente. Questi dati non lasciano mai il tuo dispositivo a meno che tu non invii esplicitamente un modulo. Puoi eliminarli in qualsiasi momento cancellando il local storage del browser o tramite le impostazioni dell'account.",
        "lb": "Wann Dir eng Telefonnummer op der Plattform ugett (z.B. beim Abschicken vun enger Serviceanfroe), speichert mir se temporar am lokale Speicher vun Aerem Browser ennert dem Schlussel nevumo_phone. Des erlaabt d'Autofill bei nofolgende Besooche. Rechtlech Basis: Art. 6(1)(f) DSGVO - berechtigten Interesse fir d'Reibung ze reduzieren an d'Nutzererfahrung ze verbesseren. Des Donneen verloossen Aeren Apparat ni, ausser Dir schickt explizit e Formulaire of. Dir kennt se jederzeit laschen, andeems Dir de lokale Speicher vum Browser leert oder iwwert d'Kontoastellungen.",
        "lt": "Kai platformoje pateikiate telefono numeri (pvz. teikiant paslaugos uzklausu), laikinai ji saugome jusu narskykles vietineje saugykloje pagal rakta nevumo_phone. Tai leidzia automatiskai uzpildyti per tolesnius apsilankymus. Teisinis pagrindas: BDAR 6 str. 1 d. f p. - teisetas interesas sumazinti trinti ir pagerinti naudotojo patirtí. Sie duomenys niekada nepalieka jusu irenginio, nebent aiSkiai pateikiate forma. Galite juos istrinti bet kada isvaldydami narsykles vietine saugykla arba per paskyros nustatymus.",
        "lv": "Kad platformā noradat talruna numuru (piem. iesniedzot pakalpojuma pieprasijumu), mes to islaicigi saglabajam jusu perlukprogrammas lokalaja krātuve zem atslēgas nevumo_phone. Tas lauj automatiski aizpildit turpmākajos apmeklejumos. Juridiskais pamats: VDAR 6. panta 1. punkta f) apaksunkts - legitimas intereses berzes samazinasana un lietotaja pieredzes uzlabosana. Sie dati nekad neatstaj jusu ierici, ja vien jus neparprotami neiesniedzat veidlapu. Jus varat tos izdzt jebkura laika, notirot parlukprogrammas lokalo kratuvi vai izmantojot konta iestatijumus.",
        "mk": "Koga davate telefonnski broj na platformata (na pr. pri podnesuvanje baranje za usluga), privremeno go zachuvuvame vo lokalnoto skladiranje na vasiot prelistuvac pod kljucot nevumo_phone. Ova ovozmuzhuvа avtomatsko popolnuvanje pri slednite poseti. Pravna osnova: chl. 6(1)(e) GDPR - legitimen interes za namaluvanje na frikcijata i podobruvanje na korisnickata iskustvo. Ovie podatoci nikogash ne gi napustaat vasiot ured osven ako izrichno ne podnesete formular. Mozete da gi izbrisete vo sekoe vreme so chishtewe na lokalnoto skladiranje na prelistuvacot ili preku postavkite na profilot.",
        "mt": "Meta tipprovdi numru ta' telefon fuq il-pjattaforma (ez. meta tibghat talba ghal servizz), nahznuh temporanjament fil-hazna lokali tal-browser tieghek taht ic-cavetta nevumo_phone. Dan jippermetti l-mili awtomatiku f'zjarat sussegwenti. Bazi legali: Art. 6(1)(f) GDPR - interess legitimu fit-tnaqqis tal-frizzjoni u t-titjib tal-esperjenza tal-utent. Dawn id-data qatt ma jitilqu mill-apparat tieghek sakemm ma tibghats formola espliċitament. Tista' thassarhom fi kwalunkwe hin billi tnehhи l-hazna lokali tal-browser jew permezz tas-settings tal-kont.",
        "nl": "Wanneer u een telefoonnummer op het platform opgeeft (bijv. bij het indienen van een serviceverzoek), slaan we het tijdelijk op in de lokale opslag van uw browser onder de sleutel nevumo_phone. Dit maakt automatisch invullen bij volgende bezoeken mogelijk. Rechtsgrondslag: Art. 6(1)(f) AVG - gerechtvaardigd belang bij het verminderen van wrijving en het verbeteren van de gebruikerservaring. Deze gegevens verlaten uw apparaat nooit tenzij u expliciet een formulier indient. U kunt ze op elk gewenst moment verwijderen door de lokale opslag van uw browser te wissen of via uw accountinstellingen.",
        "no": "Nar du oppgir et telefonnummer pa plattformen (f.eks. ved innsending av en tjenestebespørsel), lagrer vi det midlertidig i nettleserens lokale lagring under nøkkelen nevumo_phone. Dette muliggjar automatisk utfylling ved påfolgende besok. Rettsgrunnlag: Art. 6(1)(f) GDPR - berettiget interesse i a reducere friksjon og forbedre brukeropplevelsen. Disse dataene forlater aldri enheten din med mindre du eksplisitt sender inn et skjema. Du kan slette dem nar som helst ved a tomme nettleserens lokale lagring eller via kontoinnstillingene.",
        "pl": "Gdy podajesz numer telefonu na platformie (np. przy skladaniu wniosku o usluge), tymczasowo przechowujemy go w lokalnej pamieci Twojej przegladarki pod kluczem nevumo_phone. Umozliwia to autouzupelnianie przy kolejnych wizytach. Podstawa prawna: Art. 6(1)(f) RODO - uzasadniony interes w zmniejszeniu tarcia i poprawie doswiadczenia uzytkownika. Te dane nigdy nie opuszczaja Twojego urzadzenia, chyba ze jawnie wyslесz formularz. Mozesz je usunac w dowolnym momencie, czyszczac lokalna pamiec przegladarki lub poprzez ustawienia konta.",
        "pt": "Quando voce fornece um numero de telefone na plataforma (ex. ao enviar uma solicitacao de servico), o armazenamos temporariamente no armazenamento local do seu navegador sob a chave nevumo_phone. Isso permite o preenchimento automatico em visitas subsequentes. Base juridica: Art. 6(1)(f) RGPD - interesse legitimo em reduzir o atrito e melhorar a experiencia do usuario. Esses dados nunca saem do seu dispositivo a menos que voce envie explicitamente um formulario. Voce pode excluí-los a qualquer momento limpando o armazenamento local do navegador ou nas configuracoes da conta.",
        "pt-PT": "Quando fornece um numero de telefone na plataforma (ex. ao submeter um pedido de servico), armazenamo-lo temporariamente no armazenamento local do seu navegador sob a chave nevumo_phone. Isso permite o preenchimento automatico em visitas subsequentes. Base juridica: Art. 6(1)(f) RGPD - interesse legitimo na reducao do atrito e melhoria da experiencia do utilizador. Estes dados nunca saem do seu dispositivo a nao ser que submeta um formulario explicitamente. Pode eliminá-los a qualquer momento limpando o armazenamento local do navegador ou atraves das definicoes da conta.",
        "ro": "Cand furnizati un numar de telefon pe platforma (de ex. la trimiterea unei cereri de serviciu), il stocam temporar in memoria locala a browserului dvs. sub cheia nevumo_phone. Aceasta permite completarea automata la vizitele ulterioare. Temei juridic: Art. 6(1)(f) GDPR - interes legitim in reducerea fricatiunii si imbunatatirea experientei utilizatorului. Aceste date nu parasesc niciodata dispozitivul dvs. daca nu trimiteti in mod explicit un formular. Le puteti sterge oricand stergand memoria locala a browserului sau prin setarile contului.",
        "ru": "Kogda vy ukazyvaete nomer telefona na platforme (napr. pri otpravke zayavki na uslugu), my vremenno sokhranjaem ego v lokal'nom khranilishche vashego brauzera pod klyuchom nevumo_phone. Eto pozvolyaet avtomaticheski zapolnyat' ego pri posleduyushchikh poseshcheniyakh. Pravovaya osnova: St. 6(1)(f) GDPR - zakonnyy interes v sokrashchenii neudobstv i uluchshenii pol'zovatel'skogo opyta. Eti dannye nikogda ne pokidayut vashe ustroystvo, esli vy yavno ne otpravite formu. Vy mozhete udalit' ikh v lyuboye vremya, ochistiv lokal'noye khranilishche brauzera ili cherez nastroyki akkaunta.",
        "sk": "Ked na platforme zadate telefonné cislo (napr. pri odosielani ziadosti o sluzbu), docasne ho ulozime do lokalneho uloziska vasho prehliadaca pod klucom nevumo_phone. To umoznuje automaticke vyplnenie pri dalsich navstevach. Pravny zaklad: Cl. 6(1)(f) GDPR - opravneny zaujem na znizeni zataze a zlepseni pouzivatelského zazitku. Tieto data nikdy neopustia vase zariadenie, pokial vyslovne neodoslete formular. Kedykolvek ich mozete odstranit vymazanim lokalneho uloziska prehliadaca alebo v nastaveniach uctu.",
        "sl": "Ko na platformi navedete telefonsko stevilko (npr. pri oddaji prosnje za storitev), jo zacasno shranimo v lokalno shrambo vasega brskalnika pod kljucem nevumo_phone. To omogoca samodejno izpolnjevanje pri naslednjih obiskih. Pravna podlaga: cl. 6(1)(f) GDPR - zakoniti interes za zmanjsanje trenja in izboljsanje uporabniske izkusnje. Ti podatki nikoli ne zapustijo vase naprave, razen ce izrecno oddate obrazec. Kadarkoli jih lahko izbrisete s ciscenjem lokalne shrambe brskalnika ali prek nastavitev racuna.",
        "sq": "Kur jepni nje numer telefoni ne platforme (p.sh. kur dergoni nje kerkese sherbimi), e ruajme perkohesisht ne ruajtjen lokale te shfletuesit tuaj nen celsin nevumo_phone. Kjo mundeson plotesimin automatik ne vizitat pasuese. Baza ligjore: Neni 6(1)(f) GDPR - interes legjitim ne uljen e ferkimit dhe permiresimin e pervojes se perdoruesit. Keto te dhena nuk e lene kurre pajisjen tuaj nese nuk dorezoni nje formular ne menyre eksplicite. Mund ti fshini ne cdo kohe duke pastruar ruajtjen lokale te shfletuesit ose permes cilesimeve te llogarise.",
        "sr": "Kada navedete telefonski broj na platformi (npr. pri slanju zahteva za uslugom), privremeno ga cuvamo u lokalnom skladistu vaseg pregledaca pod kljucem nevumo_phone. Ovo omogucava automatsko popunjavanje pri narednim posetama. Pravni osnov: cl. 6(1)(e) GDPR - legitimni interes u smanjenju trenja i poboljsanju korisnickog iskustva. Ovi podaci nikada ne napustaju vase uredaj osim ako izricito ne podnesete obrazac. Mozete ih izbrisati u svako doba brisanjem lokalnog skladista pregledaca ili preko postavki naloga.",
        "sv": "Nar du anger ett telefonnummer pa plattformen (t.ex. vid inlamning av en serviceforfragan) lagrar vi det tillfalligt i webbläsarens lokala lagring under nyckeln nevumo_phone. Detta mojliggor automatisk ifyllning vid efterfoljande besok. Rättslig grund: Art. 6(1)(f) GDPR - berättigat intresse av att minska friktion och forbattra anvandarupplevelsen. Dessa uppgifter lämnar aldrig din enhet om du inte uttryckligen skickar in ett formulär. Du kan radera dem nar som helst genom att rensa webbläsarens lokala lagring eller via kontoinställningarna.",
        "tr": "Platformda bir telefon numarasi saglаdığınızda (örn. bir hizmet talebi gönderirken), bunu nevumo_phone anahtari altında tarayicinizin yerel depolama alaninda gecici olarak saklariz. Bu, sonraki ziyaretlerde otomatik doldurma yapilmasini saglar. Hukuki dayanak: GDPR Madde 6(1)(f) - surtunmeyi azaltma ve kullanici deneyimini iyilestirme konusunda mesru menfaat. Bu veriler, acikca bir form gondermediginiz surece cihazinizi asla terk etmez. Tarayicinizin yerel depolamasini temizleyerek veya hesap ayarlari araciligiyla istediginiz zaman silebilirsiniz.",
        "uk": "Koly vy vkazuyete nomer telefonu na platformi (napr. pry nadsilannyy zapytu na posluhu), my tymchasovo zberihayemo yoho u lokalnomu skhovyshchi vashoho brauzera pid klyuchem nevumo_phone. Tse dozvolyaye avtomatychno zapovnyuvaty yoho pry nastupnykh vidviduvannyakh. Pravova osnova: St. 6(1)(f) GDPR - zakonnyy interes u zmenshennyi nezruchn. i pokrashchenni korystuvatskoho dosvidu. Tsi dani nikoly ne zalishayut vashy prystriy, yakshcho vy yavno ne nadishlete formu. Vy mozhete vydalyty yikh bud-koly, ochystyvshу lokalne skhovyshche brauzera abo cherez nalashtuvannya oblıkovoho zapysu.",
    },
    "cookies.s5_title": {
        "en": "5. Full List of Cookies and Browser Storage Entries",
        "bg": "5. Pulen spisuk na biskvitките i zapisite v brauzarnoto hranilishte",
        "cs": "5. Uplny seznam souboru cookie a zaznamu v ulozisti prohlizece",
        "da": "5. Komplet liste over cookies og browserlagringsposter",
        "de": "5. Vollstandige Liste der Cookies und Browser-Speichereintrage",
        "el": "5. Plireis lista Cookies kai katachwritseon apothikeysis programmatos perigisis",
        "es": "5. Lista completa de cookies y entradas de almacenamiento del navegador",
        "et": "5. Kupsiste ja brauseri salvestusruumi kirjete taielik loend",
        "fi": "5. Taydellinen luettelo evasteista ja selaimen tallennustilan merkinnoista",
        "fr": "5. Liste complete des cookies et entrees de stockage du navigateur",
        "ga": "5. Liosta Iomlán Fianan agus Iontralacha Storalа Brabhsalai",
        "hr": "5. Cjelovit popis kolacica i zapisa pohrane preglednika",
        "hu": "5. Sutik es bongeszo tarhely bejegyzések teljes listaja",
        "is": "5. Fullur listi yfir vafrakokur og faerslur i vafrageymslu",
        "it": "5. Elenco completo di cookie e voci di archiviazione del browser",
        "lb": "5. Vollstanneg Lescht vu Cookies a Browser-Spaeicheraschreiwungen",
        "lt": "5. Pilnas slapuku ir narskykles saugyklos irasu sarasas",
        "lv": "5. Pilns sikdatnu un parlukprogrammas kratuves ierakstu saraksts",
        "mk": "5. Celos spisok na kolacinja i zapisi vo skladiranje na prelistuvacot",
        "mt": "5. Lista Shiha ta' Cookies u Entrati tal-Hazna tal-Browser",
        "nl": "5. Volledige lijst van cookies en browseropslagvermeldingen",
        "no": "5. Fullstendig liste over informasjonskapsler og nettleserlagringsoppforinger",
        "pl": "5. Pelna lista plikow cookie i wpisow w pamieci przegladarki",
        "pt": "5. Lista completa de cookies e entradas de armazenamento do navegador",
        "pt-PT": "5. Lista completa de cookies e entradas de armazenamento do navegador",
        "ro": "5. Lista completa de cookie-uri si inregistrari de stocare in browser",
        "ru": "5. Polnyy spisok faylov cookie i zapisey v khranilishche brauzera",
        "sk": "5. Uplny zoznam suborov cookie a zaznamov v uloziska prehliadaca",
        "sl": "5. Popoln seznam piskotkov in vnosov v shrambi brskalnika",
        "sq": "5. Lista e plote e cookies-ave dhe hyrjeve te ruajtjes se shfletuesit",
        "sr": "5. Potpuna lista kolacica i unosa u skladistenje pregledaca",
        "sv": "5. Fullstandig lista over cookies och webblaserlagringsuppgifter",
        "tr": "5. Cerezlerin ve Tarayici Depolama Girislerinin Tam Listesi",
        "uk": "5. Povnyy spysok fayliv cookie ta zapysiv u skhovyshchi brauzera",
    },
    "cookies.s5_col_name": {
        "en": "Name / Key", "bg": "Naimenovanie / Klyuch", "cs": "Nazev / Klic",
        "da": "Navn / Noggle", "de": "Name / Schlussel", "el": "Onoma / Kleidi",
        "es": "Nombre / Clave", "et": "Nimi / Voti", "fi": "Nimi / Avain",
        "fr": "Nom / Cle", "ga": "Ainm / Eochair", "hr": "Naziv / Kljuc",
        "hu": "Nev / Kulcs", "is": "Nafn / Lykill", "it": "Nome / Chiave",
        "lb": "Numm / Schlussel", "lt": "Pavadinimas / Raktas", "lv": "Nosaukums / Atslega",
        "mk": "Naziv / Kljuc", "mt": "Isem / Cavetta", "nl": "Naam / Sleutel",
        "no": "Navn / Nokkel", "pl": "Nazwa / Klucz", "pt": "Nome / Chave",
        "pt-PT": "Nome / Chave", "ro": "Nume / Cheie", "ru": "Imya / Klyuch",
        "sk": "Nazov / Kluc", "sl": "Ime / Kljuc", "sq": "Emri / Celesi",
        "sr": "Naziv / Kljuc", "sv": "Namn / Nyckel", "tr": "Ad / Anahtar",
        "uk": "Nazva / Klyuch",
    },
    "cookies.s5_col_type": {
        "en": "Storage Type", "bg": "Tip khranilishte", "cs": "Typ uloziste",
        "da": "Lagringstype", "de": "Speichertyp", "el": "Typos apothikeysis",
        "es": "Tipo de almacenamiento", "et": "Salvestusruumi tuup", "fi": "Tallennustyyppi",
        "fr": "Type de stockage", "ga": "Cineal Storalа", "hr": "Vrsta pohrane",
        "hu": "Tarolasi tipus", "is": "Geymslutegund", "it": "Tipo di archiviazione",
        "lb": "Spaeichertyp", "lt": "Saugyklos tipas", "lv": "Kratuves veids",
        "mk": "Tip na skladiranje", "mt": "Tip ta' Hazna", "nl": "Opslagtype",
        "no": "Lagringstype", "pl": "Typ pamieci", "pt": "Tipo de armazenamento",
        "pt-PT": "Tipo de armazenamento", "ro": "Tip de stocare", "ru": "Tip khranilishcha",
        "sk": "Typ uloziska", "sl": "Vrsta shrambe", "sq": "Lloji i ruajtjes",
        "sr": "Vrsta skladista", "sv": "Lagringstyp", "tr": "Depolama Turu",
        "uk": "Typ skhovyshcha",
    },
    "cookies.s5_col_purpose": {
        "en": "Purpose", "bg": "Tsel", "cs": "Ucel", "da": "Formal",
        "de": "Zweck", "el": "Skopos", "es": "Finalidad", "et": "Eesmark",
        "fi": "Tarkoitus", "fr": "Finalite", "ga": "Cuspoír", "hr": "Svrha",
        "hu": "Cel", "is": "Tilgangur", "it": "Scopo", "lb": "Zweck",
        "lt": "Tikslas", "lv": "Mērkis", "mk": "Tsel", "mt": "Skop",
        "nl": "Doel", "no": "Formal", "pl": "Cel", "pt": "Finalidade",
        "pt-PT": "Finalidade", "ro": "Scop", "ru": "Tsel", "sk": "Ucel",
        "sl": "Namen", "sq": "Qellimi", "sr": "Svrha", "sv": "Syfte",
        "tr": "Amac", "uk": "Meta",
    },
}


def seed():
    with engine.begin() as conn:
        for key, translations in TRANSLATIONS.items():
            for lang, value in translations.items():
                conn.execute(
                    text("""
                        INSERT INTO translations (key, lang, value)
                        VALUES (:key, :lang, :value)
                        ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
                    """),
                    {"key": key, "lang": lang, "value": value},
                )
    print(f"Seeded {len(TRANSLATIONS)} keys x 34 languages")


if __name__ == "__main__":
    seed()