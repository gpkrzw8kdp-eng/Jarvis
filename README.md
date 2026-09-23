# J.A.R.V.I.S. HUD

Ein animiertes Iron-Man-HUD als einzelne HTML-Datei (`index.html`). Über den
[Hermes Agent](https://hermes-agent.nousresearch.com/docs/) von Nous Research
redest du mit Jarvis, und er erledigt Dinge auf deinem PC: Terminal-Befehle,
Dateien, Browser, Websuche.

## Was das HUD kann

- Arc-Reaktor mit rotierenden Ringen und rotem Scanner-Bogen
- Echte Werte: Uhr, Datum, Monatsleiste, Sonnenauf- und -untergang (Berlin), Browser-Speicher, Akku (falls verfügbar)
- Simuliert: CPU, RAM, Netzwerk. Das Wetter sind Beispieldaten.
- Jarvis-Konsole mit Texteingabe, **Mikrofon** (Spracherkennung, Deutsch) und **Stimme** (Vorlesen)
- **Hermes Agent**: Fragen und Aufträge gehen an deinen lokalen Hermes. Du siehst live, welche
  Werkzeuge er benutzt. Riskante Befehle erscheinen als rote **Freigabe-Karte**, auf der du
  *Einmal erlauben*, *Für diese Sitzung*, *Immer erlauben* oder *Ablehnen* wählst.
  Mit **Stopp** brichst du eine laufende Aufgabe ab.
- Eingebaute Befehle ohne Hermes: `hilfe`, `status`, `zeit`, `datum`, `alarm`, `normal`, `vollbild`, `leeren`

## Einrichtung (einmalig)

### 1. Hermes installieren

Windows (PowerShell):

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

Linux / macOS / WSL2:

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

Danach ein Modell bzw. einen Anbieter wählen und einmal im Terminal testen:

```bash
hermes setup      # oder: hermes model
hermes            # kurzer Test-Chat, dann beenden
```

### 2. API-Server von Hermes einschalten

Diese Zeilen in `~/.hermes/.env` eintragen (unter Windows `%USERPROFILE%\.hermes\.env`).
Denk dir einen eigenen, langen Schlüssel aus:

```bash
API_SERVER_ENABLED=true
API_SERVER_KEY=hier-einen-langen-geheimen-schluessel-eintragen
API_SERVER_CORS_ORIGINS=http://localhost:8765,http://127.0.0.1:8765
```

`API_SERVER_CORS_ORIGINS` erlaubt dem HUD im Browser, mit Hermes zu sprechen.
Der Server bleibt standardmäßig nur auf deinem PC erreichbar (`127.0.0.1:8642`).

### 3. Starten

- **Windows:** Doppelklick auf `start-jarvis.bat`
- **Linux/macOS:** `./start-jarvis.sh`

Das Skript startet `hermes gateway`, falls er noch nicht läuft, liefert das HUD
unter <http://localhost:8765> aus und öffnet den Browser. Voraussetzung ist Python 3.

Im HUD links im Panel **Hermes Agent** den `API_SERVER_KEY` eintragen und auf
**Verbinden** klicken. Der Schlüssel wird nur in diesem Browser gespeichert.
**Trennen** löscht ihn wieder.

## Vom iPad oder Handy: Jarvis über Discord

Hermes kann zusätzlich ein Discord-Bot sein. Dann schreibst du Jarvis vom
iPad aus oder schickst ihm Sprachnachrichten, und er arbeitet auf deinem PC.
Die Schritt-für-Schritt-Anleitung steht in [`discord/ANLEITUNG.md`](discord/ANLEITUNG.md).
Eine passende Jarvis-Persönlichkeit für Hermes liegt in [`discord/SOUL.md`](discord/SOUL.md).

## Sprechen

Klick auf **Mikro**, sprich deinen Auftrag, und Jarvis antwortet laut. Das
funktioniert in Chrome und Edge. Der Browser fragt beim ersten Mal nach der
Mikrofon-Erlaubnis. Chrome schickt die Spracherkennung dabei an Google-Server.
Mit **Stimme** liest Jarvis auch Antworten auf getippte Fragen vor.

## Sicherheit

Hermes kann über diese Verbindung **echte Befehle auf deinem PC ausführen**.

- Gib den `API_SERVER_KEY` niemandem weiter. Lass `API_SERVER_HOST` auf `127.0.0.1`.
- Hermes prüft gefährliche Befehle selbst (`approvals.mode: smart` ist voreingestellt).
  Was es nicht selbst entscheidet, landet als Freigabe-Karte im HUD.
- Wähle „Immer erlauben“ nur für Befehle, bei denen du dir sicher bist.
- Über `approvals.deny` in `~/.hermes/config.yaml` sperrst du bestimmte Befehle dauerhaft.

## Warum nicht im claude.ai-Artifact?

In der veröffentlichten claude.ai-Vorschau darf die Seite keine Verbindung zu
deinem PC aufbauen, der Browser blockiert das. Dort antwortet Jarvis
stattdessen über Claude, kann aber nichts auf deinem PC tun. Für Hermes nimm
die lokale Version über `start-jarvis`.
