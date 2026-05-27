from apps.api.database import SessionLocal
from apps.api.models import Translation

def seed():
    db = SessionLocal()
    try:
        rows = [
            ("bg", "provider_dashboard.btn_view_profile", "Виж публичната си страница!"),
            ("cs", "provider_dashboard.btn_view_profile", "Zobrazit svou veřejnou stránku"),
            ("da", "provider_dashboard.btn_view_profile", "Se din offentlige side"),
            ("de", "provider_dashboard.btn_view_profile", "Öffentliche Seite ansehen"),
            ("el", "provider_dashboard.btn_view_profile", "Δείτε τη δημόσια σελίδα σας"),
            ("en", "provider_dashboard.btn_view_profile", "View your public page"),
            ("es", "provider_dashboard.btn_view_profile", "Ver tu página pública"),
            ("et", "provider_dashboard.btn_view_profile", "Vaata oma avalikku lehte"),
            ("fi", "provider_dashboard.btn_view_profile", "Katso julkinen sivusi"),
            ("fr", "provider_dashboard.btn_view_profile", "Voir ma page publique"),
            ("ga", "provider_dashboard.btn_view_profile", "Féach ar do leathanach poiblí"),
            ("hr", "provider_dashboard.btn_view_profile", "Pogledaj svoju javnu stranicu"),
            ("hu", "provider_dashboard.btn_view_profile", "Nyilvános oldalam megtekintése"),
            ("is", "provider_dashboard.btn_view_profile", "Skoða opinbera síðuna þína"),
            ("it", "provider_dashboard.btn_view_profile", "Visualizza la tua pagina pubblica"),
            ("lb", "provider_dashboard.btn_view_profile", "Ëffentlech Säit ukucken"),
            ("lt", "provider_dashboard.btn_view_profile", "Peržiūrėti viešą puslapį"),
            ("lv", "provider_dashboard.btn_view_profile", "Skatīt savu publisko lapu"),
            ("mk", "provider_dashboard.btn_view_profile", "Погледни ја јавната страница"),
            ("mt", "provider_dashboard.btn_view_profile", "Ara l-paġna pubblika tiegħek"),
            ("nl", "provider_dashboard.btn_view_profile", "Bekijk je publieke pagina"),
            ("no", "provider_dashboard.btn_view_profile", "Se din offentlige side"),
            ("pl", "provider_dashboard.btn_view_profile", "Zobacz swoją publiczną stronę"),
            ("pt", "provider_dashboard.btn_view_profile", "Ver minha página pública"),
            ("pt-PT", "provider_dashboard.btn_view_profile", "Ver a minha página pública"),
            ("ro", "provider_dashboard.btn_view_profile", "Vizualizează pagina ta publică"),
            ("ru", "provider_dashboard.btn_view_profile", "Посмотреть публичную страницу"),
            ("sk", "provider_dashboard.btn_view_profile", "Zobraziť svoju verejnú stránku"),
            ("sl", "provider_dashboard.btn_view_profile", "Oglejte si svojo javno stran"),
            ("sq", "provider_dashboard.btn_view_profile", "Shiko faqen tënde publike"),
            ("sr", "provider_dashboard.btn_view_profile", "Погледај своју јавну страницу"),
            ("sv", "provider_dashboard.btn_view_profile", "Visa din offentliga sida"),
            ("tr", "provider_dashboard.btn_view_profile", "Herkese açık sayfanı gör"),
            ("uk", "provider_dashboard.btn_view_profile", "Переглянути публічну сторінку"),
        ]
        for lang, key, value in rows:
            existing = db.query(Translation).filter_by(lang=lang, key=key).first()
            if existing:
                existing.value = value
            else:
                db.add(Translation(lang=lang, key=key, value=value))
        db.commit()
        print(f"Seeded {len(rows)} translations for btn_view_profile")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
