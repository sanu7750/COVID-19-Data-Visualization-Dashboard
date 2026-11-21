@echo off
title COVID-19 Jupyter Notebook Launcher
cd /d "%~dp0"

echo =========================================================
echo    Launching Jupyter Notebook for COVID-19 EDA
echo =========================================================
echo.

jupyter notebook notebooks/covid19_eda_and_analysis.ipynb

pause
