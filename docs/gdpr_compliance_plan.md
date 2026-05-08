# Nevumo — GDPR & Legal Compliance Plan
**Версия:** 1.1 | **Дата:** 2026-05-01 | **Статус:** В прогрес

---

## Контекст

Nevumo е регистрирано в **България**. Основен launch пазар: **Варшава, Полша**.
Lead Supervisory Authority: **КЗЛД (България)**.
UODO (Полша) е "concerned authority" за полски потребители.

Правна рамка:
- GDPR (Регламент 2016/679)
- ЗЗЛД (България)
- Ustawa o świadczeniu usług drogą elektroniczną — UŚUDE (Полша)
- Prawo komunikacji elektronicznej — PKE (в сила 10.11.2024)
- Ustawa o prawach konsumenta — CRA (Полша, с Omnibus изменения 2023)
- Digital Services Act — DSA (Регламент 2022/2065)
- P2B Regulation (2019/1150)

---

## ЗАДАЧА 1 — Cookie Consent Banner
**Приоритет:** 🔴 КРИТИЧНО — преди launch  
**Тип:** Внедряване (код)  
**Статус:** ⏸️ Частично завършено

### Статус на подзадачи
- ✅ Banner + cookie storage
- ✅ consent_logs DB + endpoint
- ✅ GA4 default denied в layout.tsx
- ✅ Cookie Settings линк
- ✅ 7/7 тестове PASS
- ⏸️ Stripe.js блокиране — отложено до Stripe интеграция
- ✅ GA4 gtag('consent','update') при grant
- ❌ Mobile touch targets — проверка
- ❌ 12-месечен re-prompt — верификация

### Изисквания
- Accept All / Reject All / Customize на **първо ниво** — еднакъв размер и цвят на бутоните
- Reject All НЕ може да е скрит в Settings
- Без pre-checked toggles за non-essential категории
- Категории: Necessary (винаги ON) / Functional / Analytics / Marketing
- Локализиран на: PL, EN, BG (минимум)
- Mobile: touch targets мин. 44×44px
- Постоянен footer линк "Cookie Settings" / "Ustawienia cookies"
- Re-prompt след 12 месеца

### Съхранение на consent
- First-party cookie: `nevumo_consent` (не localStorage)
- Структура: `{ v: 2, ts: timestamp, categories: {...}, policy_version: "2026-05-01" }`
- **Сървърен audit log** в DB (нова таблица `consent_logs`)
- Полета: `id, user_id (nullable), session_hash, ip_hash, categories JSONB, policy_version, created_at`
- Retention: 24 месеца

### GA4 Consent Mode v2
- Default `denied` за EEA **преди** зареждане на gtag.js
- Параметри: `analytics_storage`, `ad_storage`, `ad_user_data`, `ad_personalization`
- Режим: **Advanced** — GA4 се зарежда с cookieless pings при отказ; Google моделира ~85% от данните. CNIL-приемливо при правилна имплементация. По-практично от Basic за marketplace.
- При grant: `gtag('consent', 'update', {...})`
- `region: ['EEA', 'GB']` задължително

### Stripe cookies
- `__stripe_mid`, `__stripe_sid` — strictly necessary само на checkout страница
- Stripe.js не се зарежда на останалите страници без consent

### Файлове за промяна
- `apps/web/components/ui/CookieConsentBanner.tsx` — нов компонент
- `apps/web/hooks/useCookieConsent.ts` — нов hook
- `apps/web/app/layout.tsx` — добавяне на banner + GA4 consent init
- `apps/api/routes/consent.py` — нов endpoint `POST /api/v1/consent`
- `apps/api/models.py` — нова таблица `consent_logs`
- Alembic миграция

### Translation keys (namespace: `cookie_banner`)
```
cookie_title, cookie_description, accept_all, reject_all, customize,
necessary_label, necessary_description, functional_label, functional_description,
analytics_label, analytics_description, marketing_label, marketing_description,
save_preferences, cookie_settings_link, last_updated
```
34 езика × 14 keys = 476 rows

---

## ЗАДАЧА 2 — Data Portability Endpoint
**Приоритет:** 🔴 КРИТИЧНО — преди launch  
**Тип:** Backend (код)  
**Статус:** ⬜ Не започнато

### Изисквания (GDPR чл. 20)
- `GET /api/v1/user/export` — JWT protected
- Формат: JSON (machine-readable)
- Съдържа: profile, phone, leads submitted, services listed, reviews, consent log
- Rate limit: 1 заявка / 24ч per user
- Response: файл за сваляне или имейл линк
- Срок за изпълнение: незабавно (< 2MB) или async job

