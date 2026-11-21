@echo off
title COVID-19 Data Pipeline Runner
cd /d "%~dp0"

echo =========================================================
echo    COVID-19 ETL, Analysis & Export Pipeline
echo =========================================================
echo.

python src\run_all.py

echo.
echo Pipeline execution finished. Press any key to exit.
pause >nul
