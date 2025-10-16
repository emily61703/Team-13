@echo off
REM Simple installation script for Laser Tag System (Windows)

echo ==========================================
echo Laser Tag System - Simple Installation
echo ==========================================
echo.

REM Check for Python
echo Checking for Python 3...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python 3 is not installed or not in PATH.
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)
echo Python found.
echo.

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv venv
echo Virtual environment created.
echo.

REM Activate virtual environment and install packages
echo Installing Python packages...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install psycopg2-binary pillow
echo Python packages installed.
echo.

echo ==========================================
echo Installation Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Install PostgreSQL from: https://www.postgresql.org/download/windows/
echo.
echo 2. Setup the database (open pgAdmin or psql):
echo    CREATE DATABASE photon;
echo    CREATE USER student WITH PASSWORD 'your_password';
echo    GRANT ALL PRIVILEGES ON DATABASE photon TO student;
echo    \c photon
echo    CREATE TABLE players (id INTEGER PRIMARY KEY, codename VARCHAR(255) NOT NULL);
echo    GRANT ALL PRIVILEGES ON TABLE players TO student;
echo.
echo 3. Add logo.jpg to the project directory
echo.
echo 4. Run the application:
echo    venv\Scripts\activate.bat
echo    python main.py
echo.
pause