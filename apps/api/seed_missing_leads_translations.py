#!/usr/bin/env python3
"""
Seed missing translation keys for provider dashboard leads page.
Keys: label_search, placeholder_search_leads
Namespace: provider_dashboard
Languages: 34
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text

NAMESPACE = "provider_dashboard"

LANGS = [
    "en", "bg", "cs", "da", "de", "el", "es", "et", "fi", "fr", "ga", "hr",
    "hu", "is", "it", "lb", "lt", "lv", "mk", "mt", "nl", "no", "pl", "pt",
    "pt-PT", "ro", "ru", "sk", "sl", "sq", "sr", "sv", "tr", "uk",
]

TRANSLATIONS = {
    "label_search": {
        "en": "Search",
        "bg": "Търсене",
        "cs": "Hledat",
        "da": "Søg",
        "de": "Suche",
        "el": "Αναζήτηση",
        "es": "Buscar",
        "et": "Otsi",
        "fi": "Hae",
        "fr": "Rechercher",
        "ga": "Cuardaigh",
        "hr": "Pretraži",
        "hu": "Keresés",
        "is": "Leit",
        "it": "Cerca",
        "lb": "Sichen",
        "lt": "Paieška",
        "lv": "Meklēt",
        "mk": "Пребарај",
        "mt": "Fittex",
        "nl": "Zoeken",
        "no": "Søk",
        "pl": "Szukaj",
        "pt": "Pesquisar",
        "pt-PT": "Pesquisar",
        "ro": "Căutare",
        "ru": "Поиск",
        "sk": "Hľadať",
        "sl": "Iskanje",
        "sq": "Kërko",
        "sr": "Pretraži",
        "sv": "Sök",
        "tr": "Ara",
        "uk": "Пошук",
    },
    "placeholder_search_leads": {
        "en": "Search name, email, phone, description or notes...",
        "bg": "Търси име, имейл, телефон, описание или бележки...",
        "cs": "Hledejte jméno, e-mail, telefon, popis nebo poznámky...",
        "da": "Søg efter navn, e-mail, telefon, beskrivelse eller noter...",
        "de": "Name, E-Mail, Telefon, Beschreibung oder Notizen suchen...",
        "el": "Αναζήτηση ονόματος, email, τηλεφώνου, περιγραφής ή σημειώσεων...",
        "es": "Buscar nombre, correo, teléfono, descripción o notas...",
        "et": "Otsi nime, e-posti, telefoni, kirjeldust või märkmeid...",
        "fi": "Hae nimellä, sähköpostilla, puhelimella, kuvauksella tai muistiinpanoilla...",
        "fr": "Rechercher nom, e-mail, téléphone, description ou notes...",
        "ga": "Cuardaigh ainm, ríomhphost, guthán, cur síos nó nótaí...",
        "hr": "Pretražite ime, e-poštu, telefon, opis ili bilješke...",
        "hu": "Keresés név, e-mail, telefon, leírás vagy jegyzetek alapján...",
        "is": "Leita að nafni, netfangi, síma, lýsingu eða athugasemdum...",
        "it": "Cerca nome, email, telefono, descrizione o note...",
        "lb": "Sich no Numm, E-Mail, Telefon, Beschreiwung oder Notizen...",
        "lt": "Ieškoti pagal pavardę, el. paštą, telefoną, aprašymą ar pastabas...",
        "lv": "Meklēt pēc vārda, e-pasta, tālruņa, apraksta vai piezīmēm...",
        "mk": "Пребарајте име, е-пошта, телефон, опис или белешки...",
        "mt": "Fittex isem, email, telefon, deskrizzjoni jew noti...",
        "nl": "Zoek op naam, e-mail, telefoon, beschrijving of notities...",
        "no": "Søk etter navn, e-post, telefon, beskrivelse eller notater...",
        "pl": "Szukaj nazwy, e-maila, telefonu, opisu lub notatek...",
        "pt": "Pesquisar nome, e-mail, telefone, descrição ou notas...",
        "pt-PT": "Pesquisar nome, e-mail, telefone, descrição ou notas...",
        "ro": "Căutați nume, email, telefon, descriere sau note...",
        "ru": "Поиск по имени, email, телефону, описанию или заметкам...",
        "sk": "Hľadať meno, e-mail, telefón, popis alebo poznámky...",
        "sl": "Iskanje po imenu, e-pošti, telefonu, opisu ali zapisih...",
        "sq": "Kërko emër, email, telefon, përshkrim ose shënime...",
        "sr": "Pretražite ime, e-poštu, telefon, opis ili beleške...",
        "sv": "Sök efter namn, e-post, telefon, beskrivning eller anteckningar...",
        "tr": "İsim, e-posta, telefon, açıklama veya notlara göre ara...",
        "uk": "Пошук за іменем, email, телефоном, описом або нотатками...",
    },
}

def main():
    engine = create_engine("postgresql://nevumo:nevumo@localhost:5432/nevumo_leads")
    
    with engine.connect() as conn:
        for key_name, translations in TRANSLATIONS.items():
            full_key = f"{NAMESPACE}.{key_name}"
            print(f"Seeding {full_key}...")
            
            for lang, value in translations.items():
                # Check if key exists
                result = conn.execute(
                    text("SELECT id FROM translations WHERE key = :key AND lang = :lang"),
                    {"key": full_key, "lang": lang}
                ).fetchone()
                
                if result:
                    # Update existing
                    conn.execute(
                        text("UPDATE translations SET value = :value WHERE key = :key AND lang = :lang"),
                        {"value": value, "key": full_key, "lang": lang}
                    )
                else:
                    # Insert new
                    conn.execute(
                        text("INSERT INTO translations (key, lang, value) VALUES (:key, :lang, :value)"),
                        {"key": full_key, "lang": lang, "value": value}
                    )
        
        conn.commit()
    
    print("Done! Seeded 2 keys for 34 languages.")

if __name__ == "__main__":
    main()
