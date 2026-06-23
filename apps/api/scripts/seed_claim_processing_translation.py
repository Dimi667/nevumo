"""
Seed script: claim.processing translation key (34 languages)
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
    "bg": "Активираме вашия профил...",
    "cs": "Aktivujeme váš profil...",
    "da": "Vi aktiverer din profil...",
    "de": "Wir aktivieren Ihr Profil...",
    "el": "Ενεργοποιούμε το προφίλ σας...",
    "en": "Activating your profile...",
    "es": "Activando tu perfil...",
    "et": "Aktiveerime teie profiili...",
    "fi": "Aktivoimme profiiliasi...",
    "fr": "Activation de votre profil...",
    "ga": "Ag gníomhachtú do phróifíl...",
    "hr": "Aktiviramo vaš profil...",
    "hu": "Aktiváljuk a profilját...",
    "is": "Við virkjum prófílinn þinn...",
    "it": "Attivazione del tuo profilo...",
    "lb": "Mir aktivéieren Äre Profil...",
    "lt": "Aktyvuojame jūsų profilį...",
    "lv": "Aktivizējam jūsu profilu...",
    "mk": "Го активираме вашиот профил...",
    "mt": "Qed nattivaw il-profil tiegħek...",
    "nl": "We activeren uw profiel...",
    "no": "Vi aktiverer profilen din...",
    "pl": "Aktywujemy Twój profil...",
    "pt": "Ativando seu perfil...",
    "pt-PT": "A ativar o seu perfil...",
    "ro": "Activăm profilul dvs....",
    "ru": "Активируем ваш профиль...",
    "sk": "Aktivujeme váš profil...",
    "sl": "Aktiviramo vaš profil...",
    "sq": "Po aktivizojmë profilin tuaj...",
    "sr": "Активирамо ваш профил...",
    "sv": "Vi aktiverar din profil...",
    "tr": "Profiliniz etkinleştiriliyor...",
    "uk": "Активуємо ваш профіль...",
}

def seed():
    db = SessionLocal()
    try:
        inserted = 0
        updated = 0
        for lang, value in TRANSLATIONS.items():
            result = db.execute(
                text("""
                    INSERT INTO translations (lang, key, value)
                    VALUES (:lang, :key, :value)
                    ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
                """),
                {"lang": lang, "key": "claim.processing", "value": value}
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
