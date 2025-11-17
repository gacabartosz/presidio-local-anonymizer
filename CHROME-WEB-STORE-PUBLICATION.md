# 📦 Instrukcje Publikacji na Chrome Web Store

## Status: GOTOWE DO PUBLIKACJI ✅

**Wersja:** 1.3.4
**Plik ZIP:** `presidio-extension-v1.3.4.zip` (33KB)
**Data:** 17 Listopad 2025

---

## 🎯 Przedpublikacyjna Lista Kontrolna

### ✅ Wymagania Spełnione:

- [x] Manifest V3 compliant
- [x] Wszystkie ikony obecne (16px, 32px, 48px, 128px)
- [x] Privacy Policy opublikowana (GitHub)
- [x] Specyficzne host_permissions (bez wildcards)
- [x] Opis w limicie 132 znaków
- [x] ZIP package utworzony (33KB)
- [x] Kod przetestowany lokalnie
- [x] Dokumentacja kompletna

### ⚠️ Do Przygotowania:

- [ ] Screenshoty (1280x800px) - 3-5 sztuk
- [ ] Chrome Developer Account ($5 USD jednorazowo)
- [ ] Promotional tile (440x280px) - opcjonalnie

---

## 📸 Krok 1: Przygotuj Screenshoty

### Wymagania Chrome Web Store:

- **Rozmiar:** 1280x800px lub 640x400px
- **Format:** PNG lub JPG
- **Ilość:** 3-5 screenshotów (minimum 1)
- **Zawartość:** Pokaż funkcjonalność wtyczki

### Zalecane Screenshoty:

#### Screenshot 1: Extension Popup (Toggle ON/OFF)
```
Pokaż:
- Popup wtyczki z przyciskiem toggle
- Status: "Online" lub "Offline"
- Przycisk "Konfiguracja Wtyczki"
- Dashboard link
```

#### Screenshot 2: Installation Wizard
```
Pokaż:
- Zakładkę "Instalacja Backendu"
- OS selector (Windows/Mac/Linux)
- Instrukcje krok po kroku
- Linki do instalacji
```

#### Screenshot 3: ChatGPT z Anonimizacją
```
Pokaż:
- ChatGPT interface
- Tekst PRZED: "Jan Kowalski, email: jan@example.com, PESEL: 92010212345"
- Tekst PO: "[OSOBA], email: [EMAIL], PESEL: [PESEL]"
- Powiadomienie: "✅ Tekst zanonimizowany!"
```

#### Screenshot 4: Dashboard z Logami
```
Pokaż:
- Web dashboard (http://localhost:4222/dashboard)
- Sekcja "Logi"
- Before/After comparison
- Statystyki
```

#### Screenshot 5: Konfiguracja
```
Pokaż:
- Options page
- Backend URL configuration
- Test connection button
- Success message
```

### Jak Zrobić Screenshoty:

```bash
# macOS
Cmd + Shift + 4 → przeciągnij 1280x800px

# Windows
Windows + Shift + S → wybierz obszar

# Linux
PrtScn lub Shutter

# Narzędzia online do resize:
https://www.iloveimg.com/resize-image
https://www.canva.com/
```

---

## 💳 Krok 2: Załóż Chrome Developer Account

### URL Rejestracji:
https://chrome.google.com/webstore/devconsole/register

### Wymagania:
- **Konto Google** (masz już)
- **Opłata jednorazowa:** $5 USD
- **Metoda płatności:** Karta kredytowa/debetowa

### Proces:
1. Zaloguj się na konto Google
2. Akceptuj warunki Developer Agreement
3. Zapłać $5 USD
4. Aktywacja konta (natychmiastowa)

---

## 🚀 Krok 3: Utwórz Listing na Chrome Web Store

### URL Dashboard:
https://chrome.google.com/webstore/devconsole

### Proces Publikacji:

#### 3.1. Kliknij "New Item"

