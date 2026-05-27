from apps.api.database import SessionLocal
from sqlalchemy import text

def seed():
    db = SessionLocal()
    try:
        rows = [
            ('en', 'provider_dashboard.widget_share_tiktok', 'Copy link for TikTok'),
            ('bg', 'provider_dashboard.widget_share_tiktok', 'Копирай линк за TikTok'),
            ('pl', 'provider_dashboard.widget_share_tiktok', 'Kopiuj link dla TikTok'),
            ('de', 'provider_dashboard.widget_share_tiktok', 'Link für TikTok kopieren'),
            ('fr', 'provider_dashboard.widget_share_tiktok', 'Copier le lien pour TikTok'),
            ('es', 'provider_dashboard.widget_share_tiktok', 'Copiar enlace para TikTok'),
            ('it', 'provider_dashboard.widget_share_tiktok', 'Copia link per TikTok'),
            ('pt', 'provider_dashboard.widget_share_tiktok', 'Copiar link para TikTok'),
            ('pt-PT', 'provider_dashboard.widget_share_tiktok', 'Copiar link para TikTok'),
            ('nl', 'provider_dashboard.widget_share_tiktok', 'Link kopiëren voor TikTok'),
            ('cs', 'provider_dashboard.widget_share_tiktok', 'Kopírovat odkaz pro TikTok'),
            ('sk', 'provider_dashboard.widget_share_tiktok', 'Kopírovať odkaz pre TikTok'),
            ('ro', 'provider_dashboard.widget_share_tiktok', 'Copiază link pentru TikTok'),
            ('hu', 'provider_dashboard.widget_share_tiktok', 'Link másolása TikTokhoz'),
            ('hr', 'provider_dashboard.widget_share_tiktok', 'Kopiraj link za TikTok'),
            ('sl', 'provider_dashboard.widget_share_tiktok', 'Kopiraj povezavo za TikTok'),
            ('da', 'provider_dashboard.widget_share_tiktok', 'Kopiér link til TikTok'),
            ('sv', 'provider_dashboard.widget_share_tiktok', 'Kopiera länk för TikTok'),
            ('no', 'provider_dashboard.widget_share_tiktok', 'Kopier lenke for TikTok'),
            ('fi', 'provider_dashboard.widget_share_tiktok', 'Kopioi linkki TikTokiin'),
            ('et', 'provider_dashboard.widget_share_tiktok', 'Kopeeri link TikToki jaoks'),
            ('lv', 'provider_dashboard.widget_share_tiktok', 'Kopēt saiti TikTok'),
            ('lt', 'provider_dashboard.widget_share_tiktok', 'Kopijuoti nuorodą TikTok'),
            ('el', 'provider_dashboard.widget_share_tiktok', 'Αντιγραφή συνδέσμου για TikTok'),
            ('ru', 'provider_dashboard.widget_share_tiktok', 'Скопировать ссылку для TikTok'),
            ('uk', 'provider_dashboard.widget_share_tiktok', 'Скопіювати посилання для TikTok'),
            ('sr', 'provider_dashboard.widget_share_tiktok', 'Kopiraj link za TikTok'),
            ('mk', 'provider_dashboard.widget_share_tiktok', 'Копирај линк за TikTok'),
            ('sq', 'provider_dashboard.widget_share_tiktok', 'Kopjo link për TikTok'),
            ('ga', 'provider_dashboard.widget_share_tiktok', 'Cóipeáil nasc do TikTok'),
            ('is', 'provider_dashboard.widget_share_tiktok', 'Afrita tengil fyrir TikTok'),
            ('lb', 'provider_dashboard.widget_share_tiktok', 'Link fir TikTok kopéieren'),
            ('mt', 'provider_dashboard.widget_share_tiktok', 'Ikkopja link għal TikTok'),
            ('tr', 'provider_dashboard.widget_share_tiktok', 'TikTok için link kopyala'),
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
