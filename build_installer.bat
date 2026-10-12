@echo off
setlocal EnableExtensions
set "HERE=%~dp0"

echo ========================================
echo   Amar Bangla Keyboard - Installer Build
echo ========================================
echo.

REM --- 1. Make sure the app exe exists -------------------------
if not exist "%HERE%dist\Amar Bangla Keyboard.exe" (
    echo [ERROR] App exe not found:
    echo         "%HERE%dist\Amar Bangla Keyboard.exe"
    echo         Run build.bat first to build the exe.
    echo.
    pause
    exit /b 1
)

REM --- 2. Locate the Inno Setup compiler (ISCC.exe) ------------
set "ISCC="
for %%P in (
    "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
    "%ProgramFiles%\Inno Setup 6\ISCC.exe"
    "%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe"
) do if exist "%%~P" set "ISCC=%%~P"

if not defined ISCC for /f "delims=" %%I in ('where ISCC.exe 2^>nul') do set "ISCC=%%I"

if not defined ISCC (
    echo [ERROR] Inno Setup 6 not found.
    echo.
    echo         Install it with:
    echo           winget install -e --id JRSoftware.InnoSetup
    echo         Or: https://jrsoftware.org/isdl.php
    echo.
    pause
    exit /b 1
)

REM --- 3. Compile ---------------------------------------------
echo Using compiler: %ISCC%
echo Compiling installer.iss ...
echo.
"%ISCC%" "%HERE%installer.iss"
if errorlevel 1 (
    echo.
    echo [ERROR] Compile failed.
    pause
    exit /b 1
)

echo.
echo Setup file created:
echo   "%HERE%installer\AmarBanglaKeyboard-Setup-1.1.1.exe"
echo.
pause
endlocal
