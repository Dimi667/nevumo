"""
Seed script: cookies namespace — p22
Keys: s7_title, s7_col_processor, s7_col_role, s7_col_privacy,
      s8_title, s8_text, s8_col_recipient, s8_col_country, s8_col_protection
34 languages × 9 keys = 306 rows
Run: docker exec nevumo-api python -m apps.api.scripts.seed_cookies_p22
"""

import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://nevumo:nevumo@postgres:5432/nevumo_leads")
engine = create_engine(DATABASE_URL)

NAMESPACE = "cookies"

TRANSLATIONS = {
    "s7_title": {
        "en": "7. Third-Party Data Processors",
        "pl": "7. Podmioty przetwarzające danych (zewnętrzni procesorzy)",
        "bg": "7. Трети страни — обработващи данни",
        "de": "7. Drittanbieter-Datenverarbeiter",
        "fr": "7. Sous-traitants tiers",
        "es": "7. Procesadores de datos de terceros",
        "it": "7. Responsabili del trattamento terzi",
        "pt": "7. Processadores de dados de terceiros",
        "pt-PT": "7. Processadores de dados de terceiros",
        "nl": "7. Externe gegevensverwerkers",
        "cs": "7. Třetí strany — zpracovatelé dat",
        "sk": "7. Tretie strany — spracúvatelia údajov",
        "hu": "7. Harmadik feles adatfeldolgozók",
        "ro": "7. Procesatori de date terți",
        "hr": "7. Treće strane — obrađivači podataka",
        "sr": "7. Treće strane — obrađivači podataka",
        "sl": "7. Tretje osebe — obdelovalci podatkov",
        "uk": "7. Треті сторони — обробники даних",
        "ru": "7. Сторонние обработчики данных",
        "tr": "7. Üçüncü Taraf Veri İşleyicileri",
        "el": "7. Τρίτοι επεξεργαστές δεδομένων",
        "da": "7. Tredjepartsdatabehandlere",
        "sv": "7. Tredjepartsdatabehandlare",
        "no": "7. Tredjeparts databehandlere",
        "fi": "7. Kolmansien osapuolten tietojenkäsittelijät",
        "et": "7. Kolmanda osapoole andmetöötlejad",
        "lv": "7. Trešo pušu datu apstrādātāji",
        "lt": "7. Trečiųjų šalių duomenų tvarkytojai",
        "ga": "7. Próiseálaithe Sonraí Tríú Páirtí",
        "is": "7. Gagnameðhöndlarar þriðja aðila",
        "lb": "7. Drëttpartei-Datenveraarbechter",
        "mk": "7. Обработувачи на податоци од трети страни",
        "sq": "7. Përpunuesit e të Dhënave të Palëve të Treta",
        "mt": "7. Proċessuri ta' Data ta' Parti Terza",
    },
    "s7_col_processor": {
        "en": "Processor", "pl": "Procesor", "bg": "Обработващ", "de": "Verarbeiter",
        "fr": "Sous-traitant", "es": "Procesador", "it": "Responsabile", "pt": "Processador",
        "pt-PT": "Processador", "nl": "Verwerker", "cs": "Zpracovatel", "sk": "Spracúvateľ",
        "hu": "Adatfeldolgozó", "ro": "Procesator", "hr": "Obrađivač", "sr": "Obrađivač",
        "sl": "Obdelovalec", "uk": "Обробник", "ru": "Обработчик", "tr": "İşleyici",
        "el": "Επεξεργαστής", "da": "Behandler", "sv": "Behandlare", "no": "Behandler",
        "fi": "Käsittelijä", "et": "Töötleja", "lv": "Apstrādātājs", "lt": "Tvarkytojas",
        "ga": "Próiseálaí", "is": "Vinnsluaðili", "lb": "Veraarbechter",
        "mk": "Обработувач", "sq": "Përpunues", "mt": "Proċessur",
    },
    "s7_col_role": {
        "en": "Role", "pl": "Rola", "bg": "Роля", "de": "Rolle",
        "fr": "Rôle", "es": "Rol", "it": "Ruolo", "pt": "Papel",
        "pt-PT": "Papel", "nl": "Rol", "cs": "Role", "sk": "Rola",
        "hu": "Szerepkör", "ro": "Rol", "hr": "Uloga", "sr": "Uloga",
        "sl": "Vloga", "uk": "Роль", "ru": "Роль", "tr": "Rol",
        "el": "Ρόλος", "da": "Rolle", "sv": "Roll", "no": "Rolle",
        "fi": "Rooli", "et": "Roll", "lv": "Loma", "lt": "Vaidmuo",
        "ga": "Ról", "is": "Hlutverk", "lb": "Roll",
        "mk": "Улога", "sq": "Roli", "mt": "Rwol",
    },
    "s7_col_privacy": {
        "en": "Privacy Policy", "pl": "Polityka prywatności", "bg": "Политика за поверителност",
        "de": "Datenschutzrichtlinie", "fr": "Politique de confidentialité",
        "es": "Política de privacidad", "it": "Informativa sulla privacy",
        "pt": "Política de privacidade", "pt-PT": "Política de privacidade",
        "nl": "Privacybeleid", "cs": "Zásady ochrany osobních údajů",
        "sk": "Zásady ochrany osobných údajov", "hu": "Adatvédelmi irányelvek",
        "ro": "Politica de confidențialitate", "hr": "Politika privatnosti",
        "sr": "Politika privatnosti", "sl": "Politika zasebnosti",
        "uk": "Політика конфіденційності", "ru": "Политика конфиденциальности",
        "tr": "Gizlilik Politikası", "el": "Πολιτική απορρήτου",
        "da": "Privatlivspolitik", "sv": "Integritetspolicy", "no": "Personvernregler",
        "fi": "Tietosuojakäytäntö", "et": "Privaatsuspoliitika",
        "lv": "Privātuma politika", "lt": "Privatumo politika",
        "ga": "Beartas Príobháideachais", "is": "Persónuverndarstefna",
        "lb": "Dateschutzpolitik", "mk": "Политика за приватност",
        "sq": "Politika e Privatësisë", "mt": "Politika tal-Privatezza",
    },
    "s8_title": {
        "en": "8. International Data Transfers",
        "pl": "8. Przekazywanie danych poza EOG",
        "bg": "8. Международни трансфери на данни",
        "de": "8. Internationale Datenübermittlungen",
        "fr": "8. Transferts internationaux de données",
        "es": "8. Transferencias internacionales de datos",
        "it": "8. Trasferimenti internazionali di dati",
        "pt": "8. Transferências internacionais de dados",
        "pt-PT": "8. Transferências internacionais de dados",
        "nl": "8. Internationale gegevensoverdrachten",
        "cs": "8. Mezinárodní přenosy dat",
        "sk": "8. Medzinárodné prenosy údajov",
        "hu": "8. Nemzetközi adattovábbítások",
        "ro": "8. Transferuri internaționale de date",
        "hr": "8. Međunarodni prijenosi podataka",
        "sr": "8. Međunarodni prenosi podataka",
        "sl": "8. Mednarodni prenosi podatkov",
        "uk": "8. Міжнародні передачі даних",
        "ru": "8. Международные передачи данных",
        "tr": "8. Uluslararası Veri Aktarımları",
        "el": "8. Διεθνείς μεταφορές δεδομένων",
        "da": "8. Internationale dataoverførsler",
        "sv": "8. Internationella dataöverföringar",
        "no": "8. Internasjonale dataoverføringer",
        "fi": "8. Kansainväliset tiedonsiirrot",
        "et": "8. Rahvusvahelised andmeedastused",
        "lv": "8. Starptautiski datu pārsūtījumi",
        "lt": "8. Tarptautiniai duomenų perdavimai",
        "ga": "8. Aistrithe Idirnáisiúnta Sonraí",
        "is": "8. Alþjóðlegar gagnaflutningar",
        "lb": "8. International Datentransferéierungen",
        "mk": "8. Меѓународни трансфери на податоци",
        "sq": "8. Transfertat Ndërkombëtare të të Dhënave",
        "mt": "8. Trasferimenti Internazzjonali ta' Data",
    },
    "s8_text": {
        "en": "Nevumo's hosting infrastructure is based in the United States. All transfers outside the European Economic Area (EEA) are safeguarded by Standard Contractual Clauses (SCCs) approved by the European Commission. Additionally, Google LLC and Cloudflare Inc. participate in the EU–US Data Privacy Framework (DPF), providing an additional transfer safeguard.",
        "pl": "Infrastruktura hostingowa Nevumo jest zlokalizowana w Stanach Zjednoczonych. Wszystkie transfery poza Europejski Obszar Gospodarczy (EOG) są zabezpieczone Standardowymi Klauzulami Umownymi (SCC) zatwierdzonymi przez Komisję Europejską. Dodatkowo Google LLC i Cloudflare Inc. uczestniczą w programie EU–US Data Privacy Framework (DPF), stanowiącym dodatkowe zabezpieczenie transferu.",
        "bg": "Хостинг инфраструктурата на Nevumo е базирана в Съединените щати. Всички трансфери извън Европейското икономическо пространство (ЕИП) са защитени чрез Стандартни договорни клаузи (СДК), одобрени от Европейската комисия. Допълнително, Google LLC и Cloudflare Inc. участват в рамката ЕС–САЩ за защита на данните (EU–US Data Privacy Framework — DPF), което осигурява допълнителна защита при трансфера.",
        "de": "Die Hosting-Infrastruktur von Nevumo befindet sich in den Vereinigten Staaten. Alle Übermittlungen außerhalb des Europäischen Wirtschaftsraums (EWR) werden durch von der Europäischen Kommission genehmigte Standardvertragsklauseln (SCCs) abgesichert. Darüber hinaus nehmen Google LLC und Cloudflare Inc. am EU-US-Datenschutzrahmen (DPF) teil, was eine zusätzliche Schutzgarantie bietet.",
        "fr": "L'infrastructure d'hébergement de Nevumo est basée aux États-Unis. Tous les transferts en dehors de l'Espace économique européen (EEE) sont protégés par des clauses contractuelles types (CCT) approuvées par la Commission européenne. De plus, Google LLC et Cloudflare Inc. participent au cadre EU-US Data Privacy Framework (DPF), offrant une garantie supplémentaire pour les transferts.",
        "es": "La infraestructura de alojamiento de Nevumo se encuentra en los Estados Unidos. Todas las transferencias fuera del Espacio Económico Europeo (EEE) están protegidas por Cláusulas Contractuales Estándar (SCC) aprobadas por la Comisión Europea. Además, Google LLC y Cloudflare Inc. participan en el Marco de Privacidad de Datos UE-EE. UU. (DPF), proporcionando una garantía adicional de transferencia.",
        "it": "L'infrastruttura di hosting di Nevumo si trova negli Stati Uniti. Tutti i trasferimenti al di fuori dello Spazio economico europeo (SEE) sono tutelati da Clausole contrattuali standard (SCC) approvate dalla Commissione europea. Inoltre, Google LLC e Cloudflare Inc. aderiscono al quadro EU-US Data Privacy Framework (DPF), fornendo un'ulteriore garanzia di trasferimento.",
        "pt": "A infraestrutura de alojamento da Nevumo está baseada nos Estados Unidos. Todas as transferências para fora do Espaço Económico Europeu (EEE) são protegidas por Cláusulas Contratuais Padrão (CCPs) aprovadas pela Comissão Europeia. Além disso, a Google LLC e a Cloudflare Inc. participam no Quadro de Privacidade de Dados UE-EUA (DPF), proporcionando uma garantia adicional de transferência.",
        "pt-PT": "A infraestrutura de alojamento da Nevumo está sediada nos Estados Unidos. Todas as transferências para fora do Espaço Económico Europeu (EEE) são salvaguardadas por Cláusulas Contratuais Padrão (CCP) aprovadas pela Comissão Europeia. Além disso, a Google LLC e a Cloudflare Inc. participam no Quadro de Privacidade de Dados UE-EUA (DPF), proporcionando uma salvaguarda adicional às transferências.",
        "nl": "De hostinginfrastructuur van Nevumo is gevestigd in de Verenigde Staten. Alle overdrachten buiten de Europese Economische Ruimte (EER) worden beschermd door Standaardcontractbepalingen (SCB's) die door de Europese Commissie zijn goedgekeurd. Bovendien nemen Google LLC en Cloudflare Inc. deel aan het EU-VS-kader voor gegevensprivacy (DPF), wat een extra overdrachtsgarantie biedt.",
        "cs": "Hostingová infrastruktura Nevumo se nachází ve Spojených státech amerických. Veškeré přenosy mimo Evropský hospodářský prostor (EHP) jsou chráněny standardními smluvními doložkami (SCC) schválenými Evropskou komisí. Společnosti Google LLC a Cloudflare Inc. navíc participují na rámci EU–US Data Privacy Framework (DPF), který poskytuje další ochranu přenosů.",
        "sk": "Hostingová infraštruktúra Nevumo sa nachádza v Spojených štátoch amerických. Všetky prenosy mimo Európskeho hospodárskeho priestoru (EHP) sú chránené štandardnými zmluvnými doložkami (SCC) schválenými Európskou komisiou. Okrem toho sa Google LLC a Cloudflare Inc. zúčastňujú na rámci EU–US Data Privacy Framework (DPF), ktorý poskytuje dodatočnú ochranu prenosov.",
        "hu": "A Nevumo tárhelyi infrastruktúrája az Egyesült Államokban található. Az Európai Gazdasági Térségen (EGT) kívüli összes adattovábbítást az Európai Bizottság által jóváhagyott Általános Szerződési Feltételek (SCK) biztosítják. Emellett a Google LLC és a Cloudflare Inc. részt vesz az EU–USA adatvédelmi keretrendszerben (DPF), amely kiegészítő garanciát nyújt az adattovábbításhoz.",
        "ro": "Infrastructura de găzduire a Nevumo este situată în Statele Unite. Toate transferurile în afara Spațiului Economic European (SEE) sunt protejate de Clauzele Contractuale Standard (SCC) aprobate de Comisia Europeană. În plus, Google LLC și Cloudflare Inc. participă la Cadrul de Confidențialitate a Datelor UE-SUA (DPF), oferind o garanție suplimentară pentru transferuri.",
        "hr": "Hosting infrastruktura Nevumo nalazi se u Sjedinjenim Državama. Svi prijenosi izvan Europskog gospodarskog prostora (EGP) zaštićeni su Standardnim ugovornim klauzulama (SCC) odobrenima od strane Europske komisije. Dodatno, Google LLC i Cloudflare Inc. sudjeluju u okviru EU–US Data Privacy Framework (DPF), pružajući dodatno jamstvo zaštite prijenosa.",
        "sr": "Hosting infrastruktura Nevumo nalazi se u Sjedinjenim Državama. Svi prenosi izvan Evropskog ekonomskog prostora (EEP) zaštićeni su Standardnim ugovornim klauzulama (SCC) odobrenima od strane Evropske komisije. Dodatno, Google LLC i Cloudflare Inc. učestvuju u okviru EU–US Data Privacy Framework (DPF), pružajući dodatnu garanciju zaštite prenosa.",
        "sl": "Gostovalna infrastruktura Nevumo se nahaja v Združenih državah Amerike. Vsi prenosi zunaj Evropskega gospodarskega prostora (EGP) so zaščiteni s standardnimi pogodbenimi klavzulami (SCC), ki jih je odobrila Evropska komisija. Poleg tega Google LLC in Cloudflare Inc. sodelujeta v okviru EU–US Data Privacy Framework (DPF), kar zagotavlja dodatno zaščito pri prenosih.",
        "uk": "Хостингова інфраструктура Nevumo знаходиться в Сполучених Штатах Америки. Всі передачі за межі Європейського економічного простору (ЄЕП) захищені Стандартними договірними умовами (СДУ), затвердженими Єврокомісією. Крім того, Google LLC та Cloudflare Inc. беруть участь у рамці ЄС–США щодо захисту конфіденційності даних (DPF), що забезпечує додатковий захист передач.",
        "ru": "Хостинговая инфраструктура Nevumo расположена в Соединённых Штатах Америки. Все передачи за пределы Европейской экономической зоны (ЕЭЗ) защищены Стандартными договорными условиями (СДУ), утверждёнными Европейской комиссией. Кроме того, Google LLC и Cloudflare Inc. участвуют в рамке ЕС–США по защите конфиденциальности данных (DPF), обеспечивающей дополнительную гарантию передачи.",
        "tr": "Nevumo'nun barındırma altyapısı Amerika Birleşik Devletleri'nde bulunmaktadır. Avrupa Ekonomik Alanı (AEA) dışındaki tüm aktarımlar, Avrupa Komisyonu tarafından onaylanan Standart Sözleşme Maddeleri (SCC) ile güvence altına alınmaktadır. Ayrıca Google LLC ve Cloudflare Inc., ek bir aktarım güvencesi sağlayan AB-ABD Veri Gizliliği Çerçevesi'ne (DPF) katılmaktadır.",
        "el": "Η υποδομή φιλοξενίας της Nevumo βρίσκεται στις Ηνωμένες Πολιτείες. Όλες οι μεταφορές εκτός του Ευρωπαϊκού Οικονομικού Χώρου (ΕΟΧ) διασφαλίζονται από τυποποιημένες συμβατικές ρήτρες (SCC) που εγκρίθηκαν από την Ευρωπαϊκή Επιτροπή. Επιπλέον, η Google LLC και η Cloudflare Inc. συμμετέχουν στο πλαίσιο EU-US Data Privacy Framework (DPF), παρέχοντας πρόσθετη εγγύηση μεταφοράς.",
        "da": "Nevumos hostinginfrastruktur er baseret i USA. Alle overførsler uden for Det Europæiske Økonomiske Samarbejdsområde (EØS) er beskyttet af standardkontraktbestemmelser (SCC) godkendt af Europa-Kommissionen. Derudover deltager Google LLC og Cloudflare Inc. i EU-US Data Privacy Framework (DPF), som giver yderligere overførselsgaranti.",
        "sv": "Nevumos hostinginfrastruktur är baserad i USA. Alla överföringar utanför Europeiska ekonomiska samarbetsområdet (EES) skyddas av standardavtalsklausuler (SCC) som godkänts av Europeiska kommissionen. Dessutom deltar Google LLC och Cloudflare Inc. i EU-US Data Privacy Framework (DPF), vilket ger ytterligare skydd vid överföringar.",
        "no": "Nevumos hostinginfrastruktur er basert i USA. Alle overføringer utenfor Det europeiske økonomiske samarbeidsområdet (EØS) er sikret ved hjelp av standardkontraktklausuler (SCC) som er godkjent av EU-kommisjonen. I tillegg deltar Google LLC og Cloudflare Inc. i EU-US Data Privacy Framework (DPF), som gir ytterligere overføringsbeskyttelse.",
        "fi": "Nevumon hosting-infrastruktuuri sijaitsee Yhdysvalloissa. Kaikki siirrot Euroopan talousalueen (ETA) ulkopuolelle on turvattu Euroopan komission hyväksymillä vakiosopimuslausekkeilla (SCC). Lisäksi Google LLC ja Cloudflare Inc. osallistuvat EU–US Data Privacy Framework -kehykseen (DPF), mikä tarjoaa lisäsuojan siirroille.",
        "et": "Nevumo hostimistaristu asub Ameerika Ühendriikides. Kõik Euroopa Majanduspiirkonnast (EMP) väljapoole toimuvad edastused on kaitstud Euroopa Komisjoni heakskiidetud standardsete lepingutingimustega (SCC). Lisaks osalevad Google LLC ja Cloudflare Inc. EL–USA andmeprivaatsuse raamistikus (DPF), mis pakub täiendavat edastuskaitsemeedet.",
        "lv": "Nevumo hostinga infrastruktūra atrodas Amerikas Savienotajās Valstīs. Visi pārsūtījumi ārpus Eiropas Ekonomikas zonas (EEZ) tiek aizsargāti ar Eiropas Komisijas apstiprinātajiem standarta līguma noteikumiem (SCC). Turklāt Google LLC un Cloudflare Inc. piedalās ES–ASV datu privātuma satvarā (DPF), nodrošinot papildu pārsūtīšanas aizsardzību.",
        "lt": "Nevumo prieglobos infrastruktūra yra Jungtinėse Amerikos Valstijose. Visi duomenų perdavimai už Europos ekonominės erdvės (EEE) ribų yra apsaugoti Europos Komisijos patvirtintomis standartinėmis sutarties sąlygomis (SSS). Be to, Google LLC ir Cloudflare Inc. dalyvauja ES–JAV duomenų privatumo sistemoje (DPF), suteikdamos papildomą perdavimo apsaugą.",
        "ga": "Tá bonneagar óstála Nevumo lonnaithe i Stáit Aontaithe Mheiriceá. Tá gach aistriú lasmuigh den Limistéar Eorpach Eacnamaíoch (LEE) á chosaint ag Clásail Chonarthacha Caighdeánacha (SCC) a d'fhormheas an Coimisiún Eorpach. Ina theannta sin, glacann Google LLC agus Cloudflare Inc. páirt i gCreat Príobháideachais Sonraí AE-SAM (DPF), rud a sholáthraíonn cosaint bhreise aistrithe.",
        "is": "Hýsingarinnviðir Nevumo eru staðsettir í Bandaríkjunum. Allar millifærslur utan Evrópska efnahagssvæðisins (EES) eru tryggðar með stöðluðum samningsákvæðum (SCC) sem samþykkt hafa verið af framkvæmdastjórn Evrópusambandsins. Að auki taka Google LLC og Cloudflare Inc. þátt í gagnafriðarreglum ESB–Bandaríkjanna (DPF), sem veitir frekari flutningsvörn.",
        "lb": "D'Hosting-Infrastruktur vun Nevumo ass an den USA. All Transferen ausserhalb vum Europäesche Wirtschaftsraum (EWR) sinn duerch vun der Europäescher Kommissioun geneemegten Standardvertragsklauselen (SCC) ofgesechert. Zousätzlech huelen Google LLC a Cloudflare Inc. um EU-USA Dateschutzrahmen (DPF) teil, deen eng zousätzlech Transfergarantie bitt.",
        "mk": "Хостинг инфраструктурата на Nevumo е базирана во Соединетите Американски Држави. Сите трансфери надвор од Европскиот економски простор (ЕЕП) се заштитени со Стандардни договорни клаузули (СДК) одобрени од Европската комисија. Дополнително, Google LLC и Cloudflare Inc. учествуваат во рамката ЕУ–САД за заштита на приватноста на податоците (DPF), обезбедувајќи дополнителна заштита при преносот.",
        "sq": "Infrastruktura e pritjes së Nevumo ndodhet në Shtetet e Bashkuara. Të gjitha transfertat jashtë Zonës Ekonomike Europiane (ZEE) mbrohen nga Klauzolat Standarde Kontraktuale (SCC) të miratuara nga Komisioni Europian. Për më tepër, Google LLC dhe Cloudflare Inc. marrin pjesë në Kuadrin e Privatësisë së të Dhënave BE-SHBA (DPF), duke siguruar mbrojtje shtesë të transfertave.",
        "mt": "L-infrastruttura tal-hosting ta' Nevumo hija bbażata fl-Istati Uniti. It-trasferimenti kollha barra miż-Żona Ekonomika Ewropea (ŻEE) huma mħarsa minn Klawżoli Kuntrattwali Standard (SCC) approvati mill-Kummissjoni Ewropea. Barra minn hekk, Google LLC u Cloudflare Inc. jipparteċipaw fil-Qafas tal-Privatezza tad-Data bejn l-UE u l-USA (DPF), li jipprovdi salvagwardja addizzjonali għat-trasferimenti.",
    },
    "s8_col_recipient": {
        "en": "Recipient", "pl": "Odbiorca", "bg": "Получател", "de": "Empfänger",
        "fr": "Destinataire", "es": "Destinatario", "it": "Destinatario",
        "pt": "Destinatário", "pt-PT": "Destinatário", "nl": "Ontvanger",
        "cs": "Příjemce", "sk": "Príjemca", "hu": "Fogadó fél", "ro": "Destinatar",
        "hr": "Primatelj", "sr": "Primalac", "sl": "Prejemnik",
        "uk": "Одержувач", "ru": "Получатель", "tr": "Alıcı",
        "el": "Παραλήπτης", "da": "Modtager", "sv": "Mottagare", "no": "Mottaker",
        "fi": "Vastaanottaja", "et": "Saaja", "lv": "Saņēmējs", "lt": "Gavėjas",
        "ga": "Faighteoir", "is": "Móttakandi", "lb": "Empfänger",
        "mk": "Примач", "sq": "Marrësi", "mt": "Destinatarju",
    },
    "s8_col_country": {
        "en": "Country", "pl": "Kraj", "bg": "Държава", "de": "Land",
        "fr": "Pays", "es": "País", "it": "Paese", "pt": "País",
        "pt-PT": "País", "nl": "Land", "cs": "Země", "sk": "Krajina",
        "hu": "Ország", "ro": "Țară", "hr": "Zemlja", "sr": "Zemlja",
        "sl": "Država", "uk": "Країна", "ru": "Страна", "tr": "Ülke",
        "el": "Χώρα", "da": "Land", "sv": "Land", "no": "Land",
        "fi": "Maa", "et": "Riik", "lv": "Valsts", "lt": "Šalis",
        "ga": "Tír", "is": "Land", "lb": "Land",
        "mk": "Земја", "sq": "Vendi", "mt": "Pajjiż",
    },
    "s8_col_protection": {
        "en": "Safeguard", "pl": "Zabezpieczenie", "bg": "Защита",
        "de": "Schutzmaßnahme", "fr": "Garantie", "es": "Garantía",
        "it": "Garanzia", "pt": "Garantia", "pt-PT": "Garantia",
        "nl": "Waarborg", "cs": "Záruka", "sk": "Záruka", "hu": "Biztosíték",
        "ro": "Garanție", "hr": "Zaštitna mjera", "sr": "Zaštitna mera",
        "sl": "Zaščitni ukrep", "uk": "Захід захисту", "ru": "Гарантия защиты",
        "tr": "Güvence", "el": "Διασφάλιση", "da": "Sikringsforanstaltning",
        "sv": "Skyddsåtgärd", "no": "Sikringstiltak", "fi": "Suojatoimi",
        "et": "Kaitsemeede", "lv": "Aizsardzības pasākums", "lt": "Apsaugos priemonė",
        "ga": "Coimirce", "is": "Verndarráðstöfun", "lb": "Schutzmoossnam",
        "mk": "Заштитна мерка", "sq": "Masë mbrojtëse", "mt": "Salvagwardja",
    },
}


def seed():
    with engine.begin() as conn:
        count = 0
        for key, lang_map in TRANSLATIONS.items():
            db_key = f"{NAMESPACE}.{key}"
            for lang, value in lang_map.items():
                conn.execute(
                    text("""
                        INSERT INTO translations (lang, key, value)
                        VALUES (:lang, :key, :value)
                        ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
                    """),
                    {"lang": lang, "key": db_key, "value": value},
                )
                count += 1
        print(f"[seed_cookies_p22] Upserted {count} rows.")


if __name__ == "__main__":
    seed()
