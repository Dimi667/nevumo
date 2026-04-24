#!/usr/bin/env python3
"""
Seed lead status translations for client and provider dashboards.
Namespaces: client_dashboard, provider_dashboard
Run: docker exec nevumo-api python -m apps.api.scripts.seed_status_translations
"""

import os
from sqlalchemy import create_engine, text

# ---- DATA DEFINITIONS ----

CLIENT_DASHBOARD_KEYS = [
    "status_label_created", "status_label_contacted", "status_label_done",
    "status_label_cancelled_by_client", "status_label_cancelled_by_provider",
    "status_btn_contacted", "status_btn_done", "status_btn_cancel",
    "status_confirm_done", "status_confirm_cancel", "status_confirm_yes", "status_confirm_no"
]

PROVIDER_DASHBOARD_KEYS = [
    "status_label_new", "status_label_contacted", "status_label_done",
    "status_label_cancelled_by_provider", "status_label_cancelled_by_client",
    "status_btn_contacted", "status_btn_cancel"
]

# Raw data from user request
RAW_CLIENT_DATA = {
    "bg": "status_label_created=Изпратена, status_label_contacted=Осъществен контакт, status_label_done=Завършена, status_label_cancelled_by_client=Отказана, status_label_cancelled_by_provider=Отказана от специалиста, status_btn_contacted=Специалистът се свърза с мен, status_btn_done=Маркирай като завършена, status_btn_cancel=Откажи заявката, status_confirm_done=Сигурен ли си, че услугата е завършена?, status_confirm_cancel=Сигурен ли си, че искаш да откажеш тази заявка?, status_confirm_yes=Да, status_confirm_no=Не",
    "cs": "status_label_created=Odesláno, status_label_contacted=Kontakt navázán, status_label_done=Dokončeno, status_label_cancelled_by_client=Zrušeno, status_label_cancelled_by_provider=Zrušeno specialistou, status_btn_contacted=Specialista mě kontaktoval, status_btn_done=Označit jako dokončeno, status_btn_cancel=Zrušit žádost, status_confirm_done=Jste si jisti, že služba byla dokončena?, status_confirm_cancel=Jste si jisti, že chcete zrušit tuto žádost?, status_confirm_yes=Ano, status_confirm_no=Ne",
    "da": "status_label_created=Sendt, status_label_contacted=Kontakt oprettet, status_label_done=Afsluttet, status_label_cancelled_by_client=Annulleret, status_label_cancelled_by_provider=Annulleret af specialisten, status_btn_contacted=Specialisten kontaktede mig, status_btn_done=Markér som afsluttet, status_btn_cancel=Annuller anmodning, status_confirm_done=Er du sikker på, at tjenesten er afsluttet?, status_confirm_cancel=Er du sikker på, at du vil annullere denne anmodning?, status_confirm_yes=Ja, status_confirm_no=Nej",
    "de": "status_label_created=Gesendet, status_label_contacted=Kontakt hergestellt, status_label_done=Abgeschlossen, status_label_cancelled_by_client=Storniert, status_label_cancelled_by_provider=Vom Spezialisten storniert, status_btn_contacted=Der Spezialist hat mich kontaktiert, status_btn_done=Als abgeschlossen markieren, status_btn_cancel=Anfrage stornieren, status_confirm_done=Sind Sie sicher, dass die Dienstleistung abgeschlossen ist?, status_confirm_cancel=Sind Sie sicher, dass Sie diese Anfrage stornieren möchten?, status_confirm_yes=Ja, status_confirm_no=Nein",
    "el": "status_label_created=Εστάλη, status_label_contacted=Έγινε επικοινωνία, status_label_done=Ολοκληρώθηκε, status_label_cancelled_by_client=Ακυρώθηκε, status_label_cancelled_by_provider=Ακυρώθηκε από τον ειδικό, status_btn_contacted=Ο ειδικός επικοινώνησε μαζί μου, status_btn_done=Σήμανση ως ολοκληρωμένο, status_btn_cancel=Ακύρωση αιτήματος, status_confirm_done=Είστε σίγουροι ότι η υπηρεσία ολοκληρώθηκε;, status_confirm_cancel=Είστε σίγουροι ότι θέλετε να ακυρώσετε αυτό το αίτημα;, status_confirm_yes=Ναι, status_confirm_no=Όχι",
    "en": "status_label_created=Submitted, status_label_contacted=Contact made, status_label_done=Completed, status_label_cancelled_by_client=Cancelled, status_label_cancelled_by_provider=Cancelled by specialist, status_btn_contacted=The specialist contacted me, status_btn_done=Mark as completed, status_btn_cancel=Cancel request, status_confirm_done=Are you sure the service is completed?, status_confirm_cancel=Are you sure you want to cancel this request?, status_confirm_yes=Yes, status_confirm_no=No",
    "es": "status_label_created=Enviada, status_label_contacted=Contacto realizado, status_label_done=Completada, status_label_cancelled_by_client=Cancelada, status_label_cancelled_by_provider=Cancelada por el especialista, status_btn_contacted=El especialista me contactó, status_btn_done=Marcar como completada, status_btn_cancel=Cancelar solicitud, status_confirm_done=¿Estás seguro de que el servicio está completado?, status_confirm_cancel=¿Estás seguro de que quieres cancelar esta solicitud?, status_confirm_yes=Sí, status_confirm_no=No",
    "et": "status_label_created=Saadetud, status_label_contacted=Kontakt loodud, status_label_done=Lõpetatud, status_label_cancelled_by_client=Tühistatud, status_label_cancelled_by_provider=Tühistatud spetsialisti poolt, status_btn_contacted=Spetsialist võttis minuga ühendust, status_btn_done=Märgi lõpetatuks, status_btn_cancel=Tühista taotlus, status_confirm_done=Kas olete kindel, et teenus on lõpetatud?, status_confirm_cancel=Kas olete kindel, et soovite selle taotluse tühistada?, status_confirm_yes=Jah, status_confirm_no=Ei",
    "fi": "status_label_created=Lähetetty, status_label_contacted=Yhteys otettu, status_label_done=Valmis, status_label_cancelled_by_client=Peruutettu, status_label_cancelled_by_provider=Peruutettu asiantuntijan toimesta, status_btn_contacted=Asiantuntija otti minuun yhteyttä, status_btn_done=Merkitse valmiiksi, status_btn_cancel=Peruuta pyyntö, status_confirm_done=Oletko varma, että palvelu on valmis?, status_confirm_cancel=Oletko varma, että haluat peruuttaa tämän pyynnön?, status_confirm_yes=Kyllä, status_confirm_no=Ei",
    "fr": "status_label_created=Envoyée, status_label_contacted=Contact établi, status_label_done=Terminée, status_label_cancelled_by_client=Annulée, status_label_cancelled_by_provider=Annulée par le spécialiste, status_btn_contacted=Le spécialiste m'a contacté, status_btn_done=Marquer comme terminée, status_btn_cancel=Annuler la demande, status_confirm_done=Êtes-vous sûr que le service est terminé ?, status_confirm_cancel=Êtes-vous sûr de vouloir annuler cette demande ?, status_confirm_yes=Oui, status_confirm_no=Non",
    "ga": "status_label_created=Seolta, status_label_contacted=Teagmháil déanta, status_label_done=Críochnaithe, status_label_cancelled_by_client=Cealaithe, status_label_cancelled_by_provider=Cealaithe ag an speisialtóir, status_btn_contacted=Chuir an speisialtóir in aithne liom, status_btn_done=Marcáil mar chríochnaithe, status_btn_cancel=Cealaigh an t-iarratas, status_confirm_done=An bhfuil tú cinnte go bhfuil an tseirbhís críochnaithe?, status_confirm_cancel=An bhfuil tú cinnte gur mhaith leat an t-iarratas seo a chealú?, status_confirm_yes=Tá, status_confirm_no=Níl",
    "hr": "status_label_created=Poslano, status_label_contacted=Kontakt ostvaren, status_label_done=Završeno, status_label_cancelled_by_client=Otkazano, status_label_cancelled_by_provider=Otkazano od strane stručnjaka, status_btn_contacted=Stručnjak me kontaktirao, status_btn_done=Označi kao završeno, status_btn_cancel=Otkaži zahtjev, status_confirm_done=Jeste li sigurni da je usluga završena?, status_confirm_cancel=Jeste li sigurni da želite otkazati ovaj zahtjev?, status_confirm_yes=Da, status_confirm_no=Ne",
    "hu": "status_label_created=Elküldve, status_label_contacted=Kapcsolat felvéve, status_label_done=Befejezve, status_label_cancelled_by_client=Lemondva, status_label_cancelled_by_provider=A szakértő lemondta, status_btn_contacted=A szakértő felvette velem a kontaktust, status_btn_done=Megjelölés befejezettként, status_btn_cancel=Kérés visszavonása, status_confirm_done=Biztos vagy benne, hogy a szolgáltatás befejeződött?, status_confirm_cancel=Biztos vagy benne, hogy vissza akarod vonni ezt a kérést?, status_confirm_yes=Igen, status_confirm_no=Nem",
    "is": "status_label_created=Sent, status_label_contacted=Samband komið á, status_label_done=Lokið, status_label_cancelled_by_client=Hætt við, status_label_cancelled_by_provider=Hætt við af sérfræðingi, status_btn_contacted=Sérfræðingurinn hafði samband við mig, status_btn_done=Merkja sem lokið, status_btn_cancel=Hætta við beiðni, status_confirm_done=Ertu viss um að þjónustan sé lokið?, status_confirm_cancel=Ertu viss um að þú viljir hætta við þessa beiðni?, status_confirm_yes=Já, status_confirm_no=Nei",
    "it": "status_label_created=Inviata, status_label_contacted=Contatto stabilito, status_label_done=Completata, status_label_cancelled_by_client=Annullata, status_label_cancelled_by_provider=Annullata dallo specialista, status_btn_contacted=Lo specialista mi ha contattato, status_btn_done=Segna como completata, status_btn_cancel=Annulla richiesta, status_confirm_done=Sei sicuro che il servizio sia completato?, status_confirm_cancel=Sei sicuro di voler annullare questa richiesta?, status_confirm_yes=Sì, status_confirm_no=No",
    "lb": "status_label_created=Geschéckt, status_label_contacted=Kontakt gemaach, status_label_done=Ofgeschloss, status_label_cancelled_by_client=Annuléiert, status_label_cancelled_by_provider=Vum Spezialist annuléiert, status_btn_contacted=Den Spezialist huet mech kontaktéiert, status_btn_done=Als ofgeschloss markéieren, status_btn_cancel=Ufro annuléieren, status_confirm_done=Sidd Dir sécher, dass de Service ofgeschloss ass?, status_confirm_cancel=Sidd Dir sécher, dass Dir dës Ufro annuléiere wëllt?, status_confirm_yes=Jo, status_confirm_no=Nee",
    "lt": "status_label_created=Išsiųsta, status_label_contacted=Kontaktas užmegztas, status_label_done=Baigta, status_label_cancelled_by_client=Atšaukta, status_label_cancelled_by_provider=Atšaukta specialisto, status_btn_contacted=Specialistas susisiekė su manimi, status_btn_done=Pažymėti kaip baigtą, status_btn_cancel=Atšaukti užklausą, status_confirm_done=Ar tikrai paslauga baigta?, status_confirm_cancel=Ar tikrai norite atšaukti šią užklausą?, status_confirm_yes=Taip, status_confirm_no=Ne",
    "lv": "status_label_created=Nosūtīts, status_label_contacted=Kontakts nodibināts, status_label_done=Pabeigts, status_label_cancelled_by_client=Atcelts, status_label_cancelled_by_provider=Atcelts no speciālista puses, status_btn_contacted=Speciālists sazinājās ar mani, status_btn_done=Atzīmēt kā pabeigtu, status_btn_cancel=Atcelt pieprasījumu, status_confirm_done=Vai esat pārliecināts, ka pakalpojums ir pabeigts?, status_confirm_cancel=Vai esat pārliecināts, ka vēlaties atcelt šo pieprasījumu?, status_confirm_yes=Jā, status_confirm_no=Nē",
    "mk": "status_label_created=Испратена, status_label_contacted=Воспоставен контакт, status_label_done=Завршена, status_label_cancelled_by_client=Откажана, status_label_cancelled_by_provider=Откажана од специјалистот, status_btn_contacted=Специјалистот ме контактираше, status_btn_done=Означи како завршена, status_btn_cancel=Откажи барање, status_confirm_done=Дали сте сигурни дека услугата е завршена?, status_confirm_cancel=Дали сте сигурни дека сакате да ја откажете оваа барање?, status_confirm_yes=Да, status_confirm_no=Не",
    "mt": "status_label_created=Mibgħuta, status_label_contacted=Kuntatt magħmul, status_label_done=Lesta, status_label_cancelled_by_client=Ikkanċellata, status_label_cancelled_by_provider=Ikkanċellata mill-ispeċjalista, status_btn_contacted=L-ispeċjalista kkuntattjani, status_btn_done=Immarkja bħala lesta, status_btn_cancel=Ikkanċella t-talba, status_confirm_done=Ċert li s-servizz tlesta?, status_confirm_cancel=Ċert li trid tikkanċella din it-talba?, status_confirm_yes=Iva, status_confirm_no=Le",
    "nl": "status_label_created=Verzonden, status_label_contacted=Contact gelegd, status_label_done=Voltooid, status_label_cancelled_by_client=Geannuleerd, status_label_cancelled_by_provider=Geannuleerd door de specialist, status_btn_contacted=De specialist heeft contact met mij opgenomen, status_btn_done=Markeer als voltooid, status_btn_cancel=Verzoek annuleren, status_confirm_done=Weet u zeker dat de dienst is voltooid?, status_confirm_cancel=Weet u zeker dat u dit verzoek wilt annuleren?, status_confirm_yes=Ja, status_confirm_no=Nee",
    "no": "status_label_created=Sendt, status_label_contacted=Kontakt opprettet, status_label_done=Fullført, status_label_cancelled_by_client=Avbestilt, status_label_cancelled_by_provider=Avbestilt av spesialisten, status_btn_contacted=Spesialisten kontaktet meg, status_btn_done=Merk som fullført, status_btn_cancel=Avbryt forespørsel, status_confirm_done=Er du sikker på at tjenesten er fullført?, status_confirm_cancel=Er du sikker på at du vil avbryte denne forespørselen?, status_confirm_yes=Ja, status_confirm_no=Nei",
    "pl": "status_label_created=Wysłane, status_label_contacted=Nawiązano kontakt, status_label_done=Ukończone, status_label_cancelled_by_client=Anulowane, status_label_cancelled_by_provider=Anulowane przez specjalistę, status_btn_contacted=Specjalista skontaktował się ze mną, status_btn_done=Oznacz jako ukończone, status_btn_cancel=Anuluj zgłoszenie, status_confirm_done=Czy jesteś pewien, że usługa została ukończona?, status_confirm_cancel=Czy jesteś pewien, że chcesz anulować to zgłoszenie?, status_confirm_yes=Tak, status_confirm_no=Nie",
    "pt": "status_label_created=Enviada, status_label_contacted=Contato feito, status_label_done=Concluída, status_label_cancelled_by_client=Cancelada, status_label_cancelled_by_provider=Cancelada pelo especialista, status_btn_contacted=O especialista entrou em contato comigo, status_btn_done=Marcar como concluída, status_btn_cancel=Cancelar solicitação, status_confirm_done=Tem certeza de que o serviço foi concluído?, status_confirm_cancel=Tem certeza de que deseja cancelar esta solicitação?, status_confirm_yes=Sim, status_confirm_no=Não",
    "pt-PT": "status_label_created=Enviada, status_label_contacted=Contacto estabelecido, status_label_done=Concluída, status_label_cancelled_by_client=Cancelada, status_label_cancelled_by_provider=Cancelada pelo especialista, status_btn_contacted=O especialista contactou-me, status_btn_done=Marcar como concluída, status_btn_cancel=Cancelar pedido, status_confirm_done=Tem a certeza de que o serviço foi concluído?, status_confirm_cancel=Tem a certeza de que quer cancelar este pedido?, status_confirm_yes=Sim, status_confirm_no=Não",
    "ro": "status_label_created=Trimisă, status_label_contacted=Contact stabilit, status_label_done=Finalizată, status_label_cancelled_by_client=Anulată, status_label_cancelled_by_provider=Anulată de specialist, status_btn_contacted=Specialistul m-a contactat, status_btn_done=Marchează ca finalizată, status_btn_cancel=Anulează cererea, status_confirm_done=Ești sigur că serviciul a fost finalizat?, status_confirm_cancel=Ești sigur că vrei să anulezi această cerere?, status_confirm_yes=Da, status_confirm_no=Nu",
    "ru": "status_label_created=Отправлена, status_label_contacted=Контакт установлен, status_label_done=Завершена, status_label_cancelled_by_client=Отменена, status_label_cancelled_by_provider=Отменена специалистом, status_btn_contacted=Специалист связался со мной, status_btn_done=Отметить как завершённую, status_btn_cancel=Отменить заявку, status_confirm_done=Вы уверены, что услуга завершена?, status_confirm_cancel=Вы уверены, что хотите отменить эту заявку?, status_confirm_yes=Да, status_confirm_no=Нет",
    "sk": "status_label_created=Odoslané, status_label_contacted=Kontakt nadviazaný, status_label_done=Dokončené, status_label_cancelled_by_client=Zrušené, status_label_cancelled_by_provider=Zrušené špecialistom, status_btn_contacted=Špecialista ma kontaktoval, status_btn_done=Označiť ako dokončené, status_btn_cancel=Zrušiť požiadavku, status_confirm_done=Ste si istí, že služba bola dokončená?, status_confirm_cancel=Ste si istí, že chcete zrušiť túto požiadavku?, status_confirm_yes=Áno, status_confirm_no=Nie",
    "sl": "status_label_created=Poslano, status_label_contacted=Vzpostavljen stik, status_label_done=Zaključeno, status_label_cancelled_by_client=Preklicano, status_label_cancelled_by_provider=Preklicano s strani strokovnjaka, status_btn_contacted=Strokovnjak me je kontaktiral, status_btn_done=Označi kot zaključeno, status_btn_cancel=Prekliči zahtevo, status_confirm_done=Ste prepričani, da je storitev zaključena?, status_confirm_cancel=Ste prepričani, da želite preklicati to zahtevo?, status_confirm_yes=Da, status_confirm_no=Ne",
    "sq": "status_label_created=Dërguar, status_label_contacted=Kontakti u bë, status_label_done=Përfunduar, status_label_cancelled_by_client=Anuluar, status_label_cancelled_by_provider=Anuluar nga specialisti, status_btn_contacted=Specialisti u kontaktua me mua, status_btn_done=Shëno si të përfunduar, status_btn_cancel=Anulo kërkesën, status_confirm_done=Jeni të sigurt që shërbimi është përfunduar?, status_confirm_cancel=Jeni të sigurt që dëshironi të anuloni këtë kërkesë?, status_confirm_yes=Po, status_confirm_no=Jo",
    "sr": "status_label_created=Послато, status_label_contacted=Контакт успостављен, status_label_done=Завршено, status_label_cancelled_by_client=Отказано, status_label_cancelled_by_provider=Откажано од стране специјалисте, status_btn_contacted=Специјалиста ме је контактирао, status_btn_done=Означи као завршено, status_btn_cancel=Откажи захтев, status_confirm_done=Да ли сте сигурни да је услуга завршена?, status_confirm_cancel=Да ли сте сигурни да желите да откажете овај захтев?, status_confirm_yes=Да, status_confirm_no=Не",
    "sv": "status_label_created=Skickad, status_label_contacted=Kontakt tagen, status_label_done=Klar, status_label_cancelled_by_client=Avbokad, status_label_cancelled_by_provider=Avbokad av specialisten, status_btn_contacted=Specialisten kontaktade mig, status_btn_done=Markera som klar, status_btn_cancel=Avboka förfrågan, status_confirm_done=Är du säker på att tjänsten är klar?, status_confirm_cancel=Är du säker på att du vill avboka denna förfrågan?, status_confirm_yes=Ja, status_confirm_no=Nej",
    "tr": "status_label_created=Gönderildi, status_label_contacted=İletişim kuruldu, status_label_done=Tamamlandı, status_label_cancelled_by_client=İptal edildi, status_label_cancelled_by_provider=Uzman tarafından iptal edildi, status_btn_contacted=Uzman benimle iletişime geçti, status_btn_done=Tamamlandı olarak işaretle, status_btn_cancel=İsteği iptal et, status_confirm_done=Hizmetin tamamlandığından emin misiniz?, status_confirm_cancel=Bu isteği iptal etmek istediğinizden emin misiniz?, status_confirm_yes=Evet, status_confirm_no=Hayır",
    "uk": "status_label_created=Надіслано, status_label_contacted=Контакт встановлено, status_label_done=Завершено, status_label_cancelled_by_client=Скасовано, status_label_cancelled_by_provider=Скасовано фахівцем, status_btn_contacted=Фахівець зв'язався зі мною, status_btn_done=Позначити як завершено, status_btn_cancel=Скасувати заявку, status_confirm_done=Ви впевнені, що послугу завершено?, status_confirm_cancel=Ви впевнені, що хочете скасувати цю заявку?, status_confirm_yes=Так, status_confirm_no=Ні",
}

