# -*- coding: utf-8 -*-
"""
Seed script for City Page translations (city namespace).
Covers all 34 supported languages with native translations.
Run: docker exec nevumo-api python -m apps.api.scripts.seed_city_translations

SAFETY NOTES:
- Idempotent: ON CONFLICT ... DO UPDATE SET value = EXCLUDED.value
- No DELETE / TRUNCATE statements
- Parameterized queries only (no SQL injection risk)
- Wrapped in a single transaction with rollback on error
"""
from sqlalchemy import text
from apps.api.database import SessionLocal

LANGUAGES = [
    'en', 'bg', 'pl', 'de', 'fr', 'es', 'it', 'nl', 'pt', 'pt-PT',
    'ro', 'cs', 'sk', 'hu', 'hr', 'sl', 'sr', 'mk', 'sq', 'el',
    'tr', 'ru', 'uk', 'lv', 'lt', 'et', 'fi', 'sv', 'da', 'no',
    'is', 'lb', 'ga', 'mt'
]

# ---------------------------------------------------------------------------
# English (default / fallback)
# ---------------------------------------------------------------------------
EN_DATA = {
    "city.nav_link": "Become a specialist",
    "city.hero_title": "Find services in {city}",
    "city.search_placeholder": "What service do you need?",
    "city.search_btn": "Search",
    "city.cta_request": "Get offers",
    "city.categories_title": "Popular services in {city}",
    "city.cat_cleaning_leads": "Available now",
    "city.cat_plumbing_leads": "Available now",
    "city.cat_massage_leads": "Available now",
    "city.cat_cta": "View providers",
    "city.empty_title": "Can't find the right service?",
    "city.empty_subtitle": "Describe your request and we will connect you with the right specialists.",
    "city.empty_cta": "Request any service",
    "city.how_title": "How it works",
    "city.how_step_1": "Describe your request",
    "city.how_step_1_sub": "Takes 2 minutes",
    "city.how_step_2": "Get offers from specialists",
    "city.how_step_2_sub": "Usually within 30 minutes",
    "city.how_step_3": "Choose and connect directly",
    "city.how_step_3_sub": "No commission, no middlemen",
    "city.seo_title": "Services in {city}",
    "city.seo_description": "Looking for reliable services in {city}? Nevumo connects you with verified local specialists. From home cleaning to plumbing repairs and professional massage therapy, find the right provider for your needs.",
    "city.seo_p2": "All specialists on our platform are reviewed by real customers. Send a free request, compare offers, and choose the best match for your project. No hidden fees, no obligations.",
    "city.seo_p3": "Whether you need a one-time service or ongoing support, our network of professionals in {city} is ready to help. Get started with a simple request and receive responses within hours.",
    "city.footer_title": "Nevumo — Connecting you with local specialists",
    "city.footer_in": "in"
}

# ---------------------------------------------------------------------------
# Bulgarian
# ---------------------------------------------------------------------------
BG_DATA = {
    "city.nav_link": "Стани специалист",
    "city.hero_title": "Намери услуги в {city}",
    "city.search_placeholder": "Каква услуга търсиш?",
    "city.search_btn": "Търси",
    "city.cta_request": "Получи оферти",
    "city.categories_title": "Популярни услуги в {city}",
    "city.cat_cleaning_leads": "Достъпно сега",
    "city.cat_plumbing_leads": "Достъпно сега",
    "city.cat_massage_leads": "Достъпно сега",
    "city.cat_cta": "Виж изпълнители",
    "city.empty_title": "Не намираш точната услуга?",
    "city.empty_subtitle": "Опиши какво търсиш и ние ще те свържем с правилните специалисти.",
    "city.empty_cta": "Изпрати заявка — ще те свържем с изпълнител",
    "city.how_title": "Как работи",
    "city.how_step_1": "Опиши какво търсиш",
    "city.how_step_1_sub": "Отнема 2 минути",
    "city.how_step_2": "Получи оферти от специалисти",
    "city.how_step_2_sub": "Обикновено до 30 минути",
    "city.how_step_3": "Избери и се свържи директно",
    "city.how_step_3_sub": "Без комисионна, без посредници",
    "city.seo_title": "Услуги в {city}",
    "city.seo_description": "Намери надеждни специалисти в {city}. Nevumo те свързва с проверени местни специалисти. От почистване до ремонт на водопровод и професионални масажи, намери правилния изпълнител.",
    "city.seo_p2": "Всички специалисти в нашата платформа са оценени от реални клиенти. Изпрати безплатна заявка, сравни оферти и избери най-добрия за твоя проект. Без скрити такси и ангажименти.",
    "city.seo_p3": "Независимо дали имаш нужда от еднократна услуга или дългосрочна подкрепа, нашата мрежа от професионалисти в {city} е готова да помогне. Започни с лесна заявка и получи отговори до часове.",
    "city.footer_title": "Nevumo — Свързваме те с местни специалисти",
    "city.footer_in": "в"
}

# ---------------------------------------------------------------------------
# Polish
# ---------------------------------------------------------------------------
PL_DATA = {
    "city.nav_link": "Zostań specjalistą",
    "city.hero_title": "Znajdź usługi w {city}",
    "city.search_placeholder": "Jakiej usługi potrzebujesz?",
    "city.search_btn": "Szukaj",
    "city.cta_request": "Otrzymaj oferty",
    "city.categories_title": "Popularne usługi w {city}",
    "city.cat_cleaning_leads": "Dostępne teraz",
    "city.cat_plumbing_leads": "Dostępne teraz",
    "city.cat_massage_leads": "Dostępne teraz",
    "city.cat_cta": "Zobacz wykonawców",
    "city.empty_title": "Nie możesz znaleźć odpowiedniej usługi?",
    "city.empty_subtitle": "Opisz swoje zapytanie, a my skontaktujemy Cię z odpowiednimi specjalistami.",
    "city.empty_cta": "Wyślij zapytanie — znajdziemy wykonawcę dla Ciebie",
    "city.how_title": "Jak to działa",
    "city.how_step_1": "Opisz czego potrzebujesz",
    "city.how_step_1_sub": "Zajmuje 2 minuty",
    "city.how_step_2": "Otrzymaj oferty od specjalistów",
    "city.how_step_2_sub": "Zazwyczaj w ciągu 30 minut",
    "city.how_step_3": "Wybierz i połącz się bezpośrednio",
    "city.how_step_3_sub": "Bez prowizji, bez pośredników",
    "city.seo_title": "Usługi w {city}",
    "city.seo_description": "Znajdź sprawdzonych specjalistów w {city}. Nevumo łączy Cię ze zweryfikowanymi lokalnymi fachowcami. Od sprzątania po hydraulikę i masaże, znajdź odpowiedniego wykonawcę.",
    "city.seo_p2": "Wszyscy specjaliści na naszej platformie są oceniani przez prawdziwych klientów. Wyślij bezpłatne zapytanie, porównaj oferty i wybierz najlepszą dla swojego projektu. Bez ukrytych opłat i zobowiązań.",
    "city.seo_p3": "Niezależnie od tego, czy potrzebujesz jednorazowej usługi, czy stałego wsparcia, nasza sieć profesjonalistów w {city} jest gotowa do pomocy. Zacznij od prostego zapytania i otrzymaj odpowiedzi w ciągu kilku godzin.",
    "city.footer_title": "Nevumo — Łączymy Cię z lokalnymi specjalistami",
    "city.footer_in": "w"
}

# ---------------------------------------------------------------------------
# German
# ---------------------------------------------------------------------------
DE_DATA = {
    "city.nav_link": "Spezialist werden",
    "city.hero_title": "Dienstleistungen in {city} finden",
    "city.search_placeholder": "Welche Dienstleistung suchen Sie?",
    "city.search_btn": "Suchen",
    "city.cta_request": "Angebote erhalten",
    "city.categories_title": "Beliebte Dienstleistungen in {city}",
    "city.cat_cleaning_leads": "Jetzt verfügbar",
    "city.cat_plumbing_leads": "Jetzt verfügbar",
    "city.cat_massage_leads": "Jetzt verfügbar",
    "city.cat_cta": "Anbieter anzeigen",
    "city.empty_title": "Den richtigen Service nicht gefunden?",
    "city.empty_subtitle": "Beschreiben Sie Ihren Bedarf und wir verbinden Sie mit den richtigen Spezialisten.",
    "city.empty_cta": "Beliebige Dienstleistung anfragen",
    "city.how_title": "So funktioniert es",
    "city.how_step_1": "Beschreiben Sie Ihren Bedarf",
    "city.how_step_1_sub": "Dauert 2 Minuten",
    "city.how_step_2": "Angebote von Spezialisten erhalten",
    "city.how_step_2_sub": "Meistens innerhalb von 30 Minuten",
    "city.how_step_3": "Direkt wählen und verbinden",
    "city.how_step_3_sub": "Keine Provision, keine Zwischenhändler",
    "city.seo_title": "Dienstleistungen in {city}",
    "city.seo_description": "Suchen Sie zuverlässige Dienstleistungen in {city}? Nevumo verbindet Sie mit verifizierten lokalen Spezialisten. Von Hausreinigung über Klempnerarbeiten bis zu professionellen Massagen.",
    "city.seo_p2": "Alle Spezialisten auf unserer Plattform werden von echten Kunden bewertet. Senden Sie eine kostenlose Anfrage, vergleichen Sie Angebote und wählen Sie das Beste für Ihr Projekt. Keine versteckten Gebühren.",
    "city.seo_p3": "Ob Sie eine einmalige Dienstleistung oder laufende Unterstützung benötigen — unser Netzwerk von Fachleuten in {city} steht bereit. Starten Sie mit einer einfachen Anfrage.",
    "city.footer_title": "Nevumo — Wir verbinden Sie mit lokalen Spezialisten",
    "city.footer_in": "in"
}

# ---------------------------------------------------------------------------
# French
# ---------------------------------------------------------------------------
FR_DATA = {
    "city.nav_link": "Devenir specialiste",
    "city.hero_title": "Trouver des services a {city}",
    "city.search_placeholder": "Quel service recherchez-vous ?",
    "city.search_btn": "Rechercher",
    "city.cta_request": "Recevoir des offres",
    "city.categories_title": "Services populaires a {city}",
    "city.cat_cleaning_leads": "Disponible maintenant",
    "city.cat_plumbing_leads": "Disponible maintenant",
    "city.cat_massage_leads": "Disponible maintenant",
    "city.cat_cta": "Voir les prestataires",
    "city.empty_title": "Vous ne trouvez pas le bon service ?",
    "city.empty_subtitle": "Decrivez votre demande et nous vous mettrons en contact avec les bons specialistes.",
    "city.empty_cta": "Demander n'importe quel service",
    "city.how_title": "Comment ca fonctionne",
    "city.how_step_1": "Decrivez votre besoin",
    "city.how_step_1_sub": "Prend 2 minutes",
    "city.how_step_2": "Recevez des offres de specialistes",
    "city.how_step_2_sub": "Generalement en 30 minutes",
    "city.how_step_3": "Choisissez et connectez-vous directement",
    "city.how_step_3_sub": "Sans commission, sans intermediaires",
    "city.seo_title": "Services a {city}",
    "city.seo_description": "Vous cherchez des services fiables a {city} ? Nevumo vous connecte avec des specialistes locaux verifies. Du nettoyage a la plomberie et aux massages professionnels.",
    "city.seo_p2": "Tous les specialistes de notre plateforme sont evalues par de vrais clients. Envoyez une demande gratuite, comparez les offres et choisissez la meilleure pour votre projet. Sans frais caches.",
    "city.seo_p3": "Que vous ayez besoin d'un service ponctuel ou d'un soutien continu, notre reseau de professionnels a {city} est pret a aider. Commencez avec une simple demande.",
    "city.footer_title": "Nevumo — Nous vous connectons avec des specialistes locaux",
    "city.footer_in": "a"
}

# ---------------------------------------------------------------------------
# Spanish
# ---------------------------------------------------------------------------
ES_DATA = {
    "city.nav_link": "Conviertete en especialista",
    "city.hero_title": "Encuentra servicios en {city}",
    "city.search_placeholder": "¿Que servicio necesitas?",
    "city.search_btn": "Buscar",
    "city.cta_request": "Recibir ofertas",
    "city.categories_title": "Servicios populares en {city}",
    "city.cat_cleaning_leads": "Disponible ahora",
    "city.cat_plumbing_leads": "Disponible ahora",
    "city.cat_massage_leads": "Disponible ahora",
    "city.cat_cta": "Ver proveedores",
    "city.empty_title": "¿No encuentras el servicio adecuado?",
    "city.empty_subtitle": "Describe tu solicitud y te conectaremos con los especialistas adecuados.",
    "city.empty_cta": "Solicitar cualquier servicio",
    "city.how_title": "Como funciona",
    "city.how_step_1": "Describe tu solicitud",
    "city.how_step_1_sub": "Tarda 2 minutos",
    "city.how_step_2": "Recibe ofertas de especialistas",
    "city.how_step_2_sub": "Normalmente en 30 minutos",
    "city.how_step_3": "Elige y conectate directamente",
    "city.how_step_3_sub": "Sin comision, sin intermediarios",
    "city.seo_title": "Servicios en {city}",
    "city.seo_description": "¿Buscas servicios confiables en {city}? Nevumo te conecta con especialistas locales verificados. Desde limpieza hasta fontaneria y masajes profesionales.",
    "city.seo_p2": "Todos los especialistas en nuestra plataforma son evaluados por clientes reales. Envia una solicitud gratuita, compara ofertas y elige la mejor para tu proyecto. Sin tarifas ocultas.",
    "city.seo_p3": "Ya sea que necesites un servicio puntual o apoyo continuo, nuestra red de profesionales en {city} esta lista para ayudar.",
    "city.footer_title": "Nevumo — Te conectamos con especialistas locales",
    "city.footer_in": "en"
}

