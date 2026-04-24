@echo off
setlocal

echo ========================================
echo   Amar Bangla Keyboard - Installer
echo ========================================
echo.

set "INSTALL_DIR=%PROGRAMFILES%\Amar Bangla Keyboard"

if exist "%INSTALL_DIR%" (
    echo Existing installation found.
    choice /C YN /M "Do you want to reinstall (overwrite)?"
    if errorlevel 2 goto :eof
)

echo Installing to %INSTALL_DIR%...
mkdir "%INSTALL_DIR%" 2>nul

copy /Y "dist\Amar Bangla Keyboard.exe" "%INSTALL_DIR%"
copy /Y "assets\amar_bangla_keyboard_logo.ico" "%INSTALL_DIR%"

echo.
echo Creating Desktop Shortcut...
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%USERPROFILE%\Desktop\Amar Bangla Keyboard.lnk'); $s.TargetPath = '%INSTALL_DIR%\Amar Bangla Keyboard.exe'; $s.WorkingDirectory = '%INSTALL_DIR%'; $s.Save()"

echo.
echo Creating Start Menu Shortcut...
mkdir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Amar Bangla Keyboard" 2>nul
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\Amar Bangla Keyboard.lnk'); $s.TargetPath = '%INSTALL_DIR%\Amar Bangla Keyboard.exe'; $s.WorkingDirectory = '%INSTALL_DIR%'; $s.Save()"

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo   Location: %INSTALL_DIR%
echo.
echo   Usage:
echo     1. Double-click shortcut or
echo     2. Run Amar Bangla Keyboard.exe
echo     3. Press Ctrl+Space to toggle Bengali
echo.
echo   Exit: Right-click tray icon ^> Quit
echo.

choice /C YN /M "Do you want to launch now?"
if errorlevel 1 start "" "%INSTALL_DIR%\Amar Bangla Keyboard.exe"

:end