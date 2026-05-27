from apps.api.database import SessionLocal
from sqlalchemy import text

def seed():
    db = SessionLocal()
    try:
        rows = [
            ('en', 'provider_dashboard.widget_how_step2', 'Paste it into your website\'s HTML'),
            ('en', 'provider_dashboard.widget_how_step3', 'Clients send requests directly to you'),
            ('bg', 'provider_dashboard.widget_how_step2', 'Поставете го в HTML кода на вашия сайт'),
            ('bg', 'provider_dashboard.widget_how_step3', 'Клиентите изпращат заявки директно към вас'),
            ('pl', 'provider_dashboard.widget_how_step2', 'Wklej go do HTML swojej strony'),
            ('pl', 'provider_dashboard.widget_how_step3', 'Klienci wysyłają zapytania bezpośrednio do Ciebie'),
            ('de', 'provider_dashboard.widget_how_step2', 'Fügen Sie es in das HTML Ihrer Website ein'),
            ('de', 'provider_dashboard.widget_how_step3', 'Kunden senden Anfragen direkt an Sie'),
            ('fr', 'provider_dashboard.widget_how_step2', 'Collez-le dans le HTML de votre site'),
            ('fr', 'provider_dashboard.widget_how_step3', 'Les clients envoient des demandes directement à vous'),
            ('es', 'provider_dashboard.widget_how_step2', 'Pégalo en el HTML de tu sitio web'),
            ('es', 'provider_dashboard.widget_how_step3', 'Los clientes envían solicitudes directamente a ti'),
            ('it', 'provider_dashboard.widget_how_step2', 'Incollalo nel HTML del tuo sito'),
            ('it', 'provider_dashboard.widget_how_step3', 'I clienti inviano richieste direttamente a te'),
            ('pt', 'provider_dashboard.widget_how_step2', 'Cole no HTML do seu site'),
            ('pt', 'provider_dashboard.widget_how_step3', 'Os clientes enviam pedidos diretamente para você'),
            ('pt-PT', 'provider_dashboard.widget_how_step2', 'Cole no HTML do seu site'),
            ('pt-PT', 'provider_dashboard.widget_how_step3', 'Os clientes enviam pedidos diretamente para si'),
            ('nl', 'provider_dashboard.widget_how_step2', 'Plak het in de HTML van uw website'),
            ('nl', 'provider_dashboard.widget_how_step3', 'Klanten sturen aanvragen rechtstreeks naar u'),
            ('cs', 'provider_dashboard.widget_how_step2', 'Vložte ho do HTML vašeho webu'),
            ('cs', 'provider_dashboard.widget_how_step3', 'Klienti zasílají požadavky přímo vám'),
            ('sk', 'provider_dashboard.widget_how_step2', 'Vložte ho do HTML vašej stránky'),
            ('sk', 'provider_dashboard.widget_how_step3', 'Klienti posielajú požiadavky priamo vám'),
            ('ro', 'provider_dashboard.widget_how_step2', 'Lipiți-l în HTML-ul site-ului dvs.'),
            ('ro', 'provider_dashboard.widget_how_step3', 'Clienții trimit cereri direct la tine'),
            ('hu', 'provider_dashboard.widget_how_step2', 'Illessze be a weboldal HTML-jébe'),
            ('hu', 'provider_dashboard.widget_how_step3', 'Az ügyfelek közvetlenül neked küldenek kérelmeket'),
            ('hr', 'provider_dashboard.widget_how_step2', 'Zalijepite ga u HTML vaše web stranice'),
            ('hr', 'provider_dashboard.widget_how_step3', 'Klijenti šalju zahtjeve izravno vama'),
            ('sl', 'provider_dashboard.widget_how_step2', 'Prilepite ga v HTML vaše spletne strani'),
            ('sl', 'provider_dashboard.widget_how_step3', 'Stranke pošiljajo zahteve neposredno vam'),
            ('da', 'provider_dashboard.widget_how_step2', 'Indsæt det i dit websteds HTML'),
            ('da', 'provider_dashboard.widget_how_step3', 'Kunder sender anmodninger direkte til dig'),
            ('sv', 'provider_dashboard.widget_how_step2', 'Klistra in det i webbplatsens HTML'),
            ('sv', 'provider_dashboard.widget_how_step3', 'Kunder skickar förfrågningar direkt till dig'),
            ('no', 'provider_dashboard.widget_how_step2', 'Lim det inn i nettstedets HTML'),
            ('no', 'provider_dashboard.widget_how_step3', 'Kunder sender forespørsler direkte til deg'),
            ('fi', 'provider_dashboard.widget_how_step2', 'Liitä se verkkosivustosi HTML:ään'),
            ('fi', 'provider_dashboard.widget_how_step3', 'Asiakkaat lähettävät pyynnöt suoraan sinulle'),
            ('et', 'provider_dashboard.widget_how_step2', 'Kleebi see oma veebisaidi HTML-i'),
            ('et', 'provider_dashboard.widget_how_step3', 'Kliendid saadavad päringud otse sulle'),
            ('lv', 'provider_dashboard.widget_how_step2', 'Ielīmējiet to savas vietnes HTML'),
            ('lv', 'provider_dashboard.widget_how_step3', 'Klienti sūta pieprasījumus tieši jums'),
            ('lt', 'provider_dashboard.widget_how_step2', 'Įklijuokite tai į savo svetainės HTML'),
            ('lt', 'provider_dashboard.widget_how_step3', 'Klientai siunčia užklausas tiesiogiai jums'),
            ('el', 'provider_dashboard.widget_how_step2', 'Επικολλήστε το στο HTML του ιστότοπού σας'),
            ('el', 'provider_dashboard.widget_how_step3', 'Οι πελάτες στέλνουν αιτήσεις απευθείας σε εσάς'),
            ('ru', 'provider_dashboard.widget_how_step2', 'Вставьте его в HTML вашего сайта'),
            ('ru', 'provider_dashboard.widget_how_step3', 'Клиенты отправляют заявки напрямую вам'),
            ('uk', 'provider_dashboard.widget_how_step2', 'Вставте його в HTML вашого сайту'),
            ('uk', 'provider_dashboard.widget_how_step3', 'Клієнти надсилають заявки безпосередньо вам'),
            ('sr', 'provider_dashboard.widget_how_step2', 'Nalepite ga u HTML vašeg sajta'),
            ('sr', 'provider_dashboard.widget_how_step3', 'Klijenti šalju zahteve direktno vama'),
            ('mk', 'provider_dashboard.widget_how_step2', 'Залепете го во HTML на вашиот сајт'),
            ('mk', 'provider_dashboard.widget_how_step3', 'Клиентите праќаат барања директно до вас'),
            ('sq', 'provider_dashboard.widget_how_step2', 'Ngjisni në HTML të faqes suaj'),
            ('sq', 'provider_dashboard.widget_how_step3', 'Klientët dërgojnë kërkesa drejtpërdrejt te ju'),
            ('ga', 'provider_dashboard.widget_how_step2', 'Greamaigh é in HTML do láithreáin ghréasáin'),
            ('ga', 'provider_dashboard.widget_how_step3', 'Seolann cliant iarratais chuig tú go díreach'),
            ('is', 'provider_dashboard.widget_how_step2', 'Límdu það inn í HTML vefsíðunnar þinnar'),
            ('is', 'provider_dashboard.widget_how_step3', 'Viðskiptavinir senda beiðnir beint til þín'),
            ('lb', 'provider_dashboard.widget_how_step2', 'Füge et an den HTML vun ärer Websäit'),
            ('lb', 'provider_dashboard.widget_how_step3', 'Clienten schécken Ufroe direkt un Iech'),
            ('mt', 'provider_dashboard.widget_how_step2', 'Daqqa fil-HTML tas-sit tiegħek'),
            ('mt', 'provider_dashboard.widget_how_step3', 'Il-klijenti jibagħtu t-talbiet direttament lilek'),
            ('tr', 'provider_dashboard.widget_how_step2', 'Web sitenizin HTML\'ine yapıştırın'),
            ('tr', 'provider_dashboard.widget_how_step3', 'Müşteriler istekleri doğrudan size gönderir'),
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