# ---------------------------------------------------------------------------
# Italian
# ---------------------------------------------------------------------------
IT_DATA = {
    "city.nav_link": "Diventa uno specialista",
    "city.hero_title": "Trova servizi a {city}",
    "city.search_placeholder": "Di quale servizio hai bisogno?",
    "city.search_btn": "Cerca",
    "city.cta_request": "Ricevi offerte",
    "city.categories_title": "Servizi popolari a {city}",
    "city.cat_cleaning_leads": "Disponibile ora",
    "city.cat_plumbing_leads": "Disponibile ora",
    "city.cat_massage_leads": "Disponibile ora",
    "city.cat_cta": "Vedi i fornitori",
    "city.empty_title": "Non riesci a trovare il servizio giusto?",
    "city.empty_subtitle": "Descrivi la tua richiesta e ti metteremo in contatto con gli specialisti giusti.",
    "city.empty_cta": "Richiedi qualsiasi servizio",
    "city.how_title": "Come funziona",
    "city.how_step_1": "Descrivi la tua richiesta",
    "city.how_step_1_sub": "Richiede 2 minuti",
    "city.how_step_2": "Ricevi offerte dagli specialisti",
    "city.how_step_2_sub": "Di solito entro 30 minuti",
    "city.how_step_3": "Scegli e connettiti direttamente",
    "city.how_step_3_sub": "Nessuna commissione, nessun intermediario",
    "city.seo_title": "Servizi a {city}",
    "city.seo_description": "Cerchi servizi affidabili a {city}? Nevumo ti connette con specialisti locali verificati. Dalla pulizia all'idraulica e ai massaggi professionali.",
    "city.seo_p2": "Tutti gli specialisti sulla nostra piattaforma sono valutati da clienti reali. Invia una richiesta gratuita, confronta le offerte e scegli la migliore per il tuo progetto. Nessun costo nascosto.",
    "city.seo_p3": "Che tu abbia bisogno di un servizio una tantum o di supporto continuativo, la nostra rete di professionisti a {city} e pronta ad aiutarti.",
    "city.footer_title": "Nevumo — Ti colleghiamo con specialisti locali",
    "city.footer_in": "a"
}

# ---------------------------------------------------------------------------
# Dutch
# ---------------------------------------------------------------------------
NL_DATA = {
    "city.nav_link": "Word specialist",
    "city.hero_title": "Vind diensten in {city}",
    "city.search_placeholder": "Welke dienst heeft u nodig?",
    "city.search_btn": "Zoeken",
    "city.cta_request": "Ontvang offertes",
    "city.categories_title": "Populaire diensten in {city}",
    "city.cat_cleaning_leads": "Nu beschikbaar",
    "city.cat_plumbing_leads": "Nu beschikbaar",
    "city.cat_massage_leads": "Nu beschikbaar",
    "city.cat_cta": "Bekijk aanbieders",
    "city.empty_title": "Kunt u de juiste dienst niet vinden?",
    "city.empty_subtitle": "Beschrijf uw verzoek en wij verbinden u met de juiste specialisten.",
    "city.empty_cta": "Vraag een dienst aan",
    "city.how_title": "Hoe het werkt",
    "city.how_step_1": "Beschrijf uw verzoek",
    "city.how_step_1_sub": "Duurt 2 minuten",
    "city.how_step_2": "Ontvang offertes van specialisten",
    "city.how_step_2_sub": "Gewoonlijk binnen 30 minuten",
    "city.how_step_3": "Kies en verbind direct",
    "city.how_step_3_sub": "Geen provisie, geen tussenpersonen",
    "city.seo_title": "Diensten in {city}",
    "city.seo_description": "Zoekt u betrouwbare diensten in {city}? Nevumo verbindt u met geverifieerde lokale specialisten. Van schoonmaak tot loodgieterij en professionele massages.",
    "city.seo_p2": "Alle specialisten op ons platform worden beoordeeld door echte klanten. Stuur een gratis aanvraag, vergelijk offertes en kies de beste voor uw project. Geen verborgen kosten.",
    "city.seo_p3": "Of u nu een eenmalige dienst of doorlopende ondersteuning nodig heeft, ons netwerk van professionals in {city} staat klaar om te helpen.",
    "city.footer_title": "Nevumo — Wij verbinden u met lokale specialisten",
    "city.footer_in": "in"
}

# ---------------------------------------------------------------------------
# Portuguese (Brazil)
# ---------------------------------------------------------------------------
PT_DATA = {
    "city.nav_link": "Torne-se um especialista",
    "city.hero_title": "Encontre servicos em {city}",
    "city.search_placeholder": "Qual servico voce precisa?",
    "city.search_btn": "Buscar",
    "city.cta_request": "Receber ofertas",
    "city.categories_title": "Servicos populares em {city}",
    "city.cat_cleaning_leads": "Disponivel agora",
    "city.cat_plumbing_leads": "Disponivel agora",
    "city.cat_massage_leads": "Disponivel agora",
    "city.cat_cta": "Ver prestadores",
    "city.empty_title": "Nao encontrou o servico certo?",
    "city.empty_subtitle": "Descreva sua solicitacao e conectaremos voce com os especialistas certos.",
    "city.empty_cta": "Solicitar qualquer servico",
    "city.how_title": "Como funciona",
    "city.how_step_1": "Descreva sua solicitacao",
    "city.how_step_1_sub": "Leva 2 minutos",
    "city.how_step_2": "Receba ofertas de especialistas",
    "city.how_step_2_sub": "Geralmente em 30 minutos",
    "city.how_step_3": "Escolha e conecte-se diretamente",
    "city.how_step_3_sub": "Sem comissao, sem intermediarios",
    "city.seo_title": "Servicos em {city}",
    "city.seo_description": "Procura servicos confiaveis em {city}? A Nevumo conecta voce com especialistas locais verificados. De limpeza a encanamento e massagens profissionais.",
    "city.seo_p2": "Todos os especialistas na nossa plataforma sao avaliados por clientes reais. Envie uma solicitacao gratuita, compare ofertas e escolha a melhor para o seu projeto. Sem taxas ocultas.",
    "city.seo_p3": "Se voce precisa de um servico pontual ou suporte continuo, nossa rede de profissionais em {city} esta pronta para ajudar.",
    "city.footer_title": "Nevumo — Conectamos voce com especialistas locais",
    "city.footer_in": "em"
}

# ---------------------------------------------------------------------------
# Portuguese (Portugal)
# ---------------------------------------------------------------------------
PT_PT_DATA = {
    "city.nav_link": "Torne-se especialista",
    "city.hero_title": "Encontre servicos em {city}",
    "city.search_placeholder": "Que servico precisa?",
    "city.search_btn": "Pesquisar",
    "city.cta_request": "Receber propostas",
    "city.categories_title": "Servicos populares em {city}",
    "city.cat_cleaning_leads": "Disponivel agora",
    "city.cat_plumbing_leads": "Disponivel agora",
    "city.cat_massage_leads": "Disponivel agora",
    "city.cat_cta": "Ver prestadores",
    "city.empty_title": "Nao encontrou o servico certo?",
    "city.empty_subtitle": "Descreva o seu pedido e nos colocamo-lo em contacto com os especialistas certos.",
    "city.empty_cta": "Pedir qualquer servico",
    "city.how_title": "Como funciona",
    "city.how_step_1": "Descreva o seu pedido",
    "city.how_step_1_sub": "Demora 2 minutos",
    "city.how_step_2": "Receba propostas de especialistas",
    "city.how_step_2_sub": "Normalmente em 30 minutos",
    "city.how_step_3": "Escolha e contacte diretamente",
    "city.how_step_3_sub": "Sem comissao, sem intermediarios",
    "city.seo_title": "Servicos em {city}",
    "city.seo_description": "Procura servicos confiaveis em {city}? A Nevumo liga-o a especialistas locais verificados. De limpeza a canalização e massagens profissionais.",
    "city.seo_p2": "Todos os especialistas na nossa plataforma sao avaliados por clientes reais. Envie um pedido gratuito, compare propostas e escolha a melhor para o seu projeto. Sem taxas ocultas.",
    "city.seo_p3": "Seja para um servico pontual ou apoio continuo, a nossa rede de profissionais em {city} esta pronta a ajudar.",
    "city.footer_title": "Nevumo — Ligamos-o a especialistas locais",
    "city.footer_in": "em"
}

# ---------------------------------------------------------------------------
# Romanian
# ---------------------------------------------------------------------------
RO_DATA = {
    "city.nav_link": "Devino specialist",
    "city.hero_title": "Gaseste servicii in {city}",
    "city.search_placeholder": "De ce serviciu ai nevoie?",
    "city.search_btn": "Cauta",
    "city.cta_request": "Primeste oferte",
    "city.categories_title": "Servicii populare in {city}",
    "city.cat_cleaning_leads": "Disponibil acum",
    "city.cat_plumbing_leads": "Disponibil acum",
    "city.cat_massage_leads": "Disponibil acum",
    "city.cat_cta": "Vezi furnizorii",
    "city.empty_title": "Nu gasesti serviciul potrivit?",
    "city.empty_subtitle": "Descrie solicitarea ta si te vom pune in legatura cu specialistii potriviti.",
    "city.empty_cta": "Solicita orice serviciu",
    "city.how_title": "Cum functioneaza",
    "city.how_step_1": "Descrie solicitarea ta",
    "city.how_step_1_sub": "Dureaza 2 minute",
    "city.how_step_2": "Primeste oferte de la specialisti",
    "city.how_step_2_sub": "De obicei in 30 de minute",
    "city.how_step_3": "Alege si conecteaza-te direct",
    "city.how_step_3_sub": "Fara comision, fara intermediari",
    "city.seo_title": "Servicii in {city}",
    "city.seo_description": "Cauti servicii de incredere in {city}? Nevumo te conecteaza cu specialisti locali verificati. De la curatenie la instalatii sanitare si masaje profesionale.",
    "city.seo_p2": "Toti specialistii de pe platforma noastra sunt evaluati de clienti reali. Trimite o cerere gratuita, compara ofertele si alege-o pe cea mai buna pentru proiectul tau. Fara taxe ascunse.",
    "city.seo_p3": "Indiferent daca ai nevoie de un serviciu ocazional sau de suport continuu, reteaua noastra de profesionisti din {city} este pregatita sa ajute.",
    "city.footer_title": "Nevumo — Te conectam cu specialisti locali",
    "city.footer_in": "in"
}

# ---------------------------------------------------------------------------
# Czech
# ---------------------------------------------------------------------------
CS_DATA = {
    "city.nav_link": "Stat se specialistou",
    "city.hero_title": "Najit sluzby v {city}",
    "city.search_placeholder": "Jakou sluzbu potrebujete?",
    "city.search_btn": "Hledat",
    "city.cta_request": "Ziskat nabidky",
    "city.categories_title": "Oblibene sluzby v {city}",
    "city.cat_cleaning_leads": "K dispozici nyni",
    "city.cat_plumbing_leads": "K dispozici nyni",
    "city.cat_massage_leads": "K dispozici nyni",
    "city.cat_cta": "Zobrazit poskytovatele",
    "city.empty_title": "Nenasli jste spravnou sluzbu?",
    "city.empty_subtitle": "Popiste svuj pozadavek a my vas spojime se spravnymi specialisty.",
    "city.empty_cta": "Pozadat o jakoukoli sluzbu",
    "city.how_title": "Jak to funguje",
    "city.how_step_1": "Popiste svuj pozadavek",
    "city.how_step_1_sub": "Trva 2 minuty",
    "city.how_step_2": "Ziskejte nabidky od specialistu",
    "city.how_step_2_sub": "Obvykle do 30 minut",
    "city.how_step_3": "Vyberte a spojte se primo",
    "city.how_step_3_sub": "Bez provize, bez zprostredkovatelu",
    "city.seo_title": "Sluzby v {city}",
    "city.seo_description": "Hledate spolehliive sluzby v {city}? Nevumo vas spojuje s overenymi mistnimi specialisty. Od uklidu po instalaterske prace a profesionalni masaze.",
    "city.seo_p2": "Vsichni specialiste na nasi platforme jsou hodnoceni skutecnymi zakazniky. Poslete bezplatnou zadost, porovnejte nabidky a vyberte nejlepsi pro vas projekt. Bez skrytych poplatku.",
    "city.seo_p3": "At potrebujete jednorázovou sluzbu nebo pravidelnou podporu, nase sit profesionalu v {city} je pripravena pomoci.",
    "city.footer_title": "Nevumo — Spojujeme vas s mistnimi specialisty",
    "city.footer_in": "v"
}