#### 3.2. Upload ZIP
```
Plik: presidio-extension-v1.3.4.zip (33KB)
Lokalizacja: /Users/gaca/presidio-local-anonymizer/presidio-extension-v1.3.4.zip
```

#### 3.3. Wypełnij Store Listing

**Nazwa Produktu:**
```
Presidio Browser Anonymizer
```

**Krótki Opis (132 znaki):**
```
Auto-anonymize PII when pasting! Detects emails, phones, PESEL, NIP, credit cards, and more. Works with ChatGPT, Claude, Gmail.
```

**Szczegółowy Opis:**
```markdown
# Presidio Browser Anonymizer

Auto-anonymize sensitive personal information when pasting text into ChatGPT, Claude, Gmail, and any website!

## ✨ Key Features

### 🔒 Automatic PII Detection & Anonymization
- **Polish Data:** PESEL, NIP, REGON, Dowód Osobisty, Paszport
- **International Data:** Email, Phone, Credit Card, IBAN, IP Address
- **Personal Info:** Names, Locations, Dates, URLs

### 🚀 Works Everywhere
- **AI Chatbots:** ChatGPT, Claude AI, Perplexity, Gemini
- **Email:** Gmail, Outlook
- **Forms:** Contact forms, support tickets
- **Any Website:** Textareas, input fields, contentEditable

### 📦 Easy Installation Wizard
- Auto-detects your OS (Windows, Mac, Linux)
- Step-by-step installation guide
- One-click backend setup
- Direct links to installation scripts

### 🔐 Privacy First
- **100% Local Processing** - All data processed on your computer
- **No Data Collection** - We don't track, store, or transmit your data
- **Open Source** - Full transparency, audit the code yourself
- **No External Servers** - Works completely offline

### 💪 Multiple Usage Methods

1. **Auto-Paste (Recommended)**
   - Copy text with PII
   - Paste anywhere (Ctrl+V / Cmd+V)
   - Automatically anonymized!

2. **Keyboard Shortcut**
   - Select text
   - Press Ctrl+Shift+A (Mac: Cmd+Shift+A)
   - Text anonymized in place

3. **Context Menu**
   - Right-click selected text
   - Choose "Anonymize selected text"

### 🎯 Perfect For:
- Customer support agents handling sensitive data
- Developers testing with production data
- Users sharing screenshots/logs
- Anyone pasting personal info into AI chatbots
- GDPR/CCPA compliance

### 🛠️ Technical Details
- **Backend:** Microsoft Presidio (enterprise-grade PII detection)
- **Model:** SpaCy NLP (Polish + English)
- **Entities Detected:** 28+ types
- **Architecture:** Local Flask server + Chrome Extension
- **Manifest:** V3 compliant

### 📖 Documentation
- Installation Guide: [GitHub README](https://github.com/gacabartosz/presidio-local-anonymizer)
- Testing Instructions: [TESTING.md](https://github.com/gacabartosz/presidio-local-anonymizer/blob/main/TESTING.md)
- Privacy Policy: [PRIVACY_POLICY.md](https://github.com/gacabartosz/presidio-local-anonymizer/blob/main/PRIVACY_POLICY.md)

### 🌟 Why Choose Presidio Anonymizer?
- **Enterprise-grade:** Built on Microsoft Presidio
- **Privacy-focused:** Zero data collection
- **Open source:** Full transparency
- **Easy to use:** Works automatically
- **Comprehensive:** 28+ entity types
- **Multi-platform:** Windows, Mac, Linux

### 🔧 Installation
1. Install extension from Chrome Web Store
2. Click extension icon → "Installation Wizard"
3. Follow OS-specific instructions (auto-detected)
4. Run installation script (one command)
5. Done! Start pasting with confidence

### ⚡ Quick Start
1. Install backend (5 minutes)
2. Enable extension toggle
3. Copy text with PII
4. Paste into ChatGPT/Gmail/etc
5. Watch it automatically anonymize!

### 🆘 Support
- GitHub Issues: https://github.com/gacabartosz/presidio-local-anonymizer/issues
- Documentation: Complete guides in repository
- Community: Open source project

### 🔍 Example
**Before:**
```
Jan Kowalski, email: jan@example.com,
PESEL: 92010212345, tel: +48 123 456 789
```

**After:**
```
[OSOBA], email: [EMAIL],
PESEL: [PESEL], tel: [TELEFON]
```

### 📜 License
MIT License - Free and open source

---

**Made with ❤️ by Bartosz Gaca**
**Powered by Microsoft Presidio**
```

