#!/usr/bin/env python3
"""Seed auth namespace translations into the translations table."""

import os
import psycopg2
from psycopg2.extras import execute_values

# Database connection string
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://nevumo:nevumo@localhost:5432/nevumo_leads")

# Translations: language -> list of 8 values in order
TRANSLATIONS = {
    "bg":    ["Вземи своя профил в Nevumo", "Регистрирай се безплатно и управлявай клиентите си", "Вземи профила", "Бърз вход без парола", "Вход с Google", "Вход с Facebook", "или с имейл", "Продължи"],
    "pl":    ["Przejmij swój profil w Nevumo", "Zarejestruj się za darmo i zarządzaj klientami", "Przejmij profil", "Szybkie logowanie bez hasła", "Zaloguj się z Google", "Zaloguj się z Facebook", "lub z e-mailem", "Kontynuuj"],
    "en":    ["Claim your profile on Nevumo", "Register for free and manage your clients", "Claim profile", "Quick login without password", "Sign in with Google", "Sign in with Facebook", "or with email", "Continue"],
    "de":    ["Nimm dein Profil auf Nevumo", "Registriere dich kostenlos und verwalte deine Kunden", "Profil beanspruchen", "Schnelle Anmeldung ohne Passwort", "Mit Google anmelden", "Mit Facebook anmelden", "oder mit E-Mail", "Weiter"],
    "cs":    ["Převezmi svůj profil na Nevumo", "Zaregistruj se zdarma a spravuj své zákazníky", "Převzít profil", "Rychlé přihlášení bez hesla", "Přihlásit se přes Google", "Přihlásit se přes Facebook", "nebo e-mailem", "Pokračovat"],
    "da":    ["Gør krav på din profil på Nevumo", "Registrer dig gratis og administrer dine kunder", "Gør krav på profil", "Hurtig login uden adgangskode", "Log ind med Google", "Log ind med Facebook", "eller med e-mail", "Fortsæt"],
    "el":    ["Διεκδικήστε το προφίλ σας στο Nevumo", "Εγγραφείτε δωρεάν και διαχειριστείτε τους πελάτες σας", "Διεκδίκηση προφίλ", "Γρήγορη σύνδεση χωρίς κωδικό", "Σύνδεση με Google", "Σύνδεση με Facebook", "ή με email", "Συνέχεια"],
    "es":    ["Reclama tu perfil en Nevumo", "Regístrate gratis y gestiona tus clientes", "Reclamar perfil", "Acceso rápido sin contraseña", "Iniciar sesión con Google", "Iniciar sesión con Facebook", "o con correo", "Continuar"],
    "et":    ["Nõua oma profiili Nevumos", "Registreeru tasuta ja halda oma kliente", "Nõua profiili", "Kiire sisselogimine ilma paroolita", "Logi sisse Google'iga", "Logi sisse Facebookiga", "või e-postiga", "Jätka"],
    "fi":    ["Lunasta profiilisi Nevumossa", "Rekisteröidy ilmaiseksi ja hallitse asiakkaitasi", "Lunasta profiili", "Nopea kirjautuminen ilman salasanaa", "Kirjaudu Googlella", "Kirjaudu Facebookilla", "tai sähköpostilla", "Jatka"],
    "fr":    ["Réclamez votre profil sur Nevumo", "Inscrivez-vous gratuitement et gérez vos clients", "Réclamer le profil", "Connexion rapide sans mot de passe", "Se connecter avec Google", "Se connecter avec Facebook", "ou avec e-mail", "Continuer"],
    "ga":    ["Éiligh do phróifíl ar Nevumo", "Cláraigh saor in aisce agus bainistigh do chustaiméirí", "Éiligh próifíl", "Logáil isteach tapa gan pasfhocal", "Logáil isteach le Google", "Logáil isteach le Facebook", "nó le ríomhphost", "Lean ar aghaidh"],
    "hr":    ["Preuzmite svoj profil na Nevumo", "Registrirajte se besplatno i upravljajte klijentima", "Preuzmi profil", "Brza prijava bez lozinke", "Prijavi se s Google", "Prijavi se s Facebook", "ili e-mailom", "Nastavi"],
    "hu":    ["Igényeld profilodat a Nevumón", "Regisztrálj ingyen és kezeld ügyfeleidet", "Profil igénylése", "Gyors bejelentkezés jelszó nélkül", "Bejelentkezés Google-lel", "Bejelentkezés Facebookkal", "vagy e-maillel", "Folytatás"],
    "is":    ["Krefjust prófílsins þíns á Nevumo", "Skráðu þig ókeypis og stjórnaðu viðskiptavinum þínum", "Gera kröfu um prófíl", "Fljótleg innskráning án lykilorðs", "Skráðu þig inn með Google", "Skráðu þig inn með Facebook", "eða með tölvupósti", "Halda áfram"],
    "it":    ["Rivendica il tuo profilo su Nevumo", "Registrati gratuitamente e gestisci i tuoi clienti", "Rivendica profilo", "Accesso rapido senza password", "Accedi con Google", "Accedi con Facebook", "o con email", "Continua"],
    "lb":    ["Huelt äre Profil op Nevumo", "Registréiert Iech gratis a managet Är Clienten", "Profil iwwerhuelen", "Séier Login ouni Passwuert", "Mat Google aloggen", "Mat Facebook aloggen", "oder mat E-Mail", "Weider"],
    "lt":    ["Perimkite savo profilį Nevumo", "Registruokitės nemokamai ir valdykite savo klientus", "Perimti profilį", "Greitas prisijungimas be slaptažodžio", "Prisijungti su Google", "Prisijungti su Facebook", "arba el. paštu", "Tęsti"],
    "lv":    ["Pārņemiet savu profilu Nevumo", "Reģistrējieties bez maksas un pārvaldiet savus klientus", "Pārņemt profilu", "Ātra pieteikšanās bez paroles", "Pieteikties ar Google", "Pieteikties ar Facebook", "vai ar e-pastu", "Turpināt"],
    "mk":    ["Преземи го твојот профил на Nevumo", "Регистрирај се бесплатно и управувај со клиентите", "Преземи профил", "Брза најава без лозинка", "Најава со Google", "Најава со Facebook", "или со е-пошта", "Продолжи"],
    "mt":    ["Ikklejmja l-profil tiegħek fuq Nevumo", "Irreġistra b'xejn u mmaniġġja l-klijenti tiegħek", "Ikklejm profil", "Dħul rapidu mingħajr password", "Idħol b'Google", "Idħol b'Facebook", "jew bl-email", "Kompli"],
    "nl":    ["Claim uw profiel op Nevumo", "Registreer gratis en beheer uw klanten", "Profiel claimen", "Snel inloggen zonder wachtwoord", "Inloggen met Google", "Inloggen met Facebook", "of met e-mail", "Doorgaan"],
    "no":    ["Gjør krav på profilen din på Nevumo", "Registrer deg gratis og administrer kundene dine", "Gjør krav på profil", "Rask pålogging uten passord", "Logg inn med Google", "Logg inn med Facebook", "eller med e-post", "Fortsett"],
    "pt":    ["Reivindique seu perfil no Nevumo", "Registre-se gratuitamente e gerencie seus clientes", "Reivindicar perfil", "Login rápido sem senha", "Entrar com Google", "Entrar com Facebook", "ou com e-mail", "Continuar"],
    "pt-PT": ["Reivindique o seu perfil no Nevumo", "Registe-se gratuitamente e gira os seus clientes", "Reivindicar perfil", "Login rápido sem palavra-passe", "Entrar com Google", "Entrar com Facebook", "ou com e-mail", "Continuar"],
    "ro":    ["Revendicați profilul dvs. pe Nevumo", "Înregistrați-vă gratuit și gestionați-vă clienții", "Revendicați profilul", "Autentificare rapidă fără parolă", "Conectați-vă cu Google", "Conectați-vă cu Facebook", "sau cu e-mail", "Continuați"],
    "ru":    ["Заберите свой профиль на Nevumo", "Зарегистрируйтесь бесплатно и управляйте клиентами", "Забрать профиль", "Быстрый вход без пароля", "Войти через Google", "Войти через Facebook", "или по email", "Продолжить"],
    "sk":    ["Prevezmite svoj profil na Nevumo", "Zaregistrujte sa zadarmo a spravujte svojich klientov", "Prevziať profil", "Rýchle prihlásenie bez hesla", "Prihlásiť sa cez Google", "Prihlásiť sa cez Facebook", "alebo e-mailom", "Pokračovať"],
    "sl":    ["Prevzemite svoj profil na Nevumo", "Registrirajte se brezplačno in upravljajte svoje stranke", "Prevzemi profil", "Hitra prijava brez gesla", "Prijavi se z Google", "Prijavi se z Facebook", "ali z e-pošto", "Nadaljuj"],
    "sq":    ["Merrni profilin tuaj në Nevumo", "Regjistrohuni falas dhe menaxhoni klientët tuaj", "Merr profilin", "Hyrje e shpejtë pa fjalëkalim", "Hyr me Google", "Hyr me Facebook", "ose me email", "Vazhdo"],
    "sr":    ["Преузмите свој профил на Nevumo", "Региструјте се бесплатно и управљајте клијентима", "Преузмите профил", "Брза пријава без лозинке", "Пријавите се са Google", "Пријавите се са Facebook", "или е-поштом", "Настави"],
    "sv":    ["Gör anspråk på din profil på Nevumo", "Registrera dig gratis och hantera dina kunder", "Gör anspråk på profil", "Snabb inloggning utan lösenord", "Logga in med Google", "Logga in med Facebook", "eller med e-post", "Fortsätt"],
    "tr":    ["Nevumo'daki profilinizi alın", "Ücretsiz kaydolun ve müşterilerinizi yönetin", "Profili al", "Şifresiz hızlı giriş", "Google ile giriş yap", "Facebook ile giriş yap", "veya e-posta ile", "Devam et"],
    "uk":    ["Отримайте свій профіль на Nevumo", "Зареєструйтесь безкоштовно та керуйте клієнтами", "Отримати профіль", "Швидкий вхід без пароля", "Увійти через Google", "Увійти через Facebook", "або з email", "Продовжити"],
}

# Keys in order corresponding to the 8 values per language
KEYS = [
    "auth.claim_headline",
    "auth.claim_subtitle",
    "auth.claim_cta_btn",
    "auth.quick_login_label",
    "auth.google_btn",
    "auth.facebook_btn",
    "auth.or_with_email",
    "auth.continue_btn",
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
    print(f"Upserted {count} rows (8 keys × 34 languages)")
