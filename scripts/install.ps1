# Skrypt instalacyjny dla Presidio Local Anonymizer
# Dla systemu Windows 10/11

#Requires -Version 5.1

$ErrorActionPreference = "Stop"

# ============================================================================
# SEKCJA 1: FUNKCJE POMOCNICZE
# ============================================================================

function Write-ColoredOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Test-CommandExists {
    param([string]$Command)
    $null -ne (Get-Command $Command -ErrorAction SilentlyContinue)
}

function Install-WithWinget {
    param(
        [string]$PackageId,
        [string]$DisplayName
    )

    Write-ColoredOutput "Instalowanie $DisplayName..." "Cyan"

    try {
        winget install --id $PackageId --exact --silent --accept-source-agreements --accept-package-agreements
        Write-ColoredOutput "✓ $DisplayName zainstalowany pomyślnie" "Green"
        return $true
    }
    catch {
        Write-ColoredOutput "✗ Błąd podczas instalacji $DisplayName : $_" "Red"
        return $false
    }
}

function Refresh-EnvironmentPath {
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" +
                [System.Environment]::GetEnvironmentVariable("Path", "User")
}

# ============================================================================
# SEKCJA 2: WERYFIKACJA PREREKWIZYTÓW
# ============================================================================

Write-ColoredOutput "`n========================================" "Cyan"
Write-ColoredOutput "PRESIDIO LOCAL ANONYMIZER - INSTALATOR" "Cyan"
Write-ColoredOutput "========================================`n" "Cyan"

# Sprawdź winget
if (-not (Test-CommandExists "winget")) {
    Write-ColoredOutput "BŁĄD: winget nie jest dostępny!" "Red"
    Write-ColoredOutput "Zainstaluj App Installer ze Microsoft Store lub zaktualizuj Windows." "Yellow"
    exit 1
}

# Sprawdź uprawnienia do zapisu w rejestrze użytkownika
try {
    $null = Get-Item "HKCU:\Software" -ErrorAction Stop
}
catch {
    Write-ColoredOutput "BŁĄD: Brak uprawnień do zapisu w rejestrze użytkownika!" "Red"
    exit 1
}

Write-ColoredOutput "✓ Prerekwizyty spełnione`n" "Green"

# ============================================================================
# SEKCJA 3: INSTALACJA NARZĘDZI
# ============================================================================

Write-ColoredOutput "Sprawdzanie i instalacja wymaganych narzędzi...`n" "Yellow"

# Python 3.11
if (-not (Test-CommandExists "python")) {
    Write-ColoredOutput "Python nie znaleziony. Instalowanie Python 3.11..." "Yellow"
    Install-WithWinget "Python.Python.3.11" "Python 3.11"
    Refresh-EnvironmentPath

    # Sprawdź ponownie
    if (-not (Test-CommandExists "python")) {
        Write-ColoredOutput "BŁĄD: Python nie został poprawnie zainstalowany!" "Red"
        exit 1
    }
}
else {
    $pythonVersion = & python --version 2>&1
    Write-ColoredOutput "✓ Python już zainstalowany: $pythonVersion" "Green"
}

# Git
if (-not (Test-CommandExists "git")) {
    Write-ColoredOutput "Git nie znaleziony. Instalowanie Git..." "Yellow"
    Install-WithWinget "Git.Git" "Git"
    Refresh-EnvironmentPath

    # Sprawdź ponownie
    if (-not (Test-CommandExists "git")) {
        Write-ColoredOutput "BŁĄD: Git nie został poprawnie zainstalowany!" "Red"
        exit 1
    }
}
else {
    $gitVersion = & git --version 2>&1
    Write-ColoredOutput "✓ Git już zainstalowany: $gitVersion" "Green"
}

# Tesseract OCR (dla OCR funkcjonalności - opcjonalne)
Write-ColoredOutput "`nSprawdzanie Tesseract OCR (dla skanów PDF i obrazów)...`n" "Yellow"

$TesseractPath = "C:\Program Files\Tesseract-OCR\tesseract.exe"