RAW_PROVIDER_DATA = {
    "bg": "status_label_new=Нова, status_label_contacted=Осъществен контакт, status_label_done=Завършена, status_label_cancelled_by_provider=Отказана, status_label_cancelled_by_client=Клиентът отказа, status_btn_contacted=Осъществен контакт, status_btn_cancel=Откажи заявката",
    "cs": "status_label_new=Nová, status_label_contacted=Kontakt navázán, status_label_done=Dokončeno, status_label_cancelled_by_provider=Zrušeno, status_label_cancelled_by_client=Klient zrušil, status_btn_contacted=Kontakt navázán, status_btn_cancel=Zrušit žádost",
    "da": "status_label_new=Ny, status_label_contacted=Kontakt oprettet, status_label_done=Afsluttet, status_label_cancelled_by_provider=Annulleret, status_label_cancelled_by_client=Kunden annullerede, status_btn_contacted=Kontakt oprettet, status_btn_cancel=Annuller anmodning",
    "de": "status_label_new=Neu, status_label_contacted=Kontakt hergestellt, status_label_done=Abgeschlossen, status_label_cancelled_by_provider=Storniert, status_label_cancelled_by_client=Kunde hat storniert, status_btn_contacted=Kontakt hergestellt, status_btn_cancel=Anfrage stornieren",
    "el": "status_label_new=Νέα, status_label_contacted=Έγινε επικοινωνία, status_label_done=Ολοκληρώθηκε, status_label_cancelled_by_provider=Ακυρώθηκε, status_label_cancelled_by_client=Ο πελάτης ακύρωσε, status_btn_contacted=Έγινε επικοινωνία, status_btn_cancel=Ακύρωση αιτήματος",
    "en": "status_label_new=New, status_label_contacted=Contact made, status_label_done=Completed, status_label_cancelled_by_provider=Cancelled, status_label_cancelled_by_client=Client cancelled, status_btn_contacted=Contact made, status_btn_cancel=Cancel request",
    "es": "status_label_new=Nueva, status_label_contacted=Contacto realizado, status_label_done=Completada, status_label_cancelled_by_provider=Cancelada, status_label_cancelled_by_client=El cliente canceló, status_btn_contacted=Contacto realizado, status_btn_cancel=Cancelar solicitud",
    "et": "status_label_new=Uus, status_label_contacted=Kontakt loodud, status_label_done=Lõpetatud, status_label_cancelled_by_provider=Tühistatud, status_label_cancelled_by_client=Klient tühistas, status_btn_contacted=Kontakt loodud, status_btn_cancel=Tühista taotlus",
    "fi": "status_label_new=Uusi, status_label_contacted=Yhteys otettu, status_label_done=Valmis, status_label_cancelled_by_provider=Peruutettu, status_label_cancelled_by_client=Asiakas peruutti, status_btn_contacted=Yhteys otettu, status_btn_cancel=Peruuta pyyntö",
    "fr": "status_label_new=Nouvelle, status_label_contacted=Contact établi, status_label_done=Terminée, status_label_cancelled_by_provider=Annulée, status_label_cancelled_by_client=Le client a annulé, status_btn_contacted=Contact établi, status_btn_cancel=Annuler la demande",
    "ga": "status_label_new=Nua, status_label_contacted=Teagmháil déanta, status_label_done=Críochnaithe, status_label_cancelled_by_provider=Cealaithe, status_label_cancelled_by_client=Dhiúltaigh an cliant, status_btn_contacted=Teagmháil déanta, status_btn_cancel=Cealaigh an t-iarratas",
    "hr": "status_label_new=Nova, status_label_contacted=Kontakt ostvaren, status_label_done=Završeno, status_label_cancelled_by_provider=Otkazano, status_label_cancelled_by_client=Klijent je otkazao, status_btn_contacted=Kontakt ostvaren, status_btn_cancel=Otkaži zahtjev",
    "hu": "status_label_new=Új, status_label_contacted=Kapcsolat felvéve, status_label_done=Befejezve, status_label_cancelled_by_provider=Lemondva, status_label_cancelled_by_client=Az ügyfél lemondta, status_btn_contacted=Kapcsolat felvéve, status_btn_cancel=Kérés visszavonása",
    "is": "status_label_new=Ný, status_label_contacted=Samband komið á, status_label_done=Lokið, status_label_cancelled_by_provider=Hætt við, status_label_cancelled_by_client=Viðskiptavinurinn hætti við, status_btn_contacted=Samband komið á, status_btn_cancel=Hætta við beiðni",
    "it": "status_label_new=Nuova, status_label_contacted=Contatto stabilito, status_label_done=Completata, status_label_cancelled_by_provider=Annullata, status_label_cancelled_by_client=Il cliente ha annullato, status_btn_contacted=Contatto stabilito, status_btn_cancel=Annulla richiesta",
    "lb": "status_label_new=Nei, status_label_contacted=Kontakt gemaach, status_label_done=Ofgeschloss, status_label_cancelled_by_provider=Annuléiert, status_label_cancelled_by_client=De Client huet annuléiert, status_btn_contacted=Kontakt gemaach, status_btn_cancel=Ufro annuléieren",
    "lt": "status_label_new=Nauja, status_label_contacted=Kontaktas užmegztas, status_label_done=Baigta, status_label_cancelled_by_provider=Atšaukta, status_label_cancelled_by_client=Klientas atšaukė, status_btn_contacted=Kontaktas užmegztas, status_btn_cancel=Atšaukti užklausą",
    "lv": "status_label_new=Jauns, status_label_contacted=Kontakts nodibināts, status_label_done=Pabeigts, status_label_cancelled_by_provider=Atcelts, status_label_cancelled_by_client=Klients atcēla, status_btn_contacted=Kontakts nodibināts, status_btn_cancel=Atcelt pieprasījumu",
    "mk": "status_label_new=Нова, status_label_contacted=Воспоставен контакт, status_label_done=Завршена, status_label_cancelled_by_provider=Откажана, status_label_cancelled_by_client=Клиентот откажа, status_btn_contacted=Воспоставен контакт, status_btn_cancel=Откажи барање",
    "mt": "status_label_new=Ġdida, status_label_contacted=Kuntatt magħmul, status_label_done=Lesta, status_label_cancelled_by_provider=Ikkanċellata, status_label_cancelled_by_client=Il-klijent ikkanċella, status_btn_contacted=Kuntatt magħmul, status_btn_cancel=Ikkanċella t-talba",
    "nl": "status_label_new=Nieuw, status_label_contacted=Contact gelegd, status_label_done=Voltooid, status_label_cancelled_by_provider=Geannuleerd, status_label_cancelled_by_client=Klant heeft geannuleerd, status_btn_contacted=Contact gelegd, status_btn_cancel=Verzoek annuleren",
    "no": "status_label_new=Ny, status_label_contacted=Kontakt opprettet, status_label_done=Fullført, status_label_cancelled_by_provider=Avbestilt, status_label_cancelled_by_client=Kunden avbestilte, status_btn_contacted=Kontakt opprettet, status_btn_cancel=Avbryt forespørsel",
    "pl": "status_label_new=Nowe, status_label_contacted=Nawiązano kontakt, status_label_done=Ukończone, status_label_cancelled_by_provider=Anulowane, status_label_cancelled_by_client=Klient anulował, status_btn_contacted=Nawiązano kontakt, status_btn_cancel=Anuluj zgłoszenie",
    "pt": "status_label_new=Nova, status_label_contacted=Contato feito, status_label_done=Concluída, status_label_cancelled_by_provider=Cancelada, status_label_cancelled_by_client=O cliente cancelou, status_btn_contacted=Contato feito, status_btn_cancel=Cancelar solicitação",
    "pt-PT": "status_label_new=Nova, status_label_contacted=Contacto feito, status_label_done=Concluída, status_label_cancelled_by_provider=Cancelada, status_label_cancelled_by_client=O cliente cancelou, status_btn_contacted=Contacto feito, status_btn_cancel=Cancelar pedido",
    "ro": "status_label_new=Nouă, status_label_contacted=Contact stabilit, status_label_done=Finalizată, status_label_cancelled_by_provider=Anulată, status_label_cancelled_by_client=Clientul a anulat, status_btn_contacted=Contact stabilit, status_btn_cancel=Anulează cererea",
    "ru": "status_label_new=Новая, status_label_contacted=Контакт установлен, status_label_done=Завершена, status_label_cancelled_by_provider=Отменена, status_label_cancelled_by_client=Клиент отменил, status_btn_contacted=Контакт установлен, status_btn_cancel=Отменить заявку",
    "sk": "status_label_new=Nová, status_label_contacted=Kontakt nadviazaný, status_label_done=Dokončené, status_label_cancelled_by_provider=Zrušené, status_label_cancelled_by_client=Klient zrušil, status_btn_contacted=Kontakt nadviazaný, status_btn_cancel=Zrušiť požiadavku",
    "sl": "status_label_new=Nova, status_label_contacted=Vzpostavljen stik, status_label_done=Zaključeno, status_label_cancelled_by_provider=Preklicano, status_label_cancelled_by_client=Stranka je preklicala, status_btn_contacted=Vzpostavljen stik, status_btn_cancel=Prekliči zahtevo",
    "sq": "status_label_new=E re, status_label_contacted=Kontakti u bë, status_label_done=Përfunduar, status_label_cancelled_by_provider=Anuluar, status_label_cancelled_by_client=Klienti anuloi, status_btn_contacted=Kontakti u bë, status_btn_cancel=Anulo kërkesën",
    "sr": "status_label_new=Нова, status_label_contacted=Контакт успостављен, status_label_done=Завршено, status_label_cancelled_by_provider=Отказано, status_label_cancelled_by_client=Клијент је отказао, status_btn_contacted=Контакт успостављен, status_btn_cancel=Откажи захтев",
    "sv": "status_label_new=Ny, status_label_contacted=Kontakt tagen, status_label_done=Klar, status_label_cancelled_by_provider=Avbokad, status_label_cancelled_by_client=Kunden avbokade, status_btn_contacted=Kontakt tagen, status_btn_cancel=Avboka förfrågan",
    "tr": "status_label_new=Yeni, status_label_contacted=İletişim kuruldu, status_label_done=Tamamlandı, status_label_cancelled_by_provider=İptal edildi, status_label_cancelled_by_client=Müşteri iptal etti, status_btn_contacted=İletişim kuruldu, status_btn_cancel=İsteği iptal et",
    "uk": "status_label_new=Нова, status_label_contacted=Контакт встановлено, status_label_done=Завершено, status_label_cancelled_by_provider=Скасовано, status_label_cancelled_by_client=Клієнт скасував, status_btn_contacted=Контакт встановлено, status_btn_cancel=Скасувати заявку",
}

