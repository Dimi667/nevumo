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
        WHERE key = 'provider_page.error_service_or_note'
        GROUP BY lang
        ORDER BY lang
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} keys")

ALL_TRANSLATIONS: dict[str, dict[str, str]] = {
  "bg": {
    "provider_page.error_service_or_note": "Моля изберете услуга или напишете бележка",
  },
  "cs": {
    "provider_page.error_service_or_note": "Vyberte prosím službu nebo napište poznámku",
  },
  "da": {
    "provider_page.error_service_or_note": "Vælg venligst en tjeneste eller skriv en note",
  },
  "de": {
    "provider_page.error_service_or_note": "Bitte wählen Sie einen Dienst aus oder schreiben Sie eine Notiz",
  },
  "el": {
    "provider_page.error_service_or_note": "Επιλέξτε υπηρεσία ή γράψτε μια σημείωση",
  },
  "en": {
    "provider_page.error_service_or_note": "Please select a service or write a note",
  },
  "es": {
    "provider_page.error_service_or_note": "Por favor seleccione un servicio o escriba una nota",
  },
  "et": {
    "provider_page.error_service_or_note": "Palun valige teenus või kirjutage märkus",
  },
  "fi": {
    "provider_page.error_service_or_note": "Valitse palvelu tai kirjoita huomautus",
  },
  "fr": {
    "provider_page.error_service_or_note": "Veuillez sélectionner un service ou écrire une note",
  },
  "ga": {
    "provider_page.error_service_or_note": "Roghnaigh seirbhís nó scríobh nóta le do thoil",
  },
  "hr": {
    "provider_page.error_service_or_note": "Molimo odaberite uslugu ili napišite napomenu",
  },
  "hu": {
    "provider_page.error_service_or_note": "Kérjük válasszon szolgáltatást vagy írjon megjegyzést",
  },
  "is": {
    "provider_page.error_service_or_note": "Vinsamlegast veldu þjónustu eða skrifaðu athugasemd",
  },
  "it": {
    "provider_page.error_service_or_note": "Seleziona un servizio o scrivi una nota",
  },
  "lb": {
    "provider_page.error_service_or_note": "Wielt w.e.g. e Service oder schreift eng Notiz",
  },
  "lt": {
    "provider_page.error_service_or_note": "Pasirinkite paslaugą arba parašykite pastabą",
  },
  "lv": {
    "provider_page.error_service_or_note": "Lūdzu izvēlieties pakalpojumu vai uzrakstiet piezīmi",
  },
  "mk": {
    "provider_page.error_service_or_note": "Изберете услуга или напишете белешка",
  },
  "mt": {
    "provider_page.error_service_or_note": "Jekk jogħġbok agħżel servizz jew ikteb nota",
  },
  "nl": {
    "provider_page.error_service_or_note": "Selecteer een dienst of schrijf een notitie",
  },
  "no": {
    "provider_page.error_service_or_note": "Velg en tjeneste eller skriv en merknad",
  },
  "pl": {
    "provider_page.error_service_or_note": "Wybierz usługę lub wpisz notatkę",
  },
  "pt": {
    "provider_page.error_service_or_note": "Por favor selecione um serviço ou escreva uma nota",
  },
  "pt-PT": {
    "provider_page.error_service_or_note": "Por favor selecione um serviço ou escreva uma nota",
  },
  "ro": {
    "provider_page.error_service_or_note": "Vă rugăm selectați un serviciu sau scrieți o notă",
  },
  "ru": {
    "provider_page.error_service_or_note": "Пожалуйста, выберите услугу или напишите заметку",
  },
  "sk": {
    "provider_page.error_service_or_note": "Prosím vyberte službu alebo napíšte poznámku",
  },
  "sl": {
    "provider_page.error_service_or_note": "Izberite storitev ali napišite opombo",
  },
  "sq": {
    "provider_page.error_service_or_note": "Ju lutemi zgjidhni një shërbim ose shkruani një shënim",
  },
  "sr": {
    "provider_page.error_service_or_note": "Молимо изаберите услугу или напишите напомену",
  },
  "sv": {
    "provider_page.error_service_or_note": "Välj en tjänst eller skriv en anteckning",
  },
  "tr": {
    "provider_page.error_service_or_note": "Lütfen bir hizmet seçin veya not yazın",
  },
  "uk": {
    "provider_page.error_service_or_note": "Будь ласка, виберіть послугу або напишіть нотатку",
  },
}

if __name__ == "__main__":
    main()
