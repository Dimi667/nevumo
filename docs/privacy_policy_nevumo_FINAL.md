# Nevumo — Privacy Policy (FINAL — All Language Versions)
**Document version:** 2026-05-11
**Status:** FINAL DRAFT — requires legal review before publication
**Legal entity:** „ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ" ООД | EIK: 175369610
**Brand:** Nevumo

---

# ENGLISH VERSION

## Privacy Policy

**Effective date:** 11 May 2026
**Document version:** 2026-05-11

---

### 1. Data Controller

The data controller responsible for processing your personal data is:

**„PHILIPS CENTER BULGARIA" Ltd** (trading as **Nevumo**)
UIC: 175369610
Address: 77 Petko Karavelov Blvd, Entrance A, Apt. 19, Triaditza District, 1408 Sofia, Bulgaria
Email: privacy@nevumo.com

In this document, the company is referred to as "**Nevumo**".

For all privacy-related questions, contact us at: **privacy@nevumo.com**

---

### 2. What Is Nevumo?

Nevumo is an online marketplace that connects clients seeking local services (e.g., cleaning, plumbing, massage) with service providers. **Nevumo acts solely as an intermediary** — we are not a party to the contract concluded between a client and a service provider, and we do not hold or transfer funds on behalf of users.

Nevumo is registered in Bulgaria and subject to the supervision of the **Commission for Personal Data Protection (CPDP / КЗЛД)** as the Lead Supervisory Authority under GDPR.

---

### 3. What Data We Collect and Why

#### 3.1 Account Registration

| Data | Purpose | Legal Basis |
|------|---------|-------------|
| Email address | Account creation, login, transactional communications | Contract — Art. 6(1)(b) GDPR |
| Password (bcrypt hash — never stored in plain text) | Account security | Contract — Art. 6(1)(b) GDPR |
| Role (client / service provider) | Platform functionality | Contract — Art. 6(1)(b) GDPR |
| Age confirmation (18+) | Legal requirement — minimum age compliance | Legal obligation — Art. 6(1)(c) GDPR |

**Minimum age:** Nevumo is exclusively for users aged 18 and over. By registering, you confirm that you meet this requirement.

#### 3.2 Provider Profile

| Data | Purpose | Legal Basis |
|------|---------|-------------|
| Name, profile description, service category | Public provider profile | Contract — Art. 6(1)(b) GDPR |
| Profile photo (optional) | Public display | Contract — Art. 6(1)(b) GDPR |
| Phone number | Lead delivery, client-provider communication | Contract — Art. 6(1)(b) GDPR |
| Location / city | Service area matching | Contract — Art. 6(1)(b) GDPR |
| Services and prices | Marketplace listing | Contract — Art. 6(1)(b) GDPR |
| Performance indicators (completed jobs count, average rating, verification level) | Automatic calculation of ranking position and public status badge | Contract — Art. 6(1)(b) GDPR |

#### 3.3 Service Requests (Leads)

| Data | Purpose | Legal Basis |
|------|---------|-------------|
| Request details (category, date, description) | Matching clients with providers | Contract — Art. 6(1)(b) GDPR |
| Contact information shared in the lead | Communication between parties | Contract — Art. 6(1)(b) GDPR |
| Lead status history | Platform functionality and dispute resolution | Contract — Art. 6(1)(b) GDPR |

#### 3.4 Security and Technical Data

| Data | Purpose | Legal Basis |
|------|---------|-------------|
| IP address (hashed) | Security, rate limiting, fraud prevention | Legitimate interest — Art. 6(1)(f) GDPR |
| User agent (browser/device) | Security and bug detection | Legitimate interest — Art. 6(1)(f) GDPR |
| Authentication logs | Security monitoring | Legitimate interest — Art. 6(1)(f) GDPR |

Our legitimate interest: maintaining the security and integrity of the platform and protecting our users from fraudulent activity.

#### 3.5 Analytics

| Data | Purpose | Legal Basis |
|------|---------|-------------|
| Google Analytics 4 (GA4) usage data | Understanding user behaviour, improving the platform | Consent — Art. 6(1)(a) GDPR |

**Important:** We use GA4 in **Advanced Consent Mode v2**. GA4 loads only after you grant consent to analytics cookies. If you refuse, GA4 loads in "cookieless" mode and Google models aggregate data (~85% accuracy) without tracking you individually. You can withdraw consent at any time via the **Cookie Settings** link in the footer.

#### 3.6 Communications

| Data | Purpose | Legal Basis |
|------|---------|-------------|
| Transactional emails (account confirmation, lead notifications, password reset) | Service delivery | Contract — Art. 6(1)(b) GDPR |
| Marketing emails (platform updates, tips) | Marketing | Consent — Art. 6(1)(a) GDPR |

You can unsubscribe from marketing emails at any time via the unsubscribe link in any marketing email.

#### 3.7 Claimed Provider Profiles (Article 14 GDPR)

Nevumo may create provider profiles using publicly available information (e.g., from directories and business listings) prior to a provider claiming their profile. If you claim a pre-created profile, you will receive an automated email notification pursuant to **Article 14 GDPR**, informing you of what personal data Nevumo holds, the source of that data, the purpose and legal basis of processing, and your rights.

