#!/bin/bash
# Standalone Installer - Presidio Local Anonymizer
# Pobierz ten plik i uruchom: bash install-standalone.sh

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo_success() { echo -e "${GREEN}✓ $1${NC}"; }
echo_info() { echo -e "${CYAN}$1${NC}"; }
echo_warning() { echo -e "${YELLOW}⚠ $1${NC}"; }
echo_error() { echo -e "${RED}✗ $1${NC}"; }

clear
echo ""
echo_info "=========================================="
echo_info "  PRESIDIO LOCAL ANONYMIZER"
echo_info "  Prosty Instalator"
echo_info "=========================================="
echo ""
echo_info "Ten skrypt zainstaluje wszystkie wymagane"
echo_info "składniki i skonfiguruje aplikację."
echo ""
read -p "Naciśnij Enter aby kontynuować..."

# Wykryj OS
OS_TYPE=$(uname -s)
echo ""
echo_info "System: $OS_TYPE"

if [[ "$OS_TYPE" == "Darwin" ]]; then
    INSTALL_BASE="$HOME/Library/Application Support/PresidioAnon"
    INSTALL_BIN="$INSTALL_BASE/bin"
elif [[ "$OS_TYPE" == "Linux" ]]; then
    INSTALL_BASE="$HOME/.presidio-anonymizer"
    INSTALL_BIN="$INSTALL_BASE/bin"
else
    echo_error "Nieobsługiwany system: $OS_TYPE"
    exit 1
fi

echo_info "Lokalizacja: $INSTALL_BASE"
echo ""

# =============================================================================
# KROK 1: HOMEBREW (macOS)
# =============================================================================

if [[ "$OS_TYPE" == "Darwin" ]]; then
    echo_info "[1/10] Sprawdzanie Homebrew..."

    if ! command -v brew &> /dev/null; then
        echo_warning "Instalowanie Homebrew (wymaga hasła)..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

        # Dodaj do PATH
        if [[ -f "/opt/homebrew/bin/brew" ]]; then
            eval "$(/opt/homebrew/bin/brew shellenv)"
        fi

        echo_success "Homebrew zainstalowany"
    else
        echo_success "Homebrew już zainstalowany"
    fi
fi

# =============================================================================
# KROK 2: PYTHON 3.11
# =============================================================================

echo ""
echo_info "[2/10] Sprawdzanie Python 3.11..."

check_python() {
    if command -v python3.11 &> /dev/null; then
        return 0
    elif command -v python3 &> /dev/null; then
        local version=$(python3 -c 'import sys; v=sys.version_info; print(f"{v.major}.{v.minor}")')
        local major=$(echo $version | cut -d. -f1)
        local minor=$(echo $version | cut -d. -f2)

        if [[ $major -ge 3 ]] && [[ $minor -ge 11 ]]; then
            return 0
        fi
    fi
    return 1
}

if check_python; then
    echo_success "Python 3.11+ jest dostępny"
else
    if [[ "$OS_TYPE" == "Darwin" ]]; then
        echo_warning "Instalowanie Python 3.11..."
        brew install python@3.11

        echo_warning "Instalowanie python-tk@3.11 (dla GUI)..."
        brew install python-tk@3.11

        export PATH="/opt/homebrew/opt/python@3.11/bin:$PATH"
        echo_success "Python 3.11 i python-tk zainstalowane"
    else
        echo_error "Python 3.11 nie znaleziony"
        echo "Zainstaluj: sudo apt-get install python3.11 python3.11-venv python3-tk"
        exit 1
    fi
fi

# =============================================================================
# KROK 3: GIT
# =============================================================================

echo ""
echo_info "[3/10] Sprawdzanie Git..."

if ! command -v git &> /dev/null; then
    if [[ "$OS_TYPE" == "Darwin" ]]; then
        echo_warning "Instalowanie Git..."
        brew install git
        echo_success "Git zainstalowany"
    else
        echo_error "Git nie znaleziony"
        echo "Zainstaluj: sudo apt-get install git"
        exit 1
    fi
else
    echo_success "Git już zainstalowany"
fi

# =============================================================================
# KROK 4: TESSERACT OCR
# =============================================================================

echo ""
echo_info "[4/10] Sprawdzanie Tesseract OCR..."

if ! command -v tesseract &> /dev/null; then
    echo_warning "Instalowanie Tesseract OCR (może potrwać)..."

    if [[ "$OS_TYPE" == "Darwin" ]]; then
        brew install tesseract tesseract-lang
    else
        echo_error "Tesseract nie znaleziony"
        echo "Zainstaluj: sudo apt-get install tesseract-ocr tesseract-ocr-pol"
        exit 1
    fi

    echo_success "Tesseract zainstalowany"
else
    echo_success "Tesseract już zainstalowany"
fi

# =============================================================================
# KROK 5: KATALOGI
# =============================================================================

echo ""
echo_info "[5/10] Tworzenie katalogów..."

