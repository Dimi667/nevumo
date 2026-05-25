"""
seed_provider_terms_p11_art4_body.py  —  Nevumo | namespace: provider_terms
Key: art4_body  (1 key x 34 langs = 34 rows)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_provider_terms_p11_art4_body
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
    "art4_body": {
        "en": (
            "4.1 Upon completing registration, you may create a Profile and add Service Listings. Each listing must accurately describe the service offered, its scope, pricing, and availability.\n\n"
            "4.2 You warrant that all information published on your Profile and in your Service Listings is truthful, accurate, and not misleading.\n\n"
            "4.3 You may not publish content that:\n"
            "- is unlawful, offensive, discriminatory, or violates third-party rights;\n"
            "- constitutes spam, misleading advertising, or contains false reviews;\n"
            "- impersonates another person or entity;\n"
            "- infringes intellectual property rights.\n\n"
            "4.4 Nevumo reserves the right to remove or edit any content that violates these Provider Terms or applicable law, without prior notice.\n\n"
            "4.5 Claimed Profiles: If Nevumo has created a preliminary profile using publicly available information, you may claim this profile by completing the verification process. Upon claiming, you will receive a notification under Article 14 GDPR describing the personal data held about you and the legal basis for its processing."
        ),
        "pl": (
            "4.1 Po zakończeniu rejestracji Dostawca może założyć Profil i dodawać Oferty Usług. Każda Oferta musi dokładnie opisywać oferowaną usługę, jej zakres, cenę i dostępność.\n\n"
            "4.2 Dostawca zapewnia, że wszystkie informacje opublikowane na jego Profilu i w Ofertach Usług są zgodne z prawdą, dokładne i nie wprowadzają w błąd.\n\n"
            "4.3 Dostawca nie może publikować treści, które:\n"
            "- są niezgodne z prawem, obraźliwe, dyskryminujące lub naruszają prawa osób trzecich;\n"
            "- stanowią spam, wprowadzającą w błąd reklamę lub zawierają fałszywe opinie;\n"
            "- podszywają się pod inną osobę lub podmiot;\n"
            "- naruszają prawa własności intelektualnej.\n\n"
            "4.4 Nevumo zastrzega sobie prawo do usunięcia lub edycji treści naruszających niniejszy Regulamin Dostawców lub obowiązujące przepisy prawa, bez uprzedniego powiadomienia.\n\n"
            "4.5 Profile Przejęte: Jeżeli Nevumo utworzyło wstępny profil na podstawie publicznie dostępnych informacji, Dostawca może go przejąć w drodze procesu weryfikacji. Po przejęciu Dostawca otrzyma powiadomienie zgodnie z art. 14 RODO opisujące przechowywane dane osobowe i podstawę prawną ich przetwarzania."
        ),
        "bg": (
            "4.1 След завършване на регистрацията можете да създадете Профил и да добавите Обяви за услуги. Всяка обява трябва точно да описва предлаганата услуга, нейния обхват, цена и наличност.\n\n"
            "4.2 Вие гарантирате, че цялата информация, публикувана в Профила ви и в Обявите ви за услуги, е вярна, точна и невводяща в заблуждение.\n\n"
            "4.3 Забранено е публикуването на съдържание, което:\n"
            "- е незаконно, обидно, дискриминационно или нарушава права на трети лица;\n"
            "- представлява спам, подвеждаща реклама или съдържа неверни отзиви;\n"
            "- се представя за друго лице или субект;\n"
            "- нарушава права на интелектуална собственост.\n\n"
            "4.4 Nevumo си запазва правото да премахне или редактира съдържание, което нарушава настоящите Условия за Доставчици или приложимото законодателство, без предварително уведомление.\n\n"
            "4.5 Поискани профили: Ако Nevumo е създало предварителен профил въз основа на публично достъпна информация, можете да го поискате, като преминете процеса на верификация. При поемането ще получите уведомление по чл. 14 ОРЗД, описващо личните данни, съхранявани за вас, и правното основание за тяхното обработване."
        ),
        "de": (
            "4.1 Nach Abschluss der Registrierung können Sie ein Profil erstellen und Serviceangebote hinzufügen. Jedes Angebot muss die angebotene Dienstleistung, ihren Umfang, die Preisgestaltung und die Verfügbarkeit genau beschreiben.\n\n"
            "4.2 Sie gewährleisten, dass alle auf Ihrem Profil und in Ihren Serviceangeboten veröffentlichten Informationen wahrheitsgemäß, korrekt und nicht irreführend sind.\n\n"
            "4.3 Sie dürfen keine Inhalte veröffentlichen, die:\n"
            "- rechtswidrig, beleidigend, diskriminierend sind oder Rechte Dritter verletzen;\n"
            "- Spam, irreführende Werbung darstellen oder gefälschte Bewertungen enthalten;\n"
            "- eine andere Person oder Entität vortäuschen;\n"
            "- geistige Eigentumsrechte verletzen.\n\n"
            "4.4 Nevumo behält sich das Recht vor, Inhalte, die gegen diese Dienstleisterbedingungen oder geltendes Recht verstoßen, ohne vorherige Ankündigung zu entfernen oder zu bearbeiten.\n\n"
            "4.5 Beanspruchte Profile: Wenn Nevumo ein vorläufiges Profil auf der Grundlage öffentlich zugänglicher Informationen erstellt hat, können Sie dieses Profil durch Abschluss des Verifizierungsprozesses beanspruchen. Nach der Beanspruchung erhalten Sie eine Benachrichtigung gemäß Art. 14 DSGVO, die die über Sie gespeicherten personenbezogenen Daten und die Rechtsgrundlage für deren Verarbeitung beschreibt."
        ),
        "fr": (
            "4.1 Apres avoir finalise votre inscription, vous pouvez creer un Profil et ajouter des Annonces de services. Chaque annonce doit decrire avec precision le service offert, sa portee, ses tarifs et sa disponibilite.\n\n"
            "4.2 Vous garantissez que toutes les informations publiees sur votre Profil et dans vos Annonces de services sont veridiques, exactes et non trompeuses.\n\n"
            "4.3 Vous ne pouvez pas publier de contenu qui :\n"
            "- est illicite, offensant, discriminatoire ou porte atteinte aux droits de tiers ;\n"
            "- constitue du spam, de la publicite trompeuse ou contient de faux avis ;\n"
            "- usurpe l'identite d'une autre personne ou entite ;\n"
            "- viole des droits de propriete intellectuelle.\n\n"
            "4.4 Nevumo se reserve le droit de supprimer ou de modifier tout contenu enfreignant ces Conditions prestataires ou la loi applicable, sans preavis.\n\n"
            "4.5 Profils revendiques : Si Nevumo a cree un profil preliminaire a partir d'informations publiquement disponibles, vous pouvez revendiquer ce profil en completant le processus de verification. Apres la revendication, vous recevrez une notification conformement a l'article 14 du RGPD decrivant les donnees personnelles vous concernant et la base juridique de leur traitement."
        ),
        "es": (
            "4.1 Una vez completado el registro, puede crear un Perfil y anadir Listados de servicios. Cada listado debe describir con precision el servicio ofrecido, su alcance, precios y disponibilidad.\n\n"
            "4.2 Usted garantiza que toda la informacion publicada en su Perfil y en sus Listados de servicios es veridica, precisa y no enganosa.\n\n"
            "4.3 No puede publicar contenido que:\n"
            "- sea ilegal, ofensivo, discriminatorio o vulnere derechos de terceros;\n"
            "- constituya spam, publicidad enganosa o contenga resenas falsas;\n"
            "- suplante la identidad de otra persona o entidad;\n"
            "- infrinja derechos de propiedad intelectual.\n\n"
            "4.4 Nevumo se reserva el derecho de eliminar o editar cualquier contenido que infrinja estos Terminos del proveedor o la legislacion aplicable, sin previo aviso.\n\n"
            "4.5 Perfiles reclamados: Si Nevumo ha creado un perfil preliminar utilizando informacion disponible publicamente, puede reclamar este perfil completando el proceso de verificacion. Al reclamarlo, recibira una notificacion conforme al articulo 14 del RGPD que describe los datos personales que se tienen sobre usted y la base juridica para su tratamiento."
        ),
        "it": (
            "4.1 Dopo aver completato la registrazione, puoi creare un Profilo e aggiungere Annunci di servizi. Ogni annuncio deve descrivere accuratamente il servizio offerto, il suo ambito, i prezzi e la disponibilita.\n\n"
            "4.2 Garantisci che tutte le informazioni pubblicate nel tuo Profilo e nei tuoi Annunci di servizi siano veritiere, accurate e non fuorvianti.\n\n"
            "4.3 Non puoi pubblicare contenuti che:\n"
            "- siano illeciti, offensivi, discriminatori o violino i diritti di terzi;\n"
            "- costituiscano spam, pubblicita ingannevole o contengano recensioni false;\n"
            "- si spaccino per un'altra persona o entita;\n"
            "- violino diritti di proprieta intellettuale.\n\n"
            "4.4 Nevumo si riserva il diritto di rimuovere o modificare qualsiasi contenuto che violi questi Termini del fornitore o la legge applicabile, senza preavviso.\n\n"
            "4.5 Profili rivendicati: Se Nevumo ha creato un profilo preliminare utilizzando informazioni pubblicamente disponibili, puoi rivendicare questo profilo completando il processo di verifica. Dopo la rivendicazione, riceverai una notifica ai sensi dell'art. 14 GDPR che descrive i dati personali detenuti su di te e la base giuridica per il loro trattamento."
        ),
        "nl": (
            "4.1 Na het voltooien van de registratie kunt u een Profiel aanmaken en Serviceaanbiedingen toevoegen. Elke aanbieding moet de aangeboden dienst, de reikwijdte, de prijsstelling en de beschikbaarheid nauwkeurig beschrijven.\n\n"
            "4.2 U garandeert dat alle informatie die op uw Profiel en in uw Serviceaanbiedingen wordt gepubliceerd, waarheidsgetrouw, nauwkeurig en niet misleidend is.\n\n"
            "4.3 U mag geen inhoud publiceren die:\n"
            "- onwettig, aanstootgevend, discriminerend is of rechten van derden schendt;\n"
            "- spam, misleidende reclame vormt of valse beoordelingen bevat;\n"
            "- een andere persoon of entiteit imiteert;\n"
            "- intellectuele eigendomsrechten schendt.\n\n"
            "4.4 Nevumo behoudt zich het recht voor om inhoud die in strijd is met deze Dienstverlenersvoorwaarden of toepasselijk recht te verwijderen of te bewerken, zonder voorafgaande kennisgeving.\n\n"
            "4.5 Geclaimde profielen: Als Nevumo een voorlopig profiel heeft aangemaakt op basis van openbaar beschikbare informatie, kunt u dit profiel claimen door het verificatieproces te voltooien. Na het claimen ontvangt u een kennisgeving op grond van artikel 14 AVG met een beschrijving van de over u bewaarde persoonsgegevens en de rechtsgrondslag voor de verwerking ervan."
        ),
        "pt": (
            "4.1 Apos concluir o registo, pode criar um Perfil e adicionar Listagens de servicos. Cada listagem deve descrever com precisao o servico oferecido, o seu alcance, preco e disponibilidade.\n\n"
            "4.2 Garante que toda a informacao publicada no seu Perfil e nas suas Listagens de servicos e verdadeira, precisa e nao enganosa.\n\n"
            "4.3 Nao pode publicar conteudo que:\n"
            "- seja ilegal, ofensivo, discriminatorio ou viole direitos de terceiros;\n"
            "- constitua spam, publicidade enganosa ou contenha avaliacoes falsas;\n"
            "- se faca passar por outra pessoa ou entidade;\n"
            "- infrinja direitos de propriedade intelectual.\n\n"
            "4.4 A Nevumo reserva-se o direito de remover ou editar qualquer conteudo que viole estes Termos do prestador ou a legislacao aplicavel, sem aviso previo.\n\n"
            "4.5 Perfis reclamados: Se a Nevumo criou um perfil preliminar utilizando informacoes publicamente disponiveis, pode reclamar este perfil concluindo o processo de verificacao. Apos a reclamacao, recebera uma notificacao ao abrigo do artigo 14 do RGPD descrevendo os dados pessoais detidos sobre si e a base juridica para o seu tratamento."
        ),
        "pt-PT": (
            "4.1 Apos concluir o registo, pode criar um Perfil e adicionar Listagens de servicos. Cada listagem deve descrever com exactidao o servico oferecido, o seu alcance, preco e disponibilidade.\n\n"
            "4.2 Garante que toda a informacao publicada no seu Perfil e nas suas Listagens de servicos e verdadeira, precisa e nao enganosa.\n\n"
            "4.3 Nao pode publicar conteudo que:\n"
            "- seja ilegal, ofensivo, discriminatorio ou viole direitos de terceiros;\n"
            "- constitua spam, publicidade enganosa ou contenha avaliacoes falsas;\n"
            "- se faca passar por outra pessoa ou entidade;\n"
            "- infrinja direitos de propriedade intelectual.\n\n"
            "4.4 A Nevumo reserva-se o direito de remover ou editar qualquer conteudo que viole estes Termos do prestador ou a legislacao aplicavel, sem aviso previo.\n\n"
            "4.5 Perfis reclamados: Se a Nevumo criou um perfil preliminar com base em informacoes publicamente disponiveis, pode reclamar este perfil concluindo o processo de verificacao. Apos a reclamacao, recebera uma notificacao nos termos do artigo 14 do RGPD descrevendo os dados pessoais que lhe dizem respeito e a base juridica para o seu tratamento."
        ),
        "ro": (
            "4.1 Dupa finalizarea inregistrarii, puteti crea un Profil si adauga Listari de servicii. Fiecare listare trebuie sa descrie cu precizie serviciul oferit, sfera sa, pretul si disponibilitatea.\n\n"
            "4.2 Garantati ca toate informatiile publicate pe Profilul dvs. si in Listarile de servicii sunt adevarate, precise si nu induc in eroare.\n\n"
            "4.3 Nu puteti publica continut care:\n"
            "- este ilegal, ofensator, discriminatoriu sau incalca drepturi ale tertilor;\n"
            "- constituie spam, publicitate inselatoare sau contine recenzii false;\n"
            "- se da drept alta persoana sau entitate;\n"
            "- incalca drepturi de proprietate intelectuala.\n\n"
            "4.4 Nevumo isi rezerva dreptul de a elimina sau edita orice continut care incalca prezentii Termeni ai furnizorului sau legislatia aplicabila, fara notificare prealabila.\n\n"
            "4.5 Profiluri revendicate: Daca Nevumo a creat un profil preliminar utilizand informatii disponibile public, puteti revendica acest profil completand procesul de verificare. Dupa revendicare, veti primi o notificare in temeiul articolului 14 din GDPR care descrie datele cu caracter personal detinute despre dvs. si baza juridica pentru prelucrarea acestora."
        ),
        "ru": (
            "4.1 Posle zaversheniya registratsii vy mozhete sozdat Profil i dobavit Ob'yavleniya ob uslugakh. Kazhdoye ob'yavleniye dolzhno tochno opisyvat predlagayemuyu uslugu, yeyo ob'yem, tsenu i dostupnost.\n\n"
            "4.2 Vy garantiruyete, chto vsya informatsiya, opublikovannaya v vashem Profile i v vashikh Ob'yavleniyakh ob uslugakh, yavlyaetsya pravdivoy, tochnoy i ne vvodit v zabluzhdeniye.\n\n"
            "4.3 Vy ne mozhete publikovat kontent, kotoryy:\n"
            "- yavlyaetsya nezakonnym, oskorbitelnым, diskriminatsionnym ili narushayet prava tretikh lits;\n"
            "- yavlyaetsya spamom, vvodashchey v zabluzhdeniye reklamoy ili soderzhit lozhnye otzyvy;\n"
            "- vydayet sebya za drugoye litso ili subyekt;\n"
            "- narushayet prava intellektualnoy sobstvennosti.\n\n"
            "4.4 Nevumo ostavlyayet za soboy pravo udalyat ili redaktirovat lyuboy kontent, kotoryy narushayet nastoyashchiye Usloviya postavshchika ili primenimoye zakonodatelstvo, bez predvaritelnogo uvedomleniya.\n\n"
            "4.5 Zatrebovabnye Profili: Yesli Nevumo sozdalo predvaritelnyy profil na osnove obshchedostupnoy informatsii, vy mozhete zatrebovat etot profil, zavershiv protsess verifikatsii. Posle trebovaniya vy poluchite uvedomleniye v sootvetstvii so st. 14 GDPR, opisyvayushcheye personal'nyye dannyye, khranyashchiyesya o vas, i pravovoyu osnovu dlya ikh obrabotki."
        ),
        "uk": (
            "4.1 Pislia zavershennia reyestratsiyi vy mozhete stvorыty Profil i dodaty Oholoshennia pro posluhy. Kozne oholoshennia maye tochno opysuvaty posluhu, shcho proponuyetsya, ii obsiah, tsinu ta dostupnist.\n\n"
            "4.2 Vy harantuyete, shcho vsia informatsiia, opublikovana u vасhomu Profili ta Oholoshenniakh pro posluhy, ye pravdyvoiu, tochnoiu ta ne vvodyт v omanu.\n\n"
            "4.3 Zaboroneno publikuvaty kontent, yakyy:\n"
            "- ye nezakonnym, obrazlyvym, dyskryminatsiynym abo porushuye prava tretikh osib;\n"
            "- ye spamom, omanlyvоyu reklamoyu abo mistyt khybni vidhuky;\n"
            "- vydaye sebe za inshu osobu abo sub'yekt;\n"
            "- porushuye prava intelektualnoi vlasnosti.\n\n"
            "4.4 Nevumo zalyshaye za soboiu pravo vydalyaty abo redahuvaty bud-yakyy kontent, yakyy porushuye tsi Umovy postachalnika abo chynne zakonodavstvo, bez poperednоho povіdomlennia.\n\n"
            "4.5 Zayavleni profili: Yakshcho Nevumo stvorylo poperedniy profil na osnovi publichno dostupnoi informatsii, vy mozhete zayavyty prava na tsyy profil, proyshovshchy protses veryfikatsiyi. Pislia zayavky vy otrymayete povіdomlennia vidpovidno do st. 14 GDPR, shcho opysaye personalni dani, shcho zbеrihayutsya pro vas, ta pravovu osnovu dlya ikh obroblennia."
        ),
        "cs": (
            "4.1 Po dokonceni registrace muzete vytvorit Profil a pridat Nabidky sluzeb. Kazda nabidka musi presne popisovat nabizenou sluzbu, jeji rozsah, cenu a dostupnost.\n\n"
            "4.2 Zaručujete, ze vsechny informace zverejnene na vasem Profilu a v Nabidkach sluzeb jsou pravdive, presne a neni zavádzejici.\n\n"
            "4.3 Nesmiete zverejnovat obsah, ktery:\n"
            "- je nezakonny, urazlivy, diskriminacni nebo porusuje prava tretich stran;\n"
            "- predstavuje spam, klamavou reklamu nebo obsahuje falzivni recenze;\n"
            "- vydava se za jinou osobu nebo subjekt;\n"
            "- porusuje prava dusmevniho vlastnictvi.\n\n"
            "4.4 Nevumo si vyhrazuje pravo odstranit nebo upravit jakykoli obsah, ktery porusuje tato Podminky poskytovatele nebo platne pravni predpisy, bez predchoziho upozorneni.\n\n"
            "4.5 Narokovane profily: Pokud Nevumo vytvorilo predbezny profil na zaklade verejne dostupnych informaci, muzete si tento profil narokovat dokoncenim overovacino procesu. Po nerokovani obdrzite oznameni podle cl. 14 GDPR popisujici osobni udaje o vas uchovavane a pravni zaklad pro jejich zpracovani."
        ),
        "da": (
            "4.1 Naar du har faerdiggjort registreringen, kan du oprette en Profil og tilfoeje Serviceopslag. Hvert opslag skal praecist beskrive den tilbudte tjeneste, dens omfang, prissaetning og tilgaengelighed.\n\n"
            "4.2 Du garanterer, at alle oplysninger, der er offentliggjort pa din Profil og i dine Serviceopslag, er sandfaerdige, noejagtige og ikke vildledende.\n\n"
            "4.3 Du maa ikke offentliggoere indhold, der:\n"
            "- er ulovligt, staendende, diskriminerende eller kraenker tredjeparts rettigheder;\n"
            "- udgoer spam, vildledende reklame eller indeholder falske anmeldelser;\n"
            "- udgiver sig for at vaere en anden person eller enhed;\n"
            "- kraenker intellektuelle ejendomsrettigheder.\n\n"
            "4.4 Nevumo forbeholder sig retten til at fjerne eller redigere indhold, der kraenker disse Udbydervilkaar eller gaeldende lov, uden forudgaaende varsel.\n\n"
            "4.5 Kraevede profiler: Hvis Nevumo har oprettet en foreloebig profil ved hjaelp af offentligt tilgaengelige oplysninger, kan du kraeve denne profil ved at fuldfoere verificeringsprocessen. Efter kraevet vil du modtage en underretning i henhold til artikel 14 GDPR, der beskriver de personoplysninger, der opbevares om dig, og retsgrundlaget for behandlingen."
        ),
        "sv": (
            "4.1 Efter att ha slutfort registreringen kan du skapa en Profil och lagga till Tjänstelistor. Varje lista maste noggrant beskriva den erbjudna tjansten, dess omfattning, prissattning och tillganglighet.\n\n"
            "4.2 Du garanterar att all information som publiceras pa din Profil och i dina Tjänstelistor ar sanningsenlig, korrekt och inte vilseledande.\n\n"
            "4.3 Du far inte publicera innehall som:\n"
            "- ar olagligt, stotande, diskriminerande eller krankter tredje parts rattigheter;\n"
            "- utgör spam, vilseledande reklam eller innehaller falska recensioner;\n"
            "- utger sig for att vara en annan person eller entitet;\n"
            "- krankter immateriella rattigheter.\n\n"
            "4.4 Nevumo forbehaller sig ratten att ta bort eller redigera innehall som bryter mot dessa Leverantorsvillkor eller tillamplig lag, utan foregaende meddelande.\n\n"
            "4.5 Payropa profiler: Om Nevumo har skapat en preliminar profil med offentligt tillganglig information kan du gora ansprak pa denna profil genom att slutfora verifieringsprocessen. Efter payropa far du ett meddelande enligt artikel 14 i GDPR som beskriver de personuppgifter som finns om dig och den rattsliga grunden for behandlingen."
        ),
        "no": (
            "4.1 Etter а ha fullort registreringen kan du opprette en Profil og legge til Tjenestelister. Hvert oppforing mа noeyaktig beskrive den tilbudte tjenesten, dens omfang, prising og tilgjengelighet.\n\n"
            "4.2 Du garanterer at all informasjon som publiseres pa din Profil og i dine Tjenestelister er sannferdig, noeyaktig og ikke villedende.\n\n"
            "4.3 Du kan ikke publisere innhold som:\n"
            "- er ulovlig, stotende, diskriminerende eller krenker tredjeparts rettigheter;\n"
            "- utgjor spam, villedende reklame eller inneholder falske anmeldelser;\n"
            "- utgir seg for а vaere en annen person eller enhet;\n"
            "- krenker immaterielle rettigheter.\n\n"
            "4.4 Nevumo forbeholder seg retten til а fjerne eller redigere innhold som bryter med disse Leverandorvilkarene eller gjeldende lov, uten forhåndsvarsel.\n\n"
            "4.5 Krevde profiler: Hvis Nevumo har opprettet en forelopig profil ved hjelp av offentlig tilgjengelig informasjon, kan du kreve denne profilen ved а fullore verifikasjonsprosessen. Etter kravet vil du motta en varsling i henhold til artikkel 14 GDPR som beskriver personopplysningene som oppbevares om deg og rettsgrunnlaget for behandlingen."
        ),
        "fi": (
            "4.1 Rekisteroitymisen jälkeen voit luoda Profiilin ja lisata Palveluilmoituksia. Jokaisen ilmoituksen on tarkasti kuvattava tarjottava palvelu, sen laajuus, hinnoittelu ja saatavuus.\n\n"
            "4.2 Takaat, etta kaikki Profiilissasi ja Palveluilmoituksissasi julkaistu tieto on totuudenmukaista, tarkkaa eika johtava harhaan.\n\n"
            "4.3 Et saa julkaista sisaltoa, joka:\n"
            "- on laitonta, loukkaavaa, syrjivaa tai loukkaa kolmansien osapuolten oikeuksia;\n"
            "- on roskapostia, harhaanjohtavaa mainontaa tai sisaltaa valheellisia arvosteluja;\n"
            "- esiintyy toisena henkilona tai tahona;\n"
            "- loukkaa immateriaalioikeuksia.\n\n"
            "4.4 Nevumo pidattaa oikeuden poistaa tai muokata sisaltoa, joka rikkoo naita Palveluntarjoajan ehtoja tai sovellettavaa lakia, ilman ennakkoilmoitusta.\n\n"
            "4.5 Vaaditut profiilit: Jos Nevumo on luonut alustavan profiilin julkisesti saatavilla olevan tiedon perusteella, voit vaatia ta profiilin suorittamalla vahvistusprosessin. Vaatimisen jälkeen saat ilmoituksen GDPR:n 14 artiklan mukaisesti, joka kuvaa sinusta saatuja henkilotietoja ja niiden kasittelyn oikeusperustaa."
        ),
        "et": (
            "4.1 Peale registreerimise lopetamist saate luua Profiili ja lisada Teenusekuulutusi. Iga kuulutus peab tapselt kirjeldama pakutavat teenust, selle ulatust, hinda ja kattesaadavust.\n\n"
            "4.2 Te garanteerite, et koik teie Profiilil ja Teenusekuulutustes avaldatud teave on tooepärane, täpne ja mitteeksitav.\n\n"
            "4.3 Te ei tohi avaldada sisu, mis:\n"
            "- on ebaseaduslik, solvav, diskrimineeriv voi rikub kolmandate osapoolte oigusi;\n"
            "- kujutab endast rämpsposti, eksitavat reklaami voi sisaldab valeretsensioone;\n"
            "- esitleb end teise isiku voi subektina;\n"
            "- rikub intellektuaalomandi oigusi.\n\n"
            "4.4 Nevumo jätab endale oiguse eemaldada voi muuta sisu, mis rikub neid Pakkuja tingimusi voi kohaldatavat oigust, ilma eelteata.\n\n"
            "4.5 Noudutud profiilid: Kui Nevumo on loonud eelprofiili avalikult kattesaadava teabe põhjal, voidab te seda profiili noudda, lõpetades verifitseerimisprotsessi. Pärast noudmist saate teate GDPR artikli 14 alusel, mis kirjeldab teiega seotud isikuandmeid ja nende töötlemise oiguslikku alust."
        ),
        "lt": (
            "4.1 Baigus registracija, galite sukurti Profili ir prideti Paslaugu skelbimus. Kiekvienas skelbimas turi tiksliai apibūdinti siuloma paslauga, jos aprépti, kainodarą ir prieinamuma.\n\n"
            "4.2 Jus garantuojate, kad visa informacija, paskelbta jusu Profilyje ir Paslaugu skelbimuose, yra teisinga, tiksli ir neklaidinanti.\n\n"
            "4.3 Jus negalite skelbti turinio, kuris:\n"
            "- yra neteisetas, jzeidžiantis, diskriminacinis arba pazeide tretiuju saliu teises;\n"
            "- yra bruklaiskis, klaidinanti reklama arba turi netikrus atsiliepimus;\n"
            "- apsimeta kita asmeniu ar subjektu;\n"
            "- pazeide intelektines nuosavybes teises.\n\n"
            "4.4 Nevumo pasilieka teise pasalinti arba redaguoti bet koki turini, pazeidžianti šias Teikejo salygas arba taikytina teise, be isnksto esnako.\n\n"
            "4.5 Pareikalauti profiliai: Jei Nevumo sukure isankstini profili naudodamasi viesai prieinama informacija, galite pareikalauti sio profilio baigdami patvirtinimo procesa. Po pareikavimo gausite pranešima pagal GDPR 14 straipsni, aprašanti apie jus saugomus asmens duomenis ir ju tvarkymo teisini pagrina."
        ),
        "lv": (
            "4.1 Pec registracijas pabeigsanas varat izveidot Profilu un pievienot Pakalpojumu sludinajumus. Katram sludinajumam precizi jabut aprakstitam pakalpojumu, ta apjomu, cenu un pieejamību.\n\n"
            "4.2 Jus garantejat, ka visa informacija, kas publiceta jusu Profila un Pakalpojumu sludinajumos, ir patiesa, preciza un nemaldinosa.\n\n"
            "4.3 Jums nav attiesIbu publicet saturu, kas:\n"
            "- ir nelikumigs, aizskarось, diskriminejoss vai parek tresu pušu tiesibas;\n"
            "- ir mēstuļu, maldinosu reklamu vai satur vieltus atsauksmes;\n"
            "- uzdodas par citu personu vai subjektu;\n"
            "- parek intelektuala īpašuma tiesibas.\n\n"
            "4.4 Nevumo patur tiesibas nonemт vai rediget jebkadu saturu, kas parek sos Sniedzeja noteikumus vai piemejamo tiesisco regulejumu, bez iepriekšeja brïdinajuma.\n\n"
            "4.5 Pieprasitie profili: Ja Nevumo ir izveidojis pagaidu profilu, izmantojot publiski pieejamu informaciju, varat pieprasit šo profilu, pabeidzot verifikacijas procesu. Pec pieprasisanas jusat sanemsat pazinojumu saskaна ar GDPR 14. pantu, kurā aprakstiti par jums glabātie personas dati un to apstrādes juridiskais pamatojums."
        ),
        "hu": (
            "4.1 A regisztracio befejezese utan letrehozhat egy Profilt es hozzaadhat Szolgaltatasi hirdeteseket. Minden hirdetes pontosan irja le az ajanlott szolgaltatast, annak hatokóret, arat es elerheto-seget.\n\n"
            "4.2 On szavatolja, hogy a Profiljaban es Szolgaltatasi hirdetéseiben közzétett összes informacio igaz, pontos es nem félrevezetö.\n\n"
            "4.3 Nem tehet közzé olyan tartalmat, amely:\n"
            "- jogellenes, sertegetö, diszkriminativ vagy harmadik felek jogait sérti;\n"
            "- spamet, félrevezeto reklamot képvisel vagy hamis ertekeléseket tartalmaz;\n"
            "- más személyt vagy jogi alanyt személyesít meg;\n"
            "- szellemi tulajdonjogokat serti.\n\n"
            "4.4 A Nevumo fenntartja a jogot, hogy elozetes értesítes nélkül eltávolítson vagy szerkesszen bármely tartalmat, amely megsérti ezeket a Szolgáltatói Feltételeket vagy a vonatkozo jogszabályokat.\n\n"
            "4.5 Igényelt profilok: Ha a Nevumo nyilvanosan elérhető informaciok alapjan elozetes profilt hozott létre, igényelhetí ezt a profilt a verificacios folyamat befejezesevel. Az igenyles utan a GDPR 14. cikke alapjan értesítést kap, amely leirja az Önrőol tárolt személyes adatokat és azok kezelésének jogalapját."
        ),
        "hr": (
            "4.1 Nakon sto dovrsiti registraciju, mozete kreirati Profil i dodati Ponude usluga. Svaka ponuda mora tocno opisivati ponudenu uslugu, njezin opseg, cijenu i dostupnost.\n\n"
            "4.2 Jamcite da su sve informacije objavljene na vasem Profilu i u Ponudama usluga istinite, tocne i nije zavádzajuci.\n\n"
            "4.3 Ne smijete objavljivati sadrzaj koji:\n"
            "- je nezakonit, uvredljiv, diskriminatoran ili porusuje prava treecih strana;\n"
            "- predstavlja spam, zavádzajuce oglasavanje ili sadrzi lazne recenzije;\n"
            "- glumi drugu osobu ili subjekt;\n"
            "- porusuje prava intelektualnog vlasnistva.\n\n"
            "4.4 Nevumo zadrzava pravo uklanjanja ili uredivanja sadrzaja koji kuri ove Uvjete pruzatelja ili vazece pravo, bez prethodne obavijesti.\n\n"
            "4.5 Preuzeti profili: Ako je Nevumo stvorilo preliminarni profil koristeci javno dostupne informacije, mozete preuzeti taj profil dovrsavanjem procesa verifikacije. Nakon preuzimanja primit cete obavijest prema cl. 14 GDPR-a opisujuci osobne podatke koji se o vama cuvaju i pravnu osnovu za njihovu obradu."
        ),
        "sk": (
            "4.1 Po dokonceni registracie mozete vytvorit Profil a pridat Ponuky sluzieb. Kazda ponuka musi presne popisovat ponukanu sluzbu, jej rozsah, cenu a dostupnost.\n\n"
            "4.2 Zarucate, ze vsetky informacie zverejnene na vasom Profile a v Ponukach sluzieb su pravdive, presne a nezavádzajuce.\n\n"
            "4.3 Nesmiete zverejnovat obsah, ktory:\n"
            "- je nezakonny, urazlivy, diskriminacny alebo porusuje prava tretich stran;\n"
            "- predstavuje spam, klamlivu reklamu alebo obsahuje false recenzie;\n"
            "- sa vydava za inu osobu alebo subjekt;\n"
            "- porusuje prava dusevneho vlastnictva.\n\n"
            "4.4 Nevumo si vyhrazuje pravo odstranit alebo upravit akykolvek obsah, ktory porusuje tieto Podmienky poskytovatela alebo platne pravne predpisy, bez predchoziho upozornenia.\n\n"
            "4.5 Narokovane profily: Ak Nevumo vytvorilo predbezny profil na zaklade verejne dostupnych informacii, mozete si tento profil narokovat dokoncenim overovacinho procesu. Po narokovani dostanete oznamenie podla cl. 14 GDPR popisujuce osobne udaje o vas uchovavane a pravny zaklad pre ich spracovanie."
        ),
        "sl": (
            "4.1 Po zakljucku registracije lahko ustvarite Profil in dodate Oglase storitev. Vsak oglas mora natancno opisati ponujeno storitev, njen obseg, ceno in razpolozljivost.\n\n"
            "4.2 Jamcite, da so vse informacije, objavljene na vasem Profilu in v Oglasih storitev, resnicne, natancne in ne zavádzajuci.\n\n"
            "4.3 Ne smete objavljati vsebine, ki:\n"
            "- je nezakonita, zaljiva, diskriminatorna ali krsi pravice tretjih;\n"
            "- predstavlja vsiljeno pošto, zavajajoco reklamo ali vsebuje lazne ocene;\n"
            "- se dela za drugo osebo ali subjekt;\n"
            "- krsi pravice intelektualne lastnine.\n\n"
            "4.4 Nevumo si pridrzuje pravico do odstranitve ali urejanja vsebine, ki krsi te Pogoje ponudnika ali veljavno pravo, brez predhodnega obvestila.\n\n"
            "4.5 Zahtevani profili: Ce je Nevumo ustvarilo predhodni profil z uporabo javno dostopnih informacij, lahko ta profil zahtevate z zakljuckom postopka verificiranja. Po zahtevi boste prejeli obvestilo po 14. clenu GDPR, ki opisuje osebne podatke, shranjene o vas, in pravno podlago za njihovo obdelavo."
        ),
        "el": (
            "4.1 Kata tin oloklirosi tis eggrafis sas, mporite na dimiourghísite ena Profil kai na prosthesete Katalogous Ypiresbion. Kathe katálogos prepei na perigraphi akribos tin prosthethoméni ypiresia, tin ektasí tis, tin timologisi kai tin diathesimotita.\n\n"
            "4.2 Bebaiónete oti oles oi plirofories pou dimosievontai sto Profil sas kai stous Katalogous Ypiresbion einai alitheis, akribeís kai mī parapeianoúses.\n\n"
            "4.3 Den epitrepetai na dimosievete periechomeno pou:\n"
            "- einai paranomo, prosblitiko, diskriminatoriko i parabiazetai dikaiomata triton;\n"
            "- apoteleí spam, parapeinantikí diafimisi i periechei pseudes kritikoús;\n"
            "- parousiazetai os allo atomo i entiti;\n"
            "- parabiazei dikaiomata pneumatikis idioktisias.\n\n"
            "4.4 I Nevumo diatirei to dikaioma na afairései i na epeksergastei opoiodipote periechomeno pou parabiazetai autous tous Orous Paróchou i to efarmosteo dikaio, choris proigoumeni eidopoiisi.\n\n"
            "4.5 Diekeikimena Profil: An i Nevumo dimiourgise prokatarktiko profil me dimosia diathesimes plirofories, mporite na diekdikísete auto to profil oloklironontas tin diadikasia epiloghis. Meta ti diekedikisi, tha labete mia eidopoiisi symfonos me to Arthro 14 tou GDPR pou perigraphei ta prosonpika dedomena pou diatirontai gia sas kai ti nomiki vasi gia tin epeksergasia tous."
        ),
        "tr": (
            "4.1 Kaydı tamamladıktan sonra bir Profil oluşturabilir ve Hizmet Listemeleri ekleyebilirsiniz. Her listeleme sunulan hizmeti, kapsamını, fiyatlandırmasını ve müsaitlik durumunu doğru bir şekilde açıklamalıdır.\n\n"
            "4.2 Profilinizde ve Hizmet Listelerinizde yayınlanan tüm bilgilerin doğru, kesin ve yanıltıcı olmadığını garanti edersiniz.\n\n"
            "4.3 Asağıdaki içerikleri yayınlayamazsınız:\n"
            "- yasadışı, hakaret içeren, ayrımcı olan veya üçüncü tarafların haklarını ihlal eden;\n"
            "- spam, yanıltıcı reklam veya sahte değerlendirme içeren;\n"
            "- başka bir kişi veya kuruluş kılığına giren;\n"
            "- fikri mülkiyet haklarını ihlal eden.\n\n"
            "4.4 Nevumo, bu Saglayici Kosullarını veya yürürlükteki yasaları ihlal eden herhangi bir içeriği önceden bildirim yapmaksızın kaldırma veya düzenleme hakkını saklı tutar.\n\n"
            "4.5 Talep Edilen Profiller: Nevumo kamuya açık bilgileri kullanarak ön profil oluşturmuşsa, doğrulama işlemini tamamlayarak bu profili talep edebilirsiniz. Talep sonrasında GDPR Madde 14 kapsamında hakkınızda tutulan kişisel verileri ve bunların işlenmesinin hukuki dayanaklarını açıklayan bir bildirim alacaksınız."
        ),
        "ga": (
            "4.1 Tar éis an clárú a chríochnú, is féidir leat Próifíl a chruthú agus Liostaí Seirbhíse a chur leis. Ní mór do gach liostáil an tseirbhís a thairgtear, a raon, a phraghasáil agus a infhaighteacht a chur síos go cruinn.\n\n"
            "4.2 Ráthaíonn tú go bhfuil gach faisnéis a fhoilsítear ar do Phróifíl agus i do Liostaí Seirbhíse fírinneach, cruinn agus nach bhfuil sí míthreorach.\n\n"
            "4.3 Ní ceadmhach duit ábhar a fhoilsiú atá:\n"
            "- mídhleathach, maslach, idirdhealaitheach nó a sháraíonn cearta tríú páirtí;\n"
            "- ina thúsaíocht, ina fhógraíocht mhíthreorach nó ina bhfuil léirmheasanna bréagacha;\n"
            "- ag ligean air gur duine nó eintiteas eile é;\n"
            "- ag sárú cearta maoine intleachtúla.\n\n"
            "4.4 Coimeádann Nevumo an ceart ábhar a sháraíonn na Téarmaí seo don Solathroir nó dlí infheidhme a bhaint nó a chur in eagar, gan fógra roimhe ré.\n\n"
            "4.5 Próifílí a éilíodh: Má chruthaigh Nevumo próifíl réamhullmhaithe ag baint úsáide as faisnéis atá ar fáil go poiblí, is féidir leat an phróifíl seo a éileamh tríd an bpróiseas fíorúcháin a chomhlíonadh. Tar éis an éilimh, gheobhaidh tú fógra faoi Airteagal 14 GDPR ag cur síos ar na sonraí pearsanta atá á gcoimeád fút agus ar an mbonn dlí lena n-úracán."
        ),
        "is": (
            "4.1 Eftir að lokið er við skrángingu getur þú búið til Notandasnið og bætt við Þjónustufærslum. Hvert þjónustuupps verður að lýsa nákvæmlega þjónustunni sem boðin er upp á, umfangi hennar, verðlagningu og framboði.\n\n"
            "4.2 Þú tryggir að allar upplýsingar sem birt eru á þínu Notandasniði og í þínum Þjónustufærslum séu sannar, nákvæmar og ekki villandi.\n\n"
            "4.3 Þér er óheimilt að birta efni sem:\n"
            "- er ólöglegt, móðgandi, mismunandi eða brýtur gegn réttindum þriðja aðila;\n"
            "- er ruslpóstur, villandi auglysing eða inniheldur fölsk umsögn;\n"
            "- þykist vera annar aðili eða eining;\n"
            "- brýtur gegn hugverkaréttindum.\n\n"
            "4.4 Nevumo áskilur sér rétt til að fjarlægja eða breyta efni sem brýtur gegn þessum Skilmálum veituaðila eða gildandi lögum, án fyrirvara.\n\n"
            "4.5 Krafðar notandasnið: Ef Nevumo hefur búið til bráðabirgðasnið með almennt aðgengilegum upplýsingum getur þú krafist þessa sniðs með því að ljúka staðfestingarferlinu. Eftir kröfuna munt þú fá tilkynningu skv. gr. 14 GDPR sem lýsir persónuupplýsingum sem geymdar eru um þig og lagagrundvöllinn fyrir vinnslu þeirra."
        ),
        "lb": (
            "4.1 No der Vollendung vun der Registréierung kënnt Dir e Profil erstellen an Serviceannoncen addéieren. All Annonce muss d'Serviceleistung, hiren Ëmfang, d'Präisgestaltung an d'Verfügbarkeit genee beschreiwen.\n\n"
            "4.2 Dir garantéiert, datt all Informatiounen, déi op Ärem Profil an an Äre Serviceannoncen verëffentlecht ginn, wouer, korrekt a net irreféirent sinn.\n\n"
            "4.3 Dir däerft kee Inhalt publizéieren, deen:\n"
            "- illegal, beleedegend, diskriminatorisch ass oder Drëttparteienrechter verletzt;\n"
            "- Spam, irreféirent Reklamm oder falsch Bewäertungen enthält;\n"
            "- eng aner Persoun oder Entitéit virspillt;\n"
            "- intellektuell Eegentoumsrechter verletzt.\n\n"
            "4.4 Nevumo behält sech d'Recht, Inhalte, déi géint dës Presser-Bedingungen oder gëltend Recht verstoussen, ouni Virankündigung ze entfernen oder ze beaarbechten.\n\n"
            "4.5 Beanspruchte Profiler: Wann Nevumo e virleefegen Profil mat öffentlech verfügbare Informatiounen erstellt huet, kënnt Dir dëse Profil beunsprichen andeems Dir de Verifizéierungsprozess ofschléisst. No der Beanspruchung kritt Dir eng Notifikatioun gemaess Art. 14 DSGVO, déi d'iwwer Iech gespeichert perséinlech Donnéeën a Rechtsgrondlag fir hir Veraarbechtung beschreift."
        ),
        "mk": (
            "4.1 Po zavrsuvanjeto na registracijata mozete da kreirate Profil i da dodavate Oglasi za uslugi. Sekoj oglas mora tocno da ja opise ponudenata usluga, neiniot obem, cena i dostapnost.\n\n"
            "4.2 Garantirate deka site informacii objavljeni na vasiot Profil i vo Oglasit e za uslugi se vistiniti, tocni i niso zavádzajuci.\n\n"
            "4.3 Ne smee da objavljuvate sodrzina koja:\n"
            "- e nezakonita, uvredliva, diskriminatorna ili gi krsi pravata na treti strani;\n"
            "- pretstavuva spam, zavádzajuco oglasuvanje ili sodrzi lazni recenzii;\n"
            "- se pretvara deka e drug chovek ili entitet;\n"
            "- gi krsí pravata na intelektualna sopstvenost.\n\n"
            "4.4 Nevumo go zadrзuva pravoto da ja otстрани ili uredi sodrzinata koja gi krsí ovie Uslovi na davacot ili primenlivo pravo, bez prethodno izvestuvanje.\n\n"
            "4.5 Barani profili: Ako Nevumo kreiralo preliminaren profil koristejki javno dostapni informacii, moze da go barat toj profil zavrsuvajki go procesot na verifikacija. Po baranjeto ke primite izvestuvanje spored cl. 14 od GDPR koe gi opisuva personalnite podatoci shto se chuvat za vas i pravnata osnova za nivnata obrabotka."
        ),
        "mt": (
            "4.1 Meta tlesti r-registrazzjonі, tista' toħloq Profil u żżid Listati ta' Servizzi. Kull listata trid tiddeskrivi b'mod preċiż is-servizz offrut, l-ambitu tiegħu, il-prezz u d-disponibilità.\n\n"
            "4.2 Tiggarantixxi li l-informazzjonī kollha ppubblikata fuq il-Profil tiegħek u fil-Listati ta' Servizzi hija veritiera, preċiża u mhux qarrieqa.\n\n"
            "4.3 Ma tistax tippubblika kontenut li:\n"
            "- huwa illegali, offensiv, diskriminatorju jew jikser drittijiet ta' terzi;\n"
            "- jikkostitwixxi spam, reklamar qarrieqi jew fih reviews foloz;\n"
            "- jimpersona persuna jew entita oħra;\n"
            "- jikser drittijiet tal-proprjeta intellettwali.\n\n"
            "4.4 Nevumo tiżżomm id-dritt li tneħħi jew teditja kwalunkwe kontenut li jikser dawn it-Termini tal-Fornitur jew il-ligi applikabbli, mingħajr avviż minn qabel.\n\n"
            "4.5 Profilijiet Mitluba: Jekk Nevumo ħolqot profil preliminari bl-użu ta' informazzjonī disponibbli pubblikament, tista' titlob dan il-profil billi tlesti l-proċess tal-verifika. Wara t-talba, tirċievi notifika skont l-Artikolu 14 tal-GDPR li tiddeskrivi d-data personali miżmuma dwarak u l-bażi legali għall-ipproċessar tagħha."
        ),
        "sq": (
            "4.1 Pasi te perfundoni regjistrimin, mund te krijoni nje Profil dhe te shtoni Listime Sherbimesh. Cdo listim duhet te pershkruaje me saktesi sherbimin e ofruar, shtrirjen e tij, cmimet dhe disponibilitetin.\n\n"
            "4.2 Garantoni qe te gjitha informacionet e publikuara ne Profilin tuaj dhe ne Listezimet e Sherbimeve jane te verteta, te sakta dhe jo mashtruese.\n\n"
            "4.3 Nuk mund te publikoni permbajtje qe:\n"
            "- eshte e paligjshme, fyese, diskriminuese ose shkel te drejtat e paleve te treta;\n"
            "- perbejne spam, reklamim mashtrues ose permbajne komente te rreme;\n"
            "- imiton nje person tjeter ose nje entitet;\n"
            "- shkel te drejtat e pronesise intelektuale.\n\n"
            "4.4 Nevumo ruan te drejten te heqe ose te modifikoje cdo permbajtje qe shkel keto Kushte te Ofruesit ose legjislacionin e zbatueshëm, pa njoftim paraprak.\n\n"
            "4.5 Profile te reklamuara: Nese Nevumo ka krijuar nje profil paraprak duke perdorur informacione ne dispozicion te publikut, mund ta reklamoni kete profil duke perfunduar procesin e verifikimit. Pas reklamimit, do te merrni nje njoftim sipas Nenit 14 te GDPR-se qe pershkruan te dhenat personale qe mbahen per ju dhe bazen ligjore per perpunimin e tyre."
        ),
        "sr": (
            "4.1 Nakon sto zavrsiti registraciju, mozete kreirati Profil i dodavati Oglase usluga. Svaki oglas mora tacno opisivati ponudenu uslugu, njen obim, cenu i dostupnost.\n\n"
            "4.2 Garantujete da su sve informacije objavljene na vasem Profilu i u Oglasima usluga istinite, tacne i nisu zavádzajuce.\n\n"
            "4.3 Ne smete objavljivati sadrzaj koji:\n"
            "- je nezakonit, uvredljiv, diskriminatoran ili porusuje prava trecih strana;\n"
            "- predstavlja spam, zavádzajuce oglasavanje ili sadrzi lazne recenzije;\n"
            "- se pretvara da je druga osoba ili entitet;\n"
            "- porusuje prava intelektualne svojine.\n\n"
            "4.4 Nevumo zadrzava pravo da ukloni ili uredi sadrzaj koji kuri ove Uslove pruzaoca ili vazece pravo, bez prethodnog obaveštenja.\n\n"
            "4.5 Preuzeti profili: Ako je Nevumo kreiralo preliminarni profil koristeci javno dostupne informacije, mozete preuzeti taj profil dovrsavanjem procesa verifikacije. Nakon preuzimanja primicete obavestenje prema cl. 14 GDPR-a koji opisuje licne podatke koji se o vama cuvaju i pravni osnov za njihovu obradu."
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
            f"✅ seed_provider_terms_p11_art4_body: {count} rows upserted "
            f"({NAMESPACE}: art4_body x 34 langs)"
        )

    engine.dispose()


if __name__ == "__main__":
    seed()