# ---------------------------------------------------------------------------
# Slovak
# ---------------------------------------------------------------------------
SK_DATA = {
    "city.nav_link": "Stat sa specialistom",
    "city.hero_title": "Najdi sluzby v {city}",
    "city.search_placeholder": "Aku sluzbu potrebujete?",
    "city.search_btn": "Hladat",
    "city.cta_request": "Ziskat ponuky",
    "city.categories_title": "Oblubene sluzby v {city}",
    "city.cat_cleaning_leads": "K dispozicii teraz",
    "city.cat_plumbing_leads": "K dispozicii teraz",
    "city.cat_massage_leads": "K dispozicii teraz",
    "city.cat_cta": "Zobrazit poskytovatelov",
    "city.empty_title": "Nenasli ste spravnu sluzbu?",
    "city.empty_subtitle": "Opiste svoju poziadavku a my vas spojime so spravnymi specialistami.",
    "city.empty_cta": "Poziadat o akukolvek sluzbu",
    "city.how_title": "Ako to funguje",
    "city.how_step_1": "Opiste svoju poziadavku",
    "city.how_step_1_sub": "Trva 2 minuty",
    "city.how_step_2": "Ziskajte ponuky od specialistov",
    "city.how_step_2_sub": "Zvycajne do 30 minut",
    "city.how_step_3": "Vyberte a spojte sa priamo",
    "city.how_step_3_sub": "Bez provizii, bez sprostredkovatelov",
    "city.seo_title": "Sluzby v {city}",
    "city.seo_description": "Hladate spolahliive sluzby v {city}? Nevumo vas spoji s overenymi miestnymi specialistami. Od upratovania po instalaterske prace a profesionalne masaze.",
    "city.seo_p2": "Vsetci specialisti na nasej platforme su hodnoteni skutocnymi zakaznikmi. Poslite bezplatnu poziadavku, porovnajte ponuky a vyberte tu najlepsiu pre vas projekt. Bez skrytych poplatkov.",
    "city.seo_p3": "Ci potrebujete jednorazovu sluzbu alebo pravidielnu podporu, nasa siet profesionalov v {city} je pripravena pomoci.",
    "city.footer_title": "Nevumo — Spajame vas s miestnymi specialistami",
    "city.footer_in": "v"
}

# ---------------------------------------------------------------------------
# Hungarian
# ---------------------------------------------------------------------------
HU_DATA = {
    "city.nav_link": "Legyen szakerto",
    "city.hero_title": "Keress szolgaltatast {city} varosban",
    "city.search_placeholder": "Milyen szolgaltatasra van szuksege?",
    "city.search_btn": "Kereses",
    "city.cta_request": "Ajanlatok kerrese",
    "city.categories_title": "Nepszeru szolgaltatasok {city} varosban",
    "city.cat_cleaning_leads": "Most elerheto",
    "city.cat_plumbing_leads": "Most elerheto",
    "city.cat_massage_leads": "Most elerheto",
    "city.cat_cta": "Szolgaltatok megtekintese",
    "city.empty_title": "Nem talalja a megfelelo szolgaltatast?",
    "city.empty_subtitle": "Irja le kereslet es mi osszekaptoljuk a megfelelo szakertokkel.",
    "city.empty_cta": "Barmilyen szolgaltatas kerse",
    "city.how_title": "Hogyan mukodik",
    "city.how_step_1": "Irja le kereslet",
    "city.how_step_1_sub": "2 percet vesz igenybe",
    "city.how_step_2": "Ajanlatok erkeznek szakertokol",
    "city.how_step_2_sub": "Altalaban 30 percen belul",
    "city.how_step_3": "Valasszon es kapcsolodjon kozvetlenul",
    "city.how_step_3_sub": "Jutalek nelkul, kozvetitok nelkul",
    "city.seo_title": "Szolgaltatasok {city} varosban",
    "city.seo_description": "Megbizhatoo szolgaltatast keres {city} varosban? A Nevumo ellenorzott helyi szakertokkel koti ossze. Takaritastol a vizszerelesen at a professzionalis masszazsig.",
    "city.seo_p2": "Platformunkon minden szakertot valodi ugyfelek ertekelik. Kuldjoen ingyenes kerest, hasonlitsa ossze az ajanlatokat es valassza ki a legjobbat projektjehez. Nincsenek rejtett dijak.",
    "city.seo_p3": "Akár egyszeri szolgaltatasra, akar folyamatos tamogatasra van szuksege, {city} szakemberhálózatunk keszen all a segitsegre.",
    "city.footer_title": "Nevumo — Osszekapcsoljuk helyi szakertokkel",
    "city.footer_in": "varosban"
}

# ---------------------------------------------------------------------------
# Croatian
# ---------------------------------------------------------------------------
HR_DATA = {
    "city.nav_link": "Postani strucnjak",
    "city.hero_title": "Pronadji usluge u {city}",
    "city.search_placeholder": "Koju uslugu trebate?",
    "city.search_btn": "Trazi",
    "city.cta_request": "Dobij ponude",
    "city.categories_title": "Popularne usluge u {city}",
    "city.cat_cleaning_leads": "Dostupno sada",
    "city.cat_plumbing_leads": "Dostupno sada",
    "city.cat_massage_leads": "Dostupno sada",
    "city.cat_cta": "Pogledaj pruzatelje",
    "city.empty_title": "Ne mozes pronaci pravu uslugu?",
    "city.empty_subtitle": "Opisite svoj zahtjev i spojit cemo vas s pravim strucnjacima.",
    "city.empty_cta": "Zatrazite bilo koju uslugu",
    "city.how_title": "Kako funkcionira",
    "city.how_step_1": "Opisite sto trebate",
    "city.how_step_1_sub": "Traje 2 minute",
    "city.how_step_2": "Primite ponude od strucnjaka",
    "city.how_step_2_sub": "Obicno unutar 30 minuta",
    "city.how_step_3": "Odaberite i povezite se izravno",
    "city.how_step_3_sub": "Bez provizije, bez posrednika",
    "city.seo_title": "Usluge u {city}",
    "city.seo_description": "Trazite pouzdane usluge u {city}? Nevumo vas povezuje s provjerenim lokalnim strucnjacima. Od ciscenja do vodoinstalaterstva i profesionalnih masaza.",
    "city.seo_p2": "Svi strucnjaci na nasoj platformi ocijenjeni su od stvarnih kupaca. Posaljite besplatni zahtjev, usporedite ponude i odaberite najbolju za svoj projekt. Bez skrivenih naknada.",
    "city.seo_p3": "Trebate li jednokratnu uslugu ili stalnu podrsku, nasa mreza profesionalaca u {city} je spremna pomoci.",
    "city.footer_title": "Nevumo — Spajamo vas s lokalnim strucnjacima",
    "city.footer_in": "u"
}

# ---------------------------------------------------------------------------
# Slovenian
# ---------------------------------------------------------------------------
SL_DATA = {
    "city.nav_link": "Postani specialist",
    "city.hero_title": "Poisci storitve v {city}",
    "city.search_placeholder": "Katero storitev potrebujete?",
    "city.search_btn": "Iskanje",
    "city.cta_request": "Pridobi ponudbe",
    "city.categories_title": "Priljubljene storitve v {city}",
    "city.cat_cleaning_leads": "Na voljo zdaj",
    "city.cat_plumbing_leads": "Na voljo zdaj",
    "city.cat_massage_leads": "Na voljo zdaj",
    "city.cat_cta": "Poglej ponudnike",
    "city.empty_title": "Ne najdete prave storitve?",
    "city.empty_subtitle": "Opisite svojo zahtevo in vas bomo povezali s pravimi strokovnjaki.",
    "city.empty_cta": "Zahtevaj katero koli storitev",
    "city.how_title": "Kako deluje",
    "city.how_step_1": "Opisite svojo zahtevo",
    "city.how_step_1_sub": "Traja 2 minuti",
    "city.how_step_2": "Prejmite ponudbe od strokovnjakov",
    "city.how_step_2_sub": "Navadno v 30 minutah",
    "city.how_step_3": "Izberite in se neposredno povezite",
    "city.how_step_3_sub": "Brez provizije, brez posrednikov",
    "city.seo_title": "Storitve v {city}",
    "city.seo_description": "Iscete zanesljive storitve v {city}? Nevumo vas poveze z overjenimi lokalnimi strokovnjaki. Od ciscenja do vodovodnih del in profesionalnih masaz.",
    "city.seo_p2": "Vse strokovnjake na nasi platformi ocenjujejo pravi stranke. Posljite brezplacno zahtevo, primerjajte ponudbe in izberite najboljso za vas projekt. Brez skritih stroskov.",
    "city.seo_p3": "Ne glede na to, ali potrebujete enkratno storitev ali stalno podporo, je nasa mreza strokovnjakov v {city} pripravljena pomagati.",
    "city.footer_title": "Nevumo — Povezujemo vas z lokalnimi strokovnjaki",
    "city.footer_in": "v"
}

# ---------------------------------------------------------------------------
# Serbian
# ---------------------------------------------------------------------------
SR_DATA = {
    "city.nav_link": "Postani strucnjak",
    "city.hero_title": "Pronadji usluge u {city}",
    "city.search_placeholder": "Koju uslugu trebate?",
    "city.search_btn": "Trazi",
    "city.cta_request": "Dobij ponude",
    "city.categories_title": "Popularne usluge u {city}",
    "city.cat_cleaning_leads": "Dostupno sada",
    "city.cat_plumbing_leads": "Dostupno sada",
    "city.cat_massage_leads": "Dostupno sada",
    "city.cat_cta": "Pogledaj pruzaoce",
    "city.empty_title": "Ne mozes naci pravu uslugu?",
    "city.empty_subtitle": "Opisite zahtev i mi cemo vas povezati sa pravim strucnjacima.",
    "city.empty_cta": "Zatrazite bilo koju uslugu",
    "city.how_title": "Kako funkcionise",
    "city.how_step_1": "Opisite sta vam treba",
    "city.how_step_1_sub": "Traje 2 minuta",
    "city.how_step_2": "Primite ponude od strucnjaka",
    "city.how_step_2_sub": "Obicno u roku od 30 minuta",
    "city.how_step_3": "Izaberite i povezite se direktno",
    "city.how_step_3_sub": "Bez provizije, bez posrednika",
    "city.seo_title": "Usluge u {city}",
    "city.seo_description": "Trazite pouzdane usluge u {city}? Nevumo vas povezuje sa verifikovanim lokalnim strucnjacima. Od ciscenja do vodoinstalaterskih radova i profesionalnih masaza.",
    "city.seo_p2": "Svi strucnjaci na nasoj platformi se ocenjuju od strane pravih korisnika. Posaljite besplatan zahtev, uporedite ponude i izaberite onu koja je najbolja za vas projekat. Bez skrivenih naknada.",
    "city.seo_p3": "Bilo da vam je potrebna jednokratna usluga ili stalna podrska, nasa mreza profesionalaca u {city} je spremna da pomogne.",
    "city.footer_title": "Nevumo — Povezujemo vas sa lokalnim strucnjacima",
    "city.footer_in": "u"
}

