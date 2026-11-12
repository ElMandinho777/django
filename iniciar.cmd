@echo off
cd /d "%~dp0"
if not exist venv\Scripts\python.exe python -m venv venv
venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto fin
venv\Scripts\python.exe manage.py migrate
if errorlevel 1 goto fin
echo Abre http://127.0.0.1:8002/swagger/
venv\Scripts\python.exe manage.py runserver 127.0.0.1:8002 --insecure
:fin
pause
