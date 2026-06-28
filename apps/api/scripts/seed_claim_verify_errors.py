#!/usr/bin/env python3
"""Seed claim verify error translations into the translations table."""

import os
import psycopg2
from psycopg2.extras import execute_values

# Database connection string
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://nevumo:nevumo@localhost:5433/nevumo_leads")

# Translations as list of (key, lang, value) tuples
TRANSLATIONS = [
    # verify_error_invalid — "Invalid verification code"
    ("claim.verify_error_invalid", "bg", "Невалиден код за верификация"),
    ("claim.verify_error_invalid", "cs", "Neplatný ověřovací kód"),
    ("claim.verify_error_invalid", "da", "Ugyldig bekræftelseskode"),
    ("claim.verify_error_invalid", "de", "Ungültiger Bestätigungscode"),
    ("claim.verify_error_invalid", "el", "Μη έγκυρος κωδικός επαλήθευσης"),
    ("claim.verify_error_invalid", "en", "Invalid verification code"),
    ("claim.verify_error_invalid", "es", "Código de verificación no válido"),
    ("claim.verify_error_invalid", "et", "Vigane kinnituskood"),
    ("claim.verify_error_invalid", "fi", "Virheellinen vahvistuskoodi"),
    ("claim.verify_error_invalid", "fr", "Code de vérification invalide"),
    ("claim.verify_error_invalid", "ga", "Cód fíoraithe neamhbhailí"),
    ("claim.verify_error_invalid", "hr", "Nevažeći kôd za provjeru"),
    ("claim.verify_error_invalid", "hu", "Érvénytelen ellenőrző kód"),
    ("claim.verify_error_invalid", "is", "Ógildur staðfestingarkóði"),
    ("claim.verify_error_invalid", "it", "Codice di verifica non valido"),
    ("claim.verify_error_invalid", "lb", "Ongültege Verifikatiounscode"),
    ("claim.verify_error_invalid", "lt", "Netinkamas patvirtinimo kodas"),
    ("claim.verify_error_invalid", "lv", "Nederīgs verifikācijas kods"),
    ("claim.verify_error_invalid", "mk", "Невалиден код за верификација"),
    ("claim.verify_error_invalid", "mt", "Kodiċi ta' verifikazzjoni invalidu"),
    ("claim.verify_error_invalid", "nl", "Ongeldige verificatiecode"),
    ("claim.verify_error_invalid", "no", "Ugyldig bekreftelseskode"),
    ("claim.verify_error_invalid", "pl", "Nieprawidłowy kod weryfikacyjny"),
    ("claim.verify_error_invalid", "pt", "Código de verificação inválido"),
    ("claim.verify_error_invalid", "pt-PT", "Código de verificação inválido"),
    ("claim.verify_error_invalid", "ro", "Cod de verificare invalid"),
    ("claim.verify_error_invalid", "ru", "Неверный код подтверждения"),
    ("claim.verify_error_invalid", "sk", "Neplatný overovací kód"),
    ("claim.verify_error_invalid", "sl", "Neveljavna koda za preverjanje"),
    ("claim.verify_error_invalid", "sq", "Kod verifikimi i pavlefshëm"),
    ("claim.verify_error_invalid", "sr", "Невалидан код за верификацију"),
    ("claim.verify_error_invalid", "sv", "Ogiltig verifieringskod"),
    ("claim.verify_error_invalid", "tr", "Geçersiz doğrulama kodu"),
    ("claim.verify_error_invalid", "uk", "Недійсний код підтвердження"),

    # verify_error_expired — "Verification code has expired"
    ("claim.verify_error_expired", "bg", "Кодът за верификация е изтекъл"),
    ("claim.verify_error_expired", "cs", "Platnost ověřovacího kódu vypršela"),
    ("claim.verify_error_expired", "da", "Bekræftelseskoden er udløbet"),
    ("claim.verify_error_expired", "de", "Der Bestätigungscode ist abgelaufen"),
    ("claim.verify_error_expired", "el", "Ο κωδικός επαλήθευσης έχει λήξει"),
    ("claim.verify_error_expired", "en", "Verification code has expired"),
    ("claim.verify_error_expired", "es", "El código de verificación ha caducado"),
    ("claim.verify_error_expired", "et", "Kinnituskoodi kehtivus on aegunud"),
    ("claim.verify_error_expired", "fi", "Vahvistuskoodi on vanhentunut"),
    ("claim.verify_error_expired", "fr", "Le code de vérification a expiré"),
    ("claim.verify_error_expired", "ga", "Tá an cód fíoraithe imithe in éag"),
    ("claim.verify_error_expired", "hr", "Kôd za provjeru je istekao"),
    ("claim.verify_error_expired", "hu", "Az ellenőrző kód lejárt"),
    ("claim.verify_error_expired", "is", "Staðfestingarkóðinn er útrunninn"),
    ("claim.verify_error_expired", "it", "Il codice di verifica è scaduto"),
    ("claim.verify_error_expired", "lb", "De Verifikatiounscode ass ofgelaf"),
    ("claim.verify_error_expired", "lt", "Patvirtinimo kodo galiojimas baigėsi"),
    ("claim.verify_error_expired", "lv", "Verifikācijas koda derīgums ir beidzies"),
    ("claim.verify_error_expired", "mk", "Кодот за верификација е истечен"),
    ("claim.verify_error_expired", "mt", "Il-kodiċi ta' verifikazzjoni skada"),
    ("claim.verify_error_expired", "nl", "De verificatiecode is verlopen"),
    ("claim.verify_error_expired", "no", "Bekreftelseskoden er utløpt"),
    ("claim.verify_error_expired", "pl", "Kod weryfikacyjny wygasł"),
    ("claim.verify_error_expired", "pt", "O código de verificação expirou"),
    ("claim.verify_error_expired", "pt-PT", "O código de verificação expirou"),
    ("claim.verify_error_expired", "ro", "Codul de verificare a expirat"),
    ("claim.verify_error_expired", "ru", "Срок действия кода подтверждения истёк"),
    ("claim.verify_error_expired", "sk", "Platnosť overovacieho kódu vypršala"),
    ("claim.verify_error_expired", "sl", "Koda za preverjanje je potekla"),
    ("claim.verify_error_expired", "sq", "Kodi i verifikimit ka skaduar"),
    ("claim.verify_error_expired", "sr", "Код за верификацију је истекао"),
    ("claim.verify_error_expired", "sv", "Verifieringskoden har gått ut"),
    ("claim.verify_error_expired", "tr", "Doğrulama kodunun süresi doldu"),
    ("claim.verify_error_expired", "uk", "Термін дії коду підтвердження закінчився"),

    # verify_error_network — network error (нов ключ)
    ("claim.verify_error_network", "bg", "Мрежова грешка. Опитайте отново."),
    ("claim.verify_error_network", "cs", "Chyba sítě. Zkuste to znovu."),
    ("claim.verify_error_network", "da", "Netværksfejl. Prøv igen."),
    ("claim.verify_error_network", "de", "Netzwerkfehler. Bitte erneut versuchen."),
    ("claim.verify_error_network", "el", "Σφάλμα δικτύου. Δοκιμάστε ξανά."),
    ("claim.verify_error_network", "en", "Network error. Please try again."),
    ("claim.verify_error_network", "es", "Error de red. Por favor, inténtelo de nuevo."),
    ("claim.verify_error_network", "et", "Võrguviga. Proovige uuesti."),
    ("claim.verify_error_network", "fi", "Verkkovirhe. Yritä uudelleen."),
    ("claim.verify_error_network", "fr", "Erreur réseau. Veuillez réessayer."),
    ("claim.verify_error_network", "ga", "Earráid líonra. Bain triail eile as."),
    ("claim.verify_error_network", "hr", "Mrežna pogreška. Pokušajte ponovo."),
    ("claim.verify_error_network", "hu", "Hálózati hiba. Kérjük, próbálja újra."),
    ("claim.verify_error_network", "is", "Netvilla. Vinsamlegast reyndu aftur."),
    ("claim.verify_error_network", "it", "Errore di rete. Riprova."),
    ("claim.verify_error_network", "lb", "Netzwierkfehler. Versicht et nach eng Kéier."),
    ("claim.verify_error_network", "lt", "Tinklo klaida. Bandykite dar kartą."),
    ("claim.verify_error_network", "lv", "Tīkla kļūda. Lūdzu, mēģiniet vēlreiz."),
    ("claim.verify_error_network", "mk", "Мрежна грешка. Обидете се повторно."),
    ("claim.verify_error_network", "mt", "Żball tan-netwerk. Erġa' pprova."),
    ("claim.verify_error_network", "nl", "Netwerkfout. Probeer het opnieuw."),
    ("claim.verify_error_network", "no", "Nettverksfeil. Vennligst prøv igjen."),
    ("claim.verify_error_network", "pl", "Błąd sieci. Spróbuj ponownie."),
    ("claim.verify_error_network", "pt", "Erro de rede. Por favor, tente novamente."),
    ("claim.verify_error_network", "pt-PT", "Erro de rede. Por favor, tente novamente."),
    ("claim.verify_error_network", "ro", "Eroare de rețea. Vă rugăm să încercați din nou."),
    ("claim.verify_error_network", "ru", "Ошибка сети. Пожалуйста, попробуйте снова."),
    ("claim.verify_error_network", "sk", "Chyba siete. Skúste to znova."),
    ("claim.verify_error_network", "sl", "Napaka omrežja. Poskusite znova."),
    ("claim.verify_error_network", "sq", "Gabim rrjeti. Ju lutemi provoni përsëri."),
    ("claim.verify_error_network", "sr", "Мрежна грешка. Покушајте поново."),
    ("claim.verify_error_network", "sv", "Nätverksfel. Försök igen."),
    ("claim.verify_error_network", "tr", "Ağ hatası. Lütfen tekrar deneyin."),
    ("claim.verify_error_network", "uk", "Помилка мережі. Будь ласка, спробуйте ще раз."),

    # verify_error_format — "Code must be exactly 6 digits" (вече съществува — само upsert)
    ("claim.verify_error_format", "bg", "Кодът трябва да е точно 6 цифри"),
    ("claim.verify_error_format", "cs", "Kód musí mít přesně 6 číslic"),
    ("claim.verify_error_format", "da", "Koden skal være præcis 6 cifre"),
    ("claim.verify_error_format", "de", "Der Code muss genau 6 Ziffern haben"),
    ("claim.verify_error_format", "el", "Ο κωδικός πρέπει να έχει ακριβώς 6 ψηφία"),
    ("claim.verify_error_format", "en", "Code must be exactly 6 digits"),
    ("claim.verify_error_format", "es", "El código debe tener exactamente 6 dígitos"),
    ("claim.verify_error_format", "et", "Kood peab olema täpselt 6 numbrit"),
    ("claim.verify_error_format", "fi", "Koodin on oltava tasan 6 numeroa"),
    ("claim.verify_error_format", "fr", "Le code doit comporter exactement 6 chiffres"),
    ("claim.verify_error_format", "ga", "Ní mór don chód a bheith díreach 6 dhigit"),
    ("claim.verify_error_format", "hr", "Kôd mora imati točno 6 znamenki"),
    ("claim.verify_error_format", "hu", "A kódnak pontosan 6 számjegyből kell állnia"),
    ("claim.verify_error_format", "is", "Kóðinn verður að vera nákvæmlega 6 tölustafir"),
    ("claim.verify_error_format", "it", "Il codice deve essere esattamente 6 cifre"),
    ("claim.verify_error_format", "lb", "De Code muss genau 6 Ziffere hunn"),
    ("claim.verify_error_format", "lt", "Kodas turi būti lygiai 6 skaitmenys"),
    ("claim.verify_error_format", "lv", "Kodam jābūt tieši 6 cipariem"),
    ("claim.verify_error_format", "mk", "Кодот мора да има точно 6 цифри"),
    ("claim.verify_error_format", "mt", "Il-kodiċi jrid ikun eżattament 6 figuri"),
    ("claim.verify_error_format", "nl", "De code moet precies 6 cijfers bevatten"),
    ("claim.verify_error_format", "no", "Koden må være nøyaktig 6 sifre"),
    ("claim.verify_error_format", "pl", "Kod musi składać się z dokładnie 6 cyfr"),
    ("claim.verify_error_format", "pt", "O código deve ter exatamente 6 dígitos"),
    ("claim.verify_error_format", "pt-PT", "O código deve ter exatamente 6 dígitos"),
    ("claim.verify_error_format", "ro", "Codul trebuie să aibă exact 6 cifre"),
    ("claim.verify_error_format", "ru", "Код должен состоять ровно из 6 цифр"),
    ("claim.verify_error_format", "sk", "Kód musí mať presne 6 číslic"),
    ("claim.verify_error_format", "sl", "Koda mora biti natanko 6 številk"),
    ("claim.verify_error_format", "sq", "Kodi duhet të ketë saktësisht 6 shifra"),
    ("claim.verify_error_format", "sr", "Код мора имати тачно 6 цифара"),
    ("claim.verify_error_format", "sv", "Koden måste vara exakt 6 siffror"),
    ("claim.verify_error_format", "tr", "Kod tam olarak 6 rakamdan oluşmalıdır"),
    ("claim.verify_error_format", "uk", "Код повинен містити рівно 6 цифр"),

    # already_claimed_redirect
    ("claim.already_claimed_redirect", "bg", "Този профил вече е потвърден. Отиди към таблото."),
    ("claim.already_claimed_redirect", "cs", "Tento profil již byl potvrzen. Přejděte na dashboard."),
    ("claim.already_claimed_redirect", "da", "Denne profil er allerede bekræftet. Gå til dashboard."),
    ("claim.already_claimed_redirect", "de", "Dieses Profil wurde bereits bestätigt. Zum Dashboard."),
    ("claim.already_claimed_redirect", "el", "Αυτό το προφίλ έχει ήδη επαληθευτεί. Μεταβείτε στον πίνακα ελέγχου."),
    ("claim.already_claimed_redirect", "en", "This profile has already been claimed. Go to your dashboard."),
    ("claim.already_claimed_redirect", "es", "Este perfil ya ha sido reclamado. Ve al panel de control."),
    ("claim.already_claimed_redirect", "et", "See profiil on juba kinnitatud. Mine armatuurlauale."),
    ("claim.already_claimed_redirect", "fi", "Tämä profiili on jo vahvistettu. Siirry kojelautaan."),
    ("claim.already_claimed_redirect", "fr", "Ce profil a déjà été revendiqué. Accédez au tableau de bord."),
    ("claim.already_claimed_redirect", "ga", "Tá an próifíl seo éilithe cheana féin. Téigh go dtí an deais."),
    ("claim.already_claimed_redirect", "hr", "Ovaj profil je već potvrđen. Idite na nadzornu ploču."),
    ("claim.already_claimed_redirect", "hu", "Ez a profil már igénybe van véve. Lépjen az irányítópultra."),
    ("claim.already_claimed_redirect", "is", "Þessi prófíll hefur þegar verið krafist. Fara á mælaborðið."),
    ("claim.already_claimed_redirect", "it", "Questo profilo è già stato rivendicato. Vai alla dashboard."),
    ("claim.already_claimed_redirect", "lb", "Dëse Profil gouf schonn ugefuerdert. Gitt zum Dashboard."),
    ("claim.already_claimed_redirect", "lt", "Šis profilis jau pareikštas. Eikite į valdymo skydelį."),
    ("claim.already_claimed_redirect", "lv", "Šis profils jau ir pieprasīts. Dodieties uz vadības paneli."),
    ("claim.already_claimed_redirect", "mk", "Овој профил веќе е потврден. Одете на контролната табла."),
    ("claim.already_claimed_redirect", "mt", "Dan il-profil diġà ġie rreklmat. Mur għad-dashboard."),
    ("claim.already_claimed_redirect", "nl", "Dit profiel is al geclaimd. Ga naar het dashboard."),
    ("claim.already_claimed_redirect", "no", "Denne profilen er allerede bekreftet. Gå til dashbordet."),
    ("claim.already_claimed_redirect", "pl", "Ten profil został już przejęty. Przejdź do panelu."),
    ("claim.already_claimed_redirect", "pt", "Este perfil já foi reivindicado. Vá para o painel."),
    ("claim.already_claimed_redirect", "pt-PT", "Este perfil já foi reivindicado. Vá para o painel."),
    ("claim.already_claimed_redirect", "ro", "Acest profil a fost deja revendicat. Mergeți la tabloul de bord."),
    ("claim.already_claimed_redirect", "ru", "Этот профиль уже подтверждён. Перейдите в панель управления."),
    ("claim.already_claimed_redirect", "sk", "Tento profil bol už uplatnený. Prejdite na dashboard."),
    ("claim.already_claimed_redirect", "sl", "Ta profil je že zahtevani. Pojdite na nadzorno ploščo."),
    ("claim.already_claimed_redirect", "sq", "Ky profil është marrë tashmë. Shkoni te paneli juaj."),
    ("claim.already_claimed_redirect", "sr", "Овај профил је већ потврђен. Идите на контролну таблу."),
    ("claim.already_claimed_redirect", "sv", "Den här profilen har redan tagits i anspråk. Gå till instrumentpanelen."),
    ("claim.already_claimed_redirect", "tr", "Bu profil zaten talep edildi. Kontrol panelinize gidin."),
    ("claim.already_claimed_redirect", "uk", "Цей профіль вже підтверджено. Перейдіть до панелі керування."),

    # resend_code — "Send code again"
    ("claim.resend_code", "bg", "Изпрати нов код"),
    ("claim.resend_code", "cs", "Odeslat kód znovu"),
    ("claim.resend_code", "da", "Send kode igen"),
    ("claim.resend_code", "de", "Code erneut senden"),
    ("claim.resend_code", "el", "Αποστολή νέου κωδικού"),
    ("claim.resend_code", "en", "Send code again"),
    ("claim.resend_code", "es", "Reenviar código"),
    ("claim.resend_code", "et", "Saada kood uuesti"),
    ("claim.resend_code", "fi", "Lähetä koodi uudelleen"),
    ("claim.resend_code", "fr", "Renvoyer le code"),
    ("claim.resend_code", "ga", "Seol cód arís"),
    ("claim.resend_code", "hr", "Pošalji kôd ponovo"),
    ("claim.resend_code", "hu", "Kód újraküldése"),
    ("claim.resend_code", "is", "Senda kóða aftur"),
    ("claim.resend_code", "it", "Invia di nuovo il codice"),
    ("claim.resend_code", "lb", "Code nach eng Kéier schécken"),
    ("claim.resend_code", "lt", "Siųsti kodą dar kartą"),
    ("claim.resend_code", "lv", "Sūtīt kodu vēlreiz"),
    ("claim.resend_code", "mk", "Испрати нов код"),
    ("claim.resend_code", "mt", "Ibgħat il-kodiċi mill-ġdid"),
    ("claim.resend_code", "nl", "Code opnieuw verzenden"),
    ("claim.resend_code", "no", "Send kode på nytt"),
    ("claim.resend_code", "pl", "Wyślij kod ponownie"),
    ("claim.resend_code", "pt", "Reenviar código"),
    ("claim.resend_code", "pt-PT", "Reenviar código"),
    ("claim.resend_code", "ro", "Retrimite codul"),
    ("claim.resend_code", "ru", "Отправить код повторно"),
    ("claim.resend_code", "sk", "Odoslať kód znova"),
    ("claim.resend_code", "sl", "Pošlji kodo znova"),
    ("claim.resend_code", "sq", "Dërgo kodin përsëri"),
    ("claim.resend_code", "sr", "Пошаљи код поново"),
    ("claim.resend_code", "sv", "Skicka koden igen"),
    ("claim.resend_code", "tr", "Kodu tekrar gönder"),
    ("claim.resend_code", "uk", "Надіслати код повторно"),

    # resend_cooldown — "Send again in" (seconds appended in component)
    ("claim.resend_cooldown", "bg", "Изпрати отново след"),
    ("claim.resend_cooldown", "cs", "Odeslat znovu za"),
    ("claim.resend_cooldown", "da", "Send igen om"),
    ("claim.resend_cooldown", "de", "Erneut senden in"),
    ("claim.resend_cooldown", "el", "Αποστολή ξανά σε"),
    ("claim.resend_cooldown", "en", "Send again in"),
    ("claim.resend_cooldown", "es", "Reenviar en"),
    ("claim.resend_cooldown", "et", "Saada uuesti"),
    ("claim.resend_cooldown", "fi", "Lähetä uudelleen"),
    ("claim.resend_cooldown", "fr", "Renvoyer dans"),
    ("claim.resend_cooldown", "ga", "Seol arís i"),
    ("claim.resend_cooldown", "hr", "Pošalji ponovo za"),
    ("claim.resend_cooldown", "hu", "Újraküldés"),
    ("claim.resend_cooldown", "is", "Senda aftur eftir"),
    ("claim.resend_cooldown", "it", "Invia di nuovo tra"),
    ("claim.resend_cooldown", "lb", "Nach eng Kéier schécken an"),
    ("claim.resend_cooldown", "lt", "Siųsti dar kartą po"),
    ("claim.resend_cooldown", "lv", "Sūtīt vēlreiz pēc"),
    ("claim.resend_cooldown", "mk", "Испрати повторно за"),
    ("claim.resend_cooldown", "mt", "Ibgħat mill-ġdid fi"),
    ("claim.resend_cooldown", "nl", "Opnieuw verzenden over"),
    ("claim.resend_cooldown", "no", "Send på nytt om"),
    ("claim.resend_cooldown", "pl", "Wyślij ponownie za"),
    ("claim.resend_cooldown", "pt", "Reenviar em"),
    ("claim.resend_cooldown", "pt-PT", "Reenviar em"),
    ("claim.resend_cooldown", "ro", "Retrimite în"),
    ("claim.resend_cooldown", "ru", "Отправить повторно через"),
    ("claim.resend_cooldown", "sk", "Odoslať znova o"),
    ("claim.resend_cooldown", "sl", "Pošlji znova čez"),
    ("claim.resend_cooldown", "sq", "Dërgo përsëri pas"),
    ("claim.resend_cooldown", "sr", "Пошаљи поново за"),
    ("claim.resend_cooldown", "sv", "Skicka igen om"),
    ("claim.resend_cooldown", "tr", "Tekrar gönder"),
    ("claim.resend_cooldown", "uk", "Надіслати повторно через"),
]


