@echo off
setlocal
cd /d "%~dp0"
set PYTHON_MANAGER_AUTOMATIC_INSTALL=false
if exist ".venv\Scripts\python.exe" goto :verify
echo A procurar Python 3.11...
call py -3.11 -m venv .venv
if exist ".venv\Scripts\python.exe" goto :verify
echo A procurar Python 3.12...
call py -3.12 -m venv .venv
if exist ".venv\Scripts\python.exe" goto :verify
echo A procurar Python 3.10...
call py -3.10 -m venv .venv
if exist ".venv\Scripts\python.exe" goto :verify
echo.
echo Nao foi encontrado Python 3.10, 3.11 ou 3.12.
echo No terminal, executa: py install 3.11
echo Depois volta a abrir este instalador.
echo Se o comando nao existir, instala Python 3.11 em python.org.
pause
exit /b 1
:verify
".venv\Scripts\python.exe" -c "import sys; sys.exit(0 if (3,10) <= sys.version_info[:2] < (3,13) else 1)"
if errorlevel 1 (
  echo O ambiente .venv existente nao tem uma versao Python compativel.
  echo Renomeia essa pasta para .venv_anterior e volta a tentar.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" -m pip --version
if errorlevel 1 goto :failed
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto :failed
".venv\Scripts\python.exe" -m pip install "torch>=2.6,<3" --index-url https://download.pytorch.org/whl/cpu
if errorlevel 1 goto :failed
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :failed
echo Instalacao terminada. Abre start_windows.bat para iniciar.
pause
exit /b 0
:failed
echo A instalacao falhou. Guarda a mensagem acima para diagnostico.
pause
exit /b 1
