# 🔐 Presidio Browser Anonymizer

**Real-time text anonymization for ChatGPT, Claude AI, and Perplexity using Microsoft Presidio**

Automatically anonymize personal data before sending it to AI chatbots. Works locally (100% offline) with Microsoft Presidio.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

---

## ✨ Features

- ✅ **Real-time anonymization** - automatic textarea monitoring before sending
- ✅ **Zero configuration** - install and it works (auto-connect to backend)
- ✅ **100% offline** - everything runs locally, no data leaves your machine
- ✅ **Microsoft Presidio** - professional PII detection engine
- ✅ **Polish data support** - PESEL, NIP
- ✅ **Web Dashboard** - real-time monitoring and testing
- ✅ **Multi-platform** - ChatGPT, Claude AI, Perplexity

---

## 🚀 Quick Start (3 Steps)

> **📦 Full Installation Guide:** See [INSTALL.md](INSTALL.md) for complete step-by-step instructions from scratch.

### Step 1: Start Backend

```bash
cd backend
source .venv/bin/activate
python app.py
```

**Leave terminal open!** Backend must run in background.

### Step 2: Load Extension in Chrome

1. Open `chrome://extensions/`
2. Enable **"Developer mode"** (top right)
3. Click **"Load unpacked"**
4. Select `extension/` folder

### Step 3: Done!

Extension will automatically connect to backend. Check status:
- Click extension icon (blue "P")
- Status should show: **● Connected** ✅

**That's it!** Type in ChatGPT/Claude - data will be automatically anonymized.

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

| Type | Example | Mask |
|------|---------|------|
| EMAIL | jan@example.com | [EMAIL] |
| PL_PESEL | 92010212345 | [PESEL] |
| PL_NIP | 123-456-78-90 | [NIP] |
| PHONE_NUMBER | +48 123 456 789 | [TELEFON] |
| URL | https://example.com | [URL] |
| IP_ADDRESS | 192.168.1.1 | [IP] |
| DATE_TIME | 2024-12-10 | [DATA] |
| LOCATION | Warsaw | [LOKALIZACJA] |

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
