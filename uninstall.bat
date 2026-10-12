@echo off
setlocal EnableExtensions
title Amar Bangla Keyboard - Uninstall

REM ============================================================
REM  Amar Bangla Keyboard - uninstaller (per-user)
REM
REM  Usage:
REM    uninstall.bat           interactive uninstall
REM    uninstall.bat /quiet     silent uninstall (no prompts)
REM ============================================================

set "APPNAME=Amar Bangla Keyboard"
set "APPEXE=%APPNAME%.exe"
set "INSTALL_DIR=%LOCALAPPDATA%\%APPNAME%"
set "STARTMENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
set "DESKTOP=%USERPROFILE%\Desktop"
set "RUN_KEY=HKCU\Software\Microsoft\Windows\CurrentVersion\Run"
set "UNINSTALL_KEY=HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\AmarBanglaKeyboard"

set "QUIET=0"
if /I "%~1"=="/quiet" set "QUIET=1"
if /I "%~1"=="/y" set "QUIET=1"

echo ========================================
echo   %APPNAME% - Uninstall
echo ========================================
echo.

if "%QUIET%"=="0" (
    choice /C YN /M "Aapni ki sotti %APPNAME% uninstall korte chan"
    if errorlevel 2 goto :eof
)

echo [1/5] Cholti instance bondho kora hocche...
taskkill /IM "%APPEXE%" /F >nul 2>&1
ping -n 2 127.0.0.1 >nul

echo [2/5] Shortcut mucha hocche...

if exist "%DESKTOP%\%APPNAME%.lnk" del /Q "%DESKTOP%\%APPNAME%.lnk" >nul 2>&1
if exist "%STARTMENU%\%APPNAME%.lnk" del /Q "%STARTMENU%\%APPNAME%.lnk" >nul 2>&1
if exist "%STARTMENU%\%APPNAME%" rmdir /S /Q "%STARTMENU%\%APPNAME%" >nul 2>&1

echo [3/5] Auto-start entry mucha hocche...
reg delete "%RUN_KEY%" /v AmarBanglaKeyboard /f >nul 2>&1

echo [4/5] Add/Remove Programs entry mucha hocche...
reg delete "%UNINSTALL_KEY%" /f >nul 2>&1

echo [5/5] Application file mucha hocche...
del /Q "%INSTALL_DIR%\%APPEXE%" >nul 2>&1
del /Q "%INSTALL_DIR%\amar_bangla_keyboard_logo.ico" >nul 2>&1

REM Delete the install folder (including this script) shortly after we exit.
start "" /b powershell -NoProfile -Command "Start-Sleep -Milliseconds 1500; Remove-Item -LiteralPath '%INSTALL_DIR%' -Recurse -Force -ErrorAction SilentlyContinue" >nul 2>&1

echo.
echo   %APPNAME% uninstall hoye geche.
echo.

if "%QUIET%"=="0" pause
endlocal