---

### 4. Cookies and Local Storage

We use cookies and browser storage to operate the platform. Full details are in our **[Cookie Policy](/en/cookies)**.

| Key | Type | Purpose | Retention | Basis |
|-----|------|---------|-----------|-------|
| `nevumo_consent` | Cookie | Records your cookie preferences | 12 months | Necessary |
| `lang` | Cookie | Remembers your chosen language | 30 days | Functional |
| `_ga`, `_ga_*` | Cookie | GA4 analytics | 13 months | Consent |
| `__stripe_mid` | Cookie | Stripe fraud prevention (checkout only) | 1 year | Necessary |
| `__stripe_sid` | Cookie | Stripe fraud prevention (checkout only) | 30 min | Necessary |
| `nevumo_auth_token` | localStorage | Authentication (JWT) | 30 days | Contract |
| `nevumo_auth_user` | localStorage | User info cache | 30 days | Contract |
| `nevumo_phone` | localStorage | Phone number autofill convenience | Indefinite | Legitimate interest |
| `nevumo_intent` | localStorage | UX role preference at login | Session | Functional |
| `nevumo_city_preference` | localStorage | Remembers your preferred city | Indefinite | Functional |
| `nevumo_city` | Cookie | Stores the city selected by the user for homepage personalisation | 1 year | Functional |
| `nevumo_last_url` | localStorage | Last visited page for PWA smart redirect | Indefinite | Functional |
| `nevumo_auth_email` | sessionStorage | Email during registration flow | Session (tab) | Contract |

---

### 5. Who We Share Your Data With (Processors)

We share your data with the following processors, with whom we have Data Processing Agreements (DPAs) in place:

| Processor | Purpose | Country | Safeguard |
|-----------|---------|---------|-----------|
| **Google LLC** (GA4) | Platform analytics | USA | SCCs + DPF |
| **Stripe, Inc.** | Payment processing (BLIK, Przelewy24, cards) | USA | SCCs + DPF |
| **Resend, Inc.** | Transactional email delivery | USA | SCCs |
| **Vercel Inc.** | Frontend hosting | USA | SCCs |
| **Railway Corp.** | Backend API hosting | USA | SCCs |
| **Neon Inc.** | Database (PostgreSQL) | USA | SCCs |
| **Upstash Inc.** | Redis cache | USA | SCCs |
| **Cloudflare Inc.** | Image / file storage (R2) | USA | SCCs + DPF |

We do not sell your personal data. We do not share your data with third parties for their own marketing purposes.

---

### 6. Transfers Outside the EEA

All processors listed above that are based in the United States transfer data under appropriate safeguards:

- **Standard Contractual Clauses (SCCs)** — European Commission Implementing Decision 2021/914.
- **EU–US Data Privacy Framework (DPF)** — for processors certified under the DPF programme (Google, Stripe, Cloudflare).

You may request a copy of the applicable safeguards by contacting us at **privacy@nevumo.com**.

---

### 7. Automated Processing

Nevumo uses automated processing of provider data in two systems. Neither system produces legal effects, but both may significantly affect a provider's commercial visibility on the Platform.

#### 7.1 Provider Ranking

When displaying providers in search results and category listings, Nevumo's platform automatically calculates each provider's position based on the following parameters: profile completeness, average client rating, response rate and speed, recent activity, geographic match to the client's city, and account standing. No payment influences organic ranking position. Full details of the ranking parameters and their relative weights are published in the **Provider Terms**, Section 5.

Legal basis: Contract performance — Art. 6(1)(b) GDPR.

#### 7.2 Provider Status Badge

Nevumo automatically calculates a status badge for each provider profile (⚡ New Provider / ✓ Verified Specialist / ★ Top Specialist) based on measurable platform activity data: number of completed service requests, average client rating, and profile completeness (photo, description, active service listing). The badge is recalculated in real time upon any change to the underlying data and is displayed publicly on the provider's profile. Criteria are fully transparent and published in the **Provider Terms**, Section 5. Providers can influence their badge at any time by completing service requests and maintaining a complete profile.

Legal basis: Contract performance — Art. 6(1)(b) GDPR.

#### 7.3 Payment Fraud Detection (Stripe)

When processing payments, Stripe uses automated fraud detection. You have the right to request human review of any automated decision by Stripe that significantly affects you.

---

*These systems apply to provider accounts only. Client accounts are not subject to automated ranking or badge processing.*

---

### 8. How Long We Keep Your Data

| Data | Retention Period |
|------|-----------------|
| Active account (profile, services, leads) | Until account deletion |
| Data after account deletion | Max 30 days (encrypted backups) |
| Financial / Stripe records | 10 years (accounting regulations) |
| Security logs (hashed IPs) | 90 days |
| GA4 analytics data | 14 months |
| Cookie consent records | 24 months |
| Marketing consent records | Until withdrawal + 3 years |

---

### 9. Your Rights Under GDPR

