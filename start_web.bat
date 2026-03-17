@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
  echo Python not found in PATH.
  echo Install Python 3 from https://www.python.org/downloads/
  echo During install, enable "Add python.exe to PATH".
  pause
  exit /b 1
)

echo Starting local web server at http://localhost:8000/web_trainer.html
python -m http.server 8000
