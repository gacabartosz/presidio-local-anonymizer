# 🔐 Presidio Browser Anonymizer

**Real-time text anonymization for ChatGPT, Claude AI, and Perplexity**

Automatycznie anonimizuj dane osobowe zanim wyślesz je do AI chatbotów. Działa lokalnie (100% offline) z Microsoft Presidio.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

---

## ✨ Features

- ✅ **Real-time anonimizacja** - automatycznie w textarea przed wysłaniem
- ✅ **Zero konfiguracji** - zainstaluj i działa (auto-connect do backendu)
- ✅ **100% offline** - wszystko działa lokalnie, żadne dane nie wychodzą
- ✅ **Microsoft Presidio** - profesjonalne wykrywanie PII
- ✅ **Polskie dane** - PESEL, NIP, REGON
- ✅ **Web Dashboard** - monitorowanie i testy w czasie rzeczywistym
- ✅ **Multi-platform** - ChatGPT, Claude AI, Perplexity

---

## 🚀 Quick Start (3 kroki)

### 1. Uruchom backend

```bash
cd backend
source .venv/bin/activate
python app.py
```

Zostaw terminal otwarty! Backend musi działać w tle.

### 2. Załaduj extension w Chrome

1. Otwórz `chrome://extensions/`
2. Włącz **"Developer mode"**
3. Kliknij **"Load unpacked"**
4. Wybierz folder `extension/`

### 3. Gotowe!

Extension automatycznie połączy się z backendem. Sprawdź status:
- Kliknij ikonę extension
- Status powinien być: **● ONLINE** ✅

**To wszystko!** Teraz pisz w ChatGPT/Claude - dane będą automatycznie anonimizowane.

---

## 📊 Web Dashboard

Otwórz w przeglądarce: **http://127.0.0.1:4222/dashboard**

Dashboard pokazuje:
- ✅ Status serwisu (online/offline)
- 📊 Statystyki (żądania, wykryte dane, czas)
- 🧪 Test anonimizacji (live, bez extension)
- 📋 Logi aktywności (real-time)
- 🔑 Security token (auto-kopiowanie)

---

## 🎯 Jak to działa?

1. **Wpisujesz tekst** w ChatGPT/Claude:
   ```
   Cześć, jestem Jan Kowalski, PESEL 92010212345, email jan@example.com
   ```

2. **Extension wykrywa dane** i wysyła do localhost:4222

3. **Backend anonimizuje** używając Microsoft Presidio

4. **Tekst zostaje podmieniony** (po 500ms debounce):
   ```
   Cześć, jestem Jan Kowalski, PESEL [PESEL], email [EMAIL]
   ```

5. **Notyfikacja** pojawia się w prawym górnym rogu: "2 dane zanonimizowane"

---

## 📦 Struktura projektu

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
│   └── dashboard.html   # Real-time monitoring
│
└── assets/              # Logo & branding
```

---

## 🔒 Wykrywane dane

| Typ | Przykład | Maska |
|-----|----------|-------|
| EMAIL | jan@example.com | [EMAIL] |
| PL_PESEL | 92010212345 | [PESEL] |
| PL_NIP | 123-456-78-90 | [NIP] |
| PHONE_NUMBER | +48 123 456 789 | [TELEFON] |
| URL | https://example.com | [URL] |
| IP_ADDRESS | 192.168.1.1 | [IP] |
| DATE_TIME | 2024-12-10 | [DATA] |
| LOCATION | Warszawa | [LOKALIZACJA] |

---

## 📚 Dokumentacja

- **[INSTALACJA_PROSTA.md](INSTALACJA_PROSTA.md)** - Prosta instalacja (3 kroki)
- **[README_WWW.md](README_WWW.md)** - Jak logować przez WWW dashboard
- **[TESTING.md](TESTING.md)** - Instrukcje testowania

---

## 🛠️ Tech Stack

**Backend:**
- Flask 3.0
- Microsoft Presidio 2.2.354
- SpaCy 3.7.2 (polski model)
- SQLite (storage)

**Extension:**
- Manifest V3
- Vanilla JavaScript
- Auto-connect do localhost

**Dashboard:**
- HTML/CSS/JavaScript
- Real-time updates
- Responsive design

---

## 🔧 Wymagania

- **Python 3.11+**
- **Chrome/Edge browser**
- **macOS/Linux/Windows**
- **~500 MB dysku** (model SpaCy)

---

## ⚡ Performance

- **Wykrywanie:** ~50-100ms
- **Anonimizacja:** ~1-2s (pierwsze wywołanie), ~50ms (kolejne)
- **Debounce:** 500ms (nie blokuje wpisywania)

---

## 🤝 Contributing

1. Fork repo
2. Stwórz branch: `git checkout -b feature/nazwa`
3. Commit: `git commit -m "feat: opis"`
4. Push: `git push origin feature/nazwa`
5. Stwórz Pull Request

---

## 📄 License

MIT License - patrz [LICENSE](LICENSE)

---

## 🙏 Credits

- **Microsoft Presidio** - PII detection engine
- **SpaCy** - NLP dla języka polskiego
- **Flask** - lightweight web framework

---

## ⚠️ Disclaimer

To narzędzie pomaga chronić dane osobowe, ale:
- ❌ Nie daje 100% gwarancji wykrycia wszystkich danych
- ❌ Zawsze weryfikuj wyniki przed wysłaniem
- ❌ Używaj z rozwagą w przypadku wrażliwych danych

**Zalecamy zawsze przeglądać zanonimizowany tekst przed wysłaniem.**

---

## 📮 Support

Masz problem? Sprawdź:
- [TESTING.md](TESTING.md) - troubleshooting
- [GitHub Issues](https://github.com/gacabartosz/presidio-local-anonymizer/issues)
- [Web Dashboard](http://127.0.0.1:4222/dashboard) - status serwisu

---

**Made with ❤️ using Claude Code**