# ---------------------------------------------------------------------------
# Macedonian
# ---------------------------------------------------------------------------
MK_DATA = {
    "city.nav_link": "\u0421\u0442\u0430\u043d\u0438 \u0441\u043f\u0435\u0446\u0438\u0458\u0430\u043b\u0438\u0441\u0442",
    "city.hero_title": "\u041d\u0430\u0458\u0434\u0438 \u0443\u0441\u043b\u0443\u0433\u0438 \u0432\u043e {city}",
    "city.search_placeholder": "\u041a\u0430\u043a\u0432\u0430 \u0443\u0441\u043b\u0443\u0433\u0430 \u0432\u0438 \u0442\u0440\u0435\u0431\u0430?",
    "city.search_btn": "\u0411\u0430\u0440\u0430\u0458",
    "city.cta_request": "\u0414\u043e\u0431\u0438\u0458 \u043f\u043e\u043d\u0443\u0434\u0438",
    "city.categories_title": "\u041f\u043e\u043f\u0443\u043b\u0430\u0440\u043d\u0438 \u0443\u0441\u043b\u0443\u0433\u0438 \u0432\u043e {city}",
    "city.cat_cleaning_leads": "\u0414\u043e\u0441\u0442\u0430\u043f\u043d\u043e \u0441\u0435\u0433\u0430",
    "city.cat_plumbing_leads": "\u0414\u043e\u0441\u0442\u0430\u043f\u043d\u043e \u0441\u0435\u0433\u0430",
    "city.cat_massage_leads": "\u0414\u043e\u0441\u0442\u0430\u043f\u043d\u043e \u0441\u0435\u0433\u0430",
    "city.cat_cta": "\u041f\u0440\u0435\u0433\u043b\u0435\u0434\u0430\u0458 \u0434\u0430\u0432\u0430\u0442\u0435\u043b\u0438",
    "city.empty_title": "\u041d\u0435 \u043c\u043e\u0436\u0435\u0448 \u0434\u0430 \u0458\u0430 \u043d\u0430\u0458\u0434\u0435\u0448 \u0432\u0438\u0441\u0442\u0438\u043d\u0441\u043a\u0430\u0442\u0430 \u0443\u0441\u043b\u0443\u0433\u0430?",
    "city.empty_subtitle": "\u041e\u043f\u0438\u0448\u0435\u0442\u0435 \u0433\u043e \u0431\u0430\u0440\u0430\u045a\u0435\u0442\u043e \u0438 \u043d\u0438\u0435 \u043a\u0435 \u043f\u043e\u0432\u0440\u0437\u0435\u043c\u0435 \u0441\u043e \u0432\u0438\u0441\u0442\u0438\u043d\u0441\u043a\u0438\u0442\u0435 \u0441\u043f\u0435\u0446\u0438\u0458\u0430\u043b\u0438\u0441\u0442\u0438.",
    "city.empty_cta": "\u041f\u043e\u0431\u0430\u0440\u0430\u0458 \u043a\u043e\u0458\u0430 \u0431\u0438\u043b\u043e \u0443\u0441\u043b\u0443\u0433\u0430",
    "city.how_title": "\u041a\u0430\u043a\u043e \u0444\u0443\u043d\u043a\u0446\u0438\u043e\u043d\u0438\u0440\u0430",
    "city.how_step_1": "\u041e\u043f\u0438\u0448\u0435\u0442\u0435 \u0433\u043e \u0431\u0430\u0440\u0430\u045a\u0435\u0442\u043e",
    "city.how_step_1_sub": "\u0422\u0440\u0430\u0435 2 \u043c\u0438\u043d\u0443\u0442\u0438",
    "city.how_step_2": "\u0414\u043e\u0431\u0438\u0458\u0442\u0435 \u043f\u043e\u043d\u0443\u0434\u0438 \u043e\u0434 \u0441\u043f\u0435\u0446\u0438\u0458\u0430\u043b\u0438\u0441\u0442\u0438",
    "city.how_step_2_sub": "\u041e\u0431\u0438\u0447\u043d\u043e \u0432\u043e \u0440\u043e\u043a \u043e\u0434 30 \u043c\u0438\u043d\u0443\u0442\u0438",
    "city.how_step_3": "\u0418\u0437\u0431\u0435\u0440\u0435\u0442\u0435 \u0438 \u043f\u043e\u0432\u0440\u0437\u0435\u0442\u0435 \u0441\u0435 \u0434\u0438\u0440\u0435\u043a\u0442\u043d\u043e",
    "city.how_step_3_sub": "\u0411\u0435\u0437 \u043f\u0440\u043e\u0432\u0438\u0437\u0438\u0458\u0430, \u0431\u0435\u0437 \u043f\u043e\u0441\u0440\u0435\u0434\u043d\u0438\u0446\u0438",
    "city.seo_title": "\u0423\u0441\u043b\u0443\u0433\u0438 \u0432\u043e {city}",
    "city.seo_description": "\u0411\u0430\u0440\u0430\u0442\u0435 \u0434\u043e\u0432\u0435\u0440\u043b\u0438\u0432\u0438 \u0443\u0441\u043b\u0443\u0433\u0438 \u0432\u043e {city}? Nevumo \u0432\u0435 \u043f\u043e\u0432\u0440\u0437\u0443\u0432\u0430 \u0441\u043e \u0432\u0435\u0440\u0438\u0444\u0438\u043a\u0443\u0432\u0430\u043d\u0438 \u043b\u043e\u043a\u0430\u043b\u043d\u0438 \u0441\u043f\u0435\u0446\u0438\u0458\u0430\u043b\u0438\u0441\u0442\u0438.",
    "city.seo_p2": "\u0421\u0438\u0442\u0435 \u0441\u043f\u0435\u0446\u0438\u0458\u0430\u043b\u0438\u0441\u0442\u0438 \u043d\u0430 \u043d\u0430\u0448\u0430\u0442\u0430 \u043f\u043b\u0430\u0442\u0444\u043e\u0440\u043c\u0430 \u0441\u0435 \u043e\u0446\u0435\u043d\u0443\u0432\u0430\u0430\u0442 \u043e\u0434 \u0432\u0438\u0441\u0442\u0438\u043d\u0441\u043a\u0438 \u043a\u043b\u0438\u0435\u043d\u0442\u0438. \u0418\u0441\u043f\u0440\u0430\u0442\u0435\u0442\u0435 \u0431\u0435\u0441\u043f\u043b\u0430\u0442\u043d\u043e \u0431\u0430\u0440\u0430\u045a\u0435, \u0441\u043f\u043e\u0440\u0435\u0434\u0435\u0442\u0435 \u0438 \u0438\u0437\u0431\u0435\u0440\u0435\u0442\u0435 \u0433\u043e \u043d\u0430\u0458\u0434\u043e\u0431\u0440\u043e\u0442\u043e.",
    "city.seo_p3": "\u0411\u0435\u0437 \u0440\u0430\u0437\u043b\u0438\u043a\u0430 \u0434\u0430\u043b\u0438 \u0432\u0438 \u0442\u0440\u0435\u0431\u0430 \u0435\u0434\u043d\u043e\u043a\u0440\u0430\u0442\u043d\u0430 \u0443\u0441\u043b\u0443\u0433\u0430 \u0438\u043b\u0438 \u043a\u043e\u043d\u0442\u0438\u043d\u0443\u0438\u0440\u0430\u043d\u0430 \u043f\u043e\u0434\u0434\u0440\u0448\u043a\u0430, \u043d\u0430\u0448\u0430\u0442\u0430 \u043c\u0440\u0435\u0436\u0430 \u0432\u043e {city} \u0435 \u0433\u043e\u0442\u043e\u0432\u0430 \u0434\u0430 \u043f\u043e\u043c\u043e\u0433\u043d\u0435.",
    "city.footer_title": "Nevumo \u2014 \u0412\u0435 \u043f\u043e\u0432\u0440\u0437\u0443\u0432\u0430\u043c\u0435 \u0441\u043e \u043b\u043e\u043a\u0430\u043b\u043d\u0438 \u0441\u043f\u0435\u0446\u0438\u0458\u0430\u043b\u0438\u0441\u0442\u0438",
    "city.footer_in": "\u0432\u043e"
}

# ---------------------------------------------------------------------------
# Albanian
# ---------------------------------------------------------------------------
SQ_DATA = {
    "city.nav_link": "Behu specialist",
    "city.hero_title": "Gjej sherbime ne {city}",
    "city.search_placeholder": "Cfare sherbimi keni nevoje?",
    "city.search_btn": "Kerko",
    "city.cta_request": "Merr oferta",
    "city.categories_title": "Sherbime te njohura ne {city}",
    "city.cat_cleaning_leads": "Disponibel tani",
    "city.cat_plumbing_leads": "Disponibel tani",
    "city.cat_massage_leads": "Disponibel tani",
    "city.cat_cta": "Shiko ofruesit",
    "city.empty_title": "Nuk gjen sherbimin e duhur?",
    "city.empty_subtitle": "Pershkruani kerkesen tuaj dhe ne do t'ju lidhim me specialistet e duhur.",
    "city.empty_cta": "Kerko cdo sherbim",
    "city.how_title": "Si funksionon",
    "city.how_step_1": "Pershkruani kerkesen tuaj",
    "city.how_step_1_sub": "Zgjat 2 minuta",
    "city.how_step_2": "Merrni oferta nga specialistet",
    "city.how_step_2_sub": "Zakonisht brenda 30 minutave",
    "city.how_step_3": "Zgjidhni dhe lidhuni drejperdrejt",
    "city.how_step_3_sub": "Pa komision, pa ndermjetes",
    "city.seo_title": "Sherbime ne {city}",
    "city.seo_description": "Po kerkoni sherbime te besueshme ne {city}? Nevumo ju lidh me specialiste lokale te verifikuar. Nga pastrimi tek hidraulika dhe masazhet profesionale.",
    "city.seo_p2": "Te gjithe specialistet ne platformen tone vlersohen nga klientet reale. Dergoni nje kerkese falas, krahasoni ofertat dhe zgjidhni me te miren per projektin tuaj. Pa tarifa te fshehura.",
    "city.seo_p3": "Pavarsisht nese keni nevoje per nje sherbim njeheresh ose mbeshtetje te vazhdueshme, rrjeti yne i profesionisteve ne {city} eshte gati te ndihmoje.",
    "city.footer_title": "Nevumo — Ju lidhim me specialiste lokale",
    "city.footer_in": "ne"
}