mkdir -p "$INSTALL_BASE"
mkdir -p "$INSTALL_BIN"

echo_success "Katalogi utworzone"

# =============================================================================
# KROK 6: KLONOWANIE REPO
# =============================================================================

echo ""
echo_info "[6/10] Pobieranie kodu..."

APP_DIR="$INSTALL_BASE/app"

if [[ -d "$APP_DIR/.git" ]]; then
    echo_info "Aktualizowanie..."
    cd "$APP_DIR"
    git pull origin main
else
    echo_info "Klonowanie repozytorium..."
    git clone https://github.com/gacabartosz/presidio-local-anonymizer.git "$APP_DIR"
fi

echo_success "Kod pobrany"

# =============================================================================
# KROK 7: VENV
# =============================================================================

echo ""
echo_info "[7/10] Konfigurowanie Python..."

VENV_DIR="$APP_DIR/.venv"

# Znajdź Python
PYTHON_CMD="python3"
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
fi

if [[ ! -d "$VENV_DIR" ]]; then
    echo_info "Tworzenie środowiska wirtualnego..."
    $PYTHON_CMD -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
pip install --upgrade pip --quiet

echo_success "Środowisko Python gotowe"

# =============================================================================
# KROK 8: ZALEŻNOŚCI
# =============================================================================

echo ""
echo_info "[8/10] Instalowanie zależności (5-10 minut)..."

cd "$APP_DIR"
pip install -r requirements.txt --quiet

echo_success "Zależności zainstalowane"

# =============================================================================
# KROK 9: MODEL SPACY
# =============================================================================

echo ""
echo_info "[9/10] Pobieranie modelu językowego..."

# Zainstaluj przez pip z bezpośrednim URL (bardziej niezawodne niż spacy download)
pip install https://github.com/explosion/spacy-models/releases/download/pl_core_news_md-3.7.0/pl_core_news_md-3.7.0-py3-none-any.whl --quiet

echo_success "Model językowy pobrany"

# =============================================================================
# KROK 10: WRAPPER SCRIPTS
# =============================================================================

echo ""
echo_info "[10/10] Tworzenie skryptów..."

# anonymize wrapper
cat > "$INSTALL_BIN/anonymize" << 'ANONYMIZE_EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(dirname "$SCRIPT_DIR")/app"
PYTHON_EXE="$APP_DIR/.venv/bin/python"
MAIN_SCRIPT="$APP_DIR/app/main.py"

"$PYTHON_EXE" "$MAIN_SCRIPT" "$@"
ANONYMIZE_EOF

chmod +x "$INSTALL_BIN/anonymize"

# anonymize-gui wrapper
cat > "$INSTALL_BIN/anonymize-gui" << 'GUI_EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(dirname "$SCRIPT_DIR")/app"
PYTHON_EXE="$APP_DIR/.venv/bin/python"
GUI_SCRIPT="$APP_DIR/app/gui.py"

"$PYTHON_EXE" "$GUI_SCRIPT"
GUI_EOF

chmod +x "$INSTALL_BIN/anonymize-gui"

echo_success "Skrypty utworzone"

# =============================================================================
# PATH
# =============================================================================

echo ""
echo_info "Dodawanie do PATH..."

# Wykryj shell
if [[ -n "$ZSH_VERSION" ]]; then
    SHELL_RC="$HOME/.zshrc"
elif [[ -n "$BASH_VERSION" ]]; then
    SHELL_RC="$HOME/.bashrc"
    if [[ "$OS_TYPE" == "Darwin" && -f "$HOME/.bash_profile" ]]; then
        SHELL_RC="$HOME/.bash_profile"
    fi
else
    SHELL_RC="$HOME/.profile"
fi

if ! grep -q "PresidioAnon/bin" "$SHELL_RC" 2>/dev/null; then
    echo "" >> "$SHELL_RC"
    echo "# Presidio Local Anonymizer" >> "$SHELL_RC"
    echo "export PATH=\"$INSTALL_BIN:\$PATH\"" >> "$SHELL_RC"
    echo_success "PATH zaktualizowany w $SHELL_RC"
else
    echo_success "PATH już skonfigurowany"
fi

# Dodaj do bieżącej sesji
export PATH="$INSTALL_BIN:$PATH"

# =============================================================================
# KONIEC
# =============================================================================

echo ""
echo_success "=========================================="
echo_success "  INSTALACJA ZAKOŃCZONA!"
echo_success "=========================================="
echo ""
echo_info "Możesz teraz uruchomić aplikację:"
echo ""
echo "  1. GUI:    anonymize-gui"
echo "  2. CLI:    anonymize plik.docx"
echo ""
echo_warning "WAŻNE: Uruchom ponownie terminal lub wykonaj:"
echo "  source $SHELL_RC"
echo ""
echo_info "Dokumentacja:"
echo "  https://github.com/gacabartosz/presidio-local-anonymizer"
echo ""
echo_success "Gotowe! 🎉"
echo ""
