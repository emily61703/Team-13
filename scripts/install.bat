@echo off
REM Laser Tag System Installation (Windows)

cd /d "%~dp0\.."

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python 3 not found. Install from python.org
    pause
    exit /b 1
)

python -m venv venv
call venv\Scripts\activate.bat
python -m pip install -q --upgrade pip
pip install -q psycopg2-binary pillow
pip install -q pygame

echo Installation complete. Run with: venv\Scripts\activate.bat ^&^& python main.py
pause