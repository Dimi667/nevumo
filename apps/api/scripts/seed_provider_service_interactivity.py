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
        WHERE key IN ('request_service', 'select_this_service')
        GROUP BY lang
        ORDER BY lang
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} keys present")

ALL_TRANSLATIONS: dict[str, dict[str, str]] = {
  "bg": {
    "request_service": "Избери услугата",
    "select_this_service": "Избери тази услуга →",
  },
  "cs": {
    "request_service": "Vyberte službu",
    "select_this_service": "Vyberte tuto službu →",
  },
  "da": {
    "request_service": "Vælg tjenesten",
    "select_this_service": "Vælg denne service →",
  },
  "de": {
    "request_service": "Service auswählen",
    "select_this_service": "Wählen Sie diesen Service →",
  },
  "el": {
    "request_service": "Επιλέξτε την υπηρεσία",
    "select_this_service": "Επιλέξτε αυτή την υπηρεσία →",
  },
  "en": {
    "request_service": "Select the service",
    "select_this_service": "Select this service →",
  },
  "es": {
    "request_service": "Selecciona el servicio",
    "select_this_service": "Seleccionar este servicio →",
  },
  "et": {
    "request_service": "Vali teenus",
    "select_this_service": "Valige see teenus →",
  },
  "fi": {
    "request_service": "Valitse palvelu",
    "select_this_service": "Valitse tämä palvelu →",
  },
  "fr": {
    "request_service": "Sélectionnez le service",
    "select_this_service": "Sélectionner ce service →",
  },
  "ga": {
    "request_service": "Roghnaigh an tseirbhís",
    "select_this_service": "Roghnaigh an tseirbhís seo →",
  },
  "hr": {
    "request_service": "Odaberite uslugu",
    "select_this_service": "Odaberite ovu uslugu →",
  },
  "hu": {
    "request_service": "Válassza ki a szolgáltatást",
    "select_this_service": "Válassza ezt a szolgáltatást →",
  },
  "is": {
    "request_service": "Veldu þjónustuna",
    "select_this_service": "Veldu þessa þjónustu →",
  },
  "it": {
    "request_service": "Seleziona il servizio",
    "select_this_service": "Seleziona questo servizio →",
  },
  "lb": {
    "request_service": "Wielt de Service",
    "select_this_service": "Wiel dësen Service →",
  },
  "lt": {
    "request_service": "Pasirinkite paslaugą",
    "select_this_service": "Pasirinkite šią paslaugą →",
  },
  "lv": {
    "request_service": "Izvēlieties pakalpojumu",
    "select_this_service": "Izvēlēties šo pakalpojumu →",
  },
  "mk": {
    "request_service": "Избери ја услугата",
    "select_this_service": "Избери ја оваа услуга →",
  },
  "mt": {
    "request_service": "Agħżel is-servizz",
    "select_this_service": "Agħżel dan is-servizz →",
  },
  "nl": {
    "request_service": "Kies de dienst",
    "select_this_service": "Selecteer deze service →",
  },
  "no": {
    "request_service": "Velg tjenesten",
    "select_this_service": "Velg denne tjenesten →",
  },
  "pl": {
    "request_service": "Wybierz usługę",
    "select_this_service": "Wybierz tę usługę →",
  },
  "pt": {
    "request_service": "Selecione o serviço",
    "select_this_service": "Selecionar este serviço →",
  },
  "pt-PT": {
    "request_service": "Selecione o serviço",
    "select_this_service": "Selecionar este serviço →",
  },
  "ro": {
    "request_service": "Alege serviciul",
    "select_this_service": "Selectați acest serviciu →",
  },
  "ru": {
    "request_service": "Выберите услугу",
    "select_this_service": "Выбрать эту услугу →",
  },
  "sk": {
    "request_service": "Vyberte službu",
    "select_this_service": "Vyberte túto službu →",
  },
  "sl": {
    "request_service": "Izberite storitev",
    "select_this_service": "Izberite to storitev →",
  },
  "sq": {
    "request_service": "Zgjidh shërbimin",
    "select_this_service": "Zgjidhni këtë shërbim →",
  },
  "sr": {
    "request_service": "Izaberi uslugu",
    "select_this_service": "Izaberite ovu uslugu →",
  },
  "sv": {
    "request_service": "Välj tjänsten",
    "select_this_service": "Välj denna tjänst →",
  },
  "tr": {
    "request_service": "Hizmeti seçin",
    "select_this_service": "Bu hizmeti seçin →",
  },
  "uk": {
    "request_service": "Оберіть послугу",
    "select_this_service": "Вибрати цю послугу →",
  },
}

if __name__ == "__main__":
    main()
