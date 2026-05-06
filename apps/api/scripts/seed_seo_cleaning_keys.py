#!/usr/bin/env python3
"""
Seed script to add missing SEO cleaning keys for 31 languages
Run: python -m apps.api.scripts.seed_seo_cleaning_keys
"""
from sqlalchemy import text
from apps.api.database import SessionLocal
from apps.api.models import Translation

SEO_CLEANING_TRANSLATIONS = {
    "bg": {
        "category.seo_cleaning_h2": "Почистване във {city} — какво си заслужава да знаете?",
        "category.seo_cleaning_h3_2": "Колко струва почистването в {city}?",
        "category.seo_cleaning_p3": "Надеждни услуги за почистване на вашия дом или офис. Нашите проверени професионалисти гарантират безупречна среда, за да можете да се съсредоточите върху важното."
    },
    "cs": {
        "category.seo_cleaning_h2": "Úklid v {city} — co stojí za to vědět?",
        "category.seo_cleaning_h3_2": "Kolik stojí úklid v {city}?",
        "category.seo_cleaning_p3": "Spolehlivé úklidové služby pro váš domov nebo kancelář. Naši ověření profesionálové zajistí bezchybné prostředí, abyste se mohli soustředit na to, co je důležité."
    },
    "da": {
        "category.seo_cleaning_h2": "Rengøring i {city} — hvad er værd at vide?",
        "category.seo_cleaning_h3_2": "Hvad koster rengøring i {city}?",
        "category.seo_cleaning_p3": "Pålidelig rengøring til dit hjem eller kontor. Vores verificerede fagfolk sikrer et pletfrit miljø, så du kan fokusere på det, der betyder noget."
    },
    "de": {
        "category.seo_cleaning_h2": "Reinigung in {city} — was sollte man wissen?",
        "category.seo_cleaning_h3_2": "Was kostet die Reinigung in {city}?",
        "category.seo_cleaning_p3": "Zuverlässige Reinigungsdienste für Ihr Zuhause oder Büro. Unsere geprüften Profis sorgen für eine makellose Umgebung, damit Sie sich auf das Wesentliche konzentrieren können."
    },
    "el": {
        "category.seo_cleaning_h2": "Καθαρισμός σε {city} — τι αξίζει να γνωρίζετε;",
        "category.seo_cleaning_h3_2": "Πόσο κοστίζει ο καθαρισμός στο {city};",
        "category.seo_cleaning_p3": "Αξιόπιστες υπηρεσίες καθαρισμού για το σπίτι ή το γραφείο σας. Οι πιστοποιημένοι επαγγελματίες μας εξασφαλίζουν ένα πεντακάθαρο περιβάλλον, ώστε να μπορείτε να εστιάσετε σε όσα έχουν σημασία."
    },
    "en": {
        "category.seo_cleaning_h2": "Cleaning in {city} — what is worth knowing?",
        "category.seo_cleaning_h3_2": "How much does cleaning cost in {city}?",
        "category.seo_cleaning_p3": "Reliable cleaning services for your home or office. Our verified professionals ensure a spotless environment so you can focus on what matters."
    },
    "es": {
        "category.seo_cleaning_h2": "Limpieza en {city} — ¿qué vale la pena saber?",
        "category.seo_cleaning_h3_2": "¿Cuánto cuesta la limpieza en {city}?",
        "category.seo_cleaning_p3": "Servicios de limpieza confiables para su hogar u oficina. Nuestros profesionales verificados garantizan un entorno impecable para que pueda concentrarse en lo importante."
    },
    "et": {
        "category.seo_cleaning_h2": "Koristamine linnas {city} — mida tasub teada?",
        "category.seo_cleaning_h3_2": "Kui palju maksab koristamine linnas {city}?",
        "category.seo_cleaning_p3": "Usaldusväärsed koristusteenused teie koju või kontorisse. Meie kontrollitud spetsialistid tagavad puhta keskkonna, et saaksite keskenduda olulisele."
    },
    "fi": {
        "category.seo_cleaning_h2": "Siivous kaupungissa {city} — mitä on hyvä tietää?",
        "category.seo_cleaning_h3_2": "Paljonko siivous maksaa kaupungissa {city}?",
        "category.seo_cleaning_p3": "Luotettavat siivouspalvelut kotiisi tai toimistoosi. Vahvistetut ammattilaisemme takaavat tahrattoman ympäristön, jotta voit keskittyä olennaiseen."
    },
    "fr": {
        "category.seo_cleaning_h2": "Nettoyage à {city} — que faut-il savoir ?",
        "category.seo_cleaning_h3_2": "Combien coûte le nettoyage à {city} ?",
        "category.seo_cleaning_p3": "Services de nettoyage fiables pour votre maison ou votre bureau. Nos professionnels vérifiés garantissent un environnement impeccable pour que vous puissiez vous concentrer sur l'essentiel."
    },
    "ga": {
        "category.seo_cleaning_h2": "Glanadh i {city} — cad is fiú a bheith ar eolas agat?",
        "category.seo_cleaning_h3_2": "Cé mhéad a chosnaíonn glanadh i {city}?",
        "category.seo_cleaning_p3": "Seirbhísí glantacháin iontaofa do do theach nó d'oifig. Cinntíonn ár ngairmithe fíoraithe timpeallacht gan smál ionas gur féidir leat díriú ar an méid atá tábhachtach."
    },
    "hr": {
        "category.seo_cleaning_h2": "Čišćenje u {city} — što vrijedi znati?",
        "category.seo_cleaning_h3_2": "Koliko košta čišćenje u {city}?",
        "category.seo_cleaning_p3": "Pouzdane usluge čišćenja za vaš dom ili ured. Naši provjereni stručnjaci osiguravaju besprijekorno okruženje kako biste se mogli usredotočiti na ono što je važno."
    },
    "hu": {
        "category.seo_cleaning_h2": "Takarítás {city} városában — mit érdemes tudni?",
        "category.seo_cleaning_h3_2": "Mennyibe kerül a takarítás {city} városában?",
        "category.seo_cleaning_p3": "Megbízható takarítási szolgáltatások otthonába vagy irodájába. Ellenőrzött szakembereink makulátlan környezetet biztosítanak, hogy Ön a fontos dolgokra koncentrálhasson."
    },
    "is": {
        "category.seo_cleaning_h2": "Þrif í {city} — hvað er vert að vita?",
        "category.seo_cleaning_h3_2": "Hvað kostar þrif í {city}?",
        "category.seo_cleaning_p3": "Áreiðanleg ræstingarþjónusta fyrir heimili þitt eða skrifstofu. Prófaðir fagaðilar okkar tryggja flekklaust umhverfi svo þú getir einbeitt þér að því sem skiptir máli."
    },
    "it": {
        "category.seo_cleaning_h2": "Pulizie a {city} — cosa vale la pena sapere?",
        "category.seo_cleaning_h3_2": "Quanto costa la pulizia a {city}?",
        "category.seo_cleaning_p3": "Servizi di pulizia affidabili per la casa o l'ufficio. I nostri professionisti verificati garantiscono un ambiente impeccabile, così potrai concentrarti su ciò che conta."
    },
    "lb": {
        "category.seo_cleaning_h2": "Botzen zu {city} — wat ass gutt ze wëssen?",
        "category.seo_cleaning_h3_2": "Wat kascht d'Botzen zu {city}?",
        "category.seo_cleaning_p3": "Zouverlässeg Botzservicer fir Äert Doheem oder Äre Büro. Eis verifizéiert Fachleit suergen fir en impeccabelt Ëmfeld, fir datt Dir Iech op dat Wichtegst konzentréiere kënnt."
    },
    "lt": {
        "category.seo_cleaning_h2": "Valymas {city} — ką verta žinoti?",
        "category.seo_cleaning_h3_2": "Kiek kainuoja valymas {city}?",
        "category.seo_cleaning_p3": "Patikimos valymo paslaugos jūsų namams ar biurui. Mūsų patikrinti specialistai užtikrina nepriekaištingą švarą, kad galėtumėte susikoncentruoti į tai, kas svarbu."
    },
    "lv": {
        "category.seo_cleaning_h2": "Uzkopšana pilsētā {city} — ko vērts zināt?",
        "category.seo_cleaning_h3_2": "Cik maksā uzkopšana pilsētā {city}?",
        "category.seo_cleaning_p3": "Uzticami uzkopšanas pakalpojumi jūsu mājai vai birojam. Mūsu pārbaudītie speciālisti nodrošina nevainojamu vidi, lai jūs varētu koncentrēties uz svarīgāko."
    },
    "mk": {
        "category.seo_cleaning_h2": "Чистење во {city} — што вреди да се знае?",
        "category.seo_cleaning_h3_2": "Колку чини чистењето во {city}?",
        "category.seo_cleaning_p3": "Сигурни услуги за чистење на вашиот дом или канцеларија. Нашите проверени професионалци гарантираат беспрекорна средина за да можете да се фокусирате на она што е важно."
    },
    "mt": {
        "category.seo_cleaning_h2": "Tindif f'{city} — x'ta' min ikun jaf?",
        "category.seo_cleaning_h3_2": "Kemm jiswa t-tindif f'{city}?",
        "category.seo_cleaning_p3": "Servizzi ta' tindif affidabbli għad-dar jew l-uffiċċju tiegħek. Il-professjonisti vverifikati tagħna jiżguraw ambjent nadif immens biex tkun tista' tiffoka fuq dak li hu importanti."
    },
    "nl": {
        "category.seo_cleaning_h2": "Schoonmaak in {city} — wat is handig om te weten?",
        "category.seo_cleaning_h3_2": "Hoeveel kost schoonmaak in {city}?",
        "category.seo_cleaning_p3": "Betrouwbare schoonmaakdiensten voor uw huis of kantoor. Onze geverifieerde professionals zorgen voor een vlekkeloze omgeving, zodat u zich kunt concentreren op wat belangrijk is."
    },
    "no": {
        "category.seo_cleaning_h2": "Rengjøring i {city} — hva er verdt å vite?",
        "category.seo_cleaning_h3_2": "Hva koster rengjøring i {city}?",
        "category.seo_cleaning_p3": "Pålitelige rengjøringstjenester for hjemmet eller kontoret. Våre verifiserte fagfolk sikrer et plettfritt miljø slik at du kan fokusere på det som betyr noe."
    },
    "pl": {
        "category.seo_cleaning_h2": "Sprzątanie w {city} — co warto wiedzieć?",
        "category.seo_cleaning_h3_2": "Ile kosztuje sprzątanie w {city}?",
        "category.seo_cleaning_p3": "Niezawodne usługi sprzątania dla Twojego domu lub biura. Nasi zweryfikowani specjaliści zapewniają nieskazitelne otoczenie, abyś mógł skupić się na tym, co ważne."
    },
    "pt": {
        "category.seo_cleaning_h2": "Limpeza em {city} — o que vale a pena saber?",
        "category.seo_cleaning_h3_2": "Quanto custa a limpeza em {city}?",
        "category.seo_cleaning_p3": "Serviços de limpeza confiáveis para sua casa ou escritório. Nossos profissionais verificados garantem um ambiente impecável para que você possa focar no que importa."
    },
    "pt-PT": {
        "category.seo_cleaning_h2": "Limpeza em {city} — o que vale a pena saber?",
        "category.seo_cleaning_h3_2": "Quanto custa a limpeza em {city}?",
        "category.seo_cleaning_p3": "Serviços de limpeza confiáveis para a sua casa ou escritório. Os nossos profissionais verificados garantem um ambiente impecável para que se possa focar no que importa."
    },
    "ro": {
        "category.seo_cleaning_h2": "Curățenie în {city} — ce merită să știți?",
        "category.seo_cleaning_h3_2": "Cât costă curățenia în {city}?",
        "category.seo_cleaning_p3": "Servicii de curățenie de încredere pentru casa sau biroul dumneavoastră. Profesioniștii noștri verificați asigură un mediu impecabil, astfel încât să vă puteți concentra pe ceea ce contează."
    },
    "ru": {
        "category.seo_cleaning_h2": "Уборка в {city} — что стоит знать?",
        "category.seo_cleaning_h3_2": "Сколько стоит уборка в {city}?",
        "category.seo_cleaning_p3": "Надежные услуги по уборке вашего дома или офиса. Наши проверенные специалисты обеспечат безупречную чистоту, чтобы вы могли сосредоточиться на важном."
    },
    "sk": {
        "category.seo_cleaning_h2": "Upratovanie v {city} — čo sa oplatí vedieť?",
        "category.seo_cleaning_h3_2": "Koľko stojí upratovanie v {city}?",
        "category.seo_cleaning_p3": "Spoľahlivé upratovacie služby pre váš domov alebo kanceláriu. Naši overení profesionáli zabezpečia bezchybné prostredie, aby ste sa mohli sústrediť na to, čo je dôležité."
    },
    "sl": {
        "category.seo_cleaning_h2": "Čiščenje v {city} — kaj je vredno vedeti?",
        "category.seo_cleaning_h3_2": "Koliko stane čiščenje v {city}?",
        "category.seo_cleaning_p3": "Zanesljive storitve čiščenja za vaš dom ali pisarno. Naši preverjeni strokovnjaki zagotavljajo brezhibno okolje, da se lahko osredotočite na tisto, kar je pomembno."
    },
    "sq": {
        "category.seo_cleaning_h2": "Pastrimi në {city} — çfarë vlen të dini?",
        "category.seo_cleaning_h3_2": "Sa kushton pastrimi në {city}?",
        "category.seo_cleaning_p3": "Shërbime pastrimi të besueshme për shtëpinë ose zyrat tuaja. Profesionistët tanë të verifikuar sigurojnë një mjedis të patëmetë që ju të përqendroheni tek ajo që ka rëndësi."
    },
    "sr": {
        "category.seo_cleaning_h2": "Čišćenje u {city} — šta vredi znati?",
        "category.seo_cleaning_h3_2": "Koliko košta čišćenje u {city}?",
        "category.seo_cleaning_p3": "Pouzdane usluge čišćenja za vaš dom ili kancelariju. Naši provereni stručnjaci osiguravaju besprekorno okruženje kako biste mogli da se fokusirate na ono što je važno."
    },
    "sv": {
        "category.seo_cleaning_h2": "Städning i {city} — vad är värt att veta?",
        "category.seo_cleaning_h3_2": "Vad kostar städning i {city}?",
        "category.seo_cleaning_p3": "Pålitliga städtjänster för ditt hem eller kontor. Våra verifierade proffs garanterar en oklanderlig miljö så att du kan fokusera på det som betyder något."
    },
    "tr": {
        "category.seo_cleaning_h2": "{city} bölgesinde temizlik — neler bilinmeli?",
        "category.seo_cleaning_h3_2": "{city} bölgesinde temizlik ne kadar tutar?",
        "category.seo_cleaning_p3": "Eviniz veya ofisiniz için güvenilir temizlik hizmetleri. Onaylı profesyonellerimiz, önemli olan şeylere odaklanabilmeniz için kusursuz bir ortam sağlar."
    },
    "uk": {
        "category.seo_cleaning_h2": "Прибирання в {city} — що варто знати?",
        "category.seo_cleaning_h3_2": "Скільки коштує прибирання в {city}?",
        "category.seo_cleaning_p3": "Надійні послуги з прибирання вашого будинку або офісу. Наші перевірені фахівці забезпечать бездоганну чистоту, щоб ви могли зосередитися на важливому."
    }
}

