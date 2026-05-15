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
        WHERE key LIKE 'pdf.form_template_%'
        GROUP BY lang
        ORDER BY lang
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} keys")

ALL_TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "pdf.form_template_instruction": "(Complete and return this form only if you wish to withdraw from the contract)",
        "pdf.form_template_to_block": "<b>To:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\ntrading as <b>Nevumo</b>\n77 Petko Karavelov Blvd., Entrance A, Apt. 19, Triadica District, Sofia 1408, Bulgaria\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "I/We (*) hereby give notice that I/We (*) withdraw from my/our (*) contract for the provision of the following service (*):",
    },
    "bg": {
        "pdf.form_template_instruction": "(Попълнете и върнете настоящия формуляр само ако желаете да се откажете от договора)",
        "pdf.form_template_to_block": "<b>До:</b>\n\n<b>„ФИЛИПС ЦЕНТЪР БЪЛГАРИЯ“ ООД</b>\nс търговска марка <b>Nevumo</b>\nбул. Петко Каравелов бл. 77, вх. А, ап. 19, р-н Триадица, п.к. 1408, гр. София, България\nИмейл: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Аз/Ние (*) с настоящото уведомявам/уведомяваме (*), че се отказвам/отказваме (*) от сключения от мен/нас (*) договор за предоставяне на следната услуга (*):",
    },
    "cs": {
        "pdf.form_template_instruction": "(Vyplňte a vraťte tento formulář pouze v případě, že si přejete odstoupit od smlouvy)",
        "pdf.form_template_to_block": "<b>Adresát:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\npodnikající pod obchodní značkou <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, vchod A, byt 19, okres Triadica, PSČ 1408, Sofia, Bulharsko\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Já/My (*) tímto oznamuji/oznamujeme (*), že se vzdávám/vzdáváme (*) smlouvy uzavřené mnou/námi (*) na poskytování následující služby (*):",
    },
    "da": {
        "pdf.form_template_instruction": "(Udfyld og returner denne formular kun, hvis du ønsker at trække dig fra kontrakten)",
        "pdf.form_template_to_block": "<b>Til:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nhandlende under mærket <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, indgang A, lejl. 19, Triadica-distriktet, postnr. 1408, Sofia, Bulgarien\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Jeg/Vi (*) giver herved meddelelse om, at jeg/vi (*) trækker mig/os (*) fra min/vores (*) kontrakt om levering af følgende service (*):",
    },
    "de": {
        "pdf.form_template_instruction": "(Füllen Sie dieses Formular nur aus und geben Sie es nur ab, wenn Sie den Vertrag widerrufen möchten)",
        "pdf.form_template_to_block": "<b>An:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nhandelnd unter der Marke <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, Eingang A, Wohnung 19, Bezirk Triadica, PLZ 1408, Sofia, Bulgarien\nE-Mail: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Ich/Wir (*) teile/teilen (*) hiermit mit, dass ich/wir (*) den von mir/uns (*) geschlossenen Vertrag über die Erbringung der folgenden Dienstleistung (*) widerrufe/widerrufen (*):",
    },
    "el": {
        "pdf.form_template_instruction": "(Συμπληρώστε και επιστρέψτε αυτή τη φόρμα μόνο εάν επιθυμείτε να ανακαλέσετε το συμβόλαιο)",
        "pdf.form_template_to_block": "<b>Προς:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nδιαπραγματεύεται ως <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, είσοδος A, διαμέρισμα 19, περιοχή Triadica, ΤΚ 1408, Σόφια, Βουλγαρία\nΗ-mail: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Εγώ/Εμείς (*) δια του παρόντος δηλώνω/δηλώνουμε (*) ότι ανακαλώ/ανακαλούμε (*) το συμβόλαιο που συνήφθη από εμένα/εμάς (*) για την παροχή της ακόλουθης υπηρεσίας (*):",
    },
    "es": {
        "pdf.form_template_instruction": "(Rellene y devuelva este formulario solo si desea desistir del contrato)",
        "pdf.form_template_to_block": "<b>A:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\noperando bajo la marca <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, entrada A, apto. 19, distrito Triadica, código postal 1408, Sofía, Bulgaria\nCorreo electrónico: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Yo/Nosotros (*) por este medio notificamos (*) que desistimos (*) del contrato celebrado por mí/nosotros (*) para la prestación del siguiente servicio (*):",
    },
    "et": {
        "pdf.form_template_instruction": "(Täitke ja tagastage see vorm ainult siis, kui soovite lepingust taganeda)",
        "pdf.form_template_to_block": "<b>Saaja:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nkaubamärgiga <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, sissekäik A, korter 19, Triadica piirkond, postiindeks 1408, Sofia, Bulgaaria\nE-post: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Mina/Me (*) teatavad (*) käesolevaga, et ma/me (*) taganeme (*) minu/meie (*) poolt sõlmitud teenuse osutamise lepingust (*):",
    },
    "fi": {
        "pdf.form_template_instruction": "(Täytä ja palauta tämä lomake vain, jos haluat peruuttaa sopimuksen)",
        "pdf.form_template_to_block": "<b>Vastaanottaja:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\ntoimii tuotenimellä <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, sisäänkäynti A, huoneisto 19, Triadica-alue, postinumero 1408, Sofia, Bulgaria\nSähköposti: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Minä/Me (*) ilmoitan/ilmoitamme (*) täten, että peruutan/peruutamme (*) minun/meidän (*) tekemäni (*) sopimuksen seuraavan palvelun tarjoamisesta (*):",
    },
    "fr": {
        "pdf.form_template_instruction": "(Complétez et retournez ce formulaire uniquement si vous souhaitez vous rétracter du contrat)",
        "pdf.form_template_to_block": "<b>À:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nopérant sous la marque <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, entrée A, apt. 19, district Triadica, code postal 1408, Sofia, Bulgarie\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Je/Nous (*) notifie/notifions (*) par la presente que je/nous (*) me/nous (*) rétracte/rétractons (*) du contrat conclu par moi/nous (*) pour la prestation du service suivant (*):",
    },
    "ga": {
        "pdf.form_template_instruction": "(Líon agus seol ar ais an fhoirm seo ach amháin má theastaíonn uait an conradh a chealú)",
        "pdf.form_template_to_block": "<b>Chuig:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nag feidhmiú faoin bhrand <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, bealach isteach A, árasán 19, ceantar Triadica, códphoist 1408, Sofia, an Bhulgáir\nR-phost: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Mise/Muid (*) a thugann fógra (*) go bhfuil mé/muid (*) ag fágáil (*) an chonradh a dhéan mé/muid (*) do sholáthar an tseirbhíse seo a leanas (*):",
    },
    "hr": {
        "pdf.form_template_instruction": "(Ispunite i vratite ovaj obrazac samo ako želite odustati od ugovora)",
        "pdf.form_template_to_block": "<b>Primatelju:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nposluje pod markom <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, ulaz A, stan 19, okrug Triadica, poštanski broj 1408, Sofija, Bugarska\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Ja/Mi (*) ovim obavještavam/obavještavamo (*) da odustajem/odustajemo (*) od ugovora zaključenog od mene/nas (*) za pružanje sljedeće usluge (*):",
    },
    "hu": {
        "pdf.form_template_instruction": "(Töltse ki és küldje vissza ezt az űrlapot csak akkor, ha szeretne elállni a szerződéstől)",
        "pdf.form_template_to_block": "<b>Címzett:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nmüködik a <b>Nevumo</b> márka alatt\nbul. Petko Karavelov bl. 77, bejárat A, 19. lakás, Triadica kerület, irányítószám 1408, Szófia, Bulgária\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Én/Mi (*) ezúton értesítem/értesítjük (*), hogy elállok/elállunk (*) az általam/általunk (*) kötött szerződéstől az alábbi szolgáltatás nyújtására vonatkozóan (*):",
    },
    "is": {
        "pdf.form_template_instruction": "(Fylltu út og skildu þessu eyðublaði aðeins ef þú vilt segja upp samninginn)",
        "pdf.form_template_to_block": "<b>Til:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nstarfar undir vörumerkinu <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, inngangur A, íbúð 19, Triadica-hérað, póstnúmer 1408, Sófía, Búlgaría\nTölvupóstur: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Ég/Við (*) tilkynni (*) hér með að ég/við (*) segi (*) upp samningnum sem gerður var af mér/okkur (*) um afhendingu eftirfarandi þjónustu (*):",
    },
    "it": {
        "pdf.form_template_instruction": "(Compilare e restituire questo modulo solo se si desidera recedere dal contratto)",
        "pdf.form_template_to_block": "<b>A:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\noperante con il marchio <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, ingresso A, apt. 19, distretto Triadica, codice postale 1408, Sofia, Bulgaria\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Io/Noi (*) comunico/comunichiamo (*) con la presente che recedo/recediamo (*) dal contratto stipulato da me/noi (*) per la fornitura del seguente servizio (*):",
    },
    "lb": {
        "pdf.form_template_instruction": "(Fëllt dëse Formulaire nëmmen aus a schéckt en zréck, wann Dir vum Vertrag zerécktriede wëllt)",
        "pdf.form_template_to_block": "<b>An:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nhandelnd ënner der Mark <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, Agang A, App. 19, Distrikt Triadica, Postcode 1408, Sofia, Bulgarien\nE-Mail: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Ech/Mir (*) deelen hiermit mat, datt ech/mir (*) den Vertrag iwwer d'Liwwerung vum follgenden Service (*), deen ech/mir (*) ofgeschloss hunn, widderrufe/widderruff (*) :",
    },
    "lt": {
        "pdf.form_template_instruction": "(Šią formą užpildykite ir grąžinkite tik tuo atveju, jei norite atsisakyti sutarties)",
        "pdf.form_template_to_block": "<b>Gavėjas:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nveikia su prekės ženklu <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, įėjimas A, butas 19, Triadica rajonas, pašto kodas 1408, Sofija, Bulgarija\nEl. paštas: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Aš/Mes (*) šiuo pranešame (*), kad atsisakau/atsisakome (*) mano/mūsų (*) sudarytos sutarties dėl šios paslaugos teikimo (*):",
    },
    "lv": {
        "pdf.form_template_instruction": "(Aizpildiet un atgrieziet šo veidlapu tikai tad, ja vēlaties atteikties no līguma)",
        "pdf.form_template_to_block": "<b>Adresāts:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\ndarbojas ar zīmolu <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, ieeja A, dzīv. 19, Triadica rajons, pasta indekss 1408, Sofija, Bulgārija\nE-pasts: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Es/Mēs (*) ar šo paziņoju/paziņojam (*), ka es/mēs (*) atteicamies (*) no mana/mūsu (*) noslēgtā līguma par šāda pakalpojuma sniegšanu (*):",
    },
    "mk": {
        "pdf.form_template_instruction": "(Пополнете и вратете го овој образец само ако сакате да се откажете од договорот)",
        "pdf.form_template_to_block": "<b>До:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nделува под марката <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, влез A, стан 19, Triadica округ, поштенски број 1408, Софија, Бугарија\nЕ-пошта: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Јас/Ние (*) со ова известувам (*), дека се откажувам (*) од договорот заклучен од мене/нас (*) за обезбедување на следната услуга (*):",
    },
    "mt": {
        "pdf.form_template_instruction": "(Imla u ħarreġ din il-formola biss jekk trid tirtira mill-kuntratt)",
        "pdf.form_template_to_block": "<b>Lil:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\ntaħdem taħt il-marka <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, dħul A, apt. 19, distrett Triadica, kodiċi postali 1408, Sofia, Bulgarija\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Jien/Aħna (*) b'dan il-miktub nnotifika (*) li jien/aħna (*) nirtira (*) mill-kuntratt li nkiseb minn jien/aħna (*) għall-provvista tas-servizz li ġej (*):",
    },
    "nl": {
        "pdf.form_template_instruction": "(Vul dit formulier alleen in en stuur het terug als u van het contract wilt afzien)",
        "pdf.form_template_to_block": "<b>Aan:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nwerkzaam onder het merk <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, ingang A, apt. 19, district Triadica, postcode 1408, Sofia, Bulgarije\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Ik/Wij (*) geef/geven (*) hierbij kennis dat ik/wij (*) afzien (*) van het door mij/ons (*) gesloten contract voor het verlenen van de volgende dienst (*):",
    },
    "no": {
        "pdf.form_template_instruction": "(Fyll ut og send tilbake dette skjemaet bare hvis du ønsker å trekke deg fra kontrakten)",
        "pdf.form_template_to_block": "<b>Til:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nopererer under merket <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, inngang A, leilighet 19, Triadica-distriktet, postnummer 1408, Sofia, Bulgaria\nE-post: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Jeg/Vi (*) gir herved melding om at jeg/vi (*) trekker meg/oss (*) fra kontrakten inngått av meg/oss (*) for levering av følgende tjeneste (*):",
    },
    "pl": {
        "pdf.form_template_instruction": "(Formularz ten należy wypełnić i odesłać tylko w przypadku chęci odstąpienia od umowy)",
        "pdf.form_template_to_block": "<b>Adresat:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" OOD</b>\ndziałająca pod marką <b>Nevumo</b>\nbul. Petko Karawełow bl. 77, wch. A, ap. 19, dzielnica Triadica, k.p. 1408, Sofia, Bułgaria\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Ja/My(*) niniejszym informuję/informujemy(*) o moim/naszym(*) odstąpieniu od umowy o świadczenie następującej usługi(*):",
    },
    "pt": {
        "pdf.form_template_instruction": "(Preencha e devolva este formulário apenas se desejar desistir do contrato)",
        "pdf.form_template_to_block": "<b>Para:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\noperando sob a marca <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, entrada A, apt. 19, distrito Triadica, código postal 1408, Sofia, Bulgária\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Eu/Nós (*) por este meio notificamos (*) que desistimos (*) do contrato celebrado por mim/nós (*) para a prestação do seguinte serviço (*):",
    },
    "pt-PT": {
        "pdf.form_template_instruction": "(Preencha e devolva este formulário apenas se desejar desistir do contrato)",
        "pdf.form_template_to_block": "<b>Para:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\noperando sob a marca <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, entrada A, apt. 19, distrito Triadica, código postal 1408, Sofia, Bulgária\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Eu/Nós (*) por este meio notificamos (*) que desistimos (*) do contrato celebrado por mim/nós (*) para a prestação do seguinte serviço (*):",
    },
    "ro": {
        "pdf.form_template_instruction": "(Completați și returnați acest formular doar dacă doriți să renunțați la contract)",
        "pdf.form_template_to_block": "<b>Către:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\noperând sub marca <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, intrare A, apt. 19, districtul Triadica, cod poștal 1408, Sofia, Bulgaria\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Eu/Noi (*) prin aceasta notific/notificăm (*) că renunț/renunțăm (*) la contractul încheiat de mine/noi (*) pentru prestarea următorului serviciu (*):",
    },
    "ru": {
        "pdf.form_template_instruction": "(Заполните и верните данную форму только в том случае, если вы желаете отказаться от договора)",
        "pdf.form_template_to_block": "<b>Кому:</b>\n\n<b>\"ФІЛИПС ЦЕНТР БОЛГАРІЯ\" Ltd</b>\nоперирует под торговой маркой <b>Nevumo</b>\nбул. Петко Караваелов бл. 77, вход А, кв. 19, район Триадица, почтовый индекс 1408, София, Болгария\nЭ-почта: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Я/Мы (*) настоящим уведомляю/уведомляем (*), что отказываюсь/отказываемся (*) от заключённого мною/нами (*) договора об оказании следующей услуги (*):",
    },
    "sk": {
        "pdf.form_template_instruction": "(Vyplňte a vráťte tento formulár len v prípade, že si prajete odstúpiť od zmluvy)",
        "pdf.form_template_to_block": "<b>Adresát:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\npôsobí pod značkou <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, vchod A, byt 19, okres Triadica, PSČ 1408, Sofia, Bulharsko\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Ja/My (*) týmto oznamujem/oznamujeme (*), že sa vzdávam/vzdáváme (*) zmluvy uzavretej mnou/nami (*) na poskytovanie nasledujúcej služby (*):",
    },
    "sl": {
        "pdf.form_template_instruction": "(Izpolnite in vrnite ta obrazec samo, če se želite odpovedati pogodbi)",
        "pdf.form_template_to_block": "<b>Naslovnik:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\ndeluje pod blagovno znamko <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, vhod A, stan 19, okrog Triadica, poštna številka 1408, Sofija, Bolgarija\nE-pošta: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Jaz/Mi (*) s tem obveščam/obveščamo (*), da se odpovedujemo (*) pogodbi, sklenjeni s strani mene/nas (*) za opravljanje naslednje storitve (*):",
    },
    "sq": {
        "pdf.form_template_instruction": "(Plotësoni dhe ktheni këtë formular vetëm nëse dëshironi të tërhiqeni nga kontrata)",
        "pdf.form_template_to_block": "<b>Për:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\noperon nën markën <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, hyrje A, apt. 19, rrethi Triadica, kodi postar 1408, Sofia, Bullgaria\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Unë/Ne (*) me këtë njoftoj (*) se tërhiqem (*) nga kontrata e lidhur nga unë/ne (*) për ofrimin e shërbimit të mëposhtëm (*):",
    },
    "sr": {
        "pdf.form_template_instruction": "(Popunite i vratite ovaj obrazac samo ako želite da se povučete iz ugovora)",
        "pdf.form_template_to_block": "<b>Primaocu:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\ndeluje pod markom <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, ulaz A, stan 19, okrug Triadica, poštanski broj 1408, Sofija, Bugarska\nE-mail: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Ja/Mi (*) ovim obaveštavam (*) da se povlačim (*) iz ugovora zaključenog od mene/nas (*) za pružanje sledeće usluge (*):",
    },
    "sv": {
        "pdf.form_template_instruction": "(Fyll i och skicka tillbaka detta formulär endast om du vill ångra avtalet)",
        "pdf.form_template_to_block": "<b>Till:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\nverksamt under varumärket <b>Nevumo</b>\nbul. Petko Karavelov bl. 77, ingång A, lgh 19, distrikt Triadica, postnummer 1408, Sofia, Bulgarien\nE-post: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Jag/Vi (*) meddelar härmed att jag/vi (*) frånträder mitt/vårt (*) avtal om tillhandahållande av följande tjänst (*):",
    },
    "tr": {
        "pdf.form_template_instruction": "(Bu formu yalnızca sözleşmeden caymak istiyorsanız doldurup geri gönderiniz)",
        "pdf.form_template_to_block": "<b>Alıcı:</b>\n\n<b>\"FILIPHS TSENTAR BULGARIA\" Ltd</b>\n<b>Nevumo</b> markası altında faaliyet göstermektedir\nbul. Petko Karavelov bl. 77, giriş A, daire 19, Triadica bölgesi, posta kodu 1408, Sofya, Bulgaristan\nE-posta: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Ben/Biz (*) bu vesileyle, aşağıdaki hizmetin (*) sağlanmasına yönelik yapmış olduğum/olduğumuz (*) sözleşmeden caydığımı/caydıımızı (*) bildiririm/bildiririz (*):",
    },
    "uk": {
        "pdf.form_template_instruction": "(Заповніть та поверніть цю форму лише у тому випадку, якщо ви бажаєте відмовитися від договору)",
        "pdf.form_template_to_block": "<b>Кому:</b>\n\n<b>\"ФІЛІПС ЦЕНТР БОЛГАРІЯ\" Ltd</b>\nпрацює під торговою маркою <b>Nevumo</b>\nбул. Петко Каравелов бл. 77, вхід А, кв. 19, район Тріадіца, поштовий індекс 1408, Софія, Болгарія\nЕ-пошта: <b>legal@nevumo.com</b>",
        "pdf.form_template_declaration": "Я/Ми (*) цим повідомляю/повідомляємо (*), що відмовляюся/відмовляємося (*) від мого/нашого (*) договору про надання такої послуги (*):",
    },
}


if __name__ == "__main__":
    main()
