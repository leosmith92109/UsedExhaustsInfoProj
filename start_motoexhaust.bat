@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM MotoExhaust portable launcher
REM Usage: start_motoexhaust.bat [port]

cd /d "%~dp0"
set "PORT=%~1"
if "%PORT%"=="" set "PORT=8000"

echo.
echo ==============================================
echo MotoExhaust Local Host Launcher
echo ==============================================

if not exist "scripts\refresh_data.py" (
  echo ERROR: scripts\refresh_data.py not found.
  echo Make sure this .bat file is in the MotoExhaust project root folder.
  pause
  exit /b 1
)

echo [1/5] Ensuring Python is installed...
call :ensure_python
if errorlevel 1 (
  echo.
  echo ERROR: Python setup failed.
  pause
  exit /b 1
)

echo Using: %PY_CMD%

echo.
echo [2/5] Ensuring pip and Python dependencies...
call :ensure_pip
if errorlevel 1 (
  echo.
  echo ERROR: pip setup failed.
  pause
  exit /b 1
)

if exist "requirements.txt" (
  call %PY_CMD% -m pip install --disable-pip-version-check -r requirements.txt
  if errorlevel 1 (
    echo.
    echo ERROR: Failed to install requirements from requirements.txt
    pause
    exit /b 1
  )
) else (
  echo No requirements.txt found. Skipping pip installs.
)

REM Check if port is already in use
for /f "tokens=5" %%P in ('netstat -ano -p tcp ^| findstr /R /C:":%PORT% .*LISTENING"') do (
  echo ERROR: Port %PORT% is already in use by PID %%P.
  echo Close that process or run with a different port, e.g.:
  echo   start_motoexhaust.bat 8080
  pause
  exit /b 1
)

REM Try to ensure firewall allows inbound TCP on this port.
REM If not elevated, this section will fail silently and we print guidance.
set "FW_OK=0"
net session >nul 2>nul
if %errorlevel%==0 (
  netsh advfirewall firewall delete rule name="MotoExhaust HTTP %PORT%" >nul 2>nul
  netsh advfirewall firewall add rule name="MotoExhaust HTTP %PORT%" dir=in action=allow protocol=TCP localport=%PORT% profile=any >nul 2>nul
  if %errorlevel%==0 set "FW_OK=1"
)

echo.
echo [3/5] Refreshing dataset files...
call %PY_CMD% scripts\refresh_data.py
if errorlevel 1 (
  echo.
  echo ERROR: Data refresh failed.
  pause
  exit /b 1
)

echo.
echo [4/5] Resolving LAN IP for mobile devices...
set "LAN_IP="
for /f "tokens=2 delims=:" %%I in ('ipconfig ^| findstr /R /C:"IPv4 Address" /C:"IPv4 Address."') do (
  set "cand=%%I"
  set "cand=!cand: =!"
  if not "!cand!"=="127.0.0.1" if /I not "!cand:~0,8!"=="169.254." if /I not "!cand:~0,7!"=="172.23." (
    set "LAN_IP=!cand!"
    goto :ip_found
  )
)
:ip_found
if "%LAN_IP%"=="" set "LAN_IP=<your-local-ip>"

echo.
echo [5/5] Starting local web server...
echo.
echo Open on this computer:
echo   http://localhost:%PORT%/
echo.
echo Open from another device on same network:
echo   http://%LAN_IP%:%PORT%/
echo.
if "%FW_OK%"=="1" (
  echo Firewall rule applied: MotoExhaust HTTP %PORT%
) else (
  echo NOTE: Firewall rule was not auto-applied.
  echo If phone cannot connect, run this script once as Administrator.
)
echo.
echo Press Ctrl+C to stop the server.
echo.

start "" "http://localhost:%PORT%/"
call %PY_CMD% -m http.server %PORT% --bind 0.0.0.0

endlocal
exit /b 0

:detect_python
set "PY_CMD="
where py >nul 2>nul
if %errorlevel%==0 (
  set "PY_CMD=py -3"
  exit /b 0
)
where python >nul 2>nul
if %errorlevel%==0 (
  set "PY_CMD=python"
  exit /b 0
)
for /f "delims=" %%D in ('dir "%LocalAppData%\Programs\Python" /b /ad /o-n 2^>nul') do (
  if exist "%LocalAppData%\Programs\Python\%%D\python.exe" (
    set "PY_CMD=\"%LocalAppData%\Programs\Python\%%D\python.exe\""
    exit /b 0
  )
)
exit /b 1

:ensure_python
call :detect_python
if defined PY_CMD exit /b 0

echo Python not found. Attempting auto-install...

where winget >nul 2>nul
if %errorlevel%==0 (
  echo Attempting install via winget...
  winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements --silent
  call :detect_python
  if defined PY_CMD exit /b 0
)

echo Winget path failed or unavailable. Downloading Python installer...
set "PY_URL=https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe"
set "PY_EXE=%TEMP%\python-3.12.10-amd64.exe"

powershell -NoProfile -ExecutionPolicy Bypass -Command "try { Invoke-WebRequest -UseBasicParsing -Uri '%PY_URL%' -OutFile '%PY_EXE%' } catch { exit 1 }"
if errorlevel 1 (
  echo ERROR: Failed to download Python installer.
  echo Install Python 3 manually from https://www.python.org/downloads/windows/
  exit /b 1
)

echo Running Python installer (quiet mode)...
"%PY_EXE%" /quiet InstallAllUsers=0 PrependPath=1 Include_pip=1 Include_launcher=1 Shortcuts=0
if errorlevel 1 (
  echo ERROR: Python installer failed.
  exit /b 1
)

call :detect_python
if defined PY_CMD exit /b 0

echo ERROR: Python install completed but executable was not detected.
exit /b 1

:ensure_pip
call %PY_CMD% -m pip --version >nul 2>nul
if %errorlevel%==0 exit /b 0

call %PY_CMD% -m ensurepip --upgrade >nul 2>nul
call %PY_CMD% -m pip --version >nul 2>nul
if %errorlevel%==0 exit /b 0

echo ERROR: pip could not be initialized.
exit /b 1
