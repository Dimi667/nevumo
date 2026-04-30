from sqlalchemy import text
import redis

from apps.api.database import SessionLocal
from apps.api.config import settings

TRANSLATIONS = [
    ("bg", "city_selection.heading", "В кой град търсиш услуга?"),
    ("cs", "city_selection.heading", "Ve kterém městě hledáte službu?"),
    ("da", "city_selection.heading", "I hvilken by leder du efter en service?"),
    ("de", "city_selection.heading", "In welcher Stadt suchst du einen Service?"),
    ("el", "city_selection.heading", "Σε ποια πόλη ψάχνεις υπηρεσία;"),
    ("en", "city_selection.heading", "In which city are you looking for a service?"),
    ("es", "city_selection.heading", "¿En qué ciudad buscas un servicio?"),
    ("et", "city_selection.heading", "Millises linnas otsite teenust?"),
    ("fi", "city_selection.heading", "Mistä kaupungista etsit palvelua?"),
    ("fr", "city_selection.heading", "Dans quelle ville cherchez-vous un service ?"),
    ("ga", "city_selection.heading", "Cén cathair ina bhfuil tú ag lorg seirbhíse?"),
    ("hr", "city_selection.heading", "U kojem gradu tražiš uslugu?"),
    ("hu", "city_selection.heading", "Melyik városban keresel szolgáltatást?"),
    ("is", "city_selection.heading", "Í hvaða borg ertu að leita að þjónustu?"),
    ("it", "city_selection.heading", "In quale città cerchi un servizio?"),
    ("lb", "city_selection.heading", "A wéi enger Stad sichts du no engem Service?"),
    ("lt", "city_selection.heading", "Kuriame mieste ieškote paslaugos?"),
    ("lv", "city_selection.heading", "Kurā pilsētā meklējat pakalpojumu?"),
    ("mk", "city_selection.heading", "Во кој град барате услуга?"),
    ("mt", "city_selection.heading", "F'liema belt qiegħed tfittex servizz?"),
    ("nl", "city_selection.heading", "In welke stad zoek je een dienst?"),
    ("no", "city_selection.heading", "I hvilken by leter du etter en tjeneste?"),
    ("pl", "city_selection.heading", "W którym mieście szukasz usługi?"),
    ("pt", "city_selection.heading", "Em qual cidade você está procurando um serviço?"),
    ("pt-PT", "city_selection.heading", "Em que cidade está à procura de um serviço?"),
    ("ro", "city_selection.heading", "În ce oraș cauți un serviciu?"),
    ("ru", "city_selection.heading", "В каком городе вы ищете услугу?"),
    ("sk", "city_selection.heading", "V ktorom meste hľadáte službu?"),
    ("sl", "city_selection.heading", "V katerem mestu iščeš storitev?"),
    ("sq", "city_selection.heading", "Në cilën qytet po kërkoni shërbim?"),
    ("sr", "city_selection.heading", "U kom gradu tražiš uslugu?"),
    ("sv", "city_selection.heading", "I vilken stad letar du efter en tjänst?"),
    ("tr", "city_selection.heading", "Hangi şehirde hizmet arıyorsunuz?"),
    ("uk", "city_selection.heading", "У якому місті ви шукаєте послугу?"),

    ("bg", "city_selection.empty_state", "Очаквай скоро"),
    ("cs", "city_selection.empty_state", "Již brzy"),
    ("da", "city_selection.empty_state", "Kommer snart"),
    ("de", "city_selection.empty_state", "Demnächst verfügbar"),
    ("el", "city_selection.empty_state", "Έρχεται σύντομα"),
    ("en", "city_selection.empty_state", "Coming soon"),
    ("es", "city_selection.empty_state", "Próximamente"),
    ("et", "city_selection.empty_state", "Tulemas peagi"),
    ("fi", "city_selection.empty_state", "Tulossa pian"),
    ("fr", "city_selection.empty_state", "Bientôt disponible"),
    ("ga", "city_selection.empty_state", "Ag teacht go luath"),
    ("hr", "city_selection.empty_state", "Uskoro dostupno"),
    ("hu", "city_selection.empty_state", "Hamarosan"),
    ("is", "city_selection.empty_state", "Kemur fljótlega"),
    ("it", "city_selection.empty_state", "Prossimamente"),
    ("lb", "city_selection.empty_state", "Kënnt geschwënn"),
    ("lt", "city_selection.empty_state", "Netrukus"),
    ("lv", "city_selection.empty_state", "Drīzumā"),
    ("mk", "city_selection.empty_state", "Наскоро"),
    ("mt", "city_selection.empty_state", "Dalwaqt"),
    ("nl", "city_selection.empty_state", "Binnenkort beschikbaar"),
    ("no", "city_selection.empty_state", "Kommer snart"),
    ("pl", "city_selection.empty_state", "Wkrótce"),
    ("pt", "city_selection.empty_state", "Em breve"),
    ("pt-PT", "city_selection.empty_state", "Em breve"),
    ("ro", "city_selection.empty_state", "În curând"),
    ("ru", "city_selection.empty_state", "Скоро"),
    ("sk", "city_selection.empty_state", "Čoskoro"),
    ("sl", "city_selection.empty_state", "Kmalu"),
    ("sq", "city_selection.empty_state", "Së shpejti"),
    ("sr", "city_selection.empty_state", "Uskoro"),
    ("sv", "city_selection.empty_state", "Kommer snart"),
    ("tr", "city_selection.empty_state", "Yakında"),
    ("uk", "city_selection.empty_state", "Незабаром"),

    ("bg", "city_selection.nav_link", "Стани специалист"),
    ("cs", "city_selection.nav_link", "Staňte se specialistou"),
    ("da", "city_selection.nav_link", "Bliv specialist"),
    ("de", "city_selection.nav_link", "Spezialist werden"),
    ("el", "city_selection.nav_link", "Γίνε ειδικός"),
    ("en", "city_selection.nav_link", "Become a specialist"),
    ("es", "city_selection.nav_link", "Conviértete en especialista"),
    ("et", "city_selection.nav_link", "Saa spetsialistiks"),
    ("fi", "city_selection.nav_link", "Tule asiantuntijaksi"),
    ("fr", "city_selection.nav_link", "Devenir spécialiste"),
    ("ga", "city_selection.nav_link", "Bí i do speisialtóir"),
    ("hr", "city_selection.nav_link", "Postani stručnjak"),
    ("hu", "city_selection.nav_link", "Légy szakember"),
    ("is", "city_selection.nav_link", "Vertu sérfræðingur"),
    ("it", "city_selection.nav_link", "Diventa uno specialista"),
    ("lb", "city_selection.nav_link", "Spezialist ginn"),
    ("lt", "city_selection.nav_link", "Tapk specialistu"),
    ("lv", "city_selection.nav_link", "Kļūsti par speciālistu"),
    ("mk", "city_selection.nav_link", "Стани специјалист"),
    ("mt", "city_selection.nav_link", "Isir speċjalista"),
    ("nl", "city_selection.nav_link", "Word specialist"),
    ("no", "city_selection.nav_link", "Bli spesialist"),
    ("pl", "city_selection.nav_link", "Zostań specjalistą"),
    ("pt", "city_selection.nav_link", "Torne-se um especialista"),
    ("pt-PT", "city_selection.nav_link", "Torne-se um especialista"),
    ("ro", "city_selection.nav_link", "Devino specialist"),
    ("ru", "city_selection.nav_link", "Стать специалистом"),
    ("sk", "city_selection.nav_link", "Staňte sa špecialistom"),
    ("sl", "city_selection.nav_link", "Postani strokovnjak"),
    ("sq", "city_selection.nav_link", "Bëhu specialist"),
    ("sr", "city_selection.nav_link", "Postani stručnjak"),
    ("sv", "city_selection.nav_link", "Bli specialist"),
    ("tr", "city_selection.nav_link", "Uzman ol"),
    ("uk", "city_selection.nav_link", "Стань фахівцем"),

    ("bg", "city_selection.footer_text", "Nevumo — Свързваме те с местни специалисти"),
    ("cs", "city_selection.footer_text", "Nevumo — Spojujeme vás s místními specialisty"),
    ("da", "city_selection.footer_text", "Nevumo — Vi forbinder dig med lokale specialister"),
    ("de", "city_selection.footer_text", "Nevumo — Wir verbinden dich mit lokalen Spezialisten"),
    ("el", "city_selection.footer_text", "Nevumo — Σε συνδέουμε με τοπικούς ειδικούς"),
    ("en", "city_selection.footer_text", "Nevumo — Connecting you with local specialists"),
    ("es", "city_selection.footer_text", "Nevumo — Te conectamos con especialistas locales"),
    ("et", "city_selection.footer_text", "Nevumo — Ühendame teid kohalike spetsialistidega"),
    ("fi", "city_selection.footer_text", "Nevumo — Yhdistämme sinut paikallisiin asiantuntijoihin"),
    ("fr", "city_selection.footer_text", "Nevumo — Nous vous connectons avec des spécialistes locaux"),
    ("ga", "city_selection.footer_text", "Nevumo — Nascaimid thú le speisialtóirí áitiúla"),
    ("hr", "city_selection.footer_text", "Nevumo — Povezujemo vas s lokalnim stručnjacima"),
    ("hu", "city_selection.footer_text", "Nevumo — Összekötjük a helyi szakemberekkel"),
    ("is", "city_selection.footer_text", "Nevumo — Við tengjum þig við staðbundna sérfræðinga"),
    ("it", "city_selection.footer_text", "Nevumo — Ti mettiamo in contatto con specialisti locali"),
    ("lb", "city_selection.footer_text", "Nevumo — Mir verbannen dech mat lokale Spezialisten"),
    ("lt", "city_selection.footer_text", "Nevumo — Jungiam jus su vietiniais specialistais"),
    ("lv", "city_selection.footer_text", "Nevumo — Savienojam jūs ar vietējiem speciālistiem"),
    ("mk", "city_selection.footer_text", "Nevumo — Те поврзуваме со локални специјалисти"),
    ("mt", "city_selection.footer_text", "Nevumo — Inqabbduk ma' speċjalisti lokali"),
    ("nl", "city_selection.footer_text", "Nevumo — Wij verbinden jou met lokale specialisten"),
    ("no", "city_selection.footer_text", "Nevumo — Vi kobler deg med lokale spesialister"),
    ("pl", "city_selection.footer_text", "Nevumo — Łączymy cię z lokalnymi specjalistami"),
    ("pt", "city_selection.footer_text", "Nevumo — Conectando você com especialistas locais"),
    ("pt-PT", "city_selection.footer_text", "Nevumo — A conectá-lo com especialistas locais"),
    ("ro", "city_selection.footer_text", "Nevumo — Te conectăm cu specialiști locali"),
    ("ru", "city_selection.footer_text", "Nevumo — Соединяем вас с местными специалистами"),
    ("sk", "city_selection.footer_text", "Nevumo — Spájame vás s miestnymi špecialistami"),
    ("sl", "city_selection.footer_text", "Nevumo — Povezujemo vas z lokalnimi strokovnjaki"),
    ("sq", "city_selection.footer_text", "Nevumo — Ju lidhim me specialistë lokalë"),
    ("sr", "city_selection.footer_text", "Nevumo — Povezujemo vas sa lokalnim stručnjacima"),
    ("sv", "city_selection.footer_text", "Nevumo — Vi kopplar dig med lokala specialister"),
    ("tr", "city_selection.footer_text", "Nevumo — Sizi yerel uzmanlarla buluşturuyoruz"),
    ("uk", "city_selection.footer_text", "Nevumo — Пов'язуємо вас із місцевими фахівцями"),
]

def main():
    db = SessionLocal()
    try:
        insert_translations(db, TRANSLATIONS)
        flush_redis_cache()
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
    print("Seeded 102 rows — Part 3 complete")

def flush_redis_cache() -> None:
    r = redis.from_url(settings.REDIS_URL)
    keys = r.keys("translations:*:city_selection")
    if keys:
        r.delete(*keys)
        print(f"Flushed {len(keys)} Redis cache keys")

if __name__ == "__main__":
    main()
