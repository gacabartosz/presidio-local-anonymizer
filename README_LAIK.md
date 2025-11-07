<div align="center">
  <img src="assets/logo.svg" alt="Presidio Local Anonymizer" width="200"/>
</div>

<br/>

# 🔒 PRESIDIO - Ukryj Dane Osobowe (INSTRUKCJA DLA LAIKA)

> ⚡ **CHCESZ OD RAZU URUCHOMIĆ?** Zobacz [PROSTY_START.md](PROSTY_START.md) - jedna komenda i gotowe!

## 💡 CO TO ROBI?

**Automatycznie ukrywa dane osobowe w dokumentach!**

Zmienia:
- `Jan Kowalski` → `[OSOBA]`
- `jan@email.com` → `[EMAIL]`
- `+48 123 456 789` → `[TELEFON]`
- `PESEL`, `NIP` → `[PESEL]`, `[NIP]`

---

# 🚀 INSTALACJA (1 KOMENDA)

## 🪟 WINDOWS (10 minut)

### KROK 1: Otwórz PowerShell **jako administrator**

1. Naciśnij klawisz **Windows** (na klawiaturze)
2. Wpisz: `powershell`
3. Kliknij **PRAWYM** na "Windows PowerShell"
4. Wybierz: **"Uruchom jako administrator"**
5. Zapyta "Czy zezwolić?" → kliknij **TAK**

### KROK 2: Wklej i uruchom

**SKOPIUJ I WKLEJ:**
```powershell
iwr https://raw.githubusercontent.com/gacabartosz/presidio-local-anonymizer/main/scripts/install.ps1 | iex
```

**JAK WKLEIĆ?**
- Kliknij **prawym** przyciskiem myszy w oknie PowerShell
- LUB naciśnij `Ctrl + V`
- Naciśnij `Enter`

### KROK 3: Poczekaj (10-15 minut)

⏳ Pobiera Python, Git, Tesseract OCR, modele AI...

✅ **GOTOWE!** Zobaczysz:
```
✓ INSTALACJA ZAKOŃCZONA POMYŚLNIE!
```

---

## 🍎 macOS (10 minut)

### KROK 1: Otwórz Terminal

1. Naciśnij `Command + Spacja`
2. Wpisz: `terminal`
3. Naciśnij `Enter`

### KROK 2: Wklej i uruchom

**SKOPIUJ I WKLEJ:**
```bash
curl -fsSL https://raw.githubusercontent.com/gacabartosz/presidio-local-anonymizer/main/scripts/install.sh | bash
```

**JAK WKLEIĆ?**
- Naciśnij `Command + V`
- Naciśnij `Enter`

### KROK 3: Poczekaj (10-15 minut)

⏳ Instaluje Homebrew (jeśli brak), Python, Git, Tesseract...

✅ **GOTOWE!** Zobaczysz:
```
✓ INSTALACJA ZAKOŃCZONA POMYŚLNIE!
```

**⚠️ WAŻNE:** Zamknij i otwórz ponownie Terminal!

### ❌ Instalacja nie działa?

Jeśli widzisz błąd lub instalacja się zatrzymuje:

1. **Zobacz troubleshooting:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. **Instalacja ręczna krok po kroku:** [MANUAL_INSTALL.md](MANUAL_INSTALL.md)

---

# 📝 JAK UŻYWAĆ?

## 🎨 SPOSÓB 1: GUI (interfejs graficzny) - NAJŁATWIEJSZY

### Windows:
```
1. Naciśnij Windows + R
2. Wpisz: anonymize-gui.cmd
3. Naciśnij Enter
```

### macOS:
```
1. Otwórz Terminal
2. Wpisz: anonymize-gui
3. Naciśnij Enter
```

**Co dalej?**
- Kliknij "📄 Wybierz pliki..."
- Wybierz dokumenty
- Kliknij "🚀 Anonimizuj"
- **GOTOWE!** Nowe pliki w tym samym folderze

---

## 🖱️ SPOSÓB 2: Menu kontekstowe (prawy przycisk)

### Windows:
1. Kliknij **PRAWYM** na dokumencie (.docx, .pdf, .png)
2. Wybierz: **"Anonimizuj (Presidio)"**
3. Poczekaj kilka sekund
4. **GOTOWE!** W tym samym folderze jest `plik.anon.docx`

### macOS:
1. Kliknij **PRAWYM** (lub Control+klik) na pliku
2. Wybierz: **Quick Actions → Anonimizuj (Presidio)**
3. **GOTOWE!**

---

## ⌨️ SPOSÓB 3: Wiersz poleceń (dla zaawansowanych)

### Windows (CMD):
```
anonymize.cmd "C:\Dokumenty\umowa.docx"
```

### macOS/Linux (Terminal):
```
anonymize ~/Documents/umowa.docx
```

---

# 📄 OBSŁUGIWANE FORMATY

| Format | Rozszerzenie | Potrzebuje OCR? |
|--------|--------------|-----------------|
| Word | .docx | ❌ Nie |
| LibreOffice | .odt | ❌ Nie |
| PDF (tekst) | .pdf | ❌ Nie |
| PDF (skan) | .pdf | ✅ Tak (auto) |
| Obraz | .png, .jpg, .tiff | ✅ Tak |

**OCR = wykrywanie tekstu na obrazach (automatyczne!)**

---

# ❓ NAJCZĘSTSZE PYTANIA

### ❓ Czy to bezpieczne?
✅ **TAK!** Wszystko działa **lokalnie** na Twoim komputerze.
❌ **Żadne dane nie są wysyłane przez internet!**

