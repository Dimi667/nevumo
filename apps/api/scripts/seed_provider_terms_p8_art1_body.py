"""
seed_provider_terms_p8_art1_body.py  —  Nevumo | namespace: provider_terms
Key: art1_body  (1 key x 34 langs = 34 rows)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_provider_terms_p8_art1_body
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
    "art1_body": {
        "en": (
            "1.1 These Terms & Conditions for Service Providers (Provider Terms) govern the relationship between Nevumo and any natural person or legal entity that registers on the Nevumo platform as a service provider (Provider, you).\n\n"
            "1.2 Nevumo operates an online marketplace at nevumo.com and its language subdomains (Platform) that enables Providers to present their services and connects them with clients seeking those services (Clients).\n\n"
            "1.3 Nevumo acts solely as an intermediary. Nevumo is not a party to any service agreement concluded between a Provider and a Client. Nevumo does not provide the services offered by Providers, does not employ Providers, and bears no liability for the quality, completeness, or timely execution of any services.\n\n"
            "1.4 These Provider Terms constitute a binding agreement between you and Nevumo. By completing registration as a Provider, you confirm that you have read, understood, and accepted these Provider Terms in full.\n\n"
            "1.5 These Provider Terms apply in addition to Nevumo's general Terms & Conditions for Users. In the event of conflict, these Provider Terms take precedence with respect to the Provider relationship.\n\n"
            "1.6 These Provider Terms were drawn up in compliance with Regulation (EU) 2019/1150 on promoting fairness and transparency for business users of online intermediation services (P2B Regulation)."
        ),
        "pl": (
            "1. Niniejszy Regulamin dla Dostawcow Uslug (Regulamin Dostawcow) okresla zasady i warunki korzystania z platformy Nevumo przez uzytkownikow rejestrujacych sie jako dostawcy uslug (Dostawca).\n\n"
            "2. Nevumo prowadzi internetowa platforme posrednictwa uslugowego dostepna pod adresem nevumo.com oraz jej poddomenwami jezykowymi (Platforma), ktora umozliwia Dostawcom prezentowanie swoich uslug oraz laczy ich z klientami poszukujacymi tych uslug (Klienci).\n\n"
            "3. Nevumo pelni wylacznie role posrednika i nie jest strona zadnej umowy o swiadczenie uslug zawieranej pomiedzy Dostawca a Klientem. Nevumo nie swiadczy uslug oferowanych przez Dostawcow, nie zatrudnia Dostawcow i nie ponosi odpowiedzialnosci za jakosc, zakres ani terminowosc wykonania uslug.\n\n"
            "4. Niniejszy Regulamin Dostawcow stanowi wiazaca umowe pomiedzy Dostawca a Nevumo. Dokonujac rejestracji jako Dostawca, potwierdzasz, ze zapoznales sie z trescia Regulaminu Dostawcow, rozumiesz go i akceptujesz go w calosci.\n\n"
            "5. Niniejszy Regulamin Dostawcow stosuje sie lacznie z ogolnym Regulaminem Nevumo dla Uzytkownikow. W przypadku sprzecznosci, Regulamin Dostawcow ma pierwszenstwo w zakresie relacji z Dostawcami.\n\n"
            "6. Niniejszy Regulamin Dostawcow zostal sporzadzony zgodnie z wymogami Rozporzadzenia P2B (UE) 2019/1150 w sprawie propagowania sprawiedliwosci i przejrzystosci dla uzytkownikow biznesowych korzystajacych z uslug posrednictwa internetowego.\n\n"
            "7. Zabrania sie dostarczania przez Dostawcow tresci o charakterze bezprawnym."
        ),
        "bg": (
            "1.1 Настоящите Условия за Доставчици на Услуги (Условия за Доставчици) уреждат отношенията между Nevumo и всяко физическо лице или юридическо лице, което се регистрира в платформата Nevumo като доставчик на услуги (Доставчик).\n\n"
            "1.2 Nevumo управлява онлайн пазар на nevumo.com и неговите езикови поддомейни (Платформа), който позволява на Доставчиците да представят своите услуги и ги свързва с клиенти, търсещи тези услуги (Клиенти).\n\n"
            "1.3 Nevumo действа единствено като посредник. Nevumo не е страна по никакво споразумение за услуги, сключено между Доставчик и Клиент. Nevumo не предоставя услугите, предлагани от Доставчиците, не наема Доставчици и не носи отговорност за качеството, пълнотата или навременното изпълнение на каквито и да е услуги.\n\n"
            "1.4 Настоящите Условия за Доставчици представляват обвързващо споразумение между вас и Nevumo. Като завършите регистрацията като Доставчик, вие потвърждавате, че сте прочели, разбрали и приели изцяло настоящите Условия за Доставчици.\n\n"
            "1.5 Настоящите Условия за Доставчици се прилагат в допълнение към общите Условия за ползване на Nevumo. При противоречие настоящите Условия за Доставчици имат предимство по отношение на доставчическото правоотношение.\n\n"
            "1.6 Настоящите Условия за Доставчици са изготвени в съответствие с Регламент (ЕС) 2019/1150 за насърчаване на справедливостта и прозрачността за бизнес ползвателите на услуги за онлайн посредничество (Регламент P2B)."
        ),
        "cs": (
            "1.1 Tyto Podminky pro Poskytovatele Sluzeb (Podminky poskytovatele) upravuji vztah mezi Nevumo a jakoukoli fyzickou nebo pravnickou osobou, ktera se na platforme Nevumo registruje jako poskytovatel sluzeb (Poskytovatel).\n\n"
            "1.2 Nevumo provozuje online trziste na nevumo.com a jeho jazykových poddoménách (Platforma), ktera umoznuje Poskytovatelum prezentovat jejich sluzby a spojuje je s klienty hledajicimi tyto sluzby (Klienti).\n\n"
            "1.3 Nevumo jedná výhradně jako zprostředkovatel. Nevumo není stranou zadne smlouvy o poskytovani sluzeb uzavrene mezi Poskytovatelem a Klientem. Nevumo neposkytuje sluzby nabizene Poskytovateli, nezamestnava Poskytovatele a nenese zadnou odpovednost za kvalitu, uplnost nebo vcasne plneni jakychkoliv sluzeb.\n\n"
            "1.4 Tyto Podminky poskytovatele tvoři závaznou dohodu mezi vámi a Nevumo. Dokoncenim registrace jako Poskytovatele potvrzujete, ze jste si Podminky poskytovatele precetli, porozumeli jim a v plnem rozsahu je prijali.\n\n"
            "1.5 Tyto Podminky poskytovatele se uplatnuji vedle obecnych Podminek pouzivani Nevumo pro uzivatele. V pripade rozporu maji tyto Podminky poskytovatele prednost v oblasti vztahu s Poskytovatelem.\n\n"
            "1.6 Tyto Podminky poskytovatele byly vypracovany v souladu s Narizenim (EU) 2019/1150 o podpore spravedlnosti a transparentnosti pro podnikove uzivatele online zprostredkovatelskych sluzeb (Narizeni P2B)."
        ),
        "de": (
            "1.1 Diese Nutzungsbedingungen für Dienstleister (Dienstleisterbedingungen) regeln die Beziehung zwischen Nevumo und jeder natürlichen oder juristischen Person, die sich auf der Nevumo-Plattform als Dienstleister registriert (Dienstleister, Sie).\n\n"
            "1.2 Nevumo betreibt einen Online-Marktplatz unter nevumo.com und seinen Sprachsubdomains (Plattform), der es Dienstleistern ermöglicht, ihre Dienstleistungen zu präsentieren, und sie mit Kunden verbindet, die diese Dienstleistungen suchen (Kunden).\n\n"
            "1.3 Nevumo handelt ausschließlich als Vermittler. Nevumo ist keine Partei eines zwischen einem Dienstleister und einem Kunden geschlossenen Dienstleistungsvertrags. Nevumo erbringt nicht die von Dienstleistern angebotenen Leistungen, beschäftigt keine Dienstleister und haftet nicht für die Qualität, Vollständigkeit oder rechtzeitige Ausführung von Leistungen.\n\n"
            "1.4 Diese Dienstleisterbedingungen stellen eine verbindliche Vereinbarung zwischen Ihnen und Nevumo dar. Mit dem Abschluss der Registrierung als Dienstleister bestätigen Sie, dass Sie diese Dienstleisterbedingungen gelesen, verstanden und vollständig akzeptiert haben.\n\n"
            "1.5 Diese Dienstleisterbedingungen gelten zusätzlich zu den allgemeinen Nutzungsbedingungen von Nevumo für Nutzer. Im Konfliktfall haben diese Dienstleisterbedingungen in Bezug auf das Dienstleisterverhältnis Vorrang.\n\n"
            "1.6 Diese Dienstleisterbedingungen wurden in Übereinstimmung mit der Verordnung (EU) 2019/1150 zur Förderung von Fairness und Transparenz für gewerbliche Nutzer von Online-Vermittlungsdiensten (P2B-Verordnung) erstellt."
        ),
        "fr": (
            "1.1 Les presentes Conditions pour les Prestataires de Services (Conditions prestataires) regissent la relation entre Nevumo et toute personne physique ou morale qui s'inscrit sur la plateforme Nevumo en tant que prestataire de services (Prestataire, vous).\n\n"
            "1.2 Nevumo exploite une place de marche en ligne sur nevumo.com et ses sous-domaines linguistiques (Plateforme) qui permet aux Prestataires de presenter leurs services et les met en relation avec des clients recherchant ces services (Clients).\n\n"
            "1.3 Nevumo agit uniquement en tant qu'intermediaire. Nevumo n'est pas partie a un accord de services conclu entre un Prestataire et un Client. Nevumo ne fournit pas les services proposes par les Prestataires, n'emploie pas les Prestataires et n'assume aucune responsabilite quant a la qualite, l'exhaustivite ou l'execution en temps voulu des services.\n\n"
            "1.4 Les presentes Conditions prestataires constituent un accord contraignant entre vous et Nevumo. En finalisant votre inscription en tant que Prestataire, vous confirmez avoir lu, compris et accepte integralement les presentes Conditions prestataires.\n\n"
            "1.5 Les presentes Conditions prestataires s'appliquent en complement des Conditions generales d'utilisation de Nevumo pour les utilisateurs. En cas de conflit, les presentes Conditions prestataires priment en ce qui concerne la relation prestataire.\n\n"
            "1.6 Les presentes Conditions prestataires ont ete elaborees conformement au Reglement (UE) 2019/1150 promouvant l'equite et la transparence pour les entreprises utilisatrices des services d'intermediation en ligne (Reglement P2B)."
        ),
        "es": (
            "1.1 Los presentes Terminos y Condiciones para Proveedores de Servicios (Terminos del proveedor) rigen la relacion entre Nevumo y cualquier persona fisica o juridica que se registre en la plataforma Nevumo como proveedor de servicios (Proveedor, usted).\n\n"
            "1.2 Nevumo opera un mercado en linea en nevumo.com y sus subdominios de idioma (Plataforma) que permite a los Proveedores presentar sus servicios y los conecta con clientes que buscan dichos servicios (Clientes).\n\n"
            "1.3 Nevumo actua unicamente como intermediario. Nevumo no es parte de ningun acuerdo de servicios celebrado entre un Proveedor y un Cliente. Nevumo no presta los servicios ofrecidos por los Proveedores, no emplea a Proveedores y no asume ninguna responsabilidad por la calidad, integridad o ejecucion puntual de los servicios.\n\n"
            "1.4 Los presentes Terminos del proveedor constituyen un acuerdo vinculante entre usted y Nevumo. Al completar el registro como Proveedor, confirma que ha leido, comprendido y aceptado en su totalidad los presentes Terminos del proveedor.\n\n"
            "1.5 Los presentes Terminos del proveedor se aplican adicionalmente a los Terminos y Condiciones generales de Nevumo para usuarios. En caso de conflicto, los presentes Terminos del proveedor prevalecen con respecto a la relacion con el proveedor.\n\n"
            "1.6 Los presentes Terminos del proveedor fueron elaborados de conformidad con el Reglamento (UE) 2019/1150 sobre el fomento de la equidad y la transparencia para los usuarios empresariales de los servicios de intermediacion en linea (Reglamento P2B)."
        ),
        "it": (
            "1.1 I presenti Termini e Condizioni per i Fornitori di Servizi (Termini del fornitore) disciplinano il rapporto tra Nevumo e qualsiasi persona fisica o giuridica che si registra sulla piattaforma Nevumo come fornitore di servizi (Fornitore, tu).\n\n"
            "1.2 Nevumo gestisce un mercato online su nevumo.com e i suoi sottodomini linguistici (Piattaforma) che consente ai Fornitori di presentare i propri servizi e li mette in contatto con i clienti che cercano tali servizi (Clienti).\n\n"
            "1.3 Nevumo agisce esclusivamente come intermediario. Nevumo non e parte di alcun accordo di servizi concluso tra un Fornitore e un Cliente. Nevumo non fornisce i servizi offerti dai Fornitori, non impiega Fornitori e non si assume alcuna responsabilita per la qualita, la completezza o l'esecuzione tempestiva dei servizi.\n\n"
            "1.4 I presenti Termini del fornitore costituiscono un accordo vincolante tra te e Nevumo. Completando la registrazione come Fornitore, confermi di aver letto, compreso e accettato integralmente i presenti Termini del fornitore.\n\n"
            "1.5 I presenti Termini del fornitore si applicano in aggiunta ai Termini e Condizioni generali di Nevumo per gli utenti. In caso di conflitto, i presenti Termini del fornitore prevalgono in relazione al rapporto con il fornitore.\n\n"
            "1.6 I presenti Termini del fornitore sono stati redatti in conformita al Regolamento (UE) 2019/1150 che promuove equita e trasparenza per gli utenti commerciali dei servizi di intermediazione online (Regolamento P2B)."
        ),
        "nl": (
            "1.1 Deze Algemene Voorwaarden voor Dienstverleners (Dienstverlenersvoorwaarden) regelen de relatie tussen Nevumo en elke natuurlijke persoon of rechtspersoon die zich op het Nevumo-platform registreert als dienstverlener (Dienstverlener, u).\n\n"
            "1.2 Nevumo exploiteert een online marktplaats op nevumo.com en zijn taalsubdomeinen (Platform) waarmee Dienstverleners hun diensten kunnen presenteren en worden verbonden met klanten die op zoek zijn naar die diensten (Klanten).\n\n"
            "1.3 Nevumo treedt uitsluitend op als tussenpersoon. Nevumo is geen partij bij een dienstverleningsovereenkomst gesloten tussen een Dienstverlener en een Klant. Nevumo verleent de door Dienstverleners aangeboden diensten niet, heeft geen Dienstverleners in dienst en aanvaardt geen aansprakelijkheid voor de kwaliteit, volledigheid of tijdige uitvoering van diensten.\n\n"
            "1.4 Deze Dienstverlenersvoorwaarden vormen een bindende overeenkomst tussen u en Nevumo. Door de registratie als Dienstverlener te voltooien, bevestigt u dat u deze Dienstverlenersvoorwaarden volledig hebt gelezen, begrepen en aanvaard.\n\n"
            "1.5 Deze Dienstverlenersvoorwaarden zijn van toepassing naast de algemene Gebruiksvoorwaarden van Nevumo. Bij conflict hebben deze Dienstverlenersvoorwaarden voorrang met betrekking tot de dienstverlenerrelatie.\n\n"
            "1.6 Deze Dienstverlenersvoorwaarden zijn opgesteld in overeenstemming met Verordening (EU) 2019/1150 ter bevordering van billijkheid en transparantie voor zakelijke gebruikers van onlinetussenhandelsdiensten (P2B-verordening)."
        ),
        "pt": (
            "1.1 Estes Termos e Condicoes para Prestadores de Servicos (Termos do prestador) regem a relacao entre a Nevumo e qualquer pessoa singular ou coletiva que se registe na plataforma Nevumo como prestador de servicos (Prestador, voce).\n\n"
            "1.2 A Nevumo opera um mercado online em nevumo.com e seus subdominios de idioma (Plataforma) que permite aos Prestadores apresentar os seus servicos e os conecta com clientes que procuram esses servicos (Clientes).\n\n"
            "1.3 A Nevumo atua exclusivamente como intermediaria. A Nevumo nao e parte de qualquer acordo de servicos celebrado entre um Prestador e um Cliente. A Nevumo nao presta os servicos oferecidos pelos Prestadores, nao emprega Prestadores e nao assume qualquer responsabilidade pela qualidade, integralidade ou execucao pontual dos servicos.\n\n"
            "1.4 Estes Termos do prestador constituem um acordo vinculativo entre voce e a Nevumo. Ao concluir o registo como Prestador, confirma que leu, compreendeu e aceitou integralmente estes Termos do prestador.\n\n"
            "1.5 Estes Termos do prestador aplicam-se adicionalmente aos Termos e Condicoes gerais da Nevumo para utilizadores. Em caso de conflito, estes Termos do prestador prevalecem no que diz respeito a relacao com o prestador.\n\n"
            "1.6 Estes Termos do prestador foram elaborados em conformidade com o Regulamento (UE) 2019/1150 relativo a promocao da equidade e da transparencia para os utilizadores profissionais dos servicos de intermediacao em linha (Regulamento P2B)."
        ),
        "pt-PT": (
            "1.1 Estes Termos e Condicoes para Prestadores de Servicos (Termos do prestador) regem a relacao entre a Nevumo e qualquer pessoa singular ou coletiva que se registe na plataforma Nevumo como prestador de servicos (Prestador, V. Exa.).\n\n"
            "1.2 A Nevumo opera um mercado em linha em nevumo.com e nos seus subdominios linguisticos (Plataforma) que permite aos Prestadores apresentar os seus servicos e os liga a clientes que procuram esses servicos (Clientes).\n\n"
            "1.3 A Nevumo actua exclusivamente como intermediaria. A Nevumo nao e parte de qualquer acordo de prestacao de servicos celebrado entre um Prestador e um Cliente. A Nevumo nao presta os servicos oferecidos pelos Prestadores, nao emprega Prestadores e nao assume qualquer responsabilidade pela qualidade, integralidade ou execucao atempada dos servicos.\n\n"
            "1.4 Estes Termos do prestador constituem um acordo vinculativo entre si e a Nevumo. Ao concluir o registo como Prestador, confirma que leu, compreendeu e aceitou integralmente estes Termos do prestador.\n\n"
            "1.5 Estes Termos do prestador aplicam-se adicionalmente aos Termos e Condicoes gerais da Nevumo para utilizadores. Em caso de conflito, estes Termos do prestador prevalecem no que respeita a relacao com o prestador.\n\n"
            "1.6 Estes Termos do prestador foram elaborados em conformidade com o Regulamento (UE) 2019/1150 relativo a promocao da equidade e da transparencia para os utilizadores profissionais dos servicos de intermediacao em linha (Regulamento P2B)."
        ),
        "ro": (
            "1.1 Prezentii Termeni si Conditii pentru Furnizorii de Servicii (Termenii furnizorului) reglementeaza relatia dintre Nevumo si orice persoana fizica sau juridica care se inregistreaza pe platforma Nevumo ca furnizor de servicii (Furnizor, dumneavoastra).\n\n"
            "1.2 Nevumo opereaza o piata online la nevumo.com si subdomeniile sale lingvistice (Platforma) care le permite Furnizorilor sa isi prezinte serviciile si ii conecteaza cu clientii care cauta aceste servicii (Clienti).\n\n"
            "1.3 Nevumo actioneaza exclusiv ca intermediar. Nevumo nu este parte la niciun acord de servicii incheiat intre un Furnizor si un Client. Nevumo nu presteaza serviciile oferite de Furnizori, nu angajeaza Furnizori si nu isi asuma nicio responsabilitate pentru calitatea, integralitatea sau executarea la timp a oricaror servicii.\n\n"
            "1.4 Prezentii Termeni ai furnizorului constituie un acord obligatoriu intre dumneavoastra si Nevumo. Prin finalizarea inregistrarii ca Furnizor, confirmati ca ati citit, inteles si acceptat integral prezentii Termeni ai furnizorului.\n\n"
            "1.5 Prezentii Termeni ai furnizorului se aplica suplimentar fata de Termenii si Conditiile generale ale Nevumo pentru utilizatori. In caz de conflict, prezentii Termeni ai furnizorului au prioritate in ceea ce priveste relatia cu furnizorul.\n\n"
            "1.6 Prezentii Termeni ai furnizorului au fost elaborati in conformitate cu Regulamentul (UE) 2019/1150 privind promovarea echitatii si a transparentei pentru utilizatorii comerciali ai serviciilor de intermediere online (Regulamentul P2B)."
        ),
        "ru": (
            "1.1 Nastoyashchie Usloviya dlya Postavshchikov Uslug (Usloviya postavshchika) reguliruyut otnosheniya mezhdu Nevumo i lyubym fizicheskim ili yuridicheskim litsom, kotoroe registriruetsya na platforme Nevumo v kachestve postavshchika uslug (Postavshchik, vy).\n\n"
            "1.2 Nevumo upravljaet onlayn-rynkom na nevumo.com i ego yazykovykh subdomenakh (Platforma), kotoraya pozvolyaet Postavshchikam predstavlyat svoi uslugi i svyazyvaet ikh s klientami, ishchushchimi eti uslugi (Klienty).\n\n"
            "1.3 Nevumo deystvuet isklyuchitelno kak posrednik. Nevumo ne yavlyaetsya storonoy kakogo-libo soglasheniya ob okazanii uslug, zaklyuchennogo mezhdu Postavshchikom i Klientom. Nevumo ne predostavlyaet uslugi, predlagaemye Postavshchikami, ne nanimaet Postavshchikov i ne neset otvetstvennosti za kachestvo, polnotu ili svoevremennoye vypolneniye kakikh-libo uslug.\n\n"
            "1.4 Nastoyashchie Usloviya postavshchika yavlyayutsya obyazyvayushchim soglasheniyem mezhdu vami i Nevumo. Zavershiv registratsiyu v kachestve Postavshchika, vy podtverzhdayete, chto prochitali, ponyali i prinyali nastoyashchie Usloviya postavshchika v polnom ob'yome.\n\n"
            "1.5 Nastoyashchie Usloviya postavshchika primenyayutsya dopolnitelno k obshchim Pravilam i Usloviyam ispolzovaniya Nevumo dlya polzovateley. V sluchaye protivorechiya nastoyashchie Usloviya postavshchika imeyut preimushestvo v otnoshenii vzaimootnosheniy s postavshchikom.\n\n"
            "1.6 Nastoyashchie Usloviya postavshchika razrabotany v sootvetstvii s Reglamentom (ES) 2019/1150 o sozdanii spravedlivykh i prozrachnykh usloviy dlya biznes-polzovateley onlayn-posrednichestvennykh uslug (Reglament P2B)."
        ),
        "uk": (
            "1.1 Tsi Umovy dlya Postachalnikiv Posluh (Umovy postachalnika) regulyuyut vidnosyny mizh Nevumo ta bud-yakoyu fizychnoyu abo yurydychnoyu osoboyu, yaka reyestruyetsya na platformi Nevumo yak postachalnyk posluh (Postachalnyk, vy).\n\n"
            "1.2 Nevumo keruye onlayn-rynkom na nevumo.com ta yoho movnykh subdomenakh (Platforma), shcho dozvolyaye Postachalnikam predstavlyaty svoi posluhy ta zv'yazuye yikh iz kliyentamy, yaki shukayut tsi posluhy (Kliyenty).\n\n"
            "1.3 Nevumo diye vyklyuchno yak poserednyk. Nevumo ne ye storonoyu bud-yakoi uhody pro nadannya posluh, ukladenoi mizh Postachalnikom ta Kliyentom. Nevumo ne nadaye posluhy, shcho proponuyutsya Postachalnikamy, ne naymaye Postachalnikiv i ne nesе vidpovidalnosti za yakist, povnotu abo svoychasnist vykonannya bud-yakykh posluh.\n\n"
            "1.4 Tsi Umovy postachalnika stanovlyat obov'yazuyu uhodu mizh vamy ta Nevumo. Zavershyvshi reyestratsiyu yak Postachalnyk, vy pidtverdzhuyete, shcho prochtaly, zrozumily ta povnistyu pryynyaly tsi Umovy postachalnika.\n\n"
            "1.5 Tsi Umovy postachalnika zastosovuyutsya dodatkovo do zahalnykh Pravyl ta Umov vykorystannya Nevumo dlya korystuvachiv. U razi superechnosti tsi Umovy postachalnika mayut perevahy shchodo vidnosyn z postachalnikom.\n\n"
            "1.6 Tsi Umovy postachalnika rozrobleni vidpovidno do Rehlamentu (YeS) 2019/1150 pro spryyannya spravedlyvosti ta prozorosti dlya biznes-korystuvachiv onlayn-poserednyts'kykh posluh (Rehlament P2B)."
        ),
        "da": (
            "1.1 Disse Vilkaar og betingelser for tjenesteudbydere (Udbydervilkaar) regulerer forholdet mellem Nevumo og enhver fysisk eller juridisk person, der registrerer sig pa Nevumo-platformen som tjenesteudbyder (Udbyder, du).\n\n"
            "1.2 Nevumo driver en online markedsplads pa nevumo.com og dens sprogsubdomaener (Platformen), der giver Udbyderne mulighed for at praesentere deres tjenester og forbinder dem med kunder, der soger disse tjenester (Kunder).\n\n"
            "1.3 Nevumo handler udelukkende som formidler. Nevumo er ikke part i nogen tjenesteaftale indgaaet mellem en Udbyder og en Kunde. Nevumo leverer ikke de tjenester, som Udbyderne tilbyder, ansaetter ikke Udbydere og paatager sig intet ansvar for kvaliteten, fuldstaendigheden eller rettidig gennemfoerelse af nogen tjenester.\n\n"
            "1.4 Disse Udbydervilkaar udgor en bindende aftale mellem dig og Nevumo. Ved at fuldfore registreringen som Udbyder bekraefter du, at du har laest, forstaaet og accepteret disse Udbydervilkaar i deres helhed.\n\n"
            "1.5 Disse Udbydervilkaar galder ud over Nevumos generelle Brugervilkaar. I tilfaelde af konflikt har disse Udbydervilkaar forrang med hensyn til udbyderforholdet.\n\n"
            "1.6 Disse Udbydervilkaar er udarbejdet i overensstemmelse med Forordning (EU) 2019/1150 om fremme af retfaerdighed og gennemsigtighed for erhvervsbrugere af onlineformidlingstjenester (P2B-forordningen)."
        ),
        "sv": (
            "1.1 Dessa Villkor for tjanstelevarantorer (Leverantorsvillkor) reglerar forhallandet mellan Nevumo och varje fysisk eller juridisk person som registrerar sig pa Nevumo-plattformen som tjanstelevarantor (Leverantor, du).\n\n"
            "1.2 Nevumo driver en online-marknad pa nevumo.com och dess sprakliga subdomaner (Plattformen) som gor det mojligt for Leverantorer att presentera sina tjanster och kopplar dem till kunder som soker dessa tjanster (Kunder).\n\n"
            "1.3 Nevumo agerar uteslutande som formedlare. Nevumo ar inte part i nagot tjansavtal som ingats mellan en Leverantor och en Kund. Nevumo tillhandahaller inte de tjanster som Leverantorer erbjuder, anstaller inte Leverantorer och tar inget ansvar for kvaliteten, fullstandigheten eller leveransen i ratt tid av nagra tjanster.\n\n"
            "1.4 Dessa Leverantorsvillkor utgors av ett bindande avtal mellan dig och Nevumo. Genom att slutfora registreringen som Leverantor bekraftar du att du har last, forstatt och accepterat dessa Leverantorsvillkor i sin helhet.\n\n"
            "1.5 Dessa Leverantorsvillkor galler utover Nevumos allmanna Anvandarvillkor. Vid konflikt har dessa Leverantorsvillkor foretrade vad galler leverantorsforhallandet.\n\n"
            "1.6 Dessa Leverantorsvillkor har utarbetats i enlighet med Forordning (EU) 2019/1150 om framjande av rattvisa och oppen insyn for foretagsanvandare av onlineformedlingstjanster (P2B-forordningen)."
        ),
        "no": (
            "1.1 Disse Vilkarene for tjenesteleverandorer (Leverandorvilkar) regulerer forholdet mellom Nevumo og enhver fysisk eller juridisk person som registrerer seg pa Nevumo-plattformen som tjenesteleverandor (Leverandor, du).\n\n"
            "1.2 Nevumo driver en nettbasert markedsplass pa nevumo.com og dens spraklige subdomener (Plattformen) som gir Leverandorer mulighet til a presentere sine tjenester og kobler dem med kunder som soker disse tjenestene (Kunder).\n\n"
            "1.3 Nevumo opptrer utelukkende som formidler. Nevumo er ikke part i noen tjenestekontrakt inngatt mellom en Leverandor og en Kunde. Nevumo leverer ikke tjenestene som tilbys av Leverandorer, ansetter ikke Leverandorer og patar seg intet ansvar for kvaliteten, fullstendigheten eller rettidig gjennomforing av noen tjenester.\n\n"
            "1.4 Disse Leverandorvilkarene utgjor en bindende avtale mellom deg og Nevumo. Ved a fullore registreringen som Leverandor bekrefter du at du har lest, forstatt og akseptert disse Leverandorvilkarene i sin helhet.\n\n"
            "1.5 Disse Leverandorvilkarene gjelder i tillegg til Nevumos generelle Brukervilkar. Ved konflikt har disse Leverandorvilkarene forrang med hensyn til leverandorforholdet.\n\n"
            "1.6 Disse Leverandorvilkarene er utarbeidet i samsvar med Forordning (EU) 2019/1150 om fremme av rettferdighet og apen innsyn for naeringsdrivende brukere av nettbaserte formidlingstjenester (P2B-forordningen)."
        ),
        "fi": (
            "1.1 Nama Palveluntarjoajien kayttoehdot (Palveluntarjoajan ehdot) saatelevat Nevumon ja minkaan tahansa luonnollisen henkilon tai oikeushenkilon valista suhdetta, joka rekisteroityy Nevumo-alustalle palveluntarjoajana (Palveluntarjoaja, sina).\n\n"
            "1.2 Nevumo yllapitaa verkkomarkkinapaikkaa osoitteessa nevumo.com ja sen kielijohannaisilla (Alusta), joka mahdollistaa Palveluntarjoajille palvelujensa esittamisen ja yhdistaa heidan palveluja etsiviin asiakkaisiin (Asiakkaat).\n\n"
            "1.3 Nevumo toimii yksinomaan valittajana. Nevumo ei ole osapuolena Palveluntarjoajan ja Asiakkaan valilla tehdyssa palvelusopimuksessa. Nevumo ei tarjoa Palveluntarjoajien tarjoamia palveluita, ei tyollista Palveluntarjoajia eika vastaa palveluiden laadusta, kattavuudesta tai oikea-aikaisesta suorittamisesta.\n\n"
            "1.4 Nama Palveluntarjoajan ehdot muodostavat sitovan sopimuksen sinun ja Nevumon valilla. Suorittamalla rekisteroinnin Palveluntarjoajana vahvistat, etta olet lukenut, ymmartanyt ja hyvaksynyt nama Palveluntarjoajan ehdot kokonaan.\n\n"
            "1.5 Nama Palveluntarjoajan ehdot ovat voimassa Nevumon yleisten Kayttajien ehtojen lisaksi. Ristiriitatilanteessa nama Palveluntarjoajan ehdot ovat ensisijaisia palveluntarjoajasuhteen osalta.\n\n"
            "1.6 Nama Palveluntarjoajan ehdot on laadittu asetuksen (EU) 2019/1150 mukaisesti, jolla edistetaan oikeudenmukaisuutta ja lapinakyvyytta verkkovastallisuuspalveluiden yrityskattajille (P2B-asetus)."
        ),
        "et": (
            "1.1 Kaseolevad Teenusepakkujate tingimused (Pakkuja tingimused) reguleerivad suhteid Nevumo ja iga fuussilise voi juriidilise isiku vahel, kes registreerub Nevumo platvormil teenusepakkujana (Pakkuja, teie).\n\n"
            "1.2 Nevumo haldab veebimarketit aadressil nevumo.com ja selle keele alamdomeenidel (Platvorm), mis voimaldab Pakkujatel oma teenuseid esitleda ja uhendab nad teenuseid otsivate klientidega (Kliendid).\n\n"
            "1.3 Nevumo tegutseb uksnes vahendajana. Nevumo ei ole Pakkuja ja Kliendi vahel solgitud teenuslepingu osapooleks. Nevumo ei osuta Pakkujate pakutavaid teenuseid, ei toos Pakkujaid ning ei kanna vastutust teenuste kvaliteedi, taiuslikkuse ega oigeaegse sooritamise eest.\n\n"
            "1.4 Kaseolevad Pakkuja tingimused moodustavad teie ja Nevumo vahel siduva lepingu. Registreerimise lopetamisega Pakkujana kinnitate, et olete kasesolevad Pakkuja tingimused labinud, moistnud ja taieulikult heaks kiitnud.\n\n"
            "1.5 Kaseolevad Pakkuja tingimused kehtivad lisaks Nevumo uldistele Kasutajatingimustele. Vastuolu korral on kaseolevatel Pakkuja tingimustel prioriteet pakkujasuhte osas.\n\n"
            "1.6 Kaseolevad Pakkuja tingimused on koostatud vastavalt maarustele (EL) 2019/1150, mis edendab avenemust ja labilistikkust internetipohiste vahendamisteenuste ari-kasutajate jaoks (P2B maarustele)."
        ),
        "lt": (
            "1.1 Siomis Paslaugu teikejo salygomis (Teikejo salygos) reglamentuojami santykiai tarp Nevumo ir bet kurio fizinio ar juridinio asmens, kuris registruojasi Nevumo platformoje kaip paslaugu teikejas (Teikejas, jus).\n\n"
            "1.2 Nevumo valdo internetine prekyvyte nevumo.com ir jos kalbos subdomenai (Platforma), leiddzianti Teikejams pristatyti savo paslaugas ir jungianti juos su klientais, ieskanciais siu paslaugu (Klientai).\n\n"
            "1.3 Nevumo veikia iskirtinai kaip tarpininkas. Nevumo nera jokios Teikejo ir Kliento sudarytos paslaugu sutarties salimi. Nevumo neteikia Teikejo siulomu paslaugu, nessamdo Teikejus ir neatsako uz paslaugu kokybe, isamuma ar savalaiski vykdyma.\n\n"
            "1.4 Sios Teikejo salygos sudaro privaloma sutarti tarp jusu ir Nevumo. Baigdami registracija kaip Teikejas, patvirtinate, kad perskaitate, supratote ir visiskai priemete sias Teikejo salygas.\n\n"
            "1.5 Sios Teikejo salygos taikomos kartu su bendrosiomis Nevumo Naudotoju salygomis. Esant priestaryngumui, sios Teikejo salygos turi pirmenybe teikejo santykiu atvilgiu.\n\n"
            "1.6 Sios Teikejo salygos parengtos laikantis Reglamento (ES) 2019/1150 del interneto tarpininkavimo paslaugu verslo vartotojams teisingumo ir skaidrumo skatinimo (P2B Reglamentas)."
        ),
        "lv": (
            "1.1 Sie Pakalpojumu sniedzeja lietosanas noteikumi (Sniedzeja noteikumi) regulé attiecibas starp Nevumo un jebkuru fizisku vai juridisku personu, kura registréjas Nevumo platforma ka pakalpojumu sniedzejs (Sniedzejs, jus).\n\n"
            "1.2 Nevumo darbojas tiesaistes tirgus vieta nevumo.com un tas valodas subdomenós (Platforma), kas lauj Sniedzejiem prezentét savus pakalpojumus un savienó tos ar klientiem, kuri meklé sós pakalpojumus (Klienti).\n\n"
            "1.3 Nevumo darbojas wylacznie ka starpnieks. Nevumo nav puse neviena pakalpojumu liguma, kas nodibinats starp Sniedzéju un Klientu. Nevumo nesniedz Sniedzéju piedavatos pakalpojumus, nedarbina Sniedzejus un neuznemies nekadu atbildibu par pakalpojumu kvalitati, pilnigumu vai savlaicigu izpildi.\n\n"
            "1.4 Sie Sniedzeja noteikumi veido saistosus nodibinajumus starp jums un Nevumo. Pabeidzot registraciju ka Sniedzejam, jus apstiprinat, ka esat izlasijis, sapratis un pilniga apjoma pienemis sos Sniedzeja noteikumus.\n\n"
            "1.5 Sie Sniedzeja noteikumi tiek pielietoti papildus Nevumo visparejai Lietotaju lietosanas kartibai. Pretrunu gadijuma sie Sniedzeja noteikumi ir prioritari attieciba uz sniedzeja attiecibam.\n\n"
            "1.6 Sie Sniedzeja noteikumi ir izstradati atbilstosi Regulai (ES) 2019/1150 par tiessaistes starpsniedzejpakalpojumu biznesa lietotaju godticigu un parskatamu tirdzniecibas prakshu veicinasanu (P2B Regula)."
        ),
        "hu": (
            "1.1 Jelen Szolgaltatok Altal Elfogadott Felhasznalasi Feltetelek (Szolgaltatoi Feltetelek) a Nevumo es minden olyan termeszetes szemely vagy jogi szemely kozott fennallo viszonyt szabalyozzak, aki/amely a Nevumo platformon szolgaltatokent regisztral (Szolgaltato, On).\n\n"
            "1.2 A Nevumo online piacteret uzemeltet a nevumo.com es annak nyelvi aldomainjein (Platform), amely lehetove teszi a Szolgaltatoknak szolgaltatasaik bemutatast, es osszekoti oket az adott szolgaltatasokat kereso ugyfeleikkel (Ugyfelek).\n\n"
            "1.3 A Nevumo kizarolag kozvetitokent jar el. A Nevumo nem reszes a Szolgaltato es az Ugyfel kozott megkotott semmilyen szolgaltatasi megallapodasnak. A Nevumo nem nyujtja a Szolgaltatak altal kinalt szolgaltatast, nem alkalmaz Szolgaltatokat, es nem vallal felelossegert a szolgaltatasok minosegert, teljessegeert vagy idooszeru vegrehajtasaert.\n\n"
            "1.4 Jelen Szolgaltatoi Feltetelek kotelezo ervenyu megallapodasnak minositulnek On es a Nevumo kozott. A Szolgaltatokent valo regisztracio befejezesevel megerositi, hogy a jelen Szolgaltatoi Felteteleket olvasta, megertette es teljes egeszeben elfogadta.\n\n"
            "1.5 Jelen Szolgaltatoi Feltetelek a Nevumo altalanos Felhasznaloi Feltetelei mellett alkalmazandok. Utkozesuk eseten jelen Szolgaltatoi Felteteleknek a szolgaltatoi viszony tekinteteben elsobb-seguk van.\n\n"
            "1.6 Jelen Szolgaltatoi Feltetelek az online kozvetitoi szolgaltatasok uzleti felhasznaloi szamara az egyenloseg es atlathatosag elosegiteserol szolo (EU) 2019/1150 rendelet (P2B rendelet) betartasaval keszultek."
        ),
        "hr": (
            "1.1 Ovi Uvjeti poslovanja za pruzatelje usluga (Uvjeti pruzatelja) ureduju odnos izmedju Nevumo i svake fizicke ili pravne osobe koja se registrira na platformi Nevumo kao pruzatelj usluga (Pruzatelj, vi).\n\n"
            "1.2 Nevumo upravlja online trzisteom na nevumo.com i njezinim jezicnim poddomenama (Platforma) koja pruzateljima omogucuje prezentiranje njihovih usluga i povezuje ih s klijentima koji traze te usluge (Klijenti).\n\n"
            "1.3 Nevumo djeluje iskljucivo kao posrednik. Nevumo nije stranka ni jednog ugovora o uslugama zakljucenog izmedju Pruzatelja i Klijenta. Nevumo ne pruzа usluge koje nude Pruzatelji, ne zaposljavа Pruzatelje te ne snosi nikakvu odgovornost za kvalitetu, potpunost ili pravovremeno izvrsenje usluga.\n\n"
            "1.4 Ovi Uvjeti pruzatelja cine obvezujuci ugovor izmedju vas i Nevumo. Dovrsavanjem registracije kao Pruzatelja potvrdjujete da ste procitali, razumjeli i u potpunosti prihvatili ove Uvjete pruzatelja.\n\n"
            "1.5 Ovi Uvjeti pruzatelja primjenjuju se uz opce Uvjete koristenja Nevumo za korisnike. U slucaju sukoba, ovi Uvjeti pruzatelja imaju prednost u pogledu odnosa s pruzateljem.\n\n"
            "1.6 Ovi Uvjeti pruzatelja sastavljeni su u skladu s Uredbom (EU) 2019/1150 o promicanju pravednosti i transparentnosti za poslovne korisnike internetskih usluga posredovanja (Uredba P2B)."
        ),
        "sk": (
            "1.1 Tieto Podmienky pre Poskytovatelov Sluzieb (Podmienky poskytovatel'a) upravuju vztah medzi Nevumo a akoukolvel fyzickou alebo pravnickou osobou, ktora sa registruje na platforme Nevumo ako poskytovatel sluzieb (Poskytovatel, vy).\n\n"
            "1.2 Nevumo prevadzkuje online trh na nevumo.com a jeho jazykovych poddoménach (Platforma), ktora umoznuje Poskytovatelom prezentovat ich sluzby a spaja ich so zakaznikmi, ktori hlqdaju tieto sluzby (Zakaznici).\n\n"
            "1.3 Nevumo kona vylucne ako sprostredkovatel. Nevumo nie je stranou ziadnej zmluvy o poskytovani sluzieb uzavretej medzi Poskytovatelom a Zakaznikom. Nevumo neposkytuje sluzby ponukane Poskytovatelmi, nezamestnava Poskytovatelov a nenesie ziadnu zodpovednost za kvalitu, uplnost alebo vcasne plnenie akychkolvek sluzieb.\n\n"
            "1.4 Tieto Podmienky poskytovatel'a tvoria zavaznu dohodu medzi vami a Nevumo. Dokoncenim registracie ako Poskytovatel'a potvrdzujete, ze ste si Podmienky poskytovatel'a precitali, porozumeli im a v plnom rozsahu ich prijali.\n\n"
            "1.5 Tieto Podmienky poskytovatel'a sa uplatnuju popri vseobecnych Podmienkach pouzivani Nevumo pre pouzivatelov. V pripade rozporu maju tieto Podmienky poskytovatel'a prednost v oblasti vztahu s Poskytovatelom.\n\n"
            "1.6 Tieto Podmienky poskytovatel'a boli vypracovane v sulade s Nariadenim (EU) 2019/1150 o podpore spravodlivosti a transparentnosti pre podnikatel'skych pouzivatelov online sprostredkovatel'skych sluzieb (Nariadenie P2B)."
        ),
        "sl": (
            "1.1 Ti Pogoji za ponudnike storitev (Pogoji ponudnika) urejajo razmerje med Nevumo in vsako fizicno ali pravno osebo, ki se registrira na platformi Nevumo kot ponudnik storitev (Ponudnik, vi).\n\n"
            "1.2 Nevumo upravlja spletno trznico na nevumo.com in njenih jezikovnih poddomenih (Platforma), ki Ponudnikom omogoca predstavitev njihovih storitev in jih povezuje s strankami, ki iscejo te storitve (Stranke).\n\n"
            "1.3 Nevumo deluje izkljucno kot posrednik. Nevumo ni stranka nobene pogodbe o storitvah, sklenjene med Ponudnikom in Stranko. Nevumo ne zagotavlja storitev, ki jih ponujajo Ponudniki, ne zaposluje Ponudnikov in ne prevzema nikakrsne odgovornosti za kakovost, popolnost ali pravocasno izvedbo storitev.\n\n"
            "1.4 Ti Pogoji ponudnika predstavljajo obvezujoco pogodbo med vami in Nevumo. Z zakljuckom registracije kot Ponudnik potrjujete, da ste te Pogoje ponudnika prebrali, razumeli in jih v celoti sprejeli.\n\n"
            "1.5 Ti Pogoji ponudnika se uporabljajo poleg splosnih Pogojev uporabe Nevumo za uporabnike. V primeru nasprotja imajo ti Pogoji ponudnika prednost glede razmerja s ponudnikom.\n\n"
            "1.6 Ti Pogoji ponudnika so bili pripravljeni v skladu z Uredbo (EU) 2019/1150 o spodbujanju pravicnosti in transparentnosti za poslovne uporabnike spletnih posredniskih storitev (Uredba P2B)."
        ),
        "el": (
            "1.1 Oi paróntes Óroi kai Proupotheséis gia Paróchous Ypiresión (Óroi Paróchu) diépoun ti schési metaxú tis Nevumo kai opoiasdhípote physikoú i nomikoú prosópu pou eggráfetai stin platfórma Nevumo os párochos ypiresbión (Párochos, eseís).\n\n"
            "1.2 I Nevumo leitourgí agoná online agóra sto nevumo.com kai stis glóssikes ypoperiochés tis (Platfórma) pou epitrépei stous Paróchous na parousiázoune tis ypiresíes tous kai tous syndéi me pelates pou anazitoún autés tis ypiresíes (Pelates).\n\n"
            "1.3 I Nevumo energ eí aklibós os mésos. I Nevumo den eínai méros se opiadípote symfónía ypiresbión pou synáfthike metaxú Paróchou kai Pelati. I Nevumo den paréchei tis ypiresíes pou prospheroun oi Párochos, den apascholí Paróchous kai den filá kamían evthýni gia tin poiótita, tín plirótita í tín émprothesmi ektelesi ton ypiresbión.\n\n"
            "1.4 Oi parontes Óroi Paróchou apoteloún desmeftikí symfónía metaxú sas kai tis Nevumo. Oloklirónondas tin eggrafí sas os Párochos, epibebaióte óti échete diabásei, katanosísete kai apodhechteí plikros tous parontes Órous Paróchou.\n\n"
            "1.5 Oi parontes Óroi Paróchou efarmózontai epipléon ton genikón Óron Chrisís tis Nevumo gia chríste. Se períptosei sýgkrousis, oi parontes Óroi Paróchou echoún protímisi óson afará ti schési tou paróchou.\n\n"
            "1.6 Oi parontes Óroi Paróchou eíchane sýnthesi se symmórfosi me ton Kanonikmó (EE) 2019/1150 gia tin prothisi dikaiósyinis kai diafaneías gia tous epicheirisiakous christes ypiresbión online diamesólabisis (Kanonismós P2B)."
        ),
        "tr": (
            "1.1 Bu Hizmet Saglayicilar icin Kullanim Kosullari (Saglayici Kosullari), Nevumo ile Nevumo platformuna hizmet saglayici olarak kaydolan herhangi bir gercek veya tüzel kisi arasindaki iliskiyi duzenlемektedir (Saglayici, siz).\n\n"
            "1.2 Nevumo, nevumo.com ve dil alt alanlarinda (Platform) bir cevrimici pazar yeri isletmektedir; bu platform Saglayicilarin hizmetlerini sunmalarini saglamakta ve onlari bu hizmetleri arayan musterilerle (Musteriler) bulusturmaktadir.\n\n"
            "1.3 Nevumo yalnizca bir aracilik rolü ustlenmektedir. Nevumo, bir Saglayici ile Musteri arasinda akdedilen hizmet sozlesmesinin tarafi degildir. Nevumo, Saglayicilar tarafindan sunulan hizmetleri sunmamakta, Saglayicilari istihdam etmemekte ve hizmetlerin kalitesi, eksiksizligi veya zamaninda ifasi konusunda hicbir sorumluluk tasimamaktadir.\n\n"
            "1.4 Bu Saglayici Kosullari, siz ile Nevumo arasinda baglayici bir sozlesme niteligi tasimaktadir. Saglayici olarak kaydinizi tamamlayarak, bu Saglayici Kosullarini okudugunuzu, anladiginizi ve tamamen kabul ettiginizi onayliyorsunuz.\n\n"
            "1.5 Bu Saglayici Kosullari, Nevumo'nun Kullanicilar icin genel Kullanim Kosullarina ek olarak uygulanir. Catisma durumunda, bu Saglayici Kosullari saglayici iliskisi bakimindan onceliklidir.\n\n"
            "1.6 Bu Saglayici Kosullari, cevrimici aracilik hizmetlerinin is kullanicilari icin adalet ve seffafligin tesvik edilmesine iliskin (AB) 2019/1150 sayili Yonetmelge (P2B Yonetmeligi) uyumlu olarak hazirlanmistir."
        ),
        "ga": (
            "1.1 Rialaionn na Tearmai agus Coinniолlacha seo do Sholathroire Seirbhise (Tearmai an tSolathraio) an coibhneas idir Nevumo agus aon duine nadurtha no eintit dli a chlaraonn ar ardán Nevumo mar sholathroir seirbhise (Solathroir, tusa).\n\n"
            "1.2 Feidhmionn Nevumo margadh ar line ar nevumo.com agus a fhothainne teanga (an t-Ardan) a chuireann ar chumas Solathroir a gcuid seirbhisi a chur i lathair agus a nascann iad le custoimeri ata ag lorg na seirbhisi sin (Custoimeri).\n\n"
            "1.3 Gniomhaionn Nevumo mar idirghabhalair amhain. Ni pairtí i Nevumo in aon chomhaontu seirbhise a rinneadh idir Solathroir agus Custoimeir. Ni chuireann Nevumo na seirbhisi a chuireann Solathroir ar fail, ni fhostaionn se Solathroir, agus ni ghlacann se le haon fhreagracht as caighdean, iomlaineacht no cur i gcrich trath na seirbhisi.\n\n"
            "1.4 Bunann na Tearmai seo don Solathroir comhaontu ceangailteach idir tusa agus Nevumo. Tri chlaru a chur i gcrich mar Sholathroir, dearbhaionn tu go bhfuil na Tearmai seo don Solathroir leite, tuigthe agus glactha agat go hiomlán.\n\n"
            "1.5 Baineann na Tearmai seo don Solathroir in addition le Tearmai Ginearalta Usaideora Nevumo. I gcas coinbhleachta, ta tosaíocht ag Tearmai an tSolathraio maidir le coibhneas an tsolathraio.\n\n"
            "1.6 Dearadh na Tearmai seo don Solathroir i gcomhreir le Rialachan (AE) 2019/1150 maidir le cothromaíocht agus trédhearcacht a chur chun cinn d'usaideoiri gno seirbhisi idirghabhala ar line (Rialachan P2B)."
        ),
        "is": (
            "1.1 Thessi Skilmalar og skilyrdi fyrir thjonustuadila (Skilmalar veituadila) gilda um samband Nevumo og hvers einstaklingsins edur lagalegrar einingar sem skrair sig a Nevumo-vettvangi sem thjonustuadili (Veituadili, thu).\n\n"
            "1.2 Nevumo rekur netmarkad a nevumo.com og tungumalaundirlenum hans (Vettvangur) sem gerir Veituadilum kleift ad kynna thjonustu sina og tengir tha vid vidskiptavini sem leita adessa thjonustu (Vidskiptavinir).\n\n"
            "1.3 Nevumo starfar eingongu sem milligangur. Nevumo er ekki adili ad neinum thjonustusamningi sem gerður er milli Veituadila og Vidskiptavinar. Nevumo veitir ekki thjonustu sem Veituadilar bjoda upp a, raedur ekki Veituadila og ber enga abyrgd a gaeda, heildarnaesi edur timabundid framkvaemd nokkurrar thjonustu.\n\n"
            "1.4 Thessir Skilmalar veituadila mynda bindandi samkomulag milli thin og Nevumo. Med thvi ad ljuka skraning sem Veituadili stasytu thu ad thu hafir lesid, skilid og samthykkt thessar Skilmalar veituadila i heild sinni.\n\n"
            "1.5 Thessir Skilmalar veituadila gilda auk almennu Notendakilmalanna hjа Nevumo. I tilvik samreksturs hafa Skilmalar veituadila forgang hvad vardar samband veituadilans.\n\n"
            "1.6 Thessir Skilmalar veituadila voru gerdir i samraeimi vid Reglugerд (ESB) 2019/1150 um framgang sanngirnis og gagnsaeis fyrir fyrirtaekjanotendur netmiðlunarþjónustu (P2B-reglugerдin)."
        ),
        "lb": (
            "1.1 Dese Bedingungen fir Servicepresser (Presser-Bedingungen) regelen d'Beziehung tëschent Nevumo an jeder natierlecher oder juridescher Persoun, déi sech op der Nevumo-Plattform als Servicepresser aschreift (Presser, Dir).\n\n"
            "1.2 Nevumo betreit en Online-Marché op nevumo.com a senge Sprooch-Ënnerdomeinen (Plattform), dee Presseren erméiglecht, hir Servicer virzestellen a si mat Clienten verbannet, déi no dëse Servicer sichen (Clienten).\n\n"
            "1.3 Nevumo handelt ausschliesslich als Vermëttler. Nevumo ass keng Partei un engem Servicevertrag, deen tëschent engem Presser an engem Client ofgeschloss gëtt. Nevumo bitt d'Servicer vun de Presseren net un, beschäftegt keng Presser a haftet net fir Qualitéit, Vollstänigkeit oder rechtzäiteg Ausféierung vun irgendwelchen Servicer.\n\n"
            "1.4 Dese Presser-Bedingungen bilden en bindend Ofkommes tëschent Iech an Nevumo. Mat der Vollendung vun der Registréierung als Presser confirméiert Dir, dass Dir dese Presser-Bedingungen gelies, verstanen an vollstänig akzeptéiert hutt.\n\n"
            "1.5 Dese Presser-Bedingungen gëllen zousätzlech zu den allgemeinen Benotzerbedingungen vun Nevumo. Bei engem Konflikt hunn dese Presser-Bedingungen Virrang an Bezug op d'Presser-Beziehung.\n\n"
            "1.6 Dese Presser-Bedingungen goufen entspriechend der Verordnung (EU) 2019/1150 zur Foerderung vun Fairness a Transparenz fir Geschäftsbenotzer vun Online-Vermëttlungsservicer ausgeschafft (P2B-Verordnung)."
        ),
        "mk": (
            "1.1 Ovie Uslovi za davaci na uslugi (Uslovi na davacot) go ureduvaat odnosot megu Nevumo i sekoj fizicko lice ili pravno lice koe se registrira na platformata Nevumo kako davac na uslugi (Davac, vie).\n\n"
            "1.2 Nevumo upravuva so online pazarot na nevumo.com i negovite jazyčni poddomenи (Platforma), koj im ovozmoguva na Davacite da gi prezentiraat svoite uslugi i gi povrzuva so klientite koi gi baraat tie uslugi (Klienti).\n\n"
            "1.3 Nevumo postapuva iskljucivo kako posrednik. Nevumo ne e strana vo nikoj dogovor za uslugi sklucen megу Davac i Klient. Nevumo ne gi obezbeduva uslu-gite ponudeni od Davacite, ne vrabotуva Davaci i ne nosi odgovornost za kva-litetot, celosnosta ili blagovremenoto ispolnuvanje na kakvi i da e uslugi.\n\n"
            "1.4 Ovie Uslovi na davacot pretstavuvaat obvrzuvacki dogovor megu vas i Nevumo. So zavrsuvanjeto na registracijata kako Davac, potvrduvate deka ste gi procitale, razbrале i vo celost prifatile ovie Uslovi na davacot.\n\n"
            "1.5 Ovie Uslovi na davacot se primenuvaat pokraj opshtite Korisni chki uslovi na Nevumo. Vo slucaj na konflikt, ovie Uslovi na davacot imaat prednost vo odnos na odnosot so davacot.\n\n"
            "1.6 Ovie Uslovi na davacot se sostaveni vo soglasnost so Uredbata (EU) 2019/1150 za promoviranje na pravednost i transpar entnost za delovnite korisnici na onlajn posrednichki uslugi (Uredba P2B)."
        ),
        "mt": (
            "1.1 Dawn it-Termini u Kundizzjonijiet ghall-Fornituri tas-Servizz (Termini tal-Fornitur) jirregolaw ir-relazzjoni bejn Nevumo u kwalunkwe persuna naturali jew entita legali li tirregistra fuq il-pjattaforma Nevumo bhala fornitur ta' servizzi (Fornitur, inti).\n\n"
            "1.2 Nevumo topera suq online fuq nevumo.com u s-subdomeni tal-lingwa tieghu (Pjattaforma) li jippermetti lill-Fornituri jppreżentaw is-servizzi taghhom u jghaqqadhom ma' klijenti li jfittxu dawk is-servizzi (Klijenti).\n\n"
            "1.3 Nevumo taghmel l-unika rwol bhala intermedjarju. Nevumo mhix parti fi kwalunkwe ftehim ta' servizzi konkluż bejn Fornitur u Klijent. Nevumo ma tprovdix is-servizzi offruti mill-Fornituri, ma thaddemx Fornituri u ma tassumix responsabbilta ghall-kwalita, l-iggkomplejtezza jew l-ezekuzzjoni fil-hin ta' kwalunkwe servizzi.\n\n"
            "1.4 Dawn it-Termini tal-Fornitur jikkostitwixxu ftehim vinkolanti bejnek u bejn Nevumo. Billi tlesti r-registrazzjoni bhala Fornitur, tikkonfermа li qrajt, fhimt u accettajt dawn it-Termini tal-Fornitur fl-intier taghhom.\n\n"
            "1.5 Dawn it-Termini tal-Fornitur japplikaw flimkien mat-Termini Generali tal-Utent ta' Nevumo. F'kaz ta' kunflitt, dawn it-Termini tal-Fornitur ghandhom precedenza fir-rigward tar-relazzjoni tal-fornitur.\n\n"
            "1.6 Dawn it-Termini tal-Fornitur gew imfassla f'konformita mar-Regolament (UE) 2019/1150 dwar il-promozzjoni tal-ugwaljanza u t-trasparenza ghall-utenti kummerczjali tas-servizzi ta' intermedjarjament online (Regolament P2B)."
        ),
        "sq": (
            "1.1 Keto Terma dhe Kushte per Ofruesit e Sherbimeve (Kushtet e Ofruesit) rregullojne marredhënien midis Nevumo dhe cdo personi fizik ose juridik qe regjistrohet ne platformën Nevumo si ofrues sherbimesh (Ofrues, ju).\n\n"
            "1.2 Nevumo operon nje treg online ne nevumo.com dhe nëndomenet e tij gjuhesore (Platforma) qe u mundeson Ofruesve te prezantojne sherbimet e tyre dhe i lidh ata me klientet qe kerkojne ato sherbime (Klientet).\n\n"
            "1.3 Nevumo vepron vetem si ndermjetesues. Nevumo nuk eshte pale ne asnje marreveshje sherbimesh te lidhur midis nje Ofruesi dhe nje Klienti. Nevumo nuk ofron sherbimet e ofruara nga Ofruesit, nuk puneson Ofrues dhe nuk mban asnje pergjegjesi per cilesine, plotesine ose ekzekutimin ne kohe te cfaredo sherbimesh.\n\n"
            "1.4 Keto Kushte te Ofruesit perbejne nje marreveshje detyrues midis jush dhe Nevumo. Duke perfunduar regjistrimin si Ofrues, konfirmoni qe i keni lexuar, kuptuar dhe pranuar plotesisht keto Kushte te Ofruesit.\n\n"
            "1.5 Keto Kushte te Ofruesit zbatohen perveç Kushteve te Pergjithshme te Perdoruesit te Nevumo. Ne rast konflikti, keto Kushte te Ofruesit kane prioritet ne lidhje me marredhënien e ofruesit.\n\n"
            "1.6 Keto Kushte te Ofruesit jane hartuar ne perputhje me Rregulloren (BE) 2019/1150 per promovimin e drejtesise dhe transparences per perdoruesit e biznesit te sherbimeve te ndermjetesimit online (Rregullorja P2B)."
        ),
        "sr": (
            "1.1 Ovi Uslovi za pruzaoce usluga (Uslovi pruzaoca) regulisu odnos izmedju Nevumo i svakog fizickog ili pravnog lica koje se registruje na platformi Nevumo kao pruzalac usluga (Pruzalac, vi).\n\n"
            "1.2 Nevumo upravlja online trzisteom na nevumo.com i njenim jezickim poddomenima (Platforma) koja pruzaocima omogucava prezentovanje njihovih usluga i povezuje ih sa klijentima koji traze te usluge (Klijenti).\n\n"
            "1.3 Nevumo deluje iskljucivo kao posrednik. Nevumo nije strana ni u jednom ugovoru o uslugama zakljucenom izmedju Pruzaoca i Klijenta. Nevumo ne pruzа usluge koje nude Pruzaoci, ne zaposljavа Pruzaoce i ne snosi nikakvu odgovornost za kvalitet, potpunost ili blagovremeno izvrsenje usluga.\n\n"
            "1.4 Ovi Uslovi pruzaoca cine obavezujuci ugovor izmedju vas i Nevumo. Zavrsavanjem registracije kao Pruzaoca potvrdujete da ste procitali, razumeli i u potpunosti prihvatili ove Uslove pruzaoca.\n\n"
            "1.5 Ovi Uslovi pruzaoca primenjuju se uz opste Uslove koristenja Nevumo za korisnike. U slucaju sukoba, ovi Uslovi pruzaoca imaju prednost u pogledu odnosa sa pruzaocem.\n\n"
            "1.6 Ovi Uslovi pruzaoca sastavljeni su u skladu sa Uredbom (EU) 2019/1150 o promovisanju pravicnosti i transparentnosti za poslovne korisnike usluga posredovanja na internetu (Uredba P2B)."
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
            f"✅ seed_provider_terms_p8_art1_body: {count} rows upserted "
            f"({NAMESPACE}: art1_body x 34 langs)"
        )

    engine.dispose()


if __name__ == "__main__":
    seed()