- **Right of access (Art. 15):** Request a copy of all personal data we hold about you.
- **Right to rectification (Art. 16):** Request correction of inaccurate data.
- **Right to erasure (Art. 17):** Request deletion of your data ("right to be forgotten"), subject to legal retention obligations.
- **Right to data portability (Art. 20):** Request your data in machine-readable format via Settings → "Download my data."
- **Right to object (Art. 21):** Object to processing based on legitimate interest.
- **Right to restrict processing (Art. 18):** Request restriction of processing in certain circumstances.
- **Right to withdraw consent (Art. 7(3)):** Withdraw consent at any time without affecting prior processing.

To exercise your rights, contact us at **privacy@nevumo.com**. We will respond within **30 days** (extendable to 3 months for complex requests, with notice).

---

### 10. Right to Lodge a Complaint

**Lead Supervisory Authority (Bulgaria):**
Commission for Personal Data Protection (CPDP / КЗЛД)
2 Prof. Tsvetan Lazarov Blvd., Sofia 1592, Bulgaria
Website: www.cpdp.bg | Email: kzld@cpdp.bg

**Concerned Authority for Polish Users:**
Urząd Ochrony Danych Osobowych (UODO)
ul. Stawki 2, 00-193 Warsaw, Poland
Website: www.uodo.gov.pl | Helpline: 606-950-000

---

### 11. Changes to This Policy

We may update this Privacy Policy. Material changes will be notified by email and/or a prominent notice on the platform at least **14 days** before they take effect.

The current version is always available at nevumo.com/en/privacy.

---

### 12. Contact

**„PHILIPS CENTER BULGARIA" Ltd (Nevumo)**
77 Petko Karavelov Blvd, Entrance A, Apt. 19, Triaditza District, 1408 Sofia, Bulgaria
Email: privacy@nevumo.com

---
---

# BULGARIAN VERSION (ВЕРСИЯ НА БЪЛГАРСКИ)

## Политика за поверителност

**В сила от:** 11 май 2026 г.
**Версия на документа:** 2026-05-11

---

### 1. Администратор на лични данни

Администраторът, отговорен за обработването на вашите лични данни, е:

**„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ" ООД** (търговска марка: **Nevumo**)
ЕИК: 175369610
Адрес: бул. Петко Каравелов бл. 77, вх. А, ап. 19, р-н Триадица, п.к. 1408, гр. София, България
Имейл: privacy@nevumo.com

В настоящия документ дружеството се нарича „**Nevumo**".

За всички въпроси, свързани със защитата на личните ви данни: **privacy@nevumo.com**

---

### 2. Какво представлява Nevumo?

Nevumo е онлайн marketplace, свързващ клиенти, търсещи местни услуги (почистване, ВиК услуги, масажи и др.), с доставчици на тези услуги. **Nevumo действа единствено като посредник** — ние не сме страна по договора между клиент и доставчик и не задържаме или прехвърляме средства от името на потребителите.

Nevumo е регистрирано в България и подлежи на надзора на **Комисията за защита на личните данни (КЗЛД)** като водещ надзорен орган по GDPR.

---

### 3. Какви данни събираме и защо

#### 3.1 Регистрация на акаунт

| Данни | Цел | Правна основа |
|-------|-----|---------------|
| Имейл адрес | Създаване на акаунт, вход, транзакционни съобщения | Договор — чл. 6(1)(б) GDPR |
| Парола (bcrypt хеш — никога в открит текст) | Сигурност на акаунта | Договор — чл. 6(1)(б) GDPR |
| Роля (клиент / доставчик) | Функционалност на платформата | Договор — чл. 6(1)(б) GDPR |
| Потвърждение за възраст (18+) | Законово изискване | Законово задължение — чл. 6(1)(в) GDPR |

**Минимална възраст:** Nevumo е предназначена изключително за потребители на 18 и повече години.

#### 3.2 Профил на доставчика

| Данни | Цел | Правна основа |
|-------|-----|---------------|
| Име, описание, категория услуги | Публичен профил | Договор — чл. 6(1)(б) GDPR |
| Профилна снимка (незадължителна) | Публично показване | Договор — чл. 6(1)(б) GDPR |
| Телефонен номер | Доставка на поръчки, комуникация | Договор — чл. 6(1)(б) GDPR |
| Местоположение / град | Съвпадение на услуги по район | Договор — чл. 6(1)(б) GDPR |
| Услуги и цени | Обява в marketplace | Договор — чл. 6(1)(б) GDPR |
| Показатели за активност (брой завършени запитвания, средна оценка, ниво на верификация) | Автоматично изчисляване на позицията в класирането и значката за статус | Договор — чл. 6, ал. 1, б. „б" ОРЗД |

#### 3.3 Заявки за услуги (Leads)

| Данни | Цел | Правна основа |
|-------|-----|---------------|
| Детайли на заявката (категория, дата, описание) | Съвпадение клиент-доставчик | Договор — чл. 6(1)(б) GDPR |
| Контактна информация в заявката | Комуникация между страните | Договор — чл. 6(1)(б) GDPR |
| История на статусите | Функционалност и разрешаване на спорове | Договор — чл. 6(1)(б) GDPR |

