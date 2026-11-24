@echo off
rem Saves the user's Civitai API key on this PC (my\.civitai-token). The agent opens this window for the user; the key
rem is typed here at a hidden prompt and never goes through the chat.
title Civitai key for Goon Studio
call "%~dp0py.cmd" "%~dp0..\tools\civitai.py" key
echo.
pause
