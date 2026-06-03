---
name: cleanup-macos-caches
description: Clean macOS system caches and temporary files to free disk space
---

Изпълни почистване на системните кешове и временни файлове на macOS, за да освободиш място на диска, без да докосваш работната директория на проекта.

## Steps

1. **User Caches**: Изчисли размера на ~/Library/Caches и докладвай. След това изтрий съдържанието му (без самата папка).
2. **Log Files**: Изтрий системните логове в ~/Library/Logs и /Library/Logs.
3. **Chrome Cache**: Ако е инсталиран, изчисти кеша на Google Chrome, който се намира в ~/Library/Caches/Google/Chrome/Default/Cache.
4. **Xcode Junk**: Ако има остатъци от Xcode (често срещано при macOS), провери за папка ~/Library/Developer/Xcode/DerivedData и я изчисти.
5. **Downloads Folder**: Списък на 5-те най-големи файла в папката ~/Downloads, за да реша дали да ги изтрия ръчно (само ги покажи, не ги трий).
6. **Trash**: Изпразни кошчето чрез терминала: rm -rf ~/.Trash/*.

## Important Constraints

- Не докосвай нищо в /Users/dimitardimitrov/nevumo/.
- Не трий конфигурационни файлове (.plist или .json) от Library, само кеш и логове.
- Докладвай колко общо място е освободено според df -h преди и след операцията.
