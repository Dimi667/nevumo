"""
seed_provider_terms_p9_art2_body.py  —  Nevumo | namespace: provider_terms
Key: art2_body  (1 key x 34 langs = 34 rows)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_provider_terms_p9_art2_body
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
    "art2_body": {
        "en": (
            "Platform — The Nevumo website and mobile application accessible at nevumo.com and its subdomains.\n\n"
            "Provider — A natural person aged 18 or over, or a legal entity, registered on the Platform to offer services.\n\n"
            "Client — A natural person registered on the Platform to seek and order services.\n\n"
            "Lead — A service request submitted by a Client through the Platform.\n\n"
            "Profile — The Provider's public page on the Platform containing their services, description, and reviews.\n\n"
            "Service Listing — An individual service offered by the Provider within their Profile.\n\n"
            "Commission — The fee charged by Nevumo for intermediary services, as specified in the current Price List.\n\n"
            "Price List — The document specifying current commissions and fees, available at nevumo.com/pricing.\n\n"
            "Trader — A Provider acting in the capacity of a business (self-employed person, company, etc.)."
        ),
        "pl": (
            "Platforma — Serwis internetowy Nevumo dostępny pod adresem nevumo.com i jego poddomeny.\n\n"
            "Dostawca — Osoba fizyczna w wieku co najmniej 18 lat lub podmiot prawny zarejestrowany na Platformie w celu oferowania usług.\n\n"
            "Klient — Osoba fizyczna zarejestrowana na Platformie w celu poszukiwania i zamawiania usług.\n\n"
            "Zapytanie (Lead) — Zapytanie o usługę złożone przez Klienta za pośrednictwem Platformy.\n\n"
            "Profil — Publiczna strona Dostawcy na Platformie zawierająca jego usługi, opis i opinie.\n\n"
            "Oferta Usługi — Indywidualna usługa oferowana przez Dostawcę w ramach jego Profilu.\n\n"
            "Prowizja — Opłata pobierana przez Nevumo za usługi pośrednictwa, zgodnie z aktualnym Cennikiem.\n\n"
            "Cennik — Dokument określający aktualne prowizje i opłaty, dostępny pod adresem nevumo.com/pricing.\n\n"
            "Przedsiębiorca — Dostawca działający w charakterze prowadzącego działalność gospodarczą."
        ),
        "bg": (
            "Платформа — Уебсайтът и мобилното приложение на Nevumo, достъпни на nevumo.com и неговите поддомейни.\n\n"
            "Доставчик — Физическо лице на 18 или повече години, или юридическо лице, регистрирано на Платформата за предлагане на услуги.\n\n"
            "Клиент — Физическо лице, регистрирано на Платформата за търсене и поръчване на услуги.\n\n"
            "Запитване (Lead) — Заявка за услуга, подадена от Клиент чрез Платформата.\n\n"
            "Профил — Публичната страница на Доставчика в Платформата, съдържаща неговите услуги, описание и отзиви.\n\n"
            "Обява за услуга — Отделна услуга, предлагана от Доставчика в рамките на неговия Профил.\n\n"
            "Комисионна — Таксата, начислявана от Nevumo за посреднически услуги, съгласно действащия Ценоразпис.\n\n"
            "Ценоразпис — Документът, определящ актуалните комисионни и такси, достъпен на nevumo.com/pricing.\n\n"
            "Търговец — Доставчик, действащ в качеството на стопански субект (самонает, дружество и др.)."
        ),
        "de": (
            "Plattform — Die Nevumo-Website und mobile Anwendung, erreichbar unter nevumo.com und seinen Subdomains.\n\n"
            "Dienstleister — Eine natürliche Person ab 18 Jahren oder eine juristische Person, die auf der Plattform registriert ist, um Dienstleistungen anzubieten.\n\n"
            "Kunde — Eine natürliche Person, die auf der Plattform registriert ist, um Dienstleistungen zu suchen und zu buchen.\n\n"
            "Lead — Eine vom Kunden über die Plattform eingereichte Serviceanfrage.\n\n"
            "Profil — Die öffentliche Seite des Dienstleisters auf der Plattform mit seinen Dienstleistungen, Beschreibung und Bewertungen.\n\n"
            "Serviceangebot — Eine einzelne vom Dienstleister in seinem Profil angebotene Dienstleistung.\n\n"
            "Provision — Die von Nevumo für Vermittlungsdienste erhobene Gebühr gemäß der aktuellen Preisliste.\n\n"
            "Preisliste — Das Dokument mit den aktuellen Provisionen und Gebühren, verfügbar unter nevumo.com/pricing.\n\n"
            "Händler — Ein Dienstleister, der in der Eigenschaft als Unternehmen tätig ist (Selbstständiger, Firma usw.)."
        ),
        "fr": (
            "Plateforme — Le site web et l'application mobile Nevumo accessibles sur nevumo.com et ses sous-domaines.\n\n"
            "Prestataire — Une personne physique d'au moins 18 ans, ou une personne morale, enregistree sur la Plateforme pour offrir des services.\n\n"
            "Client — Une personne physique enregistree sur la Plateforme pour rechercher et commander des services.\n\n"
            "Lead — Une demande de service soumise par un Client via la Plateforme.\n\n"
            "Profil — La page publique du Prestataire sur la Plateforme contenant ses services, sa description et ses avis.\n\n"
            "Annonce de service — Un service individuel propose par le Prestataire dans son Profil.\n\n"
            "Commission — Les frais factures par Nevumo pour les services d'intermediation, conformement a la Grille tarifaire en vigueur.\n\n"
            "Grille tarifaire — Le document specifiant les commissions et frais en vigueur, disponible sur nevumo.com/pricing.\n\n"
            "Professionnel — Un Prestataire agissant en qualite d'entreprise (independant, societe, etc.)."
        ),
        "es": (
            "Plataforma — El sitio web y la aplicacion movil de Nevumo accesibles en nevumo.com y sus subdominios.\n\n"
            "Proveedor — Una persona fisica de 18 anos o mas, o una persona juridica, registrada en la Plataforma para ofrecer servicios.\n\n"
            "Cliente — Una persona fisica registrada en la Plataforma para buscar y contratar servicios.\n\n"
            "Lead — Una solicitud de servicio enviada por un Cliente a traves de la Plataforma.\n\n"
            "Perfil — La pagina publica del Proveedor en la Plataforma que contiene sus servicios, descripcion y resenas.\n\n"
            "Listado de servicio — Un servicio individual ofrecido por el Proveedor en su Perfil.\n\n"
            "Comision — La tarifa cobrada por Nevumo por los servicios de intermediacion, segun la Lista de precios vigente.\n\n"
            "Lista de precios — El documento que especifica las comisiones y tarifas vigentes, disponible en nevumo.com/pricing.\n\n"
            "Comerciante — Un Proveedor que actua en calidad de empresa (autonomo, sociedad, etc.)."
        ),
        "it": (
            "Piattaforma — Il sito web e l'applicazione mobile di Nevumo accessibili su nevumo.com e i suoi sottodomini.\n\n"
            "Fornitore — Una persona fisica di 18 anni o piu, o una persona giuridica, registrata sulla Piattaforma per offrire servizi.\n\n"
            "Cliente — Una persona fisica registrata sulla Piattaforma per cercare e ordinare servizi.\n\n"
            "Lead — Una richiesta di servizio inviata da un Cliente tramite la Piattaforma.\n\n"
            "Profilo — La pagina pubblica del Fornitore sulla Piattaforma contenente i suoi servizi, descrizione e recensioni.\n\n"
            "Annuncio di servizio — Un servizio individuale offerto dal Fornitore nel suo Profilo.\n\n"
            "Commissione — La tariffa addebitata da Nevumo per i servizi di intermediazione, come specificato nel Listino prezzi vigente.\n\n"
            "Listino prezzi — Il documento che specifica le commissioni e le tariffe vigenti, disponibile su nevumo.com/pricing.\n\n"
            "Professionista — Un Fornitore che agisce in qualita di impresa (lavoratore autonomo, societa, ecc.)."
        ),
        "nl": (
            "Platform — De Nevumo-website en mobiele applicatie toegankelijk via nevumo.com en zijn subdomains.\n\n"
            "Dienstverlener — Een natuurlijk persoon van 18 jaar of ouder, of een rechtspersoon, geregistreerd op het Platform om diensten aan te bieden.\n\n"
            "Klant — Een natuurlijk persoon geregistreerd op het Platform om diensten te zoeken en te bestellen.\n\n"
            "Lead — Een serviceverzoek ingediend door een Klant via het Platform.\n\n"
            "Profiel — De openbare pagina van de Dienstverlener op het Platform met zijn diensten, beschrijving en beoordelingen.\n\n"
            "Serviceaanbieding — Een individuele dienst aangeboden door de Dienstverlener in zijn Profiel.\n\n"
            "Commissie — De vergoeding die Nevumo in rekening brengt voor bemiddelingsdiensten, zoals gespecificeerd in de huidige Prijslijst.\n\n"
            "Prijslijst — Het document met de huidige commissies en vergoedingen, beschikbaar op nevumo.com/pricing.\n\n"
            "Handelaar — Een Dienstverlener die optreedt in de hoedanigheid van een bedrijf (zelfstandige, onderneming, enz.)."
        ),
        "pt": (
            "Plataforma — O site e aplicativo movel da Nevumo acessiveis em nevumo.com e seus subdominios.\n\n"
            "Prestador — Uma pessoa singular com 18 anos ou mais, ou uma pessoa coletiva, registada na Plataforma para oferecer servicos.\n\n"
            "Cliente — Uma pessoa singular registada na Plataforma para procurar e encomendar servicos.\n\n"
            "Lead — Uma solicitacao de servico submetida por um Cliente atraves da Plataforma.\n\n"
            "Perfil — A pagina publica do Prestador na Plataforma contendo os seus servicos, descricao e avaliacoes.\n\n"
            "Listagem de servico — Um servico individual oferecido pelo Prestador no seu Perfil.\n\n"
            "Comissao — A taxa cobrada pela Nevumo pelos servicos de intermediacao, conforme especificado na Lista de precos vigente.\n\n"
            "Lista de precos — O documento que especifica as comissoes e taxas vigentes, disponivel em nevumo.com/pricing.\n\n"
            "Comerciante — Um Prestador que atua na qualidade de empresa (trabalhador independente, sociedade, etc.)."
        ),
        "pt-PT": (
            "Plataforma — O sitio web e aplicacao movel da Nevumo acessiveis em nevumo.com e os seus subdominios.\n\n"
            "Prestador — Uma pessoa singular com 18 anos ou mais, ou uma pessoa coletiva, registada na Plataforma para oferecer servicos.\n\n"
            "Cliente — Uma pessoa singular registada na Plataforma para procurar e encomendar servicos.\n\n"
            "Lead — Um pedido de servico submetido por um Cliente atraves da Plataforma.\n\n"
            "Perfil — A pagina publica do Prestador na Plataforma contendo os seus servicos, descricao e avaliacoes.\n\n"
            "Listagem de servico — Um servico individual oferecido pelo Prestador no seu Perfil.\n\n"
            "Comissao — A taxa cobrada pela Nevumo pelos servicos de intermediacao, conforme especificado na Lista de precos em vigor.\n\n"
            "Lista de precos — O documento que especifica as comissoes e taxas em vigor, disponivel em nevumo.com/pricing.\n\n"
            "Comerciante — Um Prestador que actua na qualidade de empresa (trabalhador independente, sociedade, etc.)."
        ),
        "ro": (
            "Platforma — Site-ul web si aplicatia mobila Nevumo accesibile la nevumo.com si subdomeniile sale.\n\n"
            "Furnizor — O persoana fizica de 18 ani sau mai mult, sau o persoana juridica, inregistrata pe Platforma pentru a oferi servicii.\n\n"
            "Client — O persoana fizica inregistrata pe Platforma pentru a cauta si comanda servicii.\n\n"
            "Lead — O solicitare de serviciu depusa de un Client prin intermediul Platformei.\n\n"
            "Profil — Pagina publica a Furnizorului pe Platforma care contine serviciile, descrierea si recenziile sale.\n\n"
            "Listare serviciu — Un serviciu individual oferit de Furnizor in cadrul Profilului sau.\n\n"
            "Comision — Taxa perceputa de Nevumo pentru serviciile de intermediere, conform Listei de preturi in vigoare.\n\n"
            "Lista de preturi — Documentul care specifica comisioanele si taxele in vigoare, disponibil la nevumo.com/pricing.\n\n"
            "Comerciant — Un Furnizor care actioneaza in calitate de intreprindere (persoana fizica autorizata, societate, etc.)."
        ),
        "ru": (
            "Platforma — Veb-sayt i mobilnoye prilozheniye Nevumo, dostupnoye po adresu nevumo.com i yego subdomenakh.\n\n"
            "Postavshchik — Fizicheskoye litso v vozraste 18 let i starshe ili yuridicheskoye litso, zaregistrirovannoye na Platforme dlya predlozheniya uslug.\n\n"
            "Klient — Fizicheskoye litso, zaregistrirovannoye na Platforme dlya poiska i zakaza uslug.\n\n"
            "Lid (Lead) — Zapros na uslugu, podannyy Klientom cherez Platformu.\n\n"
            "Profil — Publichнaya stranitsa Postavshchika na Platforme, soderzhashchaya yego uslugi, opisaniye i otzyvy.\n\n"
            "Ob'yavleniye ob usluge — Otdelnaya usluga, predlagayemaya Postavshchikom v ramkakh yego Profilya.\n\n"
            "Komissiya — Plata, vzimayemaya Nevumo za posrednicheskiye uslugi, soglasno deystvuyushchemu Preyskurantu.\n\n"
            "Preyskurant — Dokument, opredelyayushchiy tekushchiye komissii i sbory, dostupnyy na nevumo.com/pricing.\n\n"
            "Torgovets — Postavshchik, deystvuyushchiy v kachestve subyekta predprinimatelskoy deyatelnosti (IP, kompaniya i dr.)."
        ),
        "uk": (
            "Platforma — Veb-sayt ta mobilnyy dodatok Nevumo, dostupni za adresoyu nevumo.com ta yoho subdomenakh.\n\n"
            "Postachalnyk — Fizychna osoba vikom 18 rokiv abo starshe abo yurydychna osoba, zareyestrovana na Platformi dlya propozytsii posluh.\n\n"
            "Kliyent — Fizychna osoba, zareyestrovana na Platformi dlya poshuku ta zamovlennya posluh.\n\n"
            "Lid (Lead) — Zapyt na posluhu, podanyy Kliyentom cherez Platformu.\n\n"
            "Profil — Publichna storinka Postachalnika na Platformi, shcho mistyt yoho posluhy, opys ta vidhuky.\n\n"
            "Ogoloshennya pro posluhu — Okrema posluha, shcho proponuyetsya Postachalnikom u mezhakh yoho Profilyu.\n\n"
            "Komisiia — Plata, yaku styhaye Nevumo za poserednyts'ki posluhy vidpovidno do diyuchoho Preyskuranta.\n\n"
            "Preyskurant — Dokument, shcho vyznachaie potochni komisiini ta zbory, dostupnyy na nevumo.com/pricing.\n\n"
            "Torhovets — Postachalnyk, shcho diye yak sub'yekt pidpryyemnytskoi diyal'nosti (FOP, kompaniya tosho)."
        ),
        "cs": (
            "Platforma — Webove stranky a mobilni aplikace Nevumo dostupne na nevumo.com a jeho poddoménách.\n\n"
            "Poskytovatel — Fyzicka osoba ve veku 18 let nebo starsi nebo pravnicka osoba registrovana na Platforme za ucelem nabizeni sluzeb.\n\n"
            "Klient — Fyzicka osoba registrovana na Platforme za ucelem vyhledavani a objednavani sluzeb.\n\n"
            "Lead — Pozadavek na sluzbu podany Klientem prostrednictvim Platformy.\n\n"
            "Profil — Verejna stranka Poskytovatele na Platforme obsahujici jeho sluzby, popis a recenze.\n\n"
            "Nabidka sluzby — Individualni sluzba nabizena Poskytovatelem v ramci jeho Profilu.\n\n"
            "Provize — Poplatek ucturovany Nevumo za zprostredkovatelske sluzby dle aktualniho Ceniku.\n\n"
            "Cenik — Dokument specifikujici aktualni provize a poplatky, dostupny na nevumo.com/pricing.\n\n"
            "Obchodnik — Poskytovatel jednajici v postaveni podnikatele (OSVC, spolecnost atd.)."
        ),
        "da": (
            "Platform — Nevumos hjemmeside og mobilapp, der er tilgaengelige pa nevumo.com og dets subdomaener.\n\n"
            "Udbyder — En fysisk person pa 18 ar eller derover, eller en juridisk person, der er registreret pa Platformen til at tilbyde tjenester.\n\n"
            "Kunde — En fysisk person registreret pa Platformen til at soge og bestille tjenester.\n\n"
            "Lead — En tjenesteforesporgsel indsendt af en Kunde via Platformen.\n\n"
            "Profil — Udbyderens offentlige side pa Platformen med vedkommendes tjenester, beskrivelse og anmeldelser.\n\n"
            "Serviceopslag — En individuel tjeneste tilbudt af Udbyderen i dennes Profil.\n\n"
            "Provision — Det gebyr Nevumo opkraever for formidlingstjenester som angivet i den gaeldende Prisliste.\n\n"
            "Prisliste — Dokumentet, der angiver gaeldende provisioner og gebyrer, tilgaengeligt pa nevumo.com/pricing.\n\n"
            "Erhvervsdrivende — En Udbyder der optræder i egenskab af en virksomhed (selvstaendig, selskab osv.)."
        ),
        "sv": (
            "Plattform — Nevumos webbplats och mobilapplikation tillgangliga pa nevumo.com och dess spraksubdomaner.\n\n"
            "Leverantor — En fysisk person som ar 18 ar eller aldre, eller en juridisk person, registrerad pa Plattformen for att erbjuda tjanster.\n\n"
            "Kund — En fysisk person registrerad pa Plattformen for att soka och bestalla tjanster.\n\n"
            "Lead — En tjanstebegaran som skickats in av en Kund via Plattformen.\n\n"
            "Profil — Leverantorens offentliga sida pa Plattformen med deras tjanster, beskrivning och recensioner.\n\n"
            "Tjansteannons — En enskild tjanst som erbjuds av Leverantoren i deras Profil.\n\n"
            "Provision — Den avgift Nevumo tar ut for formedlingstjanster enligt den aktuella Prislistan.\n\n"
            "Prislista — Dokumentet som anger aktuella provisioner och avgifter, tillgangligt pa nevumo.com/pricing.\n\n"
            "Naringsidkare — En Leverantor som agerar i egenskap av foretag (enskild firma, bolag osv.)."
        ),
        "no": (
            "Plattform — Nevumos nettside og mobilapp tilgjengelig pa nevumo.com og dens spraksubdomener.\n\n"
            "Leverandor — En fysisk person pa 18 ar eller eldre, eller en juridisk person, registrert pa Plattformen for a tilby tjenester.\n\n"
            "Kunde — En fysisk person registrert pa Plattformen for a soke og bestille tjenester.\n\n"
            "Lead — En tjenesteforesprsel innsendt av en Kunde via Plattformen.\n\n"
            "Profil — Leverandorens offentlige side pa Plattformen med vedkommendes tjenester, beskrivelse og anmeldelser.\n\n"
            "Tjenesteliste — En individuell tjeneste tilbudt av Leverandoren i vedkommendes Profil.\n\n"
            "Provisjon — Gebyret Nevumo krever for formidlingstjenester i henhold til den gjeldende Prislisten.\n\n"
            "Prisliste — Dokumentet som angir gjeldende provisjoner og gebyrer, tilgjengelig pa nevumo.com/pricing.\n\n"
            "Naeringsdrivende — En Leverandor som opptrer i egenskap av en virksomhet (selvstendig naeringsdrivende, selskap osv.)."
        ),
        "fi": (
            "Alusta — Nevumon verkkosivusto ja mobiilisovellus, jotka ovat saatavilla osoitteessa nevumo.com ja sen aliverkkotunnuksilla.\n\n"
            "Palveluntarjoaja — 18 vuotta tayttanyt luonnollinen henkilo tai oikeushenkilö, joka on rekisteroitynyt Alustalle tarjoamaan palveluja.\n\n"
            "Asiakas — Luonnollinen henkilo, joka on rekisteroitynyt Alustalle palvelujen etsimiseksi ja tilaamiseksi.\n\n"
            "Liidi — Asiakkaan Alustan kautta lahettama palvelupyynto.\n\n"
            "Profiili — Palveluntarjoajan julkinen sivu Alustalla, joka sisaltaa palvelut, kuvauksen ja arvostelut.\n\n"
            "Palveluilmoitus — Palveluntarjoajan Profiilissaan tarjoama yksittainen palvelu.\n\n"
            "Provisio — Nevumon valityspalveluista perimat maksut nykyisen Hinnaston mukaisesti.\n\n"
            "Hinnasto — Asiakirja, joka maarittaa voimassa olevat provisiot ja maksut, saatavilla osoitteessa nevumo.com/pricing.\n\n"
            "Elinkeinonharjoittaja — Palveluntarjoaja, joka toimii yrityksena (itsenaisena ammatinharjoittajana, yhtiona jne.)."
        ),
        "et": (
            "Platvorm — Nevumo veebisait ja mobiilirakendus, mis on kattesaadavad aadressil nevumo.com ja selle alamdomeenidel.\n\n"
            "Teenusepakkuja — 18-aastane voi vanem fuusiline isik voi juriidiline isik, kes on registreerunud Platvormil teenuste pakkumiseks.\n\n"
            "Klient — Fuusiline isik, kes on registreerunud Platvormil teenuste otsimiseks ja tellimiseks.\n\n"
            "Liid — Kliendi poolt Platvormi kaudu esitatud teenuseparing.\n\n"
            "Profiil — Teenusepakkuja avalik leht Platvormil, mis sisaldab tema teenuseid, kirjeldust ja arvustusi.\n\n"
            "Teenusekuulutus — Teenusepakkuja poolt tema Profiilis pakutav uks konkreetne teenus.\n\n"
            "Vahendustasu — Nevumo poolt vahendamisteenuste eest voetav tasu vastavalt kehtivale Hinnakirjale.\n\n"
            "Hinnakiri — Dokument, mis maarab kindlaks kehtivad vahendustasud ja maksud, kattesaadav aadressil nevumo.com/pricing.\n\n"
            "Kaupmees — Teenusepakkuja, kes tegutseb ettevotte (FIE, uhing jne) rollis."
        ),
        "lt": (
            "Platforma — Nevumo svetaine ir mobilioji programa, prieinamos adresu nevumo.com ir jo subdomenams.\n\n"
            "Teikejas — 18 metu ar vyresnis fizinis asmuo arba juridinis asmuo, registruotas Platformoje teikti paslaugas.\n\n"
            "Klientas — Fizinis asmuo, registruotas Platformoje ieskantiems ir uzsakantiems paslaugas.\n\n"
            "Uzklausos (Lead) — Kliento per Platforma pateiktas paslaugu uzsakymas.\n\n"
            "Profilis — Viesoji Teikejo puslapis Platformoje, kuriame yra jo paslaugos, aprasymas ir atsiliepimai.\n\n"
            "Paslaugos skelbimas — Atskira paslauga, kurią Teikejas siulo savo Profilyje.\n\n"
            "Komisiniai — Nevumo imamas mokestis uz tarpininkavimo paslaugas pagal galiojanti Kainyną.\n\n"
            "Kainyna — Dokumentas, nurodantis galiojančius komisinius ir mokesciais, prieinamas adresu nevumo.com/pricing.\n\n"
            "Verslininkas — Teikejas, veikiantis kaip imone (savaiminis asmuo, bendrove ir pan.)."
        ),
        "lv": (
            "Platforma — Nevumo vietne un mobilā lietotne, kas pieejamas nevumo.com un tā apakšdomenos.\n\n"
            "Sniedzejs — 18 gadus vecs vai vecaks fiziskа persona vai juridiskа persona, kas reģistrēta Platformā pakalpojumu sniegšanai.\n\n"
            "Klients — Fiziskā persona, kas reģistrēta Platformā pakalpojumu meklēšanai un pasūtīšanai.\n\n"
            "Lids (Lead) — Pakalpojuma pieprasijums, ko Klients iesniedzis caur Platformu.\n\n"
            "Profils — Sniedzeja publiskā lapa Platformā, kurā ir viņa pakalpojumi, apraksts un atsauksmes.\n\n"
            "Pakalpojuma sludinājums — Atsevišķs pakalpojums, ko Sniedzejs piedāvā savā Profilā.\n\n"
            "Komisija — Nevumo iekasētā maksa par starpniecibas pakalpojumiem saskaņā ar spēkā esošo Cenrādi.\n\n"
            "Cenradis — Dokuments, kas precizē spēkā esošās komisijas un maksas, pieejams nevumo.com/pricing.\n\n"
            "Tirgotājs — Sniedzejs, kas darbojas uzņēmuma statusā (pašnodarbinātais, sabiedriba u.c.)."
        ),
        "hu": (
            "Platform — A Nevumo weboldal es mobilalkalmazas, amely a nevumo.com es aldomainjein erheto el.\n\n"
            "Szolgaltato — 18 eves vagy idosebb termeszetes szemely vagy jogi szemely, aki/amely a Platformon regisztralt, hogy szolgaltatasokat kinaljon.\n\n"
            "Ugyfel — A Platformon regisztralt termeszetes szemely, aki szolgaltatasokat keres es rendel.\n\n"
            "Lead — Az Ugyfel altal a Platformon keresztul benyujtott szolgaltatasikerelem.\n\n"
            "Profil — A Szolgaltato nyilvanos oldala a Platformon, amely tartalmazza szolgaltatasait, leirаsat es ertekelесеit.\n\n"
            "Szolgaltatasi hirdetes — A Szolgaltato altal a Profiljaban kinalт egyes szolgaltatas.\n\n"
            "Jutalek — A Nevumo altal kozvetitesi szolgaltatasokert felszamitott dij, az aktualis Araink szerint.\n\n"
            "Araink — Az aktualis jutalekokat es dijakat meghatározo dokumentum, elerheto: nevumo.com/pricing.\n\n"
            "Kereskedо — Vallalkozaskent eljaró Szolgaltato (onallo vallalkozo, ceg stb.)."
        ),
        "hr": (
            "Platforma — Web-stranica i mobilna aplikacija Nevumo dostupne na nevumo.com i njezinim poddomenama.\n\n"
            "Pruzatelj — Fizicka osoba od 18 godina ili starija, ili pravna osoba, registrirana na Platformi za ponudu usluga.\n\n"
            "Klijent — Fizicka osoba registrirana na Platformi za trazenje i narudzbu usluga.\n\n"
            "Lead — Zahtjev za uslugom koji je Klijent podnio putem Platforme.\n\n"
            "Profil — Javna stranica Pruzatelja na Platformi koja sadrzi njegove usluge, opis i recenzije.\n\n"
            "Ponuda usluge — Pojedinacna usluga koju Pruzatelj nudi u okviru svog Profila.\n\n"
            "Provizija — Naknada koju Nevumo naplacuje za posrednicke usluge sukladno aktualnom Cjeniku.\n\n"
            "Cjenik — Dokument koji odreduje aktualne provizije i naknade, dostupan na nevumo.com/pricing.\n\n"
            "Obrtnik/Poduzetnik — Pruzatelj koji djeluje u svojstvu poslovnog subjekta (obrt, drustvo itd.)."
        ),
        "sk": (
            "Platforma — Webova stranka a mobilna aplikacia Nevumo dostupne na nevumo.com a jeho poddoménách.\n\n"
            "Poskytovatel — Fyzicka osoba vo veku 18 rokov alebo starsia alebo pravnicka osoba registrovana na Platforme za ucelom ponuky sluzieb.\n\n"
            "Zakaznik — Fyzicka osoba registrovana na Platforme za ucelom vyhladavania a objednavania sluzieb.\n\n"
            "Lead — Poziadavka na sluzbu podana Zakaznikom prostredníctvom Platformy.\n\n"
            "Profil — Verejna stranka Poskytovatela na Platforme obsahujuca jeho sluzby, popis a recenzie.\n\n"
            "Ponuka sluzby — Individualna sluzba ponukana Poskytovatelom v ramci jeho Profilu.\n\n"
            "Proviziya — Poplatok uctovany Nevumo za sprostredkovatel'ske sluzby podla aktualneho Cennika.\n\n"
            "Cennik — Dokument specifikujuci aktualne provizii a poplatky, dostupny na nevumo.com/pricing.\n\n"
            "Obchodnik — Poskytovatel konajuci v postaveni podnikatel'a (zivnostnik, spolocnost atd.)."
        ),
        "sl": (
            "Platforma — Nevumovo spletno mesto in mobilna aplikacija, dostopna na nevumo.com in njegovih poddomenah.\n\n"
            "Ponudnik — Fizicna oseba, stara 18 let ali vec, ali pravna oseba, registrirana na Platformi za ponudbo storitev.\n\n"
            "Stranka — Fizicna oseba, registrirana na Platformi za iskanje in narocanje storitev.\n\n"
            "Lead — Zahteva za storitev, ki jo je Stranka predlozila prek Platforme.\n\n"
            "Profil — Javna stran Ponudnika na Platformi, ki vsebuje njegove storitve, opis in ocene.\n\n"
            "Oglas storitve — Posamezna storitev, ki jo Ponudnik ponuja v svojem Profilu.\n\n"
            "Provizija — Pristojbina, ki jo Nevumo zaracuna za posredniske storitve v skladu z veljavnim Cenikom.\n\n"
            "Cenik — Dokument, ki doloca veljavne provizije in pristojbine, dostopen na nevumo.com/pricing.\n\n"
            "Podjetnik — Ponudnik, ki deluje v vlogi podjetja (samostojni podjetnik, druzba itd.)."
        ),
        "el": (
            "Platforma — O iston kai i kiniti efarmogi tis Nevumo pou einai prósita sto nevumo.com kai ta ypodomeinia tis.\n\n"
            "Párochos — Fysiko prósoopo 18 eton kai ano, i nomiko prósoopo, eggegramméno stin Platforma gia na prosthetei ypiresies.\n\n"
            "Pelatis — Fysiko prósoopo eggegramméno stin Platforma gia na anazetitei kai na paraggéllei ypiresies.\n\n"
            "Lid — Aitima gia ypiresia pou ypoballei o Pelatis meso tis Platformas.\n\n"
            "Profil — I dimósia selida tou Paróchou stin Platforma pou periechei tis ypiresies, tin perigraphi kai tis kritikas tou.\n\n"
            "Katálogos Ypiresion — Mia ekásti ypiresia pou prosthetei o Párochos sto Profil tou.\n\n"
            "Provmitheia — I amivi pou eparattei i Nevumo gia ypiresies diamesolabisis, symfonos me ton ischyonta Timokatalogo.\n\n"
            "Timokatalogos — To eggrafo pou katharizo tis ischyouses provmitheies kai telis, diathesimo sto nevumo.com/pricing.\n\n"
            "Émporos — Párochos pou energei os epicheirisias (aftoapascholoumenos, etairia k.tp.)."
        ),
        "tr": (
            "Platform — nevumo.com ve alt alanlarinda erisebilen Nevumo web sitesi ve mobil uygulamasi.\n\n"
            "Saglayici — Hizmet sunmak icin Platformda kayitli 18 yas ve uzeri bir gercek kisi veya tuzel kisi.\n\n"
            "Musteri — Hizmet aramak ve siparis vermek icin Platformda kayitli gercek kisi.\n\n"
            "Lead — Bir Musteri tarafindan Platform araciligiyla gonderilen hizmet talebi.\n\n"
            "Profil — Saglayicinin Platform uzerindeki, hizmetlerini, aciklamasini ve degerlendirmelerini iceren genel sayfasi.\n\n"
            "Hizmet Listesi — Saglayicinin Profilinde sunduğu bireysel bir hizmet.\n\n"
            "Komisyon — Nevumo'nun mevcut Fiyat Listesinde belirtildigi sekilde aracilik hizmetleri icin aldigi ucret.\n\n"
            "Fiyat Listesi — Mevcut komisyonlari ve ucretleri belirten, nevumo.com/pricing adresinde mevcut belge.\n\n"
            "Tacir — Bir isletme sifatiyla hareket eden Saglayici (serbest meslek sahibi, sirket vb.)."
        ),
        "ga": (
            "Ardan — Suiomh gréasáin agus feidhmchlár móibíleach Nevumo inrochtana ar nevumo.com agus a fothainne.\n\n"
            "Solathroir — Duine nádurtha 18 bliana d'aois nó os a chionn, nó eintit dhlithiúil, cláraithe ar an Ardan chun seirbhísí a thairiscint.\n\n"
            "Custoimeir — Duine nádurtha cláraithe ar an Ardan chun seirbhísí a lorg agus a ordú.\n\n"
            "Lead — Iarratas seirbhíse a chuireann Custoimeir isteach tríd an Ardan.\n\n"
            "Proifil — Leathanach poiblí an tSolathraio ar an Ardan ina bhfuil a sheirbhísí, a thuairisc agus a léirmheasanna.\n\n"
            "Liostáil Seirbhíse — Seirbhís aonair a thairgeann an Solathroir ina Phroifil.\n\n"
            "Coimisiún — An táille a ghearrann Nevumo ar sheirbhísí idirghabhála, mar a shonraítear sa Liosta Praghsanna reatha.\n\n"
            "Liosta Praghsanna — An doiciméad a shonraíonn na coimisiúin agus na táillí reatha, ar fáil ag nevumo.com/pricing.\n\n"
            "Tradeir — Solathroir a ghníomhaíonn i gcáil gnólachta (féinfhostaithe, cuideachta, etc.)."
        ),
        "is": (
            "Vettvangur — Nevumo vefsida og farsima forrit sem er adgengilegt a nevumo.com og undirdomena þess.\n\n"
            "Veituadili — Einstaklingur 18 ara edur eldri, edur logaðili, skrаður á Vettvangi til að bjoda upp á þjonustu.\n\n"
            "Vidskiptavinur — Einstaklingur skrаður á Vettvangi til að leita að og panta þjonustu.\n\n"
            "Lead — Þjonustubeiðni sem Vidskiptavinur sendir inn í gegnum Vettvanginn.\n\n"
            "Notandasnid — Almenna síðan hjá Veituadilanum á Vettvangi sem inniheldur þjonustu hans, lýsingu og umsagnir.\n\n"
            "Þjonustufærsla — Einstaklingsþjonusta sem Veituadilinn býður upp á í sínu Notandasniði.\n\n"
            "Þoknun — Gjaldet sem Nevumo innheimtir fyrir milligonguþjonustu samkvæmt gildandi Verdskrá.\n\n"
            "Verdskra — Skjalid sem tilgreinir gildandi þoknanir og gjöld, fáanlegt á nevumo.com/pricing.\n\n"
            "Kaupmadur — Veituadili sem starfar í þágu fyrirtækis (sjálfstætt starfandi, félag o.fl.)."
        ),
        "lb": (
            "Plattform — D'Nevumo-Website an Handyapp, déi op nevumo.com an senge Sprooch-Ënnerdomeinen zougänglech sinn.\n\n"
            "Presser — Eng natierlesch Persoun vun 18 Joer oder aelter, oder eng Gesellschaft, déi sech op der Plattform aschreift fir Servicer unzebidden.\n\n"
            "Client — Eng natierlesch Persoun déi op der Plattform ageschriwwen ass fir Servicer ze sichen an ze bestellen.\n\n"
            "Lead — Eng Servicufro vun engem Client iwwer d'Plattform agereecht.\n\n"
            "Profil — D'oeffentlech Säit vum Presser op der Plattform mat senge Servicer, Beschreiwung an Bewäertungen.\n\n"
            "Serviceannonce — E Einzelservice deen de Presser a sengem Profil ubitt.\n\n"
            "Kommissioun — D'Gebuehr déi Nevumo fir Vermëttlungsservicer in Rechnung stellt laut der aktueller Präislëschte.\n\n"
            "Präislëschte — D'Dokument dat d'aktuell Kommissiounen a Gebuehren festleet, verfügbar op nevumo.com/pricing.\n\n"
            "Händler — E Presser deen als Betrieb (Selbstaendeger, Gesellschaft asw.) handelt."
        ),
        "mk": (
            "Platforma — Veb-stranicata i mobilnata aplikacija na Nevumo dostapni na nevumo.com i negovite poddomen.\n\n"
            "Davac — Fizicko lice na 18 godini ili postaro, ili pravno lice, registrirano na Platformata za nudienje uslugi.\n\n"
            "Klient — Fizicko lice registrirano na Platformata za baranje i naruchuvanje uslugi.\n\n"
            "Lead — Baranje za usluga podnесено od Klient preku Platformata.\n\n"
            "Profil — Javnata stranica na Davacot na Platformata koja gi sodrzi negovite uslugi, opis i komentari.\n\n"
            "Oglas za usluga — Poeddinecna usluga koja Davacot ja nuди vo ramkite na negoviot Profil.\n\n"
            "Provizija — Naknadata sto Nevumo ja naplacuva za posrednichki uslugi spored vaznechkiot Cenovnik.\n\n"
            "Cenovnik — Dokumentот sto gi odreduva tekuchnite provizii i naknadi, dostapen na nevumo.com/pricing.\n\n"
            "Trgovets — Davac koj dejstvuva vo svojstvo na biznis subjekt (samovraboten, drushtvo i sl.)."
        ),
        "mt": (
            "Pjattaforma — Il-website u l-applikazzjoni mobbli ta' Nevumo accessibbli fuq nevumo.com u s-subdomeni tieghu.\n\n"
            "Fornitur — Persuna fizika ta' 18-il sena jew aktar, jew entita legali, registrata fuq il-Pjattaforma biex toffri servizzi.\n\n"
            "Klijent — Persuna fizika registrata fuq il-Pjattaforma biex tfittex u tordna servizzi.\n\n"
            "Lead — Talba ghal servizz imressqa minn Klijent permezz tal-Pjattaforma.\n\n"
            "Profil — Il-pagna pubblika tal-Fornitur fuq il-Pjattaforma li fiha s-servizzi tieghu, deskrizzjoni u reviews.\n\n"
            "Listata ta' Servizz — Servizz individwali offrut mill-Fornitur fil-Profil tieghu.\n\n"
            "Kummissjoni — It-tariffa imposta minn Nevumo ghal servizzi ta' intermedjarjament kif speċifikat fil-Lista tal-Prezz attwali.\n\n"
            "Lista tal-Prezz — Id-dokument li jispeċifika l-kummissjonijiet u t-tariffi attwali, disponibbli fuq nevumo.com/pricing.\n\n"
            "Negozjant — Fornitur li jaghmel il-haġa tieghu bhala negozju (persuna awtonoma, kumpanija ecc.)."
        ),
        "sq": (
            "Platforma — Faqja e internetit dhe aplikacioni celular i Nevumo i aksesueshëm ne nevumo.com dhe nëndomenet e tij.\n\n"
            "Ofrues — Nje person fizik 18 vjecjar ose me i madh, ose nje person juridik, i regjistruar ne Platform per te ofruar sherbime.\n\n"
            "Klient — Nje person fizik i regjistruar ne Platform per te kerkuar dhe porositur sherbime.\n\n"
            "Lead — Nje kerkese sherbimi e derguar nga nje Klient nepermjet Platforma.\n\n"
            "Profil — Faqja publike e Ofruesit ne Platform qe permban sherbimet, pershkrimin dhe vleresim et e tij.\n\n"
            "Listim Sherbimi — Nje sherbim individual i ofruar nga Ofruesi brenda Profilit te tij.\n\n"
            "Komision — Tarifa e ngarkuar nga Nevumo per sherbimet e ndermjetesimit sipas Listes Aktuale te Cmimeve.\n\n"
            "Lista e Cmimeve — Dokumenti qe specifikon komisionet dhe tarifat aktuale, i disponueshem ne nevumo.com/pricing.\n\n"
            "Tregtar — Nje Ofrues qe vepron ne cilesine e nje biznesi (i vetepunesuar, kompani, etj.)."
        ),
        "sr": (
            "Platforma — Veb-stranica i mobilna aplikacija Nevumo dostupne na nevumo.com i njenim poddomenima.\n\n"
            "Pruzalac — Fizicko lice od 18 godina ili starije, ili pravno lice, registrovano na Platformi za ponudu usluga.\n\n"
            "Klijent — Fizicko lice registrovano na Platformi za trazenje i narucivanje usluga.\n\n"
            "Lead — Zahtev za uslugom koji je Klijent podneo putem Platforme.\n\n"
            "Profil — Javna stranica Pruzaoca na Platformi koja sadrzi njegove usluge, opis i recenzije.\n\n"
            "Oglas usluge — Pojedinacna usluga koju Pruzalac nudi u okviru svog Profila.\n\n"
            "Provizija — Naknada koju Nevumo naplacuje za posrednicke usluge prema vazecim Cenovniku.\n\n"
            "Cenovnik — Dokument koji odredjuje vazece provizije i naknade, dostupan na nevumo.com/pricing.\n\n"
            "Trgovac — Pruzalac koji deluje u svojstvu poslovnog subjekta (preduzetnik, drustvo itd.)."
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
        print(
            f"✅ seed_provider_terms_p9_art2_body: {count} rows upserted "
            f"({NAMESPACE}: art2_body x 34 langs)"
        )

    engine.dispose()


if __name__ == "__main__":
    seed()
