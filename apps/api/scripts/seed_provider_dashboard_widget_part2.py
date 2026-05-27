from apps.api.database import SessionLocal
from sqlalchemy import text

def seed():
    db = SessionLocal()
    try:
        rows = [
            ('en', 'provider_dashboard.widget_size_standard', 'Standard (360px)'),
            ('en', 'provider_dashboard.widget_size_wide', 'Wide (480px)'),
            ('bg', 'provider_dashboard.widget_size_standard', 'Стандарт (360px)'),
            ('bg', 'provider_dashboard.widget_size_wide', 'Широк (480px)'),
            ('pl', 'provider_dashboard.widget_size_standard', 'Standard (360px)'),
            ('pl', 'provider_dashboard.widget_size_wide', 'Szeroki (480px)'),
            ('de', 'provider_dashboard.widget_size_standard', 'Standard (360px)'),
            ('de', 'provider_dashboard.widget_size_wide', 'Breit (480px)'),
            ('fr', 'provider_dashboard.widget_size_standard', 'Standard (360px)'),
            ('fr', 'provider_dashboard.widget_size_wide', 'Large (480px)'),
            ('es', 'provider_dashboard.widget_size_standard', 'Estándar (360px)'),
            ('es', 'provider_dashboard.widget_size_wide', 'Amplio (480px)'),
            ('it', 'provider_dashboard.widget_size_standard', 'Standard (360px)'),
            ('it', 'provider_dashboard.widget_size_wide', 'Largo (480px)'),
            ('pt', 'provider_dashboard.widget_size_standard', 'Padrão (360px)'),
            ('pt', 'provider_dashboard.widget_size_wide', 'Largo (480px)'),
            ('pt-PT', 'provider_dashboard.widget_size_standard', 'Padrão (360px)'),
            ('pt-PT', 'provider_dashboard.widget_size_wide', 'Largo (480px)'),
            ('nl', 'provider_dashboard.widget_size_standard', 'Standaard (360px)'),
            ('nl', 'provider_dashboard.widget_size_wide', 'Breed (480px)'),
            ('cs', 'provider_dashboard.widget_size_standard', 'Standard (360px)'),
            ('cs', 'provider_dashboard.widget_size_wide', 'Široký (480px)'),
            ('sk', 'provider_dashboard.widget_size_standard', 'Štandard (360px)'),
            ('sk', 'provider_dashboard.widget_size_wide', 'Široký (480px)'),
            ('ro', 'provider_dashboard.widget_size_standard', 'Standard (360px)'),
            ('ro', 'provider_dashboard.widget_size_wide', 'Lat (480px)'),
            ('hu', 'provider_dashboard.widget_size_standard', 'Standard (360px)'),
            ('hu', 'provider_dashboard.widget_size_wide', 'Széles (480px)'),
            ('hr', 'provider_dashboard.widget_size_standard', 'Standard (360px)'),
            ('hr', 'provider_dashboard.widget_size_wide', 'Širok (480px)'),
            ('sl', 'provider_dashboard.widget_size_standard', 'Standard (360px)'),
            ('sl', 'provider_dashboard.widget_size_wide', 'Širok (480px)'),
            ('da', 'provider_dashboard.widget_size_standard', 'Standard (360px)'),
            ('da', 'provider_dashboard.widget_size_wide', 'Bred (480px)'),
            ('sv', 'provider_dashboard.widget_size_standard', 'Standard (360px)'),
            ('sv', 'provider_dashboard.widget_size_wide', 'Bred (480px)'),
            ('no', 'provider_dashboard.widget_size_standard', 'Standard (360px)'),
            ('no', 'provider_dashboard.widget_size_wide', 'Bred (480px)'),
            ('fi', 'provider_dashboard.widget_size_standard', 'Standardi (360px)'),
            ('fi', 'provider_dashboard.widget_size_wide', 'Leveä (480px)'),
            ('et', 'provider_dashboard.widget_size_standard', 'Standard (360px)'),
            ('et', 'provider_dashboard.widget_size_wide', 'Lai (480px)'),
            ('lv', 'provider_dashboard.widget_size_standard', 'Standarta (360px)'),
            ('lv', 'provider_dashboard.widget_size_wide', 'Plats (480px)'),
            ('lt', 'provider_dashboard.widget_size_standard', 'Standartinis (360px)'),
            ('lt', 'provider_dashboard.widget_size_wide', 'Platus (480px)'),
            ('el', 'provider_dashboard.widget_size_standard', 'Στάνταρ (360px)'),
            ('el', 'provider_dashboard.widget_size_wide', 'Πλατύ (480px)'),
            ('ru', 'provider_dashboard.widget_size_standard', 'Стандарт (360px)'),
            ('ru', 'provider_dashboard.widget_size_wide', 'Широкий (480px)'),
            ('uk', 'provider_dashboard.widget_size_standard', 'Стандарт (360px)'),
            ('uk', 'provider_dashboard.widget_size_wide', 'Широкий (480px)'),
            ('sr', 'provider_dashboard.widget_size_standard', 'Standard (360px)'),
            ('sr', 'provider_dashboard.widget_size_wide', 'Širok (480px)'),
            ('mk', 'provider_dashboard.widget_size_standard', 'Стандард (360px)'),
            ('mk', 'provider_dashboard.widget_size_wide', 'Широк (480px)'),
            ('sq', 'provider_dashboard.widget_size_standard', 'Standard (360px)'),
            ('sq', 'provider_dashboard.widget_size_wide', 'Gjerë (480px)'),
            ('ga', 'provider_dashboard.widget_size_standard', 'Caighdeán (360px)'),
            ('ga', 'provider_dashboard.widget_size_wide', 'Leathan (480px)'),
            ('is', 'provider_dashboard.widget_size_standard', 'Standard (360px)'),
            ('is', 'provider_dashboard.widget_size_wide', 'Breiður (480px)'),
            ('lb', 'provider_dashboard.widget_size_standard', 'Standard (360px)'),
            ('lb', 'provider_dashboard.widget_size_wide', 'Breet (480px)'),
            ('mt', 'provider_dashboard.widget_size_standard', 'Standard (360px)'),
            ('mt', 'provider_dashboard.widget_size_wide', 'Wiesgħa (480px)'),
            ('tr', 'provider_dashboard.widget_size_standard', 'Standart (360px)'),
            ('tr', 'provider_dashboard.widget_size_wide', 'Geniş (480px)'),
        ]
        for lang, key, value in rows:
            db.execute(text("""
                INSERT INTO translations (lang, key, value)
                VALUES (:lang, :key, :value)
                ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
            """), {"lang": lang, "key": key, "value": value})
        db.commit()
        print(f"Seeded {len(rows)} rows.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