### Файлове за промяна
- `apps/api/routes/user.py` — нов endpoint
- `apps/api/services/export_service.py` — нов service
- `apps/web/app/[lang]/provider/dashboard/settings/page.tsx` — бутон "Изтегли данните ми"
- `apps/web/app/[lang]/client/dashboard/settings/SettingsClient.tsx` — същото

---

## ЗАДАЧА 3 — Privacy Policy страница
**Приоритет:** 🔴 КРИТИЧНО — преди launch  
**Тип:** Страница + текст  
**Статус:** ⬜ Не започнато

### Route
`/[lang]/privacy` — SSG, 34 езика

### Задължително съдържание (GDPR чл. 13)
1. Идентичност на администратора (фирма, ЕИК, седалище, имейл)
2. Контакт за privacy въпроси
3. Цели на обработването
4. Правна основа за всяка категория данни (виж таблицата по-долу)
5. Получатели / processors (Google, Stripe, Resend, hosting)
6. Трансфери извън EEA — механизъм (SCCs + DPF)
7. Срокове на съхранение (виж Retention Policy)
8. Права на субектите (достъп, корекция, изтриване, портабилност, възражение)
9. Право на жалба до КЗЛД + UODO (Полша)
10. Автоматизирано вземане на решения (Stripe fraud detection)
11. Cookie информация — линк към Cookie Policy

### Правна основа по тип данни
| Данни | Основа |
|---|---|
| Имейл, парола | Договор (чл. 6(1)(b)) |
| Телефон (core функция) | Договор (чл. 6(1)(b)) |
| IP, user agent (security) | Легитимен интерес (чл. 6(1)(f)) |
| GA4 / analytics | Съгласие (чл. 6(1)(a)) |
| Stripe payment data | Договор + законово задължение (чл. 6(1)(b)(c)) |
| Транзакционни имейли | Договор (чл. 6(1)(b)) |
| Marketing имейли | Съгласие (чл. 6(1)(a)) |

### Retention schedule (задължително в документа)
| Данни | Срок |
|---|---|
| Профил (активен) | До изтриване от потребителя |
| Профил след изтриване | Max 30 дни (backups) |
| Счетоводни/Stripe записи | 10 години (ЗСч) |
| Security logs (IP) | 90 дни |
| GA4 данни | 14 месеца |
| Consent records | 24 месеца |
| Marketing consent | До оттегляне + 3 години |

### Processor DPA статус (задължително да е направено преди launch)
| Processor | DPA | Статус |
|---|---|---|
| Google (GA4) | Google Analytics Data Processing Amendment | ⬜ Не подписан |
| Stripe | Автоматично в TOS | ✅ Активен |
| Resend | resend.com/legal/dpa | ⬜ Не подписан |
| Hosting | Зависи от провайдър | ⬜ Проверить |

### Езици
- BG версия: задължителна (КЗЛД)
- PL версия: задължителна (CRA / Ustawa o języku polskim)
- EN версия: default fallback

---

## ЗАДАЧА 4 — Cookie Policy страница
**Приоритет:** 🔴 КРИТИЧНО — преди launch  
**Тип:** Страница + текст  
**Статус:** ⬜ Не започнато

### Route
`/[lang]/cookies`

### Съдържание
Пълна таблица с всички cookies/localStorage entries:

| Ключ | Тип | Цел | Provider | Retention | Основа |
|---|---|---|---|---|---|
| `nevumo_auth_token` | localStorage | Auth JWT | Nevumo | Session/30 дни | Договор |
| `nevumo_auth_user` | localStorage | User info cache | Nevumo | Session/30 дни | Договор |
| `nevumo_phone` | localStorage | Phone autofill | Nevumo | Indefinite | Легитимен интерес |
| `nevumo_intent` | localStorage | UX role intent | Nevumo | Session | Функционален |
| `nevumo_consent` | Cookie | Consent record | Nevumo | 12 месеца | Задължителен |
| `_ga`, `_ga_*` | Cookie | GA4 analytics | Google | 13 месеца | Съгласие |
| `__stripe_mid` | Cookie | Fraud prevention | Stripe | 1 година | Задължителен (checkout) |
| `__stripe_sid` | Cookie | Fraud prevention | Stripe | 30 мин | Задължителен (checkout) |

### Езици
PL, EN, BG — задължително

---

## ЗАДАЧА 5 — Terms & Conditions (Клиенти)
**Приоритет:** 🔴 КРИТИЧНО — преди launch  
**Тип:** Страница + текст  
**Статус:** ⬜ Не започнато

