@echo off
title Generate PowerPoint Presentation (.pptx)
cd /d "%~dp0"

echo =========================================================
echo    COVID-19 Analytics - PowerPoint Presentation Builder
echo =========================================================
echo.

:: Check python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found in PATH!
    pause
    exit /b
)

:: Step 1: Install python-pptx if needed
echo [1/2] Checking dependencies...
python -c "import pptx" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing python-pptx...
    pip install python-pptx
)

:: Step 2: Generate PowerPoint presentation
echo.
echo [2/2] Generating COVID19_Data_Visualization_Presentation.pptx...
python src\generate_pptx.py

echo.
echo =========================================================
echo Presentation generated in: outputs\COVID19_Data_Visualization_Presentation.pptx
echo Also check out the interactive web presentation at: presentation\index.html
echo =========================================================
echo.
pause