# ---------------------------------------------------------------------------
# Greek
# ---------------------------------------------------------------------------
EL_DATA = {
    "city.nav_link": "\u0393\u03af\u03bd\u03b5 \u03b5\u03b9\u03b4\u03b9\u03ba\u03cc\u03c2",
    "city.hero_title": "\u0392\u03c1\u03b5\u03c2 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b5\u03c2 \u03c3\u03c4\u03b7\u03bd {city}",
    "city.search_placeholder": "\u03a0\u03bf\u03b9\u03b1 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b1 \u03c7\u03c1\u03b5\u03b9\u03ac\u03b6\u03b5\u03c3\u03b1\u03b9;",
    "city.search_btn": "\u0391\u03bd\u03b1\u03b6\u03ae\u03c4\u03b7\u03c3\u03b7",
    "city.cta_request": "\u039b\u03ac\u03b2\u03b5 \u03c0\u03c1\u03bf\u03c3\u03c6\u03bf\u03c1\u03ad\u03c2",
    "city.categories_title": "\u0394\u03b7\u03bc\u03bf\u03c6\u03b9\u03bb\u03b5\u03af\u03c2 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b5\u03c2 \u03c3\u03c4\u03b7\u03bd {city}",
    "city.cat_cleaning_leads": "\u0394\u03b9\u03b1\u03b8\u03ad\u03c3\u03b9\u03bc\u03bf \u03c4\u03ce\u03c1\u03b1",
    "city.cat_plumbing_leads": "\u0394\u03b9\u03b1\u03b8\u03ad\u03c3\u03b9\u03bc\u03bf \u03c4\u03ce\u03c1\u03b1",
    "city.cat_massage_leads": "\u0394\u03b9\u03b1\u03b8\u03ad\u03c3\u03b9\u03bc\u03bf \u03c4\u03ce\u03c1\u03b1",
    "city.cat_cta": "\u0394\u03b5\u03c2 \u03c0\u03b1\u03c1\u03cc\u03c7\u03bf\u03c5\u03c2",
    "city.empty_title": "\u0394\u03b5\u03bd \u03b2\u03c1\u03af\u03c3\u03ba\u03b5\u03b9\u03c2 \u03c4\u03b7\u03bd \u03ba\u03b1\u03c4\u03ac\u03bb\u03bb\u03b7\u03bb\u03b7 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b1;",
    "city.empty_subtitle": "\u03a0\u03b5\u03c1\u03af\u03b3\u03c1\u03b1\u03c8\u03b5 \u03c4\u03bf \u03b1\u03af\u03c4\u03b7\u03bc\u03ac \u03c3\u03bf\u03c5 \u03ba\u03b1\u03b9 \u03b8\u03b1 \u03c3\u03b5 \u03c3\u03c5\u03bd\u03b4\u03ad\u03c3\u03bf\u03c5\u03bc\u03b5 \u03bc\u03b5 \u03c4\u03bf\u03c5\u03c2 \u03ba\u03b1\u03c4\u03ac\u03bb\u03bb\u03b7\u03bb\u03bf\u03c5\u03c2 \u03b5\u03b9\u03b4\u03b9\u03ba\u03bf\u03cd\u03c2.",
    "city.empty_cta": "\u0396\u03ae\u03c4\u03b7\u03c3\u03b5 \u03bf\u03c0\u03bf\u03b9\u03b1\u03b4\u03ae\u03c0\u03bf\u03c4\u03b5 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b1",
    "city.how_title": "\u03a0\u03ce\u03c2 \u03bb\u03b5\u03b9\u03c4\u03bf\u03c5\u03c1\u03b3\u03b5\u03af",
    "city.how_step_1": "\u03a0\u03b5\u03c1\u03af\u03b3\u03c1\u03b1\u03c8\u03b5 \u03c4\u03bf \u03b1\u03af\u03c4\u03b7\u03bc\u03ac \u03c3\u03bf\u03c5",
    "city.how_step_1_sub": "\u0394\u03b9\u03b1\u03c1\u03ba\u03b5\u03af 2 \u03bb\u03b5\u03c0\u03c4\u03ac",
    "city.how_step_2": "\u039b\u03ac\u03b2\u03b5 \u03c0\u03c1\u03bf\u03c3\u03c6\u03bf\u03c1\u03ad\u03c2 \u03b1\u03c0\u03cc \u03b5\u03b9\u03b4\u03b9\u03ba\u03bf\u03cd\u03c2",
    "city.how_step_2_sub": "\u03a3\u03c5\u03bd\u03ae\u03b8\u03c9\u03c2 \u03c3\u03b5 30 \u03bb\u03b5\u03c0\u03c4\u03ac",
    "city.how_step_3": "\u0395\u03c0\u03af\u03bb\u03b5\u03be\u03b5 \u03ba\u03b1\u03b9 \u03c3\u03c5\u03bd\u03b4\u03ad\u03c3\u03bf\u03c5 \u03ac\u03bc\u03b5\u03c3\u03b1",
    "city.how_step_3_sub": "\u03a7\u03c9\u03c1\u03af\u03c2 \u03c0\u03c1\u03bf\u03bc\u03ae\u03b8\u03b5\u03b9\u03b1, \u03c7\u03c9\u03c1\u03af\u03c2 \u03bc\u03b5\u03c3\u03ac\u03b6\u03bf\u03bd\u03c4\u03b5\u03c2",
    "city.seo_title": "\u03a5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b5\u03c2 \u03c3\u03c4\u03b7\u03bd {city}",
    "city.seo_description": "\u03a8\u03ac\u03c7\u03bd\u03b5\u03b9\u03c2 \u03b1\u03be\u03b9\u03cc\u03c0\u03b9\u03c3\u03c4\u03b5\u03c2 \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b5\u03c2 \u03c3\u03c4\u03b7\u03bd {city}; \u0397 Nevumo \u03c3\u03b5 \u03c3\u03c5\u03bd\u03b4\u03ad\u03b5\u03b9 \u03bc\u03b5 \u03c0\u03b9\u03c3\u03c4\u03bf\u03c0\u03bf\u03b9\u03b7\u03bc\u03ad\u03bd\u03bf\u03c5\u03c2 \u03c4\u03bf\u03c0\u03b9\u03ba\u03bf\u03cd\u03c2 \u03b5\u03b9\u03b4\u03b9\u03ba\u03bf\u03cd\u03c2.",
    "city.seo_p2": "\u038c\u03bb\u03bf\u03b9 \u03bf\u03b9 \u03b5\u03b9\u03b4\u03b9\u03ba\u03bf\u03af \u03c3\u03c4\u03b7\u03bd \u03c0\u03bb\u03b1\u03c4\u03c6\u03cc\u03c1\u03bc\u03b1 \u03bc\u03b1\u03c2 \u03b1\u03be\u03b9\u03bf\u03bb\u03bf\u03b3\u03bf\u03cd\u03bd\u03c4\u03b1\u03b9 \u03b1\u03c0\u03cc \u03c0\u03c1\u03b1\u03b3\u03bc\u03b1\u03c4\u03b9\u03ba\u03bf\u03cd\u03c2 \u03c0\u03b5\u03bb\u03ac\u03c4\u03b5\u03c2. \u03a3\u03c4\u03b5\u03af\u03bb\u03b5 \u03b4\u03c9\u03c1\u03b5\u03ac\u03bd \u03b1\u03af\u03c4\u03b7\u03bc\u03b1, \u03c3\u03cd\u03b3\u03ba\u03c1\u03b9\u03bd\u03b5 \u03c0\u03c1\u03bf\u03c3\u03c6\u03bf\u03c1\u03ad\u03c2 \u03ba\u03b1\u03b9 \u03b5\u03c0\u03af\u03bb\u03b5\u03be\u03b5 \u03c4\u03b7\u03bd \u03ba\u03b1\u03bb\u03cd\u03c4\u03b5\u03c1\u03b7.",
    "city.seo_p3": "\u0395\u03af\u03c4\u03b5 \u03c7\u03c1\u03b5\u03b9\u03ac\u03b6\u03b5\u03c3\u03b1\u03b9 \u03b5\u03c6\u03ac\u03c0\u03b1\u03be \u03c5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b1 \u03b5\u03af\u03c4\u03b5 \u03c3\u03c5\u03bd\u03b5\u03c7\u03ae \u03c5\u03c0\u03bf\u03c3\u03c4\u03ae\u03c1\u03b9\u03be\u03b7, \u03c4\u03bf \u03b4\u03af\u03ba\u03c4\u03c5\u03bf \u03b5\u03c0\u03b1\u03b3\u03b3\u03b5\u03bb\u03bc\u03b1\u03c4\u03b9\u03ce\u03bd \u03bc\u03b1\u03c2 \u03c3\u03c4\u03b7\u03bd {city} \u03b5\u03af\u03bd\u03b1\u03b9 \u03ad\u03c4\u03bf\u03b9\u03bc\u03bf \u03bd\u03b1 \u03b2\u03bf\u03b7\u03b8\u03ae\u03c3\u03b5\u03b9.",
    "city.footer_title": "Nevumo \u2014 \u03a3\u03b5 \u03c3\u03c5\u03bd\u03b4\u03ad\u03bf\u03c5\u03bc\u03b5 \u03bc\u03b5 \u03c4\u03bf\u03c0\u03b9\u03ba\u03bf\u03cd\u03c2 \u03b5\u03b9\u03b4\u03b9\u03ba\u03bf\u03cd\u03c2",
    "city.footer_in": "\u03c3\u03c4\u03b7\u03bd"
}

# ---------------------------------------------------------------------------
# Turkish
# ---------------------------------------------------------------------------
TR_DATA = {
    "city.nav_link": "Uzman ol",
    "city.hero_title": "{city} sehrinde hizmet bul",
    "city.search_placeholder": "Hangi hizmete ihtiyaciniz var?",
    "city.search_btn": "Ara",
    "city.cta_request": "Teklifler al",
    "city.categories_title": "{city} sehrinde populer hizmetler",
    "city.cat_cleaning_leads": "Su an mevcut",
    "city.cat_plumbing_leads": "Su an mevcut",
    "city.cat_massage_leads": "Su an mevcut",
    "city.cat_cta": "Hizmet saglayanilari gor",
    "city.empty_title": "Dogru hizmeti bulamiyor musunuz?",
    "city.empty_subtitle": "Talebinizi aciklayin, sizi dogru uzmanlarla bulusturalim.",
    "city.empty_cta": "Herhangi bir hizmet talep edin",
    "city.how_title": "Nasil calisir",
    "city.how_step_1": "Talebinizi aciklayin",
    "city.how_step_1_sub": "2 dakika surer",
    "city.how_step_2": "Uzmanlardan teklifler alin",
    "city.how_step_2_sub": "Genellikle 30 dakika icinde",
    "city.how_step_3": "Secin ve dogrudan baglanin",
    "city.how_step_3_sub": "Komisyon yok, aracilar yok",
    "city.seo_title": "{city} sehrinde hizmetler",
    "city.seo_description": "{city} sehrinde guvenilir hizmetler mi ariyorsunuz? Nevumo sizi dogrulanmis yerel uzmanlarla bulustururur. Temizlikten tesisata ve profesyonel masaja kadar.",
    "city.seo_p2": "Platformumuzdaki tum uzmanlar gercek musteriler tarafindan degerlendirilmektedir. Ucretsiz talep gonderin, teklifleri karsilastirin ve projeniz icin en iyisini secin. Gizli ucret yok.",
    "city.seo_p3": "Tek seferlik bir hizmet veya surekli destek ihtiyaciniz olsun, {city} sehrindeki profesyoneller agimiz yardima hazir.",
    "city.footer_title": "Nevumo — Sizi yerel uzmanlarla bulustuuruyoruz",
    "city.footer_in": "sehrinde"
}

# ---------------------------------------------------------------------------
# Russian
# ---------------------------------------------------------------------------
RU_DATA = {
    "city.nav_link": "\u0421\u0442\u0430\u0442\u044c \u0441\u043f\u0435\u0446\u0438\u0430\u043b\u0438\u0441\u0442\u043e\u043c",
    "city.hero_title": "\u041d\u0430\u0439\u0442\u0438 \u0443\u0441\u043b\u0443\u0433\u0438 \u0432 {city}",
    "city.search_placeholder": "\u041a\u0430\u043a\u0430\u044f \u0443\u0441\u043b\u0443\u0433\u0430 \u0432\u0430\u043c \u043d\u0443\u0436\u043d\u0430?",
    "city.search_btn": "\u0418\u0441\u043a\u0430\u0442\u044c",
    "city.cta_request": "\u041f\u043e\u043b\u0443\u0447\u0438\u0442\u044c \u043f\u0440\u0435\u0434\u043b\u043e\u0436\u0435\u043d\u0438\u044f",
    "city.categories_title": "\u041f\u043e\u043f\u0443\u043b\u044f\u0440\u043d\u044b\u0435 \u0443\u0441\u043b\u0443\u0433\u0438 \u0432 {city}",
    "city.cat_cleaning_leads": "\u0414\u043e\u0441\u0442\u0443\u043f\u043d\u043e \u0441\u0435\u0439\u0447\u0430\u0441",
    "city.cat_plumbing_leads": "\u0414\u043e\u0441\u0442\u0443\u043f\u043d\u043e \u0441\u0435\u0439\u0447\u0430\u0441",
    "city.cat_massage_leads": "\u0414\u043e\u0441\u0442\u0443\u043f\u043d\u043e \u0441\u0435\u0439\u0447\u0430\u0441",
    "city.cat_cta": "\u0421\u043c\u043e\u0442\u0440\u0435\u0442\u044c \u0438\u0441\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u0435\u0439",
    "city.empty_title": "\u041d\u0435 \u043c\u043e\u0436\u0435\u0442\u0435 \u043d\u0430\u0439\u0442\u0438 \u043d\u0443\u0436\u043d\u0443\u044e \u0443\u0441\u043b\u0443\u0433\u0443?",
    "city.empty_subtitle": "\u041e\u043f\u0438\u0448\u0438\u0442\u0435 \u0441\u0432\u043e\u0439 \u0437\u0430\u043f\u0440\u043e\u0441, \u0438 \u043c\u044b \u0441\u0432\u044f\u0436\u0435\u043c \u0432\u0430\u0441 \u0441 \u043f\u043e\u0434\u0445\u043e\u0434\u044f\u0449\u0438\u043c\u0438 \u0441\u043f\u0435\u0446\u0438\u0430\u043b\u0438\u0441\u0442\u0430\u043c\u0438.",
    "city.empty_cta": "\u0417\u0430\u043f\u0440\u043e\u0441\u0438\u0442\u044c \u043b\u044e\u0431\u0443\u044e \u0443\u0441\u043b\u0443\u0433\u0443",
    "city.how_title": "\u041a\u0430\u043a \u044d\u0442\u043e \u0440\u0430\u0431\u043e\u0442\u0430\u0435\u0442",
    "city.how_step_1": "\u041e\u043f\u0438\u0448\u0438\u0442\u0435 \u0441\u0432\u043e\u0439 \u0437\u0430\u043f\u0440\u043e\u0441",
    "city.how_step_1_sub": "\u0417\u0430\u0439\u043c\u0451\u0442 2 \u043c\u0438\u043d\u0443\u0442\u044b",
    "city.how_step_2": "\u041f\u043e\u043b\u0443\u0447\u0438\u0442\u0435 \u043f\u0440\u0435\u0434\u043b\u043e\u0436\u0435\u043d\u0438\u044f \u043e\u0442 \u0441\u043f\u0435\u0446\u0438\u0430\u043b\u0438\u0441\u0442\u043e\u0432",
    "city.how_step_2_sub": "\u041e\u0431\u044b\u0447\u043d\u043e \u0432 \u0442\u0435\u0447\u0435\u043d\u0438\u0435 30 \u043c\u0438\u043d\u0443\u0442",
    "city.how_step_3": "\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0438 \u0441\u0432\u044f\u0436\u0438\u0442\u0435\u0441\u044c \u043d\u0430\u043f\u0440\u044f\u043c\u0443\u044e",
    "city.how_step_3_sub": "\u0411\u0435\u0437 \u043a\u043e\u043c\u0438\u0441\u0441\u0438\u0438, \u0431\u0435\u0437 \u043f\u043e\u0441\u0440\u0435\u0434\u043d\u0438\u043a\u043e\u0432",
    "city.seo_title": "\u0423\u0441\u043b\u0443\u0433\u0438 \u0432 {city}",
    "city.seo_description": "\u0418\u0449\u0435\u0442\u0435 \u043d\u0430\u0434\u0451\u0436\u043d\u044b\u0435 \u0443\u0441\u043b\u0443\u0433\u0438 \u0432 {city}? Nevumo \u0441\u043e\u0435\u0434\u0438\u043d\u0438\u0442 \u0432\u0430\u0441 \u0441 \u043f\u0440\u043e\u0432\u0435\u0440\u0435\u043d\u043d\u044b\u043c\u0438 \u043c\u0435\u0441\u0442\u043d\u044b\u043c\u0438 \u0441\u043f\u0435\u0446\u0438\u0430\u043b\u0438\u0441\u0442\u0430\u043c\u0438. \u041e\u0442 \u0443\u0431\u043e\u0440\u043a\u0438 \u0434\u043e \u0441\u0430\u043d\u0442\u0435\u0445\u043d\u0438\u043a\u0438 \u0438 \u043f\u0440\u043e\u0444\u0435\u0441\u0441\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e\u0433\u043e \u043c\u0430\u0441\u0441\u0430\u0436\u0430.",
    "city.seo_p2": "\u0412\u0441\u0435 \u0441\u043f\u0435\u0446\u0438\u0430\u043b\u0438\u0441\u0442\u044b \u043d\u0430 \u043d\u0430\u0448\u0435\u0439 \u043f\u043b\u0430\u0442\u0444\u043e\u0440\u043c\u0435 \u043e\u0446\u0435\u043d\u0438\u0432\u0430\u044e\u0442\u0441\u044f \u0440\u0435\u0430\u043b\u044c\u043d\u044b\u043c\u0438 \u043a\u043b\u0438\u0435\u043d\u0442\u0430\u043c\u0438. \u041e\u0442\u043f\u0440\u0430\u0432\u044c\u0442\u0435 \u0431\u0435\u0441\u043f\u043b\u0430\u0442\u043d\u044b\u0439 \u0437\u0430\u043f\u0440\u043e\u0441, \u0441\u0440\u0430\u0432\u043d\u0438\u0442\u0435 \u043f\u0440\u0435\u0434\u043b\u043e\u0436\u0435\u043d\u0438\u044f \u0438 \u0432\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u043b\u0443\u0447\u0448\u0435\u0435.",
    "city.seo_p3": "\u041d\u0443\u0436\u043d\u0430 \u0440\u0430\u0437\u043e\u0432\u0430\u044f \u0443\u0441\u043b\u0443\u0433\u0430 \u0438\u043b\u0438 \u043f\u043e\u0441\u0442\u043e\u044f\u043d\u043d\u0430\u044f \u043f\u043e\u0434\u0434\u0435\u0440\u0436\u043a\u0430 — \u043d\u0430\u0448\u0430 \u0441\u0435\u0442\u044c \u043f\u0440\u043e\u0444\u0435\u0441\u0441\u0438\u043e\u043d\u0430\u043b\u043e\u0432 \u0432 {city} \u0433\u043e\u0442\u043e\u0432\u0430 \u043f\u043e\u043c\u043e\u0447\u044c.",
    "city.footer_title": "Nevumo \u2014 \u0421\u043e\u0435\u0434\u0438\u043d\u044f\u0435\u043c \u0432\u0430\u0441 \u0441 \u043c\u0435\u0441\u0442\u043d\u044b\u043c\u0438 \u0441\u043f\u0435\u0446\u0438\u0430\u043b\u0438\u0441\u0442\u0430\u043c\u0438",
    "city.footer_in": "\u0432"
}

