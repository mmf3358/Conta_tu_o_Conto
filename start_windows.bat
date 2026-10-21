@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Primeiro segue a instalacao no README.md.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" -m streamlit run app.py
pause
