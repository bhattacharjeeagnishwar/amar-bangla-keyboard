@echo off
echo Installing dependencies...
pip install -r requirements.txt
echo Building .exe with PyInstaller (using the spec file)...
pyinstaller --noconfirm --clean "Amar Bangla Keyboard.spec"
echo.
if exist "dist\Amar Bangla Keyboard.exe" (
    echo Build successful!
    echo File: dist\Amar Bangla Keyboard.exe
) else (
    echo Build failed!
)
