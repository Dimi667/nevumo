SLAVIC_FORMS = {
    'warszawa': {
        'bg': ('Варшава',    'Варшава'),
        'cs': ('Varšavě',   'Varšavy'),
        'hr': ('Varšavi',   'Varšave'),
        'mk': ('Варшава',   'Варшава'),
        'pl': ('Warszawie', 'Warszawy'),
        'ru': ('Варшаве',   'Варшавы'),
        'sk': ('Varšave',   'Varšavy'),
        'sl': ('Varšavi',   'Varšave'),
        'sr': ('Варшави',   'Варшаве'),
        'uk': ('Варшаві',   'Варшави'),
    },
    'sofia': {
        'bg': ('София',     'София'),
        'cs': ('Sofii',     'Sofie'),
        'hr': ('Sofiji',    'Sofije'),
        'mk': ('Софија',    'Софија'),
        'pl': ('Sofii',     'Sofii'),
        'ru': ('Софии',     'Софии'),
        'sk': ('Sofii',     'Sofie'),
        'sl': ('Sofiji',    'Sofije'),
        'sr': ('Софији',    'Ософије'),
        'uk': ('Софії',     'Софії'),
    },
    'belgrade': {
        'bg': ('Белград',    'Белград'),
        'cs': ('Bělehradě', 'Bělehradu'),
        'hr': ('Beogradu',  'Beograda'),
        'mk': ('Белград',   'Белград'),
        'pl': ('Belgradzie','Belgradu'),
        'ru': ('Белграде',  'Белграда'),
        'sk': ('Belehrade', 'Belehradu'),
        'sl': ('Beogradu',  'Beograda'),
        'sr': ('Београду',  'Београда'),
        'uk': ('Белграді',  'Белграда'),
    },
}

from apps.api.database import get_db
from apps.api.models import Location, LocationTranslation
from sqlalchemy.orm import Session

def run():
    db: Session = next(get_db())
    slugs = ['warszawa', 'sofia', 'belgrade']
    
    for slug in slugs:
        location = db.query(Location).filter(Location.slug == slug).first()
        if not location:
            print(f"City not found: {slug}")
            continue
        
        rows = db.query(LocationTranslation).filter(
            LocationTranslation.location_id == location.id
        ).all()
        
        for row in rows:
            slavic = SLAVIC_FORMS.get(slug, {}).get(row.lang)
            if slavic:
                row.locative_form, row.genitive_form = slavic
            else:
                row.locative_form = row.city_name
                row.genitive_form = row.city_name
        
        print(f"Updated {len(rows)} rows for {slug}")
    
    db.commit()
    print("Done.")

if __name__ == "__main__":
    run()
