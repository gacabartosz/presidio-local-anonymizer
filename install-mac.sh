#!/bin/bash
# Presidio Browser Anonymizer - macOS Installer
# Automatyczna instalacja backendu dla macOS

set -e  # Exit on error

echo "========================================"
echo "Presidio Browser Anonymizer"
echo "Instalacja Backendu dla macOS"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 nie jest zainstalowany!"
    echo ""
    echo "Zainstaluj Python3 używając Homebrew:"
    echo "  brew install python3"
    echo ""
    echo "Lub pobierz z: https://www.python.org/downloads/"
    exit 1
fi

echo "[OK] Python3 jest zainstalowany"
python3 --version
echo ""

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
