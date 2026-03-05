@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM MotoExhaust local host launcher
REM Usage: start_motoexhaust.bat [port]

cd /d "%~dp0"
set "PORT=%~1"
if "%PORT%"=="" set "PORT=8000"

echo.
echo ==============================================
echo MotoExhaust Local Host Launcher
echo ==============================================

echo [1/3] Checking Python...
set "PY_CMD="
where py >nul 2>nul
if %errorlevel%==0 (
  set "PY_CMD=py -3"
) else (
  where python >nul 2>nul
  if %errorlevel%==0 set "PY_CMD=python"
)

if "%PY_CMD%"=="" (
  echo ERROR: Python was not found in PATH.
  echo Install Python 3 and ensure "python" or "py" works in Command Prompt.
  pause
  exit /b 1
)

if not exist "scripts\refresh_data.py" (
  echo ERROR: scripts\refresh_data.py not found.
  echo Make sure this .bat file is in the MotoExhaust project root folder.
  pause
  exit /b 1
)

echo Using: %PY_CMD%

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
echo [2/3] Refreshing dataset files...
call %PY_CMD% scripts\refresh_data.py
if errorlevel 1 (
  echo.
  echo ERROR: Data refresh failed.
  pause
  exit /b 1
)

echo.
echo [3/3] Starting local web server...
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
