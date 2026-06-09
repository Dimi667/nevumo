#!/usr/bin/env python3
"""Seed push prompt translations into the translations table."""

import os
import psycopg2
from psycopg2.extras import execute_values

# Database connection string
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://nevumo:nevumo@localhost:5433/nevumo_leads")

# Translations: list of (lang, key, value) tuples
translations = [
    # push_prompt.title
    ("bg", "push_prompt.title", "🔔 Получавай нотификации веднага!"),
    ("cs", "push_prompt.title", "🔔 Dostávejte oznámení okamžitě!"),
    ("da", "push_prompt.title", "🔔 Få beskeder øjeblikkeligt!"),
    ("de", "push_prompt.title", "🔔 Erhalte Benachrichtigungen sofort!"),
    ("el", "push_prompt.title", "🔔 Λαμβάνετε ειδοποιήσεις αμέσως!"),
    ("en", "push_prompt.title", "🔔 Get notifications instantly!"),
    ("es", "push_prompt.title", "🔔 ¡Recibe notificaciones al instante!"),
    ("et", "push_prompt.title", "🔔 Saa teavitusi kohe!"),
    ("fi", "push_prompt.title", "🔔 Saat ilmoitukset heti!"),
    ("fr", "push_prompt.title", "🔔 Recevez des notifications instantanément!"),
    ("ga", "push_prompt.title", "🔔 Faigh fógraí láithreach!"),
    ("hr", "push_prompt.title", "🔔 Primajte obavijesti odmah!"),
    ("hu", "push_prompt.title", "🔔 Kapj értesítéseket azonnal!"),
    ("is", "push_prompt.title", "🔔 Fáðu tilkynningar strax!"),
    ("it", "push_prompt.title", "🔔 Ricevi notifiche all'istante!"),
    ("lb", "push_prompt.title", "🔔 Kritt Notifikatiounen direkt!"),
    ("lt", "push_prompt.title", "🔔 Gaukite pranešimus iš karto!"),
    ("lv", "push_prompt.title", "🔔 Saņem paziņojumus uzreiz!"),
    ("mk", "push_prompt.title", "🔔 Добивај известувања веднаш!"),
    ("mt", "push_prompt.title", "🔔 Iċċekkja notifiki minnufih!"),
    ("nl", "push_prompt.title", "🔔 Ontvang meldingen direct!"),
    ("no", "push_prompt.title", "🔔 Motta varsler umiddelbart!"),
    ("pl", "push_prompt.title", "🔔 Otrzymuj powiadomienia natychmiast!"),
    ("pt", "push_prompt.title", "🔔 Receba notificações instantaneamente!"),
    ("pt-PT", "push_prompt.title", "🔔 Receba notificações instantaneamente!"),
    ("ro", "push_prompt.title", "🔔 Primește notificări instant!"),
    ("ru", "push_prompt.title", "🔔 Получай уведомления мгновенно!"),
    ("sk", "push_prompt.title", "🔔 Dostávajte oznámenia okamžite!"),
    ("sl", "push_prompt.title", "🔔 Prejemaj obvestila takoj!"),
    ("sq", "push_prompt.title", "🔔 Merr njoftimet menjëherë!"),
    ("sr", "push_prompt.title", "🔔 Добијај обавештења одмах!"),
    ("sv", "push_prompt.title", "🔔 Få aviseringar direkt!"),
    ("tr", "push_prompt.title", "🔔 Bildirimleri anında al!"),
    ("uk", "push_prompt.title", "🔔 Отримуй сповіщення миттєво!"),

    # push_prompt.provider_body
    ("bg", "push_prompt.provider_body", "Не пропускай нови запитвания от клиенти докато телефонът е в джоба ти."),
    ("cs", "push_prompt.provider_body", "Nezmeškejte nové poptávky od klientů, i když máte telefon v kapse."),
    ("da", "push_prompt.provider_body", "Gå ikke glip af nye forespørgsler fra kunder, mens din telefon er i lommen."),
    ("de", "push_prompt.provider_body", "Verpasse keine neuen Kundenanfragen, während dein Telefon in der Tasche ist."),
    ("el", "push_prompt.provider_body", "Μην χάνετε νέα αιτήματα πελατών όσο το τηλέφωνό σας είναι στην τσέπη σας."),
    ("en", "push_prompt.provider_body", "Don't miss new client requests while your phone is in your pocket."),
    ("es", "push_prompt.provider_body", "No te pierdas nuevas solicitudes de clientes mientras tu teléfono está en tu bolsillo."),
    ("et", "push_prompt.provider_body", "Ärge jätke vahele uusi kliendipäringuid, kui telefon on taskus."),
    ("fi", "push_prompt.provider_body", "Älä missaa uusia asiakaspyyntöjä puhelimen ollessa taskussa."),
    ("fr", "push_prompt.provider_body", "Ne manquez pas les nouvelles demandes de clients, même quand votre téléphone est dans votre poche."),
    ("ga", "push_prompt.provider_body", "Ná caill iarratais nua ó chliaint fad is atá do ghuthán i do phóca."),
    ("hr", "push_prompt.provider_body", "Ne propustite nove zahtjeve klijenata dok vam je telefon u džepu."),
    ("hu", "push_prompt.provider_body", "Ne maradj le az új ügyféligénylésekről, amíg a telefonod a zsebedben van."),
    ("is", "push_prompt.provider_body", "Misstu ekki af nýjum beiðnum frá viðskiptavinum meðan síminn er í vasanum þínum."),
    ("it", "push_prompt.provider_body", "Non perdere le nuove richieste dei clienti mentre il telefono è in tasca."),
    ("lb", "push_prompt.provider_body", "Verpasse keng nei Clienten-Ufroe wann däin Telefon an der Täsch ass."),
    ("lt", "push_prompt.provider_body", "Nepraleiskite naujų klientų užklausų, kol telefonas yra kišenėje."),
    ("lv", "push_prompt.provider_body", "Nepalaidiet garām jaunus klientu pieprasījumus, kamēr tālrunis ir kabatā."),
    ("mk", "push_prompt.provider_body", "Не пропуштај нови барања од клиенти додека телефонот ти е во џебот."),
    ("mt", "push_prompt.provider_body", "Taqbżux talbiet ġodda mill-klijenti waqt li t-telefon tiegħek jinsab fil-but."),
    ("nl", "push_prompt.provider_body", "Mis geen nieuwe klantverzoeken terwijl je telefoon in je zak zit."),
    ("no", "push_prompt.provider_body", "Ikke gå glipp av nye kundeforespørsler mens telefonen er i lommen."),
    ("pl", "push_prompt.provider_body", "Nie przegap nowych zapytań od klientów, gdy telefon jest w kieszeni."),
    ("pt", "push_prompt.provider_body", "Não perca novas solicitações de clientes enquanto o telefone está no bolso."),
    ("pt-PT", "push_prompt.provider_body", "Não perca novos pedidos de clientes enquanto o telemóvel está no bolso."),
    ("ro", "push_prompt.provider_body", "Nu rata noile cereri de la clienți în timp ce telefonul e în buzunar."),
    ("ru", "push_prompt.provider_body", "Не пропускай новые запросы клиентов, пока телефон в кармане."),
    ("sk", "push_prompt.provider_body", "Nezmeškajte nové požiadavky od klientov, keď máte telefón v vrecku."),
    ("sl", "push_prompt.provider_body", "Ne zamudite novih zahtev strank, ko je telefon v žepu."),
    ("sq", "push_prompt.provider_body", "Mos humb kërkesat e reja të klientëve ndërkohë që telefoni është në xhep."),
    ("sr", "push_prompt.provider_body", "Не пропуштај нове захтеве клијената док ти је телефон у џепу."),
    ("sv", "push_prompt.provider_body", "Missa inte nya kundförfrågningar medan telefonen är i fickan."),
    ("tr", "push_prompt.provider_body", "Telefon cebinizdeyken yeni müşteri isteklerini kaçırmayın."),
    ("uk", "push_prompt.provider_body", "Не пропускай нові запити від клієнтів, поки телефон у кишені."),

    # push_prompt.client_body
    ("bg", "push_prompt.client_body", "Ще те уведомим веднага когато провайдър отговори на заявката ти."),
    ("cs", "push_prompt.client_body", "Okamžitě vás upozorníme, jakmile vám poskytovatel odpoví."),
    ("da", "push_prompt.client_body", "Vi giver dig besked med det samme, når en udbyder svarer på din anmodning."),
    ("de", "push_prompt.client_body", "Wir benachrichtigen dich sofort, wenn ein Anbieter auf deine Anfrage antwortet."),
    ("el", "push_prompt.client_body", "Θα σας ειδοποιήσουμε αμέσως μόλις ένας πάροχος απαντήσει στο αίτημά σας."),
    ("en", "push_prompt.client_body", "We'll notify you instantly when a provider responds to your request."),
    ("es", "push_prompt.client_body", "Te avisaremos al instante cuando un proveedor responda a tu solicitud."),
    ("et", "push_prompt.client_body", "Teavitame teid kohe, kui teenusepakkuja teie päringule vastab."),
    ("fi", "push_prompt.client_body", "Ilmoitamme sinulle heti, kun palveluntarjoaja vastaa pyyntöösi."),
    ("fr", "push_prompt.client_body", "Nous vous informerons instantanément lorsqu'un prestataire répondra à votre demande."),
    ("ga", "push_prompt.client_body", "Cuirfimid in iúl duit láithreach nuair a fhreagróidh soláthraí do iarraidh."),
    ("hr", "push_prompt.client_body", "Odmah ćemo vas obavijestiti kad vam davatelj usluge odgovori na zahtjev."),
    ("hu", "push_prompt.client_body", "Azonnal értesítünk, amint egy szolgáltató válaszol a kérésedre."),
    ("is", "push_prompt.client_body", "Við látum þig vita um leið þegar þjónustuaðili svarar beiðni þinni."),
    ("it", "push_prompt.client_body", "Ti avviseremo immediatamente quando un fornitore risponderà alla tua richiesta."),
    ("lb", "push_prompt.client_body", "Mir informéiere dech direkt wann en Ubidder op deng Ufro äntwert."),
    ("lt", "push_prompt.client_body", "Pranešime jums iš karto, kai tiekėjas atsakys į jūsų užklausą."),
    ("lv", "push_prompt.client_body", "Mēs nekavējoties paziņosim jums, kad pakalpojumu sniedzējs atbildēs uz jūsu pieprasījumu."),
    ("mk", "push_prompt.client_body", "Ќе те известиме веднаш кога давателот ќе одговори на твоето барање."),
    ("mt", "push_prompt.client_body", "Navżawk minnufih meta fornitur iwieġeb għat-talba tiegħek."),
    ("nl", "push_prompt.client_body", "We stellen je direct op de hoogte wanneer een aanbieder op je verzoek reageert."),
    ("no", "push_prompt.client_body", "Vi varsler deg umiddelbart når en leverandør svarer på din forespørsel."),
    ("pl", "push_prompt.client_body", "Powiadomimy Cię natychmiast, gdy usługodawca odpowie na Twoje zapytanie."),
    ("pt", "push_prompt.client_body", "Vamos notificá-lo instantaneamente quando um prestador responder ao seu pedido."),
    ("pt-PT", "push_prompt.client_body", "Iremos notificá-lo instantaneamente quando um prestador responder ao seu pedido."),
    ("ro", "push_prompt.client_body", "Te vom notifica imediat când un furnizor răspunde la cererea ta."),
    ("ru", "push_prompt.client_body", "Мы мгновенно уведомим тебя, когда провайдер ответит на твою заявку."),
    ("sk", "push_prompt.client_body", "Okamžite vás upozorníme, keď vám poskytovateľ odpovie na požiadavku."),
    ("sl", "push_prompt.client_body", "Takoj vas bomo obvestili, ko se vam bo ponudnik odzval na vašo zahtevo."),
    ("sq", "push_prompt.client_body", "Do t'ju njoftojmë menjëherë kur një ofrues të përgjigjet kërkesës suaj."),
    ("sr", "push_prompt.client_body", "Одмах ћемо те обавестити када провајдер одговори на твој захтев."),
    ("sv", "push_prompt.client_body", "Vi meddelar dig direkt när en leverantör svarar på din förfrågan."),
    ("tr", "push_prompt.client_body", "Bir sağlayıcı talebinize yanıt verdiğinde sizi anında bildireceğiz."),
    ("uk", "push_prompt.client_body", "Ми миттєво повідомимо тебе, коли провайдер відповість на твій запит."),

    # push_prompt.cta_button
    ("bg", "push_prompt.cta_button", "Включи нотификации"),
    ("cs", "push_prompt.cta_button", "Zapnout oznámení"),
    ("da", "push_prompt.cta_button", "Slå beskeder til"),
    ("de", "push_prompt.cta_button", "Benachrichtigungen aktivieren"),
    ("el", "push_prompt.cta_button", "Ενεργοποίηση ειδοποιήσεων"),
    ("en", "push_prompt.cta_button", "Enable notifications"),
    ("es", "push_prompt.cta_button", "Activar notificaciones"),
    ("et", "push_prompt.cta_button", "Luba teavitused"),
    ("fi", "push_prompt.cta_button", "Ota ilmoitukset käyttöön"),
    ("fr", "push_prompt.cta_button", "Activer les notifications"),
    ("ga", "push_prompt.cta_button", "Cumasaigh fógraí"),
    ("hr", "push_prompt.cta_button", "Uključi obavijesti"),
    ("hu", "push_prompt.cta_button", "Értesítések bekapcsolása"),
    ("is", "push_prompt.cta_button", "Virkja tilkynningar"),
    ("it", "push_prompt.cta_button", "Attiva notifiche"),
    ("lb", "push_prompt.cta_button", "Notifikatiounen aktivéieren"),
    ("lt", "push_prompt.cta_button", "Įjungti pranešimus"),
    ("lv", "push_prompt.cta_button", "Iespējot paziņojumus"),
    ("mk", "push_prompt.cta_button", "Вклучи известувања"),
    ("mt", "push_prompt.cta_button", "Attiva n-notifiki"),
    ("nl", "push_prompt.cta_button", "Meldingen inschakelen"),
    ("no", "push_prompt.cta_button", "Slå på varsler"),
    ("pl", "push_prompt.cta_button", "Włącz powiadomienia"),
    ("pt", "push_prompt.cta_button", "Ativar notificações"),
    ("pt-PT", "push_prompt.cta_button", "Ativar notificações"),
    ("ro", "push_prompt.cta_button", "Activează notificările"),
    ("ru", "push_prompt.cta_button", "Включить уведомления"),
    ("sk", "push_prompt.cta_button", "Zapnúť oznámenia"),
    ("sl", "push_prompt.cta_button", "Vklopi obvestila"),
    ("sq", "push_prompt.cta_button", "Aktivizo njoftimet"),
    ("sr", "push_prompt.cta_button", "Укључи обавештења"),
    ("sv", "push_prompt.cta_button", "Aktivera aviseringar"),
    ("tr", "push_prompt.cta_button", "Bildirimleri etkinleştir"),
    ("uk", "push_prompt.cta_button", "Увімкнути сповіщення"),

    # push_prompt.dismiss_button
    ("bg", "push_prompt.dismiss_button", "Сега не"),
    ("cs", "push_prompt.dismiss_button", "Teď ne"),
    ("da", "push_prompt.dismiss_button", "Ikke nu"),
    ("de", "push_prompt.dismiss_button", "Nicht jetzt"),
    ("el", "push_prompt.dismiss_button", "Όχι τώρα"),
    ("en", "push_prompt.dismiss_button", "Not now"),
    ("es", "push_prompt.dismiss_button", "Ahora no"),
    ("et", "push_prompt.dismiss_button", "Mitte praegu"),
    ("fi", "push_prompt.dismiss_button", "Ei nyt"),
    ("fr", "push_prompt.dismiss_button", "Pas maintenant"),
    ("ga", "push_prompt.dismiss_button", "Níl anois"),
    ("hr", "push_prompt.dismiss_button", "Ne sada"),
    ("hu", "push_prompt.dismiss_button", "Most nem"),
    ("is", "push_prompt.dismiss_button", "Ekki núna"),
    ("it", "push_prompt.dismiss_button", "Non ora"),
    ("lb", "push_prompt.dismiss_button", "Net elo"),
    ("lt", "push_prompt.dismiss_button", "Ne dabar"),
    ("lv", "push_prompt.dismiss_button", "Ne tagad"),
    ("mk", "push_prompt.dismiss_button", "Не сега"),
    ("mt", "push_prompt.dismiss_button", "Mhux issa"),
    ("nl", "push_prompt.dismiss_button", "Niet nu"),
    ("no", "push_prompt.dismiss_button", "Ikke nå"),
    ("pl", "push_prompt.dismiss_button", "Nie teraz"),
    ("pt", "push_prompt.dismiss_button", "Agora não"),
    ("pt-PT", "push_prompt.dismiss_button", "Agora não"),
    ("ro", "push_prompt.dismiss_button", "Nu acum"),
    ("ru", "push_prompt.dismiss_button", "Не сейчас"),
    ("sk", "push_prompt.dismiss_button", "Teraz nie"),
    ("sl", "push_prompt.dismiss_button", "Ne zdaj"),
    ("sq", "push_prompt.dismiss_button", "Jo tani"),
    ("sr", "push_prompt.dismiss_button", "Не сада"),
    ("sv", "push_prompt.dismiss_button", "Inte nu"),
    ("tr", "push_prompt.dismiss_button", "Şimdi değil"),
    ("uk", "push_prompt.dismiss_button", "Не зараз"),
]

def main():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    query = """
        INSERT INTO translations (lang, key, value)
        VALUES %s
        ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
    """

    execute_values(cur, query, translations)
    conn.commit()

    print(f"✅ Seeded {len(translations)} translation rows")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
