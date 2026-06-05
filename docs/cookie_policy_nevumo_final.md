# Nevumo — Cookie Policy
**Версия на политиката:** 2026-05-01  
**Последна актуализация:** май 2026 г.

> Документът съдържа три езикови версии: **English → Polski → Български**  
> Всяка версия е пълна и самостоятелна.  
> Компания: „ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ" ООД (търговска марка Nevumo)  
> ЕИК: 175369610  
> Адрес: бул. Петко Каравелов бл. 77, вх. А, ап. 19, р-н Триадица, п.к. 1408, гр. София, България  
> Имейл: privacy@nevumo.com

---
---

# 🇬🇧 ENGLISH VERSION

## Cookie Policy

**Controller:** "PHILIPS CENTRE BULGARIA" Ltd. (trading as **Nevumo**)  
**Company registration number (EIK):** 175369610  
**Registered address:** 77 Petko Karavelov Blvd., Entrance A, Apt. 19, Triaditza District, 1408 Sofia, Bulgaria  
**Contact:** privacy@nevumo.com  
**Effective date:** 2026-05-01 | **Version:** 2.0

---

### 1. What Are Cookies and Browser Storage?

**Cookies** are small text files that a website places on your device (computer, phone, tablet) when you visit it. They allow the website to remember information about your visit — such as your preferences or login status — and retrieve it on future visits.

**Local storage** is a similar technology built into your browser. It stores data on your device without an expiry date (unless cleared manually). Unlike cookies, local storage data is not automatically sent to our servers with each request.

**Session storage** works like local storage but is automatically deleted when you close the browser tab.

All three technologies are used on the Nevumo platform. This policy covers all of them.

---

### 2. Who Uses These Technologies?

Nevumo uses cookies and browser storage directly (**first-party**) and allows selected third-party services to place their own cookies on your device (**third-party**). All third parties are listed in the table in Section 5.

---

### 3. Categories of Cookies We Use

#### 3.1 Strictly Necessary
Essential for the platform to function. Without them, you cannot log in, use the service, or navigate the site securely. Always active — no consent required.

**Legal basis:** Art. 6(1)(b) GDPR — performance of a contract; Art. 6(1)(f) GDPR — legitimate interest in platform security.

#### 3.2 Functional
Remember your preferences and choices (e.g., selected language, selected city, intended role as client or provider) to improve your experience. They do not track you across other websites.

**Legal basis:** Art. 6(1)(f) GDPR — legitimate interest in a consistent user experience. You can object at any time via the Cookie Settings panel in the website footer.

#### 3.3 Analytics
Help us understand how visitors use Nevumo — which pages are visited, how long users stay, and where they come from. This data is aggregated and used to improve the platform.

We use **Google Analytics 4 (GA4)** with **Advanced Consent Mode v2**. This means:
- If you decline analytics cookies, GA4 still loads but sends only anonymised, cookieless "pings."
- Google uses statistical modelling to estimate traffic trends — without identifying you personally.
- No analytics cookies (`_ga`, `_ga_[ID]`) are placed on your device without your explicit consent.

This implementation is disclosed in accordance with Google's Advanced Consent Mode v2 requirements.

**Legal basis:** Art. 6(1)(a) GDPR — your consent.

#### 3.4 Marketing
Currently, Nevumo does not use marketing or advertising cookies. This category is reserved for future features (e.g., retargeting). No marketing cookies are set at this time.

**Legal basis (when used):** Art. 6(1)(a) GDPR — your consent.

---

### 4. Your Phone Number in Local Storage

When you provide a phone number on the platform (e.g., when submitting a service request), we temporarily store it in your browser's local storage under the key `nevumo_phone`. This enables autofill on subsequent visits so you do not have to type it again.

**Legal basis:** Art. 6(1)(f) GDPR — legitimate interest in reducing friction and improving user experience. This data never leaves your device unless you explicitly submit a form. You can delete it at any time by clearing your browser's local storage or via your account settings.

---

### 5. Full List of Cookies and Browser Storage Entries