### Route
`/[lang]/terms`

### Задължително съдържание
1. Идентификация на Nevumo (фирма, ЕИК, адрес, имейл, тел.)
2. Описание на услугата — Nevumo е **intermediary**, не страна по договора клиент-доставчик
3. Регистрация и акаунт
4. Ranking parameters — как се подреждат доставчиците (прозрачност по Omnibus)
5. Дали доставчикът е trader или private individual — **задължително маркиране**
6. Цени и плащания (Stripe, BLIK, Przelewy24 за PL)
7. **Право на отказ (14 дни)** — стандартен формуляр (Annex 1)
8. Жалби — 14-дневен срок за отговор (PKE/CRA)
9. Отговорност — safe-harbour (чл. 14 UŚUDE / DSA)
10. ADR — Inspekcja Handlowa (Варшава); БЕЗ ODR линк (платформата е закрита 20.07.2025)
11. Приложимо право: Българско + императивни норми на страната на потребителя
12. Изменения: 14 дни предизвестие

### Полски специфики (ЗАДЪЛЖИТЕЛНО в PL версията)
- Клауза: *„Zabrania się dostarczania treści o charakterze bezprawnym"*
- Технически изисквания за ползване на платформата
- Пълна преформулировка на Регламента като **Regulamin** (PL правен стандарт)

### Езици
- PL: **Regulamin** — задължителен, правно обвързващ за PL потребители
- BG: Общи условия
- EN: Terms & Conditions

---

## ЗАДАЧА 6 — Regulamin за Доставчици
**Приоритет:** 🔴 КРИТИЧНО — преди launch  
**Тип:** Страница + текст  
**Статус:** ⬜ Не започнато

### Route
`/[lang]/terms-provider`

### Допълнително съдържание (P2B специфики)
1. Основания за **спиране / ограничаване / прекратяване** на акаунт — конкретни
2. **30 дни предизвестие** за прекратяване (с изключения при нарушения)
3. **15 дни предизвестие** за изменение на условията
4. Ranking параметри и дали плащането влияе
5. Достъп на доставчика до собствените му данни
6. **Mediation / ADR** — посочване на минимум двама медиатори
7. Internal complaint-handling system
8. KYC изисквания — декларация дали доставчикът е trader (NIP/REGON за PL)

---

## ЗАДАЧА 7 — Формуляр за отказ (Withdrawal Form)
**Приоритет:** 🔴 КРИТИЧНО — за PL  
**Тип:** Текст (PDF/HTML annex)  
**Статус:** ⬜ Не започнато

### Стандартна форма по Annex I, Part B на CRA
Задължително на **полски език**. Приложена като Annex 1 към T&C клиенти.
Достъпна и за download.

---

## ЗАДАЧА 8 — DSA Contact Point страница
**Приоритет:** 🟡 Важно  
**Тип:** Страница  
**Статус:** ⬜ Не започнато

### Route
`/[lang]/legal` или `/[lang]/contact-dsa`

### Съдържание
- Единна точка за контакт с власти и потребители (DSA чл. 11)
- Email за: privacy, abuse reports, law enforcement requests
- Процедура за notice-and-takedown (DSA чл. 16)

---

## ЗАДАЧА 9 — Вътрешни compliance документи (не публични)
**Приоритет:** 🟡 Важно  
**Тип:** Бизнес процеси  
**Статус:** ⬜ Не започнато

### 9.1 Article 30 Records (Регистър на дейностите по обработване)
- Вътрешен документ (Excel/Notion/doc)
- Съдържа: категории данни, цел, правна основа, retention, processors, трансфери
- Представя се при КЗЛД проверка

### 9.2 Breach Notification процедура
- 72-часов timer към КЗЛД при breach
- Template за уведомление
- Вътрешен breach register (чл. 33(5) GDPR)

### 9.3 DPA подписване
- Google: Analytics Data Processing Amendment — подписва се в GA4 Admin
- Resend: resend.com/legal/dpa — изтегли и подпиши
- Hosting провайдър: провери и подпиши

### 9.4 Retention Policy документ
- Вътрешен документ с всички срокове (виж таблицата в Задача 3)

---

## ЗАДАЧА 10 — Юридически преглед
**Приоритет:** 🟡 Препоръчително преди launch  
**Тип:** Външна услуга  
**Статус:** ⬜ Не започнато

- Текстовете пише **Claude** на база установени шаблони + специфики на Nevumo
- Адвокат прави само **финален преглед** (1–2 часа работа)
- Фокус: Regulamin (PL) + Privacy Policy — специфики на marketplace intermediary модела
- Бюджет: **~200–400 EUR** (не 1500)
- Препоръчително, но не блокиращо за launch

