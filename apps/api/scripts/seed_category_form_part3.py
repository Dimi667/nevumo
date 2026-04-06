#!/usr/bin/env python3
"""
Script to upsert translation keys for category form part 3
"""

import os
import psycopg2
from psycopg2 import sql

def main():
    # Database connection
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("ERROR: DATABASE_URL environment variable not set")
        return
    
    # Translation data
    translations = {
        'category.chip_not_sure': {
            'bg': "Не съм сигурен",
            'cs': "Nejsem si jistý",
            'da': "Ikke sikker",
            'de': "Nicht sicher",
            'el': "Δεν είμαι σίγουρος",
            'en': "Not sure",
            'es': "No estoy seguro",
            'et': "Pole kindel",
            'fi': "En ole varma",
            'fr': "Pas sûr",
            'ga': "Níl mé cinnte",
            'hr': "Nisam siguran",
            'hu': "Nem vagyok biztos",
            'is': "Ekki viss",
            'it': "Non sono sicuro",
            'lb': "Net sécher",
            'lt': "Nesu tikras",
            'lv': "Neesmu pārliecināts",
            'mk': "Не сум сигурен",
            'mt': "Mhux ċert",
            'nl': "Niet zeker",
            'no': "Ikke sikker",
            'pl': "Nie wiem dokładnie",
            'pt': "Não tenho certeza",
            'pt-PT': "Não tenho a certeza",
            'ro': "Nu sunt sigur",
            'ru': "Не уверен",
            'sk': "Nie som si istý",
            'sl': "Nisem prepričan",
            'sq': "Nuk jam i sigurt",
            'sr': "Нисам сигуран",
            'sv': "Inte säker",
            'tr': "Emin değilim",
            'uk': "Не впевнений"
        },
        'category.details_label': {
            'bg': "Добави детайли (по избор)",
            'cs': "Přidejte podrobnosti (volitelné)",
            'da': "Tilføj detaljer (valgfrit)",
            'de': "Details hinzufügen (optional)",
            'el': "Προσθέστε λεπτομέρειες (προαιρετικό)",
            'en': "Add details (optional)",
            'es': "Añade detalles (opcional)",
            'et': "Lisa üksikasjad (valikuline)",
            'fi': "Lisää tietoja (valinnainen)",
            'fr': "Ajouter des détails (facultatif)",
            'ga': "Cuir sonraí leis (roghnach)",
            'hr': "Dodajte detalje (neobavezno)",
            'hu': "Részletek hozzáadása (opcionális)",
            'is': "Bættu við upplýsingum (valfrjálst)",
            'it': "Aggiungi dettagli (opzionale)",
            'lb': "Details bäisetzen (optional)",
            'lt': "Pridėti detalių (neprivaloma)",
            'lv': "Pievienot detaļas (pēc izvēles)",
            'mk': "Додај детали (опционално)",
            'mt': "Żid dettalji (fakultattiv)",
            'nl': "Voeg details toe (optioneel)",
            'no': "Legg til detaljer (valgfritt)",
            'pl': "Dodaj szczegóły (opcjonalnie)",
            'pt': "Adicione detalhes (opcional)",
            'pt-PT': "Adicione detalhes (opcional)",
            'ro': "Adaugă detalii (opțional)",
            'ru': "Добавьте детали (необязательно)",
            'sk': "Pridajte podrobnosti (voliteľné)",
            'sl': "Dodajte podrobnosti (neobvezno)",
            'sq': "Shto detaje (opsionale)",
            'sr': "Додајте детаље (опционо)",
            'sv': "Lägg till detaljer (valfritt)",
            'tr': "Ayrıntı ekleyin (isteğe bağlı)",
            'uk': "Додайте деталі (необов'язково)"
        },
        'category.details_placeholder': {
            'bg': "Опиши заявката си — час, адрес, специфични изисквания...",
            'cs': "Popište svůj požadavek — čas, adresa, specifické požadavky...",
            'da': "Beskriv din anmodning — tidspunkt, adresse, specifikke krav...",
            'de': "Beschreibe deine Anfrage — Uhrzeit, Adresse, besondere Anforderungen...",
            'el': "Περίγραψε το αίτημά σου — ώρα, διεύθυνση, ειδικές απαιτήσεις...",
            'en': "Describe your request — time, address, specific requirements...",
            'es': "Describe tu solicitud — hora, dirección, requisitos específicos...",
            'et': "Kirjeldage oma soovi — aeg, aadress, erinõuded...",
            'fi': "Kuvaile pyyntösi — aika, osoite, erityisvaatimukset...",
            'fr': "Décrivez votre demande — heure, adresse, exigences spécifiques...",
            'ga': "Déan cur síos ar d'iarratas — am, seoladh, riachtanais shonracha...",
            'hr': "Opišite zahtjev — vrijeme, adresa, posebni zahtjevi...",
            'hu': "Írja le kérését — időpont, cím, különleges igények...",
            'is': "Lýstu beiðni þinni — tími, heimilisfang, sérstæðar kröfur...",
            'it': "Descrivi la tua richiesta — orario, indirizzo, requisiti specifici...",
            'lb': "Beschreift Är Ufro — Zäit, Adress, spezifesch Ufuerderungen...",
            'lt': "Apibūdinkite užklausą — laikas, adresas, konkretūs reikalavimai...",
            'lv': "Aprakstiet pieprasījumu — laiks, adrese, īpašās prasības...",
            'mk': "Опишете го барањето — час, адреса, посебни барања...",
            'mt': "Iddeskrivi t-talba tiegħek — ħin, indirizz, rekwiżiti speċifiċi...",
            'nl': "Beschrijf uw aanvraag — tijd, adres, specifieke wensen...",
            'no': "Beskriv forespørselen — tid, adresse, spesifikke krav...",
            'pl': "Opisz zlecenie — godzina, adres, szczegółowe wymagania...",
            'pt': "Descreva seu pedido — horário, endereço, requisitos específicos...",
            'pt-PT': "Descreva o seu pedido — hora, morada, requisitos específicos...",
            'ro': "Descrie cererea — oră, adresă, cerințe specifice...",
            'ru': "Опишите заявку — время, адрес, особые требования...",
            'sk': "Opíšte žiadosť — čas, adresa, špeciálne požiadavky...",
            'sl': "Opišite zahtevo — čas, naslov, posebne zahteve...",
            'sq': "Përshkruaj kërkesën — ora, adresa, kërkesat specifike...",
            'sr': "Опишите захтев — вријеме, адреса, посебни захтеви...",
            'sv': "Beskriv din förfrågan — tid, adress, specifika krav...",
            'tr': "Talebinizi açıklayın — saat, adres, özel gereksinimler...",
            'uk': "Опишіть запит — час, адреса, особливі вимоги..."
        },
        'category.get_offers_btn': {
            'bg': "Получи оферти",
            'cs': "Získat nabídky",
            'da': "Få tilbud",
            'de': "Angebote erhalten",
            'el': "Λήψη προσφορών",
            'en': "Get offers",
            'es': "Obtener ofertas",
            'et': "Hangi pakkumised",
            'fi': "Hae tarjouksia",
            'fr': "Obtenir des offres",
            'ga': "Faigh tairiscintí",
            'hr': "Dobij ponude",
            'hu': "Ajánlatok kérése",
            'is': "Fá tilboð",
            'it': "Ottieni offerte",
            'lb': "Ubidder kréien",
            'lt': "Gauti pasiūlymus",
            'lv': "Saņemt piedāvājumus",
            'mk': "Добиј понуди",
            'mt': "Ikseb offerti",
            'nl': "Offertes ontvangen",
            'no': "Få tilbud",
            'pl': "Otrzymaj oferty",
            'pt': "Receber propostas",
            'pt-PT': "Receber propostas",
            'ro': "Primește oferte",
            'ru': "Получить предложения",
            'sk': "Získať ponuky",
            'sl': "Prejmi ponudbe",
            'sq': "Merr oferta",
            'sr': "Добиј понуде",
            'sv': "Få erbjudanden",
            'tr': "Teklif al",
            'uk': "Отримати пропозиції"
        }
    }
    
    try:
        # Connect to database
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        # Prepare upsert query
        upsert_query = sql.SQL("""
            INSERT INTO translations (lang, key, value)
            VALUES (%s, %s, %s)
            ON CONFLICT (lang, key) 
            DO UPDATE SET 
                value = EXCLUDED.value
        """)
        
        rows_upserted = 0
        
        # Execute upserts
        for key, lang_values in translations.items():
            for lang, value in lang_values.items():
                cursor.execute(upsert_query, (lang, key, value))
                rows_upserted += 1
        
        # Commit transaction
        conn.commit()
        
        print(f"Successfully upserted {rows_upserted} translation rows")
        
    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
