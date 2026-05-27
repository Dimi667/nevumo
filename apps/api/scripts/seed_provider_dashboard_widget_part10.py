from apps.api.database import SessionLocal
from sqlalchemy import text

def seed():
    db = SessionLocal()
    try:
        rows = [
            ('en', 'provider_dashboard.widget_share_facebook', 'Share on Facebook'),
            ('en', 'provider_dashboard.widget_share_instagram', 'Copy link for Instagram'),
            ('bg', 'provider_dashboard.widget_share_facebook', 'Сподели във Facebook'),
            ('bg', 'provider_dashboard.widget_share_instagram', 'Копирай линк за Instagram'),
            ('pl', 'provider_dashboard.widget_share_facebook', 'Udostępnij na Facebooku'),
            ('pl', 'provider_dashboard.widget_share_instagram', 'Kopiuj link dla Instagrama'),
            ('de', 'provider_dashboard.widget_share_facebook', 'Auf Facebook teilen'),
            ('de', 'provider_dashboard.widget_share_instagram', 'Link für Instagram kopieren'),
            ('fr', 'provider_dashboard.widget_share_facebook', 'Partager sur Facebook'),
            ('fr', 'provider_dashboard.widget_share_instagram', 'Copier le lien pour Instagram'),
            ('es', 'provider_dashboard.widget_share_facebook', 'Compartir en Facebook'),
            ('es', 'provider_dashboard.widget_share_instagram', 'Copiar enlace para Instagram'),
            ('it', 'provider_dashboard.widget_share_facebook', 'Condividi su Facebook'),
            ('it', 'provider_dashboard.widget_share_instagram', 'Copia link per Instagram'),
            ('pt', 'provider_dashboard.widget_share_facebook', 'Compartilhar no Facebook'),
            ('pt', 'provider_dashboard.widget_share_instagram', 'Copiar link para Instagram'),
            ('pt-PT', 'provider_dashboard.widget_share_facebook', 'Partilhar no Facebook'),
            ('pt-PT', 'provider_dashboard.widget_share_instagram', 'Copiar link para Instagram'),
            ('nl', 'provider_dashboard.widget_share_facebook', 'Delen op Facebook'),
            ('nl', 'provider_dashboard.widget_share_instagram', 'Link kopiëren voor Instagram'),
            ('cs', 'provider_dashboard.widget_share_facebook', 'Sdílet na Facebooku'),
            ('cs', 'provider_dashboard.widget_share_instagram', 'Kopírovat odkaz pro Instagram'),
            ('sk', 'provider_dashboard.widget_share_facebook', 'Zdieľať na Facebooku'),
            ('sk', 'provider_dashboard.widget_share_instagram', 'Kopírovať odkaz pre Instagram'),
            ('ro', 'provider_dashboard.widget_share_facebook', 'Distribuie pe Facebook'),
            ('ro', 'provider_dashboard.widget_share_instagram', 'Copiază link pentru Instagram'),
            ('hu', 'provider_dashboard.widget_share_facebook', 'Megosztás Facebookon'),
            ('hu', 'provider_dashboard.widget_share_instagram', 'Link másolása Instagramhoz'),
            ('hr', 'provider_dashboard.widget_share_facebook', 'Podijeli na Facebooku'),
            ('hr', 'provider_dashboard.widget_share_instagram', 'Kopiraj link za Instagram'),
            ('sl', 'provider_dashboard.widget_share_facebook', 'Deli na Facebooku'),
            ('sl', 'provider_dashboard.widget_share_instagram', 'Kopiraj povezavo za Instagram'),
            ('da', 'provider_dashboard.widget_share_facebook', 'Del på Facebook'),
            ('da', 'provider_dashboard.widget_share_instagram', 'Kopiér link til Instagram'),
            ('sv', 'provider_dashboard.widget_share_facebook', 'Dela på Facebook'),
            ('sv', 'provider_dashboard.widget_share_instagram', 'Kopiera länk för Instagram'),
            ('no', 'provider_dashboard.widget_share_facebook', 'Del på Facebook'),
            ('no', 'provider_dashboard.widget_share_instagram', 'Kopier lenke for Instagram'),
            ('fi', 'provider_dashboard.widget_share_facebook', 'Jaa Facebookissa'),
            ('fi', 'provider_dashboard.widget_share_instagram', 'Kopioi linkki Instagramiin'),
            ('et', 'provider_dashboard.widget_share_facebook', 'Jaga Facebookis'),
            ('et', 'provider_dashboard.widget_share_instagram', 'Kopeeri link Instagrami jaoks'),
            ('lv', 'provider_dashboard.widget_share_facebook', 'Kopīgot Facebook'),
            ('lv', 'provider_dashboard.widget_share_instagram', 'Kopēt saiti Instagram'),
            ('lt', 'provider_dashboard.widget_share_facebook', 'Bendrinti Facebook'),
            ('lt', 'provider_dashboard.widget_share_instagram', 'Kopijuoti nuorodą Instagram'),
            ('el', 'provider_dashboard.widget_share_facebook', 'Κοινοποίηση στο Facebook'),
            ('el', 'provider_dashboard.widget_share_instagram', 'Αντιγραφή συνδέσμου για Instagram'),
            ('ru', 'provider_dashboard.widget_share_facebook', 'Поделиться в Facebook'),
            ('ru', 'provider_dashboard.widget_share_instagram', 'Скопировать ссылку для Instagram'),
            ('uk', 'provider_dashboard.widget_share_facebook', 'Поділитися у Facebook'),
            ('uk', 'provider_dashboard.widget_share_instagram', 'Скопіювати посилання для Instagram'),
            ('sr', 'provider_dashboard.widget_share_facebook', 'Podeli na Facebooku'),
            ('sr', 'provider_dashboard.widget_share_instagram', 'Kopiraj link za Instagram'),
            ('mk', 'provider_dashboard.widget_share_facebook', 'Сподели на Facebook'),
            ('mk', 'provider_dashboard.widget_share_instagram', 'Копирај линк за Instagram'),
            ('sq', 'provider_dashboard.widget_share_facebook', 'Ndaj në Facebook'),
            ('sq', 'provider_dashboard.widget_share_instagram', 'Kopjo link për Instagram'),
            ('ga', 'provider_dashboard.widget_share_facebook', 'Roinn ar Facebook'),
            ('ga', 'provider_dashboard.widget_share_instagram', 'Cóipeáil nasc do Instagram'),
            ('is', 'provider_dashboard.widget_share_facebook', 'Deila á Facebook'),
            ('is', 'provider_dashboard.widget_share_instagram', 'Afrita tengil fyrir Instagram'),
            ('lb', 'provider_dashboard.widget_share_facebook', 'Op Facebook deelen'),
            ('lb', 'provider_dashboard.widget_share_instagram', 'Link fir Instagram kopéieren'),
            ('mt', 'provider_dashboard.widget_share_facebook', 'Aqsam fuq Facebook'),
            ('mt', 'provider_dashboard.widget_share_instagram', 'Ikkopja link għal Instagram'),
            ('tr', 'provider_dashboard.widget_share_facebook', 'Facebook\'ta paylaş'),
            ('tr', 'provider_dashboard.widget_share_instagram', 'Instagram için link kopyala'),
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
