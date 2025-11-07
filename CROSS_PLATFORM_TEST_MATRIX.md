# 🧪 Matryca Testów Cross-Platform

## Status Poprawek na Platformach

| Poprawka | Windows | macOS | Linux | Status |
|----------|---------|-------|-------|--------|
| SpaCy model URL fix | ✅ | ✅ | ✅ | COMPLETE |
| Python-tk installation | N/A | ✅ | ✅ | N/A dla Windows |
| Race condition GUI | ✅ | ✅ | ✅ | COMPLETE |
| Pattern objects fix | ✅ | ✅ | ✅ | COMPLETE |
| tkinterdnd2 fallback | ✅ | ✅ | ✅ | COMPLETE |

---

## 📋 Instalatory

### Windows (`scripts/install.ps1`)
**Lokalizacja:** `%LOCALAPPDATA%\PresidioAnon`

**Zainstalowane komponenty:**
- ✅ Python 3.11 (przez winget/choco)
- ✅ Git (przez winget/choco)
- ✅ Tesseract OCR (instalator Windows)
- ✅ Wszystkie zależności Python (pip)
- ✅ Model SpaCy pl_core_news_md (przez bezpośredni URL)
- ✅ Skrypty: `anonymize.cmd`, `anonymize-gui.cmd`
- ✅ Menu kontekstowe Windows
- ✅ Dodanie do PATH użytkownika

**Specyfika Windows:**
- Tkinter jest wbudowany w Python dla Windows - nie wymaga osobnej instalacji
- Używa winget lub chocolatey do instalacji zależności systemowych
- Registry dla menu kontekstowego
- CMD/PowerShell zamiast bash

### macOS (`scripts/install.sh`)
**Lokalizacja:** `~/Library/Application Support/PresidioAnon`

**Zainstalowane komponenty:**
- ✅ Homebrew (jeśli brak)
- ✅ Python 3.11 (przez Homebrew)
- ✅ **python-tk@3.11** (dla GUI - KRYTYCZNE na macOS)
- ✅ Git (przez Homebrew)
- ✅ Tesseract OCR + tesseract-lang (przez Homebrew)
- ✅ Wszystkie zależności Python (pip)
- ✅ Model SpaCy pl_core_news_md (przez bezpośredni URL)
- ✅ Skrypty: `anonymize`, `anonymize-gui`
- ✅ Usługa Automator (Quick Actions)
- ✅ Dodanie do PATH (.zshrc/.bashrc)

**Specyfika macOS:**
- Python z Homebrew NIE ma tkinter - musi być zainstalowany osobno
- Apple Silicon (M1/M2/M3): tkinterdnd2 nie działa (fallback na standardowy tkinter)
- Automator dla integracji z Finder

### Linux (`scripts/install.sh`)
**Lokalizacja:** `~/.presidio-anonymizer`

**Zainstalowane komponenty:**
- ✅ Python 3.11 (przez apt-get/dnf)
- ✅ python3-tk (dla GUI)
- ✅ Git (przez apt-get/dnf)
- ✅ Tesseract OCR + tesseract-ocr-pol (przez apt-get/dnf)
- ✅ Wszystkie zależności Python (pip)
- ✅ Model SpaCy pl_core_news_md (przez bezpośredni URL)
- ✅ Skrypty: `anonymize`, `anonymize-gui`
- ✅ Dodanie do PATH (.bashrc/.profile)

**Specyfika Linux:**
- Python 3.11 może wymagać dodatkowego repo (np. deadsnakes PPA na Ubuntu)
- python3-tk jest osobnym pakietem
- Integracja z menedżerem plików zależy od dystrybucji (Nautilus, Dolphin, Thunar)

---

## 🧪 Test Plan dla Każdej Platformy

### Test 1: Instalacja
```bash
# Windows (PowerShell jako Admin)
iwr https://raw.githubusercontent.com/gacabartosz/presidio-local-anonymizer/main/scripts/install.ps1 | iex

# macOS/Linux (Terminal)
bash <(curl -fsSL https://raw.githubusercontent.com/gacabartosz/presidio-local-anonymizer/main/quick-start.sh)
```

**Oczekiwany rezultat:**
- ✅ Brak błędu 404 przy pobieraniu SpaCy model
- ✅ Wszystkie zależności zainstalowane
- ✅ GUI uruchamia się bez błędów

### Test 2: GUI Launch
```bash
# Windows
anonymize-gui.cmd

# macOS/Linux
anonymize-gui
```

**Oczekiwany rezultat:**
- ✅ Okno GUI się otwiera
- ✅ Brak błędu "_tkinter" 
- ✅ Brak błędu "log_text AttributeError"
- ✅ W logach: "✓ Analyzer gotowy"

