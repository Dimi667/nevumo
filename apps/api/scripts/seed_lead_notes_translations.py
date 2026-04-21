#!/usr/bin/env python3
"""
Seed script for lead notes translation keys.
Adds 5 keys: label_private_notes, placeholder_private_notes, btn_save_notes, msg_notes_saved, msg_notes_save_failed
for all 34 supported languages in the provider_dashboard namespace.
"""

import os

from sqlalchemy import text
from apps.api.database import engine
from apps.api.dependencies import get_redis

NAMESPACE = "provider_dashboard"

# All 34 translations for the 5 keys
TRANSLATIONS = {
    "bg": {
        "label_private_notes": "Лични бележки (виждате ги само вие)",
        "placeholder_private_notes": "Добавете бележка за това запитване...",
        "btn_save_notes": "Запази бележката",
        "msg_notes_saved": "Бележката е запазена успешно",
        "msg_notes_save_failed": "Грешка при запис на бележката",
        "lead_detail_title": "Бележка",
        "aria_close": "Затвори",
        "btn_close": "Затвори",
        "label_client_message": "Съобщение от клиента",
        "msg_no_description": "Няма предоставено описание",
        "msg_saving": "Запазване..."
    },
    "en": {
        "label_private_notes": "Private notes (only visible to you)",
        "placeholder_private_notes": "Add a note for this lead...",
        "btn_save_notes": "Save note",
        "msg_notes_saved": "Note saved successfully",
        "msg_notes_save_failed": "Failed to save note",
        "lead_detail_title": "Note",
        "aria_close": "Close",
        "btn_close": "Close",
        "label_client_message": "Client Message",
        "msg_no_description": "No description provided",
        "msg_saving": "Saving..."
    },
    "de": {
        "label_private_notes": "Private Notizen (nur für Sie sichtbar)",
        "placeholder_private_notes": "Notiz für diesen Lead hinzufügen...",
        "btn_save_notes": "Notiz speichern",
        "msg_notes_saved": "Notiz erfolgreich gespeichert",
        "msg_notes_save_failed": "Fehler beim Speichern der Notiz",
        "lead_detail_title": "Notiz",
        "aria_close": "Schließen",
        "btn_close": "Schließen",
        "label_client_message": "Nachricht vom Kunden",
        "msg_no_description": "Keine Beschreibung vorhanden",
        "msg_saving": "Wird gespeichert..."
    },
    "fr": {
        "label_private_notes": "Notes privées (visible uniquement par vous)",
        "placeholder_private_notes": "Ajouter une note pour ce lead...",
        "btn_save_notes": "Enregistrer la note",
        "msg_notes_saved": "Note enregistrée avec succès",
        "msg_notes_save_failed": "Échec de l'enregistrement de la note",
        "lead_detail_title": "Note",
        "aria_close": "Fermer",
        "btn_close": "Fermer",
        "label_client_message": "Message du client",
        "msg_no_description": "Aucune description fournie",
        "msg_saving": "Enregistrement..."
    },
    "it": {
        "label_private_notes": "Note private (visibili solo a te)",
        "placeholder_private_notes": "Aggiungi una nota per questo lead...",
        "btn_save_notes": "Salva nota",
        "msg_notes_saved": "Nota salvata con successo",
        "msg_notes_save_failed": "Errore nel salvataggio della nota",
        "lead_detail_title": "Nota",
        "aria_close": "Chiudi",
        "btn_close": "Chiudi",
        "label_client_message": "Messaggio del cliente",
        "msg_no_description": "Nessuna descrizione fornita",
        "msg_saving": "Salvataggio..."
    },
    "es": {
        "label_private_notes": "Notas privadas (solo visibles para ti)",
        "placeholder_private_notes": "Añadir una nota para este lead...",
        "btn_save_notes": "Guardar nota",
        "msg_notes_saved": "Nota guardada con éxito",
        "msg_notes_save_failed": "Error al guardar la nota",
        "lead_detail_title": "Nota",
        "aria_close": "Cerrar",
        "btn_close": "Cerrar",
        "label_client_message": "Mensaje del cliente",
        "msg_no_description": "No se proporcionó descripción",
        "msg_saving": "Guardando..."
    },
    "pt": {
        "label_private_notes": "Notas privadas (visíveis apenas para você)",
        "placeholder_private_notes": "Adicionar uma nota para este lead...",
        "btn_save_notes": "Salvar nota",
        "msg_notes_saved": "Nota salva com sucesso",
        "msg_notes_save_failed": "Falha ao salvar nota",
        "lead_detail_title": "Nota",
        "aria_close": "Fechar",
        "btn_close": "Fechar",
        "label_client_message": "Mensagem do cliente",
        "msg_no_description": "Nenhuma descrição fornecida",
        "msg_saving": "Salvando..."
    },
    "pt-PT": {
        "label_private_notes": "Notas privadas (visíveis apenas para si)",
        "placeholder_private_notes": "Adicionar uma nota para este lead...",
        "btn_save_notes": "Guardar nota",
        "msg_notes_saved": "Nota guardada com sucesso",
        "msg_notes_save_failed": "Falha ao guardar nota",
        "lead_detail_title": "Nota",
        "aria_close": "Fechar",
        "btn_close": "Fechar",
        "label_client_message": "Mensagem do cliente",
        "msg_no_description": "Nenhuma descrição fornecida",
        "msg_saving": "A guardar..."
    },
    "ru": {
        "label_private_notes": "Личные заметки (видимы только вам)",
        "placeholder_private_notes": "Добавить заметку к этому запросу...",
        "btn_save_notes": "Сохранить заметку",
        "msg_notes_saved": "Заметка успешно сохранена",
        "msg_notes_save_failed": "Ошибка при сохранении заметки",
        "lead_detail_title": "Заметка",
        "aria_close": "Закрыть",
        "btn_close": "Закрыть",
        "label_client_message": "Сообщение от клиента",
        "msg_no_description": "Описание отсутствует",
        "msg_saving": "Сохранение..."
    },
    "tr": {
        "label_private_notes": "Özel notlar (yalnızca siz görebilirsiniz)",
        "placeholder_private_notes": "Bu talep için bir not ekleyin...",
        "btn_save_notes": "Notu kaydet",
        "msg_notes_saved": "Not başarıyla kaydedildi",
        "msg_notes_save_failed": "Not kaydedilemedi",
        "lead_detail_title": "Not",
        "aria_close": "Kapat",
        "btn_close": "Kapat",
        "label_client_message": "Müşteri Mesajı",
        "msg_no_description": "Açıklama belirtilmedi",
        "msg_saving": "Kaydediliyor..."
    },
    "pl": {
        "label_private_notes": "Prywatne notatki (widoczne tylko dla Ciebie)",
        "placeholder_private_notes": "Dodaj notatkę do tego zapytania...",
        "btn_save_notes": "Zapisz notatkę",
        "msg_notes_saved": "Notatka zapisana pomyślnie",
        "msg_notes_save_failed": "Błąd podczas zapisywania notatki",
        "lead_detail_title": "Notatka",
        "aria_close": "Zamknij",
        "btn_close": "Zamknij",
        "label_client_message": "Wiadomość od klienta",
        "msg_no_description": "Brak opisu",
        "msg_saving": "Zapisywanie..."
    },
    "ro": {
        "label_private_notes": "Note private (vizibile doar pentru tine)",
        "placeholder_private_notes": "Adaugă o notă pentru acest lead...",
        "btn_save_notes": "Salvează nota",
        "msg_notes_saved": "Notă salvată cu succes",
        "msg_notes_save_failed": "Eroare la salvarea notei",
        "lead_detail_title": "Notă",
        "aria_close": "Închide",
        "btn_close": "Închide",
        "label_client_message": "Mesaj de la client",
        "msg_no_description": "Nicio descriere furnizată",
        "msg_saving": "Se salvează..."
    },
    "nl": {
        "label_private_notes": "Privénotities (alleen zichtbaar voor jou)",
        "placeholder_private_notes": "Voeg een notitie toe voor deze lead...",
        "btn_save_notes": "Notitie opslaan",
        "msg_notes_saved": "Notitie succesvol opgeslagen",
        "msg_notes_save_failed": "Fout bij opslaan van notitie",
        "lead_detail_title": "Notitie",
        "aria_close": "Sluiten",
        "btn_close": "Sluiten",
        "label_client_message": "Bericht van klant",
        "msg_no_description": "Geen beschrijving opgegeven",
        "msg_saving": "Opslaan..."
    },
    "el": {
        "label_private_notes": "Ιδιωτικές σημειώσεις (ορατές μόνο σε εσάς)",
        "placeholder_private_notes": "Προσθέστε μια σημείωση για αυτό το αίτημα...",
        "btn_save_notes": "Αποθήκευση σημείωσης",
        "msg_notes_saved": "Η σημείωση αποθηκεύτηκε με επιτυχία",
        "msg_notes_save_failed": "Αποτυχία αποθήκευσης σημείωσης",
        "lead_detail_title": "Σημείωση",
        "aria_close": "Κλείσιμο",
        "btn_close": "Κλείσιμο",
        "label_client_message": "Μήνυμα πελάτη",
        "msg_no_description": "Δεν παρέχεται περιγραφή",
        "msg_saving": "Αποθήκευση..."
    },
    "hu": {
        "label_private_notes": "Privát megjegyzések (csak Ön láthatja)",
        "placeholder_private_notes": "Megjegyzés hozzáadása ehhez a megkereséshez...",
        "btn_save_notes": "Megjegyzés mentése",
        "msg_notes_saved": "Megjegyzés sikeresen mentve",
        "msg_notes_save_failed": "Hiba a megjegyzés mentésekor",
        "lead_detail_title": "Megjegyzés",
        "aria_close": "Bezárás",
        "btn_close": "Bezárás",
        "label_client_message": "Ügyfél üzenete",
        "msg_no_description": "Nincs leírás megadva",
        "msg_saving": "Mentés..."
    },
    "cs": {
        "label_private_notes": "Soukromé poznámky (viditelné pouze pro vás)",
        "placeholder_private_notes": "Přidat poznámku k tomuto poptávce...",
        "btn_save_notes": "Uložit poznámku",
        "msg_notes_saved": "Poznámka byla úspěšně uložena",
        "msg_notes_save_failed": "Uložení poznámky se nezdařilo",
        "lead_detail_title": "Poznámka",
        "aria_close": "Zavřít",
        "btn_close": "Zavřít",
        "label_client_message": "Zpráva od klienta",
        "msg_no_description": "Popis nebyl zadán",
        "msg_saving": "Ukládání..."
    },
    "sk": {
        "label_private_notes": "Súkromné poznámky (viditeľné iba pre vás)",
        "placeholder_private_notes": "Pridať poznámku k tomuto dopytu...",
        "btn_save_notes": "Uložiť poznámku",
        "msg_notes_saved": "Poznámka bola úspešne uložená",
        "msg_notes_save_failed": "Uloženie poznámky zlyhalo",
        "lead_detail_title": "Poznámka",
        "aria_close": "Zavrieť",
        "btn_close": "Zavrieť",
        "label_client_message": "Správa od klienta",
        "msg_no_description": "Popis nebol zadaný",
        "msg_saving": "Ukladanie..."
    },
    "da": {
        "label_private_notes": "Private noter (kun synlige for dig)",
        "placeholder_private_notes": "Tilføj en note til denne lead...",
        "btn_save_notes": "Gem note",
        "msg_notes_saved": "Note gemt med succes",
        "msg_notes_save_failed": "Kunne ikke gemme note",
        "lead_detail_title": "Note",
        "aria_close": "Luk",
        "btn_close": "Luk",
        "label_client_message": "Besked fra klient",
        "msg_no_description": "Ingen beskrivelse angivet",
        "msg_saving": "Gemmer..."
    },
    "fi": {
        "label_private_notes": "Yksityiset muistiinpanot (vain sinulle)",
        "placeholder_private_notes": "Lisää muistiinpano tälle liidille...",
        "btn_save_notes": "Tallenna muistiinpano",
        "msg_notes_saved": "Muistiinpano tallennettu onnistuneesti",
        "msg_notes_save_failed": "Muistiinpanon tallennus epäonnistui",
        "lead_detail_title": "Muistiinpano",
        "aria_close": "Sulje",
        "btn_close": "Sulje",
        "label_client_message": "Viesti asiakkaalta",
        "msg_no_description": "Kuvausta ei ole annettu",
        "msg_saving": "Tallennetaan..."
    },
    "no": {
        "label_private_notes": "Private notater (kun synlig for deg)",
        "placeholder_private_notes": "Legg til et notat for denne leaden...",
        "btn_save_notes": "Lagre notat",
        "msg_notes_saved": "Notat lagret",
        "msg_notes_save_failed": "Kunne ikke lagre notat",
        "lead_detail_title": "Notat",
        "aria_close": "Lukk",
        "btn_close": "Lukk",
        "label_client_message": "Melding fra kunde",
        "msg_no_description": "Ingen beskrivelse oppgitt",
        "msg_saving": "Lagrer..."
    },
    "sv": {
        "label_private_notes": "Privata anteckningar (endast synliga för dig)",
        "placeholder_private_notes": "Lägg till en anteckning för detta ärende...",
        "btn_save_notes": "Spara anteckning",
        "msg_notes_saved": "Anteckning sparad",
        "msg_notes_save_failed": "Misslyckades med att spara anteckning",
        "lead_detail_title": "Anteckning",
        "aria_close": "Stäng",
        "btn_close": "Stäng",
        "label_client_message": "Meddelande från kund",
        "msg_no_description": "Ingen beskrivning angiven",
        "msg_saving": "Sparar..."
    },
    "hr": {
        "label_private_notes": "Privatne bilješke (vidljive samo vama)",
        "placeholder_private_notes": "Dodajte bilješku za ovaj upit...",
        "btn_save_notes": "Spremi bilješku",
        "msg_notes_saved": "Bilješka je uspješno spremljena",
        "msg_notes_save_failed": "Pogreška pri spremanju bilješke",
        "lead_detail_title": "Bilješka",
        "aria_close": "Zatvori",
        "btn_close": "Zatvori",
        "label_client_message": "Poruka klijenta",
        "msg_no_description": "Opis nije naveden",
        "msg_saving": "Spremanje..."
    },
    "sr": {
        "label_private_notes": "Privatne beleške (vidljive samo vama)",
        "placeholder_private_notes": "Dodajte belešku za ovaj upit...",
        "btn_save_notes": "Sačuvaj belešku",
        "msg_notes_saved": "Beleška je uspešno sačuvana",
        "msg_notes_save_failed": "Greška pri čuvanju beleške",
        "lead_detail_title": "Beleška",
        "aria_close": "Zatvori",
        "btn_close": "Zatvori",
        "label_client_message": "Poruka klijenta",
        "msg_no_description": "Opis nije naveden",
        "msg_saving": "Čuvanje..."
    },
    "sl": {
        "label_private_notes": "Zasebni zapiski (vidni samo vam)",
        "placeholder_private_notes": "Dodajte zapisek za to povpraševanje...",
        "btn_save_notes": "Shrani zapisek",
        "msg_notes_saved": "Zapisek uspešno shranjen",
        "msg_notes_save_failed": "Napaka pri shranjevanju zapiska",
        "lead_detail_title": "Opomba",
        "aria_close": "Zapri",
        "btn_close": "Zapri",
        "label_client_message": "Sporočilo stranke",
        "msg_no_description": "Opis ni podan",
        "msg_saving": "Shranjevanje..."
    },
    "et": {
        "label_private_notes": "Eramärkmed (nähtavad ainult teile)",
        "placeholder_private_notes": "Lisa märkus selle päringu kohta...",
        "btn_save_notes": "Salvesta märkus",
        "msg_notes_saved": "Märkus edukalt salvestatud",
        "msg_notes_save_failed": "Märkuse salvestamine ebaõnnestus",
        "lead_detail_title": "Märkus",
        "aria_close": "Sulge",
        "btn_close": "Sulge",
        "label_client_message": "Kliendi sõnum",
        "msg_no_description": "Kirjeldus puudub",
        "msg_saving": "Salvestamine..."
    },
    "lv": {
        "label_private_notes": "Privātās piezīmes (redzamas tikai jums)",
        "placeholder_private_notes": "Pievienot piezīmi šim pieteikumam...",
        "btn_save_notes": "Saglabāt piezīmi",
        "msg_notes_saved": "Piezīme veiksmīgi saglabāta",
        "msg_notes_save_failed": "Kļūda, saglabājot piezīmi",
        "lead_detail_title": "Piezīme",
        "aria_close": "Aizvērt",
        "btn_close": "Aizvērt",
        "label_client_message": "Klienta ziņa",
        "msg_no_description": "Apraksts nav sniegts",
        "msg_saving": "Saglabā..."
    },
    "lt": {
        "label_private_notes": "Asmeninės pastabos (matomos tik jums)",
        "placeholder_private_notes": "Pridėti pastabą šiam užklausimui...",
        "btn_save_notes": "Išsaugoti pastabą",
        "msg_notes_saved": "Pastaba sėkmingai išsaugota",
        "msg_notes_save_failed": "Nepavyko išsaugoti pastabos",
        "lead_detail_title": "Pastaba",
        "aria_close": "Uždaryti",
        "btn_close": "Uždaryti",
        "label_client_message": "Kliento žinutė",
        "msg_no_description": "Aprašymas nepateiktas",
        "msg_saving": "Saugoma..."
    },
    "uk": {
        "label_private_notes": "Приватні нотатки (видимі лише вам)",
        "placeholder_private_notes": "Додати нотатку до цього запиту...",
        "btn_save_notes": "Зберегти нотатку",
        "msg_notes_saved": "Нотатку успішно збережено",
        "msg_notes_save_failed": "Помилка при збереженні нотатки",
        "lead_detail_title": "Нотатка",
        "aria_close": "Закрити",
        "btn_close": "Закрити",
        "label_client_message": "Повідомлення від клієнта",
        "msg_no_description": "Опис відсутній",
        "msg_saving": "Збереження..."
    },
    "mk": {
        "label_private_notes": "Приватни белешки (видливи само за вас)",
        "placeholder_private_notes": "Додадете белешка за ова барање...",
        "btn_save_notes": "Зачувај белешка",
        "msg_notes_saved": "Белешката е успешно зачувана",
        "msg_notes_save_failed": "Грешка при зачувување на белешката",
        "lead_detail_title": "Белешка",
        "aria_close": "Затвори",
        "btn_close": "Затвори",
        "label_client_message": "Порака од клиентот",
        "msg_no_description": "Нема опис",
        "msg_saving": "Зачувување..."
    },
    "sq": {
        "label_private_notes": "Shënime private (duken vetëm nga ju)",
        "placeholder_private_notes": "Shto një shënim për këtë kërkesë...",
        "btn_save_notes": "Ruaj shënimin",
        "msg_notes_saved": "Shënimi u ruajt me sukses",
        "msg_notes_save_failed": "Dështoi ruajtja e shënimit",
        "lead_detail_title": "Shënim",
        "aria_close": "Mbyll",
        "btn_close": "Mbyll",
        "label_client_message": "Mesazh nga klienti",
        "msg_no_description": "Nuk ka përshkrim",
        "msg_saving": "Ruajtje..."
    },
    "mt": {
        "label_private_notes": "Noti privati (jidhru lilek biss)",
        "placeholder_private_notes": "Żid nota għal din it-talba...",
        "btn_save_notes": "Issejvja n-nota",
        "msg_notes_saved": "In-nota ġiet issejvjata b'suċċess",
        "msg_notes_save_failed": "In-nota ma setgħetx tiġi ssejvjata",
        "lead_detail_title": "Nota",
        "aria_close": "Agħlaq",
        "btn_close": "Agħlaq",
        "label_client_message": "Messaġġ mill-klijent",
        "msg_no_description": "L-ebda deskrizzjoni pprovduta",
        "msg_saving": "Issejvjar..."
    },
    "ga": {
        "label_private_notes": "Nótaí príobháideacha (le feiceáil agat féin amháin)",
        "placeholder_private_notes": "Cuir nóta leis an lead seo...",
        "btn_save_notes": "Sábháil nóta",
        "msg_notes_saved": "Nóta sábháilte go rathúil",
        "msg_notes_save_failed": "Theip ar shábháil an nóta",
        "lead_detail_title": "Nóta",
        "aria_close": "Dún",
        "btn_close": "Dún",
        "label_client_message": "Teachtaireacht ón gcliant",
        "msg_no_description": "Níl aon tuairisc curtha ar fáil",
        "msg_saving": "Á shábháil..."
    },
    "is": {
        "label_private_notes": "Einkanótur (aðeins sýnilegt þér)",
        "placeholder_private_notes": "Bæta við nótu fyrir þessa fyrirspurn...",
        "btn_save_notes": "Vista nótu",
        "msg_notes_saved": "Nóta vistuð giftusamlega",
        "msg_notes_save_failed": "Ekki tókst að vista nótu",
        "lead_detail_title": "Nóta",
        "aria_close": "Loka",
        "btn_close": "Loka",
        "label_client_message": "Skilaboð frá viðskiptavini",
        "msg_no_description": "Engin lýsing gefin",
        "msg_saving": "Vistar..."
    },
    "lb": {
        "label_private_notes": "Privat Notizen (nëmmen fir Iech siichtbar)",
        "placeholder_private_notes": "Eng Notiz fir dëse Lead derbäisetzen...",
        "btn_save_notes": "Notiz späicheren",
        "msg_notes_saved": "Notiz erfollegräich gespäichert",
        "msg_notes_save_failed": "Feeler beim Späichere vun der Notiz",
        "lead_detail_title": "Notiz",
        "aria_close": "Zoumaachen",
        "btn_close": "Zoumaachen",
        "label_client_message": "Noricht vum Client",
        "msg_no_description": "Keng Beschreiwung uginn",
        "msg_saving": "Späicheren..."
    }
}

