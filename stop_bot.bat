@echo off
REM Stop the bot using the stop helper script
SET SCRIPT_DIR=%~dp0
start "Stop USAFhelper Bot" powershell -NoProfile -ExecutionPolicy Bypass -NoExit -Command "& '%SCRIPT_DIR%stop_bot.ps1'"