# ---------------------------------------------------------------------------
# Ukrainian
# ---------------------------------------------------------------------------
UK_DATA = {
    "city.nav_link": "\u0421\u0442\u0430\u0442\u0438 \u0441\u043f\u0435\u0446\u0456\u0430\u043b\u0456\u0441\u0442\u043e\u043c",
    "city.hero_title": "\u0417\u043d\u0430\u0439\u0442\u0438 \u043f\u043e\u0441\u043b\u0443\u0433\u0438 \u0443 {city}",
    "city.search_placeholder": "\u042f\u043a\u0430 \u043f\u043e\u0441\u043b\u0443\u0433\u0430 \u0432\u0430\u043c \u043f\u043e\u0442\u0440\u0456\u0431\u043d\u0430?",
    "city.search_btn": "\u0428\u0443\u043a\u0430\u0442\u0438",
    "city.cta_request": "\u041e\u0442\u0440\u0438\u043c\u0430\u0442\u0438 \u043f\u0440\u043e\u043f\u043e\u0437\u0438\u0446\u0456\u0457",
    "city.categories_title": "\u041f\u043e\u043f\u0443\u043b\u044f\u0440\u043d\u0456 \u043f\u043e\u0441\u043b\u0443\u0433\u0438 \u0443 {city}",
    "city.cat_cleaning_leads": "\u0414\u043e\u0441\u0442\u0443\u043f\u043d\u043e \u0437\u0430\u0440\u0430\u0437",
    "city.cat_plumbing_leads": "\u0414\u043e\u0441\u0442\u0443\u043f\u043d\u043e \u0437\u0430\u0440\u0430\u0437",
    "city.cat_massage_leads": "\u0414\u043e\u0441\u0442\u0443\u043f\u043d\u043e \u0437\u0430\u0440\u0430\u0437",
    "city.cat_cta": "\u0414\u0438\u0432\u0438\u0442\u0438\u0441\u044c \u0432\u0438\u043a\u043e\u043d\u0430\u0432\u0446\u0456\u0432",
    "city.empty_title": "\u041d\u0435 \u043c\u043e\u0436\u0435\u0442\u0435 \u0437\u043d\u0430\u0439\u0442\u0438 \u043f\u043e\u0442\u0440\u0456\u0431\u043d\u0443 \u043f\u043e\u0441\u043b\u0443\u0433\u0443?",
    "city.empty_subtitle": "\u041e\u043f\u0438\u0448\u0456\u0442\u044c \u0432\u0430\u0448 \u0437\u0430\u043f\u0438\u0442, \u0456 \u043c\u0438 \u0437'\u0454\u0434\u043d\u0430\u0454\u043c\u043e \u0432\u0430\u0441 \u0437 \u043f\u043e\u0442\u0440\u0456\u0431\u043d\u0438\u043c\u0438 \u0441\u043f\u0435\u0446\u0456\u0430\u043b\u0456\u0441\u0442\u0430\u043c\u0438.",
    "city.empty_cta": "\u0417\u0430\u043f\u0440\u043e\u0441\u0438\u0442\u0438 \u0431\u0443\u0434\u044c-\u044f\u043a\u0443 \u043f\u043e\u0441\u043b\u0443\u0433\u0443",
    "city.how_title": "\u042f\u043a \u0446\u0435 \u043f\u0440\u0430\u0446\u044e\u0454",
    "city.how_step_1": "\u041e\u043f\u0438\u0448\u0456\u0442\u044c \u0432\u0430\u0448 \u0437\u0430\u043f\u0438\u0442",
    "city.how_step_1_sub": "\u0417\u0430\u0439\u043c\u0435 2 \u0445\u0432\u0438\u043b\u0438\u043d\u0438",
    "city.how_step_2": "\u041e\u0442\u0440\u0438\u043c\u0430\u0439\u0442\u0435 \u043f\u0440\u043e\u043f\u043e\u0437\u0438\u0446\u0456\u0457 \u0432\u0456\u0434 \u0441\u043f\u0435\u0446\u0456\u0430\u043b\u0456\u0441\u0442\u0456\u0432",
    "city.how_step_2_sub": "\u0417\u0432\u0438\u0447\u0430\u0439\u043d\u043e \u043f\u0440\u043e\u0442\u044f\u0433\u043e\u043c 30 \u0445\u0432\u0438\u043b\u0438\u043d",
    "city.how_step_3": "\u0412\u0438\u0431\u0435\u0440\u0456\u0442\u044c \u0442\u0430 \u0437\u0432'\u0454\u0436\u0442\u0435\u0441\u044c \u043d\u0430\u043f\u0440\u044f\u043c\u0443",
    "city.how_step_3_sub": "\u0411\u0435\u0437 \u043a\u043e\u043c\u0456\u0441\u0456\u0457, \u0431\u0435\u0437 \u043f\u043e\u0441\u0435\u0440\u0435\u0434\u043d\u0438\u043a\u0456\u0432",
    "city.seo_title": "\u041f\u043e\u0441\u043b\u0443\u0433\u0438 \u0443 {city}",
    "city.seo_description": "\u0428\u0443\u043a\u0430\u0454\u0442\u0435 \u043d\u0430\u0434\u0456\u0439\u043d\u0456 \u043f\u043e\u0441\u043b\u0443\u0433\u0438 \u0443 {city}? Nevumo \u0437'\u0454\u0434\u043d\u0443\u0454 \u0432\u0430\u0441 \u0437 \u043f\u0435\u0440\u0435\u0432\u0456\u0440\u0435\u043d\u0438\u043c\u0438 \u043c\u0456\u0441\u0446\u0435\u0432\u0438\u043c\u0438 \u0441\u043f\u0435\u0446\u0456\u0430\u043b\u0456\u0441\u0442\u0430\u043c\u0438. \u0412\u0456\u0434 \u043f\u0440\u0438\u0431\u0438\u0440\u0430\u043d\u043d\u044f \u0434\u043e \u0441\u0430\u043d\u0442\u0435\u0445\u043d\u0456\u043a\u0438 \u0442\u0430 \u043f\u0440\u043e\u0444\u0435\u0441\u0456\u0439\u043d\u043e\u0433\u043e \u043c\u0430\u0441\u0430\u0436\u0443.",
    "city.seo_p2": "\u0412\u0441\u0456 \u0441\u043f\u0435\u0446\u0456\u0430\u043b\u0456\u0441\u0442\u0438 \u043d\u0430 \u043d\u0430\u0448\u0456\u0439 \u043f\u043b\u0430\u0442\u0444\u043e\u0440\u043c\u0456 \u043e\u0446\u0456\u043d\u044e\u044e\u0442\u044c\u0441\u044f \u0440\u0435\u0430\u043b\u044c\u043d\u0438\u043c\u0438 \u043a\u043b\u0456\u0454\u043d\u0442\u0430\u043c\u0438. \u041d\u0430\u0434\u0456\u0448\u043b\u0456\u0442\u044c \u0431\u0435\u0437\u043a\u043e\u0448\u0442\u043e\u0432\u043d\u0438\u0439 \u0437\u0430\u043f\u0438\u0442, \u043f\u043e\u0440\u0456\u0432\u043d\u044f\u0439\u0442\u0435 \u043f\u0440\u043e\u043f\u043e\u0437\u0438\u0446\u0456\u0457 \u0456 \u043e\u0431\u0435\u0440\u0456\u0442\u044c \u043d\u0430\u0439\u043a\u0440\u0430\u0449\u0435.",
    "city.seo_p3": "\u0427\u0438 \u043f\u043e\u0442\u0440\u0456\u0431\u043d\u0430 \u0440\u0430\u0437\u043e\u0432\u0430 \u043f\u043e\u0441\u043b\u0443\u0433\u0430 \u0447\u0438 \u043f\u043e\u0441\u0442\u0456\u0439\u043d\u0430 \u043f\u0456\u0434\u0442\u0440\u0438\u043c\u043a\u0430 — \u043d\u0430\u0448\u0430 \u043c\u0435\u0440\u0435\u0436\u0430 \u043f\u0440\u043e\u0444\u0435\u0441\u0456\u043e\u043d\u0430\u043b\u0456\u0432 \u0443 {city} \u0433\u043e\u0442\u043e\u0432\u0430 \u0434\u043e\u043f\u043e\u043c\u043e\u0433\u0442\u0438.",
    "city.footer_title": "Nevumo \u2014 \u0417'\u0454\u0434\u043d\u0443\u0454\u043c\u043e \u0432\u0430\u0441 \u0437 \u043c\u0456\u0441\u0446\u0435\u0432\u0438\u043c\u0438 \u0441\u043f\u0435\u0446\u0456\u0430\u043b\u0456\u0441\u0442\u0430\u043c\u0438",
    "city.footer_in": "\u0443"
}