**Kategoria:**
```
Developer Tools / Productivity
```

**Język:**
```
Polish (Primary)
English (Secondary)
```

**Privacy Policy URL:**
```
https://raw.githubusercontent.com/gacabartosz/presidio-local-anonymizer/main/PRIVACY_POLICY.md
```

**Homepage URL:**
```
https://github.com/gacabartosz/presidio-local-anonymizer
```

**Support URL:**
```
https://github.com/gacabartosz/presidio-local-anonymizer/issues
```

#### 3.4. Upload Screenshoty

```
Przeciągnij 3-5 screenshotów (1280x800px)
```

#### 3.5. Uzupełnij Dodatkowe Informacje

**Single Purpose:**
```
Automatically anonymize personally identifiable information (PII) when pasting text into web forms, AI chatbots, and websites.
```

**Permission Justifications:**

```
activeTab
Reason: Required to detect paste events and insert anonymized text into active webpage inputs.

storage
Reason: Store user preferences (backend URL, extension enabled/disabled state) locally.

contextMenus
Reason: Provide right-click context menu option "Anonymize selected text" for manual anonymization.

clipboardRead
Reason: Read clipboard content during paste events to anonymize PII before insertion.

host_permissions: http://localhost:4222/*, http://127.0.0.1:4222/*
Reason: Communicate with local Presidio backend running on localhost:4222 for PII detection and anonymization.
```

**Remote Code:**
```
No remote code is used. All code is bundled with the extension.
```

#### 3.6. Wybierz Regiony

```
Zaznacz:
- Poland (główny rynek)
- United States
- United Kingdom
- European Union
- Worldwide (opcjonalnie)
```

#### 3.7. Pricing & Distribution

```
Pricing: FREE
Distribution: Public
```

---

## 🎨 Krok 4: Opcjonalne - Promotional Graphics

### Promotional Tile (440x280px)
```
Grafika wyświetlana w Chrome Web Store

Zawartość:
- Logo Presidio
- Tytuł: "Presidio Browser Anonymizer"
- Slogan: "Auto-anonymize PII when pasting"
- Ikony: Lock 🔒, Shield 🛡️
```

### Small Promotional Tile (128x128px)
```
Miniatura w wynikach wyszukiwania

Zawartość:
- Logo Presidio (uproszczone)
- Ikona lock 🔒
```

---

## 🔍 Krok 5: Submit for Review

### Pre-Submit Checklist:

- [ ] ZIP uploaded correctly
- [ ] All required fields filled
- [ ] Screenshoty uploaded (min. 1)
- [ ] Privacy Policy URL works
- [ ] Permissions justified
- [ ] Description complete

### Submit:

```
1. Kliknij "Save Draft"
2. Sprawdź podgląd
3. Kliknij "Submit for Review"
4. Potwierdź submission
```

---

## ⏱️ Krok 6: Oczekiwanie na Approval

### Timeline:

- **Review time:** 1-3 dni robocze (często szybciej)
- **First submission:** Może trwać dłużej (nawet 5-7 dni)
- **Updates:** Zazwyczaj 1-2 dni

### Co się Dzieje:

1. **Automatic Checks** (5 minut)
   - Malware scan
   - Manifest validation
   - Policy compliance

2. **Manual Review** (1-3 dni)
   - Funkcjonalność
   - Permissions usage
   - Privacy policy
   - Store listing accuracy

