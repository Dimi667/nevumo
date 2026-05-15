# -*- coding: utf-8 -*-
"""
seed_cookies_p14.py — namespace 'cookies'
cookies.s5_col_retention, cookies.s5_col_category, cookies.s5_col_basis,
cookies.s1_sessionstorage, cookies.s1_note
Run: docker exec nevumo-api python -m apps.api.scripts.seed_cookies_p14
"""

import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)

TRANSLATIONS = {
    "cookies.s5_col_retention": {
        "en": "Retention", "bg": "Period na sukhranenie", "cs": "Uchovavani",
        "da": "Opbevaring", "de": "Aufbewahrung", "el": "Diatirisi",
        "es": "Retencion", "et": "Sailitamine", "fi": "Sailytys",
        "fr": "Conservation", "ga": "Coinneail", "hr": "Cuvanje",
        "hu": "Megorzés", "is": "Vardveisla", "it": "Conservazione",
        "lb": "Aufbewahrung", "lt": "Saugojimas", "lv": "Glabāsana",
        "mk": "Chuvanje", "mt": "Zamma", "nl": "Bewaring",
        "no": "Oppbevaring", "pl": "Przechowywanie", "pt": "Retencao",
        "pt-PT": "Retencao", "ro": "Retentie", "ru": "Khraneniye",
        "sk": "Uchovavanie", "sl": "Hramba", "sq": "Ruajtja",
        "sr": "Cuvanje", "sv": "Lagring", "tr": "Saklama",
        "uk": "Zberihannya",
    },
    "cookies.s5_col_category": {
        "en": "Category", "bg": "Kategoriya", "cs": "Kategorie",
        "da": "Kategori", "de": "Kategorie", "el": "Katigoria",
        "es": "Categoria", "et": "Kategooria", "fi": "Kategoria",
        "fr": "Categorie", "ga": "Catagoír", "hr": "Kategorija",
        "hu": "Kategoria", "is": "Flokkur", "it": "Categoria",
        "lb": "Kategorie", "lt": "Kategorija", "lv": "Kategorija",
        "mk": "Kategorija", "mt": "Kategorija", "nl": "Categorie",
        "no": "Kategori", "pl": "Kategoria", "pt": "Categoria",
        "pt-PT": "Categoria", "ro": "Categorie", "ru": "Kategoriya",
        "sk": "Kategoria", "sl": "Kategorija", "sq": "Kategoria",
        "sr": "Kategorija", "sv": "Kategori", "tr": "Kategori",
        "uk": "Katehoriya",
    },
    "cookies.s5_col_basis": {
        "en": "Legal Basis", "bg": "Pravno osnovanie", "cs": "Pravni zaklad",
        "da": "Retsgrundlag", "de": "Rechtsgrundlage", "el": "Nomiki Vasi",
        "es": "Base juridica", "et": "Oiguslik alus", "fi": "Oikeusperuste",
        "fr": "Base juridique", "ga": "Banus Dli", "hr": "Pravna osnova",
        "hu": "Jogalap", "is": "Lagagrundvollur", "it": "Base giuridica",
        "lb": "Rechtlech Basis", "lt": "Teisinis pagrindas", "lv": "Juridiskais pamats",
        "mk": "Pravna osnova", "mt": "Bazi Legali", "nl": "Rechtsgrondslag",
        "no": "Rettsgrunnlag", "pl": "Podstawa prawna", "pt": "Base juridica",
        "pt-PT": "Base juridica", "ro": "Temei juridic", "ru": "Pravovaya osnova",
        "sk": "Pravny zaklad", "sl": "Pravna podlaga", "sq": "Baza ligjore",
        "sr": "Pravni osnov", "sv": "Rattslig grund", "tr": "Hukuki Dayanak",
        "uk": "Pravova osnova",
    },
    "cookies.s1_sessionstorage": {
        "en": "Session storage works like local storage but is automatically deleted when you close the browser tab.",
        "bg": "Sesiyното khranilishte raboti kato lokalnoto khranilishte, no se iztriva avtomatichno pri zatvarane na brauzarniya razdel.",
        "cs": "Uloziste relace funguje jako lokalni uloziste, ale automaticky se maze po zavreni karty prohlizece.",
        "da": "Sessionslagring fungerer som lokal lagring, men slettes automatisk, nar du lukker browserfanen.",
        "de": "Der Sitzungsspeicher funktioniert wie der lokale Speicher, wird jedoch automatisch geloscht, wenn Sie den Browser-Tab schliessen.",
        "el": "O choros apothikeysis periodou leitourgias leitourgei opos o topikos choros, alla diagrafetai automatika otan kleisete tin kartela toy programmatos perigisis.",
        "es": "El almacenamiento de sesion funciona como el almacenamiento local, pero se elimina automaticamente cuando cierra la pestana del navegador.",
        "et": "Seansi salvestusruum toimib nagu kohalik salvestusruum, kuid kustutatakse automaatselt, kui sulgete brauseri vahekaardi.",
        "fi": "Istuntotallennustila toimii kuten paikallinen tallennustila, mutta poistetaan automaattisesti, kun suljet selaimen valilehden.",
        "fr": "Le stockage de session fonctionne comme le stockage local, mais il est automatiquement supprime a la fermeture de l'onglet du navigateur.",
        "ga": "Oibrionn storailt seisiuin cosul le storailt aitiuil ach scriostar go huathoibroch e nuair a dhunann tu an tab brabhsalai.",
        "hr": "Pohrana sesije funkcionira kao lokalna pohrana, ali se automatski brise kada zatvorite karticu preglednika.",
        "hu": "A munkamenet-tarolo ugyanugy mukodik, mint a helyi tarolo, de automatikusan torlodik, amikor bezarja a bongeszolapot.",
        "is": "Lotugeymsla virkar eins og stadbundin geymsla en er sjálfkrafa eytt thegar thu lokar vafraflipanum.",
        "it": "Il session storage funziona come il local storage, ma viene eliminato automaticamente alla chiusura della scheda del browser.",
        "lb": "Session Storage funktioniert wei lokale Speicher, mee gett automatesch geläscht, wann Dir den Browser-Tab zoumaacht.",
        "lt": "Seanso saugykla veikia kaip vietine saugykla, taciau automatiskai istrintama uzdarius narskykles skirtuka.",
        "lv": "Sesijas kratuve darbojas tapat ka lokala kratuve, tacu tiek automatiski dzesta, aizvеrot parlukprogrammas cilni.",
        "mk": "Sesiskoto skladiranje funkcionira kako lokalnoto, no automatski se brise koga ke go zatvorite jaziceto na prelistuvacot.",
        "mt": "Il-hazna tal-sessjoni tahdem bhal-hazna lokali izda tithhasar awtomatikament meta taghlag it-tab tal-browser.",
        "nl": "Sessieopslag werkt als lokale opslag, maar wordt automatisch verwijderd wanneer u het browsertabblad sluit.",
        "no": "Øktlagring fungerer som lokal lagring, men slettes automatisk nar du lukker nettleserfanen.",
        "pl": "Pamiec sesji dziala jak pamiec lokalna, ale jest automatycznie usuwana po zamknieciu karty przegladarki.",
        "pt": "O armazenamento de sessao funciona como o armazenamento local, mas e automaticamente excluido quando voce fecha a aba do navegador.",
        "pt-PT": "O armazenamento de sessao funciona como o armazenamento local, mas e eliminado automaticamente quando fecha o separador do navegador.",
        "ro": "Stocarea de sesiune functioneaza ca stocarea locala, dar este stearsa automat cand inchideti fila browserului.",
        "ru": "Khranilishche sessii rabotayet kak lokal'noye khranilishche, no avtomaticheski udаляetsya pri zakrytii vkladki brauzera.",
        "sk": "Ulozisko relacie funguje ako lokalne ulozisko, ale automaticky sa vymaze po zatvori karty prehliadaca.",
        "sl": "Shramba seje deluje kot lokalna shramba, vendar se samodejno izbrise, ko zaprete zavihek brskalnika.",
        "sq": "Ruajtja e sesionit funksionon si ruajtja lokale, por fshihet automatikisht kur mbyllni skeden e shfletuesit.",
        "sr": "Skladistenje sesije radi kao lokalno skladistenje, ali se automatski brise kada zatvorite karticu pregledaca.",
        "sv": "Sessionslagring fungerar som lokal lagring men raderas automatiskt nar du stanger webblaserfliken.",
        "tr": "Oturum depolama, yerel depolama gibi calisir, ancak tarayici sekmesini kapattığınızda otomatik olarak silinir.",
        "uk": "Skhovyshche sesiyi pratsyuye yak lokalne skhovyshche, ale avtomatychno vydalyayetsya pry zakrytti vkladky brauzera.",
    },
    "cookies.s1_note": {
        "en": "All three technologies are used on the Nevumo platform. This policy covers all of them.",
        "bg": "I trite tekhnologii se izpolzvat v platformata Nevumo. Nastoyashata politika obkhvashta vsichki tyakh.",
        "cs": "Vsechny tri technologie jsou pouzivany na platforme Nevumo. Tato zasada se vztahuje na vsechny z nich.",
        "da": "Alle tre teknologier bruges pa Nevumo-platformen. Denne politik daekker dem alle.",
        "de": "Alle drei Technologien werden auf der Nevumo-Plattform verwendet. Diese Richtlinie gilt fur alle.",
        "el": "Kai oi treis technologies chrisimopoiountai stin platforma Nevumo. Ayti i politiki kalyftei kai tis treis.",
        "es": "Las tres tecnologias se utilizan en la plataforma Nevumo. Esta politica las cubre todas.",
        "et": "Koiki kolme tehnoloogiat kasutatakse Nevumo platvormil. See poliitika holmab koiki neid.",
        "fi": "Kaikkia kolmea teknologiaa kaytetaan Nevumo-alustalla. Tama kaytanto kattaa ne kaikki.",
        "fr": "Ces trois technologies sont utilisees sur la plateforme Nevumo. Cette politique les couvre toutes.",
        "ga": "Usaidtear na tri theicneolaiocht ar ardan Nevumo. Cludaionn an polasai seo iad ar fad.",
        "hr": "Sve tri tehnologije koriste se na platformi Nevumo. Ova politika obuhvaca sve njih.",
        "hu": "Mindharom technologiat hasznalja a Nevumo platform. Ez a szabalyzat mindegyikre kiterjed.",
        "is": "Allar thraer taeknileg lausnir eru notadar a Nevumo-vettvangi. Thessi stefna nar yfir thaer allar.",
        "it": "Tutte e tre le tecnologie vengono utilizzate sulla piattaforma Nevumo. Questa politica le copre tutte.",
        "lb": "Alleguer drei Technologien ginn op der Nevumo-Plattform benotzt. Des Politik deckt se alleguer of.",
        "lt": "Visos trys technologijos naudojamos Nevumo platformoje. Si politika apima jas visas.",
        "lv": "Visas tris tehnologijas tiek izmantotas Nevumo platforma. Sa politika attiecas uz visam tam.",
        "mk": "Site tri tekhnologii se koristat na platformata Nevumo. Ovaa politika gi opfaka site.",
        "mt": "It-tliet teknologiji kollha huma uzati fuq il-pjattaforma Nevumo. Din il-politika tkopri lkoll minnhom.",
        "nl": "Alle drie de technologieen worden gebruikt op het Nevumo-platform. Dit beleid dekt ze allemaal.",
        "no": "Alle tre teknologiene brukes pa Nevumo-plattformen. Denne policyen dekker dem alle.",
        "pl": "Wszystkie trzy technologie sa uzywane na platformie Nevumo. Niniejsza polityka obejmuje je wszystkie.",
        "pt": "As tres tecnologias sao usadas na plataforma Nevumo. Esta politica abrange todas elas.",
        "pt-PT": "As tres tecnologias sao utilizadas na plataforma Nevumo. Esta politica abrange todas elas.",
        "ro": "Toate cele trei tehnologii sunt utilizate pe platforma Nevumo. Aceasta politica le acopera pe toate.",
        "ru": "Vse tri tekhnologii ispol'zuyutsya na platforme Nevumo. Dannaya politika rasprostranyayetsya na vse iz nikh.",
        "sk": "Vsetky tri technologie su pouzivane na platforme Nevumo. Tieto zasady sa vztahuju na vsetky z nich.",
        "sl": "Vse tri tehnologije se uporabljajo na platformi Nevumo. Ta politika zajema vse tri.",
        "sq": "Te tria teknologjite perdoren ne platformen Nevumo. Kjo politike i mbulon te gjitha.",
        "sr": "Sve tri tehnologije se koriste na platformi Nevumo. Ova politika obuhvata sve njih.",
        "sv": "Alla tre teknologier anvands pa Nevumo-plattformen. Denna policy tacker dem alla.",
        "tr": "Her uc teknoloji de Nevumo platformunda kullanilmaktadir. Bu politika hepsini kapsamaktadir.",
        "uk": "Usi try tekhnolohiyi vykorystovuyutsya na platformi Nevumo. Tsya polityka okhoplyuye vsi z nykh.",
    },
}


def seed():
    with engine.begin() as conn:
        for key, translations in TRANSLATIONS.items():
            for lang, value in translations.items():
                conn.execute(
                    text("""
                        INSERT INTO translations (key, lang, value)
                        VALUES (:key, :lang, :value)
                        ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
                    """),
                    {"key": key, "lang": lang, "value": value},
                )
    print(f"Seeded {len(TRANSLATIONS)} keys x 34 languages")


if __name__ == "__main__":
    seed()