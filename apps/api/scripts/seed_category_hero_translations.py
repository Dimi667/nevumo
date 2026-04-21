from sqlalchemy import text
from database import SessionLocal
import subprocess

HERO_TRANSLATIONS = [
    # ─── bg ───
    {"lang": "bg", "key": "category.hero_title", "value": "Намери услуга в {city}"},
    {"lang": "bg", "key": "category.hero_subtitle_0", "value": "Получи оферти от местни специалисти безплатно! Изпрати заявка сега и ние ще те свържем с най-подходящия изпълнител възможно най-бързо."},
    {"lang": "bg", "key": "category.hero_subtitle_few", "value": "Получи оферти от проверени местни специалисти безплатно! Изпрати заявка и получи отговор в рамките на 30 минути."},
    {"lang": "bg", "key": "category.hero_subtitle_active", "value": "Получи оферти от специалисти в града безплатно! Изпрати заявка и получи отговор в рамките на 30 минути."},
    {"lang": "bg", "key": "category.hero_trust_0", "value": "Безплатно • Без ангажимент • Бърз отговор"},
    {"lang": "bg", "key": "category.hero_trust_few", "value": "Проверени специалисти • Без комисионна • Лично проследяване"},
    {"lang": "bg", "key": "category.hero_trust_requests", "value": "{count} обработени заявки • Проверени специалисти • Без комисионна"},
    {"lang": "bg", "key": "category.hero_trust_full", "value": "⭐ {rating} средна оценка • {count} обработени заявки • Без комисионна"},
    {"lang": "bg", "key": "category.hero_cta", "value": "Получи оферти безплатно сега"},
    {"lang": "bg", "key": "category.hero_cta_sub", "value": "Отнема само 60 секунди"},

    # ─── cs ───
    {"lang": "cs", "key": "category.hero_title", "value": "Najdi službu v {city}"},
    {"lang": "cs", "key": "category.hero_subtitle_0", "value": "Získej nabídky od místních specialistů zdarma! Pošli žádost teď a my tě spojíme s nejlepším poskytovatelem co nejrychleji."},
    {"lang": "cs", "key": "category.hero_subtitle_few", "value": "Získej nabídky od ověřených místních specialistů zdarma! Pošli žádost a získej odpověď do 30 minut."},
    {"lang": "cs", "key": "category.hero_subtitle_active", "value": "Získej nabídky od specialistů ve městě zdarma! Pošli žádost a získej odpověď do 30 minut."},
    {"lang": "cs", "key": "category.hero_trust_0", "value": "Zdarma • Bez závazku • Rychlá odpověď"},
    {"lang": "cs", "key": "category.hero_trust_few", "value": "Ověření specialisté • Bez provize • Osobní sledování"},
    {"lang": "cs", "key": "category.hero_trust_requests", "value": "{count} zpracovaných žádostí • Ověření specialisté • Bez provize"},
    {"lang": "cs", "key": "category.hero_trust_full", "value": "⭐ {rating} průměrné hodnocení • {count} zpracovaných žádostí • Bez provize"},
    {"lang": "cs", "key": "category.hero_cta", "value": "Získej nabídky zdarma teď"},
    {"lang": "cs", "key": "category.hero_cta_sub", "value": "Trvá jen 60 sekund"},

    # ─── da ───
    {"lang": "da", "key": "category.hero_title", "value": "Find en tjeneste i {city}"},
    {"lang": "da", "key": "category.hero_subtitle_0", "value": "Få tilbud fra lokale specialister gratis! Send en forespørgsel nu, og vi forbinder dig med den mest egnede udbyder så hurtigt som muligt."},
    {"lang": "da", "key": "category.hero_subtitle_few", "value": "Få tilbud fra verificerede lokale specialister gratis! Send en forespørgsel og få svar inden for 30 minutter."},
    {"lang": "da", "key": "category.hero_subtitle_active", "value": "Få tilbud fra specialister i byen gratis! Send en forespørgsel og få svar inden for 30 minutter."},
    {"lang": "da", "key": "category.hero_trust_0", "value": "Gratis • Ingen forpligtelse • Hurtigt svar"},
    {"lang": "da", "key": "category.hero_trust_few", "value": "Verificerede specialister • Ingen provision • Personlig opfølgning"},
    {"lang": "da", "key": "category.hero_trust_requests", "value": "{count} behandlede forespørgsler • Verificerede specialister • Ingen provision"},
    {"lang": "da", "key": "category.hero_trust_full", "value": "⭐ {rating} gennemsnitlig vurdering • {count} behandlede forespørgsler • Ingen provision"},
    {"lang": "da", "key": "category.hero_cta", "value": "Få gratis tilbud nu"},
    {"lang": "da", "key": "category.hero_cta_sub", "value": "Det tager kun 60 sekunder"},

    # ─── de ───
    {"lang": "de", "key": "category.hero_title", "value": "Finde einen Service in {city}"},
    {"lang": "de", "key": "category.hero_subtitle_0", "value": "Erhalte kostenlos Angebote von lokalen Spezialisten! Sende jetzt eine Anfrage und wir verbinden dich so schnell wie möglich mit dem geeignetsten Anbieter."},
    {"lang": "de", "key": "category.hero_subtitle_few", "value": "Erhalte kostenlos Angebote von verifizierten lokalen Spezialisten! Sende eine Anfrage und erhalte eine Antwort innerhalb von 30 Minuten."},
    {"lang": "de", "key": "category.hero_subtitle_active", "value": "Erhalte kostenlos Angebote von Spezialisten in der Stadt! Sende eine Anfrage und erhalte eine Antwort innerhalb von 30 Minuten."},
    {"lang": "de", "key": "category.hero_trust_0", "value": "Kostenlos • Keine Verpflichtung • Schnelle Antwort"},
    {"lang": "de", "key": "category.hero_trust_few", "value": "Verifizierte Spezialisten • Ohne Provision • Persönliche Betreuung"},
    {"lang": "de", "key": "category.hero_trust_requests", "value": "{count} bearbeitete Anfragen • Verifizierte Spezialisten • Ohne Provision"},
    {"lang": "de", "key": "category.hero_trust_full", "value": "⭐ {rating} Durchschnittsbewertung • {count} bearbeitete Anfragen • Ohne Provision"},
    {"lang": "de", "key": "category.hero_cta", "value": "Jetzt kostenlos Angebote erhalten"},
    {"lang": "de", "key": "category.hero_cta_sub", "value": "Dauert nur 60 Sekunden"},

    # ─── el ───
    {"lang": "el", "key": "category.hero_title", "value": "Βρες υπηρεσία στη/στο {city}"},
    {"lang": "el", "key": "category.hero_subtitle_0", "value": "Λάβε προσφορές από τοπικούς ειδικούς δωρεάν! Στείλε αίτημα τώρα και θα σε συνδέσουμε με τον πιο κατάλληλο πάροχο το συντομότερο δυνατό."},
    {"lang": "el", "key": "category.hero_subtitle_few", "value": "Λάβε προσφορές από επαληθευμένους τοπικούς ειδικούς δωρεάν! Στείλε αίτημα και λάβε απάντηση εντός 30 λεπτών."},
    {"lang": "el", "key": "category.hero_subtitle_active", "value": "Λάβε προσφορές από ειδικούς στην πόλη δωρεάν! Στείλε αίτημα και λάβε απάντηση εντός 30 λεπτών."},
    {"lang": "el", "key": "category.hero_trust_0", "value": "Δωρεάν • Χωρίς δέσμευση • Γρήγορη απάντηση"},
    {"lang": "el", "key": "category.hero_trust_few", "value": "Επαληθευμένοι ειδικοί • Χωρίς προμήθεια • Προσωπική παρακολούθηση"},
    {"lang": "el", "key": "category.hero_trust_requests", "value": "{count} επεξεργασμένα αιτήματα • Επαληθευμένοι ειδικοί • Χωρίς προμήθεια"},
    {"lang": "el", "key": "category.hero_trust_full", "value": "⭐ {rating} μέση βαθμολογία • {count} επεξεργασμένα αιτήματα • Χωρίς προμήθεια"},
    {"lang": "el", "key": "category.hero_cta", "value": "Λάβε δωρεάν προσφορές τώρα"},
    {"lang": "el", "key": "category.hero_cta_sub", "value": "Διαρκεί μόνο 60 δευτερόλεπτα"},

    # ─── en ───
    {"lang": "en", "key": "category.hero_title", "value": "Find a service in {city}"},
    {"lang": "en", "key": "category.hero_subtitle_0", "value": "Get offers from local specialists for free! Submit a request now and we'll connect you with the most suitable provider as quickly as possible."},
    {"lang": "en", "key": "category.hero_subtitle_few", "value": "Get offers from verified local specialists for free! Submit a request and get a response within 30 minutes."},
    {"lang": "en", "key": "category.hero_subtitle_active", "value": "Get offers from specialists in the city for free! Submit a request and get a response within 30 minutes."},
    {"lang": "en", "key": "category.hero_trust_0", "value": "Free • No obligation • Quick response"},
    {"lang": "en", "key": "category.hero_trust_few", "value": "Verified specialists • No commission • Personal follow-up"},
    {"lang": "en", "key": "category.hero_trust_requests", "value": "{count} processed requests • Verified specialists • No commission"},
    {"lang": "en", "key": "category.hero_trust_full", "value": "⭐ {rating} average rating • {count} processed requests • No commission"},
    {"lang": "en", "key": "category.hero_cta", "value": "Get free offers now"},
    {"lang": "en", "key": "category.hero_cta_sub", "value": "Takes only 60 seconds"},

    # ─── es ───
    {"lang": "es", "key": "category.hero_title", "value": "Encuentra un servicio en {city}"},
    {"lang": "es", "key": "category.hero_subtitle_0", "value": "¡Recibe ofertas de especialistas locales gratis! Envía una solicitud ahora y te conectaremos con el proveedor más adecuado lo antes posible."},
    {"lang": "es", "key": "category.hero_subtitle_few", "value": "¡Recibe ofertas de especialistas locales verificados gratis! Envía una solicitud y recibe respuesta en 30 minutos."},
    {"lang": "es", "key": "category.hero_subtitle_active", "value": "¡Recibe ofertas de especialistas de la ciudad gratis! Envía una solicitud y recibe respuesta en 30 minutos."},
    {"lang": "es", "key": "category.hero_trust_0", "value": "Gratis • Sin compromiso • Respuesta rápida"},
    {"lang": "es", "key": "category.hero_trust_few", "value": "Especialistas verificados • Sin comisión • Seguimiento personal"},
    {"lang": "es", "key": "category.hero_trust_requests", "value": "{count} solicitudes procesadas • Especialistas verificados • Sin comisión"},
    {"lang": "es", "key": "category.hero_trust_full", "value": "⭐ {rating} valoración media • {count} solicitudes procesadas • Sin comisión"},
    {"lang": "es", "key": "category.hero_cta", "value": "Recibe ofertas gratis ahora"},
    {"lang": "es", "key": "category.hero_cta_sub", "value": "Solo tarda 60 segundos"},

    # ─── et ───
    {"lang": "et", "key": "category.hero_title", "value": "Leia teenus linnas {city}"},
    {"lang": "et", "key": "category.hero_subtitle_0", "value": "Saa kohalikelt spetsialistidelt pakkumisi tasuta! Saada päring kohe ja me ühendame sind sobivama teenusepakkujaga nii kiiresti kui võimalik."},
    {"lang": "et", "key": "category.hero_subtitle_few", "value": "Saa kinnitatud kohalikult spetsialistidelt pakkumisi tasuta! Saada päring ja saa vastus 30 minuti jooksul."},
    {"lang": "et", "key": "category.hero_subtitle_active", "value": "Saa linna spetsialistidelt pakkumisi tasuta! Saada päring ja saa vastus 30 minuti jooksul."},
    {"lang": "et", "key": "category.hero_trust_0", "value": "Tasuta • Kohustuseta • Kiire vastus"},
    {"lang": "et", "key": "category.hero_trust_few", "value": "Kinnitatud spetsialistid • Ilma komisjonitasuta • Isiklik jälgimine"},
    {"lang": "et", "key": "category.hero_trust_requests", "value": "{count} töödeldud päringut • Kinnitatud spetsialistid • Ilma komisjonitasuta"},
    {"lang": "et", "key": "category.hero_trust_full", "value": "⭐ {rating} keskmine hinnang • {count} töödeldud päringut • Ilma komisjonitasuta"},
    {"lang": "et", "key": "category.hero_cta", "value": "Saa tasuta pakkumisi kohe"},
    {"lang": "et", "key": "category.hero_cta_sub", "value": "Võtab ainult 60 sekundit"},

    # ─── fi ───
    {"lang": "fi", "key": "category.hero_title", "value": "Löydä palvelu kaupungista {city}"},
    {"lang": "fi", "key": "category.hero_subtitle_0", "value": "Saa tarjouksia paikallisilta asiantuntijoilta ilmaiseksi! Lähetä pyyntö nyt ja yhdistämme sinut sopivimpaan palveluntarjoajaan mahdollisimman nopeasti."},
    {"lang": "fi", "key": "category.hero_subtitle_few", "value": "Saa tarjouksia vahvistetuilta paikallisilta asiantuntijoilta ilmaiseksi! Lähetä pyyntö ja saa vastaus 30 minuutin sisällä."},
    {"lang": "fi", "key": "category.hero_subtitle_active", "value": "Saa tarjouksia kaupungin asiantuntijoilta ilmaiseksi! Lähetä pyyntö ja saa vastaus 30 minuutin sisällä."},
    {"lang": "fi", "key": "category.hero_trust_0", "value": "Ilmainen • Ei sitoumusta • Nopea vastaus"},
    {"lang": "fi", "key": "category.hero_trust_few", "value": "Vahvistetut asiantuntijat • Ei provisioita • Henkilökohtainen seuranta"},
    {"lang": "fi", "key": "category.hero_trust_requests", "value": "{count} käsiteltyä pyyntöä • Vahvistetut asiantuntijat • Ei provisioita"},
    {"lang": "fi", "key": "category.hero_trust_full", "value": "⭐ {rating} keskimääräinen arvio • {count} käsiteltyä pyyntöä • Ei provisioita"},
    {"lang": "fi", "key": "category.hero_cta", "value": "Saa ilmaisia tarjouksia nyt"},
    {"lang": "fi", "key": "category.hero_cta_sub", "value": "Kestää vain 60 sekuntia"},

    # ─── fr ───
    {"lang": "fr", "key": "category.hero_title", "value": "Trouvez un service à {city}"},
    {"lang": "fr", "key": "category.hero_subtitle_0", "value": "Recevez des offres de spécialistes locaux gratuitement ! Envoyez une demande maintenant et nous vous mettrons en contact avec le prestataire le plus adapté aussi vite que possible."},
    {"lang": "fr", "key": "category.hero_subtitle_few", "value": "Recevez des offres de spécialistes locaux vérifiés gratuitement ! Envoyez une demande et recevez une réponse dans les 30 minutes."},
    {"lang": "fr", "key": "category.hero_subtitle_active", "value": "Recevez des offres de spécialistes de la ville gratuitement ! Envoyez une demande et recevez une réponse dans les 30 minutes."},
    {"lang": "fr", "key": "category.hero_trust_0", "value": "Gratuit • Sans engagement • Réponse rapide"},
    {"lang": "fr", "key": "category.hero_trust_few", "value": "Spécialistes vérifiés • Sans commission • Suivi personnalisé"},
    {"lang": "fr", "key": "category.hero_trust_requests", "value": "{count} demandes traitées • Spécialistes vérifiés • Sans commission"},
    {"lang": "fr", "key": "category.hero_trust_full", "value": "⭐ {rating} note moyenne • {count} demandes traitées • Sans commission"},
    {"lang": "fr", "key": "category.hero_cta", "value": "Recevez des offres gratuites maintenant"},
    {"lang": "fr", "key": "category.hero_cta_sub", "value": "Prend seulement 60 secondes"},

    # ─── ga ───
    {"lang": "ga", "key": "category.hero_title", "value": "Faigh seirbhís i {city}"},
    {"lang": "ga", "key": "category.hero_subtitle_0", "value": "Faigh tairiscintí ó speisialtóirí áitiúla saor in aisce! Cuir iarratas isteach anois agus cuirfimid i dteagmháil thú leis an soláthraí is oiriúnaí chomh luath agus is féidir."},
    {"lang": "ga", "key": "category.hero_subtitle_few", "value": "Faigh tairiscintí ó speisialtóirí áitiúla fíoraithe saor in aisce! Cuir iarratas isteach agus faigh freagra laistigh de 30 nóiméad."},
    {"lang": "ga", "key": "category.hero_subtitle_active", "value": "Faigh tairiscintí ó speisialtóirí sa chathair saor in aisce! Cuir iarratas isteach agus faigh freagra laistigh de 30 nóiméad."},
    {"lang": "ga", "key": "category.hero_trust_0", "value": "Saor in aisce • Gan oibleagáid • Freagra tapa"},
    {"lang": "ga", "key": "category.hero_trust_few", "value": "Speisialtóirí fíoraithe • Gan coimisiún • Leanúint phearsanta"},
    {"lang": "ga", "key": "category.hero_trust_requests", "value": "{count} iarratas próiseáilte • Speisialtóirí fíoraithe • Gan coimisiún"},
    {"lang": "ga", "key": "category.hero_trust_full", "value": "⭐ {rating} rátáil meán • {count} iarratas próiseáilte • Gan coimisiún"},
    {"lang": "ga", "key": "category.hero_cta", "value": "Faigh tairiscintí saor in aisce anois"},
    {"lang": "ga", "key": "category.hero_cta_sub", "value": "Níl ach 60 soicind i gceist"},

    # ─── hr ───
    {"lang": "hr", "key": "category.hero_title", "value": "Pronađi uslugu u {city}"},
    {"lang": "hr", "key": "category.hero_subtitle_0", "value": "Dobij ponude od lokalnih stručnjaka besplatno! Pošalji zahtjev sada i povezat ćemo te s najprikladnijim pružateljem što je brže moguće."},
    {"lang": "hr", "key": "category.hero_subtitle_few", "value": "Dobij ponude od verificiranih lokalnih stručnjaka besplatno! Pošalji zahtjev i dobij odgovor u roku od 30 minuta."},
    {"lang": "hr", "key": "category.hero_subtitle_active", "value": "Dobij ponude od stručnjaka u gradu besplatno! Pošalji zahtjev i dobij odgovor u roku od 30 minuta."},
    {"lang": "hr", "key": "category.hero_trust_0", "value": "Besplatno • Bez obveze • Brz odgovor"},
    {"lang": "hr", "key": "category.hero_trust_few", "value": "Verificirani stručnjaci • Bez provizije • Osobno praćenje"},
    {"lang": "hr", "key": "category.hero_trust_requests", "value": "{count} obrađenih zahtjeva • Verificirani stručnjaci • Bez provizije"},
    {"lang": "hr", "key": "category.hero_trust_full", "value": "⭐ {rating} prosječna ocjena • {count} obrađenih zahtjeva • Bez provizije"},
    {"lang": "hr", "key": "category.hero_cta", "value": "Dobij besplatne ponude sada"},
    {"lang": "hr", "key": "category.hero_cta_sub", "value": "Traje samo 60 sekundi"},

    # ─── hu ───
    {"lang": "hu", "key": "category.hero_title", "value": "Találj szolgáltatást {city} városban"},
    {"lang": "hu", "key": "category.hero_subtitle_0", "value": "Kapj ajánlatokat helyi szakemberektől ingyen! Küldj kérelmet most, és összekötünk a legmegfelelőbb szolgáltatóval a lehető leghamarabb."},
    {"lang": "hu", "key": "category.hero_subtitle_few", "value": "Kapj ajánlatokat ellenőrzött helyi szakemberektől ingyen! Küldj kérelmet és kapj választ 30 percen belül."},
    {"lang": "hu", "key": "category.hero_subtitle_active", "value": "Kapj ajánlatokat a városban dolgozó szakemberektől ingyen! Küldj kérelmet és kapj választ 30 percen belül."},
    {"lang": "hu", "key": "category.hero_trust_0", "value": "Ingyenes • Kötelezettség nélkül • Gyors válasz"},
    {"lang": "hu", "key": "category.hero_trust_few", "value": "Ellenőrzött szakemberek • Jutalék nélkül • Személyes nyomon követés"},
    {"lang": "hu", "key": "category.hero_trust_requests", "value": "{count} feldolgozott kérelem • Ellenőrzött szakemberek • Jutalék nélkül"},
    {"lang": "hu", "key": "category.hero_trust_full", "value": "⭐ {rating} átlagos értékelés • {count} feldolgozott kérelem • Jutalék nélkül"},
    {"lang": "hu", "key": "category.hero_cta", "value": "Kapj ingyenes ajánlatokat most"},
    {"lang": "hu", "key": "category.hero_cta_sub", "value": "Csak 60 másodpercet vesz igénybe"},

    # ─── is ───
    {"lang": "is", "key": "category.hero_title", "value": "Finndu þjónustu í {city}"},
    {"lang": "is", "key": "category.hero_subtitle_0", "value": "Fáðu tilboð frá staðbundnum sérfræðingum ókeypis! Sendu beiðni núna og við tengjum þig við hentugasta þjónustuveitandann eins fljótt og auðið er."},
    {"lang": "is", "key": "category.hero_subtitle_few", "value": "Fáðu tilboð frá staðfestum staðbundnum sérfræðingum ókeypis! Sendu beiðni og fáðu svar innan 30 mínútna."},
    {"lang": "is", "key": "category.hero_subtitle_active", "value": "Fáðu tilboð frá sérfræðingum í borginni ókeypis! Sendu beiðni og fáðu svar innan 30 mínútna."},
    {"lang": "is", "key": "category.hero_trust_0", "value": "Ókeypis • Engar skuldbindingar • Skjót svör"},
    {"lang": "is", "key": "category.hero_trust_few", "value": "Staðfestir sérfræðingar • Engin þóknun • Persónuleg fylgd"},
    {"lang": "is", "key": "category.hero_trust_requests", "value": "{count} afgreiddar beiðnir • Staðfestir sérfræðingar • Engin þóknun"},
    {"lang": "is", "key": "category.hero_trust_full", "value": "⭐ {rating} meðaleinkunn • {count} afgreiddar beiðnir • Engin þóknun"},
    {"lang": "is", "key": "category.hero_cta", "value": "Fáðu ókeypis tilboð núna"},
    {"lang": "is", "key": "category.hero_cta_sub", "value": "Tekur aðeins 60 sekúndur"},

    # ─── it ───
    {"lang": "it", "key": "category.hero_title", "value": "Trova un servizio a {city}"},
    {"lang": "it", "key": "category.hero_subtitle_0", "value": "Ricevi offerte da specialisti locali gratuitamente! Invia una richiesta ora e ti metteremo in contatto con il fornitore più adatto nel più breve tempo possibile."},
    {"lang": "it", "key": "category.hero_subtitle_few", "value": "Ricevi offerte da specialisti locali verificati gratuitamente! Invia una richiesta e ricevi una risposta entro 30 minuti."},
    {"lang": "it", "key": "category.hero_subtitle_active", "value": "Ricevi offerte da specialisti della città gratuitamente! Invia una richiesta e ricevi una risposta entro 30 minuti."},
    {"lang": "it", "key": "category.hero_trust_0", "value": "Gratuito • Senza impegno • Risposta rapida"},
    {"lang": "it", "key": "category.hero_trust_few", "value": "Specialisti verificati • Senza commissioni • Monitoraggio personale"},
    {"lang": "it", "key": "category.hero_trust_requests", "value": "{count} richieste elaborate • Specialisti verificati • Senza commissioni"},
    {"lang": "it", "key": "category.hero_trust_full", "value": "⭐ {rating} valutazione media • {count} richieste elaborate • Senza commissioni"},
    {"lang": "it", "key": "category.hero_cta", "value": "Ricevi offerte gratuite ora"},
    {"lang": "it", "key": "category.hero_cta_sub", "value": "Richiede solo 60 secondi"},

    # ─── lb ───
    {"lang": "lb", "key": "category.hero_title", "value": "Fann e Service zu {city}"},
    {"lang": "lb", "key": "category.hero_subtitle_0", "value": "Kritt Offere vu lokale Spezialiste gratis! Schéckt elo eng Ufro a mir verbannen Iech mam passendste Prestataire sou séier wéi méiglech."},
    {"lang": "lb", "key": "category.hero_subtitle_few", "value": "Kritt Offere vu verifiéierte lokale Spezialiste gratis! Schéckt eng Ufro a kritt eng Äntwert bannent 30 Minutten."},
    {"lang": "lb", "key": "category.hero_subtitle_active", "value": "Kritt Offere vu Spezialiste vun der Stad gratis! Schéckt eng Ufro a kritt eng Äntwert bannent 30 Minutten."},
    {"lang": "lb", "key": "category.hero_trust_0", "value": "Gratis • Ouni Engagement • Séier Äntwert"},
    {"lang": "lb", "key": "category.hero_trust_few", "value": "Verifiéiert Spezialisten • Ouni Kommissioun • Perséinlecht Follow-up"},
    {"lang": "lb", "key": "category.hero_trust_requests", "value": "{count} behandelt Ufroen • Verifiéiert Spezialisten • Ouni Kommissioun"},
    {"lang": "lb", "key": "category.hero_trust_full", "value": "⭐ {rating} Duerchschnëttsbewäertung • {count} behandelt Ufroen • Ouni Kommissioun"},
    {"lang": "lb", "key": "category.hero_cta", "value": "Kritt gratis Offeren elo"},
    {"lang": "lb", "key": "category.hero_cta_sub", "value": "Dauert just 60 Sekonnen"},

    # ─── lt ───
    {"lang": "lt", "key": "category.hero_title", "value": "Rask paslaugą {city} mieste"},
    {"lang": "lt", "key": "category.hero_subtitle_0", "value": "Gauk pasiūlymus iš vietinių specialistų nemokamai! Pateik užklausą dabar ir susiesime tave su tinkamiausiu tiekėju kuo greičiau."},
    {"lang": "lt", "key": "category.hero_subtitle_few", "value": "Gauk pasiūlymus iš patikrintų vietinių specialistų nemokamai! Pateik užklausą ir gauk atsakymą per 30 minučių."},
    {"lang": "lt", "key": "category.hero_subtitle_active", "value": "Gauk pasiūlymus iš miesto specialistų nemokamai! Pateik užklausą ir gauk atsakymą per 30 minučių."},
    {"lang": "lt", "key": "category.hero_trust_0", "value": "Nemokama • Be įsipareigojimų • Greitas atsakymas"},
    {"lang": "lt", "key": "category.hero_trust_few", "value": "Patikrinti specialistai • Be komisinių • Asmeninis sekimas"},
    {"lang": "lt", "key": "category.hero_trust_requests", "value": "{count} apdorotų užklausų • Patikrinti specialistai • Be komisinių"},
    {"lang": "lt", "key": "category.hero_trust_full", "value": "⭐ {rating} vidutinis įvertinimas • {count} apdorotų užklausų • Be komisinių"},
    {"lang": "lt", "key": "category.hero_cta", "value": "Gauk nemokamų pasiūlymų dabar"},
    {"lang": "lt", "key": "category.hero_cta_sub", "value": "Užtrunka tik 60 sekundžių"},

    # ─── lv ───
    {"lang": "lv", "key": "category.hero_title", "value": "Atrodi pakalpojumu {city} pilsētā"},
    {"lang": "lv", "key": "category.hero_subtitle_0", "value": "Saņem piedāvājumus no vietējiem speciālistiem bez maksas! Iesniedziet pieprasījumu tagad un mēs jūs savienosim ar vispiemērotāko pakalpojumu sniedzēju pēc iespējas ātrāk."},
    {"lang": "lv", "key": "category.hero_subtitle_few", "value": "Saņem piedāvājumus no verificētiem vietējiem speciālistiem bez maksas! Iesniedziet pieprasījumu un saņemiet atbildi 30 minūšu laikā."},
    {"lang": "lv", "key": "category.hero_subtitle_active", "value": "Saņem piedāvājumus no pilsētas speciālistiem bez maksas! Iesniedziet pieprasījumu un saņemiet atbildi 30 minūšu laikā."},
    {"lang": "lv", "key": "category.hero_trust_0", "value": "Bez maksas • Bez saistībām • Ātra atbilde"},
    {"lang": "lv", "key": "category.hero_trust_few", "value": "Verificēti speciālisti • Bez komisijas • Personīga uzraudzība"},
    {"lang": "lv", "key": "category.hero_trust_requests", "value": "{count} apstrādāti pieprasījumi • Verificēti speciālisti • Bez komisijas"},
    {"lang": "lv", "key": "category.hero_trust_full", "value": "⭐ {rating} vidējais vērtējums • {count} apstrādāti pieprasījumi • Bez komisijas"},
    {"lang": "lv", "key": "category.hero_cta", "value": "Saņem bezmaksas piedāvājumus tagad"},
    {"lang": "lv", "key": "category.hero_cta_sub", "value": "Aizņem tikai 60 sekundes"},

    # ─── mk ───
    {"lang": "mk", "key": "category.hero_title", "value": "Најди услуга во {city}"},
    {"lang": "mk", "key": "category.hero_subtitle_0", "value": "Добиј понуди од локални специјалисти бесплатно! Испрати барање сега и ние ќе те поврземе со најсоодветниот извршител што е можно побрзо."},
    {"lang": "mk", "key": "category.hero_subtitle_few", "value": "Добиј понуди од верификувани локални специјалисти бесплатно! Испрати барање и добиј одговор во рок од 30 минути."},
    {"lang": "mk", "key": "category.hero_subtitle_active", "value": "Добиј понуди од специјалисти во градот бесплатно! Испрати барање и добиј одговор во рок од 30 минути."},
    {"lang": "mk", "key": "category.hero_trust_0", "value": "Бесплатно • Без обврска • Брз одговор"},
    {"lang": "mk", "key": "category.hero_trust_few", "value": "Верификувани специјалисти • Без провизија • Лично следење"},
    {"lang": "mk", "key": "category.hero_trust_requests", "value": "{count} обработени барања • Верификувани специјалисти • Без провизија"},
    {"lang": "mk", "key": "category.hero_trust_full", "value": "⭐ {rating} просечна оценка • {count} обработени барања • Без провизија"},
    {"lang": "mk", "key": "category.hero_cta", "value": "Добиј бесплатни понуди сега"},
    {"lang": "mk", "key": "category.hero_cta_sub", "value": "Одзема само 60 секунди"},

    # ─── mt ───
    {"lang": "mt", "key": "category.hero_title", "value": "Sib servizz f'{city}"},
    {"lang": "mt", "key": "category.hero_subtitle_0", "value": "Irċievi offerti minn speċjalisti lokali b'xejn! Ibgħat talba issa u aħna ngħaqqduك mal-fornitur l-aktar xieraq malajr kemm jista' jkun."},
    {"lang": "mt", "key": "category.hero_subtitle_few", "value": "Irċievi offerti minn speċjalisti lokali vverifikati b'xejn! Ibgħat talba u irċievi risposta fi 30 minuta."},
    {"lang": "mt", "key": "category.hero_subtitle_active", "value": "Irċievi offerti minn speċjalisti tal-belt b'xejn! Ibgħat talba u irċievi risposta fi 30 minuta."},
    {"lang": "mt", "key": "category.hero_trust_0", "value": "B'xejn • Mingħajr obbligu • Risposta rapida"},
    {"lang": "mt", "key": "category.hero_trust_few", "value": "Speċjalisti vverifikati • Mingħajr kummissjoni • Segwitu personali"},
    {"lang": "mt", "key": "category.hero_trust_requests", "value": "{count} talbiet ipproċessati • Speċjalisti vverifikati • Mingħajr kummissjoni"},
    {"lang": "mt", "key": "category.hero_trust_full", "value": "⭐ {rating} klassifikazzjoni medja • {count} talbiet ipproċessati • Mingħajr kummissjoni"},
    {"lang": "mt", "key": "category.hero_cta", "value": "Irċievi offerti b'xejn issa"},
    {"lang": "mt", "key": "category.hero_cta_sub", "value": "Jieħu biss 60 sekonda"},

    # ─── nl ───
    {"lang": "nl", "key": "category.hero_title", "value": "Vind een dienst in {city}"},
    {"lang": "nl", "key": "category.hero_subtitle_0", "value": "Ontvang gratis offertes van lokale specialisten! Dien nu een aanvraag in en wij verbinden je zo snel mogelijk met de meest geschikte aanbieder."},
    {"lang": "nl", "key": "category.hero_subtitle_few", "value": "Ontvang gratis offertes van geverifieerde lokale specialisten! Dien een aanvraag in en ontvang binnen 30 minuten een reactie."},
    {"lang": "nl", "key": "category.hero_subtitle_active", "value": "Ontvang gratis offertes van specialisten in de stad! Dien een aanvraag in en ontvang binnen 30 minuten een reactie."},
    {"lang": "nl", "key": "category.hero_trust_0", "value": "Gratis • Geen verplichting • Snel antwoord"},
    {"lang": "nl", "key": "category.hero_trust_few", "value": "Geverifieerde specialisten • Geen commissie • Persoonlijke opvolging"},
    {"lang": "nl", "key": "category.hero_trust_requests", "value": "{count} verwerkte aanvragen • Geverifieerde specialisten • Geen commissie"},
    {"lang": "nl", "key": "category.hero_trust_full", "value": "⭐ {rating} gemiddelde beoordeling • {count} verwerkte aanvragen • Geen commissie"},
    {"lang": "nl", "key": "category.hero_cta", "value": "Ontvang nu gratis offertes"},
    {"lang": "nl", "key": "category.hero_cta_sub", "value": "Duurt slechts 60 seconden"},

    # ─── no ───
    {"lang": "no", "key": "category.hero_title", "value": "Finn en tjeneste i {city}"},
    {"lang": "no", "key": "category.hero_subtitle_0", "value": "Få tilbud fra lokale spesialister gratis! Send en forespørsel nå, og vi kobler deg med den mest egnede tilbyderen så raskt som mulig."},
    {"lang": "no", "key": "category.hero_subtitle_few", "value": "Få tilbud fra verifiserte lokale spesialister gratis! Send en forespørsel og få svar innen 30 minutter."},
    {"lang": "no", "key": "category.hero_subtitle_active", "value": "Få tilbud fra spesialister i byen gratis! Send en forespørsel og få svar innen 30 minutter."},
    {"lang": "no", "key": "category.hero_trust_0", "value": "Gratis • Ingen forpliktelse • Raskt svar"},
    {"lang": "no", "key": "category.hero_trust_few", "value": "Verifiserte spesialister • Ingen provisjon • Personlig oppfølging"},
    {"lang": "no", "key": "category.hero_trust_requests", "value": "{count} behandlede forespørsler • Verifiserte spesialister • Ingen provisjon"},
    {"lang": "no", "key": "category.hero_trust_full", "value": "⭐ {rating} gjennomsnittlig vurdering • {count} behandlede forespørsler • Ingen provisjon"},
    {"lang": "no", "key": "category.hero_cta", "value": "Få gratis tilbud nå"},
    {"lang": "no", "key": "category.hero_cta_sub", "value": "Tar bare 60 sekunder"},

    # ─── pl ───
    {"lang": "pl", "key": "category.hero_title", "value": "Znajdź usługę w {city}"},
    {"lang": "pl", "key": "category.hero_subtitle_0", "value": "Otrzymaj oferty od lokalnych specjalistów za darmo! Wyślij zapytanie teraz, a my połączymy Cię z najbardziej odpowiednim wykonawcą jak najszybciej."},
    {"lang": "pl", "key": "category.hero_subtitle_few", "value": "Otrzymaj oferty od zweryfikowanych lokalnych specjalistów za darmo! Wyślij zapytanie i otrzymaj odpowiedź w ciągu 30 minut."},
    {"lang": "pl", "key": "category.hero_subtitle_active", "value": "Otrzymaj oferty od specjalistów w mieście za darmo! Wyślij zapytanie i otrzymaj odpowiedź w ciągu 30 minut."},
    {"lang": "pl", "key": "category.hero_trust_0", "value": "Bezpłatnie • Bez zobowiązań • Szybka odpowiedź"},
    {"lang": "pl", "key": "category.hero_trust_few", "value": "Zweryfikowani specjaliści • Bez prowizji • Osobiste śledzenie"},
    {"lang": "pl", "key": "category.hero_trust_requests", "value": "{count} przetworzonych zapytań • Zweryfikowani specjaliści • Bez prowizji"},
    {"lang": "pl", "key": "category.hero_trust_full", "value": "⭐ {rating} średnia ocena • {count} przetworzonych zapytań • Bez prowizji"},
    {"lang": "pl", "key": "category.hero_cta", "value": "Otrzymaj bezpłatne oferty teraz"},
    {"lang": "pl", "key": "category.hero_cta_sub", "value": "Zajmuje tylko 60 sekund"},

    # ─── pt ───
    {"lang": "pt", "key": "category.hero_title", "value": "Encontre um serviço em {city}"},
    {"lang": "pt", "key": "category.hero_subtitle_0", "value": "Receba ofertas de especialistas locais gratuitamente! Envie uma solicitação agora e vamos conectá-lo ao provedor mais adequado o mais rápido possível."},
    {"lang": "pt", "key": "category.hero_subtitle_few", "value": "Receba ofertas de especialistas locais verificados gratuitamente! Envie uma solicitação e receba uma resposta em 30 minutos."},
    {"lang": "pt", "key": "category.hero_subtitle_active", "value": "Receba ofertas de especialistas da cidade gratuitamente! Envie uma solicitação e receba uma resposta em 30 minutos."},
    {"lang": "pt", "key": "category.hero_trust_0", "value": "Gratuito • Sem compromisso • Resposta rápida"},
    {"lang": "pt", "key": "category.hero_trust_few", "value": "Especialistas verificados • Sem comissão • Acompanhamento pessoal"},
    {"lang": "pt", "key": "category.hero_trust_requests", "value": "{count} solicitações processadas • Especialistas verificados • Sem comissão"},
    {"lang": "pt", "key": "category.hero_trust_full", "value": "⭐ {rating} avaliação média • {count} solicitações processadas • Sem comissão"},
    {"lang": "pt", "key": "category.hero_cta", "value": "Receba ofertas gratuitas agora"},
    {"lang": "pt", "key": "category.hero_cta_sub", "value": "Leva apenas 60 segundos"},

    # ─── pt-PT ───
    {"lang": "pt-PT", "key": "category.hero_title", "value": "Encontre um serviço em {city}"},
    {"lang": "pt-PT", "key": "category.hero_subtitle_0", "value": "Receba ofertas de especialistas locais gratuitamente! Envie um pedido agora e iremos ligá-lo ao prestador mais adequado o mais rapidamente possível."},
    {"lang": "pt-PT", "key": "category.hero_subtitle_few", "value": "Receba ofertas de especialistas locais verificados gratuitamente! Envie um pedido e receba uma resposta em 30 minutos."},
    {"lang": "pt-PT", "key": "category.hero_subtitle_active", "value": "Receba ofertas de especialistas da cidade gratuitamente! Envie um pedido e receba uma resposta em 30 minutos."},
    {"lang": "pt-PT", "key": "category.hero_trust_0", "value": "Gratuito • Sem compromisso • Resposta rápida"},
    {"lang": "pt-PT", "key": "category.hero_trust_few", "value": "Especialistas verificados • Sem comissão • Acompanhamento pessoal"},
    {"lang": "pt-PT", "key": "category.hero_trust_requests", "value": "{count} pedidos processados • Especialistas verificados • Sem comissão"},
    {"lang": "pt-PT", "key": "category.hero_trust_full", "value": "⭐ {rating} avaliação média • {count} pedidos processados • Sem comissão"},
    {"lang": "pt-PT", "key": "category.hero_cta", "value": "Receba ofertas gratuitas agora"},
    {"lang": "pt-PT", "key": "category.hero_cta_sub", "value": "Demora apenas 60 segundos"},

    # ─── ro ───
    {"lang": "ro", "key": "category.hero_title", "value": "Găsește un serviciu în {city}"},
    {"lang": "ro", "key": "category.hero_subtitle_0", "value": "Primește oferte de la specialiști locali gratuit! Trimite o cerere acum și te vom conecta cu cel mai potrivit furnizor cât mai repede posibil."},
    {"lang": "ro", "key": "category.hero_subtitle_few", "value": "Primește oferte de la specialiști locali verificați gratuit! Trimite o cerere și primești un răspuns în 30 de minute."},
    {"lang": "ro", "key": "category.hero_subtitle_active", "value": "Primește oferte de la specialiști din oraș gratuit! Trimite o cerere și primești un răspuns în 30 de minute."},
    {"lang": "ro", "key": "category.hero_trust_0", "value": "Gratuit • Fără obligații • Răspuns rapid"},
    {"lang": "ro", "key": "category.hero_trust_few", "value": "Specialiști verificați • Fără comision • Urmărire personală"},
    {"lang": "ro", "key": "category.hero_trust_requests", "value": "{count} cereri procesate • Specialiști verificați • Fără comision"},
    {"lang": "ro", "key": "category.hero_trust_full", "value": "⭐ {rating} evaluare medie • {count} cereri procesate • Fără comision"},
    {"lang": "ro", "key": "category.hero_cta", "value": "Primește oferte gratuite acum"},
    {"lang": "ro", "key": "category.hero_cta_sub", "value": "Durează doar 60 de secunde"},

    # ─── ru ───
    {"lang": "ru", "key": "category.hero_title", "value": "Найди услугу в {city}"},
    {"lang": "ru", "key": "category.hero_subtitle_0", "value": "Получи предложения от местных специалистов бесплатно! Отправь заявку сейчас, и мы свяжем тебя с наиболее подходящим исполнителем как можно быстрее."},
    {"lang": "ru", "key": "category.hero_subtitle_few", "value": "Получи предложения от проверенных местных специалистов бесплатно! Отправь заявку и получи ответ в течение 30 минут."},
    {"lang": "ru", "key": "category.hero_subtitle_active", "value": "Получи предложения от специалистов города бесплатно! Отправь заявку и получи ответ в течение 30 минут."},
    {"lang": "ru", "key": "category.hero_trust_0", "value": "Бесплатно • Без обязательств • Быстрый ответ"},
    {"lang": "ru", "key": "category.hero_trust_few", "value": "Проверенные специалисты • Без комиссии • Личное сопровождение"},
    {"lang": "ru", "key": "category.hero_trust_requests", "value": "{count} обработанных заявок • Проверенные специалисты • Без комиссии"},
    {"lang": "ru", "key": "category.hero_trust_full", "value": "⭐ {rating} средняя оценка • {count} обработанных заявок • Без комиссии"},
    {"lang": "ru", "key": "category.hero_cta", "value": "Получи бесплатные предложения сейчас"},
    {"lang": "ru", "key": "category.hero_cta_sub", "value": "Занимает всего 60 секунд"},

    # ─── sk ───
    {"lang": "sk", "key": "category.hero_title", "value": "Nájdi službu v {city}"},
    {"lang": "sk", "key": "category.hero_subtitle_0", "value": "Získaj ponuky od miestnych špecialistov zadarmo! Pošli žiadosť teraz a spojíme ťa s najvhodnejším poskytovateľom čo najrýchlejšie."},
    {"lang": "sk", "key": "category.hero_subtitle_few", "value": "Získaj ponuky od overených miestnych špecialistov zadarmo! Pošli žiadosť a získaj odpoveď do 30 minút."},
    {"lang": "sk", "key": "category.hero_subtitle_active", "value": "Získaj ponuky od špecialistov v meste zadarmo! Pošli žiadosť a získaj odpoveď do 30 minút."},
    {"lang": "sk", "key": "category.hero_trust_0", "value": "Zadarmo • Bez záväzku • Rýchla odpoveď"},
    {"lang": "sk", "key": "category.hero_trust_few", "value": "Overení špecialisti • Bez provízie • Osobné sledovanie"},
    {"lang": "sk", "key": "category.hero_trust_requests", "value": "{count} spracovaných žiadostí • Overení špecialisti • Bez provízie"},
    {"lang": "sk", "key": "category.hero_trust_full", "value": "⭐ {rating} priemerné hodnotenie • {count} spracovaných žiadostí • Bez provízie"},
    {"lang": "sk", "key": "category.hero_cta", "value": "Získaj bezplatné ponuky teraz"},
    {"lang": "sk", "key": "category.hero_cta_sub", "value": "Trvá len 60 sekúnd"},

    # ─── sl ───
    {"lang": "sl", "key": "category.hero_title", "value": "Poišči storitev v {city}"},
    {"lang": "sl", "key": "category.hero_subtitle_0", "value": "Pridobi ponudbe od lokalnih strokovnjakov brezplačno! Pošlji zahtevo zdaj in povežemo te z najprimernejšim izvajalcem čim prej."},
    {"lang": "sl", "key": "category.hero_subtitle_few", "value": "Pridobi ponudbe od preverjenih lokalnih strokovnjakov brezplačno! Pošlji zahtevo in prejmi odgovor v 30 minutah."},
    {"lang": "sl", "key": "category.hero_subtitle_active", "value": "Pridobi ponudbe od strokovnjakov v mestu brezplačno! Pošlji zahtevo in prejmi odgovor v 30 minutah."},
    {"lang": "sl", "key": "category.hero_trust_0", "value": "Brezplačno • Brez obveznosti • Hiter odgovor"},
    {"lang": "sl", "key": "category.hero_trust_few", "value": "Preverjeni strokovnjaki • Brez provizije • Osebno sledenje"},
    {"lang": "sl", "key": "category.hero_trust_requests", "value": "{count} obdelanih zahtev • Preverjeni strokovnjaki • Brez provizije"},
    {"lang": "sl", "key": "category.hero_trust_full", "value": "⭐ {rating} povprečna ocena • {count} obdelanih zahtev • Brez provizije"},
    {"lang": "sl", "key": "category.hero_cta", "value": "Pridobi brezplačne ponudbe zdaj"},
    {"lang": "sl", "key": "category.hero_cta_sub", "value": "Traja le 60 sekund"},

    # ─── sq ───
    {"lang": "sq", "key": "category.hero_title", "value": "Gjej një shërbim në {city}"},
    {"lang": "sq", "key": "category.hero_subtitle_0", "value": "Merr oferta nga specialistë lokalë falas! Dërgo një kërkesë tani dhe ne do të të lidhim me ofruesin më të përshtatshëm sa më shpejt të jetë e mundur."},
    {"lang": "sq", "key": "category.hero_subtitle_few", "value": "Merr oferta nga specialistë lokalë të verifikuar falas! Dërgo një kërkesë dhe merr përgjigje brenda 30 minutave."},
    {"lang": "sq", "key": "category.hero_subtitle_active", "value": "Merr oferta nga specialistë të qytetit falas! Dërgo një kërkesë dhe merr përgjigje brenda 30 minutave."},
    {"lang": "sq", "key": "category.hero_trust_0", "value": "Falas • Pa detyrim • Përgjigje e shpejtë"},
    {"lang": "sq", "key": "category.hero_trust_few", "value": "Specialistë të verifikuar • Pa komision • Ndjekje personale"},
    {"lang": "sq", "key": "category.hero_trust_requests", "value": "{count} kërkesa të processuara • Specialistë të verifikuar • Pa komision"},
    {"lang": "sq", "key": "category.hero_trust_full", "value": "⭐ {rating} vlerësim mesatar • {count} kërkesa të processuara • Pa komision"},
    {"lang": "sq", "key": "category.hero_cta", "value": "Merr oferta falas tani"},
    {"lang": "sq", "key": "category.hero_cta_sub", "value": "Zgjat vetëm 60 sekonda"},

    # ─── sr ───
    {"lang": "sr", "key": "category.hero_title", "value": "Pronađi uslugu u {city}"},
    {"lang": "sr", "key": "category.hero_subtitle_0", "value": "Dobij ponude od lokalnih stručnjaka besplatno! Pošalji zahtev sada i povežemo te sa najprikladnijim izvršiocem što je brže moguće."},
    {"lang": "sr", "key": "category.hero_subtitle_few", "value": "Dobij ponude od verifikovanih lokalnih stručnjaka besplatno! Pošalji zahtev i dobij odgovor u roku od 30 minuta."},
    {"lang": "sr", "key": "category.hero_subtitle_active", "value": "Dobij ponude od stručnjaka u gradu besplatno! Pošalji zahtev i dobij odgovor u roku od 30 minuta."},
    {"lang": "sr", "key": "category.hero_trust_0", "value": "Besplatno • Bez obaveze • Brz odgovor"},
    {"lang": "sr", "key": "category.hero_trust_few", "value": "Verifikovani stručnjaci • Bez provizije • Lično praćenje"},
    {"lang": "sr", "key": "category.hero_trust_requests", "value": "{count} obrađenih zahteva • Verifikovani stručnjaci • Bez provizije"},
    {"lang": "sr", "key": "category.hero_trust_full", "value": "⭐ {rating} prosečna ocena • {count} obrađenih zahteva • Bez provizije"},
    {"lang": "sr", "key": "category.hero_cta", "value": "Dobij besplatne ponude sada"},
    {"lang": "sr", "key": "category.hero_cta_sub", "value": "Traje samo 60 sekundi"},

    # ─── sv ───
    {"lang": "sv", "key": "category.hero_title", "value": "Hitta en tjänst i {city}"},
    {"lang": "sv", "key": "category.hero_subtitle_0", "value": "Få offerter från lokala specialister gratis! Skicka en förfrågan nu och vi kopplar ihop dig med den mest lämpliga leverantören så snabbt som möjligt."},
    {"lang": "sv", "key": "category.hero_subtitle_few", "value": "Få offerter från verifierade lokala specialister gratis! Skicka en förfrågan och få svar inom 30 minuter."},
    {"lang": "sv", "key": "category.hero_subtitle_active", "value": "Få offerter från specialister i staden gratis! Skicka en förfrågan och få svar inom 30 minuter."},
    {"lang": "sv", "key": "category.hero_trust_0", "value": "Gratis • Ingen förpliktelse • Snabbt svar"},
    {"lang": "sv", "key": "category.hero_trust_few", "value": "Verifierade specialister • Ingen provision • Personlig uppföljning"},
    {"lang": "sv", "key": "category.hero_trust_requests", "value": "{count} hanterade förfrågningar • Verifierade specialister • Ingen provision"},
    {"lang": "sv", "key": "category.hero_trust_full", "value": "⭐ {rating} genomsnittligt betyg • {count} hanterade förfrågningar • Ingen provision"},
    {"lang": "sv", "key": "category.hero_cta", "value": "Få gratis offerter nu"},
    {"lang": "sv", "key": "category.hero_cta_sub", "value": "Tar bara 60 sekunder"},

    # ─── tr ───
    {"lang": "tr", "key": "category.hero_title", "value": "{city} şehrinde hizmet bul"},
    {"lang": "tr", "key": "category.hero_subtitle_0", "value": "Yerel uzmanlardan ücretsiz teklifler alın! Şimdi bir istek gönderin, sizi en uygun sağlayıcıyla mümkün olan en kısa sürede bağlayalım."},
    {"lang": "tr", "key": "category.hero_subtitle_few", "value": "Doğrulanmış yerel uzmanlardan ücretsiz teklifler alın! Bir istek gönderin ve 30 dakika içinde yanıt alın."},
    {"lang": "tr", "key": "category.hero_subtitle_active", "value": "Şehirdeki uzmanlardan ücretsiz teklifler alın! Bir istek gönderin ve 30 dakika içinde yanıt alın."},
    {"lang": "tr", "key": "category.hero_trust_0", "value": "Ücretsiz • Yükümlülük yok • Hızlı yanıt"},
    {"lang": "tr", "key": "category.hero_trust_few", "value": "Doğrulanmış uzmanlar • Komisyon yok • Kişisel takip"},
    {"lang": "tr", "key": "category.hero_trust_requests", "value": "{count} işlenmiş istek • Doğrulanmış uzmanlar • Komisyon yok"},
    {"lang": "tr", "key": "category.hero_trust_full", "value": "⭐ {rating} ortalama puan • {count} işlenmiş istek • Komisyon yok"},
    {"lang": "tr", "key": "category.hero_cta", "value": "Şimdi ücretsiz teklifler alın"},
    {"lang": "tr", "key": "category.hero_cta_sub", "value": "Yalnızca 60 saniye sürer"},

    # ─── uk ───
    {"lang": "uk", "key": "category.hero_title", "value": "Знайди послугу в {city}"},
    {"lang": "uk", "key": "category.hero_subtitle_0", "value": "Отримай пропозиції від місцевих фахівців безкоштовно! Надішли запит зараз і ми з'єднаємо тебе з найбільш підходящим виконавцем якнайшвидше."},
    {"lang": "uk", "key": "category.hero_subtitle_few", "value": "Отримай пропозиції від перевірених місцевих фахівців безкоштовно! Надішли запит і отримай відповідь протягом 30 хвилин."},
    {"lang": "uk", "key": "category.hero_subtitle_active", "value": "Отримай пропозиції від фахівців міста безкоштовно! Надішли запит і отримай відповідь протягом 30 хвилин."},
    {"lang": "uk", "key": "category.hero_trust_0", "value": "Безкоштовно • Без зобов'язань • Швидка відповідь"},
    {"lang": "uk", "key": "category.hero_trust_few", "value": "Перевірені фахівці • Без комісії • Особистий супровід"},
    {"lang": "uk", "key": "category.hero_trust_requests", "value": "{count} оброблених запитів • Перевірені фахівці • Без комісії"},
    {"lang": "uk", "key": "category.hero_trust_full", "value": "⭐ {rating} середня оцінка • {count} оброблених запитів • Без комісії"},
    {"lang": "uk", "key": "category.hero_cta", "value": "Отримай безкоштовні пропозиції зараз"},
    {"lang": "uk", "key": "category.hero_cta_sub", "value": "Займає лише 60 секунд"},
]


def main():
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()


def run_seed(db):
    insert_translations(db)
    clear_redis_cache()


def insert_translations(db) -> None:
    count = 0
    for item in HERO_TRANSLATIONS:
        db.execute(
            text("""
                INSERT INTO translations (lang, key, value)
                VALUES (:lang, :key, :value)
                ON CONFLICT (lang, key)
                DO UPDATE SET value = EXCLUDED.value
            """),
            {"lang": item["lang"], "key": item["key"], "value": item["value"]}
        )
        count += 1
    db.commit()
    print(f"Inserted/updated {count} translation rows")


def clear_redis_cache() -> None:
    try:
        result = subprocess.run(
            ["redis-cli", "KEYS", "translations:*:category"],
            capture_output=True,
            text=True
        )
        keys = result.stdout.strip()
        if keys:
            subprocess.run(
                ["xargs", "redis-cli", "DEL"],
                input=keys,
                capture_output=True,
                text=True,
                check=True
            )
            print(f"Cleared Redis cache for category translations")
        else:
            print("No Redis keys found for category translations")
    except Exception as e:
        print(f"Warning: Could not clear Redis cache: {e}")


if __name__ == "__main__":
    main()
