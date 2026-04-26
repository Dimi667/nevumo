"""Idempotent seed script for provider card translation fixes.

Updates 2 keys across 34 languages (68 rows total).
Uses psycopg2 directly with INSERT ... ON CONFLICT for idempotency.
"""

import os
import sys

import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("ERROR: DATABASE_URL environment variable is not set.")
    sys.exit(1)

TRANSLATIONS = {
    "category.provider_desc_fallback": {
        "bg": "Изпрати безплатна заявка. Отговор до 30 минути.",
        "cs": "Pošli bezplatnou poptávku. Odpověď do 30 minut.",
        "da": "Send en gratis forespørgsel. Svar inden for 30 minutter.",
        "de": "Sende eine kostenlose Anfrage. Antwort innerhalb von 30 Minuten.",
        "el": "Στείλε δωρεάν αίτημα. Απάντηση εντός 30 λεπτών.",
        "en": "Send a free request. Response within 30 minutes.",
        "es": "Envía una solicitud gratuita. Respuesta en 30 minutos.",
        "et": "Saada tasuta päring. Vastus 30 minuti jooksul.",
        "fi": "Lähetä ilmainen pyyntö. Vastaus 30 minuutissa.",
        "fr": "Envoyez une demande gratuite. Réponse en 30 minutes.",
        "ga": "Seol iarratas saor in aisce. Freagra laistigh de 30 nóiméad.",
        "hr": "Pošalji besplatni upit. Odgovor u roku od 30 minuta.",
        "hu": "Küldj ingyenes megkeresést. Válasz 30 percen belül.",
        "is": "Sendu ókeypis fyrirspurn. Svar innan 30 mínútna.",
        "it": "Invia una richiesta gratuita. Risposta entro 30 minuti.",
        "lb": "Schéck eng gratis Ufro. Äntwert bannent 30 Minutten.",
        "lt": "Siųsk nemokamą užklausą. Atsakymas per 30 minučių.",
        "lv": "Sūti bezmaksas pieprasījumu. Atbilde 30 minūšu laikā.",
        "mk": "Испрати бесплатно барање. Одговор за 30 минути.",
        "mt": "Ibgħat talba bla ħlas. Risposta fi 30 minuta.",
        "nl": "Stuur een gratis aanvraag. Reactie binnen 30 minuten.",
        "no": "Send en gratis forespørsel. Svar innen 30 minutter.",
        "pl": "Wyślij bezpłatne zapytanie. Odpowiedź w ciągu 30 minut.",
        "pt": "Envie uma solicitação gratuita. Resposta em 30 minutos.",
        "pt-PT": "Envie um pedido gratuito. Resposta em 30 minutos.",
        "ro": "Trimite o solicitare gratuită. Răspuns în 30 de minute.",
        "ru": "Отправь бесплатную заявку. Ответ в течение 30 минут.",
        "sk": "Pošli bezplatnú požiadavku. Odpoveď do 30 minút.",
        "sl": "Pošlji brezplačno povpraševanje. Odgovor v 30 minutah.",
        "sq": "Dërgo një kërkesë falas. Përgjigje brenda 30 minutave.",
        "sr": "Пошаљи бесплатан захтев. Одговор у року од 30 минута.",
        "sv": "Skicka en gratis förfrågan. Svar inom 30 minuter.",
        "tr": "Ücretsiz talep gönder. 30 dakika içinde yanıt.",
        "uk": "Надішли безкоштовний запит. Відповідь протягом 30 хвилин.",
    },
    "category.provider_free_no_obligation": {
        "bg": "Безплатна заявка • Без ангажимент",
        "cs": "Bezplatná poptávka • Bez závazků",
        "da": "Gratis forespørgsel • Ingen forpligtelse",
        "de": "Kostenlose Anfrage • Unverbindlich",
        "el": "Δωρεάν αίτημα • Χωρίς δέσμευση",
        "en": "Free request • No obligation",
        "es": "Solicitud gratuita • Sin compromiso",
        "et": "Tasuta päring • Kohustuseta",
        "fi": "Ilmainen pyyntö • Ei sitoumuksia",
        "fr": "Demande gratuite • Sans engagement",
        "ga": "Iarratas saor in aisce • Gan oibleagáid",
        "hr": "Besplatni upit • Bez obveza",
        "hu": "Ingyenes megkeresés • Kötelezettség nélkül",
        "is": "Ókeypis fyrirspurn • Engar skuldbindingar",
        "it": "Richiesta gratuita • Senza impegno",
        "lb": "Gratis Ufro • Ouni Verpflichtung",
        "lt": "Nemokama užklausa • Jokių įsipareigojimų",
        "lv": "Bezmaksas pieprasījums • Bez saistībām",
        "mk": "Бесплатно барање • Без обврски",
        "mt": "Talba bla ħlas • Bla obbligu",
        "nl": "Gratis aanvraag • Geen verplichtingen",
        "no": "Gratis forespørsel • Ingen forpliktelse",
        "pl": "Bezpłatne zapytanie • Bez zobowiązań",
        "pt": "Solicitação gratuita • Sem compromisso",
        "pt-PT": "Pedido gratuito • Sem compromisso",
        "ro": "Solicitare gratuită • Fără obligații",
        "ru": "Бесплатная заявка • Без обязательств",
        "sk": "Bezplatná požiadavka • Bez záväzkov",
        "sl": "Brezplačno povpraševanje • Brez obveznosti",
        "sq": "Kërkesë falas • Pa detyrime",
        "sr": "Бесплатан захтев • Без обавеза",
        "sv": "Gratis förfrågan • Ingen förpliktelse",
        "tr": "Ücretsiz talep • Yükümlülük yok",
        "uk": "Безкоштовний запит • Без зобов'язань",
    },
}


def seed() -> None:
    conn = psycopg2.connect(DATABASE_URL)
    try:
        with conn.cursor() as cur:
            rows = []
            for key, lang_map in TRANSLATIONS.items():
                for lang, value in lang_map.items():
                    rows.append((lang, key, value))

            cur.executemany(
                """
                INSERT INTO translations (lang, key, value)
                VALUES (%s, %s, %s)
                ON CONFLICT (lang, key) DO UPDATE
                SET value = EXCLUDED.value;
                """,
                rows,
            )
            conn.commit()
            print(f"Upserted {len(rows)} translation rows.")
    finally:
        conn.close()


if __name__ == "__main__":
    seed()