| Name / Key | Storage Type | Purpose | Provider | Retention | Category | Legal Basis |
|---|---|---|---|---|---|---|
| `nevumo_consent` | Cookie (first-party) | Records your cookie consent choices | Nevumo | 12 months | Necessary | Legal obligation (Art. 7 GDPR) |
| `lang` | Cookie (first-party) | Stores your selected display language | Nevumo | 30 days | Functional | Legitimate Interest |
| `_ga` | Cookie (third-party) | Google Analytics — distinguishes unique users | Google | 13 months | Analytics | Consent |
| `_ga_[ID]` | Cookie (third-party) | Google Analytics — session tracking | Google | 13 months | Analytics | Consent |
| `__stripe_mid` | Cookie (third-party) | Stripe fraud prevention — device fingerprint | Stripe | 1 year | Necessary | Legitimate Interest / Contract |
| `__stripe_sid` | Cookie (third-party) | Stripe fraud prevention — session identifier | Stripe | 30 minutes | Necessary | Legitimate Interest / Contract |
| `nevumo_auth_token` | Local Storage | Authentication JWT — keeps you logged in | Nevumo | Session / 30 days | Necessary | Contract |
| `nevumo_auth_user` | Local Storage | Cached user profile data (id, name, role) | Nevumo | Session / 30 days | Necessary | Contract |
| `nevumo_phone` | Local Storage | Phone number autofill | Nevumo | Until cleared | Functional | Legitimate Interest |
| `nevumo_intent` | Local Storage | Stores your selected role intent (client / provider) | Nevumo | Session | Functional | Legitimate Interest |
| `nevumo_city_preference` | Local Storage | Stores your selected city | Nevumo | Until cleared | Functional | Legitimate Interest |
| `nevumo_last_url` | Local Storage | Last visited "clean" URL for PWA smart redirect | Nevumo | Until cleared | Functional | Legitimate Interest |
| `nevumo_auth_email` | Session Storage | Temporarily stores email address during registration | Nevumo | Session (tab) | Necessary | Contract |

> **Note on Stripe cookies:** `__stripe_mid` and `__stripe_sid` are set only on pages where payment processing takes place. Stripe.js is not loaded on other pages.

> **Note on GA4 Advanced Consent Mode v2:** When you decline analytics cookies, Google Analytics operates in a cookieless mode. No `_ga` or `_ga_[ID]` cookies are placed on your device. Google may use aggregated, anonymised signals to model traffic statistics, in accordance with its Advanced Consent Mode v2 framework.

> **Note on `lang` cookie:** This cookie is strictly functional — it stores your language preference so the platform displays in your chosen language on every visit. It does not track your activity and does not require consent under Art. 5(3) of the ePrivacy Directive.

---

### 6. How to Manage Your Preferences

**Via the Cookie Banner:** When you first visit Nevumo, a banner appears allowing you to accept all, reject all, or customise your preferences by category.

**Via Cookie Settings:** A "Cookie Settings" link is always available in the website footer. Click it at any time to review or change your choices.

**Via your browser:** You can delete, block, or manage all cookies through your browser settings. Note that blocking strictly necessary cookies may prevent the platform from functioning correctly.

| Browser | Settings path |
|---|---|
| Chrome | Settings → Privacy and security → Cookies and other site data |
| Firefox | Settings → Privacy & Security → Cookies and Site Data |
| Safari | Settings → Privacy → Manage Website Data |
| Edge | Settings → Cookies and site permissions |

**Via local/session storage:** You can clear browser storage data through your browser's developer tools (Application → Local Storage / Session Storage → nevumo.com → Delete all).

---

### 7. Third-Party Data Processors

| Processor | Role | Privacy Policy |
|---|---|---|
| Google LLC | Analytics (GA4) | https://policies.google.com/privacy |
| Stripe, Inc. | Payment processing (fraud prevention) | https://stripe.com/privacy |
| Vercel Inc. | Frontend hosting | https://vercel.com/legal/privacy-policy |
| Railway Corp. | Backend API hosting | https://railway.app/legal/privacy |
| Neon Inc. | PostgreSQL database hosting | https://neon.tech/privacy-policy |
| Upstash Inc. | Redis cache hosting | https://upstash.com/trust/privacy.pdf |
| Cloudflare Inc. | Media storage (R2) | https://www.cloudflare.com/privacypolicy/ |

All third parties listed above have signed Data Processing Agreements (DPAs) with Nevumo where required by GDPR.

---

### 8. International Data Transfers

Nevumo's hosting infrastructure is based in the United States. All transfers outside the European Economic Area (EEA) are safeguarded by Standard Contractual Clauses (SCCs) approved by the European Commission.

Additionally, Google LLC and Cloudflare Inc. participate in the EU–US Data Privacy Framework (DPF), providing an additional transfer safeguard.

| Recipient | Country | Safeguard |
|---|---|---|
| Google LLC (GA4) | USA | SCCs + EU-US DPF |
| Stripe, Inc. | USA | SCCs |
| Vercel Inc. | USA | SCCs |
| Railway Corp. | USA | SCCs |
| Neon Inc. | USA | SCCs |
| Upstash Inc. | USA | SCCs |
| Cloudflare Inc. (R2) | USA | SCCs + EU-US DPF |

