import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://localhost/nevumo_leads")

NAMESPACE = "category"

TRANSLATIONS = {
    "lv": {
        "price_meta_none": "Salīdziniet vietējo pakalpojumu sniedzēju cenas",
        "price_meta_single": "no {price} {currency}",
        "price_meta_range": "no {min} līdz {max} {currency}",
        "price_faq_none": "Cenas atšķiras atkarībā no darba apjoma un platības.",
        "price_faq_single": "Pakalpojums maksā aptuveni {price} {currency}, atkarībā no darba apjoma.",
        "price_faq_range": "Pakalpojums maksā no {min} līdz {max} {currency}, atkarībā no apjoma un platības.",
        "price_text_none": "Cenas atšķiras atkarībā no darba apjoma un platības.",
        "price_text_single": "Pakalpojums maksā aptuveni {price} {currency}, atkarībā no darba apjoma.",
        "price_text_range": "Pakalpojums maksā no {min} līdz {max} {currency}, atkarībā no apjoma un platības.",
    },
    "mk": {
        "price_meta_none": "Споредете цени од локални даватели на услуги",
        "price_meta_single": "од {price} {currency}",
        "price_meta_range": "од {min} до {max} {currency}",
        "price_faq_none": "Цените варираат во зависност од обемот и површината на работата.",
        "price_faq_single": "Услугата чини околу {price} {currency}, во зависност од обемот на работата.",
        "price_faq_range": "Услугата чини од {min} до {max} {currency}, во зависност од обемот и површината.",
        "price_text_none": "Цените варираат во зависност од обемот и површината на работата.",
        "price_text_single": "Услугата чини околу {price} {currency}, во зависност од обемот на работата.",
        "price_text_range": "Услугата чини од {min} до {max} {currency}, во зависност од обемот и површината.",
    },
    "mt": {
        "price_meta_none": "Qabbel il-prezzijiet tal-fornituri lokali",
        "price_meta_single": "minn {price} {currency}",
        "price_meta_range": "minn {min} sa {max} {currency}",
        "price_faq_none": "Il-prezzijiet jvarjaw skont il-kamp tal-applikazzjoni u l-erja tax-xogħol.",
        "price_faq_single": "Is-servizz jiswa madwar {price} {currency}, skont il-kamp tax-xogħol.",
        "price_faq_range": "Is-servizz jiswa minn {min} sa {max} {currency}, skont il-kamp u l-erja.",
        "price_text_none": "Il-prezzijiet jvarjaw skont il-kamp tal-applikazzjoni u l-erja tax-xogħol.",
        "price_text_single": "Is-servizz jiswa madwar {price} {currency}, skont il-kamp tax-xogħol.",
        "price_text_range": "Is-servizz jiswa minn {min} sa {max} {currency}, skont il-kamp u l-erja.",
    },
    "nl": {
        "price_meta_none": "Vergelijk prijzen van lokale dienstverleners",
        "price_meta_single": "vanaf {price} {currency}",
        "price_meta_range": "van {min} tot {max} {currency}",
        "price_faq_none": "Prijzen variëren afhankelijk van de omvang en het oppervlak van het werk.",
        "price_faq_single": "De dienst kost ongeveer {price} {currency}, afhankelijk van de omvang van het werk.",
        "price_faq_range": "De dienst kost van {min} tot {max} {currency}, afhankelijk van omvang en oppervlak.",
        "price_text_none": "Prijzen variëren afhankelijk van de omvang en het oppervlak van het werk.",
        "price_text_single": "De dienst kost ongeveer {price} {currency}, afhankelijk van de omvang van het werk.",
        "price_text_range": "De dienst kost van {min} tot {max} {currency}, afhankelijk van omvang en oppervlak.",
    },
    "no": {
        "price_meta_none": "Sammenlign priser fra lokale leverandører",
        "price_meta_single": "fra {price} {currency}",
        "price_meta_range": "fra {min} til {max} {currency}",
        "price_faq_none": "Prisene varierer avhengig av omfang og areal for arbeidet.",
        "price_faq_single": "Tjenesten koster ca. {price} {currency}, avhengig av arbeidsomfanget.",
        "price_faq_range": "Tjenesten koster fra {min} til {max} {currency}, avhengig av omfang og areal.",
        "price_text_none": "Prisene varierer avhengig av omfang og areal for arbeidet.",
        "price_text_single": "Tjenesten koster ca. {price} {currency}, avhengig av arbeidsomfanget.",
        "price_text_range": "Tjenesten koster fra {min} til {max} {currency}, avhengig av omfang og areal.",
    },
    "pl": {
        "price_meta_none": "Porównaj ceny lokalnych wykonawców",
        "price_meta_single": "od {price} {currency}",
        "price_meta_range": "od {min} do {max} {currency}",
        "price_faq_none": "Ceny zależą od zakresu i powierzchni pracy.",
        "price_faq_single": "Usługa kosztuje około {price} {currency}, w zależności od zakresu prac.",
        "price_faq_range": "Usługa kosztuje od {min} do {max} {currency}, w zależności od zakresu i powierzchni.",
        "price_text_none": "Ceny zależą od zakresu i powierzchni pracy.",
        "price_text_single": "Usługa kosztuje około {price} {currency}, w zależności od zakresu prac.",
        "price_text_range": "Usługa kosztuje od {min} do {max} {currency}, w zależności od zakresu i powierzchni.",
    },
    "pt": {
        "price_meta_none": "Compare preços de prestadores locais",
        "price_meta_single": "a partir de {price} {currency}",
        "price_meta_range": "de {min} a {max} {currency}",
        "price_faq_none": "Os preços variam conforme o escopo e a área do trabalho.",
        "price_faq_single": "O serviço custa em torno de {price} {currency}, conforme o escopo do trabalho.",
        "price_faq_range": "O serviço custa de {min} a {max} {currency}, conforme o escopo e a área.",
        "price_text_none": "Os preços variam conforme o escopo e a área do trabalho.",
        "price_text_single": "O serviço custa em torno de {price} {currency}, conforme o escopo do trabalho.",
        "price_text_range": "O serviço custa de {min} a {max} {currency}, conforme o escopo e a área.",
    },
    "pt-PT": {
        "price_meta_none": "Compare preços de prestadores locais",
        "price_meta_single": "a partir de {price} {currency}",
        "price_meta_range": "de {min} a {max} {currency}",
        "price_faq_none": "Os preços variam consoante o âmbito e a área do trabalho.",
        "price_faq_single": "O serviço custa cerca de {price} {currency}, consoante o âmbito do trabalho.",
        "price_faq_range": "O serviço custa de {min} a {max} {currency}, consoante o âmbito e a área.",
        "price_text_none": "Os preços variam consoante o âmbito e a área do trabalho.",
        "price_text_single": "O serviço custa cerca de {price} {currency}, consoante o âmbito do trabalho.",
        "price_text_range": "O serviço custa de {min} a {max} {currency}, consoante o âmbito e a área.",
    },
    "ro": {
        "price_meta_none": "Comparați prețurile furnizorilor locali",
        "price_meta_single": "de la {price} {currency}",
        "price_meta_range": "de la {min} la {max} {currency}",
        "price_faq_none": "Prețurile variază în funcție de amploarea și suprafața lucrării.",
        "price_faq_single": "Serviciul costă aproximativ {price} {currency}, în funcție de amploarea lucrării.",
        "price_faq_range": "Serviciul costă de la {min} la {max} {currency}, în funcție de amploare și suprafață.",
        "price_text_none": "Prețurile variază în funcție de amploarea și suprafața lucrării.",
        "price_text_single": "Serviciul costă aproximativ {price} {currency}, în funcție de amploarea lucrării.",
        "price_text_range": "Serviciul costă de la {min} la {max} {currency}, în funcție de amploare și suprafață.",
    },
    "ru": {
        "price_meta_none": "Сравните цены местных поставщиков услуг",
        "price_meta_single": "от {price} {currency}",
        "price_meta_range": "от {min} до {max} {currency}",
        "price_faq_none": "Цены варьируются в зависимости от объёма и площади работ.",
        "price_faq_single": "Услуга стоит около {price} {currency}, в зависимости от объёма работ.",
        "price_faq_range": "Услуга стоит от {min} до {max} {currency}, в зависимости от объёма и площади.",
        "price_text_none": "Цены варьируются в зависимости от объёма и площади работ.",
        "price_text_single": "Услуга стоит около {price} {currency}, в зависимости от объёма работ.",
        "price_text_range": "Услуга стоит от {min} до {max} {currency}, в зависимости от объёма и площади.",
    },
    "sk": {
        "price_meta_none": "Porovnajte ceny miestnych poskytovateľov",
        "price_meta_single": "od {price} {currency}",
        "price_meta_range": "od {min} do {max} {currency}",
        "price_faq_none": "Ceny sa líšia v závislosti od rozsahu a plochy práce.",
        "price_faq_single": "Služba stojí približne {price} {currency}, v závislosti od rozsahu prác.",
        "price_faq_range": "Služba stojí od {min} do {max} {currency}, v závislosti od rozsahu a plochy.",
        "price_text_none": "Ceny sa líšia v závislosti od rozsahu a plochy práce.",
        "price_text_single": "Služba stojí približne {price} {currency}, v závislosti od rozsahu prác.",
        "price_text_range": "Služba stojí od {min} do {max} {currency}, v závislosti od rozsahu a plochy.",
    },
    "sl": {
        "price_meta_none": "Primerjajte cene lokalnih ponudnikov",
        "price_meta_single": "od {price} {currency}",
        "price_meta_range": "od {min} do {max} {currency}",
        "price_faq_none": "Cene se razlikujejo glede na obseg in površino dela.",
        "price_faq_single": "Storitev stane približno {price} {currency}, odvisno od obsega dela.",
        "price_faq_range": "Storitev stane od {min} do {max} {currency}, odvisno od obsega in površine.",
        "price_text_none": "Cene se razlikujejo glede na obseg in površino dela.",
        "price_text_single": "Storitev stane približno {price} {currency}, odvisno od obsega dela.",
        "price_text_range": "Storitev stane od {min} do {max} {currency}, odvisno od obsega in površine.",
    },
    "sq": {
        "price_meta_none": "Krahasoni çmimet e ofruesve lokalë",
        "price_meta_single": "nga {price} {currency}",
        "price_meta_range": "nga {min} deri {max} {currency}",
        "price_faq_none": "Çmimet variojnë në varësi të shtrirjes dhe sipërfaqes së punës.",
        "price_faq_single": "Shërbimi kushton rreth {price} {currency}, në varësi të shtrirjes së punës.",
        "price_faq_range": "Shërbimi kushton nga {min} deri {max} {currency}, në varësi të shtrirjes dhe sipërfaqes.",
        "price_text_none": "Çmimet variojnë në varësi të shtrirjes dhe sipërfaqes së punës.",
        "price_text_single": "Shërbimi kushton rreth {price} {currency}, në varësi të shtrirjes së punës.",
        "price_text_range": "Shërbimi kushton nga {min} deri {max} {currency}, në varësi të shtrirjes dhe sipërfaqes.",
    },
    "sr": {
        "price_meta_none": "Упоредите цене локалних пружалаца услуга",
        "price_meta_single": "од {price} {currency}",
        "price_meta_range": "од {min} до {max} {currency}",
        "price_faq_none": "Цене варирају у зависности од обима и површине посла.",
        "price_faq_single": "Услуга кошта oko {price} {currency}, у зависности од обима посла.",
        "price_faq_range": "Услуга кошта од {min} до {max} {currency}, у зависности од обима и површине.",
        "price_text_none": "Цене варирају у зависности од обима и површине посла.",
        "price_text_single": "Услуга кошта oko {price} {currency}, у зависности од обима посла.",
        "price_text_range": "Услуга кошта од {min} до {max} {currency}, у зависности од обима и површине.",
    },
    "sv": {
        "price_meta_none": "Jämför priser från lokala leverantörer",
        "price_meta_single": "från {price} {currency}",
        "price_meta_range": "från {min} till {max} {currency}",
        "price_faq_none": "Priserna varierar beroende på arbetets omfattning och yta.",
        "price_faq_single": "Tjänsten kostar ca {price} {currency}, beroende på arbetets omfattning.",
        "price_faq_range": "Tjänsten kostar från {min} till {max} {currency}, beroende på omfattning och yta.",
        "price_text_none": "Priserna varierar beroende på arbetets omfattning och yta.",
        "price_text_single": "Tjänsten kostar ca {price} {currency}, beroende på arbetets omfattning.",
        "price_text_range": "Tjänsten kostar från {min} till {max} {currency}, beroende på omfattning och yta.",
    },
    "tr": {
        "price_meta_none": "Yerel hizmet sağlayıcıların fiyatlarını karşılaştırın",
        "price_meta_single": "{price} {currency}'dan başlayan fiyatlarla",
        "price_meta_range": "{min} ile {max} {currency} arasında",
        "price_faq_none": "Fiyatlar, işin kapsamına ve alanına bağlı olarak değişir.",
        "price_faq_single": "Hizmet, işin kapsamına bağlı olarak yaklaşık {price} {currency} tutarındadır.",
        "price_faq_range": "Hizmet, kapsamına ve alanına bağlı olarak {min} ile {max} {currency} arasında değişir.",
        "price_text_none": "Fiyatlar, işin kapsamına ve alanına bağlı olarak değişir.",
        "price_text_single": "Hizmet, işin kapsamına bağlı olarak yaklaşık {price} {currency} tutarındadır.",
        "price_text_range": "Hizmet, kapsamına ve alanına bağlı olarak {min} ile {max} {currency} arasında değişir.",
    },
    "uk": {
        "price_meta_none": "Порівняйте ціни місцевих постачальників послуг",
        "price_meta_single": "від {price} {currency}",
        "price_meta_range": "від {min} до {max} {currency}",
        "price_faq_none": "Ціни варіюються залежно від обсягу та площі роботи.",
        "price_faq_single": "Послуга коштує близько {price} {currency}, залежно від обсягу роботи.",
        "price_faq_range": "Послуга коштує від {min} до {max} {currency}, залежно від обсягу та площі.",
        "price_text_none": "Ціни варіюються залежно від обсягу та площі роботи.",
        "price_text_single": "Послуга коштує близько {price} {currency}, залежно від обсягу роботи.",
        "price_text_range": "Послуга коштує від {min} до {max} {currency}, залежно від обсягу та площі.",
    },
}


def run():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    count = 0
    for lang, keys in TRANSLATIONS.items():
        for key, value in keys.items():
            db_key = f"{NAMESPACE}.{key}"
            cur.execute(
                """
                INSERT INTO translations (lang, key, value)
                VALUES (%s, %s, %s)
                ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
                """,
                (lang, db_key, value),
            )
            count += 1
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Part 2 done: {count} rows upserted ({len(TRANSLATIONS)} languages)")


if __name__ == "__main__":
    run()
