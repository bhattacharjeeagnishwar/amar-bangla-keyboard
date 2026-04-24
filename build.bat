@echo off
echo Installing dependencies...
pip install -r requirements.txt
echo Building .exe with PyInstaller...
pyinstaller --onefile --windowed --name "Amar Bangla Keyboard" app.py
echo.
if exist "dist\Amar Bangla Keyboard.exe" (
    echo Build successful!
    echo File: dist\Amar Bangla Keyboard.exe
) else (
    echo Build failed!
)