---

### 9. Re-consent

We will ask for your consent again after 12 months, or sooner if we make material changes to the types of cookies we use.

---

### 10. Changes to This Policy

We may update this Cookie Policy from time to time. The "Effective date" at the top of this page will always show the date of the latest version. Significant changes will be communicated via the cookie consent banner.

---

### 11. Contact and Complaints

**Data controller:**  
"PHILIPS CENTRE BULGARIA" Ltd. (trading as Nevumo)  
EIK: 175369610  
77 Petko Karavelov Blvd., Entrance A, Apt. 19, Triaditza District, 1408 Sofia, Bulgaria  
Email: privacy@nevumo.com

**Lead Supervisory Authority (Bulgaria):**  
Commission for Personal Data Protection (CPDP / КЗЛД)  
2 Prof. Tsvetan Lazarov Blvd., Sofia 1592, Bulgaria  
https://www.cpdp.bg

**Concerned Supervisory Authority (Poland):**  
Urząd Ochrony Danych Osobowych (UODO)  
ul. Stawki 2, 00-193 Warszawa  
https://uodo.gov.pl

---
---

# 🇵🇱 WERSJA POLSKA

## Polityka plików cookies

**Administrator danych:** „PHILIPS CENTRE BULGARIA" Sp. z o.o. (marka handlowa **Nevumo**)  
**Numer rejestracyjny (EIK):** 175369610  
**Adres rejestracyjny:** 77 Petko Karavelov Blvd., kl. A, m. 19, dzielnica Triaditza, 1408 Sofia, Bułgaria  
**Kontakt:** privacy@nevumo.com  
**Data wejścia w życie:** 2026-05-01 | **Wersja:** 2.0

---

### 1. Czym są pliki cookies i pamięć przeglądarki?

**Pliki cookies** (ciasteczka) to małe pliki tekstowe, które serwis internetowy umieszcza na Twoim urządzeniu (komputerze, telefonie, tablecie) podczas wizyty. Pozwalają witrynie zapamiętać informacje o Twojej wizycie — np. preferencje lub status logowania — i odczytać je przy kolejnej wizycie.

**Local storage** (pamięć lokalna) to podobna technologia wbudowana w przeglądarkę. Przechowuje dane na Twoim urządzeniu bez daty ważności (chyba że zostaną ręcznie usunięte). W przeciwieństwie do cookies, dane z local storage nie są automatycznie wysyłane do serwerów przy każdym żądaniu.

**Session storage** (pamięć sesji) działa jak local storage, ale jest automatycznie usuwana po zamknięciu karty przeglądarki.

Wszystkie trzy technologie są stosowane na platformie Nevumo. Niniejsza polityka obejmuje je wszystkie.

---

### 2. Kto korzysta z tych technologii?

Nevumo korzysta z cookies i pamięci przeglądarki bezpośrednio (**własne**) oraz pozwala wybranym usługom zewnętrznym umieszczać własne pliki cookies na Twoim urządzeniu (**cookies podmiotów trzecich**). Wszyscy dostawcy zewnętrzni są wymienieni w tabeli w rozdziale 5.

---

### 3. Kategorie stosowanych plików cookies

#### 3.1 Niezbędne
Konieczne do działania platformy. Bez nich nie możesz się zalogować, korzystać z usługi ani bezpiecznie poruszać się po stronie. Zawsze aktywne — nie wymagają zgody.

**Podstawa prawna:** Art. 6 ust. 1 lit. b) RODO — wykonanie umowy; art. 6 ust. 1 lit. f) RODO — uzasadniony interes w zakresie bezpieczeństwa platformy.

#### 3.2 Funkcjonalne
Zapamiętują Twoje preferencje i wybory (np. wybrany język, wybrane miasto, zamierzona rola jako klient lub usługodawca) w celu poprawy komfortu korzystania. Nie śledzą Cię na innych stronach internetowych.

**Podstawa prawna:** Art. 6 ust. 1 lit. f) RODO — uzasadniony interes w zapewnieniu spójnego doświadczenia użytkownika. Możesz wnieść sprzeciw w dowolnym momencie przez panel Ustawienia cookies w stopce witryny.

#### 3.3 Analityczne
Pomagają nam zrozumieć, jak odwiedzający korzystają z Nevumo — które strony są odwiedzane, jak długo użytkownicy na nich przebywają i skąd pochodzą. Dane te są agregowane i służą do ulepszenia platformy.

