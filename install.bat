@echo off
REM Laser Tag System Installation Script for Windows
REM This script sets up the Python environment

echo ==========================================
echo Laser Tag System Installation (Windows)
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

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%
echo.

REM Check for PostgreSQL
echo Checking for PostgreSQL...
psql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Warning: PostgreSQL not found in PATH.
    echo Please ensure PostgreSQL is installed.
    echo Download from: https://www.postgresql.org/download/windows/
    echo.
) else (
    for /f "tokens=3" %%i in ('psql --version') do set PSQL_VERSION=%%i
    echo Found PostgreSQL %PSQL_VERSION%
    echo.
)

REM Create virtual environment
echo Creating Python virtual environment...
if exist venv (
    echo Virtual environment already exists. Skipping creation.
) else (
    python -m venv venv
    echo Virtual environment created.
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install Python dependencies
echo Installing Python dependencies...
pip install psycopg2-binary pillow
echo Python dependencies installed.
echo.

REM Create requirements.txt
echo Creating requirements.txt...
(
echo psycopg2-binary>=2.9.0
echo pillow>=10.0.0
) > requirements.txt
echo requirements.txt created.
echo.

REM Create run script
echo Creating run.bat...
(
echo @echo off
echo call venv\Scripts\activate.bat
echo python main.py
echo pause
) > run.bat
echo run.bat created.
echo.

REM Check for logo.jpg
echo Checking for logo.jpg...
if not exist logo.jpg (
    echo Warning: logo.jpg not found in current directory.
    echo The application requires logo.jpg for the splash screen.
    echo Please add logo.jpg to the project directory before running.
    echo.
)

echo ==========================================
echo Installation Complete!
echo ==========================================
echo.
echo PostgreSQL Setup (Manual Steps Required):
echo 1. Open pgAdmin or psql command line
echo 2. Create database: CREATE DATABASE photon;
echo 3. Create user: CREATE USER student;
echo 4. Grant privileges: GRANT ALL PRIVILEGES ON DATABASE photon TO student;
echo 5. Connect to photon database and create table:
echo    CREATE TABLE players (
echo        id INTEGER PRIMARY KEY,
echo        codename VARCHAR(255) NOT NULL
echo    );
echo 6. Grant table privileges: GRANT ALL PRIVILEGES ON TABLE players TO student;
echo.
echo Next steps:
echo 1. Complete the PostgreSQL setup above
echo 2. Make sure logo.jpg is in the project directory
echo 3. Run the application with: run.bat
echo.
echo To start the UDP server (for testing):
echo    venv\Scripts\activate.bat
echo    python udpserver.py
echo.
pause