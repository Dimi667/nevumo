from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Custom database URL with port 5433
DATABASE_URL = "postgresql://nevumo:nevumo@localhost:5433/nevumo_leads"

engine = create_engine(
    DATABASE_URL,
    connect_args={"options": "-c client_encoding=utf8"},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def main():
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()

def run_seed(db):
    # Update Sofia city translation
    update_sofia_translation(db)
    
    # Insert FAQ translations
    insert_translations(db, FAQ_TRANSLATIONS)
    
    # Verify
    verify(db)

def update_sofia_translation(db):
    """Find location with slug 'sofia' and update/add Bulgarian translation"""
    result = db.execute(
        text("""
            SELECT id FROM locations WHERE slug = 'sofia'
        """)
    ).fetchone()
    
    if not result:
        print("ERROR: Location with slug 'sofia' not found!")
        return
    
    location_id = result[0]
    print(f"Found location with ID: {location_id}")
    
    # Insert or update Bulgarian translation
    db.execute(
        text("""
            INSERT INTO location_translations (location_id, lang, city_name)
            VALUES (:location_id, 'bg', :city_name)
            ON CONFLICT (location_id, lang)
            DO UPDATE SET city_name = EXCLUDED.city_name
        """),
        {"location_id": location_id, "city_name": "София"}
    )
    db.commit()
    print("Updated Sofia Bulgarian translation to 'София'")

def insert_translations(db, data: list[dict]) -> None:
    """Insert/update FAQ translations for category namespace"""
    count = 0
    for item in data:
        lang = item["lang"]
        translations = item["translations"]
        for key, value in translations.items():
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
    print(f"Inserted/updated {count} FAQ translation rows")

def verify(db) -> None:
    """Verify the inserted translations"""
    print("\n=== Sofia Location Translation ===")
    result = db.execute(
        text("""
            SELECT l.slug, lt.lang, lt.city_name
            FROM locations l
            JOIN location_translations lt ON l.id = lt.location_id
            WHERE l.slug = 'sofia' AND lt.lang = 'bg'
        """)
    ).fetchone()
    if result:
        print(f"  Slug: {result[0]}, Lang: {result[1]}, City Name: {result[2]}")
    else:
        print("  ERROR: No Bulgarian translation found for Sofia")
    
    print("\n=== FAQ Translations by Language ===")
    result = db.execute(
        text("""
            SELECT lang, COUNT(*) as keys
            FROM translations
            WHERE key LIKE 'faq_cleaning_%'
            GROUP BY lang
            ORDER BY lang
        """)
    )
    rows = result.fetchall()
    for row in rows:
        print(f"  {row[0]}: {row[1]} keys")

FAQ_TRANSLATIONS: list[dict] = [
  {"lang": "bg", "translations": {"faq_cleaning_q1": "{category_name} в {city} — какво е важно да знаете?", "faq_cleaning_a1": "Професионални специалисти по {category_name} в {city} предлагат комплексни услуги за домове, апартаменти и офиси. В Nevumo ще намерите проверени професионалисти, налични в цяла {city}.", "faq_cleaning_q2": "Как да изберете специалист по {category_name}?", "faq_cleaning_a2": "При избор на специалист за {category_name} в {city}, обърнете внимание на отзивите, обхвата на услугите и опита на професионалистите.", "faq_cleaning_q3": "Колко струва {category_name} в {city}?", "faq_cleaning_a3": "Цените за {category_name} в {city} се определят от обема работа и започват от {min_price} до {max_price} {currency}. Нашите професионалисти гарантират чистота."}},
  {"lang": "en", "translations": {"faq_cleaning_q1": "{category_name} in {city} — what is worth knowing?", "faq_cleaning_a1": "Professional {category_name} specialists in {city} offer comprehensive services for homes, apartments, and offices. On Nevumo you will find verified professionals available throughout {city}.", "faq_cleaning_q2": "How to choose a {category_name} specialist?", "faq_cleaning_a2": "When choosing a {category_name} specialist in {city}, pay attention to client reviews, scope of services, and the expert's experience.", "faq_cleaning_q3": "How much does {category_name} cost in {city}?", "faq_cleaning_a3": "The price for {category_name} in {city} is determined by the scope of work and ranges from {min_price} to {max_price} {currency}. Our professionals guarantee cleanliness."}},
  {"lang": "de", "translations": {"faq_cleaning_q1": "{category_name} in {city} — was Sie wissen sollten?", "faq_cleaning_a1": "Professionelle {category_name}-Spezialisten in {city} bieten umfassende Dienstleistungen für Häuser, Wohnungen und Büros an. Auf Nevumo finden Sie geprüfte Profis, die in ganz {city} verfügbar sind.", "faq_cleaning_q2": "Wie wählt man einen {category_name}-Spezialisten aus?", "faq_cleaning_a2": "Achten Sie bei der Auswahl eines {category_name}-Spezialisten in {city} auf Kundenbewertungen, den Leistungsumfang und die Erfahrung des Profis.", "faq_cleaning_q3": "Was kostet {category_name} in {city}?", "faq_cleaning_a3": "Die Kosten für {category_name} in {city} hängen vom Arbeitsumfang ab und liegen zwischen {min_price} und {max_price} {currency}. Unsere Profis garantieren Sauberkeit."}},
  {"lang": "fr", "translations": {"faq_cleaning_q1": "{category_name} à {city} — ce qu'il faut savoir ?", "faq_cleaning_a1": "Des spécialistes professionnels du {category_name} à {city} proposent des services complets pour les maisons, appartements et bureaux. Sur Nevumo, vous trouverez des professionnels vérifiés disponibles dans tout {city}.", "faq_cleaning_q2": "Comment choisir un spécialiste en {category_name} ?", "faq_cleaning_a2": "Lors du choix d'un spécialiste en {category_name} à {city}, portez une attention particulière aux avis des clients, à l'étendue des services et à l'expérience.", "faq_cleaning_q3": "Combien coûte le {category_name} à {city} ?", "faq_cleaning_a3": "Les tarifs du {category_name} à {city} sont déterminés par l'ampleur des travaux et varient de {min_price} à {max_price} {currency}. Nos experts garantissent la propreté."}},
  {"lang": "es", "translations": {"faq_cleaning_q1": "{category_name} en {city}: ¿qué es importante saber?", "faq_cleaning_a1": "Especialistas profesionales de {category_name} en {city} ofrecen servicios integrales para hogares, apartamentos y oficinas. En Nevumo encontrará profesionales verificados disponibles en todo {city}.", "faq_cleaning_q2": "¿Cómo elegir un especialista en {category_name}?", "faq_cleaning_a2": "Al elegir un especialista en {category_name} en {city}, preste atención a las opiniones de los clientes, el alcance de los servicios y la experiencia profesional.", "faq_cleaning_q3": "¿Cuánto cuesta el {category_name} en {city}?", "faq_cleaning_a3": "Los precios de {category_name} en {city} se determinan por el volumen de trabajo y oscilan entre {min_price} y {max_price} {currency}. Garantizamos limpieza total."}},
  {"lang": "it", "translations": {"faq_cleaning_q1": "{category_name} a {city} — cosa è importante sapere?", "faq_cleaning_a1": "Specialisti professionisti di {category_name} a {city} offrono servizi completi per case, appartamenti e uffici. Su Nevumo troverai professionisti verificati disponibili in tutta {city}.", "faq_cleaning_q2": "Come scegliere uno specialista in {category_name}?", "faq_cleaning_a2": "Nella scelta di uno specialista in {category_name} a {city}, presta attenzione alle recensioni dei clienti, alla gamma di servizi e all'esperienza.", "faq_cleaning_q3": "Quanto costa il {category_name} a {city}?", "faq_cleaning_a3": "I costi per {category_name} a {city} sono determinati dall'entità del lavoro e vanno da {min_price} a {max_price} {currency}. I nostri esperti garantiscono il pulito."}},
  {"lang": "nl", "translations": {"faq_cleaning_q1": "{category_name} in {city} — wat u moet weten?", "faq_cleaning_a1": "Professionele {category_name}-specialisten in {city} bieden uitgebreide diensten voor huizen, appartementen en kantoren. Op Nevumo vindt u geverifieerde professionals die beschikbaar zijn in heel {city}.", "faq_cleaning_q2": "Hoe kiest u een {category_name}-specialist?", "faq_cleaning_a2": "Let bij het kiezen van een {category_name}-specialist in {city} op klantbeoordelingen, de omvang van de diensten en de ervaring van de expert.", "faq_cleaning_q3": "Wat kost {category_name} in {city}?", "faq_cleaning_a3": "De prijzen voor {category_name} in {city} worden bepaald door de omvang van het werk en liggen tussen {min_price} and {max_price} {currency}."}},
  {"lang": "pl", "translations": {"faq_cleaning_q1": "{category_name} w {city} — co warto wiedzieć?", "faq_cleaning_a1": "Profesjonalni specjaliści od {category_name} w {city} oferują kompleksowe usługi dla domów, mieszkań i biur. Na Nevumo znajdziesz sprawdzonych fachowców dostępnych w całym {city}.", "faq_cleaning_q2": "Jak wybrać specjalistę od {category_name}?", "faq_cleaning_a2": "Wybierając specjalistę od {category_name} w {city}, zwróć uwagę na opinie klientów, zakres usług oraz doświadczenie eksperta.", "faq_cleaning_q3": "Ile kosztuje {category_name} w {city}?", "faq_cleaning_a3": "Ceny za {category_name} w {city} zależą od zakresu prac i wahają się od {min_price} do {max_price} {currency}. Gwarantujemy nieskazitelną czystość."}},
  {"lang": "ro", "translations": {"faq_cleaning_q1": "{category_name} în {city} — ce merită să știi?", "faq_cleaning_a1": "Specialiști profesioniști în {category_name} din {city} oferă servicii complete pentru case, apartamente și birouri. Pe Nevumo veți găsi profesioniști verificați disponibili în tot orașul {city}.", "faq_cleaning_q2": "Cum să alegi un specialist în {category_name}?", "faq_cleaning_a2": "Când alegeți un specialist în {category_name} în {city}, acordați atenție recenziilor, gamei de servicii și experienței profesionale.", "faq_cleaning_q3": "Cât costă {category_name} în {city}?", "faq_cleaning_a3": "Prețurile pentru {category_name} în {city} sunt determinate de volumul de muncă și variază între {min_price} și {max_price} {currency}."}},
  {"lang": "ru", "translations": {"faq_cleaning_q1": "{category_name} в {city} — что важно знать?", "faq_cleaning_a1": "Профессиональные специалисты по {category_name} в {city} предлагают комплексные услуги для домов, квартир и офисов. На Nevumo вы найдете проверенных профи, доступных по всему {city}.", "faq_cleaning_q2": "Как выбрать специалиста по {category_name}?", "faq_cleaning_a2": "При выборе специалиста по {category_name} в {city}, обратите внимание на отзывы клиентов, объем услуг и опыт эксперта.", "faq_cleaning_q3": "Сколько стоит {category_name} в {city}?", "faq_cleaning_a3": "Цены на {category_name} в {city} определяются объемом работ и начинаются от {min_price} до {max_price} {currency}. Наши профи гарантируют чистоту."}},
  {"lang": "tr", "translations": {"faq_cleaning_q1": "{city} içinde {category_name} — bilmeniz gerekenler nelerdir?", "faq_cleaning_a1": "{city} şehrindeki profesyonel {category_name} uzmanları evler, daireler ve ofisler için kapsamlı hizmetler sunmaktadır. Nevumo'da {city} genelinde doğrulanmış profesyoneller bulacaksınız.", "faq_cleaning_q2": "Bir {category_name} uzmanı nasıl seçilir?", "faq_cleaning_a2": "{city} şehrinde bir {category_name} uzmanı seçerken müşteri yorumlarına, hizmet kapsamına ve uzman deneyimine dikkat edin.", "faq_cleaning_q3": "{city} içinde {category_name} maliyeti ne kadar?", "faq_cleaning_a3": "{city} içindeki {category_name} fiyatları iş kapsamına göre belirlenir ve {min_price} ile {max_price} {currency} arasındadır."}},
  {"lang": "uk", "translations": {"faq_cleaning_q1": "{category_name} у {city} — що варто знати?", "faq_cleaning_a1": "Професійні спеціалісти з {category_name} у {city} пропонують комплексні послуги для будинків, квартир та офісів. На Nevumo ви знайдете перевірених фахівців, доступних у всьому {city}.", "faq_cleaning_q2": "Як обрати спеціаліста з {category_name}?", "faq_cleaning_a2": "При виборі спеціаліста з {category_name} у {city} зверніть увагу на відгуки клієнтів, обсяг послуг та досвід фахівця.", "faq_cleaning_q3": "Скільки коштує {category_name} у {city}?", "faq_cleaning_a3": "Ціни на {category_name} у {city} визначаються обсягом робіт і становлять від {min_price} до {max_price} {currency}."}}
]

if __name__ == "__main__":
    main()
