#!/usr/bin/env python3
"""
Script to upsert translation keys for category form part 1
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
        'category.no_providers_title': {
            'bg': "Бъди първият, поискал тази услуга в района си",
            'cs': "Buďte první, kdo si vyžádá tuto službu ve svém okolí",
            'da': "Vær den første til at anmode om denne tjeneste i dit område",
            'de': "Sei der Erste, der diesen Service in deiner Region anfragt",
            'el': "Γίνε ο πρώτος που θα ζητήσει αυτή την υπηρεσία στην περιοχή σου",
            'en': "Be the first to request this service in your area",
            'es': "Sé el primero en solicitar este servicio en tu área",
            'et': "Ole esimene, kes seda teenust oma piirkonnas taotleb",
            'fi': "Ole ensimmäinen, joka pyytää tätä palvelua alueellasi",
            'fr': "Soyez le premier à demander ce service dans votre région",
            'ga': "Bí ar an gcéad duine a iarrann an tseirbhís seo i do cheantar",
            'hr': "Budite prvi koji traži ovu uslugu u vašem području",
            'hu': "Legyen Ön az első, aki ezt a szolgáltatást igényli a térségben",
            'is': "Vertu fyrstur til að óska eftir þessari þjónustu á þínu svæði",
            'it': "Sii il primo a richiedere questo servizio nella tua zona",
            'lb': "Sidd déi éischt, déi dëse Service an Ärer Regioun ufroen",
            'lt': "Būkite pirmasis, prašantis šios paslaugos savo vietovėje",
            'lv': "Esi pirmais, kas pieprasa šo pakalpojumu savā apgabalā",
            'mk': "Биди прв кој ќе побара оваа услуга во својот реон",
            'mt': "Kun l-ewwel li titlob din is-servizz f'żontek",
            'nl': "Wees de eerste die deze dienst in jouw regio aanvraagt",
            'no': "Vær den første til å be om denne tjenesten i ditt område",
            'pl': "Jako pierwszy zamów tę usługę w swojej okolicy",
            'pt': "Seja o primeiro a solicitar este serviço na sua área",
            'pt-PT': "Seja o primeiro a solicitar este serviço na sua área",
            'ro': "Fii primul care solicită acest serviciu în zona ta",
            'ru': "Будьте первым, кто закажет эту услугу в вашем районе",
            'sk': "Buďte prvý, kto si vyžiada túto službu vo svojom okolí",
            'sl': "Bodite prvi, ki zahtevate to storitev v vašem območju",
            'sq': "Bëhu i pari që kërkon këtë shërbim në zonën tënde",
            'sr': "Будите први који тражи ову услугу у вашем подручју",
            'sv': "Var den första att efterfråga denna tjänst i ditt område",
            'tr': "Bölgenizdeki bu hizmeti talep eden ilk kişi olun",
            'uk': "Будьте першим, хто замовить цю послугу у вашому районі"
        },
        'category.no_providers_subtitle': {
            'bg': "Доставчиците, присъединяващи се към Nevumo, ще видят заявката ти и ще се свържат с теб",
            'cs': "Poskytovatelé, kteří se připojí k Nevumo, uvidí vaši žádost a kontaktují vás",
            'da': "Udbydere, der tilmelder sig Nevumo, vil se din anmodning og kontakte dig",
            'de': "Anbieter, die Nevumo beitreten, sehen deine Anfrage und melden sich bei dir",
            'el': "Οι πάροχοι που εντάσσονται στο Nevumo θα δουν το αίτημά σου και θα επικοινωνήσουν μαζί σου",
            'en': "Providers joining Nevumo will see your request and contact you",
            'es': "Los proveedores que se unan a Nevumo verán tu solicitud y te contactarán",
            'et': "Nevumoga liituvad teenusepakkujad näevad teie taotlust ja võtavad teiega ühendust",
            'fi': "Nevumoon liittyvät palveluntarjoajat näkevät pyyntösi ja ottavat sinuun yhteyttä",
            'fr': "Les prestataires rejoignant Nevumo verront votre demande et vous contacteront",
            'ga': "Feicfidh soláthróirí a bheidh ag dul isteach ar Nevumo d'iarratas agus déanfaidh siad teagmháil leat",
            'hr': "Pružatelji koji se pridružuju Nevumu vidjet će vaš zahtjev i kontaktirati vas",
            'hu': "A Nevumóhoz csatlakozó szolgáltatók látják kérését és felveszik Önnel a kapcsolatot",
            'is': "Þjónustuaðilar sem ganga til liðs við Nevumo munu sjá beiðni þína og hafa samband við þig",
            'it': "I fornitori che si uniscono a Nevumo vedranno la tua richiesta e ti contatteranno",
            'lb': "Ubidder, déi sech bei Nevumo aschreiben, wäerte Är Ufro gesinn an Iech kontaktéieren",
            'lt': "Nevumo prisijungiantys tiekėjai matys jūsų užklausą ir susisieks su jumis",
            'lv': "Pakalpojumu sniedzēji, kas pievienojas Nevumo, redzēs jūsu pieprasījumu un sazināsies ar jums",
            'mk': "Давателите на услуги кои се приклучуваат кон Nevumo ќе го видат вашето барање и ќе ве контактираат",
            'mt': "Il-fornituri li jingħaqdu ma' Nevumo se jaraw it-talba tiegħek u jikkuntattjawk",
            'nl': "Aanbieders die zich bij Nevumo aansluiten, zien uw aanvraag en nemen contact met u op",
            'no': "Leverandører som blir med i Nevumo vil se din forespørsel og kontakte deg",
            'pl': "Specjaliści dołączający do Nevumo zobaczą Twoje zlecenie i skontaktują się z Tobą",
            'pt': "Prestadores que ingressarem no Nevumo verão seu pedido e entrarão em contato",
            'pt-PT': "Prestadores que aderirem ao Nevumo verão o seu pedido e entrarão em contacto",
            'ro': "Furnizorii care se alătură Nevumo vor vedea solicitarea ta și te vor contacta",
            'ru': "Специалисты, присоединяющиеся к Nevumo, увидят вашу заявку и свяжутся с вами",
            'sk': "Poskytovatelia, ktorí sa pripoja k Nevumo, uvidia vašu žiadosť a skontaktujú vás",
            'sl': "Ponudniki, ki se pridružijo Nevumu, bodo videli vašo zahtevo in vas kontaktirali",
            'sq': "Ofruesit që bashkohen me Nevumo do ta shohin kërkesën tënde dhe do të kontaktojnë",
            'sr': "Пружаоци услуга који се придружују Nevumu видеће ваш захтев и контактираће вас",
            'sv': "Leverantörer som går med i Nevumo kommer att se din förfrågan och kontakta dig",
            'tr': "Nevumo'ya katılan sağlayıcılar talebinizi görecek ve sizi arayacak",
            'uk': "Спеціалісти, що приєднуються до Nevumo, побачать ваш запит і зв'яжуться з вами"
        },
        'category.form_subtext': {
            'bg': "Изпрати една заявка и получи оферти от наличните специалисти",
            'cs': "Pošlete jednu žádost a získejte nabídky od dostupných poskytovatelů",
            'da': "Send én anmodning og modtag tilbud fra tilgængelige udbydere",
            'de': "Sende eine Anfrage und erhalte Angebote von verfügbaren Anbietern",
            'el': "Στείλε ένα αίτημα και λάβε προσφορές από διαθέσιμους παρόχους",
            'en': "Send one request and receive offers from available providers",
            'es': "Envía una solicitud y recibe ofertas de los proveedores disponibles",
            'et': "Saatke üks taotlus ja saage pakkumisi saadaolevatelt teenusepakkujatelt",
            'fi': "Lähetä yksi pyyntö ja vastaanota tarjouksia saatavilla olevilta palveluntarjoajilta",
            'fr': "Envoyez une demande et recevez des offres des prestataires disponibles",
            'ga': "Seol iarratas amháin agus faigh tairiscintí ó sholáthrairí atá ar fáil",
            'hr': "Pošaljite jedan zahtjev i primite ponude od dostupnih pružatelja",
            'hu': "Küldjön egy kérést, és kapjon ajánlatokat az elérhető szolgáltatóktól",
            'is': "Sendu eina beiðni og fáðu tilboð frá tiltækum þjónustuaðilum",
            'it': "Invia una richiesta e ricevi offerte dai fornitori disponibili",
            'lb': "Schéckt eng Ufro a kritt Ubidder vun disponibelen Ubidder",
            'lt': "Išsiųskite vieną užklausą ir gaukite pasiūlymus iš galimų tiekėjų",
            'lv': "Nosūtiet vienu pieprasījumu un saņemiet piedāvājumus no pieejamiem pakalpojumu sniedzējiem",
            'mk': "Испратете едно барање и добијте понуди од достапните даватели",
            'mt': "Ibgħat talba waħda u irċievi offerti minn fornituri disponibbli",
            'nl': "Stuur één aanvraag en ontvang offertes van beschikbare aanbieders",
            'no': "Send én forespørsel og motta tilbud fra tilgjengelige leverandører",
            'pl': "Wyślij jedno zlecenie i otrzymaj oferty od dostępnych specjalistów",
            'pt': "Envie um pedido e receba propostas de prestadores disponíveis",
            'pt-PT': "Envie um pedido e receba propostas de prestadores disponíveis",
            'ro': "Trimite o cerere și primește oferte de la furnizorii disponibili",
            'ru': "Отправьте один запрос и получите предложения от доступных специалистов",
            'sk': "Pošlite jednu žiadosť a získajte ponuky od dostupných poskytovateľov",
            'sl': "Pošljite eno zahtevo in prejemajte ponudbe od razpoložljivih ponudnikov",
            'sq': "Dërgoni një kërkesë dhe merrni oferta nga ofruesit e disponueshëm",
            'sr': "Пошаљите један захтев и примите понуде од доступних пружалаца",
            'sv': "Skicka en förfrågan och ta emot erbjudanden från tillgängliga leverantörer",
            'tr': "Bir istek gönderin ve mevcut sağlayıcılardan teklifler alın",
            'uk': "Надішліть один запит і отримайте пропозиції від доступних спеціалістів"
        },
        'category.how_it_works_label': {
            'bg': "Как работи",
            'cs': "Jak to funguje",
            'da': "Sådan fungerer det",
            'de': "So funktioniert es",
            'el': "Πώς λειτουργεί",
            'en': "How it works",
            'es': "Cómo funciona",
            'et': "Kuidas see toimib",
            'fi': "Näin se toimii",
            'fr': "Comment ça marche",
            'ga': "Conas a oibríonn sé",
            'hr': "Kako funkcionira",
            'hu': "Hogyan működik",
            'is': "Hvernig það virkar",
            'it': "Come funziona",
            'lb': "Wéi et funktionéiert",
            'lt': "Kaip tai veikia",
            'lv': "Kā tas darbojas",
            'mk': "Како функционира",
            'mt': "Kif taħdem",
            'nl': "Hoe het werkt",
            'no': "Slik fungerer det",
            'pl': "Jak to działa",
            'pt': "Como funciona",
            'pt-PT': "Como funciona",
            'ro': "Cum funcționează",
            'ru': "Как это работает",
            'sk': "Ako to funguje",
            'sl': "Kako deluje",
            'sq': "Si funksionon",
            'sr': "Како функционише",
            'sv': "Hur det fungerar",
            'tr': "Nasıl çalışır",
            'uk': "Як це працює"
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
