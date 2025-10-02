#!/usr/bin/env python3
"""
TrustEye Online Server
Simple HTTP server to run TrustEye online
"""
import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

class TrustEyeHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent), **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.path = '/trusteye_dashboard.html'
        super().do_GET()

def start_server():
    PORT = 8080
    
    print("🚀 Starting TrustEye Online Server...")
    print(f"📱 Local Access: http://localhost:{PORT}")
    print(f"🌐 Network Access: http://0.0.0.0:{PORT}")
    print("✨ TrustEye is now running online!")
    print("📊 Features: Scanner + Dashboard + Analytics")
    print("\n🔥 Press Ctrl+C to stop server")
    
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), TrustEyeHandler) as httpd:
            # Auto-open browser
            webbrowser.open(f'http://localhost:{PORT}')
            
            print(f"\n✅ Server running on port {PORT}")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 TrustEye server stopped!")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    start_server()