Korzystamy z **Google Analytics 4 (GA4)** w trybie **Advanced Consent Mode v2**. Oznacza to:
- Jeśli odrzucisz cookies analityczne, GA4 nadal się ładuje, ale wysyła jedynie anonimowe, bezplikowe „pingi".
- Google wykorzystuje modelowanie statystyczne do szacowania trendów ruchu — bez identyfikowania Cię osobiście.
- Żadne cookies analityczne (`_ga`, `_ga_[ID]`) nie są ustawiane bez Twojej wyraźnej zgody.

Wdrożenie to jest ujawniane zgodnie z wymogami Google Advanced Consent Mode v2.

**Podstawa prawna:** Art. 6 ust. 1 lit. a) RODO — Twoja zgoda.

#### 3.4 Marketingowe
Aktualnie Nevumo nie stosuje marketingowych plików cookies. Kategoria ta jest zarezerwowana na przyszłe funkcje (np. remarketing). Aktualnie żadne cookies marketingowe nie są ustawiane.

**Podstawa prawna (gdy stosowane):** Art. 6 ust. 1 lit. a) RODO — Twoja zgoda.

---

### 4. Twój numer telefonu w local storage

Gdy podasz numer telefonu na platformie (np. podczas składania zapytania o usługę), tymczasowo przechowujemy go w pamięci lokalnej przeglądarki pod kluczem `nevumo_phone`. Umożliwia to automatyczne uzupełnianie numeru telefonu podczas kolejnych wizyt.

**Podstawa prawna:** Art. 6 ust. 1 lit. f) RODO — uzasadniony interes w zmniejszeniu uciążliwości i poprawie doświadczenia użytkownika. Dane te nigdy nie opuszczają Twojego urządzenia, chyba że wyraźnie prześlesz formularz. Możesz je usunąć w dowolnym momencie, czyszcząc local storage przeglądarki lub poprzez ustawienia konta.

---

### 5. Pełna lista plików cookies i wpisów pamięci przeglądarki

| Nazwa / Klucz | Typ pamięci | Cel | Dostawca | Czas przechowywania | Kategoria | Podstawa prawna |
|---|---|---|---|---|---|---|
| `nevumo_consent` | Cookie (własny) | Rejestruje Twoje wybory dotyczące zgody na cookies | Nevumo | 12 miesięcy | Niezbędne | Obowiązek prawny (art. 7 RODO) |
| `lang` | Cookie (własny) | Przechowuje wybrany język wyświetlania | Nevumo | 30 dni | Funkcjonalne | Uzasadniony interes |
| `_ga` | Cookie (podmiot trzeci) | Google Analytics — rozróżnia unikatowych użytkowników | Google | 13 miesięcy | Analityczne | Zgoda |
| `_ga_[ID]` | Cookie (podmiot trzeci) | Google Analytics — śledzenie sesji | Google | 13 miesięcy | Analityczne | Zgoda |
| `__stripe_mid` | Cookie (podmiot trzeci) | Zapobieganie oszustwom Stripe — odcisk urządzenia | Stripe | 1 rok | Niezbędne | Uzasadniony interes / Umowa |
| `__stripe_sid` | Cookie (podmiot trzeci) | Zapobieganie oszustwom Stripe — identyfikator sesji | Stripe | 30 minut | Niezbędne | Uzasadniony interes / Umowa |
| `nevumo_auth_token` | Local Storage | JWT uwierzytelniania — utrzymuje sesję logowania | Nevumo | Sesja / 30 dni | Niezbędne | Umowa |
| `nevumo_auth_user` | Local Storage | Zbuforowane dane profilu użytkownika (id, imię, rola) | Nevumo | Sesja / 30 dni | Niezbędne | Umowa |
| `nevumo_phone` | Local Storage | Autouzupełnianie numeru telefonu | Nevumo | Do wyczyszczenia | Funkcjonalne | Uzasadniony interes |
| `nevumo_intent` | Local Storage | Przechowuje wybraną rolę (klient / usługodawca) | Nevumo | Sesja | Funkcjonalne | Uzasadniony interes |
| `nevumo_city_preference` | Local Storage | Przechowuje wybrane miasto | Nevumo | Do wyczyszczenia | Funkcjonalne | Uzasadniony interes |
| `nevumo_last_url` | Local Storage | Ostatnio odwiedzona strona dla inteligentnego przekierowania PWA | Nevumo | Do wyczyszczenia | Funkcjonalne | Uzasadniony interes |
| `nevumo_auth_email` | Session Storage | Tymczasowo przechowuje adres e-mail podczas rejestracji | Nevumo | Sesja (karta) | Niezbędne | Umowa |

