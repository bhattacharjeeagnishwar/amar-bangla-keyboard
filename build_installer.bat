@echo off
setlocal EnableExtensions
set "HERE=%~dp0"

echo ========================================
echo   Amar Bangla Keyboard - Installer Build
echo ========================================
echo.

REM --- 1. Make sure the app exe exists -------------------------
if not exist "%HERE%dist\Amar Bangla Keyboard.exe" (
    echo [ERROR] App exe paoa gelo na:
    echo         "%HERE%dist\Amar Bangla Keyboard.exe"
    echo         Prothome build.bat chaliye exe build korun.
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
    echo [ERROR] Inno Setup 6 paoa gelo na.
    echo.
    echo         Install korun:
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
    echo [ERROR] Compile fail korlo.
    pause
    exit /b 1
)

echo.
echo Setup file toiri hoye geche:
echo   "%HERE%installer\AmarBanglaKeyboard-Setup-1.1.0.exe"
echo.
pause
endlocal