def seed_translations() -> int:
    """Seed translations into the database."""
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    rows_to_upsert = []
    for key, lang, value in TRANSLATIONS:
        rows_to_upsert.append((lang, key, value))

    execute_values(
        cursor,
        """
        INSERT INTO translations (lang, key, value)
        VALUES %s
        ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
        """,
        rows_to_upsert,
        template="(%s, %s, %s)",
    )

    conn.commit()
    cursor.close()
    conn.close()

    return len(rows_to_upsert)


def clear_redis_cache() -> None:
    """Clear Redis cache for claim namespace."""
    try:
        from apps.api.dependencies import get_redis
        
        r = get_redis()
        if not r:
            print("✓ Redis not available, skipping cache clear")
            return

        # Delete all keys matching the pattern for claim namespace
        pattern = "trans:*:claim"
        keys = list(r.scan_iter(match=pattern))
        if keys:
            r.delete(*keys)
            print(f"✓ Cleared {len(keys)} keys from Redis cache for 'claim' namespace")
        else:
            print("✓ No Redis keys found to clear for 'claim' namespace")
    except Exception as e:
        print(f"⚠ Redis cache clear failed (non-critical): {e}")


if __name__ == "__main__":
    print("Seeding claim verify error translations...")
    count = seed_translations()
    print(f"✓ Seeded {count} translations")
    
    print("Clearing Redis cache for claim namespace...")
    clear_redis_cache()
    
    print("Done!")
