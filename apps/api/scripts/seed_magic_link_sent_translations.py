import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")

TRANSLATIONS = [
    # bg
    ("bg", "magic_link_sent_title", "Провери имейла си"),
    ("bg", "magic_link_sent_subtitle", "Изпратихме ти линк за вход"),
    ("bg", "magic_link_use_different_email", "Използвай друг имейл"),
    # cs
    ("cs", "magic_link_sent_title", "Zkontrolujte svůj e-mail"),
    ("cs", "magic_link_sent_subtitle", "Poslali jsme vám přihlašovací odkaz"),
    ("cs", "magic_link_use_different_email", "Použijte jiný e-mail"),
    # da
    ("da", "magic_link_sent_title", "Tjek din e-mail"),
    ("da", "magic_link_sent_subtitle", "Vi har sendt dig et login-link"),
    ("da", "magic_link_use_different_email", "Brug en anden e-mail"),
    # de
    ("de", "magic_link_sent_title", "Überprüf deine E-Mail"),
    ("de", "magic_link_sent_subtitle", "Wir haben dir einen Anmeldelink geschickt"),
    ("de", "magic_link_use_different_email", "Andere E-Mail verwenden"),
    # el
    ("el", "magic_link_sent_title", "Έλεγξε το email σου"),
    ("el", "magic_link_sent_subtitle", "Σου στείλαμε έναν σύνδεσμο σύνδεσης"),
    ("el", "magic_link_use_different_email", "Χρησιμοποίησε άλλο email"),
    # en
    ("en", "magic_link_sent_title", "Check your email"),
    ("en", "magic_link_sent_subtitle", "We've sent you a login link"),
    ("en", "magic_link_use_different_email", "Use a different email"),
    # es
    ("es", "magic_link_sent_title", "Revisa tu correo"),
    ("es", "magic_link_sent_subtitle", "Te hemos enviado un enlace de acceso"),
    ("es", "magic_link_use_different_email", "Usar un correo diferente"),
    # et
    ("et", "magic_link_sent_title", "Kontrolli oma e-posti"),
    ("et", "magic_link_sent_subtitle", "Saatsime sulle sisselogimislingi"),
    ("et", "magic_link_use_different_email", "Kasuta teist e-posti"),
    # fi
    ("fi", "magic_link_sent_title", "Tarkista sähköpostisi"),
    ("fi", "magic_link_sent_subtitle", "Lähetimme sinulle kirjautumislinkin"),
    ("fi", "magic_link_use_different_email", "Käytä eri sähköpostia"),
    # fr
    ("fr", "magic_link_sent_title", "Vérifiez votre e-mail"),
    ("fr", "magic_link_sent_subtitle", "Nous vous avons envoyé un lien de connexion"),
    ("fr", "magic_link_use_different_email", "Utiliser un autre e-mail"),
    # ga
    ("ga", "magic_link_sent_title", "Seiceáil do ríomhphost"),
    ("ga", "magic_link_sent_subtitle", "Sheol muid nasc logáil isteach chugat"),
    ("ga", "magic_link_use_different_email", "Úsáid ríomhphost difriúil"),
    # hr
    ("hr", "magic_link_sent_title", "Provjeri svoju e-poštu"),
    ("hr", "magic_link_sent_subtitle", "Poslali smo ti link za prijavu"),
    ("hr", "magic_link_use_different_email", "Koristi drugu e-poštu"),
    # hu
    ("hu", "magic_link_sent_title", "Ellenőrizd az e-mailedet"),
    ("hu", "magic_link_sent_subtitle", "Küldtünk neked egy bejelentkezési linket"),
    ("hu", "magic_link_use_different_email", "Más e-mail használata"),
    # is
    ("is", "magic_link_sent_title", "Athugaðu tölvupóstinn þinn"),
    ("is", "magic_link_sent_subtitle", "Við sendum þér innskráningartengil"),
    ("is", "magic_link_use_different_email", "Notaðu annan tölvupóst"),
    # it
    ("it", "magic_link_sent_title", "Controlla la tua email"),
    ("it", "magic_link_sent_subtitle", "Ti abbiamo inviato un link di accesso"),
    ("it", "magic_link_use_different_email", "Usa un'altra email"),
    # lb
    ("lb", "magic_link_sent_title", "Kuckt äre E-Mail no"),
    ("lb", "magic_link_sent_subtitle", "Mir hunn Iech e Login-Link geschéckt"),
    ("lb", "magic_link_use_different_email", "En anert E-Mail benotzen"),
    # lt
    ("lt", "magic_link_sent_title", "Patikrinkite savo el. paštą"),
    ("lt", "magic_link_sent_subtitle", "Išsiuntėme jums prisijungimo nuorodą"),
    ("lt", "magic_link_use_different_email", "Naudoti kitą el. paštą"),
    # lv
    ("lv", "magic_link_sent_title", "Pārbaudi savu e-pastu"),
    ("lv", "magic_link_sent_subtitle", "Mēs nosūtījām tev pieteikšanās saiti"),
    ("lv", "magic_link_use_different_email", "Izmantot citu e-pastu"),
    # mk
    ("mk", "magic_link_sent_title", "Провери го твојот е-пошта"),
    ("mk", "magic_link_sent_subtitle", "Ти испративме линк за најава"),
    ("mk", "magic_link_use_different_email", "Користи друга е-пошта"),
    # mt
    ("mt", "magic_link_sent_title", "Iċċekkja l-email tiegħek"),
    ("mt", "magic_link_sent_subtitle", "Bgħatnilek link biex tidħol"),
    ("mt", "magic_link_use_different_email", "Uża email differenti"),
    # nl
    ("nl", "magic_link_sent_title", "Controleer je e-mail"),
    ("nl", "magic_link_sent_subtitle", "We hebben je een inloglink gestuurd"),
    ("nl", "magic_link_use_different_email", "Gebruik een ander e-mailadres"),
    # no
    ("no", "magic_link_sent_title", "Sjekk e-posten din"),
    ("no", "magic_link_sent_subtitle", "Vi har sendt deg en innloggingslenke"),
    ("no", "magic_link_use_different_email", "Bruk en annen e-post"),
    # pl
    ("pl", "magic_link_sent_title", "Sprawdź swój e-mail"),
    ("pl", "magic_link_sent_subtitle", "Wysłaliśmy Ci link do logowania"),
    ("pl", "magic_link_use_different_email", "Użyj innego adresu e-mail"),
    # pt
    ("pt", "magic_link_sent_title", "Verifique seu e-mail"),
    ("pt", "magic_link_sent_subtitle", "Enviamos um link de acesso para você"),
    ("pt", "magic_link_use_different_email", "Usar outro e-mail"),
    # pt-PT
    ("pt-PT", "magic_link_sent_title", "Verifique o seu e-mail"),
    ("pt-PT", "magic_link_sent_subtitle", "Enviámos-lhe um link de acesso"),
    ("pt-PT", "magic_link_use_different_email", "Utilizar outro e-mail"),
    # ro
    ("ro", "magic_link_sent_title", "Verificați e-mailul dvs."),
    ("ro", "magic_link_sent_subtitle", "V-am trimis un link de autentificare"),
    ("ro", "magic_link_use_different_email", "Folosiți un alt e-mail"),
    # ru
    ("ru", "magic_link_sent_title", "Проверьте почту"),
    ("ru", "magic_link_sent_subtitle", "Мы отправили вам ссылку для входа"),
    ("ru", "magic_link_use_different_email", "Использовать другой email"),
    # sk
    ("sk", "magic_link_sent_title", "Skontrolujte svoj e-mail"),
    ("sk", "magic_link_sent_subtitle", "Poslali sme vám prihlasovací odkaz"),
    ("sk", "magic_link_use_different_email", "Použiť iný e-mail"),
    # sl
    ("sl", "magic_link_sent_title", "Preverite svojo e-pošto"),
    ("sl", "magic_link_sent_subtitle", "Poslali smo vam prijavno povezavo"),
    ("sl", "magic_link_use_different_email", "Uporabi drug e-naslov"),
    # sq
    ("sq", "magic_link_sent_title", "Kontrollo emailin tënd"),
    ("sq", "magic_link_sent_subtitle", "Të dërguam një lidhje identifikimi"),
    ("sq", "magic_link_use_different_email", "Përdor një email tjetër"),
    # sr
    ("sr", "magic_link_sent_title", "Провери своју е-пошту"),
    ("sr", "magic_link_sent_subtitle", "Послали смо ти линк за пријаву"),
    ("sr", "magic_link_use_different_email", "Користи другу е-пошту"),
    # sv
    ("sv", "magic_link_sent_title", "Kontrollera din e-post"),
    ("sv", "magic_link_sent_subtitle", "Vi har skickat dig en inloggningslänk"),
    ("sv", "magic_link_use_different_email", "Använd en annan e-post"),
    # tr
    ("tr", "magic_link_sent_title", "E-postanı kontrol et"),
    ("tr", "magic_link_sent_subtitle", "Sana bir giriş bağlantısı gönderdik"),
    ("tr", "magic_link_use_different_email", "Farklı bir e-posta kullan"),
    # uk
    ("uk", "magic_link_sent_title", "Перевірте свою пошту"),
    ("uk", "magic_link_sent_subtitle", "Ми надіслали вам посилання для входу"),
    ("uk", "magic_link_use_different_email", "Використати іншу електронну пошту"),
]

def main():
    if not DATABASE_URL:
        print("ERROR: DATABASE_URL environment variable not set")
        return

    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Prepare data with namespace
    data = [(lang, "auth", key, value) for lang, key, value in TRANSLATIONS]

    query = """
        INSERT INTO translations (lang, key, value)
        VALUES (%s, %s, %s)
        ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
    """

    cursor.executemany(query, [(r[0], 'auth.' + r[1], r[2]) for r in TRANSLATIONS])
    conn.commit()

    print(f"Inserted/updated {cursor.rowcount} translations in 'auth' namespace")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
