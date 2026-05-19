#!/usr/bin/env python3
"""Seed auth OAuth terms translations into the translations table."""

import os
import psycopg2
from psycopg2.extras import execute_values

# Database connection string
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://nevumo:nevumo@localhost:5433/nevumo_leads")

# Translations: language -> dict of key -> value
TRANSLATIONS = {
  "bg": {
    "auth.oauth_terms_title": "Преди да продължиш",
    "auth.oauth_terms_subtitle": "Моля прочети и приеми условията",
    "auth.oauth_continue_google": "Продължи с Google",
    "auth.oauth_error_generic": "Възникна грешка. Моля опитай отново."
  },
  "cs": {
    "auth.oauth_terms_title": "Než budete pokračovat",
    "auth.oauth_terms_subtitle": "Přečtěte si prosím a přijměte podmínky",
    "auth.oauth_continue_google": "Pokračovat přes Google",
    "auth.oauth_error_generic": "Došlo k chybě. Zkuste to prosím znovu."
  },
  "da": {
    "auth.oauth_terms_title": "Før du fortsætter",
    "auth.oauth_terms_subtitle": "Læs og accepter venligst vilkårene",
    "auth.oauth_continue_google": "Fortsæt med Google",
    "auth.oauth_error_generic": "Der opstod en fejl. Prøv venligst igen."
  },
  "de": {
    "auth.oauth_terms_title": "Bevor Sie fortfahren",
    "auth.oauth_terms_subtitle": "Bitte lesen und akzeptieren Sie die Bedingungen",
    "auth.oauth_continue_google": "Mit Google fortfahren",
    "auth.oauth_error_generic": "Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut."
  },
  "el": {
    "auth.oauth_terms_title": "Πριν συνεχίσετε",
    "auth.oauth_terms_subtitle": "Παρακαλώ διαβάστε και αποδεχτείτε τους όρους",
    "auth.oauth_continue_google": "Συνέχεια με Google",
    "auth.oauth_error_generic": "Προέκυψε ένα σφάλμα. Παρακαλώ προσπαθήστε ξανά."
  },
  "en": {
    "auth.oauth_terms_title": "Before you continue",
    "auth.oauth_terms_subtitle": "Please read and accept the terms and conditions",
    "auth.oauth_continue_google": "Continue with Google",
    "auth.oauth_error_generic": "An error occurred. Please try again."
  },
  "es": {
    "auth.oauth_terms_title": "Antes de continuar",
    "auth.oauth_terms_subtitle": "Por favor, lea y acepte los términos",
    "auth.oauth_continue_google": "Continuar con Google",
    "auth.oauth_error_generic": "Ocurrió un error. Por favor, inténtelo de nuevo."
  },
  "et": {
    "auth.oauth_terms_title": "Enne jätkamist",
    "auth.oauth_terms_subtitle": "Palun lugege ja nõustuge tingimustega",
    "auth.oauth_continue_google": "Jätka Google'iga",
    "auth.oauth_error_generic": "Ilmnes viga. Palun proovige uuesti."
  },
  "fi": {
    "auth.oauth_terms_title": "Ennen kuin jatkat",
    "auth.oauth_terms_subtitle": "Lue ja hyväksy ehdot",
    "auth.oauth_continue_google": "Jatka Google-tilillä",
    "auth.oauth_error_generic": "Tapahtui virhe. Ole hyvä ja yritä uudelleen."
  },
  "fr": {
    "auth.oauth_terms_title": "Avant de continuer",
    "auth.oauth_terms_subtitle": "Veuillez lire et accepter les conditions",
    "auth.oauth_continue_google": "Continuer avec Google",
    "auth.oauth_error_generic": "Une erreur est survenue. Veuillez réessayer."
  },
  "ga": {
    "auth.oauth_terms_title": "Sula leanann tú ar aghaidh",
    "auth.oauth_terms_subtitle": "Ligh agus glac leis na téarmaí, le do thoil",
    "auth.oauth_continue_google": "Lean ar aghaidh le Google",
    "auth.oauth_error_generic": "Tharla earráid. Déan iarracht arís, le do thoil."
  },
  "hr": {
    "auth.oauth_terms_title": "Prije nego što nastavite",
    "auth.oauth_terms_subtitle": "Molimo pročitajte i prihvatite uvjete",
    "auth.oauth_continue_google": "Nastavi putem Googlea",
    "auth.oauth_error_generic": "Došlo je do pogreške. Molimo pokušajte ponovno."
  },
  "hu": {
    "auth.oauth_terms_title": "Mielőtt folytatná",
    "auth.oauth_terms_subtitle": "Kérjük, olvassa el és fogadja el a feltételeket",
    "auth.oauth_continue_google": "Folytatás a Google-lal",
    "auth.oauth_error_generic": "Hiba történt. Kérjük, próbálja újra."
  },
  "is": {
    "auth.oauth_terms_title": "Áður en þú heldur áfram",
    "auth.oauth_terms_subtitle": "Vinsamlegast lestu og samþykktu skilmálana",
    "auth.oauth_continue_google": "Halda áfram með Google",
    "auth.oauth_error_generic": "Villa kom upp. Vinsamlegast reyndu aftur."
  },
  "it": {
    "auth.oauth_terms_title": "Prima di continuare",
    "auth.oauth_terms_subtitle": "Si prega di leggere e accettare i termini",
    "auth.oauth_continue_google": "Continua con Google",
    "auth.oauth_error_generic": "Si è verificato un errore. Si prega di riprovare."
  },
  "lb": {
    "auth.oauth_terms_title": "Ier Dir weiderfuerat",
    "auth.oauth_terms_subtitle": "Liest an akzeptéiert wgl. d'Konditiounen",
    "auth.oauth_continue_google": "Weidergi mat Google",
    "auth.oauth_error_generic": "Et ass e Feeler opgetrueden. Probéiert wgl. nach eng Kéier."
  },
  "lt": {
    "auth.oauth_terms_title": "Prieš tęsiant",
    "auth.oauth_terms_subtitle": "Perskaitykite ir sutikite su sąlygomis",
    "auth.oauth_continue_google": "Tęsti su „Google“",
    "auth.oauth_error_generic": "Įvyko klaida. Bandykite dar kartą."
  },
  "lv": {
    "auth.oauth_terms_title": "Pirms turpināt",
    "auth.oauth_terms_subtitle": "Lūdzu, izlasiet un apstipriniet noteikumus",
    "auth.oauth_continue_google": "Turpināt ar Google",
    "auth.oauth_error_generic": "Radās kļūda. Lūdzu, mēģiniet vēlreiz."
  },
  "mk": {
    "auth.oauth_terms_title": "Пред да продолжите",
    "auth.oauth_terms_subtitle": "Ве молиме прочитајте ги и прифатете ги условите",
    "auth.oauth_continue_google": "Продолжи со Google",
    "auth.oauth_error_generic": "Настана грешка. Ве молиме обидете се повторно."
  },
  "mt": {
    "auth.oauth_terms_title": "Qabel ma tkompli",
    "auth.oauth_terms_subtitle": "Jekk jogħġbok aqra u aċċetta t-termini",
    "auth.oauth_continue_google": "Kompli bil-Google",
    "auth.oauth_error_generic": "Inqala' żball. Jekk jogħġbok erġa' pprova."
  },
  "nl": {
    "auth.oauth_terms_title": "Voordat u verdergaat",
    "auth.oauth_terms_subtitle": "Lees en accepteer de voorwaarden",
    "auth.oauth_continue_google": "Doorgaan met Google",
    "auth.oauth_error_generic": "Er is een fout opgetreden. Probeer het opnieuw."
  },
  "no": {
    "auth.oauth_terms_title": "Før du fortsetter",
    "auth.oauth_terms_subtitle": "Vennligst les og godta vilkårene",
    "auth.oauth_continue_google": "Fortsett med Google",
    "auth.oauth_error_generic": "Det oppstod en feil. Vennligst prøv igjen."
  },
  "pl": {
    "auth.oauth_terms_title": "Zanim przejdziesz dalej",
    "auth.oauth_terms_subtitle": "Przeczytaj i zaakceptuj regulamin",
    "auth.oauth_continue_google": "Kontynuuj przez Google",
    "auth.oauth_error_generic": "Wystąpił błąd. Spróbuj ponownie."
  },
  "pt": {
    "auth.oauth_terms_title": "Antes de continuar",
    "auth.oauth_terms_subtitle": "Por favor, leia e aceite os termos",
    "auth.oauth_continue_google": "Continuar com Google",
    "auth.oauth_error_generic": "Ocorreu um erro. Por favor, tente novamente."
  },
  "pt-PT": {
    "auth.oauth_terms_title": "Antes de continuar",
    "auth.oauth_terms_subtitle": "Por favor, leia e aceite os termos e condições",
    "auth.oauth_continue_google": "Continuar com o Google",
    "auth.oauth_error_generic": "Ocorreu um erro. Por favor, tente novamente."
  },
  "ro": {
    "auth.oauth_terms_title": "Înainte de a continua",
    "auth.oauth_terms_subtitle": "Vă rugăm să citiți și să acceptați termenii",
    "auth.oauth_continue_google": "Continuă cu Google",
    "auth.oauth_error_generic": "A apărut o eroare. Vă rugăm să încercați din nou."
  },
  "ru": {
    "auth.oauth_terms_title": "Прежде чем продолжить",
    "auth.oauth_terms_subtitle": "Пожалуйста, ознакомьтесь и примите условия",
    "auth.oauth_continue_google": "Продолжить через Google",
    "auth.oauth_error_generic": "Произошла ошибка. Пожалуйста, попробуйте еще раз."
  },
  "sk": {
    "auth.oauth_terms_title": "Skôr ako budete pokračovať",
    "auth.oauth_terms_subtitle": "Prečítajte si a prijmite podmienky",
    "auth.oauth_continue_google": "Pokračovať cez Google",
    "auth.oauth_error_generic": "Vyskytla sa chyba. Skúste to znova."
  },
  "sl": {
    "auth.oauth_terms_title": "Preden nadaljujete",
    "auth.oauth_terms_subtitle": "Preberite in sprejmite pogoje",
    "auth.oauth_continue_google": "Nadaljuj z Googlom",
    "auth.oauth_error_generic": "Prišlo je do napake. Prosimo, poskusite znova."
  },
  "sq": {
    "auth.oauth_terms_title": "Para se të vazhdoni",
    "auth.oauth_terms_subtitle": "Ju lutemi lexoni dhe pranoni kushtet",
    "auth.oauth_continue_google": "Vazhdo me Google",
    "auth.oauth_error_generic": "Ndodhi një gabim. Ju lutemi provoni përsëri."
  },
  "sr": {
    "auth.oauth_terms_title": "Пре него што наставите",
    "auth.oauth_terms_subtitle": "Молимо прочитајте и прихватите услове",
    "auth.oauth_continue_google": "Настави путем Google-а",
    "auth.oauth_error_generic": "Дошло је до грешке. Молимо покушајте поново."
  },
  "sv": {
    "auth.oauth_terms_title": "Innan du fortsätter",
    "auth.oauth_terms_subtitle": "Vänligen läs och godkänn villkoren",
    "auth.oauth_continue_google": "Fortsätt med Google",
    "auth.oauth_error_generic": "Ett fel uppstod. Vänligen försök igen."
  },
  "tr": {
    "auth.oauth_terms_title": "Devam etmeden önce",
    "auth.oauth_terms_subtitle": "Lütfen şartları okuyun ve kabul edin",
    "auth.oauth_continue_google": "Google ile devam et",
    "auth.oauth_error_generic": "Bir hata oluştu. Lütfen tekrar deneyin."
  },
  "uk": {
    "auth.oauth_terms_title": "Перш ніж продовжити",
    "auth.oauth_terms_subtitle": "Будь ласка, ознайомтеся та прийміть умови",
    "auth.oauth_continue_google": "Продовжити через Google",
    "auth.oauth_error_generic": "Виникла помилка. Будь ласка, спробуйте ще раз."
  }
}


def seed_translations() -> int:
    """Seed auth OAuth terms translations and return the number of rows upserted."""
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    rows_to_upsert = []
    for lang, translations in TRANSLATIONS.items():
        for key, value in translations.items():
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
    print(f"Upserted {count} rows (4 keys × 34 languages)")
