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

REM Upgrade pip and install wheel
python -m pip install --upgrade pip
pip install wheel setuptools --upgrade

REM Install packages using binary wheels when possible
pip install Flask==2.0.1
pip install SQLAlchemy==1.4.46
pip install Flask-SQLAlchemy==2.5.1
pip install python-dotenv==0.19.0
pip install Werkzeug==2.0.1
pip install Flask-Login==0.5.0
pip install --only-binary :all: pillow==10.4.0

REM Run the application
echo Starting the application...
python app.py

pause
