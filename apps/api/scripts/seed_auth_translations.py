#!/usr/bin/env python3
"""Seed auth namespace translations into the translations table."""

import os
import psycopg2
from psycopg2.extras import execute_values

# Database connection string
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://nevumo:nevumo@localhost:5433/nevumo_leads")

# Translations: language -> list of 9 values in order
TRANSLATIONS = {
    "bg":    ["Вземи своя профил в Nevumo", "Регистрирай се безплатно и управлявай клиентите си", "Вземи профила", "Бърз вход без парола", "Вход с Google", "Вход с Facebook", "или с имейл", "Продължи", "OAuth входът не успя. Опитайте отново."],
    "pl":    ["Przejmij swój profil w Nevumo", "Zarejestruj się za darmo i zarządzaj klientami", "Przejmij profil", "Szybkie logowanie bez hasła", "Zaloguj się z Google", "Zaloguj się z Facebook", "lub z e-mailem", "Kontynuuj", "Logowanie OAuth nie powiodło się. Spróbuj ponownie."],
    "en":    ["Claim your profile on Nevumo", "Register for free and manage your clients", "Claim profile", "Quick login without password", "Sign in with Google", "Sign in with Facebook", "or with email", "Continue", "OAuth login failed. Please try again."],
    "de":    ["Nimm dein Profil auf Nevumo", "Registriere dich kostenlos und verwalte deine Kunden", "Profil beanspruchen", "Schnelle Anmeldung ohne Passwort", "Mit Google anmelden", "Mit Facebook anmelden", "oder mit E-Mail", "Weiter", "OAuth-Anmeldung fehlgeschlagen. Bitte versuchen Sie es erneut."],
    "cs":    ["Převezmi svůj profil na Nevumo", "Zaregistruj se zdarma a spravuj své zákazníky", "Převzít profil", "Rychlé přihlášení bez hesla", "Přihlásit se přes Google", "Přihlásit se přes Facebook", "nebo e-mailem", "Pokračovat", "OAuth přihlášení selhalo. Zkuste to znovu."],
    "da":    ["Gør krav på din profil på Nevumo", "Registrer dig gratis og administrer dine kunder", "Gør krav på profil", "Hurtig login uden adgangskode", "Log ind med Google", "Log ind med Facebook", "eller med e-mail", "Fortsæt", "OAuth-login mislykkedes. Prøv igen."],
    "el":    ["Διεκδικήστε το προφίλ σας στο Nevumo", "Εγγραφείτε δωρεάν και διαχειριστείτε τους πελάτες σας", "Διεκδίκηση προφίλ", "Γρήγορη σύνδεση χωρίς κωδικό", "Σύνδεση με Google", "Σύνδεση με Facebook", "ή με email", "Συνέχεια", "Η σύνδεση OAuth απέτυχε. Δοκιμάστε ξανά."],
    "es":    ["Reclama tu perfil en Nevumo", "Regístrate gratis y gestiona tus clientes", "Reclamar perfil", "Acceso rápido sin contraseña", "Iniciar sesión con Google", "Iniciar sesión con Facebook", "o con correo", "Continuar", "El inicio de sesión OAuth falló. Inténtelo de nuevo."],
    "et":    ["Nõua oma profiili Nevumos", "Registreeru tasuta ja halda oma kliente", "Nõua profiili", "Kiire sisselogimine ilma paroolita", "Logi sisse Google'iga", "Logi sisse Facebookiga", "või e-postiga", "Jätka", "OAuth sisselogimine ebaõnnestus. Proovige uuesti."],
    "fi":    ["Lunasta profiilisi Nevumossa", "Rekisteröidy ilmaiseksi ja hallitse asiakkaitasi", "Lunasta profiili", "Nopea kirjautuminen ilman salasanaa", "Kirjaudu Googlella", "Kirjaudu Facebookilla", "tai sähköpostilla", "Jatka", "OAuth-kirjautuminen epäonnistui. Yritä uudelleen."],
    "fr":    ["Réclamez votre profil sur Nevumo", "Inscrivez-vous gratuitement et gérez vos clients", "Réclamer le profil", "Connexion rapide sans mot de passe", "Se connecter avec Google", "Se connecter avec Facebook", "ou avec e-mail", "Continuer", "La connexion OAuth a échoué. Veuillez réessayer."],
    "ga":    ["Éiligh do phróifíl ar Nevumo", "Cláraigh saor in aisce agus bainistigh do chustaiméirí", "Éiligh próifíl", "Logáil isteach tapa gan pasfhocal", "Logáil isteach le Google", "Logáil isteach le Facebook", "nó le ríomhphost", "Lean ar aghaidh", "Theip ar logáil isteach OAuth. Déan iarracht eile."],
    "hr":    ["Preuzmite svoj profil na Nevumo", "Registrirajte se besplatno i upravljajte klijentima", "Preuzmi profil", "Brza prijava bez lozinke", "Prijavi se s Google", "Prijavi se s Facebook", "ili e-mailom", "Nastavi", "OAuth prijava nije uspjela. Pokušajte ponovno."],
    "hu":    ["Igényeld profilodat a Nevumón", "Regisztrálj ingyen és kezeld ügyfeleidet", "Profil igénylése", "Gyors bejelentkezés jelszó nélkül", "Bejelentkezés Google-lel", "Bejelentkezés Facebookkal", "vagy e-maillel", "Folytatás", "OAuth bejelentkezés sikertelen. Próbálja újra."],
    "is":    ["Krefjust prófílsins þíns á Nevumo", "Skráðu þig ókeypis og stjórnaðu viðskiptavinum þínum", "Gera kröfu um prófíl", "Fljótleg innskráning án lykilorðs", "Skráðu þig inn með Google", "Skráðu þig inn með Facebook", "eða með tölvupósti", "Halda áfram", "OAuth innskráning mistókst. Reyndu aftur."],
    "it":    ["Rivendica il tuo profilo su Nevumo", "Registrati gratuitamente e gestisci i tuoi clienti", "Rivendica profilo", "Accesso rapido senza password", "Accedi con Google", "Accedi con Facebook", "o con email", "Continua", "Accesso OAuth non riuscito. Riprova."],
    "lb":    ["Huelt äre Profil op Nevumo", "Registréiert Iech gratis a managet Är Clienten", "Profil iwwerhuelen", "Séier Login ouni Passwuert", "Mat Google aloggen", "Mat Facebook aloggen", "oder mat E-Mail", "Weider", "OAuth Login ass feelgeschloen. Versicht et nach."],
    "lt":    ["Perimkite savo profilį Nevumo", "Registruokitės nemokamai ir valdykite savo klientus", "Perimti profilį", "Greitas prisijungimas be slaptažodžio", "Prisijungti su Google", "Prisijungti su Facebook", "arba el. paštu", "Tęsti", "OAuth prisijungimas nepavyko. Pabandykite dar kartą."],
    "lv":    ["Pārņemiet savu profilu Nevumo", "Reģistrējieties bez maksas un pārvaldiet savus klientus", "Pārņemt profilu", "Ātra pieteikšanās bez paroles", "Pieteikties ar Google", "Pieteikties ar Facebook", "vai ar e-pastu", "Turpināt", "OAuth pieteikšanās neizdevās. Mēģiniet vēlreiz."],
    "mk":    ["Преземи го твојот профил на Nevumo", "Регистрирај се бесплатно и управувај со клиентите", "Преземи профил", "Брза најава без лозинка", "Најава со Google", "Најава со Facebook", "или со е-пошта", "Продолжи", "OAuth најавата не успеа. Обидете се повторно."],
    "mt":    ["Ikklejmja l-profil tiegħek fuq Nevumo", "Irreġistra b'xejn u mmaniġġja l-klijenti tiegħek", "Ikklejm profil", "Dħul rapidu mingħajr password", "Idħol b'Google", "Idħol b'Facebook", "jew bl-email", "Kompli", "Il-login OAuth falla. Erġa pprova."],
    "nl":    ["Claim uw profiel op Nevumo", "Registreer gratis en beheer uw klanten", "Profiel claimen", "Snel inloggen zonder wachtwoord", "Inloggen met Google", "Inloggen met Facebook", "of met e-mail", "Doorgaan", "OAuth-inloggen mislukt. Probeer het opnieuw."],
    "no":    ["Gjør krav på profilen din på Nevumo", "Registrer deg gratis og administrer kundene dine", "Gjør krav på profil", "Rask pålogging uten passord", "Logg inn med Google", "Logg inn med Facebook", "eller med e-post", "Fortsett", "OAuth-pålogging mislyktes. Prøv igjen."],
    "pt":    ["Reivindique seu perfil no Nevumo", "Registre-se gratuitamente e gerencie seus clientes", "Reivindicar perfil", "Login rápido sem senha", "Entrar com Google", "Entrar com Facebook", "ou com e-mail", "Continuar", "Login OAuth falhou. Tente novamente."],
    "pt-PT": ["Reivindique o seu perfil no Nevumo", "Registe-se gratuitamente e gira os seus clientes", "Reivindicar perfil", "Login rápido sem palavra-passe", "Entrar com Google", "Entrar com Facebook", "ou com e-mail", "Continuar", "Login OAuth falhou. Tente novamente."],
    "ro":    ["Revendicați profilul dvs. pe Nevumo", "Înregistrați-vă gratuit și gestionați-vă clienții", "Revendicați profilul", "Autentificare rapidă fără parolă", "Conectați-vă cu Google", "Conectați-vă cu Facebook", "sau cu e-mail", "Continuați", "Autentificarea OAuth a eșuat. Încercați din nou."],
    "ru":    ["Заберите свой профиль на Nevumo", "Зарегистрируйтесь бесплатно и управляйте клиентами", "Забрать профиль", "Быстрый вход без пароля", "Войти через Google", "Войти через Facebook", "или по email", "Продолжить", "OAuth вход не удался. Попробуйте еще раз."],
    "sk":    ["Prevezmite svoj profil na Nevumo", "Zaregistrujte sa zadarmo a spravujte svojich klientov", "Prevziať profil", "Rýchle prihlásenie bez hesla", "Prihlásiť sa cez Google", "Prihlásiť sa cez Facebook", "alebo e-mailom", "Pokračovať", "OAuth prihlásenie zlyhalo. Skúste to znova."],
    "sl":    ["Prevzemite svoj profil na Nevumo", "Registrirajte se brezplačno in upravljajte svoje stranke", "Prevzemi profil", "Hitra prijava brez gesla", "Prijavi se z Google", "Prijavi se z Facebook", "ali z e-pošto", "Nadaljuj", "OAuth prijava ni uspela. Poskusite znova."],
    "sq":    ["Merrni profilin tuaj në Nevumo", "Regjistrohuni falas dhe menaxhoni klientët tuaj", "Merr profilin", "Hyrje e shpejtë pa fjalëkalim", "Hyr me Google", "Hyr me Facebook", "ose me email", "Vazhdo", "Hyrja OAuth dështoi. Provo përsëri."],
    "sr":    ["Преузмите свој профил на Nevumo", "Региструјте се бесплатно и управљајте клијентима", "Преузмите профил", "Брза пријава без лозинке", "Пријавите се са Google", "Пријавите се са Facebook", "или е-поштом", "Настави", "OAuth пријава није успела. Покушајте поново."],
    "sv":    ["Gör anspråk på din profil på Nevumo", "Registrera dig gratis och hantera dina kunder", "Gör anspråk på profil", "Snabb inloggning utan lösenord", "Logga in med Google", "Logga in med Facebook", "eller med e-post", "Fortsätt", "OAuth-inloggning misslyckades. Försök igen."],
    "tr":    ["Nevumo'daki profilinizi alın", "Ücretsiz kaydolun ve müşterilerinizi yönetin", "Profili al", "Şifresiz hızlı giriş", "Google ile giriş yap", "Facebook ile giriş yap", "veya e-posta ile", "Devam et", "OAuth girişi başarısız oldu. Lütfen tekrar deneyin."],
    "uk":    ["Отримайте свій профіль на Nevumo", "Зареєструйтесь безкоштовно та керуйте клієнтами", "Отримати профіль", "Швидкий вхід без пароля", "Увійти через Google", "Увійти через Facebook", "або з email", "Продовжити", "Вхід через OAuth не вдався. Спробуйте ще раз."],
}

# Keys in order corresponding to the 9 values per language
KEYS = [
    "auth.claim_headline",
    "auth.claim_subtitle",
    "auth.claim_cta_btn",
    "auth.quick_login_label",
    "auth.google_btn",
    "auth.facebook_btn",
    "auth.or_with_email",
    "auth.continue_btn",
    "auth.oauth_error",
]


def seed_translations() -> int:
    """Seed auth translations and return the number of rows upserted."""
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    rows_to_upsert = []
    for lang, values in TRANSLATIONS.items():
        for key, value in zip(KEYS, values):
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


if __name__ == "__main__":
    count = seed_translations()
    print(f"Upserted {count} rows (9 keys × 34 languages)")
