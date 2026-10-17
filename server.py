import http.server
import socketserver

PORT = 8080

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Servidor del Portal Cautivo corriendo en http://localhost:{PORT}")
    print("Presiona Ctrl+C para detenerlo.")
    httpd.serve_forever()