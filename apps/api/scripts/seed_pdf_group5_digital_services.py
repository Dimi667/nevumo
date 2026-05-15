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
        WHERE key LIKE 'pdf.digital_services_%'
        GROUP BY lang
        ORDER BY lang
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} keys")

ALL_TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "pdf.digital_services_title": "Digital services",
        "pdf.digital_services_text": "If the contract concerns the supply of digital content not supplied on a tangible medium, the withdrawal period shall expire after 14 days from the day of the conclusion of the contract.",
        "pdf.digital_services_text_part2": "To exercise the right of withdrawal, you must inform us of your decision to withdraw from this contract before the expiry of the withdrawal period by an unequivocal statement (e.g., a letter sent by post or e-mail).",
    },
    "bg": {
        "pdf.digital_services_title": "Цифрови услуги",
        "pdf.digital_services_text": "Ако договорът се отнася до доставка на цифрово съдържание, не доставено на материален носител, срокът за отказ изтича след 14 дни от деня на сключване на договора.",
        "pdf.digital_services_text_part2": "За да упражните правото на отказ, трябва да ни уведомите за решението си да се откажете от договора преди изтичането на срока за отказ чрез недвусмислено заявление (например писмо, изпратено по пощата или имейл).",
    },
    "pl": {
        "pdf.digital_services_title": "Usługi cyfrowe",
        "pdf.digital_services_text": "Jeżeli umowa dotyczy dostarczania treści cyfrowych nie dostarczanych na nośniku materialnym, termin do odstąpienia od umowy wygasa po upływie 14 dni od dnia zawarcia umowy.",
        "pdf.digital_services_text_part2": "Aby skorzystać z prawa odstąpienia od umowy, muszą Państwo poinformować nas o swojej decyzji o odstąpieniu od niniejszej umowy przed upływem terminu do odstąpienia od umowy v drodze jednoznacznego oświadczenia (na przykład pismo wysłane pocztą lub pocztą elektroniczną).",
    },
    "cs": {
        "pdf.digital_services_title": "Digitální služby",
        "pdf.digital_services_text": "Týká-li se smlouva dodání digitálního obsahu, který není dodán na hmotném nosiči, uplyne lhůta pro odstoupení od smlouvy po 14 dnech ode dne uzavření smlouvy.",
        "pdf.digital_services_text_part2": "Pro uplatnění práva na odstoupení od smlouvy nás musíte o svém rozhodnutí odstoupit od této smlouvy informovat před uplynutím lhůty pro odstoupení od smlouvy formou jednoznačného prohlášení (např. dopisem zaslaným poštou nebo e-mailem).",
    },
    "da": {
        "pdf.digital_services_title": "Digitale tjenester",
        "pdf.digital_services_text": "Hvis kontrakten vedrører levering af digitalt indhold, som ikke leveres på et fysisk medium, udløber fortrydelsesfristen 14 dage efter dagen for kontraktens indgåelse.",
        "pdf.digital_services_text_part2": "For at udøve fortrydelsesretten skal du informere os om din beslutning om at trække dig ud af denne kontrakt inden fortrydelsesfristens udløb ved en utvetydig erklæring (f.eks. et brev sendt med post eller e-mail).",
    },
    "de": {
        "pdf.digital_services_title": "Digitale Dienste",
        "pdf.digital_services_text": "Betrifft der Vertrag die Lieferung von digitalen Inhalten, die nicht auf einem körperlichen Datenträger geliefert werden, läuft die Widerrufsfrist nach 14 Tagen ab dem Tag des Vertragsabschlusses ab.",
        "pdf.digital_services_text_part2": "Um Ihr Widerrufsrecht auszuüben, müssen Sie uns vor Ablauf der Widerrufsfrist mittels einer eindeutigen Erklärung (z. B. ein mit der Post versandter Brief oder eine E-Mail) über Ihren Entschluss, diesen Vertrag zu widerrufen, informieren.",
    },
    "el": {
        "pdf.digital_services_title": "Ψηφιακές υπηρεσίες",
        "pdf.digital_services_text": "Εάν η σύμβαση αφορά την προμήθεια ψηφιακού περιεχομένου που δεν παρέχεται σε υλικό μέσο, η προθεσμία υπαναχώρησης λήγει 14 ημέρες μετά την ημέρα σύναψης της σύμβασης.",
        "pdf.digital_services_text_part2": "Για να ασκήσετε το δικαίωμα υπαναχώρησης, πρέπει να μας ενημερώσετε για την απόφασή σας να υπαναχωρήσετε από την παρούσα σύμβαση πριν από τη λήξη της προθεσμίας υπαναχώρησης με μια σαφή δήλωση (π.χ. επιστολή που αποστέλλεται ταχυδρομικώς ή μέσω e-mail).",
    },
    "es": {
        "pdf.digital_services_title": "Servicios digitales",
        "pdf.digital_services_text": "Si el contrato se refiere al suministro de contenido digital que no se preste en soporte material, el plazo de desistimiento expirará a los 14 días del día de la celebración del contrato.",
        "pdf.digital_services_text_part2": "Para ejercer el derecho de desistimiento, deberá notificarnos su decisión de desistir del presente contrato antes de que expire el plazo de desistimiento a través de una declaración inequívoca (por ejemplo, una carta enviada por correo postal o por correo electrónico).",
    },
    "et": {
        "pdf.digital_services_title": "Digiteenused",
        "pdf.digital_services_text": "Kui leping puudutab sellise digitaalse sisu edastamist, mida ei toimetata kätte füüsilisel andmekandjal, lõpeb taganemistähtaeg 14 päeva möödumisel lepingu sõlmimisest.",
        "pdf.digital_services_text_part2": "Taganemisõiguse kasutamiseks peate meid teavitama oma otsusest lepingust taganeda enne taganemistähtaja möödumist ühemõttelise avaldusega (nt posti või e-postiga saadetud kiri).",
    },
    "fi": {
        "pdf.digital_services_title": "Digitaaliset palvelut",
        "pdf.digital_services_text": "Jos sopimus koskee sellaisen digitaalisen sisällön toimittamista, jota ne toimiteta aineellisella välineellä, peruuttamisaika päättyy 14 päivän kuluttua sopimuksen tekemisestä.",
        "pdf.digital_services_text_part2": "Peruuttamisoikeuden käyttämiseksi sinun on ilmoitettava meille päätöksestäsi peruuttaa sopimus ennen peruuttamisajan päättymistä yksiselitteisellä ilmoituksella (esim. postitse tai sähköpostilla lähetetyllä kirjeellä).",
    },
    "fr": {
        "pdf.digital_services_title": "Services numériques",
        "pdf.digital_services_text": "Si le contrat concerne la fourniture d'un contenu numérique non fourni sur un support matériel, le délai de rétractation expire 14 jours après le jour de la conclusion du contrat.",
        "pdf.digital_services_text_part2": "Pour exercer le droit de rétractation, vous devez nous informer de votre décision de vous rétracter du présent contrat avant l'expiration du délai de rétractation par une déclaration dénuée d'ambiguïté (par exemple, une lettre envoyée par la poste ou par e-mail).",
    },
    "ga": {
        "pdf.digital_services_title": "Seirbhísí digiteacha",
        "pdf.digital_services_text": "Más rud é go mbaineann an conradh le soláthar ábhair dhigitigh nach soláthraítear ar mheán inbhraite, rachaidh an tréimhse tarraingt siar in éag tar éis 14 lá ón lá a tugadh an conradh i gcrích.",
        "pdf.digital_services_text_part2": "Chun an ceart tarraingt siar a fheidhmiú, ní mór duit do chinneadh tarraingt siar as an gconradh seo a chur in iúl dúinn sula n-éagfaidh an tréimhse tarraingt siar trí ráiteas soiléir (m.sh. litir a sheoltar tríd an bpost nó trí ríomhphost).",
    },
    "hr": {
        "pdf.digital_services_title": "Digitalne usluge",
        "pdf.digital_services_text": "Ako se ugovor odnosi na isporuku digitalnog sadržaja koji nije isporučen na materijalnom nosaču, rok za odustajanje istječe nakon 14 dana od dana sklapanja ugovora.",
        "pdf.digital_services_text_part2": "Kako biste ostvarili pravo na odustajanje, morate nas obavijestiti o svojoj odluci o odustajanju od ovog ugovora prije isteka roka za odustajanje nedvosmislenom izjavom (npr. pismom poslanim poštom ili e-poštom).",
    },
    "hu": {
        "pdf.digital_services_title": "Digitális szolgáltatások",
        "pdf.digital_services_text": "Ha a szerződés nem tárgyi adathordozón nyújtott digitális adattartalom szolgáltatására vonatkozik, az elállási határidő a szerződés megkötésének napjától számított 14 nap elteltével jár le.",
        "pdf.digital_services_text_part2": "Az elállási jog gyakorlásához Önnek az elállási határidő lejárta előtt egyértelmű nyilatkozatban (pl. postán küldött levélben oder e-mailben) kell tájékoztatnia minket a szerződéstől való elállási szándékáról.",
    },
    "is": {
        "pdf.digital_services_title": "Stafræn þjónusta",
        "pdf.digital_services_text": "Ef samningurinn varðar afhendingu á stafrænu efni sem er ekki afhent á áþreifanlegum miðli, rennur frestur til að falla frá samningi út 14 dögum eftir þann dag sem samningurinn var gerður.",
        "pdf.digital_services_text_part2": "Til að nýta réttinn til að falla frá samningi verður þú að láta okkur vita af ákvörðun þinni um að falla frá þessum samningi áður en fresturinn rennur út með ótvíræðri yfirlýsingu (t.d. með bréfi sent með pósti eða tölvupósti).",
    },
    "it": {
        "pdf.digital_services_title": "Servizi digitali",
        "pdf.digital_services_text": "Se il contratto riguarda la fornitura di contenuto digitale non fornito su un supporto materiale, il periodo di recesso scade dopo 14 giorni dal giorno della conclusione del contratto.",
        "pdf.digital_services_text_part2": "Per esercitare il diritto di recesso, è tenuto a informarci della sua decisione di recedere dal presente contratto prima della scadenza del periodo di recesso tramite una dichiarazione esplicita (ad esempio lettera inviata per posta o posta elettronica).",
    },
    "lb": {
        "pdf.digital_services_title": "Digitale Servicer",
        "pdf.digital_services_text": "Wann de Vertrag d'Liwwerung vun digitalen Inhalter betrëfft, déi net op engem kierperlechen Datenträger geliwwert ginn, leeft d'Widerrufsfrist no 14 Deeg ab dem Dag vum Vertragsoschlëss of.",
        "pdf.digital_services_text_part2": "Fir Äert Widerrufsrecht auszeüben, musst Dir eis virum Oflaf vun der Widerrufsfrist iwwer Är Entscheedung, dëse Vertrag ze widderruffen, mat enger kloerer Erklärung (z. B. e Bréif per Post oder eng E-Mail) informéieren.",
    },
    "lt": {
        "pdf.digital_services_title": "Skaitmeninės paslaugos",
        "pdf.digital_services_text": "Jei sutartis susijusi su skaitmeninio turinio, kuris netiekiamas materialioje laikmenoje, teikimu, sutarties atsisakymo laikotarpis baigiasi po 14 dienų nuo sutarties sudarymo dienos.",
        "pdf.digital_services_text_part2": "Norėdami pasinaudoti teise atsisakyti sutarties, turite mus informuoti apie savo sprendimą atsisakyti šios sutarties nepasibaigus sutarties atsisakymo laikotarpiui nedviprasmišku pareiškimu (pvz., paštu išsiųstu laišku arba el. paštu).",
    },
    "lv": {
        "pdf.digital_services_title": "Digitālie pakalpojumi",
        "pdf.digital_services_text": "Ja līgums attiecas uz tāda digitālā satura piegādi, kas netiek piegādāts materiālā datu nesējā, atteikuma termiņš beidzas pēc 14 dienām no līguma noslēgšanas dienas.",
        "pdf.digital_services_text_part2": "Lai izmantotu atteikuma tiesības, jums par savu lēmumu atteikties no šī līguma ir jāinformē mūs pirms atteikuma termiņa beigām ar nepārprotamu paziņojumu (piemēram, pa pastu nosūtītu vēstuli vai e-pastu).",
    },
    "me": {
        "pdf.digital_services_title": "Digitalne usluge",
        "pdf.digital_services_text": "Ako se ugovor odnosi na isporuku digitalnog sadržaja koji nije isporučen na trajnom mediju, rok za odustanak ističe nakon 14 dana od dana zaključenja ugovora.",
        "pdf.digital_services_text_part2": "Da biste ostvarili pravo na odustanak, morate nas obavijestiti o svojoj odluci da odustanete od ovog ugovora prije isteka roka za odustanak nedvosmislenom izjavom (npr. pismom poslatim poštom ili e-mailom).",
    },
    "mk": {
        "pdf.digital_services_title": "Дигитални услуги",
        "pdf.digital_services_text": "Ако договорот се однесува на испорака на дигитална содржина која не е доставена на материјален медиум, рокот за повлекување истекува по 14 дена од денот на склучување на договорот.",
        "pdf.digital_services_text_part2": "За да го остварите правото на повлекување, мора да нè информирате за вашата одлука за повлекување од овој договор пред истекот на рокот за повлекување со недвосмислена изјава (на пр. писмо испратено по пошта или е-пошта).",
    },
    "mt": {
        "pdf.digital_services_title": "Servizzi diġitali",
        "pdf.digital_services_text": "Jekk il-kuntratt jikkonċerna l-provvista ta' kontenut diġitali li mhuwiex fornut fuq mezz tanġibbli, il-perjodu ta' rtirar jiskadi wara 14-il jum mill-jum tal-konklużjoni tal-kuntratt.",
        "pdf.digital_services_text_part2": "Sabiex teżerċita d-dritt ta' rtirar, inti trid tinfurmana bid-deċiżjoni tiegħek li tirtira minn dan il-kuntratt qabel l-iskadenza tal-perjodu ta' rtirar b'dikjarazzjoni ċara (eż. ittra mibgħuta bil-posta jew bl-e-mail).",
    },
    "nl": {
        "pdf.digital_services_title": "Digitale diensten",
        "pdf.digital_services_text": "Indien de overeenkomst de levering van digitale inhoud betreft die niet op een materiële drager wordt geleverd, verstrijkt de herroepingstermijn 14 dagen na de dag waarop de overeenkomst is gesloten.",
        "pdf.digital_services_text_part2": "Om het herroepingsrecht uit te oefenen, moet u ons voor het verstrijken van de herroepingstermijn via een ondubbelzinnige verklaring (bv. schriftelijk per post of e-mail) op de hoogte stellen van uw beslissing de overeenkomst te herroepen.",
    },
    "no": {
        "pdf.digital_services_title": "Digitale tjenester",
        "pdf.digital_services_text": "Dersom kontrakten gjelder levering av digitalt innhold som ikke leveres på et fysisk medium, utløper angrefristen 14 dager etter dagen for avtaleinngåelse.",
        "pdf.digital_services_text_part2": "For å utøve angreretten må du informere oss om din beslutning om å gå fra denne kontrakten før angrefristen utløper ved en utvetydig erklæring (f.eks. et brev sendt per post eller e-post).",
    },
    "pt": {
        "pdf.digital_services_title": "Serviços digitais",
        "pdf.digital_services_text": "Se o contrato disser respeito ao fornecimento de conteúdos digitais não fornecidos num suporte material, o prazo de livre resolução expira após 14 dias a contar do dia da celebração do contrato.",
        "pdf.digital_services_text_part2": "Para exercer o seu direito de livre resolução, tem de nos comunicar a sua decisão de resolução do presente contrato antes do termo do prazo de resolução por meio de uma declaração inequívoca (por exemplo, carta enviada pelo correio ou correio eletrónico).",
    },
    "ro": {
        "pdf.digital_services_title": "Servicii digitale",
        "pdf.digital_services_text": "În cazul în care contractul vizează furnizarea de conținut digital care nu este livrat pe un suport material, perioada de retragere expiră după 14 zile de la data încheierii contractului.",
        "pdf.digital_services_text_part2": "Pentru a vă exercita dreptul de retragere, trebuie să ne informați cu privire la decizia dumneavoastră de a vă retrage din prezentul contract înainte de expirarea perioadei de retragere, prin intermediul unei declarații neechivoce (de exemplu, o scrisoare trimisă prin poștă sau e-mail).",
    },
    "ru": {
        "pdf.digital_services_title": "Цифровые услуги",
        "pdf.digital_services_text": "Если договор касается предоставления цифрового контента не на материальном носителе, срок отказа истекает через 14 дней со дня заключения договора.",
        "pdf.digital_services_text_part2": "Чтобы воспользоваться правом на отказ, вы должны уведомить нас о своем решении отказаться от этого договора до истечения срока отказа посредством недвусмысленного заявления (например, письмом, отправленным по почте или электронной почте).",
    },
    "sk": {
        "pdf.digital_services_title": "Digitálne služby",
        "pdf.digital_services_text": "Ak sa zmluva týka dodávania digitálneho obsahu inak ako na hmotnom nosiči, lehota na odstúpenie od zmluvy uplynie po 14 dňoch odo dňa uzavretia zmluvy.",
        "pdf.digital_services_text_part2": "Na uplatnenie práva na odstúpenie od zmluvy nás musíte o svojom rozhodnutí odstúpiť od tejto zmluvy informovať pred uplynutím lehoty na odstúpenie od zmluvy jednoznačným vyhlásením (napr. listom zaslaným poštou alebo e-mailom).",
    },
    "sl": {
        "pdf.digital_services_title": "Digitalne storitve",
        "pdf.digital_services_text": "Če se pogodba nanaša na dobavo digitalne vsebine, ki ni dostavljena na otipljivem nosilcu, odstopni rok poteče po 14 dneh od dneva sklenitve pogodbe.",
        "pdf.digital_services_text_part2": "Za uveljavljanje pravice do odstopa nas morate o svoji odločitvi o odstopu od te pogodbe pred iztekom odstopnega roka obvestiti z nedvoumno izjavo (npr. s pismom, poslanim po pošti ali e-pošti).",
    },
    "sq": {
        "pdf.digital_services_title": "Shërbime digjitale",
        "pdf.digital_services_text": "Nëse kontrata ka të bëjë me furnizimin e përmbajtjes digjitale që nuk jepet në një medium fizik, afati i tërheqjes përfundon pas 14 ditësh nga dita e lidhjes së kontratës.",
        "pdf.digital_services_text_part2": "Për të ushtruar të drejtën e tërheqjes, duhet të na njoftoni për vendimin tuaj për t'u tërhequr nga kjo kontratë para përfundimit të afatit të tërheqjes me anë të një deklarate të qartë (p.sh. një letër e dërguar me postë ose e-mail).",
    },
    "sr": {
        "pdf.digital_services_title": "Digitalne usluge",
        "pdf.digital_services_text": "Ako se ugovor odnosi na isporuku digitalnog sadržaja koji nije isporučen na trajnom nosaču, rok za odustanak ističe nakon 14 dana od dana zaključenja ugovora.",
        "pdf.digital_services_text_part2": "Da biste ostvarili pravo na odustanak, morate nas obavestiti o svojoj odluci da odustanete od ovog ugovora pre isteka roka za odustanak nedvosmislenom izjavom (npr. pismom poslatim poštom ili e-mailom).",
    },
    "sv": {
        "pdf.digital_services_title": "Digitala tjänster",
        "pdf.digital_services_text": "Om avtalet avser tillhandahållande av digitalt innehåll som inte levereras på ett fysiskt medium, löper ångerfristen ut 14 dagar efter den dag då avtalet ingicks.",
        "pdf.digital_services_text_part2": "För att utöva ångerrätten måste du informera oss om ditt beslut att frånträda detta avtal före ångerfristens utgång genom ett tydligt meddelande (t.ex. ett brev skickat per post eller e-post).",
    },
    "tr": {
        "pdf.digital_services_title": "Dijital hizmetler",
        "pdf.digital_services_text": "Sözleşme, maddi bir ortamda sunulmayan dijital içeriğin sağlanmasına ilişkinse, cayma süresi sözleşmenin kurulduğu günden itibaren 14 gün sonra sona erer.",
        "pdf.digital_services_text_part2": "Cayma hakkını kullanmak için, cayma süresi dolmadan önce bu sözleşmeden cayma kararınızı açık bir beyanla (örneğin posta veya e-posta yoluyla gönderilen bir mektup) bize bildirmeniz gerekir.",
    },
    "uk": {
        "pdf.digital_services_title": "Цифрові послуги",
        "pdf.digital_services_text": "Якщо договір стосується постачання цифрового контенту не на матеріальному носії, термін відмови закінчується через 14 днів з дня укладення договору.",
        "pdf.digital_services_text_part2": "Щоб скористатися правом на відмова, ви повинні повідомити нас про своє рішення відмовитися від цього договору до закінчення терміну відмови за допомогою однозначної заяви (наприклад, листом, надісланим поштою або електронною поштою).",
    },
    "bs": {
        "pdf.digital_services_title": "Digitalne usluge",
        "pdf.digital_services_text": "Ako se ugovor odnosi na isporuku digitalnog sadržaja koji nije isporučen na trajnom mediju, rok za odustanak ističe nakon 14 dana od dana zaključenja ugovora.",
        "pdf.digital_services_text_part2": "Da biste ostvarili pravo na odustanak, morate nas obavijestiti o svojoj odluci da odustanete od ovog ugovora prije isteka roka za odustanak nedvosmislenom izjavom (npr. pismom poslatim poštom ili e-mailom).",
    },
}

if __name__ == "__main__":
    main()
