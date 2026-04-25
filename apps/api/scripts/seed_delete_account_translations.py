#!/usr/bin/env python3
"""
Seed delete-account translations.
Namespaces: provider_dashboard, client_dashboard
Keys: 5 | Languages: 34
Run: python scripts/seed_delete_account_translations.py
"""

import os

from sqlalchemy import create_engine, text

NAMESPACES = ["provider_dashboard", "client_dashboard"]

LANGS = [
    "en", "bg", "cs", "da", "de", "el", "es", "et", "fi", "fr", "ga", "hr",
    "hu", "is", "it", "lb", "lt", "lv", "mk", "mt", "nl", "no", "pl", "pt",
    "pt-PT", "ro", "ru", "sk", "sl", "sq", "sr", "sv", "tr", "uk",
]

KEYS = [
    "delete_account_btn",
    "delete_account_title",
    "delete_account_warning",
    "delete_account_confirm",
    "delete_account_cancel",
]

TRANSLATIONS = {
    "en": [
        "Delete account",
        "Delete your account",
        "This action is permanent and cannot be undone. All your data, services and history will be permanently deleted.",
        "Yes, delete my account",
        "Cancel",
    ],
    "bg": [
        "Изтрий акаунт",
        "Изтрий акаунта си",
        "Това действие е необратимо. Всички твои данни, услуги и история ще бъдат изтрити завинаги.",
        "Да, изтрий акаунта ми",
        "Отказ",
    ],
    "cs": [
        "Smazat účet",
        "Smazat svůj účet",
        "Tato akce je trvalá a nelze ji vrátit zpět. Všechna vaše data, služby a historie budou trvale smazány.",
        "Ano, smazat můj účet",
        "Zrušit",
    ],
    "da": [
        "Slet konto",
        "Slet din konto",
        "Denne handling er permanent og kan ikke fortrydes. Alle dine data, tjenester og historik slettes permanent.",
        "Ja, slet min konto",
        "Annuller",
    ],
    "de": [
        "Konto löschen",
        "Konto löschen",
        "Diese Aktion ist dauerhaft und kann nicht rückgängig gemacht werden. Alle Ihre Daten, Dienste und der Verlauf werden dauerhaft gelöscht.",
        "Ja, mein Konto löschen",
        "Abbrechen",
    ],
    "el": [
        "Διαγραφή λογαριασμού",
        "Διαγραφή του λογαριασμού σας",
        "Αυτή η ενέργεια είναι μόνιμη και δεν μπορεί να αναιρεθεί. Όλα τα δεδομένα, οι υπηρεσίες και το ιστορικό σας θα διαγραφούν οριστικά.",
        "Ναι, διαγραφή του λογαριασμού μου",
        "Ακύρωση",
    ],
    "es": [
        "Eliminar cuenta",
        "Eliminar tu cuenta",
        "Esta acción es permanente e irreversible. Todos tus datos, servicios e historial serán eliminados permanentemente.",
        "Sí, eliminar mi cuenta",
        "Cancelar",
    ],
    "et": [
        "Kustuta konto",
        "Kustuta oma konto",
        "See toiming on püsiv ja seda ei saa tagasi võtta. Kõik teie andmed, teenused ja ajalugu kustutatakse jäädavalt.",
        "Jah, kustuta minu konto",
        "Tühista",
    ],
    "fi": [
        "Poista tili",
        "Poista tilisi",
        "Tämä toiminto on pysyvä eikä sitä voi peruuttaa. Kaikki tietosi, palvelusi ja historiatietosi poistetaan pysyvästi.",
        "Kyllä, poista tilini",
        "Peruuta",
    ],
    "fr": [
        "Supprimer le compte",
        "Supprimer votre compte",
        "Cette action est permanente et irréversible. Toutes vos données, services et historique seront définitivement supprimés.",
        "Oui, supprimer mon compte",
        "Annuler",
    ],
    "ga": [
        "Scrios an cuntas",
        "Scrios do chuntas",
        "Tá an gníomh seo buan agus ní féidir é a chealú. Scriosfar do chuid sonraí, seirbhísí agus stair go buan.",
        "Tá, scrios mo chuntas",
        "Cealaigh",
    ],
    "hr": [
        "Izbriši račun",
        "Izbriši svoj račun",
        "Ova radnja je trajna i ne može se poništiti. Svi vaši podaci, usluge i povijest bit će trajno izbrisani.",
        "Da, izbriši moj račun",
        "Odustani",
    ],
    "hu": [
        "Fiók törlése",
        "Fiókod törlése",
        "Ez a művelet végleges és nem vonható vissza. Minden adatod, szolgáltatásod és előzményed véglegesen törlődik.",
        "Igen, töröld a fiókomat",
        "Mégse",
    ],
    "is": [
        "Eyða reikningi",
        "Eyða reikningnum þínum",
        "Þessi aðgerð er varanleg og ekki hægt að afturkalla. Öll gögn þín, þjónusta og saga verða eytt að fullu.",
        "Já, eyða reikningnum mínum",
        "Hætta við",
    ],
    "it": [
        "Elimina account",
        "Elimina il tuo account",
        "Questa azione è permanente e non può essere annullata. Tutti i tuoi dati, servizi e cronologia verranno eliminati definitivamente.",
        "Sì, elimina il mio account",
        "Annulla",
    ],
    "lb": [
        "Kont läschen",
        "Äre Kont läschen",
        "Dës Aktioun ass permanent a kann net réckgängeg gemaach ginn. All Är Daten, Servicer an Historique ginn permanent geläscht.",
        "Jo, läscht mäi Kont",
        "Ofbriechen",
    ],
    "lt": [
        "Ištrinti paskyrą",
        "Ištrinti savo paskyrą",
        "Šis veiksmas yra neatšaukiamas. Visi jūsų duomenys, paslaugos ir istorija bus visam laikui ištrinti.",
        "Taip, ištrinti mano paskyrą",
        "Atšaukti",
    ],
    "lv": [
        "Dzēst kontu",
        "Dzēst savu kontu",
        "Šī darbība ir neatgriezeniska. Visi jūsu dati, pakalpojumi un vēsture tiks neatgriezeniski dzēsti.",
        "Jā, dzēst manu kontu",
        "Atcelt",
    ],
    "mk": [
        "Избриши сметка",
        "Избриши ја својата сметка",
        "Оваа акција е трајна и не може да се поништи. Сите ваши податоци, услуги и историја ќе бидат трајно избришани.",
        "Да, избриши ја мојата сметка",
        "Откажи",
    ],
    "mt": [
        "Ħassar il-kont",
        "Ħassar il-kont tiegħek",
        "Dan l-att huwa permanenti u ma jistax jiġi revokat. Id-data, is-servizzi u l-istorja tiegħek kollha jitħassru b'mod permanenti.",
        "Iva, ħassar il-kont tiegħi",
        "Ikkanċella",
    ],
    "nl": [
        "Account verwijderen",
        "Je account verwijderen",
        "Deze actie is permanent en kan niet ongedaan worden gemaakt. Al je gegevens, diensten en geschiedenis worden permanent verwijderd.",
        "Ja, verwijder mijn account",
        "Annuleren",
    ],
    "no": [
        "Slett konto",
        "Slett kontoen din",
        "Denne handlingen er permanent og kan ikke angres. Alle dine data, tjenester og historikk vil bli permanent slettet.",
        "Ja, slett kontoen min",
        "Avbryt",
    ],
    "pl": [
        "Usuń konto",
        "Usuń swoje konto",
        "Ta operacja jest trwała i nie można jej cofnąć. Wszystkie Twoje dane, usługi i historia zostaną trwale usunięte.",
        "Tak, usuń moje konto",
        "Anuluj",
    ],
    "pt": [
        "Excluir conta",
        "Excluir sua conta",
        "Esta ação é permanente e não pode ser desfeita. Todos os seus dados, serviços e histórico serão excluídos permanentemente.",
        "Sim, excluir minha conta",
        "Cancelar",
    ],
    "pt-PT": [
        "Eliminar conta",
        "Eliminar a sua conta",
        "Esta ação é permanente e não pode ser revertida. Todos os seus dados, serviços e histórico serão eliminados permanentemente.",
        "Sim, eliminar a minha conta",
        "Cancelar",
    ],
    "ro": [
        "Șterge contul",
        "Șterge-ți contul",
        "Această acțiune este permanentă și nu poate fi anulată. Toate datele, serviciile și istoricul tău vor fi șterse definitiv.",
        "Da, șterge contul meu",
        "Anulează",
    ],
    "ru": [
        "Удалить аккаунт",
        "Удалить аккаунт",
        "Это действие необратимо. Все ваши данные, услуги и история будут удалены навсегда.",
        "Да, удалить мой аккаунт",
        "Отмена",
    ],
    "sk": [
        "Zmazať účet",
        "Zmazať svoj účet",
        "Táto akcia je trvalá a nedá sa vrátiť späť. Všetky vaše údaje, služby a história budú trvalo zmazané.",
        "Áno, zmazať môj účet",
        "Zrušiť",
    ],
    "sl": [
        "Izbriši račun",
        "Izbriši svoj račun",
        "To dejanje je trajno in ga ni mogoče razveljaviti. Vsi vaši podatki, storitve in zgodovina bodo trajno izbrisani.",
        "Da, izbriši moj račun",
        "Prekliči",
    ],
    "sq": [
        "Fshi llogarinë",
        "Fshi llogarinë tënde",
        "Ky veprim është i përhershëm dhe nuk mund të zhbëhet. Të gjitha të dhënat, shërbimet dhe historia juaj do të fshihen përgjithmonë.",
        "Po, fshi llogarinë time",
        "Anulo",
    ],
    "sr": [
        "Обриши налог",
        "Обриши свој налог",
        "Ова радња је трајна и не може се поништити. Сви ваши подаци, услуге и историја биће трајно обрисани.",
        "Да, обриши мој налог",
        "Откажи",
    ],
    "sv": [
        "Ta bort konto",
        "Ta bort ditt konto",
        "Den här åtgärden är permanent och kan inte ångras. All din data, dina tjänster och historik raderas permanent.",
        "Ja, ta bort mitt konto",
        "Avbryt",
    ],
    "tr": [
        "Hesabı sil",
        "Hesabınızı silin",
        "Bu işlem kalıcıdır ve geri alınamaz. Tüm verileriniz, hizmetleriniz ve geçmişiniz kalıcı olarak silinecektir.",
        "Evet, hesabımı sil",
        "İptal",
    ],
    "uk": [
        "Видалити акаунт",
        "Видалити свій акаунт",
        "Ця дія є незворотною. Усі ваші дані, послуги та історія будуть видалені назавжди.",
        "Так, видалити мій акаунт",
        "Скасувати",
    ],
}


def main() -> None:
    db_url = os.getenv("DATABASE_URL", "postgresql://nevumo:nevumo@localhost:5432/nevumo_leads")
    engine = create_engine(db_url)
    rows = []
    total_upserted = 0

    for namespace in NAMESPACES:
        for lang in LANGS:
            values = TRANSLATIONS[lang]
            for idx, key in enumerate(KEYS):
                rows.append({
                    "lang": lang,
                    "key": f"{namespace}.{key}",
                    "value": values[idx],
                })
            print(f"  → {namespace} | {lang}")

        with engine.connect() as conn:
            result = conn.execute(
                text("""
                    INSERT INTO translations (lang, key, value)
                    VALUES (:lang, :key, :value)
                    ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
                """),
                rows,
            )
            conn.commit()
            total_upserted += len(rows)
            rows = []

    print(f"✅ Seeded {total_upserted} rows total")


if __name__ == "__main__":
    main()
