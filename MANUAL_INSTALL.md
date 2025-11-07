# 🛠️ Instalacja Ręczna Krok Po Kroku - macOS

Jeśli automatyczna instalacja nie działa, użyj tej instrukcji.

---

## 🎯 Dla Kogo

Ta instrukcja jest dla ciebie jeśli:
- ❌ Automatyczna instalacja się nie powiodła
- ❌ Widzisz błąd `command not found: anonymize-gui`
- ❌ Instalacja zatrzymuje się bez komunikatu
- ✅ Wolisz widzieć każdy krok instalacji

---

## ⏱️ Czas: ~20-30 minut

---

## 📋 KROK 1: Zainstaluj Homebrew (jeśli nie masz)

Otwórz **Terminal** (Command + Spacja, wpisz "Terminal", Enter).

Wklej tę komendę:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Co się stanie:**
- Zapyta o hasło - WPISZ hasło (nie będzie widoczne, to normalne!)
- Instalacja może potrwać 5-10 minut
- Zobaczysz komunikat "Installation successful!"

**Po instalacji wykonaj:**

```bash
eval "$(/opt/homebrew/bin/brew shellenv)"
```

**Sprawdź czy działa:**

```bash
brew --version
```

Powinieneś zobaczyć: `Homebrew 4.x.x`

✅ **Homebrew zainstalowane!**

---

## 📋 KROK 2: Zainstaluj Python 3.11

Wklej w Terminal:

```bash
brew install python@3.11
```

**Co się stanie:**
- Instalacja 3-5 minut
- Zobaczysz "🍺 python@3.11 was successfully installed!"

**Dodaj Python 3.11 do PATH:**

```bash
echo 'export PATH="/opt/homebrew/opt/python@3.11/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Sprawdź czy działa:**

```bash
python3.11 --version
```

Powinieneś zobaczyć: `Python 3.11.x`

✅ **Python 3.11 zainstalowany!**

---

## 📋 KROK 3: Zainstaluj Git

Wklej w Terminal:

```bash
brew install git
```

**Sprawdź czy działa:**

```bash
git --version
```

Powinieneś zobaczyć: `git version 2.x.x`

✅ **Git zainstalowany!**

---

## 📋 KROK 4: Zainstaluj Tesseract OCR

Wklej w Terminal:

```bash
brew install tesseract tesseract-lang
```

**Co się stanie:**
- To najdłuższa część - może potrwać 10-15 minut!
- Instaluje wiele zależności graficznych
- Nie przerywaj, poczekaj cierpliwie ☕

**Sprawdź czy działa:**

```bash
tesseract --version
```

Powinieneś zobaczyć: `tesseract 5.x.x`

**Sprawdź polski model:**

```bash
tesseract --list-langs | grep pol
```

Powinieneś zobaczyć: `pol`

✅ **Tesseract OCR zainstalowany!**

---

## 📋 KROK 5: Utwórz folder instalacji

Wklej w Terminal:

```bash
mkdir -p ~/Library/Application\ Support/PresidioAnon/bin
cd ~/Library/Application\ Support/PresidioAnon
```

**Sprawdź gdzie jesteś:**

```bash
pwd
```

Powinieneś zobaczyć: `/Users/TWOJE_IMIE/Library/Application Support/PresidioAnon`

✅ **Folder utworzony!**

---

## 📋 KROK 6: Pobierz kod aplikacji

Wklej w Terminal:

```bash
git clone https://github.com/gacabartosz/presidio-local-anonymizer.git app
cd app
```

**Sprawdź czy się sklonowało:**

```bash
ls -la
```

Powinieneś zobaczyć foldery: `app`, `config`, `scripts`, `processors`, itd.

✅ **Kod pobrany!**

---

## 📋 KROK 7: Utwórz środowisko Python

Wklej w Terminal:

```bash
python3.11 -m venv .venv
```

**Aktywuj środowisko:**

```bash
source .venv/bin/activate
```

**Powinieneś zobaczyć** `(.venv)` na początku linii:

```
(.venv) gaca@MacBook-Pro app %
```

**Zaktualizuj pip:**

```bash
pip install --upgrade pip
```

✅ **Środowisko Python utworzone!**

---

## 📋 KROK 8: Zainstaluj zależności Python

**⚠️ WAŻNE:** Upewnij się że środowisko jest aktywne (widzisz `(.venv)`)

Wklej w Terminal:

```bash
pip install -r requirements.txt
```

**Co się stanie:**
- Instalacja 5-8 minut
- Zobaczysz wiele komunikatów "Successfully installed..."
- Zainstaluje ~20 bibliotek Python

**Poczekaj aż zobaczysz:**
```
Successfully installed presidio-analyzer-2.2.354 presidio-anonymizer-2.2.354 ...
```

✅ **Zależności zainstalowane!**

---

## 📋 KROK 9: Pobierz model językowy polski

Wklej w Terminal:

```bash
python -m spacy download pl_core_news_md
```

**Co się stanie:**
- Pobieranie ~50 MB
- Instalacja modelu AI dla języka polskiego
- Zobaczysz "✔ Download and installation successful"

✅ **Model językowy pobrany!**

---

## 📋 KROK 10: Utwórz skrypty uruchamiające

Wklej w Terminal **cały blok naraz:**

```bash
cd ~/Library/Application\ Support/PresidioAnon/bin

