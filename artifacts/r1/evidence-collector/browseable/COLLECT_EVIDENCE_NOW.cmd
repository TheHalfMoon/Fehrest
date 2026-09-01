@echo off
setlocal
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0collect-r1-evidence.ps1"
set "RC=%ERRORLEVEL%"
echo.
if not "%RC%"=="0" echo Evidence collection failed with exit code %RC%.
if "%RC%"=="0" echo Evidence collection completed.
echo.
pause
exit /b %RC%