#### 3.4 Технически данни и сигурност

| Данни | Цел | Правна основа |
|-------|-----|---------------|
| IP адрес (хеширан) | Сигурност, rate limiting, превенция на измами | Легитимен интерес — чл. 6(1)(е) GDPR |
| User agent (браузър/устройство) | Сигурност и диагностика | Легитимен интерес — чл. 6(1)(е) GDPR |
| Логове за удостоверяване | Мониторинг на сигурността | Легитимен интерес — чл. 6(1)(е) GDPR |

#### 3.5 Анализи

| Данни | Цел | Правна основа |
|-------|-----|---------------|
| Данни за използване чрез Google Analytics 4 | Подобряване на платформата | Съгласие — чл. 6(1)(а) GDPR |

**Важно:** Използваме GA4 в режим **Advanced Consent Mode v2**. GA4 се зарежда само след вашето съгласие. При отказ GA4 работи в "cookieless" режим — Google моделира обобщени данни (~85% точност) без индивидуално проследяване. Можете да оттеглите съгласието си чрез **Настройки за бисквитки** в долния колонтитул.

#### 3.6 Комуникации

| Данни | Цел | Правна основа |
|-------|-----|---------------|
| Транзакционни имейли | Предоставяне на услугата | Договор — чл. 6(1)(б) GDPR |
| Маркетингови имейли | Маркетинг | Съгласие — чл. 6(1)(а) GDPR |

#### 3.7 Предварително заявени профили (чл. 14 GDPR)

Nevumo може да създаде профил въз основа на публично достъпна информация преди доставчикът да го е потвърдил. При потвърждаване ще получите автоматично имейл известие по **чл. 14 GDPR** с информация за събраните данни, техния източник, целта на обработването и вашите права.

---

### 4. Бисквитки и локално хранилище

| Ключ | Тип | Цел | Съхранение | Основание |
|------|-----|-----|------------|-----------|
| `nevumo_consent` | Бисквитка | Запис на cookie съгласие | 12 месеца | Задължителна |
| `lang` | Бисквитка | Избран език | 30 дни | Функционална |
| `_ga`, `_ga_*` | Бисквитка | GA4 анализи | 13 месеца | Съгласие |
| `__stripe_mid` | Бисквитка | Stripe fraud prevention (само плащане) | 1 година | Задължителна |
| `__stripe_sid` | Бисквитка | Stripe fraud prevention (само плащане) | 30 мин | Задължителна |
| `nevumo_auth_token` | localStorage | Удостоверяване (JWT) | 30 дни | Договор |
| `nevumo_auth_user` | localStorage | Кеш с данни за потребителя | 30 дни | Договор |
| `nevumo_phone` | localStorage | Автоматично попълване на телефон | Неопределено | Легитимен интерес |
| `nevumo_intent` | localStorage | UX предпочитание за роля при вход | Сесия | Функционален |
| `nevumo_city_preference` | localStorage | Предпочитан град | Неопределено | Функционален |
| `nevumo_city` | Бисквитка | Съхранява избрания от потребителя град за персонализация на началната страница | 1 година | Функционален |
| `nevumo_last_url` | localStorage | Последно посетена страница за PWA пренасочване | Неопределено | Функционален |
| `nevumo_auth_email` | sessionStorage | Имейл по време на регистрация | Сесия (таб) | Договор |

Пълни подробности: **[Политика за бисквитки](/bg/cookies)**

---

### 5. С кого споделяме данните ви

| Обработващ | Цел | Държава | Защитна мярка |
|------------|-----|---------|---------------|
| **Google LLC** (GA4) | Анализи | САЩ | SCCs + DPF |
| **Stripe, Inc.** | Плащания (BLIK, Przelewy24, карти) | САЩ | SCCs + DPF |
| **Resend, Inc.** | Транзакционни имейли | САЩ | SCCs |
| **Vercel Inc.** | Frontend хостинг | САЩ | SCCs |
| **Railway Corp.** | Backend API хостинг | САЩ | SCCs |
| **Neon Inc.** | База данни (PostgreSQL) | САЩ | SCCs |
| **Upstash Inc.** | Redis кеш | САЩ | SCCs |
| **Cloudflare Inc.** | Снимки / R2 Storage | САЩ | SCCs + DPF |

Не продаваме личните ви данни. Не ги споделяме с трети страни за техни маркетингови цели.

---

### 6. Предаване на данни извън ЕИП

Всички обработващи в САЩ предават данни при подходящи гаранции:

- **Стандартни договорни клаузи (SCCs)** — Решение 2021/914 на ЕК.
- **EU–US Data Privacy Framework (DPF)** — за сертифицираните обработващи (Google, Stripe, Cloudflare).

Можете да поискате копие от гаранциите на **privacy@nevumo.com**.

---

### 7. Автоматизирано обработване

Nevumo прилага автоматизирано обработване на данни на Доставчиците в две системи. Нито една от тях не произвежда правни последици, но и двете могат значително да засегнат търговската видимост на Доставчика в Платформата.

