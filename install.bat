@echo off
echo Starting setup and running application...

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not installed! Please install Python first.
    pause
    exit /b 1
)

REM Remove existing virtual environment if exists
if exist venv (
    echo Removing existing virtual environment...
    rmdir /s /q venv
)

REM Create fresh virtual environment
echo Creating new virtual environment...
python -m venv venv

REM Activate and install requirements
echo Installing requirements...
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Run the application
echo Starting the application...
python app.py

pause