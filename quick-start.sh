#!/bin/bash
# Quick Start - Presidio Local Anonymizer
# Prosty skrypt który instaluje (jeśli trzeba) i uruchamia aplikację

set -e

# Kolory
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo_success() { echo -e "${GREEN}✓ $1${NC}"; }
echo_info() { echo -e "${CYAN}$1${NC}"; }
echo_warning() { echo -e "${YELLOW}⚠ $1${NC}"; }
echo_error() { echo -e "${RED}✗ $1${NC}"; }

# Wykryj OS
OS_TYPE=$(uname -s)

if [[ "$OS_TYPE" == "Darwin" ]]; then
    INSTALL_BASE="$HOME/Library/Application Support/PresidioAnon"
else
    INSTALL_BASE="$HOME/.presidio-anonymizer"
fi

echo ""
echo_info "======================================"
echo_info "  PRESIDIO LOCAL ANONYMIZER"
echo_info "  Quick Start"
echo_info "======================================"
echo ""

# Sprawdź czy aplikacja jest zainstalowana
if [[ ! -d "$INSTALL_BASE/app" ]]; then
    echo_warning "Aplikacja nie jest zainstalowana."
    echo_info "Rozpoczynam automatyczną instalację..."
    echo ""

    # Pobierz i uruchom instalator
    if [[ "$OS_TYPE" == "Darwin" ]] || [[ "$OS_TYPE" == "Linux" ]]; then
        # macOS/Linux
        bash <(curl -fsSL https://raw.githubusercontent.com/gacabartosz/presidio-local-anonymizer/main/scripts/install.sh)
    else
        echo_error "Nieobsługiwany system operacyjny: $OS_TYPE"
        exit 1
    fi

    echo ""
    echo_info "Instalacja zakończona!"
    echo ""
fi

# Sprawdź czy venv istnieje
if [[ ! -d "$INSTALL_BASE/app/.venv" ]]; then
    echo_error "Błąd: Środowisko Python nie zostało utworzone"
    echo_warning "Spróbuj ręcznej instalacji:"
    echo "  https://github.com/gacabartosz/presidio-local-anonymizer/blob/main/MANUAL_INSTALL.md"
    exit 1
fi

# Sprawdź czy GUI script istnieje
GUI_SCRIPT="$INSTALL_BASE/app/app/gui.py"
if [[ ! -f "$GUI_SCRIPT" ]]; then
    echo_error "Błąd: Nie znaleziono skryptu GUI"
    echo_warning "Reinstaluj aplikację lub zobacz:"
    echo "  https://github.com/gacabartosz/presidio-local-anonymizer/blob/main/TROUBLESHOOTING.md"
    exit 1
fi

# Uruchom GUI
echo_info "Uruchamiam interfejs graficzny..."
echo ""

PYTHON_EXE="$INSTALL_BASE/app/.venv/bin/python"

"$PYTHON_EXE" "$GUI_SCRIPT"

# Sprawdź kod wyjścia
if [[ $? -ne 0 ]]; then
    echo ""
    echo_error "GUI nie uruchomiło się poprawnie"
    echo_warning "Spróbuj uruchomić ręcznie:"
    echo "  cd '$INSTALL_BASE/app'"
    echo "  source .venv/bin/activate"
    echo "  python app/gui.py"
    echo ""
    echo_warning "Lub zobacz troubleshooting:"
    echo "  https://github.com/gacabartosz/presidio-local-anonymizer/blob/main/TROUBLESHOOTING.md"
    exit 1
fi
