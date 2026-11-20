@echo off
rem Double-click to start the NSFW Studio.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0kit\start.ps1" %*
if errorlevel 1 pause
