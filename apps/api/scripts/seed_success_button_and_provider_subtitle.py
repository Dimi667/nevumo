#!/usr/bin/env python3
"""
Script to upsert translation keys for category.new_request_button and provider_page.success_subtitle
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
    DATA = [
        # category.new_request_button
        ("bg", "category.new_request_button", "Нова заявка"),
        ("cs", "category.new_request_button", "Nová žádost"),
        ("da", "category.new_request_button", "Ny anmodning"),
        ("de", "category.new_request_button", "Neue Anfrage"),
        ("el", "category.new_request_button", "Νέο αίτημα"),
        ("en", "category.new_request_button", "New Request"),
        ("es", "category.new_request_button", "Nueva solicitud"),
        ("et", "category.new_request_button", "Uus päring"),
        ("fi", "category.new_request_button", "Uusi pyyntö"),
        ("fr", "category.new_request_button", "Nouvelle demande"),
        ("ga", "category.new_request_button", "Iarratas Nua"),
        ("hr", "category.new_request_button", "Novi zahtjev"),
        ("hu", "category.new_request_button", "Új kérés"),
        ("is", "category.new_request_button", "Ný beiðni"),
        ("it", "category.new_request_button", "Nuova richiesta"),
        ("lb", "category.new_request_button", "Nei Ufro"),
        ("lt", "category.new_request_button", "Nauja užklausa"),
        ("lv", "category.new_request_button", "Jauns pieprasījums"),
        ("mk", "category.new_request_button", "Нов барање"),
        ("mt", "category.new_request_button", "Talba Ġdida"),
        ("nl", "category.new_request_button", "Nieuw verzoek"),
        ("no", "category.new_request_button", "Ny forespørsel"),
        ("pl", "category.new_request_button", "Nowe zapytanie"),
        ("pt", "category.new_request_button", "Nova solicitação"),
        ("pt-PT", "category.new_request_button", "Nova solicitação"),
        ("ro", "category.new_request_button", "Cerere nouă"),
        ("ru", "category.new_request_button", "Новый запрос"),
        ("sk", "category.new_request_button", "Nová žiadosť"),
        ("sl", "category.new_request_button", "Nova zahteva"),
        ("sq", "category.new_request_button", "Kërkesë e re"),
        ("sr", "category.new_request_button", "Нови захтев"),
        ("sv", "category.new_request_button", "Ny förfrågan"),
        ("tr", "category.new_request_button", "Yeni talep"),
        ("uk", "category.new_request_button", "Новий запит"),
        # provider_page.success_subtitle
        ("bg", "provider_page.success_subtitle", "Вашата заявка беше изпратена на специалиста."),
        ("cs", "provider_page.success_subtitle", "Vaše žádost byla odeslána specialistovi."),
        ("da", "provider_page.success_subtitle", "Din anmodning er sendt til specialisten."),
        ("de", "provider_page.success_subtitle", "Ihre Anfrage wurde an den Spezialisten gesendet."),
        ("el", "provider_page.success_subtitle", "Το αίτημά σας εστάλη στον ειδικό."),
        ("en", "provider_page.success_subtitle", "Your request has been sent to the specialist."),
        ("es", "provider_page.success_subtitle", "Su solicitud ha sido enviada al especialista."),
        ("et", "provider_page.success_subtitle", "Teie päring on saadetud spetsialistile."),
        ("fi", "provider_page.success_subtitle", "Pyyntösi on lähetetty asiantuntijalle."),
        ("fr", "provider_page.success_subtitle", "Votre demande a été envoyée au spécialiste."),
        ("ga", "provider_page.success_subtitle", "Seoladh d'iarratas chuig an speisialtóir."),
        ("hr", "provider_page.success_subtitle", "Vaš zahtjev je poslan stručnjaku."),
        ("hu", "provider_page.success_subtitle", "Kérése elküldve a szakembernek."),
        ("is", "provider_page.success_subtitle", "Beiðni þín hefur verið send til sérfræðingsins."),
        ("it", "provider_page.success_subtitle", "La sua richiesta è stata inviata allo specialista."),
        ("lb", "provider_page.success_subtitle", "Är Ufro gouf un de Spezialist geschéckt."),
        ("lt", "provider_page.success_subtitle", "Jūsų užklausa išsiųsta specialistui."),
        ("lv", "provider_page.success_subtitle", "Jūsu pieprasījums ir nosūtīts speciālistam."),
        ("mk", "provider_page.success_subtitle", "Вашето барање е испратено на специјалистот."),
        ("mt", "provider_page.success_subtitle", "It-talba tiegħek intbagħtet lill-ispeċjalista."),
        ("nl", "provider_page.success_subtitle", "Uw verzoek is verzonden naar de specialist."),
        ("no", "provider_page.success_subtitle", "Din forespørsel er sendt til spesialisten."),
        ("pl", "provider_page.success_subtitle", "Twoje zapytanie zostało wysłane do specjalisty."),
        ("pt", "provider_page.success_subtitle", "Seu pedido foi enviado ao especialista."),
        ("pt-PT", "provider_page.success_subtitle", "O seu pedido foi enviado ao especialista."),
        ("ro", "provider_page.success_subtitle", "Cererea dvs. a fost trimisă specialistului."),
        ("ru", "provider_page.success_subtitle", "Ваш запрос был отправлен специалисту."),
        ("sk", "provider_page.success_subtitle", "Vaša žiadosť bola odoslaná špecialistovi."),
        ("sl", "provider_page.success_subtitle", "Vaša zahteva je bila poslana specialistu."),
        ("sq", "provider_page.success_subtitle", "Kërkesa juaj u dërgua te specialisti."),
        ("sr", "provider_page.success_subtitle", "Ваш захтев је послат специјалисти."),
        ("sv", "provider_page.success_subtitle", "Din förfrågan har skickats till specialisten."),
        ("tr", "provider_page.success_subtitle", "Talebiniz uzmana gönderildi."),
        ("uk", "provider_page.success_subtitle", "Ваш запит надіслано спеціалісту."),
    ]
    
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
        for lang, key, value in DATA:
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