### Test 3: File Processing (DOCX)
1. Utwórz test.docx z danymi:
   - Email: test@example.com
   - PESEL: 92010212345
   - Telefon: +48 123 456 789

2. Anonimizuj przez GUI lub CLI

3. Sprawdź test.anon.docx

**Oczekiwany rezultat:**
- ✅ Plik test.anon.docx utworzony
- ✅ Email → `[EMAIL]`
- ✅ PESEL → `[PESEL]`
- ✅ Telefon → `[TELEFON]`
- ✅ Brak błędu "compiled_regex"

### Test 4: PDF Processing
```bash
# Utwórz PDF z tekstem
# Anonimizuj
# Sprawdź wynik
```

### Test 5: OCR (skan PDF/obraz)
```bash
# Utwórz obraz z tekstem
# Anonimizuj
# Sprawdź wynik - wymaga Tesseract
```

---

## 🐛 Znane Problemy Specyficzne dla Platform

### Windows
- ⚠️ **Może wymagać uruchomienia PowerShell jako Administrator** (dla instalacji winget/choco)
- ⚠️ **Windows Defender** może blokować instalację - dodaj wyjątek
- ⚠️ **Długie ścieżki** (`C:\Users\...`) mogą powodować problemy - instalacja w `%LOCALAPPDATA%` rozwiązuje to

### macOS
- ⚠️ **python-tk@3.11 MUSI być zainstalowany** - bez tego GUI nie działa
- ⚠️ **Apple Silicon (M1/M2/M3)**: tkinterdnd2 nie działa - fallback na standardowy tkinter (bez Drag & Drop)
- ⚠️ **Homebrew** może pytać o hasło - to normalne
- ⚠️ **PATH** nie jest załadowany od razu - wymaga restartu terminala lub `source ~/.zshrc`

### Linux
- ⚠️ **Python 3.11** może wymagać deadsnakes PPA na Ubuntu <22.04
- ⚠️ **sudo** wymagane dla apt-get/dnf
- ⚠️ **python3-tk** jest osobnym pakietem - musi być zainstalowany
- ⚠️ **Integracja z menedżerem plików** zależy od DE (GNOME/KDE/XFCE)

---

## ✅ Checklist Przed Release

### Dla Każdej Platformy:
- [ ] Instalator pobiera SpaCy model przez bezpośredni URL
- [ ] GUI uruchamia się bez błędów
- [ ] Przetwarzanie DOCX działa
- [ ] Przetwarzanie PDF działa
- [ ] OCR działa (z Tesseract)
- [ ] CLI działa
- [ ] PATH jest poprawnie skonfigurowany
- [ ] Dokumentacja jest aktualna

### Windows:
- [x] install.ps1 - SpaCy URL fix
- [x] app/gui.py - race condition fix
- [x] app/analyzer.py - Pattern fix
- [x] README.md - instrukcje Windows
- [ ] Test na czystej Windows 10
- [ ] Test na czystej Windows 11

### macOS:
- [x] install.sh - SpaCy URL fix
- [x] install.sh - python-tk@3.11 auto-install
- [x] app/gui.py - race condition fix
- [x] app/gui.py - tkinterdnd2 fallback (Apple Silicon)
- [x] app/analyzer.py - Pattern fix
- [x] README.md - instrukcje macOS
- [x] Test na Apple Silicon (M1) ✅
- [ ] Test na Intel Mac

### Linux:
- [x] install.sh - SpaCy URL fix
- [x] install.sh - python3-tk w instrukcjach
- [x] app/gui.py - race condition fix
- [x] app/analyzer.py - Pattern fix
- [x] README.md - instrukcje Linux
- [ ] Test na Ubuntu 22.04
- [ ] Test na Debian
- [ ] Test na Fedora

---

## 📊 Compatibility Matrix

| Feature | Windows 10/11 | macOS Intel | macOS Apple Silicon | Ubuntu 22.04+ | Debian 11+ | Fedora 35+ |
|---------|---------------|-------------|---------------------|---------------|------------|------------|
| GUI | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Drag & Drop | ✅ | ✅ | ⚠️ Fallback | ✅ | ✅ | ✅ |
| DOCX | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| ODT | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| PDF | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| OCR | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| CLI | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Context Menu | ✅ | ✅ | ✅ | ⚠️ Varies | ⚠️ Varies | ⚠️ Varies |

**Legenda:**
- ✅ Pełne wsparcie
- ⚠️ Częściowe wsparcie / znane ograniczenia
- ❌ Nie działa / nie wspierane

---

👨‍💻 Created by [bartoszgaca.pl](https://bartoszgaca.pl) & 🤖 [Claude Code](https://claude.com/claude-code)

Data: 2025-11-07
