@echo off
cd /d "%~dp0"
"venv\Scripts\python.exe" configurar.py
if errorlevel 1 pause
