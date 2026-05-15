from sqlalchemy import text
from apps.api.database import SessionLocal

def main():
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()

def run_seed(db):
    insert_translations(db, ALL_TRANSLATIONS)
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
    result = db.execute(text("""
        SELECT lang, COUNT(*) as keys
        FROM translations
        WHERE key LIKE 'pdf.effects_of_withdrawal_%'
        GROUP BY lang
        ORDER BY lang
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} keys")

ALL_TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "pdf.effects_of_withdrawal_title": "Effects of withdrawal",
        "pdf.effects_of_withdrawal_text": "If you withdraw from this contract, we shall reimburse to you all payments received from you, including the costs of delivery (with the exception of the supplementary costs resulting from your choice of a type of delivery other than the least expensive type of standard delivery offered by us), without undue delay and in any event not later than 14 days from the day on which we are informed about your decision to withdraw from this contract. We will carry out such reimbursement using the same means of payment as you used for the initial transaction, unless you have expressly agreed otherwise.",
    },
    "bg": {
        "pdf.effects_of_withdrawal_title": "Последствия от упражняването на правото на отказ",
        "pdf.effects_of_withdrawal_text": "При упражняване на правото на отказ от договора ще ви възстановим всички плащания, получени от вас, без излишно забавяне, а при всички положения — не по-късно от 14 дни, считано от датата, на която сме получили уведомлението ви за отказ от настоящия договор. Ще извършим възстановяването чрез същото платежно средство, използвано от вас при първоначалната трансакция, освен ако изрично не сте се договорили за друго.",
    },
    "pl": {
        "pdf.effects_of_withdrawal_title": "Skutki odstąpienia od umowy",
        "pdf.effects_of_withdrawal_text": "W przypadku odstąpienia od niniejszej umowy zwracamy Państwu wszystkie otrzymane od Państwa płatności, w tym koszty dostarczenia rzeczy (z wyjątkiem dodatkowych kosztów wynikających z wybranego przez Państwa sposobu dostarczenia innego niż najtańszy zwykły sposób dostarczenia oferowany przez nas), niezwłocznie, a w każdym przypadku ne później niż 14 dni od dnia, w którym zostaliśmy poinformowani o Państwa decyzji o wykonaniu prawa odstąpienia od niniejszej umowy. Zwrotu płatności dokonamy przy użyciu takich samych sposobów płatności, jakie zostały przez Państwa użyte v pierwotnej transakcji, chyba że wyraźnie zgodziliście się Państwo na inne rozwiązanie.",
    },
    "cs": {
        "pdf.effects_of_withdrawal_title": "Následky odstoupení od smlouvy",
        "pdf.effects_of_withdrawal_text": "Pokud odstoupíte od této smlouvy, vrátíme Vám bez zbytečného odkladu, nejpozději do 14 dnů ode dne, kdy nám došlo Vaše oznámení o odstoupení od smlouvy, všechny platby, které jsme od Vás obdrželi, včetně nákladů na dodání (kromě dodatečných nákladů vzniklých v důsledku Vámi zvoleného způsobu dodání, který je jiný než nejlevnější způsob standardního dodání námi nabízený). Pro vrácení plateb použijeme stejný platební prostředek, který jste použil(a) pro provedení počáteční transakce, pokud jste výslovně neurčil(a) jinak.",
    },
    "da": {
        "pdf.effects_of_withdrawal_title": "Følger af fortrydelse",
        "pdf.effects_of_withdrawal_text": "Hvis du udøver din fortrydelsesret i denne kontrakt, refunderer vi alle betalinger modtaget fra dig, herunder leveringsomkostninger (dog ikke ekstra omkostninger som følge af dit eget valg af en anden leveringsform end den billigste form for standardlevering, som vi tilbyder), uden unødig forsinkelse og under alle omstændigheder senest 14 dage fra den dato, hvor vi har modtaget meddelelse om din beslutning om at fortryde denne kontrakt. Vi gennemfører en sådan tilbagebetaling med samme betalingsmiddel, som du benyttede ved den oprindelige transaktion, medmindre du udtrykkeligt har indvilget i noget andet.",
    },
    "de": {
        "pdf.effects_of_withdrawal_title": "Folgen des Widerrufs",
        "pdf.effects_of_withdrawal_text": "Wenn Sie diesen Vertrag widerrufen, haben wir Ihnen alle Zahlungen, die wir von Ihnen erhalten haben, einschließlich der Lieferkosten (mit Ausnahme der zusätzlichen Kosten, die sich daraus ergeben, dass Sie eine andere Art der Lieferung als die von uns angebotene, günstigste Standardlieferung gewählt haben), unverzüglich und spätestens binnen vierzehn Tagen ab dem Tag zurückzuzahlen, an dem die Mitteilung über Ihren Widerruf dieses Vertrags bei uns eingegangen ist. Für diese Rückzahlung verwenden wir dasselbe Zahlungsmittel, das Sie bei der ursprünglichen Transaktion eingesetzt haben, es sei denn, mit Ihnen wurde ausdrücklich etwas anderes vereinbart.",
    },
    "el": {
        "pdf.effects_of_withdrawal_title": "Συνέπειες της υπαναχώρησης",
        "pdf.effects_of_withdrawal_text": "Εάν υπαναχωρήσετε από την παρούσα σύμβαση, θα σας επιστρέψουμε όλες τις πληρωμές που λάβαμε από εσάς, συμπεριλαμβανομένων των εξόδων παράδοσης (εξαιρουμένων των πρόσθετων εξόδων που οφείλονται στη δική σας επιλογή να χρησιμοποιηθεί τρόπος παράδοσης άλλος από τον φθηνότερο τυποποιημένο τρόπο παράδοσης που εμείς προσφέρουμε), χωρίς αδικαιολόγητη καθυστέρηση και οπωσδήποτε εντός 14 ημερολογιακών ημερών από την ημέρα που θα πληροφορηθούμε την απόφασή σας να υπαναχωρήσετε από την παρούσα σύμβαση. Θα εκτελέσουμε την ανωτέρω επιστροφή χρημάτων χρησιμοποιώντας το ίδιο μέσο πληρωμής που εσείς χρησιμοποιήσατε για την αρχική συναλλαγή, εκτός κι αν εσείς έχετε συμφωνήσει ρητώς κάτι διαφορετικό.",
    },
    "es": {
        "pdf.effects_of_withdrawal_title": "Consecuencias del desistimiento",
        "pdf.effects_of_withdrawal_text": "En caso de desistimiento por su parte, le devolveremos todos los pagos recibidos de usted, incluidos los gastos de entrega (con la excepción de los gastos adicionales resultantes de la elección por su parte de una modalidad de entrega diferente a la modalidad menos costosa de entrega ordinaria que ofrezcamos) sin ninguna demora indebida y, en todo caso, a más tardar 14 días naturales a partir de la fecha en la que se nos informe de su decisión de desistir del presente contrato. Procedерemos a efectuar dicho reembolso utilizando el mismo medio de pago empleado por usted para la transacción inicial, a no ser que haya usted dispuesto expresamente lo contrario.",
    },
    "et": {
        "pdf.effects_of_withdrawal_title": "Taganemise tagajärjed",
        "pdf.effects_of_withdrawal_text": "Kui Te taganete käesolevast lepingust, tagastame Teile kõik Teilt saadud maksed, sealhulgas kättetoimetamise kulud (välja arvatud täiendavad kulud, miз tulenevad Teie valitud kättetoimetamise viisist, mis erineb meie pakutud kõige odavamast tavapärasest kättetoimetamise viisist) viivitamata, kuid hiljemalt 14 päeva möödumisel alates päevast, mil saame teada Teie otsusest käesolevast lepingust taganeda. Teeme nimetatud tagasimaksed, kasutades sama makseviisi, mida kasutasite algses tehingus, v.a juhul, kui olete sõnaselgelt andnud nõusoleku teistsuguse makseviisi kasutamiseks.",
    },
    "fi": {
        "pdf.effects_of_withdrawal_title": "Peruuttamisen vaikutukset",
        "pdf.effects_of_withdrawal_text": "Jos peruutat tämän sopimuksen, palautamme teille kaikki teiltä saamamme suoritukset, myös toimituskustannukset (lukuun ottamatta lisäkustannuksia, jotka ovat aiheutuneet valitsemastanne muusta kuin tarjoamastamme edullisimmasta vakiotoimitustavasta), viivytyksettä ja joka tapauksessa viimeistään 14 päivän kuluttua siitä, kun olemme saaneet tietää päätöksestänne peruuttaa sopimus. Suoritamme palautuksen samalla maksutavalla, jota olette käyttänyt alkuperäisessä liiketoimessa, ellette ole nimenomaisesti suostunut muuhun.",
    },
    "fr": {
        "pdf.effects_of_withdrawal_title": "Effets de la rétractation",
        "pdf.effects_of_withdrawal_text": "En cas de rétractation de votre part du présent contrat, nous vous rembourserons tous les paiements reçus de vous, y compris les frais de livraison (à l'exception des frais supplémentaires découlant du fait que vous avez choisi, le cas échéant, un mode de livraison autre que le mode moins coûteux de livraison standard proposé par nous) sans retard excessif et, en tout état de cause, au plus tard quatorze jours à compter du jour où nous sommes informés de votre décision de rétractation du présent contrat. Nous procéderons au remboursement en utilisant le même moyen de paiement que celui que vous avez utilisé pour la transaction initiale, sauf si vous convenez expressément d'un moyen différent.",
    },
    "ga": {
        "pdf.effects_of_withdrawal_title": "Éifeachtaí an tarraingt siar",
        "pdf.effects_of_withdrawal_text": "Má tharraingíonn tú siar ón gconradh seo, aisíocfaimid na híocaíochtaí go léir a fuaireamar uait, lena n-áirítear na costais seachadta (seachas na costais bhreise a thig as do rogha féin cineál seachadta seachas an cineál seachadta caighdeánach is saoire atá ar fáil uainn), gan mhoill mhíchuí agus ar aon chuma tráth nach déanaí ná 14 lá ón lá a gcuirtear d'aon chinneadh chun tarraingt siar ón gconradh seo in iúl dúinn. Déanfaimid an t-aisíoc sin ag baint úsáide as na modhanna íocaíochta céanna a d'úsáid tú don idirbheart tosaigh, mura rud é gur aontaigh tú go sainráite a mhalairt.",
    },
    "hr": {
        "pdf.effects_of_withdrawal_title": "Posljedice odustajanja",
        "pdf.effects_of_withdrawal_text": "Ako odustanete od ovog ugovora, izvršit ćemo povrat svih uplaćenih sredstava koje smo od vas primili, uključujući i troškove isporuke (osim dodatnih troškova koji su nastali kao rezultat vašeg odabira vrste isporuke koja je različita od najjeftinije standardne isporuke koju mi nudimo), bez odgađanja, a najkasnije u roku od 14 dana od dana kada smo zaprimili vašu obavijest o odluci o odustajanju od ugovora. Povrat sredstava izvršit ćemo koristeći ista sredstva plaćanja koja ste vi koristili prilikom početne transakcije, osim ako niste izričito pristali na drugo sredstvo plaćanja.",
    },
    "hu": {
        "pdf.effects_of_withdrawal_title": "Az elállás joghatásai",
        "pdf.effects_of_withdrawal_text": "Ha Ön eláll ettől a szerződéstől, haladéktalanul, de legkésőbb az Ön elállási nyilatkozatának kézhezvételétől számított 14 napon belül visszatérítjük az Ön által teljesített valamennyi ellenszolgáltatást, ideértve a fuvarozási költséget is (kivéve azokat a többletköltségeket, amelyek amiatt merültek fel, hogy Ön az általunk felkínált, legolcsóbb szokásos fuvarozási módtól eltérő fuvarozási módot választott). A visszatérítés során az eredeti ügylet során alkalmazott fizetési móddal egyező fizetési módot alkalmazunk, kivéve, ha Ön más fizetési mód igénybevételéhez kifejezetten hozzájárulását adja.",
    },
    "it": {
        "pdf.effects_of_withdrawal_title": "Effetti del recesso",
        "pdf.effects_of_withdrawal_text": "Se lei recede dal presente contratto, le saranno rimborsati tutti i pagamenti che ha effettuato a nostro favore, compresi i costi di consegna (ad eccezione dei costi supplementari derivanti dalla sua eventuale scelta di un tipo di consegna diverso dal tipo meno costoso di consegna standard da noi offerto), senza indebito ritardo e in ogni caso non oltre 14 giorni dal giorno in cui siamo informati della sua decisione di recedere dal presente contratto. Tali rimborsi saranno effettuati utilizzando lo stesso mezzo di pagamento da lei usato per la transazione iniziale, salvo che lei non abbia espressamente convenuto altrimenti.",
    },
    "lt": {
        "pdf.effects_of_withdrawal_title": "Sutarties atsisakymo pasekmės",
        "pdf.effects_of_withdrawal_text": "Jei Jūs atsisakote šios sutarties, mes Jums grąžinsime visus iš Jūsų gautus mokėjimus, įskaitant pristatymo išlaidas (išskyrus papildomas išlaidas, susidariusias dėl Jūsų pasirinkto kito nei mūsų siūlomas pigiausias standartinis pristatymo būdas), nepagrįstai nedelsdami ir bet kuriuo atveju ne vėliau kaip per 14 dienų nuo tos dienos, kai pranešėte mums apie savo sprendimą atsisakyti šios sutarties. Mes atliksime tokį grąžinimą naudodami tokį patį mokėjimo būdą, kokį Jūs naudojote pradinei operacijai, nebent Jūs aiškiai sutikote su kitu būdu.",
    },
    "lv": {
        "pdf.effects_of_withdrawal_title": "Atteikuma sekas",
        "pdf.effects_of_withdrawal_text": "Ja Jūs atteiksieties no šā līguma, mēs Jums atmaksāsim visus no Jums saņemtos maksājumus, tostarp piegādes izmaksas (izņemot papildu izmaksas, kas radušās tādēļ, ka Jūs esat izvēlējies piegādes veidu, kas nav mūсу piedāvātais lētākais standarta piegādes veids), bez nepamatotas kavēšanās un jebkurā gadījumā ne vēlāk kā 14 dienu laikā no dienas, kad mēs tikām informēti par Jūsu lēmumu atteikties no šā līguma. Atmaksāšana tiks veikta, izmantojot tādu pašu maksāšanas līdzekli, kādu Jūs izmantojāt sākotnējam darījumam, ja vien neesat skaidri paudis piekrišanu citam maksāšanas līdzeklim.",
    },
    "mt": {
        "pdf.effects_of_withdrawal_title": "Effetti tal-irtirar",
        "pdf.effects_of_withdrawal_text": "Jekk tirtira minn dan il-kuntratt, aħna nroddulek lura l-pagamenti kollha li rċevejna mingħandek, inklużi l-ispejjeż tal-kunsinna (bl-eċċezzjoni tal-ispejjeż supplimentari li jirriżultaw mill-għażla tiegħek ta’ tip ta’ kunsinna li mhijiex l-orħos tip ta’ kunsinna standard offruta minna), mingħajr dewmien żejjed u f'kull każ mhux aktar tard minn 14-il jum mill-jum li fih inkunu infurmati bid-deċiżjoni tiegħek li tirtira minn dan il-kuntratt. Se nwettqu dan ir-rimborż billi nużaw l-istess mezz ta’ pagament li użajt int għat-tranżazzjoni inizjali, sakemm ma tkunx ftehimt mod ieħor espressament.",
    },
    "nl": {
        "pdf.effects_of_withdrawal_title": "Gevolgen van de herroeping",
        "pdf.effects_of_withdrawal_text": "Als u de overeenkomst herroept, ontvangt u alle betalingen die u tot op dat moment heeft gedaan, inclusief leveringskosten (met uitzondering van eventuele extra kosten ten gevolge van uw keuze voor een andere wijze van levering dan de door ons geboden goedkoopste standaard levering) onverwijld en in ieder geval niet later dan 14 dagen nadat wij op de hoogte zijn gesteld van uw beslissing de overeenkomst te herroepen, van ons terug. Wij betalen u terug met hetzelfde betaalmiddel als waarmee u de oorspronkelijke transactie heeft verricht, tenzij u uitdrukkelijk anderszins heeft ingestemd.",
    },
    "pt": {
        "pdf.effects_of_withdrawal_title": "Efeitos da livre resolução",
        "pdf.effects_of_withdrawal_text": "Em caso de resolução do presente contrato, ser-lhe-ão reembolsados todos os pagamentos efetuados, incluindo os custos de entrega (com exceção de custos suplementares resultantes da sua escolha de uma modalidade de envio diferente da modalidade menos onerosa de envio normal por nós oferecida), sem demora injustificada e, em qualquer caso, o mais tardar 14 dias a contar da data em que fomos informados da sua decisão de resolução do presente contrato. Efetuamos esses reembolsos usando o mesmo meio de pagamento que usou na transação inicial, salvo acordo expresso em contrário da sua parte.",
    },
    "ro": {
        "pdf.effects_of_withdrawal_title": "Efectele retragerii",
        "pdf.effects_of_withdrawal_text": "Dacă vă retrageți, vom rambursa orice sumă pe care am primit-o de la dumneavoastră, inclusiv costurile livrării (cu excepția costurilor suplimentare determinate de faptul că ați ales altă modalitate de livrare decât cel mai ieftin tip de livrare standard oferit de noi), fără întârzieri nejustificate și, în orice caz, nu mai târziu de 14 zile de la data la care suntem informați cu privire la decizia dumneavoastră de a vă retrage din prezentul contract. Vom efectua această rambursare folosind aceeași metodă de plată ca și cea folosită pentru tranzacția inițială, cu excepția cazului în care v-ați exprimat acordul expres for o altă modalitate.",
    },
    "sk": {
        "pdf.effects_of_withdrawal_title": "Dôsledky odstúpenia od zmluvy",
        "pdf.effects_of_withdrawal_text": "Po odstúpení od zmluvy Vám vrátime všetky platby, ktoré ste uhradili v súvislosti s uzavretím zmluvy, najmä kúpnu cenu vrátane nákladov na doručenie tovaru k Vám. To sa nevzťahuje na dodatočné náklady, ak ste si zvolili iný druh doručenia, ako je najlacnejší bežný spôsob doručenia, ktorý ponúkame. Platby Vám budú vrátené bez zbytočného odkladu, najneskôr do 14 dní odo dňa, keď nám bude doručené Vaše oznámenie o odstúpení od tejto zmluvy. Ich úhrada bude uskutočnená rovnakým spôsobom, aký ste použili pri Vašej platbe, ak ste výslovne nesúhlasili s iným spôsobom platby.",
    },
    "sl": {
        "pdf.effects_of_withdrawal_title": "Učinki odstopa od pogodbe",
        "pdf.effects_of_withdrawal_text": "Če odstopite od te pogodbe, vam brez nepotrebnega odlašanja in v vsakem primeru najpozneje v 14 dneh od dneva, ko smo obveščeni o vaši odločitvi o odstopu od te pogodbe, povrnemo vsa prejeta plačila, vključno s stroški dostave (razen dodatnih stroškov zaradi izbire vrste dostave, ki ni najcenejša ponujena standardna oblika dostave). Tako povračilo izvedemo z istim plačilnim sredstvom, kot ste ga uporabili pri prvotni transakciji, razen če ste se izrecno dogovorili drugače.",
    },
    "sv": {
        "pdf.effects_of_withdrawal_title": "Verkan av utövad ångerrätt",
        "pdf.effects_of_withdrawal_text": "Om du frånträder detta avtal kommer vi att betala tillbaka alla betalningar vi fått från dig, bland dem också leveranskostnader (men då räknas inte extra leveranskostnader till följd av att du valt något annat leveranssätt än den billigaste standardleverans vi erbjuder). Återbetalningen kommer att ske utan onödigt dröjsmål och i hvilket fall som helst senast 14 dagar från och med den dag då vi underrättades om ditt beslut att frånträder avtalet. Vi kommer att använda samma betalningsmedel för återbetalningen som du själv har använt för den inledande affärshändelsen, om du inte uttryckligen kommit överens med oss om något annat.",
    },
    "sq": {
        "pdf.effects_of_withdrawal_title": "Pasojat e tërheqjes",
        "pdf.effects_of_withdrawal_text": "Nëse tërhiqeni nga kjo kontratë, ne do t'ju rimbursojmë të gjitha pagesat e marra nga ju, duke përfshirë kostot e dërgesës (me përjashtim të kostove shtesë që vijnë nga zgjedhja juaj e një lloji dërgese tjetër nga lloji më pak i kushtueshëm i dërgesës standarde të ofruar nga ne), pa vonesa të pajustifikuara dhe në çdo rast jo më vonë se 14 ditë nga dita në të cilën jemi informuar për vendimin tuaj për t'u tërhequr nga kjo kontratë. Ne do ta kryejmë këtë rimbursim duke përdorur të njëjtat mjete pagese si ato që keni përdorur për transaksionin fillestar, përveç nëse keni rënë dakord shprehimisht ndryshe.",
    },
    "sr": {
        "pdf.effects_of_withdrawal_title": "Posledice odustanka",
        "pdf.effects_of_withdrawal_text": "Ako odustanete od ovog ugovora, izvršićemo povraćaj svih uplata koje smo primili od vas, uključujući i troškove isporuke (osim dodatnih troškova koji su nastali kao posledica vašeg izbora načina isporuke koji je drugačiji od najjeftinijeg standardnog načina isporuke koji nudimo), bez odlaganja, a najkasnije u roku od 14 dana od dana kada smo primili vaše obaveštenje o odluci o odustajanju od ugovora. Povraćaj ćemo izvršiti koristeći ista sredstva plaćanja koja ste vi koristili prilikom prvobitne transakcije, osim ako niste izričito pristali na neko drugo sredstvo plaćanja.",
    },
    "mk": {
        "pdf.effects_of_withdrawal_title": "Последици од откажувањето",
        "pdf.effects_of_withdrawal_text": "Доколку се откажете од овој договор, ќе ви ги вратиме сите плаќања што сме ги примиле од вас, вклучувајќи ги и трошоците за испорака (со исклучок на дополнителните трошоци што произлегуваат од вашиот избор на тип на испорака различен од најевтиниот тип на стандардна испорака понудена од нас), без непотребно одложување и во секој случај најдоцна во рок од 14 дена од денот кога сме информирани за вашата одлука за откажување од овој договор. Враќањето ќе го извршиме со истите средства за плаќање што сте ги користеле за првичната трансакција, освен ако изрично не сте се договориле поинаку.",
    },
    "me": {
        "pdf.effects_of_withdrawal_title": "Posljedice odustanka",
        "pdf.effects_of_withdrawal_text": "Ako odustanete od ovog ugovora, izvršićemo povraćaj svih uplata koje smo primili od vas, uključujući i troškove isporuke (osim dodatnih troškova koji su nastali kao posljedica vašeg izbora načina isporuke koji je drugačiji od najjeftinijeg standardnog načina isporuke koji nudimo), bez odlaganja, a najkasnije u roku od 14 dana od dana kada smo primili vaše obaveštenje o odluci o odustajanju od ugovora. Povraćaj ćemo izvršiti koristeći ista sredstva plaćanja koja ste vi koristili prilikom prvobitne transakcije, osim ako niste izričito pristali na neko drugo sredstvo plaćanja.",
    },
    "bs": {
        "pdf.effects_of_withdrawal_title": "Posljedice odustajanja",
        "pdf.effects_of_withdrawal_text": "Ako odustanete od ovog ugovora, izvršit ćemo povrat svih uplata koje smo primili od vas, uključujući i troškove isporuke (osim dodatних troškova koji su nastali kao rezultat vašeg odabira vrste isporuke koja je različita od najjeftinije standardne isporuke koju mi nudimo), bez odlaganja, a najkasnije u roku od 14 dana od dana kada smo zaprimili vašu obavijest o odluci o odustajanju od ugovora. Povrat ćemo izvršiti koristeći ista sredstva plaćanja koja ste vi koristili prilikom početne transakcije, osim ako niste izričito pristali na drugo sredstvo plaćanja.",
    },
    "is": {
        "pdf.effects_of_withdrawal_title": "Réttaráhrif riftunar",
        "pdf.effects_of_withdrawal_text": "Ef þú riftir þessum samningi munum við endurgreiða þér allar greiðslur sem við höfum fengið frá þér, þar með talinn sendingarkostnað (að undanskildum viðbótarkostnaði sem stafar af því að þú valdir aðra sendingaraðferð en ódýrustu staðalsendinguna sem við bjóðum upp á), án ótilhlýðilegrar tafar og í öllu falli eigi síðar en 14 dögum frá þeim degi er okkur er tilkynnt um ákvörðun þína um að rifta þessum samningi. Við munum framkvæma slíka endurgreiðslu með sama greiðslumiðli og þú notaðir við upphaflegu viðskiptin, nema þú hafir beinlínis samþykkt annað.",
    },
    "no": {
        "pdf.effects_of_withdrawal_title": "Virkningene av angreretten",
        "pdf.effects_of_withdrawal_text": "Dersom du går fra denne avtalen, skal vi tilbakebetale alle betalinger vi har mottatt fra deg, herunder leveringskostnadene (med unntak av tilleggskostnader som følge av at du har valgt en annen type levering enn den billigste typen standardlevering vi tilbyr), uten unødig opphold og i alle tilfeller senest 14 dager etter den dag vi mottar melding om din beslutning om å gå fra denne avtalen. Vi foretar tilbakebetalingen med samme betalingsmiddel som du benyttet ved den opprinnelige transaksjonen, med mindre du uttrykkelig har avtalt noe annet med oss.",
    },
    "tr": {
        "pdf.effects_of_withdrawal_title": "Caymanın Etkileri",
        "pdf.effects_of_withdrawal_text": "Bu sözleşmeden caymanız durumunda, tarafımıza iletilen teslimat masrafları da dahil (tarafımızca sunulan en ucuz standart teslimat türü dışında bir teslimat türünü seçmenizden kaynaklanan ek masraflar hariç) tüm ödemeleri, cayma kararınıza ilişkin bildirimin tarafımıza ulaştığı tarihten itibaren en geç 14 gün içinde gecikmeksizin size iade edeceğiz. Aksi yönde açıkça bir anlaşmanız olmadığı sürece, bu iade işlemini ilk işlemde kullandığınız ödeme yöntemiyle gerçekleştireceğiz.",
    },
    "uk": {
        "pdf.effects_of_withdrawal_title": "Наслідки відмови від договору",
        "pdf.effects_of_withdrawal_text": "Якщо ви відмовляєтеся від цього договору, ми відшкодуємо вам усі платежі, отримані від вас, включаючи витрати на доставку (за винятком додаткових витрат, що виникають внаслідок обраного вами способу доставки, відмінного від найдешевшого способу стандартної доставки, запропонованого нами), без невиправданої затримки і в будь-якому випадку не пізніше 14 днів з дня, коли ми були проінформовані про ваше рішення відмовитися від цього договору. Ми здійснимо таке відшкодування за допомогою того ж засобу платежу, який ви використовували для початкової транзакції, якщо ви явно не погодилися на інше.",
    },
    "ru": {
        "pdf.effects_of_withdrawal_title": "Последствия отказа от договора",
        "pdf.effects_of_withdrawal_text": "В случае отказа от настоящего договора мы вернем вам все платежи, полученные от вас, включая расходы по доставке (за исключением дополнительных расходов, возникших в результате вашего выбора способа доставки, отличного от самого дешевого вида стандартной доставки, предлагаемого нами), без неоправданной задержки и в любом случае не позднее 14 дней со дня, когда мы были проинформированы о вашем решении отказаться от настоящего договора. Мы осуществим такой возврат с использованием того же платежного средства, которое вы использовали для первоначальной транзакции, если вы прямо не согласились на иное.",
    },
}

if __name__ == "__main__":
    main()
