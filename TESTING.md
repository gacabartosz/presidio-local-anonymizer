# Testing Guide - Presidio Browser Anonymizer

## 📦 Co zostało zaimplementowane:

### ✅ FAZA 1 - Backend API (localhost:4222)
- Flask server z Microsoft Presidio
- Endpoints: `/api/health`, `/api/anonymize`, `/api/config`
- Token authentication
- CORS dla browser extension
- Wykrywanie: EMAIL, PESEL, NIP, URL

### ✅ FAZA 2 - Browser Extension (MVP)
- Manifest V3
- Service worker - komunikacja z API
- Content script - injection do ChatGPT/Claude/Perplexity
- Popup UI - konfiguracja
- Real-time anonimizacja
- Visual feedback

---

## 🚀 Instrukcja testowania na macOS

### KROK 1: Uruchom backend

```bash
cd /Users/gaca/presidio-local-anonymizer/backend

# Aktywuj virtual environment
source .venv/bin/activate

# Uruchom server
python app.py
```

**Powinieneś zobaczyć:**
```
============================================================
Presidio Browser Anonymizer - Backend Service
============================================================
Security token: dmROn8AMOxGC0HWAu7HYgKGFgMZoOYRGy7EVYxL7_OM
Copy this token to browser extension settings
============================================================
 * Running on http://127.0.0.1:4222
```

**✅ Skopiuj token!** Będzie potrzebny w kroku 3.

**💡 ALTERNATYWNIE:** Otwórz **Web Dashboard** w przeglądarce:
```
http://127.0.0.1:4222/dashboard
```

Dashboard pokazuje:
- ✅ Status serwisu (online/offline)
- 🔑 Security Token (auto-kopiowanie)
- 🧪 Test anonimizacji (bez extension)
- 📊 Statystyki (liczba żądań, wykryte dane)
- 📋 Logi aktywności w czasie rzeczywistym

---

### KROK 2: Załaduj extension w Chrome

1. Otwórz Chrome
2. Wejdź na: `chrome://extensions/`
3. Włącz **"Developer mode"** (prawy górny róg)
4. Kliknij **"Load unpacked"**
5. Wybierz folder: `/Users/gaca/presidio-local-anonymizer/extension`

**Powinieneś zobaczyć:**
- Extension załadowany
- Ikona extension w pasku narzędzi (może być placeholder)

---

### KROK 3: Skonfiguruj extension

1. Kliknij ikonę extension (prawy górny róg Chrome)
2. W popup wpisz **API Token** (skopiowany z kroku 1)
3. Kliknij **"Save"**
4. Sprawdź status:
   - **Zielony punkt** = Connected ✅
   - **Czerwony punkt** = Backend nie działa ❌

---

### KROK 4: Testuj anonimizację

#### Test 1: ChatGPT (https://chat.openai.com)

1. Otwórz ChatGPT w nowym tabie
2. W textarea wpisz:
   ```
   Cześć, jestem Jan Kowalski, PESEL 92010212345, email jan@example.com
   ```
3. **Poczekaj 500ms** (debounce)
4. **Sprawdź:**
   - Tekst został zamieniony na: `"Cześć, jestem Jan Kowalski, PESEL [PESEL], email [EMAIL]"`
   - Zielona notyfikacja w prawym górnym rogu: "2 dane zanonimizowane"
   - Textarea mignie zielonym obramowaniem

#### Test 2: Claude AI (https://claude.ai)

1. Otwórz Claude AI
2. Wklej tekst z danymi (Cmd+V)
3. Sprawdź anonimizację

#### Test 3: Perplexity (https://www.perplexity.ai)

1. Otwórz Perplexity
2. Wpisz tekst z danymi
3. Sprawdź anonimizację

---

### KROK 5: Testuj popup

1. Kliknij ikonę extension
2. Sprawdź:
   - **Status:** "Connected" (zielony)
   - **Toggle:** Auto-anonymize (włączony)
   - **Token:** Zapisany
3. Wyłącz toggle → anonimizacja przestaje działać
4. Włącz toggle → anonimizacja wraca

---

## 🧪 Test backend (bez extension)

```bash
# Test health
curl http://127.0.0.1:4222/api/health

# Test anonymize (z tokenem)
curl -X POST http://127.0.0.1:4222/api/anonymize \
  -H "Content-Type: application/json" \
  -H "X-Presidio-Token: dmROn8AMOxGC0HWAu7HYgKGFgMZoOYRGy7EVYxL7_OM" \
  -d '{"text": "Jan Kowalski, PESEL 92010212345, jan@example.com"}' \
  | python3 -m json.tool
```

**Oczekiwany wynik:**
```json
{
  "anonymized_text": "Jan Kowalski, PESEL [PESEL], [EMAIL]",
  "entities_found": [
    {"type": "EMAIL_ADDRESS", "text": "jan@example.com", "score": 1.0},
    {"type": "PL_PESEL", "text": "92010212345", "score": 0.6},
    {"type": "URL", "text": "example.com", "score": 0.5}
  ],
  "stats": {
    "total_entities": 3,
    "processing_time_ms": ~2000
  }
}
```

---

## 🐛 Troubleshooting

### Problem: Extension "Offline" (czerwony status)

**Rozwiązanie:**
1. Sprawdź czy backend działa: `curl http://127.0.0.1:4222/api/health`
2. Jeśli nie działa, uruchom: `cd backend && source .venv/bin/activate && python app.py`

### Problem: "Invalid token"

**Rozwiązanie:**
1. Sprawdź token w backend logs
2. Skopiuj dokładnie (bez spacji!)
3. Wklej do extension popup → Save

### Problem: Tekst nie jest anonimizowany

**Sprawdź:**
1. Extension jest włączony (toggle = ON)
2. Backend działa (zielony status)
3. Token jest poprawny
4. Czekasz 500ms po wpisaniu tekstu (debounce)
5. Sprawdź console (F12) → szukaj `[Presidio]` logs

### Problem: "Jan Kowalski" nie jest anonimizowany

**To normalne!**
- PERSON recognizer nie jest jeszcze zaimplementowany (FAZA 1.6)
- Obecnie wykrywane: EMAIL, PESEL, NIP, URL

---

## 📊 Status implementacji

| Faza | Status | Opis |
|------|--------|------|
| FAZA 0 | ✅ DONE | Struktura projektu |
| FAZA 1 | ✅ DONE | Backend API (localhost:4222) |
| FAZA 2.1-2.8 | ✅ DONE | Browser Extension MVP |
| FAZA 2.9 | ⏳ PENDING | Testowanie extension |
| FAZA 3 | ⏳ PENDING | Dashboard UI |
| FAZA 4 | ⏳ PENDING | Installer |

---

## 📍 GitHub

**Branch:** `browser-extension`
**Commits:** 3
**Link:** https://github.com/gacabartosz/presidio-local-anonymizer/tree/browser-extension

---

## 🎯 Następne kroki

1. **Testy extension** - sprawdź czy działa na ChatGPT/Claude/Perplexity
2. **Dashboard** - web UI do konfiguracji (FAZA 3)
3. **Installer** - automatyczna instalacja (FAZA 4)
4. **PERSON recognizer** - wykrywanie imion i nazwisk (FAZA 1.6)

---

**Powodzenia w testach!** 🚀

Jeśli coś nie działa, sprawdź browser console (F12) i backend logs.
