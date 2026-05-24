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
        WHERE key LIKE 'privacy.%'
        GROUP BY lang
        ORDER BY lang
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} keys")

ALL_TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "privacy.section_7_title": "7. Automated Processing",
        "privacy.section_7_intro": "Nevumo uses automated processing of provider data in two systems. Neither system produces legal effects, but both may significantly affect a provider's commercial visibility on the Platform.",
        "privacy.section_7_1_title": "7.1 Provider Ranking",
        "privacy.section_7_1_body": "When displaying providers in search results and category listings, Nevumo's platform automatically calculates each provider's position based on the following parameters: profile completeness, average client rating, response rate and speed, recent activity, geographic match to the client's city, and account standing. No payment influences organic ranking position. Full details of the ranking parameters and their relative weights are published in the Provider Terms, Section 5.",
        "privacy.section_7_2_title": "7.2 Provider Status Badge",
        "privacy.section_7_2_body": "Nevumo automatically calculates a status badge for each provider profile (New Provider / Verified Specialist / Top Specialist) based on measurable platform activity data: number of completed service requests, average client rating, and profile completeness (photo, description, active service listing). The badge is recalculated in real time upon any change to the underlying data and is displayed publicly on the provider's profile. Criteria are fully transparent and published in the Provider Terms, Section 5. Providers can influence their badge at any time by completing service requests and maintaining a complete profile.",
        "privacy.section_7_3_title": "7.3 Payment Fraud Detection (Stripe)",
        "privacy.section_7_3_body": "When processing payments, Stripe uses automated fraud detection. You have the right to request human review of any automated decision by Stripe that significantly affects you.",
        "privacy.section_7_note": "These systems apply to provider accounts only. Client accounts are not subject to automated ranking or badge processing.",
        "privacy.section_7_legal_basis_label": "Legal basis:",
        "privacy.t32_performance_data": "Performance indicators (completed jobs count, average rating, verification level)",
        "privacy.t32_performance_purpose": "Automatic calculation of ranking position and public status badge",
    },
    "bg": {
        "privacy.section_7_title": "7. Автоматизирано обработване",
        "privacy.section_7_intro": "Nevumo прилага автоматизирано обработване на данни на Доставчиците в две системи. Нито една от тях не произвежда правни последици, но и двете могат значително да засегнат търговската видимост на Доставчика в Платформата.",
        "privacy.section_7_1_title": "7.1 Класиране на Доставчиците",
        "privacy.section_7_1_body": "При показване на Доставчиците в резултатите от търсенето и в листингите по категории Платформата автоматично изчислява позицията на всеки Доставчик въз основа на следните параметри: пълнота на профила, средна оценка от клиенти, степен и скорост на отговор, скорошна активност в Платформата, географско съответствие с града на клиента и статус на акаунта. Плащането не влияе на органичната позиция в класирането. Пълна информация за параметрите за класиране и относителните им тежести е публикувана в Условията за Доставчици, чл. 5.",
        "privacy.section_7_2_title": "7.2 Значка за статус на Доставчика",
        "privacy.section_7_2_body": "Nevumo автоматично изчислява значка за статус за всеки профил на Доставчик (Нов Доставчик / Верифициран специалист / Топ специалист) въз основа на измерими данни за активност: брой завършени запитвания, средна оценка от клиенти и пълнота на профила (снимка, описание, активна обява за услуга). Значката се преизчислява в реално време при всяка промяна на изходните данни и се показва публично в профила на Доставчика. Критериите са напълно прозрачни и публикувани в Условията за Доставчици, чл. 5. Доставчикът може по всяко време да повлияе на своята значка, като изпълнява запитвания и поддържа попълнен профил.",
        "privacy.section_7_3_title": "7.3 Засичане на платежни измами (Stripe)",
        "privacy.section_7_3_body": "При обработка на плащания Stripe използва автоматизирано засичане на измами. Имате право да поискате намеса на човек при всяко автоматизирано решение на Stripe, което ви засяга съществено.",
        "privacy.section_7_note": "Тези системи се отнасят само за акаунти на Доставчици. Акаунтите на Клиенти не подлежат на автоматизирано класиране или присвояване на значки.",
        "privacy.section_7_legal_basis_label": "Правно основание:",
        "privacy.t32_performance_data": "Показатели за активност (брой завършени запитвания, средна оценка, ниво на верификация)",
        "privacy.t32_performance_purpose": "Автоматично изчисляване на позицията в класирането и значката за статус",
    },
    "pl": {
        "privacy.section_7_title": "7. Zautomatyzowane przetwarzanie",
        "privacy.section_7_intro": "Nevumo stosuje zautomatyzowane przetwarzanie danych Dostawców w dwóch systemach. Żaden z nich nie wywołuje skutków prawnych, jednak oba mogą znacząco wpływać na widoczność handlową Dostawcy na Platformie.",
        "privacy.section_7_1_title": "7.1 Ranking Dostawców",
        "privacy.section_7_1_body": "Przy wyświetlaniu Dostawców w wynikach wyszukiwania i listingach kategorii Platforma automatycznie oblicza pozycję każdego Dostawcy na podstawie następujących parametrów: kompletność profilu, średnia ocena klientów, wskaźnik i szybkość odpowiedzi, aktywność na Platformie, dopasowanie geograficzne do miasta klienta oraz status konta. Płatność nie wpływa na organiczną pozycję w rankingu. Pełne informacje o parametrach rankingowych i ich względnych wagach są opublikowane w Regulaminie Dostawców, §5.",
        "privacy.section_7_2_title": "7.2 Odznaka statusu Dostawcy",
        "privacy.section_7_2_body": "Nevumo automatycznie oblicza odznakę statusu dla każdego profilu Dostawcy (Nowy Dostawca / Zweryfikowany Specjalista / Najlepszy Specjalista) na podstawie mierzalnych danych aktywności: liczby ukończonych zleceń, średniej oceny klientów oraz kompletności profilu (zdjęcie, opis, aktywna oferta usługi). Odznaka jest przeliczana w czasie rzeczywistym przy każdej zmianie danych źródłowych i wyświetlana publicznie na profilu Dostawcy. Kryteria są w pełni przejrzyste i opublikowane w Regulaminie Dostawców, §5. Dostawca może wpływać na swoją odznakę w dowolnym momencie, realizując zlecenia i uzupełniając profil.",
        "privacy.section_7_3_title": "7.3 Wykrywanie oszustw płatniczych (Stripe)",
        "privacy.section_7_3_body": "Stripe stosuje automatyczne wykrywanie oszustw przy płatnościach. Masz prawo żądać interwencji człowieka w przypadku zautomatyzowanej decyzji Stripe, która istotnie Cię dotyczy.",
        "privacy.section_7_note": "Systemy te dotyczą wyłącznie kont Dostawców. Konta Klientów nie podlegają zautomatyzowanemu rankingowi ani przyznawaniu odznak.",
        "privacy.section_7_legal_basis_label": "Podstawa prawna:",
        "privacy.t32_performance_data": "Wskaźniki aktywności (liczba ukończonych zleceń, średnia ocena, poziom weryfikacji)",
        "privacy.t32_performance_purpose": "Automatyczne obliczanie pozycji w rankingu i odznaki statusu",
    },
}

if __name__ == "__main__":
    main()
