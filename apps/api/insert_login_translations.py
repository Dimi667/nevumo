from typing import Dict, Iterable, Tuple

from apps.api.database import SessionLocal
from apps.api.models import Translation

TranslationEntry = Tuple[str, str, str]


TRANSLATIONS_BY_LANGUAGE: Dict[str, Dict[str, Dict[str, str]]] = {
    "bg": {
        "login": {
            "heading": "Как искаш да използваш платформата?",
            "findService": {
                "label": "Намери услуга",
                "subtext": "Търси и резервирай услуги. Може да станеш доставчик по-късно.",
            },
            "offerService": {
                "label": "Предлагай услуги",
                "subtext": "Създай своя профил и предложи услуги. Винаги можеш да търсиш услуги като клиент.",
            },
        }
    },
    "en": {
        "login": {
            "heading": "How would you like to use the platform?",
            "findService": {
                "label": "Find a service",
                "subtext": "Browse and book services now—becoming a provider is an option later.",
            },
            "offerService": {
                "label": "Offer services",
                "subtext": "Create your profile and list services. You can still search for services as a client.",
            },
        }
    },
    "tr": {
        "login": {
            "heading": "Platformu nasıl kullanmak istersin?",
            "findService": {
                "label": "Hizmet ara",
                "subtext": "Hizmetleri keşfet ve hemen rezerve et; sonra sağlayıcı olabilirsin.",
            },
            "offerService": {
                "label": "Hizmet sun",
                "subtext": "Profilini oluştur ve hizmetlerini listele. İstersen yine müşteri olarak hizmet arayabilirsin.",
            },
        }
    },
    "de": {
        "login": {
            "heading": "Wie möchtest du die Plattform nutzen?",
            "findService": {
                "label": "Dienst finden",
                "subtext": "Durchsuche und buche Dienstleistungen – Anbieter werden kannst du später noch.",
            },
            "offerService": {
                "label": "Dienstleistungen anbieten",
                "subtext": "Erstelle dein Profil und biete Leistungen an. Du kannst weiterhin als Kunde nach Diensten suchen.",
            },
        }
    },
    "fr": {
        "login": {
            "heading": "Comment souhaitez-vous utiliser la plateforme ?",
            "findService": {
                "label": "Trouver un service",
                "subtext": "Parcourez et réservez des services. Vous pourrez toujours devenir prestataire plus tard.",
            },
            "offerService": {
                "label": "Proposer des services",
                "subtext": "Créez votre profil et proposez vos services. Vous pourrez continuer à chercher des services en tant que client.",
            },
        }
    },
    "es": {
        "login": {
            "heading": "¿Cómo quieres usar la plataforma?",
            "findService": {
                "label": "Encuentra un servicio",
                "subtext": "Busca y reserva servicios; más adelante puedes convertirte en proveedor.",
            },
            "offerService": {
                "label": "Ofrece servicios",
                "subtext": "Crea tu perfil y ofrece tus servicios. Siempre puedes seguir buscando servicios como cliente.",
            },
        }
    },
    "it": {
        "login": {
            "heading": "Come vuoi usare la piattaforma?",
            "findService": {
                "label": "Trova un servizio",
                "subtext": "Cerca e prenota servizi; potrai diventare fornitore anche dopo.",
            },
            "offerService": {
                "label": "Offri servizi",
                "subtext": "Crea il tuo profilo e proponi i tuoi servizi. Puoi comunque cercare servizi come cliente.",
            },
        }
    },
    "ro": {
        "login": {
            "heading": "Cum vrei să folosești platforma?",
            "findService": {
                "label": "Găsește un serviciu",
                "subtext": "Caută și rezervă servicii; poți deveni furnizor ulterior.",
            },
            "offerService": {
                "label": "Oferă servicii",
                "subtext": "Creează-ți profilul și propune servicii. Poți în continuare căuta servicii ca client.",
            },
        }
    },
    "sr": {
        "login": {
            "heading": "Како желиш да користиш платформу?",
            "findService": {
                "label": "Пронађи услугу",
                "subtext": "Прегледај и резервиши услуге; касније можеш постати пружалац.",
            },
            "offerService": {
                "label": "Пружај услуге",
                "subtext": "Направи профил и понуди услуге. Увек можеш тражити услуге као клијент.",
            },
        }
    },
    "mk": {
        "login": {
            "heading": "Како сакаш да ја користиш платформата?",
            "findService": {
                "label": "Најди услуга",
                "subtext": "Пребарувај и резервирај услуги, а подоцна можеш да станеш добавувач.",
            },
            "offerService": {
                "label": "Нуди услуги",
                "subtext": "Создади профил и понуди услуги. Сè уште можеш да бараш услуги како клиент.",
            },
        }
    },
    "el": {
        "login": {
            "heading": "Πώς θέλεις να χρησιμοποιήσεις την πλατφόρμα;",
            "findService": {
                "label": "Βρες υπηρεσία",
                "subtext": "Αναζήτησε και κλείσε υπηρεσίες – μπορείς να γίνεις πάροχος αργότερα.",
            },
            "offerService": {
                "label": "Προσέφερε υπηρεσίες",
                "subtext": "Δημιούργησε το προφίλ σου και πρόσφερε υπηρεσίες. Μπορείς να συνεχίσεις να αναζητάς υπηρεσίες ως πελάτης.",
            },
        }
    },
    "da": {
        "login": {
            "heading": "Hvordan vil du bruge platformen?",
            "findService": {
                "label": "Find en service",
                "subtext": "Søg og book services – du kan blive udbyder senere.",
            },
            "offerService": {
                "label": "Tilbyd services",
                "subtext": "Opret din profil og tilbyd services. Du kan stadig søge efter services som kunde.",
            },
        }
    },
    "no": {
        "login": {
            "heading": "Hvordan vil du bruke plattformen?",
            "findService": {
                "label": "Finn en tjeneste",
                "subtext": "Søk og book tjenester – du kan bli leverandør senere.",
            },
            "offerService": {
                "label": "Tilby tjenester",
                "subtext": "Lag profilen din og tilby tjenester. Du kan fortsatt søke etter tjenester som kunde.",
            },
        }
    },
    "cs": {
        "login": {
            "heading": "Jak chceš používat platformu?",
            "findService": {
                "label": "Najdi službu",
                "subtext": "Podívej se na služby a rezervuj je. Později můžeš začít poskytovat.",
            },
            "offerService": {
                "label": "Nabízej služby",
                "subtext": "Vytvoř si profil a nabídni služby. Jako klient můžeš dál hledat služby.",
            },
        }
    },
    "et": {
        "login": {
            "heading": "Kuidas soovid platvormi kasutada?",
            "findService": {
                "label": "Leia teenus",
                "subtext": "Otsi ja broneeri teenuseid. Hiljem võid ise teenusepakkujaks hakata.",
            },
            "offerService": {
                "label": "Pakku teenuseid",
                "subtext": "Loo profiil ja paku teenuseid. Sa võid jätkuvalt teenuseid otsida kliendina.",
            },
        }
    },
    "fi": {
        "login": {
            "heading": "Kuinka haluat käyttää alustaa?",
            "findService": {
                "label": "Löydä palvelu",
                "subtext": "Etsi ja varaa palveluita. Voit myöhemmin ryhtyä tarjoajaksi.",
            },
            "offerService": {
                "label": "Tarjoa palveluita",
                "subtext": "Luo profiilisi ja tarjoa palveluita. Voit silti etsiä palveluita asiakkaana.",
            },
        }
    },
    "ga": {
        "login": {
            "heading": "Cén chaoi ar mhaith leat an t-ardán a úsáid?",
            "findService": {
                "label": "Faigh seirbhís",
                "subtext": "Cuardaigh agus leag seirbhísí in áirithe. Is féidir leat a bheith díoltóir níos déanaí.",
            },
            "offerService": {
                "label": "Tairg seirbhísí",
                "subtext": "Cruthaigh do phróifíl agus tairg do sheirbhísí. Féadfaidh tú leanúint ar aghaidh ag cuardach seirbhísí mar chliant.",
            },
        }
    },
    "hr": {
        "login": {
            "heading": "Kako želiš koristiti platformu?",
            "findService": {
                "label": "Pronađi uslugu",
                "subtext": "Pregledaj i rezerviraj usluge. Kasnije se možeš pridružiti kao pružatelj.",
            },
            "offerService": {
                "label": "Nudi usluge",
                "subtext": "Izradi profil i ponudi usluge. I dalje možeš tražiti usluge kao klijent.",
            },
        }
    },
    "hu": {
        "login": {
            "heading": "Hogyan szeretnéd használni a platformot?",
            "findService": {
                "label": "Szolgáltatás keresése",
                "subtext": "Keress és foglalj szolgáltatásokat. Később szolgáltatóként is csatlakozhatsz.",
            },
            "offerService": {
                "label": "Szolgáltatások kínálása",
                "subtext": "Hozd létre profilodat és ajánld szolgáltatásaidat. Kliensként továbbra is kereshetsz szolgáltatásokat.",
            },
        }
    },
    "lt": {
        "login": {
            "heading": "Kaip norėtum naudoti platformą?",
            "findService": {
                "label": "Rask paslaugą",
                "subtext": "Ieškok ir užsisakyk paslaugas. Vėliau gali tapti tiekėju.",
            },
            "offerService": {
                "label": "Siūlyk paslaugas",
                "subtext": "Sukurk profilį ir siūlyk paslaugas. Visada gali ieškoti paslaugų kaip klientas.",
            },
        }
    },
    "lv": {
        "login": {
            "heading": "Kā vēlies izmantot platformu?",
            "findService": {
                "label": "Atrodi pakalpojumu",
                "subtext": "Meklē un rezervē pakalpojumus. Vēlāk vari kļūt par sniedzēju.",
            },
            "offerService": {
                "label": "Piedāvā pakalpojumus",
                "subtext": "Izveido profilu un piedāvā pakalpojumus. Tu joprojām vari meklēt pakalpojumus kā klients.",
            },
        }
    },
    "mt": {
        "login": {
            "heading": "Kif tixtieq tuża l-pjattaforma?",
            "findService": {
                "label": "Sib servizz",
                "subtext": "Fittex u ippjana servizzi; tista' ssir fornitur aktar tard.",
            },
            "offerService": {
                "label": "Offri servizzi",
                "subtext": "Oħloq il-profil tiegħek u offrilek servizzi. Tista' tibqa' tfittxija servizzi bħala klijent.",
            },
        }
    },
    "nl": {
        "login": {
            "heading": "Hoe wil je het platform gebruiken?",
            "findService": {
                "label": "Vind een dienst",
                "subtext": "Zoek en boek diensten. Je kunt later aanbieder worden.",
            },
            "offerService": {
                "label": "Bied diensten aan",
                "subtext": "Maak je profiel aan en bied diensten aan. Je kunt nog steeds als klant diensten zoeken.",
            },
        }
    },
    "pl": {
        "login": {
            "heading": "Jak chcesz korzystać z platformy?",
            "findService": {
                "label": "Znajdź usługę",
                "subtext": "Przeglądaj i rezerwuj usługi. Później możesz zostać usługodawcą.",
            },
            "offerService": {
                "label": "Oferuj usługi",
                "subtext": "Załóż profil i oferuj usługi. Wciąż możesz szukać usług jako klient.",
            },
        }
    },
    "pt": {
        "login": {
            "heading": "Como você quer usar a plataforma?",
            "findService": {
                "label": "Encontre um serviço",
                "subtext": "Pesquise e reserve serviços. Você pode se tornar um prestador depois.",
            },
            "offerService": {
                "label": "Ofereça serviços",
                "subtext": "Crie seu perfil e ofereça serviços. Você ainda pode procurar serviços como cliente.",
            },
        }
    },
    "pt-PT": {
        "login": {
            "heading": "Como queres usar a plataforma?",
            "findService": {
                "label": "Encontra um serviço",
                "subtext": "Pesquisa e reserva serviços; mais tarde podes tornar-te prestador.",
            },
            "offerService": {
                "label": "Oferece serviços",
                "subtext": "Cria o teu perfil e oferece serviços. Podes continuar a procurar serviços como cliente.",
            },
        }
    },
    "sk": {
        "login": {
            "heading": "Ako chceš používať platformu?",
            "findService": {
                "label": "Nájdi službu",
                "subtext": "Prezri si a rezervuj služby. Neskôr sa môžeš stať poskytovateľom.",
            },
            "offerService": {
                "label": "Ponúkaj služby",
                "subtext": "Vytvor si profil a ponúkaj služby. Stále môžeš hľadať služby ako klient.",
            },
        }
    },
    "sl": {
        "login": {
            "heading": "Kako želiš uporabljati platformo?",
            "findService": {
                "label": "Najdi storitev",
                "subtext": "Prebrskaj in rezerviraj storitve. Kasneje lahko postaneš ponudnik.",
            },
            "offerService": {
                "label": "Ponuja storitve",
                "subtext": "Ustvari profil in ponudi storitve. Še vedno lahko iščeš storitve kot naročnik.",
            },
        }
    },
    "sq": {
        "login": {
            "heading": "Si do të përdorësh platformën?",
            "findService": {
                "label": "Gjej një shërbim",
                "subtext": "Kërko dhe rezervoni shërbime. Më vonë mund të bëhesh ofrues.",
            },
            "offerService": {
                "label": "Ofroni shërbime",
                "subtext": "Krijo profilin tënd dhe ofro shërbime. Mund të vazhdosh të kërkosh shërbime si klient.",
            },
        }
    },
    "sv": {
        "login": {
            "heading": "Hur vill du använda plattformen?",
            "findService": {
                "label": "Hitta en tjänst",
                "subtext": "Sök och boka tjänster. Du kan bli leverantör senare.",
            },
            "offerService": {
                "label": "Erbjud tjänster",
                "subtext": "Skapa din profil och erbjud tjänster. Du kan fortfarande söka efter tjänster som kund.",
            },
        }
    },
}


