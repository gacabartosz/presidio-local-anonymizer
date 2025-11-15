# 🔐 Presidio Browser Anonymizer

**Chrome Extension + Local Backend - Auto-anonymize PII when pasting text!**

Automatically anonymize personal data when pasting into ChatGPT, Gmail, forms, and any website. Powered by Microsoft Presidio. Works 100% locally - no data leaves your computer.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Chrome Extension](https://img.shields.io/badge/chrome-extension-brightgreen.svg)
![Version](https://img.shields.io/badge/version-1.3.0-blue.svg)

---

## ✨ Features

- 🚀 **Auto-Paste Anonymization (NEW!)** - Automatically anonymizes when you paste (Ctrl+V) anywhere!
- ✅ **Zero configuration** - One-click installation scripts for Windows/Mac/Linux
- ✅ **100% offline** - Everything runs locally, no data leaves your machine
- ✅ **Microsoft Presidio** - Professional PII detection engine
- ✅ **28 entity types** - PESEL, NIP, emails, phones, credit cards, passports, IDs
- ✅ **Polish language optimized** - Native support for Polish PII
- ✅ **Works everywhere** - ChatGPT, Gmail, forms, content-editable fields
- ✅ **Web Dashboard** - Real-time monitoring and testing

---

## 🚀 Quick Installation

> **📖 Full Documentation:** [INSTALLATION.md](INSTALLATION.md) - Complete step-by-step guide with troubleshooting

### Windows

1. Download project and run installer:
   ```cmd
   git clone https://github.com/gacabartosz/presidio-local-anonymizer
   cd presidio-local-anonymizer
   install-windows.bat
   ```

2. Install Chrome extension:
   - Open `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked" → select `chrome-extension/` folder

3. **Done!** Start pasting text and it will be auto-anonymized!

### macOS

1. Download project and run installer:
   ```bash
   git clone https://github.com/gacabartosz/presidio-local-anonymizer
   cd presidio-local-anonymizer
   ./install-mac.sh
   ```

2. Install Chrome extension:
   - Open `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked" → select `chrome-extension/` folder

3. **Done!** Start pasting text and it will be auto-anonymized!

### Linux

1. Download project and run installer:
   ```bash
   git clone https://github.com/gacabartosz/presidio-local-anonymizer
   cd presidio-local-anonymizer
   ./install-linux.sh
   ```

2. Install Chrome extension:
   - Open `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked" → select `chrome-extension/` folder

3. **Done!** Start pasting text and it will be auto-anonymized!

---

## 🎯 How It Works

### Auto-Paste Anonymization (Primary Method)

1. **Copy text with PII:**
   ```
   Mój PESEL: 44051401359, email: jan@example.com, tel: +48 123 456 789
   ```

2. **Paste anywhere (Ctrl+V):**
   - ChatGPT prompt
   - Gmail compose
   - Any form field
   - Content-editable areas

3. **Text automatically anonymized:**
   ```
   Mój PESEL: [PESEL], email: [EMAIL], tel: [TELEFON]
   ```

### Alternative Methods

**Keyboard Shortcut:** Select text → Press `Ctrl+Shift+A` (Mac: `Cmd+Shift+A`)

**Context Menu:** Select text → Right-click → "Anonimizuj zaznaczony tekst"

---

## 📊 Web Dashboard

Open in browser: **http://127.0.0.1:4222/dashboard**

Dashboard shows:
- ✅ Service status (online/offline)
- 📊 Statistics (requests, detected data, time)
- 🧪 Live anonymization testing (without extension)
- 📋 Activity logs (real-time)
- 🔑 Security token (auto-copy)

---

## 🎯 How It Works

1. **You type text** in ChatGPT/Claude:
   ```
   Hi, I'm Jan Kowalski, PESEL 92010212345, email jan@example.com
   ```

2. **Extension detects data** and sends to localhost:4222

3. **Backend anonymizes** using Microsoft Presidio

4. **Text gets replaced** (after 500ms debounce):
   ```
   Hi, I'm Jan Kowalski, PESEL [PESEL], email [EMAIL]
   ```

5. **Notification** appears in top-right corner: "2 data anonymized"

---

## 🔒 Detected Data Types

### 🇵🇱 Polskie dane (domyślnie włączone):

| Type | Example | Mask | Enabled |
|------|---------|------|---------|
| EMAIL | jan@example.com | [EMAIL] | ✅ |
| PL_PESEL | 92010212345 | [PESEL] | ✅ |
| PL_NIP | 123-456-78-90 | [NIP] | ✅ |
| PL_PASSPORT | AB1234567 | [PASZPORT_PL] | ✅ |
| PL_ID_CARD | ABC123456 | [DOWOD_PL] | ✅ |
| PHONE_NUMBER | +48 123 456 789 | [TELEFON] | ✅ |
| CREDIT_CARD | 4532-1234-5678-9010 | [KARTA] | ✅ |
| IBAN_CODE | PL61109010140000071219812874 | [IBAN] | ✅ |
| IP_ADDRESS | 192.168.1.1 | [IP] | ✅ |
| URL | https://example.com | [URL] | ✅ |
| DATE_TIME | 2024-12-10 | [DATA] | ✅ |
| LOCATION | Warsaw | [LOKALIZACJA] | ✅ |

### 🌍 Dane międzynarodowe (domyślnie wyłączone):

| Type | Example | Mask | Country |
|------|---------|------|---------|
| US_SSN | 123-45-6789 | [SSN] | 🇺🇸 USA |
| US_PASSPORT | 123456789 | [PASZPORT_US] | 🇺🇸 USA |
| US_BANK_NUMBER | 123456789 | [BANK_US] | 🇺🇸 USA |
| US_DRIVER_LICENSE | D1234567 | [PRAWO_JAZDY_US] | 🇺🇸 USA |
| US_ITIN | 912-34-5678 | [ITIN] | 🇺🇸 USA |
| UK_NHS | 123 456 7890 | [NHS] | 🇬🇧 UK |
| AU_ABN | 12 345 678 901 | [ABN] | 🇦🇺 Australia |
| AU_ACN | 123 456 789 | [ACN] | 🇦🇺 Australia |
| AU_TFN | 123 456 782 | [TFN] | 🇦🇺 Australia |
| AU_MEDICARE | 1234 56789 0 | [MEDICARE_AU] | 🇦🇺 Australia |
| SG_NRIC_FIN | S1234567D | [NRIC_SG] | 🇸🇬 Singapore |

### 🔐 Inne dane:

| Type | Example | Mask | Enabled |
|------|---------|------|---------|
| PERSON | Jan Kowalski | [OSOBA] | ❌ (off by default) |
| CRYPTO | 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa | [CRYPTO] | ❌ |
| MEDICAL_LICENSE | MD123456 | [LICENCJA_MED] | ❌ |
| PL_REGON | 123456789 | [REGON] | ❌ |
| NRP | AB123456C | [NRP] | ❌ |

**Razem: 27 typów danych osobowych!**

Możesz włączyć/wyłączyć każdy typ w Settings: http://127.0.0.1:4222

---

## 🧪 Testing

### Test on ChatGPT:

1. Open https://chat.openai.com
2. Type in textarea:
   ```
   Hi, I'm Jan Kowalski, PESEL 92010212345, email jan@example.com
   ```
3. **Wait 500ms** (extension processes in background)
4. **See result:**
   - Text changes to: `"PESEL [PESEL], email [EMAIL]"`
   - Notification in top-right: **"2 data anonymized"**
   - Textarea flashes green border

✅ **It works!**

### Test on Dashboard:

1. Open http://127.0.0.1:4222/dashboard
2. In "Test anonymization" section, paste test text
3. Click "Test anonymization"
4. See results with statistics

---

## 🐛 Troubleshooting

### Extension shows "Offline"

**Problem:** Backend not running or token not loaded.

**Solution:**
```bash
# Start backend
cd backend
source .venv/bin/activate
python app.py
```

Then reload extension:
1. Open `chrome://extensions/`
2. Find "Presidio Browser Anonymizer"
3. Click 🔄 **Reload** button

### Text not anonymizing

**Check:**
1. Extension is enabled (toggle = ON in popup)
2. Backend is running (status = Connected)
3. Wait 500ms after typing (debounce delay)
4. Check service worker console for errors

### How to check service worker console

1. Open `chrome://extensions/`
2. Find extension
3. Click **"service worker"** link (under "Inspect views")
4. See console logs - should show:
   ```
   [Presidio] Service worker loaded
   [Presidio] Token loaded from cache ✓
   ```

### "Missing authentication token" error

**Solution:** Extension auto-loads token on first use. If error persists:
1. Reload extension (chrome://extensions/ → Reload)
2. Open popup (click extension icon)
3. Token loads automatically from backend

---

## 📦 Project Structure

```
presidio-local-anonymizer/
├── backend/              # Flask API (localhost:4222)
│   ├── app.py           # Main server
│   ├── api/             # REST endpoints
│   ├── core/            # Presidio integration
│   └── storage/         # Security & token
│
├── extension/           # Browser Extension (Manifest V3)
│   ├── manifest.json
│   ├── background/      # Service worker
│   ├── content/         # Content scripts
│   ├── popup/           # UI panel
│   └── icons/           # Extension icons
│
├── web-ui/              # Web Dashboard
│   ├── dashboard.html   # Real-time monitoring
│   └── favicon.ico
│
└── assets/              # Logo & branding
```

---

## 🛠️ Tech Stack

**Backend:**
- Flask 3.0
- Microsoft Presidio 2.2.354
- SpaCy 3.7.2 (Polish model)
- SQLite (storage)

**Extension:**
- Manifest V3
- Vanilla JavaScript
- Auto-connect to localhost

**Dashboard:**
- HTML/CSS/JavaScript
- Real-time updates
- Responsive design

---

## 🔧 Requirements

- **Python 3.11+**
- **Chrome/Edge browser**
- **macOS/Linux/Windows**
- **~500 MB disk** (SpaCy model)

---

## ⚡ Performance

- **Detection:** ~50-100ms
- **Anonymization:** ~1-2s (first call), ~50ms (subsequent)
- **Debounce:** 500ms (doesn't block typing)

---

## 💡 FAQ

### Q: Do I need to copy/paste a token?
**A:** NO! Extension automatically fetches token from backend. Nothing to configure.

### Q: Extension shows "Offline"?
**A:** Backend not running. Start: `cd backend && source .venv/bin/activate && python app.py`

### Q: Text doesn't anonymize?
**A:** Check:
1. Extension is ON (toggle enabled)
2. Backend running (status Connected)
3. Wait 500ms after typing

### Q: Where can I see what's happening?
**A:** Open dashboard: http://127.0.0.1:4222/dashboard
- Real-time statistics
- Activity logs
- Test anonymization

### Q: Must I always keep terminal open?
**A:** Yes, backend must run in background. You can minimize terminal.

**Optional:** Create alias in `.zshrc`:
```bash
alias presidio='cd /path/to/presidio-local-anonymizer/backend && source .venv/bin/activate && python app.py'
```

Then just: `presidio` 🚀

---

## 🤝 Contributing

1. Fork repo
2. Create branch: `git checkout -b feature/name`
3. Commit: `git commit -m "feat: description"`
4. Push: `git push origin feature/name`
5. Create Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 🙏 Credits

- **Microsoft Presidio** - PII detection engine
- **SpaCy** - NLP for Polish language
- **Flask** - lightweight web framework

---

## ⚠️ Disclaimer

This tool helps protect personal data, but:
- ❌ Does NOT guarantee 100% detection of all data
- ❌ Always verify results before sending
- ❌ Use with caution for sensitive data

**We recommend always reviewing anonymized text before sending.**

---

## 📮 Support

Having problems? Check:
- [GitHub Issues](https://github.com/gacabartosz/presidio-local-anonymizer/issues)
- [Web Dashboard](http://127.0.0.1:4222/dashboard) - service status

---

**Made with ❤️ using Claude Code**
