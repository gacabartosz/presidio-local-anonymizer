# Plan czyszczenia repo - Browser Extension

## ❌ DO USUNIĘCIA (stare pliki desktop app):

### Stare katalogi:
- `app/` - stary kod GUI (tkinter)
- `processors/` - stare procesory DOCX/PDF
- `config/` - stara konfiguracja (jest w backend/config/)
- `scripts/` - stare skrypty instalacyjne
- `tests/` - stare testy
- `installer/` - stary installer

### Stare pliki:
- `requirements.txt` (w roota - jest w backend/)
- `README.md` - stary (o desktop app)
- `README_LAIK.md` - stary
- `PROSTY_START.md` - stary
- `MANUAL_INSTALL.md` - stary
- `INSTALLATION_SUMMARY.md` - stary
- `INSTALLATION_TESTS.md` - stary
- `SPACY_MODEL_FIX.md` - stary
- `TEST_OCR.md` - stary
- `TROUBLESHOOTING.md` - stary
- `CROSS_PLATFORM_TEST_MATRIX.md` - stary
- `quick-start.sh` - stary
- `install-standalone.sh` - stary
- `presidio_anonymizer.log` - log file

## ✅ DO ZACHOWANIA:

- `backend/` - nowy backend API ✅
- `extension/` - nowy browser extension ✅
- `web-ui/` - dashboard ✅
- `assets/` - logo ✅
- `INSTALACJA_PROSTA.md` - nowa instrukcja ✅
- `README_WWW.md` - instrukcja WWW ✅
- `TESTING.md` - instrukcje testowania ✅
- `LICENSE` - licencja MIT ✅
- `VERSION` - wersja ✅
- `.gitignore` ✅

## ➕ DO DODANIA:

- `README.md` - NOWY główny README dla browser extension
- `web-ui/favicon.ico` - favicon dla dashboard
- `docs/API.md` - dokumentacja API

## 📝 Struktura po czyszczeniu:

```
presidio-local-anonymizer/
├── backend/              # Flask API
├── extension/            # Browser extension
├── web-ui/              # Dashboard
├── assets/              # Logo/ikony
├── docs/                # Dokumentacja
├── README.md            # Główny README (NOWY)
├── INSTALACJA_PROSTA.md # Prosta instrukcja
├── README_WWW.md        # Instrukcja WWW
├── TESTING.md           # Testowanie
├── LICENSE
├── VERSION
└── .gitignore
```

Czyste, uporządkowane, bez starych plików! ✨