> **Uwaga dotycząca cookies Stripe:** `__stripe_mid` i `__stripe_sid` są ustawiane wyłącznie na stronach, na których odbywa się przetwarzanie płatności. Stripe.js nie jest ładowany na innych stronach.

> **Uwaga dotycząca GA4 Advanced Consent Mode v2:** Gdy odrzucisz cookies analityczne, Google Analytics działa w trybie bezplikowym. Na Twoim urządzeniu nie są ustawiane cookies `_ga` ani `_ga_[ID]`. Google może używać zagregowanych, zanonimizowanych sygnałów do modelowania statystyk ruchu, zgodnie z frameworkiem Advanced Consent Mode v2.

> **Uwaga dotycząca cookie `lang`:** To cookie jest ściśle funkcjonalne — przechowuje Twoje preferencje językowe, aby platforma wyświetlała się w wybranym przez Ciebie języku. Nie śledzi Twojej aktywności i nie wymaga zgody na podstawie art. 5 ust. 3 Dyrektywy o prywatności i łączności elektronicznej.

---

### 6. Jak zarządzać preferencjami

**Za pomocą banera cookies:** Przy pierwszej wizycie na Nevumo pojawia się baner umożliwiający akceptację wszystkich, odrzucenie wszystkich lub dostosowanie preferencji według kategorii.

**Za pomocą Ustawień cookies:** Link „Ustawienia cookies" jest zawsze dostępny w stopce witryny. Kliknij go w dowolnym momencie, aby przejrzeć lub zmienić swoje wybory.

**Za pomocą przeglądarki:** Możesz usuwać, blokować lub zarządzać wszystkimi plikami cookies w ustawieniach przeglądarki. Pamiętaj, że zablokowanie niezbędnych cookies może uniemożliwić prawidłowe działanie platformy.

| Przeglądarka | Ścieżka ustawień |
|---|---|
| Chrome | Ustawienia → Prywatność i bezpieczeństwo → Pliki cookie i inne dane witryn |
| Firefox | Ustawienia → Prywatność i bezpieczeństwo → Dane cookie i witryn |
| Safari | Ustawienia → Prywatność → Zarządzaj danymi witryn |
| Edge | Ustawienia → Pliki cookie i uprawnienia witryn |

**Za pomocą pamięci przeglądarki:** Możesz wyczyścić dane local/session storage za pomocą narzędzi deweloperskich przeglądarki (Aplikacja → Local Storage / Session Storage → nevumo.com → Usuń wszystko).

---

### 7. Podmioty przetwarzające danych (zewnętrzni procesorzy)

| Procesor | Rola | Polityka prywatności |
|---|---|---|
| Google LLC | Analityka (GA4) | https://policies.google.com/privacy |
| Stripe, Inc. | Przetwarzanie płatności (zapobieganie oszustwom) | https://stripe.com/privacy |
| Vercel Inc. | Hosting frontendu | https://vercel.com/legal/privacy-policy |
| Railway Corp. | Hosting backendu API | https://railway.app/legal/privacy |
| Neon Inc. | Hosting bazy danych PostgreSQL | https://neon.tech/privacy-policy |
| Upstash Inc. | Hosting pamięci podręcznej Redis | https://upstash.com/trust/privacy.pdf |
| Cloudflare Inc. | Przechowywanie mediów (R2) | https://www.cloudflare.com/privacypolicy/ |

Wszyscy wymienieni wyżej procesorzy podpisali z Nevumo umowy powierzenia przetwarzania danych (DPA) w zakresie wymaganym przez RODO.

---

### 8. Przekazywanie danych poza EOG

Infrastruktura hostingowa Nevumo jest zlokalizowana w Stanach Zjednoczonych. Wszystkie transfery poza Europejski Obszar Gospodarczy (EOG) są zabezpieczone Standardowymi Klauzulami Umownymi (SCC) zatwierdzonymi przez Komisję Europejską.

Dodatkowo Google LLC i Cloudflare Inc. uczestniczą w programie EU–US Data Privacy Framework (DPF), stanowiącym dodatkowe zabezpieczenie transferu.

| Odbiorca | Kraj | Zabezpieczenie |
|---|---|---|
| Google LLC (GA4) | USA | SCC + EU-US DPF |
| Stripe, Inc. | USA | SCC |
| Vercel Inc. | USA | SCC |
| Railway Corp. | USA | SCC |
| Neon Inc. | USA | SCC |
| Upstash Inc. | USA | SCC |
| Cloudflare Inc. (R2) | USA | SCC + EU-US DPF |

