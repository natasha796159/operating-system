@echo off
cd /d "%~dp0"
echo ==========================================
echo    IntelliSys - Process Dashboard
echo ==========================================

IF NOT EXIST "backend\requirements.txt" (
    echo.
    echo ==========================================
    echo [CRITICAL ERROR] The "backend" folder is missing! 
    echo ==========================================
    echo.
    echo If you moved or copied out 'start.bat' to your Desktop, it will NOT work.
    echo It must remain completely inside the folder with the rest of the code!
    echo.
    echo Solution:
    echo 1. Move this file back into the OSOMNI project folder.
    echo 2. If you want it on your Desktop, Right-Click start.bat -^> Create Shortcut, then move the shortcut.
    echo.
    pause
    exit /b 1
)

echo This script will install dependencies, start the backend, and open the dashboard.

echo.
echo [1/3] Installing/verifying dependencies...
python -m pip install -r backend\requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies. Please ensure Python is installed and added to PATH.
    pause
    exit /b 1
)

echo.
echo [2/3] Starting Backend Server...
:: Start the flask app in a separate minimized window
start "IntelliSys Backend" /MIN python backend\app.py

echo.
echo [3/3] Opening Dashboard...
:: Wait 2 seconds for Flask to boot
timeout /t 2 /nobreak >nul
start http://127.0.0.1:5000

echo.
echo Dashboard is now running! 
echo Keep the new minimized console window open to maintain the backend.
echo You can close this window now.
pause
