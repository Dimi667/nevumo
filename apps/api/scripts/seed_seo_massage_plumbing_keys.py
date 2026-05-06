#!/usr/bin/env python3
"""
Seed script to add remaining SEO massage and plumbing keys for 34 languages (Phase 3B)
This is Part 2: 16 languages (lv through uk)
Run: python -m apps.api.scripts.seed_seo_massage_plumbing_keys
"""
from sqlalchemy import text
from apps.api.database import SessionLocal

def main():
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()

def run_seed(db):
    insert_translations(db, SEO_MASSAGE_PLUMBING_TRANSLATIONS_PART2)
    verify(db)

def insert_translations(db, data: dict[str, dict[str, str]]) -> None:
    count = 0
    for lang, keys in data.items():
        for key, value in keys.items():
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
    print(f"Inserted/updated {count} translation rows")

def verify(db) -> None:
    # Verify massage keys
    massage_result = db.execute(text("""
        SELECT lang, COUNT(*) as keys
        FROM translations
        WHERE key LIKE 'category.seo_massage%'
        GROUP BY lang
        ORDER BY lang
    """))
    massage_rows = massage_result.fetchall()
    print("\nSEO Massage Keys Verification:")
    for row in massage_rows:
        print(f"  {row[0]}: {row[1]} keys")

    # Verify plumbing keys
    plumbing_result = db.execute(text("""
        SELECT lang, COUNT(*) as keys
        FROM translations
        WHERE key LIKE 'category.seo_plumbing%'
        GROUP BY lang
        ORDER BY lang
    """))
    plumbing_rows = plumbing_result.fetchall()
    print("\nSEO Plumbing Keys Verification:")
    for row in plumbing_rows:
        print(f"  {row[0]}: {row[1]} keys")

    # Summary
    print(f"\nSummary: Updated {len(SEO_MASSAGE_PLUMBING_TRANSLATIONS_PART2)} languages")