---

### 9. Ponowna zgoda

Poprosimy o ponowną zgodę po 12 miesiącach lub wcześniej, jeśli dokonamy istotnych zmian w rodzajach stosowanych przez nas cookies.

---

### 10. Zmiany niniejszej polityki

Niniejsza Polityka cookies może być od czasu do czasu aktualizowana. „Data wejścia w życie" widoczna na górze strony zawsze wskazuje datę najnowszej wersji. O istotnych zmianach poinformujemy poprzez baner zgody na cookies.

---

### 11. Kontakt i skargi

**Administrator danych:**  
„PHILIPS CENTRE BULGARIA" Sp. z o.o. (marka handlowa Nevumo)  
EIK: 175369610  
77 Petko Karavelov Blvd., kl. A, m. 19, dzielnica Triaditza, 1408 Sofia, Bułgaria  
E-mail: privacy@nevumo.com

**Organ nadzorczy (Bułgaria — wiodący organ):**  
Komisja Ochrony Danych Osobowych (CPDP / КЗЛД)  
ul. Prof. Cvetan Lazarov 2, Sofia 1592, Bułgaria  
https://www.cpdp.bg

**Organ nadzorczy (Polska — organ właściwy):**  
Urząd Ochrony Danych Osobowych (UODO)  
ul. Stawki 2, 00-193 Warszawa  
https://uodo.gov.pl

---
---

# 🇧🇬 БЪЛГАРСКА ВЕРСИЯ

## Политика за бисквитките

**Администратор на данни:** „ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ" ООД (търговска марка **Nevumo**)  
**ЕИК:** 175369610  
**Адрес:** бул. Петко Каравелов бл. 77, вх. А, ап. 19, р-н Триадица, п.к. 1408, гр. София, България  
**Контакт:** privacy@nevumo.com  
**Дата на влизане в сила:** 2026-05-01 | **Версия:** 2.0

---

### 1. Какво представляват бисквитките и браузърното хранилище?

**Бисквитките (cookies)** са малки текстови файлове, които даден уебсайт поставя на вашето устройство (компютър, телефон, таблет) при посещение. Те позволяват на сайта да запомни информация за вашата сесия — например предпочитания или статус на влизане — и да я прочете при следващо посещение.

**Local storage (локалното хранилище)** е подобна технология, вградена в браузъра. Съхранява данни на вашето устройство без срок на изтичане (освен ако не бъдат ръчно изтрити). За разлика от бисквитките, данните в local storage не се изпращат автоматично до нашите сървъри при всяка заявка.

**Session storage (сесийното хранилище)** работи като local storage, но се изтрива автоматично при затваряне на браузърния таб.

И трите технологии се използват в платформата Nevumo. Настоящата политика обхваща всички от тях.

---

### 2. Кой използва тези технологии?

Nevumo използва бисквитки и браузърно хранилище директно (**собствени**) и позволява на избрани услуги на трети страни да поставят свои бисквитки на вашето устройство (**бисквитки на трети страни**). Всички доставчици на трети страни са изброени в таблицата в раздел 5.

---

### 3. Категории бисквитки, които използваме

#### 3.1 Задължително необходими
Те са от съществено значение за функционирането на платформата. Без тях не можете да влезете в профила си, да използвате услугата или да навигирате сигурно в сайта. Те са винаги активни — не изискват вашето съгласие.

**Правно основание:** Чл. 6, ал. 1, б. „б)" GDPR — изпълнение на договор; чл. 6, ал. 1, б. „е)" GDPR — легитимен интерес за сигурността на платформата.

#### 3.2 Функционални
Запомнят вашите предпочитания и избори (напр. избран език, избран град, предвидена роля като клиент или доставчик), за да подобрят вашето преживяване. Те не ви проследяват в други уебсайтове.

**Правно основание:** Чл. 6, ал. 1, б. „е)" GDPR — легитимен интерес за осигуряване на последователно потребителско преживяване. Можете да възразите по всяко време чрез панела за настройки на бисквитките в долния колонтитул на сайта.

#### 3.3 Аналитични
Помагат ни да разберем как посетителите използват Nevumo — кои страници се посещават, колко дълго остават потребителите и откъде идват. Тези данни са агрегирани и се използват за подобряване на платформата.

Използваме **Google Analytics 4 (GA4)** с режим **Advanced Consent Mode v2**. Това означава:
- Ако откажете аналитичните бисквитки, GA4 все още се зарежда, но изпраща само анонимизирани „сигнали" без бисквитки.
- Google използва статистическо моделиране за оценка на тенденциите в трафика — без да ви идентифицира лично.
- Никакви аналитични бисквитки (`_ga`, `_ga_[ID]`) не се поставят без вашето изрично съгласие.

