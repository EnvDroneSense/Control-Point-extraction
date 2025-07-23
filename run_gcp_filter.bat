@echo off
REM Launcher script for GCP Filter application
REM This script starts the GCP Control Point Filter GUI

echo Starting GCP Control Point Filter...
echo.
echo Make sure you have:
echo - GCP data file (tab-delimited with CRS header)
echo - Control points file (tab-delimited with CRS header)
echo.

python gcp_filter.py

echo.
echo Application closed.
pause