---

## Приоритетен ред на изпълнение

| # | Задача | Тип | Кой прави | Модел |
|---|---|---|---|---|
| 1 | Cookie Consent Banner | Код | Windsurf | SWE-1.5 / Phoenix |
| 2 | GA4 Consent Mode v2 | Код | Windsurf | Kimi-2.5 |
| 3 | Consent audit log (DB + endpoint) | Код | Windsurf | Phoenix |
| 4 | Data Export endpoint | Код | Windsurf | SWE-1.5 |
| 5 | Privacy Policy текст | Текст | Claude | — |
| 6 | Cookie Policy текст | Текст | Claude | — |
| 7 | T&C клиенти (EN+PL+BG) | Текст | Claude | — |
| 8 | Regulamin доставчици (EN+PL+BG) | Текст | Claude | — |
| 9 | Withdrawal Form (PL) | Текст | Claude | — |
| 10 | Frontend страници /privacy /cookies /terms | Код | Windsurf | Kimi-2.5 |
| 11 | DSA Contact Point страница | Код | Windsurf | Kimi-2.5 |
| 12 | Вътрешни compliance docs | Бизнес | Dimitrov | — |
| 13 | DPA подписване | Бизнес | Dimitrov | — |
| 14 | Юридически преглед | Юрист | Адвокат (препоръчително) | — |

---

## Статус tracker

```
GDPR Compliance Progress:
[⏸️] Task 1  — Cookie Consent Banner (частично)
[✅] Task 2  — GA4 Consent Mode v2
[⬜] Task 3  — Consent Audit Log
[⬜] Task 4  — Data Export Endpoint
[⬜] Task 5  — Privacy Policy текст
[⬜] Task 6  — Cookie Policy текст
[⬜] Task 7  — T&C клиенти
[⬜] Task 8  — Regulamin доставчици
[⬜] Task 9  — Withdrawal Form PL
[⬜] Task 10 — Frontend страници
[⬜] Task 11 — DSA страница
[⬜] Task 12 — Вътрешни docs
[⬜] Task 13 — DPA подписване
[⬜] Task 14 — Юридически преглед
```

---

## Важни бележки

### Бизнес модел
- **Клиент плаща директно на доставчика** — Nevumo е чист intermediary, не държи фондове
- **Безплатен старт** — T&C трябва да съдържа клауза: „Nevumo си запазва правото да въведе платени функции с предизвестие от 30 дни"
- **Stripe Connect** не е нужен на старт; Stripe стандартен е достатъчен. KNF лиценз не се изисква.
- **BLIK и Przelewy24** — добави като payment методи за PL при Stripe интеграцията (Stripe ги поддържа)

### Възраст
- **Минимална регистрационна възраст: 18 години**
- Верификация: **checkbox** при регистрация — „Потвърждавам, че съм навършил/а 18 години" / „Potwierdzam, że mam ukończone 18 lat"
- Правната отговорност е изцяло на потребителя — стандартна практика
- Не се изисква ID верификация

### GA4
- Режим: **Advanced Consent Mode v2** — GA4 зарежда cookieless pings при отказ, Google моделира ~85% от данните
- Consent rate в Полша: ~30–50% — Basic Mode би означавал загуба на 50–70% от данните
- Задължително разкриване на Advanced Mode в Privacy Policy и Cookie Policy

### Claimed Profiles (GDPR чл. 14)
- Профилите са създадени от Nevumo (scrape) **без** директен контакт с доставчика
- При claim → **автоматично изпращане на чл. 14 уведомление** по имейл:
  „Nevumo е създал профил с тези данни. Ето какво пазим и защо."
- Срок: в момента на claim (или max 1 месец след публикуване ако профилът е публичен)
- Имплементацията е в claim flow — при `POST /api/v1/claim/{token}` → trigger email

### Правни документи
- Текстовете пише **Claude** — установени шаблони + специфики на Nevumo
- Адвокат прави **финален преглед** (~200–400 EUR) — препоръчително, не блокиращо
- Полският **Regulamin** е правно обвързващ за PL потребители, дори ако регистрацията е в BG
- **ODR линк НЕ се добавя** — платформата е закрита от 20.07.2025
- За PL маркетинг имейли: отделен **PKE consent checkbox** — НЕ е включен в T&C acceptance

### Технически
- `nevumo_phone` в localStorage → задължително в Cookie Policy (Легитимен интерес)
- **НИКОГА** не зареждай GA4 без Consent Mode v2 default `denied`
