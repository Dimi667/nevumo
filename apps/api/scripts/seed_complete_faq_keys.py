#!/usr/bin/env python3
"""
Seed script to add complete FAQ keys (both prefixed and non-prefixed) for all 34 languages
Run: python -m apps.api.scripts.seed_complete_faq_keys
"""
from sqlalchemy import text
from apps.api.database import SessionLocal
from apps.api.i18n import SUPPORTED_LANGUAGES

# FAQ translations extracted from existing seed scripts
FAQ_TRANSLATIONS: list[dict] = [
    # Batch 1: seed_faq_batch1_v2.py
    {"lang": "bg", "translations": {"faq_cleaning_q1": "{category_name} в {city} — какво е важно да знаете?", "faq_cleaning_a1": "Професионални специалисти по {category_name} в {city} предлагат комплексни услуги за домове, апартаменти и офиси. В Nevumo ще намерите проверени професионалисти, налични в цяла {city}.", "faq_cleaning_q2": "Как да изберете специалист по {category_name}?", "faq_cleaning_a2": "При избор на специалист за {category_name} в {city}, обърнете внимание на отзивите, обхвата на услугите и опита на професионалистите.", "faq_cleaning_q3": "Колко струва {category_name} в {city}?", "faq_cleaning_a3": "Цените за {category_name} в {city} се определят от обема работа и започват от {min_price} до {max_price} {currency}. Нашите професионалисти гарантират чистота."}},
    {"lang": "en", "translations": {"faq_cleaning_q1": "{category_name} in {city} — what is worth knowing?", "faq_cleaning_a1": "Professional {category_name} specialists in {city} offer comprehensive services for homes, apartments, and offices. On Nevumo you will find verified professionals available throughout {city}.", "faq_cleaning_q2": "How to choose a {category_name} specialist?", "faq_cleaning_a2": "When choosing a {category_name} specialist in {city}, pay attention to client reviews, scope of services, and the expert's experience.", "faq_cleaning_q3": "How much does {category_name} cost in {city}?", "faq_cleaning_a3": "The price for {category_name} in {city} is determined by the scope of work and ranges from {min_price} to {max_price} {currency}. Our professionals guarantee cleanliness."}},
    {"lang": "de", "translations": {"faq_cleaning_q1": "{category_name} in {city} — was Sie wissen sollten?", "faq_cleaning_a1": "Professionelle {category_name}-Spezialisten in {city} bieten umfassende Dienstleistungen für Häuser, Wohnungen und Büros an. Auf Nevumo finden Sie geprüfte Profis, die in ganz {city} verfügbar sind.", "faq_cleaning_q2": "Wie wählt man einen {category_name}-Spezialisten aus?", "faq_cleaning_a2": "Achten Sie bei der Auswahl eines {category_name}-Spezialisten in {city} auf Kundenbewertungen, den Leistungsumfang und die Erfahrung des Profis.", "faq_cleaning_q3": "Was kostet {category_name} in {city}?", "faq_cleaning_a3": "Die Kosten für {category_name} in {city} hängen vom Arbeitsumfang ab und liegen zwischen {min_price} und {max_price} {currency}. Unsere Profis garantieren Sauberkeit."}},
    {"lang": "fr", "translations": {"faq_cleaning_q1": "{category_name} à {city} — ce qu'il faut savoir ?", "faq_cleaning_a1": "Des spécialistes professionnels du {category_name} à {city} proposent des services complets pour les maisons, appartements et bureaux. Sur Nevumo, vous trouverez des professionnels vérifiés disponibles dans tout {city}.", "faq_cleaning_q2": "Comment choisir un spécialiste en {category_name} ?", "faq_cleaning_a2": "Lors du choix d'un spécialiste en {category_name} à {city}, portez une attention particulière aux avis des clients, à l'étendue des services et à l'expérience.", "faq_cleaning_q3": "Combien coûte le {category_name} à {city} ?", "faq_cleaning_a3": "Les tarifs du {category_name} à {city} sont déterminés par l'ampleur des travaux et varient de {min_price} à {max_price} {currency}. Nos experts garantissent la propreté."}},
    {"lang": "es", "translations": {"faq_cleaning_q1": "{category_name} en {city}: ¿qué es importante saber?", "faq_cleaning_a1": "Especialistas profesionales de {category_name} en {city} ofrecen servicios integrales para hogares, apartamentos y oficinas. En Nevumo encontrará profesionales verificados disponibles en todo {city}.", "faq_cleaning_q2": "¿Cómo elegir un especialista en {category_name}?", "faq_cleaning_a2": "Al elegir un especialista en {category_name} en {city}, preste atención a las opiniones de los clientes, el alcance de los servicios y la experiencia profesional.", "faq_cleaning_q3": "¿Cuánto cuesta el {category_name} en {city}?", "faq_cleaning_a3": "Los precios de {category_name} en {city} se determinan por el volumen de trabajo y oscilan entre {min_price} y {max_price} {currency}. Garantizamos limpieza total."}},
    {"lang": "it", "translations": {"faq_cleaning_q1": "{category_name} a {city} — cosa è importante sapere?", "faq_cleaning_a1": "Specialisti professionisti di {category_name} a {city} offrono servizi completi per case, appartamenti e uffici. Su Nevumo troverai professionisti verificati disponibili in tutta {city}.", "faq_cleaning_q2": "Come scegliere uno specialista in {category_name}?", "faq_cleaning_a2": "Nella scelta di uno specialista in {category_name} a {city}, presta attenzione alle recensioni dei clienti, alla gamma di servizi e all'esperienza.", "faq_cleaning_q3": "Quanto costa il {category_name} a {city}?", "faq_cleaning_a3": "I costi per {category_name} a {city} sono determinati dall'entità del lavoro e vanno da {min_price} a {max_price} {currency}. I nostri esperti garantiscono il pulito."}},
    {"lang": "nl", "translations": {"faq_cleaning_q1": "{category_name} in {city} — wat u moet weten?", "faq_cleaning_a1": "Professionele {category_name}-specialisten in {city} bieden uitgebreide diensten voor huizen, appartementen en kantoren. Op Nevumo vindt u geverifieerde professionals die beschikbaar zijn in heel {city}.", "faq_cleaning_q2": "Hoe kiest u een {category_name}-specialist?", "faq_cleaning_a2": "Let bij het kiezen van een {category_name}-specialist in {city} op klantbeoordelingen, de omvang van de diensten en de ervaring van de expert.", "faq_cleaning_q3": "Wat kost {category_name} in {city}?", "faq_cleaning_a3": "De prijzen voor {category_name} in {city} worden bepaald door de omvang van het werk en liggen tussen {min_price} and {max_price} {currency}."}},
    {"lang": "pl", "translations": {"faq_cleaning_q1": "{category_name} w {city} — co warto wiedzieć?", "faq_cleaning_a1": "Profesjonalni specjaliści od {category_name} w {city} oferują kompleksowe usługi dla domów, mieszkań i biur. Na Nevumo znajdziesz sprawdzonych fachowców dostępnych w całym {city}.", "faq_cleaning_q2": "Jak wybrać specjalistę od {category_name}?", "faq_cleaning_a2": "Wybierając specjalistę od {category_name} w {city}, zwróć uwagę na opinie klientów, zakres usług oraz doświadczenie eksperta.", "faq_cleaning_q3": "Ile kosztuje {category_name} w {city}?", "faq_cleaning_a3": "Ceny za {category_name} w {city} zależą od zakresu prac i wahają się od {min_price} do {max_price} {currency}. Gwarantujemy nieskazitelną czystość."}},
    {"lang": "ro", "translations": {"faq_cleaning_q1": "{category_name} în {city} — ce merită să știi?", "faq_cleaning_a1": "Specialiști profesioniști în {category_name} din {city} oferă servicii complete pentru case, apartamente și birouri. Pe Nevumo veți găsi profesioniști verificați disponibili în tot orașul {city}.", "faq_cleaning_q2": "Cum să alegi un specialist în {category_name}?", "faq_cleaning_a2": "Când alegeți un specialist în {category_name} în {city}, acordați atenție recenziilor, gamei de servicii și experienței profesionale.", "faq_cleaning_q3": "Cât costă {category_name} în {city}?", "faq_cleaning_a3": "Prețurile pentru {category_name} în {city} sunt determinate de volumul de muncă și variază între {min_price} și {max_price} {currency}."}},
    {"lang": "ru", "translations": {"faq_cleaning_q1": "{category_name} в {city} — что важно знать?", "faq_cleaning_a1": "Профессиональные специалисты по {category_name} в {city} предлагают комплексные услуги для домов, квартир и офисов. На Nevumo вы найдете проверенных профи, доступных по всему {city}.", "faq_cleaning_q2": "Как выбрать специалиста по {category_name}?", "faq_cleaning_a2": "При выборе специалиста по {category_name} в {city}, обратите внимание на отзывы клиентов, объем услуг и опыт эксперта.", "faq_cleaning_q3": "Сколько стоит {category_name} в {city}?", "faq_cleaning_a3": "Цены на {category_name} в {city} определяются объемом работ и начинаются от {min_price} до {max_price} {currency}. Наши профи гарантируют чистоту."}},
    {"lang": "tr", "translations": {"faq_cleaning_q1": "{city} içinde {category_name} — bilmeniz gerekenler nelerdir?", "faq_cleaning_a1": "{city} şehrindeki profesyonel {category_name} uzmanları evler, daireler ve ofisler için kapsamlı hizmetler sunmaktadır. Nevumo'da {city} genelinde doğrulanmış profesyoneller bulacaksınız.", "faq_cleaning_q2": "Bir {category_name} uzmanı nasıl seçilir?", "faq_cleaning_a2": "{city} şehrinde bir {category_name} uzmanı seçerken müşteri yorumlarına, hizmet kapsamına ve uzman deneyimine dikkat edin.", "faq_cleaning_q3": "{city} içinde {category_name} maliyeti ne kadar?", "faq_cleaning_a3": "{city} içindeki {category_name} fiyatları iş kapsamına göre belirlenir ve {min_price} ile {max_price} {currency} arasındadır."}},
    {"lang": "uk", "translations": {"faq_cleaning_q1": "{category_name} у {city} — що варто знати?", "faq_cleaning_a1": "Професійні спеціалісти з {category_name} у {city} пропонують комплексні послуги для будинків, квартир та офісів. На Nevumo ви знайдете перевірених фахівців, доступних у всьому {city}.", "faq_cleaning_q2": "Як обрати спеціаліста з {category_name}?", "faq_cleaning_a2": "При виборі спеціаліста з {category_name} у {city} зверніть увагу на відгуки клієнтів, обсяг послуг та досвід фахівця.", "faq_cleaning_q3": "Скільки коштує {category_name} у {city}?", "faq_cleaning_a3": "Ціни на {category_name} у {city} визначаються обсягом робіт і становлять від {min_price} до {max_price} {currency}."}},
    # Batch 2: seed_faq_batch2.py
    {"lang": "cs", "translations": {"faq_cleaning_q1": "{category_name} v {city} — co je dobré vědět?", "faq_cleaning_a1": "Profesionální specialisté na {category_name} v {city} nabízejí komplexní služby pro domy, byty a kanceláře. Na Nevumo najdete ověřené profesionály dostupné v celém {city}.", "faq_cleaning_q2": "Jak vybrat specialistu na {category_name}?", "faq_cleaning_a2": "Při výběru specialisty na {category_name} v {city} věnujte pozornost recenzím klientů, rozsahu služeb a zkušenostem odborníka.", "faq_cleaning_q3": "Kolik stojí {category_name} v {city}?", "faq_cleaning_a3": "Ceny za {category_name} v {city} jsou určeny rozsahem prací a pohybují se od {min_price} do {max_price} {currency}."}},
    {"lang": "da", "translations": {"faq_cleaning_q1": "{category_name} i {city} — hvad er værd at vide?", "faq_cleaning_a1": "Professionelle {category_name}-specialister i {city} tilbyder omfattende tjenester til huse, lejligheder og kontorer. På Nevumo finder du verificerede fagfolk tilgængelige i hele {city}.", "faq_cleaning_q2": "Hvordan vælger man en {category_name}-specialist?", "faq_cleaning_a2": "Når du vælger en {category_name}-specialist i {city}, skal du være opmærksom på kundeanmeldelser, serviceomfang og ekspertens erfaring.", "faq_cleaning_q3": "Hvad koster {category_name} i {city}?", "faq_cleaning_a3": "Priserne for {category_name} i {city} bestemmes af arbejdets omfang og ligger mellem {min_price} og {max_price} {currency}."}},
    {"lang": "el", "translations": {"faq_cleaning_q1": "{category_name} σε {city} — τι αξίζει να γνωρίζετε;", "faq_cleaning_a1": "Οι επαγγελματίες ειδικοί {category_name} στο {city} προσφέρουν ολοκληρωμένες υπηρεσίες για σπίτια, διαμερίσματα και γραφεία. Στο Nevumo θα βρείτε επαληθευμένους επαγγελματίες διαθέσιμους σε όλο το {city}.", "faq_cleaning_q2": "Πώς να επιλέξετε έναν ειδικό {category_name};", "faq_cleaning_a2": "Κατά την επιλογή ενός ειδικού {category_name} στο {city}, δώστε προσοχή στις κριτικές πελατών, το εύρος των υπηρεσιών και την εμπειρία του επαγγελματία.", "faq_cleaning_q3": "Πόσο κοστίζει το {category_name} στο {city};", "faq_cleaning_a3": "Οι τιμές για {category_name} στο {city} καθορίζονται από το εύρος των εργασιών και κυμαίνονται από {min_price} έως {max_price} {currency}."}},
    {"lang": "et", "translations": {"faq_cleaning_q1": "{category_name} linnas {city} — mida tasub teada?", "faq_cleaning_a1": "Professionaalsed {category_name} spetsialistid linnas {city} pakuvad terviklikke teenuseid kodudele, korteritele ja kontoritele. Nevumost leiate kontrollitud professionaalid, kes on saadaval kogu {city} piirkonnas.", "faq_cleaning_q2": "Kuidas valida {category_name} spetsialisti?", "faq_cleaning_a2": "Valides {category_name} spetsialisti linnas {city}, pöörake tähelepanu klientide arvustustele, teenuste ulatusele ja eksperdi kogemustele.", "faq_cleaning_q3": "Kui palju maksab {category_name} linnas {city}?", "faq_cleaning_a3": "{category_name} hinnad linnas {city} määravad töö maht ja need jäävad vahemikku {min_price} kuni {max_price} {currency}."}},
    {"lang": "fi", "translations": {"faq_cleaning_q1": "{category_name} kaupungissa {city} — mitä on hyvä tietää?", "faq_cleaning_a1": "Ammattimaiset {category_name}-asiantuntijat kaupungissa {city} tarjoavat kattavia palveluita koteihin, asuntoihin ja toimistoihin. Nevumosta löydät vahvistetut ammattilaiset kaikkialla {city}.", "faq_cleaning_q2": "Miten valita {category_name}-asiantuntija?", "faq_cleaning_a2": "Valitessasi {category_name}-asiantuntijaa kaupungissa {city}, kiinnitä huomiota asiakasarvioihin, palveluiden laajuuteen ja asiantuntijan kokemukseen.", "faq_cleaning_q3": "Paljonko {category_name} maksaa kaupungissa {city}?", "faq_cleaning_a3": "{category_name} hinnat kaupungissa {city} määräytyvät työn laajuuden mukaan ja ovat välillä {min_price} – {max_price} {currency}."}},
    {"lang": "ga", "translations": {"faq_cleaning_q1": "{category_name} i {city} — cad is fiú a bheith ar eolas agat?", "faq_cleaning_a1": "Cuireann speisialtóirí gairmiúla {category_name} i {city} seirbhísí cuimsitheacha ar fáil do thithe, árasáin agus oifigí. Ar Nevumo gheobhaidh tú gairmithe fíoraithe ar fáil ar fud {city}.", "faq_cleaning_q2": "Conas speisialtóir {category_name} a roghnú?", "faq_cleaning_a2": "Agus speisialtóir {category_name} á roghnú agat i {city}, tabhair aird ar léirmheasanna custaiméirí, raon na seirbhísí agus taithí an taineolaí.", "faq_cleaning_q3": "Cé mhéad a chosnaíonn {category_name} i {city}?", "faq_cleaning_a3": "Is é raon na hoibre a chinneann na praghsanna do {category_name} i {city} agus bíonn siad idir {min_price} agus {max_price} {currency}."}},
    {"lang": "hr", "translations": {"faq_cleaning_q1": "{category_name} u {city} — što je važno znati?", "faq_cleaning_a1": "Profesionalni stručnjaci za {category_name} u {city} nude sveobuhvatne usluge za kuće, stanove i urede. Na Nevumo platformi pronaći ćete provjerene stručnjake dostupne u cijelom {city}.", "faq_cleaning_q2": "Kako odabrati stručnjaka za {category_name}?", "faq_cleaning_a2": "Pri odabiru stručnjaka za {category_name} u {city}, obratite pozornost na recenzije klijenata, opseg usluga i iskustvo stručnjaka.", "faq_cleaning_q3": "Koliko košta {category_name} u {city}?", "faq_cleaning_a3": "Cijene za {category_name} u {city} određene su opsegom posla i kreću se od {min_price} do {max_price} {currency}."}},
    {"lang": "hu", "translations": {"faq_cleaning_q1": "{category_name} {city} területén — mit érdemes tudni?", "faq_cleaning_a1": "A professzionális {category_name} szakemberek {city} területén átfogó szolgáltatásokat kínálnak házak, lakások és irodák számára. A Nevumo-n ellenőrzött szakembereket talál {city} egész területén.", "faq_cleaning_q2": "Hogyan válasszunk {category_name} szakembert?", "faq_cleaning_a2": "Amikor {category_name} szakembert választ {city} területén, figyeljen az ügyfélvéleményekre, a szolgáltatások körére és a szakember tapasztalatára.", "faq_cleaning_q3": "Mennyibe kerül a {category_name} {city} területén?", "faq_cleaning_a3": "A {category_name} árait {city} területén a munka volumene határozza meg, {min_price} és {max_price} {currency} között mozognak."}},
    {"lang": "is", "translations": {"faq_cleaning_q1": "{category_name} í {city} — hvað er gott að vita?", "faq_cleaning_a1": "Fagmenn í {category_name} í {city} bjóða upp á alhliða þjónustu fyrir heimili, íbúðir og skrifstofur. Á Nevumo finnur þú vottaða fagaðila um allt {city}.", "faq_cleaning_q2": "Hvernig á að velja sérfræðing í {category_name}?", "faq_cleaning_a2": "Þegar þú velur sérfræðing í {category_name} í {city} skaltu fylgjast með umsögnum viðskiptavina, umfangi þjónustu og reynslu fagaðila.", "faq_cleaning_q3": "Hvað kostar {category_name} í {city}?", "faq_cleaning_a3": "Verð fyrir {category_name} í {city} ræðst af umfangi verksins og er á bilinu {min_price} til {max_price} {currency}."}},
    {"lang": "lb", "translations": {"faq_cleaning_q1": "{category_name} zu {city} — wat ee wësse sollt?", "faq_cleaning_a1": "Professionell {category_name}-Spezialisten zu {city} bidden ëmfaassend Servicer fir Haiser, Appartementer a Büroen un. Op Nevumo fannt Dir iwwerpréift Fachleit an der ganzer {city}.", "faq_cleaning_q2": "Wéi wielt een en {category_name}-Spezialist?", "faq_cleaning_a2": "Wann Dir en {category_name}-Spezialist zu {city} wielt, oppasst op d'Client-Bewäertungen, den Ëmfang vum Service an d'Erfahrung vum Profi.", "faq_cleaning_q3": "Wat kascht {category_name} zu {city}?", "faq_cleaning_a3": "D'Präisser fir {category_name} zu {city} ginn duerch den Ëmfang vun der Aarbecht bestëmmt a leien tëscht {min_price} a {max_price} {currency}."}},
    {"lang": "lt", "translations": {"faq_cleaning_q1": "{category_name} mieste {city} - ką verta žinoti?", "faq_cleaning_a1": "Profesionalūs {category_name} specialistai mieste {city} siūlo kompleksines paslaugas namams, butams ir biurams. \"Nevumo\" rasite patikrintus profesionalus, dirbančius visame {city}.", "faq_cleaning_q2": "Kaip pasirinkti {category_name} specialistą?", "faq_cleaning_a2": "Renkantis {category_name} specialistą mieste {city}, atkreipkite dėmesį į klientų atsiliepimus, paslaugų apimtį ir specialisto patirtį.", "faq_cleaning_q3": "Kiek kainuoja {category_name} mieste {city}?", "faq_cleaning_a3": "{category_name} kainos mieste {city} priklauso nuo darbų apimties ir svyruoja nuo {min_price} iki {max_price} {currency}."}},
    # Batch 3: seed_faq_batch3_final.py
    {"lang": "lv", "translations": {"faq_cleaning_q1": "{category_name} pilsētā {city} — kas jāzina?", "faq_cleaning_a1": "Profesionāli {category_name} speciālisti pilsētā {city} piedāvā visaptverošus pakalpojumus mājām, dzīvokļiem un birojiem. Nevumo platformā atradīsiet pārbaudītus profesionāļus visā {city}.", "faq_cleaning_q2": "Kā izvēlēties {category_name} speciālistu?", "faq_cleaning_a2": "Izvēloties {category_name} speciālistu pilsētā {city}, pievērsiet uzmanību atsauksmēm, pakalpojumu klāstam un eksperta pieredzei.", "faq_cleaning_q3": "Cik maksā {category_name} pilsētā {city}?", "faq_cleaning_a3": "{category_name} cenas pilsētā {city} nosaka darba apjoms, un tās ir no {min_price} līdz {max_price} {currency}."}},
    {"lang": "mk", "translations": {"faq_cleaning_q1": "{category_name} во {city} — што треба да знаете?", "faq_cleaning_a1": "Професионални специјалисти за {category_name} во {city} нудат сеопфатни услуги за куќи, станови и канцеларии. На Nevumo ќе најдете проверени професионалци достапни низ цела {city}.", "faq_cleaning_q2": "Како да изберете специјалист за {category_name}?", "faq_cleaning_a2": "При избор на специјалист за {category_name} во {city}, обрнете внимание на препораките, опсегот на услуги и искуството на експертот.", "faq_cleaning_q3": "Колку чини {category_name} во {city}?", "faq_cleaning_a3": "Цените за {category_name} во {city} се одредуваат според обемот на работа и се движат од {min_price} до {max_price} {currency}."}},
    {"lang": "mt", "translations": {"faq_cleaning_q1": "{category_name} f'{city} — x'inhu tajjeb li tkun taf?", "faq_cleaning_a1": "Speċjalisti professjonali tal-{category_name} f'{city} joffru servizzi komprensivi għal djar, appartamenti u uffiċċji. Fuq Nevumo ssib professjonisti vverifikati disponibbli madwar {city}.", "faq_cleaning_q2": "Kif tagħżel speċjalista tal-{category_name}?", "faq_cleaning_a2": "Meta tagħżel speċjalista tal-{category_name} f'{city}, oqgħod attent għar-reviżjonijiet tal-klijenti, l-ambitu tas-servizzi u l-esperjenza tal-espert.", "faq_cleaning_q3": "Kemm jiswa l-{category_name} f'{city}?", "faq_cleaning_a3": "Il-prezzijiet għal {category_name} f'{city} huma determinati mill-ambitu tax-xogħol u jvarjaw minn {min_price} sa {max_price} {currency}."}},
    {"lang": "no", "translations": {"faq_cleaning_q1": "{category_name} i {city} — hva er verdt å vite?", "faq_cleaning_a1": "Profesjonelle {category_name}-spesialister i {city} tilbyr omfattende tjenester for hjem, leiligheter og kontorer. På Nevumo finner du verifiserte fagfolk tilgjengelig i hele {city}.", "faq_cleaning_q2": "Hvordan velge en {category_name}-spesialist?", "faq_cleaning_a2": "Når du velger en {category_name}-spesialist i {city}, vær oppmerksom på kundeanmeldelser, omfanget av tjenester og ekspertens erfaring.", "faq_cleaning_q3": "Hva koster {category_name} i {city}?", "faq_cleaning_a3": "Prisene for {category_name} i {city} bestemmes av arbeidets omfang og ligger mellom {min_price} og {max_price} {currency}."}},
    {"lang": "pt", "translations": {"faq_cleaning_q1": "{category_name} em {city} — o que é importante saber?", "faq_cleaning_a1": "Especialistas profissionais de {category_name} em {city} oferecem serviços abrangentes para casas, apartamentos e escritórios. No Nevumo você encontrará profissionais verificados disponíveis em toda a {city}.", "faq_cleaning_q2": "Como escolher um especialista em {category_name}?", "faq_cleaning_a2": "Ao escolher um especialista em {category_name} em {city}, preste atenção às avaliações dos clientes, ao escopo dos serviços e à experiência do profissional.", "faq_cleaning_q3": "Quanto custa o {category_name} em {city}?", "faq_cleaning_a3": "Os preços para {category_name} em {city} são determinados pelo volume de trabalho e variam de {min_price} a {max_price} {currency}."}},
    {"lang": "pt-PT", "translations": {"faq_cleaning_q1": "{category_name} em {city} — o que é importante saber?", "faq_cleaning_a1": "Especialistas profissionais de {category_name} em {city} oferecem serviços abrangentes para casas, apartamentos e escritórios. No Nevumo encontrará profissionais verificados disponíveis em toda a {city}.", "faq_cleaning_q2": "Como escolher um especialista em {category_name}?", "faq_cleaning_a2": "Ao escolher um especialista em {category_name} em {city}, preste atenção às avaliações dos clientes, ao âmbito dos serviços e à experiência do profissional.", "faq_cleaning_q3": "Quanto custa o {category_name} em {city}?", "faq_cleaning_a3": "Os preços para {category_name} em {city} são determinados pelo volume de trabalho e variam de {min_price} a {max_price} {currency}."}},
    {"lang": "sk", "translations": {"faq_cleaning_q1": "{category_name} v {city} — čo je dobré vedieť?", "faq_cleaning_a1": "Profesionálni špecialisti na {category_name} v {city} ponúkajú komplexné služby pre domy, byty a kancelárie. Na Nevumo nájdete overených profesionálov dostupných v celom {city}.", "faq_cleaning_q2": "Ako si vybrať špecialistu na {category_name}?", "faq_cleaning_a2": "Pri výbere špecialistu na {category_name} v {city} venujte pozornosť recenziám klientov, rozsahu služieb a skúsenostiam odborníka.", "faq_cleaning_q3": "Koľko stojí {category_name} v {city}?", "faq_cleaning_a3": "Ceny za {category_name} v {city} sú určené rozsahom prác a pohybujú sa od {min_price} do {max_price} {currency}."}},
    {"lang": "sl", "translations": {"faq_cleaning_q1": "{category_name} v {city} — kaj je dobro vedeti?", "faq_cleaning_a1": "Profesionalni strokovnjaki za {category_name} v {city} ponujajo celovite storitve za hiše, stanovanja in pisarne. Na Nevumo boste našli preverjene strokovnjake, ki so na voljo po vsem {city}.", "faq_cleaning_q2": "Kako izbrati strokovnjaka za {category_name}?", "faq_cleaning_a2": "Pri izbiri strokovnjaka za {category_name} v {city} bodite pozorni na ocene strank, obseg storitev in izkušnje strokovnjaka.", "faq_cleaning_q3": "Koliko stane {category_name} v {city}?", "faq_cleaning_a3": "Cene za {category_name} v {city} so določene z obsegom dela in se gibljejo od {min_price} do {max_price} {currency}."}},
    {"lang": "sq", "translations": {"faq_cleaning_q1": "{category_name} në {city} — çfarë duhet të dini?", "faq_cleaning_a1": "Specialistët profesionistë të {category_name} në {city} ofrojnë shërbime gjithëpërfshirëse për shtëpi, apartamente dhe zyra. Në Nevumo do të gjeni profesionistë të verifikuar në të gjithë {city}.", "faq_cleaning_q2": "Si të zgjidhni një specialist {category_name}?", "faq_cleaning_a2": "Kur zgjidhni një specialist {category_name} në {city}, kushtojini vëmendje rishikimeve të klientëve, fushëveprimit të shërbimeve dhe përvojës së ekspertit.", "faq_cleaning_q3": "Sa kushton {category_name} në {city}?", "faq_cleaning_a3": "Çmimet për {category_name} në {city} përcaktohen nga vëllimi i punës dhe lëvizin nga {min_price} deri në {max_price} {currency}."}},
    {"lang": "sr", "translations": {"faq_cleaning_q1": "{category_name} u {city} — šta je važno znati?", "faq_cleaning_a1": "Profesionalni stručnjaci za {category_name} u {city} nude sveobuhvatne usluge za kuće, stanove i kancelarije. Na Nevumo platformi ćete pronaći proverene stručnjake dostupne u celom {city}.", "faq_cleaning_q2": "Kako odabrati stručnjaka za {category_name}?", "faq_cleaning_a2": "Pri odabiru stručnjaka za {category_name} u {city}, obratite pažnju na recenzije klijenata, obim usluga i iskustvo stručnjaka.", "faq_cleaning_q3": "Koliko košta {category_name} u {city}?", "faq_cleaning_a3": "Cene za {category_name} u {city} određene su obimom posla i kreću se od {min_price} do {max_price} {currency}."}},
    {"lang": "sv", "translations": {"faq_cleaning_q1": "{category_name} i {city} — vad är bra att veta?", "faq_cleaning_a1": "Professionella {category_name}-specialister i {city} erbjuder heltäckande tjänster för hem, lägenheter och kontor. På Nevumo hittar du verifierade yrkesmän tillgängliga i hela {city}.", "faq_cleaning_q2": "Hur väljer man en {category_name}-specialist?", "faq_cleaning_a2": "När du väljer en {category_name}-specialist i {city}, var uppmärksam på kundrecensioner, tjänsternas omfattning och expertens erfarenhet.", "faq_cleaning_q3": "Vad kostar {category_name} i {city}?", "faq_cleaning_a3": "Priserna för {category_name} i {city} fastställs av arbetets omfattning och varierar från {min_price} do {max_price} {currency}."}},
]

