# Page snapshot

```yaml
- generic [ref=e1]:
  - button "Open Next.js Dev Tools" [ref=e7] [cursor=pointer]:
    - img [ref=e8]
  - alert [ref=e11]: Вход | Nevumo
  - generic [ref=e13]:
    - generic [ref=e14]:
      - heading "Намери услуга за минути" [level=1] [ref=e15]
      - paragraph [ref=e16]: Безплатно • Без ангажимент
    - paragraph [ref=e17]: Бърз вход без парола
    - generic [ref=e18]:
      - button "Вход с Google" [ref=e19] [cursor=pointer]:
        - img [ref=e20]
        - text: Вход с Google
      - button "Вход с Facebook" [ref=e25] [cursor=pointer]:
        - img [ref=e26]
        - text: Вход с Facebook
    - generic [ref=e31]: или с имейл
    - textbox "Email address" [active] [ref=e33]:
      - /placeholder: name@email.com
    - button "Продължи" [disabled] [ref=e34]
```