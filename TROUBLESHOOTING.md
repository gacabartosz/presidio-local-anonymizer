# 🔧 Troubleshooting - Presidio Local Anonymizer

Przewodnik rozwiązywania problemów z instalacją i użytkowaniem.

---

## 📋 Spis treści

1. [Problemy z instalacją](#problemy-z-instalacją)
2. [Diagnoza problemu](#diagnoza-problemu)
3. [Instalacja ręczna (macOS)](#instalacja-ręczna-macos)
4. [Instalacja ręczna (Linux)](#instalacja-ręczna-linux)
5. [Problemy z uruchomieniem](#problemy-z-uruchomieniem)
6. [FAQ - Najczęstsze błędy](#faq---najczęstsze-błędy)

---

## Problemy z instalacją

### ❌ Problem: `command not found: anonymize-gui` (macOS)

**Przyczyna:** Instalacja nie dokończyła się lub PATH nie został zaktualizowany.

**Rozwiązanie:**

#### Krok 1: Sprawdź czy instalacja się powiodła

```bash
ls -la ~/Library/Application\ Support/PresidioAnon
```

**Jeśli folder NIE ISTNIEJE** - instalacja się nie powiodła. Przejdź do [Instalacji ręcznej](#instalacja-ręczna-macos).

**Jeśli folder ISTNIEJE** - sprawdź PATH:

```bash
echo $PATH | grep PresidioAnon
```

Jeśli nie widać `PresidioAnon/bin`, dodaj do PATH:

```bash
# Dla zsh (domyślny na macOS):
echo 'export PATH="$HOME/Library/Application Support/PresidioAnon/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Dla bash:
echo 'export PATH="$HOME/Library/Application Support/PresidioAnon/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### Krok 2: Sprawdź Python

```bash
python3 --version
```

**Wymagane:** Python 3.11 lub nowszy

**Jeśli masz Python 3.9.x:**

```bash
brew install python@3.11
export PATH="/opt/homebrew/opt/python@3.11/bin:$PATH"
```

---

### ⚠️ Problem: Instalacja zatrzymuje się na Tesseract

**Przyczyna:** Homebrew instaluje wiele zależności, może to zająć długo.

**Rozwiązanie:** Poczekaj cierpliwie (~10-15 minut). Jeśli instalacja się zawiesza ponad 30 minut, przerwij (Ctrl+C) i spróbuj ponownie.

---

### 🐍 Problem: Python 3.9.6 zamiast 3.11+

**Przyczyna:** macOS ma starą wersję Python domyślnie.

**Rozwiązanie:**

```bash
# Zainstaluj Python 3.11
brew install python@3.11

# Sprawdź czy zainstalowało się
python3.11 --version

# Dodaj do PATH (zsh)
echo 'export PATH="/opt/homebrew/opt/python@3.11/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Lub utwórz alias
echo 'alias python3=python3.11' >> ~/.zshrc
source ~/.zshrc
```

---

## Diagnoza problemu

### 🔍 Skrypt diagnostyczny

Uruchom ten skrypt aby zdiagnozować problem:

```bash
#!/bin/bash

echo "=== DIAGNOZA PRESIDIO ANONYMIZER ==="
echo ""

echo "1. Sprawdzanie Python:"
if command -v python3 &> /dev/null; then
    python3 --version
    python3 -c 'import sys; print(f"  Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")'
else
    echo "  ❌ Python nie znaleziony"
fi

echo ""
echo "2. Sprawdzanie Python 3.11:"
if command -v python3.11 &> /dev/null; then
    python3.11 --version
else
    echo "  ❌ Python 3.11 nie znaleziony"
fi

echo ""
echo "3. Sprawdzanie Git:"
if command -v git &> /dev/null; then
    git --version
else
    echo "  ❌ Git nie znaleziony"
fi

echo ""
echo "4. Sprawdzanie Tesseract:"
if command -v tesseract &> /dev/null; then
    tesseract --version | head -n1
else
    echo "  ❌ Tesseract nie znaleziony"
fi

echo ""
echo "5. Sprawdzanie folderu instalacji:"
if [[ -d "$HOME/Library/Application Support/PresidioAnon" ]]; then
    echo "  ✅ Folder istnieje"
    ls -la "$HOME/Library/Application Support/PresidioAnon"
else
    echo "  ❌ Folder nie istnieje - instalacja nie powiodła się"
fi

echo ""
echo "6. Sprawdzanie PATH:"
echo $PATH | grep -q "PresidioAnon" && echo "  ✅ PATH zawiera PresidioAnon" || echo "  ❌ PATH nie zawiera PresidioAnon"

echo ""
echo "7. Sprawdzanie komend:"
command -v anonymize &> /dev/null && echo "  ✅ anonymize dostępne" || echo "  ❌ anonymize niedostępne"
command -v anonymize-gui &> /dev/null && echo "  ✅ anonymize-gui dostępne" || echo "  ❌ anonymize-gui niedostępne"

echo ""
echo "=== KONIEC DIAGNOZY ==="
```

Zapisz jako `diagnoza.sh`, nadaj uprawnienia i uruchom:

```bash
chmod +x diagnoza.sh
./diagnoza.sh
```

---

## Instalacja ręczna (macOS)

Jeśli automatyczna instalacja nie działa, zainstaluj ręcznie:

### Krok 1: Zainstaluj zależności systemowe

```bash
# Homebrew (jeśli nie masz)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python 3.11
brew install python@3.11

# Git
brew install git

# Tesseract OCR
brew install tesseract tesseract-lang
```

### Krok 2: Utwórz folder instalacji

```bash
mkdir -p ~/Library/Application\ Support/PresidioAnon/bin
cd ~/Library/Application\ Support/PresidioAnon
```

### Krok 3: Sklonuj repozytorium

```bash
git clone https://github.com/gacabartosz/presidio-local-anonymizer.git app
cd app
```

### Krok 4: Utwórz środowisko wirtualne Python

```bash
# Użyj Python 3.11
python3.11 -m venv .venv

# Aktywuj środowisko
source .venv/bin/activate

# Aktualizuj pip
pip install --upgrade pip
```

### Krok 5: Zainstaluj zależności Python

```bash
pip install -r requirements.txt
```

### Krok 6: Pobierz model językowy SpaCy

```bash
python -m spacy download pl_core_news_md
```

### Krok 7: Utwórz skrypty wrapper

```bash
cd ~/Library/Application\ Support/PresidioAnon/bin

# Skrypt 'anonymize'
cat > anonymize << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(dirname "$SCRIPT_DIR")/app"
PYTHON_EXE="$APP_DIR/.venv/bin/python"
MAIN_SCRIPT="$APP_DIR/app/main.py"

"$PYTHON_EXE" "$MAIN_SCRIPT" "$@"
EOF

chmod +x anonymize

# Skrypt 'anonymize-gui'
cat > anonymize-gui << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(dirname "$SCRIPT_DIR")/app"
PYTHON_EXE="$APP_DIR/.venv/bin/python"
GUI_SCRIPT="$APP_DIR/app/gui.py"

"$PYTHON_EXE" "$GUI_SCRIPT"
EOF

chmod +x anonymize-gui
```

### Krok 8: Dodaj do PATH

```bash
# Dla zsh (domyślny shell na macOS)
echo 'export PATH="$HOME/Library/Application Support/PresidioAnon/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Dla bash
echo 'export PATH="$HOME/Library/Application Support/PresidioAnon/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Krok 9: Sprawdź instalację

```bash
anonymize --help
anonymize-gui
```

---

## Instalacja ręczna (Linux)

### Krok 1: Zainstaluj zależności systemowe

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-venv git tesseract-ocr tesseract-ocr-pol

# Fedora
sudo dnf install -y python3.11 git tesseract tesseract-langpack-pol
```

### Krok 2-9: Analogicznie jak macOS

Zmień tylko ścieżkę instalacji:
- macOS: `~/Library/Application Support/PresidioAnon`
- Linux: `~/.presidio-anonymizer`

---

## Problemy z uruchomieniem

### ❌ `ModuleNotFoundError: No module named 'presidio_analyzer'`

**Przyczyna:** Zależności nie zostały zainstalowane w środowisku wirtualnym.

**Rozwiązanie:**

```bash
cd ~/Library/Application\ Support/PresidioAnon/app
source .venv/bin/activate
pip install -r requirements.txt
```

---

### ❌ `Language 'pl' not found`

**Przyczyna:** Model językowy SpaCy nie został pobrany.

**Rozwiązanie:**

```bash
cd ~/Library/Application\ Support/PresidioAnon/app
source .venv/bin/activate
python -m spacy download pl_core_news_md
```

---

### ⚠️ GUI nie otwiera się

**Przyczyna:** Brak biblioteki tkinter.

**Rozwiązanie:**

```bash
# macOS
brew install python-tk@3.11

# Linux
sudo apt-get install python3-tk
```

---

### ❌ OCR nie działa dla skanów

**Przyczyna:** Tesseract OCR nie jest zainstalowany lub brak polskiego modelu.

**Rozwiązanie:**

```bash
# macOS
brew install tesseract tesseract-lang

# Sprawdź czy polski model istnieje
tesseract --list-langs | grep pol
```

---

## FAQ - Najczęstsze błędy

### Q: Instalacja zatrzymuje się i nic się nie dzieje

**A:** To normalne - Homebrew może pobierać setki megabajtów. Poczekaj do 30 minut. Możesz sprawdzić postęp w Activity Monitor.

### Q: `permission denied` podczas instalacji

**A:** Nie używaj `sudo` z instalatorem. Instalacja odbywa się w katalogu użytkownika i nie wymaga sudo. Jeśli Homebrew prosi o hasło - to normalne, podaj hasło.

### Q: Po instalacji terminal nie widzi komend

**A:** Zrestartuj terminal lub wykonaj:
```bash
source ~/.zshrc  # lub ~/.bashrc
```

### Q: Czy mogę używać Python 3.9 zamiast 3.11?

**A:** Nie zalecane. Niektóre zależności wymagają Python 3.11+. Zainstaluj Python 3.11:
```bash
brew install python@3.11
```

### Q: Jak całkowicie odinstalować i zainstalować od nowa?

**A:**
```bash
# Usuń folder instalacji
rm -rf ~/Library/Application\ Support/PresidioAnon

# Usuń wpis z PATH (edytuj ręcznie)
nano ~/.zshrc  # usuń linię z PresidioAnon

# Zainstaluj ponownie
curl -fsSL https://raw.githubusercontent.com/gacabartosz/presidio-local-anonymizer/main/scripts/install.sh | bash
```

---

## 📞 Nadal masz problem?

1. **Uruchom diagnozę** (skrypt powyżej)
2. **Sprawdź logi** w folderze instalacji
3. **Zgłoś issue na GitHub:**
   https://github.com/gacabartosz/presidio-local-anonymizer/issues

Dołącz wynik diagnozy i dokładny opis błędu.

---

👨‍💻 Created by [bartoszgaca.pl](https://bartoszgaca.pl) & 🤖 [Claude Code](https://claude.com/claude-code)