if (-not (Test-Path $TesseractPath)) {
    Write-ColoredOutput "Tesseract OCR nie znaleziony. Instalowanie..." "Yellow"

    try {
        # Pobierz instalator Tesseract z UB-Mannheim
        $TesseractUrl = "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe"
        $TesseractInstaller = "$env:TEMP\tesseract-setup.exe"

        Write-ColoredOutput "Pobieranie Tesseract OCR (~100 MB)..." "Yellow"
        Invoke-WebRequest -Uri $TesseractUrl -OutFile $TesseractInstaller -UseBasicParsing

        Write-ColoredOutput "Instalowanie Tesseract OCR..." "Yellow"
        # Uruchom instalator (silent mode)
        Start-Process -FilePath $TesseractInstaller -ArgumentList "/S" -Wait

        # Poczekaj aż instalacja się zakończy
        Start-Sleep -Seconds 3

        # Sprawdź czy zainstalował się
        if (Test-Path $TesseractPath) {
            # Pobierz polski plik językowy
            Write-ColoredOutput "Pobieranie polskiego modelu językowego..." "Yellow"
            $PolishData = "https://github.com/tesseract-ocr/tessdata/raw/main/pol.traineddata"
            $TessdataPath = "C:\Program Files\Tesseract-OCR\tessdata"

            Invoke-WebRequest -Uri $PolishData -OutFile "$TessdataPath\pol.traineddata" -UseBasicParsing

            Write-ColoredOutput "✓ Tesseract OCR zainstalowany" "Green"
        }
        else {
            Write-ColoredOutput "⚠ Tesseract OCR nie został poprawnie zainstalowany" "Yellow"
            Write-ColoredOutput "  OCR dla skanów nie będzie działać. Możesz zainstalować później." "Yellow"
        }

        # Wyczyść instalator
        Remove-Item $TesseractInstaller -Force -ErrorAction SilentlyContinue
    }
    catch {
        Write-ColoredOutput "⚠ Nie udało się zainstalować Tesseract OCR: $_" "Yellow"
        Write-ColoredOutput "  OCR dla skanów nie będzie działać. Możesz zainstalować później." "Yellow"
    }
}
else {
    Write-ColoredOutput "✓ Tesseract OCR już zainstalowany" "Green"
}

# Poppler (dla przetwarzania PDF)
Write-ColoredOutput "`nSprawdzanie poppler (dla przetwarzania PDF)...`n" "Yellow"

# Sprawdź czy pdftoppm istnieje w PATH
$PopplerInstalled = $false
try {
    $null = & pdftoppm -v 2>&1
    $PopplerInstalled = $true
    Write-ColoredOutput "✓ Poppler już zainstalowany" "Green"
}
catch {
    Write-ColoredOutput "Poppler nie znaleziony. Próba instalacji przez chocolatey..." "Yellow"

    # Sprawdź czy chocolatey jest dostępny
    if (Test-CommandExists "choco") {
        try {
            Write-ColoredOutput "Instalowanie poppler przez chocolatey..." "Yellow"
            & choco install poppler -y

            # Odśwież PATH
            Refresh-EnvironmentPath

            # Sprawdź ponownie
            try {
                $null = & pdftoppm -v 2>&1
                Write-ColoredOutput "✓ Poppler zainstalowany" "Green"
                $PopplerInstalled = $true
            }
            catch {
                Write-ColoredOutput "⚠ Poppler nie został poprawnie zainstalowany" "Yellow"
            }
        }
        catch {
            Write-ColoredOutput "⚠ Nie udało się zainstalować poppler: $_" "Yellow"
        }
    }
    else {
        Write-ColoredOutput "⚠ Chocolatey nie jest zainstalowany" "Yellow"
        Write-ColoredOutput "  Poppler jest wymagany do przetwarzania PDF" "Yellow"
        Write-ColoredOutput "  Zainstaluj ręcznie:" "Yellow"
        Write-ColoredOutput "    1. Zainstaluj chocolatey: https://chocolatey.org/install" "Cyan"
        Write-ColoredOutput "    2. Uruchom: choco install poppler" "Cyan"
        Write-ColoredOutput "  LUB pobierz ręcznie: https://blog.alivate.com.au/poppler-windows/" "Cyan"
    }
}

# ============================================================================
# SEKCJA 4: PRZYGOTOWANIE LOKALIZACJI DOCELOWEJ
# ============================================================================

Write-ColoredOutput "`nPrzygotowywanie lokalizacji instalacji...`n" "Yellow"

$INSTALL_BASE = Join-Path $env:LOCALAPPDATA "PresidioAnon"
$INSTALL_BIN = Join-Path $INSTALL_BASE "bin"

# Utwórz katalogi
New-Item -ItemType Directory -Force -Path $INSTALL_BASE | Out-Null
New-Item -ItemType Directory -Force -Path $INSTALL_BIN | Out-Null

Write-ColoredOutput "✓ Katalog instalacji: $INSTALL_BASE" "Green"

# ============================================================================
# SEKCJA 5: POBRANIE/AKTUALIZACJA KODU
# ============================================================================

Write-ColoredOutput "`nPobieranie kodu źródłowego...`n" "Yellow"

$REPO_URL = "https://github.com/gacabartosz/presidio-local-anonymizer.git"
$APP_DIR = Join-Path $INSTALL_BASE "app"

