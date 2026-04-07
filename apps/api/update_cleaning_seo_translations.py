import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://localhost/nevumo_leads")

UPDATES = [
    # seo_cleaning_h3_1 — "How to choose a cleaning specialist?"
    ("bg", "category.seo_cleaning_h3_1", "Как да изберете специалист по почистване?"),
    ("cs", "category.seo_cleaning_h3_1", "Jak vybrat specialistu na úklid?"),
    ("da", "category.seo_cleaning_h3_1", "Hvordan vælger man en rengøringsspecialist?"),
    ("de", "category.seo_cleaning_h3_1", "Wie wählt man einen Reinigungsspezialisten?"),
    ("el", "category.seo_cleaning_h3_1", "Πώς να επιλέξετε ειδικό καθαρισμού;"),
    ("es", "category.seo_cleaning_h3_1", "¿Cómo elegir un especialista en limpieza?"),
    ("et", "category.seo_cleaning_h3_1", "Kuidas valida koristuseksperte?"),
    ("fi", "category.seo_cleaning_h3_1", "Kuinka valita siivousasiantuntija?"),
    ("fr", "category.seo_cleaning_h3_1", "Comment choisir un spécialiste en nettoyage?"),
    ("ga", "category.seo_cleaning_h3_1", "Conas speisialtóir glantacháin a roghnú?"),
    ("hr", "category.seo_cleaning_h3_1", "Kako odabrati stručnjaka za čišćenje?"),
    ("hu", "category.seo_cleaning_h3_1", "Hogyan válasszunk takarítási szakembert?"),
    ("is", "category.seo_cleaning_h3_1", "Hvernig á að velja þrif sérfræðing?"),
    ("it", "category.seo_cleaning_h3_1", "Come scegliere uno specialista delle pulizie?"),
    ("lb", "category.seo_cleaning_h3_1", "Wéi wielt een e Botzspezialist?"),
    ("lt", "category.seo_cleaning_h3_1", "Kaip pasirinkti valymo specialistą?"),
    ("lv", "category.seo_cleaning_h3_1", "Kā izvēlēties tīrīšanas speciālistu?"),
    ("mk", "category.seo_cleaning_h3_1", "Како да изберете специјалист за чистење?"),
    ("mt", "category.seo_cleaning_h3_1", "Kif tagħżel speċjalista tat-tindif?"),
    ("nl", "category.seo_cleaning_h3_1", "Hoe kies je een schoonmaakspecialist?"),
    ("no", "category.seo_cleaning_h3_1", "Hvordan velge en renholdsspesialist?"),
    ("pl", "category.seo_cleaning_h3_1", "Jak wybrać specjalistę od sprzątania?"),
    ("pt", "category.seo_cleaning_h3_1", "Como escolher um especialista em limpeza?"),
    ("pt-PT", "category.seo_cleaning_h3_1", "Como escolher um especialista em limpeza?"),
    ("ro", "category.seo_cleaning_h3_1", "Cum să alegi un specialist în curățenie?"),
    ("ru", "category.seo_cleaning_h3_1", "Как выбрать специалиста по уборке?"),
    ("sk", "category.seo_cleaning_h3_1", "Ako vybrať špecialistu na upratovanie?"),
    ("sl", "category.seo_cleaning_h3_1", "Kako izbrati strokovnjaka za čiščenje?"),
    ("sq", "category.seo_cleaning_h3_1", "Si të zgjidhni një specialist pastrimi?"),
    ("sr", "category.seo_cleaning_h3_1", "Kako izabrati stručnjaka za čišćenje?"),
    ("sv", "category.seo_cleaning_h3_1", "Hur väljer man en städspecialist?"),
    ("tr", "category.seo_cleaning_h3_1", "Temizlik uzmanı nasıl seçilir?"),
    ("uk", "category.seo_cleaning_h3_1", "Як вибрати фахівця з прибирання?"),

    # seo_cleaning_p1 — professional specialists (not companies)
    ("bg", "category.seo_cleaning_p1", "Професионални специалисти по почистване във Варшава предлагат комплексни услуги за домове, апартаменти и офиси. В Nevumo ще намерите проверени професионалисти, налични в цяла Варшава."),
    ("cs", "category.seo_cleaning_p1", "Profesionální specialisté na úklid ve Varšavě nabízejí komplexní služby pro domy, byty a kanceláře. Na Nevumo najdete ověřené odborníky dostupné po celé Varšavě."),
    ("da", "category.seo_cleaning_p1", "Professionelle rengøringsspecialister i Warszawa tilbyder omfattende tjenester til hjem, lejligheder og kontorer. På Nevumo finder du betroede fagfolk tilgængelige i hele Warszawa."),
    ("de", "category.seo_cleaning_p1", "Professionelle Reinigungsspezialisten in Warschau bieten umfassende Dienstleistungen für Häuser, Wohnungen und Büros an. Bei Nevumo finden Sie geprüfte Fachleute, die in ganz Warschau verfügbar sind."),
    ("el", "category.seo_cleaning_p1", "Επαγγελματίες ειδικοί καθαρισμού στη Βαρσοβία προσφέρουν ολοκληρωμένες υπηρεσίες για σπίτια, διαμερίσματα και γραφεία. Στο Nevumo θα βρείτε αξιόπιστους επαγγελματίες διαθέσιμους σε όλη τη Βαρσοβία."),
    ("es", "category.seo_cleaning_p1", "Especialistas profesionales en limpieza en Varsovia ofrecen servicios integrales para hogares, apartamentos y oficinas. En Nevumo encontrarás profesionales de confianza disponibles en toda Varsovia."),
    ("et", "category.seo_cleaning_p1", "Professionaalsed koristuseksperdid Varssavis pakuvad terviklikke teenuseid kodudele, korteritele ja kontoritele. Nevumol leiate usaldusväärseid spetsialiste üle kogu Varssavi."),
    ("fi", "category.seo_cleaning_p1", "Ammattimaiset siivousasiantuntijat Varsovassa tarjoavat kattavia palveluita koteihin, asuntoihin ja toimistoihin. Nevumosta löydät luotettavia ammattilaisia kaikkialla Varsovassa."),
    ("fr", "category.seo_cleaning_p1", "Des spécialistes professionnels du nettoyage à Varsovie offrent des services complets pour les maisons, appartements et bureaux. Sur Nevumo, vous trouverez des professionnels de confiance disponibles dans toute Varsovie."),
    ("ga", "category.seo_cleaning_p1", "Cuireann speisialtóirí gairmiúla glantacháin i Vársá seirbhísí cuimsitheacha ar fáil do thithe, árasáin agus oifigí. Ar Nevumo, gheobhaidh tú gairmithe iontaofa ar fáil ar fud Vársá."),
    ("hr", "category.seo_cleaning_p1", "Profesionalni stručnjaci za čišćenje u Varšavi nude sveobuhvatne usluge za kuće, stanove i urede. Na Nevumo ćete pronaći provjerene profesionalce dostupne diljem Varšave."),
    ("hu", "category.seo_cleaning_p1", "Professzionális takarítási szakemberek Varsóban átfogó szolgáltatásokat kínálnak házakhoz, lakásokhoz és irodákhoz. A Nevumón megbízható szakembereket találhat Varsó-szerte."),
    ("is", "category.seo_cleaning_p1", "Faglegir þrif sérfræðingar í Varsjá bjóða upp á alhliða þjónustu fyrir heimili, íbúðir og skrifstofur. Á Nevumo finnur þú trausta sérfræðinga víðs vegar um Varsjá."),
    ("it", "category.seo_cleaning_p1", "Specialisti professionisti delle pulizie a Varsavia offrono servizi completi per case, appartamenti e uffici. Su Nevumo troverai professionisti affidabili disponibili in tutta Varsavia."),
    ("lb", "category.seo_cleaning_p1", "Professionell Botzspezialisten a Warschau bidden ëmfangräich Servicer fir Haiser, Wunnengen a Büroen. Op Nevumo fannt Dir iwwerpréift Fachleit, déi iwwerall zu Warschau disponibel sinn."),
    ("lt", "category.seo_cleaning_p1", "Profesionalūs valymo specialistai Varšuvoje siūlo išsamias paslaugas namams, butams ir biurams. Nevumo rasite patikimų specialistų visoje Varšuvoje."),
    ("lv", "category.seo_cleaning_p1", "Profesionāli tīrīšanas speciālisti Varšavā piedāvā visaptverošus pakalpojumus mājām, dzīvokļiem un birojiem. Nevumo atradīsiet uzticamus speciālistus visā Varšavā."),
    ("mk", "category.seo_cleaning_p1", "Професионални специјалисти за чистење во Варшава нудат сеопфатни услуги за домови, станови и канцеларии. На Nevumo ќе најдете проверени професионалци достапни низ цела Варшава."),
    ("mt", "category.seo_cleaning_p1", "Speċjalisti professjonali tat-tindif f'Varsavja joffru servizzi komprensivi għal djar, appartamenti u uffiċċji. Fuq Nevumo ssib professjonisti affidabbli disponibbli madwar Varsavja kollha."),
    ("nl", "category.seo_cleaning_p1", "Professionele schoonmaakspecialisten in Warschau bieden uitgebreide diensten aan voor huizen, appartementen en kantoren. Op Nevumo vind je betrouwbare professionals beschikbaar door heel Warschau."),
    ("no", "category.seo_cleaning_p1", "Profesjonelle renholdsspesialister i Warszawa tilbyr omfattende tjenester for hjem, leiligheter og kontorer. På Nevumo finner du pålitelige fagfolk tilgjengelige over hele Warszawa."),
    ("pl", "category.seo_cleaning_p1", "Profesjonalni specjaliści od sprzątania w Warszawie oferują kompleksowe usługi dla domów, mieszkań i biur. Na Nevumo znajdziesz sprawdzonych fachowców dostępnych na terenie całej Warszawy."),
    ("pt", "category.seo_cleaning_p1", "Especialistas profissionais em limpeza em Varsóvia oferecem serviços abrangentes para casas, apartamentos e escritórios. No Nevumo você encontrará profissionais confiáveis disponíveis em toda Varsóvia."),
    ("pt-PT", "category.seo_cleaning_p1", "Especialistas profissionais de limpeza em Varsóvia oferecem serviços abrangentes para casas, apartamentos e escritórios. No Nevumo encontrará profissionais de confiança disponíveis em toda Varsóvia."),
    ("ro", "category.seo_cleaning_p1", "Specialiști profesioniști în curățenie din Varșovia oferă servicii complete pentru case, apartamente și birouri. Pe Nevumo veți găsi profesioniști de încredere disponibili în toată Varșovia."),
    ("ru", "category.seo_cleaning_p1", "Профессиональные специалисты по уборке в Варшаве предлагают комплексные услуги для домов, квартир и офисов. На Nevumo вы найдёте проверенных профессионалов, доступных по всей Варшаве."),
    ("sk", "category.seo_cleaning_p1", "Profesionálni špecialisti na upratovanie vo Varšave ponúkajú komplexné služby pre domy, byty a kancelárie. Na Nevumo nájdete overených odborníkov dostupných po celej Varšave."),
    ("sl", "category.seo_cleaning_p1", "Profesionalni strokovnjaki za čiščenje v Varšavi ponujajo celovite storitve za hiše, stanovanja in pisarne. Na Nevumo boste našli zanesljive strokovnjake, ki so na voljo po vsej Varšavi."),
    ("sq", "category.seo_cleaning_p1", "Specialistët profesionistë të pastrimit në Varshavë ofrojnë shërbime gjithëpërfshirëse për shtëpi, apartamente dhe zyra. Në Nevumo do të gjeni profesionistë të besuar të disponueshëm në të gjithë Varshavën."),
    ("sr", "category.seo_cleaning_p1", "Profesionalni stručnjaci za čišćenje u Varšavi nude sveobuhvatne usluge za kuće, stanove i kancelarije. Na Nevumo ćete naći proverene profesionalce dostupne širom Varšave."),
    ("sv", "category.seo_cleaning_p1", "Professionella städspecialister i Warszawa erbjuder omfattande tjänster för hus, lägenheter och kontor. På Nevumo hittar du betrodda proffs tillgängliga i hela Warszawa."),
    ("tr", "category.seo_cleaning_p1", "Varşova'daki profesyonel temizlik uzmanları evler, daireler ve ofisler için kapsamlı hizmetler sunmaktadır. Nevumo'da Varşova genelinde hizmet veren güvenilir uzmanlar bulabilirsiniz."),
    ("uk", "category.seo_cleaning_p1", "Професійні фахівці з прибирання у Варшаві пропонують комплексні послуги для будинків, квартир і офісів. На Nevumo ви знайдете перевірених професіоналів, доступних по всій Варшаві."),

    # seo_cleaning_p2 — best specialists (not companies)
    ("bg", "category.seo_cleaning_p2", "Обърнете внимание на отзивите на клиентите, обхвата на услугите и гъвкавостта на сроковете. Най-добрите специалисти предлагат редовно сътрудничество с отстъпка."),
    ("cs", "category.seo_cleaning_p2", "Věnujte pozornost recenzím klientů, rozsahu služeb a flexibilitě termínů. Nejlepší specialisté nabízejí pravidelnou spolupráci se slevou."),
    ("da", "category.seo_cleaning_p2", "Vær opmærksom på kundeanmeldelser, serviceomfang og fleksibilitet i tidspunkter. De bedste specialister tilbyder regelmæssigt samarbejde med rabat."),
    ("de", "category.seo_cleaning_p2", "Achten Sie auf Kundenbewertungen, Leistungsumfang und Terminflexibilität. Die besten Spezialisten bieten regelmäßige Zusammenarbeit mit Rabatt an."),
    ("el", "category.seo_cleaning_p2", "Δώστε προσοχή στις κριτικές πελατών, στο εύρος υπηρεσιών και στην ευελιξία χρονοδιαγραμμάτων. Οι καλύτεροι ειδικοί προσφέρουν τακτική συνεργασία με έκπτωση."),
    ("es", "category.seo_cleaning_p2", "Presta atención a las reseñas de clientes, el alcance de los servicios y la flexibilidad de horarios. Los mejores especialistas ofrecen colaboración regular con descuento."),
    ("et", "category.seo_cleaning_p2", "Pöörake tähelepanu klientide arvustustele, teenuste ulatusele ja ajakava paindlikkusele. Parimad spetsialistid pakuvad regulaarset koostööd soodustusega."),
    ("fi", "category.seo_cleaning_p2", "Kiinnitä huomiota asiakasarvosteluihin, palvelujen laajuuteen ja aikataulujen joustavuuteen. Parhaat asiantuntijat tarjoavat säännöllistä yhteistyötä alennuksella."),
    ("fr", "category.seo_cleaning_p2", "Faites attention aux avis des clients, à l'étendue des services et à la flexibilité des horaires. Les meilleurs spécialistes proposent une collaboration régulière avec remise."),
    ("ga", "category.seo_cleaning_p2", "Tabhair aird ar léirmheasanna custaiméirí, raon seirbhísí agus solúbthacht sceideal. Cuireann na speisialtóirí is fearr comhoibriú rialta le lascaine ar fáil."),
    ("hr", "category.seo_cleaning_p2", "Obratite pozornost na recenzije klijenata, opseg usluga i fleksibilnost termina. Najbolji stručnjaci nude redovitu suradnju s popustom."),
    ("hu", "category.seo_cleaning_p2", "Figyeljen az ügyfélértékelésekre, a szolgáltatások körére és az időpontok rugalmasságára. A legjobb szakemberek rendszeres együttműködést kínálnak kedvezménnyel."),
    ("is", "category.seo_cleaning_p2", "Gefðu gaum að umsögnum viðskiptavina, umfangi þjónustu og sveigjanleika tímasetningar. Bestu sérfræðingarnir bjóða upp á reglulegt samstarf með afslátt."),
    ("it", "category.seo_cleaning_p2", "Presta attenzione alle recensioni dei clienti, all'ambito dei servizi e alla flessibilità degli orari. I migliori specialisti offrono collaborazione regolare con sconto."),
    ("lb", "category.seo_cleaning_p2", "Gitt Opmierksamkeet op Clientbewäertungen, Servicëëmfang a Flexibilitéit vun Terminer. Déi bescht Spezialiste bidden regelméisseg Zesummenaarbecht mat Rabatt."),
    ("lt", "category.seo_cleaning_p2", "Atkreipkite dėmesį į klientų atsiliepimus, paslaugų apimtį ir tvarkaraščio lankstumą. Geriausi specialistai siūlo reguliarų bendradarbiavimą su nuolaida."),
    ("lv", "category.seo_cleaning_p2", "Pievērsiet uzmanību klientu atsauksmēm, pakalpojumu apjomam un grafika elastībai. Labākie speciālisti piedāvā regulāru sadarbību ar atlaidi."),
    ("mk", "category.seo_cleaning_p2", "Обрнете внимание на рецензиите на клиентите, опсегот на услуги и флексибилноста на термините. Најдобрите специјалисти нудат редовна соработка со попуст."),
    ("mt", "category.seo_cleaning_p2", "Agħti attenzjoni lill-reviews tal-klijenti, l-ambitu tas-servizzi u l-flessibbiltà tal-iskeda. L-aħjar speċjalisti joffru kollaborazzjoni regolari b'skont."),
    ("nl", "category.seo_cleaning_p2", "Let op klantbeoordelingen, het dienstenpakket en de flexibiliteit van afspraken. De beste specialisten bieden regelmatige samenwerking met korting."),
    ("no", "category.seo_cleaning_p2", "Vær oppmerksom på kundeanmeldelser, tjenestenes omfang og fleksibilitet i timeplanlegging. De beste spesialistene tilbyr regelmessig samarbeid med rabatt."),
    ("pl", "category.seo_cleaning_p2", "Zwróć uwagę na opinie klientów, zakres usług oraz elastyczność terminów. Najlepsi specjaliści oferują stałą współpracę z rabatem."),
    ("pt", "category.seo_cleaning_p2", "Preste atenção às avaliações de clientes, ao escopo dos serviços e à flexibilidade de horários. Os melhores especialistas oferecem colaboração regular com desconto."),
    ("pt-PT", "category.seo_cleaning_p2", "Preste atenção às avaliações dos clientes, ao âmbito dos serviços e à flexibilidade de horários. Os melhores especialistas oferecem colaboração regular com desconto."),
    ("ro", "category.seo_cleaning_p2", "Acordați atenție recenziilor clienților, domeniului de servicii și flexibilității programului. Cei mai buni specialiști oferă colaborare regulată cu reducere."),
    ("ru", "category.seo_cleaning_p2", "Обратите внимание на отзывы клиентов, спектр услуг и гибкость расписания. Лучшие специалисты предлагают регулярное сотрудничество со скидкой."),
    ("sk", "category.seo_cleaning_p2", "Venujte pozornosť recenziám klientov, rozsahu služieb a flexibilite termínov. Najlepší špecialisti ponúkajú pravidelnú spoluprácu so zľavou."),
    ("sl", "category.seo_cleaning_p2", "Bodite pozorni na ocene strank, obseg storitev in prožnost urnikov. Najboljši strokovnjaki ponujajo redno sodelovanje s popustom."),
    ("sq", "category.seo_cleaning_p2", "Kushtojini vëmendje vlerësimeve të klientëve, gamës së shërbimeve dhe fleksibilitetit të orareve. Specialistët më të mirë ofrojnë bashkëpunim të rregullt me zbritje."),
    ("sr", "category.seo_cleaning_p2", "Obratite pažnju na recenzije klijenata, obim usluga i fleksibilnost termina. Najbolji stručnjaci nude redovno saradnju sa popustom."),
    ("sv", "category.seo_cleaning_p2", "Var uppmärksam på kundrecensioner, tjänsternas omfattning och schemaflexibilitet. De bästa specialisterna erbjuder regelbundet samarbete med rabatt."),
    ("tr", "category.seo_cleaning_p2", "Müşteri yorumlarına, hizmet kapsamına ve program esnekliğine dikkat edin. En iyi uzmanlar indirimli düzenli işbirliği sunar."),
    ("uk", "category.seo_cleaning_p2", "Зверніть увагу на відгуки клієнтів, спектр послуг і гнучкість розкладу. Найкращі фахівці пропонують регулярне співробітництво зі знижкою."),
]


def run():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    count = 0
    for lang, key, value in UPDATES:
        cur.execute(
            """
            INSERT INTO translations (lang, key, value)
            VALUES (%s, %s, %s)
            ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
            """,
            (lang, key, value)
        )
        count += cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Done: {count} rows updated")


if __name__ == "__main__":
    run()
