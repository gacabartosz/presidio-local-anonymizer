#!/bin/bash
# Instalator Presidio Local Anonymizer dla macOS/Linux
# Użycie: curl -fsSL https://raw.githubusercontent.com/gacabartosz/presidio-local-anonymizer/main/scripts/install.sh | bash

set -e

# Kolory
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

echo_info() {
    echo -e "${CYAN}$1${NC}"
}

echo_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

echo_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Header
echo ""
echo_info "========================================"
echo_info "PRESIDIO LOCAL ANONYMIZER - INSTALATOR"
echo_info "========================================"
echo ""

# Wykryj system operacyjny
OS_TYPE=$(uname -s)
echo_info "Wykryto system: $OS_TYPE"

# Ustaw ścieżki instalacji
if [[ "$OS_TYPE" == "Darwin" ]]; then
    # macOS
    INSTALL_BASE="$HOME/Library/Application Support/PresidioAnon"
    INSTALL_BIN="$INSTALL_BASE/bin"
else
    # Linux
    INSTALL_BASE="$HOME/.presidio-anonymizer"
    INSTALL_BIN="$INSTALL_BASE/bin"
fi

echo_info "Lokalizacja instalacji: $INSTALL_BASE"
echo ""

# =============================================================================
# SEKCJA 1: SPRAWDŹ HOMEBREW (macOS)
# =============================================================================

if [[ "$OS_TYPE" == "Darwin" ]]; then
    echo_info "Sprawdzanie Homebrew..."

    if ! command -v brew &> /dev/null; then
        echo_warning "Homebrew nie znaleziony. Instalowanie..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

        # Dodaj brew do PATH
        if [[ -f "/opt/homebrew/bin/brew" ]]; then
            eval "$(/opt/homebrew/bin/brew shellenv)"
        elif [[ -f "/usr/local/bin/brew" ]]; then
            eval "$(/usr/local/bin/brew shellenv)"
        fi

        echo_success "Homebrew zainstalowany"
    else
        echo_success "Homebrew już zainstalowany"
    fi
fi

# =============================================================================
# SEKCJA 2: INSTALACJA PYTHON
# =============================================================================

echo ""
echo_info "Sprawdzanie Python 3.11..."

# Funkcja sprawdzająca wersję Python
check_python_version() {
    if command -v python3 &> /dev/null; then
        local version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        local major=$(echo $version | cut -d. -f1)
        local minor=$(echo $version | cut -d. -f2)

        if [[ $major -ge 3 ]] && [[ $minor -ge 11 ]]; then
            return 0  # Wersja OK
        fi
    fi
    return 1  # Wersja za stara lub brak Python
}

# Sprawdź czy Python 3.11+ istnieje
if check_python_version; then
    PYTHON_VERSION=$(python3 --version)
    echo_success "Python już zainstalowany: $PYTHON_VERSION"
else
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        echo_warning "Znaleziono $PYTHON_VERSION, ale wymagane jest Python 3.11+"
    else
        echo_warning "Python nie znaleziony."
    fi

    if [[ "$OS_TYPE" == "Darwin" ]]; then
        echo_info "Instalowanie Python 3.11 przez Homebrew..."
        brew install python@3.11

        # Instaluj python-tk dla GUI (tkinter)
        echo_info "Instalowanie python-tk@3.11 (dla GUI)..."
        brew install python-tk@3.11

        # Instaluj poppler dla przetwarzania PDF
        echo_info "Instalowanie poppler (dla PDF)..."
        brew install poppler

        # Dodaj Python 3.11 do PATH dla bieżącej sesji
        export PATH="/opt/homebrew/opt/python@3.11/bin:$PATH"

        # Sprawdź czy instalacja się powiodła
        if command -v python3.11 &> /dev/null; then
            # Użyj python3.11 zamiast python3
            ln -sf /opt/homebrew/opt/python@3.11/bin/python3.11 /opt/homebrew/bin/python3 2>/dev/null || true
            echo_success "Python 3.11 i python-tk zainstalowane"
        else
            echo_error "Nie udało się zainstalować Python 3.11"
            exit 1
        fi
    else
        echo_error "Zainstaluj Python 3.11 ręcznie: sudo apt-get install python3.11"
        exit 1
    fi
fi

# =============================================================================
# SEKCJA 3: INSTALACJA GIT
# =============================================================================

echo ""
echo_info "Sprawdzanie Git..."

if ! command -v git &> /dev/null; then
    if [[ "$OS_TYPE" == "Darwin" ]]; then
        echo_warning "Git nie znaleziony. Instalowanie..."
        brew install git
        echo_success "Git zainstalowany"
    else
        echo_error "Git nie znaleziony. Zainstaluj ręcznie: sudo apt-get install git"
        exit 1
    fi
else
    GIT_VERSION=$(git --version)
    echo_success "Git już zainstalowany: $GIT_VERSION"
fi

