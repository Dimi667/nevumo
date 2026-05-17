"""
seed_provider_terms_p12_art5_body.py  —  Nevumo | namespace: provider_terms
Key: art5_body  (1 key x 34 langs = 34 rows)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_provider_terms_p12_art5_body
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
    "art5_body": {
        "en": (
            "5.1 Nevumo displays Provider profiles and Service Listings in search results and category listings. The order in which Providers appear (ranking) is determined by the following parameters:\n\n"
            "- Profile completeness (High weight): Profiles with full information, photo, and verified contact details rank higher.\n"
            "- Average review score (High weight): Higher average rating from verified Clients improves ranking.\n"
            "- Response rate and speed (Medium weight): Providers who respond to Leads promptly receive a higher position.\n"
            "- Activity recency (Medium weight): Recently active profiles rank above inactive ones.\n"
            "- Service geographic match (Medium weight): Proximity or match to the Client's city.\n"
            "- Account standing (High weight): Accounts without warnings or restrictions rank higher.\n\n"
            "5.2 Payment does not affect organic ranking. Nevumo does not accept payments in exchange for ranking improvements in organic search results.\n\n"
            "5.3 Nevumo may offer paid promotional placements (sponsored positions) in the future. Such placements will be clearly labelled as Sponsored or Promoted. Any introduction of paid promotions will be announced with at least 30 days' notice.\n\n"
            "5.4 Nevumo may modify the ranking algorithm periodically. Material changes to ranking parameters will be communicated to Providers via the notice procedure set out in Section 10."
        ),
        "pl": (
            "5.1 Nevumo wyswietla profile Dostawcow i Oferty Uslug w wynikach wyszukiwania oraz w listingach kategorii. Kolejnosc, w jakiej Dostawcy sa prezentowani (ranking), ustalana jest na podstawie nastepujacych parametrow:\n\n"
            "- Kompletnosc profilu (wysoka waga): Profile z pelnymi informacjami, zdjeciem i zweryfikowanymi danymi kontaktowymi zajmuja wyzsze pozycje.\n"
            "- Srednia ocena opinii (wysoka waga): Wyzsza srednia ocena od zweryfikowanych Klientow poprawia pozycje w rankingu.\n"
            "- Wskaznik i szybkosc odpowiedzi (srednia waga): Dostawcy, ktorzy szybko odpowiadaja na Zapytania, zajmuja wyzsza pozycje.\n"
            "- Aktywnosc na Platformie (srednia waga): Profile aktywne ostatnio maja przewage nad nieaktywnymi.\n"
            "- Dopasowanie geograficzne uslugi (srednia waga): Bliskosc lub zgodnosc z miastem Klienta.\n"
            "- Status konta (wysoka waga): Konta bez ostrzezen ani ograniczen zajmuja wyzsze pozycje.\n\n"
            "5.2 Platnosc nie wplywa na organiczny ranking. Nevumo nie przyjmuje platnosci w zamian za poprawe pozycji w organicznych wynikach wyszukiwania.\n\n"
            "5.3 W przyszlosci Nevumo moze oferowac platne pozycje promocyjne (pozycje sponsorowane). Takie pozycje beda wyraznie oznaczone jako Sponsorowane lub Promowane. O wprowadzeniu platnych promocji Dostawcy zostana poinformowani z wyprzedzeniem co najmniej 30 dni.\n\n"
            "5.4 Nevumo moze okresowo modyfikowac algorytm rankingowy. O istotnych zmianach parametrow rankingowych Dostawcy zostana poinformowani zgodnie z procedura powiadomien okreslona w paragrafie 10."
        ),
        "bg": (
            "5.1 Nevumo показва профилите на Доставчиците и Обявите за услуги в резултатите от търсенето и в категорийните листинги. Редът, в който се показват Доставчиците (класиране), се определя от следните параметри:\n\n"
            "- Пълнота на профила (висока тежест): Профилите с пълна информация, снимка и верифицирани данни за контакт се класират по-високо.\n"
            "- Средна оценка от отзиви (висока тежест): По-висока средна оценка от верифицирани Клиенти подобрява класирането.\n"
            "- Коефициент и скорост на отговор (средна тежест): Доставчиците, които отговарят на Запитванията бързо, получават по-висока позиция.\n"
            "- Скорошна активност (средна тежест): Наскоро активните профили се класират над неактивните.\n"
            "- Географско съответствие на услугата (средна тежест): Близост или съответствие с града на Клиента.\n"
            "- Статус на акаунта (висока тежест): Акаунтите без предупреждения или ограничения се класират по-високо.\n\n"
            "5.2 Плащането не влияе на органичното класиране. Nevumo не приема плащания срещу подобряване на позицията в органичните резултати от търсенето.\n\n"
            "5.3 В бъдеще Nevumo може да предложи платени промоционални позиции (спонсорирани позиции). Такива позиции ще бъдат ясно обозначени като Спонсорирани или Промотирани. Въвеждането на платени промоции ще бъде обявено с предизвестие от поне 30 дни.\n\n"
            "5.4 Nevumo може периодично да променя алгоритъма за класиране. Съществени промени в параметрите за класиране ще бъдат съобщавани на Доставчиците по реда за уведомяване, установен в Раздел 10."
        ),
        "de": (
            "5.1 Nevumo zeigt Dienstleisterprofile und Serviceangebote in Suchergebnissen und Kategorielisten an. Die Reihenfolge, in der Dienstleister erscheinen (Ranking), wird durch folgende Parameter bestimmt:\n\n"
            "- Vollständigkeit des Profils (hohes Gewicht): Profile mit vollständigen Informationen, Foto und verifizierten Kontaktdaten ranken höher.\n"
            "- Durchschnittliche Bewertung (hohes Gewicht): Eine höhere Durchschnittsbewertung von verifizierten Kunden verbessert das Ranking.\n"
            "- Antwortrate und -geschwindigkeit (mittleres Gewicht): Dienstleister, die schnell auf Anfragen reagieren, erhalten eine höhere Position.\n"
            "- Aktualität der Aktivität (mittleres Gewicht): Kürzlich aktive Profile ranken über inaktiven.\n"
            "- Geografische Übereinstimmung (mittleres Gewicht): Nähe oder Übereinstimmung mit der Stadt des Kunden.\n"
            "- Kontostatus (hohes Gewicht): Konten ohne Warnungen oder Einschränkungen ranken höher.\n\n"
            "5.2 Zahlungen beeinflussen das organische Ranking nicht. Nevumo akzeptiert keine Zahlungen für Ranking-Verbesserungen in organischen Suchergebnissen.\n\n"
            "5.3 Nevumo kann in Zukunft bezahlte Werbeplatzierungen (gesponserte Positionen) anbieten. Solche Platzierungen werden klar als Gesponsert oder Beworben gekennzeichnet. Die Einführung bezahlter Werbung wird mit mindestens 30 Tagen Vorankündigung bekannt gegeben.\n\n"
            "5.4 Nevumo kann den Ranking-Algorithmus regelmäßig ändern. Wesentliche Änderungen der Ranking-Parameter werden den Dienstleistern über das in Abschnitt 10 beschriebene Benachrichtigungsverfahren mitgeteilt."
        ),
        "fr": (
            "5.1 Nevumo affiche les profils des Prestataires et les Annonces de services dans les resultats de recherche et les listes de categories. L'ordre d'affichage des Prestataires (classement) est determine par les parametres suivants :\n\n"
            "- Exhaustivite du profil (poids eleve) : Les profils avec des informations completes, une photo et des coordonnees verifiees sont mieux classes.\n"
            "- Note moyenne des avis (poids eleve) : Une note moyenne plus elevee de la part de Clients verifies ameliore le classement.\n"
            "- Taux et rapidite de reponse (poids moyen) : Les Prestataires qui repondent rapidement aux Leads obtiennent une meilleure position.\n"
            "- Recence de l'activite (poids moyen) : Les profils recemment actifs sont mieux classes que les inactifs.\n"
            "- Correspondance geographique du service (poids moyen) : Proximite ou correspondance avec la ville du Client.\n"
            "- Statut du compte (poids eleve) : Les comptes sans avertissements ni restrictions sont mieux classes.\n\n"
            "5.2 Le paiement n'affecte pas le classement organique. Nevumo n'accepte pas de paiements en echange d'ameliorations de classement dans les resultats de recherche organiques.\n\n"
            "5.3 Nevumo pourra proposer a l'avenir des placements publicitaires payants (positions sponsorisees). Ces placements seront clairement etiquetes comme Sponsorise ou Promu. Toute introduction de promotions payantes sera annoncee avec un preavis d'au moins 30 jours.\n\n"
            "5.4 Nevumo peut modifier l'algorithme de classement periodiquement. Les modifications importantes des parametres de classement seront communiquees aux Prestataires via la procedure de notification decrite a la Section 10."
        ),
        "es": (
            "5.1 Nevumo muestra los perfiles de los Proveedores y los Listados de servicios en los resultados de busqueda y los listados de categorias. El orden en que aparecen los Proveedores (clasificacion) se determina por los siguientes parametros:\n\n"
            "- Completitud del perfil (peso alto): Los perfiles con informacion completa, foto y datos de contacto verificados se clasifican mas alto.\n"
            "- Puntuacion media de resenas (peso alto): Una puntuacion media mas alta de Clientes verificados mejora la clasificacion.\n"
            "- Tasa y velocidad de respuesta (peso medio): Los Proveedores que responden rapidamente a los Leads reciben una posicion mas alta.\n"
            "- Recencia de actividad (peso medio): Los perfiles activos recientemente se clasifican por encima de los inactivos.\n"
            "- Coincidencia geografica del servicio (peso medio): Proximidad o coincidencia con la ciudad del Cliente.\n"
            "- Estado de la cuenta (peso alto): Las cuentas sin advertencias ni restricciones se clasifican mas alto.\n\n"
            "5.2 El pago no afecta la clasificacion organica. Nevumo no acepta pagos a cambio de mejoras de clasificacion en los resultados de busqueda organicos.\n\n"
            "5.3 Nevumo podra ofrecer ubicaciones promocionales de pago (posiciones patrocinadas) en el futuro. Dichas ubicaciones seran claramente etiquetadas como Patrocinado o Promovido. Cualquier introduccion de promociones de pago se anunciara con al menos 30 dias de antelacion.\n\n"
            "5.4 Nevumo puede modificar el algoritmo de clasificacion periodicamente. Los cambios materiales en los parametros de clasificacion se comunicaran a los Proveedores a traves del procedimiento de notificacion establecido en la Seccion 10."
        ),
        "it": (
            "5.1 Nevumo mostra i profili dei Fornitori e gli Annunci di servizi nei risultati di ricerca e negli elenchi di categorie. L'ordine in cui appaiono i Fornitori (posizionamento) e determinato dai seguenti parametri:\n\n"
            "- Completezza del profilo (peso alto): I profili con informazioni complete, foto e dati di contatto verificati si posizionano piu in alto.\n"
            "- Punteggio medio delle recensioni (peso alto): Una valutazione media piu alta da parte di Clienti verificati migliora il posizionamento.\n"
            "- Tasso e velocita di risposta (peso medio): I Fornitori che rispondono prontamente ai Lead ricevono una posizione piu alta.\n"
            "- Recency dell'attivita (peso medio): I profili recentemente attivi si posizionano sopra quelli inattivi.\n"
            "- Corrispondenza geografica del servizio (peso medio): Vicinanza o corrispondenza con la citta del Cliente.\n"
            "- Stato dell'account (peso alto): Gli account senza avvertimenti o restrizioni si posizionano piu in alto.\n\n"
            "5.2 Il pagamento non influisce sul posizionamento organico. Nevumo non accetta pagamenti in cambio di miglioramenti del posizionamento nei risultati di ricerca organici.\n\n"
            "5.3 Nevumo potra offrire in futuro posizionamenti promozionali a pagamento (posizioni sponsorizzate). Tali posizionamenti saranno chiaramente etichettati come Sponsorizzato o Promosso. Qualsiasi introduzione di promozioni a pagamento sara annunciata con almeno 30 giorni di preavviso.\n\n"
            "5.4 Nevumo puo modificare periodicamente l'algoritmo di posizionamento. Le modifiche sostanziali ai parametri di posizionamento saranno comunicate ai Fornitori tramite la procedura di notifica descritta nella Sezione 10."
        ),
        "nl": (
            "5.1 Nevumo toont Dienstverlenersprofielen en Serviceaanbiedingen in zoekresultaten en categorieoverzichten. De volgorde waarin Dienstverleners verschijnen (rangschikking) wordt bepaald door de volgende parameters:\n\n"
            "- Volledigheid profiel (hoog gewicht): Profielen met volledige informatie, foto en geverifieerde contactgegevens ranken hoger.\n"
            "- Gemiddelde beoordelingsscore (hoog gewicht): Een hogere gemiddelde score van geverifieerde Klanten verbetert de rangschikking.\n"
            "- Responspercentage en -snelheid (gemiddeld gewicht): Dienstverleners die snel reageren op Leads krijgen een hogere positie.\n"
            "- Recente activiteit (gemiddeld gewicht): Recent actieve profielen ranken boven inactieve.\n"
            "- Geografische overeenkomst van de dienst (gemiddeld gewicht): Nabijheid of overeenkomst met de stad van de Klant.\n"
            "- Accountstatus (hoog gewicht): Accounts zonder waarschuwingen of beperkingen ranken hoger.\n\n"
            "5.2 Betaling heeft geen invloed op de organische rangschikking. Nevumo aanvaardt geen betalingen in ruil voor rangschikkingsverbeteringen in organische zoekresultaten.\n\n"
            "5.3 Nevumo kan in de toekomst betaalde promotionele plaatsingen (gesponsorde posities) aanbieden. Dergelijke plaatsingen zullen duidelijk worden aangeduid als Gesponsord of Gepromoot. De introductie van betaalde promoties wordt aangekondigd met ten minste 30 dagen vooraankondiging.\n\n"
            "5.4 Nevumo kan het rangschikkingsalgoritme periodiek aanpassen. Wezenlijke wijzigingen in rangschikkingsparameters worden aan Dienstverleners gecommuniceerd via de kennisgevingsprocedure beschreven in Sectie 10."
        ),
        "pt": (
            "5.1 A Nevumo exibe perfis de Prestadores e Listagens de servicos nos resultados de pesquisa e nas listas de categorias. A ordem em que os Prestadores aparecem (classificacao) e determinada pelos seguintes parametros:\n\n"
            "- Completude do perfil (peso alto): Perfis com informacoes completas, foto e dados de contacto verificados classificam-se mais alto.\n"
            "- Pontuacao media de avaliacoes (peso alto): Uma pontuacao media mais alta de Clientes verificados melhora a classificacao.\n"
            "- Taxa e velocidade de resposta (peso medio): Prestadores que respondem prontamente aos Leads recebem uma posicao mais alta.\n"
            "- Recencia de atividade (peso medio): Perfis recentemente ativos classificam-se acima dos inativos.\n"
            "- Correspondencia geografica do servico (peso medio): Proximidade ou correspondencia com a cidade do Cliente.\n"
            "- Estado da conta (peso alto): Contas sem avisos ou restricoes classificam-se mais alto.\n\n"
            "5.2 O pagamento nao afeta a classificacao organica. A Nevumo nao aceita pagamentos em troca de melhorias de classificacao nos resultados de pesquisa organicos.\n\n"
            "5.3 A Nevumo podera oferecer no futuro posicionamentos promocionais pagos (posicoes patrocinadas). Tais posicionamentos serao claramente rotulados como Patrocinado ou Promovido. A introducao de promocoes pagas sera anunciada com pelo menos 30 dias de antecedencia.\n\n"
            "5.4 A Nevumo pode modificar o algoritmo de classificacao periodicamente. Alteracoes materiais nos parametros de classificacao serao comunicadas aos Prestadores atraves do procedimento de notificacao definido na Seccao 10."
        ),
        "pt-PT": (
            "5.1 A Nevumo apresenta perfis de Prestadores e Listagens de servicos nos resultados de pesquisa e nas listas de categorias. A ordem em que os Prestadores aparecem (classificacao) e determinada pelos seguintes parametros:\n\n"
            "- Completude do perfil (peso elevado): Perfis com informacoes completas, fotografia e dados de contacto verificados classificam-se mais alto.\n"
            "- Pontuacao media de avaliacoes (peso elevado): Uma pontuacao media mais elevada de Clientes verificados melhora a classificacao.\n"
            "- Taxa e velocidade de resposta (peso medio): Prestadores que respondem prontamente aos Leads recebem uma posicao mais elevada.\n"
            "- Recencia de actividade (peso medio): Perfis recentemente activos classificam-se acima dos inactivos.\n"
            "- Correspondencia geografica do servico (peso medio): Proximidade ou correspondencia com a cidade do Cliente.\n"
            "- Estado da conta (peso elevado): Contas sem avisos ou restricoes classificam-se mais alto.\n\n"
            "5.2 O pagamento nao afecta a classificacao organica. A Nevumo nao aceita pagamentos em troca de melhorias de classificacao nos resultados de pesquisa organicos.\n\n"
            "5.3 A Nevumo podera oferecer no futuro posicionamentos promocionais pagos (posicoes patrocinadas). Tais posicionamentos serao claramente identificados como Patrocinado ou Promovido. A introducao de promocoes pagas sera anunciada com pelo menos 30 dias de antecedencia.\n\n"
            "5.4 A Nevumo pode modificar o algoritmo de classificacao periodicamente. Alteracoes materiais nos parametros de classificacao serao comunicadas aos Prestadores atraves do procedimento de notificacao definido na Seccao 10."
        ),
        "ro": (
            "5.1 Nevumo afiseaza profilurile Furnizorilor si Listarile de servicii in rezultatele cautarii si in listele de categorii. Ordinea in care apar Furnizorii (clasament) este determinata de urmatorii parametri:\n\n"
            "- Completitudinea profilului (pondere ridicata): Profilurile cu informatii complete, fotografie si date de contact verificate se clasifica mai sus.\n"
            "- Scorul mediu al recenziilor (pondere ridicata): Un rating mediu mai mare din partea Clientilor verificati imbunatateste clasamentul.\n"
            "- Rata si viteza de raspuns (pondere medie): Furnizorii care raspund prompt la Lead-uri primesc o pozitie mai inalta.\n"
            "- Recenta activitatii (pondere medie): Profilurile recent active se clasifica deasupra celor inactive.\n"
            "- Potrivirea geografica a serviciului (pondere medie): Proximitate sau potrivire cu orasul Clientului.\n"
            "- Starea contului (pondere ridicata): Conturile fara avertismente sau restrictii se clasifica mai sus.\n\n"
            "5.2 Plata nu afecteaza clasamentul organic. Nevumo nu accepta plati in schimbul imbunatatirii clasamentului in rezultatele organice ale cautarii.\n\n"
            "5.3 Nevumo poate oferi in viitor plasamente promotionale platite (pozitii sponsorizate). Astfel de plasamente vor fi clar etichetate ca Sponsorizat sau Promovat. Orice introducere a promotiilor platite va fi anuntata cu cel putin 30 de zile inainte.\n\n"
            "5.4 Nevumo poate modifica periodic algoritmul de clasament. Modificarile semnificative ale parametrilor de clasament vor fi comunicate Furnizorilor prin procedura de notificare prevazuta la Sectiunea 10."
        ),
        "ru": (
            "5.1 Nevumo otobrazhayet profili Postavshchikov i Ob'yavleniya ob uslugakh v rezultatakh poiska i kategoriynnykh spiskakh. Poryadok otobrazheniya Postavshchikov (reyting) opredelyaetsya sleduyushchimi parametrami:\n\n"
            "- Polnota profilya (vysokiy ves): Profili s polnoy informatsiey, foto i verifilsirovannymi kontaktnymi dannymi imeyut bolee vyssokuyu pozitsiyu.\n"
            "- Srednyaya otsenka otzyrov (vysokiy ves): Bolee vysokiy srednyy reyting ot verifirovannykh Klientov uluchshayet pozitsiyu.\n"
            "- Koeffitsient i skorost otveta (sredniy ves): Postavshchiki, bystro otvechayushchiye na Lidy, poluchayut bolee vysokuyu pozitsiyu.\n"
            "- Nedavnyaya aktivnost (sredniy ves): Nedavno aktivnyye profili rankiruyutsya vyshe neaktivnykh.\n"
            "- Geograficheskoye sootvetstviye uslugi (sredniy ves): Blizkost ili sootvetstviye gorodu Klienta.\n"
            "- Status akkaunta (vysokiy ves): Akkaunty bez preduprezhdeny ili ogranicheniy imeyut bolee vysokuyu pozitsiyu.\n\n"
            "5.2 Oplata ne vliyayet na organicheskiy reyting. Nevumo ne prinimayet platezhey v obmen na uluchsheniye pozitsii v organicheskikh rezultatakh poiska.\n\n"
            "5.3 V budushchem Nevumo mozhet predlagat platnye reklamnyye razmeshcheniya (sponsirovannyye pozitsii). Takiye razmeshcheniya budut yasno pomecheny kak Sponsorirovannoye ili Prodvigayemoye. Vvedeniye platnykh aktsiy budet ob'yavleno s preduprezhdeniyem ne meneye 30 dney.\n\n"
            "5.4 Nevumo mozhet periodicheski izmenyat algoritm reytinga. O sushchestvennykh izmeneniyakh parametrov reytinga Postavshchiki budut uvedomleny cherez protseduru uvedomleniya, opisannuyu v Razdele 10."
        ),
        "uk": (
            "5.1 Nevumo vidobrazhaye profili Postachalnikiv ta Oholoshennia pro posluhy v rezultatakh poshuku ta kategoriynykh spyskakh. Poriadok vidobrazhennia Postachalnikiv (reytыnh) vyznachayetsya nastupnymy parametramy:\n\n"
            "- Povnota profilyu (vysokа vaha): Profili z povnoyu informatsiieiu, foto ta veryfikovanymy kontaktnymy danymy mayut vyschu pozytsiiu.\n"
            "- Serednia otsinka vidhukov (vysoka vaha): Vyscha serednia otsinka vid veryfikovanykh Kliyentiv polipshuye pozytsiiu.\n"
            "- Koefitsient i shvydkist vidpovidi (serednia vaha): Postachalniky, yaki shvydko vidpovidayut na Lidy, otrymuyut vyschu pozytsiiu.\n"
            "- Nedavnia aktyvnist (serednia vaha): Nednno aktyvni profili rankuyutsya vyshe neaktyvnykh.\n"
            "- Heohrafichna vidpovidnist posluhy (serednia vaha): Blyzкist abo vidpovidnist mistu Kliyenta.\n"
            "- Status oblіkovoho zapysu (vysoka vaha): Oblіkovi zapysy bez poperedzen abo obmezhen mayut vyschu pozytsiiu.\n\n"
            "5.2 Oplata ne vplyvaye na orhanichnыy reytыnh. Nevumo ne pryymayet platezhiv v obmin na polipshennya pozytsiyi v orhanichnykh rezultatakh poshuku.\n\n"
            "5.3 U maybutnomu Nevumo mozhe proponuvaty platni reklamni rozmishchennia (sponsorovani pozytsiyi). Taki rozmishchennia budut chіtko poznacheni yak Sponsorovane abo Prosuvane. Vprovadzhennia platnykh aktsiy bude anonsovano z poperedzhennyam ne menshe 30 dniv.\n\n"
            "5.4 Nevumo mozhe periodychno zminyuvaty alhorytm reytynhu. Pro iстottni zminy parametriv reytynhu Postachalnykiv bude povidomleno cherez protseduru povidomlennia, vyznachenu v Rozdili 10."
        ),
        "cs": (
            "5.1 Nevumo zobrazuje profily Poskytovatelu a Nabidky sluzeb ve vysledcich vyhledavani a v kategorializacich. Porad, v nemz se Poskytovatel zobrazuji (poradi), je urceno nasledujicimi parametry:\n\n"
            "- Uplnost profilu (vysoka vaha): Profily s uplnymi informacemi, fotkou a overenymi kontaktnimi udaji jsou razeny vysе.\n"
            "- Prumerna hodnoceni recenzi (vysoka vaha): Vyssi prumerné hodnoceni od overenykh Klientu zlepsuje poradí.\n"
            "- Mira a rychlost odpovedi (stredni vaha): Poskytovatelé, kteri rychle reaguji na Leady, dostávají vyssi pozici.\n"
            "- Nedavna aktivita (stredni vaha): Nedavno aktivni profily jsou razeny nad neaktivnimi.\n"
            "- Geograficka shoda sluzby (stredni vaha): Blizkost nebo shoda s mestem Klienta.\n"
            "- Stav uctu (vysoka vaha): Ucty bez upozorneni nebo omezeni jsou razeny vysе.\n\n"
            "5.2 Platba neovlivnuje organicke poradi. Nevumo neprijima platby vymenou za zlepseni poradi v organickych vysledcich vyhledavani.\n\n"
            "5.3 Nevumo muze v budoucnu nabizet placene reklamni umisteni (sponzorovaná místa). Taka umisteni budou jasne oznacena jako Sponzorovano nebo Propagovano. Zavedeni placenych reklam bude oznameno s predstihom nejméne 30 dni.\n\n"
            "5.4 Nevumo muze pravidelne menit algoritmus poradi. Podstatne zmeny parametru poradi budou Poskytovateli sdeleny prostrednictvim postupu oznameni popsaneho v clanku 10."
        ),
        "da": (
            "5.1 Nevumo viser Udbyderens profiler og Serviceopslag i sogeresultater og kategorioverskrifter. Den raekkefolge, hvori Udbydere vises (rangering), bestemmes af folgende parametre:\n\n"
            "- Profilfuldstaendighed (hoj vaegt): Profiler med fuld information, foto og verificerede kontaktoplysninger rangerer hojere.\n"
            "- Gennemsnitlig anmeldelsesscore (hoj vaegt): En hojere gennemsnitlig vurdering fra verificerede Kunder forbedrer rangeringen.\n"
            "- Svarrate og -hastighed (medium vaegt): Udbydere, der reagerer hurtigt pa Leads, faar en hojere position.\n"
            "- Aktivitetens aktualitet (medium vaegt): Nyligt aktive profiler rangerer over inaktive.\n"
            "- Geografisk overensstemmelse med tjenesten (medium vaegt): Naerhed eller overensstemmelse med Kundens by.\n"
            "- Kontostatus (hoj vaegt): Konti uden advarsler eller begraensninger rangerer hojere.\n\n"
            "5.2 Betaling pavirker ikke den organiske rangering. Nevumo accepterer ikke betalinger til gengaeld for forbedringer af rangeringen i organiske sogeresultater.\n\n"
            "5.3 Nevumo kan i fremtiden tilbyde betalte reklamepladser (sponsorerede positioner). Sadanne placeringer vil vaere tydeligt maerket som Sponsoreret eller Promoveret. Enhver indforelse af betalte kampagner vil blive annonceret med mindst 30 dages varsel.\n\n"
            "5.4 Nevumo kan med jaemlighed aendre rangeringsalgoritmen. Vaesentlige aendringer i rangeringsparametrene vil blive kommunikeret til Udbydere via underretningsproceduren beskrevet i afsnit 10."
        ),
        "sv": (
            "5.1 Nevumo visar Leverantorers profiler och Tjänstelistor i sökresultat och kategorilister. Ordningen i vilken Leverantorer visas (rankning) bestäms av följande parametrar:\n\n"
            "- Profilkomplettering (hög vikt): Profiler med fullständig information, foto och verifierade kontaktuppgifter rankas högre.\n"
            "- Genomsnittlig omdömespoäng (hög vikt): Högre genomsnittlig betyg från verifierade Kunder förbättrar rankningen.\n"
            "- Svarsfrekvens och -hastighet (medelvikt): Leverantorer som svarar snabbt på Leads får en högre position.\n"
            "- Aktivitetens aktualitet (medelvikt): Nyligen aktiva profiler rankas över inaktiva.\n"
            "- Geografisk tjänstematchning (medelvikt): Närhet eller matchning med Kundens stad.\n"
            "- Kontostatus (hög vikt): Konton utan varningar eller begränsningar rankas högre.\n\n"
            "5.2 Betalning påverkar inte den organiska rankningen. Nevumo accepterar inga betalningar i utbyte mot rankningförbättringar i organiska sökresultat.\n\n"
            "5.3 Nevumo kan i framtiden erbjuda betalda marknadsföringsplatser (sponsrade positioner). Sådana placeringar kommer tydligt märkas som Sponsrad eller Marknadsförd. Introduktionen av betalda kampanjer meddelas med minst 30 dagars varsel.\n\n"
            "5.4 Nevumo kan periodiskt ändra rankningsalgoritmen. Väsentliga ändringar av rankningsparametrarna kommuniceras till Leverantorer via det aviseringsförfarande som beskrivs i Avsnitt 10."
        ),
        "no": (
            "5.1 Nevumo viser Leverandorens profiler og Tjenestelister i sokeresultater og kategorilister. Rekkefølgen der Leverandorer vises (rangering) bestemmes av følgende parametere:\n\n"
            "- Profilkomplettering (høy vekt): Profiler med full informasjon, foto og verifiserte kontaktdetaljer rangerer høyere.\n"
            "- Gjennomsnittlig anmeldelsesscore (høy vekt): Høyere gjennomsnittlig vurdering fra verifiserte Kunder forbedrer rangeringen.\n"
            "- Svarprosent og -hastighet (medium vekt): Leverandorer som svarer raskt pa Leads faar en høyere posisjon.\n"
            "- Aktivitetens aktualitet (medium vekt): Nylig aktive profiler rangerer over inaktive.\n"
            "- Geografisk tjenestematch (medium vekt): Naerhet eller match med Kundens by.\n"
            "- Kontostatus (høy vekt): Kontoer uten advarsler eller begrensninger rangerer høyere.\n\n"
            "5.2 Betaling pavirker ikke den organiske rangeringen. Nevumo aksepterer ikke betalinger i bytte mot rangeringsforbedringer i organiske sokeresultater.\n\n"
            "5.3 Nevumo kan i fremtiden tilby betalte reklameplasseringer (sponsede posisjoner). Slike plasseringer vil tydelig merkes som Sponset eller Fremmet. Introduksjonen av betalte kampanjer vil bli annonsert med minst 30 dagers varsel.\n\n"
            "5.4 Nevumo kan jevnlig endre rangeringsalgoritmen. Vesentlige endringer i rangeringsparametrene vil bli kommunisert til Leverandorer via varslingsprosedyren beskrevet i Seksjon 10."
        ),
        "fi": (
            "5.1 Nevumo näyttää Palveluntarjoajien profiileja ja Palveluilmoituksia hakutuloksissa ja kategorioissa. Palveluntarjoajien esitysjärjestys (sijoitus) määräytyy seuraavien parametrien perusteella:\n\n"
            "- Profiilin täydellisyys (korkea paino): Täydellisillä tiedoilla, kuvalla ja varmennetuilla yhteystiedoilla olevat profiilit sijoittuvat korkeammalle.\n"
            "- Arvosanojen keskiarvo (korkea paino): Korkeampi keskiarvo verifioiduilta Asiakkailta parantaa sijoitusta.\n"
            "- Vastausprosentti ja -nopeus (keskipaino): Leadeihin nopeasti vastaavat Palveluntarjoajat saavat korkeamman sijoituksen.\n"
            "- Toiminnan viimeisin ajankohta (keskipaino): Äskettäin aktiiviset profiilit sijoittuvat inaktiivisten yläpuolelle.\n"
            "- Palvelun maantieteellinen vastaavuus (keskipaino): Läheisyys tai vastaavuus Asiakkaan kaupungin kanssa.\n"
            "- Tilin tila (korkea paino): Tilit ilman varoituksia tai rajoituksia sijoittuvat korkeammalle.\n\n"
            "5.2 Maksaminen ei vaikuta orgaaniseen sijoitukseen. Nevumo ei hyväksy maksuja sijoitusten parantamiseksi orgaanisissa hakutuloksissa.\n\n"
            "5.3 Nevumo voi tulevaisuudessa tarjota maksullisia mainospaikkoja (sponsoroituja positioita). Tällaiset sijoitukset merkitään selkeästi Sponsoroitu tai Edistetty -merkinnöillä. Maksullisten kampanjoiden käyttöönotto ilmoitetaan vähintään 30 päivän ennakkoilmoituksella.\n\n"
            "5.4 Nevumo voi muuttaa sijoitusalgoritmia säännöllisesti. Olennaisista muutoksista sijoitusparametreihin ilmoitetaan Palveluntarjoajille Kohdan 10 mukaista ilmoitusmenettelyä käyttäen."
        ),
        "et": (
            "5.1 Nevumo kuvab Teenusepakkujate profiile ja Teenusekuulutusi otsingutulemustes ja kategoorialoendites. Järjekord, milles Teenusepakkujad ilmuvad (edetabel), määratakse järgmiste parameetrite alusel:\n\n"
            "- Profiili täielikkus (kõrge kaal): Täieliku teabe, foto ja kontrollitud kontaktandmetega profiilid asuvad kõrgemal.\n"
            "- Keskmise arvustuse skoor (kõrge kaal): Kõrgem keskmise hinnang kinnitatud Klientidelt parandab edetabeli positsiooni.\n"
            "- Vastamismäär ja kiirus (keskmise kaaluga): Liididele kiiresti vastavad Teenusepakkujad saavad kõrgema positsiooni.\n"
            "- Tegevuse värskus (keskmise kaaluga): Hiljuti aktiivsed profiilid asuvad kõrgemal kui passiivsed.\n"
            "- Teenuse geograafiline vastavus (keskmise kaaluga): Lähedus või vastavus Kliendi linnaga.\n"
            "- Konto staatus (kõrge kaal): Hoiatuste ja piiranguteta kontod asuvad kõrgemal.\n\n"
            "5.2 Maksmine ei mõjuta orgaanilist edetabelit. Nevumo ei võta vastu makseid orgaaniliste otsingutulemuste edetabelipositsiooni parandamise eest.\n\n"
            "5.3 Nevumo võib tulevikus pakkuda tasulisi reklaampaigutusi (sponsoreeritud positsioonid). Sellised paigutused märgitakse selgelt kui Sponsoreeritud või Reklaamitud. Tasuliste reklaamide kasutuselevõtust teatatakse vähemalt 30 päeva ette.\n\n"
            "5.4 Nevumo võib edetabeli algoritmi perioodiliselt muuta. Edetabeli parameetrite olulisest muutustest teavitatakse Teenusepakkujaid Jaotises 10 kirjeldatud teavitamisprotseduuri kaudu."
        ),
        "lt": (
            "5.1 Nevumo rodo Teikejų profilius ir Paslaugu skelbimus paieškos rezultatuose ir kategorijų sąrašuose. Teikeju rodymo tvarka (reitingas) nustatoma pagal šiuos parametrus:\n\n"
            "- Profilio pilnumas (aukštas svoris): Profiliai su pilna informacija, nuotrauka ir patvirtintais kontaktais reitinguojami auksciau.\n"
            "- Vidutinis atsiliepimu balas (aukštas svoris): Aukštesnis vidutinis vertinimas iš patvirtintų Klientų gerina reitingą.\n"
            "- Atsakymo dažnis ir greitis (vidutinis svoris): Teikejai, greitai atsakantys į Lidus, gauna aukštesne pozicija.\n"
            "- Veiklos naujumas (vidutinis svoris): Neseniai aktyvūs profiliai reitinguojami auksciau nei neaktyvūs.\n"
            "- Paslaugos geografinis atitikimas (vidutinis svoris): Artumas arba atitikimas Kliento miestui.\n"
            "- Paskyros statusas (aukštas svoris): Paskyros be įspejimų ar apribojimų reitinguojamos auksciau.\n\n"
            "5.2 Mokejimas nedaro įtakos organiniam reitingui. Nevumo nepriima mokejimu mainais už reitingo gerinimaą organiniuose paieškos rezultatuose.\n\n"
            "5.3 Ateityje Nevumo gali pasiūlyti mokamas reklamines vietas (remiamas pozicijas). Tokios vietos bus aiškiai pazeymetos kaip Remiama arba Reklamuojama. Apie mokaму reklamu įvedima bus pranešta bent prieš 30 dienu.\n\n"
            "5.4 Nevumo gali periodiskai keisti reitingo algoritma. Apie esminius reitingo parametrų pakeitimus Teikejai bus informuoti per 10 skirsnyje nustatyta pranešimo procedūra."
        ),
        "lv": (
            "5.1 Nevumo rāda Sniedzēju profilus un Pakalpojumu sludinājumus meklēšanas rezultātos un kategoriju sarakstos. Sniedzēju parādīšanās kārtību (rangu) nosaka šādi parametri:\n\n"
            "- Profila pilnīgums (augsts svars): Profili ar pilnu informāciju, fotogrāfiju un verificētiem kontaktiem tiek ranžēti augstāk.\n"
            "- Vidējais atsauksmju vērtējums (augsts svars): Augstāks vidējais vērtējums no verificētiem Klientiem uzlabo rangu.\n"
            "- Atbildes biežums un ātrums (vidējs svars): Sniedzēji, kas ātri atbild uz Lidu pieprasījumiem, iegūst augstāku pozīciju.\n"
            "- Aktivitātes jaunums (vidējs svars): Neseni aktīvi profili tiek ranžēti augstāk nekā neaktīvie.\n"
            "- Pakalpojuma ģeogrāfiskā atbilstība (vidējs svars): Tuvums vai atbilstība Klienta pilsētai.\n"
            "- Konta statuss (augsts svars): Konti bez brīdinājumiem vai ierobežojumiem tiek ranžēti augstāk.\n\n"
            "5.2 Maksājums neietekmē organisko rangu. Nevumo nepieņem maksājumus apmaiņā pret ranga uzlabošanu organiskajos meklēšanas rezultātos.\n\n"
            "5.3 Nākotnē Nevumo var piedāvāt maksas reklāmas izvietojumus (sponsorētas pozīcijas). Šādi izvietojumi tiks skaidri apzīmēti kā Sponsorēts vai Reklamēts. Par maksas reklāmu ieviešanu tiks paziņots vismaz 30 dienas iepriekš.\n\n"
            "5.4 Nevumo var periodiski mainīt ranžēšanas algoritmu. Par būtiskām ranžēšanas parametru izmaiņām Sniedzēji tiks informēti, izmantojot 10. sadaļā aprakstīto paziņošanas procedūru."
        ),
        "hu": (
            "5.1 A Nevumo a Szolgáltatok profiljait és Szolgáltatási hirdetéseit megjeleníti a keresési eredményekben és a kategórianevzetékekben. A Szolgáltatók megjelenési sorrendjét (rangsor) a következő paraméterek határozzák meg:\n\n"
            "- Profil teljessége (magas súly): A teljes információval, fotóval és ellenőrzött elérhetőségekkel rendelkező profilok magasabban szerepelnek.\n"
            "- Átlagos értékelési pontszám (magas súly): A verifikált Ügyfelek magasabb átlagos értékelése javítja a rangsort.\n"
            "- Válaszarány és -sebesség (közepes súly): A Leadekre gyorsan reagáló Szolgáltatók magasabb pozíciót kapnak.\n"
            "- Tevékenység frissessége (közepes súly): A nemrég aktív profilok az inaktívak felett szerepelnek.\n"
            "- Szolgáltatás földrajzi egyezése (közepes súly): Közelség vagy egyezés az Ügyfél városával.\n"
            "- Fiók állapota (magas súly): Figyelmeztetés vagy korlátozás nélküli fiókok magasabban szerepelnek.\n\n"
            "5.2 A fizetés nem befolyásolja az organikus rangsort. A Nevumo nem fogad el fizetéseket organikus keresési eredményekben való rangsorjavítás ellenében.\n\n"
            "5.3 A Nevumo a jövőben fizetett promóciós elhelyezéseket kínálhat (szponzorált pozíciókat). Az ilyen elhelyezések egyértelműen Szponzorált vagy Promótált felirattal lesznek jelölve. A fizetett promóciók bevezetéséről legalább 30 nappal korábban értesítik a Szolgáltatókat.\n\n"
            "5.4 A Nevumo időről időre módosíthatja a rangsoroló algoritmust. A rangsoroló paraméterek lényeges változásait a Szolgáltatok a 10. szakaszban ismertetett értesítési eljárás útján kapják meg."
        ),
        "hr": (
            "5.1 Nevumo prikazuje profile Pruzatelja i Ponude usluga u rezultatima pretrage i kategorijskim listama. Redoslijed prikaza Pruzatelja (rangiranje) odredjuje se sljedecim parametrima:\n\n"
            "- Potpunost profila (visoka tezina): Profili s potpunim informacijama, fotografijom i verificiranim kontaktnim podacima rangiraju se vise.\n"
            "- Prosjecna ocjena recenzija (visoka tezina): Visa prosjecna ocjena od verificiranih Klijenata poboljsava rang.\n"
            "- Stopa i brzina odgovora (srednja tezina): Pruzatelji koji brzo odgovaraju na Leadove dobivaju visu poziciju.\n"
            "- Nedavna aktivnost (srednja tezina): Nedavno aktivni profili rangiraju se iznad neaktivnih.\n"
            "- Geografsko podudaranje usluge (srednja tezina): Blizina ili podudaranje s gradom Klijenta.\n"
            "- Status racuna (visoka tezina): Racuni bez upozorenja ili ogranicenja rangiraju se vise.\n\n"
            "5.2 Placanje ne utjece na organsko rangiranje. Nevumo ne prihvaca placanja u zamjenu za poboljsanje ranga u organskim rezultatima pretrage.\n\n"
            "5.3 Nevumo u buducnosti moze nuditi placene promotivne pozicije (sponzorirane pozicije). Takve pozicije bit ce jasno oznacene kao Sponzorirano ili Promovirano. Uvodenje placenih promocija najavljuje se s najmanje 30 dana unaprijed.\n\n"
            "5.4 Nevumo moze povremeno mijenjati algoritam rangiranja. O znacajnim promjenama parametara rangiranja Pruzatelji ce biti obavijesteni putem postupka obavjestivanja opisanog u Odjeljku 10."
        ),
        "sk": (
            "5.1 Nevumo zobrazuje profily Poskytovatelov a Ponuky sluzieb vo vysledkoch vyhladavania a v zoznamoch kategorii. Poradie, v akom sa Poskytovatelia zobrazuju (poradie), je urcene nasledujucimi parametrami:\n\n"
            "- Uplnost profilu (vysoka vaha): Profily s uplnymi informaciami, fotografiou a overenymi kontaktnymi udajmi sa zobrazuju vysie.\n"
            "- Priemerné hodnotenie recenzii (vysoka vaha): Vysšie priemerné hodnotenie od overených Zakaznikov zlepsuje poradie.\n"
            "- Miera a rychlost odpovede (stredna vaha): Poskytovatelia, ktori rychlo reaguju na Leady, dostávajú vysiu pozíciu.\n"
            "- Nedavna aktivita (stredna vaha): Nedavno aktivne profily sú zaradzene nad neaktívnymi.\n"
            "- Geograficka zhoda sluzby (stredna vaha): Blizkost alebo zhoda s mestom Zákaznika.\n"
            "- Stav uctu (vysoka vaha): Ucty bez upozorneni alebo obmedzeni sa zobrazuju vysie.\n\n"
            "5.2 Platba neovplyvnuje organické poradie. Nevumo neprijima platby vymenou za zlepsenie poradia v organickych vysledkoch vyhladavania.\n\n"
            "5.3 Nevumo moze v buducnosti ponukat platene reklamne umiestnenia (sponzorované pozície). Takéto umiestnenia budu jasne oznacené ako Sponzorované alebo Propagované. Zavedenie platenekh reklam bude oznámené s predstihom najmenej 30 dni.\n\n"
            "5.4 Nevumo moze pravidelne menit algoritmus poradia. Podstatné zmeny parametrov poradia budu Poskytovatelom oznamene prostredníctvom postupu oznamovania opísaného v clanku 10."
        ),
        "sl": (
            "5.1 Nevumo prikazuje profile Ponudnikov in Oglase storitev v rezultatih iskanja in kategorialnih seznamih. Vrstni red, v katerem se Ponudniki prikažejo (razvrstitev), določajo naslednji parametri:\n\n"
            "- Popolnost profila (visoka utež): Profili s popolnimi informacijami, fotografijo in preverenimi kontaktnimi podatki so uvrščeni višje.\n"
            "- Povprečna ocena recenzij (visoka utež): Višja povprečna ocena od preverjenih Strank izboljša uvrstitev.\n"
            "- Stopnja in hitrost odziva (srednja utež): Ponudniki, ki se hitro odzivajo na Leade, dobijo višjo pozicijo.\n"
            "- Nedavna aktivnost (srednja utež): Nedavno aktivni profili so uvrščeni nad neaktivnimi.\n"
            "- Geografska ujemanje storitve (srednja utež): Bližina ali ujemanje z mestom Stranke.\n"
            "- Status računa (visoka utež): Računi brez opozoril ali omejitev so uvrščeni višje.\n\n"
            "5.2 Plačilo ne vpliva na organsko uvrstitev. Nevumo ne sprejema plačil v zameno za izboljšanje uvrstitve v organskih rezultatih iskanja.\n\n"
            "5.3 Nevumo lahko v prihodnosti ponudi plačana promocijska mesta (sponzorirane pozicije). Taka mesta bodo jasno označena kot Sponzorirano ali Promovirano. Uvedba plačanih promocij bo najavljena z vsaj 30-dnevnim opozorilom.\n\n"
            "5.4 Nevumo lahko občasno spreminja algoritem uvrstitve. Bistvene spremembe parametrov uvrstitve bodo Ponudnikom sporočene prek postopka obvestila, opisanega v 10. razdelku."
        ),
        "el": (
            "5.1 I Nevumo emphanizei profil Paróchon kai Katalogous Ypiresbion sta apotelesmata anazetisis kai stous katalogous kategorion. I seira emfanisis ton Paróchon (taxinomisi) kathorizetai apo tous akólouthous parametrous:\n\n"
            "- Plirótita profil (ypsiló vàros): Ta profil me plires pliroforiei, foto kai verifes epikoinonies katatasson psylotera.\n"
            "- Meso skoros axiologiseon (ypsilò vàros): Ypsilótero meso skoros apo verifikous Pelates beltionei tin taxinomisi.\n"
            "- Pososto kai tachytita apantisis (mésio vàros): Oi Párochoi pou apantoun ámesa sta Lids lambánoun ypsilóteri thési.\n"
            "- Prosfahtita drastiriotitas (mésio vàros): Ta prosfata enérgima profil taxinomoúntai panō apo ta anengina.\n"
            "- Geografiki antistichisi ypiresias (mésio vàros): Eggytita i antistichisi me tin poli tou Pelati.\n"
            "- Katastasi logariasmou (ypsilò vàros): Oi logariasmoi choris preidopoiiseis i periorismous taxinomoúntai psylotera.\n\n"
            "5.2 I pliromi den epitrepei tin organiki taxinomisi. I Nevumo den dektetai pliromes se antallagi me betiomenis taxinomisis sta organika apotelesmata anazetisis.\n\n"
            "5.3 I Nevumo mporei sto mellon na prosthetei pliromes diafimistikes theseis (sponsorisménes theseis). Tetoia thesi tha simainontai ksekathara os Sponsorismeno i Promovárismeno. I eisagogi pliromes proothiseis tha agelletai me toulachiton 30 imeron proeídopisi.\n\n"
            "5.4 I Nevumo mporei periodika na tropopoii ton algorithmo taxinomisis. Ousiastikes allagés stous parametrous taxinomisis tha anakoinonontai stous Párochous meso tis diadikasias eidopoiisis pou perigrafetai sto Arthro 10."
        ),
        "tr": (
            "5.1 Nevumo, Saglayici profillerini ve Hizmet Listelerini arama sonuçlarında ve kategori listelerinde gösterir. Saglayicilarin görünme sırası (sıralama) asagıdaki parametrelerle belirlenir:\n\n"
            "- Profil tamamlanma oranı (yüksek agırlık): Tam bilgi, fotoğraf ve doğrulanmış iletisim bilgilerine sahip profiller daha üst sıralarda yer alır.\n"
            "- Ortalama inceleme puanı (yüksek agırlık): Doğrulanmış Müsterilerden alınan daha yüksek ortalama puan sıralamayı iyilestirir.\n"
            "- Yanıt oranı ve hızı (orta agırlık): Leadlere hızlıca yanıt veren Saglayicilar daha yüksek bir konum alır.\n"
            "- Aktivite güncelliği (orta agırlık): Son zamanlarda aktif olan profiller inaktiflerden üstte yer alır.\n"
            "- Hizmetin cografi eslesmesi (orta agırlık): Müsterinin sehrine yakınlık veya uyum.\n"
            "- Hesap durumu (yüksek agırlık): Uyarı veya kısıtlama olmayan hesaplar daha üst sıralarda yer alır.\n\n"
            "5.2 Ödeme organik sıralamayı etkilemez. Nevumo, organik arama sonuçlarında sıralama iyilestirmeleri karşılığında ödeme kabul etmez.\n\n"
            "5.3 Nevumo gelecekte ücretli tanıtım yerlesimi (sponsorlu konumlar) sunabilir. Bu tür yerlesimler açıkça Sponsorlu veya Tanıtılan olarak etiketlenecektir. Ücretli tanıtımların tanıtımı en az 30 gün önceden duyurulacaktır.\n\n"
            "5.4 Nevumo sıralama algoritmasını periyodik olarak değistirebilir. Sıralama parametrelerindeki önemli değisiklikler, Bölüm 10'da belirtilen bildirim prosedürü aracılığıyla Saglayicilara iletilecektir."
        ),
        "ga": (
            "5.1 Taispeánann Nevumo próifílí Solathroir agus Liostaí Seirbhíse i dtorthaí cuardaigh agus i liostálacha catagóire. Cinntear an t-ord ina bhfeictear Solathroir (rangú) ag na paraiméadair seo a leanas:\n\n"
            "- Iomláine próifíl (meáchan ard): Próifílí le faisnéis iomlán, grianghraf agus sonraí teagmhála fíoraithe rangaítear níos airde.\n"
            "- Meánscór léirmheasa (meáchan ard): Meánrátáil níos airde ó Chustoimeri fíoraithe feabhsaíonn an rangú.\n"
            "- Ráta agus luas freagra (meáchan meánach): Solathroir a fhreagra go pras ar Leannta faigheann siad seasamh níos airde.\n"
            "- Déanaí na gníomhaíochta (meáchan meánach): Próifílí a bhí gníomhach le déanaí rangaítear os cionn cinn neamhghníomhacha.\n"
            "- Meaitseáil gheografach an tseirbhís (meáchan meánach): Gar don gcathair nó comhoiriúnach le cathair an Chustoimeara.\n"
            "- Stádas cuntais (meáchan ard): Cuntais gan rabhaidh ná srianta rangaítear níos airde.\n\n"
            "5.2 Ní théann íocaíocht i bhfeidhm ar an rangú orgánach. Ní ghlacann Nevumo le híocaíochtaí mar mhalairt ar fheabhsuithe rangaithe i dtorthaí cuardaigh orgánacha.\n\n"
            "5.3 Féadfaidh Nevumo socrúcháin tráchtála iochtartha (suíomhanna urraithe) a thairiscint sa todhchaí. Beidh socrúcháin den sórt sin lipéadaithe go soiléir mar Urraithe nó Curtha Chun Cinn. Fógrófar aon réamhrá ar fheachtas íochta ar a laghad 30 lá roimh ré.\n\n"
            "5.4 Féadfaidh Nevumo an t-algartam rangaithe a mhodhnú go tréimhsiúil. Cuirfear in iúl d'athruithe ábhartha ar pharaiméadair rangaithe do Sholathroir tríd an nós imeachta fógartha a leagtar amach in Alt 10."
        ),
        "is": (
            "5.1 Nevumo sýnir notandasnið Veituaðila og Þjónustufærslur í leitarniðurstöðum og flokkalistum. Röðin sem Veituaðilar birtast í (röðun) er ákvörðuð af eftirfarandi breytum:\n\n"
            "- Fullnæging notandasniðs (mikið vægi): Snið með fullnægjandi upplýsingum, mynd og staðfestar tengiliðaupplýsingar eru raðað hærra.\n"
            "- Meðaleinkunnir umsagna (mikið vægi): Hærri meðaleinkunn frá staðfestum Viðskiptavinum bætir röðun.\n"
            "- Svarhlutfall og -hraði (meðalvægi): Veituaðilar sem svara Leiðum fljótt fá hærri stöðu.\n"
            "- Nýleg virkni (meðalvægi): Nýlega virk snið eru raðað yfir óvirk.\n"
            "- Landfræðilegar þjónustusamsvörun (meðalvægi): Nálægð eða samsvörun við borg Viðskiptavinar.\n"
            "- Reikningstaða (mikið vægi): Reikningar án viðvarana eða takmarkana eru raðað hærra.\n\n"
            "5.2 Greiðsla hefur ekki áhrif á lífrænna röðun. Nevumo tekur ekki við greiðslum í skiptum fyrir bætta röðun í lífrænum leitarniðurstöðum.\n\n"
            "5.3 Nevumo kann í framtíðinni að bjóða upp á greiddar kynningarstaðsetningar (styrktarstaðar). Slíkar staðsetningar verða skýrt merktar sem Styrkt eða Kynnt. Tilkynnt verður um innleiðingu greiddar kynningar með minnst 30 daga fyrirvara.\n\n"
            "5.4 Nevumo getur reglulega breytt röðunarreikniritinu. Verulegur breytingar á röðunarbreytum verða tilkynntar Veituaðilum í gegnum tilkynningaferli sem lýst er í kafla 10."
        ),
        "lb": (
            "5.1 Nevumo weist Presser-Profiler a Serviceannoncen a Sichresultater a Kategorielisten un. D'Uerdnung, wéi Presser sech weisen (Ranking), gëtt vun den folgenden Parameteren bestëmmt:\n\n"
            "- Vollstännegkeet vum Profil (hohes Gewiicht): Profiler mat volle Informatiounen, Foto a verifizierten Kontaktdaten ranken méi héich.\n"
            "- Duerchschnëttlech Bewäertungsscor (hohes Gewiicht): Eng méi héich Duerchschnëttsbewerung vun verifizéierte Clienten verbessert d'Ranking.\n"
            "- Äntwertrate a -geschwindegkeet (mëttlert Gewiicht): Presser déi séier op Leads äntwerten kréien eng méi héich Positioun.\n"
            "- Aktualitéit vun der Aktivitéit (mëttlert Gewiicht): Rezent aktiv Profiler ranken iwwer inaktiver.\n"
            "- Geografesch Correspondenz vum Service (mëttlert Gewiicht): Nähert oder Correspondenz mat der Stad vum Client.\n"
            "- Kontostatus (hohes Gewiicht): Konten ouni Warnungen oder Aschränkungen ranken méi héich.\n\n"
            "5.2 Bezuelung beaflosst d'organesch Ranking net. Nevumo akzeptéiert keng Bezuelungen als Austausch fir Ranking-Verbesserungen a organeschen Sichresultater.\n\n"
            "5.3 Nevumo kann an der Zukunft bezuelte Werbeplatzéierungen (sponsoriséiert Positiounen) ubidden. Solch Platzéierungen ginn klar als Sponsoriséiert oder Promovéiert markéiert. All Aféierung vu bezuelete Kampagnen gëtt mat mindestens 30 Deeg Virankëndigung annoncéiert.\n\n"
            "5.4 Nevumo kann de Ranking-Algorithmus periodesch änneren. Wesentlech Ännerungen vun de Ranking-Parameteren ginn de Presseren iwwert de Meldeprozedure an Abschnitt 10 matgedeelt."
        ),
        "mk": (
            "5.1 Nevumo gi prikazuva profilite na Davacite i Oglasit za uslugi vo rezultatite od prebaruvanjeto i vo kategoriski listinzi. Redot na prikazuvanje na Davacite (rangiranje) se odreduva spored slednite parametri:\n\n"
            "- Celosnost na profilot (visoka tezina): Profilite so polna informacija, fotografija i verifikuvani kontakti se rankuvaat povisoko.\n"
            "- Prosecen skor na recenzii (visoka tezina): Povisok prosecen ocenok od verifikuvani Klienti go podobruva rangiranjeto.\n"
            "- Stапка i brzina na odgovor (sredna tezina): Davacite koi brzo odgovaraat na Lidovite dobivaat povisoka pozicija.\n"
            "- Skoreshna aktivnost (sredna tezina): Nedavno aktivnite profili se rankuvaat nad neaktivnite.\n"
            "- Geografska sogласnost na uslugata (sredna tezina): Blizina ili sogласnost so gradot na Klientot.\n"
            "- Status na smetkata (visoka tezina): Smetkite bez predupreda ili ogranichuvanja se rankuvaat povisoko.\n\n"
            "5.2 Plakanjeто ne vlijae na organskoto rangiranje. Nevumo ne prima plakanja vo zamena za podobruvanje na rangot vo organskite rezultati od prebaruvanjeto.\n\n"
            "5.3 Nevumo vo idnina mozhe da nudi plateni promociski pozicii (sponsorirani pozicii). Takvi pozicii jasno ke bidat oznacheni kako Sponsorirano ili Promovano. Voveduvanjeto na plateni promocii ke se najavi so najmalku 30 dena odnapred.\n\n"
            "5.4 Nevumo mozhe periodichno da go menuva algoritmot za rangiranje. Za sustinski promeni vo parametrite za rangiranje, Davacite ke bidat informirani preku postapkata za notifikacija sodrzhana vo Oddelok 10."
        ),
        "mt": (
            "5.1 Nevumo turi profili tal-Fornituri u Listati ta' Servizzi fir-riżultati tat-tfittxija u l-listati tal-kategoriji. L-ordni li fiha jidher il-Fornituri (klassifikazzjoni) tiġi determinata mill-parametri li ġejjin:\n\n"
            "- Kompletezza tal-profil (piż għoli): Profili b'informazzjoniта sħiħa, ritratt u dettalji ta' kuntatt verifikati jiġu kklassifikati ogħla.\n"
            "- Punteġġ medju tar-reviews (piż għoli): Rata medja ogħla minn Klijenti verifikati jtejjeb il-klassifikazzjoni.\n"
            "- Rata u veloċità ta' risposta (piż medju): Fornituri li jirrispondu malajr ghal Leads jirċievu pożizzjoni ogħla.\n"
            "- Recency tal-attività (piż medju): Profili li kienu attivi reċentement jiġu kklassifikati fuq dawk inattivi.\n"
            "- Tqabbil ġeografiku tas-servizz (piż medju): Qrubija jew tqabbil mal-belt tal-Klijent.\n"
            "- Status tal-kont (piż għoli): Kontijiet mingħajr twissijiet jew restrizzjonijiet jiġu kklassifikati ogħla.\n\n"
            "5.2 Il-ħlas ma jaffettwax il-klassifikazzjoni organika. Nevumo ma taċċettax ħlasijiet bi skambju ghal titjib fil-klassifikazzjonî fir-riżultati organiċi tat-tfittxija.\n\n"
            "5.3 Nevumo tista' fil-futur toffri postijiet promozzjonali mħallsa (pożizzjonijiet sponsorjati). Tali postijiet jiġu etikettati b'mod ċar bħala Sponsorjat jew Imħeġġeġ. Kwalunkwe introduzzjoni ta' promozzjonijiet mħallsa tiġi mħabbra b'avviż ta' mhux anqas minn 30 jum.\n\n"
            "5.4 Nevumo tista' timmodifika l-algoritmu tal-klassifikazzjonî perjodikament. Tibdiliet materjali fil-parametri tal-klassifikazzjonî jiġu kkomunikati lill-Fornituri permezz tal-proċedura ta' avviż imniżżla fit-Taqsima 10."
        ),
        "sq": (
            "5.1 Nevumo shfaq profilet e Ofruesve dhe Listezimet e Sherbimeve ne rezultatet e kerkimit dhe ne listat e kategorive. Radha ne te cilen shfaqen Ofruesit (renditja) percaktohet nga parametrat e meposhtme:\n\n"
            "- Ploteesia e profilit (peshe e larte): Profilet me informacion te plote, foto dhe detaje kontakti te verifikuara renditen me lart.\n"
            "- Rezultati mesatar i komenteve (peshe e larte): Nje vleresim mesatar me i larte nga Klientet e verifikuar permieson renditjen.\n"
            "- Shkalla dhe shpejtesia e pergjigjes (peshe mesatare): Ofruesit qe u pergjigjen shpejt Leadeve marrin nje pozicion me te larte.\n"
            "- Recentsia e aktivitetit (peshe mesatare): Profilet e aktivizuara se fundi renditen mbi ato joaktive.\n"
            "- Perputhjashmeria gjeografike e sherbimit (peshe mesatare): Afria ose perputhjashmeria me qytetin e Klientit.\n"
            "- Statusi i llogarise (peshe e larte): Llogarite pa paralajmerime ose kufizime renditen me lart.\n\n"
            "5.2 Pagesa nuk ndikon ne renditjen organike. Nevumo nuk pranon pagesat ne kembim te permisimeve te renditjes ne rezultatet organike te kerkimit.\n\n"
            "5.3 Nevumo mund te ofrojne ne te ardhmen vendosje reklamuese te paguar (pozicione te sponsorizuara). Vendosje te tilla do te jene te etiketuara qarte si E sponsorizuar ose E promovuar. Cdo futje e promovimeve te paguara do te njoftohet me se pakten 30 dite paralajmerim.\n\n"
            "5.4 Nevumo mund te modifikoje periodikisht algoritmin e renditjes. Ndryshimet materiale ne parametrat e renditjes do t'u komunikohen Ofruesve nepermjet procedures se njoftimit te percaktuar ne Seksionin 10."
        ),
        "sr": (
            "5.1 Nevumo prikazuje profile Pruzaoca i Oglase usluga u rezultatima pretrage i kategorijskim listama. Redosled prikazivanja Pruzaoca (rangiranje) odredjuje se sledecim parametrima:\n\n"
            "- Potpunost profila (visoka tezina): Profili sa potpunim informacijama, fotografijom i verifikovanim kontaktnim podacima rangiraju se vise.\n"
            "- Prosecna ocena recenzija (visoka tezina): Visa prosecna ocena od verifikovanih Klijenata poboljsava rang.\n"
            "- Stopa i brzina odgovora (srednja tezina): Pruzaoci koji brzo odgovaraju na Lidove dobijaju visu poziciju.\n"
            "- Nedavna aktivnost (srednja tezina): Nedavno aktivni profili rangiraju se iznad neaktivnih.\n"
            "- Geografsko podudaranje usluge (srednja tezina): Blizina ili podudaranje sa gradom Klijenta.\n"
            "- Status naloga (visoka tezina): Nalozi bez upozorenja ili ogranicenja rangiraju se vise.\n\n"
            "5.2 Placanje ne utice na organsko rangiranje. Nevumo ne prihvata placanja u zamenu za poboljsanje ranga u organskim rezultatima pretrage.\n\n"
            "5.3 Nevumo u buducnosti moze nuditi placene promotivne pozicije (sponzorisane pozicije). Takve pozicije bice jasno oznacene kao Sponzorisano ili Promovisano. Uvodjenje placenih promocija najavljuje se sa najmanje 30 dana unapred.\n\n"
            "5.4 Nevumo moze povremeno menjati algoritam rangiranja. O znacajnim promenama parametara rangiranja Pruzaoci ce biti obavesteni putem postupka obavestavanja opisanog u Odeljku 10."
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
        print(
            f"✅ seed_provider_terms_p12_art5_body: {count} rows upserted "
            f"({NAMESPACE}: art5_body x 34 langs)"
        )

    engine.dispose()


if __name__ == "__main__":
    seed()
