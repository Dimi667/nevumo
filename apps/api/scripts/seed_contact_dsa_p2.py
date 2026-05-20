#!/usr/bin/env python3
"""
Seed contact DSA translations - Part 2.
Namespace: contact_dsa
Keys: 9 | Languages: 34
Run: docker exec nevumo-api python -m apps.api.scripts.seed_contact_dsa_p2
"""

import os

from sqlalchemy import create_engine, text

NAMESPACE = "contact_dsa"

# Language dictionaries with full keys (including namespace)
TRANSLATIONS_BY_LANG = {
    "en": {
        "contact_dsa.s3_title": "How to Report Illegal Content",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Your notice should include:",
        "contact_dsa.s3_what_to_include_body": "1. A description of the content you believe to be illegal and its exact location on the platform (URL or description).\n2. The legal reason why you believe the content is illegal.\n3. Your name and email address (except for reports involving child sexual abuse material).\n4. A statement confirming that the information in your notice is accurate and complete to the best of your knowledge.",
        "contact_dsa.s4_title": "What Happens After You Report",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Supported Languages",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Back to Home",
    },
    "bg": {
        "contact_dsa.s3_title": "Как да подадете сигнал за незаконно съдържание",
        "contact_dsa.s3_body": "Ако смятате, че съдържание в Nevumo е незаконно съгласно правото на ЕС или националното право, изпратете уведомление на legal@nevumo.com. За да можем да обработим сигнала Ви ефективно, моля включете следната информация:",
        "contact_dsa.s3_what_to_include_title": "Уведомлението Ви трябва да съдържа:",
        "contact_dsa.s3_what_to_include_body": "1. Описание на съдържанието, което смятате за незаконно, и точното му местоположение в платформата (URL адрес или описание).\n2. Правното основание, поради което смятате, че съдържанието е незаконно.\n3. Вашето ime и имейл адрес (с изключение на сигнали, свързани с материали за сексуално насилие над деца).\n4. Декларация, потвърждаваща, че информацията в уведомлението Ви е точна и пълна според Вашите знания.",
        "contact_dsa.s4_title": "Какво се случва след подаване на сигнал",
        "contact_dsa.s4_body": "При получаване на Вашето уведомление ние ще:\n• Изпратим автоматично потвърждение за получаване незабавно.\n• Разгледаме сигнала Ви своевременно, старателно и безпристрастно.\n• Предприемем действие в срок до 72 часа при спешни случаи (напр. съдържание, свързано с насилие, безопасност на деца или непосредствена заплаха).\n• Предприемем действие в срок до 7 работни дни при стандартни сигнали.\n• Уведомим Ви за нашето решение и основанията за него.\n• Информираме Ви за правото Ви да обжалвате решението ни.",
        "contact_dsa.s5_title": "Поддържани езици",
        "contact_dsa.s5_body": "Nevumo приема уведомления по DSA и комуникации от власти на следните езици: английски, български, полски. Когато е възможно, ще отговаряме на езика на Вашата комуникация.",
        "contact_dsa.back_to_home": "Начало",
    },
    "cs": {
        "contact_dsa.s3_title": "Jak nahlásit nezákonný obsah",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Vaše oznámení by mělo obsahovat:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Co se stane po nahlášení",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Podporované jazyky",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Zpět na úvod",
    },
    "da": {
        "contact_dsa.s3_title": "Sådan anmelder du ulovligt indhold",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Din anmeldelse bør indeholde:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Hvad sker der efter din anmeldelse",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Understøttede sprog",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Tilbage til forsiden",
    },
    "de": {
        "contact_dsa.s3_title": "So melden Sie rechtswidrige Inhalte",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Ihre Meldung sollte enthalten:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Was nach Ihrer Meldung passiert",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Unterstützte Sprachen",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Zurück zur Startseite",
    },
    "el": {
        "contact_dsa.s3_title": "Πώς να αναφέρετε παράνομο περιεχόμενο",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Η ειδοποίησή σας πρέπει να περιλαμβάνει:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Τι γίνεται μετά την αναφορά",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Υποστηριζόμενες γλώσσες",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Επιστροφή στην αρχική",
    },
    "es": {
        "contact_dsa.s3_title": "Cómo denunciar contenido ilegal",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Su aviso debe incluir:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Qué sucede después de su denuncia",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Idiomas admitidos",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Volver al inicio",
    },
    "et": {
        "contact_dsa.s3_title": "Kuidas teatada ebaseaduslikust sisust",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Teie teatis peaks sisaldama:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Mis juhtub pärast teatamist",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Toetatud keeled",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Tagasi avalehele",
    },
    "fi": {
        "contact_dsa.s3_title": "Kuinka ilmoittaa laittomasta sisällöstä",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Ilmoituksesi tulee sisältää:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Mitä tapahtuu ilmoituksen jälkeen",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Tuetut kielet",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Takaisin etusivulle",
    },
    "fr": {
        "contact_dsa.s3_title": "Comment signaler un contenu illicite",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Votre notification doit inclure :",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Que se passe-t-il après votre signalement",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Langues prises en charge",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Retour à l'accueil",
    },
    "ga": {
        "contact_dsa.s3_title": "Conas Ábhar Neamhdhleathach a Thuairisciú",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Ba cheart go n-áireofaí i d'fhógra:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Cad a Tharlaíonn Tar éis Tuairisciú",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Teangacha Tacaithe",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Ar ais go dtí an Baile",
    },
    "hr": {
        "contact_dsa.s3_title": "Kako prijaviti nezakoniti sadržaj",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Vaša prijava treba sadržavati:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Što se događa nakon prijave",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Podržani jezici",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Natrag na početnu",
    },
    "hu": {
        "contact_dsa.s3_title": "Hogyan jelentsen illegális tartalmat",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Az értesítésnek tartalmaznia kell:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Mi történik a bejelentés után",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Támogatott nyelvek",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Vissza a főoldalra",
    },
    "is": {
        "contact_dsa.s3_title": "Hvernig á að tilkynna um ólöglegt efni",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Tilkynning þín ætti að innihalda:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Hvað gerist eftir að þú tilkynnir",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Studdar tungumál",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Aftur á forsíðu",
    },
    "it": {
        "contact_dsa.s3_title": "Come segnalare contenuti illegali",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "La sua segnalazione deve includere:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Cosa succede dopo la segnalazione",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Lingue supportate",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Torna alla home",
    },
    "lb": {
        "contact_dsa.s3_title": "Wéi ee illegalen Inhalt mellt",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Är Meldung soll enthalen:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Wat geschitt no Ärer Meldung",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Ënnerstëtzte Sproochen",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Zréck zur Haaptsäit",
    },
    "lt": {
        "contact_dsa.s3_title": "Kaip pranešti apie neteisėtą turinį",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Jūsų pranešime turėtų būti:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Kas nutinka po pranešimo",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Palaikomos kalbos",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Grįžti į pradžią",
    },
    "lv": {
        "contact_dsa.s3_title": "Kā ziņot par nelikumīgu saturu",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Jūsu paziņojumā jāiekļauj:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Kas notiek pēc ziņošanas",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Atbalstītās valodas",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Atpakaļ uz sākumu",
    },
    "mk": {
        "contact_dsa.s3_title": "Како да пријавите незаконита содржина",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Вашата пријава треба да содржи:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Што се случува по пријавата",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Поддржани јазици",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Назад кон почетна",
    },
    "mt": {
        "contact_dsa.s3_title": "Kif Tirrapporta Kontenut Illegali",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "L-avviż tiegħek għandu jinkludi:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "X'jiġri Wara li Tirrapporta",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Lingwi Appoġġjati",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Lura għad-Dar",
    },
    "nl": {
        "contact_dsa.s3_title": "Hoe illegale inhoud te melden",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Uw melding moet het volgende bevatten:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Wat er na uw melding gebeurt",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Ondersteunde talen",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Terug naar home",
    },
    "no": {
        "contact_dsa.s3_title": "Slik rapporterer du ulovlig innhold",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Meldingen din bør inneholde:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Hva skjer etter at du rapporterer",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Støttede språk",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Tilbake til forsiden",
    },
    "pl": {
        "contact_dsa.s3_title": "Jak zgłosić nielegalne treści",
        "contact_dsa.s3_body": "Jeśli uważasz, że treści w serwisie Nevumo są nielegalne zgodnie z prawem UE lub prawem krajowym, wyślij zgłoszenie na adres legal@nevumo.com. Aby umożliwić nam skuteczne rozpatrzenie zgłoszenia, prosimy o podanie następujących informacji:",
        "contact_dsa.s3_what_to_include_title": "Zgłoszenie powinno zawierać:",
        "contact_dsa.s3_what_to_include_body": "1. Opis treści, które uważasz za nielegalne, oraz dokładna lokalizacja w serwisie (adres URL lub opis).\n2. Podstawa prawna, na której opierasz się, twierdząc, że treść jest nielegalna.\n3. Twoje imię i nazwisko oraz adres e-mail (z wyjątkiem zgłoszeń dotyczących materiałów przedstawiających seksualne wykorzystywanie dzieci).\n4. Oświadczenie potwierdzające, że informacje zawarte w zgłoszeniu są zgodne z Twoją najlepszą wiedzą.",
        "contact_dsa.s4_title": "Co dzieje się po zgłoszeniu",
        "contact_dsa.s4_body": "Po otrzymaniu zgłoszenia:\n• Niezwłocznie wyślemy automatyczne potwierdzenie odbioru.\n• Rozpatrzymy zgłoszenie terminowo, starannie i bezstronnie.\n• Podejmiemy działania w ciągu 72 godzin w pilnych przypadkach (np. treści związane z przemocą, bezpieczeństwem dzieci lub bezpośrednim zagrożeniem).\n• Podejmiemy działania w ciągu 7 dni roboczych w przypadku standardowych zgłoszeń.\n• Poinformujemy Cię o naszej decyzji i jej uzasadnieniu.\n• Poinformujemy Cię o prawie do odwołania od naszej decyzji.",
        "contact_dsa.s5_title": "Obsługiwane języki",
        "contact_dsa.s5_body": "Nevumo przyjmuje zgłoszenia DSA i komunikację od organów w następujących językach: angielskim, bułgarskim i polskim. W miarę możliwości będziemy odpowiadać w języku Twojej wiadomości.",
        "contact_dsa.back_to_home": "Powrót do strony głównej",
    },
    "pt": {
        "contact_dsa.s3_title": "Como Denunciar Conteúdo Ilegal",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Seu aviso deve incluir:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "O Que Acontece Após a Denúncia",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Idiomas Suportados",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Voltar ao início",
    },
    "pt_PT": {
        "contact_dsa.s3_title": "Como Denunciar Conteúdo Ilegal",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "O seu aviso deve incluir:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "O Que Acontece Após a Denúncia",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Idiomas Suportados",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Voltar ao início",
    },
    "ro": {
        "contact_dsa.s3_title": "Cum să raportați conținut ilegal",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Notificarea dvs. trebuie să includă:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Ce se întâmplă după raportare",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Limbi acceptate",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Înapoi la pagina principală",
    },
    "ru": {
        "contact_dsa.s3_title": "Как сообщить о незаконном контенте",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Ваше уведомление должно содержать:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Что происходит после подачи сообщения",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Поддерживаемые языки",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "На главную",
    },
    "sk": {
        "contact_dsa.s3_title": "Ako nahlásiť nezákonný obsah",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Vaše oznámenie by malo obsahovať:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Čo sa stane po nahlásení",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Podporované jazyky",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Späť na úvod",
    },
    "sl": {
        "contact_dsa.s3_title": "Kako prijaviti nezakonito vsebino",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Vaše obvestilo mora vsebovati:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Kaj se zgodi po prijavi",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Podprti jeziki",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Nazaj na začetek",
    },
    "sq": {
        "contact_dsa.s3_title": "Si të raportoni përmbajtje ilegale",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Njoftimi juaj duhet të përfshijë:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Çfarë ndodh pas raportimit",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Gjuhët e mbështetura",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Kthehu në faqen kryesore",
    },
    "sr": {
        "contact_dsa.s3_title": "Kako prijaviti nezakoniti sadržaj",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Vaša prijava treba da sadrži:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Šta se dešava nakon prijave",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Podržani jezici",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Nazad na početnu",
    },
    "sv": {
        "contact_dsa.s3_title": "Hur du anmäler olagligt innehåll",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Din anmälan bör innehålla:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Vad händer efter att du rapporterar",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Språk som stöds",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Tillbaka till startsidan",
    },
    "tr": {
        "contact_dsa.s3_title": "Yasadışı İçerik Nasıl Bildirilir",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Bildiriminiz şunları içermelidir:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Bildirimin Ardından Ne Olur",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Desteklenen Diller",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "Ana Sayfaya Dön",
    },
    "uk": {
        "contact_dsa.s3_title": "Як повідомити про незаконний вміст",
        "contact_dsa.s3_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s3_what_to_include_title": "Ваше повідомлення має містити:",
        "contact_dsa.s3_what_to_include_body": "If you believe content on Nevumo is illegal under EU or national law, please send a notice to legal@nevumo.com. To allow us to process your report effectively, please include the following information:",
        "contact_dsa.s4_title": "Що відбувається після повідомлення",
        "contact_dsa.s4_body": "Upon receipt of your notice, we will:\n• Send an automatic confirmation of receipt immediately.\n• Review your report in a timely, diligent, and non-arbitrary manner.\n• Take action within 72 hours for urgent cases (e.g. content involving violence, child safety, or imminent harm).\n• Take action within 7 working days for standard reports.\n• Notify you of our decision and the reasons for it.\n• Inform you of your right to appeal our decision.",
        "contact_dsa.s5_title": "Підтримувані мови",
        "contact_dsa.s5_body": "Nevumo accepts DSA notices and authority communications in the following languages: English, Bulgarian, Polish. We will respond in the language of your communication where possible.",
        "contact_dsa.back_to_home": "На головну",
    },
}


