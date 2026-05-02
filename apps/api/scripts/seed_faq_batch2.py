# -*- coding: utf-8 -*-
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Custom database URL with port 5433
DATABASE_URL = "postgresql://nevumo:nevumo@localhost:5433/nevumo_leads"

engine = create_engine(
    DATABASE_URL,
    connect_args={"options": "-c client_encoding=utf8"},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def main():
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()

def run_seed(db):
    # Insert FAQ translations
    insert_translations(db, FAQ_TRANSLATIONS)
    
    # Verify
    verify(db)

def insert_translations(db, data: list[dict]) -> None:
    """Insert/update FAQ translations for category namespace"""
    count = 0
    for item in data:
        lang = item["lang"]
        translations = item["translations"]
        for key, value in translations.items():
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
    print(f"Inserted/updated {count} FAQ translation rows")

def verify(db) -> None:
    """Verify the inserted translations"""
    print("\n=== FAQ Translations by Language ===")
    result = db.execute(
        text("""
            SELECT lang, COUNT(*) as keys
            FROM translations
            WHERE key LIKE 'faq_cleaning_%'
            GROUP BY lang
            ORDER BY lang
        """)
    )
    rows = result.fetchall()
    for row in rows:
        print(f"  {row[0]}: {row[1]} keys")

FAQ_TRANSLATIONS: list[dict] = [
  {"lang": "cs", "translations": {"faq_cleaning_q1": "{category_name} v {city} — co je dobré vědět?", "faq_cleaning_a1": "Profesionální specialisté na {category_name} v {city} nabízejí komplexní služby pro domy, byty a kanceláře. Na Nevumo najdete ověřené profesionály dostupné v celém {city}.", "faq_cleaning_q2": "Jak vybrat specialistu na {category_name}?", "faq_cleaning_a2": "Při výběru specialisty na {category_name} v {city} věnujte pozornost recenzím klientů, rozsahu služeb a zkušenostem odborníka.", "faq_cleaning_q3": "Kolik stojí {category_name} v {city}?", "faq_cleaning_a3": "Ceny za {category_name} v {city} jsou určeny rozsahem prací a pohybují se od {min_price} do {max_price} {currency}."}},
  {"lang": "da", "translations": {"faq_cleaning_q1": "{category_name} i {city} — hvad er værd at vide?", "faq_cleaning_a1": "Professionelle {category_name}-specialister i {city} tilbyder omfattende tjenester til huse, lejligheder og kontorer. På Nevumo finder du verificerede fagfolk tilgængelige i hele {city}.", "faq_cleaning_q2": "Hvordan vælger man en {category_name}-specialist?", "faq_cleaning_a2": "Når du vælger en {category_name}-specialist i {city}, skal du være opmærksom på kundeanmeldelser, serviceomfang og ekspertens erfaring.", "faq_cleaning_q3": "Hvad koster {category_name} i {city}?", "faq_cleaning_a3": "Priserne for {category_name} i {city} bestemmes af arbejdets omfang og ligger mellem {min_price} og {max_price} {currency}."}},
  {"lang": "el", "translations": {"faq_cleaning_q1": "{category_name} σε {city} — τι αξίζει να γνωρίζετε;", "faq_cleaning_a1": "Οι επαγγελματίες ειδικοί {category_name} στο {city} προσφέρουν ολοκληρωμένες υπηρεσίες για σπίτια, διαμερίσματα και γραφεία. Στο Nevumo θα βρείτε επαληθευμένους επαγγελματίες διαθέσιμους σε όλο το {city}.", "faq_cleaning_q2": "Πώς να επιλέξετε έναν ειδικό {category_name};", "faq_cleaning_a2": "Κατά την επιλογή ενός ειδικού {category_name} στο {city}, δώστε προσοχή στις κριτικές πελατών, το εύρος των υπηρεσιών και την εμπειρία του επαγγελματία.", "faq_cleaning_q3": "Πόσο κοστίζει το {category_name} στο {city};", "faq_cleaning_a3": "Οι τιμές για {category_name} στο {city} καθορίζονται από το εύρος των εργασιών και κυμαίνονται από {min_price} έως {max_price} {currency}."}},
  {"lang": "et", "translations": {"faq_cleaning_q1": "{category_name} linnas {city} — mida tasub teada?", "faq_cleaning_a1": "Professionaalsed {category_name} spetsialistid linnas {city} pakuvad terviklikke teenuseid kodudele, korteritele ja kontoritele. Nevumost leiate kontrollitud professionaalid, kes on saadaval kogu {city} piirkonnas.", "faq_cleaning_q2": "Kuidas valida {category_name} spetsialisti?", "faq_cleaning_a2": "Valides {category_name} spetsialisti linnas {city}, pöörake tähelepanu klientide arvustustele, teenuste ulatusele ja eksperdi kogemustele.", "faq_cleaning_q3": "Kui palju maksab {category_name} linnas {city}?", "faq_cleaning_a3": "{category_name} hinnad linnas {city} määravad töö maht ja need jäävad vahemikku {min_price} kuni {max_price} {currency}."}},
  {"lang": "fi", "translations": {"faq_cleaning_q1": "{category_name} kaupungissa {city} — mitä on hyvä tietää?", "faq_cleaning_a1": "Ammattimaiset {category_name}-asiantuntijat kaupungissa {city} tarjoavat kattavia palveluita koteihin, asuntoihin ja toimistoihin. Nevumosta löydät vahvistetut ammattilaiset kaikkialla {city}.", "faq_cleaning_q2": "Miten valita {category_name}-asiantuntija?", "faq_cleaning_a2": "Valitessasi {category_name}-asiantuntijaa kaupungissa {city}, kiinnitä huomiota asiakasarvioihin, palveluiden laajuuteen ja asiantuntijan kokemukseen.", "faq_cleaning_q3": "Paljonko {category_name} maksaa kaupungissa {city}?", "faq_cleaning_a3": "{category_name} hinnat kaupungissa {city} määräytyvät työn laajuuden mukaan ja ovat välillä {min_price} – {max_price} {currency}."}},
  {"lang": "ga", "translations": {"faq_cleaning_q1": "{category_name} i {city} — cad is fiú a bheith ar eolas agat?", "faq_cleaning_a1": "Cuireann speisialtóirí gairmiúla {category_name} i {city} seirbhísí cuimsitheacha ar fáil do thithe, árasáin agus oifigí. Ar Nevumo gheobhaidh tú gairmithe fíoraithe ar fáil ar fud {city}.", "faq_cleaning_q2": "Conas speisialtóir {category_name} a roghnú?", "faq_cleaning_a2": "Agus speisialtóir {category_name} á roghnú agat i {city}, tabhair aird ar léirmheasanna custaiméirí, raon na seirbhísí agus taithí an taineolaí.", "faq_cleaning_q3": "Cé mhéad a chosnaíonn {category_name} i {city}?", "faq_cleaning_a3": "Is é raon na hoibre a chinneann na praghsanna do {category_name} i {city} agus bíonn siad idir {min_price} agus {max_price} {currency}."}},
  {"lang": "hr", "translations": {"faq_cleaning_q1": "{category_name} u {city} — što je važno znati?", "faq_cleaning_a1": "Profesionalni stručnjaci za {category_name} u {city} nude sveobuhvatne usluge za kuće, stanove i urede. Na Nevumo platformi pronaći ćete provjerene stručnjake dostupne u cijelom {city}.", "faq_cleaning_q2": "Kako odabrati stručnjaka za {category_name}?", "faq_cleaning_a2": "Pri odabiru stručnjaka za {category_name} u {city}, obratite pozornost na recenzije klijenata, opseg usluga i iskustvo stručnjaka.", "faq_cleaning_q3": "Koliko košta {category_name} u {city}?", "faq_cleaning_a3": "Cijene za {category_name} u {city} određene su opsegom posla i kreću se od {min_price} do {max_price} {currency}."}},
  {"lang": "hu", "translations": {"faq_cleaning_q1": "{category_name} {city} területén — mit érdemes tudni?", "faq_cleaning_a1": "A professzionális {category_name} szakemberek {city} területén átfogó szolgáltatásokat kínálnak házak, lakások és irodák számára. A Nevumo-n ellenőrzött szakembereket talál {city} egész területén.", "faq_cleaning_q2": "Hogyan válasszunk {category_name} szakembert?", "faq_cleaning_a2": "Amikor {category_name} szakembert választ {city} területén, figyeljen az ügyfélvéleményekre, a szolgáltatások körére és a szakember tapasztalatára.", "faq_cleaning_q3": "Mennyibe kerül a {category_name} {city} területén?", "faq_cleaning_a3": "A {category_name} árait {city} területén a munka volumene határozza meg, {min_price} és {max_price} {currency} között mozognak."}},
  {"lang": "is", "translations": {"faq_cleaning_q1": "{category_name} í {city} — hvað er gott að vita?", "faq_cleaning_a1": "Fagmenn í {category_name} í {city} bjóða upp á alhliða þjónustu fyrir heimili, íbúðir og skrifstofur. Á Nevumo finnur þú vottaða fagaðila um allt {city}.", "faq_cleaning_q2": "Hvernig á að velja sérfræðing í {category_name}?", "faq_cleaning_a2": "Þegar þú velur sérfræðing í {category_name} í {city} skaltu fylgjast með umsögnum viðskiptavina, umfangi þjónustu og reynslu fagaðila.", "faq_cleaning_q3": "Hvað kostar {category_name} í {city}?", "faq_cleaning_a3": "Verð fyrir {category_name} í {city} ræðst af umfangi verksins og er á bilinu {min_price} til {max_price} {currency}."}},
  {"lang": "lb", "translations": {"faq_cleaning_q1": "{category_name} zu {city} — wat ee wësse sollt?", "faq_cleaning_a1": "Professionell {category_name}-Spezialisten zu {city} bidden ëmfaassend Servicer fir Haiser, Appartementer a Büroen un. Op Nevumo fannt Dir iwwerpréift Fachleit an der ganzer {city}.", "faq_cleaning_q2": "Wéi wielt een en {category_name}-Spezialist?", "faq_cleaning_a2": "Wann Dir en {category_name}-Spezialist zu {city} wielt, oppasst op d'Client-Bewäertungen, den Ëmfang vum Service an d'Erfahrung vum Profi.", "faq_cleaning_q3": "Wat kascht {category_name} zu {city}?", "faq_cleaning_a3": "D'Präisser fir {category_name} zu {city} ginn duerch den Ëmfang vun der Aarbecht bestëmmt a leien tëscht {min_price} a {max_price} {currency}."}},
  {"lang": "lt", "translations": {"faq_cleaning_q1": "{category_name} mieste {city} - ką verta žinoti?", "faq_cleaning_a1": "Profesionalūs {category_name} specialistai mieste {city} siūlo kompleksines paslaugas namams, butams ir biurams. \"Nevumo\" rasite patikrintus profesionalus, dirbančius visame {city}.", "faq_cleaning_q2": "Kaip pasirinkti {category_name} specialistą?", "faq_cleaning_a2": "Renkantis {category_name} specialistą mieste {city}, atkreipkite dėmesį į klientų atsiliepimus, paslaugų apimtį ir specialisto patirtį.", "faq_cleaning_q3": "Kiek kainuoja {category_name} mieste {city}?", "faq_cleaning_a3": "{category_name} kainos mieste {city} priklauso nuo darbų apimties ir svyruoja nuo {min_price} iki {max_price} {currency}."}}
]

if __name__ == "__main__":
    main()
