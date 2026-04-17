#!/usr/bin/env python3
"""
Seed label_notes_privacy_disclaimer translation for provider_dashboard namespace.
Uses simple translations table structure (key format: provider_dashboard.key_name)
Run: python scripts/seed_notes_privacy_translations_v2.py
"""

import os

from sqlalchemy import text
from apps.api.database import engine
from apps.api.dependencies import get_redis

NAMESPACE = "provider_dashboard"
KEY = "label_notes_privacy_disclaimer"
FULL_KEY = f"{NAMESPACE}.{KEY}"

# All 34 translations
TRANSLATIONS = {
    'en': 'These notes are only visible to you and will not be shared with the client.',
    'bg': 'Тези бележки са видими само за Вас и няма да бъдат споделяни с клиента.',
    'cs': 'Tyto poznámky vidíte pouze vy a nebudou sdíleny s klientem.',
    'da': 'Disse noter er kun synlige for dig og vil ikke blive delt med kunden.',
    'de': 'Diese Notizen sind nur für Sie sichtbar und werden nicht mit dem Kunden geteilt.',
    'el': 'Αυτές οι σημειώσεις είναι ορατές μόνο σε εσάς και δεν θα κοινοποιηθούν στον πελάτη.',
    'es': 'Estas notas solo son visibles para usted y no se compartirán con el cliente.',
    'et': 'Need märkmed on nähtavad ainult teile ja neid ei jagata kliendiga.',
    'fi': 'Nämä muistiinpanot näkyvät vain sinulle, eikä niitä jaeta asiakkaalle.',
    'fr': 'Ces notes ne sont visibles que par vous et ne seront pas partagées avec le client.',
    'ga': 'Níl na nótaí seo le feiceáil ach agat féin agus ní roinnfear iad leis an gcliant.',
    'hr': 'Ove bilješke vidljive su samo vama i neće se dijeliti s klijentom.',
    'hu': 'Ezeket a jegyzeteket csak Ön láthatja, az ügyféllel nem kerülnek megosztásra.',
    'is': 'Þessar athugasemdir eru aðeins sýnilegar þér og verður ekki deilt með viðskiptavininum.',
    'it': 'Queste note sono visibili solo a te e non saranno condivise con il cliente.',
    'lb': 'Dës Notize si just fir Iech sichtbar a ginn net mam Client gedeelt.',
    'lt': 'Šios pastabos matomos tik jums ir nebus bendrinamos su klientu.',
    'lv': 'Šīs piezīmes ir redzamas tikai jums un netiks kopīgotas ar klientu.',
    'mk': 'Овие белешки се видливи само за Вас и няма да бидат споделени со клиентот.',
    'mt': 'Dawn in-noti huma viżibbli għalik biss u mhux se jinqasmu mal-klijent.',
    'nl': 'Deze notities zijn alleen zichtbaar voor u en worden niet gedeeld met de klant.',
    'no': 'Disse notatene er kun synlige for deg og vil bli delt med kunden.',
    'pl': 'Te notatki są widoczne tylko dla Ciebie i nie będą udostępniane klientowi.',
    'pt': 'Estas notas são visíveis apenas para si e não serão partilhadas com o cliente.',
    'pt-PT': 'Estas notas são visíveis apenas para si e não serão partilhadas com o cliente.',
    'ro': 'Aceste note sunt vizibile doar pentru dvs. și nu vor fi partajate cu clientul.',
    'ru': 'Эти заметки видны только вам и не будут переданы клиенту.',
    'sk': 'Tieto poznámky vidíte iba vy a nebudú zdieľané s klientom.',
    'sl': 'Te opombe so vidne samo vam in ne bodo deljene s stranko.',
    'sq': 'Këto shënime janë të dukshme vetëm për ju dhe nuk do të ndahen me klientin.',
    'sr': 'Ove beleške su vidljive samo vama i neće biti deljene sa klijentom.',
    'sv': 'Dessa anteckningar är endast synliga för dig och kommer inte att delas med kunden.',
    'tr': 'Bu notlar sadece sizin tarafınızdan görülebilir ve müşteriyle paylaşılmaz.',
    'uk': 'Ці нотатки бачите лише ви, вони не будуть передані клієнту.',
}


def main():
    with engine.connect() as conn:
        # Insert or update translations using ON CONFLICT upsert
        for lang, value in TRANSLATIONS.items():
            conn.execute(
                text("""
                    INSERT INTO translations (lang, key, value)
                    VALUES (:lang, :key, :value)
                    ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
                """),
                {"lang": lang, "key": FULL_KEY, "value": value}
            )
        
        conn.commit()
        print(f"✓ Successfully seeded {len(TRANSLATIONS)} translations for '{FULL_KEY}'")
        
        # Verify count
        result = conn.execute(
            text("SELECT COUNT(*) FROM translations WHERE key = :key"),
            {"key": FULL_KEY}
        )
        count = result.scalar()
        print(f"✓ Total rows in database for this key: {count}")
    
    # Clear Redis cache for provider_dashboard namespace
    try:
        r = get_redis()
        if not r:
            print("✓ Redis not available, skipping cache clear")
            return

        # Delete all keys matching the pattern for provider_dashboard
        pattern = f"i18n:{NAMESPACE}:*"
        keys = list(r.scan_iter(match=pattern))
        if keys:
            r.delete(*keys)
            print(f"✓ Cleared {len(keys)} keys from Redis cache")
        else:
            print("✓ No Redis keys to clear")
    except Exception as e:
        print(f"⚠ Could not clear Redis cache: {e}")


if __name__ == "__main__":
    main()