def get_database_url() -> str:
    """Get database URL from environment or use default."""
    return os.getenv("DATABASE_URL", "postgresql://nevumo:nevumo@localhost:5432/nevumo_leads")


def seed_translations() -> None:
    """Seed all contact DSA translations into the database."""
    engine = create_engine(get_database_url())

    with engine.connect() as conn:
        count = 0
        for lang, translations in TRANSLATIONS_BY_LANG.items():
            for key, value in translations.items():
                conn.execute(
                    text("""
                        INSERT INTO translations (lang, key, value)
                        VALUES (:lang, :key, :value)
                        ON CONFLICT (lang, key)
                        DO UPDATE SET value = EXCLUDED.value
                    """),
                    {"lang": lang, "key": key, "value": value}
                )
                count += 1

        conn.commit()
        print(f"Inserted/updated {count} translation rows for namespace '{NAMESPACE}'")


def verify_translations() -> None:
    """Verify the translations were inserted correctly."""
    engine = create_engine(get_database_url())

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT lang, COUNT(*) as keys
                FROM translations
                WHERE key LIKE :pattern
                GROUP BY lang
                ORDER BY lang
            """),
            {"pattern": f"{NAMESPACE}.%"}
        )
        rows = result.fetchall()
        print(f"\nVerification for namespace '{NAMESPACE}':")
        for row in rows:
            print(f"  {row[0]}: {row[1]} keys")


if __name__ == "__main__":
    seed_translations()
    verify_translations()
