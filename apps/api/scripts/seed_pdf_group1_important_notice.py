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
        "pdf.important_notice_title": "⚠️ IMPORTANT NOTICE",
        "pdf.important_notice_text": "This form applies exclusively to the contract concluded between you and <b>Nevumo</b> (the platform operator). <b>It does not apply to contracts between Clients and Service Providers</b> facilitated through the Nevumo platform.",
        "pdf.important_notice_text_part2": "Withdrawal from a contract with a specific Service Provider is governed directly by the terms agreed with that Service Provider.",
    },
    "bg": {
        "pdf.important_notice_title": "⚠️ ВАЖНА БЕЛЕЖКА",
        "pdf.important_notice_text": "Настоящият формуляр се отнася единствено до договора, сключен между вас и <b>Nevumo</b> (оператора на платформата). <b>Не се отнася до договори между Клиенти и Доставчици на услуги</b>, сключени чрез платформата Nevumo.",
        "pdf.important_notice_text_part2": "Отказът от договор с конкретен Доставчик на услуги се урежда пряко от условията, договорени с него.",
    },
    "cs": {
        "pdf.important_notice_title": "⚠️ DŮLEŽITÉ UPOZORNĚNÍ",
        "pdf.important_notice_text": "Tento formulář se vztahuje výhradně na smlouvu uzavřenou mezi vámi a společností <b>Nevumo</b> (provozovatelem platformy). <b>Nevztahuje se na smlouvy mezi klienty a poskytovateli služeb</b> zprostředkované prostřednictvím platformy Nevumo.",
        "pdf.important_notice_text_part2": "Odstoupení od smlouvy s konkrétním poskytovatelem služeb se řídí přímo podmínkami dohodnutými s tímto poskytovatelem.",
    },
    "da": {
        "pdf.important_notice_title": "⚠️ VIGTIG MEDDELELSE",
        "pdf.important_notice_text": "Denne formular gælder udelukkende for den kontrakt, der er indgået mellem dig og <b>Nevumo</b> (platformoperatøren). <b>Den gælder ikke for kontrakter mellem kunder og tjenesteudbydere</b>, der formidles via Nevumo-platformen.",
        "pdf.important_notice_text_part2": "Fortrydelse af en kontrakt med en specifik tjenesteudbyder er direkte styret af de vilkår, der er aftalt med den pågældende tjenesteudbyder.",
    },
    "de": {
        "pdf.important_notice_title": "⚠️ WICHTIGER HINWEIS",
        "pdf.important_notice_text": "Dieses Formular bezieht sich ausschließlich auf den zwischen Ihnen und <b>Nevumo</b> (dem Plattformbetreiber) geschlossenen Vertrag. <b>Es gilt nicht für Verträge zwischen Kunden und Dienstleistern</b>, die über die Nevumo-Plattform vermittelt werden.",
        "pdf.important_notice_text_part2": "Der Rücktritt von einem Vertrag mit einem bestimmten Dienstleister richtet sich direkt nach den mit diesem Dienstleister vereinbarten Bedingungen.",
    },
    "el": {
        "pdf.important_notice_title": "⚠️ ΣΗΜΑΝΤΙΚΗ ΣΗΜΕΙΩΣΗ",
        "pdf.important_notice_text": "Αυτή η φόρμα ισχύει αποκλειστικά για τη σύμβαση που συνάπτεται μεταξύ εσάς και της <b>Nevumo</b> (του διαχειριστή της πλατφόρμας). <b>Δεν ισχύει για συμβάσεις μεταξύ Πελατών και Παρόχων Υπηρεσιών</b> που διευκολύνονται μέσω της πλατφόρμας Nevumo.",
        "pdf.important_notice_text_part2": "Η υπαναχώρηση από σύμβαση με συγκεκριμένο Πάροχο Υπηρεσιών διέπεται απευθείας από τους όρους που έχουν συμφωνηθεί με τον εν λόγω Πάροχο.",
    },
    "es": {
        "pdf.important_notice_title": "⚠️ AVISO IMPORTANTE",
        "pdf.important_notice_text": "Este formulario se aplica exclusivamente al contrato suscrito entre usted y <b>Nevumo</b> (el operador de la plataforma). <b>No se aplica a los contratos entre Clientes y Proveedores de Servicios</b> facilitados a través de la plataforma Nevumo.",
        "pdf.important_notice_text_part2": "El desistimiento de un contrato con un Proveedor de Servicios específico se rige directamente por las condiciones acordadas con dicho proveedor.",
    },
    "et": {
        "pdf.important_notice_title": "⚠️ OLULINE TEADE",
        "pdf.important_notice_text": "See vorm kehtib eranditult teie ja <b>Nevumo</b> (platvormi haldaja) vahel sõlmitud lepingu kohta. <b>See ne kehti klientide ja teenusepakkujate vahelistele lepingutele</b>, mis on sõlmitud Nevumo platvormi kaudu.",
        "pdf.important_notice_text_part2": "Konkreetsest teenusepakkujast lepingust taganemist reguleerivad vahetult selle teenusepakkujaga kokkulepitud tingimused.",
    },
    "fi": {
        "pdf.important_notice_title": "⚠️ TÄRKEÄ ILMOITUS",
        "pdf.important_notice_text": "Tämä lomake koskee ainoastaan sinun ja <b>Nevumon</b> (alustan ylläpitäjä) välistä sopimusta. <b>Se ei koske asiakkaiden ja palveluntarjoajien välisiä sopimuksia</b>, jotka on solmitu Nevumo-alustan kautta.",
        "pdf.important_notice_text_part2": "Sopimuksen peruuttamiseen tietyn palveluntarjoajan kanssa sovelletaan suoraan kyseisen palveluntarjoajan kanssa sovittuja ehtoja.",
    },
    "fr": {
        "pdf.important_notice_title": "⚠️ AVIS IMPORTANT",
        "pdf.important_notice_text": "Ce formulaire s'applique exclusivement au contrat conclu entre vous et <b>Nevumo</b> (l'opérateur de la plateforme). <b>Il ne s'applique pas aux contrats entre Clients et Prestataires de Services</b> facilités par la plateforme Nevumo.",
        "pdf.important_notice_text_part2": "La rétractation d'un contrat avec un Prestataire de Services spécifique est régie directement par les conditions convenues avec ce prestataire.",
    },
    "ga": {
        "pdf.important_notice_title": "⚠️ FÓGRA TÁBHACHTACH",
        "pdf.important_notice_text": "Baineann an fhoirm seo go heisiach leis an gconradh a tugadh i gcrích idir tú féin agus <b>Nevumo</b> (oibreoir an ardáin). <b>Ní bhaineann sé le conarthaí idir Cliaint agus Soláthraithe Seirbhíse</b> a éascaítear trí ardán Nevumo.",
        "pdf.important_notice_text_part2": "Tá tarraingt siar ó chonradh le Soláthraí Seirbhíse sonrach á rialú go díreach ag na téarmaí a comhaontaíodh leis an Soláthraí Seirbhíse sin.",
    },
    "hr": {
        "pdf.important_notice_title": "⚠️ VAŽNA NAPOMENA",
        "pdf.important_notice_text": "Ovaj se obrazac odnosi isključivo na ugovor sklopljen između vas i <b>Nevuma</b> (operatera platforme). <b>Ne odnosi se na ugovore između klijenata i pružatelja usluga</b> sklopljene putem platforme Nevumo.",
        "pdf.important_notice_text_part2": "Odustajanje od ugovora s određenim pružateljem usluga izravno je regulirano uvjetima dogovorenim s tim pružateljem usluga.",
    },
    "hu": {
        "pdf.important_notice_title": "⚠️ FONTOS FIGYELMEZTETÉS",
        "pdf.important_notice_text": "Ez a nyomtatvány kizárólag az Ön és a <b>Nevumo</b> (a platform üzemeltetője) között létrejött szerződésre vonatkozik. <b>Nem vonatkozik az ügyfelek és a szolgáltatók közötti</b>, a Nevumo platformon keresztül létrejött szerződésekre.",
        "pdf.important_notice_text_part2": "Egy adott szolgáltatóval kötött szerződéstől való elállásra közvetlenül az adott szolgáltatóval kötött feltételek az irányadóak.",
    },
    "is": {
        "pdf.important_notice_title": "⚠️ MIKILVÆG TILKYNNING",
        "pdf.important_notice_text": "Þetta eyðublað gildir eingöngu um samninginn sem gerður er á milli þín og <b>Nevumo</b> (rekstraraðila vettvangsins). <b>Það á ekki við um samninga milli viðskiptavina og þjónustuaðila</b> sem gerðir eru í gegnum Nevumo vettvanginn.",
        "pdf.important_notice_text_part2": "Uppsögn samnings við ákveðinn þjónustuaðila fer beint eftir þeim skilmálum sem um var samið við þann þjónustuaðila.",
    },
    "it": {
        "pdf.important_notice_title": "⚠️ AVVISO IMPORTANTE",
        "pdf.important_notice_text": "Il presente modulo si applica esclusivamente al contratto concluso tra l'utente e <b>Nevumo</b> (il gestore della piattaforma). <b>Non si applica ai contratti tra Clienti e Fornitori di Servizi</b> conclusi tramite la piattaforma Nevumo.",
        "pdf.important_notice_text_part2": "Il recesso da un contratto con un Fornitore di Servizi specifico è regolato direttamente dalle condizioni concordate con tale fornitore.",
    },
    "lb": {
        "pdf.important_notice_title": "⚠️ WICHTEGEN HIWEIS",
        "pdf.important_notice_text": "Dëse Formulaire bezitt sech exklusiv op de Kontrakt deen tëscht Iech an <b>Nevumo</b> (dem Bedreiwer vun der Plattform) ofgeschloss gouf. <b>En ass net applicabel op Kontrakter tëscht Clienten a Serviceprovideren</b>, déi iwwer d'Nevumo Plattform vermëttelt ginn.",
        "pdf.important_notice_text_part2": "De Récktrëtt vun engem Kontrakt mat engem spezifesche Serviceprovider gëtt direkt duerch d'Konditioune geregelt, déi mat deem Serviceprovider ausgemaach goufen.",
    },
    "lt": {
        "pdf.important_notice_title": "⚠️ SVARBI INFORMACIJA",
        "pdf.important_notice_text": "Ši forma taikoma tik sutartims, sudarytoms tarp jūsų ir <b>Nevumo</b> (platformos operatoriaus). <b>Ji netaikoma sutartims tarp klientų ir paslaugų teikėjų</b>, sudarytoms per Nevumo platformą.",
        "pdf.important_notice_text_part2": "Sutarties su konkrečiu paslaugų teikėju nutraukimą tiesiogiai reglamentuoja su tuo paslaugų teikėju suderintos sąlygos.",
    },
    "lv": {
        "pdf.important_notice_title": "⚠️ SVARĪGS PAZIŅOJUMS",
        "pdf.important_notice_text": "Šī veidlapa attiecas tikai uz līgumu, kas noslēgts starp jums un <b>Nevumo</b> (platformas operatoru). <b>Tā neattiecas uz līgumiem starp klientiem un pakalpojumu sniedzējiem</b>, kas noslēgti ar Nevumo platformas starpniecību.",
        "pdf.important_notice_text_part2": "Atteikšanos no līguma ar konkrētu pakalpojumu sniedzēju tieši regulē ar šo pakalpojumu sniedzēju saskaņotie noteikumi.",
    },
    "mk": {
        "pdf.important_notice_title": "⚠️ ВАЖНО ИЗВЕСТУВАЊЕ",
        "pdf.important_notice_text": "Овој формулар се однесува исклучиво на договорот склучен помеѓу вас и <b>Nevumo</b> (операторот на платформата). <b>Не се однесува на договорите помеѓу клиентите и добавувачите на услуги</b> склучени преку платформата Nevumo.",
        "pdf.important_notice_text_part2": "Откажувањето од договор со конкретен добавувач на услуги е директно регулирано со условите договорени со тој добавувач.",
    },
    "mt": {
        "pdf.important_notice_title": "⚠️ AVVIŻ IMPORTANTI",
        "pdf.important_notice_text": "Din il-formola tapplika esklussivament għall-kuntratt konkluż bejnek u <b>Nevumo</b> (l-operatur tal-pjattaforma). <b>Ma tapplikax għal kuntratti bejn Klijenti u Fornituri ta' Servizzi</b> ffaċilitati permezz tal-pjattaforma Nevumo.",
        "pdf.important_notice_text_part2": "L-irtirar minn kuntratt ma' Fornitur ta' Servizzi speċifiku huwa rregolat direttament mit-termini miftiehma ma' dak il-Fornitur ta' Servizzi.",
    },
    "nl": {
        "pdf.important_notice_title": "⚠️ BELANGRIJKE MEDEDELING",
        "pdf.important_notice_text": "Dit formulier heeft uitsluitend betrekking op het contract tussen u en <b>Nevumo</b> (de exploitant van het platform). <b>Het is niet van toepassing op contracten tussen klanten en dienstverleners</b> die via het Nevumo-platform tot stand zijn gekomen.",
        "pdf.important_notice_text_part2": "Herroeping van een contract with een specifieke dienstverlener wordt rechtstreeks beheerst door de met die dienstverlener overeengekomen voorwaarden.",
    },
    "no": {
        "pdf.important_notice_title": "⚠️ VIKTIG MELDING",
        "pdf.important_notice_text": "Dette skjemaet gjelder utelukkende for kontrakten inngått mellom deg og <b>Nevumo</b> (plattformoperatøren). <b>Det gjelder ikke for kontrakter mellom kunder og tjenesteleverandører</b> formidlet via Nevumo-plattformen.",
        "pdf.important_notice_text_part2": "Angring av en kontrakt med en spesifikk tjenesteleverandør styres direkte av vilkårene som er avtalt med den aktuelle tjenesteleverandøren.",
    },
    "pl": {
        "pdf.important_notice_title": "⚠️ WAŻNA INFORMACJA",
        "pdf.important_notice_text": "Niniejszy formularz dotyczy wyłącznie umowy zawartej pomiędzy Użytkownikiem a <b>Nevumo</b> (operatorem platformy internetowej). <b>Nie dotyczy umów zawieranych pomiędzy Klientami a Usługodawcami</b> za pośrednictwem platformy Nevumo.",
        "pdf.important_notice_text_part2": "Odstąpienie od umowy z konkretnym Usługodawcą regulowane jest bezpośrednio przez warunki uzgodnione z tym Usługodawcą.",
    },
    "pt": {
        "pdf.important_notice_title": "⚠️ AVISO IMPORTANTE",
        "pdf.important_notice_text": "Este formulário aplica-se exclusivamente ao contrato celebrado entre você e a <b>Nevumo</b> (operadora da plataforma). <b>Não se aplica a contratos entre Clientes e Prestadores de Serviços</b> facilitados através da plataforma Nevumo.",
        "pdf.important_notice_text_part2": "A rescisão de um contrato com um Prestador de Serviços específico é regida diretamente pelos termos acordados com esse prestador.",
    },
    "pt-PT": {
        "pdf.important_notice_title": "⚠️ AVISO IMPORTANTE",
        "pdf.important_notice_text": "Este formulário aplica-se exclusivamente au contrato celebrado entre si e a <b>Nevumo</b> (operadora da plataforma). <b>Não se aplica a contratos entre Clientes e Prestadores de Serviços</b> facilitados através da plataforma Nevumo.",
        "pdf.important_notice_text_part2": "A rescisão de um contrato com um Prestador de Serviços específico é regida diretamente pelos termos acordados com esse prestador.",
    },
    "ro": {
        "pdf.important_notice_title": "⚠️ NOTĂ IMPORTANTĂ",
        "pdf.important_notice_text": "Prezentul formular se aplică exclusiv contractului încheiat între dumneavoastră și <b>Nevumo</b> (operatorul platformei). <b>Nu se aplică contractelor dintre Clienți și Furnizorii de Servicii</b> intermediate prin intermediul platformei Nevumo.",
        "pdf.important_notice_text_part2": "Retragerea dintr-un contract cu un anumit furnizor de servicii este guvernată direct de condițiile convenite cu furnizorul respectiv.",
    },
    "ru": {
        "pdf.important_notice_title": "⚠️ ВАЖНОЕ ПРИМЕЧАНИЕ",
        "pdf.important_notice_text": "Данная форма относится исключительно к договору, заключенному между вами и <b>Nevumo</b> (оператором платформы). <b>Она не относится к договорам между Клиентами и Поставщиками услуг</b>, заключенным через платформу Nevumo.",
        "pdf.important_notice_text_part2": "Отказ от договора с конкретным Поставщиком услуг регулируется непосредственно условиями, согласованными с этим Поставщиком.",
    },
    "sk": {
        "pdf.important_notice_title": "⚠️ DÔLEŽITÉ UPOZORNENIE",
        "pdf.important_notice_text": "Tento formulár sa vzťahuje výlučne na zmluvu uzavretú medzi vami a spoločnosťou <b>Nevumo</b> (prevádzkovateľom platformy). <b>Nevzťahuje sa na zmluvy medzi klientmi a poskytovateľmi služieb</b> sprostredkované prostredníctvom platformy Nevumo.",
        "pdf.important_notice_text_part2": "Odstúpenie od zmluvy s konkrétnym poskytovateľom služieb sa riadi priamo podmienkami dohodnutými s týmto poskytovateľom.",
    },
    "sl": {
        "pdf.important_notice_title": "⚠️ POMEMBNO OBVESTILO",
        "pdf.important_notice_text": "Ta obrazec se nanaša izključno na pogodbo, sklenjeno med vami in podjetjem <b>Nevumo</b> (upravljavcem platforme). <b>Ne velja za pogodbe med strankami in ponudniki storitev</b>, sklenjene prek platforme Nevumo.",
        "pdf.important_notice_text_part2": "Odstop od pogodbe s posameznim ponudnikom storitev neposredno urejajo pogoji, dogovorjeni s tem ponudnikom.",
    },
    "sq": {
        "pdf.important_notice_title": "⚠️ NJOFTIM I RËNDËSISHËM",
        "pdf.important_notice_text": "Ky formular zbatohet ekskluzivisht për kontratën e lidhur midis jush dhe <b>Nevumo</b> (operatori i platformës). <b>Nuk zbatohet për kontratat midis Klientëve dhe Ofruesve të Shërbimeve</b> të ndërmjetësuara përmes platformës Nevumo.",
        "pdf.important_notice_text_part2": "Tërheqja nga një kontratë me një Ofrues Shërbimi specifik rregullohet drejtpërdrejt nga kushtet e rëna dakord me atë Ofrues Shërbimi.",
    },
    "sr": {
        "pdf.important_notice_title": "⚠️ VAŽNO OBAVEŠTENJE",
        "pdf.important_notice_text": "Ovaj formular se odnosi isključivo na ugovor zaključen između vas i <b>Nevuma</b> (operatera platforme). <b>Ne odnosi se na ugovore između klijenata i pružalaca usluga</b> zaključene putem platforme Nevumo.",
        "pdf.important_notice_text_part2": "Odustanak od ugovora sa određenim pružaocem usluga direktno je regulisan uslovima dogovorenim sa tim pružaocem usluga.",
    },
    "sv": {
        "pdf.important_notice_title": "⚠️ VIKTIGT MEDDELANDE",
        "pdf.important_notice_text": "Detta formulär gäller uteslutande det avtal som ingåtts mellan dig och <b>Nevumo</b> (plattformsoperatören). <b>Det gäller inte avtal mellan kunder och tjänsteleverantörer</b> som förmedlas via Nevumo-plattformen.",
        "pdf.important_notice_text_part2": "Frånträde från ett avtal med en specifik tjänsteleverandör styrs direkt av de villkor som avtalats med den tjänsteleverantören.",
    },
    "tr": {
        "pdf.important_notice_title": "⚠️ ÖNEMLİ NOT",
        "pdf.important_notice_text": "Bu form münhasıran sizinle <b>Nevumo</b> (platform operatörü) arasında akdedilen sözleşme için geçerlidir. <b>Nevumo platformu aracılığıyla Müşteriler ve Hizmet Sağlayıcılar arasında akdedilen sözleşmeler için geçerli değildir</b>.",
        "pdf.important_notice_text_part2": "Belirli bir Hizmet Sağlayıcı ile yapılan sözleşmeden cayma hakkı, doğrudan o Hizmet Sağlayıcı ile kararlaştırılan şartlara tabidir.",
    },
    "uk": {
        "pdf.important_notice_title": "⚠️ ВАЖЛИВЕ ЗАУВАЖЕННЯ",
        "pdf.important_notice_text": "Ця форма стосується виключно договору, укладеного між вами та <b>Nevumo</b> (оператором платформи). <b>Вона не стосується договорів між клієнтами та постачальниками послуг</b>, укладених через платформу Nevumo.",
        "pdf.important_notice_text_part2": "Відмова від договору з конкретним постачальником послуг регулюється безпосередньо умовами, погодженими з цим постачальником.",
    },
}


if __name__ == "__main__":
    main()
