# Skrypt deinstalacyjny dla Presidio Local Anonymizer
# Usuwa aplikację z systemu Windows

#Requires -Version 5.1

$ErrorActionPreference = "Stop"

# ============================================================================
# FUNKCJE POMOCNICZE
# ============================================================================

function Write-ColoredOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# ============================================================================
# SEKCJA 1: POTWIERDZENIE OD UŻYTKOWNIKA
# ============================================================================

Write-ColoredOutput "`n========================================" "Red"
Write-ColoredOutput "PRESIDIO LOCAL ANONYMIZER - DEINSTALACJA" "Red"
Write-ColoredOutput "========================================`n" "Red"

$INSTALL_BASE = Join-Path $env:LOCALAPPDATA "PresidioAnon"

Write-ColoredOutput "To działanie usunie następujące elementy:" "Yellow"
Write-ColoredOutput "  • Pliki aplikacji: $INSTALL_BASE" "White"
Write-ColoredOutput "  • Wpis w menu kontekstowym (prawy przycisk myszy)" "White"
Write-ColoredOutput "  • Wpis w PATH użytkownika`n" "White"

$Confirmation = Read-Host "Czy na pewno chcesz odinstalować? (tak/nie)"

if ($Confirmation -ne "tak") {
    Write-ColoredOutput "`nDeinstalacja anulowana." "Yellow"
    exit 0
}

Write-ColoredOutput "`nRozpoczynanie deinstalacji...`n" "Yellow"

# ============================================================================
# SEKCJA 2: USUNIĘCIE Z PATH
# ============================================================================

Write-ColoredOutput "Usuwanie z PATH użytkownika..." "Yellow"

try {
    $CurrentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    $INSTALL_BIN = Join-Path $INSTALL_BASE "bin"

    # Usuń wpis zawierający ścieżkę do PresidioAnon
    $PathParts = $CurrentPath -split ';' | Where-Object { $_ -notlike "*PresidioAnon*" }
    $NewPath = $PathParts -join ';'

    [Environment]::SetEnvironmentVariable("Path", $NewPath, "User")

    Write-ColoredOutput "✓ Usunięto z PATH" "Green"
}
catch {
    Write-ColoredOutput "✗ Błąd podczas usuwania z PATH: $_" "Red"
}

# ============================================================================
# SEKCJA 3: USUNIĘCIE Z REJESTRU (MENU KONTEKSTOWE)
# ============================================================================

Write-ColoredOutput "Usuwanie menu kontekstowego..." "Yellow"

# Menu dla plików
$RegKeyFiles = "HKCU:\Software\Classes\*\shell\PresidioAnon"

if (Test-Path $RegKeyFiles) {
    try {
        Remove-Item -Path $RegKeyFiles -Recurse -Force
        Write-ColoredOutput "✓ Usunięto menu kontekstowe dla plików" "Green"
    }
    catch {
        Write-ColoredOutput "✗ Błąd podczas usuwania menu dla plików: $_" "Red"
    }
}

# Menu dla folderów
$RegKeyFolders = "HKCU:\Software\Classes\Directory\shell\PresidioAnon"

if (Test-Path $RegKeyFolders) {
    try {
        Remove-Item -Path $RegKeyFolders -Recurse -Force
        Write-ColoredOutput "✓ Usunięto menu kontekstowe dla folderów" "Green"
    }
    catch {
        Write-ColoredOutput "✗ Błąd podczas usuwania menu dla folderów: $_" "Red"
    }
}

# ============================================================================
# SEKCJA 4: USUNIĘCIE PLIKÓW
# ============================================================================

Write-ColoredOutput "Usuwanie plików aplikacji..." "Yellow"

if (Test-Path $INSTALL_BASE) {
    try {
        # Zatrzymaj ewentualne procesy Python z tej instalacji
        $VenvPython = Join-Path $INSTALL_BASE "app\.venv\Scripts\python.exe"

        if (Test-Path $VenvPython) {
            Get-Process | Where-Object { $_.Path -eq $VenvPython } | Stop-Process -Force -ErrorAction SilentlyContinue
        }

        # Usuń folder
        Remove-Item -Path $INSTALL_BASE -Recurse -Force

        Write-ColoredOutput "✓ Pliki aplikacji usunięte" "Green"
    }
    catch {
        Write-ColoredOutput "✗ Błąd podczas usuwania plików: $_" "Red"
        Write-ColoredOutput "  Niektóre pliki mogą być zablokowane. Spróbuj ponownie po restarcie." "Yellow"
    }
}
else {
    Write-ColoredOutput "⚠ Folder instalacji nie istnieje" "Yellow"
}

# ============================================================================
# SEKCJA 5: KOMUNIKAT KOŃCOWY
# ============================================================================

Write-ColoredOutput "`n========================================" "Green"
Write-ColoredOutput "DEINSTALACJA ZAKOŃCZONA" "Green"
Write-ColoredOutput "========================================`n" "Green"

Write-ColoredOutput "Presidio Local Anonymizer został usunięty z systemu.`n" "White"
Write-ColoredOutput "Restart nie jest wymagany, ale może być potrzebny aby zaktualizować PATH w otwartych terminalach.`n" "Yellow"

Write-ColoredOutput "Naciśnij dowolny klawisz aby zakończyć..." "Gray"
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
