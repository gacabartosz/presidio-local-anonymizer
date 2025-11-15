# 📦 Installation Guide - Presidio Browser Anonymizer

Complete installation guide from scratch. Follow these steps carefully.

---

## 📋 Prerequisites

Before you begin, make sure you have:

- **Python 3.11+** installed
- **Google Chrome** or **Microsoft Edge** browser
- **Git** installed (for cloning repository)
- **~500 MB free disk space** (for SpaCy model)

---

## 🚀 Installation Steps

### Step 1: Clone Repository

```bash
# Clone from GitHub
git clone -b browser-extension https://github.com/gacabartosz/presidio-local-anonymizer.git

# Navigate to project directory
cd presidio-local-anonymizer
```

### Step 2: Install Backend Dependencies

```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# OR
.venv\Scripts\activate  # On Windows

# Install Python packages
pip install -r requirements.txt

# Download Polish language model for SpaCy
pip install https://github.com/explosion/spacy-models/releases/download/pl_core_news_md-3.7.0/pl_core_news_md-3.7.0-py3-none-any.whl
```

**Expected output:**
```
Successfully installed Flask-3.0.0 presidio-analyzer-2.2.354 spacy-3.7.2 ...
Successfully installed pl-core-news-md-3.7.0
```

### Step 3: Start Backend

```bash
# Make sure you're in backend directory with activated venv
python app.py
```

**Expected output:**
```
============================================================
Presidio Browser Anonymizer - Backend Service
============================================================
Security token: dmROn8AMOxGC0HWAu7HYgKGFgMZoOYRGy7EVYxL7_OM
Extension will auto-load this token automatically
============================================================
 * Running on http://127.0.0.1:4222
```

✅ **Leave this terminal open!** Backend must run continuously.

### Step 4: Verify Backend is Running

Open another terminal and test:

```bash
curl http://127.0.0.1:4222/api/health
```

**Expected response:**
```json
{"service":"presidio-browser-anonymizer","status":"healthy","version":"1.0.0"}
```

### Step 5: Load Browser Extension

1. Open Chrome/Edge
2. Navigate to: `chrome://extensions/`
3. Enable **"Developer mode"** (toggle in top-right corner)
4. Click **"Load unpacked"** button
5. Select the `extension/` folder from cloned repository
6. Extension icon (blue "P") should appear in browser toolbar

### Step 6: Test Extension

1. Click extension icon (blue "P") in toolbar
2. Check status:
   - Should show: **● Connected** (green dot)
   - Toggle should be: **ON** (blue)

3. Open ChatGPT: https://chat.openai.com
4. Type test message:
   ```
   Hi, my email is jan@example.com and PESEL 92010212345
   ```
5. Wait 500ms
6. Text should change to:
   ```
   Hi, my email is [EMAIL] and PESEL [PESEL]
   ```
7. Notification appears: **"2 data anonymized"**

✅ **Success!** Extension is working correctly.

---

## 🌐 Access Web Interfaces

With backend running, you can access:

### Settings Page
```
http://127.0.0.1:4222
```
- Configure which data types to anonymize
- Interactive toggle switches
- Save/reset settings

### Dashboard
```
http://127.0.0.1:4222/dashboard
```
- Real-time statistics
- Test anonymization
- Activity logs
- Token management

---

## 🔧 Troubleshooting

### Backend won't start

**Error:** `Port 4222 is in use`

**Solution:**
```bash
# Find process using port 4222
lsof -i :4222

# Kill the process
kill -9 <PID>

# Try starting backend again
python app.py
```

### Extension shows "Offline"

**Possible causes:**
1. Backend not running → Start backend
2. Wrong port → Backend must run on 4222
3. Token not loaded → Reload extension

**Solution:**
```bash
# Restart backend
cd backend
source .venv/bin/activate
python app.py

# Reload extension in Chrome
chrome://extensions/ → Reload button
```

### SpaCy model fails to download

**Error:** `HTTP error 404`

**Solution:**
```bash
# Download model manually
pip install https://github.com/explosion/spacy-models/releases/download/pl_core_news_md-3.7.0/pl_core_news_md-3.7.0-py3-none-any.whl
```

### Text not anonymizing in ChatGPT

**Check:**
1. Extension is ON (toggle enabled)
2. Backend status shows "Connected"
3. Wait 500ms after typing (debounce)
4. Check service worker console for errors

**Debug:**
1. Open `chrome://extensions/`
2. Find extension
3. Click **"service worker"** link
4. Check console for errors

---

## 📁 Directory Structure

After installation, your directory should look like:

```
presidio-local-anonymizer/
├── backend/
│   ├── .venv/              # Python virtual environment
│   ├── api/                # REST endpoints
│   ├── core/               # Presidio integration
│   ├── storage/            # Security & token
│   └── requirements.txt    # Python dependencies
├── extension/
│   ├── background/         # Service worker
│   ├── content/            # Content scripts
│   ├── popup/              # Extension UI
│   └── manifest.json       # Extension config
├── web-ui/
│   ├── index.html          # Settings page
│   ├── dashboard.html      # Dashboard
│   └── favicon.ico
└── README.md               # Main documentation
```

---

## 🎯 Next Steps

1. **Configure entities:** Visit http://127.0.0.1:4222
2. **Test thoroughly:** Try different data types
3. **Read documentation:** Check README.md for advanced features
4. **Report issues:** https://github.com/gacabartosz/presidio-local-anonymizer/issues

---

## 🆘 Getting Help

If you encounter problems:

1. Check [Troubleshooting](#-troubleshooting) section above
2. Verify all prerequisites are met
3. Check backend logs in terminal
4. Check extension console (service worker)
5. Open issue on GitHub with:
   - Error message
   - System info (OS, Python version)
   - Steps to reproduce

---

## ✅ Verification Checklist

Before reporting issues, verify:

- [ ] Python 3.11+ installed (`python3 --version`)
- [ ] Virtual environment activated
- [ ] All dependencies installed (`pip list`)
- [ ] SpaCy model downloaded
- [ ] Backend starts without errors
- [ ] Port 4222 is free
- [ ] Extension loaded in Chrome
- [ ] Extension shows "Connected" status
- [ ] Tested on ChatGPT/Claude

---

**Installation complete!** 🎉

**Created by [bartoszgaca.pl](https://bartoszgaca.pl) & [Claude Code](https://claude.ai)**