# Languages that already have all 6 keys (skip these)
LANGUAGES_WITH_FULL_KEYS = {"bg", "en"}

# Missing keys to add for 31 languages
MISSING_KEYS = [
    "category.seo_cleaning_h2",
    "category.seo_cleaning_h3_2",
    "category.seo_cleaning_p3"
]

def main():
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()

def run_seed(db):
    print("Starting SEO cleaning keys seed...")
    
    # Track statistics
    languages_updated = []
    total_inserted = 0
    
    # Iterate through all languages except those with full keys
    for lang, translations in SEO_CLEANING_TRANSLATIONS.items():
        if lang in LANGUAGES_WITH_FULL_KEYS:
            print(f"Skipping {lang} (already has full keys)")
            continue
        
        inserted_count = 0
        for key in MISSING_KEYS:
            if key in translations:
                # Check if translation already exists
                existing = db.query(Translation).filter(
                    Translation.lang == lang,
                    Translation.key == key
                ).first()
                
                if not existing:
                    # Insert new translation
                    translation = Translation(
                        lang=lang,
                        key=key,
                        value=translations[key]
                    )
                    db.add(translation)
                    inserted_count += 1
                    print(f"  Inserted: {lang} - {key}")
                else:
                    print(f"  Skipped (exists): {lang} - {key}")
        
        if inserted_count > 0:
            languages_updated.append(lang)
            total_inserted += inserted_count
    
    # Commit changes
    db.commit()
    
    print(f"\n✓ Inserted {total_inserted} translations for {len(languages_updated)} languages")
    print(f"Languages updated: {', '.join(sorted(languages_updated))}")
    
    # Verify results
    verify_results(db)

