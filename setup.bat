@echo off
REM CricketIQ Setup Script for Windows
REM This script automates the setup process for local development

setlocal enabledelayedexpansion

cls
echo ================================================
echo    CricketIQ - IPL Analytics Platform
echo    Setup Script v1.0 (Windows)
echo ================================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python version: %PYTHON_VERSION%
echo.

REM Create virtual environment
echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip >nul
pip install -r requirements.txt >nul
echo [OK] Dependencies installed
echo.

REM Create .env file
echo Configuring .env file...
(
    echo FLASK_APP=app.py
    echo FLASK_ENV=development
    echo FLASK_DEBUG=True
    echo.
    echo # MySQL Configuration
    echo MYSQL_HOST=localhost
    echo MYSQL_USER=root
    echo MYSQL_PASSWORD=
    echo MYSQL_PORT=3306
    echo MYSQL_DATABASE=cricketiq
    echo.
    echo # Flask Configuration
    echo SECRET_KEY=dev-secret-key-change-this
) > .env

echo [OK] .env file created
echo.

echo ================================================
echo [SUCCESS] Setup Complete!
echo ================================================
echo.
echo To start the application:
echo.
echo 1. Activate virtual environment:
echo    venv\Scripts\activate
echo.
echo 2. Create MySQL database (optional):
echo    - Open MySQL Command Line Client
echo    - Run: CREATE DATABASE cricketiq;
echo.
echo 3. Initialize database:
echo    python init_db.py
echo.
echo 4. Run the Flask app:
echo    python app.py
echo.
echo 5. Open your browser:
echo    http://localhost:5000
echo.
echo For help, see: README.md or QUICKSTART.md
echo.
pause
