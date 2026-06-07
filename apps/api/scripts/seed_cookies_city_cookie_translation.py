import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from apps.api.database import SessionLocal
from apps.api.models import Translation

translations = [
    ("bg", "cookies.s5_p_city_cookie", "Съхранява избрания от потребителя град за персонализация на началната страница"),
    ("cs", "cookies.s5_p_city_cookie", "Ukládá město vybrané uživatelem pro personalizaci domovské stránky"),
    ("da", "cookies.s5_p_city_cookie", "Gemmer den by, brugeren har valgt, til personalisering af startsiden"),
    ("de", "cookies.s5_p_city_cookie", "Speichert die vom Nutzer gewählte Stadt zur Personalisierung der Startseite"),
    ("el", "cookies.s5_p_city_cookie", "Αποθηκεύει την πόλη που επέλεξε ο χρήστης για εξατομίκευση της αρχικής σελίδας"),
    ("en", "cookies.s5_p_city_cookie", "Stores the city selected by the user for homepage personalisation"),
    ("es", "cookies.s5_p_city_cookie", "Guarda la ciudad seleccionada por el usuario para personalizar la página de inicio"),
    ("et", "cookies.s5_p_city_cookie", "Salvestab kasutaja valitud linna avalehe isikupärastamiseks"),
    ("fi", "cookies.s5_p_city_cookie", "Tallentaa käyttäjän valitseman kaupungin etusivun personointia varten"),
    ("fr", "cookies.s5_p_city_cookie", "Enregistre la ville sélectionnée par l'utilisateur pour personnaliser la page d'accueil"),
    ("ga", "cookies.s5_p_city_cookie", "Stórálann an chathair a roghnaíonn an t-úsáideoir chun an leathanach baile a phearsantú"),
    ("hr", "cookies.s5_p_city_cookie", "Sprema grad koji je korisnik odabrao za personalizaciju početne stranice"),
    ("hu", "cookies.s5_p_city_cookie", "Elmenti a felhasználó által kiválasztott várost a kezdőlap személyre szabásához"),
    ("is", "cookies.s5_p_city_cookie", "Geymir borgina sem notandinn velur til að sérsníða heimasíðuna"),
    ("it", "cookies.s5_p_city_cookie", "Memorizza la città selezionata dall'utente per personalizzare la homepage"),
    ("lb", "cookies.s5_p_city_cookie", "Späichert d'Stad, déi vum Benotzer gewielt gouf, fir d'Haaptsäit ze personaliséieren"),
    ("lt", "cookies.s5_p_city_cookie", "Išsaugo vartotojo pasirinktą miestą pagrindinio puslapio personalizavimui"),
    ("lv", "cookies.s5_p_city_cookie", "Saglabā lietotāja izvēlēto pilsētu sākumlapas personalizēšanai"),
    ("mk", "cookies.s5_p_city_cookie", "Го зачувува градот избран од корисникот за персонализација на почетната страница"),
    ("mt", "cookies.s5_p_city_cookie", "Jaħżen il-belt magħżula mill-utent għall-personalizzazzjoni tal-paġna ewlenija"),
    ("nl", "cookies.s5_p_city_cookie", "Slaat de door de gebruiker geselecteerde stad op voor personalisatie van de startpagina"),
    ("no", "cookies.s5_p_city_cookie", "Lagrer byen brukeren har valgt for å tilpasse startsiden"),
    ("pl", "cookies.s5_p_city_cookie", "Przechowuje miasto wybrane przez użytkownika do personalizacji strony głównej"),
    ("pt", "cookies.s5_p_city_cookie", "Armazena a cidade selecionada pelo usuário para personalização da página inicial"),
    ("pt-PT", "cookies.s5_p_city_cookie", "Armazena a cidade selecionada pelo utilizador para personalização da página inicial"),
    ("ro", "cookies.s5_p_city_cookie", "Salvează orașul selectat de utilizator pentru personalizarea paginii principale"),
    ("ru", "cookies.s5_p_city_cookie", "Сохраняет город, выбранный пользователем, для персонализации главной страницы"),
    ("sk", "cookies.s5_p_city_cookie", "Ukladá mesto vybrané používateľom na personalizáciu domovskej stránky"),
    ("sl", "cookies.s5_p_city_cookie", "Shrani mesto, ki ga je izbral uporabnik, za personalizacijo domače strani"),
    ("sq", "cookies.s5_p_city_cookie", "Ruan qytetin e zgjedhur nga përdoruesi për personalizimin e faqes kryesore"),
    ("sr", "cookies.s5_p_city_cookie", "Чува град који је корисник изабрао за персонализацију почетне странице"),
    ("sv", "cookies.s5_p_city_cookie", "Sparar den stad som användaren har valt för personalisering av startsidan"),
    ("tr", "cookies.s5_p_city_cookie", "Kullanıcının seçtiği şehri ana sayfa kişiselleştirmesi için saklar"),
    ("uk", "cookies.s5_p_city_cookie", "Зберігає місто, обране користувачем, для персоналізації головної сторінки"),
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
        print(f"✅ Seeded {len(translations)} translations for cookies.s5_p_city_cookie")
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed()
