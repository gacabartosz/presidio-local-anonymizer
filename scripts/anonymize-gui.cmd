@echo off
REM Launcher dla GUI Presidio Anonymizer

setlocal

set "APPBASE=%~dp0.."
set "PYTHON_EXE=%APPBASE%\.venv\Scripts\python.exe"
set "GUI_SCRIPT=%APPBASE%\app\gui.py"

"%PYTHON_EXE%" "%GUI_SCRIPT%"
