#!/bin/bash
# Presidio Browser Anonymizer - Linux Installer
# Automatyczna instalacja backendu dla Linux

set -e  # Exit on error

echo "========================================"
echo "Presidio Browser Anonymizer"
echo "Instalacja Backendu dla Linux"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 nie jest zainstalowany!"
    echo ""
    echo "Zainstaluj Python3:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "  Fedora/RHEL:   sudo dnf install python3 python3-pip"
    echo "  Arch:          sudo pacman -S python python-pip"
    exit 1
fi

echo "[OK] Python3 jest zainstalowany"
python3 --version
echo ""

# Check if venv is available
if ! python3 -m venv --help &> /dev/null; then
    echo "[ERROR] python3-venv nie jest zainstalowany!"
    echo ""
    echo "Zainstaluj python3-venv:"
    echo "  Ubuntu/Debian: sudo apt install python3-venv"
    echo "  Fedora/RHEL:   sudo dnf install python3-venv"
    exit 1
fi

# Navigate to backend directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/backend"

echo "[1/5] Tworzenie wirtualnego środowiska..."
python3 -m venv .venv
echo "[OK] Wirtualne środowisko utworzone"
echo ""

echo "[2/5] Aktywowanie venv..."
source .venv/bin/activate
echo "[OK] Venv aktywowane"
echo ""

echo "[3/5] Instalowanie zależności..."
pip install --upgrade pip
pip install -r requirements.txt
echo "[OK] Zależności zainstalowane"
echo ""

echo "[4/5] Pobieranie modelu SpaCy (pl_core_news_md)..."
python -m spacy download pl_core_news_md
echo "[OK] Model SpaCy pobrany"
echo ""

echo "[5/5] Uruchamianie backendu..."
echo ""
echo "========================================"
echo "BACKEND URUCHOMIONY!"
echo "========================================"
echo ""
echo "Backend URL: http://localhost:4222"
echo "Dashboard:   http://localhost:4222/dashboard"
echo "Ustawienia:  http://localhost:4222/"
echo ""
echo "Naciśnij Ctrl+C aby zatrzymać backend"
echo "========================================"
echo ""

python app.py