#### 7.1 Класиране на Доставчиците

При показване на Доставчиците в резултатите от търсенето и в листингите по категории Платформата автоматично изчислява позицията на всеки Доставчик въз основа на следните параметри: пълнота на профила, средна оценка от клиенти, степен и скорост на отговор, скорошна активност в Платформата, географско съответствие с града на клиента и статус на акаунта. Плащането не влияе на органичната позиция в класирането. Пълна информация за параметрите за класиране и относителните им тежести е публикувана в **Условията за Доставчици**, чл. 5.

Правно основание: изпълнение на договор — чл. 6, ал. 1, б. „б" от ОРЗД.

#### 7.2 Значка за статус на Доставчика

Nevumo автоматично изчислява значка за статус за всеки профил на Доставчик (⚡ Нов Доставчик / ✓ Верифициран специалист / ★ Топ специалист) въз основа на измерими данни за активност: брой завършени запитвания, средна оценка от клиенти и пълнота на профила (снимка, описание, активна обява за услуга). Значката се преизчислява в реално време при всяка промяна на изходните данни и се показва публично в профила на Доставчика. Критериите са напълно прозрачни и публикувани в **Условията за Доставчици**, чл. 5. Доставчикът може по всяко време да повлияе на своята значка, като изпълнява запитвания и поддържа попълнен профил.

Правно основание: изпълнение на договор — чл. 6, ал. 1, б. „б" от ОРЗД.

#### 7.3 Засичане на платежни измами (Stripe)

При обработка на плащания Stripe използва автоматизирано засичане на измами. Имате право да поискате намеса на човек при всяко автоматизирано решение на Stripe, което ви засяга съществено.

---

*Системите по т. 7.1 и т. 7.2 се отнасят само за акаунти на Доставчици. Акаунтите на Клиенти не подлежат на автоматизирано класиране или присвояване на значки.*

---

### 8. Срокове на съхранение

| Данни | Срок |
|-------|------|
| Активен акаунт | До изтриване от потребителя |
| Данни след изтриване на акаунт | Макс. 30 дни (криптирани backups) |
| Финансови записи / Stripe | 10 години (счетоводно законодателство) |
| Логове за сигурност (хеширани IP) | 90 дни |
| GA4 данни | 14 месеца |
| Записи за cookie съгласие | 24 месеца |
| Записи за маркетингово съгласие | До оттегляне + 3 години |

---

### 9. Вашите права по GDPR

- **Право на достъп (чл. 15):** Копие от всички данни, които пазим за вас.
- **Право на коригиране (чл. 16):** Коригиране на неточни данни.
- **Право на изтриване (чл. 17):** „Право да бъдеш забравен", при спазване на законовите задължения за съхранение.
- **Право на преносимост (чл. 20):** Данните ви в машинночетим формат чрез Настройки → „Изтегли данните ми".
- **Право на възражение (чл. 21):** Срещу обработване въз основа на легитимен интерес.
- **Право на ограничаване (чл. 18):** При определени обстоятелства.
- **Право на оттегляне на съгласие (чл. 7(3)):** По всяко време, без да засяга предишното обработване.

Свържете се с нас на **privacy@nevumo.com**. Отговаряме в срок от **30 дни**.

---

### 10. Право на жалба

**Водещ надзорен орган (България):**
Комисия за защита на личните данни (КЗЛД)
бул. „Проф. Цветан Лазаров" №2, София 1592
www.cpdp.bg | kzld@cpdp.bg

**Засегнат орган за полски потребители:**
Urząd Ochrony Danych Osobowych (UODO)
ul. Stawki 2, 00-193 Варшава | www.uodo.gov.pl | 606-950-000

---

### 11. Промени в тази политика

При съществени промени ще уведомим потребителите по имейл и/или с известие на платформата поне **14 дни** преди влизането им в сила.

Актуалната версия е достъпна на nevumo.com/bg/privacy.

---

### 12. Контакт

**„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ" ООД (Nevumo)**
бул. Петко Каравелов бл. 77, вх. А, ап. 19, р-н Триадица, п.к. 1408, гр. София, България
Имейл: privacy@nevumo.com

---
---

# POLISH VERSION (WERSJA POLSKA)

## Polityka prywatności

**Data wejścia w życie:** 11 maja 2026 r.
**Wersja dokumentu:** 2026-05-11

---

### 1. Administrator danych osobowych

Administratorem odpowiedzialnym za przetwarzanie Twoich danych osobowych jest:

**„PHILIPS CENTER BULGARIA" Sp. z o.o.** (marka: **Nevumo**)
NIP bułgarski (UIC): 175369610
Adres: 77 Petko Karavelov Blvd, wejście A, m. 19, dzielnica Triaditza, 1408 Sofia, Bułgaria
E-mail: privacy@nevumo.com

W niniejszym dokumencie spółka jest nazywana „**Nevumo**".

We wszystkich kwestiach dotyczących ochrony danych: **privacy@nevumo.com**

---

### 2. Czym jest Nevumo?

