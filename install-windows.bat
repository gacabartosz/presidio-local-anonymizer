@echo off
REM Presidio Browser Anonymizer - Windows Installer
REM Automatyczna instalacja backendu dla Windows

echo ========================================
echo Presidio Browser Anonymizer
echo Instalacja Backendu dla Windows
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python nie jest zainstalowany!
    echo.
    echo Pobierz Python z: https://www.python.org/downloads/
    echo WAZNE: Zaznacz "Add Python to PATH" podczas instalacji!
    echo.
    pause
    exit /b 1
)

echo [OK] Python jest zainstalowany
python --version
echo.

REM Navigate to backend directory
cd /d "%~dp0backend"
if %errorlevel% neq 0 (
    echo [ERROR] Katalog backend/ nie istnieje!
    pause
    exit /b 1
)

echo [1/5] Tworzenie wirtualnego srodowiska...
python -m venv .venv
if %errorlevel% neq 0 (
    echo [ERROR] Nie udalo sie utworzyc venv!
    pause
    exit /b 1
)
echo [OK] Wirtualne srodowisko utworzone
echo.

echo [2/5] Aktywowanie venv...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Nie udalo sie aktywowac venv!
    pause
    exit /b 1
)
echo [OK] Venv aktywowane
echo.

echo [3/5] Instalowanie zaleznosci...
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Instalacja zaleznosci nie powiodla sie!
    pause
    exit /b 1
)
echo [OK] Zaleznosci zainstalowane
echo.

echo [4/5] Pobieranie modelu SpaCy (pl_core_news_md)...
python -m spacy download pl_core_news_md
if %errorlevel% neq 0 (
    echo [ERROR] Nie udalo sie pobrac modelu SpaCy!
    pause
    exit /b 1
)
echo [OK] Model SpaCy pobrany
echo.

echo [5/5] Uruchamianie backendu...
echo.
echo ========================================
echo BACKEND URUCHOMIONY!
echo ========================================
echo.
echo Backend URL: http://localhost:4222
echo Dashboard:   http://localhost:4222/dashboard
echo Ustawienia:  http://localhost:4222/
echo.
echo Nacisnij Ctrl+C aby zatrzymac backend
echo ========================================
echo.

python app.py

pause
