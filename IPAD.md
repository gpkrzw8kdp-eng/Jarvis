# Jarvis-HUD auf dem iPad (mit Sprache)

Das HUD läuft auf dem iPad im Browser, mit Mikrofon, Vorlesen und Freigabe-Karten.
Hermes bleibt dabei auf dem PC. Der PC muss an sein, und `start-jarvis.bat` muss laufen.

**Warum Tailscale?** Safari erlaubt Mikrofon und Spracherkennung nur über eine
verschlüsselte Verbindung (HTTPS). Tailscale verbindet iPad und PC über ein
privates Netz, liefert das HTTPS-Zertifikat automatisch und funktioniert auch
unterwegs im Mobilfunk. Nur deine eigenen Geräte kommen an den PC heran. Es ist
für den privaten Gebrauch kostenlos.

## Einmalige Einrichtung

### 1. Tailscale auf dem PC

1. <https://tailscale.com/download> öffnen, Tailscale für Windows installieren und
   mit einem Konto anmelden (Google, Microsoft, Apple oder GitHub).
2. Im Browser <https://login.tailscale.com/admin/dns> öffnen:
   - **MagicDNS** einschalten (falls nicht schon an).
   - Unter **HTTPS Certificates** auf **Enable HTTPS** klicken.

### 2. Tailscale auf dem iPad

App Store → **Tailscale** installieren → mit **demselben Konto** anmelden → VPN-Verbindung erlauben.

### 3. HUD über HTTPS freigeben (einmalig, am PC in PowerShell)

```powershell
tailscale serve --bg 8765
```

Tailscale zeigt dann die Adresse, unter der das HUD erreichbar ist, etwa
`https://dein-pc.tail1234.ts.net`. Die Einstellung bleibt auch nach einem
Neustart erhalten. Prüfen mit `tailscale serve status`, abschalten mit
`tailscale serve reset`.

Beim ersten Mal kann Tailscale einen Link anzeigen, über den du HTTPS im
Admin-Bereich bestätigen musst. Das ist Schritt 1, Punkt 2.

## Benutzen

1. Am PC muss laufen: `hermes gateway` (läuft meist schon als Aufgabe) und
   `start-jarvis.bat` (Fenster offen lassen).
2. Auf dem iPad in **Safari** die Adresse aus Schritt 3 öffnen.
3. Links im Panel **Hermes Agent** steht die Adresse schon richtig
   (`https://…/hermes`). Nur den `API_SERVER_KEY` eintragen und **Verbinden**.
4. **Mikro** antippen, Safari fragt einmal nach der Mikrofon-Erlaubnis, dann sprechen.
   Jarvis antwortet und liest die Antwort vor, wenn **Stimme** an ist.

**Tipp:** Über das Teilen-Symbol → **Zum Home-Bildschirm** wird das HUD zu einer
App ohne Browser-Leiste.

## Was du wissen solltest

- Die Spracherkennung läuft über Apples Diktierfunktion. Sie muss unter
  Einstellungen → Allgemein → Tastatur → **Diktieren** eingeschaltet sein.
  Apple verarbeitet die Aufnahme dabei auf seinen Servern.
- Das Vorlesen nutzt die deutsche Systemstimme des iPads. Unter Einstellungen →
  Bedienungshilfen → Gesprochene Inhalte → Stimmen kannst du eine bessere
  deutsche Stimme laden.
- Ohne Tailscale, nur über die WLAN-Adresse (`http://192.168…`), funktionieren
  Text und Freigaben, aber nicht das Mikrofon.
- Der `API_SERVER_KEY` wird nur im Safari auf dem iPad gespeichert. Mit
  **Trennen** im HUD wird er wieder gelöscht.

## Wenn es nicht klappt

| Problem | Lösung |
|---|---|
| Seite lädt nicht | Läuft `start-jarvis.bat` am PC? Sind PC und iPad in Tailscale verbunden (beide Geräte in der App sichtbar)? |
| „Fehler“ beim Verbinden | `hermes gateway status` am PC; Schlüssel prüfen |
| Mikro-Knopf fehlt | Die Adresse muss mit `https://` beginnen |
| Mikro geht, aber nichts wird erkannt | Diktieren in den iPad-Einstellungen einschalten, Internet nötig |
| Keine Sprachausgabe | Einmal irgendwo auf die Seite tippen (Safari verlangt eine Berührung), Stummschalter prüfen |
