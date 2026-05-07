#!/usr/bin/env python3
"""
Seed script to add Phase 3B Part 1 SEO keys for 15 missing languages
Keys: category.seo_massage_h3_1, h3_2, p1, p2, p3 (5 keys)
      category.seo_plumbing_h3_1, h3_2, p2, p3 (4 keys)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_phase3b_part1_seo_keys
"""
from sqlalchemy import text
from apps.api.database import SessionLocal

PHASE3B_PART1_TRANSLATIONS = {
    "cs": {
        "category.seo_massage_h3_1": "Jak si vybrat maséra?",
        "category.seo_massage_h3_2": "Kolik stojí masáž v {city}?",
        "category.seo_massage_p1": "{city} nabízí široký výběr profesionálních masérů. Ať už hledáte relaxační, sportovní nebo terapeutickou masáž, Nevumo vám pomůže najít důvěryhodné odborníky v okolí.",
        "category.seo_massage_p2": "Prověřte si recenze předchozích klientů, zkušenosti specialisty a rozsah nabízených služeb. Dobrý masér přizpůsobí techniku vašim potřebám.",
        "category.seo_massage_p3": "Profesionální masážní terapie pro uvolnění stresu a zlepšení vaší pohody. Rezervujte si sezení u zkušených terapeutů ve vašem městě.",
        "category.seo_plumbing_h3_1": "Kdy zavolat instalatéra?",
        "category.seo_plumbing_h3_2": "Kolik stojí instalatér v {city}?",
        "category.seo_plumbing_p2": "Instalatéra zavolejte v případě poruchy vodovodního systému, kapajících kohoutků, ucpaných odtoků a při rekonstrukci koupelny nebo kuchyně.",
        "category.seo_plumbing_p3": "Expertní instalatérská řešení pro jakékoli naléhavé situace nebo plánované opravy. Rychlá reakce a garantovaná kvalita od místních specialistů."
    },
    "da": {
        "category.seo_massage_h3_1": "Hvordan vælger man en massagespecialist?",
        "category.seo_massage_h3_2": "Hvad koster massage i {city}?",
        "category.seo_massage_p1": "{city} tilbyder et bredt udvalg af professionelle massagespecialister. Uanset om du leder efter afslappende, sports- eller terapeutisk massage, hjælper Nevumo dig med at finde betroede fagfolk i nærheden.",
        "category.seo_massage_p2": "Tjek tidligere kunders anmeldelser, specialistens erfaring og omfanget af de tilbudte tjenester. En god massagespecialist vil tilpasse teknikken til dine behov.",
        "category.seo_massage_p3": "Professionel massageterapi til at lindre stress og forbedre dit velvære. Book en session med erfarne terapeuter i din by.",
        "category.seo_plumbing_h3_1": "Hvornår skal man ringe til en blikkenslager?",
        "category.seo_plumbing_h3_2": "Hvad koster en blikkenslager i {city}?",
        "category.seo_plumbing_p2": "Ring til en blikkenslager ved fejl i vandsystemet, utætte vandhaner, tilstoppede afløb og under renovering af badeværelse eller køkken.",
        "category.seo_plumbing_p3": "Eksperte VVS-løsninger til enhver nødsituation eller planlagt reparation. Hurtig respons og garanteret kvalitet fra lokale specialister."
    },
    "de": {
        "category.seo_massage_h3_1": "Wie wählt man einen Massagespezialisten aus?",
        "category.seo_massage_h3_2": "Was kostet eine Massage in {city}?",
        "category.seo_massage_p1": "{city} bietet eine große Auswahl an professionellen Massagespezialisten. Egal, ob Sie eine Entspannungs-, Sport- oder Therapiemassage suchen, Nevumo hilft Ihnen, vertrauenswürdige Profis in Ihrer Nähe zu finden.",
        "category.seo_massage_p2": "Überprüfen Sie frühere Kundenbewertungen, die Erfahrung des Spezialisten und den Umfang der angebotenen Dienstleistungen. Ein guter Massagespezialist passt die Technik an Ihre Bedürfnisse an.",
        "category.seo_massage_p3": "Professionelle Massagetherapie zum Stressabbau und zur Verbesserung Ihres Wohlbefindens. Buchen Sie eine Sitzung bei erfahrenen Therapeuten in Ihrer Stadt.",
        "category.seo_plumbing_h3_1": "Wann sollte man einen Klempner rufen?",
        "category.seo_plumbing_h3_2": "Was kostet ein Klempner in {city}?",
        "category.seo_plumbing_p2": "Rufen Sie einen Klempner bei Ausfällen des Wassersystems, undichten Wasserhähnen, verstopften Abflüssen sowie bei Bad- oder Küchenrenovierungen.",
        "category.seo_plumbing_p3": "Expertenlösungen für Sanitärinstallationen bei Notfällen oder geplanten Reparaturen. Schnelle Reaktion und garantierte Qualität von lokalen Spezialisten."
    },
    "el": {
        "category.seo_massage_h3_1": "Πώς να επιλέξετε έναν ειδικό στο μασάζ;",
        "category.seo_massage_h3_2": "Πόσο κοστίζει το μασάζ στο {city};",
        "category.seo_massage_p1": "Το {city} προσφέρει μια μεγάλη ποικιλία από επαγγελματίες ειδικούς στο μασάζ. Είτε αναζητάτε χαλαρωτικό, αθλητικό ή θεραπευτικό μασάζ, το Nevumo σας βοηθά να βρείτε έμπιστους επαγγελματίες κοντά σας.",
        "category.seo_massage_p2": "Ελέγξτε τις κριτικές προηγούμενων πελατών, την εμπειρία του ειδικού και το εύρος των προσφερόμενων υπηρεσιών. Ένας καλός ειδικός στο μασάζ θα προσαρμόσει την τεχνική στις ανάγκες σας.",
        "category.seo_massage_p3": "Επαγγελματική θεραπεία μασάζ για την ανακούφιση από το στρες και τη βελτίωση της ευεξίας σας. Κλείστε μια συνεδρία με έμπειρους θεραπευτές στην πόλη σας.",
        "category.seo_plumbing_h3_1": "Πότε να καλέσετε έναν υδραυλικό;",
        "category.seo_plumbing_h3_2": "Πόσο κοστίζει ένας υδραυλικός στο {city};",
        "category.seo_plumbing_p2": "Καλέστε έναν υδραυλικό για βλάβες στο σύστημα ύδρευσης, βρύσες που στάζουν, βουλωμένες αποχετεύσεις και κατά τη διάρκεια ανακαινίσεων μπάνιου ή κουζίνας.",
        "category.seo_plumbing_p3": "Εξειδικευμένες υδραυλικές λύσεις για κάθε επείγουσα ανάγκη ή προγραμματισμένη επισκευή. Γρήγορη ανταπόκριση και εγγυημένη ποιότητα από τοπικούς ειδικούς."
    },
    "es": {
        "category.seo_massage_h3_1": "¿Cómo elegir a un especialista en masajes?",
        "category.seo_massage_h3_2": "¿Cuánto cuesta un masaje en {city}?",
        "category.seo_massage_p1": "{city} ofrece una amplia selección de especialistas en masajes profesionales. Ya sea que busques un masaje relajante, deportivo o terapéutico, Nevumo te ayuda a encontrar profesionales de confianza cerca de ti.",
        "category.seo_massage_p2": "Consulta las opiniones de clientes anteriores, la experiencia del especialista y la oferta de servicios. Un buen especialista en masajes adaptará la técnica a tus necesidades.",
        "category.seo_massage_p3": "Terapia de masaje profesional para aliviar el estrés y mejorar tu bienestar. Reserva una sesión con terapeutas experimentados en tu ciudad.",
        "category.seo_plumbing_h3_1": "¿Cuándo llamar a un fontanero?",
        "category.seo_plumbing_h3_2": "¿Cuánto cuesta un fontanero en {city}?",
        "category.seo_plumbing_p2": "Llama a un fontanero por averías en el sistema de agua, grifos que gotean, desagües atascados y durante reformas de baño o cocina.",
        "category.seo_plumbing_p3": "Soluciones de fontanería expertas para cualquier emergencia o reparación planificada. Respuesta rápida y calidad garantizada de especialistas locales."
    },
    "et": {
        "category.seo_massage_h3_1": "Kuidas valida masaažispetsialisti?",
        "category.seo_massage_h3_2": "Kui palju maksab massaaž {city}?",
        "category.seo_massage_p1": "{city} pakub laia valikut professionaalseid masaažispetsialiste. Olenemata sellest, enjoy kas otsite lõõgastavat, spordi- või ravimassaaži, aitab Nevumo teil leida usaldusväärseid spetsialiste lähedases.",
        "category.seo_massage_p2": "Kontrollige varasemate klientide arvustusi, spetsialisti kogemusi ja pakutavate teenuste ulatust. Hea masaažispetsialist kohandab tehnika vastavalt teie vajadustele.",
        "category.seo_massage_p3": "Professionaalne massaažiteraapia stressi leevendamiseks ja heaolu parandamiseks. Broneerige seanss kogenud terapeutide juures oma linnas.",
        "category.seo_plumbing_h3_1": "Millal helistada torulukksepale?",
        "category.seo_plumbing_h3_2": "Kui palju maksab torulukksepp {city}?",
        "category.seo_plumbing_p2": "Helistage torulukksepale veesüsteemi rikete, lekivate kraanide, ummistunud äravoolude ning vannitoa või köögi renoveerimise korral.",
        "category.seo_plumbing_p3": "Ekspertsed sanitaartehnilised lahendused igaks hädaolukorraks või planeeritud remondiks. Kiire reageerimine ja garanteeritud kvaliteet kohalikelt spetsialistidelt."
    },
    "fi": {
        "category.seo_massage_h3_1": "Kuinka valita hieronnan ammattilainen?",
        "category.seo_massage_h3_2": "Paljonko hieronta maksaa kaupungissa {city}?",
        "category.seo_massage_p1": "{city} tarjoaa laajan valikoiman ammattitaitoisia hieronnan asiantuntijoita. Etsitpä sitten rentouttavaa, urheilu- tai terapeuttista hierontaa, Nevumo auttaa sinua löytämään luotettavat ammattilaiset läheltäsi.",
        "category.seo_massage_p2": "Tarkista aiempien asiakkaiden arvostelut, asiantuntijan kokemus ja tarjottujen palvelujen laajuus. Hyvä hieroja mukauttaa tekniikan tarpeisiisi.",
        "category.seo_massage_p3": "Ammattimainen hierontaterapia stressin lievittämiseen ja hyvinvointisi parantamiseen. Varaa aika kokeneelta terapeutilta kaupungissasi.",
        "category.seo_plumbing_h3_1": "Milloin kutsua putkiasentaja?",
        "category.seo_plumbing_h3_2": "Paljonko putkiasentaja maksaa kaupungissa {city}?",
        "category.seo_plumbing_p2": "Kutsu putkiasentaja vesijärjestelmän vikojen, vuotavien hanojen, tukkeutuneiden viemäreiden sattuessa sekä kylpyhuone- tai keittiöremontin aikana.",
        "category.seo_plumbing_p3": "Asiantuntevat putkityöratkaisut kaikkiin hätätilanteisiin tai suunniteltuihin korjauksiin. Nopea vastaus ja taattu laatu paikallisilta asiantuntijoilta."
    },
    "fr": {
        "category.seo_massage_h3_1": "Comment choisir un spécialiste du massage ?",
        "category.seo_massage_h3_2": "Combien coûte un massage à {city} ?",
        "category.seo_massage_p1": "{city} offre une large sélection de spécialistes du massage professionnels. Que vous recherchiez un massage relaxant, sportif ou thérapeutique, Nevumo vous aide à trouver des professionnels de confiance à proximité.",
        "category.seo_massage_p2": "Consultez les avis des clients précédents, l'expérience du spécialiste et l'éventail des services offerts. Un bon spécialiste du massage saura adapter sa technique à vos besoins.",
        "category.seo_massage_p3": "Massothérapie professionnelle pour soulager le stress et améliorer votre bien-être. Réservez une séance avec des thérapeutes expérimentés dans votre ville.",
        "category.seo_plumbing_h3_1": "Quand appeler un plombier ?",
        "category.seo_plumbing_h3_2": "Combien coûte un plombier à {city} ?",
        "category.seo_plumbing_p2": "Appelez un plombier en cas de panne du système d'eau, de robinets qui fuient, de canalisations bouchées et lors de rénovations de salle de bain ou de cuisine.",
        "category.seo_plumbing_p3": "Solutions de plomberie expertes pour toute urgence ou réparation planifiée. Réponse rapide et qualité garantie par des spécialistes locaux."
    },
    "ga": {
        "category.seo_massage_h3_1": "Conas speisialtóir suathaireachta a roghnú?",
        "category.seo_massage_h3_2": "Cé mhéad a chosnaíonn suathaireacht i {city}?",
        "category.seo_massage_p1": "Cuireann {city} rogha leathan de speisialtóirí suathaireachta gairmiúla ar fáil. Cibé an bhfuil tú ag lorg suathaireacht scíthe, spóirt nó teiripeach, cabhraíonn Nevumo leat gairmithe iontaofa a fháil in aice láimhe.",
        "category.seo_massage_p2": "Seiceáil léirmheasanna ó chliaint roimhe seo, taithí an speisialtóra, agus raon na seirbhísí a chuirtear ar fáil. Déanfaidh speisialtóir suathaireachta maith an teicníc a oiriúnú do do chuid riachtanas.",
        "category.seo_massage_p3": "Teiripe suathaireachta gairmiúil chun strus a mhaolú agus do dhea-bhail a fheabhsú. Cuir seisiún in áirithe le teiripeoirí oilte i do chathair.",
        "category.seo_plumbing_h3_1": "Cathain ar chóir pluiméir a ghlaoch?",
        "category.seo_plumbing_h3_2": "Cé mhéad a chosnaíonn pluiméir i {city}?",
        "category.seo_plumbing_p2": "Glaoigh ar phluiméir le haghaidh teipeanna sa chóras uisce, sconnaí ag sceitheadh, draenacha clogged, agus le linn athchóirithe seomra folctha nó cistine.",
        "category.seo_plumbing_p3": "Réitigh pluiméireachta saineolacha d'aon éigeandáil nó deisiúchán pleanáilte. Freagairt thapa agus cáilíocht ráthaithe ó speisialtóirí pluiméireachta áitiúla."
    },
    "hr": {
        "category.seo_massage_h3_1": "Kako odabrati stručnjaka za masažu?",
        "category.seo_massage_h3_2": "Koliko košta masaža u {city}?",
        "category.seo_massage_p1": "{city} nudi širok izbor profesionalnih stručnjaka za masažu. Bez obzira tražite li opuštajuću, sportsku ili terapeutsku masažu, Nevumo vam pomaže pronaći provjerene stručnjake u blizini.",
        "category.seo_massage_p2": "Provjerite recenzije prethodnih klijenata, iskustvo stručnjaka i opseg ponuđenih usluga. Dobar stručnjak za masažu prilagodit će tehniku vašim potrebama.",
        "category.seo_massage_p3": "Profesionalna masažna terapija za ublažavanje stresa i poboljšanje vašeg blagostanja. Rezervirajte termin kod iskusnih terapeuta u svom gradu.",
        "category.seo_plumbing_h3_1": "Kada pozvati vodoinstalatera?",
        "category.seo_plumbing_h3_2": "Koliko košta vodoinstalater u {city}?",
        "category.seo_plumbing_p2": "Pozovite vodoinstalatera u slučaju kvara vodovodnog sustava, slavina koje cure, začepljenih odvoda te tijekom renoviranja kupaonice ili kuhinje.",
        "category.seo_plumbing_p3": "Stručna rješenja za vodoinstalacije za sve hitne slučajeve ili planirane popravke. Brza reakcija i zajamčena kvaliteta lokalnih stručnjaka."
    },
    "hu": {
        "category.seo_massage_h3_1": "Hogyan válasszunk masszázsspecialistát?",
        "category.seo_massage_h3_2": "Mennyibe kerül a masszázs {city} területén?",
        "category.seo_massage_p1": "{city} professzionális masszázsspecialisták széles választékát kínálja. Akár relaxáló, sport- vagy terápiás masszázst keres, a Nevumo segít megbízható szakembereket találni a közelben.",
        "category.seo_massage_p2": "Ellenőrizze a korábbi ügyfelek véleményét, a szakember tapasztalatát és a kínált szolgáltatások körét. Egy jó masszázsspecialista az Ön igényeihez igazítja a technikát.",
        "category.seo_massage_p3": "Professzionális masszázsterápia a stressz oldására és a közérzet javítására. Foglaljon időpontot tapasztalt terapeutákhoz az Ön városában.",
        "category.seo_plumbing_h3_1": "Mikor hívjunk vízvezeték-szerelőt?",
        "category.seo_plumbing_h3_2": "Mennyibe kerül egy vízvezeték-szerelő {city} területén?",
        "category.seo_plumbing_p2": "Hívjon vízvezeték-szerelőt vízhálózat-meghibásodás, csöpögő csapok, eldugult lefolyók esetén, valamint fürdőszoba- vagy konyhafelújítás során.",
        "category.seo_plumbing_p3": "Szakszerű vízvezeték-szerelési megoldások sürgősségi esetekre vagy tervezett javításokra. Gyors válaszadás és garantált minőség helyi szakemberektől."
    },
    "is": {
        "category.seo_massage_h3_1": "Hvernig á að velja nuddara?",
        "category.seo_massage_h3_2": "Hvað kostar nudd í {city}?",
        "category.seo_massage_p1": "{city} býður upp á mikið úrval af faglegum nuddurum. Hvort sem þú ert að leita að slökunar-, íþrótta- eða lækninganuddi, þá hjálpar Nevumo þér að finna trausta fagaðila í nágrenninu.",
        "category.seo_massage_p2": "Skoðaðu umsagnir fyrri viðskiptavina, reynslu fagaðilans og umfang þeirrar þjónustu sem í boði er. Góður nuddari mun aðlaga tæknina að þínum þörfum.",
        "category.seo_massage_p3": "Fagleg nuddmeðferð til að losa um streitu og bæta vellíðan þína. Bókaðu tíma hjá reyndum nuddara í þinni borg.",
        "category.seo_plumbing_h3_1": "Hvenær á að hringja í pípulagningamann?",
        "category.seo_plumbing_h3_2": "Hvað kostar pípulagningamaður í {city}?",
        "category.seo_plumbing_p2": "Hringdu í pípulagningamann vegna bilana í vatnskerfi, lekandi krana, stíflaðra niðurfalla og við endurbætur á baðherbergi eða eldhúsi.",
        "category.seo_plumbing_p3": "Sérhæfðar lausnir í pípulögnum fyrir hvers kyns neyðartilvik eða skipulagðar viðgerðir. Fljótleg viðbrögð og tryggð gæði frá staðbundnum fagaðilum."
    },
    "it": {
        "category.seo_massage_h3_1": "Come scegliere uno specialista del massaggio?",
        "category.seo_massage_h3_2": "Quanto costa un messaggio a {city}?",
        "category.seo_massage_p1": "{city} offre un'ampia selezione di specialisti del massaggio professionale. Che tu stia cercando un massaggio rilassante, sportivo o terapeutico, Nevumo ti aiuta a trovare professionisti fidati nelle vicinanze.",
        "category.seo_massage_p2": "Controlla le recensioni dei clienti precedenti, l'esperienza dello specialista e la gamma di servizi offerti. Un buon specialista del massaggio saprà adattare la tecnica alle tue esigenze.",
        "category.seo_massage_p3": "Massoterapia professionale per alleviare lo stress e migliorare il tuo benessere. Prenota una seduta con terapisti esperti nella tua città.",
        "category.seo_plumbing_h3_1": "Quando chiamare un idraulico?",
        "category.seo_plumbing_h3_2": "Quanto costa un idraulico a {city}?",
        "category.seo_plumbing_p2": "Chiama un idraulico per guasti al sistema idrico, rubinetti che perdono, scarichi intasati e durante le ristrutturazioni di bagni o cucine.",
        "category.seo_plumbing_p3": "Soluzioni idrauliche esperte per ogni emergenza o riparazione pianificata. Risposta rapida e qualità garantita da specialisti idraulici locali."
    },
    "lb": {
        "category.seo_massage_h3_1": "Wéi wielt een e Massagespezialist?",
        "category.seo_massage_h3_2": "Wat kascht eng Massage an {city}?",
        "category.seo_massage_p1": "{city} bitt eng grouss Auswiel u professionelle Massagespezialisten un. Egal ob Dir eng entspannend, Sport- oder therapeutesch Massage sicht, Nevumo hëlleft Iech vertrauenswürdeg Profien an Ärer Géigend ze fannen.",
        "category.seo_massage_p2": "Iwwerpréift d'Bewäertunge vu fréiere Clienten, d'Erfahrung vum Spezialist an den Ëmfang vun de ugebuedene Servicer. E gudde Massagespezialist passt d'Technik un Är Bedierfnesser un.",
        "category.seo_massage_p3": "Professionell Massagetherapie fir Stress ofzebauen an Äert Wuelbefannen ze verbesseren. Reservéiert eng Sitzung bei erfuerenen Therapeuten an Ärer Stad.",
        "category.seo_plumbing_h3_1": "Wéini soll een e Klempner ruffen?",
        "category.seo_plumbing_h3_2": "Wat kascht e Klempner an {city}?",
        "category.seo_plumbing_p2": "Rufft e Klempner bei Ausfäll vum Waassersystem, tropfende Kranen, verstoppten Offloss an bei Buedzëmmer- oder Kichenrenovatiounen.",
        "category.seo_plumbing_p3": "Experteléisunge fir Sanitär bei all Noutfall oder geplangter Reparatur. Schnell Reaktioun a garantéiert Qualitéit vu lokale Spezialisten."
    },
    "lt": {
        "category.seo_massage_h3_1": "Kaip išsirinkti masažo specialistą?",
        "category.seo_massage_h3_2": "Kiek kainuoja masažas {city}?",
        "category.seo_massage_p1": "{city} siūlo platų profesionalių masažo specialistų pasirinkimą. Nesvarbu, ar ieškote atpalaiduojančio, sportinio ar terapinio masažo, \"Nevumo\" padės rasti patikimus specialistus netoliese.",
        "category.seo_massage_p2": "Peržiūrėkite ankstesnių klientų atsiliepimus, specialisto patirtį ir siūlomų paslaugų spektrą. Geras masažo specialistas pritaikys techniką pagal jūsų poreikius.",
        "category.seo_massage_p3": "Profesionali masažo terapija stresui malšinti ir savijautai gerinti. Užsisakykite seansą pas patyrusius terapeutus savo mieste.",
        "category.seo_plumbing_h2": "Santechnika {city} — ką verta žinoti?",
        "category.seo_plumbing_h3_1": "Kada kviesti santechniką?",
        "category.seo_plumbing_h3_2": "Kiek kainuoja santechnikas {city}?",
        "category.seo_plumbing_p2": "Kvieskite santechniką įvykus vandentiekio sistemos gedimams, varvant čiaupams, užsikimšus nuotakams bei atliekant vonios ar virtuvės remontą.",
        "category.seo_plumbing_p3": "Ekspertiniai santechnikos sprendimai bet kokiu skubiu atveju ar planuotam remontui. Greitas reagavimas ir garantuota vietinių specialistų kokybė."
    }
}

