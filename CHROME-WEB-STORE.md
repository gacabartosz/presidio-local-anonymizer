# 📦 Publikacja na Chrome Web Store - Krok po Kroku

## ✅ Status Przygotowania

### Gotowe do Publikacji:
- ✅ Manifest v3 (wymagany od 2024)
- ✅ Wszystkie ikony (16, 32, 48, 128px)
- ✅ ZIP gotowy: `presidio-extension-v1.3.0.zip` (30KB)
- ✅ Kod w GitHub: https://github.com/gacabartosz/presidio-local-anonymizer
- ✅ Dokumentacja kompletna

---

## 📋 Wymagania Chrome Web Store

### 1. Konto Google Developer
- ✅ Potrzebne jest konto deweloperskie
- ✅ Jednorazowa opłata: $5 USD
- 🔗 https://chrome.google.com/webstore/devconsole/

### 2. Dokumenty wymagane:
- ✅ **manifest.json** - gotowy
- ✅ **Ikony** - wszystkie rozmiary gotowe (16, 32, 48, 128px)
- ✅ **ZIP rozszerzenia** - `presidio-extension-v1.3.0.zip`
- ⚠️ **Screenshot** (1280x800 lub 640x400) - trzeba zrobić
- ⚠️ **Promotional tile** (440x280) - opcjonalny ale zalecany
- ⚠️ **Privacy Policy** - WYMAGANA dla rozszerzeń z uprawnieniami

---

## 🚀 KROK 1: Przygotowanie Materiałów

### A. Screenshoty (WYMAGANE!)

**Wymiary:**
- Wymagana szerokość: 1280px lub 640px
- Wymagana wysokość: 800px lub 400px
- Format: PNG lub JPG
- Minimalna liczba: 1, maksymalna: 5

**Co pokazać:**
1. Screenshot głównego interfejsu (popup rozszerzenia)
2. Screenshot dashboardu z logami
3. Screenshot działającego rozszerzenia na ChatGPT
4. Screenshot ustawień

**Instrukcja:**
```bash
# Otwórz rozszerzenie w Chrome
# Kliknij prawym przyciskiem → Zbadaj element → zakładka Console
# Zrób screenshoty:

1. Popup rozszerzenia (toggle, status online)
2. Dashboard http://localhost:4222/dashboard → sekcja "Logi"
3. ChatGPT z anonimizowanym tekstem
4. Strona ustawień (opcje rozszerzenia)

# Przytnij do 1280x800 px używając narzędzia online lub:
# macOS: Preview → Tools → Adjust Size
# Windows: Paint → Resize → Pixels
```

### B. Privacy Policy (WYMAGANA!)

**Dlaczego wymagana:**
- Rozszerzenie ma uprawnienie `storage` (przechowuje konfigurację)
- Rozszerzenie ma uprawnienie `clipboardRead` (czyta schowek)
- Rozszerzenie komunikuje się z localhost:4222

**Gdzie umieścić:**
1. Stwórz `PRIVACY_POLICY.md` w repo GitHub
2. Opublikuj na GitHubPages lub swojej stronie
3. Dodaj link w Chrome Web Store

**Template Privacy Policy:**

```markdown
# Privacy Policy - Presidio Browser Anonymizer

**Last updated:** November 15, 2025

## Data Collection

This extension does NOT collect, store, or transmit any personal data to external servers.

### What data is processed:
- Text pasted into web forms (processed locally via localhost:4222)
- Extension configuration (stored locally in browser)
- Anonymization logs (stored temporarily in browser, max 100 entries)

### Where data is processed:
- **Locally only** - All processing happens on your computer
- Backend runs at `http://localhost:4222` (your machine)
- **No external servers** - We don't send data anywhere

### What permissions we use:
- `storage`: Save extension settings locally
- `clipboardRead`: Read pasted text to anonymize it
- `activeTab`: Access current webpage content
- `contextMenus`: Add right-click menu option

### Third-party services:
- **Microsoft Presidio**: Open-source library running locally on your machine
- **No analytics**: We don't use Google Analytics or any tracking
- **No ads**: We don't display advertisements

### Data retention:
- Configuration: Stored until you uninstall the extension
- Logs: Maximum 100 recent anonymizations, stored in browser
- Backend data: Temporary, cleared on backend restart

### Your rights:
- Delete all data: Uninstall the extension or clear logs in dashboard
- Export data: Not applicable (nothing stored permanently)
- Contact: GitHub Issues at https://github.com/gacabartosz/presidio-local-anonymizer

## Open Source

This extension is fully open source:
https://github.com/gacabartosz/presidio-local-anonymizer

You can audit the code to verify our privacy claims.

## Contact

