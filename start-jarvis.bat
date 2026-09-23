@echo off
rem Startet das Jarvis-HUD lokal auf http://localhost:8765 und bei Bedarf den Hermes-Gateway.
cd /d "%~dp0"

curl -s -o nul http://127.0.0.1:8642/health
if errorlevel 1 (
  echo Hermes-Gateway laeuft nicht - starte "hermes gateway" in neuem Fenster ...
  start "Hermes Gateway" cmd /k hermes gateway
  timeout /t 4 /nobreak >nul
)

start "" http://localhost:8765/index.html
where py >nul 2>nul && (py -m http.server 8765 --bind 127.0.0.1) || (python -m http.server 8765 --bind 127.0.0.1)