### ❓ Czy to kosztuje?
✅ **DARMOWE** - na zawsze!

### ❓ Czy zmienia oryginalny plik?
❌ **NIE!** Tworzy **KOPIĘ** z nazwą `oryginalny.anon.docx`
Oryginalny plik **pozostaje niezmieniony**!

### ❓ Co dostanę po przetworzeniu?
📄 **Zanonimizowany dokument:** `plik.anon.docx`
📊 **Raport JSON:** `plik.anon.json` (co wykryto)

### ❓ Ile to trwa?
- Mały dokument (1-5 stron): **~5 sekund**
- Duży dokument (50 stron): **~30 sekund**
- Skan PDF (OCR): **~10 sekund/strona**

### ❓ Czy działa bez internetu?
✅ **TAK!** Po instalacji działa **100% offline**

### ❓ Jak odinstalować?

**Windows:**
```powershell
& "$env:LOCALAPPDATA\PresidioAnon\app\scripts\uninstall.ps1"
```

**macOS:**
```bash
bash ~/Library/Application\ Support/PresidioAnon/app/scripts/uninstall.sh
```

---

# 🆘 POMOC - COŚ NIE DZIAŁA?

## Problem 1: "Instalacja nie działa"

**Windows:**
- Czy uruchomiłeś PowerShell **jako administrator**?
- Spróbuj ponownie

**macOS:**
- Czy zainstalowało się Homebrew? (zapyta o hasło - to normalne!)
- Zamknij i otwórz Terminal ponownie

## Problem 2: "Komenda 'anonymize' nie działa"

**Windows:**
- Uruchom ponownie CMD/PowerShell

**macOS:**
- Wykonaj: `source ~/.zshrc` (lub `~/.bashrc`)
- LUB zamknij i otwórz Terminal ponownie

## Problem 3: "Menu kontekstowe nie pojawia się"

**Windows:**
- Zamknij wszystkie okna Eksploratora (Windows + E)
- Otwórz ponownie

**macOS:**
- Przejdź do: System Preferences → Keyboard → Shortcuts → Services
- Znajdź "Anonimizuj (Presidio)" i zaznacz ✅

## Problem 4: "OCR nie działa dla skanów"

**Sprawdź czy Tesseract jest zainstalowany:**

Windows:
```powershell
tesseract --version
```

macOS:
```bash
tesseract --version
```

Jeśli nie - zainstaluj ręcznie:
- **Windows:** https://github.com/UB-Mannheim/tesseract/wiki
- **macOS:** `brew install tesseract tesseract-lang`

## Problem 5: Inny błąd

📧 **Zgłoś na GitHub:**
https://github.com/gacabartosz/presidio-local-anonymizer/issues

---

# 🎓 JAK TO DZIAŁA? (dla ciekawskich)

1. **Otwiera dokument** (Word, PDF, obraz)
2. **AI czyta tekst** (Microsoft Presidio + SpaCy)
3. **Szuka wzorców:**
   - Imiona i nazwiska
   - Adresy email
   - Numery telefonów
   - PESEL, NIP (polskie regex)
4. **Zamienia na maski:** `[OSOBA]`, `[EMAIL]` itd.
5. **Zapisuje nowy plik** z sufiksem `.anon.*`

**Wszystko lokalnie - bez chmury!**

---

# 📞 KONTAKT I WSPARCIE

- 🐛 **Błędy:** https://github.com/gacabartosz/presidio-local-anonymizer/issues
- 💬 **Pytania:** https://github.com/gacabartosz/presidio-local-anonymizer/discussions
- 📖 **Dokumentacja:** [README.md](README.md)

---

# 📜 LICENCJA

**MIT License** - możesz używać za darmo do celów:
- ✅ Prywatnych
- ✅ Komercyjnych
- ✅ Edukacyjnych

---

# 🎉 DODATKOWE FUNKCJE

## 🎨 GUI - Graficzny Interfejs

**Uruchom:**
- Windows: `anonymize-gui.cmd`
- macOS: `anonymize-gui`

**Funkcje:**
- 📁 Wybór wielu plików naraz
- 📊 Pasek postępu
- 📝 Logi na żywo
- ✅ Drag & Drop (przeciągnij pliki)

## 📊 Przykład Raportu JSON

```json
{
  "source_file": "umowa.docx",
  "output_file": "umowa.anon.docx",
  "status": "success",
  "analysis": {
    "total_detections": 12,
    "entities": {
      "PERSON": {"count": 3, "mask": "[OSOBA]"},
      "EMAIL_ADDRESS": {"count": 2, "mask": "[EMAIL]"},
      "PL_PESEL": {"count": 2, "mask": "[PESEL]"}
    }
  }
}
```

---

# ✅ CHECKLIST - Czy zadziała u mnie?

## Windows:
- [x] Windows 10 lub 11
- [x] Połączenie z internetem (tylko instalacja)
- [x] ~1 GB wolnego miejsca
- [x] Uprawnienia administratora (tylko instalacja)

## macOS:
- [x] macOS 10.15 (Catalina) lub nowszy
- [x] Połączenie z internetem (tylko instalacja)
- [x] ~1 GB wolnego miejsca
- [x] Xcode Command Line Tools (auto-instalowane)

## Linux:
- [x] Ubuntu 20.04+ / Debian 10+ / Fedora 30+
- [x] Python 3.11+
- [x] Git
- [x] Tesseract OCR

---

**Wykonane z ❤️ dla społeczności open-source**

👨‍💻 Created by [bartoszgaca.pl](https://bartoszgaca.pl) & 🤖 [Claude Code](https://claude.com/claude-code)
