@echo off
setlocal enabledelayedexpansion

echo =============================================
echo 🚀 Installing dependencies...
echo =============================================

:: Kiểm tra Python đã được cài đặt hay chưa
python --version > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Python is not installed or not in PATH! Please install Python first.
    pause
    exit /b 1
)

:: Xóa môi trường ảo nếu đã tồn tại
if exist venv (
    echo 🔧 Removing existing virtual environment...
    rmdir /s /q venv
)

:: Tạo môi trường ảo mới
echo 🔧 Creating new virtual environment...
python -m venv venv

:: Kích hoạt môi trường ảo
call venv\Scripts\activate

:: Cập nhật pip, wheel và setuptools
echo 🔧 Upgrading pip, wheel, and setuptools...
python -m pip install --upgrade pip wheel setuptools

:: Cài đặt các gói từ requirements.txt
if exist requirements.txt (
    echo 🔧 Installing dependencies from requirements.txt...
    pip install -r requirements.txt
    if %ERRORLEVEL% neq 0 (
        echo ❌ Installation failed! Trying alternative method...
        pip install --no-cache-dir -r requirements.txt
        if %ERRORLEVEL% neq 0 (
            echo ❌ Installation failed! Please check the error messages above.
            pause
            exit /b 1
        )
    )
) else (
    echo ❌ No requirements.txt found! Please add it to the project folder.
    pause
    exit /b 1
)

:: Hoàn thành cài đặt
echo =============================================
echo ✅ Installation completed successfully!
echo =============================================

:: Chạy ứng dụng
echo 🚀 Starting server...
python app.py

pause
