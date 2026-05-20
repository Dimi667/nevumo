#!/usr/bin/env python3
"""
Seed contact DSA translations - Part 1.
Namespace: contact_dsa
Keys: 8 (page_title, meta_description, s1_title, s1_body, s2_title, s2_body, s2_email_privacy, s2_email_legal)
Languages: 34
Run: docker exec nevumo-api python -m apps.api.scripts.seed_contact_dsa_p1
"""

import os
from sqlalchemy import create_engine, text

NAMESPACE = "contact_dsa"

TRANSLATIONS_BY_LANG = {
    "en": {
        "contact_dsa.page_title": "DSA Contact Point",
        "contact_dsa.meta_description": "Contact point for authorities and users under the Digital Services Act (DSA). Report illegal content or contact Nevumo for DSA-related matters.",
        "contact_dsa.s1_title": "About This Page",
        "contact_dsa.s1_body": "Nevumo is operated by \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), registered in Sofia, Bulgaria. This page serves as our single point of contact under Article 11 of the Digital Services Act (Regulation (EU) 2022/2065), applicable from 17 February 2024.",
        "contact_dsa.s2_title": "Single Point of Contact",
        "contact_dsa.s2_body": "All DSA-related communications \u2014 including reports of illegal content, law enforcement requests, and authority enquiries \u2014 should be directed to:",
        "contact_dsa.s2_email_privacy": "Privacy & GDPR matters:",
        "contact_dsa.s2_email_legal": "Illegal content reports & law enforcement:",
    },
    "bg": {
        "contact_dsa.page_title": "\u0422\u043e\u0447\u043a\u0430 \u0437\u0430 \u043a\u043e\u043d\u0442\u0430\u043a\u0442 \u043f\u043e DSA",
        "contact_dsa.meta_description": "\u0422\u043e\u0447\u043a\u0430 \u0437\u0430 \u043a\u043e\u043d\u0442\u0430\u043a\u0442 \u0441 \u0432\u043b\u0430\u0441\u0442\u0438 \u0438 \u043f\u043e\u0442\u0440\u0435\u0431\u0438\u0442\u0435\u043b\u0438 \u043f\u043e \u0417\u0430\u043a\u043e\u043d\u0430 \u0437\u0430 \u0446\u0438\u0444\u0440\u043e\u0432\u0438\u0442\u0435 \u0443\u0441\u043b\u0443\u0433\u0438 (DSA). \u0421\u0438\u0433\u043d\u0430\u043b\u0438\u0437\u0438\u0440\u0430\u0439\u0442\u0435 \u0437\u0430 \u043d\u0435\u0437\u0430\u043a\u043e\u043d\u043d\u043e \u0441\u044a\u0434\u044a\u0440\u0436\u0430\u043d\u0438\u0435 \u0438\u043b\u0438 \u0441\u0435 \u0441\u0432\u044a\u0440\u0436\u0435\u0442\u0435 \u0441 Nevumo.",
        "contact_dsa.s1_title": "\u0417\u0430 \u0442\u0430\u0437\u0438 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430",
        "contact_dsa.s1_body": "Nevumo \u0441\u0435 \u0443\u043f\u0440\u0430\u0432\u043b\u044f\u0432\u0430 \u043e\u0442 \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (\u0415\u0418\u041a: 175369610), \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0438\u0440\u0430\u043d\u043e \u0432 \u0421\u043e\u0444\u0438\u044f, \u0411\u044a\u043b\u0433\u0430\u0440\u0438\u044f. \u0422\u0430\u0437\u0438 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 \u043f\u0440\u0435\u0434\u0441\u0442\u0430\u0432\u043b\u044f\u0432\u0430 \u043d\u0430\u0448\u0430\u0442\u0430 \u0435\u0434\u0438\u043d\u043d\u0430 \u0442\u043e\u0447\u043a\u0430 \u0437\u0430 \u043a\u043e\u043d\u0442\u0430\u043a\u0442 \u0441\u044a\u0433\u043b\u0430\u0441\u043d\u043e \u0447\u043b. 11 \u043e\u0442 \u0417\u0430\u043a\u043e\u043d\u0430 \u0437\u0430 \u0446\u0438\u0444\u0440\u043e\u0432\u0438\u0442\u0435 \u0443\u0441\u043b\u0443\u0433\u0438 (\u0420\u0435\u0433\u043b\u0430\u043c\u0435\u043d\u0442 (\u0415\u0421) 2022/2065), \u043f\u0440\u0438\u043b\u043e\u0436\u0438\u043c \u043e\u0442 17 \u0444\u0435\u0432\u0440\u0443\u0430\u0440\u0438 2024 \u0433.",
        "contact_dsa.s2_title": "\u0415\u0434\u0438\u043d\u043d\u0430 \u0442\u043e\u0447\u043a\u0430 \u0437\u0430 \u043a\u043e\u043d\u0442\u0430\u043a\u0442",
        "contact_dsa.s2_body": "\u0412\u0441\u0438\u0447\u043a\u0438 \u043a\u043e\u043c\u0443\u043d\u0438\u043a\u0430\u0446\u0438\u0438, \u0441\u0432\u044a\u0440\u0437\u0430\u043d\u0438 \u0441 DSA \u2014 \u0432\u043a\u043b\u044e\u0447\u0438\u0442\u0435\u043b\u043d\u043e \u0441\u0438\u0433\u043d\u0430\u043b\u0438 \u0437\u0430 \u043d\u0435\u0437\u0430\u043a\u043e\u043d\u043d\u043e \u0441\u044a\u0434\u044a\u0440\u0436\u0430\u043d\u0438\u0435, \u0437\u0430\u043f\u0438\u0442\u0432\u0430\u043d\u0438\u044f \u043e\u0442 \u043f\u0440\u0430\u0432\u043e\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u0435\u043b\u043d\u0438 \u043e\u0440\u0433\u0430\u043d\u0438 \u0438 \u043a\u043e\u043c\u043f\u0435\u0442\u0435\u043d\u0442\u043d\u0438 \u0432\u043b\u0430\u0441\u0442\u0438 \u2014 \u0441\u043b\u0435\u0434\u0432\u0430 \u0434\u0430 \u0431\u044a\u0434\u0430\u0442 \u0438\u0437\u043f\u0440\u0430\u0449\u0430\u043d\u0438 \u043d\u0430:",
        "contact_dsa.s2_email_privacy": "\u0412\u044a\u043f\u0440\u043e\u0441\u0438 \u0437\u0430 \u043f\u043e\u0432\u0435\u0440\u0438\u0442\u0435\u043b\u043d\u043e\u0441\u0442 \u0438 GDPR:",
        "contact_dsa.s2_email_legal": "\u0421\u0438\u0433\u043d\u0430\u043b\u0438 \u0437\u0430 \u043d\u0435\u0437\u0430\u043a\u043e\u043d\u043d\u043e \u0441\u044a\u0434\u044a\u0440\u0436\u0430\u043d\u0438\u0435 \u0438 \u0437\u0430\u043f\u0438\u0442\u0432\u0430\u043d\u0438\u044f \u043e\u0442 \u0432\u043b\u0430\u0441\u0442\u0438:",
    },
    "cs": {
        "contact_dsa.page_title": "Kontaktn\u00ed m\u00edsto DSA",
        "contact_dsa.meta_description": "Kontaktn\u00ed m\u00edsto pro org\u00e1ny a u\u017eivatele v r\u00e1mci z\u00e1kona o digit\u00e1ln\u00edch slu\u017eb\u00e1ch (DSA). Nahla\u0161te nelegit\u00e1ln\u00ed obsah nebo kontaktujte Nevumo v z\u00e1le\u017eitostech DSA.",
        "contact_dsa.s1_title": "O t\u00e9to str\u00e1nce",
        "contact_dsa.s1_body": "Nevumo provozuje \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), registrovan\u00e1 v Sofii v Bulharsku. Tato str\u00e1nka slou\u017e\u00ed jako na\u0161e jednotn\u00e9 kontaktn\u00ed m\u00edsto podle \u010dl\u00e1nku 11 z\u00e1kona o digit\u00e1ln\u00edch slu\u017eb\u00e1ch (na\u0159\u00edzen\u00ed (EU) 2022/2065), platn\u00e9ho od 17. \u00fanora 2024.",
        "contact_dsa.s2_title": "Jednotn\u00e9 kontaktn\u00ed m\u00edsto",
        "contact_dsa.s2_body": "Ve\u0161ker\u00e1 komunikace t\u00fdkaj\u00edc\u00ed se DSA \u2014 v\u010detn\u011b hl\u00e1\u0161en\u00ed nelegit\u00e1ln\u00edho obsahu, \u017e\u00e1dost\u00ed org\u00e1n\u016f \u010dinn\u00fdch v trestn\u00edm \u0159\u00edzen\u00ed a dotaz\u016f p\u0159\u00edslu\u0161n\u00fdch org\u00e1n\u016f \u2014 by m\u011bla b\u00fdt zas\u00edl\u00e1na na:",
        "contact_dsa.s2_email_privacy": "Ochrana soukrom\u00ed a GDPR:",
        "contact_dsa.s2_email_legal": "Hl\u00e1\u0161en\u00ed nelegit\u00e1ln\u00edho obsahu a org\u00e1ny:",
    },
    "da": {
        "contact_dsa.page_title": "DSA-kontaktpunkt",
        "contact_dsa.meta_description": "Kontaktpunkt for myndigheder og brugere i henhold til lov om digitale tjenester (DSA). Anmeld ulovligt indhold eller kontakt Nevumo i DSA-relaterede sager.",
        "contact_dsa.s1_title": "Om denne side",
        "contact_dsa.s1_body": "Nevumo drives af \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), registreret i Sofia, Bulgarien. Denne side fungerer som vores enkelt kontaktpunkt i henhold til artikel 11 i lov om digitale tjenester (forordning (EU) 2022/2065), g\u00e6ldende fra 17. februar 2024.",
        "contact_dsa.s2_title": "Enkelt kontaktpunkt",
        "contact_dsa.s2_body": "Al DSA-relateret kommunikation \u2014 herunder anmeldelser af ulovligt indhold, anmodninger fra retsh\u00e5ndh\u00e6vende myndigheder og foresp\u00f8rgsler fra myndigheder \u2014 bedes rettes til:",
        "contact_dsa.s2_email_privacy": "Privatlivs- og GDPR-sp\u00f8rgsm\u00e5l:",
        "contact_dsa.s2_email_legal": "Rapportering af ulovligt indhold og myndigheder:",
    },
    "de": {
        "contact_dsa.page_title": "DSA-Kontaktstelle",
        "contact_dsa.meta_description": "Kontaktstelle f\u00fcr Beh\u00f6rden und Nutzer gem\u00e4\u00df dem Gesetz \u00fcber digitale Dienste (DSA). Melden Sie illegale Inhalte oder kontaktieren Sie Nevumo in DSA-Angelegenheiten.",
        "contact_dsa.s1_title": "\u00dcber diese Seite",
        "contact_dsa.s1_body": "Nevumo wird betrieben von \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), eingetragen in Sofia, Bulgarien. Diese Seite dient als unsere einheitliche Kontaktstelle gem\u00e4\u00df Artikel 11 des Gesetzes \u00fcber digitale Dienste (Verordnung (EU) 2022/2065), anwendbar ab 17. Februar 2024.",
        "contact_dsa.s2_title": "Einheitliche Kontaktstelle",
        "contact_dsa.s2_body": "Alle DSA-bezogenen Mitteilungen \u2014 einschlie\u00dflich Meldungen rechtswidriger Inhalte, Anfragen von Strafverfolgungsbeh\u00f6rden und Beh\u00f6rdenanfragen \u2014 sind zu richten an:",
        "contact_dsa.s2_email_privacy": "Datenschutz & DSGVO:",
        "contact_dsa.s2_email_legal": "Meldungen rechtswidriger Inhalte & Beh\u00f6rdenanfragen:",
    },
    "el": {
        "contact_dsa.page_title": "\u03a3\u03b7\u03bc\u03b5\u03af\u03bf \u03b5\u03c0\u03b1\u03c6\u03ae\u03c2 DSA",
        "contact_dsa.meta_description": "\u03a3\u03b7\u03bc\u03b5\u03af\u03bf \u03b5\u03c0\u03b1\u03c6\u03ae\u03c2 \u03b3\u03b9\u03b1 \u03b1\u03c1\u03c7\u03ad\u03c2 \u03ba\u03b1\u03b9 \u03c7\u03c1\u03ae\u03c3\u03c4\u03b5\u03c2 \u03b2\u03ac\u03c3\u03b5\u03b9 \u03c4\u03b7\u03c2 \u03a0\u03c1\u03ac\u03be\u03b7\u03c2 \u03b3\u03b9\u03b1 \u03c4\u03b9\u03c2 \u03a8\u03b7\u03c6\u03b9\u03b1\u03ba\u03ad\u03c2 \u03a5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b5\u03c2 (DSA). \u0391\u03bd\u03b1\u03c6\u03ad\u03c1\u03b5\u03c4\u03b5 \u03c0\u03b1\u03c1\u03ac\u03bd\u03bf\u03bc\u03bf \u03c0\u03b5\u03c1\u03b9\u03b5\u03c7\u03cc\u03bc\u03b5\u03bd\u03bf \u03ae \u03b5\u03c0\u03b9\u03ba\u03bf\u03b9\u03bd\u03c9\u03bd\u03ae\u03c3\u03c4\u03b5 \u03bc\u03b5 \u03c4\u03bf Nevumo.",
        "contact_dsa.s1_title": "\u03a3\u03c7\u03b5\u03c4\u03b9\u03ba\u03ac \u03bc\u03b5 \u03b1\u03c5\u03c4\u03ae \u03c4\u03b7 \u03c3\u03b5\u03bb\u03af\u03b4\u03b1",
        "contact_dsa.s1_body": "\u03a4\u03bf Nevumo \u03bb\u03b5\u03b9\u03c4\u03bf\u03c5\u03c1\u03b3\u03b5\u03af \u03b1\u03c0\u03cc \u03c4\u03b7\u03bd \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0394 (EIK: 175369610), \u03b5\u03b3\u03b3\u03b5\u03b3\u03c1\u03b1\u03bc\u03bc\u03ad\u03bd\u03b7 \u03c3\u03c4\u03b7 \u03a3\u03cc\u03c6\u03b9\u03b1, \u0392\u03bf\u03c5\u03bb\u03b3\u03b1\u03c1\u03af\u03b1. \u0397 \u03c3\u03b5\u03bb\u03af\u03b4\u03b1 \u03b1\u03c5\u03c4\u03ae \u03b1\u03c0\u03bf\u03c4\u03b5\u03bb\u03b5\u03af \u03c4\u03bf \u03b5\u03bd\u03b9\u03b1\u03af\u03bf \u03c3\u03b7\u03bc\u03b5\u03af\u03bf \u03b5\u03c0\u03b1\u03c6\u03ae\u03c2 \u03bc\u03b1\u03c2 \u03b2\u03ac\u03c3\u03b5\u03b9 \u03c4\u03bf\u03c5 \u03ac\u03c1\u03b8\u03c1\u03bf\u03c5 11 \u03c4\u03b7\u03c2 \u03a0\u03c1\u03ac\u03be\u03b7\u03c2 \u03b3\u03b9\u03b1 \u03c4\u03b9\u03c2 \u03a8\u03b7\u03c6\u03b9\u03b1\u03ba\u03ad\u03c2 \u03a5\u03c0\u03b7\u03c1\u03b5\u03c3\u03af\u03b5\u03c2 (\u039a\u03b1\u03bd\u03bf\u03bd\u03b9\u03c3\u03bc\u03cc\u03c2 (\u0395\u0395) 2022/2065), \u03c0\u03bf\u03c5 \u03b5\u03c6\u03b1\u03c1\u03bc\u03cc\u03b6\u03b5\u03c4\u03b1\u03b9 \u03b1\u03c0\u03cc 17 \u03a6\u03b5\u03b2\u03c1\u03bf\u03c5\u03b1\u03c1\u03af\u03bf\u03c5 2024.",
        "contact_dsa.s2_title": "\u0395\u03bd\u03b9\u03b1\u03af\u03bf \u03c3\u03b7\u03bc\u03b5\u03af\u03bf \u03b5\u03c0\u03b1\u03c6\u03ae\u03c2",
        "contact_dsa.s2_body": "\u038c\u03bb\u03b5\u03c2 \u03bf\u03b9 \u03b5\u03c0\u03b9\u03ba\u03bf\u03b9\u03bd\u03c9\u03bd\u03af\u03b5\u03c2 \u03c3\u03c7\u03b5\u03c4\u03b9\u03ba\u03ac \u03bc\u03b5 \u03c4\u03b7 DSA \u2014 \u03c3\u03c5\u03bc\u03c0\u03b5\u03c1\u03b9\u03bb\u03b1\u03bc\u03b2\u03b1\u03bd\u03bf\u03bc\u03ad\u03bd\u03c9\u03bd \u03b1\u03bd\u03b1\u03c6\u03bf\u03c1\u03ce\u03bd \u03c0\u03b1\u03c1\u03ac\u03bd\u03bf\u03bc\u03bf\u03c5 \u03c0\u03b5\u03c1\u03b9\u03b5\u03c7\u03bf\u03bc\u03ad\u03bd\u03bf\u03c5, \u03b1\u03b9\u03c4\u03b7\u03bc\u03ac\u03c4\u03c9\u03bd \u03b1\u03c1\u03c7\u03ce\u03bd \u03b5\u03c0\u03b9\u03b2\u03bf\u03bb\u03ae\u03c2 \u03bd\u03cc\u03bc\u03bf\u03c5 \u03ba\u03b1\u03b9 \u03b5\u03c1\u03c9\u03c4\u03b7\u03bc\u03ac\u03c4\u03c9\u03bd \u03b1\u03c1\u03c7\u03ce\u03bd \u2014 \u03c0\u03c1\u03ad\u03c0\u03b5\u03b9 \u03bd\u03b1 \u03b1\u03c0\u03b5\u03c5\u03b8\u03cd\u03bd\u03bf\u03bd\u03c4\u03b1\u03b9 \u03c3\u03c4\u03bf:",
        "contact_dsa.s2_email_privacy": "\u0398\u03ad\u03bc\u03b1\u03c4\u03b1 \u03b1\u03c0\u03bf\u03c1\u03c1\u03ae\u03c4\u03bf\u03c5 & GDPR:",
        "contact_dsa.s2_email_legal": "\u0391\u03bd\u03b1\u03c6\u03bf\u03c1\u03ad\u03c2 \u03c0\u03b1\u03c1\u03ac\u03bd\u03bf\u03bc\u03bf\u03c5 \u03c0\u03b5\u03c1\u03b9\u03b5\u03c7\u03bf\u03bc\u03ad\u03bd\u03bf\u03c5 & \u03b1\u03c1\u03c7\u03ad\u03c2:",
    },
    "es": {
        "contact_dsa.page_title": "Punto de contacto DSA",
        "contact_dsa.meta_description": "Punto de contacto para autoridades y usuarios en virtud de la Ley de Servicios Digitales (DSA). Denuncie contenido ilegal o contacte con Nevumo para asuntos relacionados con DSA.",
        "contact_dsa.s1_title": "Acerca de esta p\u00e1gina",
        "contact_dsa.s1_body": "Nevumo es operado por \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), registrada en Sof\u00eda, Bulgaria. Esta p\u00e1gina sirve como nuestro punto \u00fanico de contacto en virtud del art\u00edculo 11 de la Ley de Servicios Digitales (Reglamento (UE) 2022/2065), aplicable desde el 17 de febrero de 2024.",
        "contact_dsa.s2_title": "Punto \u00fanico de contacto",
        "contact_dsa.s2_body": "Todas las comunicaciones relacionadas con la DSA \u2014 incluidos los informes de contenido ilegal, las solicitudes de los organismos de seguridad y las consultas de las autoridades \u2014 deben dirigirse a:",
        "contact_dsa.s2_email_privacy": "Privacidad y RGPD:",
        "contact_dsa.s2_email_legal": "Informes de contenido ilegal y autoridades:",
    },
    "et": {
        "contact_dsa.page_title": "DSA kontaktpunkt",
        "contact_dsa.meta_description": "Kontaktpunkt ametiasutustele ja kasutajatele vastavalt digitaalteenuste seadusele (DSA). Teatage ebaseaduslikust sisust v\u00f5i v\u00f5tke \u00fchendust Nevumoga DSA-ga seotud k\u00fcsimuste.",
        "contact_dsa.s1_title": "Sellest lehest",
        "contact_dsa.s1_body": "Nevumot haldab \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), registreeritud Sofias, Bulgaarias. See leht toimib meie \u00fchtse kontaktpunktina vastavalt digitaalteenuste seaduse (m\u00e4\u00e4rus (EL) 2022/2065) artiklile 11, mis kehtib alates 17. veebruarist 2024.",
        "contact_dsa.s2_title": "\u00dcHtne kontaktpunkt",
        "contact_dsa.s2_body": "Kogu DSA-ga seotud kirjavahetus \u2014 sealhulgas teated ebaseadusliku sisu kohta, \u00f5iguskaitseasutuste taotlused ja ametiasutuste p\u00e4ringud \u2014 tuleks saata aadressile:",
        "contact_dsa.s2_email_privacy": "Privaatsus ja GDPR:",
        "contact_dsa.s2_email_legal": "Ebaseadusliku sisu teatised ja \u00f5iguskaitse:",
    },
    "fi": {
        "contact_dsa.page_title": "DSA-yhteystaho",
        "contact_dsa.meta_description": "Yhteystaho viranomaisille ja k\u00e4ytt\u00e4jille digitaalisia palveluja koskevan s\u00e4\u00e4d\u00f6ksen (DSA) mukaisesti. Ilmoita laittomasta sis\u00e4ll\u00f6st\u00e4 tai ota yhteytt\u00e4 Nevumoon DSA-asioissa.",
        "contact_dsa.s1_title": "Tietoja t\u00e4st\u00e4 sivusta",
        "contact_dsa.s1_body": "Nevumoa yll\u00e4pit\u00e4\u00e4 \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), rekister\u00f6ity Sofiassa, Bulgariassa. T\u00e4m\u00e4 sivu toimii yhteis\u00e4n\u00e4 yhteystahona digitaalisia palveluja koskevan s\u00e4\u00e4d\u00f6ksen (asetus (EU) 2022/2065) 11 artiklan mukaisesti, sovellettavana 17. helmikuuta 2024 alkaen.",
        "contact_dsa.s2_title": "Yhteinen yhteystaho",
        "contact_dsa.s2_body": "Kaikki DSA:han liittyv\u00e4t viestit \u2014 mukaan lukien ilmoitukset laittomasta sis\u00e4ll\u00f6st\u00e4, lainvalvontaviranomaisten pyynn\u00f6t ja viranomaisten tiedustelut \u2014 tulee osoittaa:",
        "contact_dsa.s2_email_privacy": "Tietosuoja ja GDPR:",
        "contact_dsa.s2_email_legal": "Laittoman sis\u00e4ll\u00f6n ilmoitukset ja viranomaiset:",
    },
    "fr": {
        "contact_dsa.page_title": "Point de contact DSA",
        "contact_dsa.meta_description": "Point de contact pour les autorit\u00e9s et les utilisateurs dans le cadre du r\u00e8glement sur les services num\u00e9riques (DSA). Signalez un contenu illicite ou contactez Nevumo pour toute question relative au DSA.",
        "contact_dsa.s1_title": "\u00c0 propos de cette page",
        "contact_dsa.s1_body": "Nevumo est exploit\u00e9 par \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), enregistr\u00e9e \u00e0 Sofia, en Bulgarie. Cette page constitue notre point de contact unique au titre de l\u2019article 11 du r\u00e8glement sur les services num\u00e9riques (r\u00e8glement (UE) 2022/2065), applicable \u00e0 partir du 17 f\u00e9vrier 2024.",
        "contact_dsa.s2_title": "Point de contact unique",
        "contact_dsa.s2_body": "Toutes les communications relatives au DSA \u2014 y compris les signalements de contenus illicites, les demandes des autorit\u00e9s charg\u00e9es de l\u2019application de la loi et les demandes des autorit\u00e9s \u2014 doivent \u00eatre adress\u00e9es \u00e0 :",
        "contact_dsa.s2_email_privacy": "Confidentialit\u00e9 et RGPD :",
        "contact_dsa.s2_email_legal": "Signalements de contenus illicites et autorit\u00e9s :",
    },
    "ga": {
        "contact_dsa.page_title": "Pointe Teagmh\u00e1la DSA",
        "contact_dsa.meta_description": "Pointe teagmh\u00e1la d'\u00fadar\u00e1is agus d'\u00fas\u00e1ideoirí faoin Acht um Sheirbh\u00edsi Digiteacha (DSA). Tuairiscigh \u00e1bhar neamhdhleathach n\u00f3 d\u00e9an teagmh\u00e1il le Nevumo maidir le c\u00farsa\u00ed DSA.",
        "contact_dsa.s1_title": "Maidir leis an Leathanach Seo",
        "contact_dsa.s1_body": "D\u00e9anann \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), cl\u00e1raithe i S\u00f3ifia, an Bh\u00falgair, oibri\u00fa ar Nevumo. Feidhmíonn an leathanach seo mar \u00e1r bpointe aon\u00e1ir teagmh\u00e1la faoi Airteagal 11 den Acht um Sheirbh\u00edsi Digiteacha (Rialach\u00e1n (AE) 2022/2065), infheidhme \u00f3n 17 Feabhra 2024.",
        "contact_dsa.s2_title": "Pointe Aon\u00e1ir Teagmh\u00e1la",
        "contact_dsa.s2_body": "Ba ch\u00f3ir gach cumars\u00e1id a bhaineann le DSA \u2014 lena n-\u00e1ir\u00edtear tuairisc\u00ed ar \u00e1bhar neamhdhleathach, iarratais \u00f3 fhorfheidhmí\u00fa dl\u00ed, agus fios\u00fachain \u00f3 \u00fadar\u00e1is \u2014 a sheoladh chuig:",
        "contact_dsa.s2_email_privacy": "Pr\u00edobh\u00e1ideacht & GDPR:",
        "contact_dsa.s2_email_legal": "Tuairisc\u00ed \u00e1bhair neamhdhleathach & forfheidhmí\u00fa dl\u00ed:",
    },
    "hr": {
        "contact_dsa.page_title": "DSA kontaktna to\u010dka",
        "contact_dsa.meta_description": "Kontaktna to\u010dka za tijela i korisnike u okviru Zakona o digitalnim uslugama (DSA). Prijavite nezakoniti sadr\u017eaj ili kontaktirajte Nevumo u vezi s pitanjima DSA-e.",
        "contact_dsa.s1_title": "O ovoj stranici",
        "contact_dsa.s1_body": "Nevumo upravlja \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), registrirana u Sofiji, Bugarskoj. Ova stranica slu\u017ei kao na\u0161a jedinstvena kontaktna to\u010dka sukladno \u010dlanku 11. Zakona o digitalnim uslugama (Uredba (EU) 2022/2065), primjenjivog od 17. velja\u010de 2024.",
        "contact_dsa.s2_title": "Jedinstvena kontaktna to\u010dka",
        "contact_dsa.s2_body": "Sva komunikacija vezana uz DSA \u2014 uklju\u010duju\u0107i prijave nezakonitog sadr\u017eaja, zahtjeve tijela kaznenog progona i upite nadle\u017enih tijela \u2014 treba biti upu\u0107ena na:",
        "contact_dsa.s2_email_privacy": "Privatnost i GDPR:",
        "contact_dsa.s2_email_legal": "Prijave nezakonitog sadr\u017eaja i tijela kaznenog progona:",
    },
    "hu": {
        "contact_dsa.page_title": "DSA kapcsolattart\u00e1si pont",
        "contact_dsa.meta_description": "Kapcsolattart\u00e1si pont hat\u00f3s\u00e1gok \u00e9s felhaszn\u00e1l\u00f3k sz\u00e1m\u00e1ra a digit\u00e1lis szolg\u00e1ltat\u00e1sokr\u00f3l sz\u00f3l\u00f3 jogszab\u00e1ly (DSA) alapj\u00e1n. Jelentse az ilegit\u00e1lis tartalmakat, vagy l\u00e9pjen kapcsolatba a Nevum\u00f3val DSA-\u00fcgyekben.",
        "contact_dsa.s1_title": "Az oldalr\u00f3l",
        "contact_dsa.s1_body": "A Nevum\u00f3t a \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (\u00dczemelteti: EIK: 175369610) \u00fczemelteti, bejegyezve Sz\u00f3fi\u00e1ban, Bulg\u00e1ri\u00e1ban. Ez az oldal egypontos kapcsolattart\u00e1si pontk\u00e9nt szolg\u00e1l a digit\u00e1lis szolg\u00e1ltat\u00e1sokr\u00f3l sz\u00f3l\u00f3 rendelet (EU) 2022/2065 11. cikke alapj\u00e1n, amely 2024. febru\u00e1r 17-t\u0151l alkalmazand\u00f3.",
        "contact_dsa.s2_title": "Egypontos kapcsolatfelv\u00e9tel",
        "contact_dsa.s2_body": "Minden DSA-val kapcsolatos kommunik\u00e1ci\u00f3 \u2014 bele\u00e9rtve az illegit\u00e1lis tartalmakra vonatkoz\u00f3 bejelent\u00e9seket, a b\u0171n\u00fcldöz\u0151 szervek k\u00e9relmeit \u00e9s a hat\u00f3s\u00e1gi megkeres\u00e9seket \u2014 a k\u00f6vetkező c\u00edmre ir\u00e1ny\u00estand\u00f3:",
        "contact_dsa.s2_email_privacy": "Adatv\u00e9delem \u00e9s GDPR:",
        "contact_dsa.s2_email_legal": "Illegit\u00e1lis tartalom bejelent\u00e9se \u00e9s hat\u00f3s\u00e1gok:",
    },
    "is": {
        "contact_dsa.page_title": "DSA tengilíður",
        "contact_dsa.meta_description": "Tengilíður fyrir yfirvöld og notendur samkvæmt lögum um stafrænar þjónustur (DSA). Tilkynntu um ólöglegt efni eða hafðu samband við Nevumo vegna DSA-mála.",
        "contact_dsa.s1_title": "Um þessa síðu",
        "contact_dsa.s1_body": "Nevumo er rekið af \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), skráð í Sofíu, Búlgaríu. Þessi síða þjónar sem einn tengiliður okkar samkvæmt 11. grein laga um stafrænar þjónustur (reglugerð (ESB) 2022/2065), sem gildir frá 17. febrúar 2024.",
        "contact_dsa.s2_title": "Einn tengiliður",
        "contact_dsa.s2_body": "Öll samskipti tengd DSA \u2014 þar á meðal tilkynningar um ólöglegt efni, beiðnir lögregluyfirvalda og fyrirspurnir yfirvalda \u2014 skulu beint til:",
        "contact_dsa.s2_email_privacy": "Persónuvernd og GDPR:",
        "contact_dsa.s2_email_legal": "Tilkynningar um ólöglegt efni og löggæsla:",
    },
    "it": {
        "contact_dsa.page_title": "Punto di contatto DSA",
        "contact_dsa.meta_description": "Punto di contatto per autorit\u00e0 e utenti ai sensi del Regolamento sui servizi digitali (DSA). Segnala contenuti illegali o contatta Nevumo per questioni relative al DSA.",
        "contact_dsa.s1_title": "Informazioni su questa pagina",
        "contact_dsa.s1_body": "Nevumo \u00e8 gestito da \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), registrata a Sofia, Bulgaria. Questa pagina funge da unico punto di contatto ai sensi dell\u2019articolo 11 del Regolamento sui servizi digitali (Regolamento (UE) 2022/2065), applicabile dal 17 febbraio 2024.",
        "contact_dsa.s2_title": "Punto di contatto unico",
        "contact_dsa.s2_body": "Tutte le comunicazioni relative alla DSA \u2014 incluse le segnalazioni di contenuti illegali, le richieste delle forze dell\u2019ordine e le richieste delle autorit\u00e0 \u2014 devono essere indirizzate a:",
        "contact_dsa.s2_email_privacy": "Privacy e GDPR:",
        "contact_dsa.s2_email_legal": "Segnalazioni di contenuti illegali e autorit\u00e0:",
    },
    "lb": {
        "contact_dsa.page_title": "DSA Kontaktpunkt",
        "contact_dsa.meta_description": "Kontaktpunkt fir Beh\u00f6rden a Benotzer gem\u00e4ss dem Gesetz iwwer digital Servicer (DSA). Mellt illegalen Inhalt oder kontakt\u00e9iert Nevumo a DSA-Froen.",
        "contact_dsa.s1_title": "Iwwer d\u00ebs S\u00e4it",
        "contact_dsa.s1_body": "Nevumo g\u00ebtt vun \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610) bedriwwen, agemaach zu Sofia, Bulgarien. D\u00ebs S\u00e4it d\u00e9ngt als eenzegen Kontaktpunkt gem\u00e4ss Artikel 11 vum Gesetz iwwer digital Servicer (Verordnung (EU) 2022/2065), uwendbar ab 17. Februar 2024.",
        "contact_dsa.s2_title": "Eenzegen Kontaktpunkt",
        "contact_dsa.s2_body": "All DSA-bezunnen Kommunikatiounen \u2014 inklusiv Meldunge vun illegalen Inhalter, Ufroe vu Strofverfolgungsbeh\u00f6rden an Ufroe vun Autorit\u00e9iten \u2014 sollen un follgend Adress gescheckt ginn:",
        "contact_dsa.s2_email_privacy": "Dateschutz & GDPR:",
        "contact_dsa.s2_email_legal": "Meldunge vun illegalen Inhalter & Beh\u00f6rden:",
    },
    "lt": {
        "contact_dsa.page_title": "DSA kontaktinis punktas",
        "contact_dsa.meta_description": "Kontaktinis punktas vald\u017eos institucijoms ir naudotojams pagal Skaitmenini\u0173 paslaug\u0173 akt\u0105 (DSA). Prane\u0161kite apie nete\u0131s\u0117t\u0105 turin\u012f arba susisiekite su Nevumo DSA klausimais.",
        "contact_dsa.s1_title": "Apie \u0161\u012f puslap\u012f",
        "contact_dsa.s1_body": "Nevumo valdo \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), registruota Sofijoje, Bulgarijoje. \u0160is puslapis yra m\u016bs\u0173 vienintelis kontaktinis punktas pagal Skaitmenini\u0173 paslaug\u0173 akto (Reglamento (ES) 2022/2065) 11 straipsn\u012f, taikomu nuo 2024 m. vasario 17 d.",
        "contact_dsa.s2_title": "Vienintelis kontaktinis punktas",
        "contact_dsa.s2_body": "Visa su DSA susijusi komunikacija \u2014 \u012fskaitant prane\u0161imus apie nete\u0131s\u0117t\u0105 turin\u012f, teis\u0117saug\u0173 institucij\u0173 pra\u0161ymus ir vald\u017eos institucij\u0173 u\u017eklausas \u2014 tur\u0117t\u0173 b\u016bti siuniama:",
        "contact_dsa.s2_email_privacy": "Privatumas ir BDAR:",
        "contact_dsa.s2_email_legal": "Prane\u0161imai apie nete\u0131s\u0117t\u0105 turin\u012f ir teis\u0117sauga:",
    },
    "lv": {
        "contact_dsa.page_title": "DSA kontaktpunkts",
        "contact_dsa.meta_description": "Kontaktpunkts iest\u0101d\u0113m un lietot\u0101jiem saska\u0146\u0101 ar Digit\u0101lo pakalpojumu aktu (DSA). Zi\u0146ojiet par nelik\u016bmīgu saturu vai sazinieties ar Nevumo DSA jaut\u0101jumos.",
        "contact_dsa.s1_title": "Par \u0161o lapu",
        "contact_dsa.s1_body": "Nevumo p\u0101rvalda \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), re\u0123istr\u0113ta Sofij\u0101, Bulg\u0101rij\u0101. \u0160\u012b lapa kalpo k\u0101 m\u016bsu vienotais kontaktpunkts saska\u0146\u0101 ar Digit\u0101lo pakalpojumu akta (Regula (ES) 2022/2065) 11. pantu, kas piem\u0113rojams no 2024. gada 17. febru\u0101ra.",
        "contact_dsa.s2_title": "Vienots kontaktpunkts",
        "contact_dsa.s2_body": "Visa ar DSA saist\u012bt\u0101 sazi\u0146a \u2014 tostarp pazi\u0146ojumi par nelik\u016bmīgu saturu, ties\u012bbaizsardz\u012bbas iest\u0101\u017eu piepras\u012bjumi un iest\u0101\u017eu jaut\u0101jumi \u2014 j\u0101s\u016bta uz:",
        "contact_dsa.s2_email_privacy": "Priv\u0101tums un GDPR:",
        "contact_dsa.s2_email_legal": "Nelik\u016bmīga satura zi\u0146ojumi un iest\u0101des:",
    },
    "mk": {
        "contact_dsa.page_title": "DSA \u043a\u043e\u043d\u0442\u0430\u043a\u0442\u043d\u0430 \u0442\u043e\u0447\u043a\u0430",
        "contact_dsa.meta_description": "\u041a\u043e\u043d\u0442\u0430\u043a\u0442\u043d\u0430 \u0442\u043e\u0447\u043a\u0430 \u0437\u0430 \u043e\u0440\u0433\u0430\u043d\u0438 \u0438 \u043a\u043e\u0440\u0438\u0441\u043d\u0438\u0446\u0438 \u0432\u043e \u0440\u0430\u043c\u043a\u0438 \u043d\u0430 \u0417\u0430\u043a\u043e\u043d\u043e\u0442 \u0437\u0430 \u0434\u0438\u0433\u0438\u0442\u0430\u043b\u043d\u0438 \u0443\u0441\u043b\u0443\u0433\u0438 (DSA). \u041f\u0440\u0438\u0458\u0430\u0432\u0435\u0442\u0435 \u043d\u0435\u0437\u0430\u043a\u043e\u043d\u0438\u0442\u0430 \u0441\u043e\u0434\u0440\u0436\u0438\u043d\u0430 \u0438\u043b\u0438 \u043a\u043e\u043d\u0442\u0430\u043a\u0442\u0438\u0440\u0430\u0458\u0442\u0435 \u0433\u043e Nevumo \u0437\u0430 \u043f\u0440\u0430\u0448\u0430\u045a\u0430 \u043f\u043e\u0432\u0440\u0437\u0430\u043d\u0438 \u0441\u043e DSA.",
        "contact_dsa.s1_title": "\u0417\u0430 \u043e\u0432\u0430\u0430 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430",
        "contact_dsa.s1_body": "Nevumo \u0433\u043e \u0443\u043f\u0440\u0430\u0432\u0443\u0432\u0430 \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0438\u0440\u0430\u043d\u043e \u0432\u043e \u0421\u043e\u0444\u0438\u0458\u0430, \u0411\u0443\u0433\u0430\u0440\u0438\u0458\u0430. \u041e\u0432\u0430\u0430 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 \u0441\u043b\u0443\u0436\u0438 \u043a\u0430\u043a\u043e \u043d\u0430\u0448\u0430 \u0435\u0434\u0438\u043d\u0441\u0442\u0432\u0435\u043d\u0430 \u043a\u043e\u043d\u0442\u0430\u043a\u0442\u043d\u0430 \u0442\u043e\u0447\u043a\u0430 \u0441\u043e\u0433\u043b\u0430\u0441\u043d\u043e \u0447\u043b. 11 \u043e\u0434 \u0417\u0430\u043a\u043e\u043d\u043e\u0442 \u0437\u0430 \u0434\u0438\u0433\u0438\u0442\u0430\u043b\u043d\u0438 \u0443\u0441\u043b\u0443\u0433\u0438 (\u0420\u0435\u0433\u0443\u043b\u0430\u0442\u0438\u0432\u0430 (\u0415\u0423) 2022/2065), \u043f\u0440\u0438\u043c\u0435\u043d\u043b\u0438\u0432\u0430 \u043e\u0434 17 \u0444\u0435\u0432\u0440\u0443\u0430\u0440\u0438 2024 \u0433.",
        "contact_dsa.s2_title": "\u0415\u0434\u0438\u043d\u0441\u0442\u0432\u0435\u043d\u0430 \u043a\u043e\u043d\u0442\u0430\u043a\u0442\u043d\u0430 \u0442\u043e\u0447\u043a\u0430",
        "contact_dsa.s2_body": "\u0421\u0438\u0442\u0435 \u043a\u043e\u043c\u0443\u043d\u0438\u043a\u0430\u0446\u0438\u0438 \u043f\u043e\u0432\u0440\u0437\u0430\u043d\u0438 \u0441\u043e DSA \u2014 \u0432\u043a\u043b\u0443\u0447\u0443\u0432\u0430\u0458\u045c\u0438 \u043f\u0440\u0438\u0458\u0430\u0432\u0438 \u0437\u0430 \u043d\u0435\u0437\u0430\u043a\u043e\u043d\u0438\u0442\u0430 \u0441\u043e\u0434\u0440\u0436\u0438\u043d\u0430, \u0431\u0430\u0440\u0430\u045a\u0430 \u043e\u0434 \u043e\u0440\u0433\u0430\u043d\u0438 \u0437\u0430 \u0441\u043f\u0440\u043e\u0432\u0435\u0434\u0443\u0432\u0430\u045a\u0435 \u043d\u0430 \u0437\u0430\u043a\u043e\u043d\u043e\u0442 \u0438 \u043f\u0440\u0430\u0448\u0430\u045a\u0430 \u043e\u0434 \u043d\u0430\u0434\u043b\u0435\u0436\u043d\u0438 \u043e\u0440\u0433\u0430\u043d\u0438 \u2014 \u0442\u0440\u0435\u0431\u0430 \u0434\u0430 \u0441\u0435 \u0443\u043f\u0430\u0442\u0443\u0432\u0430\u0430\u0442 \u043d\u0430:",
        "contact_dsa.s2_email_privacy": "\u041f\u0440\u0438\u0432\u0430\u0442\u043d\u043e\u0441\u0442 \u0438 GDPR:",
        "contact_dsa.s2_email_legal": "\u041f\u0440\u0438\u0458\u0430\u0432\u0438 \u0437\u0430 \u043d\u0435\u0437\u0430\u043a\u043e\u043d\u0438\u0442\u0430 \u0441\u043e\u0434\u0440\u0436\u0438\u043d\u0430 \u0438 \u043e\u0440\u0433\u0430\u043d\u0438:",
    },
    "mt": {
        "contact_dsa.page_title": "Punt ta\u2019 kuntatt DSA",
        "contact_dsa.meta_description": "Punt ta\u2019 kuntatt g\u0127al awtoritajiet u utenti skont l-Att dwar is-Servizzi Di\u0121itali (DSA). Irrapporta kontenut illegali jew ikkuntattja lil Nevumo g\u0127al kw\u0131stjonijet relatati mad-DSA.",
        "contact_dsa.s1_title": "Dwar din il-Pa\u0121na",
        "contact_dsa.s1_body": "Nevumo huwa operat minn \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), irre\u0121istrata f\u2019Sofija, il-Bulgarija. Din il-pa\u0121na sservi b\u0127ala l-punt ta\u2019 kuntatt uniku tag\u0127na skont l-Artikolu 11 tal-Att dwar is-Servizzi Di\u0121itali (Regolament (UE) 2022/2065), applikabbli mill-17 ta\u2019 Frar 2024.",
        "contact_dsa.s2_title": "Punt ta\u2019 kuntatt uniku",
        "contact_dsa.s2_body": "Il-komunikazzjonijiet kollha relatati mad-DSA \u2014 inklużi rapporti dwar kontenut illegali, talbiet mill-awtoritajiet tal-infurzar tal-li\u0121i, u mistoqsijiet mill-awtoritajiet \u2014 g\u0127andhom ji\u0121u indirizzati lil:",
        "contact_dsa.s2_email_privacy": "Privatezza u GDPR:",
        "contact_dsa.s2_email_legal": "Rapporti ta\u2019 kontenut illegali u awtoritajiet:",
    },
    "nl": {
        "contact_dsa.page_title": "DSA-contactpunt",
        "contact_dsa.meta_description": "Contactpunt voor autoriteiten en gebruikers op grond van de wet inzake digitale diensten (DSA). Meld illegale inhoud of neem contact op met Nevumo voor DSA-gerelateerde zaken.",
        "contact_dsa.s1_title": "Over deze pagina",
        "contact_dsa.s1_body": "Nevumo wordt ge\u00ebxploiteerd door \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), geregistreerd in Sofia, Belgi\u00eb. Deze pagina dient als ons enkel contactpunt op grond van artikel 11 van de wet inzake digitale diensten (Verordening (EU) 2022/2065), van toepassing vanaf 17 februari 2024.",
        "contact_dsa.s2_title": "Enkel contactpunt",
        "contact_dsa.s2_body": "Alle DSA-gerelateerde communicatie \u2014 inclusief meldingen van illegale inhoud, verzoeken van rechtshandhavingsinstanties en vragen van autoriteiten \u2014 dient te worden gericht aan:",
        "contact_dsa.s2_email_privacy": "Privacy & AVG:",
        "contact_dsa.s2_email_legal": "Meldingen illegale inhoud en autoriteiten:",
    },
    "no": {
        "contact_dsa.page_title": "DSA-kontaktpunkt",
        "contact_dsa.meta_description": "Kontaktpunkt for myndigheter og brukere i henhold til lov om digitale tjenester (DSA). Rapporter ulovlig innhold eller kontakt Nevumo i DSA-relaterte saker.",
        "contact_dsa.s1_title": "Om denne siden",
        "contact_dsa.s1_body": "Nevumo drives av \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), registrert i Sofia, Bulgaria. Denne siden fungerer som v\u00e5rt enkelt kontaktpunkt i henhold til artikkel 11 i lov om digitale tjenester (forordning (EU) 2022/2065), gjeldende fra 17. februar 2024.",
        "contact_dsa.s2_title": "Enkelt kontaktpunkt",
        "contact_dsa.s2_body": "All DSA-relatert kommunikasjon \u2014 inkludert rapporter om ulovlig innhold, foresp\u00f8rsler fra rettsh\u00e5ndhevende myndigheter og henvendelser fra myndigheter \u2014 skal rettes til:",
        "contact_dsa.s2_email_privacy": "Personvern og GDPR:",
        "contact_dsa.s2_email_legal": "Rapporter om ulovlig innhold og myndigheter:",
    },
    "pl": {
        "contact_dsa.page_title": "Punkt kontaktowy DSA",
        "contact_dsa.meta_description": "Punkt kontaktowy dla organ\u00f3w i u\u017cytkownik\u00f3w zgodnie z Aktem o us\u0142ugach cyfrowych (DSA). Zg\u0142o\u015b nielegalne tre\u015bci lub skontaktuj si\u0119 z Nevumo w sprawach DSA.",
        "contact_dsa.s1_title": "O tej stronie",
        "contact_dsa.s1_body": "Nevumo jest obs\u0142ugiwane przez \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), zarejestrowan\u0105 w Sofii, w Bu\u0142garii. Niniejsza strona stanowi nasz pojedynczy punkt kontaktowy zgodnie z art. 11 Aktu o us\u0142ugach cyfrowych (Rozporz\u0105dzenie (UE) 2022/2065), stosowanego od 17 lutego 2024 r.",
        "contact_dsa.s2_title": "Pojedynczy punkt kontaktowy",
        "contact_dsa.s2_body": "Wszelka komunikacja zwi\u0105zana z DSA \u2014 w tym zg\u0142oszenia nielegalnych tre\u015bci, wnioski organ\u00f3w \u015bcigania oraz zapytania w\u0142a\u015bciwych organ\u00f3w \u2014 powinna by\u0107 kierowana na adres:",
        "contact_dsa.s2_email_privacy": "Prywatno\u015b\u0107 i RODO:",
        "contact_dsa.s2_email_legal": "Zg\u0142oszenia nielegalnych tre\u015bci i organy \u015bcigania:",
    },
    "pt": {
        "contact_dsa.page_title": "Ponto de Contato DSA",
        "contact_dsa.meta_description": "Ponto de contato para autoridades e usu\u00e1rios ao abrigo da Lei dos Servi\u00e7os Digitais (DSA). Den\u00fancie conte\u00fado ilegal ou contacte a Nevumo para assuntos relacionados com o DSA.",
        "contact_dsa.s1_title": "Sobre Esta P\u00e1gina",
        "contact_dsa.s1_body": "A Nevumo \u00e9 operada pela \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), registada em S\u00f3fia, Bulg\u00e1ria. Esta p\u00e1gina serve como nosso ponto \u00fanico de contacto ao abrigo do artigo 11.\u00ba da Lei dos Servi\u00e7os Digitais (Regulamento (UE) 2022/2065), aplic\u00e1vel a partir de 17 de fevereiro de 2024.",
        "contact_dsa.s2_title": "Ponto \u00danico de Contato",
        "contact_dsa.s2_body": "Todas as comunica\u00e7\u00f5es relacionadas com o DSA \u2014 incluindo relat\u00f3rios de conte\u00fado ilegal, pedidos de autoridades policiais e consultas de autoridades \u2014 devem ser dirigidas a:",
        "contact_dsa.s2_email_privacy": "Privacidade e GDPR:",
        "contact_dsa.s2_email_legal": "Relat\u00f3rios de conte\u00fado ilegal e autoridades:",
    },
    "pt_PT": {
        "contact_dsa.page_title": "Ponto de Contacto DSA",
        "contact_dsa.meta_description": "Ponto de contacto para autoridades e utilizadores ao abrigo da Lei dos Servi\u00e7os Digitais (DSA). Den\u00fancie conte\u00fado ilegal ou contacte a Nevumo para assuntos relacionados com o DSA.",
        "contact_dsa.s1_title": "Sobre Esta P\u00e1gina",
        "contact_dsa.s1_body": "A Nevumo \u00e9 operada pela \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), registada em S\u00f3fia, Bulg\u00e1ria. Esta p\u00e1gina serve como nosso ponto \u00fanico de contacto ao abrigo do artigo 11.\u00ba da Lei dos Servi\u00e7os Digitais (Regulamento (UE) 2022/2065), aplic\u00e1vel a partir de 17 de fevereiro de 2024.",
        "contact_dsa.s2_title": "Ponto \u00danico de Contacto",
        "contact_dsa.s2_body": "Todas as comunica\u00e7\u00f5es relacionadas com o DSA \u2014 incluindo relat\u00f3rios de conte\u00fado ilegal, pedidos de autoridades policiais e consultas de autoridades \u2014 devem ser dirigidas a:",
        "contact_dsa.s2_email_privacy": "Privacidade e RGPD:",
        "contact_dsa.s2_email_legal": "Relat\u00f3rios de conte\u00fado ilegal e autoridades:",
    },
    "ro": {
        "contact_dsa.page_title": "Punct de contact DSA",
        "contact_dsa.meta_description": "Punct de contact pentru autorit\u0103\u021bi \u015fi utilizatori \u00een temeiul Legii privind serviciile digitale (DSA). Raporta\u021bi con\u021binut ilegal sau contacta\u021bi Nevumo pentru aspecte legate de DSA.",
        "contact_dsa.s1_title": "Despre aceast\u0103 pagin\u0103",
        "contact_dsa.s1_body": "Nevumo este operat de \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), \u00eenregistrat\u0103 \u00een Sofia, Bulgaria. Aceast\u0103 pagin\u0103 serve\u015fte drept punct unic de contact \u00een temeiul articolului 11 din Legea privind serviciile digitale (Regulamentul (UE) 2022/2065), aplicabil de la 17 februarie 2024.",
        "contact_dsa.s2_title": "Punct unic de contact",
        "contact_dsa.s2_body": "Toate comunic\u0103rile legate de DSA \u2014 inclusiv raport\u0103rile de con\u021binut ilegal, solicit\u0103rile autorit\u0103\u021bilor de aplicare a legii \u015fi \u00eentreb\u0103rile autorit\u0103\u021bilor \u2014 trebuie adresate la:",
        "contact_dsa.s2_email_privacy": "Confiden\u021bialitate \u015fi GDPR:",
        "contact_dsa.s2_email_legal": "Raport\u0103ri de con\u021binut ilegal \u015fi autorit\u0103\u021bi:",
    },
    "ru": {
        "contact_dsa.page_title": "\u041a\u043e\u043d\u0442\u0430\u043a\u0442\u043d\u0430\u044f \u0442\u043e\u0447\u043a\u0430 DSA",
        "contact_dsa.meta_description": "\u041a\u043e\u043d\u0442\u0430\u043a\u0442\u043d\u0430\u044f \u0442\u043e\u0447\u043a\u0430 \u0434\u043b\u044f \u043e\u0440\u0433\u0430\u043d\u043e\u0432 \u0432\u043b\u0430\u0441\u0442\u0438 \u0438 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439 \u0432 \u0441\u043e\u043e\u0442\u0432\u0435\u0442\u0441\u0442\u0432\u0438\u0438 \u0441 \u0417\u0430\u043a\u043e\u043d\u043e\u043c \u043e \u0446\u0438\u0444\u0440\u043e\u0432\u044b\u0445 \u0443\u0441\u043b\u0443\u0433\u0430\u0445 (DSA). \u0421\u043e\u043e\u0431\u0449\u0430\u0439\u0442\u0435 \u043e \u043d\u0435\u0437\u0430\u043a\u043e\u043d\u043d\u043e\u043c \u043a\u043e\u043d\u0442\u0435\u043d\u0442\u0435 \u0438\u043b\u0438 \u043e\u0431\u0440\u0430\u0449\u0430\u0439\u0442\u0435\u0441\u044c \u0432 Nevumo \u043f\u043e \u0432\u043e\u043f\u0440\u043e\u0441\u0430\u043c DSA.",
        "contact_dsa.s1_title": "\u041e\u0431 \u044d\u0442\u043e\u0439 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0435",
        "contact_dsa.s1_body": "Nevumo \u0443\u043f\u0440\u0430\u0432\u043b\u044f\u0435\u0442\u0441\u044f \u043a\u043e\u043c\u043f\u0430\u043d\u0438\u0435\u0439 \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), \u0437\u0430\u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u043e\u0439 \u0432 \u0421\u043e\u0444\u0438\u0438, \u0411\u043e\u043b\u0433\u0430\u0440\u0438\u044f. \u0414\u0430\u043d\u043d\u0430\u044f \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430 \u0441\u043b\u0443\u0436\u0438\u0442 \u0435\u0434\u0438\u043d\u043e\u0439 \u043a\u043e\u043d\u0442\u0430\u043a\u0442\u043d\u043e\u0439 \u0442\u043e\u0447\u043a\u043e\u0439 \u0432 \u0441\u043e\u043e\u0442\u0432\u0435\u0442\u0441\u0442\u0432\u0438\u0438 \u0441\u043e \u0441\u0442\u0430\u0442\u044c\u0451\u0439 11 \u0417\u0430\u043a\u043e\u043d\u0430 \u043e \u0446\u0438\u0444\u0440\u043e\u0432\u044b\u0445 \u0443\u0441\u043b\u0443\u0433\u0430\u0445 (\u0420\u0435\u0433\u043b\u0430\u043c\u0435\u043d\u0442 (\u0415\u0421) 2022/2065), \u043f\u0440\u0438\u043c\u0435\u043d\u0438\u043c\u043e\u0433\u043e \u0441 17 \u0444\u0435\u0432\u0440\u0430\u043b\u044f 2024 \u0433\u043e\u0434\u0430.",
        "contact_dsa.s2_title": "\u0415\u0434\u0438\u043d\u0430\u044f \u043a\u043e\u043d\u0442\u0430\u043a\u0442\u043d\u0430\u044f \u0442\u043e\u0447\u043a\u0430",
        "contact_dsa.s2_body": "\u0412\u0441\u0435 \u043a\u043e\u043c\u043c\u0443\u043d\u0438\u043a\u0430\u0446\u0438\u0438, \u0441\u0432\u044f\u0437\u0430\u043d\u043d\u044b\u0435 \u0441 DSA, \u2014 \u0432\u043a\u043b\u044e\u0447\u0430\u044f \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u044f \u043e \u043d\u0435\u0437\u0430\u043a\u043e\u043d\u043d\u043e\u043c \u043a\u043e\u043d\u0442\u0435\u043d\u0442\u0435, \u0437\u0430\u043f\u0440\u043e\u0441\u044b \u043f\u0440\u0430\u0432\u043e\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0445 \u043e\u0440\u0433\u0430\u043d\u043e\u0432 \u0438 \u043e\u0431\u0440\u0430\u0449\u0435\u043d\u0438\u044f \u0432\u043b\u0430\u0441\u0442\u0435\u0439 \u2014 \u0441\u043b\u0435\u0434\u0443\u0435\u0442 \u043d\u0430\u043f\u0440\u0430\u0432\u043b\u044f\u0442\u044c \u043f\u043e \u0430\u0434\u0440\u0435\u0441\u0443:",
        "contact_dsa.s2_email_privacy": "\u041a\u043e\u043d\u0444\u0438\u0434\u0435\u043d\u0446\u0438\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u044c \u0438 GDPR:",
        "contact_dsa.s2_email_legal": "\u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u044f \u043e \u043d\u0435\u0437\u0430\u043a\u043e\u043d\u043d\u043e\u043c \u043a\u043e\u043d\u0442\u0435\u043d\u0442\u0435 \u0438 \u043e\u0440\u0433\u0430\u043d\u044b:",
    },
    "sk": {
        "contact_dsa.page_title": "Kontaktn\u00e9 miesto DSA",
        "contact_dsa.meta_description": "Kontaktn\u00e9 miesto pre org\u00e1ny a pou\u017e\u00edvate\u013eov v r\u00e1mci z\u00e1kona o digit\u00e1lnych slu\u017eb\u00e1ch (DSA). Nahlaste nez\u00e1konn\u00fd obsah alebo kontaktujte Nevumo v z\u00e1le\u017eitostiach DSA.",
        "contact_dsa.s1_title": "O tejto str\u00e1nke",
        "contact_dsa.s1_body": "Nevumo prev\u00e1dzkuje \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), registrovan\u00e1 v Sofii v Bulharsku. T\u00e1to str\u00e1nka sl\u00fa\u017ei ako na\u0161e jedin\u00e9 kontaktn\u00e9 miesto pod\u013ea \u010dl\u00e1nku 11 z\u00e1kona o digit\u00e1lnych slu\u017eb\u00e1ch (nariadenie (E\u00da) 2022/2065), platn\u00e9ho od 17. febru\u00e1ra 2024.",
        "contact_dsa.s2_title": "Jedin\u00e9 kontaktn\u00e9 miesto",
        "contact_dsa.s2_body": "V\u0161etka komunik\u00e1cia t\u00fdkaj\u00faca sa DSA \u2014 vr\u00e1tane hl\u00e1sen\u00ed nez\u00e1konn\u00e9ho obsahu, \u017eiadost\u00ed org\u00e1nov \u010dinn\u00fdch v trestnom konan\u00ed a dopytov pr\u00edlu\u0161n\u00fdch org\u00e1nov \u2014 by mala by\u0165 zasielan\u00e1 na:",
        "contact_dsa.s2_email_privacy": "Ochrana s\u00fakromia a GDPR:",
        "contact_dsa.s2_email_legal": "Hl\u00e1senia nez\u00e1konn\u00e9ho obsahu a org\u00e1ny:",
    },
    "sl": {
        "contact_dsa.page_title": "Kontaktna to\u010dka DSA",
        "contact_dsa.meta_description": "Kontaktna to\u010dka za organe in uporabnike v okviru Zakona o digitalnih storitvah (DSA). Prijavite nezakonito vsebino ali stopite v stik z Nevumo v zadevah DSA.",
        "contact_dsa.s1_title": "O tej strani",
        "contact_dsa.s1_body": "Nevumo upravlja \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), registrirana v Sofiji, Bolgarija. Ta stran slu\u017ei kot na\u0161a enotna kontaktna to\u010dka v skladu s \u010dlenom 11 Zakona o digitalnih storitvah (Uredba (EU) 2022/2065), ki se uporablja od 17. februarja 2024.",
        "contact_dsa.s2_title": "Enotna kontaktna to\u010dka",
        "contact_dsa.s2_body": "Vsa komunikacija v zvezi z DSA \u2014 vklju\u010dno s prijavami nezakonite vsebine, zahtevami organov pregona in poizvedbami pristojnih organov \u2014 naj bo naslovljena na:",
        "contact_dsa.s2_email_privacy": "Zasebnost in GDPR:",
        "contact_dsa.s2_email_legal": "Prijave nezakonite vsebine in organi:",
    },
    "sq": {
        "contact_dsa.page_title": "Pika e kontaktit DSA",
        "contact_dsa.meta_description": "Pik\u00eb kontakti p\u00ebr autoritetet dhe p\u00ebrdoruesit sipas Aktit t\u00eb Shp\u00ebrbimeve Dixhitale (DSA). Raportoni p\u00ebrmbajte ilegale ose kontaktoni Nevumo p\u00ebr \u00e7\u00ebshtje t\u00eb lidhura me DSA.",
        "contact_dsa.s1_title": "Rreth k\u00ebsaj faqeje",
        "contact_dsa.s1_body": "Nevumo operohet nga \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), e regjistruar n\u00eb Sofje, Bullgari. Kjo faqe sh\u00ebrben si pika jon\u00eb e vet\u00ebm e kontaktit sipas nenit 11 t\u00eb Aktit t\u00eb Shp\u00ebrbimeve Dixhitale (Rregullore (BE) 2022/2065), e zbatueshme nga 17 shkurti 2024.",
        "contact_dsa.s2_title": "Pika e vet\u00ebm e kontaktit",
        "contact_dsa.s2_body": "T\u00eb gjitha komunikimet e lidhura me DSA \u2014 duke p\u00ebrfshir\u00eb raportet e p\u00ebrmbajtes ilegale, k\u00ebrkesat e zbatimit t\u00eb ligjit dhe pyetjet e autoriteteve \u2014 duhet t\u2019i drejtohen:",
        "contact_dsa.s2_email_privacy": "Privat\u00ebsia dhe GDPR:",
        "contact_dsa.s2_email_legal": "Raportet e p\u00ebrmbajtes ilegale dhe autoritetet:",
    },
    "sr": {
        "contact_dsa.page_title": "DSA kontaktna ta\u010dka",
        "contact_dsa.meta_description": "Kontaktna ta\u010dka za organe i korisnike u okviru Zakona o digitalnim uslugama (DSA). Prijavite nezakoniti sadr\u017eaj ili kontaktirajte Nevumo u vezi s pitanjima DSA.",
        "contact_dsa.s1_title": "O ovoj stranici",
        "contact_dsa.s1_body": "Nevumo upravlja \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), registrovana u Sofiji, Bugarskoj. Ova stranica slu\u017ei kao na\u0161a jedinstvena kontaktna ta\u010dka u skladu sa \u010dlanom 11 Zakona o digitalnim uslugama (Uredba (EU) 2022/2065), primenjivog od 17. februara 2024.",
        "contact_dsa.s2_title": "Jedinstvena kontaktna ta\u010dka",
        "contact_dsa.s2_body": "Sva komunikacija vezana za DSA \u2014 uklju\u010duju\u0107i prijave nezakonitog sadr\u017eaja, zahteve organa za sprovo\u0111enje zakona i upite nadle\u017enih organa \u2014 treba biti upu\u0107ena na:",
        "contact_dsa.s2_email_privacy": "Privatnost i GDPR:",
        "contact_dsa.s2_email_legal": "Prijave nezakonitog sadr\u017eaja i organi:",
    },
    "sv": {
        "contact_dsa.page_title": "DSA-kontaktpunkt",
        "contact_dsa.meta_description": "Kontaktpunkt f\u00f6r myndigheter och anv\u00e4ndare enligt lagen om digitala tj\u00e4nster (DSA). Rapportera olagligt inneh\u00e5ll eller kontakta Nevumo i DSA-relaterade \u00e4renden.",
        "contact_dsa.s1_title": "Om den h\u00e4r sidan",
        "contact_dsa.s1_body": "Nevumo drivs av \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), registrerat i Sofia, Bulgarien. Denna sida fungerar som v\u00e5r enda kontaktpunkt enligt artikel 11 i lagen om digitala tj\u00e4nster (f\u00f6rordning (EU) 2022/2065), till\u00e4mplig fr\u00e5n och med den 17 februari 2024.",
        "contact_dsa.s2_title": "Enda kontaktpunkt",
        "contact_dsa.s2_body": "All DSA-relaterad kommunikation \u2014 inklusive rapporter om olagligt inneh\u00e5ll, f\u00f6rfr\u00e5gningar fr\u00e5n brottsbek\u00e4mpande myndigheter och myndighetsf\u00f6rfr\u00e5gningar \u2014 ska riktas till:",
        "contact_dsa.s2_email_privacy": "Integritet och GDPR:",
        "contact_dsa.s2_email_legal": "Rapporter om olagligt inneh\u00e5ll och myndigheter:",
    },
    "tr": {
        "contact_dsa.page_title": "DSA \u0130leti\u015fim Noktas\u0131",
        "contact_dsa.meta_description": "Dijital Hizmetler Yasas\u0131 (DSA) kapsam\u0131nda yetkililer ve kullan\u0131c\u0131lar i\u00e7in ileti\u015fim noktas\u0131. Yasad\u0131\u015f\u0131 i\u00e7eri\u011fi bildirin veya DSA ile ilgili konular i\u00e7in Nevumo ile ileti\u015fime ge\u00e7in.",
        "contact_dsa.s1_title": "Bu Sayfa Hakk\u0131nda",
        "contact_dsa.s1_body": "Nevumo, Sofya, Bulgaristan\u2019da kay\u0131tl\u0131 \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610) taraf\u0131ndan i\u015fletilmektedir. Bu sayfa, 17 \u015eubat 2024\u2019ten itibaren ge\u00e7erli olan Dijital Hizmetler Yasas\u0131\u2019n\u0131n (AB Y\u00f6netmeli\u011fi 2022/2065) 11. maddesi kapsam\u0131nda tek ileti\u015fim noktas\u0131m\u0131z olarak hizmet vermektedir.",
        "contact_dsa.s2_title": "Tek \u0130leti\u015fim Noktas\u0131",
        "contact_dsa.s2_body": "DSA ile ilgili t\u00fcm ileti\u015fimler \u2014 yasad\u0131\u015f\u0131 i\u00e7erik raporlar\u0131, kolluk kuvvetleri talepleri ve yetkili makam soru\u015fturmalar\u0131 dahil \u2014 a\u015fa\u011f\u0131daki adrese y\u00f6nlendirilmelidir:",
        "contact_dsa.s2_email_privacy": "Gizlilik ve GDPR:",
        "contact_dsa.s2_email_legal": "Yasad\u0131\u015f\u0131 i\u00e7erik bildirimleri ve yetkililer:",
    },
    "uk": {
        "contact_dsa.page_title": "\u041a\u043e\u043d\u0442\u0430\u043a\u0442\u043d\u0430 \u0442\u043e\u0447\u043a\u0430 DSA",
        "contact_dsa.meta_description": "\u041a\u043e\u043d\u0442\u0430\u043a\u0442\u043d\u0430 \u0442\u043e\u0447\u043a\u0430 \u0434\u043b\u044f \u043e\u0440\u0433\u0430\u043d\u0456\u0432 \u0432\u043b\u0430\u0434\u0438 \u0442\u0430 \u043a\u043e\u0440\u0438\u0441\u0442\u0443\u0432\u0430\u0447\u0456\u0432 \u0432\u0456\u0434\u043f\u043e\u0432\u0456\u0434\u043d\u043e \u0434\u043e \u0417\u0430\u043a\u043e\u043d\u0443 \u043f\u0440\u043e \u0446\u0438\u0444\u0440\u043e\u0432\u0456 \u043f\u043e\u0441\u043b\u0443\u0433\u0438 (DSA). \u041f\u043e\u0432\u0456\u0434\u043e\u043c\u043b\u044f\u0439\u0442\u0435 \u043f\u0440\u043e \u043d\u0435\u0437\u0430\u043a\u043e\u043d\u043d\u0438\u0439 \u0432\u043c\u0456\u0441\u0442 \u0430\u0431\u043e \u0437\u0432\u0435\u0440\u0442\u0430\u0439\u0442\u0435\u0441\u044f \u0434\u043e Nevumo \u0437 \u043f\u0438\u0442\u0430\u043d\u044c DSA.",
        "contact_dsa.s1_title": "\u041f\u0440\u043e \u0446\u044e \u0441\u0442\u043e\u0440\u0456\u043d\u043a\u0443",
        "contact_dsa.s1_body": "Nevumo \u0443\u043f\u0440\u0430\u0432\u043b\u044f\u0454\u0442\u044c\u0441\u044f \u043a\u043e\u043c\u043f\u0430\u043d\u0456\u0454\u044e \u201e\u0424\u0418\u041b\u0418\u041f\u0421 \u0426\u0415\u041d\u0422\u042c\u0420 \u0411\u042a\u041b\u0413\u0410\u0420\u0418\u042f\u201c \u041e\u041e\u0414 (EIK: 175369610), \u0437\u0430\u0440\u0435\u0454\u0441\u0442\u0440\u043e\u0432\u0430\u043d\u043e\u044e \u0432 \u0421\u043e\u0444\u0456\u0457, \u0411\u043e\u043b\u0433\u0430\u0440\u0456\u044f. \u0426\u044f \u0441\u0442\u043e\u0440\u0456\u043d\u043a\u0430 \u0441\u043b\u0443\u0433\u0443\u0454 \u0454\u0434\u0438\u043d\u043e\u044e \u043a\u043e\u043d\u0442\u0430\u043a\u0442\u043d\u043e\u044e \u0442\u043e\u0447\u043a\u043e\u044e \u0432\u0456\u0434\u043f\u043e\u0432\u0456\u0434\u043d\u043e \u0434\u043e \u0441\u0442\u0430\u0442\u0442\u0456 11 \u0417\u0430\u043a\u043e\u043d\u0443 \u043f\u0440\u043e \u0446\u0438\u0444\u0440\u043e\u0432\u0456 \u043f\u043e\u0441\u043b\u0443\u0433\u0438 (\u0420\u0435\u0433\u043b\u0430\u043c\u0435\u043d\u0442 (\u0404\u0421) 2022/2065), \u0449\u043e \u0437\u0430\u0441\u0442\u043e\u0441\u043e\u0432\u0443\u0454\u0442\u044c\u0441\u044f \u0437 17 \u043b\u044e\u0442\u043e\u0433\u043e 2024 \u0440\u043e\u043a\u0443.",
        "contact_dsa.s2_title": "\u0404\u0434\u0438\u043d\u0430 \u043a\u043e\u043d\u0442\u0430\u043a\u0442\u043d\u0430 \u0442\u043e\u0447\u043a\u0430",
        "contact_dsa.s2_body": "\u0412\u0441\u0456 \u043a\u043e\u043c\u0443\u043d\u0456\u043a\u0430\u0446\u0456\u0457, \u043f\u043e\u0432\u2019\u044f\u0437\u0430\u043d\u0456 \u0437 DSA, \u2014 \u0432\u043a\u043b\u044e\u0447\u0430\u044e\u0447\u0438 \u043f\u043e\u0432\u0456\u0434\u043e\u043c\u043b\u0435\u043d\u043d\u044f \u043f\u0440\u043e \u043d\u0435\u0437\u0430\u043a\u043e\u043d\u043d\u0438\u0439 \u0432\u043c\u0456\u0441\u0442, \u0437\u0430\u043f\u0438\u0442\u0438 \u043f\u0440\u0430\u0432\u043e\u043e\u0445\u043e\u0440\u043e\u043d\u043d\u0438\u0445 \u043e\u0440\u0433\u0430\u043d\u0456\u0432 \u0442\u0430 \u0437\u0432\u0435\u0440\u043d\u0435\u043d\u043d\u044f \u043e\u0440\u0433\u0430\u043d\u0456\u0432 \u0432\u043b\u0430\u0434\u0438 \u2014 \u0441\u043b\u0456\u0434 \u043d\u0430\u0434\u0441\u0438\u043b\u0430\u0442\u0438 \u043d\u0430:",
        "contact_dsa.s2_email_privacy": "\u041a\u043e\u043d\u0444\u0456\u0434\u0435\u043d\u0446\u0456\u0439\u043d\u0456\u0441\u0442\u044c \u0456 GDPR:",
        "contact_dsa.s2_email_legal": "\u041f\u043e\u0432\u0456\u0434\u043e\u043c\u043b\u0435\u043d\u043d\u044f \u043f\u0440\u043e \u043d\u0435\u0437\u0430\u043a\u043e\u043d\u043d\u0438\u0439 \u0432\u043c\u0456\u0441\u0442 \u0442\u0430 \u043e\u0440\u0433\u0430\u043d\u0438:",
    },
}


def get_database_url() -> str:
    return os.getenv("DATABASE_URL", "postgresql://nevumo:nevumo@localhost:5432/nevumo_leads")


def seed_translations() -> None:
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