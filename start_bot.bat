@echo off
REM Start the bot in a new PowerShell window using the project's helper script
SET SCRIPT_DIR=%~dp0
start "USAFhelper Bot" powershell -NoProfile -ExecutionPolicy Bypass -NoExit -Command "& '%SCRIPT_DIR%run_bot.ps1'"
