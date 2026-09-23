@echo off
rem Startet das Jarvis-HUD lokal auf http://localhost:8765.
cd /d "%~dp0"

curl -s -o nul http://127.0.0.1:8642/health
if errorlevel 1 (
  echo.
  echo  Hermes-API-Server nicht erreichbar.
  echo  1. In %LOCALAPPDATA%\hermes\.env muessen API_SERVER_ENABLED, API_SERVER_KEY und API_SERVER_CORS_ORIGINS stehen.
  echo  2. Danach: hermes gateway restart
  echo  Das HUD startet trotzdem, Hermes kannst du spaeter verbinden.
  echo.
)

set "PY=%LOCALAPPDATA%\hermes\hermes-agent\venv\Scripts\python.exe"
if not exist "%PY%" (
  where py >nul 2>nul && (set "PY=py") || (set "PY=python")
)

start "" http://localhost:8765/index.html
echo  Jarvis-HUD laeuft auf http://localhost:8765 - dieses Fenster offen lassen.
"%PY%" -m http.server 8765 --bind 127.0.0.1
