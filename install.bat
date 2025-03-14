@echo off
echo Starting installation...

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Node.js is not installed! Please install Node.js first.
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
npm install

echo Installation complete!
pause