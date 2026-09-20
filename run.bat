@echo off
title Divinity Music Mod Manager
cd /d "%~dp0"

echo ====================================================
echo       Divinity Music Mod Manager (DOS:EE)
echo ====================================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.10 or higher from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

if not exist ".venv" (
    echo Creating virtual environment (.venv)...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

echo Checking and installing dependencies...
pip install -r requirements.txt

echo Starting Divinity Music Mod Manager...
python app.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application closed with an error.
    pause
)
