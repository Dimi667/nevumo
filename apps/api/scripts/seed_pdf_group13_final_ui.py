from sqlalchemy import text
from apps.api.database import SessionLocal

def main():
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()

def run_seed(db):
    insert_translations(db, ALL_TRANSLATIONS)
    verify(db)

def insert_translations(db, data: dict[str, dict[str, str]]) -> None:
    count = 0
    for lang, keys in data.items():
        for key, value in keys.items():
            db.execute(
                text("""
                    INSERT INTO translations (lang, key, value)
                    VALUES (:lang, :key, :value)
                    ON CONFLICT (lang, key)
                    DO UPDATE SET value = EXCLUDED.value
                """),
                {"lang": lang, "key": key, "value": value}
            )
            count += 1
    db.commit()
    print(f"Inserted/updated {count} translation rows")

def verify(db) -> None:
    result = db.execute(text("""
        SELECT lang, COUNT(*) as keys
        FROM translations
        WHERE key LIKE 'pdf.%'
        GROUP BY lang
        ORDER BY lang
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} keys")

ALL_TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "pdf.submit_button_label": "Submit withdrawal form",
        "pdf.success_message": "Your withdrawal form has been submitted successfully",
        "pdf.error_message": "An error occurred while submitting your withdrawal form",
    },
    "bg": {
        "pdf.submit_button_label": "Изпрати формуляр за отказ",
        "pdf.success_message": "Вашият формуляр за отказ е изпратен успешно",
        "pdf.error_message": "Възникна грешка при изпращане на формуляра за отказ",
    },
    "pl": {
        "pdf.submit_button_label": "Wyślij formularz odstąpienia",
        "pdf.success_message": "Twój formularz odstąpienia został pomyślnie wysłany",
        "pdf.error_message": "Wystąpił błąd podczas wysyłania formularza odstąpienia",
    },
    "cs": {
        "pdf.submit_button_label": "Odeslat formulář pro odstoupení",
        "pdf.success_message": "Váš formulář pro odstoupení byl úspěšně odeslán",
        "pdf.error_message": "Při odesílání formuláře pro odstoupení došlo k chybě",
    },
    "da": {
        "pdf.submit_button_label": "Indsend fortrydelsesformular",
        "pdf.success_message": "Din fortrydelsesformular er blevet indsendt korrekt",
        "pdf.error_message": "Der opstod en fejl under indsendelse af din fortrydelsesformular",
    },
    "de": {
        "pdf.submit_button_label": "Widerrufsformular absenden",
        "pdf.success_message": "Ihr Widerrufsformular wurde erfolgreich übermittelt",
        "pdf.error_message": "Beim Übermitteln Ihres Widerrufsformulars ist ein Fehler aufgetreten",
    },
    "el": {
        "pdf.submit_button_label": "Υποβολή εντύπου υπαναχώρησης",
        "pdf.success_message": "Το έντυπο υπαναχώρησης υποβλήθηκε με επιτυχία",
        "pdf.error_message": "Παρουσιάστηκε σφάλμα κατά την υποβολή του εντύπου υπαναχώρησης",
    },
    "es": {
        "pdf.submit_button_label": "Enviar formulario de desistimiento",
        "pdf.success_message": "Su formulario de desistimiento ha sido enviado con éxito",
        "pdf.error_message": "Se ha producido un error al enviar su formulario de desistimiento",
    },
    "et": {
        "pdf.submit_button_label": "Esita taganemisavaldus",
        "pdf.success_message": "Teie taganemisavaldus on edukalt esitatud",
        "pdf.error_message": "Taganemisavalduse esitamisel tekkis viga",
    },
    "fi": {
        "pdf.submit_button_label": "Lähetä peruuttamislomake",
        "pdf.success_message": "Peruuttamislomakkeesi on lähetetty onnistuneesti",
        "pdf.error_message": "Peruuttamislomakkeen lähettämisessä tapahtui virhe",
    },
    "fr": {
        "pdf.submit_button_label": "Envoyer le formulaire de rétractation",
        "pdf.success_message": "Votre formulaire de rétractation a été envoyé avec succès",
        "pdf.error_message": "Une erreur est survenue lors de l'envoi de votre formulaire de rétractation",
    },
    "ga": {
        "pdf.submit_button_label": "Cuir foirm tarraingt siar isteach",
        "pdf.success_message": "D'éirigh le d'fhoirm tarraingt siar a chur isteach",
        "pdf.error_message": "Tharla earráid agus d'fhoirm tarraingt siar á cur isteach",
    },
    "hr": {
        "pdf.submit_button_label": "Pošalji obrazac za odustajanje",
        "pdf.success_message": "Vaš obrazac za odustajanje uspješno je poslan",
        "pdf.error_message": "Došlo je do pogreške prilikom slanja obrasca za odustajanje",
    },
    "hu": {
        "pdf.submit_button_label": "Elállási nyilatkozat beküldése",
        "pdf.success_message": "Az elállási nyilatkozat beküldése sikeres volt",
        "pdf.error_message": "Hiba történt az elállási nyilatkozat beküldése során",
    },
    "is": {
        "pdf.submit_button_label": "Senda afturköllunareyðublað",
        "pdf.success_message": "Afturköllunareyðublaðið þitt hefur verið sent",
        "pdf.error_message": "Villa kom upp við að senda afturköllunareyðublaðið þitt",
    },
    "it": {
        "pdf.submit_button_label": "Invia modulo di recesso",
        "pdf.success_message": "Il tuo modulo di recesso è stato inviato con successo",
        "pdf.error_message": "Si è verificato un errore durante l'invio del modulo di recesso",
    },
    "lb": {
        "pdf.submit_button_label": "Widerrufsformular ofschécken",
        "pdf.success_message": "Äert Widerrufsformular gouf erfollegräich iwwermëttelt",
        "pdf.error_message": "Beim Iwwermëttelen vun Ärem Widerrufsformular ass e Feeler opgetrueden",
    },
    "lt": {
        "pdf.submit_button_label": "Pateikti atsisakymo formą",
        "pdf.success_message": "Jūsų atsisakymo forma sėkmingai pateikta",
        "pdf.error_message": "Pateikiant atsisakymo formą įvyko klaida",
    },
    "lv": {
        "pdf.submit_button_label": "Iesniegt atteikuma veidlapu",
        "pdf.success_message": "Jūsu atteikuma veidlapa ir veiksmīgi iesniegta",
        "pdf.error_message": "Iesniedzot atteikuma veidlapu, radās kļūda",
    },
    "mk": {
        "pdf.submit_button_label": "Испрати формулар за повлекување",
        "pdf.success_message": "Вашиот формулар за повлекување е успешно испратен",
        "pdf.error_message": "Се случи грешка при испраќањето на вашиот формулар за повлекување",
    },
    "mt": {
        "pdf.submit_button_label": "Ibgħat il-formola tal-irtirar",
        "pdf.success_message": "Il-formola tal-irtirar tiegħek intbagħtet b'suċċess",
        "pdf.error_message": "Inqalgħet problema waqt li kont qed tibgħat il-formola tal-irtirar tiegħek",
    },
    "nl": {
        "pdf.submit_button_label": "Herroepingsformulier verzenden",
        "pdf.success_message": "Uw herroepingsformulier is succesvol verzonden",
        "pdf.error_message": "Er is een fout opgetreden bij het verzenden van uw herroepingsformulier",
    },
    "no": {
        "pdf.submit_button_label": "Send inn angrerettsskjema",
        "pdf.success_message": "Ditt angrerettsskjema er sendt inn",
        "pdf.error_message": "Det oppsto en feil under innsending av angrerettsskjemaet",
    },
    "pt": {
        "pdf.submit_button_label": "Enviar formulário de desistência",
        "pdf.success_message": "O seu formulário de desistência foi enviado com sucesso",
        "pdf.error_message": "Ocorreu um erro ao enviar o seu formulário de desistência",
    },
    "pt-PT": {
        "pdf.submit_button_label": "Enviar formulário de desistência",
        "pdf.success_message": "O seu formulário de desistência foi enviado com sucesso",
        "pdf.error_message": "Ocorreu um erro ao enviar o seu formulário de desistência",
    },
    "ro": {
        "pdf.submit_button_label": "Trimite formularul de retragere",
        "pdf.success_message": "Formularul dvs. de retragere a fost trimis cu succes",
        "pdf.error_message": "A apărut o eroare la trimiterea formularului de retragere",
    },
    "ru": {
        "pdf.submit_button_label": "Отправить форму отзыва",
        "pdf.success_message": "Ваша форма отзыва была успешно отправлена",
        "pdf.error_message": "Произошла ошибка при отправке вашей формы отзыва",
    },
    "sk": {
        "pdf.submit_button_label": "Odoslať formulár na odstúpenie",
        "pdf.success_message": "Váš formulár na odstúpenie bol úspešne odoslaný",
        "pdf.error_message": "Pri odosielaní formulára na odstúpenie sa vyskytla chyba",
    },
    "sl": {
        "pdf.submit_button_label": "Oddajte obrazec za odstop",
        "pdf.success_message": "Vaš obrazec za odstop je bil uspešno oddan",
        "pdf.error_message": "Pri oddaji obrazca za odstop je prišlo do napake",
    },
    "sq": {
        "pdf.submit_button_label": "Dërgo formularin e tërheqjes",
        "pdf.success_message": "Formulari juaj i tërheqjes u dërgua me sukses",
        "pdf.error_message": "Ndodhi një gabim gjatë dërgimit të formularit tuaj të tërheqjes",
    },
    "sr": {
        "pdf.submit_button_label": "Pošalji obrazac za odustanak",
        "pdf.success_message": "Vaš obrazac za odustanak je uspešno poslat",
        "pdf.error_message": "Došlo je do greške prilikom slanja vašeg obrasca za odustanak",
    },
    "sv": {
        "pdf.submit_button_label": "Skicka in ångerblankett",
        "pdf.success_message": "Din ångerblankett har skickats in",
        "pdf.error_message": "Ett fel uppstod när din ångerblankett skulle skickas in",
    },
    "tr": {
        "pdf.submit_button_label": "Cayma formunu gönder",
        "pdf.success_message": "Cayma formunuz başarıyla gönderildi",
        "pdf.error_message": "Cayma formunuz gönderilirken bir hata oluştu",
    },
    "uk": {
        "pdf.submit_button_label": "Надіслати форму відкликання",
        "pdf.success_message": "Вашу форму відкликання було успішно надіслано",
        "pdf.error_message": "Під час надсилання форми відкликання виникла помилка",
    },
}

if __name__ == "__main__":
    main()
