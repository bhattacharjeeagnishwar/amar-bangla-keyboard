@echo off
setlocal EnableExtensions
title Amar Bangla Keyboard - Setup

REM ============================================================
REM  Amar Bangla Keyboard - per-user installer (no admin needed)
REM
REM  Usage:
REM    install.bat                 interactive install
REM    install.bat /autostart      also start with Windows
REM    install.bat /quiet          silent install, no prompts
REM ============================================================

set "HERE=%~dp0"
set "APPNAME=Amar Bangla Keyboard"
set "APPVERSION=1.1.1"
set "APPEXE=%APPNAME%.exe"
set "INSTALL_DIR=%LOCALAPPDATA%\%APPNAME%"
set "SRC_EXE=%HERE%dist\%APPEXE%"
set "SRC_ICO=%HERE%assets\amar_bangla_keyboard_logo.ico"
set "STARTMENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
set "DESKTOP=%USERPROFILE%\Desktop"
set "RUN_KEY=HKCU\Software\Microsoft\Windows\CurrentVersion\Run"
set "UNINSTALL_KEY=HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\AmarBanglaKeyboard"

set "QUIET=0"
set "AUTOSTART="
set "NOLAUNCH=0"

:parse_args
if "%~1"=="" goto :args_done
if /I "%~1"=="/quiet" set "QUIET=1"
if /I "%~1"=="/silent" set "QUIET=1"
if /I "%~1"=="/y" set "QUIET=1"
if /I "%~1"=="/autostart" set "AUTOSTART=1"
if /I "%~1"=="/noautostart" set "AUTOSTART=0"
if /I "%~1"=="/nolaunch" set "NOLAUNCH=1"
shift
goto :parse_args
:args_done

echo ========================================
echo   %APPNAME% v%APPVERSION% - Setup
echo ========================================
echo.

if not exist "%SRC_EXE%" (
    echo [ERROR] Build not found:
    echo         "%SRC_EXE%"
    echo.
    echo         Run "build.bat" first to build the exe, then run this setup.
    echo.
    if "%QUIET%"=="0" pause
    exit /b 1
)

if exist "%INSTALL_DIR%\%APPEXE%" (
    if "%QUIET%"=="0" (
        choice /C YN /M "Existing installation found - install again (overwrite)?"
        if errorlevel 2 goto :eof
    )
)

echo [1/5] Stopping any running instance...
taskkill /IM "%APPEXE%" /F >nul 2>&1

echo [2/5] Copying files to: "%INSTALL_DIR%"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
copy /Y "%SRC_EXE%" "%INSTALL_DIR%\%APPEXE%" >nul
if exist "%SRC_ICO%" copy /Y "%SRC_ICO%" "%INSTALL_DIR%\" >nul
if exist "%HERE%uninstall.bat" copy /Y "%HERE%uninstall.bat" "%INSTALL_DIR%\uninstall.bat" >nul

if not exist "%INSTALL_DIR%\%APPEXE%" (
    echo [ERROR] Copy failed. Close the app and try again.
    echo.
    if "%QUIET%"=="0" pause
    exit /b 1
)

echo [3/5] Creating shortcuts (Desktop + Start Menu)...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ws=New-Object -ComObject WScript.Shell; $s=$ws.CreateShortcut('%DESKTOP%\%APPNAME%.lnk'); $s.TargetPath='%INSTALL_DIR%\%APPEXE%'; $s.WorkingDirectory='%INSTALL_DIR%'; $s.IconLocation='%INSTALL_DIR%\%APPEXE%,0'; $s.Description='%APPNAME%'; $s.Save()" >nul 2>&1
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ws=New-Object -ComObject WScript.Shell; $s=$ws.CreateShortcut('%STARTMENU%\%APPNAME%.lnk'); $s.TargetPath='%INSTALL_DIR%\%APPEXE%'; $s.WorkingDirectory='%INSTALL_DIR%'; $s.IconLocation='%INSTALL_DIR%\%APPEXE%,0'; $s.Description='%APPNAME%'; $s.Save()" >nul 2>&1

echo [4/5] Setting up auto-start with Windows...
if "%AUTOSTART%"=="" (
    if "%QUIET%"=="0" (
        choice /C YN /M "Start %APPNAME% automatically when Windows starts"
        if errorlevel 2 (set "AUTOSTART=0") else (set "AUTOSTART=1")
    )
)
if "%AUTOSTART%"=="1" reg add "%RUN_KEY%" /v AmarBanglaKeyboard /t REG_SZ /d "\"%INSTALL_DIR%\%APPEXE%\"" /f >nul
if "%AUTOSTART%"=="0" reg delete "%RUN_KEY%" /v AmarBanglaKeyboard /f >nul 2>&1

echo [5/5] Registering with Windows Uninstall (Add/Remove Programs)...
reg add "%UNINSTALL_KEY%" /v DisplayName /t REG_SZ /d "%APPNAME%" /f >nul
reg add "%UNINSTALL_KEY%" /v DisplayVersion /t REG_SZ /d "%APPVERSION%" /f >nul
reg add "%UNINSTALL_KEY%" /v Publisher /t REG_SZ /d "Amar Bangla" /f >nul
reg add "%UNINSTALL_KEY%" /v DisplayIcon /t REG_SZ /d "%INSTALL_DIR%\%APPEXE%" /f >nul
reg add "%UNINSTALL_KEY%" /v InstallLocation /t REG_SZ /d "%INSTALL_DIR%" /f >nul
reg add "%UNINSTALL_KEY%" /v UninstallString /t REG_SZ /d "\"%INSTALL_DIR%\uninstall.bat\"" /f >nul
reg add "%UNINSTALL_KEY%" /v QuietUninstallString /t REG_SZ /d "\"%INSTALL_DIR%\uninstall.bat\" /quiet" /f >nul
reg add "%UNINSTALL_KEY%" /v NoModify /t REG_DWORD /d 1 /f >nul
reg add "%UNINSTALL_KEY%" /v NoRepair /t REG_DWORD /d 1 /f >nul
reg add "%UNINSTALL_KEY%" /v EstimatedSize /t REG_DWORD /d 16200 /f >nul

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo   Location : %INSTALL_DIR%
echo   Shortcut : Desktop + Start Menu
echo.
echo   Usage:
echo     1. Double-click the shortcut (or run %APPEXE%)
echo     2. Press Ctrl+Space to turn Bengali on/off
echo.
echo   Uninstall: Windows Settings ^> Apps, or
echo              "%INSTALL_DIR%\uninstall.bat"
echo.

if "%NOLAUNCH%"=="1" goto :done
if "%QUIET%"=="1" goto :done

choice /C YN /M "Start %APPNAME% now"
if errorlevel 2 goto :done
start "" "%INSTALL_DIR%\%APPEXE%"

:done
if "%QUIET%"=="0" pause
endlocal