# ---------------------------------------------------------------------------
# Latvian
# ---------------------------------------------------------------------------
LV_DATA = {
    "city.nav_link": "Klust par specialistu",
    "city.hero_title": "Atrodi pakalpojumus pilseta {city}",
    "city.search_placeholder": "Kadu pakalpojumu vajag?",
    "city.search_btn": "Meklet",
    "city.cta_request": "Sanemt piedavajumus",
    "city.categories_title": "Populari pakalpojumi pilseta {city}",
    "city.cat_cleaning_leads": "Pieejams tagad",
    "city.cat_plumbing_leads": "Pieejams tagad",
    "city.cat_massage_leads": "Pieejams tagad",
    "city.cat_cta": "Skatit pakalpojumu sniedzejus",
    "city.empty_title": "Nevari atrast pareizo pakalpojumu?",
    "city.empty_subtitle": "Apraksti savu pieprasijumu un mes tevi savienosim ar pareizajiem specialistiem.",
    "city.empty_cta": "Pieprasit jebkuru pakalpojumu",
    "city.how_title": "Ka tas darbojas",
    "city.how_step_1": "Apraksti savu pieprasijumu",
    "city.how_step_1_sub": "Aiznem 2 minutes",
    "city.how_step_2": "Sanem piedavajumus no specialistiem",
    "city.how_step_2_sub": "Parasti 30 minusu laika",
    "city.how_step_3": "Izveleties un savienojies tiesi",
    "city.how_step_3_sub": "Bez komisijas, bez starpniekiem",
    "city.seo_title": "Pakalpojumi pilseta {city}",
    "city.seo_description": "Mekle uzticamus pakalpojumus pilseta {city}? Nevumo savieno ar parbauditiem vietejiem specialistiem. No tirisanas lidz santehnikas darbiem un profesionalai masazai.",
    "city.seo_p2": "Visus musu platformas specialistus verte isti klienti. Suti bezmaksas pieprasijumu, salimina piedavajumus un izveleties labako savam projektam. Bez slepenajiem maksajumiem.",
    "city.seo_p3": "Vai vajag vienreizeju pakalpojumu vai pastāvīgu atbalstu, musu profesionalu tikls pilseta {city} ir gatavs palidzet.",
    "city.footer_title": "Nevumo — Savienojam ar vietejiem specialistiem",
    "city.footer_in": "pilseta"
}

# ---------------------------------------------------------------------------
# Lithuanian
# ---------------------------------------------------------------------------
LT_DATA = {
    "city.nav_link": "Tapk specialistu",
    "city.hero_title": "Rask paslaugas mieste {city}",
    "city.search_placeholder": "Kokios paslaugos jums reikia?",
    "city.search_btn": "Ieskoti",
    "city.cta_request": "Gauti pasiulymus",
    "city.categories_title": "Populiarios paslaugos mieste {city}",
    "city.cat_cleaning_leads": "Prieinama dabar",
    "city.cat_plumbing_leads": "Prieinama dabar",
    "city.cat_massage_leads": "Prieinama dabar",
    "city.cat_cta": "Perziureti teikejus",
    "city.empty_title": "Nerandati tinkamos paslaugos?",
    "city.empty_subtitle": "Apibudinkit savo uzklausima ir mes jus susiesime su tinkamais specialistais.",
    "city.empty_cta": "Uzsakyti bet kokia paslauga",
    "city.how_title": "Kaip tai veikia",
    "city.how_step_1": "Apibudinkite savo uzklausima",
    "city.how_step_1_sub": "Uztrunka 2 minutes",
    "city.how_step_2": "Gaukite pasiulymus is specialistu",
    "city.how_step_2_sub": "Paprastai per 30 minuciu",
    "city.how_step_3": "Pasirinkite ir susisiekite tiesiogiai",
    "city.how_step_3_sub": "Be komisinių, be tarpininku",
    "city.seo_title": "Paslaugos mieste {city}",
    "city.seo_description": "Ieskote patikimu paslaugu mieste {city}? Nevumo susieja jus su patikrintais vietiniais specialistais. Nuo valymo iki santechnikos ir profesionaliu masazu.",
    "city.seo_p2": "Visi musu platformos specialistai vertinami tikru klientu. Siuskite nemokama uzklausima, palyginkite pasiulymus ir pasirinkite geriausia savo projektui. Be pasleptų mokesciu.",
    "city.seo_p3": "Nesvarbu, ar jums reikia vienkartines paslaugos ar nuolatiines paramos, musu specialistu tinklas mieste {city} yra pasirengis padeti.",
    "city.footer_title": "Nevumo — Susiejame jus su vietiniais specialistais",
    "city.footer_in": "mieste"
}

# ---------------------------------------------------------------------------
# Estonian
# ---------------------------------------------------------------------------
ET_DATA = {
    "city.nav_link": "Saa spetsialistiks",
    "city.hero_title": "Leia teenuseid linnas {city}",
    "city.search_placeholder": "Millist teenust vajad?",
    "city.search_btn": "Otsi",
    "city.cta_request": "Saa pakkumisi",
    "city.categories_title": "Populaarsed teenused linnas {city}",
    "city.cat_cleaning_leads": "Saadaval kohe",
    "city.cat_plumbing_leads": "Saadaval kohe",
    "city.cat_massage_leads": "Saadaval kohe",
    "city.cat_cta": "Vaata pakkujaid",
    "city.empty_title": "Ei leia sobivat teenust?",
    "city.empty_subtitle": "Kirjelda oma vajadust ja me uhendame sind oigete spetsialistidega.",
    "city.empty_cta": "Kusi mis tahes teenust",
    "city.how_title": "Kuidas see toimib",
    "city.how_step_1": "Kirjelda oma vajadust",
    "city.how_step_1_sub": "Votab 2 minutit",
    "city.how_step_2": "Saa pakkumisi spetsialistidelt",
    "city.how_step_2_sub": "Tavaliselt 30 minuti jooksul",
    "city.how_step_3": "Vali ja vota otse uhendust",
    "city.how_step_3_sub": "Ilma vahendustasuta, ilma vahendajateta",
    "city.seo_title": "Teenused linnas {city}",
    "city.seo_description": "Otsid usaldusväärseid teenuseid linnas {city}? Nevumo uhendab sind kontrollitud kohalike spetsialistidega. Koristamisest torustikutoödeni ja professionaalsete massaazideni.",
    "city.seo_p2": "Koiki meie platvormi spetsialiste hindavad päris kliendid. Saada tasuta paring, vorrdle pakkumisi ja vali parim oma projekti jaoks. Peidetud tasusid ei ole.",
    "city.seo_p3": "Kas vajad uhekordset teenust voi pidevat tuge, meie professionaalide vorgustik linnas {city} on valmis aitama.",
    "city.footer_title": "Nevumo — Uhendame sind kohalike spetsialistidega",
    "city.footer_in": "linnas"
}

# ---------------------------------------------------------------------------
# Finnish
# ---------------------------------------------------------------------------
FI_DATA = {
    "city.nav_link": "Tule asiantuntijaksi",
    "city.hero_title": "Loyda palveluita kaupungissa {city}",
    "city.search_placeholder": "Mita palvelua tarvitset?",
    "city.search_btn": "Etsi",
    "city.cta_request": "Saa tarjouksia",
    "city.categories_title": "Suosittuja palveluita kaupungissa {city}",
    "city.cat_cleaning_leads": "Saatavilla nyt",
    "city.cat_plumbing_leads": "Saatavilla nyt",
    "city.cat_massage_leads": "Saatavilla nyt",
    "city.cat_cta": "Katso palveluntarjoajat",
    "city.empty_title": "Etkö loyda oikeaa palvelua?",
    "city.empty_subtitle": "Kuvaile pyyntosi ja yhdistamme sinut oikeiden asiantuntijoiden kanssa.",
    "city.empty_cta": "Pyydä mita tahansa palvelua",
    "city.how_title": "Kuinka se toimii",
    "city.how_step_1": "Kuvaile pyyntosi",
    "city.how_step_1_sub": "Kestaa 2 minuuttia",
    "city.how_step_2": "Saa tarjouksia asiantuntijoilta",
    "city.how_step_2_sub": "Yleensa 30 minuutin sisalla",
    "city.how_step_3": "Valitse ja ota yhteytta suoraan",
    "city.how_step_3_sub": "Ei provisioita, ei vakasia",
    "city.seo_title": "Palvelut kaupungissa {city}",
    "city.seo_description": "Etsitkö luotettavia palveluita kaupungissa {city}? Nevumo yhdistaa sinut tarkistettuihin paikallisiin asiantuntijoihin. Siivouksesta putkitoihin ja ammattimassaaseihin.",
    "city.seo_p2": "Kaikki asiantuntijamme arvioidaan oikeilla asiakkailla. Laheta ilmainen pyynto, vertaile tarjouksia ja valitse paras projektillesi. Ei piilomaksuja.",
    "city.seo_p3": "Tarvitsetpa kertaluonteisen palvelun tai jatkuvan tuen, asiantuntijaverkostomme kaupungissa {city} on valmis auttamaan.",
    "city.footer_title": "Nevumo — Yhdistamme sinut paikallisiin asiantuntijoihin",
    "city.footer_in": "kaupungissa"
}

# ---------------------------------------------------------------------------
# Swedish
# ---------------------------------------------------------------------------
SV_DATA = {
    "city.nav_link": "Bli specialist",
    "city.hero_title": "Hitta tjanster i {city}",
    "city.search_placeholder": "Vilken tjanst behover du?",
    "city.search_btn": "Sok",
    "city.cta_request": "Ta emot erbjudanden",
    "city.categories_title": "Populara tjanster i {city}",
    "city.cat_cleaning_leads": "Tillganglig nu",
    "city.cat_plumbing_leads": "Tillganglig nu",
    "city.cat_massage_leads": "Tillganglig nu",
    "city.cat_cta": "Se leverantorer",
    "city.empty_title": "Hittar du inte ratt tjanst?",
    "city.empty_subtitle": "Beskriv din forfragan sa satter vi dig i kontakt med ratt specialister.",
    "city.empty_cta": "Begar vilken tjanst som helst",
    "city.how_title": "Sa har fungerar det",
    "city.how_step_1": "Beskriv din forfragan",
    "city.how_step_1_sub": "Tar 2 minuter",
    "city.how_step_2": "Ta emot erbjudanden fran specialister",
    "city.how_step_2_sub": "Vanligtvis inom 30 minuter",
    "city.how_step_3": "Valj och kontakta direkt",
    "city.how_step_3_sub": "Ingen provision, inga mellanhander",
    "city.seo_title": "Tjanster i {city}",
    "city.seo_description": "Letar du efter palitliga tjanster i {city}? Nevumo kopplar dig med verifierade lokala specialister. Fran stadning till rorlaggeri och professionella massager.",
    "city.seo_p2": "Alla specialister pa var plattform bedoms av riktiga kunder. Skicka en gratis forfragan, jamfor erbjudanden och valj det basta for ditt projekt. Inga dolda avgifter.",
    "city.seo_p3": "Oavsett om du behover en engangstjanst eller lopande stod ar vart natverk av proffs i {city} redo att hjalpa.",
    "city.footer_title": "Nevumo — Vi kopplar dig med lokala specialister",
    "city.footer_in": "i"
}

# ---------------------------------------------------------------------------
# Danish
# ---------------------------------------------------------------------------
DA_DATA = {
    "city.nav_link": "Bliv specialist",
    "city.hero_title": "Find tjenester i {city}",
    "city.search_placeholder": "Hvilken tjeneste har du brug for?",
    "city.search_btn": "Sog",
    "city.cta_request": "Modtag tilbud",
    "city.categories_title": "Populaere tjenester i {city}",
    "city.cat_cleaning_leads": "Tilgaengelig nu",
    "city.cat_plumbing_leads": "Tilgaengelig nu",
    "city.cat_massage_leads": "Tilgaengelig nu",
    "city.cat_cta": "Se udbydere",
    "city.empty_title": "Kan du ikke finde den rigtige tjeneste?",
    "city.empty_subtitle": "Beskriv din anmodning, og vi saetter dig i forbindelse med de rette specialister.",
    "city.empty_cta": "Anmod om en hvilken som helst tjeneste",
    "city.how_title": "Sadan fungerer det",
    "city.how_step_1": "Beskriv din anmodning",
    "city.how_step_1_sub": "Tager 2 minutter",
    "city.how_step_2": "Modtag tilbud fra specialister",
    "city.how_step_2_sub": "Normalt inden for 30 minutter",
    "city.how_step_3": "Vaelg og kontakt direkte",
    "city.how_step_3_sub": "Ingen provision, ingen mellemaend",
    "city.seo_title": "Tjenester i {city}",
    "city.seo_description": "Leder du efter pålidelige tjenester i {city}? Nevumo forbinder dig med verificerede lokale specialister. Fra rengoring til VVS og professionelle massager.",
    "city.seo_p2": "Alle specialister pa vores platform vurderes af rigtige kunder. Send en gratis anmodning, sammenlign tilbud og vaelg det bedste til dit projekt. Ingen skjulte gebyrer.",
    "city.seo_p3": "Uanset om du har brug for en engangsydelse eller lobende support, er vores netvaerk af fagfolk i {city} klar til at hjaelpe.",
    "city.footer_title": "Nevumo — Vi forbinder dig med lokale specialister",
    "city.footer_in": "i"
}

