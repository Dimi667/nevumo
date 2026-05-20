#!/usr/bin/env python3
"""
Seed contact DSA translations.
Namespace: contact_dsa
Keys: 9 | Languages: 34
Run: docker exec nevumo-api python -m apps.api.scripts.seed_contact_dsa_p1
"""

import os

from sqlalchemy import create_engine, text

NAMESPACE = "contact_dsa"

# Language dictionaries with full keys (including namespace)
TRANSLATIONS_BY_LANG = {
    "en": {
        "contact_dsa.page_title": "DSA Contact Point",
        "contact_dsa.meta_description": "Contact point for authorities and users under the Digital Services Act (DSA). Report illegal content or contact Nevumo for DSA-related matters.",
        "contact_dsa.s1_title": "About This Page",
        "contact_dsa.s1_body": "Nevumo is operated by \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), registered in Sofia, Bulgaria. This page serves as our single point of contact under Article 11 of the Digital Services Act (Regulation (EU) 2022/2065), applicable from 17 February 2024.",
        "contact_dsa.s2_title": "Single Point of Contact",
        "contact_dsa.s2_body": "All DSA-related communications — including reports of illegal content, law enforcement requests, and authority enquiries — should be directed to:",
        "contact_dsa.s2_email_label": "Email:",
        "contact_dsa.s2_email_privacy": "Privacy & GDPR matters:",
        "contact_dsa.s2_email_legal": "Illegal content reports & law enforcement:",
    },
    "bg": {
        "contact_dsa.page_title": "Точка за контакт по DSA",
        "contact_dsa.meta_description": "Точка за контакт с власти и потребители по Закона за цифровите услуги (DSA). Сигнализирайте за незаконно съдържание или се свържете с Nevumo.",
        "contact_dsa.s1_title": "За тази страница",
        "contact_dsa.s1_body": "Nevumo се управлява от \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (ЕИК: 175369610), регистрирано в София, България. Тази страница представлява нашата единна точка за контакт съгласно чл. 11 от Закона за цифровите услуги (Регламент (ЕС) 2022/2065), приложим от 17 февруари 2024 г.",
        "contact_dsa.s2_title": "Единна точка за контакт",
        "contact_dsa.s2_body": "Всички комуникации, свързани с DSA — включително сигнали за незаконно съдържание, запитвания от правоохранителни органи и компетентни власти — следва да бъдат изпращани на:",
        "contact_dsa.s2_email_label": "Имейл:",
        "contact_dsa.s2_email_privacy": "Въпроси за поверителност и GDPR:",
        "contact_dsa.s2_email_legal": "Сигнали за незаконно съдържание и запитвания от власти:",
    },
    "cs": {
        "contact_dsa.page_title": "Kontaktní místo DSA",
        "contact_dsa.meta_description": "Kontaktní místo pro orgány a uživatele v rámci zákona o digitálních službách (DSA). Nahlaste nelegální obsah nebo kontaktujte Nevumo v záležitostech DSA.",
        "contact_dsa.s1_title": "O této stránce",
        "contact_dsa.s1_body": "Nevumo provozuje \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), registrovaná v Sofii v Bulharsku. Tato stránka slouží jako naše jednotné kontaktní místo podle článku 11 zákona o digitálních službách (nařízení (EU) 2022/2065), platného od 17. února 2024.",
        "contact_dsa.s2_title": "Jednotné kontaktní místo",
        "contact_dsa.s2_body": "Veškerá komunikace týkající se DSA — včetně hlášení nelegálního obsahu, žádostí orgánů činných v trestním řízení a dotazů příslušných orgánů — by měla být zasílána na:",
        "contact_dsa.s2_email_label": "E-mail:",
        "contact_dsa.s2_email_privacy": "Ochrana soukromí a GDPR:",
        "contact_dsa.s2_email_legal": "Hlášení nelegálního obsahu a orgány:",
    },
    "da": {
        "contact_dsa.page_title": "DSA-kontaktpunkt",
        "contact_dsa.meta_description": "Kontaktpunkt for myndigheder og brugere i henhold til lov om digitale tjenester (DSA). Anmeld ulovligt indhold eller kontakt Nevumo i DSA-relaterede sager.",
        "contact_dsa.s1_title": "Om denne side",
        "contact_dsa.s1_body": "Nevumo drives af \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), registreret i Sofia, Bulgarien. Denne side fungerer som vores enkelt kontaktpunkt i henhold til artikel 11 i lov om digitale tjenester (forordning (EU) 2022/2065), gældende fra 17. februar 2024.",
        "contact_dsa.s2_title": "Enkelt kontaktpunkt",
        "contact_dsa.s2_body": "Al DSA-relateret kommunikation — herunder anmeldelser af ulovligt indhold, anmodninger fra retshåndhævende myndigheder og forespørgsler fra myndigheder — bedes rettes til:",
        "contact_dsa.s2_email_label": "E-mail:",
        "contact_dsa.s2_email_privacy": "Privatlivs- og GDPR-spørgsmål:",
        "contact_dsa.s2_email_legal": "Rapportering af ulovligt indhold og myndigheder:",
    },
    "de": {
        "contact_dsa.page_title": "DSA-Kontaktstelle",
        "contact_dsa.meta_description": "Kontaktstelle für Behörden und Nutzer gemäß dem Gesetz über digitale Dienste (DSA). Melden Sie illegale Inhalte oder kontaktieren Sie Nevumo in DSA-Angelegenheiten.",
        "contact_dsa.s1_title": "Über diese Seite",
        "contact_dsa.s1_body": "Nevumo wird betrieben von \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), eingetragen in Sofia, Bulgarien. Diese Seite dient als unsere einheitliche Kontaktstelle gemäß Artikel 11 des Gesetzes über digitale Dienste (Verordnung (EU) 2022/2065), anwendbar ab 17. Februar 2024.",
        "contact_dsa.s2_title": "Einheitliche Kontaktstelle",
        "contact_dsa.s2_body": "Alle DSA-bezogenen Mitteilungen — einschließlich Meldungen rechtswidriger Inhalte, Anfragen von Strafverfolgungsbehörden und Behördenanfragen — sind zu richten an:",
        "contact_dsa.s2_email_label": "E-Mail:",
        "contact_dsa.s2_email_privacy": "Datenschutz & DSGVO:",
        "contact_dsa.s2_email_legal": "Meldungen rechtswidriger Inhalte & Behördenanfragen:",
    },
    "el": {
        "contact_dsa.page_title": "Σημείο επαφής DSA",
        "contact_dsa.meta_description": "Σημείο επαφής για αρχές και χρήστες βάσει της Πράξης για τις Ψηφιακές Υπηρεσίες (DSA). Αναφέρετε παράνομο περιεχόμενο ή επικοινωνήστε με το Nevumo.",
        "contact_dsa.s1_title": "Σχετικά με αυτή τη σελίδα",
        "contact_dsa.s1_body": "Το Nevumo λειτουργεί από την \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), εγγεγραμμένη στη Σόφια, Βουλγαρία. Η σελίδα αυτή αποτελεί το ενιαίο σημείο επαφής μας βάσει του άρθρου 11 της Πράξης για τις Ψηφιακές Υπηρεσίες (Κανονισμός (ΕΕ) 2022/2065), που εφαρμόζεται από 17 Φεβρουαρίου 2024.",
        "contact_dsa.s2_title": "Ενιαίο σημείο επαφής",
        "contact_dsa.s2_body": "Όλες οι επικοινωνίες σχετικά με τη DSA — συμπεριλαμβανομένων αναφορών παράνομου περιεχομένου, αιτημάτων αρχών επιβολής νόμου και ερωτημάτων αρχών — πρέπει να απευθύνονται στο:",
        "contact_dsa.s2_email_label": "Email:",
        "contact_dsa.s2_email_privacy": "Θέματα απορρήτου & GDPR:",
        "contact_dsa.s2_email_legal": "Αναφορές παράνομου περιεχομένου & αρχές:",
    },
    "es": {
        "contact_dsa.page_title": "Punto de contacto DSA",
        "contact_dsa.meta_description": "Punto de contacto para autoridades y usuarios en virtud de la Ley de Servicios Digitales (DSA). Denuncie contenido ilegal o contacte con Nevumo para asuntos relacionados con DSA.",
        "contact_dsa.s1_title": "Acerca de esta página",
        "contact_dsa.s1_body": "Nevumo es operado por \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), registrada en Sofía, Bulgaria. Esta página sirve como nuestro punto único de contacto en virtud del artículo 11 de la Ley de Servicios Digitales (Reglamento (UE) 2022/2065), aplicable desde el 17 de febrero de 2024.",
        "contact_dsa.s2_title": "Punto único de contacto",
        "contact_dsa.s2_body": "Todas las comunicaciones relacionadas con la DSA — incluidos los informes de contenido ilegal, las solicitudes de los organismos de seguridad y las consultas de las autoridades — deben dirigirse a:",
        "contact_dsa.s2_email_label": "Correo:",
        "contact_dsa.s2_email_privacy": "Privacidad y RGPD:",
        "contact_dsa.s2_email_legal": "Informes de contenido ilegal y autoridades:",
    },
    "et": {
        "contact_dsa.page_title": "DSA kontaktpunkt",
        "contact_dsa.meta_description": "Kontaktpunkt ametiasutustele ja kasutajatele vastavalt digitaalteenuste seadusele (DSA). Teatage ebaseaduslikust sisust või võtke ühendust Nevumoga DSA-ga seotud küsimustes.",
        "contact_dsa.s1_title": "Sellest lehest",
        "contact_dsa.s1_body": "Nevumot haldab \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), registreeritud Sofias, Bulgaarias. See leht toimib meie ühtse kontaktpunktina vastavalt digitaalteenuste seaduse (määrus (EL) 2022/2065) artiklile 11, mis kehtib alates 17. veebruarist 2024.",
        "contact_dsa.s2_title": "Ühtne kontaktpunkt",
        "contact_dsa.s2_body": "Kogu DSA-ga seotud kirjavahetus — sealhulgas teated ebaseadusliku sisu kohta, õiguskaitseasutuste taotlused ja ametiasutuste päringud — tuleks saata aadressile:",
        "contact_dsa.s2_email_label": "E-post:",
        "contact_dsa.s2_email_privacy": "Privaatsus ja GDPR:",
        "contact_dsa.s2_email_legal": "Ebaseadusliku sisu teatised ja õiguskaitse:",
    },
    "fi": {
        "contact_dsa.page_title": "DSA-yhteystaho",
        "contact_dsa.meta_description": "Yhteystaho viranomaisille ja käyttäjille digitaalisia palveluja koskevan säädöksen (DSA) mukaisesti. Ilmoita laittomasta sisällöstä tai ota yhteyttä Nevumoon DSA-asioissa.",
        "contact_dsa.s1_title": "Tietoja tästä sivusta",
        "contact_dsa.s1_body": "Nevumoa ylläpitää \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), rekisteröity Sofiassa, Bulgariassa. Tämä sivu toimii yhtenäisenä yhteystahona digitaalisia palveluja koskevan säädöksen (asetus (EU) 2022/2065) 11 artiklan mukaisesti, sovellettavana 17. helmikuuta 2024 alkaen.",
        "contact_dsa.s2_title": "Yhteinen yhteystaho",
        "contact_dsa.s2_body": "Kaikki DSA:han liittyvät viestit — mukaan lukien ilmoitukset laittomasta sisällöstä, lainvalvontaviranomaisten pyynnöt ja viranomaisten tiedustelut — tulee osoittaa:",
        "contact_dsa.s2_email_label": "Sähköposti:",
        "contact_dsa.s2_email_privacy": "Tietosuoja ja GDPR:",
        "contact_dsa.s2_email_legal": "Laittoman sisällön ilmoitukset ja viranomaiset:",
    },
    "fr": {
        "contact_dsa.page_title": "Point de contact DSA",
        "contact_dsa.meta_description": "Point de contact pour les autorités et les utilisateurs dans le cadre du règlement sur les services numériques (DSA). Signalez un contenu illicite ou contactez Nevumo pour toute question relative au DSA.",
        "contact_dsa.s1_title": "À propos de cette page",
        "contact_dsa.s1_body": "Nevumo est exploité par \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), enregistrée à Sofia, en Bulgarie. Cette page constitue notre point de contact unique au titre de l'article 11 du règlement sur les services numériques (règlement (UE) 2022/2065), applicable à partir du 17 février 2024.",
        "contact_dsa.s2_title": "Point de contact unique",
        "contact_dsa.s2_body": "Toutes les communications relatives au DSA — y compris les signalements de contenus illicites, les demandes des autorités chargées de l'application de la loi et les demandes des autorités — doivent être adressées à :",
        "contact_dsa.s2_email_label": "E-mail :",
        "contact_dsa.s2_email_privacy": "Confidentialité et RGPD :",
        "contact_dsa.s2_email_legal": "Signalements de contenus illicites et autorités :",
    },
    "ga": {
        "contact_dsa.page_title": "Pointe Teagmhála DSA",
        "contact_dsa.meta_description": "Pointe teagmhála d'údaráis agus d'úsáideoirí faoin Acht um Sheirbhísí Digiteacha (DSA). Tuairiscigh ábhar neamhdhleathach nó déan teagmháil le Nevumo maidir le cúrsaí DSA.",
        "contact_dsa.s1_title": "Maidir leis an Leathanach Seo",
        "contact_dsa.s1_body": "Déanann \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), cláraithe i Sóifia, an Bhulgáir, oibriú ar Nevumo. Feidhmíonn an leathanach seo mar ár bpointe aonair teagmhála faoi Airteagal 11 den Acht um Sheirbhísí Digiteacha (Rialachán (AE) 2022/2065), infheidhme ón 17 Feabhra 2024.",
        "contact_dsa.s2_title": "Pointe Aonair Teagmhála",
        "contact_dsa.s2_body": "Ba cheart gach cumarsáid a bhaineann le DSA — lena n-áirítear tuairiscí ar ábhar neamhdhleathach, iarratais ó fhorfheidhmíú dlí, agus fiosrúcháin ó údaráis — a sheoladh chuig:",
        "contact_dsa.s2_email_label": "Ríomhphost:",
        "contact_dsa.s2_email_privacy": "Príobháideacht & GDPR:",
        "contact_dsa.s2_email_legal": "Tuairiscí ábhair neamhdhleathach & forfheidhmíú dlí:",
    },
    "hr": {
        "contact_dsa.page_title": "DSA kontaktna točka",
        "contact_dsa.meta_description": "Kontaktna točka za tijela i korisnike u okviru Zakona o digitalnim uslugama (DSA). Prijavite nezakoniti sadržaj ili kontaktirajte Nevumo u vezi s pitanjima DSA-e.",
        "contact_dsa.s1_title": "O ovoj stranici",
        "contact_dsa.s1_body": "Nevumo upravlja \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), registrirana u Sofiji, Bugarskoj. Ova stranica služi kao naša jedinstvena kontaktna točka sukladno članku 11. Zakona o digitalnim uslugama (Uredba (EU) 2022/2065), primjenjivog od 17. veljače 2024.",
        "contact_dsa.s2_title": "Jedinstvena kontaktna točka",
        "contact_dsa.s2_body": "Sva komunikacija vezana uz DSA — uključujući prijave nezakonitog sadržaja, zahtjeve tijela kaznenog progona i upite nadležnih tijela — treba biti upućena na:",
        "contact_dsa.s2_email_label": "E-pošta:",
        "contact_dsa.s2_email_privacy": "Privatnost i GDPR:",
        "contact_dsa.s2_email_legal": "Prijave nezakonitog sadržaja i tijela kaznenog progona:",
    },
    "hu": {
        "contact_dsa.page_title": "DSA kapcsolattartási pont",
        "contact_dsa.meta_description": "Kapcsolattartási pont hatóságok és felhasználók számára a digitális szolgáltatásokról szóló jogszabály (DSA) alapján. Jelentse az illegális tartalmakat, vagy lépjen kapcsolatba a Nevumóval DSA-ügyekben.",
        "contact_dsa.s1_title": "Az oldalról",
        "contact_dsa.s1_body": "A Nevumót a \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610) üzemelteti, bejegyezve Szófiában, Bulgáriában. Ez az oldal egypontos kapcsolattartási pontként szolgál a digitális szolgáltatásokról szóló rendelet (EU) 2022/2065 11. cikke alapján, amely 2024. február 17-től alkalmazandó.",
        "contact_dsa.s2_title": "Egypontos kapcsolatfelvétel",
        "contact_dsa.s2_body": "Minden DSA-val kapcsolatos kommunikáció — beleértve az illegális tartalmakra vonatkozó bejelentéseket, a bűnüldöző szervek kérelmeit és a hatósági megkereséseket — a következő címre irányítandó:",
        "contact_dsa.s2_email_label": "E-mail:",
        "contact_dsa.s2_email_privacy": "Adatvédelem és GDPR:",
        "contact_dsa.s2_email_legal": "Illegális tartalom bejelentése és hatóságok:",
    },
    "is": {
        "contact_dsa.page_title": "DSA tengiliður",
        "contact_dsa.meta_description": "Tengiliður fyrir yfirvöld og notendur samkvæmt lögum um stafrænar þjónustur (DSA). Tilkynntu um ólöglegt efni eða hafðu samband við Nevumo vegna DSA-mála.",
        "contact_dsa.s1_title": "Um þessa síðu",
        "contact_dsa.s1_body": "Nevumo er rekið af \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), skráð í Sofíu, Búlgaríu. Þessi síða þjónar sem einn tengiliður okkar samkvæmt 11. grein laga um stafrænar þjónustur (reglugerð (ESB) 2022/2065), sem gildir frá 17. febrúar 2024.",
        "contact_dsa.s2_title": "Einn tengiliður",
        "contact_dsa.s2_body": "Öll samskipti tengd DSA — þar á meðal tilkynningar um ólöglegt efni, beiðnir lögregluyfirvalda og fyrirspurnir yfirvalda — skulu beint til:",
        "contact_dsa.s2_email_label": "Netfang:",
        "contact_dsa.s2_email_privacy": "Persónuvernd og GDPR:",
        "contact_dsa.s2_email_legal": "Tilkynningar um ólöglegt efni og löggælsa:",
    },
    "it": {
        "contact_dsa.page_title": "Punto di contatto DSA",
        "contact_dsa.meta_description": "Punto di contatto per autorità e utenti ai sensi del Regolamento sui servizi digitali (DSA). Segnala contenuti illegali o contatta Nevumo per questioni relative al DSA.",
        "contact_dsa.s1_title": "Informazioni su questa pagina",
        "contact_dsa.s1_body": "Nevumo è gestito da \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), registrata a Sofia, Bulgaria. Questa pagina funge da unico punto di contatto ai sensi dell'articolo 11 del Regolamento sui servizi digitali (Regolamento (UE) 2022/2065), applicabile dal 17 febbraio 2024.",
        "contact_dsa.s2_title": "Punto di contatto unico",
        "contact_dsa.s2_body": "Tutte le comunicazioni relative alla DSA — incluse le segnalazioni di contenuti illegali, le richieste delle forze dell'ordine e le richieste delle autorità — devono essere indirizzate a:",
        "contact_dsa.s2_email_label": "Email:",
        "contact_dsa.s2_email_privacy": "Privacy e GDPR:",
        "contact_dsa.s2_email_legal": "Segnalazioni di contenuti illegali e autorità:",
    },
    "lb": {
        "contact_dsa.page_title": "DSA Kontaktpunkt",
        "contact_dsa.meta_description": "Kontaktpunkt fir Behörden a Benotzer gemäss dem Gesetz iwwer digital Servicer (DSA). Mellt illegalen Inhalt oder kontaktéiert Nevumo a DSA-Froen.",
        "contact_dsa.s1_title": "Iwwer dës Säit",
        "contact_dsa.s1_body": "Nevumo gëtt vun \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610) bedriwwen, agemaach zu Sofia, Bulgarien. Dës Säit déngt als eenzegen Kontaktpunkt gemäss Artikel 11 vum Gesetz iwwer digital Servicer (Verordnung (EU) 2022/2065), uwendbar ab 17. Februar 2024.",
        "contact_dsa.s2_title": "Eenzegen Kontaktpunkt",
        "contact_dsa.s2_body": "All DSA-bezunnen Kommunikatiounen — inklusiv Meldunge vun illegalen Inhalter, Ufroe vu Strofverfolgungsbehörden an Ufroe vun Autoritéiten — sollen un follend Adress geschéckt ginn:",
        "contact_dsa.s2_email_label": "E-Mail:",
        "contact_dsa.s2_email_privacy": "Dateschutz & GDPR:",
        "contact_dsa.s2_email_legal": "Meldunge vun illegalen Inhalter & Behörden:",
    },
    "lt": {
        "contact_dsa.page_title": "DSA kontaktinis punktas",
        "contact_dsa.meta_description": "Kontaktinis punktas valdžios institucijoms ir naudotojams pagal Skaitmeninių paslaugų aktą (DSA). Praneškite apie neteisėtą turinį arba susisiekite su Nevumo DSA klausimais.",
        "contact_dsa.s1_title": "Apie šį puslapį",
        "contact_dsa.s1_body": "Nevumo valdo \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), registruota Sofijoje, Bulgarijoje. Šis puslapis yra mūsų vienintelis kontaktinis punktas pagal Skaitmeninių paslaugų akto (Reglamento (ES) 2022/2065) 11 straipsnį, taikomą nuo 2024 m. vasario 17 d.",
        "contact_dsa.s2_title": "Vienintelis kontaktinis punktas",
        "contact_dsa.s2_body": "Visa su DSA susijusi komunikacija — įskaitant pranešimus apie neteisėtą turinį, teisėsaugos institucijų prašymus ir valdžios institucijų užklausas — turėtų būti siuniama:",
        "contact_dsa.s2_email_label": "El. paštas:",
        "contact_dsa.s2_email_privacy": "Privatumas ir BDAR:",
        "contact_dsa.s2_email_legal": "Pranešimai apie neteisėtą turinį ir teisėsauga:",
    },
    "lv": {
        "contact_dsa.page_title": "DSA kontaktpunkts",
        "contact_dsa.meta_description": "Kontaktpunkts iestādēm un lietotājiem saskaņā ar Digitālo pakalpojumu aktu (DSA). Ziņojiet par nelikumīgu saturu vai sazinieties ar Nevumo DSA jautājumos.",
        "contact_dsa.s1_title": "Par šo lapu",
        "contact_dsa.s1_body": "Nevumo pārvalda \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), reģistrēta Sofijā, Bulgārijā. Šī lapa kalpo kā mūsu vienotais kontaktpunkts saskaņā ar Digitālo pakalpojumu akta (Regula (ES) 2022/2065) 11. pantu, kas piemērojams no 2024. gada 17. februāra.",
        "contact_dsa.s2_title": "Vienots kontaktpunkts",
        "contact_dsa.s2_body": "Visa ar DSA saistītā saziņa — tostarp paziņojumi par nelikumīgu saturu, tiesībaizsardzības iestāžu pieprasījumi un iestāžu jautājumi — jāsūta uz:",
        "contact_dsa.s2_email_label": "E-pasts:",
        "contact_dsa.s2_email_privacy": "Privātums un GDPR:",
        "contact_dsa.s2_email_legal": "Nelikumīga satura ziņojumi un iestādes:",
    },
    "mk": {
        "contact_dsa.page_title": "DSA контактна точка",
        "contact_dsa.meta_description": "Контактна точка за органи и корисници во рамки на Законот за дигитални услуги (DSA). Пријавете незаконита содржина или контактирајте го Nevumo за прашања поврзани со DSA.",
        "contact_dsa.s1_title": "За оваа страница",
        "contact_dsa.s1_body": "Nevumo го управува \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), регистрирано во Софија, Бугарија. Оваа страница служи како наша единствена контактна точка согласно чл. 11 од Законот за дигитални услуги (Регулатива (ЕУ) 2022/2065), применлива од 17 февруари 2024 г.",
        "contact_dsa.s2_title": "Единствена контактна точка",
        "contact_dsa.s2_body": "Сите комуникации поврзани со DSA — вклучувајќи пријави за незаконита содржина, барања од органи за спроведување на законот и прашања од надлежни органи — треба да се упатуваат на:",
        "contact_dsa.s2_email_label": "Е-пошта:",
        "contact_dsa.s2_email_privacy": "Приватност и GDPR:",
        "contact_dsa.s2_email_legal": "Пријави за незаконита содржина и органи:",
    },
    "mt": {
        "contact_dsa.page_title": "Punt ta' kuntatt DSA",
        "contact_dsa.meta_description": "Punt ta' kuntatt għal awtoritajiet u utenti skont l-Att dwar is-Servizzi Diġitali (DSA). Irrapporta kontenut illegali jew ikkuntattja lil Nevumo għal kwistjonijiet relatati mad-DSA.",
        "contact_dsa.s1_title": "Dwar din il-Paġna",
        "contact_dsa.s1_body": "Nevumo huwa operat minn \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), irreġistrata f'Sofija, il-Bulgarija. Din il-paġna sservi bħala l-punt ta' kuntatt uniku tagħna skont l-Artikolu 11 tal-Att dwar is-Servizzi Diġitali (Regolament (UE) 2022/2065), applikabbli mill-17 ta' Frar 2024.",
        "contact_dsa.s2_title": "Punt ta' kuntatt uniku",
        "contact_dsa.s2_body": "Il-komunikazzjonijiet kollha relatati mad-DSA — inkluż rapporti dwar kontenut illegali, talbiet mill-awtoritajiet tal-infurzar tal-liġi, u mistoqsijiet mill-awtoritajiet — għandhom jiġu indirizzati lil:",
        "contact_dsa.s2_email_label": "Email:",
        "contact_dsa.s2_email_privacy": "Privatezza u GDPR:",
        "contact_dsa.s2_email_legal": "Rapporti ta' kontenut illegali u awtoritajiet:",
    },
    "nl": {
        "contact_dsa.page_title": "DSA-contactpunt",
        "contact_dsa.meta_description": "Contactpunt voor autoriteiten en gebruikers op grond van de wet inzake digitale diensten (DSA). Meld illegale inhoud of neem contact op met Nevumo voor DSA-gerelateerde zaken.",
        "contact_dsa.s1_title": "Over deze pagina",
        "contact_dsa.s1_body": "Nevumo wordt geëxploiteerd door \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), geregistreerd in Sofia, Bulgarije. Deze pagina dient als ons enkel contactpunt op grond van artikel 11 van de wet inzake digitale diensten (Verordening (EU) 2022/2065), van toepassing vanaf 17 februari 2024.",
        "contact_dsa.s2_title": "Enkel contactpunt",
        "contact_dsa.s2_body": "Alle DSA-gerelateerde communicatie — inclusief meldingen van illegale inhoud, verzoeken van rechtshandhavingsinstanties en vragen van autoriteiten — dient te worden gericht aan:",
        "contact_dsa.s2_email_label": "E-mail:",
        "contact_dsa.s2_email_privacy": "Privacy & AVG:",
        "contact_dsa.s2_email_legal": "Meldingen illegale inhoud en autoriteiten:",
    },
    "no": {
        "contact_dsa.page_title": "DSA-kontaktpunkt",
        "contact_dsa.meta_description": "Kontaktpunkt for myndigheter og brukere i henhold til lov om digitale tjenester (DSA). Rapporter ulovlig innhold eller kontakt Nevumo i DSA-relaterte saker.",
        "contact_dsa.s1_title": "Om denne siden",
        "contact_dsa.s1_body": "Nevumo drives av \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), registrert i Sofia, Bulgaria. Denne siden fungerer som vårt enkelt kontaktpunkt i henhold til artikkel 11 i lov om digitale tjenester (forordning (EU) 2022/2065), gjeldende fra 17. februar 2024.",
        "contact_dsa.s2_title": "Enkelt kontaktpunkt",
        "contact_dsa.s2_body": "All DSA-relatert kommunikasjon — inkludert rapporter om ulovlig innhold, forespørsler fra rettshåndhevende myndigheter og henvendelser fra myndigheter — skal rettes til:",
        "contact_dsa.s2_email_label": "E-post:",
        "contact_dsa.s2_email_privacy": "Personvern og GDPR:",
        "contact_dsa.s2_email_legal": "Rapporter om ulovlig innhold og myndigheter:",
    },
    "pl": {
        "contact_dsa.page_title": "Punkt kontaktowy DSA",
        "contact_dsa.meta_description": "Punkt kontaktowy dla organów i użytkowników zgodnie z Aktem o usługach cyfrowych (DSA). Zgłoś nielegalne treści lub skontaktuj się z Nevumo w sprawach DSA.",
        "contact_dsa.s1_title": "O tej stronie",
        "contact_dsa.s1_body": "Nevumo jest obsługiwane przez \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), zarejestrowaną w Sofii, w Bułgarii. Niniejsza strona stanowi nasz pojedynczy punkt kontaktowy zgodnie z art. 11 Aktu o usługach cyfrowych (Rozporządzenie (UE) 2022/2065), stosowanego od 17 lutego 2024 r.",
        "contact_dsa.s2_title": "Pojedynczy punkt kontaktowy",
        "contact_dsa.s2_body": "Wszelka komunikacja związana z DSA — w tym zgłoszenia nielegalnych treści, wnioski organów ścigania oraz zapytania właściwych organów — powinna być kierowana na adres:",
        "contact_dsa.s2_email_label": "E-mail:",
        "contact_dsa.s2_email_privacy": "Prywatność i RODO:",
        "contact_dsa.s2_email_legal": "Zgłoszenia nielegalnych treści i organy ścigania:",
    },
    "pt": {
        "contact_dsa.page_title": "Ponto de Contato DSA",
        "contact_dsa.meta_description": "Ponto de contato para autoridades e usuários ao abrigo da Lei dos Serviços Digitais (DSA). Denuncie conteúdo ilegal ou contacte a Nevumo para assuntos relacionados com o DSA.",
        "contact_dsa.s1_title": "Sobre Esta Página",
        "contact_dsa.s1_body": "A Nevumo é operada pela \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), registada em Sófia, Bulgária. Esta página serve como nosso ponto único de contacto ao abrigo do artigo 11.º da Lei dos Serviços Digitais (Regulamento (UE) 2022/2065), aplicável a partir de 17 de fevereiro de 2024.",
        "contact_dsa.s2_title": "Ponto Único de Contato",
        "contact_dsa.s2_body": "Todas as comunicações relacionadas com o DSA — incluindo relatórios de conteúdo ilegal, pedidos de autoridades policiais e consultas de autoridades — devem ser dirigidas a:",
        "contact_dsa.s2_email_label": "E-mail:",
        "contact_dsa.s2_email_privacy": "Privacidade e GDPR:",
        "contact_dsa.s2_email_legal": "Relatórios de conteúdo ilegal e autoridades:",
    },
    "pt_PT": {
        "contact_dsa.page_title": "Ponto de Contacto DSA",
        "contact_dsa.meta_description": "Ponto de contacto para autoridades e utilizadores ao abrigo da Lei dos Serviços Digitais (DSA). Denuncie conteúdo ilegal ou contacte a Nevumo para assuntos relacionados com o DSA.",
        "contact_dsa.s1_title": "Sobre Esta Página",
        "contact_dsa.s1_body": "A Nevumo é operada pela \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), registada em Sófia, Bulgária. Esta página serve como nosso ponto único de contacto ao abrigo do artigo 11.º da Lei dos Serviços Digitais (Regulamento (UE) 2022/2065), aplicável a partir de 17 de fevereiro de 2024.",
        "contact_dsa.s2_title": "Ponto Único de Contacto",
        "contact_dsa.s2_body": "Todas as comunicações relacionadas com o DSA — incluindo relatórios de conteúdo ilegal, pedidos de autoridades policiais e consultas de autoridades — devem ser dirigidas a:",
        "contact_dsa.s2_email_label": "E-mail:",
        "contact_dsa.s2_email_privacy": "Privacidade e RGPD:",
        "contact_dsa.s2_email_legal": "Relatórios de conteúdo ilegal e autoridades:",
    },
    "ro": {
        "contact_dsa.page_title": "Punct de contact DSA",
        "contact_dsa.meta_description": "Punct de contact pentru autorități și utilizatori în temeiul Legii privind serviciile digitale (DSA). Raportați conținut ilegal sau contactați Nevumo pentru aspecte legate de DSA.",
        "contact_dsa.s1_title": "Despre această pagină",
        "contact_dsa.s1_body": "Nevumo este operat de \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), înregistrată în Sofia, Bulgaria. Această pagină servește drept punct unic de contact în temeiul articolului 11 din Legea privind serviciile digitale (Regulamentul (UE) 2022/2065), aplicabil de la 17 februarie 2024.",
        "contact_dsa.s2_title": "Punct unic de contact",
        "contact_dsa.s2_body": "Toate comunicările legate de DSA — inclusiv raportările de conținut ilegal, solicitările autorităților de aplicare a legii și întrebările autorităților — trebuie adresate la:",
        "contact_dsa.s2_email_label": "E-mail:",
        "contact_dsa.s2_email_privacy": "Confidențialitate și GDPR:",
        "contact_dsa.s2_email_legal": "Raportări de conținut ilegal și autorități:",
    },
    "ru": {
        "contact_dsa.page_title": "Контактная точка DSA",
        "contact_dsa.meta_description": "Контактная точка для органов власти и пользователей в соответствии с Законом о цифровых услугах (DSA). Сообщайте о незаконном контенте или обращайтесь в Nevumo по вопросам DSA.",
        "contact_dsa.s1_title": "Об этой странице",
        "contact_dsa.s1_body": "Nevumo управляется компанией \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), зарегистрированной в Софии, Болгария. Данная страница служит единой контактной точкой в соответствии со статьёй 11 Закона о цифровых услугах (Регламент (ЕС) 2022/2065), применимого с 17 февраля 2024 года.",
        "contact_dsa.s2_title": "Единая контактная точка",
        "contact_dsa.s2_body": "Все коммуникации, связанные с DSA, — включая сообщения о незаконном контенте, запросы правоохранительных органов и обращения властей — следует направлять по адресу:",
        "contact_dsa.s2_email_label": "Эл. почта:",
        "contact_dsa.s2_email_privacy": "Конфиденциальность и GDPR:",
        "contact_dsa.s2_email_legal": "Сообщения о незаконном контенте и органы:",
    },
    "sk": {
        "contact_dsa.page_title": "Kontaktné miesto DSA",
        "contact_dsa.meta_description": "Kontaktné miesto pre orgány a používateľov v rámci zákona o digitálnych službách (DSA). Nahlaste nezákonný obsah alebo kontaktujte Nevumo v záležitostiach DSA.",
        "contact_dsa.s1_title": "O tejto stránke",
        "contact_dsa.s1_body": "Nevumo prevádzkuje \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), registrovaná v Sofii v Bulharsku. Táto stránka slúži ako naše jediné kontaktné miesto podľa článku 11 zákona o digitálnych službách (nariadenie (EÚ) 2022/2065), platného od 17. februára 2024.",
        "contact_dsa.s2_title": "Jednotné kontaktné miesto",
        "contact_dsa.s2_body": "Všetka komunikácia týkajúca sa DSA — vrátane hlásení nezákonného obsahu, žiadostí orgánov činných v trestnom konaní a dopytov príslušných orgánov — by mala byť zasielaná na:",
        "contact_dsa.s2_email_label": "E-mail:",
        "contact_dsa.s2_email_privacy": "Ochrana súkromia a GDPR:",
        "contact_dsa.s2_email_legal": "Hlásenia nezákonného obsahu a orgány:",
    },
    "sl": {
        "contact_dsa.page_title": "Kontaktna točka DSA",
        "contact_dsa.meta_description": "Kontaktna točka za organe in uporabnike v okviru Zakona o digitalnih storitvah (DSA). Prijavite nezakonito vsebino ali stopite v stik z Nevumo v zadevah DSA.",
        "contact_dsa.s1_title": "O tej strani",
        "contact_dsa.s1_body": "Nevumo upravlja \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), registrirana v Sofiji, Bolgarija. Ta stran služi kot naša enotna kontaktna točka v skladu s členom 11 Zakona o digitalnih storitvah (Uredba (EU) 2022/2065), ki se uporablja od 17. februarja 2024.",
        "contact_dsa.s2_title": "Enotna kontaktna točka",
        "contact_dsa.s2_body": "Vsa komunikacija v zvezi z DSA — vključno s prijavami nezakonite vsebine, zahtevami organov pregona in poizvedbami pristojnih organov — naj bo naslovljena na:",
        "contact_dsa.s2_email_label": "E-pošta:",
        "contact_dsa.s2_email_privacy": "Zasebnost in GDPR:",
        "contact_dsa.s2_email_legal": "Prijave nezakonite vsebine in organi:",
    },
    "sq": {
        "contact_dsa.page_title": "Pika e kontaktit DSA",
        "contact_dsa.meta_description": "Pikë kontakti për autoritetet dhe përdoruesit sipas Aktit të Shërbimeve Dixhitale (DSA). Raportoni përmbajtje ilegale ose kontaktoni Nevumo për çështje të lidhura me DSA.",
        "contact_dsa.s1_title": "Rreth kësaj faqeje",
        "contact_dsa.s1_body": "Nevumo operohet nga \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), e regjistruar në Sofje, Bullgari. Kjo faqe shërben si pika jonë e vetme e kontaktit sipas nenit 11 të Aktit të Shërbimeve Dixhitale (Rregullore (BE) 2022/2065), e zbatueshme nga 17 shkurti 2024.",
        "contact_dsa.s2_title": "Pika e vetme e kontaktit",
        "contact_dsa.s2_body": "Të gjitha komunikimet e lidhura me DSA — duke përfshirë raportet e përmbajtjes ilegale, kërkesat e zbatimit të ligjit dhe pyetjet e autoriteteve — duhet t'i drejtohen:",
        "contact_dsa.s2_email_label": "Email:",
        "contact_dsa.s2_email_privacy": "Privatësia dhe GDPR:",
        "contact_dsa.s2_email_legal": "Raportet e përmbajtjes ilegale dhe autoritetet:",
    },
    "sr": {
        "contact_dsa.page_title": "DSA kontaktna tačka",
        "contact_dsa.meta_description": "Kontaktna tačka za organe i korisnike u okviru Zakona o digitalnim uslugama (DSA). Prijavite nezakoniti sadržaj ili kontaktirajte Nevumo u vezi s pitanjima DSA.",
        "contact_dsa.s1_title": "O ovoj stranici",
        "contact_dsa.s1_body": "Nevumo upravlja \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), registrovana u Sofiji, Bugarskoj. Ova stranica služi kao naša jedinstvena kontaktna tačka u skladu sa članom 11 Zakona o digitalnim uslugama (Uredba (EU) 2022/2065), primenjivog od 17. februara 2024.",
        "contact_dsa.s2_title": "Jedinstvena kontaktna tačka",
        "contact_dsa.s2_body": "Sva komunikacija vezana za DSA — uključujući prijave nezakonitog sadržaja, zahteve organa za sprovođenje zakona i upite nadležnih organa — treba biti upućena na:",
        "contact_dsa.s2_email_label": "Imejl:",
        "contact_dsa.s2_email_privacy": "Privatnost i GDPR:",
        "contact_dsa.s2_email_legal": "Prijave nezakonitog sadržaja i organi:",
    },
    "sv": {
        "contact_dsa.page_title": "DSA-kontaktpunkt",
        "contact_dsa.meta_description": "Kontaktpunkt för myndigheter och användare enligt lagen om digitala tjänster (DSA). Rapportera olagligt innehåll eller kontakta Nevumo i DSA-relaterade ärenden.",
        "contact_dsa.s1_title": "Om den här sidan",
        "contact_dsa.s1_body": "Nevumo drivs av \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), registrerat i Sofia, Bulgarien. Denna sida fungerar som vår enda kontaktpunkt enligt artikel 11 i lagen om digitala tjänster (förordning (EU) 2022/2065), tillämplig från och med den 17 februari 2024.",
        "contact_dsa.s2_title": "Enda kontaktpunkt",
        "contact_dsa.s2_body": "All DSA-relaterad kommunikation — inklusive rapporter om olagligt innehåll, förfrågningar från brottsbekämpande myndigheter och myndighetsförfrågningar — ska riktas till:",
        "contact_dsa.s2_email_label": "E-post:",
        "contact_dsa.s2_email_privacy": "Integritet och GDPR:",
        "contact_dsa.s2_email_legal": "Rapporter om olagligt innehåll och myndigheter:",
    },
    "tr": {
        "contact_dsa.page_title": "DSA İletişim Noktası",
        "contact_dsa.meta_description": "Dijital Hizmetler Yasası (DSA) kapsamında yetkililer ve kullanıcılar için iletişim noktası. Yasadışı içeriği bildirin veya DSA ile ilgili konular için Nevumo ile iletişime geçin.",
        "contact_dsa.s1_title": "Bu Sayfa Hakkında",
        "contact_dsa.s1_body": "Nevumo, Sofya, Bulgaristan'da kayıtlı \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610) tarafından işletilmektedir. Bu sayfa, 17 Şubat 2024'ten itibaren geçerli olan Dijital Hizmetler Yasası'nın (AB Yönetmeliği 2022/2065) 11. maddesi kapsamında tek iletişim noktamız olarak hizmet vermektedir.",
        "contact_dsa.s2_title": "Tek İletişim Noktası",
        "contact_dsa.s2_body": "DSA ile ilgili tüm iletişimler — yasadışı içerik raporları, kolluk kuvvetleri talepleri ve yetkili makam soruşturmaları dahil — aşağıdaki adrese yönlendirilmelidir:",
        "contact_dsa.s2_email_label": "E-posta:",
        "contact_dsa.s2_email_privacy": "Gizlilik ve GDPR:",
        "contact_dsa.s2_email_legal": "Yasadışı içerik bildirimleri ve yetkililer:",
    },
    "uk": {
        "contact_dsa.page_title": "Контактна точка DSA",
        "contact_dsa.meta_description": "Контактна точка для органів влади та користувачів відповідно до Закону про цифрові послуги (DSA). Повідомляйте про незаконний вміст або звертайтеся до Nevumo з питань DSA.",
        "contact_dsa.s1_title": "Про цю сторінку",
        "contact_dsa.s1_body": "Nevumo управляється компанією \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (EIK: 175369610), зареєстрованою в Софії, Болгарія. Ця сторінка слугує єдиною контактною точкою відповідно до статті 11 Закону про цифрові послуги (Регламент (ЄС) 2022/2065), що застосовується з 17 лютого 2024 року.",
        "contact_dsa.s2_title": "Єдина контактна точка",
        "contact_dsa.s2_body": "Всі комунікації, пов'язані з DSA, — включаючи повідомлення про незаконний вміст, запити правоохоронних органів та звернення органів влади — слід надсилати на:",
        "contact_dsa.s2_email_label": "Ел. пошта:",
        "contact_dsa.s2_email_privacy": "Конфіденційність і GDPR:",
        "contact_dsa.s2_email_legal": "Повідомлення про незаконний вміст та органи:",
    },
}


