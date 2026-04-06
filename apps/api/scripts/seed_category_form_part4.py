#!/usr/bin/env python3
"""
Script to upsert translation keys for category form part 4
"""

import os
import psycopg2
from psycopg2 import sql

def main():
    # Database connection
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("ERROR: DATABASE_URL environment variable not set")
        return
    
    # Translation data
    translations = {
        'category.trust_multiple': {
            'bg': "Заявката се изпраща до няколко специалиста",
            'cs': "Vaše žádost bude odeslána více poskytovatelům",
            'da': "Din anmodning sendes til flere udbydere",
            'de': "Deine Anfrage wird an mehrere Anbieter gesendet",
            'el': "Το αίτημά σου αποστέλλεται σε πολλούς παρόχους",
            'en': "Your request will be sent to multiple providers",
            'es': "Tu solicitud se enviará a múltiples proveedores",
            'et': "Teie taotlus saadetakse mitmele teenusepakkujale",
            'fi': "Pyyntösi lähetetään useille palveluntarjoajille",
            'fr': "Votre demande sera envoyée à plusieurs prestataires",
            'ga': "Seolfar d'iarratas chuig roinnt soláthróirí",
            'hr': "Vaš zahtjev bit će poslan više pružatelja",
            'hu': "Kérése több szolgáltatóhoz kerül elküldésre",
            'is': "Beiðni þín verður send til margra þjónustuaðila",
            'it': "La tua richiesta verrà inviata a più fornitori",
            'lb': "Är Ufro gëtt un méi Ubidder geschéckt",
            'lt': "Jūsų užklausa bus išsiųsta keliems tiekėjams",
            'lv': "Jūsu pieprasījums tiks nosūtīts vairākiem pakalpojumu sniedzējiem",
            'mk': "Вашето барање ќе биде испратено до повеќе даватели",
            'mt': "It-talba tiegħek se tintbagħat lil diversi fornituri",
            'nl': "Uw aanvraag wordt naar meerdere aanbieders gestuurd",
            'no': "Din forespørsel sendes til flere leverandører",
            'pl': "Twoje zlecenie zostanie wysłane do wielu specjalistów",
            'pt': "Seu pedido será enviado para múltiplos prestadores",
            'pt-PT': "O seu pedido será enviado para vários prestadores",
            'ro': "Cererea ta va fi trimisă la mai mulți furnizori",
            'ru': "Ваша заявка будет отправлена нескольким специалистам",
            'sk': "Vaša žiadosť bude odoslaná viacerým poskytovateľom",
            'sl': "Vaša zahteva bo poslana več ponudnikom",
            'sq': "Kërkesa juaj do t'u dërgohet disa ofruesve",
            'sr': "Ваш захтев биће послат на више пружалаца",
            'sv': "Din förfrågan skickas till flera leverantörer",
            'tr': "Talebiniz birden fazla sağlayıcıya gönderilecek",
            'uk': "Ваш запит буде надіслано кільком спеціалістам"
        },
        'category.trust_response': {
            'bg': "Отговор до 30 мин",
            'cs': "Odpověď do 30 minut",
            'da': "Svar inden for 30 min",
            'de': "Antwort innerhalb von 30 Min",
            'el': "Απάντηση εντός 30 λεπτών",
            'en': "Response within 30 min",
            'es': "Respuesta en 30 min",
            'et': "Vastus 30 minuti jooksul",
            'fi': "Vastaus 30 minuutin kuluessa",
            'fr': "Réponse en 30 min",
            'ga': "Freagra laistigh de 30 nóiméad",
            'hr': "Odgovor unutar 30 min",
            'hu': "Válasz 30 percen belül",
            'is': "Svar innan 30 mínútna",
            'it': "Risposta entro 30 min",
            'lb': "Äntwert bannent 30 Minutten",
            'lt': "Atsakymas per 30 min",
            'lv': "Atbilde 30 minūšu laikā",
            'mk': "Одговор за 30 мин",
            'mt': "Risposta fi 30 minuta",
            'nl': "Reactie binnen 30 min",
            'no': "Svar innen 30 min",
            'pl': "Odpowiedź w ciągu 30 min",
            'pt': "Resposta em 30 min",
            'pt-PT': "Resposta em 30 min",
            'ro': "Răspuns în 30 min",
            'ru': "Ответ в течение 30 мин",
            'sk': "Odpoveď do 30 minút",
            'sl': "Odgovor v 30 min",
            'sq': "Përgjigje brenda 30 min",
            'sr': "Одговор у року од 30 мин",
            'sv': "Svar inom 30 min",
            'tr': "30 dk içinde yanıt",
            'uk': "Відповідь протягом 30 хв"
        },
        'category.sticky_btn': {
            'bg': "Получи оферти — безплатно",
            'cs': "Získat nabídky — zdarma",
            'da': "Få tilbud — gratis",
            'de': "Angebote erhalten — kostenlos",
            'el': "Λήψη προσφορών — δωρεάν",
            'en': "Get offers — Free",
            'es': "Obtener ofertas — Gratis",
            'et': "Hangi pakkumised — tasuta",
            'fi': "Hae tarjouksia — ilmaiseksi",
            'fr': "Obtenir des offres — Gratuit",
            'ga': "Faigh tairiscintí — Saor in aisce",
            'hr': "Dobij ponude — Besplatno",
            'hu': "Ajánlatok kérése — Ingyenes",
            'is': "Fá tilboð — Ókeypis",
            'it': "Ottieni offerte — Gratis",
            'lb': "Ubidder kréien — Gratis",
            'lt': "Gauti pasiūlymus — nemokamai",
            'lv': "Saņemt piedāvājumus — bez maksas",
            'mk': "Добиј понуди — Бесплатно",
            'mt': "Ikseb offerti — Bla ħlas",
            'nl': "Offertes ontvangen — Gratis",
            'no': "Få tilbud — Gratis",
            'pl': "Otrzymaj oferty — Bezpłatnie",
            'pt': "Receber propostas — Grátis",
            'pt-PT': "Receber propostas — Grátis",
            'ro': "Primește oferte — Gratuit",
            'ru': "Получить предложения — бесплатно",
            'sk': "Získať ponuky — zadarmo",
            'sl': "Prejmi ponudbe — brezplačno",
            'sq': "Merr oferta — Falas",
            'sr': "Добиј понуде — Бесплатно",
            'sv': "Få erbjudanden — Gratis",
            'tr': "Teklif al — Ücretsiz",
            'uk': "Отримати пропозиції — безкоштовно"
        }
    }
    
    try:
        # Connect to database
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        # Prepare upsert query
        upsert_query = sql.SQL("""
            INSERT INTO translations (lang, key, value)
            VALUES (%s, %s, %s)
            ON CONFLICT (lang, key) 
            DO UPDATE SET 
                value = EXCLUDED.value
        """)
        
        rows_upserted = 0
        
        # Execute upserts
        for key, lang_values in translations.items():
            for lang, value in lang_values.items():
                cursor.execute(upsert_query, (lang, key, value))
                rows_upserted += 1
        
        # Commit transaction
        conn.commit()
        
        print(f"Successfully upserted {rows_upserted} translation rows")
        
    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