cat > anonymize << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(dirname "$SCRIPT_DIR")/app"
PYTHON_EXE="$APP_DIR/.venv/bin/python"
MAIN_SCRIPT="$APP_DIR/app/main.py"

"$PYTHON_EXE" "$MAIN_SCRIPT" "$@"
EOF

chmod +x anonymize

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

**Sprawdź czy się utworzyły:**

```bash
ls -la
```

Powinieneś zobaczyć:
```
-rwxr-xr-x  anonymize
-rwxr-xr-x  anonymize-gui
```

✅ **Skrypty utworzone!**

---

## 📋 KROK 11: Dodaj do PATH

Wklej w Terminal:

```bash
echo 'export PATH="$HOME/Library/Application Support/PresidioAnon/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Sprawdź PATH:**

```bash
echo $PATH | grep PresidioAnon
```

Powinieneś zobaczyć ścieżkę z "PresidioAnon/bin"

✅ **PATH zaktualizowany!**

---

## 📋 KROK 12: SPRAWDŹ CZY DZIAŁA!

**Test 1: Sprawdź pomoc CLI**

```bash
anonymize --help
```

Powinieneś zobaczyć:
```
usage: main.py [-h] [--verbose] ...
```

**Test 2: Uruchom GUI**

```bash
anonymize-gui
```

Powinno otworzyć się okno z interfejsem graficznym!

**Test 3: Przetestuj na pliku**

Utwórz testowy plik:

```bash
echo "Jan Kowalski, email: jan@example.com, PESEL: 92010212345" > ~/Desktop/test.txt
anonymize ~/Desktop/test.txt
```

Sprawdź plik `test.anon.txt` - dane powinny być ukryte!

---

## 🎉 GRATULACJE!

### ✅ Instalacja zakończona pomyślnie!

**Możesz teraz używać:**

1. **GUI** - najłatwiejsze:
   ```bash
   anonymize-gui
   ```

2. **CLI** - z terminala:
   ```bash
   anonymize plik.docx
   anonymize folder/
   ```

3. **Quick Actions** (opcjonalne) - prawy przycisk w Finder

---

## 🆘 Coś nie działa?

### ❌ `command not found: anonymize`

**Rozwiązanie:**
```bash
# Zrestartuj terminal
# LUB wykonaj:
source ~/.zshrc
```

### ❌ `ModuleNotFoundError: No module named ...`

**Rozwiązanie:**
```bash
cd ~/Library/Application\ Support/PresidioAnon/app
source .venv/bin/activate
pip install -r requirements.txt
```

### ❌ GUI nie otwiera się

**Rozwiązanie:**
```bash
brew install python-tk@3.11
```

### ❌ Inny problem?

Zobacz [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 🗑️ Jak odinstalować?

```bash
rm -rf ~/Library/Application\ Support/PresidioAnon
nano ~/.zshrc  # Usuń linię z PresidioAnon
```

---

👨‍💻 Created by [bartoszgaca.pl](https://bartoszgaca.pl) & 🤖 [Claude Code](https://claude.com/claude-code)
