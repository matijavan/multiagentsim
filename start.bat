@echo off
echo Starting Dispatch Sim (backend + frontend)...

REM --- Backend: create the venv and install dependencies if missing ---
if not exist "%~dp0backend\.venv\Scripts\uvicorn.exe" (
    echo Backend .venv not found - setting it up for the first time...
    python -m venv "%~dp0backend\.venv"
    "%~dp0backend\.venv\Scripts\pip.exe" install -r "%~dp0backend\requirements.txt"
)

REM --- Frontend: install node_modules if missing ---
if not exist "%~dp0frontend\node_modules" (
    echo Frontend node_modules not found - running npm install for the first time...
    call npm install --prefix "%~dp0frontend"
)

start "Dispatch Sim - Backend" /D "%~dp0backend" cmd /k ".venv\Scripts\uvicorn.exe app.main:app --reload --port 8000"
start "Dispatch Sim - Frontend" /D "%~dp0frontend" cmd /k "npm run dev"

timeout /t 3 /nobreak >nul
start http://localhost:5173
