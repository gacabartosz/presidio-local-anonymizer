<div align="center">
  <img src="assets/logo-banner.svg" alt="Presidio Local Anonymizer" width="600"/>
</div>

<br/>

# Presidio Local Anonymizer

> System anonimizacji dokumentów DOCX/ODT z wykorzystaniem Microsoft Presidio - działa offline, wykrywa polskie dane osobowe

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Windows | macOS | Linux](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue.svg)](https://github.com/gacabartosz/presidio-local-anonymizer)

</div>

## Przegląd

**Presidio Local Anonymizer** to narzędzie CLI do automatycznej anonimizacji danych osobowych (PII) w dokumentach biurowych. Wykorzystuje bibliotekę [Microsoft Presidio](https://github.com/microsoft/presidio) i działa całkowicie **offline** - nie wymaga połączenia z internetem ani wysyłania danych do zewnętrznych API.

> 📖 **Szukasz prostej instrukcji?** Zobacz [README_LAIK.md](README_LAIK.md) - instrukcja krok po kroku dla osób nie-technicznych!

### Kluczowe funkcje

✅ **Offline First** - wszystkie operacje wykonywane lokalnie na Twoim komputerze
✅ **Obsługa polskich danych** - wykrywa PESEL, NIP, imiona, nazwiska
✅ **Formaty dokumentów** - DOCX (Microsoft Word), ODT (LibreOffice), PDF
✅ **OCR dla skanów** - Tesseract OCR dla skanowanych PDF i obrazów (PNG, JPG, TIFF)
✅ **Integracja z systemem** - menu kontekstowe (prawy przycisk myszy) na Windows, macOS i Linux
✅ **Przetwarzanie wsadowe** - obsługa pojedynczych plików i całych folderów
✅ **Raporty JSON** - szczegółowe informacje o wykrytych danych
✅ **Konfigurowalność** - dostosuj wykrywane encje i maski w YAML
✅ **GUI (interfejs graficzny)** - prosty interfejs z paskiem postępu

### Wykrywane typy danych osobowych

- 👤 **PERSON** - imiona i nazwiska
- 📧 **EMAIL_ADDRESS** - adresy email
- 📱 **PHONE_NUMBER** - numery telefonów
- 🆔 **PL_PESEL** - polskie numery PESEL
- 🏢 **PL_NIP** - polskie numery NIP
- 📍 **LOCATION** - lokalizacje geograficzne
- 📅 **DATE_TIME** - daty i czas
- 🌐 **URL** - adresy internetowe
- 💻 **IP_ADDRESS** - adresy IP

## Wymagania systemowe

### Windows
- **System operacyjny:** Windows 10 lub Windows 11
- **Wolne miejsce:** ~500 MB (dla instalacji i zależności)
- **Uprawnienia:** Instalacja w katalogu użytkownika (nie wymaga praw administratora)

### macOS
- **System operacyjny:** macOS 10.15 (Catalina) lub nowszy
- **Wolne miejsce:** ~1 GB (dla instalacji, Homebrew i zależności)
- **Uprawnienia:** Instalacja w katalogu użytkownika, Homebrew może wymagać hasła

### Linux
- **System operacyjny:** Ubuntu 20.04+, Debian 10+, Fedora 30+
- **Wolne miejsce:** ~500 MB (dla instalacji i zależności)
- **Uprawnienia:** Python 3.11+, Git, Tesseract OCR (instalowane przez użytkownika)

## Instalacja

### 🪟 Windows

**Metoda 1: One-liner PowerShell (zalecana)**

Otwórz PowerShell i uruchom:

```powershell
iwr https://raw.githubusercontent.com/gacabartosz/presidio-local-anonymizer/main/scripts/install.ps1 | iex
```

**Metoda 2: Pobranie i uruchomienie skryptu**

1. Pobierz [`scripts/install.ps1`](https://raw.githubusercontent.com/gacabartosz/presidio-local-anonymizer/main/scripts/install.ps1)
2. Kliknij prawym przyciskiem → **Run with PowerShell**

**Co zostanie zainstalowane:**
- ✅ Python 3.11, Git (jeśli brak)
- ✅ Tesseract OCR (dla skanów i obrazów)
- ✅ Repozytorium + środowisko wirtualne Python
- ✅ Wszystkie zależności (Presidio, SpaCy, PyPDF2, OCR libs)
- ✅ Model językowy SpaCy dla języka polskiego
- ✅ Polski model językowy dla Tesseract OCR
- ✅ Wpis w menu kontekstowym Windows
- ✅ Narzędzie w PATH

**Lokalizacja:** `%LOCALAPPDATA%\PresidioAnon`
**Czas instalacji:** ~10-15 minut

### 🍎 macOS

**One-liner Bash (zalecana)**

Otwórz Terminal i uruchom:

```bash
curl -fsSL https://raw.githubusercontent.com/gacabartosz/presidio-local-anonymizer/main/scripts/install.sh | bash
```

**Co zostanie zainstalowane:**
- ✅ Homebrew (jeśli brak)
- ✅ Python 3.11, Git, Tesseract OCR
- ✅ Repozytorium + środowisko wirtualne Python
- ✅ Wszystkie zależności
- ✅ Modele językowe (SpaCy + Tesseract polski)
- ✅ Usługa Automator (Quick Actions w Finder)
- ✅ Narzędzie w PATH (.zshrc/.bashrc)

**Lokalizacja:** `~/Library/Application Support/PresidioAnon`
**Czas instalacji:** ~10-15 minut
**⚠️ WAŻNE:** Uruchom ponownie Terminal po instalacji!

### 🐧 Linux

**One-liner Bash (zalecana)**

Otwórz Terminal i uruchom:

```bash
curl -fsSL https://raw.githubusercontent.com/gacabartosz/presidio-local-anonymizer/main/scripts/install.sh | bash
```

**Co zostanie zainstalowane:**
- ✅ Python 3.11, Git, Tesseract OCR (przez apt-get/dnf)
- ✅ Repozytorium + środowisko wirtualne Python
- ✅ Wszystkie zależności
- ✅ Modele językowe (SpaCy + Tesseract polski)
- ✅ Narzędzie w PATH

**Lokalizacja:** `~/.presidio-anonymizer`
**Czas instalacji:** ~10-15 minut

## Użycie

### 1. GUI (interfejs graficzny) 🎨

Uruchom graficzny interfejs:

```bash
# Windows
anonymize-gui.cmd

# macOS / Linux
anonymize-gui
```

**Funkcje GUI:**
- 📁 Wybór wielu plików lub całego folderu
- 📊 Pasek postępu
- 📝 Logi w czasie rzeczywistym
- ✅ Proste w obsłudze (drag & drop - jeśli zainstalowano tkinterdnd2)

### 2. Menu kontekstowe (najłatwiejsze)

**Windows:**
1. Kliknij prawym przyciskiem myszy na pliku (`.docx`, `.odt`, `.pdf`, `.png`, `.jpg`)
2. Wybierz **"Anonimizuj (Presidio)"**
3. Poczekaj na zakończenie
4. Znajdź zanonimizowany plik w tym samym folderze (np. `.anon.pdf`)

**macOS:**
1. Kliknij prawym przyciskiem (lub Control+klik) na pliku
2. Wybierz **Quick Actions → Anonimizuj (Presidio)**
3. Znajdź zanonimizowany plik w tym samym folderze

**Linux:**
- Integracja z menedżerem plików zależy od dystrybucji
- Użyj GUI lub CLI zamiast

### 3. Wiersz poleceń

**Windows (CMD / PowerShell):**

```bash
# Pojedynczy plik
anonymize.cmd dokument.docx
anonymize.cmd raport.pdf
anonymize.cmd skan.png

# Folder (wszystkie DOCX, ODT, PDF i obrazy)
anonymize.cmd C:\Moje_Dokumenty\

# Z raportem zbiorczym
anonymize.cmd C:\Moje_Dokumenty\ --report raport.jsonl

# Verbose mode (szczegółowe logi)
anonymize.cmd dokument.docx --verbose
```

**macOS / Linux (Terminal):**

```bash
# Pojedynczy plik
anonymize dokument.docx
anonymize raport.pdf
anonymize skan.png

# Folder (wszystkie DOCX, ODT, PDF i obrazy)
anonymize ~/Documents/Moje_Dokumenty/

# Z raportem zbiorczym
anonymize ~/Documents/Moje_Dokumenty/ --report raport.jsonl

# Verbose mode (szczegółowe logi)
anonymize dokument.docx --verbose
```

### 4. Przykład użycia

**Przed anonimizacją** (`dokument.docx`):
```
Dane kontaktowe:
Imię: Jan Kowalski
Email: jan.kowalski@example.com
Telefon: +48 123 456 789
PESEL: 92010212345
NIP: 123-456-78-90
```

**Po anonimizacji** (`dokument.anon.docx`):
```
Dane kontaktowe:
Imię: [OSOBA]
Email: [EMAIL]
Telefon: [TELEFON]
PESEL: [PESEL]
NIP: [NIP]
```

## Raporty i logi

### Raport JSON

Dla każdego przetworzonego pliku generowany jest raport w formacie JSON:

```json
{
  "source_file": "dokument.docx",
  "output_file": "dokument.anon.docx",
  "status": "success",
  "timestamp": "2024-12-10T14:30:00",
  "format": "DOCX",
  "analysis": {
    "total_detections": 14,
    "entities": {
      "PERSON": {"count": 3, "mask": "[OSOBA]", "avg_score": 0.85},
      "EMAIL_ADDRESS": {"count": 2, "mask": "[EMAIL]", "avg_score": 1.0},
      "PL_PESEL": {"count": 2, "mask": "[PESEL]", "avg_score": 0.6}
    },
    "threshold_used": 0.35
  }
}
```

### Lokalizacja logów

Logi zapisywane są w: `%LOCALAPPDATA%\PresidioAnon\app\presidio_anonymizer.log`

**⚠️ WAŻNE:** Logi **nie zawierają** wartości PII - tylko typy wykrytych encji i statystyki.

## Konfiguracja

Pliki konfiguracyjne znajdują się w: `%LOCALAPPDATA%\PresidioAnon\app\config\`

### Dostosowanie masek (`config/entities.yaml`)

Możesz zmienić sposób maskowania danych:

```yaml
entities:
  PERSON:
    mask: "[OSOBA]"           # Zmień na "[REDACTED]" lub "***"
    description: "Imię i nazwisko osoby"

  PL_PESEL:
    mask: "[PESEL]"
    description: "Polski numer PESEL"
    patterns:
      - name: "PESEL_PATTERN"
        regex: '\b\d{11}\b'
        score: 0.6              # Wyższy score = mniejsza czułość
```

### Dodanie własnej encji

```yaml
  MY_CUSTOM_ID:
    mask: "[CUSTOM_ID]"
    description: "Mój niestandardowy identyfikator"
    patterns:
      - name: "CUSTOM_ID_PATTERN"
        regex: '\bCUST-\d{6}\b'
        score: 0.8
```

### Dostosowanie progu detekcji

```yaml
threshold: 0.35  # Niższy = więcej wykryć (więcej false positives)
                 # Wyższy = mniej wykryć (mniej false positives)
```

## Znane ograniczenia (MVP v0.1.0)

⚠️ **Formatowanie dokumentów:**
- DOCX: Podstawowe style mogą się uprościć (runs są łączone)
- ODT: Struktura dokumentu jest linearyzowana - złożone formatowanie nie jest zachowane

⚠️ **Wydajność:**
- Przetwarzanie sekwencyjne (nie równoległe)
- Duże dokumenty (>100 stron) mogą być przetwarzane wolniej

⚠️ **Wykrywanie:**
- Model NLP może mieć trudności z nietypowymi imionami/nazwiskami
- Możliwe false positives dla krótkich słów (np. "Pan", "Jan" w kontekście nazw miesięcy)

## Deinstalacja

### Windows

Uruchom PowerShell i wykonaj:

```powershell
& "$env:LOCALAPPDATA\PresidioAnon\app\scripts\uninstall.ps1"
```

Skrypt usunie:
- Wszystkie pliki aplikacji
- Wpisy w menu kontekstowym Windows
- Wpis w PATH użytkownika

### macOS / Linux

Uruchom Terminal i wykonaj:

```bash
# macOS
bash ~/Library/Application\ Support/PresidioAnon/app/scripts/uninstall.sh

# Linux
bash ~/.presidio-anonymizer/app/scripts/uninstall.sh
```

Skrypt usunie:
- Wszystkie pliki aplikacji
- Wpisy w PATH (.zshrc, .bashrc)
- Usługę Automator (tylko macOS)

## Roadmap

### v0.2.1 (ZREALIZOWANE) ✅
- [x] Obsługa dokumentów PDF (text layer) ✅
- [x] Obsługa OCR dla skanów PDF i obrazów (Tesseract) ✅
- [x] Obsługa formatów obrazów (PNG, JPG, TIFF) ✅
- [x] GUI (interfejs graficzny - tkinter) ✅
- [x] Wsparcie dla macOS (Homebrew, Automator) ✅
- [x] Wsparcie dla Linux (apt-get/dnf) ✅
- [x] One-liner instalacja dla wszystkich platform ✅

### v0.3.0 (w planowaniu)
- [ ] Zachowanie formatowania DOCX (runs, styles)
- [ ] Lepsza obsługa ODT (zachowanie struktury)
- [ ] Przetwarzanie równoległe (wielowątkowość)
- [ ] Podgląd przed/po w GUI
- [ ] Tryb "pseudonimizacji" (zamiana na fałszywe dane zamiast masek)
- [ ] Export do CSV/Excel
- [ ] Dashboard ze statystykami

### v1.0.0 (planowane)
- [ ] Wtyczka dla Microsoft Office
- [ ] API REST (opcjonalne)
- [ ] Profesjonalne GUI (PyQt)

## Licencja

Ten projekt jest dostępny na licencji [MIT](LICENSE).

Wykorzystuje bibliotekę [Microsoft Presidio](https://github.com/microsoft/presidio), która również jest dostępna na licencji MIT.

## Wsparcie i kontakt

- 🐛 **Zgłaszanie błędów:** [GitHub Issues](https://github.com/gacabartosz/presidio-local-anonymizer/issues)
- 💬 **Dyskusje:** [GitHub Discussions](https://github.com/gacabartosz/presidio-local-anonymizer/discussions)
- 📧 **Email:** (dodaj swój email jeśli chcesz)

## Kontrybutorzy

Projekt jest otwarty na wkład społeczności! Zobacz [CONTRIBUTING.md](docs/CONTRIBUTING.md) aby dowiedzieć się jak możesz pomóc.

## Bezpieczeństwo i prywatność

✅ **100% offline** - żadne dane nie są wysyłane do zewnętrznych serwerów
✅ **Brak telemetrii** - aplikacja nie zbiera żadnych danych analitycznych
✅ **Open Source** - kod jest otwarty i może być zweryfikowany przez każdego
✅ **Logi bezpieczne** - logi nie zawierają wartości PII

⚠️ **Uwaga:** Narzędzie jest pomocne, ale nie jest w 100% niezawodne. Zawsze weryfikuj wyniki przed publikacją dokumentów.

---

**Wykonane z ❤️ dla społeczności open-source**

👨‍💻 Created by [bartoszgaca.pl](https://bartoszgaca.pl) & 🤖 [Claude Code](https://claude.com/claude-code)