# FAQ keys to process
FAQ_KEYS = [
    "faq_cleaning_q1",
    "faq_cleaning_a1",
    "faq_cleaning_q2",
    "faq_cleaning_a2",
    "faq_cleaning_q3",
    "faq_cleaning_a3",
]


def main():
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()


def run_seed(db):
    print("=== Seeding Complete FAQ Keys for All 34 Languages ===\n")
    
    # Step 1: Insert non-prefixed FAQ keys from existing seed scripts
    print("Step 1: Inserting non-prefixed FAQ keys...")
    insert_non_prefixed_faq_keys(db)
    
    # Step 2: Add prefixed FAQ keys for all 34 languages with fallback
    print("\nStep 2: Adding prefixed FAQ keys for all 34 languages...")
    add_prefixed_faq_keys(db)
    
    # Step 3: Verification
    print("\nStep 3: Verification...")
    verify_prefixed_keys(db)
    
    print("\n=== Seed Complete ===")


def insert_non_prefixed_faq_keys(db):
    """Insert non-prefixed FAQ keys from existing seed scripts"""
    count = 0
    for item in FAQ_TRANSLATIONS:
        lang = item["lang"]
        translations = item["translations"]
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
            count += 1
    db.commit()
    print(f"  Inserted/updated {count} non-prefixed FAQ translation rows")


