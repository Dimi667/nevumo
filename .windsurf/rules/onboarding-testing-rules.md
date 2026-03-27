# 🧪 Автоматизирани правила за тестване след промени

## 🎯 Цел:
Гарантиране че всички UX подобрения и промени в Nevumo onboarding процеса работят коректно след всяка модификация.

## 🔄 Тригери за автоматично тестване:

### 1. **След всяка промяна в onboarding файлове:**
- `/apps/web/app/[lang]/provider/dashboard/profile/page.tsx`
- `/apps/web/app/[lang]/provider/dashboard/layout.tsx` 
- `/apps/web/app/[lang]/provider/dashboard/page.tsx`

### 2. **След промени в UI компоненти:**
- Progress bar компоненти
- CTA бутони
- Form валидация
- Photo upload функционалност

### 3. **След промени в layout/navigation:**
- Sidebar скриване/показване
- Центриране на съдържание
- Responsive дизайн

## 🧪 Задължителни тестове след всяка промяна:

### ✅ **Основни UX тестове:**
1. **Onboarding page load**
   - ✅ Центриран layout (`justify-center`)
   - ✅ Правилен header/subtitle текст
   - ✅ Progress bar с labels

2. **Progress Bar функционалност**
   - ✅ Step 1: `[1] Profile` (orange за active)
   - ✅ Step 2: `[2] Service` (gray за inactive)
   - ✅ Progress line между стъпките

3. **Description Field подобрения**
   - ✅ Нов placeholder: "Describe your services, experience and what makes you different"
   - ✅ Character counter: `X/50 minimum characters`
   - ✅ Валидация за минимум символи

4. **CTA бутони**
   - ✅ Step 1: "Continue →" (не "Next")
   - ✅ Step 2: "Complete Setup"
   - ✅ Правилни hover states

5. **Skip функционалност**
   - ✅ "Skip for now" бутон в Step 1
   - ✅ Водещ към dashboard с hero banner
   - ✅ Hero banner: "🚀 You're 1 step away from getting clients"
   - ✅ CTA: "Add your first service" → водещ към Step 2

6. **Time hints**
   - ✅ Step 1: "Takes less than 1 minute"
   - ✅ Step 2: "Almost done!"

7. **Photo Upload**
   - ✅ Upload бутон: "Upload photo" / "Change photo"
   - ✅ File input присъстващ
   - ✅ Error handling за cache проблеми
   - ✅ Timestamp за cache busting

8. **Layout центриране**
   - ✅ Onboarding: `justify-center` с `max-w-2xl`
   - ✅ Sidebar: скрит по време на onboarding
   - ✅ Post-onboarding: нормален layout със sidebar

9. **Sidebar State Management**
   - ✅ Реактивна проверка с `useCallback`
   - ✅ Автоматично обновяване след completion
   - ✅ Правилно показване след onboarding

10. **Skip Flow Logic**
    - ✅ Автоматично прескачане към Step 2 ако profile е попълнен
    - ✅ Правилна проверка за `missing_fields.includes('services')`

## 🌐 Мултиезична поддръжка:

### **Тестове за всички активни езици:**
- 🇧🇷 **Български (bg)**: `/bg/provider/dashboard`
   - Header: "Намери услуга за минути"
   - Subtitle: "Започни да получаваш заявки за минути"
   - Continue: "Продължи →"
   - Skip: "Пропусни за сега"
   - Time: "Отнема по-малко от 1 минута"

- 🇬🇧 **Английски (en)**: `/en/provider/dashboard`
   - Header: "Complete your profile"
   - Subtitle: "Start receiving client requests in minutes"
   - Continue: "Continue →"
   - Skip: "Skip for now"
   - Time: "Takes less than 1 minute"

## 📱 Responsive тестове:

### **Mobile (< 768px):**
- ✅ Onboarding центрирано вертикално
- ✅ Progress bar адаптивен
- ✅ Buttons с правилни размери
- ✅ Forms scroll-ват правилно

### **Tablet (768px - 1024px):**
- ✅ Optimized layout
- ✅ Touch-friendly елементи

### **Desktop (> 1024px):**
- ✅ Пълен layout с sidebar (post-onboarding)
- ✅ Hover states и micro-interactions

## 🔧 Технически тестове:

### **Build тестове:**
```bash
npm run build  # ✅ Трябва да минава без грешки
```

### **TypeScript проверка:**
```bash
npm run check-types  # ✅ Няма type errors
```

### **E2E тестове:**
```bash
npm run test  # ✅ Всички Playwright тестове минават
```

## 🚨 Critical Failure условия:

Ако някой от тези тестове се провали:
1. **Спряни всички промени**
2. **Провери build грешки**
3. **Провери TypeScript грешки**
4. **Ръчно тествай в браузър**
5. **Поправи и тествай отново**

## 📊 Тестови метрики:

### **Performance:**
- Onboarding load time: < 2 секунди
- Step transitions: < 500ms
- Photo upload: < 3 секунди

### **Conversion:**
- Step 1 completion rate: > 90%
- Skip flow работи: 100%
- Full onboarding completion: > 85%

## 🚀 Automated Testing Command:
```bash
# След всяка промяна изпълни:
npm run test && npm run build && npm run check-types

# Ако всичко е наред:
echo "✅ Всички тестове минават - промяната е готова!"
```

## 📝 Бележки:
- Всички тестове трябва да минават преди commit
- Build failures блокират merge
- TypeScript errors блокират deployment
- Manual тестване в браузър е задължително

---
**Създадено на:** $(date)
**Последна актуализация:** След всяка промяна на onboarding компонентите
