from sqlalchemy import text

from apps.api.database import SessionLocal

TRANSLATIONS = [
    ("bg", "city_selection.meta_title", "Избери своя град"),
    ("cs", "city_selection.meta_title", "Vyberte své město"),
    ("da", "city_selection.meta_title", "Vælg din by"),
    ("de", "city_selection.meta_title", "Wähle deine Stadt"),
    ("el", "city_selection.meta_title", "Επιλέξτε την πόλη σας"),
    ("en", "city_selection.meta_title", "Choose your city"),
    ("es", "city_selection.meta_title", "Elige tu ciudad"),
    ("et", "city_selection.meta_title", "Vali oma linn"),
    ("fi", "city_selection.meta_title", "Valitse kaupunkisi"),
    ("fr", "city_selection.meta_title", "Choisissez votre ville"),
    ("ga", "city_selection.meta_title", "Roghnaigh do chathair"),
    ("hr", "city_selection.meta_title", "Odaberi svoj grad"),
    ("hu", "city_selection.meta_title", "Válassz várost"),
    ("is", "city_selection.meta_title", "Veldu borg þína"),
    ("it", "city_selection.meta_title", "Scegli la tua città"),
    ("lb", "city_selection.meta_title", "Wiel deng Stad"),
    ("lt", "city_selection.meta_title", "Pasirinkite savo miestą"),
    ("lv", "city_selection.meta_title", "Izvēlieties savu pilsētu"),
    ("mk", "city_selection.meta_title", "Избери го твојот град"),
    ("mt", "city_selection.meta_title", "Agħżel il-belt tiegħek"),
    ("nl", "city_selection.meta_title", "Kies je stad"),
    ("no", "city_selection.meta_title", "Velg din by"),
    ("pl", "city_selection.meta_title", "Wybierz swoje miasto"),
    ("pt", "city_selection.meta_title", "Escolha sua cidade"),
    ("pt-PT", "city_selection.meta_title", "Escolha a sua cidade"),
    ("ro", "city_selection.meta_title", "Alege orașul tău"),
    ("ru", "city_selection.meta_title", "Выберите свой город"),
    ("sk", "city_selection.meta_title", "Vyberte svoje mesto"),
    ("sl", "city_selection.meta_title", "Izberi svoje mesto"),
    ("sq", "city_selection.meta_title", "Zgjidhni qytetin tuaj"),
    ("sr", "city_selection.meta_title", "Izaberi svoj grad"),
    ("sv", "city_selection.meta_title", "Välj din stad"),
    ("tr", "city_selection.meta_title", "Şehrinizi seçin"),
    ("uk", "city_selection.meta_title", "Виберіть своє місто"),
]

def main():
    db = SessionLocal()
    try:
        insert_translations(db, TRANSLATIONS)
    finally:
        db.close()

def insert_translations(db, data: list[tuple[str, str, str]]) -> None:
    for lang, key, value in data:
        db.execute(
            text("""
                INSERT INTO translations (lang, key, value)
                VALUES (:lang, :key, :value)
                ON CONFLICT (lang, key)
                DO UPDATE SET value = EXCLUDED.value
            """),
            {"lang": lang, "key": key, "value": value}
        )
    db.commit()
    print("Seeded 34 rows — Part 1 complete")

if __name__ == "__main__":
    main()