Nevumo to internetowy marketplace łączący klientów poszukujących lokalnych usług (sprzątanie, hydraulika, masaż itp.) z dostawcami tych usług. **Nevumo działa wyłącznie jako pośrednik** — nie jesteśmy stroną umowy między klientem a dostawcą i nie przechowujemy ani nie przekazujemy środków pieniężnych.

Nevumo jest zarejestrowane w Bułgarii i podlega nadzorowi **Komisji Ochrony Danych Osobowych (КЗЛД)** jako Wiodącego Organu Nadzorczego w rozumieniu RODO. Dla użytkowników z Polski właściwym organem zaangażowanym jest **UODO**.

---

### 3. Jakie dane zbieramy i dlaczego

#### 3.1 Rejestracja konta

| Dane | Cel | Podstawa prawna |
|------|-----|-----------------|
| Adres e-mail | Utworzenie konta, logowanie, komunikacja transakcyjna | Umowa — art. 6 ust. 1 lit. b RODO |
| Hasło (hash bcrypt — nigdy w postaci jawnej) | Bezpieczeństwo konta | Umowa — art. 6 ust. 1 lit. b RODO |
| Rola (klient / dostawca usług) | Funkcjonalność platformy | Umowa — art. 6 ust. 1 lit. b RODO |
| Potwierdzenie wieku (18+) | Wymóg prawny | Obowiązek prawny — art. 6 ust. 1 lit. c RODO |

**Minimalny wiek:** Nevumo jest przeznaczona wyłącznie dla użytkowników, którzy ukończyli 18 lat.

#### 3.2 Profil dostawcy usług

| Dane | Cel | Podstawa prawna |
|------|-----|-----------------|
| Imię/nazwa, opis, kategoria usług | Publiczny profil dostawcy | Umowa — art. 6 ust. 1 lit. b RODO |
| Zdjęcie profilowe (opcjonalne) | Publiczne wyświetlanie | Umowa — art. 6 ust. 1 lit. b RODO |
| Numer telefonu | Dostarczanie zleceń, komunikacja | Umowa — art. 6 ust. 1 lit. b RODO |
| Lokalizacja / miasto | Dopasowanie usług do obszaru | Umowa — art. 6 ust. 1 lit. b RODO |
| Usługi i ceny | Ogłoszenie na marketplace | Umowa — art. 6 ust. 1 lit. b RODO |
| Wskaźniki aktywności (liczba ukończonych zleceń, średnia ocena, poziom weryfikacji) | Automatyczne obliczanie pozycji w rankingu i odznaki statusu | Umowa — art. 6 ust. 1 lit. b RODO |

#### 3.3 Zapytania o usługi (leads)

| Dane | Cel | Podstawa prawna |
|------|-----|-----------------|
| Szczegóły zapytania (kategoria, data, opis) | Dopasowanie klientów z dostawcami | Umowa — art. 6 ust. 1 lit. b RODO |
| Dane kontaktowe w zapytaniu | Komunikacja między stronami | Umowa — art. 6 ust. 1 lit. b RODO |
| Historia statusów zapytania | Funkcjonalność i rozwiązywanie sporów | Umowa — art. 6 ust. 1 lit. b RODO |

#### 3.4 Dane bezpieczeństwa i techniczne

| Dane | Cel | Podstawa prawna |
|------|-----|-----------------|
| Adres IP (zahashowany) | Bezpieczeństwo, rate limiting, zapobieganie oszustwom | Uzasadniony interes — art. 6 ust. 1 lit. f RODO |
| User agent (przeglądarka/urządzenie) | Bezpieczeństwo i diagnostyka | Uzasadniony interes — art. 6 ust. 1 lit. f RODO |
| Logi uwierzytelniania | Monitoring bezpieczeństwa | Uzasadniony interes — art. 6 ust. 1 lit. f RODO |

#### 3.5 Analityka

| Dane | Cel | Podstawa prawna |
|------|-----|-----------------|
| Dane o użytkowaniu (Google Analytics 4) | Ulepszanie platformy | Zgoda — art. 6 ust. 1 lit. a RODO |

**Ważne:** Używamy GA4 w trybie **Advanced Consent Mode v2**. GA4 ładuje się dopiero po wyrażeniu zgody. Przy odmowie GA4 działa w trybie „cookieless" — Google modeluje zbiorcze dane (~85% dokładności) bez indywidualnego śledzenia. Zgodę można wycofać w **Ustawieniach cookies** w stopce.

#### 3.6 Komunikacja

| Dane | Cel | Podstawa prawna |
|------|-----|-----------------|
| E-maile transakcyjne | Świadczenie usługi | Umowa — art. 6 ust. 1 lit. b RODO |
| E-maile marketingowe | Marketing | Zgoda — art. 6 ust. 1 lit. a RODO |

**Uwaga dla użytkowników z Polski:** Wysyłka komunikacji marketingowej wymaga osobnej zgody zgodnie z Prawem komunikacji elektronicznej (PKE) z dnia 10 listopada 2024 r.

#### 3.7 Profile przejęte przez Nevumo (art. 14 RODO)

