#!/usr/bin/env python3
"""Final translation fix - UPSERT specific translation keys for bg and en."""

import os
import psycopg2
from psycopg2.extras import execute_values

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://nevumo:nevumo@localhost:5432/nevumo_leads")

# Exact translations provided by user
TRANSLATIONS = {
    "bg": {
        "aria_close": "Затвори",
        "btn_close": "Затвори",
        "auth.hero_title_provider": "Разширете бизнеса си с Nevumo",
        "auth.hero_title_client": "Намерете най-добрите експерти във вашия район",
        "auth.hero_subtitle_client": "Получете оферти от доверени професионалисти за минути",
        "auth.coming_soon": "Очаквайте скоро...",
        "auth.password_placeholder_login": "Въведете вашата парола",
        "auth.error_wrong_password": "Невалидна парола. Моля, опитайте отново.",
        "auth.forgot_password_link": "Забравена парола?",
        "auth.logging_in_btn": "Влизане...",
        "auth.login_btn": "Вход",
        "auth.register_subtitle": "Създайте своя професионален профил",
        "auth.password_placeholder_register": "Изберете сигурна парола",
        "auth.registering_btn": "Създаване на профил...",
        "auth.register_success": "Регистрацията е успешна!",
        "auth.forgot_title": "Възстановяване на парола",
        "auth.forgot_subtitle": "Въведете имейл за линк за възстановяване",
        "auth.forgot_sent_btn": "Имейлът е изпратен!",
        "auth.sending_btn": "Изпращане...",
        "auth.forgot_send_btn": "Изпрати линк",
        "auth.forgot_check_email": "Проверете пощата си",
        "auth.checking_btn": "Проверка...",
        "auth.error_generic": "Нещо се обърка. Опитайте пак.",
        "auth.error_rate_limit": "Твърде много опити. Опитайте по-късно.",
        "category.seo_cleaning_p3": "Надеждни почистващи услуги за вашия дом или офис. Нашите проверени професионалисти гарантират безупречна чистота, за да се фокусирате върху важното.",
        "category.seo_massage_p3": "Професионална масажна терапия за облекчаване на стреса и подобряване на тонуса. Резервирайте сесия при опитни терапевти във вашия град.",
        "category.seo_plumbing_p3": "Експертни водопроводни услуги за спешни случаи или планови ремонти. Бърза реакция и гарантирано качество от местни специалисти.",
        "shortcut-recorder": "Натиснете клавиши за бърз достъп",
    },
    "en": {
        "aria_close": "Close",
        "btn_close": "Close",
        "auth.hero_title_provider": "Grow your business with Nevumo",
        "auth.hero_title_client": "Find the best experts in your area",
        "auth.hero_subtitle_client": "Get quotes from trusted professionals in minutes",
        "auth.coming_soon": "Coming soon...",
        "auth.password_placeholder_login": "Enter your password",
        "auth.error_wrong_password": "Invalid password. Please try again.",
        "auth.forgot_password_link": "Forgot password?",
        "auth.logging_in_btn": "Logging in...",
        "auth.login_btn": "Sign in",
        "auth.register_subtitle": "Create your professional profile",
        "auth.password_placeholder_register": "Choose a strong password",
        "auth.registering_btn": "Creating account...",
        "auth.register_success": "Registration successful!",
        "auth.forgot_title": "Reset password",
        "auth.forgot_subtitle": "Enter email to receive reset link",
        "auth.forgot_sent_btn": "Email sent!",
        "auth.sending_btn": "Sending...",
        "auth.forgot_send_btn": "Send reset link",
        "auth.forgot_check_email": "Check your email",
        "auth.checking_btn": "Checking...",
        "auth.error_generic": "Something went wrong. Try again.",
        "auth.error_rate_limit": "Too many attempts. Try later.",
        "category.seo_cleaning_p3": "Reliable cleaning services for your home or office. Our verified professionals ensure a spotless environment so you can focus on what matters.",
        "category.seo_massage_p3": "Professional massage therapy to relieve stress and improve your well-being. Book a session with experienced therapists in your city.",
        "category.seo_plumbing_p3": "Expert plumbing solutions for any emergency or planned repair. Quick response and guaranteed quality from local plumbing specialists.",
        "shortcut-recorder": "Press keys to record shortcut",
    },
}


def seed_translations() -> int:
    """UPSERT translations and return the number of rows upserted."""
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
    print(f"Upserted {count} translation rows")