def get_database_url() -> str:
    """Get database URL from environment or use default."""
    return os.getenv("DATABASE_URL", "postgresql://nevumo:nevumo@localhost:5432/nevumo_leads")


def seed_translations() -> None:
    """Seed all contact DSA translations into the database."""
    engine = create_engine(get_database_url())

    with engine.connect() as conn:
        count = 0
        for lang, translations in TRANSLATIONS_BY_LANG.items():
            for key, value in translations.items():
                conn.execute(
                    text("""
                        INSERT INTO translations (lang, key, value)
                        VALUES (:lang, :key, :value)
                        ON CONFLICT (lang, key)
                        DO UPDATE SET value = EXCLUDED.value
                    """),
                    {"lang": lang, "key": key, "value": value}
                )
                count += 1

        conn.commit()
        print(f"Inserted/updated {count} translation rows for namespace '{NAMESPACE}'")


def verify_translations() -> None:
    """Verify the translations were inserted correctly."""
    engine = create_engine(get_database_url())

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT lang, COUNT(*) as keys
                FROM translations
                WHERE key LIKE :pattern
                GROUP BY lang
                ORDER BY lang
            """),
            {"pattern": f"{NAMESPACE}.%"}
        )
        rows = result.fetchall()
        print(f"\nVerification for namespace '{NAMESPACE}':")
        for row in rows:
            print(f"  {row[0]}: {row[1]} keys")


if __name__ == "__main__":
    seed_translations()
    verify_translations()
