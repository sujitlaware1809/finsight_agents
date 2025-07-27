@echo off
echo Starting FinSight AI Local Server...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if requirements are installed
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements_local.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo 🚀 Starting FinSight AI Local Development Server...
echo 📍 Server URL: http://localhost:8000
echo 📋 Demo Page: frontend_demo.html
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
python local_server.py

echo.
echo Server stopped.
pause
