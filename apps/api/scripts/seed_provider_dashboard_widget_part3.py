from apps.api.database import SessionLocal
from sqlalchemy import text

def seed():
    db = SessionLocal()
    try:
        rows = [
            ('en', 'provider_dashboard.widget_subtitle', 'Add the request form to any site where possible! Clients will send requests directly to you.'),
            ('bg', 'provider_dashboard.widget_subtitle', 'Добави формата за заявки на всеки сайт където е възможно! Клиентите ще изпращат заявки директно към вас.'),
            ('pl', 'provider_dashboard.widget_subtitle', 'Dodaj formularz zapytań na każdej stronie, gdzie to możliwe! Klienci będą wysyłać zapytania bezpośrednio do Ciebie.'),
            ('de', 'provider_dashboard.widget_subtitle', 'Fügen Sie das Anfrageformular auf jeder möglichen Website hinzu! Kunden senden ihre Anfragen direkt an Sie.'),
            ('fr', 'provider_dashboard.widget_subtitle', 'Ajoutez le formulaire de demande sur n\'importe quel site là où c\'est possible ! Les clients vous enverront leurs demandes directement.'),
            ('es', 'provider_dashboard.widget_subtitle', '¡Añade el formulario de solicitud a cualquier sitio web donde sea posible! Los clientes te enviarán solicitudes directamente.'),
            ('it', 'provider_dashboard.widget_subtitle', 'Aggiungi il modulo di richiesta a qualsiasi sito web in cui sia possibile! I clienti invieranno le richieste direttamente a te.'),
            ('pt', 'provider_dashboard.widget_subtitle', 'Adicione o formulário de solicitação a qualquer site onde for possível! Os clientes enviarão solicitações diretamente para você.'),
            ('pt-PT', 'provider_dashboard.widget_subtitle', 'Adicione o formulário de pedido a qualquer site onde seja possível! Os clientes enviarão os pedidos diretamente para si.'),
            ('nl', 'provider_dashboard.widget_subtitle', 'Voeg het aanvraagformulier toe aan elke website waar dit mogelijk is! Klanten sturen aanvragen direct naar u toe.'),
            ('cs', 'provider_dashboard.widget_subtitle', 'Přidejte formulář žádosti na jakýkoli web, kde je to možné! Klienti vám budou posílat žádosti přímo.'),
            ('sk', 'provider_dashboard.widget_subtitle', 'Pridajte formulár žiadosti na akúkoľvek webovú stránku, kde je to možné! Klienti vám budú posielať žiadosti priamo.'),
            ('ro', 'provider_dashboard.widget_subtitle', 'Adaugă formularul de cerere pe orice site unde este posibil! Clienții vor trimite cererile direct către tine.'),
            ('hu', 'provider_dashboard.widget_subtitle', 'Adja hozzá az ajánlatkérő űrlapot minden weboldalhoz, ahol lehetséges! Az ügyfelek közvetlenül Önnek küldik majd a kéréseket.'),
            ('hr', 'provider_dashboard.widget_subtitle', 'Dodajte obrazac za zahtjeve na bilo koju web stranicu gdje je to moguće! Klijenti će slati zahtjeve izravno vama.'),
            ('sl', 'provider_dashboard.widget_subtitle', 'Dodajte obrazec za povpraševanje na katero koli spletno mesto, kjer je to mogoče! Stranke vam bodo pošiljale povpraševanja neposredno.'),
            ('da', 'provider_dashboard.widget_subtitle', 'Tilføj anmodningsformularen til ethvert websted, hvor det er muligt! Kunder vil sende anmodninger direkte til dig.'),
            ('sv', 'provider_dashboard.widget_subtitle', 'Lägg till förfrågningsformuläret på valfri webbplats där det är möjligt! Kunder kommer att skicka förfrågningar direkt till dig.'),
            ('no', 'provider_dashboard.widget_subtitle', 'Legg til forespørselsskjemaet på et hvilket som helst nettsted der det er mulig! Kunder vil sende forespørsler direkte til deg.'),
            ('fi', 'provider_dashboard.widget_subtitle', 'Lisää pyyntölomake mille tahansa sivustolle, missä se on mahdollista! Asiakkaat lähettävät pyynnöt suoraan sinulle.'),
            ('et', 'provider_dashboard.widget_subtitle', 'Lisa päringuvorm igale võimalikule veebisaidile! Kliendid saadavad päringud otse sulle.'),
            ('lv', 'provider_dashboard.widget_subtitle', 'Pievienojiet pieprasījuma veidlapu jebkurai vietnei, kur tas ir iespējams! Klienti sūtīs pieprasījumus tieši jums.'),
            ('lt', 'provider_dashboard.widget_subtitle', 'Pridėkite užklausų formą bet kurioje svetainėje, kur tai įmanoma! Klientai siųs užklausas tiesiai jums.'),
            ('el', 'provider_dashboard.widget_subtitle', 'Προσθέστε τη φόρμα αιτήματος σε οποιονδήποτε ιστότοπο, όπου είναι δυνατόν! Οι πελάτες θα στέλνουν αιτήματα απευθείας σε εσάς.'),
            ('ru', 'provider_dashboard.widget_subtitle', 'Добавьте форму заявки на любой сайт, где это возможно! Клиенты будут отправлять заявки напрямую вам.'),
            ('uk', 'provider_dashboard.widget_subtitle', 'Додайте форму заявки на будь-який сайт, де це можливо! Клієнти надсилатимуть заявки безпосередньо вам.'),
            ('sr', 'provider_dashboard.widget_subtitle', 'Dodajte obrazac za zahteve na svaki sajt gde je to moguće! Klijenti će slati zahteve direktno vama.'),
            ('mk', 'provider_dashboard.widget_subtitle', 'Додајте го формуларот за барања на која било веб-страница каде што е можно! Клиентите ќе испраќаат барања директно до вас.'),
            ('sq', 'provider_dashboard.widget_subtitle', 'Shtoni formularin e kërkesës në çdo faqe ku të jetë e mundur! Klientët do t\'i dërgojnë kërkesat drejtpërdrejt tek ju.'),
            ('ga', 'provider_dashboard.widget_subtitle', 'Cuir an fhoirm iarratais le haon suíomh nuair is féidir! Seolfaidh cliaint iarratais díreach chugat.'),
            ('is', 'provider_dashboard.widget_subtitle', 'Bættu beiðnaforminu við hvaða vefsíðu sem er þar sem það er mögulegt! Viðskiptavinir munu senda beiðnir beint til þín.'),
            ('lb', 'provider_dashboard.widget_subtitle', 'Setzt d\'Ufroformulaire op all Websäit derbäi, wou et méiglech ass! D\'Clientë wäerten d\'Ufroen direkt un iech schécken.'),
            ('mt', 'provider_dashboard.widget_subtitle', 'Żid il-formola tat-talba ma\' kwalunkwe sit fejn possibbli! Il-klijenti jibagħtu t-talbiet direttament lilek.'),
            ('tr', 'provider_dashboard.widget_subtitle', 'Talep formunu mümkün olan her siteye ekleyin! Müşteriler taleplerini doğrudan size gönderecektir.'),
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