Questions? Open an issue on GitHub:
https://github.com/gacabartosz/presidio-local-anonymizer/issues
```

### C. Promotional Tile (Opcjonalny)

**Wymiary:** 440x280px
**Format:** PNG lub JPG

Można stworzyć w Canva lub Figma.

---

## 🚀 KROK 2: Rejestracja w Chrome Developer Console

1. Wejdź na: https://chrome.google.com/webstore/devconsole/
2. Zaloguj się kontem Google
3. **Jednorazowa opłata: $5 USD**
4. Wypełnij dane dewelopera

---

## 🚀 KROK 3: Upload Rozszerzenia

### A. Wejdź do Developer Dashboard

1. Otwórz: https://chrome.google.com/webstore/devconsole/
2. Kliknij **"New Item"**

### B. Upload ZIP

1. **Upload**: `presidio-extension-v1.3.0.zip`
2. Czekaj na weryfikację (1-2 minuty)

### C. Wypełnij Formularz

#### 1. **Store Listing** (Opis dla użytkowników)

**Detailed description** (maksymalnie 16,000 znaków):

```
🔒 PRESIDIO BROWSER ANONYMIZER

Auto-anonymize personally identifiable information (PII) when pasting text into ChatGPT, Claude, Perplexity, Gmail, and any website!

✨ KEY FEATURES:

• ⚡ AUTO-ANONYMIZATION ON PASTE (Ctrl+V)
  Automatically detects and anonymizes PII before pasting

• 🎯 28 PII ENTITY TYPES DETECTED:
  - Personal: Names, emails, phone numbers, addresses
  - Polish IDs: PESEL, NIP, REGON, ID cards, passports
  - Financial: Credit cards, IBANs
  - Technical: IPs, URLs, dates
  - And more!

• 🤖 WORKS WITH AI CHATBOTS:
  - ChatGPT (chatgpt.com)
  - Claude (claude.ai)
  - Perplexity (perplexity.ai)
  - Google Gemini
  - Microsoft Copilot
  - And ALL other websites!

• 📊 DASHBOARD WITH LOGS:
  View history: original → anonymized text
  Track what was anonymized
  Clear logs anytime

• 🔐 100% PRIVATE & SECURE:
  - All processing on YOUR computer (localhost)
  - No external servers
  - No data collection
  - Open source - audit the code!

• 🎛️ EASY ON/OFF TOGGLE:
  Enable/disable auto-anonymization with one click

🚀 HOW TO USE:

1. Install extension
2. Run local backend (Python)
3. Copy text with PII
4. Paste (Ctrl+V) into ChatGPT/Claude/any website
5. ✅ Text automatically anonymized!

💡 METHODS:

• Auto-paste (Ctrl+V) - Best method! Works everywhere
• Keyboard shortcut (Ctrl+Shift+A) - Manual anonymization
• Right-click menu - "Anonymize selected text"

🔧 TECHNICAL:

• Powered by Microsoft Presidio (open-source)
• Manifest V3 (latest standard)
• Local backend required (included)
• GitHub: https://github.com/gacabartosz/presidio-local-anonymizer

🌍 PRIVACY:

No data leaves your computer. Everything runs locally.
Privacy Policy: [LINK TO YOUR PRIVACY POLICY]

📚 DOCUMENTATION:

Full setup guide in GitHub README
AI sites guide included
Testing instructions
Troubleshooting help

⭐ PERFECT FOR:

• Data privacy enthusiasts
• GDPR compliance professionals
• Security researchers
• Anyone sharing data with AI
• Polish users (supports PESEL, NIP, etc.)

🆓 100% FREE & OPEN SOURCE

Support development:
https://github.com/gacabartosz/presidio-local-anonymizer

---

KEYWORDS: privacy, PII, anonymization, ChatGPT, Claude, GDPR, PESEL, NIP, data protection, security
```

#### 2. **Category**

Select:
- **Productivity** (najlepsze dopasowanie)
- Alternatywnie: **Developer Tools**

#### 3. **Language**

- Primary: **English**
- Dodatkowe: **Polish** (jeśli chcesz polską wersję opisu)

#### 4. **Screenshots** (WYMAGANE!)

Upload 1-5 screenshotów (1280x800 px):
1. Extension popup showing toggle and status
2. Dashboard with logs (before → after)
3. ChatGPT with anonymized text
4. Settings page

#### 5. **Promotional tile** (Opcjonalny)

Upload 440x280px image (jeśli masz)

#### 6. **Icon** (128x128)

- Upload: `chrome-extension/icons/icon-128.png`

#### 7. **Small tile** (Opcjonalny, 440x280)

Skip or upload if you have it.

#### 8. **Privacy Policy**

**WYMAGANE!** Link do Privacy Policy:
- Option 1: GitHub Pages: `https://gacabartosz.github.io/presidio-local-anonymizer/PRIVACY_POLICY.html`
- Option 2: Your website
- Option 3: GitHub raw: `https://raw.githubusercontent.com/gacabartosz/presidio-local-anonymizer/main/PRIVACY_POLICY.md`

#### 9. **Permissions justification**

**storage:**
```
Used to save extension configuration (backend URL, toggle state) locally in the browser.
No data is sent to external servers.
```

**clipboardRead:**
```
Used to read pasted text when user presses Ctrl+V, in order to anonymize PII before pasting.
Only processes text on user action (paste).
```

