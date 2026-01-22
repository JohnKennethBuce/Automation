@echo off
:: ============================================================
:: StartHmopiTunnel.bat
:: This batch file runs the Python script as Administrator
:: Location: C:\1jap\Automation\StartHmopiTunnel.bat
:: ============================================================

:: Check for admin rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting Administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: Set title
title HMOPI ORS Tunnel Starter

:: Change to script directory
cd /d "C:\1jap\Automation"

:: Run the Python script
python AutoOpenHmopiorsTunnelorig.py

:: Pause if there's an error
if %errorLevel% neq 0 (
    echo.
    echo An error occurred. Press any key to exit...
    pause >nul
)