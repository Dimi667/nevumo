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
        SELECT COUNT(*) as total
        FROM translations
        WHERE key LIKE 'provider_page.select_this_service%'
           OR key LIKE 'provider_page.service_selected_confirm%'
           OR key LIKE 'provider_page.service_deselect%'
    """))
    row = result.fetchone()
    print(f"\nVerification: {row[0]} total rows inserted")

ALL_TRANSLATIONS: dict[str, dict[str, str]] = {
  "bg": {
    "provider_page.select_this_service": "Избери тази услуга →",
    "provider_page.service_selected_confirm": "✓ Избрана",
    "provider_page.service_deselect": "✕ Премахни",
  },
  "cs": {
    "provider_page.select_this_service": "Vybrat tuto službu →",
    "provider_page.service_selected_confirm": "✓ Vybráno",
    "provider_page.service_deselect": "✕ Zrušit",
  },
  "da": {
    "provider_page.select_this_service": "Vælg denne ydelse →",
    "provider_page.service_selected_confirm": "✓ Valgt",
    "provider_page.service_deselect": "✕ Fjern",
  },
  "de": {
    "provider_page.select_this_service": "Diesen Service wählen →",
    "provider_page.service_selected_confirm": "✓ Ausgewählt",
    "provider_page.service_deselect": "✕ Entfernen",
  },
  "el": {
    "provider_page.select_this_service": "Επιλέξτε αυτή την υπηρεσία →",
    "provider_page.service_selected_confirm": "✓ Επιλέχθηκε",
    "provider_page.service_deselect": "✕ Αφαίρεση",
  },
  "en": {
    "provider_page.select_this_service": "Select this service →",
    "provider_page.service_selected_confirm": "✓ Selected",
    "provider_page.service_deselect": "✕ Remove",
  },
  "es": {
    "provider_page.select_this_service": "Seleccionar este servicio →",
    "provider_page.service_selected_confirm": "✓ Seleccionado",
    "provider_page.service_deselect": "✕ Eliminar",
  },
  "et": {
    "provider_page.select_this_service": "Vali see teenus →",
    "provider_page.service_selected_confirm": "✓ Valitud",
    "provider_page.service_deselect": "✕ Eemalda",
  },
  "fi": {
    "provider_page.select_this_service": "Valitse tämä palvelu →",
    "provider_page.service_selected_confirm": "✓ Valittu",
    "provider_page.service_deselect": "✕ Poista",
  },
  "fr": {
    "provider_page.select_this_service": "Sélectionner ce service →",
    "provider_page.service_selected_confirm": "✓ Sélectionné",
    "provider_page.service_deselect": "✕ Supprimer",
  },
  "ga": {
    "provider_page.select_this_service": "Roghnaigh an tseirbhís seo →",
    "provider_page.service_selected_confirm": "✓ Roghnaithe",
    "provider_page.service_deselect": "✕ Bain",
  },
  "hr": {
    "provider_page.select_this_service": "Odaberi ovu uslugu →",
    "provider_page.service_selected_confirm": "✓ Odabrano",
    "provider_page.service_deselect": "✕ Ukloni",
  },
  "hu": {
    "provider_page.select_this_service": "Válassza ezt a szolgáltatást →",
    "provider_page.service_selected_confirm": "✓ Kiválasztva",
    "provider_page.service_deselect": "✕ Eltávolítás",
  },
  "is": {
    "provider_page.select_this_service": "Veldu þessa þjónustu →",
    "provider_page.service_selected_confirm": "✓ Valið",
    "provider_page.service_deselect": "✕ Fjarlægja",
  },
  "it": {
    "provider_page.select_this_service": "Seleziona questo servizio →",
    "provider_page.service_selected_confirm": "✓ Selezionato",
    "provider_page.service_deselect": "✕ Rimuovi",
  },
  "lb": {
    "provider_page.select_this_service": "Dës Déngschtleeschtung wielen →",
    "provider_page.service_selected_confirm": "✓ Gewielt",
    "provider_page.service_deselect": "✕ Ewechhuelen",
  },
  "lt": {
    "provider_page.select_this_service": "Pasirinkti šią paslaugą →",
    "provider_page.service_selected_confirm": "✓ Pasirinkta",
    "provider_page.service_deselect": "✕ Pašalinti",
  },
  "lv": {
    "provider_page.select_this_service": "Izvēlēties šo pakalpojumu →",
    "provider_page.service_selected_confirm": "✓ Izvēlēts",
    "provider_page.service_deselect": "✕ Noņemt",
  },
  "mk": {
    "provider_page.select_this_service": "Избери ја оваа услуга →",
    "provider_page.service_selected_confirm": "✓ Избрана",
    "provider_page.service_deselect": "✕ Отстрани",
  },
  "mt": {
    "provider_page.select_this_service": "Agħżel dan is-servizz →",
    "provider_page.service_selected_confirm": "✓ Magħżul",
    "provider_page.service_deselect": "✕ Neħħi",
  },
  "nl": {
    "provider_page.select_this_service": "Selecteer deze dienst →",
    "provider_page.service_selected_confirm": "✓ Geselecteerd",
    "provider_page.service_deselect": "✕ Verwijderen",
  },
  "no": {
    "provider_page.select_this_service": "Velg denne tjenesten →",
    "provider_page.service_selected_confirm": "✓ Valgt",
    "provider_page.service_deselect": "✕ Fjern",
  },
  "pl": {
    "provider_page.select_this_service": "Wybierz tę usługę →",
    "provider_page.service_selected_confirm": "✓ Wybrano",
    "provider_page.service_deselect": "✕ Usuń",
  },
  "pt": {
    "provider_page.select_this_service": "Selecionar este serviço →",
    "provider_page.service_selected_confirm": "✓ Selecionado",
    "provider_page.service_deselect": "✕ Remover",
  },
  "pt-PT": {
    "provider_page.select_this_service": "Selecionar este serviço →",
    "provider_page.service_selected_confirm": "✓ Selecionado",
    "provider_page.service_deselect": "✕ Remover",
  },
  "ro": {
    "provider_page.select_this_service": "Selectați acest serviciu →",
    "provider_page.service_selected_confirm": "✓ Selectat",
    "provider_page.service_deselect": "✕ Eliminați",
  },
  "ru": {
    "provider_page.select_this_service": "Выбрать эту услугу →",
    "provider_page.service_selected_confirm": "✓ Выбрано",
    "provider_page.service_deselect": "✕ Убрать",
  },
  "sk": {
    "provider_page.select_this_service": "Vybrať túto službu →",
    "provider_page.service_selected_confirm": "✓ Vybraté",
    "provider_page.service_deselect": "✕ Odstrániť",
  },
  "sl": {
    "provider_page.select_this_service": "Izberi to storitev →",
    "provider_page.service_selected_confirm": "✓ Izbrano",
    "provider_page.service_deselect": "✕ Odstrani",
  },
  "sq": {
    "provider_page.select_this_service": "Zgjidhni këtë shërbim →",
    "provider_page.service_selected_confirm": "✓ Zgjedhur",
    "provider_page.service_deselect": "✕ Hiq",
  },
  "sr": {
    "provider_page.select_this_service": "Изабери ову услугу →",
    "provider_page.service_selected_confirm": "✓ Изабрано",
    "provider_page.service_deselect": "✕ Уклони",
  },
  "sv": {
    "provider_page.select_this_service": "Välj den här tjänsten →",
    "provider_page.service_selected_confirm": "✓ Vald",
    "provider_page.service_deselect": "✕ Ta bort",
  },
  "tr": {
    "provider_page.select_this_service": "Bu hizmeti seç →",
    "provider_page.service_selected_confirm": "✓ Seçildi",
    "provider_page.service_deselect": "✕ Kaldır",
  },
  "uk": {
    "provider_page.select_this_service": "Вибрати цю послугу →",
    "provider_page.service_selected_confirm": "✓ Вибрано",
    "provider_page.service_deselect": "✕ Видалити",
  },
}

if __name__ == "__main__":
    main()
