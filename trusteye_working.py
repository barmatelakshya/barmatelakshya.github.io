#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import os

PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/trusteye_dashboard.html'
        return super().do_GET()

print(f"🚀 Starting TrustEye on http://localhost:{PORT}")

try:
    os.chdir('/Users/barmate_lakshya/Documents/SIH_PS1')
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        webbrowser.open(f'http://localhost:{PORT}')
        print(f"✅ Server running on port {PORT}")
        httpd.serve_forever()
except Exception as e:
    print(f"❌ Error: {e}")
