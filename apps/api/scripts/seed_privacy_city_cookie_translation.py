import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from apps.api.database import SessionLocal
from apps.api.models import Translation

translations = [
    ("bg", "privacy.t4_purpose_city_cookie", "Съхранява избрания от потребителя град за персонализация на началната страница"),
    ("cs", "privacy.t4_purpose_city_cookie", "Ukládá město vybrané uživatelem pro personalizaci domovské stránky"),
    ("da", "privacy.t4_purpose_city_cookie", "Gemmer den by, brugeren har valgt, til personalisering af startsiden"),
    ("de", "privacy.t4_purpose_city_cookie", "Speichert die vom Nutzer gewählte Stadt zur Personalisierung der Startseite"),
    ("el", "privacy.t4_purpose_city_cookie", "Αποθηκεύει την πόλη που επέλεξε ο χρήστης για εξατομίκευση της αρχικής σελίδας"),
    ("en", "privacy.t4_purpose_city_cookie", "Stores the city selected by the user for homepage personalisation"),
    ("es", "privacy.t4_purpose_city_cookie", "Guarda la ciudad seleccionada por el usuario para personalizar la página de inicio"),
    ("et", "privacy.t4_purpose_city_cookie", "Salvestab kasutaja valitud linna avalehe isikupärastamiseks"),
    ("fi", "privacy.t4_purpose_city_cookie", "Tallentaa käyttäjän valitseman kaupungin etusivun personointia varten"),
    ("fr", "privacy.t4_purpose_city_cookie", "Enregistre la ville sélectionnée par l'utilisateur pour personnaliser la page d'accueil"),
    ("ga", "privacy.t4_purpose_city_cookie", "Stórálann an chathair a roghnaíonn an t-úsáideoir chun an leathanach baile a phearsantú"),
    ("hr", "privacy.t4_purpose_city_cookie", "Sprema grad koji je korisnik odabrao za personalizaciju početne stranice"),
    ("hu", "privacy.t4_purpose_city_cookie", "Elmenti a felhasználó által kiválasztott várost a kezdőlap személyre szabásához"),
    ("is", "privacy.t4_purpose_city_cookie", "Geymir borgina sem notandinn velur til að sérsníða heimasíðuna"),
    ("it", "privacy.t4_purpose_city_cookie", "Memorizza la città selezionata dall'utente per personalizzare la homepage"),
    ("lb", "privacy.t4_purpose_city_cookie", "Späichert d'Stad, déi vum Benotzer gewielt gouf, fir d'Haaptsäit ze personaliséieren"),
    ("lt", "privacy.t4_purpose_city_cookie", "Išsaugo vartotojo pasirinktą miestą pagrindinio puslapio personalizavimui"),
    ("lv", "privacy.t4_purpose_city_cookie", "Saglabā lietotāja izvēlēto pilsētu sākumlapas personalizēšanai"),
    ("mk", "privacy.t4_purpose_city_cookie", "Го зачувува градот избран од корисникот за персонализација на почетната страница"),
    ("mt", "privacy.t4_purpose_city_cookie", "Jaħżen il-belt magħżula mill-utent għall-personalizzazzjoni tal-paġna ewlenija"),
    ("nl", "privacy.t4_purpose_city_cookie", "Slaat de door de gebruiker geselecteerde stad op voor personalisatie van de startpagina"),
    ("no", "privacy.t4_purpose_city_cookie", "Lagrer byen brukeren har valgt for å tilpasse startsiden"),
    ("pl", "privacy.t4_purpose_city_cookie", "Przechowuje miasto wybrane przez użytkownika do personalizacji strony głównej"),
    ("pt", "privacy.t4_purpose_city_cookie", "Armazena a cidade selecionada pelo usuário para personalização da página inicial"),
    ("pt-PT", "privacy.t4_purpose_city_cookie", "Armazena a cidade selecionada pelo utilizador para personalização da página inicial"),
    ("ro", "privacy.t4_purpose_city_cookie", "Salvează orașul selectat de utilizator pentru personalizarea paginii principale"),
    ("ru", "privacy.t4_purpose_city_cookie", "Сохраняет город, выбранный пользователем, для персонализации главной страницы"),
    ("sk", "privacy.t4_purpose_city_cookie", "Ukladá mesto vybrané používateľom na personalizáciu domovskej stránky"),
    ("sl", "privacy.t4_purpose_city_cookie", "Shrani mesto, ki ga je izbral uporabnik, za personalizacijo domače strani"),
    ("sq", "privacy.t4_purpose_city_cookie", "Ruan qytetin e zgjedhur nga përdoruesi për personalizimin e faqes kryesore"),
    ("sr", "privacy.t4_purpose_city_cookie", "Чува град који је корисник изабрао за персонализацију почетне странице"),
    ("sv", "privacy.t4_purpose_city_cookie", "Sparar den stad som användaren har valt för personalisering av startsidan"),
    ("tr", "privacy.t4_purpose_city_cookie", "Kullanıcının seçtiği şehri ana sayfa kişiselleştirmesi için saklar"),
    ("uk", "privacy.t4_purpose_city_cookie", "Зберігає місто, обране користувачем, для персоналізації головної сторінки"),
]

def seed():
    db = SessionLocal()
    try:
        for lang, key, value in translations:
            obj = db.query(Translation).filter_by(lang=lang, key=key).first()
            if obj:
                obj.value = value
            else:
                db.add(Translation(lang=lang, key=key, value=value))
        db.commit()
        print(f"✅ Seeded {len(translations)} translations for privacy.t4_purpose_city_cookie")
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed()