Тази имплементация се оповестява в съответствие с изискванията на Google Advanced Consent Mode v2.

**Правно основание:** Чл. 6, ал. 1, б. „а)" GDPR — вашето съгласие.

#### 3.4 Маркетингови
В момента Nevumo не използва маркетингови бисквитки. Тази категория е запазена за бъдещи функции (напр. ремаркетинг). В момента не се поставят маркетингови бисквитки.

**Правно основание (при използване):** Чл. 6, ал. 1, б. „а)" GDPR — вашето съгласие.

---

### 4. Вашият телефонен номер в local storage

Когато предоставите телефонен номер на платформата (напр. при изпращане на запитване за услуга), го съхраняваме временно в локалното хранилище на браузъра ви под ключ `nevumo_phone`. Това позволява автоматичното попълване на вашия телефонен номер при последващи посещения.

**Правно основание:** Чл. 6, ал. 1, б. „е)" GDPR — легитимен интерес за намаляване на затруднения и подобряване на потребителското преживяване. Тези данни никога не напускат вашето устройство, освен ако изрично не изпратите формуляр. Можете да ги изтриете по всяко време, като изчистите local storage на браузъра си, или чрез настройките на профила.

---

### 5. Пълен списък на бисквитките и записите в браузърното хранилище

| Наименование / Ключ | Тип хранилище | Цел | Доставчик | Период на съхранение | Категория | Правно основание |
|---|---|---|---|---|---|---|
| `nevumo_consent` | Бисквитка (собствена) | Записва вашите избори за съгласие с бисквитки | Nevumo | 12 месеца | Необходими | Законово задължение (чл. 7 GDPR) |
| `lang` | Бисквитка (собствена) | Съхранява избрания от вас език за показване | Nevumo | 30 дни | Функционални | Легитимен интерес |
| `_ga` | Бисквитка (трета страна) | Google Analytics — разграничава уникални потребители | Google | 13 месеца | Аналитични | Съгласие |
| `_ga_[ID]` | Бисквитка (трета страна) | Google Analytics — проследяване на сесия | Google | 13 месеца | Аналитични | Съгласие |
| `__stripe_mid` | Бисквитка (трета страна) | Предотвратяване на измами от Stripe — пръстов отпечатък на устройство | Stripe | 1 година | Необходими | Легитимен интерес / Договор |
| `__stripe_sid` | Бисквитка (трета страна) | Предотвратяване на измами от Stripe — идентификатор на сесия | Stripe | 30 минути | Необходими | Легитимен интерес / Договор |
| `nevumo_auth_token` | Local Storage | JWT за удостоверяване — поддържа ви влезли в профила | Nevumo | Сесия / 30 дни | Необходими | Договор |
| `nevumo_auth_user` | Local Storage | Кеширани данни за потребителски профил (id, ime, роля) | Nevumo | Сесия / 30 дни | Необходими | Договор |
| `nevumo_phone` | Local Storage | Автоматично попълване на телефонен номер | Nevumo | До изчистване | Функционални | Легитимен интерес |
| `nevumo_intent` | Local Storage | Съхранява избраната роля (клиент / доставчик) | Nevumo | Сесия | Функционални | Легитимен интерес |
| `nevumo_city_preference` | Local Storage | Съхранява избрания град | Nevumo | До изчистване | Функционални | Легитимен интерес |
| `nevumo_last_url` | Local Storage | Последно посетена страница за PWA пренасочване | Nevumo | До изчистване | Функционални | Легитимен интерес |
| `nevumo_auth_email` | Session Storage | Временно съхранява имейл адрес по време на регистрация | Nevumo | Сесия (таб) | Необходими | Договор |

> **Забележка за бисквитките на Stripe:** `__stripe_mid` и `__stripe_sid` се задават само на страниците, на които се осъществява обработка на плащания. Stripe.js не се зарежда на другите страници.

> **Забележка за GA4 Advanced Consent Mode v2:** Когато откажете аналитичните бисквитки, Google Analytics работи в режим без бисквитки. На вашето устройство не се задават бисквитки `_ga` или `_ga_[ID]`. Google може да използва агрегирани, анонимизирани сигнали за моделиране на статистики за трафика, в съответствие с рамката Advanced Consent Mode v2.

