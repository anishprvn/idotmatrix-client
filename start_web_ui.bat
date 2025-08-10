@echo off
REM iDotMatrix Web UI Launcher for Windows
REM This script starts the web-based user interface for controlling iDotMatrix displays

echo 🚀 Starting iDotMatrix Web Controller...

REM Get the directory where this script is located
cd /d "%~dp0"

REM Check if virtual environment exists
if exist "my-venv" (
    echo 📦 Activating virtual environment...
    call my-venv\Scripts\activate.bat
)

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3 and try again
    pause
    exit /b 1
)

REM Start the web server
echo 🌐 Starting web server...
python web_server.py %*

pause