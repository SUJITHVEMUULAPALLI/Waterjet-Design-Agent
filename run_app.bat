@echo off
echo ======================================
echo    WATERJET DESIGN AGENT LAUNCHER
echo ======================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Checking if in correct directory...
if not exist "app.py" (
    echo ERROR: Please run this script from the waterjet_design_agent directory
    pause
    exit /b 1
)

echo Checking dependencies...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Installing missing dependencies...
    pip install -r requirements.txt
)

echo Creating outputs directory if needed...
if not exist "data\outputs" mkdir "data\outputs"

echo Checking catalog...
python -c "import json; json.load(open('data/catalogue.json'))" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Catalog file is corrupted or missing
    pause
    exit /b 1
)

echo.
echo ======================================
echo   STARTING WATERJET DESIGN AGENT
echo ======================================
echo.
echo The app will open in your web browser at:
echo http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run app.py
