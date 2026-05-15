"""
seed_terms_p8_bodies.py  —  Nevumo | namespace: terms
Key: art8_body (34 езика)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_terms_p8_bodies
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://nevumo:nevumo@postgres:5432/nevumo_leads",
)

NAMESPACE = "terms"

TRANSLATIONS: dict[str, dict[str, str]] = {
    "art8_body": {
        "en": (
            '8.1 After a service is completed, you may leave a review for the provider. '
            'Reviews must be truthful, based on a genuine experience, and must not contain '
            'defamatory, discriminatory, or unlawful content.\n\n'
            '8.2 Nevumo reserves the right to remove reviews that violate these Terms. '
            'Nevumo does not edit reviews to alter their meaning.\n\n'
            '8.3 Reviews are visible to all platform users and may be read by the provider '
            'and other clients.'
        ),
        "pl": (
            '10.1 Po wykonaniu usługi Klient może wystawić Usługodawcy opinię. Opinie muszą '
            'być zgodne z prawdą, oparte na rzeczywistym doświadczeniu i nie mogą zawierać '
            'treści zniesławiających, dyskryminujących ani bezprawnych.\n\n'
            '10.2 Nevumo zastrzega sobie prawo do usunięcia opinii naruszających Regulamin. '
            'Nevumo nie modyfikuje opinii w sposób zmieniający ich znaczenie.\n\n'
            '10.3 Opinie są widoczne dla wszystkich użytkowników platformy.'
        ),
        "bg": (
            '8.1 След извършване на услугата Клиентът може да публикува отзив за Доставчика. '
            'Отзивите трябва да са верни, основани на реален опит и да не съдържат '
            'клеветнически, дискриминационни или незаконни съдържания.\n\n'
            '8.2 Nevumo си запазва правото да премахва отзиви, нарушаващи настоящите ОУ. '
            'Nevumo не редактира отзиви по начин, изменящ тяхното значение.\n\n'
            '8.3 Отзивите са видими за всички потребители на платформата.'
        ),
        "cs": (
            '8.1 Po dokončení služby můžete zanechat recenzi na poskytovatele. Recenze musí '
            'být pravdivé, založené na skutečné zkušenosti a nesmí obsahovat hanlivý, '
            'diskriminační nebo nezákonný obsah.\n\n'
            '8.2 Nevumo si vyhrazuje právo odstranit recenze, které porušují tyto podmínky. '
            'Nevumo neupravuje recenze způsobem, který mění jejich smysl.\n\n'
            '8.3 Recenze jsou viditelné všem uživatelům platformy a mohou je číst poskytovatel '
            'i ostatní klienti.'
        ),
        "da": (
            '8.1 Når en tjeneste er afsluttet, kan du skrive en anmeldelse af udbyderen. '
            'Anmeldelser skal være sandfærdige, baseret på en ægte oplevelse og må ikke '
            'indeholde ærekrænkende, diskriminerende eller ulovligt indhold.\n\n'
            '8.2 Nevumo forbeholder sig retten til at fjerne anmeldelser, der overtræder '
            'disse vilkår. Nevumo redigerer ikke anmeldelser på en måde, der ændrer '
            'deres betydning.\n\n'
            '8.3 Anmeldelser er synlige for alle platformbrugere og kan læses af udbyderen '
            'og andre klienter.'
        ),
        "de": (
            '8.1 Nach Abschluss einer Dienstleistung können Sie eine Bewertung für den '
            'Anbieter hinterlassen. Bewertungen müssen wahrheitsgemäß, auf echter Erfahrung '
            'basierend sein und dürfen keine verleumderischen, diskriminierenden oder '
            'rechtswidrigen Inhalte enthalten.\n\n'
            '8.2 Nevumo behält sich das Recht vor, Bewertungen zu entfernen, die gegen diese '
            'Bedingungen verstoßen. Nevumo bearbeitet Bewertungen nicht in einer Weise, die '
            'ihren Sinn verändert.\n\n'
            '8.3 Bewertungen sind für alle Plattformnutzer sichtbar und können vom Anbieter '
            'und anderen Kunden gelesen werden.'
        ),
        "el": (
            '8.1 Μετά την ολοκλήρωση μιας υπηρεσίας, μπορείτε να αφήσετε μια αξιολόγηση '
            'για τον πάροχο. Οι αξιολογήσεις πρέπει να είναι αληθείς, βασισμένες σε '
            'πραγματική εμπειρία και να μην περιέχουν δυσφημιστικό, διακριτικό ή παράνομο '
            'περιεχόμενο.\n\n'
            '8.2 Το Nevumo διατηρεί το δικαίωμα να αφαιρεί αξιολογήσεις που παραβιάζουν '
            'τους παρόντες Όρους. Το Nevumo δεν επεξεργάζεται αξιολογήσεις κατά τρόπο που '
            'αλλοιώνει το νόημά τους.\n\n'
            '8.3 Οι αξιολογήσεις είναι ορατές σε όλους τους χρήστες της πλατφόρμας.'
        ),
        "es": (
            '8.1 Tras completar un servicio, puede dejar una reseña sobre el proveedor. '
            'Las reseñas deben ser verídicas, basadas en una experiencia genuina y no deben '
            'contener contenido difamatorio, discriminatorio o ilícito.\n\n'
            '8.2 Nevumo se reserva el derecho de eliminar reseñas que infrinjan estos '
            'Términos. Nevumo no edita reseñas de manera que altere su significado.\n\n'
            '8.3 Las reseñas son visibles para todos los usuarios de la plataforma y pueden '
            'ser leídas por el proveedor y otros clientes.'
        ),
        "et": (
            '8.1 Pärast teenuse lõpetamist võite jätta teenusepakkuja kohta arvustuse. '
            'Arvustused peavad olema tõesed, põhinema tegelikul kogemusel ja ei tohi '
            'sisaldada laimavat, diskrimineerivat ega ebaseaduslikku sisu.\n\n'
            '8.2 Nevumo jätab endale õiguse eemaldada arvustused, mis rikuvad neid tingimusi. '
            'Nevumo ei muuda arvustusi viisil, mis muudab nende tähendust.\n\n'
            '8.3 Arvustused on nähtavad kõigile platvormi kasutajatele.'
        ),
        "fi": (
            '8.1 Palvelun päätyttyä voit jättää arvostelun palveluntarjoajasta. Arvostelujen '
            'on oltava totuudenmukaisia, perustuttava aitoon kokemukseen eivätkä ne saa '
            'sisältää herjaavaa, syrjivää tai laitonta sisältöä.\n\n'
            '8.2 Nevumo pidättää oikeuden poistaa arvostelut, jotka rikkovat näitä ehtoja. '
            'Nevumo ei muokkaa arvosteluja tavalla, joka muuttaa niiden merkitystä.\n\n'
            '8.3 Arvostelut ovat kaikkien alustan käyttäjien nähtävissä.'
        ),
        "fr": (
            '8.1 Après l\'achèvement d\'un service, vous pouvez laisser un avis sur le '
            'prestataire. Les avis doivent être véridiques, basés sur une expérience réelle '
            'et ne pas contenir de contenu diffamatoire, discriminatoire ou illicite.\n\n'
            '8.2 Nevumo se réserve le droit de supprimer les avis qui enfreignent les '
            'présentes Conditions. Nevumo ne modifie pas les avis de manière à en altérer '
            'le sens.\n\n'
            '8.3 Les avis sont visibles de tous les utilisateurs de la plateforme et peuvent '
            'être lus par le prestataire et d\'autres clients.'
        ),
        "ga": (
            '8.1 Tar éis seirbhíse a bheith críochnaithe, féadfaidh tú léirmheas a fhágáil '
            'ar an soláthróir. Caithfidh léirmheasanna a bheith fírinneach, bunaithe ar '
            'fhíordhomhan agus ní ceadaítear ábhar clúmhilleach, idirdhealaitheach nó '
            'neamhdhleathach.\n\n'
            '8.2 Tá an ceart ag Nevumo léirmheasanna a scarann na Téarmaí seo a bhaint. '
            'Ní dhéanann Nevumo léirmheasanna a chur in eagar ar bhealach a athraíonn '
            'a gciall.\n\n'
            '8.3 Tá léirmheasanna le feiceáil ag gach úsáideoir ar an ardán agus is féidir '
            'leis an soláthróir agus cliaint eile iad a léamh.'
        ),
        "hr": (
            '8.1 Nakon završetka usluge možete ostaviti recenziju za davatelja usluge. '
            'Recenzije moraju biti istinite, temeljene na stvarnom iskustvu i ne smiju '
            'sadržavati klevetničke, diskriminatorne ili nezakonite sadržaje.\n\n'
            '8.2 Nevumo zadržava pravo ukloniti recenzije koje krše ove Uvjete. Nevumo '
            'ne uređuje recenzije na način koji mijenja njihov smisao.\n\n'
            '8.3 Recenzije su vidljive svim korisnicima platforme.'
        ),
        "hu": (
            '8.1 Egy szolgáltatás elvégzése után értékelést hagyhat a szolgáltatóról. Az '
            'értékeléseknek igaznak kell lenniük, valódi tapasztalaton kell alapulniuk, és '
            'nem tartalmazhatnak rágalmazó, diszkriminatív vagy jogellenes tartalmat.\n\n'
            '8.2 A Nevumo fenntartja a jogot az ezen feltételeket sértő értékelések '
            'eltávolítására. A Nevumo nem szerkeszti az értékeléseket oly módon, hogy '
            'megváltoztassa azok értelmét.\n\n'
            '8.3 Az értékelések a platform összes felhasználója számára láthatók.'
        ),
        "is": (
            '8.1 Eftir að þjónusta er lokið getur þú skilið eftir umsögn um þjónustuaðilann. '
            'Umsagnir verða að vera sannar, byggðar á raunverulegri reynslu og mega ekki '
            'innihalda meiðandi, mismunandi eða ólöglegt efni.\n\n'
            '8.2 Nevumo áskilur sér rétt til að fjarlægja umsagnir sem brjóta í bága við '
            'þessa skilmála. Nevumo breytir ekki umsögnum á þann hátt að merking þeirra '
            'breytist.\n\n'
            '8.3 Umsagnir eru sýnilegar öllum notendum vettvangsins.'
        ),
        "it": (
            '8.1 Al termine di un servizio, puoi lasciare una recensione sul prestatore. '
            'Le recensioni devono essere veritiere, basate su un\'esperienza genuina e non '
            'devono contenere contenuti diffamatori, discriminatori o illeciti.\n\n'
            '8.2 Nevumo si riserva il diritto di rimuovere le recensioni che violano i '
            'presenti Termini. Nevumo non modifica le recensioni in modo da alterarne '
            'il significato.\n\n'
            '8.3 Le recensioni sono visibili a tutti gli utenti della piattaforma.'
        ),
        "lb": (
            '8.1 No der Erbréngung vun engem Service kënnt Dir eng Bewäertung fir de '
            'Prestataire hannerloossen. Bewäertunge mussen wouer sinn, op echter Erfahrung '
            'baséiert a kënnen kee verleemderischen, diskriminéierenden oder illegalen '
            'Inhalt enthalen.\n\n'
            '8.2 Nevumo behält sech vir, Bewäertungen ze läschen, déi géint dës '
            'Bedéngunge verstoussen. Nevumo bearbeecht Bewäertunge net op eng Aart, '
            'déi hir Bedeitung ännert.\n\n'
            '8.3 Bewäertunge sinn fir all Plattformbenotzer siichtbar.'
        ),
        "lt": (
            '8.1 Pasibaigus paslaugai, galite palikti atsiliepimą apie paslaugų teikėją. '
            'Atsiliepimai turi būti teisingi, pagrįsti tikra patirtimi ir neturi turėti '
            'šmeižikiško, diskriminuojančio ar neteisėto turinio.\n\n'
            '8.2 Nevumo pasilieka teisę pašalinti atsiliepimus, pažeidžiančius šias sąlygas. '
            'Nevumo neredaguoja atsiliepimų taip, kad pakeistų jų prasmę.\n\n'
            '8.3 Atsiliepimai matomi visiems platformos naudotojams.'
        ),
        "lv": (
            '8.1 Pēc pakalpojuma pabeigšanas varat atstāt atsauksmi par pakalpojumu '
            'sniedzēju. Atsauksmēm jābūt patiesām, balstītām uz patiesu pieredzi, un tās '
            'nedrīkst saturēt aizskarošu, diskriminējošu vai nelikumīgu saturu.\n\n'
            '8.2 Nevumo patur tiesības noņemt atsauksmes, kas pārkāpj šos noteikumus. '
            'Nevumo nerediģē atsauksmes tā, lai mainītu to nozīmi.\n\n'
            '8.3 Atsauksmes ir redzamas visiem platformas lietotājiem.'
        ),
        "mk": (
            '8.1 По завршувањето на услугата, можете да оставите рецензија за Давателот. '
            'Рецензиите мора да бидат вистинити, засновани на вистинско искуство и не смеат '
            'да содржат клеветнички, дискриминаторни или незаконски содржини.\n\n'
            '8.2 Nevumo го задржува правото да ги отстрани рецензиите кои ги кршат овие '
            'Услови. Nevumo не ги уредува рецензиите на начин кој го менува нивното '
            'значење.\n\n'
            '8.3 Рецензиите се видливи за сите корисници на платформата.'
        ),
        "mt": (
            '8.1 Wara li s-servizz jitlesta, tista\' tħalli reviżjoni dwar il-fornitur. '
            'Ir-reviżjonijiet iridu jkunu veritieri, ibbażati fuq esperjenza ġenwina u ma '
            'jistgħux jinkludu kontenut malafamanti, diskriminatorju jew illegali.\n\n'
            '8.2 Nevumo jiriserva d-dritt li jneħħi reviżjonijiet li jiksru dawn it-Termini. '
            'Nevumo ma jeditjax reviżjonijiet b\'mod li jibdel it-tifsira tagħhom.\n\n'
            '8.3 Ir-reviżjonijiet huma viżibbli għall-utenti kollha tal-pjattaforma.'
        ),
        "nl": (
            '8.1 Na afronding van een dienst kunt u een beoordeling achterlaten voor de '
            'provider. Beoordelingen moeten waarheidsgetrouw zijn, gebaseerd op een echte '
            'ervaring, en mogen geen lasterlijke, discriminerende of onwettige inhoud '
            'bevatten.\n\n'
            '8.2 Nevumo behoudt zich het recht voor beoordelingen te verwijderen die deze '
            'Voorwaarden schenden. Nevumo bewerkt geen beoordelingen op een manier die de '
            'betekenis ervan verandert.\n\n'
            '8.3 Beoordelingen zijn zichtbaar voor alle platformgebruikers.'
        ),
        "no": (
            '8.1 Etter at en tjeneste er fullført, kan du skrive en anmeldelse av '
            'leverandøren. Anmeldelser må være sannferdige, basert på en ekte opplevelse '
            'og må ikke inneholde ærekrenkende, diskriminerende eller ulovlig innhold.\n\n'
            '8.2 Nevumo forbeholder seg retten til å fjerne anmeldelser som bryter disse '
            'Vilkårene. Nevumo redigerer ikke anmeldelser på en måte som endrer deres '
            'betydning.\n\n'
            '8.3 Anmeldelser er synlige for alle plattformbrukere.'
        ),
        "pt": (
            '8.1 Após a conclusão de um serviço, você pode deixar uma avaliação sobre o '
            'prestador. As avaliações devem ser verídicas, baseadas em experiência genuína '
            'e não devem conter conteúdo difamatório, discriminatório ou ilícito.\n\n'
            '8.2 O Nevumo reserva-se o direito de remover avaliações que violem estes '
            'Termos. O Nevumo não edita avaliações de forma a alterar o seu significado.\n\n'
            '8.3 As avaliações são visíveis para todos os utilizadores da plataforma.'
        ),
        "pt-PT": (
            '8.1 Após a conclusão de um serviço, pode deixar uma avaliação sobre o '
            'prestador. As avaliações devem ser verídicas, baseadas em experiência genuína '
            'e não devem conter conteúdo difamatório, discriminatório ou ilícito.\n\n'
            '8.2 O Nevumo reserva-se o direito de remover avaliações que violem estes '
            'Termos. O Nevumo não edita avaliações de forma a alterar o seu significado.\n\n'
            '8.3 As avaliações são visíveis para todos os utilizadores da plataforma.'
        ),
        "ro": (
            '8.1 După finalizarea unui serviciu, puteți lăsa o recenzie despre prestator. '
            'Recenziile trebuie să fie adevărate, bazate pe o experiență reală și nu trebuie '
            'să conțină conținut defăimător, discriminatoriu sau ilegal.\n\n'
            '8.2 Nevumo își rezervă dreptul de a elimina recenziile care încalcă acești '
            'Termeni. Nevumo nu editează recenzii în mod care să le altereze sensul.\n\n'
            '8.3 Recenziile sunt vizibile tuturor utilizatorilor platformei.'
        ),
        "ru": (
            '8.1 После завершения услуги вы можете оставить отзыв об исполнителе. Отзывы '
            'должны быть правдивыми, основанными на реальном опыте и не должны содержать '
            'клеветнический, дискриминационный или незаконный контент.\n\n'
            '8.2 Nevumo оставляет за собой право удалять отзывы, нарушающие настоящие '
            'условия. Nevumo не редактирует отзывы способом, меняющим их смысл.\n\n'
            '8.3 Отзывы видны всем пользователям платформы.'
        ),
        "sk": (
            '8.1 Po dokončení služby môžete zanechať recenziu na poskytovateľa. Recenzie '
            'musia byť pravdivé, založené na skutočnej skúsenosti a nesmú obsahovať '
            'hanlivý, diskriminačný alebo nezákonný obsah.\n\n'
            '8.2 Nevumo si vyhradzuje právo odstrániť recenzie, ktoré porušujú tieto '
            'podmienky. Nevumo neupravuje recenzie spôsobom, ktorý mení ich zmysel.\n\n'
            '8.3 Recenzie sú viditeľné všetkým používateľom platformy.'
        ),
        "sl": (
            '8.1 Po zaključku storitve lahko pustite oceno ponudnika. Ocene morajo biti '
            'resnične, osnovane na resnični izkušnji in ne smejo vsebovati žaljivih, '
            'diskriminatornih ali nezakonitih vsebin.\n\n'
            '8.2 Nevumo si pridržuje pravico odstraniti ocene, ki kršijo te pogoje. '
            'Nevumo ne ureja ocen na način, ki bi spremenil njihov pomen.\n\n'
            '8.3 Ocene so vidne vsem uporabnikom platforme.'
        ),
        "sq": (
            '8.1 Pas përfundimit të shërbimit, mund të lini një vlerësim për ofruesin. '
            'Vlerësimet duhet të jenë të vërteta, të bazuara në eksperiencë të vërtetë dhe '
            'nuk duhet të përmbajnë përmbajtje shpifëse, diskriminuese ose të paligjshme.\n\n'
            '8.2 Nevumo rezervon të drejtën të heqë vlerësimet që shkelin këto Terma. '
            'Nevumo nuk redakton vlerësimet në mënyrë që të ndryshojë kuptimin e tyre.\n\n'
            '8.3 Vlerësimet janë të dukshme për të gjithë përdoruesit e platformës.'
        ),
        "sr": (
            '8.1 Nakon završetka usluge možete ostaviti recenziju za pružaoca. Recenzije '
            'moraju biti istinite, zasnovane na stvarnom iskustvu i ne smeju sadržati '
            'klevetničke, diskriminatorne ili nezakonite sadržaje.\n\n'
            '8.2 Nevumo zadržava pravo da ukloni recenzije koje krše ove Uslove. Nevumo '
            'ne uređuje recenzije na način koji menja njihov smisao.\n\n'
            '8.3 Recenzije su vidljive svim korisnicima platforme.'
        ),
        "sv": (
            '8.1 När en tjänst är slutförd kan du lämna en recension av leverantören. '
            'Recensioner måste vara sanningsenliga, baserade på en genuin erfarenhet och '
            'får inte innehålla ärekränkande, diskriminerande eller olagligt innehåll.\n\n'
            '8.2 Nevumo förbehåller sig rätten att ta bort recensioner som bryter mot '
            'dessa Villkor. Nevumo redigerar inte recensioner på ett sätt som förändrar '
            'deras innebörd.\n\n'
            '8.3 Recensioner är synliga för alla plattformsanvändare.'
        ),
        "tr": (
            '8.1 Bir hizmet tamamlandıktan sonra sağlayıcı hakkında değerlendirme '
            'bırakabilirsiniz. Değerlendirmeler gerçek bir deneyime dayalı, doğru olmalı '
            've iftira niteliğinde, ayrımcı veya yasadışı içerik barındırmamalıdır.\n\n'
            '8.2 Nevumo, bu Koşulları ihlal eden değerlendirmeleri kaldırma hakkını saklı '
            'tutar. Nevumo, değerlendirmeleri anlamlarını değiştirecek şekilde düzenlemez.\n\n'
            '8.3 Değerlendirmeler tüm platform kullanıcıları tarafından görülebilir.'
        ),
        "uk": (
            '8.1 Після завершення послуги ви можете залишити відгук про виконавця. Відгуки '
            'повинні бути правдивими, ґрунтуватися на реальному досвіді та не містити '
            'наклепницького, дискримінаційного або незаконного контенту.\n\n'
            '8.2 Nevumo залишає за собою право видаляти відгуки, що порушують ці Умови. '
            'Nevumo не редагує відгуки способом, що змінює їхній зміст.\n\n'
            '8.3 Відгуки видимі всім користувачам платформи.'
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
        print(f"✅ seed_terms_p8_bodies: {count} rows upserted ({NAMESPACE}, art8_body × 34 langs)")

    engine.dispose()


if __name__ == "__main__":
    seed()
