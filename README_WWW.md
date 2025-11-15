# 🌐 Logowanie przez WWW - Web Dashboard

## 🚀 Jak się zalogować i zobaczyć co się dzieje?

### KROK 1: Uruchom backend

```bash
cd /Users/gaca/presidio-local-anonymizer/backend
source .venv/bin/activate
python app.py
```

**Czekaj aż zobaczysz:**
```
============================================================
Presidio Browser Anonymizer - Backend Service
============================================================
Security token: dmROn8AMOxGC0HWAu7HYgKGFgMZoOYRGy7EVYxL7_OM
============================================================
 * Running on http://127.0.0.1:4222
```

---

### KROK 2: Otwórz Dashboard w przeglądarce

**Wejdź na adres:**
```
http://127.0.0.1:4222/dashboard
```

lub po prostu kliknij: [**localhost:4222/dashboard**](http://127.0.0.1:4222/dashboard)

---

## 📊 Co zobaczysz na dashboardzie?

### 1. **Status Serwisu**
- **● ONLINE** (zielony) - backend działa
- **● OFFLINE** (szary) - backend nie działa

### 2. **Security Token**
- Token wyświetlony na górze strony
- Przycisk **📋 Kopiuj** do szybkiego kopiowania
- Potrzebny do konfiguracji browser extension

### 3. **Statystyki Real-Time**
```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│   Status    │   Żądania   │ Wykryte dane│   Śr. czas  │
│  ● ONLINE   │     47      │     156     │    85ms     │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

- **Żądania** - ile razy użyto anonimizacji
- **Wykryte dane** - suma wykrytych danych osobowych
- **Śr. czas** - średni czas przetwarzania

### 4. **Wykrywane Typy Danych**
- 🔵 EMAIL_ADDRESS
- 🔵 PL_PESEL
- 🔵 PL_NIP
- 🔵 PHONE_NUMBER
- 🔵 URL
- 🔵 IP_ADDRESS
- 🔵 DATE_TIME
- 🔵 LOCATION

### 5. **🧪 Test Anonimizacji** (live testing)

Wpisz tekst z danymi:
```
Cześć, jestem Jan Kowalski
Email: jan.kowalski@example.com
PESEL: 92010212345
Telefon: +48 123 456 789
```

Kliknij **🚀 Testuj Anonimizację**

**Wynik:**
```
✅ Sukces! Czas: 1967ms

Oryginalny tekst:
Cześć, jestem Jan Kowalski, PESEL 92010212345, email jan@example.com

Zanonimizowany tekst:
Cześć, jestem Jan Kowalski, PESEL [PESEL], email [EMAIL]

Wykryte dane (3):
- EMAIL_ADDRESS: "jan@example.com" (pewność: 100%)
- PL_PESEL: "92010212345" (pewność: 60%)
- URL: "example.com" (pewność: 50%)
```

### 6. **📋 Logi Aktywności** (real-time)

```
[12:30:15] Token załadowany pomyślnie
[12:30:20] Wysyłanie żądania anonimizacji...
[12:30:22] ✅ Anonimizacja zakończona: 3 danych wykrytych w 1967ms
[12:31:05] Test wyczyszczony
```

Logi pokazują wszystko co się dzieje w czasie rzeczywistym.

---

## 🎯 Użycie Dashboard

### Scenariusz 1: Szybki test bez extension
1. Otwórz dashboard
2. Wklej tekst w pole testowe
3. Kliknij "Testuj"
4. Zobacz wyniki natychmiast

### Scenariusz 2: Monitorowanie extension
1. Otwórz dashboard
2. Używaj extension w ChatGPT/Claude
3. Obserwuj statystyki rosną w real-time
4. Sprawdzaj logi aktywności

### Scenariusz 3: Kopiowanie tokenu
1. Otwórz dashboard
2. Kliknij **📋 Kopiuj** obok tokenu
3. Wklej w extension popup
4. Kliknij "Save"

---

## 🖥️ Screenshot Dashboard

```
┌────────────────────────────────────────────────────────┐
│ 🔐 Presidio Browser Anonymizer                         │
│ Dashboard monitorowania i testowania                   │
├────────────────────────────────────────────────────────┤
│ ⚠️ Security Token: dmROn8A...L7_OM [📋 Kopiuj]        │
├────────────────────────────────────────────────────────┤
│                  Status Serwisu                        │
│  ┌──────┬──────────┬───────────┬─────────┐           │
│  │● ON  │    47    │    156    │  85ms   │           │
│  │Status│ Żądania  │ Wykryte   │ Śr.czas │           │
│  └──────┴──────────┴───────────┴─────────┘           │
├────────────────────────────────────────────────────────┤
│              🧪 Test Anonimizacji                      │
│  ┌──────────────────────────────────────┐            │
│  │ Wpisz tekst z danymi...              │            │
│  │                                       │            │
│  └──────────────────────────────────────┘            │
│  [🚀 Testuj] [🗑️ Wyczyść]                            │
├────────────────────────────────────────────────────────┤
│              📋 Logi Aktywności                        │
│  ┌──────────────────────────────────────┐            │
│  │ [12:30:15] Token załadowany          │            │
│  │ [12:30:22] ✅ 3 dane wykryte          │            │
│  └──────────────────────────────────────┘            │
└────────────────────────────────────────────────────────┘
```

---

## ⚡ Quick Links

| Link | Opis |
|------|------|
| [Dashboard](http://127.0.0.1:4222/dashboard) | Główny panel |
| [API Health](http://127.0.0.1:4222/api/health) | Status API |
| [API Token](http://127.0.0.1:4222/api/token) | Pobierz token (JSON) |
| [Root](http://127.0.0.1:4222/) | Info o serwisie |

---

## 🐛 Troubleshooting

### Dashboard nie ładuje się

**Sprawdź:**
1. Czy backend działa? → `curl http://127.0.0.1:4222/api/health`
2. Czy port 4222 jest wolny? → `lsof -i :4222`
3. Uruchom backend: `cd backend && source .venv/bin/activate && python app.py`

### "Offline" status

**Przyczyna:** Backend nie działa
**Rozwiązanie:** Uruchom backend (patrz KROK 1)

### Token nie wyświetla się

**Sprawdź:**
- Czy backend załadował SecurityManager?
- Sprawdź terminal - czy są błędy?

---

## 📱 Dostęp mobilny

Dashboard działa też z telefonu (jeśli jesteś w tej samej sieci WiFi):

1. Znajdź IP komputera: `ifconfig | grep inet`
2. Otwórz w telefonie: `http://[TWOJE_IP]:4222/dashboard`

**Przykład:** `http://192.168.1.100:4222/dashboard`

---

## 🎉 Gotowe!

Teraz masz pełny wgląd w to co się dzieje z anonimizacją:
- ✅ Status serwisu
- ✅ Statystyki
- ✅ Testy live
- ✅ Logi real-time
- ✅ Kopiowanie tokenu

**Miłego testowania!** 🚀