> **Забележка за бисквитката `lang`:** Тази бисквитка е изцяло функционална — съхранява вашите езикови предпочитания, за да може платформата да се показва на избрания от вас език. Тя не проследява вашата активност и не изисква съгласие съгласно чл. 5, ал. 3 от Директивата за електронна поверителност.

---

### 6. Как да управлявате предпочитанията си

**Чрез банера за бисквитки:** При първото ви посещение на Nevumo се появява банер, позволяващ да приемете всички, да откажете всички или да персонализирате предпочитанията си по категории.

**Чрез Настройки за бисквитки:** Връзката „Настройки за бисквитки" е винаги достъпна в долния колонтитул на уебсайта. Кликнете върху нея по всяко време, за да прегледате или промените изборите си.

**Чрез вашия браузър:** Можете да изтривате, блокирате или управлявате всички бисквитки чрез настройките на браузъра. Имайте предвид, че блокирането на задължително необходимите бисквитки може да попречи на правилното функциониране на платформата.

| Браузър | Път до настройките |
|---|---|
| Chrome | Настройки → Поверителност и сигурност → Бисквитки и данни от сайтове |
| Firefox | Настройки → Поверителност и сигурност → Бисквитки и данни от сайтове |
| Safari | Настройки → Поверителност → Управление на данните от уебсайтове |
| Edge | Настройки → Бисквитки и разрешения за сайтове |

**Чрез браузърното хранилище:** Можете да изчистите данните в local/session storage чрез инструментите за разработчици на браузъра (Приложение → Local Storage / Session Storage → nevumo.com → Изтрий всичко).

---

### 7. Трети страни — обработващи данни

| Обработващ | Роля | Политика за поверителност |
|---|---|---|
| Google LLC | Анализи (GA4) | https://policies.google.com/privacy |
| Stripe, Inc. | Обработка на плащания (предотвратяване на измами) | https://stripe.com/privacy |
| Vercel Inc. | Хостинг на фронтенда | https://vercel.com/legal/privacy-policy |
| Railway Corp. | Хостинг на backend API | https://railway.app/legal/privacy |
| Neon Inc. | Хостинг на PostgreSQL база данни | https://neon.tech/privacy-policy |
| Upstash Inc. | Хостинг на Redis кеш | https://upstash.com/trust/privacy.pdf |
| Cloudflare Inc. | Съхранение на медии (R2) | https://www.cloudflare.com/privacypolicy/ |

Всички изброени по-горе обработващи данни са подписали с Nevumo споразумения за обработка на данни (DPA) в обхвата, изискван от GDPR.

---

### 8. Международни трансфери на данни

Хостинг инфраструктурата на Nevumo е базирана в Съединените щати. Всички трансфери извън Европейското икономическо пространство (ЕИП) са защитени чрез Стандартни договорни клаузи (СДК), одобрени от Европейската комисия.

Допълнително, Google LLC и Cloudflare Inc. участват в рамката ЕС–САЩ за защита на данните (EU–US Data Privacy Framework — DPF), което осигурява допълнителна защита при трансфера.

| Получател | Държава | Защита |
|---|---|---|
| Google LLC (GA4) | САЩ | СДК + EU-US DPF |
| Stripe, Inc. | САЩ | СДК |
| Vercel Inc. | САЩ | СДК |
| Railway Corp. | САЩ | СДК |
| Neon Inc. | САЩ | СДК |
| Upstash Inc. | САЩ | СДК |
| Cloudflare Inc. (R2) | САЩ | СДК + EU-US DPF |

---

### 9. Ново съгласие

Ще поискаме ново съгласие след 12 месеца или по-рано, ако направим съществени промени в видовете бисквитки, които използваме.

---

### 10. Промени в тази политика

Тази Политика за бисквитките може да бъде актуализирана периодично. „Датата на влизане в сила" в началото на страницата винаги показва датата на последната версия. За съществени промени ще бъдете уведомени чрез банера за съгласие с бисквитките.

---

### 11. Контакт и жалби

**Администратор на данни:**  
„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ" ООД (търговска марка Nevumo)  
ЕИК: 175369610  
бул. Петко Каравелов бл. 77, вх. А, ап. 19, р-н Триадица, п.к. 1408, гр. София, България  
Имейл: privacy@nevumo.com

**Надзорен орган (България — водещ надзорен орган):**  
Комисия за защита на личните данни (КЗЛД)  
бул. „Проф. Цветан Лазаров" № 2, София 1592, България  
https://www.cpdp.bg

**Надзорен орган (Полша — засегнат орган):**  
Urząd Ochrony Danych Osobowych (UODO)  
ul. Stawki 2, 00-193 Warszawa  
https://uodo.gov.pl