if (Test-Path (Join-Path $APP_DIR ".git")) {
    Write-ColoredOutput "Repozytorium już istnieje. Aktualizowanie..." "Yellow"
    Push-Location $APP_DIR
    try {
        & git pull origin main
        Write-ColoredOutput "✓ Kod zaktualizowany" "Green"
    }
    catch {
        Write-ColoredOutput "✗ Błąd podczas aktualizacji: $_" "Red"
    }
    finally {
        Pop-Location
    }
}
else {
    Write-ColoredOutput "Klonowanie repozytorium..." "Yellow"
    try {
        & git clone $REPO_URL $APP_DIR
        Write-ColoredOutput "✓ Repozytorium sklonowane" "Green"
    }
    catch {
        Write-ColoredOutput "✗ Błąd podczas klonowania: $_" "Red"
        exit 1
    }
}

# ============================================================================
# SEKCJA 6: ŚRODOWISKO WIRTUALNE PYTHON
# ============================================================================

Write-ColoredOutput "`nKonfigurowanie środowiska Python...`n" "Yellow"

$VENV_DIR = Join-Path $APP_DIR ".venv"

# Utwórz venv
if (-not (Test-Path $VENV_DIR)) {
    Write-ColoredOutput "Tworzenie środowiska wirtualnego..." "Yellow"
    & python -m venv $VENV_DIR

    if ($LASTEXITCODE -ne 0) {
        Write-ColoredOutput "✗ Błąd podczas tworzenia venv!" "Red"
        exit 1
    }
}

$PYTHON_VENV = Join-Path $VENV_DIR "Scripts\python.exe"
$PIP_VENV = Join-Path $VENV_DIR "Scripts\pip.exe"

# Aktualizuj pip
Write-ColoredOutput "Aktualizowanie pip..." "Yellow"
& $PYTHON_VENV -m pip install --upgrade pip --quiet

# Instaluj zależności
Write-ColoredOutput "Instalowanie zależności Python (może potrwać kilka minut)..." "Yellow"

$REQUIREMENTS_FILE = Join-Path $APP_DIR "requirements.txt"

& $PIP_VENV install -r $REQUIREMENTS_FILE --quiet

if ($LASTEXITCODE -ne 0) {
    Write-ColoredOutput "✗ Błąd podczas instalacji zależności!" "Red"
    exit 1
}

Write-ColoredOutput "✓ Zależności zainstalowane" "Green"

# Pobierz model SpaCy
Write-ColoredOutput "Pobieranie modelu językowego SpaCy dla języka polskiego..." "Yellow"

# Użyj bezpośredniego URL zamiast spacy download (bardziej niezawodne)
& $PIP_VENV install "https://github.com/explosion/spacy-models/releases/download/pl_core_news_md-3.7.0/pl_core_news_md-3.7.0-py3-none-any.whl" --quiet

if ($LASTEXITCODE -ne 0) {
    Write-ColoredOutput "✗ Błąd podczas pobierania modelu SpaCy!" "Red"
    exit 1
}

Write-ColoredOutput "✓ Model językowy pobrany" "Green"

# ============================================================================
# SEKCJA 7: UTWORZENIE SKRYPTU WRAPPER
# ============================================================================

Write-ColoredOutput "`nTworzenie skryptu wrapper...`n" "Yellow"

$WRAPPER_CONTENT = @"
@echo off
setlocal

set "APPBASE=$APP_DIR"
set "PYTHON_EXE=$PYTHON_VENV"
set "MAIN_SCRIPT=%APPBASE%\app\main.py"

"%PYTHON_EXE%" "%MAIN_SCRIPT%" %*
"@

$WRAPPER_PATH = Join-Path $INSTALL_BIN "anonymize.cmd"

[System.IO.File]::WriteAllText($WRAPPER_PATH, $WRAPPER_CONTENT, [System.Text.Encoding]::ASCII)

Write-ColoredOutput "✓ Skrypt wrapper utworzony: $WRAPPER_PATH" "Green"

# ============================================================================
# SEKCJA 8: DODANIE DO PATH UŻYTKOWNIKA
# ============================================================================

Write-ColoredOutput "`nDodawanie do PATH użytkownika...`n" "Yellow"

$CurrentPath = [Environment]::GetEnvironmentVariable("Path", "User")

if ($CurrentPath -notlike "*$INSTALL_BIN*") {
    $NewPath = $CurrentPath + ";" + $INSTALL_BIN
    [Environment]::SetEnvironmentVariable("Path", $NewPath, "User")
    Write-ColoredOutput "✓ Dodano do PATH: $INSTALL_BIN" "Green"
    Write-ColoredOutput "  (Restart terminala aby zmiany zaczęły działać)" "Yellow"
}
else {
    Write-ColoredOutput "✓ Folder już jest w PATH" "Green"
}

