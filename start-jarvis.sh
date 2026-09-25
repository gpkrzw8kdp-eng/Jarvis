#!/usr/bin/env bash
# Startet das Jarvis-HUD lokal auf http://localhost:8765 (mit Weiterleitung /hermes -> Hermes-API-Server).
cd "$(dirname "$0")"

if ! curl -fs -o /dev/null http://127.0.0.1:8642/health; then
  echo "Hermes-API-Server nicht erreichbar. In ~/.hermes/.env API_SERVER_ENABLED=true und API_SERVER_KEY setzen,"
  echo "dann: hermes gateway restart   (das HUD startet trotzdem)"
fi

URL=http://localhost:8765/
(command -v xdg-open >/dev/null && xdg-open "$URL" || open "$URL") >/dev/null 2>&1 &
exec python3 serve.py