Nevumo może tworzyć profile dostawców na podstawie publicznie dostępnych informacji przed ich przejęciem. W przypadku przejęcia profilu otrzymasz automatyczne powiadomienie e-mail zgodnie z **art. 14 RODO** zawierające informacje o przechowywanych danych, ich źródle, celu przetwarzania i Twoich prawach.

---

### 4. Pliki cookie i lokalne przechowywanie danych

| Klucz | Typ | Cel | Przechowywanie | Podstawa |
|-------|-----|-----|----------------|----------|
| `nevumo_consent` | Cookie | Zapis preferencji cookie | 12 miesięcy | Niezbędny |
| `lang` | Cookie | Zapamiętanie wybranego języka | 30 dni | Funkcjonalny |
| `_ga`, `_ga_*` | Cookie | Analityka GA4 | 13 miesięcy | Zgoda |
| `__stripe_mid` | Cookie | Zapobieganie oszustwom Stripe (tylko płatność) | 1 rok | Niezbędny |
| `__stripe_sid` | Cookie | Zapobieganie oszustwom Stripe (tylko płatność) | 30 min | Niezbędny |
| `nevumo_auth_token` | localStorage | Uwierzytelnianie (JWT) | 30 dni | Umowa |
| `nevumo_auth_user` | localStorage | Cache danych użytkownika | 30 dni | Umowa |
| `nevumo_phone` | localStorage | Automatyczne wypełnianie numeru telefonu | Nieokreślone | Uzasadniony interes |
| `nevumo_intent` | localStorage | Preferencja roli UX przy logowaniu | Sesja | Funkcjonalny |
| `nevumo_city_preference` | localStorage | Zapamiętane preferowane miasto | Nieokreślone | Funkcjonalny |
| `nevumo_city` | Cookie | Przechowuje miasto wybrane przez użytkownika do personalizacji strony głównej | 1 rok | Funkcjonalny |
| `nevumo_last_url` | localStorage | Ostatnio odwiedzona strona do przekierowania PWA | Nieokreślone | Funkcjonalny |
| `nevumo_auth_email` | sessionStorage | E-mail podczas rejestracji | Sesja (karta) | Umowa |

Szczegóły: **[Polityka cookies](/pl/cookies)**

---

### 5. Komu przekazujemy Twoje dane

| Podmiot przetwarzający | Cel | Kraj | Zabezpieczenie |
|-----------------------|-----|------|----------------|
| **Google LLC** (GA4) | Analityka | USA | SCCs + DPF |
| **Stripe, Inc.** | Płatności (BLIK, Przelewy24, karty) | USA | SCCs + DPF |
| **Resend, Inc.** | E-maile transakcyjne | USA | SCCs |
| **Vercel Inc.** | Hosting frontendu | USA | SCCs |
| **Railway Corp.** | Hosting API backendu | USA | SCCs |
| **Neon Inc.** | Baza danych (PostgreSQL) | USA | SCCs |
| **Upstash Inc.** | Cache Redis | USA | SCCs |
| **Cloudflare Inc.** | Przechowywanie plików/zdjęć (R2) | USA | SCCs + DPF |

Nie sprzedajemy Twoich danych. Nie udostępniamy ich podmiotom trzecim na ich własne cele marketingowe.

---

### 6. Przekazywanie danych poza EOG

Wszystkie wymienione podmioty przekazują dane przy odpowiednich zabezpieczeniach:

- **Standardowe klauzule umowne (SCCs)** — decyzja wykonawcza KE 2021/914.
- **EU–US Data Privacy Framework (DPF)** — dla podmiotów certyfikowanych (Google, Stripe, Cloudflare).

Kopię zabezpieczeń możesz uzyskać pod adresem **privacy@nevumo.com**.

---

### 7. Zautomatyzowane przetwarzanie

Nevumo stosuje zautomatyzowane przetwarzanie danych Dostawców w dwóch systemach. Żaden z nich nie wywołuje skutków prawnych, jednak oba mogą znacząco wpływać na widoczność handlową Dostawcy na Platformie.

#### 7.1 Ranking Dostawców

Przy wyświetlaniu Dostawców w wynikach wyszukiwania i listingach kategorii Platforma automatycznie oblicza pozycję każdego Dostawcy na podstawie następujących parametrów: kompletność profilu, średnia ocena klientów, wskaźnik i szybkość odpowiedzi, aktywność na Platformie, dopasowanie geograficzne do miasta klienta oraz status konta. Płatność nie wpływa na organiczną pozycję w rankingu. Pełne informacje o parametrach rankingowych i ich względnych wagach są opublikowane w **Regulaminie Dostawców**, §5.

Podstawa prawna: wykonanie umowy — art. 6 ust. 1 lit. b RODO.

#### 7.2 Odznaka statusu Dostawcy

