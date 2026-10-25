@echo off
cd /d "%~dp0"
py --version >nul 2>&1
if errorlevel 1 (
  echo Install Python 3.10 or newer from https://www.python.org/downloads/
  pause
  exit /b 1
)
if not exist ".venv\Scripts\python.exe" py -m venv .venv
if errorlevel 1 goto error
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto error
.venv\Scripts\python.exe manage.py migrate
if errorlevel 1 goto error
.venv\Scripts\python.exe manage.py seed_demo
if errorlevel 1 goto error
.venv\Scripts\python.exe manage.py ensure_admin
if errorlevel 1 goto error
echo Open http://127.0.0.1:8000/ in your browser.
echo Admin site: http://127.0.0.1:8000/admin/
.venv\Scripts\python.exe manage.py runserver
pause
exit /b 0
:error
echo Setup failed. Send a screenshot of this window for help.
pause
exit /b 1