# ---------------------------------------------------------------------------
# Norwegian
# ---------------------------------------------------------------------------
NO_DATA = {
    "city.nav_link": "Bli spesialist",
    "city.hero_title": "Finn tjenester i {city}",
    "city.search_placeholder": "Hvilken tjeneste trenger du?",
    "city.search_btn": "Sok",
    "city.cta_request": "Motta tilbud",
    "city.categories_title": "Populaere tjenester i {city}",
    "city.cat_cleaning_leads": "Tilgjengelig na",
    "city.cat_plumbing_leads": "Tilgjengelig na",
    "city.cat_massage_leads": "Tilgjengelig na",
    "city.cat_cta": "Se leverandorer",
    "city.empty_title": "Finner du ikke riktig tjeneste?",
    "city.empty_subtitle": "Beskriv din forespørsel, og vi setter deg i kontakt med de rette spesialistene.",
    "city.empty_cta": "Forespørsel om en hvilken som helst tjeneste",
    "city.how_title": "Slik fungerer det",
    "city.how_step_1": "Beskriv din forespørsel",
    "city.how_step_1_sub": "Tar 2 minutter",
    "city.how_step_2": "Motta tilbud fra spesialister",
    "city.how_step_2_sub": "Vanligvis innen 30 minutter",
    "city.how_step_3": "Velg og koble til direkte",
    "city.how_step_3_sub": "Ingen provisjon, ingen mellommenn",
    "city.seo_title": "Tjenester i {city}",
    "city.seo_description": "Leter du etter palitelige tjenester i {city}? Nevumo kobler deg med verifiserte lokale spesialister. Fra rengjøring til rorleggerarbeid og profesjonelle massasjer.",
    "city.seo_p2": "Alle spesialister pa plattformen var vurderes av ekte kunder. Send en gratis forespørsel, sammenlign tilbud og velg det beste for prosjektet ditt. Ingen skjulte gebyrer.",
    "city.seo_p3": "Enten du trenger en engangsytelse eller lopende stotte, er vart nettverk av fagfolk i {city} klar til a hjelpe.",
    "city.footer_title": "Nevumo — Vi kobler deg med lokale spesialister",
    "city.footer_in": "i"
}

# ---------------------------------------------------------------------------
# Icelandic
# ---------------------------------------------------------------------------
IS_DATA = {
    "city.nav_link": "Verddu serfraedingur",
    "city.hero_title": "Finndu tjonustur i {city}",
    "city.search_placeholder": "Hvaða tjonustu tharf tho?",
    "city.search_btn": "Leita",
    "city.cta_request": "Fa tilbod",
    "city.categories_title": "Vinsaalar tjonustur i {city}",
    "city.cat_cleaning_leads": "I bodi nuna",
    "city.cat_plumbing_leads": "I bodi nuna",
    "city.cat_massage_leads": "I bodi nuna",
    "city.cat_cta": "Sja tjonustuadila",
    "city.empty_title": "Finnstur ekki rettu tjonustuna?",
    "city.empty_subtitle": "Lystu beidni thinni og vid munum tengja thig vid rettu serfraedingana.",
    "city.empty_cta": "Bidja um hvaða tjonustu sem er",
    "city.how_title": "Hvernig tad virkar",
    "city.how_step_1": "Lystu beidni thinni",
    "city.how_step_1_sub": "Tekur 2 minutur",
    "city.how_step_2": "Faðu tilbod fra serfraedingum",
    "city.how_step_2_sub": "Venjulega innan 30 minutna",
    "city.how_step_3": "Veldu og tengstu beint",
    "city.how_step_3_sub": "Engin thoknun, engir millilidad",
    "city.seo_title": "Tjonustur i {city}",
    "city.seo_description": "Ertu ad leita ad areidanlegri tjonustu i {city}? Nevumo tengir thig vid stadfestar stadbaednar serfraedingar. Fra thrif til pipu og faglegs nudds.",
    "city.seo_p2": "Allir serfraedingar a vetvangi okkar eru metnir af raunverulegum vidskiptavinum. Sendu okeypis beidni, berdhu saman tilbod og veldu tad besta fyrir verkefni thitt.",
    "city.seo_p3": "Hvort sem thu tharf einskiptistjonustu eda reglulegan studning, er fagmannanet okkar i {city} tilbuid ad hjalpa.",
    "city.footer_title": "Nevumo — Vid tengum thig vid stadbaednar serfraedingar",
    "city.footer_in": "i"
}

# ---------------------------------------------------------------------------
# Luxembourgish
# ---------------------------------------------------------------------------
LB_DATA = {
    "city.nav_link": "Spezialist ginn",
    "city.hero_title": "Servicer fannen zu {city}",
    "city.search_placeholder": "Wat fir e Service brauche Sie?",
    "city.search_btn": "Sichen",
    "city.cta_request": "Offeren kréien",
    "city.categories_title": "Populaer Servicer zu {city}",
    "city.cat_cleaning_leads": "Elo verfügbar",
    "city.cat_plumbing_leads": "Elo verfügbar",
    "city.cat_massage_leads": "Elo verfügbar",
    "city.cat_cta": "Ubidder weisen",
    "city.empty_title": "Den richtege Service net fonnt?",
    "city.empty_subtitle": "Beschreift Ar Ufro an mir verbannen Iech mat de richtege Spezialisten.",
    "city.empty_cta": "All Service ufroe",
    "city.how_title": "Wei et fonctionéiert",
    "city.how_step_1": "Är Ufro beschreiwen",
    "city.how_step_1_sub": "Dauert 2 Minutten",
    "city.how_step_2": "Offere vun Spezialiste kréien",
    "city.how_step_2_sub": "Normalerweis bannent 30 Minutten",
    "city.how_step_3": "Wiehlt an direkt verbannen",
    "city.how_step_3_sub": "Keng Provisioun, keng Mettler",
    "city.seo_title": "Servicer zu {city}",
    "city.seo_description": "Sicht Dir zouverlasseg Servicer zu {city}? Nevumo verbënnt Iech mat verifizéierte lokale Spezialisten. Vum Botzen bis Installatiounsaarbechten a professionelle Massagen.",
    "city.seo_p2": "All Spezialisten op eisem Plattform ginn vu richtege Clienten evaluéiert. Schéckt eng gratis Ufro, vergläicht Offeren a wiehlt déi Bescht fir Äre Projet. Keng verstoppten Tauxen.",
    "city.seo_p3": "Egal ob Dir eng eemolege Prestatioun oder lafend Support braucht, eist Netzwierk vun Professionellen zu {city} ass prett fir ze hëllefen.",
    "city.footer_title": "Nevumo — Mir verbannen Iech mat lokale Spezialisten",
    "city.footer_in": "zu"
}

# ---------------------------------------------------------------------------
# Irish
# ---------------------------------------------------------------------------
GA_DATA = {
    "city.nav_link": "Bi i do speisialtoir",
    "city.hero_title": "Aimsigh seirbhisi i {city}",
    "city.search_placeholder": "Cen tseirbhis ata uait?",
    "city.search_btn": "Cuardaigh",
    "city.cta_request": "Faigh tairiscinti",
    "city.categories_title": "Seirbhisi coitianta i {city}",
    "city.cat_cleaning_leads": "Ar fail anois",
    "city.cat_plumbing_leads": "Ar fail anois",
    "city.cat_massage_leads": "Ar fail anois",
    "city.cat_cta": "Feach ar sholathraigh",
    "city.empty_title": "Ni feidir leat an tseirbhis cheart a fail?",
    "city.empty_subtitle": "Dean cur sios ar do iarratas agus cuirfimid i dteagmhail leis na speisialtoirs cearta thu.",
    "city.empty_cta": "Iarr aon tseirbhis",
    "city.how_title": "Conas a oibrionn se",
    "city.how_step_1": "Dean cur sios ar do iarratas",
    "city.how_step_1_sub": "Togann se 2 noimead",
    "city.how_step_2": "Faigh tairiscinti o speisialtoirs",
    "city.how_step_2_sub": "De ghnath laistigh de 30 noimead",
    "city.how_step_3": "Roghnaigh agus ceangail go direach",
    "city.how_step_3_sub": "Gan coimisiun, gan idirghabhalaigh",
    "city.seo_title": "Seirbhisi i {city}",
    "city.seo_description": "Ag lorg seirbhisi iontaofa i {city}? Ceanglaionn Nevumo thu le speisialtoirs aitiula fioraithe. O ghlanadh go pluimeireacht agus massaigh ghairmiula.",
    "city.seo_p2": "Meastar gach speisialtoir ar ar n-ardan ag custaimers fiora. Seol iarratas saor in aisce, cuir moltai i gcomparaid agus roghnaigh an ceann is fearr don togra. Gan taillte i bhfolach.",
    "city.seo_p3": "Cibe an bhfuil seirbhis aon uaire no tacaiocht leanunach uait, ta ar lionra gairmiuil i {city} reidi chun cabhrú.",
    "city.footer_title": "Nevumo — Ceanglaimimid thu le speisialtoirs aitiula",
    "city.footer_in": "i"
}

# ---------------------------------------------------------------------------
# Maltese
# ---------------------------------------------------------------------------
MT_DATA = {
    "city.nav_link": "Isir specjalista",
    "city.hero_title": "Sib servizzi f'{city}",
    "city.search_placeholder": "Liema servizz tehtiég?",
    "city.search_btn": "Fittex",
    "city.cta_request": "Ircievi offerti",
    "city.categories_title": "Servizzi popolari f'{city}",
    "city.cat_cleaning_leads": "Disponibbli issa",
    "city.cat_plumbing_leads": "Disponibbli issa",
    "city.cat_massage_leads": "Disponibbli issa",
    "city.cat_cta": "Ara l-fornituri",
    "city.empty_title": "Ma tistax issib is-servizz it-tajjeb?",
    "city.empty_subtitle": "Iddeskrivi t-talba tieghek u se nqabbduk mas-specjalisti t-tajbin.",
    "city.empty_cta": "Itlob kwalunkwe servizz",
    "city.how_title": "Kif jahdem",
    "city.how_step_1": "Iddeskrivi t-talba tieghek",
    "city.how_step_1_sub": "Jiehdu 2 minuti",
    "city.how_step_2": "Ircievi offerti minn specjalisti",
    "city.how_step_2_sub": "Normalment fi zmien 30 minuta",
    "city.how_step_3": "Aghzel u qabbad direttament",
    "city.how_step_3_sub": "Ebda kummissjoni, ebda intermediarji",
    "city.seo_title": "Servizzi f'{city}",
    "city.seo_description": "Qieghed tfittex servizzi affidabbli f'{city}? Nevumo jqabbdek ma specjalisti lokali vverifikati. Mill-indaf sal-idrawlika u massaggi professjonali.",
    "city.seo_p2": "Il-specjalisti kollha fuq il-pjattaforma taghna huma evalwati minn klijenti reali. Ibghat talba b'xejn, iqabbel l-offerti u aghzel l-ahjar ghall-progett tieghek. L-ebda tariffi mohbija.",
    "city.seo_p3": "Kemm jekk tehtiég servizz ta' darba kif ukoll appogg kontinwu, in-netwerk ta' professjonisti taghna f'{city} huwa lest jghinek.",
    "city.footer_title": "Nevumo — Nqabbduk ma specjalisti lokali",
    "city.footer_in": "f'"
}

# ---------------------------------------------------------------------------
# Master translations map
# ---------------------------------------------------------------------------
TRANSLATIONS = {
    'en':    EN_DATA,
    'bg':    BG_DATA,
    'pl':    PL_DATA,
    'de':    DE_DATA,
    'fr':    FR_DATA,
    'es':    ES_DATA,
    'it':    IT_DATA,
    'nl':    NL_DATA,
    'pt':    PT_DATA,
    'pt-PT': PT_PT_DATA,
    'ro':    RO_DATA,
    'cs':    CS_DATA,
    'sk':    SK_DATA,
    'hu':    HU_DATA,
    'hr':    HR_DATA,
    'sl':    SL_DATA,
    'sr':    SR_DATA,
    'mk':    MK_DATA,
    'sq':    SQ_DATA,
    'el':    EL_DATA,
    'tr':    TR_DATA,
    'ru':    RU_DATA,
    'uk':    UK_DATA,
    'lv':    LV_DATA,
    'lt':    LT_DATA,
    'et':    ET_DATA,
    'fi':    FI_DATA,
    'sv':    SV_DATA,
    'da':    DA_DATA,
    'no':    NO_DATA,
    'is':    IS_DATA,
    'lb':    LB_DATA,
    'ga':    GA_DATA,
    'mt':    MT_DATA,
}


def main() -> None:
    db = SessionLocal()
    try:
        count = 0
        for lang in LANGUAGES:
            data = TRANSLATIONS.get(lang, EN_DATA)  # EN fallback (safety net)
            for key, value in data.items():
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
        print(f"Successfully seeded {count} translation rows for 'city' namespace.")

        # Verification — expected: 26 keys x 34 languages = 884 rows
        result = db.execute(
            text("SELECT lang, COUNT(*) AS cnt FROM translations WHERE key LIKE 'city.%' GROUP BY lang ORDER BY lang")
        )
        print("\nVerification (keys per language):")
        total = 0
        for row in result:
            print(f"  {row[0]}: {row[1]}")
            total += row[1]
        print(f"\nTotal city.* rows in DB: {total}")

    except Exception as e:
        db.rollback()
        print(f"Error seeding translations: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()