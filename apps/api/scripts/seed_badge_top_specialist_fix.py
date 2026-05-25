from sqlalchemy.orm import Session
from apps.api.database import get_db
from apps.api.models import Translation

# Badge top specialist translations without preposition (city added dynamically with ' – ')
TRANSLATIONS = {
    'bg': 'Топ специалист',
    'cs': 'Top specialista',
    'da': 'Topspecialist',
    'de': 'Top-Spezialist',
    'el': 'Κορυφαίος ειδικός',
    'en': 'Top specialist',
    'es': 'Especialista top',
    'et': 'Tippspetsialist',
    'fi': 'Huippuasiantuntija',
    'fr': 'Meilleur spécialiste',
    'ga': 'Speisialtóir is fearr',
    'hr': 'Top stručnjak',
    'hu': 'Top szakember',
    'is': 'Topp sérfræðingur',
    'it': 'Miglior professionista',
    'lb': 'Top-Spezialist',
    'lt': 'Geriausias specialistas',
    'lv': 'Labākais speciālists',
    'mk': 'Топ специјалист',
    'mt': 'L-aqwa speċjalista',
    'nl': 'Topspecialist',
    'no': 'Toppspesialist',
    'pl': 'Najlepszy specjalista',
    'pt': 'Melhor especialista',
    'pt-PT': 'Melhor especialista',
    'ro': 'Specialist de top',
    'ru': 'Топ специалист',
    'sk': 'Top špecialista',
    'sl': 'Najboljši strokovnjak',
    'sq': 'Specialist i parë',
    'sr': 'Топ стручњак',
    'sv': 'Toppspecialist',
    'tr': 'En iyi uzman',
    'uk': 'Топ спеціаліст',
}

def main():
    db: Session = next(get_db())
    
    key = 'widget.badge_top_specialist'
    
    for lang, value in TRANSLATIONS.items():
        translation = db.query(Translation).filter(
            Translation.key == key,
            Translation.lang == lang
        ).first()
        
        if translation:
            translation.value = value
            print(f"Updated {lang}: {value}")
        else:
            print(f"WARNING: {lang} not found for key {key}")
    
    db.commit()
    print(f"\nUpdated {len(TRANSLATIONS)} translations for key '{key}'")

if __name__ == '__main__':
    main()
