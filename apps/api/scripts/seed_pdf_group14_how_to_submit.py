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
        WHERE key LIKE 'pdf.how_to_submit_%'
        GROUP BY lang
        ORDER BY lang
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} keys")

ALL_TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "pdf.how_to_submit_title": "HOW TO SUBMIT THIS FORM",
        "pdf.how_to_submit_electronic": "<b>Electronically (recommended):</b> Complete the form and send it to <b>legal@nevumo.com</b> with the subject line: \"Withdrawal from contract\".",
        "pdf.how_to_submit_post": "<b>By post:</b> Print, sign and send to: \"FILIPHS TSENTAR BULGARIA\" Ltd, 77 Petko Karavelov Blvd., Entrance A, Apt. 19, Triadica District, Sofia 1408, Bulgaria.",
        "pdf.how_to_submit_acknowledgement": "<b>Acknowledgement:</b> We will communicate to you an acknowledgement of receipt of such a withdrawal on a durable medium (e-mail) without delay.",
    },
    "bg": {
        "pdf.how_to_submit_title": "КАК ДА ИЗПРАТИТЕ ФОРМУЛЯРА?",
        "pdf.how_to_submit_electronic": "<b>По електронен път (препоръчително):</b> Попълнете формуляра и го изпратете на <b>legal@nevumo.com</b> с тема: „Отказ от договор“.",
        "pdf.how_to_submit_post": "<b>По пощата:</b> Отпечатайте, подпишете и изпратете на адрес: „ФИЛИПС ЦЕНТЪР БЪЛГАРИЯ“ ООД, бул. Петко Каравелов бл. 77, вх. А, ап. 19, р-н Триадица, п.к. 1408, гр. София, България.",
        "pdf.how_to_submit_acknowledgement": "<b>Потвърждение:</b> Ще потвърдим незабавно получаването на отказа на траен носител (имейл).",
    },
    "cs": {
        "pdf.how_to_submit_title": "JAK TENTO FORMULÁŘ ODESLAT",
        "pdf.how_to_submit_electronic": "<b>Elektronicky (doporučeno):</b> Vyplňte formulář a zašlete jej na adresu <b>legal@nevumo.com</b> s předmětem: „Odstoupení od smlouvy“.",
        "pdf.how_to_submit_post": "<b>Poštou:</b> Vytiskněte, podepište a zašlete na adresu: „PHILIPS CENTER BULGARIA“ OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulharsko.",
        "pdf.how_to_submit_acknowledgement": "<b>Potvrzení:</b> Bezodkladně vám potvrdíme přijetí takového odstoupení na trvalém nosiči (e-mailem).",
    },
    "da": {
        "pdf.how_to_submit_title": "SÅDAN INDSENDES DENNE FORMULAR",
        "pdf.how_to_submit_electronic": "<b>Elektronisk (anbefales):</b> Udfyld formularen og send den til <b>legal@nevumo.com</b> med emnelinjen: \"Fortrydelse af kontrakt\".",
        "pdf.how_to_submit_post": "<b>Med post:</b> Udskriv, underskriv og send til: \"PHILIPS CENTER BULGARIA\" OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Danmark.",
        "pdf.how_to_submit_acknowledgement": "<b>Bekræftelse:</b> Vi vil straks sende dig en bekræftelse på modtagelse af en sådan fortrydelse på et varigt medium (e-mail).",
    },
    "de": {
        "pdf.how_to_submit_title": "SO REICHEN SIE DIESES FORMULAR EIN",
        "pdf.how_to_submit_electronic": "<b>Elektronisch (empfohlen):</b> Füllen Sie das Formular aus und senden Sie es an <b>legal@nevumo.com</b> mit dem Betreff: „Widerruf vom Vertrag“.",
        "pdf.how_to_submit_post": "<b>Per Post:</b> Drucken, unterschreiben und senden an: „PHILIPS CENTER BULGARIA“ OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgarien.",
        "pdf.how_to_submit_acknowledgement": "<b>Bestätigung:</b> Wir werden Ihnen unverzüglich eine Bestätigung über den Eingang eines solchen Widerrufs auf einem dauerhaften Datenträger (E-Mail) übermitteln.",
    },
    "el": {
        "pdf.how_to_submit_title": "ΠΩΣ ΝΑ ΥΠΟΒΑΛΕΤΕ ΑΥΤΟ ΤΟ ΕΝΤΥΠΟ",
        "pdf.how_to_submit_electronic": "<b>Ηλεκτρονικά (συνιστάται):</b> Συμπληρώστε το έντυπο και στείλτε το στο <b>legal@nevumo.com</b> με θέμα: \"Υπαναχώρηση από τη σύμβαση\".",
        "pdf.how_to_submit_post": "<b>Ταχυδρομικώς:</b> Εκτυπώστε, υπογράψτε και στείλτε στη διεύθυνση: \"PHILIPS CENTER BULGARIA\" OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Βουλγαρία.",
        "pdf.how_to_submit_acknowledgement": "<b>Επιβεβαίωση:</b> Θα σας διαβιβάσουμε χωρίς καθυστέρηση επιβεβαίωση παραλαβής αυτής της υπαναχώρησης σε σταθερό μέσο (e-mail).",
    },
    "es": {
        "pdf.how_to_submit_title": "CÓMO ENVIAR ESTE FORMULARIO",
        "pdf.how_to_submit_electronic": "<b>Electrónicamente (recomendado):</b> Complete el formulario y envíelo a <b>legal@nevumo.com</b> con el asunto: \"Desistimiento del contrato\".",
        "pdf.how_to_submit_post": "<b>Por correo:</b> Imprima, firme y envíe a: \"PHILIPS CENTER BULGARIA\" OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria.",
        "pdf.how_to_submit_acknowledgement": "<b>Acuse de recibo:</b> Le comunicaremos sin demora un acuse de recibo de dicho desistimiento en un soporte duradero (correo electrónico).",
    },
    "et": {
        "pdf.how_to_submit_title": "KUIDAS SEDA VORMI ESITADA",
        "pdf.how_to_submit_electronic": "<b>Elektrooniliselt (soovitatav):</b> Täitke vorm ja saatke see aadressile <b>legal@nevumo.com</b> märksõnaga: \"Lepingust taganemine\".",
        "pdf.how_to_submit_post": "<b>Postiga:</b> Prindi, allkirjasta ja saada aadressile: \"PHILIPS CENTER BULGARIA\" OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaaria.",
        "pdf.how_to_submit_acknowledgement": "<b>Kinnitamine:</b> Edastame teile viivitamata kinnituse sellise taganemisteate kättesaamise kohta püsival andmekandjal (e-posti teel).",
    },
    "fi": {
        "pdf.how_to_submit_title": "KUINKA TÄMÄ LOMAKE TOIMITETAAN",
        "pdf.how_to_submit_electronic": "<b>Sähköisesti (suositus):</b> Täytä lomake ja lähetä se osoitteeseen <b>legal@nevumo.com</b> aiheella: \"Sopimuksen peruuttaminen\".",
        "pdf.how_to_submit_post": "<b>Postitse:</b> Tulosta, allekirjoita ja lähetä osoitteeseen: \"PHILIPS CENTER BULGARIA\" OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria.",
        "pdf.how_to_submit_acknowledgement": "<b>Vastaanottoilmoitus:</b> Ilmoitamme viipymättä peruutuksen vastaanottamisesta pysyvällä tavalla (sähköpostitse).",
    },
    "fr": {
        "pdf.how_to_submit_title": "COMMENT SOUMETTRE CE FORMULAIRE",
        "pdf.how_to_submit_electronic": "<b>Par voie électronique (recommandé) :</b> Remplissez le formulaire et envoyez-le à <b>legal@nevumo.com</b> avec l'objet : « Rétractation du contrat ».",
        "pdf.how_to_submit_post": "<b>Par la poste :</b> Imprimez, signez et envoyez à : \"PHILIPS CENTER BULGARIA\" OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgarie.",
        "pdf.how_to_submit_acknowledgement": "<b>Accusé de réception :</b> Nous vous communiquerons sans délai un accusé de réception de cette rétractation sur un support durable (e-mail).",
    },
    "ga": {
        "pdf.how_to_submit_title": "CONAS AN FOIRM SEO A SHEOLADH",
        "pdf.how_to_submit_electronic": "<b>Go leictreonach (molta):</b> Comhlánaigh an fhoirm agus seol chuig <b>legal@nevumo.com</b> í leis an líne ábhair: \"Tarraingt siar as conradh\".",
        "pdf.how_to_submit_post": "<b>Tríd an bpost:</b> Priontáil, sínigh agus seol chuig: \"PHILIPS CENTER BULGARIA\" OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, an Bhulgáir.",
        "pdf.how_to_submit_acknowledgement": "<b>Admháil:</b> Cuirfimid admháil ar fháil na tarraingthe siar sin in iúl duit gan mhoill ar mheán marthanach (r-phost).",
    },
    "hr": {
        "pdf.how_to_submit_title": "KAKO PODNIJETI OVAJ OBRAZAC",
        "pdf.how_to_submit_electronic": "<b>Elektronički (preporučeno):</b> Ispunite obrazac i pošaljite ga na <b>legal@nevumo.com</b> s naslovom: „Odustajanje od ugovora“.",
        "pdf.how_to_submit_post": "<b>Poštom:</b> Ispišite, potpišite i pošaljite na adresu: „PHILIPS CENTER BULGARIA“ OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofija, Bugarska.",
        "pdf.how_to_submit_acknowledgement": "<b>Potvrda:</b> Bez odgađanja ćemo vam dostaviti potvrdu o primitku takvog odustajanja na trajnom nosaču podataka (e-mail).",
    },
    "hu": {
        "pdf.how_to_submit_title": "HOGYAN KELL BENYÚJTANI EZT A FORMANYOMTATVÁNYT",
        "pdf.how_to_submit_electronic": "<b>Elektronikusan (ajánlott):</b> Töltse ki a nyomtatványt, és küldje el a <b>legal@nevumo.com</b> címre a következő tárggyal: „Elállás a szerződéstől“.",
        "pdf.how_to_submit_post": "<b>Postai úton:</b> Nyomtassa ki, írja alá és küldje el a következő címre: „PHILIPS CENTER BULGARIA“ OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Szófia, Bulgária.",
        "pdf.how_to_submit_acknowledgement": "<b>Visszaigazolás:</b> Az elállás kézhezvételéről haladéktalanul visszaigazolást küldünk Önnek tartós adathordozón (e-mailben).",
    },
    "is": {
        "pdf.how_to_submit_title": "HVERNIG Á AÐ SENDA ÞETTA EYÐUBLAÐ",
        "pdf.how_to_submit_electronic": "<b>Rafrænt (mælt með):</b> Fylltu út eyðublaðið og sendu það á <b>legal@nevumo.com</b> með efnislínunni: „Uppsögn samnings“.",
        "pdf.how_to_submit_post": "<b>Með pósti:</b> Prentaðu út, undirritaðu og sendu til: „PHILIPS CENTER BULGARIA“ OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Búlgaría.",
        "pdf.how_to_submit_acknowledgement": "<b>Staðfesting:</b> Við munum án tafar senda þér staðfestingu á móttöku uppsagnarinnar á varanlegum miðli (tölvupósti).",
    },
    "it": {
        "pdf.how_to_submit_title": "COME INVIARE QUESTO MODULO",
        "pdf.how_to_submit_electronic": "<b>Elettronicamente (raccomandato):</b> Completa il modulo e invialo a <b>legal@nevumo.com</b> con l'oggetto: \"Recesso dal contratto\".",
        "pdf.how_to_submit_post": "<b>Per posta:</b> Stampa, firma e invia a: \"PHILIPS CENTER BULGARIA\" OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria.",
        "pdf.how_to_submit_acknowledgement": "<b>Conferma di ricezione:</b> Le comunicheremo senza indugio una conferma di ricezione di tale recesso su un supporto durevole (e-mail).",
    },
    "lb": {
        "pdf.how_to_submit_title": "WIE DIR DËS FORMULAR AREECHE KENNT",
        "pdf.how_to_submit_electronic": "<b>Elektronesch (recommandéiert):</b> Fëllt de Formular aus a schéckt en op <b>legal@nevumo.com</b> mam Betreff: „Récktrëtt vum Vertrag“.",
        "pdf.how_to_submit_post": "<b>Iwwer Post:</b> Dréckt en aus, ënnerschreift en a schéckt en un: „PHILIPS CENTER BULGARIA“ OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgarien.",
        "pdf.how_to_submit_acknowledgement": "<b>Bestätegung:</b> Mir schécken Iech ouni Verspéidung eng Bestätegung vum Empfang vun dësem Récktrëtt op engem dauerhaften Datenträger (E-Mail).",
    },
    "lt": {
        "pdf.how_to_submit_title": "KAIP PATEIKTI ŠIĄ FORMĄ",
        "pdf.how_to_submit_electronic": "<b>Elektroniniu būdu (rekomenduojama):</b> Užpildykite formą ir nusiųskite ją adresu <b>legal@nevumo.com</b>, nurodydami temą: „Sutarties atsisakymas“.",
        "pdf.how_to_submit_post": "<b>Paštu:</b> Atsispausdinkite, pasirašykite ir siųskite adresu: „PHILIPS CENTER BULGARIA“ OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofija, Bulgarija.",
        "pdf.how_to_submit_acknowledgement": "<b>Patvirtinimas:</b> Nedelsdami patvirtinsime tokio atsisakymo gavimą patvarioje laikmenoje (el. paštu).",
    },
    "lv": {
        "pdf.how_to_submit_title": "KĀ IESNIEGT ŠO VEIDLAPU",
        "pdf.how_to_submit_electronic": "<b>Elektroniski (ieteicams):</b> Aizpildiet veidlapu un nosūtiet to uz <b>legal@nevumo.com</b> ar tematu: \"Atteikšanās no līguma\".",
        "pdf.how_to_submit_post": "<b>Pa pastu:</b> Izdrukājiet, parakstiet un nosūtiet uz: \"PHILIPS CENTER BULGARIA\" OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofija, Bulgārija.",
        "pdf.how_to_submit_acknowledgement": "<b>Apstiprinājums:</b> Mēs nekavējoties paziņosim jums apstiprinājumu par šādas atteikšanās saņemšanu pastāvīgā vidē (e-pastā).",
    },
    "mk": {
        "pdf.how_to_submit_title": "КАКО ДА ГО ПОДНЕСЕТЕ ОВОЈ ФОРМУЛАР",
        "pdf.how_to_submit_electronic": "<b>Електронски (препорачано):</b> Пополнете го формуларот и испратете го на <b>legal@nevumo.com</b> со наслов: „Откажување од договор“.",
        "pdf.how_to_submit_post": "<b>По пошта:</b> Отпечатете, потпишете и испратете на адреса: „ФИЛИПС ЦЕНТАР БЪЛГАРИЯ“ ООД, бул. Петко Каравелов бл. 77, вх. А, ап. 19, р-н Триадица, п.к. 1408, Софија, Бугарија.",
        "pdf.how_to_submit_acknowledgement": "<b>Потврда:</b> Веднаш ќе ви потврдиме приемот на таквото откажување на траен медиум (е-пошта).",
    },
    "mt": {
        "pdf.how_to_submit_title": "KIF GĦANDEK TIRRITORNA DIN IL-FORMOLA",
        "pdf.how_to_submit_electronic": "<b>B'mod elettroniku (rakkomandat):</b> Imla l-formola u ibgħatha lil <b>legal@nevumo.com</b> bis-suġġett: \"Irtirar mill-kuntratt\".",
        "pdf.how_to_submit_post": "<b>Bil-posta:</b> Ipprintja, iffirma u ibgħat lil: \"PHILIPS CENTER BULGARIA\" OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, il-Bulgarija.",
        "pdf.how_to_submit_acknowledgement": "<b>Rikonoxximent:</b> Aħna ser nikkomunikawlek rikonoxximent tal-irċevuta ta' dan l-irtirar fuq mezz durabbli (e-mail) mingħajr dewmien.",
    },
    "nl": {
        "pdf.how_to_submit_title": "HOE DIT FORMULIER IN TE DIENEN",
        "pdf.how_to_submit_electronic": "<b>Elektronisch (aanbevolen):</b> Vul het formulier in en stuur het naar <b>legal@nevumo.com</b> met als onderwerp: \"Herroeping van contract\".",
        "pdf.how_to_submit_post": "<b>Per post:</b> Afdrukken, ondertekenen en verzenden naar: \"PHILIPS CENTER BULGARIA\" OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgarije.",
        "pdf.how_to_submit_acknowledgement": "<b>Ontvangstbevestiging:</b> Wij zullen u onverwijld op een duurzame gegevensdrager (e-mail) een bevestiging van de ontvangst van de herroeping meedelen.",
    },
    "no": {
        "pdf.how_to_submit_title": "HVORDAN SENDE INN DETTE SKJEMAET",
        "pdf.how_to_submit_electronic": "<b>Elektronisk (anbefales):</b> Fyll ut skjemaet og send det til <b>legal@nevumo.com</b> med emnelinjen: \"Angring av kontrakt\".",
        "pdf.how_to_submit_post": "<b>Per post:</b> Skriv ut, signer og send til: \"PHILIPS CENTER BULGARIA\" OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgaria.",
        "pdf.how_to_submit_acknowledgement": "<b>Bekreftelse:</b> Vi vil uten opphold sende deg en bekreftelse på mottak av angremeldingen på et varig medium (e-post).",
    },
    "pl": {
        "pdf.how_to_submit_title": "JAK WYSŁAĆ FORMULARZ?",
        "pdf.how_to_submit_electronic": "<b>Elektronicznie (zalecane):</b> Wypełnij formularz i wyślij go na adres <b>legal@nevumo.com</b> z tytułem wiadomości: „Odstąpienie od umowy”.",
        "pdf.how_to_submit_post": "<b>Pocztą:</b> Wydrukuj, podpisz i wyślij na adres: „PHILIPS CENTER BULGARIA“ OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bułgaria.",
        "pdf.how_to_submit_acknowledgement": "<b>Potwierdzenie:</b> Niezwłocznie potwierdzimy otrzymanie odstąpienia od umowy pocztą elektroniczną.",
    },
    "pt": {
        "pdf.how_to_submit_title": "COMO ENVIAR ESTE FORMULÁRIO",
        "pdf.how_to_submit_electronic": "<b>Eletronicamente (recomendado):</b> Preencha o formulário e envie-o para <b>legal@nevumo.com</b> with the subject: \"Rescisão do contrato\".",
        "pdf.how_to_submit_post": "<b>Por correio:</b> Imprima, assine e envie para: \"PHILIPS CENTER BULGARIA\" OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgária.",
        "pdf.how_to_submit_acknowledgement": "<b>Confirmação:</b> Comunicaremos sem demora o recebimento de tal rescisão em um suporte duradouro (e-mail).",
    },
    "pt-PT": {
        "pdf.how_to_submit_title": "COMO ENVIAR ESTE FORMULÁRIO",
        "pdf.how_to_submit_electronic": "<b>Eletronicamente (recomendado):</b> Preencha o formulário e envie-o para <b>legal@nevumo.com</b> com o assunto: \"Rescisão do contrato\".",
        "pdf.how_to_submit_post": "<b>Por correio:</b> Imprima, assine e envie para: \"PHILIPS CENTER BULGARIA\" OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulgária.",
        "pdf.how_to_submit_acknowledgement": "<b>Aviso de receção:</b> Comunicaremos sem demora um aviso de receção de tal rescisão num suporte duradouro (e-mail).",
    },
    "ro": {
        "pdf.how_to_submit_title": "CUM SE TRIMITE ACEST FORMULAR",
        "pdf.how_to_submit_electronic": "<b>Electronic (recomandat):</b> Completați formularul și trimiteți-l la <b>legal@nevumo.com</b> cu subiectul: „Retragerea din contract”.",
        "pdf.how_to_submit_post": "<b>Prin poștă:</b> Imprimați, semnați și trimiteți la: „PHILIPS CENTER BULGARIA“ OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, România.",
        "pdf.how_to_submit_acknowledgement": "<b>Confirmare de primire:</b> Vă vom comunica fără întârziere confirmarea de primire a unei astfel de retrageri pe un suport durabil (e-mail).",
    },
    "ru": {
        "pdf.how_to_submit_title": "КАК ОТПРАВИТЬ ЭТУ ФОРМУ",
        "pdf.how_to_submit_electronic": "<b>Электронно (рекомендуется):</b> Заполните форму и отправьте ее на <b>legal@nevumo.com</b> с темой: «Расторжение договора».",
        "pdf.how_to_submit_post": "<b>По почте:</b> Распечатайте, подпишите и отправьте по адресу: „PHILIPS CENTER BULGARIA“ OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Болгария.",
        "pdf.how_to_submit_acknowledgement": "<b>Подтверждение:</b> Мы незамедлительно подтвердим получение такого уведомления на долговечном носителе (по электронной почте).",
    },
    "sk": {
        "pdf.how_to_submit_title": "AKO TENTO FORMULÁR ODOSLAŤ",
        "pdf.how_to_submit_electronic": "<b>Elektronicky (odporúčané):</b> Vyplňte formulár a pošlite ho na <b>legal@nevumo.com</b> s predmetom: „Odstúpenie od zmluvy“.",
        "pdf.how_to_submit_post": "<b>Poštou:</b> Vytlačte, podpíšte a pošlite na adresu: „PHILIPS CENTER BULGARIA“ OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Bulharsko.",
        "pdf.how_to_submit_acknowledgement": "<b>Potvrdenie:</b> Bezodkladne vám potvrdíme prijatie takéhoto odstúpenia na trvanlivom nosiči (e-mailom).",
    },
    "sl": {
        "pdf.how_to_submit_title": "KAKO ODDATI TA OBRAZEC",
        "pdf.how_to_submit_electronic": "<b>Elektronsko (priporočeno):</b> Izpolnite obrazec in ga pošljite na <b>legal@nevumo.com</b> z zadevo: „Odstop od pogodbe“.",
        "pdf.how_to_submit_post": "<b>Po pošti:</b> Natisnite, podpišite in pošljite na naslov: „PHILIPS CENTER BULGARIA“ OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofija, Bolgarija.",
        "pdf.how_to_submit_acknowledgement": "<b>Potrdilo:</b> O prejemu takšnega odstopa vam bomo brez odlašanja poslali potrdilo na trajnem nosilcu (e-pošta).",
    },
    "sq": {
        "pdf.how_to_submit_title": "SI TË DORËZONI KËTË FORMULAR",
        "pdf.how_to_submit_electronic": "<b>Elektronikisht (rekomandohet):</b> Plotësoni formularin dhe dërgojeni në <b>legal@nevumo.com</b> me subjektin: \"Tërheqja nga kontrata\".",
        "pdf.how_to_submit_post": "<b>Me postë:</b> Printoni, nënshkruani dhe dërgojeni në: \"PHILIPS CENTER BULGARIA\" OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofje, Bullgari.",
        "pdf.how_to_submit_acknowledgement": "<b>Konfirmimi:</b> Ne do t'ju njoftojmë pa vonesë një konfirmim për marrjen e kësaj tërheqjeje në një mjet të qëndrueshëm (e-mail).",
    },
    "sr": {
        "pdf.how_to_submit_title": "КАКО ДА ПОДНЕСЕТЕ ОВАЈ ФОРМУЛАР",
        "pdf.how_to_submit_electronic": "<b>Електронски (препоручено):</b> Попуните формулар и пошаљите га на <b>legal@nevumo.com</b> са насловом: „Одустанак од уговора“.",
        "pdf.how_to_submit_post": "<b>Поштом:</b> Одштампајте, потпишите и пошаљите на адресу: „PHILIPS CENTER BULGARIA“ OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Софија, Бугарска.",
        "pdf.how_to_submit_acknowledgement": "<b>Потврда:</b> Без одлагања ћемо вам потврдити пријем таквог одустанка на трајном носачу података (е-маил).",
    },
    "sv": {
        "pdf.how_to_submit_title": "HUR DU SKICKAR IN DETTA FORMULÄR",
        "pdf.how_to_submit_electronic": "<b>Elektroniskt (rekommenderas):</b> Fyll i formuläret och skicka det till <b>legal@nevumo.com</b> med ämnesraden: \"Frånträde från avtal\".",
        "pdf.how_to_submit_post": "<b>Per post:</b> Skriv ut, signera och skicka till: \"PHILIPS CENTER BULGARIA\" OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofia, Sverige.",
        "pdf.how_to_submit_acknowledgement": "<b>Bekräftelse:</b> Vi kommer utan dröjsmål att skicka en bekräftelse på mottagandet av ett sådant frånträde på ett varaktigt medium (e-post).",
    },
    "tr": {
        "pdf.how_to_submit_title": "BU FORM NASIL TESLİM EDİLİR",
        "pdf.how_to_submit_electronic": "<b>Elektronik olarak (önerilir):</b> Formu doldurun ve <b>legal@nevumo.com</b> adresine \"Sözleşmeden cayma\" konu başlığıyla gönderin.",
        "pdf.how_to_submit_post": "<b>Posta yoluyla:</b> Yazdırın, imzalayın ve şu adrese gönderin: \"PHILIPS CENTER BULGARIA\" OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Sofya, Bulgaristan.",
        "pdf.how_to_submit_acknowledgement": "<b>Teyit:</b> Cayma bildiriminin tarafımıza ulaştığına dair teyit bilgisini gecikmeksizin kalıcı bir veri taşıyıcısı (e-posta) ile size ileteceğiz.",
    },
    "uk": {
        "pdf.how_to_submit_title": "ЯК ПОДАТИ ЦЮ ФОРМУ",
        "pdf.how_to_submit_electronic": "<b>Електронно (рекомендовано):</b> Заповніть форму та надішліть її на <b>legal@nevumo.com</b> з темою: «Розірвання договору».",
        "pdf.how_to_submit_post": "<b>Поштою:</b> Роздрукуйте, підпишіть та надішліть за адресою: „PHILIPS CENTER BULGARIA“ OOD, bul. Petko Karavelov bl. 77, vh. A, ap. 19, r-n Triaditsa, p.k. 1408, Софія, Болгарія.",
        "pdf.how_to_submit_acknowledgement": "<b>Підтвердження:</b> Ми негайно підтвердимо отримання такої заяви на довговічному носії (електронною поштою).",
    },
}


if __name__ == "__main__":
    main()
