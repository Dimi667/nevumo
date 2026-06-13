# Nevumo — Ръководство за миграция между лаптопи

## Важно преди да започнеш

Продъкшън инфраструктурата (Neon, Upstash, Railway, Vercel, Cloudflare) е в облака и не се мества. Мигрира се само локалната среда за разработка.

---

## Стъпка 1 — На стария лаптоп: архивирай всичко

### 1.1 Синхронизирай кода
```bash
cd /Users/dimitardimitrov/nevumo
git add .
git commit -m "pre-migration snapshot"
git push origin main
git push nevumo-git main
```

### 1.2 Архивирай Devin на SSD-то
```bash
mkdir -p /Volumes/Transcend\ ESD310C\ 128GB/windsurf-backup/app-support
mkdir -p /Volumes/Transcend\ ESD310C\ 128GB/windsurf-backup/windsurf-home
mkdir -p /Volumes/Transcend\ ESD310C\ 128GB/windsurf-backup/devin-new/IndexedDB
mkdir -p /Volumes/Transcend\ ESD310C\ 128GB/windsurf-backup/devin-new/LocalStorage
mkdir -p /Volumes/Transcend\ ESD310C\ 128GB/windsurf-backup/devin-new/User

cp -r ~/Library/Application\ Support/Windsurf/ /Volumes/Transcend\ ESD310C\ 128GB/windsurf-backup/app-support/
cp -r ~/.windsurf/ /Volumes/Transcend\ ESD310C\ 128GB/windsurf-backup/windsurf-home/
cp -r ~/Library/Application\ Support/Devin/IndexedDB/ /Volumes/Transcend\ ESD310C\ 128GB/windsurf-backup/devin-new/IndexedDB/
cp -r ~/Library/Application\ Support/Devin/Local\ Storage/ /Volumes/Transcend\ ESD310C\ 128GB/windsurf-backup/devin-new/LocalStorage/
cp -r ~/Library/Application\ Support/Devin/User/ /Volumes/Transcend\ ESD310C\ 128GB/windsurf-backup/devin-new/User/
```

### 1.3 Копирай кода на SSD-то (без node_modules и .venv)
```bash
cd /Users/dimitardimitrov
cp -r nevumo /Volumes/Transcend\ ESD310C\ 128GB/nevumo-transfer
```

> **Забележка:** `.venv` не съществува в production setup. `node_modules` трябва да се изключи ако съществува.

---

## Стъпка 2 — На новия лаптоп: инсталирай prerequisites

### 2.1 Инсталирай Homebrew
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

После добави към PATH:
```bash
echo >> /Users/dimitardimitrov/.zprofile
echo 'eval "$(/opt/homebrew/bin/brew shellenv zsh)"' >> /Users/dimitardimitrov/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv zsh)"
```

### 2.2 Инсталирай Node.js 22
```bash
brew install node@22
echo 'export PATH="/opt/homebrew/opt/node@22/bin:$PATH"' >> ~/.zprofile
export PATH="/opt/homebrew/opt/node@22/bin:$PATH"
```

Провери:
```bash
node --version   # трябва да покаже v22.x.x
npx --version
```

### 2.3 Инсталирай Devin
Свали от [windsurf.ai](https://windsurf.ai) и инсталирай.

### 2.4 Инсталирай Railway CLI
```bash
brew install railway
railway --version  # трябва да покаже railway 5.x.x
railway login      # отваря браузър → влез с GitHub акаунт
cd /Users/dimitardimitrov/nevumo
railway link       # избери: Nevumo's Projects → nevumo → production → api
railway status     # трябва да покаже api: Online
```

### 2.5 Инсталирай Python 3.13
macOS идва с Python 3.9 (вграден в Xcode Tools) — твърде стар за проекта (изисква 3.10+).
```bash
brew install python@3.13
python3.13 --version  # трябва да покаже Python 3.13.x
pip3.13 install psycopg2-binary sqlalchemy --break-system-packages
python3.13 -c "import psycopg2, sqlalchemy; print('OK')"
```

Използвай `python3.13` и `pip3.13` за всички production seed скриптове:
```bash
railway run python3.13 -m apps.api.scripts.SCRIPT_NAME
```

---

## Стъпка 3 — На новия лаптоп: пренеси кода

```bash
cp -r /Volumes/Transcend\ ESD310C\ 128GB/nevumo-transfer /Users/dimitardimitrov/nevumo
```

---

## Стъпка 4 — На новия лаптоп: конфигурирай Git

```bash
cd /Users/dimitardimitrov/nevumo
git remote -v
```

Ако `origin` и `nevumo-git` не са там (обикновено са, защото `.git` папката е копирана):
```bash
git remote add origin https://github.com/Dimi667/nevumo.git
git remote add nevumo-git /Volumes/Transcend\ ESD310C\ 128GB/Nevumo_Git_Backups/Nevumo.git
```

Настрой самоличност:
```bash
git config --global user.name "Dimitar Dimitrov"
git config --global user.email "dimitar.j.dimitroff@gmail.com"
```

---

## Стъпка 5 — На новия лаптоп: инсталирай пакетите

```bash
cd /Users/dimitardimitrov/nevumo
npm install
npx playwright install
```

---

## Стъпка 6 — На новия лаптоп: пренеси Devin история и екстеншъни

```bash
# Стара Windsurf история (сесии от преди преименуването)
cp -r /Volumes/Transcend\ ESD310C\ 128GB/windsurf-backup/app-support/ ~/Library/Application\ Support/Windsurf/
cp -r ~/Library/Application\ Support/Windsurf/ ~/Library/Application\ Support/Devin/

# Екстеншъни
cp -r /Volumes/Transcend\ ESD310C\ 128GB/windsurf-backup/windsurf-home/extensions/ ~/.devin/extensions/

# Нови Devin сесии (от след преименуването)
cp -r /Volumes/Transcend\ ESD310C\ 128GB/windsurf-backup/devin-new/IndexedDB/ ~/Library/Application\ Support/Devin/IndexedDB/
cp -r /Volumes/Transcend\ ESD310C\ 128GB/windsurf-backup/devin-new/LocalStorage/ ~/Library/Application\ Support/Devin/Local\ Storage/
cp -r /Volumes/Transcend\ ESD310C\ 128GB/windsurf-backup/devin-new/User/ ~/Library/Application\ Support/Devin/User/
```

Рестартирай Devin.

---

## Стъпка 7 — Финален тест

```bash
cd /Users/dimitardimitrov/nevumo
git add .
git commit -m "chore: migrate to new laptop"
git push origin main
git push nevumo-git main
```

За `git push origin main` ще поиска GitHub credentials:
- Username: `Dimi667`
- Password: GitHub Personal Access Token (не паролата!) от [github.com/settings/tokens](https://github.com/settings/tokens)

---

## Бележки

- `node_modules/` и `.venv/` никога не се копират — генерират се наново с `npm install`
- `.env` файловете не са в Git — копират се ръчно от стария лаптоп
- Playwright браузърите не се копират — инсталират се наново с `npx playwright install`
- Devin session историята се пази в две места: `Windsurf/` (стари) и `Devin/` (нови след преименуването)
