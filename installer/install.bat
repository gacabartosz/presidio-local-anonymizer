@echo off
REM One-liner installer dla Presidio Local Anonymizer
REM Pobiera i uruchamia skrypt instalacyjny z GitHub

powershell -NoProfile -ExecutionPolicy Bypass -Command "& {Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/gacabartosz/presidio-local-anonymizer/main/scripts/install.ps1' -OutFile '%TEMP%\presidio_install.ps1'; & '%TEMP%\presidio_install.ps1'; Remove-Item '%TEMP%\presidio_install.ps1' -Force}"

pause