Nevumo automatycznie oblicza odznakę statusu dla każdego profilu Dostawcy (⚡ Nowy Dostawca / ✓ Zweryfikowany Specjalista / ★ Najlepszy Specjalista) na podstawie mierzalnych danych aktywności: liczby ukończonych zleceń, średniej oceny klientów oraz kompletności profilu (zdjęcie, opis, aktywna oferta usługi). Odznaka jest przeliczana w czasie rzeczywistym przy każdej zmianie danych źródłowych i wyświetlana publicznie na profilu Dostawcy. Kryteria są w pełni przejrzyste i opublikowane w **Regulaminie Dostawców**, §5. Dostawca może wpływać na swoją odznakę w dowolnym momencie, realizując zlecenia i uzupełniając profil.

Podstawa prawna: wykonanie umowy — art. 6 ust. 1 lit. b RODO.

#### 7.3 Wykrywanie oszustw płatniczych (Stripe)

Stripe stosuje automatyczne wykrywanie oszustw przy płatnościach. Masz prawo żądać interwencji człowieka w przypadku zautomatyzowanej decyzji Stripe, która istotnie Cię dotyczy.

---

*Systemy opisane w pkt 7.1 i 7.2 dotyczą wyłącznie kont Dostawców. Konta Klientów nie podlegają zautomatyzowanemu rankingowi ani przyznawaniu odznak.*

---

### 8. Okresy przechowywania danych

| Dane | Okres przechowywania |
|------|---------------------|
| Aktywne konto | Do usunięcia konta |
| Dane po usunięciu konta | Maks. 30 dni (zaszyfrowane kopie) |
| Dokumentacja finansowa / Stripe | 10 lat (przepisy rachunkowości) |
| Logi bezpieczeństwa (zahashowane IP) | 90 dni |
| Dane GA4 | 14 miesięcy |
| Zapisy zgody na cookies | 24 miesiące |
| Zapisy zgody marketingowej | Do wycofania + 3 lata |

---

### 9. Twoje prawa wynikające z RODO

- **Prawo dostępu (art. 15):** Kopia wszystkich danych, które przechowujemy.
- **Prawo do sprostowania (art. 16):** Poprawienie niedokładnych danych.
- **Prawo do usunięcia (art. 17):** „Prawo do bycia zapomnianym", z zastrzeżeniem obowiązków prawnych.
- **Prawo do przenoszenia (art. 20):** Dane w formacie maszynowym przez Ustawienia → „Pobierz moje dane".
- **Prawo do sprzeciwu (art. 21):** Wobec przetwarzania opartego na uzasadnionym interesie.
- **Prawo do ograniczenia (art. 18):** W określonych okolicznościach.
- **Prawo do wycofania zgody (art. 7 ust. 3):** W dowolnym momencie, bez wpływu na wcześniejsze przetwarzanie.

Kontakt: **privacy@nevumo.com**. Odpowiadamy w ciągu **30 dni**.

---

### 10. Prawo do złożenia skargi

**Wiodący Organ Nadzorczy (Bułgaria):**
Komisja Ochrony Danych Osobowych (КЗЛД)
2 Prof. Tsvetan Lazarov Blvd., Sofia 1592, Bułgaria
www.cpdp.bg | kzld@cpdp.bg

**Organ zaangażowany dla użytkowników z Polski:**
Urząd Ochrony Danych Osobowych (UODO)
ul. Stawki 2, 00-193 Warszawa
www.uodo.gov.pl | 606-950-000

---

### 11. Zmiany niniejszej polityki

O istotnych zmianach poinformujemy e-mailem i/lub powiadomieniem na platformie co najmniej **14 dni** przed ich wejściem w życie.

Aktualna wersja dostępna na nevumo.com/pl/privacy.

---

### 12. Kontakt

**„PHILIPS CENTER BULGARIA" Sp. z o.o. (Nevumo)**
77 Petko Karavelov Blvd, wejście A, m. 19, dzielnica Triaditza, 1408 Sofia, Bułgaria
E-mail: privacy@nevumo.com

---
---

# COMPLIANCE CHECKLIST

## GDPR Art. 13 — всички реквизити:
- ✅ Юридическо наименование + адрес + ЕИК
- ✅ Privacy contact email
- ✅ Цели и правна основа по категория данни
- ✅ Всички processors с DPA статус
- ✅ Трансфери извън ЕИП (SCCs + DPF)
- ✅ Retention schedule
- ✅ 7 права на субекта на данни
- ✅ Право на жалба — КЗЛД + UODO
- ✅ Автоматизирано обработване: Ranking (§5) + Badge (§5) + Stripe (7.1, 7.2, 7.3)
- ✅ GA4 Advanced Consent Mode v2 disclosure
- ✅ Article 14 (claimed profiles)
- ✅ PKE consent бележка (Полша)
- ✅ Минимална възраст 18
- ✅ Пълна cookie/localStorage таблица (11 entries)

## Действия преди публикуване:
- [ ] Подписване на Google Analytics DPA (GA4 Admin панел)
- [ ] Сваляне и подписване на Resend DPA (resend.com/legal/dpa)
- [ ] Подписване на DPA с Vercel, Railway, Neon, Upstash, Cloudflare
- [ ] Създаване на privacy@nevumo.com mailbox
- [ ] Финален преглед от адвокат (~200–400 EUR)
- [ ] При преименуване на фирмата — актуализиране на документа
