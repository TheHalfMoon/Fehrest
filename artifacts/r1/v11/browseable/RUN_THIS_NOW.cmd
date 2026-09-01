@echo off
setlocal
title FEHREST R1-X1 Replacement Pilot V9
echo ============================================================
echo LAUNCHER_STARTED=YES
echo FEHREST_R1_X1_REPLACEMENT_EXECUTOR_VERSION=9
echo ============================================================
echo.
cd /d "%~dp0"
echo PACKAGE_DIR=%CD%
echo.
if not exist "replacement.ps1" (
  echo FAIL_CLOSED: replacement.ps1 missing
  echo.
  pause
  exit /b 1
)
if not exist "supervisor.py" (
  echo FAIL_CLOSED: supervisor.py missing
  echo.
  pause
  exit /b 1
)
echo SIDECAR_FILES=PASS
echo STARTING_POWERSHELL=YES
echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0replacement.ps1"
set "RC=%ERRORLEVEL%"
echo.
echo ============================================================
echo POWERSHELL_EXIT_CODE=%RC%
echo ============================================================
echo.
if not "%RC%"=="0" (
  echo The launcher failed. The window will remain open.
  echo Upload FEHREST-R1-X1-REPLACEMENT-LAUNCHER.txt from Desktop.
) else (
  echo Replacement executor finished.
  echo Upload FEHREST-R1-X1-REPLACEMENT-PILOT-RESULT.txt from Desktop.
)
echo.
pause
exit /b %RC%