3. **Approval / Rejection**
   - Email notification
   - If rejected: Fix issues → Resubmit

### Status Check:

```
Chrome Web Store Developer Dashboard
→ Items
→ Presidio Browser Anonymizer
→ Status: "Pending review" / "Published" / "Rejected"
```

---

## 📊 Krok 7: Post-Publication

### Po Aprobacie:

✅ Extension live on Chrome Web Store!
✅ Public URL: `https://chrome.google.com/webstore/detail/[YOUR-EXTENSION-ID]`
✅ Users can install directly from store

### Co Dalej:

1. **Add Extension URL to GitHub README**
   ```markdown
   ## Installation from Chrome Web Store

   [Install from Chrome Web Store](https://chrome.google.com/webstore/detail/YOUR-EXTENSION-ID)
   ```

2. **Monitor Reviews**
   - Odpowiadaj na pytania użytkowników
   - Fix reportowane bugi
   - Update extension regularnie

3. **Analytics**
   - Chrome Web Store Dashboard
   - Liczba instalacji
   - Liczba aktywnych użytkowników
   - Rating

4. **Future Updates**
   - Version bump w manifest.json
   - Create new ZIP
   - Upload jako update (instant review dla minor changes)

---

## 🛡️ Najczęstsze Problemy i Rozwiązania

### Problem 1: "Manifest validation failed"
**Rozwiązanie:** Sprawdź czy manifest.json jest poprawny JSON (użyj JSONLint)

### Problem 2: "Permissions not justified"
**Rozwiązanie:** Dodaj szczegółowe wyjaśnienie każdego permission w formularzu

### Problem 3: "Privacy policy not accessible"
**Rozwiązanie:** Sprawdź czy URL działa: https://raw.githubusercontent.com/gacabartosz/presidio-local-anonymizer/main/PRIVACY_POLICY.md

### Problem 4: "Screenshots required"
**Rozwiązanie:** Upload minimum 1 screenshot (1280x800px lub 640x400px)

### Problem 5: "Remote code detected"
**Rozwiązanie:** Upewnij się że nie używasz CDN ani zewnętrznych skryptów. Wszystko bundled w extension.

### Problem 6: "Description too vague"
**Rozwiązanie:** Dodaj konkretne przykłady użycia i features w opisie

---

## 📝 Quick Command Reference

### Sprawdź czy ZIP jest OK:
```bash
unzip -l presidio-extension-v1.3.4.zip

# Powinno pokazać:
# - manifest.json ✅
# - background.js ✅
# - content-script.js ✅
# - popup.html/js ✅
# - options.html/js ✅
# - icons/ (all 4 sizes) ✅
```

### Sprawdź Privacy Policy:
```bash
curl https://raw.githubusercontent.com/gacabartosz/presidio-local-anonymizer/main/PRIVACY_POLICY.md

# Powinno zwrócić pełny tekst Privacy Policy
```

### Sprawdź rozmiar ZIP:
```bash
ls -lh presidio-extension-v1.3.4.zip

# Powinno być ~33KB (max 100MB dla CWS)
```

---

## 🎯 Status: READY TO PUBLISH!

**Wszystko przygotowane:**
- ✅ ZIP package (33KB)
- ✅ Manifest V3 compliant
- ✅ Privacy Policy live
- ✅ Documentation complete
- ✅ Icons present
- ✅ Permissions justified

**Do zrobienia:**
- ⚠️ Screenshoty (3-5 sztuk, 1280x800px)
- ⚠️ Chrome Developer Account ($5 USD)
- ⚠️ Upload ZIP do Chrome Web Store
- ⚠️ Submit for review

**Przewidywany czas do publikacji:** 1-3 dni po submit

---

## 📞 Kontakt

- **GitHub:** https://github.com/gacabartosz/presidio-local-anonymizer
- **Issues:** https://github.com/gacabartosz/presidio-local-anonymizer/issues
- **Author:** Bartosz Gaca

---

**Good luck! 🚀**
