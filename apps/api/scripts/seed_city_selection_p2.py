from sqlalchemy import text

from apps.api.database import SessionLocal

TRANSLATIONS = [
    ("bg", "city_selection.meta_description", "Намери проверени специалисти за услуги в твоя град. Сравни и поръчай местни специалисти лесно на Nevumo."),
    ("cs", "city_selection.meta_description", "Najděte ověřené poskytovatele služeb ve vašem městě. Porovnejte a objednejte místní specialisty snadno na Nevumo."),
    ("da", "city_selection.meta_description", "Find betroede serviceudbydere i din by. Sammenlign og bestil lokale specialister nemt på Nevumo."),
    ("de", "city_selection.meta_description", "Finde geprüfte Dienstleister in deiner Stadt. Vergleiche und buche lokale Spezialisten einfach auf Nevumo."),
    ("el", "city_selection.meta_description", "Βρείτε αξιόπιστους παρόχους υπηρεσιών στην πόλη σας. Συγκρίνετε και κλείστε τοπικούς ειδικούς εύκολα στο Nevumo."),
    ("en", "city_selection.meta_description", "Find trusted service providers in your city. Compare and book local specialists easily on Nevumo."),
    ("es", "city_selection.meta_description", "Encuentra proveedores de servicios de confianza en tu ciudad. Compara y reserva especialistas locales fácilmente en Nevumo."),
    ("et", "city_selection.meta_description", "Leia usaldusväärseid teenuseosutajaid oma linnas. Võrdle ja broneeri kohalikke spetsialiste lihtsalt Nevumos."),
    ("fi", "city_selection.meta_description", "Löydä luotettavia palveluntarjoajia kaupungissasi. Vertaile ja varaa paikallisia asiantuntijoita helposti Nevumossa."),
    ("fr", "city_selection.meta_description", "Trouvez des prestataires de services de confiance dans votre ville. Comparez et réservez des spécialistes locaux facilement sur Nevumo."),
    ("ga", "city_selection.meta_description", "Aimsigh soláthraithe seirbhíse iontaofa i do chathair. Déan comparáid agus cuir in áirithe speisialtóirí áitiúla go héasca ar Nevumo."),
    ("hr", "city_selection.meta_description", "Pronađi pouzdane pružatelje usluga u svom gradu. Usporedi i rezerviraj lokalne stručnjake jednostavno na Nevumo."),
    ("hu", "city_selection.meta_description", "Találj megbízható szolgáltatókat a városodban. Hasonlítsd össze és foglald le a helyi szakembereket könnyen a Nevumón."),
    ("is", "city_selection.meta_description", "Finndu trausta þjónustuaðila í þinni borg. Berðu saman og pantaðu staðbundna sérfræðinga auðveldlega á Nevumo."),
    ("it", "city_selection.meta_description", "Trova fornitori di servizi affidabili nella tua città. Confronta e prenota specialisti locali facilmente su Nevumo."),
    ("lb", "city_selection.meta_description", "Fannt vertrauenswürdeg Serviceanbieder an denger Stad. Vergläicht a bucht lokal Spezialisten einfach op Nevumo."),
    ("lt", "city_selection.meta_description", "Raskite patikimus paslaugų teikėjus savo mieste. Palyginkite ir užsakykite vietos specialistus lengvai Nevumo."),
    ("lv", "city_selection.meta_description", "Atrodiet uzticamus pakalpojumu sniedzējus savā pilsētā. Salīdziniet un rezervējiet vietējos speciālistus viegli Nevumo."),
    ("mk", "city_selection.meta_description", "Пронајди доверливи даватели на услуги во твојот град. Спореди и резервирај локални специјалисти лесно на Nevumo."),
    ("mt", "city_selection.meta_description", "Sib fornituri ta' servizzi affidabbli fil-belt tiegħek. Qabbel u ibbukkja speċjalisti lokali b'mod faċli fuq Nevumo."),
    ("nl", "city_selection.meta_description", "Vind betrouwbare dienstverleners in jouw stad. Vergelijk en boek lokale specialisten eenvoudig op Nevumo."),
    ("no", "city_selection.meta_description", "Finn pålitelige tjenesteleverandører i din by. Sammenlign og bestill lokale spesialister enkelt på Nevumo."),
    ("pl", "city_selection.meta_description", "Znajdź zaufanych dostawców usług w swoim mieście. Porównaj i zamów lokalnych specjalistów łatwo na Nevumo."),
    ("pt", "city_selection.meta_description", "Encontre prestadores de serviços confiáveis na sua cidade. Compare e agende especialistas locais facilmente no Nevumo."),
    ("pt-PT", "city_selection.meta_description", "Encontre prestadores de serviços de confiança na sua cidade. Compare e agende especialistas locais facilmente no Nevumo."),
    ("ro", "city_selection.meta_description", "Găsește furnizori de servicii de încredere în orașul tău. Compară și rezervă specialiști locali ușor pe Nevumo."),
    ("ru", "city_selection.meta_description", "Найдите проверенных поставщиков услуг в вашем городе. Сравнивайте и заказывайте местных специалистов легко на Nevumo."),
    ("sk", "city_selection.meta_description", "Nájdite overených poskytovateľov služieb vo vašom meste. Porovnajte a objednajte miestnych špecialistov ľahko na Nevumo."),
    ("sl", "city_selection.meta_description", "Poišči zanesljive ponudnike storitev v svojem mestu. Primerjaj in rezerviraj lokalne strokovnjake preprosto na Nevumo."),
    ("sq", "city_selection.meta_description", "Gjeni ofrues të besueshëm shërbimesh në qytetin tuaj. Krahasoni dhe rezervoni specialistë lokalë lehtësisht në Nevumo."),
    ("sr", "city_selection.meta_description", "Pronađi pouzdane pružaoce usluga u svom gradu. Uporedi i rezerviši lokalne stručnjake jednostavno na Nevumo."),
    ("sv", "city_selection.meta_description", "Hitta pålitliga tjänsteleverantörer i din stad. Jämför och boka lokala specialister enkelt på Nevumo."),
    ("tr", "city_selection.meta_description", "Şehrinizde güvenilir hizmet sağlayıcılar bulun. Nevumo'da yerel uzmanları kolayca karşılaştırın ve rezervasyon yapın."),
    ("uk", "city_selection.meta_description", "Знайдіть перевірених постачальників послуг у вашому місті. Порівнюйте та замовляйте місцевих фахівців легко на Nevumo."),
]

def main():
    db = SessionLocal()
    try:
        insert_translations(db, TRANSLATIONS)
    finally:
        db.close()

def insert_translations(db, data: list[tuple[str, str, str]]) -> None:
    for lang, key, value in data:
        db.execute(
            text("""
                INSERT INTO translations (lang, key, value)
                VALUES (:lang, :key, :value)
                ON CONFLICT (lang, key)
                DO UPDATE SET value = EXCLUDED.value
            """),
            {"lang": lang, "key": key, "value": value}
        )
    db.commit()
    print("Seeded 34 rows — Part 2 complete")

if __name__ == "__main__":
    main()