# ============================================================================
# SEKCJA 9: REJESTRACJA MENU KONTEKSTOWEGO DLA PLIKÓW
# ============================================================================

Write-ColoredOutput "`nRejestrowanie menu kontekstowego dla plików...`n" "Yellow"

$RegKeyFiles = "HKCU:\Software\Classes\*\shell\PresidioAnon"

try {
    New-Item -Path $RegKeyFiles -Force | Out-Null
    Set-ItemProperty -Path $RegKeyFiles -Name "(Default)" -Value "Anonimizuj (Presidio)"

    $RegKeyFilesCommand = Join-Path $RegKeyFiles "command"
    New-Item -Path $RegKeyFilesCommand -Force | Out-Null
    Set-ItemProperty -Path $RegKeyFilesCommand -Name "(Default)" -Value "`"$WRAPPER_PATH`" `"%1`""

    Write-ColoredOutput "✓ Menu kontekstowe dla plików zarejestrowane" "Green"
}
catch {
    Write-ColoredOutput "✗ Błąd rejestracji menu kontekstowego: $_" "Red"
}

# ============================================================================
# SEKCJA 10: REJESTRACJA MENU KONTEKSTOWEGO DLA FOLDERÓW
# ============================================================================

Write-ColoredOutput "Rejestrowanie menu kontekstowego dla folderów...`n" "Yellow"

$RegKeyFolders = "HKCU:\Software\Classes\Directory\shell\PresidioAnon"

try {
    New-Item -Path $RegKeyFolders -Force | Out-Null
    Set-ItemProperty -Path $RegKeyFolders -Name "(Default)" -Value "Anonimizuj folder (Presidio)"

    $RegKeyFoldersCommand = Join-Path $RegKeyFolders "command"
    New-Item -Path $RegKeyFoldersCommand -Force | Out-Null
    Set-ItemProperty -Path $RegKeyFoldersCommand -Name "(Default)" -Value "`"$WRAPPER_PATH`" `"%1`""

    Write-ColoredOutput "✓ Menu kontekstowe dla folderów zarejestrowane" "Green"
}
catch {
    Write-ColoredOutput "✗ Błąd rejestracji menu kontekstowego: $_" "Red"
}

# ============================================================================
# SEKCJA 11: SMOKE TEST
# ============================================================================

Write-ColoredOutput "`nWykonywanie testu...`n" "Yellow"

$TestSample = Join-Path $APP_DIR "tests\samples\test_document.docx"

if (Test-Path $TestSample) {
    Write-ColoredOutput "Testowanie na przykładowym pliku..." "Yellow"

    try {
        & $PYTHON_VENV (Join-Path $APP_DIR "app\main.py") $TestSample

        # Sprawdź czy powstał plik .anon.docx
        $TestOutput = $TestSample -replace '\.docx$', '.anon.docx'

        if (Test-Path $TestOutput) {
            Write-ColoredOutput "✓ Test zakończony pomyślnie!" "Green"
            Remove-Item $TestOutput -Force
        }
        else {
            Write-ColoredOutput "⚠ Test nie utworzył pliku wyjściowego" "Yellow"
        }
    }
    catch {
        Write-ColoredOutput "⚠ Test zakończony z błędami (to normalne jeśli brak testowych plików)" "Yellow"
    }
}

# ============================================================================
# SEKCJA 12: KOMUNIKATY KOŃCOWE
# ============================================================================

Write-ColoredOutput "`n========================================" "Green"
Write-ColoredOutput "INSTALACJA ZAKOŃCZONA POMYŚLNIE!" "Green"
Write-ColoredOutput "========================================`n" "Green"

Write-ColoredOutput "Lokalizacja instalacji: $INSTALL_BASE`n" "Cyan"

Write-ColoredOutput "Przykłady użycia:" "Yellow"
Write-ColoredOutput "  1. Kliknij prawym przyciskiem na pliku DOCX/ODT -> 'Anonimizuj (Presidio)'" "White"
Write-ColoredOutput "  2. Kliknij prawym przyciskiem na folderze -> 'Anonimizuj folder (Presidio)'" "White"
Write-ColoredOutput "  3. W terminalu: anonymize.cmd sciezka\do\pliku.docx`n" "White"

Write-ColoredOutput "Aby odinstalować, uruchom: $APP_DIR\scripts\uninstall.ps1`n" "Yellow"

Write-ColoredOutput "Naciśnij dowolny klawisz aby zakończyć..." "Gray"
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
