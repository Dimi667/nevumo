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
        WHERE key LIKE 'pdf.signature_section_%'
        GROUP BY lang
        ORDER BY lang
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} keys")

ALL_TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "pdf.signature_section_title": "Signature",
        "pdf.signature_section_text": "Signature of consumer(s) [only if this form is notified on paper]",
        "pdf.signature_section_text_part2": "Place and date",
    },
    "bg": {
        "pdf.signature_section_title": "Подпис",
        "pdf.signature_section_text": "Подпис на потребителя/-ите [само ако този формуляр е уведомен на хартия]",
        "pdf.signature_section_text_part2": "Място и дата",
    },
    "pl": {
        "pdf.signature_section_title": "Podpis",
        "pdf.signature_section_text": "Podpis konsumenta(-ów) [tylko w przypadku, gdy formularz jest zgłaszany na papierze]",
        "pdf.signature_section_text_part2": "Miejsce i data",
    },
    "cs": {
        "pdf.signature_section_title": "Podpis",
        "pdf.signature_section_text": "Podpis spotřebitele (spotřebitelů) [pouze pokud je tento formulář zasílán v listinné podobě]",
        "pdf.signature_section_text_part2": "Místo a datum",
    },
    "da": {
        "pdf.signature_section_title": "Underskrift",
        "pdf.signature_section_text": "Forbrugerens/forbrugernes underskrift(er) [kun hvis formularens indhold meddeles på papir]",
        "pdf.signature_section_text_part2": "Sted og dato",
    },
    "de": {
        "pdf.signature_section_title": "Unterschrift",
        "pdf.signature_section_text": "Unterschrift des/der Verbraucher(s) [nur bei Mitteilung auf Papier]",
        "pdf.signature_section_text_part2": "Ort und Datum",
    },
    "el": {
        "pdf.signature_section_title": "Υπογραφή",
        "pdf.signature_section_text": "Υπογραφή καταναλωτή(-ών) [μόνο εάν το παρόν έντυπο κοινοποιηθεί σε χαρτί]",
        "pdf.signature_section_text_part2": "Τόπος και ημερομηνία",
    },
    "es": {
        "pdf.signature_section_title": "Firma",
        "pdf.signature_section_text": "Firma del consumidor o de los consumidores [solo si el presente formulario se somete en papel]",
        "pdf.signature_section_text_part2": "Lugar y fecha",
    },
    "et": {
        "pdf.signature_section_title": "Allkiri",
        "pdf.signature_section_text": "Tarbija(te) allkiri [ainult juhul, kui käesolev vorm esitatakse paberil]",
        "pdf.signature_section_text_part2": "Koht ja kuupäev",
    },
    "fi": {
        "pdf.signature_section_title": "Allekirjoitus",
        "pdf.signature_section_text": "Kuluttajan/kuluttajien allekirjoitus (allekirjoitukset) [vain jos lomake ilmoitetaan paperilla]",
        "pdf.signature_section_text_part2": "Paikka ja päiväys",
    },
    "fr": {
        "pdf.signature_section_title": "Signature",
        "pdf.signature_section_text": "Signature du (des) consommateur(s) [uniquement si le présent formulaire est notifié sur papier]",
        "pdf.signature_section_text_part2": "Lieu et date",
    },
    "ga": {
        "pdf.signature_section_title": "Síniú",
        "pdf.signature_section_text": "Síniú an tomhaltóra/na dtomhaltóirí [ach amháin má thugtar fógra faoin bhfoirm seo ar pháipéar]",
        "pdf.signature_section_text_part2": "Áit agus dáta",
    },
    "hr": {
        "pdf.signature_section_title": "Potpis",
        "pdf.signature_section_text": "Potpis potrošača [samo ako se ovaj obrazac dostavlja na papiru]",
        "pdf.signature_section_text_part2": "Mjesto i datum",
    },
    "hu": {
        "pdf.signature_section_title": "Aláírás",
        "pdf.signature_section_text": "A fogyasztó(k) aláírása [kizárólag papíron tett nyilatkozat esetén]",
        "pdf.signature_section_text_part2": "Hely és dátum",
    },
    "is": {
        "pdf.signature_section_title": "Undirskrift",
        "pdf.signature_section_text": "Undirskrift neytanda/neytenda [aðeins ef þetta eyðublað er afhent á pappír]",
        "pdf.signature_section_text_part2": "Staður og dagsetning",
    },
    "it": {
        "pdf.signature_section_title": "Firma",
        "pdf.signature_section_text": "Firma del consumatore (o dei consumatori) [solo se il presente modulo è notificato su carta]",
        "pdf.signature_section_text_part2": "Luogo e data",
    },
    "lt": {
        "pdf.signature_section_title": "Parašas",
        "pdf.signature_section_text": "Vartotojo (-ų) parašas (-ai) [tik tada, jei ši forma teikiama popieriuje]",
        "pdf.signature_section_text_part2": "Vieta ir data",
    },
    "lv": {
        "pdf.signature_section_title": "Paraksts",
        "pdf.signature_section_text": "Patērētāja(-u) paraksts(-i) [tikai tad, ja šo veidlapu nosūta uz papīra]",
        "pdf.signature_section_text_part2": "Vieta un datums",
    },
    "mt": {
        "pdf.signature_section_title": "Firma",
        "pdf.signature_section_text": "Firma tal-konsumatur(i) [biss jekk din il-formola tkun notifikata fuq il-karta]",
        "pdf.signature_section_text_part2": "Post u data",
    },
    "nl": {
        "pdf.signature_section_title": "Handtekening",
        "pdf.signature_section_text": "Handtekening van consument(en) [alleen wanneer dit formulier op papier wordt ingediend]",
        "pdf.signature_section_text_part2": "Plaats en datum",
    },
    "no": {
        "pdf.signature_section_title": "Underskrift",
        "pdf.signature_section_text": "Forbrukerens underskrift [kun dersom skjemaet leveres på papir]",
        "pdf.signature_section_text_part2": "Sted og dato",
    },
    "pt": {
        "pdf.signature_section_title": "Assinatura",
        "pdf.signature_section_text": "Assinatura do(s) consumidor(es) [só se o presente formulário for notificado em papel]",
        "pdf.signature_section_text_part2": "Local e data",
    },
    "ro": {
        "pdf.signature_section_title": "Semnătura",
        "pdf.signature_section_text": "Semnătura consumatorului (consumatorilor) [doar în cazul în care prezentul formular este notificat pe hârtie]",
        "pdf.signature_section_text_part2": "Locul și data",
    },
    "sk": {
        "pdf.signature_section_title": "Podpis",
        "pdf.signature_section_text": "Podpis spotrebiteľa (spotrebiteľov) [iba ak sa tento formulár podáva v listinnej podobe]",
        "pdf.signature_section_text_part2": "Miesto a dátum",
    },
    "sl": {
        "pdf.signature_section_title": "Podpis",
        "pdf.signature_section_text": "Podpis potrošnika (potrošnikov) [samo če se ta obrazec pošlje na papirju]",
        "pdf.signature_section_text_part2": "Kraj in datum",
    },
    "sv": {
        "pdf.signature_section_title": "Underskrift",
        "pdf.signature_section_text": "Konsumentens/konsumenternas underskrift(er) [endast om denna blankett meddelas på papper]",
        "pdf.signature_section_text_part2": "Ort und datum",
    },
    "tr": {
        "pdf.signature_section_title": "İmza",
        "pdf.signature_section_text": "Tüketicinin (tüketicilerin) imzası [sadece bu form kağıt üzerinde bildirilirse]",
        "pdf.signature_section_text_part2": "Yer ve tarih",
    },
    "uk": {
        "pdf.signature_section_title": "Підпис",
        "pdf.signature_section_text": "Підпис споживача(-ів) [лише якщо ця форма надається на папері]",
        "pdf.signature_section_text_part2": "Місце та дата",
    },
    "ru": {
        "pdf.signature_section_title": "Подпись",
        "pdf.signature_section_text": "Подпись потребителя(-ей) [только если эта форма подается на бумаге]",
        "pdf.signature_section_text_part2": "Место и дата",
    },
    "sr": {
        "pdf.signature_section_title": "Potpis",
        "pdf.signature_section_text": "Potpis potrošača [samo ako se ovaj obrazac dostavlja na papiru]",
        "pdf.signature_section_text_part2": "Mesto i datum",
    },
    "mk": {
        "pdf.signature_section_title": "Потпис",
        "pdf.signature_section_text": "Потпис на потрошувачот(ите) [само ако овој формуляр се доставува на хартија]",
        "pdf.signature_section_text_part2": "Место и датум",
    },
    "sq": {
        "pdf.signature_section_title": "Nënshkrimi",
        "pdf.signature_section_text": "Nënshkrimi i konsumatorit(ëve) [vetëm nëse kjo formë njoftohet në letër]",
        "pdf.signature_section_text_part2": "Vendi dhe data",
    },
    "bs": {
        "pdf.signature_section_title": "Potpis",
        "pdf.signature_section_text": "Potpis potrošača [samo ako se ovaj obrazac dostavlja na papiru]",
        "pdf.signature_section_text_part2": "Mjesto i datum",
    },
    "me": {
        "pdf.signature_section_title": "Potpis",
        "pdf.signature_section_text": "Potpis potrošača [samo ako se ovaj obrazac dostavlja na papiru]",
        "pdf.signature_section_text_part2": "Mjesto i datum",
    },
}

if __name__ == "__main__":
    main()
