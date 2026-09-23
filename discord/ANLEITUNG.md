# Jarvis über Discord (auch vom iPad)

Dein PC betreibt Hermes, und Discord ist die Fernbedienung. Du schreibst dem
Bot vom iPad oder Handy aus oder schickst ihm eine Sprachnachricht. Hermes
erledigt die Aufgabe auf deinem PC und antwortet in Discord.

Dafür gelten zwei Bedingungen: Der PC muss eingeschaltet sein, und
`hermes gateway` muss laufen. Das ist derselbe Prozess, den `start-jarvis.bat`
startet. Er bedient HUD und Discord gleichzeitig.

Grundlage ist die offizielle Anleitung:
<https://hermes-agent.nousresearch.com/docs/user-guide/messaging/discord>

---

## Teil A – Bot bei Discord anlegen (geht komplett in Safari auf dem iPad)

1. Öffne <https://discord.com/developers/applications> und melde dich an.
2. **New Application**, Name z. B. `Jarvis`, AGB bestätigen, **Create**.
3. Links auf **Bot**:
   - Optional: Profilbild setzen.
   - Unter **Privileged Gateway Intents** diese beiden einschalten:
     **Server Members Intent** und **Message Content Intent**.
     Das ist der wichtigste Schritt: Ohne *Message Content* sieht der Bot
     deine Nachrichten nicht.
   - **Save Changes**.
4. Noch auf der Seite **Bot**: **Reset Token**, dann den Token kopieren und
   sicher aufbewahren (z. B. im Passwort-Manager). Discord zeigt ihn nur
   einmal an. Wer den Token hat, steuert deinen Bot und damit deinen PC.
5. Links auf **Installation**:
   - **Guild Install** aktivieren. Install Link: **Discord Provided Link**.
   - Scopes: `bot` und `applications.commands`.
   - Permissions: *View Channels, Send Messages, Embed Links, Attach Files,
     Read Message History, Send Messages in Threads, Add Reactions*.
   - Den Link öffnen und den Bot in **deinen eigenen** Server einladen.
     Leg dir notfalls einen privaten Server an: „+“ in der Discord-App.

## Teil B – Deine Discord-Benutzer-ID herausfinden

Nur diese ID darf später mit Jarvis sprechen.

- **iPad/iPhone-App:** Profilbild → Einstellungen (Zahnrad) → **Erweitert** →
  **Entwicklermodus** einschalten. Dann auf deinen Namen tippen → **•••** →
  **Benutzer-ID kopieren**.
- **PC:** Einstellungen → Erweitert → Entwicklermodus. Dann Rechtsklick auf
  deinen Namen → *Benutzer-ID kopieren*.

Die ID ist eine lange Zahl, z. B. `284102345871466496`.

## Teil C – Hermes auf dem PC einrichten

Das geht nur am PC. Hermes muss schon installiert sein (siehe `README.md`).

1. Einrichtungsassistent starten:

   ```bash
   hermes gateway setup
   ```

   **Discord** wählen und dann Bot-Token und Benutzer-ID einfügen.

   Alternativ trägst du es von Hand in `~/.hermes/.env` ein
   (unter Windows `%USERPROFILE%\.hermes\.env`):

   ```bash
   DISCORD_BOT_TOKEN=dein-bot-token
   DISCORD_ALLOWED_USERS=deine-benutzer-id
   ```

   Lass `DISCORD_ALLOWED_USERS` **nie** weg, und setze nie
   `DISCORD_ALLOW_ALL_USERS=true`. Sonst könnte jeder, der den Bot erreicht,
   Befehle auf deinem PC auslösen.

2. **Jarvis-Persönlichkeit** (optional, empfohlen): Kopiere `discord/SOUL.md`
   aus diesem Projekt nach `~/.hermes/SOUL.md`. Sichere vorher die vorhandene
   Datei, denn sie wird ersetzt:

   ```powershell
   # Windows (PowerShell, im Jarvis-Ordner)
   Copy-Item $HOME\.hermes\SOUL.md $HOME\.hermes\SOUL.backup.md -ErrorAction SilentlyContinue
   Copy-Item .\discord\SOUL.md $HOME\.hermes\SOUL.md
   ```

   ```bash
   # Linux / macOS
   cp ~/.hermes/SOUL.md ~/.hermes/SOUL.backup.md 2>/dev/null; cp discord/SOUL.md ~/.hermes/SOUL.md
   ```

   Die Persönlichkeit gilt dann überall: in Discord, im HUD und im Terminal.

3. Gateway starten, entweder mit `hermes gateway` oder mit `start-jarvis.bat`.
   Nach ein paar Sekunden ist der Bot in Discord online.

## Teil D – Benutzen

- **Direktnachricht (empfohlen):** In Discord auf den Bot tippen → **Nachricht**.
  In Direktnachrichten antwortet er auf alles, ohne @-Erwähnung.
- **Im Server-Kanal:** Dort antwortet er nur mit `@Jarvis …`. Soll er in
  einem Kanal auf alles antworten, trag in `.env` Folgendes ein:
  `DISCORD_FREE_RESPONSE_CHANNELS=<Kanal-ID>`
- **Freigaben:** Bei riskanten Befehlen schickt Jarvis eine Nachricht mit
  Knöpfen. Du tippst auf dem iPad auf „Erlauben“ oder „Ablehnen“.
- Beispiele: „Wie voll ist meine Festplatte?“, „Lade die neueste
  Rechnung aus meinem Download-Ordner hoch und fasse sie zusammen“,
  „Starte Spotify“.

## Teil E – Sprechen statt tippen

In der Discord-App auf dem iPad hältst du in der Direktnachricht das
**Mikrofon** gedrückt und sprichst.

- Damit Hermes Sprachnachrichten versteht, braucht er Spracherkennung. Am
  einfachsten ist das kostenlose, lokale `faster-whisper`. Laut Hermes-Doku
  installierst du die Sprach- und Messaging-Extras so:

  ```bash
  cd ~/.hermes/hermes-agent && uv pip install -e ".[voice,messaging]"
  ```

  Mit dem Hermes-Desktop-Installer unter Windows ist das eventuell schon
  dabei. Probier zuerst eine Sprachnachricht.
- Damit Jarvis auch **laut antwortet**, schreibst du ihm einmal einen dieser
  Befehle:
  - `/voice on` – er antwortet gesprochen, wenn du gesprochen hast
  - `/voice tts` – er antwortet immer auch als Sprachnachricht
  - `/voice off` – nur Text

  Die Standard-Stimme (Edge TTS) braucht keinen API-Schlüssel.

## Wenn es nicht klappt

| Problem | Lösung |
|---|---|
| Bot ist offline | Läuft `hermes gateway` auf dem PC? Ist der PC an und nicht im Ruhezustand? |
| Bot ist online, antwortet aber nicht | **Message Content Intent** im Developer Portal einschalten (Teil A, Schritt 3) |
| „Nicht autorisiert“ oder keine Reaktion in der Direktnachricht | Stimmt die ID in `DISCORD_ALLOWED_USERS`? |
| Sprachnachricht wird nicht verstanden | Extras installieren (Teil E) und Gateway neu starten |
| Token versehentlich geteilt | Im Developer Portal sofort **Reset Token**, neuen Token eintragen |
