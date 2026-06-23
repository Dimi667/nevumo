"""
Seed script: wizard_welcome_heading and wizard_welcome_subtitle translation keys (34 languages)
Idempotent — safe to run multiple times.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)
))))

from sqlalchemy import text
from apps.api.database import SessionLocal

TRANSLATIONS = {
    "wizard_welcome_heading": {
        "bg": "Добре дошли!",
        "cs": "Vítejte!",
        "da": "Velkommen!",
        "de": "Willkommen!",
        "el": "Καλώς ορίσατε!",
        "en": "Welcome!",
        "es": "¡Bienvenido!",
        "et": "Tere tulemast!",
        "fi": "Tervetuloa!",
        "fr": "Bienvenue !",
        "ga": "Fáilte!",
        "hr": "Dobrodošli!",
        "hu": "Üdvözöljük!",
        "is": "Velkominn!",
        "it": "Benvenuto!",
        "lb": "Wëllkomm!",
        "lt": "Sveiki!",
        "lv": "Laipni lūdzam!",
        "mk": "Добредојдовте!",
        "mt": "Merħba!",
        "nl": "Welkom!",
        "no": "Velkommen!",
        "pl": "Witamy!",
        "pt": "Bem-vindo!",
        "pt-PT": "Bem-vindo!",
        "ro": "Bun venit!",
        "ru": "Добро пожаловать!",
        "sk": "Vitajte!",
        "sl": "Dobrodošli!",
        "sq": "Mirë se vini!",
        "sr": "Добродошли!",
        "sv": "Välkommen!",
        "tr": "Hoş geldiniz!",
        "uk": "Ласкаво просимо!",
    },
    "wizard_welcome_subtitle": {
        "bg": "Добавете снимка, описание и после услуги за да получавате клиенти",
        "cs": "Přidejte fotografii, popis a poté služby, abyste začali přijímat klienty",
        "da": "Tilføj et foto, beskrivelse og derefter ydelser for at begynde at modtage kunder",
        "de": "Fügen Sie ein Foto, eine Beschreibung und dann Dienstleistungen hinzu, um Kunden zu erhalten",
        "el": "Προσθέστε φωτογραφία, περιγραφή και στη συνέχεια υπηρεσίες για να αρχίσετε να λαμβάνετε πελάτες",
        "en": "Add a photo, description and then services to start receiving clients",
        "es": "Añade una foto, descripción y luego servicios para empezar a recibir clientes",
        "et": "Lisage foto, kirjeldus ja seejärel teenused, et hakata kliente saama",
        "fi": "Lisää kuva, kuvaus ja sitten palvelut aloittaaksesi asiakkaiden vastaanottamisen",
        "fr": "Ajoutez une photo, une description puis des services pour commencer à recevoir des clients",
        "ga": "Cuir grianghraf, cur síos agus ansin seirbhísí leis chun tosú ag fáil cliantanna",
        "hr": "Dodajte fotografiju, opis i zatim usluge kako biste počeli primati klijente",
        "hu": "Adjon hozzá fényképet, leírást, majd szolgáltatásokat, hogy ügyfeleket fogadhasson",
        "is": "Bættu við mynd, lýsingu og síðan þjónustu til að byrja að fá viðskiptavini",
        "it": "Aggiungi una foto, una descrizione e poi i servizi per iniziare a ricevere clienti",
        "lb": "Fügt e Foto, eng Beschreiwung an dann Servicer bäi fir Clienten ze kréien",
        "lt": "Pridėkite nuotrauką, aprašymą ir vėliau paslaugas, kad pradėtumėte gauti klientų",
        "lv": "Pievienojiet fotoattēlu, aprakstu un pēc tam pakalpojumus, lai sāktu saņemt klientus",
        "mk": "Додадете фотографија, опис и потоа услуги за да почнете да добивате клиенти",
        "mt": "Żid ritratt, deskrizzjoni u mbagħad servizzi biex tibda tirċievi klijenti",
        "nl": "Voeg een foto, beschrijving en dan diensten toe om klanten te ontvangen",
        "no": "Legg til et bilde, beskrivelse og deretter tjenester for å begynne å motta kunder",
        "pl": "Dodaj zdjęcie, opis, a następnie usługi, aby zacząć otrzymywać klientów",
        "pt": "Adicione uma foto, descrição e depois serviços para começar a receber clientes",
        "pt-PT": "Adicione uma foto, descrição e depois serviços para começar a receber clientes",
        "ro": "Adăugați o fotografie, descriere și apoi servicii pentru a începe să primiți clienți",
        "ru": "Добавьте фото, описание и затем услуги, чтобы начать получать клиентов",
        "sk": "Pridajte fotografiu, popis a potom služby, aby ste začali prijímať klientov",
        "sl": "Dodajte fotografijo, opis in nato storitve, da začnete prejemati stranke",
        "sq": "Shtoni një foto, përshkrim dhe më pas shërbime për të filluar të merrni klientë",
        "sr": "Додајте фотографију, опис и затим услуге да бисте почели да примате клијенте",
        "sv": "Lägg till ett foto, beskrivning och sedan tjänster för att börja ta emot kunder",
        "tr": "Müşteri almaya başlamak için fotoğraf, açıklama ve ardından hizmetler ekleyin",
        "uk": "Додайте фото, опис і потім послуги, щоб почати отримувати клієнтів",
    },
}

def seed():
    db = SessionLocal()
    try:
        inserted = 0
        updated = 0
        for key_name, lang_values in TRANSLATIONS.items():
            for lang, value in lang_values.items():
                result = db.execute(
                    text("""
                        INSERT INTO translations (lang, key, value)
                        VALUES (:lang, :key, :value)
                        ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
                    """),
                    {"lang": lang, "key": f"provider_dashboard.{key_name}", "value": value}
                )
                if result.rowcount == 1:
                    inserted += 1
                else:
                    updated += 1
        db.commit()
        print(f"Done: {inserted} inserted, {updated} updated")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