SEO_MASSAGE_PLUMBING_TRANSLATIONS_PART2 = {
    "lv": {
        "category.seo_massage_h3_1": "Kā izvēlēties masāžas speciālistu?",
        "category.seo_massage_h3_2": "Cik maksā masāža {city}?",
        "category.seo_massage_p1": "{city} piedāvā plašu profesionālu masāžas speciālistu izvēli. Neatkarīgi no tā, vai meklējat relaksējošu, sporta vai terapeitisko masāžu, Nevumo palīdz atrast uzticamus speciālistus tuvumā.",
        "category.seo_massage_p2": "Pārbaudiet iepriekšējo klientu atsauksmes, speciālista pieredzi un piedāvāto pakalpojumu klāstu. Labs masāžas speciālists pielāgos tehniku jūsu vajadzībām.",
        "category.seo_massage_p3": "Profesionāla masāžas terapija stresa mazināšanai un labsajūtas uzlabošanai. Rezervējiet sesiju pie pieredzējušiem terapeitiem savā pilsētā.",
        "category.seo_plumbing_h2": "Santehnikas pakalpojumi {city} — ko ir vērts zināt?",
        "category.seo_plumbing_h3_1": "Kad saukt santehniķi?",
        "category.seo_plumbing_h3_2": "Cik maksā santehniķis {city}?",
        "category.seo_plumbing_p2": "Sauciet santehniķi ūdens sistēmas bojājumu, pilošu krānu, aizsērējušu noteku gadījumos, kā arī vannas istabas vai virtuves remonta laikā.",
        "category.seo_plumbing_p3": "Ekspertu santehnikas risinājumi jebkurai ārkārtas situācijai vai plānotam remontam. Ātra reakcija un garantēta kvalitāte no vietējiem speciālistiem."
    },
    "mk": {
        "category.seo_massage_h3_1": "Како да изберете специјалист за масажа?",
        "category.seo_massage_h3_2": "Колку чини масажа во {city}?",
        "category.seo_massage_p1": "{city} нуди широк избор на професионални специјалисти за масажа. Без разлика дали барате релаксирачка, спортска или терапевтска масажа, Nevumo ви помага да најдете доверливи професионалци во близина.",
        "category.seo_massage_p2": "Проверете ги прегледите од претходните клиенти, искуството на специјалистот и обемот на понудените услуги. Добриот специјалист за масажа ќе ја прилагоди техниката на вашите потреби.",
        "category.seo_massage_p3": "Професионална масажна терапија за ослободување од стресот и подобрување на вашата благосостојба. Резервирајте сесија кај искусни терапевти во вашиот град.",
        "category.seo_plumbing_h2": "Водовод во {city} — што вреди да се знае?",
        "category.seo_plumbing_h3_1": "Кога да повикате водоводџија?",
        "category.seo_plumbing_h3_2": "Колку чини водоводџија во {city}?",
        "category.seo_plumbing_p2": "Повикајте водоводџија за дефекти на водоводниот систем, славини што течат, затнати одводи и за време на реновирање на бања или кујна.",
        "category.seo_plumbing_p3": "Експертни водоводни решенија за какви било итни случаи или планирани поправки. Брза реакција и загарантиран квалитет од локални специјалисти."
    },
    "mt": {
        "category.seo_massage_h3_1": "Kif tagħżel speċjalista tal-massaġġi?",
        "category.seo_massage_h3_2": "Kemm jiswa massaġġ f' {city}?",
        "category.seo_massage_p1": "{city} joffri għażla wiesgħa ta' speċjalisti professjonali tal-massaġġi. Kemm jekk qed tfittex massaġġi rilassanti, sportivi, jew terapewtiċi, Nevumo jgħinek issib professjonisti fdati fil-qrib.",
        "category.seo_massage_p2": "Iċċekkja r-reviżjonijiet tal-klijenti preċedenti, l-esperjenza tal-ispeċjalista, u l-firxa ta' servizzi offruti. Speċjalista tal-massaġġi tajjeb jadatta t-teknika għall-bżonnijiet tiegħek.",
        "category.seo_massage_p3": "Terapija tal-massaġġi professjonali biex ittaffi l-istress u ttejjeb il-benessere tiegħek. Ibbukja sessjoni ma' terapeuti b'esperjenza fil-belt tiegħek.",
        "category.seo_plumbing_h2": "Plaming f' {city} — x'taf tajjeb tkun taf?",
        "category.seo_plumbing_h3_1": "Meta għandek iċċempel plamer?",
        "category.seo_plumbing_h3_2": "Kemm jiswa plamer f' {city}?",
        "category.seo_plumbing_p2": "Ċempel plamer għal ħsarat fis-sistema tal-ilma, viti li jqattru, katusi misduda, u waqt rinnovazzjonijiet tal-kamra tal-banju jew tal-kċina.",
        "category.seo_plumbing_p3": "Soluzzjonijiet tal-plaming esperti għal kwalunkwe emergenza jew tiswija ppjanata. Reazzjoni malajr u kwalità garantita minn speċjalisti lokali."
    },
    "nl": {
        "category.seo_massage_h3_1": "Hoe kies je een massagespecialist?",
        "category.seo_massage_h3_2": "Wat kost een massage in {city}?",
        "category.seo_massage_p1": "{city} biedt een brede selectie aan professionele massagespecialisten. Of je nu op zoek bent naar een ontspannende, sport- of therapeutische massage, Nevumo helpt je bij het vinden van vertrouwde professionals in de buurt.",
        "category.seo_massage_p2": "Bekijk beoordelingen van eerdere klanten, de ervaring van de specialist en het aanbod van diensten. Een goede massagespecialist past de techniek aan jouw behoeften aan.",
        "category.seo_massage_p3": "Professionele massagetherapie om stress te verlichten en je welzijn te verbeteren. Boek een sessie bij ervaren therapeuten in jouw stad.",
        "category.seo_plumbing_h2": "Loodgieterswerk in {city} — wat is handig om te weten?",
        "category.seo_plumbing_h3_1": "Wanneer moet je een loodgieter bellen?",
        "category.seo_plumbing_h3_2": "Wat kost een loodgieter in {city}?",
        "category.seo_plumbing_p2": "Bel een loodgieter bij storingen aan het watersysteem, lekkende kranen, verstopte afvoeren en tijdens badkamer- of keukenrenovaties.",
        "category.seo_plumbing_p3": "Deskundige loodgietersoplossingen voor elk noodgeval of geplande reparatie. Snelle reactie en gegarandeerde kwaliteit door lokale specialisten."
    },
    "no": {
        "category.seo_massage_h3_1": "Hvordan velge en massagespesialist?",
        "category.seo_massage_h3_2": "Hva koster massasje i {city}?",
        "category.seo_massage_p1": "{city} tilbyr et bredt utvalg av profesjonelle massasjespesialister. Enten du leter etter avslappende, sports- eller terapeutisk massasje, hjelper Nevumo deg med å finne pålitelige fagfolk i nærheten.",
        "category.seo_massage_p2": "Sjekk tidligere kundeanmeldelser, spesialistens erfaring og omfanget av tjenestene som tilbys. En god massasjespesialist vil tilpasse teknikken til dine behov.",
        "category.seo_massage_p3": "Profesjonell massasjeterapi for å lindre stress og forbedre ditt velvære. Bestill en time hos erfarne terapeuter i din by.",
        "category.seo_plumbing_h2": "Rørleggertjenester i {city} — hva er verdt å vite?",
        "category.seo_plumbing_h3_1": "Når bør du ringe en rørlegger?",
        "category.seo_plumbing_h3_2": "Hva koster en rørlegger i {city}?",
        "category.seo_plumbing_p2": "Ring en rørlegger ved feil i vannsystemet, lekkende kraner, tett avløp og ved renovering av bad eller kjøkken.",
        "category.seo_plumbing_p3": "Ekspertløsninger for rørleggertjenester ved enhver nødssituasjon eller planlagt reparasjon. Rask respons og garantert kvalitet fra lokale spesialister."
    },
    "pl": {
        "category.seo_massage_h3_1": "Jak wybrać specjalistę od masażu?",
        "category.seo_massage_h3_2": "Ile kosztuje masaż w {city}?",
        "category.seo_massage_p1": "{city} oferuje szeroki wybór profesjonalnych specjalistów od masażu. Niezależnie od tego, czy szukasz masażu relaksującego, sportowego czy terapeutycznego, Nevumo pomoże Ci znaleźć zaufanych profesjonalistów w pobliżu.",
        "category.seo_massage_p2": "Sprawdź opinie poprzednich klientów, doświadczenie specjalisty oraz zakres oferowanych usług. Dobry specjalista od masażu dostosuje technikę do Twoich potrzeb.",
        "category.seo_massage_p3": "Profesjonalna terapia masażem, która łagodzi stres i poprawia samopoczucie. Zarezerwuj sesję u doświadczonych terapeutów w Twoim mieście.",
        "category.seo_plumbing_h2": "Hydraulika w {city} — co warto wiedzieć?",
        "category.seo_plumbing_h3_1": "Kiedy wezwać hydraulika?",
        "category.seo_plumbing_h3_2": "Ile kosztuje hydraulik w {city}?",
        "category.seo_plumbing_p2": "Wezwij hydraulika w przypadku awarii instalacji wodnej, przeciekających kranów, zapchanych odpływów oraz podczas remontów łazienek lub kuchni.",
        "category.seo_plumbing_p3": "Eksperckie rozwiązania hydrauliczne w przypadku nagłych awarii lub planowanych napraw. Szybka reakcja i gwarantowana jakość od lokalnych specjalistów."
    },
    "pt": {
        "category.seo_massage_h3_1": "Como escolher um massagista?",
        "category.seo_massage_h3_2": "Quanto custa uma massagem em {city}?",
        "category.seo_massage_p1": "{city} oferece uma ampla seleção de massagistas profissionais. Esteja você procurando uma massagem relaxante, esportiva ou terapêutica, o Nevumo ajuda você a encontrar profissionais de confiança por perto.",
        "category.seo_massage_p2": "Verifique as avaliações de clientes anteriores, a experiência do especialista e o escopo dos serviços oferecidos. Um bom massagista adaptará a técnica às suas necessidades.",
        "category.seo_massage_p3": "Massoterapia profissional para aliviar o estresse e melhorar o seu bem-estar. Reserve uma sessão com terapeutas experientes em sua cidade.",
        "category.seo_plumbing_h2": "Encanamento em {city} — o que vale a pena saber?",
        "category.seo_plumbing_h3_1": "Quando chamar um encanador?",
        "category.seo_plumbing_h3_2": "Quanto custa um encanador em {city}?",
        "category.seo_plumbing_p2": "Chame um encanador para falhas no sistema de água, torneiras com vazamento, ralos entupidos e durante reformas de banheiro ou cozinha.",
        "category.seo_plumbing_p3": "Soluções especializadas em encanamento para qualquer emergência ou reparo planejado. Resposta rápida e qualidade garantida de especialistas locais."
    },
    "pt-PT": {
        "category.seo_massage_h3_1": "Como escolher um massagista?",
        "category.seo_massage_h3_2": "Quanto custa uma massagem em {city}?",
        "category.seo_massage_p1": "{city} oferece uma ampla seleção de massagistas profissionais. Quer procure uma massagem relaxante, desportiva ou terapêutica, o Nevumo ajuda-o a encontrar profissionais de confiança por perto.",
        "category.seo_massage_p2": "Verifique as avaliações de clientes anteriores, a experiência do especialista e o âmbito dos serviços oferecidos. Um bom massagista adaptará a técnica às suas necessidades.",
        "category.seo_massage_p3": "Massoterapia profissional para aliviar o stress e melhorar o seu bem-estar. Marque uma sessão com terapeutas experientes na sua cidade.",
        "category.seo_plumbing_h2": "Canalização em {city} — o que vale a pena saber?",
        "category.seo_plumbing_h3_1": "Quando chamar um canalizador?",
        "category.seo_plumbing_h3_2": "Quanto custa um canalizador em {city}?",
        "category.seo_plumbing_p2": "Chame um canalizador em caso de falhas no sistema de água, torneiras a pingar, canos entupidos e durante remodelações de casa de banho ou cozinha.",
        "category.seo_plumbing_p3": "Soluções de canalização especializadas para qualquer emergência ou reparação planeada. Resposta rápida e qualidade garantida por especialistas locais."
    },
    "ro": {
        "category.seo_massage_h3_1": "Cum să alegi un specialist în masaj?",
        "category.seo_massage_h3_2": "Cât costă un masaj în {city}?",
        "category.seo_massage_p1": "{city} oferă o selecție largă de specialiști în masaj profesional. Indiferent dacă sunteți în căutarea unui masaj de relaxare, sportiv sau terapeutic, Nevumo vă ajută să găsiți profesioniști de încredere în apropiere.",
        "category.seo_massage_p2": "Verificați recenziile clienților anteriori, experiența specialistului și gama de servicii oferite. Un bun specialist în masaj va adapta tehnica nevoilor dumneavoastră.",
        "category.seo_massage_p3": "Masoterapie profesională pentru ameliorarea stresului și îmbunătățirea stării de bine. Rezervați o ședință cu terapeuți cu experiență în orașul dumneavoastră.",
        "category.seo_plumbing_h2": "Instalații sanitare în {city} — ce merită să știți?",
        "category.seo_plumbing_h3_1": "Când să apelați la un instalator?",
        "category.seo_plumbing_h3_2": "Cât costă un instalator în {city}?",
        "category.seo_plumbing_p2": "Apelați la un instalator pentru defecțiuni ale sistemului de apă, robinete care curg, scurgeri înfundate și în timpul renovărilor băii sau bucătăriei.",
        "category.seo_plumbing_p3": "Soluții expert în instalații sanitare pentru orice urgență sau reparație planificată. Răspuns rapid și calitate garantată de la specialiști locali."
    },
    "ru": {
        "category.seo_massage_h3_1": "Как выбрать специалиста по массажу?",
        "category.seo_massage_h3_2": "Сколько стоит массаж в {city}?",
        "category.seo_massage_p1": "{city} предлагает широкий выбор профессиональных специалистов по массажу. Ищете ли вы расслабляющий, спортивный или лечебный массаж, Nevumo поможет вам найти надежных профессионалов поблизости.",
        "category.seo_massage_p2": "Ознакомьтесь с отзывами предыдущих клиентов, опытом специалиста и перечнем предлагаемых услуг. Хороший специалист по массажу адаптирует технику под ваши потребности.",
        "category.seo_massage_p3": "Профессиональная массажная терапия для снятия стресса и улучшения самочувствия. Запишитесь на сеанс к опытным терапевтам в вашем городе.",
        "category.seo_plumbing_h2": "Сантехника в {city} — что стоит знать?",
        "category.seo_plumbing_h3_1": "Когда вызывать сантехника?",
        "category.seo_plumbing_h3_2": "Сколько стоят услуги сантехника в {city}?",
        "category.seo_plumbing_p2": "Вызывайте сантехника при поломках водопровода, протекающих кранах, засорах в канализации, а также при ремонте ванной или кухни.",
        "category.seo_plumbing_p3": "Экспертные сантехнические решения для любых экстренных ситуаций или планового ремонта. Быстрая реакция и гарантированное качество от местных специалистов."
    },
    "sk": {
        "category.seo_massage_h3_1": "Ako si vybrať maséra?",
        "category.seo_massage_h3_2": "Koľko stojí masáž v {city}?",
        "category.seo_massage_p1": "{city} ponúka široký výber profesionálnych masérov. Či už hľadáte relaxačnú, športovú alebo terapeutickú masáž, Nevumo vám pomôže nájsť dôveryhodných odborníkov v okolí.",
        "category.seo_massage_p2": "Preverte si recenzie predchádzajúcich klientov, skúsenosti špecialistu a rozsah ponúkaných služieb. Dobrý masér prispôsobí techniku vašim potrebám.",
        "category.seo_massage_p3": "Profesionálna masážna terapia na uvoľnenie stresu a zlepšenie vašej pohody. Rezervujte si sedenie u skúsených terapeutov vo vašom meste.",
        "category.seo_plumbing_h2": "Inštalatérstvo v {city} — čo sa oplatí vedieť?",
        "category.seo_plumbing_h3_1": "Kedy zavolať inštalatéra?",
        "category.seo_plumbing_h3_2": "Koľko stojí inštalatér v {city}?",
        "category.seo_plumbing_p2": "Inštalatéra zavolajte v prípade poruchy vodovodného systému, kvapkajúcich kohútikov, upchatých odtokov a pri rekonštrukcii kúpeľne alebo kuchyne.",
        "category.seo_plumbing_p3": "Expertné inštalatérske riešenia pre akékoľvek naliehavé situácie alebo plánované opravy. Rýchla reakcia a garantovaná kvalita od miestnych špecialistov."
    },
    "sl": {
        "category.seo_massage_h3_1": "Kako izbrati strokovnjaka za masažo?",
        "category.seo_massage_h3_2": "Koliko stane masaža v {city}?",
        "category.seo_massage_p1": "{city} ponuja široko izbiro profesionalnih strokovnjakov za masažo. Ne glede na to, ali iščete sprostitveno, športno ali terapevtsko masažo, vam Nevumo pomaga najti zaupanja vredne strokovnjake v bližini.",
        "category.seo_massage_p2": "Preverite ocene prejšnjih strank, izkušnje strokovnjaka in obseg ponujenih storitev. Dober strokovnjak za masažo bo tehniko prilagodil vašim potrebam.",
        "category.seo_massage_p3": "Profesionalna masažna terapija za lajšanje stresa in izboljšanje vašega počutja. Rezervirajte termin pri izkušenih terapevtih v vašem mestu.",
        "category.seo_plumbing_h2": "Vodovodne instalacije v {city} — kaj je vredno vedeti?",
        "category.seo_plumbing_h3_1": "Kdaj poklicati vodovodarja?",
        "category.seo_plumbing_h3_2": "Koliko stane vodovodar v {city}?",
        "category.seo_plumbing_p2": "Pokličite vodovodarja v primeru okvar vodovodnega sistema, puščajočih pip, zamašenih odtokov ter med prenovo kopalnice ali kuhinje.",
        "category.seo_plumbing_p3": "Strokovne vodovodne rešitve za vse nujne primere ali načrtovane popravila. Hiter odziv in zajamčena kakovost lokalnih strokovnjakov."
    },
    "sq": {
        "category.seo_massage_h3_1": "Si të zgjidhni një specialist masazhi?",
        "category.seo_massage_h3_2": "Sa kushton masazhi në {city}?",
        "category.seo_massage_p1": "{city} ofron një përzgjedhje të gjerë të specialistëve profesionistë të masazhit. Pavarësisht nëse po kërkoni masazh relaksues, sportiv ose terapeutik, Nevumo ju ndihmon të gjeni profesionistë të besuar pranë jush.",
        "category.seo_massage_p2": "Kontrolloni vlerësimet e klientëve të mëparshëm, përvojën e specialistit dhe gamën e shërbimeve të ofruara. Një specialist i mirë masazhi do ta përshtatë teknikën sipas nevojave tuaja.",
        "category.seo_massage_p3": "Terapi masazhi profesioniste për të lehtësuar stresin dhe për të përmirësuar mirëqenien tuaj. Rezervoni një seancë me terapistë me përvojë në qytetin tuaj.",
        "category.seo_plumbing_h2": "Putunimet hidraulike në {city} — çfarë ia vlen të dini?",
        "category.seo_plumbing_h3_1": "Kur duhet thirrur një hidraulik?",
        "category.seo_plumbing_h3_2": "Sa kushton një hidraulik në {city}?",
        "category.seo_plumbing_p2": "Thirreni një hidraulik për defekte në sistemin e ujit, rubinetat që pikojnë, kullimet e bllokuara dhe gjatë renovimeve të banjës ose kuzhinës.",
        "category.seo_plumbing_p3": "Zgjidhje ekspertësh hidraulikë për çdo rast urgjence ose riparim të planifikuar. Përgjigje e shpejtë dhe cilësi e garantuar nga specialistët vendas."
    },
    "sr": {
        "category.seo_massage_h3_1": "Kako odabrati stručnjaka za masažu?",
        "category.seo_massage_h3_2": "Koliko košta masaža u {city}?",
        "category.seo_massage_p1": "{city} nudi širok izbor profesionalnih stručnjaka za masažu. Bilo da tražite opuštajuću, sportsku ili terapeutsku masažu, Nevumo vam pomaže da pronađete proverene stručnjake u blizini.",
        "category.seo_massage_p2": "Proverite recenzije prethodnih klijenata, iskustvo stručnjaka i obim ponuđenih usluga. Dobar stručnjak za masažu će prilagoditi tehniku vašim potrebama.",
        "category.seo_massage_p3": "Profesionalna masažna terapija za ublažavanje stresa i poboljšanje vašeg blagostanja. Rezervišite termin kod iskusnih terapeuta u svom gradu.",
        "category.seo_plumbing_h2": "Vodoinstalacije u {city} — šta vredi znati?",
        "category.seo_plumbing_h3_1": "Kada pozvati vodoinstalatera?",
        "category.seo_plumbing_h3_2": "Koliko košta vodoinstalater u {city}?",
        "category.seo_plumbing_p2": "Pozovite vodoinstalatera u slučaju kvara vodovodnog sistema, slavina koje cure, zapušenih odvoda i tokom renoviranja kupatila ili kuhinje.",
        "category.seo_plumbing_p3": "Ekspertska rešenja za vodoinstalacije za sve hitne slučajeve ili planirane popravke. Brza reakcija i zagarantovan kvalitet lokalnih stručnjaka."
    },
    "sv": {
        "category.seo_massage_h3_1": "Hur väljer man en massagespecialist?",
        "category.seo_massage_h3_2": "Vad kostar massage i {city}?",
        "category.seo_massage_p1": "{city} erbjuder ett brett urval av professionella massagespecialister. Oavsett om du letar efter avslappnande, sport- eller terapeutisk massage, hjälper Nevumo dig att hitta betrodda proffs i närheten.",
        "category.seo_massage_p2": "Kontrollera tidigare kundrecensioner, specialistens erfarenhet och omfattningen av de tjänster som erbjuds. En bra massagespecialist anpassar tekniken efter dina behov.",
        "category.seo_massage_p3": "Professionell massageterapi för att lindra stress och förbättra ditt välbefinnande. Boka en session med erfarna terapeuter i din stad.",
        "category.seo_plumbing_h2": "Rörmokeri i {city} — vad är värt att veta?",
        "category.seo_plumbing_h3_1": "När ska man ringa en rörmokare?",
        "category.seo_plumbing_h3_2": "Vad kostar en rörmokare i {city}?",
        "category.seo_plumbing_p2": "Ring en rörmokare vid fel i vattensystemet, läckande kranar, igensatta avlopp och under badrums- eller köksrenoveringar.",
        "category.seo_plumbing_p3": "Expertlösningar för rörmokeri vid nödsituationer eller planerade reparationer. Snabb respons och garanterad kvalitet från lokala specialister."
    },
    "tr": {
        "category.seo_massage_h3_1": "Masaj uzmanı nasıl seçilir?",
        "category.seo_massage_h3_2": "{city} bölgesinde masaj ücreti ne kadar?",
        "category.seo_massage_p1": "{city}, profesyonel masaj uzmanlarından oluşan geniş bir seçenek sunar. İster rahatlatıcı, ister spor veya terapötik masaj arıyor olun, Nevumo yakınınızdaki güvenilir profesyonelleri bulmanıza yardımcı olur.",
        "category.seo_massage_p2": "Önceki müşteri yorumlarını, uzmanlık deneyimini ve sunulan hizmetlerin kapsamını kontrol edin. İyi bir masaj uzmanı, tekniği ihtiyaçlarınıza göre uyarlayacaktır.",
        "category.seo_massage_p3": "Stresi azaltmak ve refahınızı artırmak için profesyonel masaj terapisi. Şehrinizdeki deneyimli terapistlerle bir seans ayarlayın.",
        "category.seo_plumbing_h2": "{city} bölgesinde su tesisatı — bilmeniz gerekenler nelerdir?",
        "category.seo_plumbing_h3_1": "Ne zaman tesisatçı çağırmalıyız?",
        "category.seo_plumbing_h3_2": "{city} bölgesinde bir tesisatçı ne kadar tutar?",
        "category.seo_plumbing_p2": "Su sistemi arızaları, sızdıran musluklar, tıkanmış giderler için ve banyo veya mutfak tadilatları sırasında bir tesisatçı çağırın.",
        "category.seo_plumbing_p3": "Her türlü acil durum veya planlı onarım için uzman tesisat çözümleri. Yerel tesisat uzmanlarından hızlı yanıt ve garantili kalite."
    },
    "uk": {
        "category.seo_massage_h3_1": "Як обрати спеціаліста з масажу?",
        "category.seo_massage_h3_2": "Скільки коштує масаж у {city}?",
        "category.seo_massage_p1": "{city} пропонує широкий вибір професійних спеціалістів із масажу. Незалежно від того, чи шукаєте ви розслабляючий, спортивний або лікувальний масаж, Nevumo допоможе вам знайти надійних професіоналів поблизу.",
        "category.seo_massage_p2": "Перевірте відгуки попередніх клієнтів, досвід спеціаліста та перелік пропонованих послуг. Хороший спеціаліст із масажу адаптує техніку до ваших потреб.",
        "category.seo_massage_p3": "Професійна масажна терапія для зняття стресу та покращення самопочуття. Запишіться на сеанс до досвідчених терапевтів у вашому місті.",
        "category.seo_plumbing_h2": "Сантехніка у {city} — що варто знати?",
        "category.seo_plumbing_h3_1": "Коли викликати сантехніка?",
        "category.seo_plumbing_h3_2": "Скільки коштує сантехнік у {city}?",
        "category.seo_plumbing_p2": "Викликайте сантехніка при поломках водопроводу, кранах, що протікають, засміченнях у каналізації, а також під час ремонту ванної кімнати чи кухні.",
        "category.seo_plumbing_p3": "Експертні сантехнічні рішення для будь-яких екстрених випадків або планового ремонту. Швидке реагування та гарантована якість від місцевих спеціалістів."
    }
}

if __name__ == "__main__":
    main()