def verify_results(db):
    print("\n--- Verification ---")
    
    # Count SEO cleaning keys per language
    seo_keys = [
        "category.seo_cleaning_h2",
        "category.seo_cleaning_h3_1",
        "category.seo_cleaning_h3_2",
        "category.seo_cleaning_p1",
        "category.seo_cleaning_p2",
        "category.seo_cleaning_p3"
    ]
    
    results = db.execute(
        text("""
            SELECT lang, COUNT(*) as count
            FROM translations
            WHERE key = ANY(:keys)
            GROUP BY lang
            ORDER BY lang
        """),
        {"keys": seo_keys}
    ).fetchall()
    
    complete_count = 0
    incomplete_count = 0
    
    for row in results:
        lang, count = row
        if count == 6:
            complete_count += 1
            print(f"✓ {lang}: {count}/6 keys (complete)")
        else:
            incomplete_count += 1
            print(f"✗ {lang}: {count}/6 keys (incomplete)")
    
    print(f"\nSummary: {complete_count} languages with complete keys, {incomplete_count} incomplete")
    
    if complete_count == 34:
        print("✓ All 34 languages have complete SEO cleaning keys!")
    else:
        print(f"✗ Expected 34 languages with complete keys, got {complete_count}")

if __name__ == "__main__":
    main()
