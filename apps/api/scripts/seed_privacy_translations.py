#!/usr/bin/env python3
import sys
from pathlib import Path

# Add the project root to the python path to allow imports
project_root = str(Path(__file__).resolve().parent.parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from apps.api.database import SessionLocal
from apps.api.i18n import SUPPORTED_LANGUAGES, upsert_translation_values

ENGLISH_BASE = {
    "privacy.page_title": "Privacy Policy",
    "privacy.meta_description": "Learn how Nevumo collects, uses and protects your personal data in accordance with GDPR.",
    "privacy.heading": "Privacy Policy",
    "privacy.effective_date_label": "Effective date:",
    "privacy.effective_date_value": "11 May 2026",
    "privacy.version_label": "Document version:",
    "privacy.version_value": "2026-05-11",
    "privacy.section_1_title": "1. Data Controller",
    "privacy.section_1_body": "The data controller is „PHILIPS CENTER BULGARIA\" Ltd (trading as Nevumo), UIC: 175369610, 77 Petko Karavelov Blvd, Entrance A, Apt. 19, Triaditza District, 1408 Sofia, Bulgaria. In this document the company is referred to as \"Nevumo\". Privacy contact: privacy@nevumo.com",
    "privacy.section_2_title": "2. What Is Nevumo?",
    "privacy.section_2_body": "Nevumo is an online marketplace connecting clients with local service providers. Nevumo acts solely as an intermediary — not a party to contracts between clients and providers, and does not hold or transfer funds. Nevumo is registered in Bulgaria under the supervision of the CPDP (КЗЛД) as Lead Supervisory Authority.",
    "privacy.section_3_title": "3. What Data We Collect and Why",
    "privacy.section_3_1_title": "3.1 Account Registration",
    "privacy.section_3_2_title": "3.2 Provider Profile",
    "privacy.section_3_3_title": "3.3 Service Requests (Leads)",
    "privacy.section_3_4_title": "3.4 Security and Technical Data",
    "privacy.section_3_5_title": "3.5 Analytics",
    "privacy.section_3_5_body": "We use GA4 in Advanced Consent Mode v2. GA4 loads only after you grant consent. If you refuse, GA4 loads in cookieless mode and Google models aggregate data (~85% accuracy) without individual tracking. Withdraw consent anytime via Cookie Settings in the footer.",
    "privacy.section_3_6_title": "3.6 Communications",
    "privacy.section_3_6_note": "For users in Poland: marketing emails require a separate consent under the Electronic Communications Law (PKE) of 10 November 2024.",
    "privacy.section_3_7_title": "3.7 Claimed Provider Profiles (Article 14 GDPR)",
    "privacy.section_3_7_body": "Nevumo may create provider profiles from publicly available information before a provider claims them. Upon claiming, you receive an automated Article 14 GDPR email with details of the data held, its source, processing purpose, and your rights.",
    "privacy.section_4_title": "4. Cookies and Local Storage",
    "privacy.section_4_intro": "We use cookies and browser storage to operate the platform. Full details in our Cookie Policy.",
    "privacy.section_5_title": "5. Who We Share Your Data With",
    "privacy.section_5_note": "We do not sell your personal data. We do not share it with third parties for their own marketing purposes.",
    "privacy.section_6_title": "6. Transfers Outside the EEA",
    "privacy.section_6_body": "All processors based in the USA transfer data under Standard Contractual Clauses (SCCs, EU Decision 2021/914) and, where applicable, the EU–US Data Privacy Framework (DPF). Request a copy at privacy@nevumo.com.",
    "privacy.section_7_title": "7. Automated Decision-Making",
    "privacy.section_7_body": "Nevumo does not make fully automated decisions with significant legal effects. Stripe uses automated fraud detection for payment processing — you have the right to request human review of any decision that significantly affects you.",
    "privacy.section_8_title": "8. How Long We Keep Your Data",
    "privacy.section_9_title": "9. Your Rights Under GDPR",
    "privacy.section_10_title": "10. Right to Lodge a Complaint",
    "privacy.section_10_body": "If you believe your data has been processed unlawfully, you have the right to lodge a complaint with the supervisory authority.",
    "privacy.section_10_lead_label": "Lead Supervisory Authority (Bulgaria):",
    "privacy.section_10_lead_body": "Commission for Personal Data Protection (CPDP / КЗЛД), 2 Prof. Tsvetan Lazarov Blvd., Sofia 1592. Website: www.cpdp.bg | Email: kzld@cpdp.bg",
    "privacy.section_10_pl_label": "Concerned Authority for Polish Users:",
    "privacy.section_10_pl_body": "Urząd Ochrony Danych Osobowych (UODO), ul. Stawki 2, 00-193 Warsaw. Website: www.uodo.gov.pl | Helpline: 606-950-000",
    "privacy.section_11_title": "11. Changes to This Policy",
    "privacy.section_11_body": "We may update this Privacy Policy. Material changes will be notified by email and/or a notice on the platform at least 14 days before they take effect.",
    "privacy.section_12_title": "12. Contact",
    "privacy.section_12_body": "„PHILIPS CENTER BULGARIA\" Ltd (Nevumo), 77 Petko Karavelov Blvd, Entrance A, Apt. 19, Triaditza District, 1408 Sofia, Bulgaria. Email: privacy@nevumo.com",
    "privacy.cookies_link_text": "Cookie Policy",
    "privacy.rights_access": "Right of access (Art. 15): Request a copy of all personal data we hold about you.",
    "privacy.rights_rectification": "Right to rectification (Art. 16): Request correction of inaccurate data.",
    "privacy.rights_erasure": "Right to erasure (Art. 17): Request deletion of your data, subject to legal retention obligations.",
    "privacy.rights_portability": "Right to data portability (Art. 20): Request your data in machine-readable format via Settings → Download my data.",
    "privacy.rights_object": "Right to object (Art. 21): Object to processing based on legitimate interest.",
    "privacy.rights_restrict": "Right to restrict processing (Art. 18): Request restriction in certain circumstances.",
    "privacy.rights_withdraw": "Right to withdraw consent (Art. 7(3)): Withdraw consent at any time without affecting prior processing.",
    "privacy.rights_response_time": "To exercise your rights, contact us at privacy@nevumo.com. We will respond within 30 days.",
    "privacy.min_age_note": "Nevumo is exclusively for users aged 18 and over.",
    "privacy.back_to_home": "Back to home",
}

BULGARIAN_BASE = {
    "privacy.page_title": "Политика за поверителност",
    "privacy.meta_description": "Научете как Nevumo събира, използва и защитава личните ви данни съгласно GDPR.",
    "privacy.heading": "Политика за поверителност",
    "privacy.effective_date_label": "В сила от:",
    "privacy.effective_date_value": "11 май 2026 г.",
    "privacy.version_label": "Версия на документа:",
    "privacy.version_value": "2026-05-11",
    "privacy.section_1_title": "1. Администратор на лични данни",
    "privacy.section_1_body": "Администраторът е \"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (търговска марка: Nevumo), ЕИК: 175369610, бул. Петко Каравелов бл. 77, вх. А, ап. 19, р-н Триадица, п.к. 1408, гр. София, България. В документа дружеството се нарича \"Nevumo\". Контакт: privacy@nevumo.com",
    "privacy.section_2_title": "2. Какво представлява Nevumo?",
    "privacy.section_2_body": "Nevumo е онлайн marketplace, свързващ клиенти с местни доставчици на услуги. Nevumo действа единствено като посредник — не е страна по договора между клиент и доставчик и не задържа или прехвърля средства. Nevumo е регистрирано в България под надзора на КЗЛД като водещ надзорен орган.",
    "privacy.section_3_title": "3. Какви данни събираме и защо",
    "privacy.section_3_1_title": "3.1 Регистрация на акаунт",
    "privacy.section_3_2_title": "3.2 Профил на доставчика",
    "privacy.section_3_3_title": "3.3 Заявки за услуги (Leads)",
    "privacy.section_3_4_title": "3.4 Технически данни и сигурност",
    "privacy.section_3_5_title": "3.5 Анализи",
    "privacy.section_3_5_body": "Използваме GA4 в режим Advanced Consent Mode v2. GA4 се зарежда само след вашето съгласие. При отказ GA4 работи в cookieless режим — Google моделира обобщени данни (~85% точност) без индивидуално проследяване. Оттеглете съгласието чрез Настройки за бисквитки в долния колонтитул.",
    "privacy.section_3_6_title": "3.6 Комуникации",
    "privacy.section_3_6_note": "За потребители от Полша: маркетинговите имейли изискват отделно съгласие съгласно PKE от 10 ноември 2024 г.",
    "privacy.section_3_7_title": "3.7 Предварително заявени профили (чл. 14 GDPR)",
    "privacy.section_3_7_body": "Nevumo може да създаде профил въз основа на публично достъпна информация преди доставчикът да го е потвърдил. При потвърждаване ще получите автоматично имейл по чл. 14 GDPR с информация за събраните данни, техния източник, целта на обработването и вашите права.",
    "privacy.section_4_title": "4. Бисквитки и локално хранилище",
    "privacy.section_4_intro": "Използваме бисквитки и localStorage за работата на платформата. Пълни подробности в нашата Политика за бисквитки.",
    "privacy.section_5_title": "5. С кого споделяме данните ви",
    "privacy.section_5_note": "Не продаваме личните ви данни. Не ги споделяме с трети страни за техни маркетингови цели.",
    "privacy.section_6_title": "6. Предаване на данни извън ЕИП",
    "privacy.section_6_body": "Всички обработващи в САЩ предават данни при стандартни договорни клаузи (SCCs, Решение 2021/914) и, където е приложимо, EU–US Data Privacy Framework (DPF). Поискайте копие на privacy@nevumo.com.",
    "privacy.section_7_title": "7. Автоматизирано вземане на решения",
    "privacy.section_7_body": "Nevumo не взема изцяло автоматизирани решения с правни последици. Stripe използва автоматизирана детекция на измами при плащания — имате право да поискате проверка от човек.",
    "privacy.section_8_title": "8. Срокове на съхранение на данните",
    "privacy.section_9_title": "9. Вашите права по GDPR",
    "privacy.section_10_title": "10. Право на жалба",
    "privacy.section_10_body": "Ако смятате, че данните ви са обработени незаконосъобразно, имате право да подадете жалба до надзорния орган.",
    "privacy.section_10_lead_label": "Водещ надзорен орган (България):",
    "privacy.section_10_lead_body": "Комисия за защита на личните данни (КЗЛД), бул. Проф. Цветан Лазаров №2, София 1592. Сайт: www.cpdp.bg | Имейл: kzld@cpdp.bg",
    "privacy.section_10_pl_label": "Засегнат орган за полски потребители:",
    "privacy.section_10_pl_body": "Urząd Ochrony Danych Osobowych (UODO), ul. Stawki 2, 00-193 Варшава. Сайт: www.uodo.gov.pl | Телефон: 606-950-000",
    "privacy.section_11_title": "11. Промени в тази политика",
    "privacy.section_11_body": "Може да актуализираме тази Политика за поверителност. При съществени промени ще уведомим потребителите по имейл и/или с известие на платформата поне 14 дни преди влизането им в сила.",
    "privacy.section_12_title": "12. Контакт",
    "privacy.section_12_body": "\"ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД (Nevumo), бул. Петко Каравелов бл. 77, вх. А, ап. 19, р-н Триадица, п.к. 1408, гр. София, България. Имейл: privacy@nevumo.com",
    "privacy.cookies_link_text": "Политика за бисквитки",
    "privacy.rights_access": "Право на достъп (чл. 15): Копие от всички данни, които пазим за вас.",
    "privacy.rights_rectification": "Право на коригиране (чл. 16): Коригиране на неточни данни.",
    "privacy.rights_erasure": "Право на изтриване (чл. 17): Изтриване на данните при спазване на законовите задължения.",
    "privacy.rights_portability": "Право на преносимост (чл. 20): Данните ви в машинночетим формат чрез Настройки → Изтегли данните ми.",
    "privacy.rights_object": "Право на възражение (чл. 21): Срещу обработване въз основа на легитимен интерес.",
    "privacy.rights_restrict": "Право на ограничаване (чл. 18): При определени обстоятелства.",
    "privacy.rights_withdraw": "Право на оттегляне на съгласие (чл. 7(3)): По всяко време без да засяга предишното обработване.",
    "privacy.rights_response_time": "Свържете се с нас на privacy@nevumo.com. Отговаряме в срок от 30 дни.",
    "privacy.min_age_note": "Nevumo е предназначена изключително за потребители на 18 и повече години.",
    "privacy.back_to_home": "Начало",
}

POLISH_BASE = {
    "privacy.page_title": "Polityka prywatności",
    "privacy.meta_description": "Dowiedz się, jak Nevumo zbiera, wykorzystuje i chroni Twoje dane osobowe zgodnie z RODO.",
    "privacy.heading": "Polityka prywatności",
    "privacy.effective_date_label": "Data wejścia w życie:",
    "privacy.effective_date_value": "11 maja 2026 r.",
    "privacy.version_label": "Wersja dokumentu:",
    "privacy.version_value": "2026-05-11",
    "privacy.section_1_title": "1. Administrator danych osobowych",
    "privacy.section_1_body": "Administratorem danych jest \"PHILIPS CENTER BULGARIA\" Sp. z o.o. (marka: Nevumo), NIP bułgarski: 175369610, 77 Petko Karavelov Blvd, wejście A, m. 19, dzielnica Triaditza, 1408 Sofia, Bułgaria. W niniejszym dokumencie spółka jest nazywana \"Nevumo\". Kontakt: privacy@nevumo.com",
    "privacy.section_2_title": "2. Czym jest Nevumo?",
    "privacy.section_2_body": "Nevumo to internetowy marketplace łączący klientów z lokalnymi dostawcami usług. Nevumo działa wyłącznie jako pośrednik — nie jest stroną umowy między klientem a dostawcą i nie przechowuje ani nie przekazuje środków pieniężnych. Nevumo jest zarejestrowane w Bułgarii pod nadzorem КЗЛД jako Wiodącego Organu Nadzorczego.",
    "privacy.section_3_title": "3. Jakie dane zbieramy i dlaczego",
    "privacy.section_3_1_title": "3.1 Rejestracja konta",
    "privacy.section_3_2_title": "3.2 Profil dostawcy usług",
    "privacy.section_3_3_title": "3.3 Zapytania o usługi (leads)",
    "privacy.section_3_4_title": "3.4 Dane bezpieczeństwa i techniczne",
    "privacy.section_3_5_title": "3.5 Analityka",
    "privacy.section_3_5_body": "Używamy GA4 w trybie Advanced Consent Mode v2. GA4 ładuje się dopiero po wyrażeniu zgody. Przy odmowie GA4 działa w trybie cookieless — Google modeluje zbiorcze dane (~85% dokładności) bez indywidualnego śledzenia. Zgodę można wycofać w Ustawieniach cookies w stopce.",
    "privacy.section_3_6_title": "3.6 Komunikacja",
    "privacy.section_3_6_note": "Dla użytkowników z Polski: e-maile marketingowe wymagają osobnej zgody zgodnie z Prawem komunikacji elektronicznej (PKE) z dnia 10 listopada 2024 r.",
    "privacy.section_3_7_title": "3.7 Profile przejęte przez Nevumo (art. 14 RODO)",
    "privacy.section_3_7_body": "Nevumo może tworzyć profile dostawców na podstawie publicznie dostępnych informacji przed ich przejęciem. Po przejęciu otrzymasz automatyczne powiadomienie e-mail zgodnie z art. 14 RODO z informacjami o danych, ich źródle, celu przetwarzania i Twoich prawach.",
    "privacy.section_4_title": "4. Pliki cookie i lokalne przechowywanie danych",
    "privacy.section_4_intro": "Używamy plików cookie i localStorage do obsługi platformy. Szczegóły w naszej Polityce cookies.",
    "privacy.section_5_title": "5. Komu przekazujemy Twoje dane",
    "privacy.section_5_note": "Nie sprzedajemy Twoich danych. Nie udostępniamy ich podmiotom trzecim na ich własne cele marketingowe.",
    "privacy.section_6_title": "6. Przekazywanie danych poza EOG",
    "privacy.section_6_body": "Wszystkie podmioty w USA przekazują dane na podstawie Standardowych klauzul umownych (SCCs, decyzja KE 2021/914) oraz, gdzie dotyczy, EU–US Data Privacy Framework (DPF). Kopię zabezpieczeń uzyskasz pod adresem privacy@nevumo.com.",
    "privacy.section_7_title": "7. Zautomatyzowane podejmowanie decyzji",
    "privacy.section_7_body": "Nevumo nie podejmuje w pełni zautomatyzowanych decyzji wywołujących istotne skutki prawne. Stripe używa automatycznego wykrywania oszustw przy płatnościach — masz prawo żądać interwencji człowieka.",
    "privacy.section_8_title": "8. Jak długo przechowujemy Twoje dane",
    "privacy.section_9_title": "9. Twoje prawa wynikające z RODO",
    "privacy.section_10_title": "10. Prawo do złożenia skargi",
    "privacy.section_10_body": "Jeśli uważasz, że Twoje dane zostały przetworzone niezgodnie z prawem, masz prawo złożyć skargę do organu nadzorczego.",
    "privacy.section_10_lead_label": "Wiodący Organ Nadzorczy (Bułgaria):",
    "privacy.section_10_lead_body": "Komisja Ochrony Danych Osobowych (КЗЛД), 2 Prof. Tsvetan Lazarov Blvd., Sofia 1592. Strona: www.cpdp.bg | E-mail: kzld@cpdp.bg",
    "privacy.section_10_pl_label": "Organ zaangażowany dla użytkowników z Polski:",
    "privacy.section_10_pl_body": "Urząd Ochrony Danych Osobowych (UODO), ul. Stawki 2, 00-193 Warszawa. Strona: www.uodo.gov.pl | Infolinia: 606-950-000",
    "privacy.section_11_title": "11. Zmiany niniejszej polityki",
    "privacy.section_11_body": "Możemy aktualizować niniejszą Politykę prywatności. O istotnych zmianach poinformujemy e-mailem i/lub powiadomieniem na platformie co najmniej 14 dni przed ich wejściem w życie.",
    "privacy.section_12_title": "12. Kontakt",
    "privacy.section_12_body": "\"PHILIPS CENTER BULGARIA\" Sp. z o.o. (Nevumo), 77 Petko Karavelov Blvd, wejście A, m. 19, dzielnica Triaditza, 1408 Sofia, Bułgaria. E-mail: privacy@nevumo.com",
    "privacy.cookies_link_text": "Polityka cookies",
    "privacy.rights_access": "Prawo dostępu (art. 15): Kopia wszystkich danych, które przechowujemy.",
    "privacy.rights_rectification": "Prawo do sprostowania (art. 16): Poprawienie niedokładnych danych.",
    "privacy.rights_erasure": "Prawo do usunięcia (art. 17): Usunięcie danych z zastrzeżeniem obowiązków prawnych.",
    "privacy.rights_portability": "Prawo do przenoszenia (art. 20): Dane w formacie maszynowym przez Ustawienia → Pobierz moje dane.",
    "privacy.rights_object": "Prawo do sprzeciwu (art. 21): Wobec przetwarzania opartego na uzasadnionym interesie.",
    "privacy.rights_restrict": "Prawo do ograniczenia (art. 18): W określonych okolicznościach.",
    "privacy.rights_withdraw": "Prawo do wycofania zgody (art. 7 ust. 3): W dowolnym momencie bez wpływu na wcześniejsze przetwarzanie.",
    "privacy.rights_response_time": "Kontakt: privacy@nevumo.com. Odpowiadamy w ciągu 30 dni.",
    "privacy.min_age_note": "Nevumo jest przeznaczona wyłącznie dla użytkowników, którzy ukończyli 18 lat.",
    "privacy.back_to_home": "Powrót do strony głównej",
}

PRIVACY_TRANSLATIONS = {
    key: {
        lang: (
            BULGARIAN_BASE[key] if lang == "bg" else
            POLISH_BASE[key] if lang == "pl" else
            ENGLISH_BASE[key]
        )
        for lang in SUPPORTED_LANGUAGES
    }
    for key in ENGLISH_BASE
}

def seed_privacy_translations():
    db = SessionLocal()
    try:
        for key, translations in PRIVACY_TRANSLATIONS.items():
            upsert_translation_values(db, key, translations)
            print(f"✅ Seeded: {key}")
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding privacy translations: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_privacy_translations()