# =============================================================================
# SEKCJA 4: INSTALACJA TESSERACT OCR (dla skanów)
# =============================================================================

echo ""
echo_info "Sprawdzanie Tesseract OCR (dla skanów PDF i obrazów)..."

if ! command -v tesseract &> /dev/null; then
    if [[ "$OS_TYPE" == "Darwin" ]]; then
        echo_warning "Tesseract nie znaleziony. Instalowanie..."
        brew install tesseract
        brew install tesseract-lang  # Polski model językowy
        echo_success "Tesseract OCR zainstalowany"
    else
        echo_warning "Tesseract nie znaleziony. Instalowanie..."
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y tesseract-ocr tesseract-ocr-pol
            echo_success "Tesseract OCR zainstalowany"
        else
            echo_error "Nie można zainstalować Tesseract. Zainstaluj ręcznie."
        fi
    fi
else
    TESS_VERSION=$(tesseract --version | head -n1)
    echo_success "Tesseract już zainstalowany: $TESS_VERSION"
fi

# =============================================================================
# SEKCJA 4A: INSTALACJA POPPLER (dla PDF)
# =============================================================================

echo ""
echo_info "Sprawdzanie poppler (dla przetwarzania PDF)..."

if ! command -v pdftoppm &> /dev/null; then
    if [[ "$OS_TYPE" == "Darwin" ]]; then
        echo_warning "Poppler nie znaleziony. Instalowanie..."
        brew install poppler
        echo_success "Poppler zainstalowany"
    else
        echo_warning "Poppler nie znaleziony. Instalowanie..."
        if command -v apt-get &> /dev/null; then
            sudo apt-get install -y poppler-utils
            echo_success "Poppler zainstalowany"
        else
            echo_error "Nie można zainstalować poppler. Zainstaluj ręcznie."
        fi
    fi
else
    POPPLER_VERSION=$(pdftoppm -v 2>&1 | head -n1)
    echo_success "Poppler już zainstalowany: $POPPLER_VERSION"
fi

# =============================================================================
# SEKCJA 5: TWORZENIE KATALOGÓW
# =============================================================================

echo ""
echo_info "Tworzenie katalogów instalacji..."

mkdir -p "$INSTALL_BASE"
mkdir -p "$INSTALL_BIN"

echo_success "Katalogi utworzone"

# =============================================================================
# SEKCJA 6: KLONOWANIE REPOZYTORIUM
# =============================================================================

echo ""
echo_info "Pobieranie kodu źródłowego..."

REPO_URL="https://github.com/gacabartosz/presidio-local-anonymizer.git"
APP_DIR="$INSTALL_BASE/app"

if [[ -d "$APP_DIR/.git" ]]; then
    echo_info "Repozytorium już istnieje. Aktualizowanie..."
    cd "$APP_DIR"
    git pull origin main
    echo_success "Kod zaktualizowany"
else
    echo_info "Klonowanie repozytorium..."
    git clone "$REPO_URL" "$APP_DIR"
    echo_success "Repozytorium sklonowane"
fi

# =============================================================================
# SEKCJA 7: ŚRODOWISKO WIRTUALNE PYTHON
# =============================================================================

echo ""
echo_info "Konfigurowanie środowiska Python..."

VENV_DIR="$APP_DIR/.venv"

# Znajdź odpowiednią wersję Python
PYTHON_CMD="python3"
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
elif command -v python3.12 &> /dev/null; then
    PYTHON_CMD="python3.12"
fi

echo_info "Używam: $PYTHON_CMD ($($PYTHON_CMD --version))"

if [[ ! -d "$VENV_DIR" ]]; then
    echo_info "Tworzenie środowiska wirtualnego..."
    $PYTHON_CMD -m venv "$VENV_DIR"
    echo_success "Środowisko wirtualne utworzone"
fi

# Aktywuj venv
source "$VENV_DIR/bin/activate"

# Aktualizuj pip
echo_info "Aktualizowanie pip..."
pip install --upgrade pip --quiet

# Instaluj zależności
echo_info "Instalowanie zależności Python (może potrwać kilka minut)..."
pip install -r "$APP_DIR/requirements.txt" --quiet

echo_success "Zależności zainstalowane"

# Pobierz model SpaCy
echo_info "Pobieranie modelu językowego SpaCy dla języka polskiego..."

# Zainstaluj przez pip z bezpośrednim URL (bardziej niezawodne niż spacy download)
pip install https://github.com/explosion/spacy-models/releases/download/pl_core_news_md-3.7.0/pl_core_news_md-3.7.0-py3-none-any.whl --quiet

echo_success "Model językowy pobrany"

# =============================================================================
# SEKCJA 8: TWORZENIE SKRYPTU WRAPPER
# =============================================================================

echo ""
echo_info "Tworzenie skryptu wrapper..."

WRAPPER_PATH="$INSTALL_BIN/anonymize"