def main():
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()

def run_seed(db):
    print("Starting Phase 3B Part 1 SEO keys seed...")
    
    total_inserted = 0
    for lang, translations in PHASE3B_PART1_TRANSLATIONS.items():
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
    print(f"\n✓ Inserted/updated {total_inserted} translation rows for {len(PHASE3B_PART1_TRANSLATIONS)} languages")
    
    # Verify
    verify(db)

def verify(db):
    print("\n--- Verification ---")
    
    # Check massage keys for the 15 languages
    massage_result = db.execute(text("""
        SELECT lang, COUNT(*) as keys
        FROM translations
        WHERE key LIKE 'category.seo_massage%'
        AND lang IN ('cs', 'da', 'de', 'el', 'es', 'et', 'fi', 'fr', 'ga', 'hr', 'hu', 'is', 'it', 'lb', 'lt')
        GROUP BY lang
        ORDER BY lang
    """)).fetchall()
    print(f"\nSEO Massage Keys Verification:")
    for row in massage_result:
        print(f"  {row[0]}: {row[1]} keys")
    
    # Check plumbing keys for the 15 languages
    plumbing_result = db.execute(text("""
        SELECT lang, COUNT(*) as keys
        FROM translations
        WHERE key LIKE 'category.seo_plumbing%'
        AND lang IN ('cs', 'da', 'de', 'el', 'es', 'et', 'fi', 'fr', 'ga', 'hr', 'hu', 'is', 'it', 'lb', 'lt')
        GROUP BY lang
        ORDER BY lang
    """)).fetchall()
    print(f"\nSEO Plumbing Keys Verification:")
    for row in plumbing_result:
        print(f"  {row[0]}: {row[1]} keys")

if __name__ == "__main__":
    main()