def add_prefixed_faq_keys(db):
    """Add prefixed FAQ keys for all 34 languages with English fallback"""
    # Get English translations as fallback
    english_translations = {}
    for item in FAQ_TRANSLATIONS:
        if item["lang"] == "en":
            english_translations = item["translations"]
            break
    
    if not english_translations:
        print("  ERROR: English translations not found!")
        return
    
    # Query database for existing non-prefixed FAQ keys
    result = db.execute(
        text("""
            SELECT lang, key, value
            FROM translations
            WHERE key IN :keys
        """),
        {"keys": tuple(FAQ_KEYS)}
    )
    
    # Build dictionary of existing translations
    existing_translations = {}
    for row in result:
        lang, key, value = row
        if lang not in existing_translations:
            existing_translations[lang] = {}
        existing_translations[lang][key] = value
    
    # Insert prefixed keys for all 34 languages
    count = 0
    fallback_count = 0
    languages_with_fallback = []
    
    for lang in SUPPORTED_LANGUAGES:
        for key in FAQ_KEYS:
            prefixed_key = f"category.{key}"
            
            # Try to get translation from existing data, otherwise use English fallback
            if lang in existing_translations and key in existing_translations[lang]:
                value = existing_translations[lang][key]
            elif key in english_translations:
                value = english_translations[key]
                if lang not in languages_with_fallback:
                    languages_with_fallback.append(lang)
                fallback_count += 1
            else:
                print(f"  WARNING: No translation found for {key} in {lang} or English fallback")
                continue
            
            db.execute(
                text("""
                    INSERT INTO translations (lang, key, value)
                    VALUES (:lang, :key, :value)
                    ON CONFLICT (lang, key)
                    DO UPDATE SET value = EXCLUDED.value
                """),
                {"lang": lang, "key": prefixed_key, "value": value}
            )
            count += 1
    
    db.commit()
    print(f"  Inserted/updated {count} prefixed FAQ translation rows")
    
    if languages_with_fallback:
        print(f"  WARNING: Used English fallback for {len(languages_with_fallback)} languages:")
        print(f"    {', '.join(sorted(languages_with_fallback))}")
        print(f"  Total fallback entries: {fallback_count}")