**activeTab:**
```
Used to access the current webpage content to replace pasted text with anonymized version.
Only active when user pastes text.
```

**contextMenus:**
```
Used to add "Anonymize selected text" option to right-click menu for manual anonymization.
```

**host_permissions (localhost):**
```
Used to communicate with local backend (http://localhost:4222) running on user's computer.
No external servers - all processing is local for maximum privacy.
```

---

## 🚀 KROK 4: Publikacja

### A. Review

1. **Przejrzyj wszystkie pola**
2. Sprawdź czy screenshoty są OK
3. Sprawdź Privacy Policy link

### B. Submit for Review

1. Kliknij **"Submit for review"**
2. Potwierdź submission

### C. Czas przeglądu

- Zwykle: **1-3 dni robocze**
- Czasem: Do 7 dni
- Google sprawdzi:
  - Kod (bezpieczeństwo)
  - Uprawnienia (czy są uzasadnione)
  - Opis (czy zgodny z funkcjami)
  - Privacy policy (czy istnieje)

---

## 🚀 KROK 5: Po Zatwierdzeniu

### A. Rozszerzenie Live!

URL będzie:
```
https://chrome.google.com/webstore/detail/presidio-browser-anonymizer/[RANDOM-ID]
```

### B. Dodaj do README

Zaktualizuj `README.md` w repo:
```markdown
## Install from Chrome Web Store

[![Chrome Web Store](https://img.shields.io/chrome-web-store/v/[YOUR-EXTENSION-ID])](https://chrome.google.com/webstore/detail/[YOUR-EXTENSION-ID])

[Install from Chrome Web Store](https://chrome.google.com/webstore/detail/[YOUR-EXTENSION-ID])
```

### C. Promuj!

- Tweet o tym
- Post na LinkedIn
- Reddit (r/Privacy, r/chrome_extensions)
- Product Hunt
- Hacker News (Show HN:)

---

## 📦 Aktualizacje w Przyszłości

### Jak zaktualizować rozszerzenie:

1. **Zwiększ wersję w `manifest.json`:**
   ```json
   "version": "1.4.0"
   ```

2. **Commit i push do GitHub**

3. **Stwórz nowy ZIP:**
   ```bash
   cd chrome-extension
   zip -r ../presidio-extension-v1.4.0.zip . -x "*.crx" -x "*.pem" -x "*.DS_Store"
   ```

4. **Upload do Chrome Web Store:**
   - Developer Dashboard → Your extension → "Upload new version"
   - Upload ZIP
   - Dodaj release notes
   - Submit for review

5. **Czas przeglądu:** Zwykle szybciej niż pierwsza publikacja (1-2 dni)

---

## ⚠️ Częste Problemy

### Problem: "Missing manifest key"

**Rozwiązanie:** Sprawdź czy `manifest.json` ma wszystkie wymagane pola:
- `manifest_version`
- `name`
- `version`
- `description`
- `icons`

### Problem: "Permission not justified"

**Rozwiązanie:** Dodaj dokładne uzasadnienie w sekcji "Permissions justification"

### Problem: "Missing privacy policy"

**Rozwiązanie:** Dodaj link do Privacy Policy (GitHub, własna strona, etc.)

### Problem: "Screenshots required"

**Rozwiązanie:** Dodaj przynajmniej 1 screenshot (1280x800 px)

### Problem: "Icon too small"

**Rozwiązanie:** Upewnij się że ikony mają dokładnie: 16, 32, 48, 128 px

---

## 📊 Checklist Przed Publikacją

```
✅ Manifest v3 (manifest_version: 3)
✅ Wszystkie ikony (16, 32, 48, 128px)
✅ ZIP rozszerzenia gotowy
✅ Screenshoty (minimum 1, zalecane 3-5) - 1280x800px
✅ Privacy Policy napisana i opublikowana
✅ Opis rozszerzenia (krótki i długi)
✅ Uzasadnienie uprawnień
✅ Kategoria wybrana (Productivity)
✅ Konto Chrome Developer ($5 USD opłacone)
✅ Kod w GitHub (publiczny)
✅ README zaktualizowany
✅ Dokumentacja kompletna
```

---

## 🎯 Co dalej?

Po publikacji:

1. ✅ **Monitor reviews** - odpowiadaj na opinie użytkowników
2. ✅ **Track analytics** - Developer Dashboard pokazuje statystyki
3. ✅ **Plan updates** - regularne aktualizacje (co 2-3 miesiące)
4. ✅ **Fix bugs** - szybko reaguj na zgłoszenia
5. ✅ **Add features** - słuchaj użytkowników

---

## 📞 Pomoc

- Chrome Web Store Help: https://support.google.com/chrome_webstore/
- Developer docs: https://developer.chrome.com/docs/webstore/
- GitHub Issues: https://github.com/gacabartosz/presidio-local-anonymizer/issues

---

**Powodzenia z publikacją! 🚀**

Twoje rozszerzenie jest gotowe do Chrome Web Store!
