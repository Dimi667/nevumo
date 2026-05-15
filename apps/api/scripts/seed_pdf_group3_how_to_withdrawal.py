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
        WHERE key LIKE 'pdf.%'
        GROUP BY lang
        ORDER BY lang
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} keys")

ALL_TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "pdf.how_to_withdrawal_text": "To exercise the right of withdrawal, you must inform us:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\ntrading as <b>Nevumo</b>\n77 Petko Karavelov Blvd., Entrance A, Apt. 19, Triadica District, Sofia 1408, Bulgaria\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "of your decision to withdraw from this contract by an unequivocal statement (e.g., a letter sent by post or e-mail).",
    },
    "bg": {
        "pdf.how_to_withdrawal_text": "За да упражните правото на отказ, трябва да ни уведомите:",
        "pdf.company_address_block": "<b>„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД</b>\nс търговска марка <b>Nevumo</b>\nбул. Петко Каравелов бл. 77, вх. А, ап. 19, р-н Триадица, п.к. 1408, гр. София, България\nИмейл: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "за решението си да се откажете от договора чрез недвусмислено заявление (например писмо, изпратено по пощата, или имейл).",
    },
    "pl": {
        "pdf.how_to_withdrawal_text": "Aby skorzystać z prawa odstąpienia od umowy, muszą Państwo poinformować nas:",
        "pdf.company_address_block": "<b>„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООD</b>\ndziałającą pod marką <b>Nevumo</b>\nul. bul. Petko Karawełow bl. 77, wch. A, ap. 19, dzielnica Triadica, k.p. 1408, Sofia, Bułgaria\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "o swojej decyzji o odstąpieniu od niniejszej umowy w drodze jednoznacznego oświadczenia (na przykład pismo wysłane pocztą lub pocztą elektroniczną).",
    },
    "cs": {
        "pdf.how_to_withdrawal_text": "Pro uplatnění práva na odstoupení od smlouvy nás musíte informovat:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" s.r.o.</b>\nobchodující jako <b>Nevumo</b>\n77 Petko Karavelov Blvd., vchod A, byt 19, obvod Triadica, Sofie 1408, Bulharsko\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "o svém rozhodnutí odstoupit od této smlouvy formou jednoznačného prohlášení (např. dopisem zaslaným poštou nebo e-mailem).",
    },
    "da": {
        "pdf.how_to_withdrawal_text": "For at udøve fortrydelsesretten skal du informere os:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nder handler som <b>Nevumo</b>\n77 Petko Karavelov Blvd., Indgang A, Lejl. 19, Triadica District, Sofia 1408, Bulgarien\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "om din beslutning om at trække dig ud af denne kontrakt ved en utvetydig erklæring (f.eks. et brev sendt med post eller e-mail).",
    },
    "de": {
        "pdf.how_to_withdrawal_text": "Um Ihr Widerrufsrecht auszuüben, müssen Sie uns informieren:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nhandelnd als <b>Nevumo</b>\n77 Petko Karavelov Blvd., Eingang A, App. 19, Stadtteil Triadica, Sofia 1408, Bulgarien\nE-Mail: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "über Ihren Entschluss, diesen Vertrag zu widerrufen, mittels einer eindeutigen Erklärung (z. B. ein mit der Post versandter Brief oder eine E-Mail).",
    },
    "el": {
        "pdf.how_to_withdrawal_text": "Για να ασκήσετε το δικαίωμα υπαναχώρησης, πρέπει να μας ενημερώσετε:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" ΕΠΕ</b>\nμε την εμπορική ονομασία <b>Nevumo</b>\nΛεωφόρος Petko Karavelov 77, Είσοδος Α, Διαμ. 19, Περιοχή Triadica, Σόφια 1408, Βουλγαρία\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "για την απόφασή σας να υπαναχωρήσετε από την παρούσα σύμβαση με μια σαφή δήλωση (π.χ. επιστολή που αποστέλλεται ταχυδρομικώς ή μέσω e-mail).",
    },
    "es": {
        "pdf.how_to_withdrawal_text": "Para ejercer el derecho de desistimiento, deberá informarnos:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\noperando como <b>Nevumo</b>\n77 Petko Karavelov Blvd., Portal A, Apt. 19, Distrito de Triadica, Sofía 1408, Bulgaria\nCorreo electrónico: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "de su decisión de desistir del presente contrato a través de una declaración inequívoca (por ejemplo, una carta enviada por correo postal o por correo electrónico).",
    },
    "et": {
        "pdf.how_to_withdrawal_text": "Taganemisõiguse kasutamiseks peate meid teavitama:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\ntegutseb nime all <b>Nevumo</b>\n77 Petko Karavelov Blvd., sissepääs A, korter 19, Triadica piirkond, Sofia 1408, Bulgaaria\nE-post: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "oma otsusest lepingust taganeda ühemõttelise avaldusega (nt posti või e-postiga saadetud kiri).",
    },
    "fi": {
        "pdf.how_to_withdrawal_text": "Peruuttamisoikeuden käyttämiseksi sinun on ilmoitettava meille:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\ntoimii nimellä <b>Nevumo</b>\n77 Petko Karavelov Blvd., Sisäänkäynti A, Huon. 19, Triadica, Sofia 1408, Bulgaria\nSähköposti: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "päätöksestäsi peruuttaa sopimus yksiselitteisellä ilmoituksella (esim. postitse tai sähköpostilla lähetetyllä kirjeellä).",
    },
    "fr": {
        "pdf.how_to_withdrawal_text": "Pour exercer le droit de rétractation, vous devez nous informer :",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nexerçant sous le nom de <b>Nevumo</b>\n77 Petko Karavelov Blvd., Entrée A, Apt. 19, District de Triadica, Sofia 1408, Bulgarie\nE-mail : <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "de votre décision de vous rétracter du présent contrat par une déclaration dénuée d'ambiguïté (par exemple, une lettre envoyée par la poste ou par e-mail).",
    },
    "ga": {
        "pdf.how_to_withdrawal_text": "Chun an ceart tarraingt siar a fheidhmiú, ní mór duit sinn a chur ar an eolas:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nag trádáil mar <b>Nevumo</b>\n77 Petko Karavelov Blvd., Iontráil A, Árasán 19, Ceantar Triadica, Sóifia 1408, an Bhulgáir\nR-phost: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "faoi do chinneadh tarraingt siar as an gconradh seo trí ráiteas soiléir (m.sh. litir a sheoltar tríd an bpost nó trí ríomhphost).",
    },
    "hr": {
        "pdf.how_to_withdrawal_text": "Kako biste ostvarili pravo na odustajanje, morate nas obavijestiti:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" d.o.o.</b>\nposluje kao <b>Nevumo</b>\n77 Petko Karavelov Blvd., Ulaz A, Stan 19, Triadica, Sofija 1408, Bugarska\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "o svojoj odluci o odustajanju od ovog ugovora nedvosmislenom izjavom (npr. pismom poslanim poštom ili e-poštom).",
    },
    "hu": {
        "pdf.how_to_withdrawal_text": "Az elállási jog gyakorlásához tájékoztatnia kell minket:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nmint <b>Nevumo</b>\n77 Petko Karavelov Blvd., A lépcsőház, 19. lakás, Triadica negyed, Szófia 1408, Bulgária\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "abból a döntéséből, hogy eláll ettől a szerződéstől egy egyértelmű nyilatkozat útján (pl. postán vagy e-mailben küldött levélben).",
    },
    "is": {
        "pdf.how_to_withdrawal_text": "Til að nýta réttinn til að falla frá samningi verður þú að láta okkur vita:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nstarfar sem <b>Nevumo</b>\n77 Petko Karavelov Blvd., Inngangur A, Íbúð 19, Triadica hérað, Sofía 1408, Búlgaría\nNetfang: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "um ákvörðun þína um að falla frá þessum samningi með ótvíræðri yfirlýsingu (t.d. bréfi sem sent er með pósti eða tölvupósti).",
    },
    "it": {
        "pdf.how_to_withdrawal_text": "Per esercitare il diritto di recesso, è tenuto a informarci:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" S.r.l.</b>\nche opera come <b>Nevumo</b>\n77 Petko Karavelov Blvd., Ingresso A, Int. 19, Distretto di Triadica, Sofia 1408, Bulgaria\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "della sua decisione di recedere dal presente contratto tramite una dichiarazione esplicita (ad esempio, una lettera inviata per posta o e-mail).",
    },
    "lb": {
        "pdf.how_to_withdrawal_text": "Fir d'Widderruffsrecht auszeüben, musst Dir eis informéieren:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nhandelnd als <b>Nevumo</b>\n77 Petko Karavelov Blvd., Agank A, App. 19, Distrikt Triadica, Sofia 1408, Bulgarien\nE-Mail: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "iwwer Är Decisioun, dëse Vertrag ze widderruffen, mat enger eendeiteger Erklärung (z. B. e Bréif per Post oder E-Mail).",
    },
    "lt": {
        "pdf.how_to_withdrawal_text": "Norėdami pasinaudoti teise atsisakyti sutarties, turite mus informuoti:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nveikianti kaip <b>Nevumo</b>\n77 Petko Karavelov Blvd., A įėjimas, 19 butas, Triadica rajonas, Sofija 1408, Bulgarija\nEl. paštas: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "apie savo sprendimą atsisakyti šios sutarties pateikdami vienareikšmišką pareiškimą (pvz., paštu arba el. paštu išsiųstu laišku).",
    },
    "lv": {
        "pdf.how_to_withdrawal_text": "Lai izmantotu atteikuma tiesības, jums ir jāinformē mūs:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\ndarbojas kā <b>Nevumo</b>\n77 Petko Karavelov Blvd., Ieeja A, Dz. 19, Triadica rajons, Sofija 1408, Bulgārija\nE-pasts: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "par savu lēmumu atteikties no šī līguma ar nepārprotamu paziņojumu (piemēram, pa pastu vai e-pastu nosūtītu vēstuli).",
    },
    "mk": {
        "pdf.how_to_withdrawal_text": "За да го остварите правото на повлекување, мора да нè известите:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nработи како <b>Nevumo</b>\nБул. Петко Каравелов бр. 77, Влез А, Стан 19, Област Триадица, Софија 1408, Бугарија\nЕ-пошта: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "за вашата одлука за повлекување од овој договор со недвосмислена изјава (на пр. писмо испратено по пошта или е-пошта).",
    },
    "mt": {
        "pdf.how_to_withdrawal_text": "Biex teżerċita d-dritt ta' rtirar, trid tinformana:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\ntopera bħala <b>Nevumo</b>\n77 Petko Karavelov Blvd., Daħla A, Apt. 19, Distrett ta' Triadica, Sofia 1408, il-Bulgarija\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "bid-deċiżjoni tiegħek li tirtira minn dan il-kuntratt permezz ta' dikjarazzjoni ċara (eż. ittra mibgħuta bil-posta jew bl-email).",
    },
    "nl": {
        "pdf.how_to_withdrawal_text": "Om het herroepingsrecht uit te oefenen, moet u ons informeren:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nhandelend onder de naam <b>Nevumo</b>\n77 Petko Karavelov Blvd., Ingang A, Apt. 19, Triadica District, Sofia 1408, Bulgarije\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "van uw beslissing om de overeenkomst te herroepen via een ondubbelzinnige verklaring (bijv. een brief per post of e-mail).",
    },
    "no": {
        "pdf.how_to_withdrawal_text": "For å utøve angreretten må du informere oss:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nsom opererer som <b>Nevumo</b>\n77 Petko Karavelov Blvd., Inngang A, Lejl. 19, Triadica-distriktet, Sofia 1408, Bulgaria\nE-post: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "om din beslutning om å gå bort fra denne kontrakten ved en utvetydig erklæring (f.eks. et brev sendt per post eller e-post).",
    },
    "pt": {
        "pdf.how_to_withdrawal_text": "Para exercer o direito de arrependimento, você deve nos informar:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\noperando como <b>Nevumo</b>\n77 Petko Karavelov Blvd., Entrada A, Apt. 19, Distrito de Triadica, Sófia 1408, Bulgária\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "da sua decisão de rescindir este contrato por meio de uma declaração inequívoca (por exemplo, uma carta enviada por correio ou e-mail).",
    },
    "pt-PT": {
        "pdf.how_to_withdrawal_text": "Para exercer o direito de livre resolução, deve informar-nos:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\noperando como <b>Nevumo</b>\n77 Petko Karavelov Blvd., Entrada A, Apt. 19, Distrito de Triadica, Sófia 1408, Bulgária\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "da sua decisão de resolver o presente contrato através de uma declaração inequívoca (por exemplo, uma carta enviada por correio ou e-mail).",
    },
    "ro": {
        "pdf.how_to_withdrawal_text": "Pentru a vă exercita dreptul de retragere, trebuie să ne informați:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" S.R.L.</b>\ntranzacționând ca <b>Nevumo</b>\n77 Petko Karavelov Blvd., Intrarea A, Apt. 19, Sector Triadica, Sofia 1408, Bulgaria\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "cu privire la decizia dumneavoastră de a vă retrage din prezentul contract prin intermediul unei declarații neechivoce (de exemplu, o scrisoare trimisă prin poștă sau e-mail).",
    },
    "ru": {
        "pdf.how_to_withdrawal_text": "Чтобы воспользоваться правом на отказ от договора, вы должны уведомить нас:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nпод торговой маркой <b>Nevumo</b>\nбул. Петко Каравелов 77, под. А, кв. 19, р-н Триадица, София 1408, Болгария\nЭлектронная почта: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "о вашем решении отказаться от настоящего договора посредством недвусмысленного заявления (например, письмом, отправленным по почте или по электронной почте).",
    },
    "sk": {
        "pdf.how_to_withdrawal_text": "Na uplatnenie práva na odstúpenie od zmluvy nás musíte informovať:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" s.r.o.</b>\nobchodujúca ako <b>Nevumo</b>\n77 Petko Karavelov Blvd., vchod A, byt 19, obvod Triadica, Sofia 1408, Bulharsko\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "o svojom rozhodnutí odstúpiť od tejto zmluvy jednoznačným vyhlásením (napr. listom zaslaným poštou alebo e-mailom).",
    },
    "sl": {
        "pdf.how_to_withdrawal_text": "Za uveljavljanje pravice do odstopa nas morate obvestiti:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" d.o.o.</b>\nki posluje kot <b>Nevumo</b>\n77 Petko Karavelov Blvd., Vhod A, Stan. 19, Okrožje Triadica, Sofija 1408, Bolgarija\nE-pošta: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "o svoji odločitvi, da odstopate od te pogodbe, z nedvoumno izjavo (npr. s pismom, poslanim po pošti ali e-pošti).",
    },
    "sq": {
        "pdf.how_to_withdrawal_text": "Për të ushtruar të drejtën e tërheqjes, duhet të na informoni:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nduke tregtuar si <b>Nevumo</b>\n77 Petko Karavelov Blvd., Hyrja A, Apt. 19, Distrikti Triadica, Sofje 1408, Bullgari\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "për vendimin tuaj për t'u tërhequr nga kjo kontratë me anë të një deklarate të qartë (p.sh. një letër e dërguar me postë ose e-mail).",
    },
    "sr": {
        "pdf.how_to_withdrawal_text": "Da biste ostvarili pravo na odustanak, morate nas obavestiti:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" d.o.o.</b>\nposluje kao <b>Nevumo</b>\n77 Petko Karavelov Blvd., Ulaz A, Stan 19, Triadica, Sofija 1408, Bugarska\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "o svojoj odluci da odustanete od ovog ugovora nedvosmislenom izjavom (npr. pismom poslatim poštom ili e-poštom).",
    },
    "sv": {
        "pdf.how_to_withdrawal_text": "För att utöva ångerrätten måste du informera oss:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nsom verkar under namnet <b>Nevumo</b>\n77 Petko Karavelov Blvd., Ingång A, Lgh 19, Distriktet Triadica, Sofia 1408, Bulgarien\nE-post: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "om ditt beslut att frånträda detta avtal genom ett entydigt meddelande (t.ex. ett brev skickat per post eller e-post).",
    },
    "tr": {
        "pdf.how_to_withdrawal_text": "Cayma hakkını kullanmak için bizi bilgilendirmelisiniz:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\n<b>Nevumo</b> olarak faaliyet gösteren\n77 Petko Karavelov Blvd., Giriş A, Daire 19, Triadica Bölgesi, Sofya 1408, Bulgaristan\nE-posta: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "bu sözleşmeden cayma kararınızı açık bir beyanla (örneğin posta veya e-posta yoluyla gönderilen bir mektup) bildirmelisiniz.",
    },
    "uk": {
        "pdf.how_to_withdrawal_text": "Щоб скористатися правом на відмову від договору, ви повинні повідомити нас:",
        "pdf.company_address_block": "<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nпід торговою маркою <b>Nevumo</b>\nбул. Петко Каравелов 77, під. А, кв. 19, р-н Тріадіца, Софія 1408, Болгарія\nЕлектронна пошта: <b>legal@nevumo.com</b>",
        "pdf.how_to_withdrawal_text_part2": "про своє рішення відмовитися від цього договору за допомогою однозначної заяви (наприклад, листом, надісланим поштою або електронною поштою).",
    },
}


if __name__ == "__main__":
    main()
