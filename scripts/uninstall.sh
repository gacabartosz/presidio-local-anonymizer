#!/bin/bash
# Deinstalator Presidio Local Anonymizer dla macOS/Linux

set -e

# Kolory
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

echo_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

echo_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Header
echo ""
echo_error "========================================"
echo_error "PRESIDIO - DEINSTALACJA"
echo_error "========================================"
echo ""

# Wykryj system
OS_TYPE=$(uname -s)

if [[ "$OS_TYPE" == "Darwin" ]]; then
    INSTALL_BASE="$HOME/Library/Application Support/PresidioAnon"
else
    INSTALL_BASE="$HOME/.presidio-anonymizer"
fi

echo_warning "To działanie usunie:"
echo "  • Pliki aplikacji: $INSTALL_BASE"
echo "  • Wpis w PATH"
if [[ "$OS_TYPE" == "Darwin" ]]; then
    echo "  • Usługę Automator (menu kontekstowe)"
fi
echo ""

read -p "Czy na pewno chcesz odinstalować? (tak/nie): " CONFIRM

if [[ "$CONFIRM" != "tak" ]]; then
    echo ""
    echo_warning "Deinstalacja anulowana."
    exit 0
fi

echo ""
echo_warning "Deinstalowanie..."

# =============================================================================
# USUWANIE Z PATH
# =============================================================================

echo ""
echo_warning "Usuwanie z PATH..."

# Wykryj shell config
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

# Usuń wpis z PATH
if [[ -f "$SHELL_RC" ]]; then
    # Utwórz backup
    cp "$SHELL_RC" "$SHELL_RC.presidio-backup"

    # Usuń linie związane z Presidio
    sed -i.bak '/Presidio Local Anonymizer/d' "$SHELL_RC" 2>/dev/null || true
    sed -i.bak '/PresidioAnon\/bin/d' "$SHELL_RC" 2>/dev/null || true

    # Usuń pliki backup
    rm -f "$SHELL_RC.bak"

    echo_success "Usunięto z PATH"
else
    echo_warning "Plik $SHELL_RC nie istnieje"
fi

# =============================================================================
# USUWANIE USŁUGI AUTOMATOR (macOS)
# =============================================================================

if [[ "$OS_TYPE" == "Darwin" ]]; then
    echo ""
    echo_warning "Usuwanie usługi Automator..."

    SERVICE_PATH="$HOME/Library/Services/Anonimizuj (Presidio).workflow"

    if [[ -d "$SERVICE_PATH" ]]; then
        rm -rf "$SERVICE_PATH"
        echo_success "Usługa Automator usunięta"
    else
        echo_warning "Usługa nie istnieje"
    fi
fi

# =============================================================================
# USUWANIE PLIKÓW APLIKACJI
# =============================================================================

echo ""
echo_warning "Usuwanie plików aplikacji..."

if [[ -d "$INSTALL_BASE" ]]; then
    rm -rf "$INSTALL_BASE"
    echo_success "Pliki aplikacji usunięte"
else
    echo_warning "Folder instalacji nie istnieje"
fi

# =============================================================================
# KOMUNIKAT KOŃCOWY
# =============================================================================

echo ""
echo_success "========================================"
echo_success "DEINSTALACJA ZAKOŃCZONA"
echo_success "========================================"
echo ""

echo_success "Presidio Local Anonymizer został usunięty."
echo ""
echo_warning "Uruchom ponownie terminal aby zaktualizować PATH."
echo ""
echo_success "Backup konfiguracji shell: $SHELL_RC.presidio-backup"
echo ""