def _flatten_translation_entries(lang: str, payload: Dict[str, Dict[str, str]]) -> Iterable[TranslationEntry]:
    login_section = payload.get("login", {})
    heading = login_section.get("heading")
    if heading:
        yield lang, "login.heading", heading

    find_section = login_section.get("findService", {})
    if find_section:
        label = find_section.get("label")
        if label:
            yield lang, "login.findService.label", label
        subtext = find_section.get("subtext")
        if subtext:
            yield lang, "login.findService.subtext", subtext

    offer_section = login_section.get("offerService", {})
    if offer_section:
        label = offer_section.get("label")
        if label:
            yield lang, "login.offerService.label", label
        subtext = offer_section.get("subtext")
        if subtext:
            yield lang, "login.offerService.subtext", subtext


def upsert_login_translations():
    session = SessionLocal()
    try:
        for lang, payload in TRANSLATIONS_BY_LANGUAGE.items():
            for language, key, value in _flatten_translation_entries(lang, payload):
                existing = (
                    session.query(Translation)
                    .filter(Translation.lang == language, Translation.key == key)
                    .one_or_none()
                )
                if existing:
                    existing.value = value
                else:
                    session.add(Translation(lang=language, key=key, value=value))
        session.commit()
    finally:
        session.close()


if __name__ == "__main__":
    upsert_login_translations()
