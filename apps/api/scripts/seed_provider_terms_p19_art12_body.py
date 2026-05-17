"""
seed_provider_terms_p19_art12_body.py  —  Nevumo | namespace: provider_terms
Key: art12_body  (1 key x 34 langs = 34 rows)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_provider_terms_p19_art12_body
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
    "art12_body": {
        "en": (
            "12.1 Providers may submit complaints about Nevumo's decisions, including decisions on account suspension, restriction, or termination, or alleged non-compliance with these Provider Terms.\n\n"
            "12.2 To submit a complaint, write to: **legal@nevumo.com**, subject: \"Provider Complaint\". Please include:\n"
            "- your account email and Provider ID;\n"
            "- a description of the decision or action complained about;\n"
            "- the outcome you are seeking.\n\n"
            "12.3 Nevumo will acknowledge receipt of the complaint within **5 business days** and provide a substantive written response within **30 calendar days** of receipt.\n\n"
            "12.4 The internal complaint procedure is **free of charge** for Providers.\n\n"
            "12.5 If you are not satisfied with the outcome of the internal complaint procedure, you may proceed to mediation as described in Section 13."
        ),
        "bg": (
            "1. Доставчиците могат да подават жалби относно решения на Nevumo, включително решения за спиране, ограничаване или прекратяване на акаунт, или за предполагаемо неспазване на настоящите Условия за Доставчици.\n\n"
            "2. За подаване на жалба следва да се пише на: **legal@nevumo.com**, с тема: „Жалба на Доставчик“. Жалбата трябва да съдържа:\n"
            "- имейл адреса на акаунта и идентификатора на Доставчика;\n"
            "- описание на решението или действието, предмет на жалбата;\n"
            "- желания резултат от разглеждането на жалбата.\n\n"
            "3. Nevumo ще потвърди получаването на жалбата в рамките на **5 работни дни** и ще предостави писмен отговор по същество в срок от **30 календарни дни** от получаването й.\n\n"
            "4. Вътрешната процедура за разглеждане на жалби е **безплатна** за Доставчиците.\n\n"
            "5. В случай на неудовлетвореност от резултата от вътрешната процедура за разглеждане на жалби, Доставчикът може да пристъпи към медиация съгласно чл. 13."
        ),
        "pl": (
            "1. Dostawcy mogą składać skargi dotyczące decyzji Nevumo, w tym decyzji o zawieszeniu, ograniczeniu lub rozwiązaniu konta albo zarzucanego naruszenia niniejszego Regulaminu Dostawców.\n\n"
            "2. Skargę należy kierować na adres: **legal@nevumo.com**, temat wiadomości: „Skarga Dostawcy“. Skarga powinna zawierać:\n"
            "- adres e-mail konta i identyfikator Dostawcy;\n"
            "- opis decyzji lub działania będącego przedmiotem skargi;\n"
            "- oczekiwany wynik rozpatrzenia skargi.\n\n"
            "3. Nevumo potwierdzi otrzymanie skargi w terminie **5 dni roboczych** i udzieli merytorycznej odpowiedzi na piśmie w terminie **30 dni kalendarzowych** od jej otrzymania.\n\n"
            "4. Wewnętrzna procedura skargowa jest dla Dostawców **bezpłatna**.\n\n"
            "5. W przypadku braku satysfakcji z wyniku wewnętrznej procedury skargowej Dostawca może skierować sprawę do mediacji zgodnie z §13."
        ),
        "de": (
            "12.1 Anbieter können Beschwerden über Entscheidungen von Nevumo einreichen, einschließlich Entscheidungen über die Sperrung, Einschränkung oder Kündigung von Konten oder angebliche Nichteinhaltung dieser Anbieterbedingungen.\n\n"
            "12.2 Um eine Beschwerde einzureichen, schreiben Sie an: **legal@nevumo.com**, Betreff: \"Provider Complaint\". Bitte geben Sie Folgendes an:\n"
            "- Ihre Konto-E-Mail-Adresse und Anbieter-ID;\n"
            "- eine Beschreibung der Entscheidung oder Handlung, über die Sie sich beschweren;\n"
            "- das von Ihnen angestrebte Ergebnis.\n\n"
            "12.3 Nevumo wird den Eingang der Beschwerde innerhalb von **5 Werktagen** bestätigen und innerhalb von **30 Kalendertagen** nach Eingang eine inhaltliche schriftliche Antwort geben.\n\n"
            "12.4 Das interne Beschwerdeverfahren ist für Anbieter **kostenlos**.\n\n"
            "12.5 Wenn Sie mit dem Ergebnis des internen Beschwerdeverfahrens nicht zufrieden sind, können Sie eine Mediation einleiten, wie in Abschnitt 13 beschrieben."
        ),
        "fr": (
            "12.1 Les Fournisseurs peuvent soumettre des plaintes concernant les décisions de Nevumo, y compris les décisions de suspension, de restriction ou de résiliation de compte, ou de non-respect présumé de ces Conditions pour les Fournisseurs.\n\n"
            "12.2 Pour soumettre une plainte, écrivez à : **legal@nevumo.com**, objet : \"Provider Complaint\". Veuillez inclure :\n"
            "- l'e-mail de votre compte et votre identifiant de Fournisseur ;\n"
            "- une description de la décision ou de l'action faisant l'objet de la plainte ;\n"
            "- le résultat que vous recherchez.\n\n"
            "12.3 Nevumo accusera réception de la plainte dans les **5 jours ouvrables** et fournira une réponse écrite détaillée dans les **30 jours civils** suivant la réception.\n\n"
            "12.4 La procédure de plainte interne est **gratuite** pour les Fournisseurs.\n\n"
            "12.5 Si vous n'êtes pas satisfait de l'issue de la procédure de plainte interne, vous pouvez procéder à une médiation comme décrit à la Section 13."
        ),
        "es": (
            "12.1 Los Proveedores pueden presentar quejas sobre las decisiones de Nevumo, incluidas las decisiones sobre la suspensión, restricción o rescisión de la cuenta, o el supuesto incumplimiento de estas Condiciones para Proveedores.\n\n"
            "12.2 Para presentar una queja, escriba a: **legal@nevumo.com**, asunto: \"Provider Complaint\". Por favor incluya:\n"
            "- el correo electrónico de su cuenta y el ID de Proveedor;\n"
            "- una descripción de la decisión o acción objeto de queja;\n"
            "- el resultado que busca.\n\n"
            "12.3 Nevumo acusará recibo de la queja dentro de los **5 días hábiles** y proporcionará una respuesta por escrito detallada dentro de los **30 días calendario** posteriores a la recepción.\n\n"
            "12.4 El procedimiento de queja interna es **gratuito** para los Proveedores.\n\n"
            "12.5 Si no está satisfecho con el resultado del procedimiento de queja interna, puede proceder a la mediación como se describe en la Sección 13."
        ),
        "it": (
            "12.1 I Fornitori possono presentare reclami in merito alle decisioni di Nevumo, incluse le decisioni su sospensione, restrizione o risoluzione dell'account o presunta mancata conformità con le presenti Condizioni per i Fornitori.\n\n"
            "12.2 Per inviare un reclamo, scrivi a: **legal@nevumo.com**, oggetto: \"Provider Complaint\". Si prega di includere:\n"
            "- l'e-mail del tuo account e l'ID Fornitore;\n"
            "- una descrizione della decisione o dell'azione oggetto del reclamo;\n"
            "- il risultato che si sta cercando.\n\n"
            "12.3 Nevumo confermerà la ricezione del reclamo entro **5 giorni lavorativi** e fornirà una risposta scritta dettagliata entro **30 giorni di calendario** dalla ricezione.\n\n"
            "12.4 La procedura di reclamo interna è **gratuita** per i Fornitori.\n\n"
            "12.5 Se non sei soddisfatto dell'esito della procedura di reclamo interna, puoi procedere alla mediazione come descritto nella Sezione 13."
        ),
        "nl": (
            "12.1 Dienstverleners kunnen klachten indienen over de beslissingen van Nevumo, met inbegrip van beslissingen over de opschorting, beperking of beëindiging van accounts, of vermeende niet-naleving van deze Voorwaarden voor Dienstverleners.\n\n"
            "12.2 Om een klacht in te dienen, schrijft u naar: **legal@nevumo.com**, onderwerp: \"Provider Complaint\". Voeg het volgende toe:\n"
            "- uw account-e-mailadres en Dienstverlener-ID;\n"
            "- een beschrijving van de beslissing of actie waarover wordt geklaagd;\n"
            "- het resultaat dat u zoekt.\n\n"
            "12.3 Nevumo zal de ontvangst van de klacht binnen **5 werkdagen** bevestigen en binnen **30 kalenderdagen** na ontvangst een inhoudelijke schriftelijke reactie geven.\n\n"
            "12.4 De interne klachtenprocedure is **kosteloos** voor Dienstverleners.\n\n"
            "12.5 Indien u niet tevreden bent met de uitkomst van de interne klachtenprocedure, kunt u overgaan tot bemiddeling zoals beschreven in Sectie 13."
        ),
        "pt": (
            "12.1 Os Prestadores podem enviar reclamações sobre as decisões da Nevumo, incluindo decisões sobre a suspensão, restrição ou rescisão da conta, ou alegado incumprimento destes Termos para Prestadores.\n\n"
            "12.2 Para enviar uma reclamação, escreva para: **legal@nevumo.com**, assunto: \"Provider Complaint\". Por favor inclua:\n"
            "- o e-mail da sua conta e o ID de Prestador;\n"
            "- uma descrição da decisão ou ação de que reclama;\n"
            "- o resultado que procura.\n\n"
            "12.3 A Nevumo acusará a receção da reclamação no prazo de **5 dias úteis** e fornecerá uma resposta por escrito fundamentada no prazo de **30 dias de calendário** a contar da receção.\n\n"
            "12.4 O procedimento interno de reclamação é **gratuito** para os Prestadores.\n\n"
            "12.5 Se não estiver satisfeito com o resultado do procedimento interno de reclamação, pode prosseguir para mediação conforme descrito na Secção 13."
        ),
        "pt-PT": (
            "12.1 Os Prestadores podem enviar reclamações sobre as decisões da Nevumo, incluindo decisões sobre a suspensão, restrição ou rescisão da conta, ou alegado incumprimento destes Termos para Prestadores.\n\n"
            "12.2 Para enviar uma reclamação, escreva para: **legal@nevumo.com**, assunto: \"Provider Complaint\". Por favor inclua:\n"
            "- o e-mail da sua conta e o ID de Prestador;\n"
            "- uma descrição da decisão ou ação de que reclama;\n"
            "- o resultado que procura.\n\n"
            "12.3 A Nevumo acusará a receção da reclamação no prazo de **5 dias úteis** e fornecerá uma resposta por escrito fundamentada no prazo de **30 dias de calendário** a contar da receção.\n\n"
            "12.4 O procedimento interno de reclamação é **gratuito** para os Prestadores.\n\n"
            "12.5 Se não estiver satisfeito com o resultado do procedimento interno de reclamação, pode prosseguir para mediação conforme descrito na Secção 13."
        ),
        "ro": (
            "12.1 Furnizorii pot depune plângeri cu privire la deciziile Nevumo, inclusiv deciziile privind suspendarea, restricționarea sau rezilierea contului sau presupusa nerespectare a acestor Termeni pentru Furnizori.\n\n"
            "12.2 Pentru a trimite o plângere, scrieți la: **legal@nevumo.com**, subiect: \"Provider Complaint\". Vă rugăm să includeți:\n"
            "- e-mailul contului dvs. și ID-ul Furnizorului;\n"
            "- o descriere a deciziei sau acțiunii reclamate;\n"
            "- rezultatul pe care îl căutați.\n\n"
            "12.3 Nevumo va confirma primirea plângerii în termen de **5 zile lucrătoare** și va oferi un răspuns scris de fond în termen de **30 de zile calendaristice** de la primire.\n\n"
            "12.4 Procedura internă de soluționare a plângerilor este **gratuită** pentru Furnizori.\n\n"
            "12.5 Dacă nu sunteți mulțumit de rezultatul procedurii interne de reclamație, puteți proceda la mediere așa cum este descris în Secțiunea 13."
        ),
        "ru": (
            "12.1 Поставщики могут подавать жалобы на решения Nevumo, включая решения о приостановке, ограничении или закрытии учетной записи, или о предполагаемом несоблюдении настоящих Условий для Поставщиков.\n\n"
            "12.2 Чтобы подать жалобу, напишите по адресу: **legal@nevumo.com**, тема: \"Provider Complaint\". Пожалуйста, укажите:\n"
            "- адрес электронной почты вашей учетной записи и ID Поставщика;\n"
            "- описание решения или действия, на которое подается жалоба;\n"
            "- результат, который вы ищете.\n\n"
            "12.3 Nevumo подтвердит получение жалобы в течение **5 рабочих дней** и предоставит письменный ответ по существу в течение **30 календарных дней** после получения.\n\n"
            "12.4 Внутренняя процедура рассмотрения жалоб является **бесплатной** для Поставщиков.\n\n"
            "12.5 Если вы не удовлетворены результатом внутренней процедуры рассмотрения жалоб, вы можете перейти к посредничеству, как описано в Разделе 13."
        ),
        "uk": (
            "12.1 Постачальники можуть подавати скарги на рішення Nevumo, включаючи рішення про призупинення, обмеження або закриття облікового запису, або про ймовірне недотримання цих Умов для Постачальників.\n\n"
            "12.2 Щоб подати скаргу, напишіть за адресою: **legal@nevumo.com**, тема: \"Provider Complaint\". Будь ласка, вкажіть:\n"
            "- електронну адресу вашого облікового запису та ID Постачальника;\n"
            "- опис рішення або дії, на яку подається скарга;\n"
            "- результат, якого ви прагнете.\n\n"
            "12.3 Nevumo підтвердить отримання скарги протягом **5 робочих днів** і надасть змістовну письмову відповідь протягом **30 календарних днів** з моменту отримання.\n\n"
            "12.4 Внутрішня процедура розгляду скарг є **безкоштовною** для Постачальників.\n\n"
            "12.5 Якщо ви не задоволені результатом внутрішньої процедури розгляду скарг, ви можете перейти до медіації, як описано в Розділі 13."
        ),
        "cs": (
            "12.1 Poskytovatelé mohou podávat stížnosti na rozhodnutí společnosti Nevumo, včetně rozhodnutí o pozastavení, omezení nebo ukončení účtu, nebo na údajné nedodržování těchto podmínek pro poskytovatele.\n\n"
            "12.2 Chcete-li podat stížnost, napište na: **legal@nevumo.com**, předmět: \"Provider Complaint\". Uveďte prosím:\n"
            "- e-mail vašeho účtu a ID poskytovatele;\n"
            "- popis rozhodnutí nebo opatření, na které si stěžujete;\n"
            "- výsledek, o který usilujete.\n\n"
            "12.3 Společnost Nevumo potvrdí přijetí stížnosti do **5 pracovních dnů** a poskytne věcnou písemnou odpověď do **30 kalendářních dnů** od obdržení.\n\n"
            "12.4 Interní postup pro podávání stížností je pro poskytovatele **zdarma**.\n\n"
            "12.5 Pokud nejste spokojeni s výsledkem interního postupu pro podávání stížností, můžete přistoupit k mediaci, jak je popsáno v oddílu 13."
        ),
        "da": (
            "12.1 Udbydere kan indsende klager over Nevumos beslutninger, herunder beslutninger om kontosuspension, begrænsning eller opsigelse, eller påstået manglende overholdelse af disse vilkår for udbydere.\n\n"
            "12.2 For at indsende en klage skal du skrive til: **legal@nevumo.com**, emne: \"Provider Complaint\". Medtag venligst:\n"
            "- din konto-e-mail og udbyder-id;\n"
            "- en beskrivelse af den beslutning eller handling, der klages over;\n"
            "- det resultat, du søger.\n\n"
            "12.3 Nevumo vil bekræfte modtagelsen af klagen inden for **5 hverdage** og give et fyldestgørende skriftligt svar inden for **30 kalenderdage** efter modtagelsen.\n\n"
            "12.4 Den interne klageprocedure er **gratis** for udbydere.\n\n"
            "12.5 Hvis du ikke er tilfreds med resultatet af den interne klageprocedure, kan du gå videre til mægling som beskrevet i afsnit 13."
        ),
        "sv": (
            "12.1 Leverantörer kan lämna in klagomål på Nevumos beslut, inklusive beslut om kontosuspension, begränsning eller uppsägning, eller påstådd bristande efterlevnad av dessa villkor för leverantörer.\n\n"
            "12.2 För att lämna in ett klagomål, skriv till: **legal@nevumo.com**, ämne: \"Provider Complaint\". Vänligen inkludera:\n"
            "- din konto-e-postadress och leverantörs-ID;\n"
            "- en beskrivning av det beslut eller den åtgärd som klagomålet gäller;\n"
            "- det resultat du eftersträvar.\n\n"
            "12.3 Nevumo kommer att bekräfta mottagandet av klagomålet inom **5 arbetsdagar** och ge ett skriftligt svar i sak inom **30 kalenderdagar** efter mottagandet.\n\n"
            "12.4 Det interna klagomålsförfarandet är **kostnadsfritt** för leverantörer.\n\n"
            "12.5 Om du inte är nöjd med resultatet av det interna klagomålsförfarandet kan du gå vidare till medling enligt beskrivningen i avsnitt 13."
        ),
        "no": (
            "12.1 Leverandører kan sende inn klager på Nevumos beslutninger, inkludert beslutninger om kontosuspensjon, begrensning eller oppsigelse, eller påstått manglende overholdelse av disse vilkårene for leverandører.\n\n"
            "12.2 For å sende inn en klage, skriv til: **legal@nevumo.com**, emne: \"Provider Complaint\". Vennligst inkluder:\n"
            "- konto-e-posten din og leverandør-ID;\n"
            "- en beskrivelse av beslutningen eller handlingen du klager på;\n"
            "- resultatet du søker.\n\n"
            "12.3 Nevumo vil bekrefte mottak av klagen innen **5 virkedager** og gi et skriftlig svar innen **30 kalenderdager** etter mottak.\n\n"
            "12.4 Den interne klageprosedyren er **gratis** for leverandører.\n\n"
            "12.5 Hvis du ikke er fornøyd med utfallet av den interne klageprosedyren, kan du gå videre til mekling som beskrevet i seksjon 13."
        ),
        "fi": (
            "12.1 Palveluntarjoajat voivat jättää valituksia Nevumon päätöksistä, mukaan lukien päätökset tilin jäädyttämisestä, rajoittamisesta tai irtisanomisesta, tai väitetystä näiden palveluntarjoajien ehtojen noudattamatta jättämisestä.\n\n"
            "12.2 Jos haluat jättää valituksen, kirjoita osoitteeseen: **legal@nevumo.com**, aihe: \"Provider Complaint\". Sisällytä seuraavat tiedot:\n"
            "- tilisi sähköpostiosoite ja palveluntarjoajan tunnus;\n"
            "- kuvaus päätöksestä tai toimenpiteestä, josta valitetaan;\n"
            "- haluamasi lopputulos.\n\n"
            "12.3 Nevumo vahvistaa valituksen vastaanottamisen **5 työpäivän** kuluessa ja antaa asiallisen kirjallisen vastauksen **30 kalenteripäivän** kuluessa vastaanottamisesta.\n\n"
            "12.4 Sisäinen valitusmenettely on palveluntarjoajille **maksuton**.\n\n"
            "12.5 Jos et ole tyytyväinen sisäisen valitusmenettelyn tulokseen, voit edetä sovitteluun osiossa 13 kuvatulla tavalla."
        ),
        "et": (
            "12.1 Teenusepakkujad võivad esitada kaebusi Nevumo otsuste peale, sealhulgas otsused konto peatamise, piiramise või lõpetamise kohta või nende teenusepakkujate tingimuste väidetava eiramise kohta.\n\n"
            "12.2 Kaebuse esitamiseks kirjutage aadressile: **legal@nevumo.com**, teema: \"Provider Complaint\". Palun lisage:\n"
            "- oma konto e-posti aadress ja teenusepakkuja ID;\n"
            "- kaevatava otsuse või tegevuse kirjeldus;\n"
            "- tulemus, mida te taotlete.\n\n"
            "12.3 Nevumo kinnitab kaebuse kättesaamist **5 tööpäeva** jooksul ja annab sisulise kirjaliku vastuse **30 kalendripäeva** jooksul alates kättesaamisest.\n\n"
            "12.4 Sisemine kaebuste lahendamise menetlus on teenusepakkujatele **tasuta**.\n\n"
            "12.5 Kui te ei ole sisemise kaebuste lahendamise menetluse tulemusega rahul, võite jätkata lepitusega, nagu on kirjeldatud jaotises 13."
        ),
        "lt": (
            "12.1 Paslaugų teikėjai gali teikti skundus dėl Nevumo sprendimų, įskaitant sprendimus dėl paskyros sustabdymo, apribojimo ar nutraukimo, arba dėl tariamo šių Paslaugų teikėjų sąlygų nesilaikymo.\n\n"
            "12.2 Norėdami pateikti skundą, rašykite adresu: **legal@nevumo.com**, tema: „Provider Complaint“. Nurodykite:\n"
            "- savo paskyros el. pašto adresą ir paslaugų teikėjo ID;\n"
            "- skundžiamo sprendimo ar veiksmo aprašymą;\n"
            "- rezultatą, kurio siekiate.\n\n"
            "12.3 Nevumo patvirtins skundo gavimą per **5 darbo dienas** ir pateiks išsamų atsakymą raštu per **30 kalendorinių dienų** nuo gavimo.\n\n"
            "12.4 Vidinė skundų nagrinėjimo procedūra paslaugų teikėjams yra **nemokama**.\n\n"
            "12.5 Jei nesate patenkinti vidinės skundų nagrinėjimo procedūros rezultatais, galite kreiptis į tarpininką, kaip aprašyta 13 skirsnyje."
        ),
        "lv": (
            "12.1 Pakalpojumu sniedzēji var iesniegt sūdzības par Nevumo lēmumiem, tostarp lēmumiem par konta darbības apturēšanu, ierobežošanu vai izbeigšanu, vai par iespējamu šo Pakalpojumu sniedzēju noteikumu neievērošanu.\n\n"
            "12.2 Lai iesniegtu sūdzību, rakstiet uz: **legal@nevumo.com**, tēma: \"Provider Complaint\". Lūdzu, iekļaujiet:\n"
            "- sava konta e-pastu un Pakalpojumu sniedzēja ID;\n"
            "- lēmuma vai darbības, par kuru tiek iesniegta sūdzība, aprakstu;\n"
            "- rezultātu, kuru vēlaties sasniegt.\n\n"
            "12.3 Nevumo apstiprinās sūdzības saņemšanu **5 darba dienu** laikā un sniegs rakstisku atbildi pēc būtības **30 kalendāro dienu** laikā pēc saņemšanas.\n\n"
            "12.4 Iekšējā sūdzību izskatīšanas procedūra Pakalpojumu sniedzējiem ir **bezmaksas**.\n\n"
            "12.5 Ja neesat apmierināts ar iekšējās sūdzību izskatīšanas procedūras rezultātu, varat turpināt mediāciju, kā aprakstīts 13. sadaļā."
        ),
        "hu": (
            "12.1 A Szolgáltatók panaszt nyújthatnak be a Nevumo döntéseivel kapcsolatban, beleértve a fiók felfüggesztésével, korlátozásával vagy megszüntetésével kapcsolatos döntéseket, vagy a jelen Szolgáltatói Feltételek feltételezett be nem tartását.\n\n"
            "12.2 Panasz benyújtásához írjon a **legal@nevumo.com** címre, tárgy: \"Provider Complaint\". Kérjük, adja meg a következőket:\n"
            "- a fiók e-mail címét és a Szolgáltatói azonosítót;\n"
            "- a panaszolt döntés vagy intézkedés leírását;\n"
            "- az Ön által elvárt eredményt.\n\n"
            "12.3 A Nevumo **5 munkanapon** belül visszaigazolja a panasz kézhezvételét, és a kézhezvételtől számított **30 naptári napon** belül érdemi írásbeli választ ad.\n\n"
            "12.4 A belső panaszkezelési eljárás a Szolgáltatók számára **ingyenes**.\n\n"
            "12.5 Ha nem elégedett a belső panaszkezelési eljárás eredményével, a 13. szakaszban leírtak szerint közvetítéshez fordulhat."
        ),
        "hr": (
            "12.1 Pružatelji usluga mogu podnijeti pritužbe na odluke tvrtke Nevumo, uključujući odluke o suspenziji, ograničenju ili zatvaranju računa, ili navodnom nepoštivanju ovih Uvjeta za pružatelje usluga.\n\n"
            "12.2 Da biste podnijeli pritužbu, pišite na: **legal@nevumo.com**, predmet: \"Provider Complaint\". Uključite:\n"
            "- e-poštu vašeg računa i ID Pružatelja usluga;\n"
            "- opis odluke ili radnje na koju se žalite;\n"
            "- ishod koji tražite.\n\n"
            "12.3 Nevumo će potvrditi primitak pritužbe u roku od **5 radnih dana** i pružiti sadržajan pisani odgovor u roku od **30 kalendarskih dana** od primitka.\n\n"
            "12.4 Interni postupak rješavanja pritužbi je **besplatan** za Pružatelje usluga.\n\n"
            "12.5 Ako niste zadovoljni ishodom internog postupka rješavanja pritužbi, možete pokrenuti mirenje kako je opisano u odjeljku 13."
        ),
        "sk": (
            "12.1 Poskytovatelia môžu podávať sťažnosti na rozhodnutia spoločnosti Nevumo, vrátane rozhodnutí o pozastavení, obmedzení alebo ukončení účtu, alebo na údajné nedodržiavanie týchto podmienok pre poskytovateľov.\n\n"
            "12.2 Ak chcete podať sťažnosť, napíšte na: **legal@nevumo.com**, predmet: \"Provider Complaint\". Uveďte prosím:\n"
            "- e-mail vášho účtu a ID poskytovateľa;\n"
            "- opis rozhodnutia alebo opatrenia, na ktoré sa sťažujete;\n"
            "- výsledok, o ktorý sa usilujete.\n\n"
            "12.3 Spoločnosť Nevumo potvrdí prijatie sťažnosti do **5 pracovných dní** a poskytne vecnú písomnú odpoveď do **30 kalendárnych dní** od prijatia.\n\n"
            "12.4 Interný postup podávania sťažností je pre poskytovateľov **bezplatný**.\n\n"
            "12.5 Ak nie ste spokojní s výsledkom interného postupu podávania sťažností, môžete pristúpiť k mediácii, ako je opísané v oddiele 13."
        ),
        "sl": (
            "12.1 Ponudniki lahko vložijo pritožbe glede odločitev podjetja Nevumo, vključno z odločitvami o začasni ustavitvi, omejitvi ali prekinitvi računa, ali domnevnem neupoštevanju teh pogojev za ponudnike.\n\n"
            "12.2 Za oddajo pritožbe pišite na: **legal@nevumo.com**, zadeva: \"Provider Complaint\". Vključite:\n"
            "- e-poštni naslov vašega računa in ID ponudnika;\n"
            "- opis odločitve ali dejanja, na katerega se pritožujete;\n"
            "- rezultat, ki ga iščete.\n\n"
            "12.3 Nevumo bo potrdil prejem pritožbe v **5 delovnih dneh** in zagotovil vsebinski pisni odgovor v **30 koledarskih dneh** od prejema.\n\n"
            "12.4 Notranji pritožbeni postopek je za ponudnike **brezplačen**.\n\n"
            "12.5 Če niste zadovoljni z izidom notranjega pritožbenega postopka, lahko nadaljujete z mediacijo, kot je opisano v razdelku 13."
        ),
        "el": (
            "12.1 Οι Πάροχοι μπορούν να υποβάλλουν παράπονα σχετικά με τις αποφάσεις της Nevumo, συμπεριλαμβανομένων αποφάσεων για αναστολή, περιορισμό ή τερματισμό λογαριασμού, ή για εικαζόμενη μη συμμόρφωση με αυτούς τους Όρους Παρόχου.\n\n"
            "12.2 Για να υποβάλετε ένα παράπονο, γράψτε στο: **legal@nevumo.com**, θέμα: \"Provider Complaint\". Παρακαλούμε συμπεριλάβετε:\n"
            "- το email του λογαριασμού σας και το ID Παρόχου.\n"
            "- μια περιγραφή της απόφασης ή της ενέργειας για την οποία παραπονείστε.\n"
            "- το αποτέλεσμα που επιδιώκετε.\n\n"
            "12.3 Η Nevumo θα επιβεβαιώσει τη λήψη του παραπόνου εντός **5 εργάσιμων ημερών** και θα παράσχει ουσιαστική γραπτή απάντηση εντός **30 ημερολογιακών ημερών** από τη λήψη.\n\n"
            "12.4 Η εσωτερική διαδικασία παραπόνων είναι **δωρεάν** για τους Παρόχους.\n\n"
            "12.5 Εάν δεν είστε ικανοποιημένοι με το αποτέλεσμα της εσωτερικής διαδικασίας παραπόνων, μπορείτε να προχωρήσετε σε διαμεσολάβηση όπως περιγράφεται στην Ενότητα 13."
        ),
        "tr": (
            "12.1 Sağlayıcılar, hesabın askıya alınması, kısıtlanması veya feshedilmesine ilişkin kararlar veya bu Sağlayıcı Şartlarına uyulmadığı iddiası dahil olmak üzere Nevumo'nun kararları hakkında şikayette bulunabilirler.\n\n"
            "12.2 Şikayette bulunmak için şu adrese yazın: **legal@nevumo.com**, konu: \"Provider Complaint\". Lütfen şunları ekleyin:\n"
            "- hesap e-postanız ve Sağlayıcı Kimliğiniz;\n"
            "- şikayet edilen kararın veya eylemin açıklaması;\n"
            "- aradığınız sonuç.\n\n"
            "12.3 Nevumo, şikayetin alındığını **5 iş günü** içinde onaylayacak ve alındıktan sonraki **30 takvim günü** içinde esaslı bir yazılı yanıt verecektir.\n\n"
            "12.4 Dahili şikayet prosedürü Sağlayıcılar için **ücretsizdir**.\n\n"
            "12.5 Dahili şikayet prosedürünün sonucundan memnun kalmazsanız, Bölüm 13'te açıklandığı gibi arabuluculuğa başvurabilirsiniz."
        ),
        "ga": (
            "12.1 Féadfaidh Soláthraithe gearáin a chur isteach faoi chinntí Nevumo, lena n-áirítear cinntí ar fhionraí, srianadh nó foirceannadh cuntais, nó neamhchomhlíonadh líomhnaithe leis na Téarmaí Soláthraí seo.\n\n"
            "12.2 Chun gearán a chur isteach, scríobh chuig: **legal@nevumo.com**, ábhar: \"Provider Complaint\". Cuir san áireamh, le do thoil:\n"
            "- ríomhphost do chuntais agus d'Aitheantas Soláthraí;\n"
            "- cur síos ar an gcinneadh nó an gníomh a bhfuil gearán á dhéanamh faoi;\n"
            "- an toradh atá á lorg agat.\n\n"
            "12.3 Admhóidh Nevumo fáil an ghearáin laistigh de **5 lá gnó** agus soláthróidh sé freagra scríofa substainteach laistigh de **30 lá féilire** ón bhfáil.\n\n"
            "12.4 Tá an nós imeachta gearán inmheánach **saor in aisce** do Sholáthraithe.\n\n"
            "12.5 Mura bhfuil tú sásta le toradh an nós imeachta gearán inmheánach, féadfaidh tú dul ar aghaidh go hidirghabháil mar a thuairiscítear i Roinn 13."
        ),
        "is": (
            "12.1 Þjónustuveitendur geta lagt fram kvartanir vegna ákvarðana Nevumo, þar á meðal ákvarðana um stöðvun, takmörkun eða uppsögn reiknings, eða meints vanefnda á þessum skilmálum fyrir þjónustuveitendur.\n\n"
            "12.2 Til að leggja fram kvörtun skaltu skrifa á: **legal@nevumo.com**, efni: \"Provider Complaint\". Vinsamlegast láttu fylgja með:\n"
            "- netfang reikningsins þíns og auðkenni þjónustuveitanda;\n"
            "- lýsingu á þeirri ákvörðun eða aðgerð sem kvartað er yfir;\n"
            "- þeirri niðurstöðu sem þú sækist eftir.\n\n"
            "12.3 Nevumo mun staðfesta móttöku kvörtunarinnar innan **5 virkra daga** og veita efnislegt skriflegt svar innan **30 almanaksdaga** frá móttöku.\n\n"
            "12.4 Innra kvörtunarferlið er **ókeypis** fyrir þjónustuveitendur.\n\n"
            "12.5 Ef þú ert ekki ánægður með niðurstöðu innra kvörtunarferlisins geturðu farið í sáttameðferð eins og lýst er í hluta 13."
        ),
        "lb": (
            "12.1 Ubidder kënne Reklamatiounen iwwer d'Entscheedunge vum Nevumo asetzen, inklusiv Entscheedungen iwwer d'Suspensioun, Restriktioun oder Kënnegung vum Kont, oder angeblechen Net-Respektéiere vun dësen Ubidderbedéngungen.\n\n"
            "12.2 Fir eng Reklamatioun ofzeginn, schreift un: **legal@nevumo.com**, Betreff: \"Provider Complaint\". Gitt w.e.g. un:\n"
            "- Är Kont-E-Mail an Är Ubidder-ID;\n"
            "- eng Beschreiwung vun der Entscheedung oder Handlung, iwwer déi Dir Iech beschwéiert;\n"
            "- dat Resultat dat Dir ustrieft.\n\n"
            "12.3 Nevumo wäert den Empfang vun der Reklamatioun bannent **5 Aarbechtsdeeg** bestätegen an eng inhaltlech schrëftlech Äntwert bannent **30 Kalennerdeeg** nom Empfang ginn.\n\n"
            "12.4 Déi intern Reklamatiounsprozedur ass fir Ubidder **gratis**.\n\n"
            "12.5 Wann Dir mam Resultat vun der interner Reklamatiounsprozedur net zefridde sidd, kënnt Dir mat der Mediatioun virfueren, wéi am Sektioun 13 beschriwwen."
        ),
        "mk": (
            "12.1 Давателите можат да поднесат поплаки за одлуките на Nevumo, вклучувајќи одлуки за суспензија, ограничување или раскинување на профил, или наводно непочитување на овие Услови за Даватели.\n\n"
            "12.2 За да поднесете поплака, пишете на: **legal@nevumo.com**, тема: \"Provider Complaint\". Ве молиме вклучете:\n"
            "- е-поштата на вашиот профил и ID на Давател;\n"
            "- опис на одлуката или дејството за кое се жалите;\n"
            "- исходот што го барате.\n\n"
            "12.3 Nevumo ќе го потврди приемот на поплаката во рок од **5 работни дена** и ќе обезбеди суштински писмен одговор во рок од **30 календарски дена** од приемот.\n\n"
            "12.4 Внатрешната процедура за поплаки е **бесплатна** за Давателите.\n\n"
            "12.5 Доколку не сте задоволни со исходот од внатрешната процедура за поплаки, можете да продолжите кон медијација како што е опишано во Дел 13."
        ),
        "mt": (
            "12.1 Fornituri jistgħu jissottomettu ilmenti dwar id-deċiżjonijiet ta' Nevumo, inklużi deċiżjonijiet dwar sospensjoni, restrizzjoni, jew terminazzjoni ta' kont, jew allegat nuqqas ta' konformità ma' dawn it-Termini għall-Fornituri.\n\n"
            "12.2 Biex tissottometti ilment, ikteb lil: **legal@nevumo.com**, suġġett: \"Provider Complaint\". Jekk jogħġbok inkludi:\n"
            "- l-email tal-kont tiegħek u l-ID tal-Fornitur;\n"
            "- deskrizzjoni tad-deċiżjoni jew azzjoni li qed tilmenta dwarha;\n"
            "- ir-riżultat li qed tfittex.\n\n"
            "12.3 Nevumo ser jirrikonoxxi l-irċevuta tal-ilment fi żmien **5 ijiem tax-xogħol** u jipprovdi tweġiba sostantiva bil-miktub fi żmien **30 jum kalendarju** mill-wasla.\n\n"
            "12.4 Il-proċedura interna tal-ilmenti hija **mingħajr ħlas** għall-Fornituri.\n\n"
            "12.5 Jekk m'intix sodisfatt bir-riżultat tal-proċedura interna tal-ilmenti, tista' tipproċedi għall-medjazzjoni kif deskritt fit-Taqsima 13."
        ),
        "sq": (
            "12.1 Ofruesit mund të paraqesin ankesa rreth vendimeve të Nevumo, duke përfshirë vendimet për pezullimin, kufizimin ose përfundimin e llogarisë, ose mospërputhjen e supozuar me këto Kushte për Ofruesit.\n\n"
            "12.2 Për të paraqitur një ankesë, shkruani në: **legal@nevumo.com**, subjekti: \"Provider Complaint\". Ju lutemi përfshini:\n"
            "- email-in e llogarisë suaj dhe ID-në e Ofruesit;\n"
            "- një përshkrim të vendimit ose veprimit për të cilin ankoheni;\n"
            "- rezultatin që kërkoni.\n\n"
            "12.3 Nevumo do të konfirmojë marrjen e ankesës brenda **5 ditëve të punës** dhe do të ofrojë një përgjigje thelbësore me shkrim brenda **30 ditëve kalendarike** nga marrja.\n\n"
            "12.4 Procedura e brendshme e ankesave është **falas** për Ofruesit.\n\n"
            "12.5 Nëse nuk jeni të kënaqur me rezultatin e procedurës së brendshme të ankesave, mund të vazhdoni me ndërmjetësimin siç përshkruhet në Seksionin 13."
        ),
        "sr": (
            "12.1 Pružaoci usluga mogu podnositi pritužbe na odluke kompanije Nevumo, uključujući odluke o suspenziji, ograničenju ili zatvaranju naloga, ili navodnom nepoštovanju ovih Uslova za pružaoce usluga.\n\n"
            "12.2 Da biste podneli pritužbu, pišite na: **legal@nevumo.com**, predmet: \"Provider Complaint\". Uključite:\n"
            "- e-poštu vašeg naloga i ID Pružaoca usluga;\n"
            "- opis odluke ili radnje na koju se žalite;\n"
            "- ishod koji tražite.\n\n"
            "12.3 Nevumo će potvrditi prijem pritužbe u roku od **5 radnih dana** i pružiti sadržajan pisani odgovor u roku od **30 kalendarskih dana** od prijema.\n\n"
            "12.4 Interni postupak rešavanja pritužbi je **besplatan** za Pružaoce usluga.\n\n"
            "12.5 Ako niste zadovoljni ishodom internog postupka rešavanja pritužbi, možete pokrenuti posredovanje kako je opisano u odeljku 13."
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
            
            for lang, text_val in lang_values.items():
                query = text("""
                    INSERT INTO translations (key, lang, value)
                    VALUES (:k, :l, :v)
                    ON CONFLICT (key, lang)
                    DO UPDATE SET value = EXCLUDED.value
                """)
                session.execute(query, {"k": db_key, "l": lang, "v": text_val})
                count += 1

        session.commit()
        print(f"✅ Seeded {count} translations for {NAMESPACE}.art12_body")

if __name__ == "__main__":
    seed()
