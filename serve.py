#!/usr/bin/env python3
"""Liefert das Jarvis-HUD aus und leitet /hermes/* an den lokalen Hermes-API-Server weiter.

Dadurch laufen HUD und Hermes unter derselben Adresse. Das braucht es, damit das HUD
auch von einem anderen Gerät (iPad, Handy) funktioniert, z. B. über Tailscale mit HTTPS.
Der Server lauscht nur auf 127.0.0.1 – nach außen kommt man nur über Tailscale.

Nur Python-Standardbibliothek, keine Installation nötig.
"""
import http.client
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HOST = "127.0.0.1"
PORT = int(os.environ.get("JARVIS_PORT", "8765"))
HERMES_HOST = os.environ.get("HERMES_HOST", "127.0.0.1")
HERMES_PORT = int(os.environ.get("HERMES_PORT", "8642"))
PREFIX = "/hermes"

# Header, die nicht 1:1 weitergereicht werden dürfen (Verbindungssteuerung).
HOP_BY_HOP = {"connection", "keep-alive", "transfer-encoding", "content-length",
              "proxy-authenticate", "proxy-authorization", "te", "trailers", "upgrade", "host"}


class Handler(SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.0"  # Verbindung schließt am Ende → Streams brauchen keine Content-Length

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=os.path.dirname(os.path.abspath(__file__)), **kw)

    def log_message(self, fmt, *args):  # nur Fehler und Proxy-Aufrufe loggen, keine Assets
        if self.path.startswith(PREFIX) or "40" in str(args[1:2]):
            sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    # ---- Proxy ------------------------------------------------------------
    def _is_proxy(self):
        return self.path == PREFIX or self.path.startswith(PREFIX + "/")

    def proxy(self):
        upstream_path = self.path[len(PREFIX):] or "/"
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else None
        headers = {k: v for k, v in self.headers.items() if k.lower() not in HOP_BY_HOP}
        headers["Host"] = f"{HERMES_HOST}:{HERMES_PORT}"
        headers["Connection"] = "close"
        try:
            conn = http.client.HTTPConnection(HERMES_HOST, HERMES_PORT, timeout=None)
            conn.request(self.command, upstream_path, body=body, headers=headers)
            resp = conn.getresponse()
        except OSError as exc:
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(('{"error": {"message": "Hermes nicht erreichbar (%s). Läuft hermes gateway?"}}'
                              % exc).encode())
            return
        self.send_response(resp.status, resp.reason)
        for k, v in resp.getheaders():
            if k.lower() not in HOP_BY_HOP and k.lower() != "content-encoding":
                self.send_header(k, v)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        try:
            # Zeilenweise durchreichen und sofort flushen → SSE-Events kommen live an.
            while True:
                line = resp.readline()
                if not line:
                    break
                self.wfile.write(line)
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass
        finally:
            conn.close()

    def do_GET(self):
        if self._is_proxy():
            return self.proxy()
        if self.path in ("/", ""):
            self.path = "/index.html"
        return super().do_GET()

    def do_POST(self):
        return self.proxy() if self._is_proxy() else self.send_error(405)

    def do_DELETE(self):
        return self.proxy() if self._is_proxy() else self.send_error(405)

    def do_OPTIONS(self):
        return self.proxy() if self._is_proxy() else self.send_error(405)

    def end_headers(self):
        # Kein Caching für das HUD selbst, damit Änderungen sofort ankommen.
        if not self._is_proxy():
            self.send_header("Cache-Control", "no-cache")
        super().end_headers()


def main():
    # Accept-Encoding nicht weiterreichen: wir wollen unkomprimierte Zeilen für SSE.
    class NoGzipHandler(Handler):
        def proxy(self):
            if "Accept-Encoding" in self.headers:
                del self.headers["Accept-Encoding"]
            return super().proxy()

    server = ThreadingHTTPServer((HOST, PORT), NoGzipHandler)
    server.daemon_threads = True
    print(f"Jarvis-HUD: http://localhost:{PORT}/   (Hermes-Proxy: /hermes -> {HERMES_HOST}:{HERMES_PORT})")
    print("Dieses Fenster offen lassen. Beenden mit Strg+C.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
