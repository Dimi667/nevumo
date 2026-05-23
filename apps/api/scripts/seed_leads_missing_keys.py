import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://nevumo:nevumo@nevumo-postgres:5432/nevumo_leads")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

TRANSLATIONS = [
    # label_cancelled_leads — "Cancelled" статус leads
    ("bg", "provider_dashboard.label_cancelled_leads", "Отказани запитвания"),
    ("cs", "provider_dashboard.label_cancelled_leads", "Zrušené poptávky"),
    ("da", "provider_dashboard.label_cancelled_leads", "Annullerede forespørgsler"),
    ("de", "provider_dashboard.label_cancelled_leads", "Stornierte Anfragen"),
    ("el", "provider_dashboard.label_cancelled_leads", "Ακυρωμένα αιτήματα"),
    ("en", "provider_dashboard.label_cancelled_leads", "Cancelled leads"),
    ("es", "provider_dashboard.label_cancelled_leads", "Solicitudes canceladas"),
    ("et", "provider_dashboard.label_cancelled_leads", "Tühistatud päringud"),
    ("fi", "provider_dashboard.label_cancelled_leads", "Perutut kyselyt"),
    ("fr", "provider_dashboard.label_cancelled_leads", "Demandes annulées"),
    ("ga", "provider_dashboard.label_cancelled_leads", "Iarrataí cealaithe"),
    ("hr", "provider_dashboard.label_cancelled_leads", "Otkazani upiti"),
    ("hu", "provider_dashboard.label_cancelled_leads", "Visszavont érdeklődések"),
    ("is", "provider_dashboard.label_cancelled_leads", "Afturkallaðar fyrirspurnir"),
    ("it", "provider_dashboard.label_cancelled_leads", "Richieste annullate"),
    ("lb", "provider_dashboard.label_cancelled_leads", "Ofgesot Ufroe"),
    ("lt", "provider_dashboard.label_cancelled_leads", "Atšaukti užklausos"),
    ("lv", "provider_dashboard.label_cancelled_leads", "Atceltie pieprasījumi"),
    ("mk", "provider_dashboard.label_cancelled_leads", "Откажани барања"),
    ("mt", "provider_dashboard.label_cancelled_leads", "Talbiet mħassra"),
    ("nl", "provider_dashboard.label_cancelled_leads", "Geannuleerde aanvragen"),
    ("no", "provider_dashboard.label_cancelled_leads", "Avbrutte forespørsler"),
    ("pl", "provider_dashboard.label_cancelled_leads", "Anulowane zapytania"),
    ("pt", "provider_dashboard.label_cancelled_leads", "Solicitações canceladas"),
    ("pt-PT", "provider_dashboard.label_cancelled_leads", "Pedidos cancelados"),
    ("ro", "provider_dashboard.label_cancelled_leads", "Solicitări anulate"),
    ("ru", "provider_dashboard.label_cancelled_leads", "Отменённые заявки"),
    ("sk", "provider_dashboard.label_cancelled_leads", "Zrušené dopyty"),
    ("sl", "provider_dashboard.label_cancelled_leads", "Preklicane povpraševanja"),
    ("sq", "provider_dashboard.label_cancelled_leads", "Kërkesat e anuluara"),
    ("sr", "provider_dashboard.label_cancelled_leads", "Otkazani upiti"),
    ("sv", "provider_dashboard.label_cancelled_leads", "Avbrutna förfrågningar"),
    ("tr", "provider_dashboard.label_cancelled_leads", "İptal edilen talepler"),
    ("uk", "provider_dashboard.label_cancelled_leads", "Скасовані запити"),

    # label_notes_privacy_disclaimer — бележка за поверителност на бележките
    ("bg", "provider_dashboard.label_notes_privacy_disclaimer", "Бележките са видими само за Вас"),
    ("cs", "provider_dashboard.label_notes_privacy_disclaimer", "Poznámky jsou viditelné pouze pro vás"),
    ("da", "provider_dashboard.label_notes_privacy_disclaimer", "Noter er kun synlige for dig"),
    ("de", "provider_dashboard.label_notes_privacy_disclaimer", "Notizen sind nur für Sie sichtbar"),
    ("el", "provider_dashboard.label_notes_privacy_disclaimer", "Οι σημειώσεις είναι ορατές μόνο σε εσάς"),
    ("en", "provider_dashboard.label_notes_privacy_disclaimer", "Notes are visible only to you"),
    ("es", "provider_dashboard.label_notes_privacy_disclaimer", "Las notas solo son visibles para usted"),
    ("et", "provider_dashboard.label_notes_privacy_disclaimer", "Märkmed on nähtavad ainult teile"),
    ("fi", "provider_dashboard.label_notes_privacy_disclaimer", "Muistiinpanot näkyvät vain sinulle"),
    ("fr", "provider_dashboard.label_notes_privacy_disclaimer", "Les notes ne sont visibles que par vous"),
    ("ga", "provider_dashboard.label_notes_privacy_disclaimer", "Níl nótaí le feiceáil ach agat féin"),
    ("hr", "provider_dashboard.label_notes_privacy_disclaimer", "Bilješke su vidljive samo vama"),
    ("hu", "provider_dashboard.label_notes_privacy_disclaimer", "A jegyzetek csak Ön számára láthatók"),
    ("is", "provider_dashboard.label_notes_privacy_disclaimer", "Minnismiðar eru aðeins sýnilegir þér"),
    ("it", "provider_dashboard.label_notes_privacy_disclaimer", "Le note sono visibili solo a te"),
    ("lb", "provider_dashboard.label_notes_privacy_disclaimer", "Notizen si nëmmen fir Iech siichtbar"),
    ("lt", "provider_dashboard.label_notes_privacy_disclaimer", "Pastabos matomos tik jums"),
    ("lv", "provider_dashboard.label_notes_privacy_disclaimer", "Piezīmes ir redzamas tikai jums"),
    ("mk", "provider_dashboard.label_notes_privacy_disclaimer", "Белешките се видливи само за вас"),
    ("mt", "provider_dashboard.label_notes_privacy_disclaimer", "In-noti huma viżibbli biss għalik"),
    ("nl", "provider_dashboard.label_notes_privacy_disclaimer", "Notities zijn alleen voor u zichtbaar"),
    ("no", "provider_dashboard.label_notes_privacy_disclaimer", "Notater er bare synlige for deg"),
    ("pl", "provider_dashboard.label_notes_privacy_disclaimer", "Notatki są widoczne tylko dla Ciebie"),
    ("pt", "provider_dashboard.label_notes_privacy_disclaimer", "As notas são visíveis apenas para você"),
    ("pt-PT", "provider_dashboard.label_notes_privacy_disclaimer", "As notas são visíveis apenas para si"),
    ("ro", "provider_dashboard.label_notes_privacy_disclaimer", "Notele sunt vizibile doar pentru dvs."),
    ("ru", "provider_dashboard.label_notes_privacy_disclaimer", "Заметки видны только вам"),
    ("sk", "provider_dashboard.label_notes_privacy_disclaimer", "Poznámky sú viditeľné iba pre vás"),
    ("sl", "provider_dashboard.label_notes_privacy_disclaimer", "Opombe so vidne samo vam"),
    ("sq", "provider_dashboard.label_notes_privacy_disclaimer", "Shënimet janë të dukshme vetëm për ju"),
    ("sr", "provider_dashboard.label_notes_privacy_disclaimer", "Белешке су видљиве само вама"),
    ("sv", "provider_dashboard.label_notes_privacy_disclaimer", "Anteckningar är bara synliga för dig"),
    ("tr", "provider_dashboard.label_notes_privacy_disclaimer", "Notlar yalnızca size görünür"),
    ("uk", "provider_dashboard.label_notes_privacy_disclaimer", "Нотатки видимі лише вам"),
]

with Session() as session:
    for lang, key, value in TRANSLATIONS:
        session.execute(text("""
            INSERT INTO translations (lang, key, value)
            VALUES (:lang, :key, :value)
            ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
        """), {"lang": lang, "key": key, "value": value})
    session.commit()
    print(f"✅ Seeded {len(TRANSLATIONS)} rows for 2 missing keys.")
