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
        "pdf.model_form_title": "Model withdrawal form",
        "pdf.model_form_text": "You may use the attached model withdrawal form, but you are not obliged to do so.",
    },
    "bg": {
        "pdf.model_form_title": "Образец на формуляр за отказ",
        "pdf.model_form_text": "Можете да се възползвате от приложения образец на формуляр за отказ, но не сте задължени да го използвате.",
    },
    "cs": {
        "pdf.model_form_title": "Vzorový formulář pro odstoupení od smlouvy",
        "pdf.model_form_text": "Můžete použít přiložený vzorový formulář pro odstoupení od smlouvy, není to však Vaší povinností.",
    },
    "da": {
        "pdf.model_form_title": "Standardfortrydelsesformular",
        "pdf.model_form_text": "De kan bruge den vedlagte standardfortrydelsesformular, men det er ikke obligatorisk.",
    },
    "de": {
        "pdf.model_form_title": "Muster-Widerrufsformular",
        "pdf.model_form_text": "Sie können das beigefügte Muster-Widerrufsformular verwenden, das jedoch nicht vorgeschrieben ist.",
    },
    "el": {
        "pdf.model_form_title": "Υπόδειγμα εντύπου υπαναχώρησης",
        "pdf.model_form_text": "Μπορείτε να χρησιμοποιήσετε το συνημμένο υπόδειγμα εντύπου υπαναχώρησης, αλλά δεν είναι υποχρεωτικό.",
    },
    "es": {
        "pdf.model_form_title": "Modelo de formulario de desistimiento",
        "pdf.model_form_text": "Podrá utilizar el modelo de formulario de desistimiento que figura a continuación, aunque su uso no es obligatorio.",
    },
    "et": {
        "pdf.model_form_title": "Taganemisavalduse tüüpvorm",
        "pdf.model_form_text": "Te võite kasutada lisatud taganemisavalduse tüüpvormi, kuid see ei ole kohustuslik.",
    },
    "fi": {
        "pdf.model_form_title": "Malliperuuttamislomake",
        "pdf.model_form_text": "Voitte käyttää liitteenä olevaa malliperuuttamislomaketta, mutta se ei ole pakollista.",
    },
    "fr": {
        "pdf.model_form_title": "Modèle de formulaire de rétractation",
        "pdf.model_form_text": "Vous pouvez utiliser le modèle de formulaire de rétractation joint, mais ce n’est pas obligatoire.",
    },
    "ga": {
        "pdf.model_form_title": "Samhailfhoirm tarraingthe siar",
        "pdf.model_form_text": "Is féidir leat an t-uasmhailfhoirm tarraingthe siar faoi iamh a úsáid, ach níl aon oibleagáid ort é sin a dhéanamh.",
    },
    "hr": {
        "pdf.model_form_title": "Primjer obrasca za jednostrani raskid ugovora",
        "pdf.model_form_text": "Možete koristiti priloženi primjer obrasca za jednostrani raskid ugovora, ali to nije obvezno.",
    },
    "hu": {
        "pdf.model_form_title": "Elállási/Felmondási nyilatkozatminta",
        "pdf.model_form_text": "Ön felhasználhatja a mellékelt elállási/felmondási nyilatkozatmintát is, de ez nem kötelező.",
    },
    "is": {
        "pdf.model_form_title": "Mintaeyðublað fyrir uppsögn",
        "pdf.model_form_text": "Þú getur notað meðfylgjandi mintaeyðublað fyrir uppsögn, en þér er það ekki skylt.",
    },
    "it": {
        "pdf.model_form_title": "Modulo di recesso tipo",
        "pdf.model_form_text": "È possibile utilizzare il modulo di recesso tipo allegato, ma non è obbligatorio.",
    },
    "lb": {
        "pdf.model_form_title": "Muster-Widderrufformulaire",
        "pdf.model_form_text": "Dir kënnt de bäigefügte Muster-Widderrufformulaire benotzen, mä dat ass net obligatoresch.",
    },
    "lt": {
        "pdf.model_form_title": "Pavyzdinė sutarties atsisakymo forma",
        "pdf.model_form_text": "Galite naudotis pridėta pavyzdine sutarties atsisakymo forma, tačiau tai nėra privaloma.",
    },
    "lv": {
        "pdf.model_form_title": "Atteikuma veidlapas paraugs",
        "pdf.model_form_text": "Jūs varat izmantot pievienoto atteikuma veidlapas paraugu, taču tas nav obligāti.",
    },
    "mk": {
        "pdf.model_form_title": "Образец на формулар за повлекување",
        "pdf.model_form_text": "Може да го користите прикачениот образец на формулар за повлекување, но не сте обврзани да го сторите тоа.",
    },
    "mt": {
        "pdf.model_form_title": "Mudell tal-formola tal-irtirar",
        "pdf.model_form_text": "Tista' tuża l-mudell tal-formola tal-irtirar mehmuża, iżda m'intix obbligat li tagħmel dan.",
    },
    "nl": {
        "pdf.model_form_title": "Modelformulier voor herroeping",
        "pdf.model_form_text": "U kunt gebruikmaken van het bijgevoegde modelformulier voor herroeping, maar bent hiertoe niet verplicht.",
    },
    "no": {
        "pdf.model_form_title": "Standard angreskjema",
        "pdf.model_form_text": "Du kan benytte det vedlagte standard angreskjemaet, men det er ikke obligatorisk.",
    },
    "pl": {
        "pdf.model_form_title": "Wzór formularza odstąpienia od umowy",
        "pdf.model_form_text": "Mogą Państwo skorzystać z załączonego wzoru formularza odstąpienia od umowy, jednak nie są Państwo do tego zobowiązani.",
    },
    "pt": {
        "pdf.model_form_title": "Modelo de formulário de livre resolução",
        "pdf.model_form_text": "Pode utilizar o modelo de formulário de livre resolução em anexo, mas não é obrigatório.",
    },
    "pt-PT": {
        "pdf.model_form_title": "Modelo de formulário de livre resolução",
        "pdf.model_form_text": "Pode utilizar o modelo de formulário de livre resolução em anexo, mas não é obrigatório.",
    },
    "ro": {
        "pdf.model_form_title": "Model de formular de retragere",
        "pdf.model_form_text": "Puteți folosi modelul de formular de retragere alăturat; folosirea lui nu este însă obligatorie.",
    },
    "ru": {
        "pdf.model_form_title": "Образец формы для отказа",
        "pdf.model_form_text": "Вы можете использовать прилагаемую форму для отказа, но это не обязательно.",
    },
    "sk": {
        "pdf.model_form_title": "Vzorový formulár na odstúpenie od zmluvy",
        "pdf.model_form_text": "Môžete použiť priložený vzorový formulár na odstúpenie od zmluvy, nie je to však Vašou povinnosťou.",
    },
    "sl": {
        "pdf.model_form_title": "Vzorčni odstopni obrazec",
        "pdf.model_form_text": "Uporabite lahko priloženi vzorčni odstopni obrazec, vendar to ni obvezno.",
    },
    "sq": {
        "pdf.model_form_title": "Modeli i formularit të tërheqjes",
        "pdf.model_form_text": "Mund të përdorni modelin e bashkëngjitur të formularit të tërheqjes, por nuk jeni të detyruar ta bëni këtë.",
    },
    "sr": {
        "pdf.model_form_title": "Obrazac za odustanak od ugovora",
        "pdf.model_form_text": "Možete koristiti priloženi obrazac za odustanak od ugovora, ali niste obavezni to da učinite.",
    },
    "sv": {
        "pdf.model_form_title": "Standardblankett för utövande av ångerrätten",
        "pdf.model_form_text": "Du kan använda den bifogade standardblanketten, men det är inget krav.",
    },
    "tr": {
        "pdf.model_form_title": "Örnek cayma formu",
        "pdf.model_form_text": "Ekteki örnek cayma formunu kullanabilirsiniz, ancak bu zorunlu değildir.",
    },
    "uk": {
        "pdf.model_form_title": "Зразок форми для відмови",
        "pdf.model_form_text": "Ви можете використовувати додану форму для відмови, але це не обов'язково.",
    },
}

if __name__ == "__main__":
    main()