KEYS = [
    "label_private_notes", "placeholder_private_notes", "btn_save_notes", 
    "msg_notes_saved", "msg_notes_save_failed", "lead_detail_title", 
    "aria_close", "btn_close", "label_client_message", 
    "msg_no_description", "msg_saving"
]


def main():
    # Ensure all languages have all keys (fallback to English)
    en_defaults = TRANSLATIONS.get("en", {})
    for lang, lang_translations in TRANSLATIONS.items():
        if lang == "en":
            continue
        for key in KEYS:
            if key not in lang_translations:
                lang_translations[key] = en_defaults.get(key, "")

    total_inserted = 0
    
    with engine.connect() as conn:
        # Insert or update translations using ON CONFLICT upsert
        for lang, lang_translations in TRANSLATIONS.items():
            for key_name, value in lang_translations.items():
                full_key = f"{NAMESPACE}.{key_name}"
                conn.execute(
                    text("""
                        INSERT INTO translations (lang, key, value)
                        VALUES (:lang, :key, :value)
                        ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
                    """),
                    {"lang": lang, "key": full_key, "value": value}
                )
                total_inserted += 1
        
        conn.commit()
        print(f"✓ Successfully seeded {total_inserted} translations for {len(KEYS)} keys in '{NAMESPACE}' namespace")
        
        # Verify count
        for key_name in KEYS:
            full_key = f"{NAMESPACE}.{key_name}"
            result = conn.execute(
                text("SELECT COUNT(*) FROM translations WHERE key = :key"),
                {"key": full_key}
            )
            count = result.scalar()
            print(f"✓ '{full_key}': {count} translations in database")
    
    # Clear Redis cache for provider_dashboard namespace
    try:
        r = get_redis()
        if not r:
            print("✓ Redis not available, skipping cache clear")
            return

        # Delete all keys matching the pattern for provider_dashboard
        # The key format in translation_service.py is trans:{lang}:{namespace}
        pattern = f"trans:*:{NAMESPACE}"
        keys = list(r.scan_iter(match=pattern))
        if keys:
            r.delete(*keys)
            print(f"✓ Cleared {len(keys)} keys from Redis cache for '{NAMESPACE}' namespace")
        else:
            # Also try the older pattern just in case
            old_pattern = f"i18n:{NAMESPACE}:*"
            old_keys = list(r.scan_iter(match=old_pattern))
            if old_keys:
                r.delete(*old_keys)
                print(f"✓ Cleared {len(old_keys)} legacy keys from Redis cache")
            else:
                print("✓ No Redis keys found to clear")
    except Exception as e:
        print(f"⚠ Could not clear Redis cache: {e}")


if __name__ == "__main__":
    main()
