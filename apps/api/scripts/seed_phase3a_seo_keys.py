#!/usr/bin/env python3
"""
Seed script to add Phase 3A SEO keys for all 34 languages
Keys: category.seo_massage_h2, category.seo_plumbing_h2, category.seo_cleaning_p1
Run: docker exec nevumo-api python -m apps.api.scripts.seed_phase3a_seo_keys
"""
from sqlalchemy import text
from apps.api.database import SessionLocal

PHASE3A_TRANSLATIONS = {
    "bg": {
        "category.seo_massage_h2": "Масаж във {city} — какво си заслужава да знаете?",
        "category.seo_plumbing_h2": "Водопровод във {city} — какво си заслужава да знаете?",
        "category.seo_plumbing_p1": "Спешен водопроводен проблем изисква бърза реакция. В Nevumo ще намерите проверени водопроводчици в {city}, достъпни дори за спешни работи. Безплатна заявка, бърз отговор.",
        "category.seo_cleaning_p1": "{city} предлага широк избор от професионални специалисти по почистване за домовете, апартаментите и офисите. На Nevumo ще намерите проверени професионалисти, достъпни в целия {city}.",
    },
    "cs": {
        "category.seo_massage_h2": "Masáž v {city} — co stojí za to vědět?",
        "category.seo_plumbing_h2": "Instalatérství v {city} — co stojí za to vědět?",
        "category.seo_plumbing_p1": "Porucha instalatérství vyžaduje rychlou reakci. Na Nevumo najdete ověřené instalatéry v {city}, dostupné i pro nouzové práce. Bezplatná žádost, rychlá odpověď.",
        "category.seo_cleaning_p1": "{city} nabízí široký výběr profesionálních specialistů na úklid pro domy, byty a kanceláře. Na Nevumo najdete ověřené profesionály dostupné v celém {city}.",
    },
    "da": {
        "category.seo_massage_h2": "Massage i {city} — hvad er værd at vide?",
        "category.seo_plumbing_h2": "VVS-arbejde i {city} — hvad er værd at vide?",
        "category.seo_plumbing_p1": "En VVS-nødsituation kræver hurtig reaktion. På Nevumo finder du pålidelige VVS-installatører i {city}, også til akutte opgaver. Gratis forespørgsel, hurtigt svar.",
        "category.seo_cleaning_p1": "{city} tilbyder et bredt udvalg af professionelle rengøringsspecialister til hjem, lejligheder og kontorer. På Nevumo finder du verificerede fagfolk tilgængelige i hele {city}.",
    },
    "de": {
        "category.seo_massage_h2": "Massage in {city} — was sollte man wissen?",
        "category.seo_plumbing_h2": "Sanitär in {city} — was sollte man wissen?",
        "category.seo_plumbing_p1": "Ein Sanitärnotfall erfordert eine schnelle Reaktion. Auf Nevumo finden Sie verifizierte Installateure in {city}, auch für Notfälle. Kostenlose Anfrage, schnelle Antwort.",
        "category.seo_cleaning_p1": "{city} bietet eine breite Auswahl professioneller Reinigungsspezialisten für Häuser, Wohnungen und Büros. Auf Nevumo finden Sie verifizierte Fachleute in ganz {city}.",
    },
    "el": {
        "category.seo_massage_h2": "Μασάζ στο {city} — τι αξίζει να γνωρίζετε;",
        "category.seo_plumbing_h2": "Υδραυλικά στο {city} — τι αξίζει να γνωρίζετε;",
        "category.seo_plumbing_p1": "Μια υδραυλική έκτακτη ανάγκη απαιτεί γρήγορη αντίδραση. Στο Nevumo θα βρείτε επαληθευμένους υδραυλικούς στο {city}, διαθέσιμους ακόμη και για επείγουσες εργασίες. Δωρεάν αίτημα, γρήγορη απάντηση.",
        "category.seo_cleaning_p1": "Η {city} προσφέρει μια ευρεία επιλογή επαγγελματιών καθαρισμού για σπίτια, διαμερίσματα και γραφεία. Στο Nevumo θα βρείτε επαληθευμένους επαγγελματίες διαθέσιμους σε όλη την {city}.",
    },
    "en": {
        "category.seo_massage_h2": "Massage in {city} — what is worth knowing?",
        "category.seo_plumbing_h2": "Plumbing in {city} — what is worth knowing?",
        "category.seo_plumbing_p1": "A plumbing emergency requires a quick response. On Nevumo you will find trusted plumbers in {city} available even for urgent jobs. Free request, fast response.",
        "category.seo_cleaning_p1": "{city} offers a wide selection of professional cleaning specialists for homes, apartments, and offices. On Nevumo you will find verified professionals available throughout {city}.",
    },
    "es": {
        "category.seo_massage_h2": "Masaje en {city} — ¿qué vale la pena saber?",
        "category.seo_plumbing_h2": "Fontanería en {city} — ¿qué vale la pena saber?",
        "category.seo_plumbing_p1": "Una emergencia de fontanería requiere una respuesta rápida. En Nevumo encontrará fontaneros de confianza en {city} disponibles incluso para trabajos urgentes. Solicitud gratuita, respuesta rápida.",
        "category.seo_cleaning_p1": "{city} ofrece una amplia selección de especialistas en limpieza profesionales para hogares, apartamentos y oficinas. En Nevumo encontrará profesionales verificados disponibles en toda {city}.",
    },
    "et": {
        "category.seo_massage_h2": "Massaaž linnas {city} — mida tasub teada?",
        "category.seo_plumbing_h2": "Torustiköök linnas {city} — mida tasub teada?",
        "category.seo_plumbing_p1": "Torustiköö probleem nõuab kiiret reaktsiooni. Nevumost leiate kontrollitud torustiköötjad linnas {city}, kellel on võimalus teha ka kiireid töid. Tasuta päring, kiire vastus.",
        "category.seo_cleaning_p1": "{city} pakub laia valiku professionaalseid puhastusspetsialiste kodude, korterite ja kontorite jaoks. Nevumost leiate kontrollitud spetsialistid, kes on kättesaadavad kogu {city}.",
    },
    "fi": {
        "category.seo_massage_h2": "Hieronta kaupungissa {city} — mitä kannattaa tietää?",
        "category.seo_plumbing_h2": "LVI-työt kaupungissa {city} — mitä kannattaa tietää?",
        "category.seo_plumbing_p1": "LVI-hätätilanne vaatii nopean toiminnan. Nevumosta löydät luotettuja LVI-ammattilaisia kaupungissa {city}, jotka ovat saatavilla myös kiireellisiin töihin. Ilmainen pyyntö, nopea vastaus.",
        "category.seo_cleaning_p1": "{city} tarjoaa laajan valikoiman ammattimaisia siivousalan asiantuntijoita koteihin, asuntoihin ja toimistoihin. Nevumosta löydät vahvistetut ammattilaiset, jotka ovat saatavilla koko {city}.",
    },
    "fr": {
        "category.seo_massage_h2": "Massage à {city} — que faut-il savoir ?",
        "category.seo_plumbing_h2": "Plomberie à {city} — que faut-il savoir ?",
        "category.seo_plumbing_p1": "Une urgence de plomberie nécessite une réponse rapide. Sur Nevumo, vous trouverez des plombiers de confiance à {city} disponibles même pour les travaux d'urgence. Demande gratuite, réponse rapide.",
        "category.seo_cleaning_p1": "{city} offre un large choix de spécialistes du nettoyage professionnels pour les maisons, les appartements et les bureaux. Sur Nevumo, vous trouverez des professionnels vérifiés disponibles dans toute la {city}.",
    },
    "ga": {
        "category.seo_massage_h2": "Maiseadh i {city} — cad is fiú a bheith ar eolas agat?",
        "category.seo_plumbing_h2": "Pliombléireacht i {city} — cad is fiú a bheith ar eolas agat?",
        "category.seo_plumbing_p1": "Éigeandacht pliombléireachta tá gá le freagra tapa. Ar Nevumo gheobhaidh tú plumbéirí iontaofa i {city} atá ar fáil fiú le hoibreacha éigeandála. Iarratas saor in aisce, freagra tapa.",
        "category.seo_cleaning_p1": "Tairgeann {city} rogha leathan de speisialteoirí glantacháin gairmiúla do dhíonta, árasáin agus oifigí. Ar Nevumo gheobhaidh tú gairmithe fíoraithe atá ar fáil ar fud na {city}.",
    },
    "hr": {
        "category.seo_massage_h2": "Masáža u {city} — što vrijedi znati?",
        "category.seo_plumbing_h2": "Vodoinstalacije u {city} — što vrijedi znati?",
        "category.seo_plumbing_p1": "Hitna situacija s vodoinstalacijama zahtijeva brz odgovor. Na Nevumo ćete pronaći provjerene vodoinstalatere u {city}, dostupne čak i za hitne poslove. Besplatni zahtjev, brz odgovor.",
        "category.seo_cleaning_p1": "{city} nudi širok izbor stručnjaka za čišćenje za kuće, stanove i uredske prostore. Na Nevumo ćete pronaći provjerene stručnjake dostupne u cijelom {city}.",
    },
    "hu": {
        "category.seo_massage_h2": "Masszázs {city} városában — mit érdemes tudni?",
        "category.seo_plumbing_h2": "Vízvezeték-szerelés {city} városában — mit érdemes tudni?",
        "category.seo_plumbing_p1": "Vízvezeték-szerelési vészhelyzet gyors reagálást igényel. A Nevumón ellenőrzött vízvezeték-szerelőket találhat {city} városában, akik akár sürgős munkákra is elérhetők. Ingyenes kérés, gyors válasz.",
        "category.seo_cleaning_p1": "{city} városában széles választékban érhetők el professzionális takarítási szakemberek otthonok, lakások és irodák számára. A Nevumón ellenőrzött szakembereket találhat, akik az egész {city} területén elérhetők.",
    },
    "is": {
        "category.seo_massage_h2": "Nudd í {city} — hvað er vert að vita?",
        "category.seo_plumbing_h2": "Pípunagerð í {city} — hvað er vert að vita?",
        "category.seo_plumbing_p1": "Pípunagerðarvandamál krefst fljóts viðbragðs. Á Nevumo muntuðu finna staðfesta pípunagerðarmenn í {city} sem tiltækir eru jafnvel fyrir brýnar verk. Ókeypis beiðni, fljót svar.",
        "category.seo_cleaning_p1": "{city} býður upp á víðtækt úrval fagaðila í hreinsun fyrir heima, íbúðir og skrifstofur. Á Nevumo muntuðu finna staðfesti fagsplitsmenn sem tiltækir eru í öllu {city}.",
    },
    "it": {
        "category.seo_massage_h2": "Massaggio a {city} — cosa vale la pena sapere?",
        "category.seo_plumbing_h2": "Idraulica a {city} — cosa vale la pena sapere?",
        "category.seo_plumbing_p1": "Un'emergenza idraulica richiede una risposta rapida. Su Nevumo troverai idraulici fidati a {city} disponibili anche per lavori urgenti. Richiesta gratuita, risposta rapida.",
        "category.seo_cleaning_p1": "{city} offre una vasta selezione di specialisti di pulizia professionale per case, appartamenti e uffici. Su Nevumo troverai professionisti verificati disponibili in tutta {city}.",
    },
    "lb": {
        "category.seo_massage_h2": "Massage zu {city} — wat ass gutt ze wëssen?",
        "category.seo_plumbing_h2": "Sanitär zu {city} — wat ass gutt ze wëssen?",
        "category.seo_plumbing_p1": "Eng Sanitärnoutsetz brauch eng séier Reaktioun. Op Nevumo fan dir verifizéiert Sanitärinstallateuren zu {city}, déi och fir dréngend Aarbechten disponibel sinn. Gratis Ufro, séier Äntwert.",
        "category.seo_cleaning_p1": "{city} bitt eng breet Auswiel vu professionelle Reinigungsspezialisten fir Haiser, Wunnengen a Büros. Op Nevumo fan dir verifizéiert Fachleit, déi an der ganzer {city} verfügbar sinn.",
    },
    "lt": {
        "category.seo_massage_h2": "Masažas mieste {city} — ką verta žinoti?",
        "category.seo_plumbing_h2": "Vandentiekio mieste {city} — ką verta žinoti?",
        "category.seo_plumbing_p1": "Vandentiekio avarija reikalauja greito atsakymo. Nevumo svetainėje rasite patikrintus vadytojus mieste {city}, galinčius atlikti net skubius darbus. Nemokamas prašymas, greitas atsakymas.",
        "category.seo_cleaning_p1": "{city} siūlo platų profesionalių valymo specialistų pasirinkimą namams, butams ir biurams. Nevumo svetainėje rasite patikrintus specialistus, prieinamus visame {city}.",
    },
    "lv": {
        "category.seo_massage_h2": "Masāža pilsētā {city} — ko vērts zināt?",
        "category.seo_plumbing_h2": "Santehnikas pakalpojumi {city} — ko vērts zināt?",
        "category.seo_plumbing_p1": "Santehnikas avārija prasa ātru reakciju. Nevumo platformā atradīsiet pārbaudītus santehniķus pilsētā {city}, kas pieejami arī steidzamiem darbiem. Bezmaksas pieprasījums, ātra atbilde.",
        "category.seo_cleaning_p1": "{city} piedāvā plašu profesionālu tīrīšanas speciālistu izvēli mājām, dzīvokļiem un birojiem. Nevumo platformā atradīsiet pārbaudītus profesionāļus pieejamus visā {city}.",
    },
    "mk": {
        "category.seo_massage_h2": "Масажа во {city} — што вреди да се знае?",
        "category.seo_plumbing_h2": "Водовод во {city} — што вреди да се знае?",
        "category.seo_plumbing_p1": "Водоводна итна состојба бара брз одговор. На Nevumo ќе најдете проверени водоводџии во {city}, достапни дури и за итни работи. Безплатно барање, брз одговор.",
        "category.seo_cleaning_p1": "{city} нуди широк избор на професионални специјалисти за чистење за домови, станови и канцеларии. На Nevumo ќе најдете проверени професионалци достапни низ целата {city}.",
    },
    "mt": {
        "category.seo_massage_h2": "Massaġġ f'{city} — x'ta' min ikun jaf?",
        "category.seo_plumbing_h2": "Plumbing f'{city} — x'ta' min ikun jaf?",
        "category.seo_plumbing_p1": "Sitwazzjoni ta' plumbing taħtieġ risposti rapida. Fuq Nevumo ssib plumbers fiduċjużi f'{city} disponibbli anke għal xogħolijiet ta' urġenza. Talba bla ħlas, risposti rapida.",
        "category.seo_cleaning_p1": "{city} joffri għażla wiesgħa ta' speċjalisti professjonali tat-tindif għad-djar, appartamenti u uffiċċji. Fuq Nevumo ssib professjonisti vverifikati disponibbli madwar {city}.",
    },
    "nl": {
        "category.seo_massage_h2": "Massage in {city} — wat is handig om te weten?",
        "category.seo_plumbing_h2": "Loodgieterswerk in {city} — wat is handig om te weten?",
        "category.seo_plumbing_p1": "Een loodgietersnoodsituatie vereist een snelle reactie. Op Nevumo vindt u betrouwbare loodgieters in {city}, zelfs voor spoedklussen. Gratis aanvraag, snel antwoord.",
        "category.seo_cleaning_p1": "{city} biedt een breed scala aan professionele schoonmaakspecialisten voor huizen, appartementen en kantoren. Op Nevumo vindt u geverifieerde professionals beschikbaar in heel {city}.",
    },
    "no": {
        "category.seo_massage_h2": "Massasje i {city} — hva er verdt å vite?",
        "category.seo_plumbing_h2": "Rørleggertjenester i {city} — hva er verdt å vite?",
        "category.seo_plumbing_p1": "En rørleggerkrise krever rask respons. På Nevumo finner du pålitelige rørleggere i {city}, tilgjengelige selv for haster. Gratis forespørsel, raskt svar.",
        "category.seo_cleaning_p1": "{city} tilbyr et bredt utvalg av profesjonelle renholdsspesialister for hjem, leiligheter og kontorer. På Nevumo finner du verifiserte fagfolk tilgjengelig over hele {city}.",
    },
    "pl": {
        "category.seo_massage_h2": "Masaż w {city} — co warto wiedzieć?",
        "category.seo_plumbing_h2": "Hydraulika w {city} — co warto wiedzieć?",
        "category.seo_plumbing_p1": "Awaria hydrauliczna wymaga szybkiej reakcji. Na Nevumo znajdziesz zaufanych hydraulików w {city}, dostępnych nawet do prac pilnych. Darmowe zapytanie, szybka odpowiedź.",
        "category.seo_cleaning_p1": "{city} oferuje szeroki wybór profesjonalnych specjalistów od sprzątania dla domów, mieszkań i biur. Na Nevumo znajdziesz zweryfikowanych specjalistów dostępnych w całym {city}.",
    },
    "pt": {
        "category.seo_massage_h2": "Massagem em {city} — o que vale a pena saber?",
        "category.seo_plumbing_h2": "Encanamento em {city} — o que vale a pena saber?",
        "category.seo_plumbing_p1": "Uma emergência de encanamento exige uma resposta rápida. No Nevumo você encontrará encanadores de confiança em {city}, disponíveis mesmo para trabalhos urgentes. Solicitação gratuita, resposta rápida.",
        "category.seo_cleaning_p1": "{city} oferece uma ampla seleção de especialistas em limpeza profissionais para casas, apartamentos e escritórios. No Nevumo você encontrará profissionais verificados disponíveis em toda {city}.",
    },
    "pt-PT": {
        "category.seo_massage_h2": "Massagem em {city} — o que vale a pena saber?",
        "category.seo_plumbing_h2": "Canalização em {city} — o que vale a pena saber?",
        "category.seo_plumbing_p1": "Uma emergência de canalização exige uma resposta rápida. No Nevumo encontrará canalizadores de confiança em {city}, disponíveis mesmo para trabalhos urgentes. Solicitação gratuita, resposta rápida.",
        "category.seo_cleaning_p1": "{city} oferece uma ampla seleção de especialistas em limpeza profissionais para casas, apartamentos e escritórios. No Nevumo encontrará profissionais verificados disponíveis em toda {city}.",
    },
    "ro": {
        "category.seo_massage_h2": "Masaj în {city} — ce merită să știți?",
        "category.seo_plumbing_h2": "Instalații sanitare în {city} — ce merită să știți?",
        "category.seo_plumbing_p1": "O urgență sanitară necesită un răspuns rapid. Pe Nevumo veți găsi instalatori de încredere în {city}, disponibili chiar și pentru lucrări urgente. Cerere gratuită, răspuns rapid.",
        "category.seo_cleaning_p1": "{city} oferă o selecție largă de specialiști în curățenie profesională pentru case, apartamente și birouri. Pe Nevumo veți găsi profesioniști verificați disponibili în toată {city}.",
    },
    "ru": {
        "category.seo_massage_h2": "Массаж в {city} — что стоит знать?",
        "category.seo_plumbing_h2": "Сантехника в {city} — что стоит знать?",
        "category.seo_plumbing_p1": "Сантехническая авария требует быстрого реагирования. На Nevumo вы найдете проверенных сантехников в {city}, доступных даже для срочных работ. Бесплатная заявка, быстрый ответ.",
        "category.seo_cleaning_p1": "{city} предлагает широкий выбор профессиональных специалистов по уборке для домов, квартир и офисов. На Nevumo вы найдете проверенных профессионалов, доступных по всему {city}.",
    },
    "sk": {
        "category.seo_massage_h2": "Masáž v {city} — čo sa oplatí vedieť?",
        "category.seo_plumbing_h2": "Inštalatérstvo v {city} — čo sa oplatí vedieť?",
        "category.seo_plumbing_p1": "Inštalačná havária vyžaduje rýchlu reakciu. Na Nevumo nájdete overených inštalatérov v {city}, dostupných aj pre núdzové práce. Bezplatná požiadavka, rýchla odpoveď.",
        "category.seo_cleaning_p1": "{city} ponúka široký výber profesionálnych špecialistov na upratovanie pre domy, byty a kancelárie. Na Nevumo nájdete overených profesionálov dostupných v celom {city}.",
    },
    "sl": {
        "category.seo_massage_h2": "Masaža v {city} — kaj je vredno vedeti?",
        "category.seo_plumbing_h2": "Vodovodne instalacije v {city} — kaj je vredno vedeti?",
        "category.seo_plumbing_p1": "Vodovodna nesreča zahteva hitro odzivanje. Na Nevumo boste našli preverjene vodovodarje v {city}, ki so na voljo tudi za nujne delo. Brezplačna zahteva, hiter odgovor.",
        "category.seo_cleaning_p1": "{city} ponuja široko izbiro profesionalnih specialistov za čiščenje za domove, stanovanja in pisarne. Na Nevumo boste našli preverjene strokovnjake, ki so na voljo po vsem {city}.",
    },
    "sq": {
        "category.seo_massage_h2": "Masazh në {city} — çfarë vlen të dini?",
        "category.seo_plumbing_h2": "Instalime hidraulike në {city} — çfarë vlen të dini?",
        "category.seo_plumbing_p1": "Një emergjencë hidraulike kërkon përgjigje të shpejtë. Në Nevumo do të gjeni specialistë hidraulikë të besuar në {city}, të disponueshëm edhe për punë të shpejtë. Kërkesë falas, përgjigje e shpejtë.",
        "category.seo_cleaning_p1": "{city} ofron një përzgjedhje të gjerë të specialistëve profesionistë të pastrimit për shtëpi, apartamente dhe zyra. Në Nevumo do të gjeni profesionistë të verifikuar në të gjithë {city}.",
    },
    "sr": {
        "category.seo_massage_h2": "Масажа у {city} — шта вреди знати?",
        "category.seo_plumbing_h2": "Водоинсталације у {city} — шта вреди знати?",
        "category.seo_plumbing_p1": "Водоинсталатерска хитна ситуација захтева брз одговор. На Nevumo ћете пронаћи проверене водоинсталатере у {city}, доступне чак и за хитне послове. Бесплатан захтев, брз одговор.",
        "category.seo_cleaning_p1": "{city} нуди широк избор стручњака за чишћење за куће, станове и канцеларије. На Nevumo ћете пронаћи проверене стручњаке доступне у целом {city}.",
    },
    "sv": {
        "category.seo_massage_h2": "Massage i {city} — vad är värt att veta?",
        "category.seo_plumbing_h2": "Rörmokeri i {city} — vad är värt att veta?",
        "category.seo_plumbing_p1": "En rörmokeri-nödsituation kräver snabb respons. På Nevumo hittar du pålitliga rörmokare i {city}, tillgängliga även för akuta jobb. Gratis förfrågan, snabbt svar.",
        "category.seo_cleaning_p1": "{city} erbjuder ett brett utbud av professionella städspecialister för hem, lägenheter och kontor. På Nevumo hittar du verifierade proffs som är tillgängliga i hela {city}.",
    },
    "tr": {
        "category.seo_massage_h2": "{city} bölgesinde masaj — neler bilinmeli?",
        "category.seo_plumbing_h2": "{city} bölgesinde tesisat — neler bilinmeli?",
        "category.seo_plumbing_p1": "Tesisat acil durumu hızlı bir yanıt gerektirir. Nevumo'da {city} bölgesinde acil işler için bile hazır güvenilir tesisatçılar bulabilirsiniz. Ücretsiz talep, hızlı yanıt.",
        "category.seo_cleaning_p1": "{city}, evler, daireler ve ofisler için profesyonel temizlik uzmanlarından oluşan geniş bir seçenek sunar. Nevumo'da tüm {city} genelinde onaylı profesyoneller bulabilirsiniz.",
    },
    "uk": {
        "category.seo_massage_h2": "Масаж у {city} — що варто знати?",
        "category.seo_plumbing_h2": "Сантехніка у {city} — що варто знати?",
        "category.seo_plumbing_p1": "Сантехнічна аварія вимагає швидкої реакції. На Nevumo ви знайдете перевірених сантехніків у {city}, доступних навіть для термінових робіт. Безкоштовний запит, швидка відповідь.",
        "category.seo_cleaning_p1": "{city} пропонує широкий вибір професійних спеціалістів з прибирання для будинків, квартир та офісів. На Nevumo ви знайдете перевірених фахівців, доступних у всьому {city}.",
    },
}