def verify_prefixed_keys(db):
    """Verify all 34 languages have 6 prefixed FAQ keys"""
    result = db.execute(
        text("""
            SELECT lang, COUNT(*) as keys
            FROM translations
            WHERE key LIKE 'category.faq_cleaning_%'
            GROUP BY lang
            ORDER BY lang
        """)
    )
    
    rows = result.fetchall()
    
    print("\n  Prefixed FAQ keys by language:")
    languages_with_6_keys = []
    languages_incomplete = []
    
    for row in rows:
        lang, key_count = row
        if key_count == 6:
            languages_with_6_keys.append(lang)
            print(f"    {lang}: {key_count} keys ✓")
        else:
            languages_incomplete.append(lang)
            print(f"    {lang}: {key_count} keys ✗ (expected 6)")
    
    print(f"\n  Summary:")
    print(f"    Languages with complete 6 keys: {len(languages_with_6_keys)}/34")
    print(f"    Languages incomplete: {len(languages_incomplete)}")
    
    if languages_incomplete:
        print(f"    Incomplete languages: {', '.join(sorted(languages_incomplete))}")
    
    if len(languages_with_6_keys) == 34:
        print(f"\n  ✓ SUCCESS: All 34 languages have 6 prefixed FAQ keys!")
    else:
        print(f"\n  ✗ INCOMPLETE: Not all languages have 6 prefixed FAQ keys")


if __name__ == "__main__":
    main()