def parse_raw_data(raw_data):
    """Parse comma-separated key=value string into a dict."""
    result = {}
    # Use split carefully to handle potential commas in values (though not present here)
    parts = raw_data.split(", ")
    for part in parts:
        if "=" in part:
            k, v = part.split("=", 1)
            result[k.strip()] = v.strip()
    return result

def main():
    db_url = os.getenv("DATABASE_URL", "postgresql://nevumo:nevumo@localhost:5432/nevumo_leads")
    engine = create_engine(db_url)
    
    rows = []
    
    # Process client_dashboard
    client_translations = {}
    for lang, raw_str in RAW_CLIENT_DATA.items():
        lang_data = parse_raw_data(raw_str)
        for key in CLIENT_DASHBOARD_KEYS:
            if key in lang_data:
                rows.append({
                    "lang": lang,
                    "key": f"client_dashboard.{key}",
                    "value": lang_data[key]
                })
                # Cache for provider_dashboard confirm keys
                if key in ["status_confirm_cancel", "status_confirm_yes", "status_confirm_no"]:
                    if lang not in client_translations:
                        client_translations[lang] = {}
                    client_translations[lang][key] = lang_data[key]

    # Process provider_dashboard
    for lang, raw_str in RAW_PROVIDER_DATA.items():
        lang_data = parse_raw_data(raw_str)
        # Main keys
        for key in PROVIDER_DASHBOARD_KEYS:
            if key in lang_data:
                rows.append({
                    "lang": lang,
                    "key": f"provider_dashboard.{key}",
                    "value": lang_data[key]
                })
        
        # Confirm keys (same as client_dashboard)
        confirm_keys = ["status_confirm_cancel", "status_confirm_yes", "status_confirm_no"]
        for key in confirm_keys:
            if lang in client_translations and key in client_translations[lang]:
                rows.append({
                    "lang": lang,
                    "key": f"provider_dashboard.{key}",
                    "value": client_translations[lang][key]
                })

    if not rows:
        print("❌ No rows to seed!")
        return

    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO translations (lang, key, value)
                VALUES (:lang, :key, :value)
                ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
            """),
            rows,
        )
        conn.commit()
    
    print(f"✅ Seeded {len(rows)} rows for lead status translations.")

if __name__ == "__main__":
    main()
