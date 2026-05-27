from apps.api.database import SessionLocal
from sqlalchemy import text

def seed():
    db = SessionLocal()
    try:
        rows = [
            ('en', 'provider_dashboard.msg_failed_load_widget', 'Failed to load widget data'),
            ('en', 'provider_dashboard.msg_no_widget_data', 'No widget data available'),
            ('bg', 'provider_dashboard.msg_failed_load_widget', 'Грешка при зареждане на widget данните'),
            ('bg', 'provider_dashboard.msg_no_widget_data', 'Няма налични widget данни'),
            ('pl', 'provider_dashboard.msg_failed_load_widget', 'Nie udało się załadować danych widgetu'),
            ('pl', 'provider_dashboard.msg_no_widget_data', 'Brak dostępnych danych widgetu'),
            ('de', 'provider_dashboard.msg_failed_load_widget', 'Widget-Daten konnten nicht geladen werden'),
            ('de', 'provider_dashboard.msg_no_widget_data', 'Keine Widget-Daten verfügbar'),
            ('fr', 'provider_dashboard.msg_failed_load_widget', 'Échec du chargement des données du widget'),
            ('fr', 'provider_dashboard.msg_no_widget_data', 'Aucune donnée de widget disponible'),
            ('es', 'provider_dashboard.msg_failed_load_widget', 'Error al cargar los datos del widget'),
            ('es', 'provider_dashboard.msg_no_widget_data', 'No hay datos de widget disponibles'),
            ('it', 'provider_dashboard.msg_failed_load_widget', 'Impossibile caricare i dati del widget'),
            ('it', 'provider_dashboard.msg_no_widget_data', 'Nessun dato widget disponibile'),
            ('pt', 'provider_dashboard.msg_failed_load_widget', 'Falha ao carregar dados do widget'),
            ('pt', 'provider_dashboard.msg_no_widget_data', 'Nenhum dado de widget disponível'),
            ('pt-PT', 'provider_dashboard.msg_failed_load_widget', 'Falha ao carregar dados do widget'),
            ('pt-PT', 'provider_dashboard.msg_no_widget_data', 'Sem dados de widget disponíveis'),
            ('nl', 'provider_dashboard.msg_failed_load_widget', 'Widgetgegevens konden niet worden geladen'),
            ('nl', 'provider_dashboard.msg_no_widget_data', 'Geen widgetgegevens beschikbaar'),
            ('cs', 'provider_dashboard.msg_failed_load_widget', 'Nepodařilo se načíst data widgetu'),
            ('cs', 'provider_dashboard.msg_no_widget_data', 'Žádná data widgetu nejsou k dispozici'),
            ('sk', 'provider_dashboard.msg_failed_load_widget', 'Nepodarilo sa načítať dáta widgetu'),
            ('sk', 'provider_dashboard.msg_no_widget_data', 'Žiadne dáta widgetu nie sú k dispozícii'),
            ('ro', 'provider_dashboard.msg_failed_load_widget', 'Eroare la încărcarea datelor widget'),
            ('ro', 'provider_dashboard.msg_no_widget_data', 'Nu sunt disponibile date widget'),
            ('hu', 'provider_dashboard.msg_failed_load_widget', 'A widget adatok betöltése sikertelen'),
            ('hu', 'provider_dashboard.msg_no_widget_data', 'Nem állnak rendelkezésre widget adatok'),
            ('hr', 'provider_dashboard.msg_failed_load_widget', 'Nije uspjelo učitavanje podataka widgeta'),
            ('hr', 'provider_dashboard.msg_no_widget_data', 'Nema dostupnih podataka widgeta'),
            ('sl', 'provider_dashboard.msg_failed_load_widget', 'Nalaganje podatkov gradnika ni uspelo'),
            ('sl', 'provider_dashboard.msg_no_widget_data', 'Ni razpoložljivih podatkov gradnika'),
            ('da', 'provider_dashboard.msg_failed_load_widget', 'Kunne ikke indlæse widget-data'),
            ('da', 'provider_dashboard.msg_no_widget_data', 'Ingen widget-data tilgængelige'),
            ('sv', 'provider_dashboard.msg_failed_load_widget', 'Det gick inte att läsa in widgetdata'),
            ('sv', 'provider_dashboard.msg_no_widget_data', 'Inga widgetdata tillgängliga'),
            ('no', 'provider_dashboard.msg_failed_load_widget', 'Kunne ikke laste inn widget-data'),
            ('no', 'provider_dashboard.msg_no_widget_data', 'Ingen widget-data tilgjengelig'),
            ('fi', 'provider_dashboard.msg_failed_load_widget', 'Widgetin tietojen lataaminen epäonnistui'),
            ('fi', 'provider_dashboard.msg_no_widget_data', 'Ei widget-tietoja saatavilla'),
            ('et', 'provider_dashboard.msg_failed_load_widget', 'Vidina andmete laadimine ebaõnnestus'),
            ('et', 'provider_dashboard.msg_no_widget_data', 'Vidina andmed pole saadaval'),
            ('lv', 'provider_dashboard.msg_failed_load_widget', 'Neizdevās ielādēt logrīka datus'),
            ('lv', 'provider_dashboard.msg_no_widget_data', 'Nav pieejamu logrīka datu'),
            ('lt', 'provider_dashboard.msg_failed_load_widget', 'Nepavyko įkelti valdiklio duomenų'),
            ('lt', 'provider_dashboard.msg_no_widget_data', 'Nėra galimų valdiklio duomenų'),
            ('el', 'provider_dashboard.msg_failed_load_widget', 'Αποτυχία φόρτωσης δεδομένων widget'),
            ('el', 'provider_dashboard.msg_no_widget_data', 'Δεν υπάρχουν διαθέσιμα δεδομένα widget'),
            ('ru', 'provider_dashboard.msg_failed_load_widget', 'Не удалось загрузить данные виджета'),
            ('ru', 'provider_dashboard.msg_no_widget_data', 'Данные виджета недоступны'),
            ('uk', 'provider_dashboard.msg_failed_load_widget', 'Не вдалося завантажити дані віджета'),
            ('uk', 'provider_dashboard.msg_no_widget_data', 'Дані віджета недоступні'),
            ('sr', 'provider_dashboard.msg_failed_load_widget', 'Nije uspelo učitavanje podataka widgeta'),
            ('sr', 'provider_dashboard.msg_no_widget_data', 'Nema dostupnih podataka widgeta'),
            ('mk', 'provider_dashboard.msg_failed_load_widget', 'Неуспешно вчитување на податоците на виџетот'),
            ('mk', 'provider_dashboard.msg_no_widget_data', 'Нема достапни податоци за виџетот'),
            ('sq', 'provider_dashboard.msg_failed_load_widget', 'Dështoi ngarkimi i të dhënave të widget'),
            ('sq', 'provider_dashboard.msg_no_widget_data', 'Nuk ka të dhëna widget të disponueshme'),
            ('ga', 'provider_dashboard.msg_failed_load_widget', 'Theip ar lódáil sonraí an ghiuirléid'),
            ('ga', 'provider_dashboard.msg_no_widget_data', 'Níl sonraí giuirléide ar fáil'),
            ('is', 'provider_dashboard.msg_failed_load_widget', 'Mistókst að hlaða widget gögnum'),
            ('is', 'provider_dashboard.msg_no_widget_data', 'Engin widget gögn tiltæk'),
            ('lb', 'provider_dashboard.msg_failed_load_widget', 'Widget-Daten konnten net gelueden ginn'),
            ('lb', 'provider_dashboard.msg_no_widget_data', 'Keng Widget-Daten verfügbar'),
            ('mt', 'provider_dashboard.msg_failed_load_widget', 'Falliment fil-tagħbija tad-dejta tal-widget'),
            ('mt', 'provider_dashboard.msg_no_widget_data', 'L-ebda dejta tal-widget mhix disponibbli'),
            ('tr', 'provider_dashboard.msg_failed_load_widget', 'Widget verileri yüklenemedi'),
            ('tr', 'provider_dashboard.msg_no_widget_data', 'Widget verisi mevcut değil'),
        ]
        for lang, key, value in rows:
            db.execute(text("""
                INSERT INTO translations (lang, key, value)
                VALUES (:lang, :key, :value)
                ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
            """), {"lang": lang, "key": key, "value": value})
        db.commit()
        print(f"Seeded {len(rows)} rows.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
