#!/usr/bin/env bash
# Startet das Jarvis-HUD lokal auf http://localhost:8765 und bei Bedarf den Hermes-Gateway.
cd "$(dirname "$0")"

if ! curl -fs -o /dev/null http://127.0.0.1:8642/health; then
  echo "Hermes-Gateway läuft nicht – starte 'hermes gateway' im Hintergrund (Log: hermes-gateway.log) …"
  nohup hermes gateway > hermes-gateway.log 2>&1 &
  sleep 4
fi

URL=http://localhost:8765/index.html
(command -v xdg-open >/dev/null && xdg-open "$URL" || open "$URL") >/dev/null 2>&1 &
python3 -m http.server 8765 --bind 127.0.0.1
