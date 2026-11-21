@echo off
title COVID-19 Analytics Dashboard Launcher
cd /d "%~dp0"

echo =========================================================
echo    COVID-19 Data Visualization - Streamlit Dashboard
echo =========================================================
echo.

:: Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found in PATH!
    echo Please install Python from https://www.python.org/ and check "Add Python to PATH".
    pause
    exit /b
)

:: Step 1: Install required libraries if needed
echo [1/3] Checking dependencies...
pip install -r requirements.txt

:: Step 2: Ensure data is extracted and cleaned
echo.
echo [2/3] Verifying and updating COVID-19 datasets...
if not exist "data\processed\covid_19_cleaned_timeseries.csv" (
    python src\run_all.py
)

:: Step 3: Launch Streamlit Dashboard
echo.
echo [3/3] Launching Interactive COVID-19 Dashboard in your browser...
echo.
echo Dashboard URL: http://localhost:8501
echo (Press Ctrl+C in this terminal when you want to stop the dashboard server)
echo.

streamlit run dashboard\app.py

pause
