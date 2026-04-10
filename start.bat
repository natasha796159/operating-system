@echo off
echo ==========================================
echo    OmniWatch - Process Dashboard
echo ==========================================
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
start "OmniWatch Backend" /MIN python backend\app.py

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