def main():
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()

def run_seed(db):
    print("Starting Phase 3A SEO keys seed...")
    
    total_inserted = 0
    for lang, translations in PHASE3A_TRANSLATIONS.items():
        for key, value in translations.items():
            db.execute(
                text("""
                    INSERT INTO translations (lang, key, value)
                    VALUES (:lang, :key, :value)
                    ON CONFLICT (lang, key)
                    DO UPDATE SET value = EXCLUDED.value
                """),
                {"lang": lang, "key": key, "value": value}
            )
            total_inserted += 1
            print(f"  Inserted: {lang} - {key}")
    
    db.commit()
    print(f"\n✓ Inserted/updated {total_inserted} translation rows for {len(PHASE3A_TRANSLATIONS)} languages")
    
    # Verify
    verify(db)

def verify(db):
    print("\n--- Verification ---")
    
    # Check seo_massage_h2
    massage_result = db.execute(text("""
        SELECT lang, value FROM translations
        WHERE key = 'category.seo_massage_h2'
        ORDER BY lang
    """)).fetchall()
    print(f"\nseo_massage_h2: {len(massage_result)} languages")
    for row in massage_result[:5]:
        print(f"  {row[0]}: {row[1][:50]}...")
    
    # Check seo_plumbing_h2
    plumbing_result = db.execute(text("""
        SELECT lang, value FROM translations
        WHERE key = 'category.seo_plumbing_h2'
        ORDER BY lang
    """)).fetchall()
    print(f"\nseo_plumbing_h2: {len(plumbing_result)} languages")
    for row in plumbing_result[:5]:
        print(f"  {row[0]}: {row[1][:50]}...")
    
    # Check seo_cleaning_p1
    cleaning_result = db.execute(text("""
        SELECT lang, value FROM translations
        WHERE key = 'category.seo_cleaning_p1'
        ORDER BY lang
    """)).fetchall()
    print(f"\nseo_cleaning_p1: {len(cleaning_result)} languages")
    for row in cleaning_result[:5]:
        print(f"  {row[0]}: {row[1][:50]}...")

if __name__ == "__main__":
    main()
