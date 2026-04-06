#!/usr/bin/env python3
"""
Script to upsert translation keys for category form part 2
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
        'category.how_step_1': {
            'bg': "Опиши нуждата си",
            'cs': "Popište, co potřebujete",
            'da': "Beskriv hvad du har brug for",
            'de': "Beschreibe was du brauchst",
            'el': "Περίγραψε τι χρειάζεσαι",
            'en': "Describe what you need",
            'es': "Describe lo que necesitas",
            'et': "Kirjeldage, mida vajate",
            'fi': "Kuvaile mitä tarvitset",
            'fr': "Décrivez ce dont vous avez besoin",
            'ga': "Déan cur síos ar a bhfuil uait",
            'hr': "Opišite što trebate",
            'hu': "Írja le, mire van szüksége",
            'is': "Lýstu því sem þú þarft",
            'it': "Descrivi di cosa hai bisogno",
            'lb': "Beschreift wat Dir braucht",
            'lt': "Apibūdinkite, ko jums reikia",
            'lv': "Aprakstiet, kas jums nepieciešams",
            'mk': "Опишете ја вашата потреба",
            'mt': "Iddeskrivi x'għandek bżonn",
            'nl': "Beschrijf wat u nodig heeft",
            'no': "Beskriv hva du trenger",
            'pl': "Opisz czego potrzebujesz",
            'pt': "Descreva o que você precisa",
            'pt-PT': "Descreva o que precisa",
            'ro': "Descrie ce ai nevoie",
            'ru': "Опишите что вам нужно",
            'sk': "Opíšte, čo potrebujete",
            'sl': "Opišite, kaj potrebujete",
            'sq': "Përshkruaj çfarë ke nevojë",
            'sr': "Опишите шта вам треба",
            'sv': "Beskriv vad du behöver",
            'tr': "İhtiyacınızı açıklayın",
            'uk': "Опишіть що вам потрібно"
        },
        'category.how_step_2': {
            'bg': "Специалистите те контактуват",
            'cs': "Poskytovatelé vás kontaktují",
            'da': "Udbydere kontakter dig",
            'de': "Anbieter kontaktieren dich",
            'el': "Οι πάροχοι επικοινωνούν μαζί σου",
            'en': "Providers contact you",
            'es': "Los proveedores te contactan",
            'et': "Teenusepakkujad võtavad teiega ühendust",
            'fi': "Palveluntarjoajat ottavat sinuun yhteyttä",
            'fr': "Les prestataires vous contactent",
            'ga': "Déanann soláthróirí teagmháil leat",
            'hr': "Pružatelji vas kontaktiraju",
            'hu': "A szolgáltatók felveszik Önnel a kapcsolatot",
            'is': "Þjónustuaðilar hafa samband við þig",
            'it': "I fornitori ti contattano",
            'lb': "Ubidder kontaktéieren Iech",
            'lt': "Tiekėjai susisiekia su jumis",
            'lv': "Pakalpojumu sniedzēji sazinās ar jums",
            'mk': "Давателите ве контактираат",
            'mt': "Il-fornituri jikkuntattjawk",
            'nl': "Aanbieders nemen contact met u op",
            'no': "Leverandører kontakter deg",
            'pl': "Specjaliści kontaktują się z Tobą",
            'pt': "Prestadores entram em contato",
            'pt-PT': "Prestadores entram em contacto",
            'ro': "Furnizorii te contactează",
            'ru': "Специалисты связываются с вами",
            'sk': "Poskytovatelia vás kontaktujú",
            'sl': "Ponudniki vas kontaktirajo",
            'sq': "Ofruesit ju kontaktojnë",
            'sr': "Пружаоци вас контактирају",
            'sv': "Leverantörer kontaktar dig",
            'tr': "Sağlayıcılar sizi arar",
            'uk': "Спеціалісти зв'яжуться з вами"
        },
        'category.how_step_3': {
            'bg': "Избери най-добрата оферта",
            'cs': "Vyberte nejlepší nabídku",
            'da': "Vælg det bedste tilbud",
            'de': "Wähle das beste Angebot",
            'el': "Επίλεξε την καλύτερη προσφορά",
            'en': "Choose the best offer",
            'es': "Elige la mejor oferta",
            'et': "Valige parim pakkumine",
            'fi': "Valitse paras tarjous",
            'fr': "Choisissez la meilleure offre",
            'ga': "Roghnaigh an tairiscint is fearr",
            'hr': "Odaberite najbolju ponudu",
            'hu': "Válassza a legjobb ajánlatot",
            'is': "Veldu besta tilboðið",
            'it': "Scegli l'offerta migliore",
            'lb': "Wielt dat bescht Ubidder",
            'lt': "Pasirinkite geriausią pasiūlymą",
            'lv': "Izvēlieties labāko piedāvājumu",
            'mk': "Изберете ја најдобрата понуда",
            'mt': "Agħżel l-aħjar offerta",
            'nl': "Kies het beste aanbod",
            'no': "Velg det beste tilbudet",
            'pl': "Wybierz najlepszą ofertę",
            'pt': "Escolha a melhor oferta",
            'pt-PT': "Escolha a melhor oferta",
            'ro': "Alege cea mai bună ofertă",
            'ru': "Выберите лучшее предложение",
            'sk': "Vyberte najlepšiu ponuku",
            'sl': "Izberite najboljšo ponudbo",
            'sq': "Zgjidhni ofertën më të mirë",
            'sr': "Изаберите најбољу понуду",
            'sv': "Välj det bästa erbjudandet",
            'tr': "En iyi teklifi seçin",
            'uk': "Оберіть найкращу пропозицію"
        },
        'category.what_need_label': {
            'bg': "Какво ви трябва?",
            'cs': "Co potřebujete?",
            'da': "Hvad har du brug for?",
            'de': "Was benötigst du?",
            'el': "Τι χρειάζεστε;",
            'en': "What do you need?",
            'es': "¿Qué necesitas?",
            'et': "Mida vajate?",
            'fi': "Mitä tarvitset?",
            'fr': "De quoi avez-vous besoin?",
            'ga': "Cad atá uait?",
            'hr': "Što vam treba?",
            'hu': "Mire van szüksége?",
            'is': "Hvað þarftu?",
            'it': "Di cosa hai bisogno?",
            'lb': "Wat braucht Dir?",
            'lt': "Ko jums reikia?",
            'lv': "Kas jums nepieciešams?",
            'mk': "Што ви треба?",
            'mt': "X'għandek bżonn?",
            'nl': "Wat heeft u nodig?",
            'no': "Hva trenger du?",
            'pl': "Czego potrzebujesz?",
            'pt': "O que você precisa?",
            'pt-PT': "Do que precisa?",
            'ro': "De ce ai nevoie?",
            'ru': "Что вам нужно?",
            'sk': "Čo potrebujete?",
            'sl': "Kaj potrebujete?",
            'sq': "Çfarë keni nevojë?",
            'sr': "Шта вам треба?",
            'sv': "Vad behöver du?",
            'tr': "Neye ihtiyacınız var?",
            'uk': "Що вам потрібно?"
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