cat > "$WRAPPER_PATH" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(dirname "$SCRIPT_DIR")/app"
PYTHON_EXE="$APP_DIR/.venv/bin/python"
MAIN_SCRIPT="$APP_DIR/app/main.py"

"$PYTHON_EXE" "$MAIN_SCRIPT" "$@"
EOF

chmod +x "$WRAPPER_PATH"

echo_success "Skrypt wrapper utworzony: $WRAPPER_PATH"

# =============================================================================
# SEKCJA 9: DODANIE DO PATH
# =============================================================================

echo ""
echo_info "Dodawanie do PATH..."

# Wykryj shell
if [[ -n "$ZSH_VERSION" ]]; then
    SHELL_RC="$HOME/.zshrc"
elif [[ -n "$BASH_VERSION" ]]; then
    SHELL_RC="$HOME/.bashrc"
    # Na macOS często używa się .bash_profile
    if [[ "$OS_TYPE" == "Darwin" && -f "$HOME/.bash_profile" ]]; then
        SHELL_RC="$HOME/.bash_profile"
    fi
else
    SHELL_RC="$HOME/.profile"
fi

# Dodaj do PATH jeśli jeszcze nie ma
if ! grep -q "PresidioAnon/bin" "$SHELL_RC" 2>/dev/null; then
    echo "" >> "$SHELL_RC"
    echo "# Presidio Local Anonymizer" >> "$SHELL_RC"
    echo "export PATH=\"$INSTALL_BIN:\$PATH\"" >> "$SHELL_RC"
    echo_success "Dodano do PATH w $SHELL_RC"
    echo_warning "Uruchom ponownie terminal lub wykonaj: source $SHELL_RC"
else
    echo_success "PATH już skonfigurowany"
fi

# Dodaj do bieżącej sesji
export PATH="$INSTALL_BIN:$PATH"

# =============================================================================
# SEKCJA 10: TWORZENIE SKRYPTU GUI (opcjonalnie)
# =============================================================================

echo ""
echo_info "Tworzenie skryptu GUI..."

GUI_WRAPPER="$INSTALL_BIN/anonymize-gui"

cat > "$GUI_WRAPPER" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(dirname "$SCRIPT_DIR")/app"
PYTHON_EXE="$APP_DIR/.venv/bin/python"
GUI_SCRIPT="$APP_DIR/app/gui.py"

"$PYTHON_EXE" "$GUI_SCRIPT"
EOF

chmod +x "$GUI_WRAPPER"

echo_success "Skrypt GUI utworzony"

# =============================================================================
# SEKCJA 11: AUTOMATOR (macOS - menu kontekstowe)
# =============================================================================

if [[ "$OS_TYPE" == "Darwin" ]]; then
    echo ""
    echo_info "Tworzenie usługi Automator dla macOS..."

    SERVICES_DIR="$HOME/Library/Services"
    mkdir -p "$SERVICES_DIR"

    SERVICE_NAME="Anonimizuj (Presidio).workflow"
    SERVICE_PATH="$SERVICES_DIR/$SERVICE_NAME"

    # Utwórz prostą usługę Automator
    mkdir -p "$SERVICE_PATH/Contents"

    cat > "$SERVICE_PATH/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSServices</key>
    <array>
        <dict>
            <key>NSMenuItem</key>
            <dict>
                <key>default</key>
                <string>Anonimizuj (Presidio)</string>
            </dict>
            <key>NSMessage</key>
            <string>runWorkflowAsService</string>
            <key>NSSendFileTypes</key>
            <array>
                <string>public.item</string>
            </array>
        </dict>
    </array>
</dict>
</plist>
EOF

    echo_success "Usługa Automator utworzona"
    echo_warning "Aby aktywować menu kontekstowe:"
    echo_info "  1. Otwórz System Preferences → Keyboard → Shortcuts → Services"
    echo_info "  2. Znajdź 'Anonimizuj (Presidio)' i zaznacz"
fi

# =============================================================================
# SEKCJA 12: KOMUNIKATY KOŃCOWE
# =============================================================================

echo ""
echo_success "========================================"
echo_success "INSTALACJA ZAKOŃCZONA POMYŚLNIE!"
echo_success "========================================"
echo ""

echo_info "Lokalizacja instalacji: $INSTALL_BASE"
echo ""

echo_info "Przykłady użycia:"
echo "  1. CLI: anonymize dokument.docx"
echo "  2. GUI: anonymize-gui"
if [[ "$OS_TYPE" == "Darwin" ]]; then
    echo "  3. Finder: Kliknij prawym na pliku → Quick Actions → Anonimizuj (Presidio)"
fi
echo ""

echo_warning "WAŻNE: Uruchom ponownie terminal lub wykonaj:"
echo "  source $SHELL_RC"
echo ""

echo_info "Aby odinstalować, uruchom:"
echo "  $APP_DIR/scripts/uninstall.sh"
echo ""

echo_success "Gotowe! 🎉"
