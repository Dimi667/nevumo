from apps.api.database import SessionLocal
from sqlalchemy import text

def seed():
    db = SessionLocal()
    try:
        rows = [
            ('en', 'provider_dashboard.widget_how_title', 'How it works'),
            ('en', 'provider_dashboard.widget_how_step1', 'Copy the code above'),
            ('bg', 'provider_dashboard.widget_how_title', 'Как работи'),
            ('bg', 'provider_dashboard.widget_how_step1', 'Копирайте кода по-горе'),
            ('pl', 'provider_dashboard.widget_how_title', 'Jak to działa'),
            ('pl', 'provider_dashboard.widget_how_step1', 'Skopiuj powyższy kod'),
            ('de', 'provider_dashboard.widget_how_title', 'So funktioniert es'),
            ('de', 'provider_dashboard.widget_how_step1', 'Kopieren Sie den obigen Code'),
            ('fr', 'provider_dashboard.widget_how_title', 'Comment ça fonctionne'),
            ('fr', 'provider_dashboard.widget_how_step1', 'Copiez le code ci-dessus'),
            ('es', 'provider_dashboard.widget_how_title', 'Cómo funciona'),
            ('es', 'provider_dashboard.widget_how_step1', 'Copia el código de arriba'),
            ('it', 'provider_dashboard.widget_how_title', 'Come funziona'),
            ('it', 'provider_dashboard.widget_how_step1', 'Copia il codice sopra'),
            ('pt', 'provider_dashboard.widget_how_title', 'Como funciona'),
            ('pt', 'provider_dashboard.widget_how_step1', 'Copie o código acima'),
            ('pt-PT', 'provider_dashboard.widget_how_title', 'Como funciona'),
            ('pt-PT', 'provider_dashboard.widget_how_step1', 'Copie o código acima'),
            ('nl', 'provider_dashboard.widget_how_title', 'Hoe het werkt'),
            ('nl', 'provider_dashboard.widget_how_step1', 'Kopieer de bovenstaande code'),
            ('cs', 'provider_dashboard.widget_how_title', 'Jak to funguje'),
            ('cs', 'provider_dashboard.widget_how_step1', 'Zkopírujte výše uvedený kód'),
            ('sk', 'provider_dashboard.widget_how_title', 'Ako to funguje'),
            ('sk', 'provider_dashboard.widget_how_step1', 'Skopírujte vyššie uvedený kód'),
            ('ro', 'provider_dashboard.widget_how_title', 'Cum funcționează'),
            ('ro', 'provider_dashboard.widget_how_step1', 'Copiați codul de mai sus'),
            ('hu', 'provider_dashboard.widget_how_title', 'Hogyan működik'),
            ('hu', 'provider_dashboard.widget_how_step1', 'Másolja a fenti kódot'),
            ('hr', 'provider_dashboard.widget_how_title', 'Kako funkcionira'),
            ('hr', 'provider_dashboard.widget_how_step1', 'Kopirajte gornji kod'),
            ('sl', 'provider_dashboard.widget_how_title', 'Kako deluje'),
            ('sl', 'provider_dashboard.widget_how_step1', 'Kopirajte zgornjo kodo'),
            ('da', 'provider_dashboard.widget_how_title', 'Sådan fungerer det'),
            ('da', 'provider_dashboard.widget_how_step1', 'Kopiér koden ovenfor'),
            ('sv', 'provider_dashboard.widget_how_title', 'Hur det fungerar'),
            ('sv', 'provider_dashboard.widget_how_step1', 'Kopiera koden ovan'),
            ('no', 'provider_dashboard.widget_how_title', 'Slik fungerer det'),
            ('no', 'provider_dashboard.widget_how_step1', 'Kopier koden ovenfor'),
            ('fi', 'provider_dashboard.widget_how_title', 'Näin se toimii'),
            ('fi', 'provider_dashboard.widget_how_step1', 'Kopioi yllä oleva koodi'),
            ('et', 'provider_dashboard.widget_how_title', 'Kuidas see töötab'),
            ('et', 'provider_dashboard.widget_how_step1', 'Kopeeri ülalolev kood'),
            ('lv', 'provider_dashboard.widget_how_title', 'Kā tas darbojas'),
            ('lv', 'provider_dashboard.widget_how_step1', 'Kopējiet augstāk esošo kodu'),
            ('lt', 'provider_dashboard.widget_how_title', 'Kaip tai veikia'),
            ('lt', 'provider_dashboard.widget_how_step1', 'Nukopijuokite aukščiau esantį kodą'),
            ('el', 'provider_dashboard.widget_how_title', 'Πώς λειτουργεί'),
            ('el', 'provider_dashboard.widget_how_step1', 'Αντιγράψτε τον παραπάνω κώδικα'),
            ('ru', 'provider_dashboard.widget_how_title', 'Как это работает'),
            ('ru', 'provider_dashboard.widget_how_step1', 'Скопируйте код выше'),
            ('uk', 'provider_dashboard.widget_how_title', 'Як це працює'),
            ('uk', 'provider_dashboard.widget_how_step1', 'Скопіюйте код вище'),
            ('sr', 'provider_dashboard.widget_how_title', 'Kako funkcioniše'),
            ('sr', 'provider_dashboard.widget_how_step1', 'Kopirajte gornji kod'),
            ('mk', 'provider_dashboard.widget_how_title', 'Како функционира'),
            ('mk', 'provider_dashboard.widget_how_step1', 'Копирајте го горниот код'),
            ('sq', 'provider_dashboard.widget_how_title', 'Si funksionon'),
            ('sq', 'provider_dashboard.widget_how_step1', 'Kopjoni kodin e mësipërm'),
            ('ga', 'provider_dashboard.widget_how_title', 'Conas a oibríonn sé'),
            ('ga', 'provider_dashboard.widget_how_step1', 'Cóipeáil an cód thuas'),
            ('is', 'provider_dashboard.widget_how_title', 'Hvernig það virkar'),
            ('is', 'provider_dashboard.widget_how_step1', 'Afritaðu kóðann hér að ofan'),
            ('lb', 'provider_dashboard.widget_how_title', 'Wéi et funktionéiert'),
            ('lb', 'provider_dashboard.widget_how_step1', 'Kopéiert de Code hei uewen'),
            ('mt', 'provider_dashboard.widget_how_title', 'Kif jaħdem'),
            ('mt', 'provider_dashboard.widget_how_step1', 'Ikkopja l-kodiċi ta\' hawn fuq'),
            ('tr', 'provider_dashboard.widget_how_title', 'Nasıl çalışır'),
            ('tr', 'provider_dashboard.widget_how_step1', 'Yukarıdaki kodu kopyalayın'),
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
