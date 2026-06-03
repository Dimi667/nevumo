# 🧪 Автоматизирани правила за тестване на Nevumo

## 🎯 Обхват:
Пълно автоматизирано тестване на всички критични части на Nevumo приложението след всяка промяна.

## 🔄 Тригери за автоматично тестване:

### 1. **След всяка промяна в ANY файл:**
- `/apps/web/app/[lang]/**/page.tsx`
- `/apps/web/components/**/*.tsx`
- `/apps/web/lib/**/*.ts`
- `/packages/**/*.ts`

### 2. **След промени в middleware/layout:**
- `/apps/web/middleware.ts`
- `/apps/web/app/[lang]/layout.tsx`
- `/apps/web/app/layout.tsx`

### 3. **След промени в API/routes:**
- `/apps/api/**/*.ts`
- `/apps/api/routes/**/*.ts`

### 4. **След промени в database/schema:**
- Alembic migrations
- Database schema changes

## 🧪 Категории тестове:

### ✅ **Onboarding Flow Tests:**
1. **Page Load Tests**
   - ✅ Всички езици (bg, en, de, fr, etc.)
   - ✅ Layout центриране
   - ✅ Responsive дизайн

2. **UX Component Tests**
   - ✅ Progress bar functionality
   - ✅ Form валидация
   - ✅ CTA бутони
   - ✅ Skip функционалност
   - ✅ Photo upload
   - ✅ Time hints

3. **Dashboard Tests**
   - ✅ Sidebar показване/скриване
   - ✅ Hero banner при incomplete profile
   - ✅ Locked sections
   - ✅ Navigation functionality

### ✅ **Services Page Tests:**
- ✅ Service CRUD операции
- ✅ Category филтриране
- ✅ Search функционалност
- ✅ Pagination

### ✅ **Profile Page Tests:**
- ✅ Profile редактиране
- ✅ Settings промени
- ✅ Photo management

### ✅ **Leads Page Tests:**
- ✅ Lead CRUD операции
- ✅ Status промени
- ✅ Филтриране

### ✅ **Analytics Page Tests:**
- ✅ Dashboard статистики
- ✅ Chart визуализации
- ✅ Date range филтри

### ✅ **Responsive/Mobile Tests:**
- ✅ Mobile viewport (< 768px)
- ✅ Tablet viewport (768px - 1024px)
- ✅ Touch interactions
- ✅ Swipe gestures

### ✅ **Accessibility Tests:**
- ✅ WCAG 2.1 AA съответствие
- ✅ Keyboard navigation
- ✅ Screen reader съвместимост
- ✅ Focus management

### ✅ **Performance Tests:**
- ✅ Page load time (< 3 сек)
- ✅ Core Web Vitals
- ✅ Bundle size анализ
- ✅ Memory usage

### ✅ **Security Tests:**
- ✅ XSS защита
- ✅ CSRF токени
- ✅ Authentication flows
- ✅ Authorization checks

### ✅ **E2E Tests:**
- ✅ Пълен user journeys
- ✅ Multi-user сценарии
- ✅ Cross-browser съвместимост

## 🔧 Технически тестове:

### **Build Tests:**
```bash
npm run build          # ✅ Clean build
npm run check-types      # ✅ TypeScript валидация
```

### **Unit Tests:**
```bash
npm run test:unit      # Jest/Vitest unit тестове
```

### **Integration Tests:**
```bash
npm run test:integration # API integration тестове
```

### **E2E Tests:**
```bash
npm run test:e2e        # Playwright E2E тестове
```

### **Visual Regression Tests:**
```bash
npm run test:visual     # Screenshot сравнения
```

## 🌐 Мултиезична поддръжка:

### **Основни езици (Critical):**
- 🇧🇷 **Български (bg)** - Основен пазар
- 🇬🇧 **Английски (en)** - International
- 🇩🇪 **Немски (de)** - Европейски пазар

### **Вторични езици (Important):**
- 🇷🇸 **Сръбски (sr)** - Балкански пазар
- 🇬🇪 **Френски (fr)** - Западноевропейски
- 🇮🇹 **Италиански (it)** - Европейски
- 🇪🇸 **Испански (es)** - Международни

### **Test Matrix:**
| Език | Onboarding | Dashboard | Services | Profile | Leads | Analytics |
|-------|------------|----------|----------|---------|----------|-----------|
| bg    | ✅          | ✅       | ✅      | ✅     | ✅        |
| en    | ✅          | ✅       | ✅      | ✅     | ✅        |
| de    | ✅          | ✅       | ✅      | ✅     | ✅        |
| fr    | ✅          | ✅       | ✅      | ✅     | ✅        |

## 📊 Тестови метрики и цели:

### **Performance Targets:**
- Page load: < 2 секунди
- First Contentful Paint: < 1.5 секунди
- Largest Contentful Paint: < 2 секунди
- Cumulative Layout Shift: < 0.1
- Time to Interactive: < 3 секунди

### **Quality Gates:**
- ✅ 0 TypeScript грешки
- ✅ 0 ESLint грешки
- ✅ 95% test coverage
- ✅ 0 accessibility нарушения
- ✅ 0 security уязвимости

### **Conversion Targets:**
- Onboarding completion: > 90%
- Service creation rate: > 85%
- User retention: > 80%

## 🚀 CI/CD Integration:

### **GitHub Actions:**
```yaml
name: Nevumo Testing
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run test:e2e
      - run: npm run test:visual
```

### **Pre-deployment Checks:**
```bash
npm run validate:all  # Всички тестове
npm run build          # Build проверка
npm run audit          # Security проверка
```

## 📱 Responsive Breakpoints:

### **Mobile:**
- Small phones: 320px - 374px
- Phones: 375px - 414px
- Large phones: 414px - 736px
- Tablets: 768px - 1024px

### **Desktop:**
- Small desktop: 1024px - 1280px
- Standard: 1280px - 1440px
- Large: 1440px - 1920px

## 🔍 Debugging и Monitoring:

### **Browser DevTools:**
- Network request анализ
- Performance профилиране
- Console error tracking
- Accessibility audit

### **Real User Monitoring:**
- Click tracking
- Form submission анализ
- Error bounce rate
- User session recordings

## 📝 Automated Testing Commands:

### **Бърза проверка (Pre-commit):**
```bash
npm run test:smoke && npm run build
```

### **Пълна валидация (Pre-merge):**
```bash
npm run test:all && npm run build && npm run audit
```

### **Deployment тестове (Pre-production):**
```bash
npm run test:e2e:production && npm run test:visual:production
```

## 🎯 Критични Success Criteria:

### **За Release Ready:**
1. ✅ Всички critical тестове минават
2. ✅ Build е чист без грешки
3. ✅ Performance targets са постигнати
4. ✅ Accessibility score > 95%
5. ✅ Security scan е чист
6. ✅ Multi-browser съвместимост

### **За Hotfix:**
1. ✅ Регресионни тестове минават
2. ✅ Problem area е изолирана
3. ✅ Fix е валидиран
4. ✅ Няма side effects

---

**Създадено на:** $(date)
**Последна актуализация:** Цялост покритие на Nevumo тестване
**Отговорен за:** Dev Team и QA отдел
